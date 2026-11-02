"""Connection manager and apply engine.

The apply order, handshake and frame payloads follow analysis/OVERVIEW.md
section 6/7 and the shipped executable's disassembly.  All writes go through
:class:`sm809.transport.HidTransport`, so the same code path runs against real
hardware and against the demo transport used by the tests.
"""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass, field
from typing import Callable

from .config import DeviceConfig
from .model import DataStore, Profile
from .protocol import (
    CMD_SETTLE,
    HANDSHAKE_EXPECTED,
    HANDSHAKE_PLAIN,
    MACRO_CHUNK_DELAY,
    PacketError,
    build_button_slots,
    build_dpi_block,
    button_frames,
    checksum,
    commit_frame,
    deobfuscate,
    dpi_header,
    fixed_color_frame,
    frame,
    handshake_reply_ok,
    high_dpi_frame,
    light_frame,
    lod_frame,
    macro_blocks,
    mode_frame,
    obfuscate,
    palette_block,
    palette_header,
    rate_frame,
    stage_frame,
    status_frame,
    table_budget_warnings,
    validate_buttons,
)
from .transport import HidTransport
from .winspi import PointerSettings


_log = logging.getLogger("sm809.device")
# Library-style default: stay silent (and avoid logging's lastResort stderr
# output) until app.logging_setup installs real handlers.
if not logging.getLogger("sm809").handlers:
    logging.getLogger("sm809").addHandler(logging.NullHandler())


class DeviceError(RuntimeError):
    pass


@dataclass
class ApplyResult:
    ok: bool
    warnings: list[str] = field(default_factory=list)
    windows_changes: list[str] = field(default_factory=list)
    sent_packets: int = 0
    sent_blocks: int = 0
    changed_sections: list[str] = field(default_factory=list)
    version: tuple[int, int] | None = None
    error: str = ""


@dataclass
class DeviceStatus:
    present: bool = False
    linked: bool = False
    version: tuple[int, int] = (0, 0)
    last_error: str = ""


