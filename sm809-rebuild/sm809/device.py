"""Connection manager and apply engine.

The apply order, handshake and frame payloads follow analysis/OVERVIEW.md
section 6/7 and the shipped executable's disassembly.  All writes go through
:class:`sm809.transport.HidTransport`, so the same code path runs against real
hardware and against the demo transport used by the tests.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Callable

from .config import DeviceConfig
from .model import DataStore, Profile
from .protocol import (
    HANDSHAKE_EXPECTED,
    HANDSHAKE_PLAIN,
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
    validate_buttons,
)
from .transport import HidTransport
from .winspi import PointerSettings


class DeviceError(RuntimeError):
    pass


@dataclass
class ApplyResult:
    ok: bool
    warnings: list[str] = field(default_factory=list)
    windows_changes: list[str] = field(default_factory=list)
    sent_packets: int = 0
    sent_blocks: int = 0
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

        self.on_device_event: Callable[[int, int], None] | None = None
        self.on_profile_changed: Callable[[str], None] | None = None
        self.on_disconnect: Callable[[], None] | None = None
        self.on_log: Callable[[str], None] | None = None

        self.transport.on_event = self._handle_event
        self.transport.on_disconnect = self._transport_lost

    # -- diagnostics -------------------------------------------------------
    def log(self, text: str) -> None:
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
            if not self.transport.open():
                self.linked = False
                self.last_error = "SM809 not found (VID 04D9 / PID A09F)"
                return False
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
                    self.transport.close()
                    self.linked = False
                return ok
            except Exception as exc:  # pragma: no cover - hardware path
                self.last_error = f"connect failed: {exc}"
                self.transport.close()
                self.linked = False
                self.log(self.last_error)
                return False

    def disconnect(self) -> None:
        self.transport.close()
        self.linked = False

    def _transport_lost(self) -> None:
        self.linked = False
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
        self._sleep(self.pace if pace is None else pace)
        if not ok:
            raise DeviceError("SetFeature failed")
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
            raise ValueError("block must be 32 bytes")
        if not self.transport.write_block(block):
            raise DeviceError("WriteUSB failed")
        self._sleep(self.pace if pace is None else pace)

    # -- handshake / status ------------------------------------------------
    def handshake(self) -> bool:
        """FUN_0041bbc0: plain packet, then the same bytes obfuscated."""
        plain = HANDSHAKE_PLAIN
        self.send_feature(plain, obfuscated=True, pace=max(self.pace, 0.03))
        self.transport.get_feature()  # first reply is ignored
        self._sleep(0.03)
        encoded = obfuscate(plain, self.config.key)
        self.send_feature(encoded, obfuscated=True, pace=max(self.pace, 0.03))
        reply = self.transport.get_feature()
        self._sleep(0.03)
        # FUN_0041bbc0 only accepts a reply that decrypts to the magic; the
        # raw GetFeature buffer is never compared, so a static/echoed report
        # cannot pass by accident.
        ok = handshake_reply_ok(reply, self.config.key)
        if not ok:
            self.log("handshake reply did not decrypt to AA DD 3B 62")
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
            self.send_feature(frame(0x80, (0,)), pace=max(self.pace, 0.03))
            self._sleep(0.03)
            self.send_feature(frame(0x80, (0,)), pace=max(self.pace, 0.03))
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
            return self.version
        except Exception as exc:
            self.log(f"version query failed: {exc}")
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
            result.error = str(exc)
            result.ok = False
            self.log(f"apply failed: {exc}")
            return result

        result.sent_packets = len(self.transport.sent_packets) - before_packets
        result.sent_blocks = len(self.transport.sent_blocks) - before_blocks
        result.version = self.version
        if persist:
            self._persist()
        result.ok = not result.error
        return result

    def _apply_sequence(self, prof: Profile, result: ApplyResult) -> None:
        # FUN_004196b0 status frames run before the profile body.
        self.send_feature(frame(0x83))
        self.read_feature()
        self.send_feature(status_frame(prof))

        # FUN_00418a40 body.
        self.send_feature(mode_frame(prof))
        self.send_feature(rate_frame(prof))
        self.send_feature(stage_frame(prof))
        self.send_feature(fixed_color_frame(prof))
        self.send_feature(light_frame(prof))

        # 0x10 palette blocks: 0 = cycle colours, 1 = per-stage colours.
        self.send_feature(palette_header(0))
        self.send_block(palette_block(prof.cycle_colors))
        self.send_feature(palette_header(1))
        self.send_block(palette_block(prof.stage_colors))

        # 0x11 DPI table.
        self.send_feature(dpi_header(prof))
        self.send_block(build_dpi_block(prof, self.config.sensor))

        # 0x12 button table: four frames of two 32-byte blocks.
        slots, _macro_counter, gun_count = build_button_slots(prof, self.config)
        for header, first, second in button_frames(slots):
            self.send_feature(header)
            self.send_block(first)
            self.send_block(second)

        # 0x13 macro table: each 128-byte entry is split into four blocks.
        blocks = macro_blocks(prof)
        for index, block in enumerate(blocks):
            self.send_feature(frame(0x13, (index + 1, 0x80, 0, 0, 0)))
            for offset in range(0, 128, 32):
                self.send_block(block[offset:offset + 32])

        # 0x04 lift-off / key response is only meaningful when Distance != 0.
        if self.config.distance != 0:
            self.send_feature(lod_frame(prof, self.config))

        # Commit magic, then the high-DPI mask (also gated on Distance).
        self.send_feature(commit_frame())
        if self.config.distance != 0:
            self.send_feature(high_dpi_frame(prof, self.config.sensor))

        if gun_count:
            result.warnings.append(
                f"{gun_count} gun action(s) uploaded. The shipped application "
                "never copied gun tables into the upload buffer; treat this "
                "as experimental and verify on hardware."
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
    def _handle_event(self, event: int, value: int) -> None:
        """Map 0x52D payloads the same way FUN_004194a0 does.

        The app receives ``(event << 16) | value`` and decodes the high word as
        the event and the low word as the value.
        """
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
                changed = "stage"
            elif 0x0500 <= event <= 0x05FF and self.store is not None:
                mapping = {8: 0, 4: 1, 2: 2, 1: 3}
                if value in mapping:
                    self.store.profile.rate = mapping[value]
                    self.store.save_profiles()
                    changed = "rate"
            elif 0x0800 <= event <= 0x08FF and self.store is not None:
                self.store.profile.mode = 1 if value >= 2 else 0
                self.store.save_profiles()
                changed = "mode"
        except Exception as exc:
            self.log(f"device event 0x{event:04X}/{value} failed: {exc}")
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
        """Write just the active DPI stage (used by the page radios)."""
        if not self.store:
            return False
        self.store.profile.stage = max(0, min(7, int(stage)))
        self.store.save_profiles()
        if not self.ensure():
            return False
        try:
            self.send_feature(stage_frame(self.store.profile))
            return True
        except DeviceError:
            return False

    def raw_packet(self, cmd: int, args=()) -> bytes:
        return frame(cmd, args)

    def packet_checksum(self, packet: bytes) -> int:
        return checksum(packet)