class DeviceService:
    """Owns the HID link, the handshake and the apply sequence.

    Callbacks run on the monitor thread; a tkinter UI should marshal them with
    ``after`` rather than touching widgets directly.
    """

    def __init__(
        self,
        config: DeviceConfig,
        store: DataStore | None = None,
        *,
        demo: bool = False,
        transport: HidTransport | None = None,
        pace: float | None = None,
        settle: float | None = None,
    ):
        self.config = config
        self.store = store
        self.transport = transport or HidTransport(config, demo=demo)
        self.demo = demo or self.transport.demo
        self.pointer = PointerSettings()
        self.linked = False
        self.version: tuple[int, int] = (config.ver_h, config.ver_l)
        self.last_error = ""
        self._busy = threading.Lock()
        self.pace = (0.0 if self.demo else 0.02) if pace is None else pace
        # Mandatory settle window after every feature write (the firmware can
        # wedge without it).  Demo mode never sleeps so tests stay fast.
        self.cmd_settle = (0.0 if self.demo else CMD_SETTLE) if settle is None else settle
        self.macro_chunk_delay = 0.0 if self.demo else MACRO_CHUNK_DELAY
        # Wire payload of every section last written to THIS device.  Applies
        # diff against it, so switching a profile only sends what changed.
        self._applied: dict[str, object] = {}
        # Which section is being written right now; included in failure logs so
        # a wedged write points at the command that caused it.
        self._phase = "idle"
        self._written: list[str] = []
        # Mode reports arrive asynchronously from the monitor interface.  The
        # 0x02 write records which layer was just requested so an echo that
        # still describes the layer being left cannot flip the UI back.
        self._mode_expected: int | None = None
        self._mode_expected_at = 0.0

        self.on_device_event: Callable[[int, int], None] | None = None
        self.on_profile_changed: Callable[[str], None] | None = None
        self.on_disconnect: Callable[[], None] | None = None
        self.on_log: Callable[[str], None] | None = None

        self.transport.on_event = self._handle_event
        self.transport.on_disconnect = self._transport_lost

    # -- diagnostics -------------------------------------------------------
    def log(self, text: str, level: int = logging.INFO) -> None:
        """Record a diagnostic line; optional callback for embedders/tests."""
        _log.log(level, "%s", text)
        if self.on_log:
            try:
                self.on_log(text)
            except Exception:
                pass

    def _sleep(self, seconds: float) -> None:
        if seconds > 0:
            time.sleep(seconds)

    # -- connection --------------------------------------------------------
    @property
    def status(self) -> DeviceStatus:
        return DeviceStatus(
            present=self.present(),
            linked=self.linked,
            version=self.version,
            last_error=self.last_error,
        )

    def present(self) -> bool:
        if self.demo:
            return True
        return bool(self.transport.enumerate())

    def connect(self) -> bool:
        """Open the device, run the link handshake and the status frames."""
        with self._busy:
            if self.linked:
                return True
            # A fresh link means the device state is unknown: force the next
            # apply to write every section.
            self._applied.clear()
            if not self.transport.open():
                self.linked = False
                self.last_error = "SM809 not found (VID 04D9 / PID A09F)"
                _log.debug("HID open failed: %s", self.last_error)
                return False
            _log.debug("HID link opened (VID %04X / PID %04X)", self.config.vid, self.config.pid)
            try:
                ok = self.handshake()
                if ok:
                    self.status_frames()
                    # The shipped build only queries the firmware version when
                    # Data.ini Update != 0; otherwise it trusts Ver_H/Ver_L.
                    if self.config.update:
                        self.read_version()
                    else:
                        self.version = (self.config.ver_h, self.config.ver_l)
                    self.linked = True
                    self.last_error = ""
                    self.log("device linked")
                else:
                    self.last_error = "link handshake rejected"
                    self.log(self.last_error, logging.WARNING)
                    self.transport.close()
                    self.linked = False
                return ok
            except Exception as exc:  # pragma: no cover - hardware path
                self.last_error = f"connect failed: {exc}"
                self.transport.close()
                self.linked = False
                _log.exception("connect failed")
                return False

    def disconnect(self) -> None:
        self.transport.close()
        self.linked = False
        self._applied.clear()

    def _transport_lost(self) -> None:
        self.linked = False
        self._applied.clear()
        self.log("device disconnected")
        if self.on_disconnect:
            try:
                self.on_disconnect()
            except Exception:
                pass

    def ensure(self) -> bool:
        """Reconnect on demand (used by Apply when the link has dropped)."""
        if self.linked and self.transport.connected:
            return True
        return self.connect()

    # -- raw frames --------------------------------------------------------
    def _plain(self, packet: bytes) -> bytes:
        return obfuscate(packet, self.config.key) if self.config.has_password else packet

    def send_feature(self, packet: bytes, *, obfuscated: bool = False,
                     pace: float | None = None) -> bool:
        """Send an 8-byte feature packet (checksum already present)."""
        wire = packet if obfuscated else self._plain(packet)
        ok = self.transport.set_feature(wire)
        self._sleep(self.cmd_settle if pace is None else pace)
        if not ok:
            # The payload is what makes a failure actionable: it identifies the
            # command byte (e.g. 0x0D lighting) that the firmware rejected.
            raise DeviceError(f"SetFeature failed for frame {wire.hex(' ')}")
        _log.debug("feature frame %s", wire.hex(" "))
        return True

    def read_feature(self) -> bytes:
        reply = self.transport.get_feature()
        if reply and self.config.has_password:
            try:
                return deobfuscate(reply[:8], self.config.key)
            except Exception:
                return b""
        return reply

    def send_block(self, block: bytes, *, pace: float | None = None) -> None:
        if len(block) != 32:
            raise ValueError(f"block must be 32 bytes, got {len(block)}")
        if not self.transport.write_block(block):
            raise DeviceError(
                "WriteUSB failed for block "
                f"{block[:8].hex(' ')} ... ({block[-4:].hex(' ')})")
        _log.debug("block %s", block.hex(" "))
        self._sleep(self.pace if pace is None else pace)

    # -- handshake / status ------------------------------------------------
    def handshake(self) -> bool:
        """FUN_0041bbc0: plain packet, then the same bytes obfuscated."""
        plain = HANDSHAKE_PLAIN
        self.send_feature(plain, obfuscated=True, pace=max(self.cmd_settle, 0.03))
        self.transport.get_feature()  # first reply is ignored
        self._sleep(0.03)
        encoded = obfuscate(plain, self.config.key)
        self.send_feature(encoded, obfuscated=True, pace=max(self.cmd_settle, 0.03))
        reply = self.transport.get_feature()
        self._sleep(0.03)
        # FUN_0041bbc0 only accepts a reply that decrypts to the magic; the
        # raw GetFeature buffer is never compared, so a static/echoed report
        # cannot pass by accident.
        ok = handshake_reply_ok(reply, self.config.key)
        if not ok:
            _log.warning("handshake reply did not decrypt to AA DD 3B 62 "
                         "(reply=%s)", reply.hex(" ") if reply else "(empty)")
        return ok

    def status_frames(self) -> None:
        """FUN_004196b0: 0x83, a status read, then the 0x03 status set.

        The 0x8B value is only the *buffer* passed to GetFeature; MSDriver's
        GetFeature ignores its input buffer, so nothing is transmitted for it.
        """
        self.send_feature(frame(0x83))
        self.read_feature()  # reply intentionally discarded
        profile = self.store.profile if self.store else Profile()
        self.send_feature(status_frame(profile))

    def read_version(self) -> tuple[int, int] | None:
        """FUN_0041b850: query firmware version; returns (ver_h, ver_l)."""
        try:
            self.send_feature(frame(0x80, (0,)), pace=max(self.cmd_settle, 0.03))
            self._sleep(0.03)
            self.send_feature(frame(0x80, (0,)), pace=max(self.cmd_settle, 0.03))
            reply = self.transport.get_feature()
            self._sleep(0.03)
            if len(reply) < 8:
                return None
            if self.config.has_password:
                reply = deobfuscate(reply[:8], self.config.key)
            # Some firmware revisions answer every GetFeature with the
            # handshake status report.  That is not a version, so keep the
            # configured Ver_H/Ver_L instead of displaying 170.221.
            if reply[1:5] == HANDSHAKE_EXPECTED[1:5]:
                self.log("version query returned the status report; "
                         "keeping the configured firmware version")
                return None
            self.version = (reply[1], reply[2])
            _log.debug("firmware version %d.%d", self.version[0], self.version[1])
            return self.version
        except Exception as exc:
            _log.warning("version query failed: %s", exc)
            return None

    def version_matches(self) -> bool:
        return self.version == (self.config.ver_h, self.config.ver_l)

    # -- apply -------------------------------------------------------------
    def apply(
        self,
        profile: Profile | None = None,
        *,
        apply_windows: bool = True,
        persist: bool = True,
        allow_offline: bool = True,
    ) -> ApplyResult:
        """Send the complete profile.

        ``profile`` is committed into the store first when supplied, matching
        the original's copy of the working profile into the selected record.
        """
        if self.store is None:
            raise ValueError("apply requires a DataStore")
        result = ApplyResult(ok=False)
        if profile is not None and profile is not self.store.profile:
            self.store.profile.raw[:] = profile.raw
            profile = self.store.profile
        prof = self.store.profile

        if not validate_buttons(prof):
            result.warnings.append(
                "No button is mapped to Left Click or Send Gun; "
                "the original application refuses this profile."
            )

        if apply_windows:
            try:
                result.windows_changes = self.pointer.apply(
                    prof.speed, prof.scroll, prof.double,
                    bool(prof.enhance), bool(prof.onepage),
                )
            except Exception as exc:  # pragma: no cover - platform call
                result.warnings.append(f"Windows pointer settings failed: {exc}")

        if not self.ensure():
            msg = self.last_error or "device not connected"
            if not allow_offline:
                result.error = msg
                result.ok = False
                return result
            result.warnings.append(f"Not connected: {msg}. Profile saved locally.")
            result.ok = True
            if persist:
                self._persist()
            return result

        before_packets = len(self.transport.sent_packets)
        before_blocks = len(self.transport.sent_blocks)
        try:
            with self._busy:
                self._apply_sequence(prof, result)
        except (DeviceError, PacketError, ValueError) as exc:
            # A partial write leaves the device in an unknown state; force the
            # next apply to resend every section.
            self._applied.clear()
            result.error = str(exc)
            result.ok = False
            written = ", ".join(self._written) or "nothing"
            self.log(
                f"apply failed in '{self._phase}' after writing {written}: {exc}",
                logging.ERROR,
            )
            _log.debug("apply failure details", exc_info=True)
            return result

        result.sent_packets = len(self.transport.sent_packets) - before_packets
        result.sent_blocks = len(self.transport.sent_blocks) - before_blocks
        result.version = self.version
        if persist:
            self._persist()
        result.ok = not result.error
        return result

    def _apply_sequence(self, prof: Profile, result: ApplyResult) -> None:
        """Write only the profile sections that differ from the last apply.

        The device is stateful, so the wire bytes we sent last are a reliable
        description of what it currently holds.  Building every section first
        (and comparing bytes) makes a profile switch that only changes DPI or
        lighting send just those packets instead of the whole profile.  The
        cache is cleared on connect/disconnect and after a failed write, when
        the hardware state is unknown.
        """
        self._written = []
        self._phase = "build"
        # Build the complete set of section payloads up front.  A macro that
        # cannot be encoded (too many events or bytes) is replaced by an empty
        # table inside macro_blocks, so one bad binding never aborts the write.
        mode_pkt = mode_frame(prof)
        rate_pkt = rate_frame(prof)
        stage_pkt = stage_frame(prof)
        color_pkt = fixed_color_frame(prof)
        light_pkt = light_frame(prof)
        palette = (palette_header(0), palette_block(prof.cycle_colors),
                   palette_header(1), palette_block(prof.stage_colors))
        dpi = (dpi_header(prof), build_dpi_block(prof, self.config.sensor))
        slots, _macro_counter, gun_count = build_button_slots(prof, self.config)
        # Full 0x12 table in the log: when a binding "doesn't work", this shows
        # exactly which firmware slot received it (Office = 0-15, Game = 32-47).
        for block_no in range(4):
            _log.debug("button table %d/4: %s", block_no + 1,
                       slots[block_no * 64:(block_no + 1) * 64].hex(" "))
        buttons = tuple(button_frames(slots))
        macros = tuple(macro_blocks(prof))
        # A binding beyond the shared 1..11 table range is encoded with C = 0
        # and would otherwise fail silently on the mouse.
        for problem in table_budget_warnings(prof):
            if problem not in result.warnings:
                result.warnings.append(problem)
        lod_pkt = (lod_frame(prof, self.config)
                   if self.config.distance != 0 else None)
        high_pkt = (high_dpi_frame(prof, self.config.sensor)
                    if self.config.distance != 0 else None)

        # Keep the encoded values in the log: a rejected/wedging write is a
        # value problem, and the firmware still answers "write OK".
        _log.debug(
            "apply profile: mode=%d rate=%d stage=%d | light mode=%d "
            "brightness=%d breathing=%d colour=%d length=%d rgb=%s | dpi=%s",
            prof.mode, prof.rate, prof.stage,
            prof.light_mode, prof.brightness, prof.length, prof.frequency,
            prof.direction, prof.fixed_rgb,
            prof.dpi_values[:prof.stage_count],
        )
        _log.debug("lighting frame: %s", light_pkt.hex(" "))
        _log.debug("palette block 0 (cycle): %s", palette[1].hex(" "))
        _log.debug("palette block 1 (stage): %s", palette[3].hex(" "))

        sections = (
            ("mode", mode_pkt), ("rate", rate_pkt), ("stage", stage_pkt),
            ("color", color_pkt), ("lighting", light_pkt),
            ("palette", palette), ("dpi", dpi), ("buttons", buttons),
            ("macros", macros), ("lod", lod_pkt), ("high-dpi", high_pkt),
        )
        changed = [key for key, value in sections
                   if value is not None and self._applied.get(key) != value]

        # The firmware only latches the active stage as part of the vendor's
        # DPI sequence.  FUN_00418a40 never writes 0x0B on its own: the stage
        # travels before the 0x11 table and is adopted after the 0x08 commit.
        # A stage-only diff used to send just 0x0B, which left the sensor on
        # the previous stage while the UI showed the new one -- that is the
        # "every DPI value is wrong" report.  Always carry the DPI section.
        if "stage" in changed and "dpi" not in changed:
            wanted = set(changed) | {"dpi"}
            changed = [key for key, value in sections
                       if key in wanted and value is not None]

        # A lone 0x02 frame does not switch the active layer on the wired
        # firmware.  The vendor build only ever changes the mode inside a
        # complete profile download (FUN_00418a40 always writes every section
        # in order), and on hardware a mode-only write leaves the mouse
        # running the previous layer's bindings.  Mirror the vendor byte for
        # byte whenever the mode changes, including the 0x12 button table.
        if "mode" in changed:
            complete = [key for key, value in sections if value is not None]
            if complete != changed:
                _log.debug(
                    "work mode changed: forcing a complete profile download "
                    "(%s)", ", ".join(complete))
            changed = complete

        # The LED state is one unit on the firmware: the effect frame (0x0D)
        # samples the fixed colour (0x0C) and both palette blocks (0x10) that
        # the vendor writes together in the same download.  Sending 0x0D alone
        # let an effect (notably Slide with Loop Color) read colour state left
        # behind by an earlier profile, so its colour fade started halfway or
        # did not happen at all.  Carry the whole LED group whenever any part
        # of it changes, in the vendor's 0x0C -> 0x0D -> 0x10 order.
        led_sections = {"color", "lighting", "palette"}
        if led_sections & set(changed):
            wanted = set(changed) | led_sections
            led = [key for key, value in sections
                   if key in wanted and value is not None]
            if led != changed:
                _log.debug(
                    "LED state changed: carrying the complete colour group "
                    "(%s)", ", ".join(led))
            changed = led

        _log.debug("changed sections: %s",
                   ", ".join(changed) if changed else "(none)")
        if not changed:
            # The mouse already holds exactly this profile: no HID traffic at
            # all (important when alt-tabbing across apps with the same rules).
            result.changed_sections = []
            return

        # FUN_004196b0 status frames run before the profile body.
        self._phase = "status"
        self.send_feature(frame(0x83))
        self.read_feature()
        self.send_feature(status_frame(prof))

        # FUN_00418a40 body, in the vendor's order.
        if "mode" in changed:
            self._phase = "mode"
            self._mode_expected = int(prof.mode) & 1
            self._mode_expected_at = time.monotonic()
            self.send_feature(mode_pkt)
            self._applied["mode"] = mode_pkt
            self._written.append("mode")
        if "rate" in changed:
            self._phase = "rate"
            self.send_feature(rate_pkt)
            self._applied["rate"] = rate_pkt
            self._written.append("rate")
        if "stage" in changed:
            self._phase = "stage"
            self.send_feature(stage_pkt)
            self._applied["stage"] = stage_pkt
            self._written.append("stage")
        if "color" in changed:
            self._phase = "fixed colour"
            self.send_feature(color_pkt)
            self._applied["color"] = color_pkt
            self._written.append("color")
        if "lighting" in changed:
            self._phase = "lighting"
            self.send_feature(light_pkt)
            self._applied["lighting"] = light_pkt
            self._written.append("lighting")

        if "palette" in changed:
            # 0x10 palette blocks: 0 = cycle colours, 1 = per-stage colours.
            self._phase = "palette"
            self.send_feature(palette[0])
            self.send_block(palette[1])
            self.send_feature(palette[2])
            self.send_block(palette[3])
            self._applied["palette"] = palette
            self._written.append("palette")

        if "dpi" in changed:
            # 0x11 DPI table, then re-assert the active stage: changing the
            # table can move the selected index on some firmware revisions.
            self._phase = "dpi"
            self.send_feature(dpi[0])
            self.send_block(dpi[1])
            self.send_feature(stage_pkt)
            self._applied["dpi"] = dpi
            self._applied["stage"] = stage_pkt
            self._written.append("dpi")

        if "buttons" in changed:
            # 0x12 button table: four frames of two 32-byte blocks.
            self._phase = "buttons"
            for header, first, second in buttons:
                self.send_feature(header)
                self.send_block(first)
                self.send_block(second)
            self._applied["buttons"] = buttons
            self._written.append("buttons")

        if "macros" in changed:
            # 0x13 macro table: each 128-byte entry is split into four blocks.
            # The firmware needs the longer inter-chunk delay while it programs
            # macro memory.
            self._phase = "macros"
            # Each table goes to the index the button descriptor names, not to
            # a dense position in this list.  A macro followed by a gun used to
            # shift every later table by one and point the descriptor at data
            # that was never uploaded.  The 0x13 header selects the table
            # before its four 32-byte blocks.
            for index, block in macros:
                self.send_feature(frame(0x13, (index, 0x80, 0, 0, 0)))
                for offset in range(0, 128, 32):
                    self.send_block(block[offset:offset + 32],
                                    pace=self.macro_chunk_delay)
            self._applied["macros"] = macros
            self._written.append("macros")

        # 0x04 lift-off / key response is only meaningful when Distance != 0.
        if "lod" in changed and lod_pkt is not None:
            self._phase = "lod"
            self.send_feature(lod_pkt)
            self._applied["lod"] = lod_pkt
            self._written.append("lod")

        # Commit magic, then the high-DPI mask (also gated on Distance).
        self._phase = "commit"
        self.send_feature(commit_frame())
        if "high-dpi" in changed and high_pkt is not None:
            self._phase = "high-dpi"
            self.send_feature(high_pkt)
            self._applied["high-dpi"] = high_pkt
            self._written.append("high-dpi")

        self._phase = "done"
        result.changed_sections = changed

        if gun_count:
            result.warnings.append(
                f"{gun_count} gun pattern(s) uploaded. The vendor build hid its "
                "Gun page and never copied gun tables into the upload buffer, "
                "so the studio's encoder is inferred; treat this as "
                "experimental and verify a small pattern on hardware."
            )
        if self.config.distance == 0:
            result.warnings.append(
                "Data.ini Distance=0: lift-off distance and high-DPI mask "
                "frames were skipped exactly as the original does."
            )

    def _persist(self) -> None:
        if self.store is not None:
            self.store.save_profiles()

    # -- device events -----------------------------------------------------
    # How long after a mode write an 0x08xx report may still describe the layer
    # the mouse is leaving.  The complete re-download that accompanies a mode
    # change takes about 1.5 s, so the window covers the whole sequence.
    MODE_ECHO_WINDOW = 2.5

    def _handle_event(self, event: int, value: int) -> None:
        """Map 0x52D payloads the same way FUN_004194a0 does.

        The app receives ``(event << 16) | value`` and decodes the high word as
        the event and the low word as the value.
        """
        _log.debug("device event 0x%04X value=%d", event, value)
        changed = ""
        try:
            if event == 0x7F00:
                if value == 1:
                    # Hot-plug: the original waits 500 ms before reopening.
                    self._sleep(0.5 if not self.demo else 0)
                    self.connect()
                    changed = "connected"
                elif value == 2:
                    self.disconnect()
                    changed = "disconnected"
            elif 0x0700 <= event <= 0x07FF and self.store is not None:
                stage = max(1, min(8, value)) - 1
                self.store.profile.stage = stage
                self.store.save_profiles()
                # The mouse changed the active stage itself: keep the diff
                # cache truthful so the next apply does not resend it.
                self._applied["stage"] = stage_frame(self.store.profile)
                changed = "stage"
            elif 0x0500 <= event <= 0x05FF and self.store is not None:
                mapping = {8: 0, 4: 1, 2: 2, 1: 3}
                if value in mapping:
                    self.store.profile.rate = mapping[value]
                    self.store.save_profiles()
                    self._applied["rate"] = rate_frame(self.store.profile)
                    changed = "rate"
            elif 0x0800 <= event <= 0x08FF and self.store is not None:
                reported = 1 if value >= 2 else 0
                expected = self._mode_expected
                if (expected is not None and reported != expected
                        and time.monotonic() - self._mode_expected_at
                        < self.MODE_ECHO_WINDOW):
                    # Right after our 0x02 write the mouse can still report the
                    # layer it is leaving.  Honouring that echo made the Keys
                    # page jump back to the previous mode (and saved it), so
                    # the just-requested layer wins inside this window.
                    self.log(
                        f"ignoring stale mode report 0x{event:04X}/{value}: "
                        f"just selected {'game' if expected else 'office'}",
                        logging.DEBUG)
                else:
                    self._mode_expected = None
                    self.store.profile.mode = reported
                    self.store.save_profiles()
                    self._applied["mode"] = mode_frame(self.store.profile)
                    changed = "mode"
        except Exception as exc:
            self.log(f"device event 0x{event:04X}/{value} failed: {exc}",
                     logging.WARNING)
        if changed and self.on_profile_changed:
            try:
                self.on_profile_changed(changed)
            except Exception:
                pass
        if self.on_device_event:
            try:
                self.on_device_event(event, value)
            except Exception:
                pass

    # -- convenience -------------------------------------------------------
    def set_stage(self, stage: int) -> bool:
        """Make ``stage`` the live DPI stage using the vendor's DPI sequence.

        FUN_00418a40 never sends 0x0B by itself.  The stage frame travels
        inside the DPI update: 0x11 header + 32-byte table, then 0x0B, and the
        change is only adopted after the 0x08 commit.  A lone 0x0B left the
        sensor on the previous stage on hardware, so every stage except the
        one latched by the last full apply reported the wrong DPI.
        """
        if not self.store:
            return False
        prof = self.store.profile
        prof.stage = max(0, min(prof.stage_count - 1, int(stage)))
        self.store.save_profiles()
        if not self.ensure():
            return False
        dpi = (dpi_header(prof), build_dpi_block(prof, self.config.sensor))
        stage_pkt = stage_frame(prof)
        try:
            # FUN_004196b0 status frames run before the profile body.
            self._phase = "status"
            self.send_feature(frame(0x83))
            self.read_feature()
            self.send_feature(status_frame(prof))
            self._phase = "dpi"
            self.send_feature(dpi[0])
            self.send_block(dpi[1])
            self.send_feature(stage_pkt)
            self._phase = "commit"
            self.send_feature(commit_frame())
        except DeviceError:
            # The hardware state is unknown now: make the next apply rewrite
            # the whole profile instead of trusting the diff cache.
            self._applied.clear()
            return False
        self._applied["dpi"] = dpi
        self._applied["stage"] = stage_pkt
        self._phase = "done"
        return True

    def raw_packet(self, cmd: int, args=()) -> bytes:
        return frame(cmd, args)

    def packet_checksum(self, packet: bytes) -> int:
        return checksum(packet)
