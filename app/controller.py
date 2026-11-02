"""DeviceController -- owns the wired SM809 session off the UI thread.

All HID traffic (a full profile is hundreds of feature/block writes) runs on a
worker thread. The UI queues commands by name and receives results through Qt
signals. Unlike the wireless reference there is no status listener or battery
channel: the wired monitor interface reports stage / rate / mode changes, which
the service forwards here.

Usage:
    ctrl = DeviceController(profile_store)
    ctrl.connected.connect(on_connected)
    ctrl.command_done.connect(on_done)
    ctrl.start()
    ctrl.call("apply_config", config, pid)   # queue a full-profile write
"""

from __future__ import annotations

import logging
import queue
import threading
import time

from PySide6.QtCore import QObject, Signal

from wired.bridge import dpi_from_display, rate_hz
from wired.device import DeviceService
from wired.transport import HidTransport

_log = logging.getLogger("sm809.controller")


class DeviceController(QObject):
    # lifecycle
    connected = Signal(dict)        # {connection, product, configurable}
    disconnected = Signal()
    error = Signal(str)
    # live device push (wired monitor interface)
    dpi_level_changed = Signal(int)     # current DPI stage index
    rate_changed = Signal(int)          # current polling rate (Hz)
    mode_changed = Signal(int)          # work mode: 0 = Office, 1 = Game
    # kept for shell compatibility; the wired mouse has no battery
    battery_changed = Signal(int)
    charging_changed = Signal(bool)
    alive_changed = Signal(bool)
    runapp_pressed = Signal(int)
    # a queued command finished: (method_name, ok)
    command_done = Signal(str, bool)
    busy_changed = Signal(bool)         # True while a queued command is running

    def __init__(self, profiles, demo=False, parent=None):
        super().__init__(parent)
        self._profiles = profiles
        self._dev = DeviceService(
            profiles.device_config,
            profiles.data,
            demo=demo,
            transport=None if not demo else HidTransport(profiles.device_config, demo=True),
        )
        self._dev.connection = "wired"
        self._dev.pid = profiles.device_config.pid
        self._dev.vid = profiles.device_config.vid
        self._dev.configurable = True
        self._dev.interface_info = {"product_string": "SM809 (USB wired)"}
        self._dev.on_profile_changed = self._on_profile_changed
        self._dev.on_disconnect = self._on_lost
        # DeviceService logs through app.logging_setup itself; no print wiring.
        self._dev.on_log = None
        # Apply warnings describe standing configuration (e.g. Distance=0) and
        # would otherwise repeat on every write. Show them once per session.
        self._seen_warnings: set[str] = set()

        self._q: queue.Queue = queue.Queue()
        self._worker: threading.Thread | None = None
        self._stop = threading.Event()
        self._lost = threading.Event()      # set by the HID monitor thread
        self._is_connected = False
        self._last_check = 0.0
        self._dev_lock = threading.RLock()

    # -- public API -----------------------------------------------------------
    @property
    def demo(self) -> bool:
        return self._dev.demo

    def start(self):
        self._stop.clear()
        self._worker = threading.Thread(target=self._run, daemon=True,
                                        name="sm809-wired")
        self._worker.start()

    def call(self, method: str, *args, **kwargs):
        """Queue a device method call by name; result via command_done.

        Full-profile writes are state snapshots: if several are waiting, only
        the newest matters. Replacing the stale ones keeps a slider drag or a
        fast series of edits from building a backlog that keeps the HID link
        busy for seconds (the pointer visibly stutters while it is flooded).
        """
        item = (method, args, kwargs)
        if method == "apply_config":
            with self._q.mutex:
                pending = list(self._q.queue)
                if any(p is not None and p[0] == "apply_config" for p in pending):
                    # Keep the queue order (a stage change queued after the
                    # write must still run after it) and swap the newest
                    # snapshot into the first waiting slot.
                    kept = []
                    replaced = False
                    for p in pending:
                        if p is not None and p[0] == "apply_config":
                            if not replaced:
                                kept.append(item)
                                replaced = True
                            continue
                        kept.append(p)
                    self._q.queue.clear()
                    self._q.queue.extend(kept)
                    self._q.not_empty.notify()
                    return
        self._q.put(item)

    def shutdown(self):
        self._stop.set()
        self._q.put(None)
        if self._worker and self._worker.is_alive():
            self._worker.join(timeout=3.0)
        with self._dev_lock:
            try:
                self._dev.disconnect()
            except Exception:
                pass

    # -- worker ---------------------------------------------------------------
    def _run(self):
        while not self._stop.is_set():
            # 0. The monitor thread only raises a flag: closing the HID
            #    handles from that thread would race the worker's own writes.
            #    Do the teardown here, on the thread that owns the device.
            if self._lost.is_set():
                self._lost.clear()
                self._teardown()

            # 1. Connect / reconnect when the cable appears.
            if not self._is_connected:
                self._attempt_connect()
                if not self._is_connected:
                    self._drain_queue()
                    self._stop.wait(1.5)
                    continue

            # 2. Wait for a queued command (1 s timeout for link maintenance).
            try:
                item = self._q.get(timeout=1.0)
            except queue.Empty:
                item = None
            if self._stop.is_set():
                break

            # 3. Execute it.
            if item is not None:
                method, args, kwargs = item
                if method is None:
                    continue
                self.busy_changed.emit(True)
                ok = False
                try:
                    with self._dev_lock:
                        ok = bool(self._dispatch(method, args, kwargs))
                except Exception as exc:
                    _log.exception("command %s failed", method)
                    self.error.emit(f"{method} failed: {exc}")
                    ok = False
                self.command_done.emit(method, ok)
                if self._q.empty():
                    self.busy_changed.emit(False)

            # 4. Link health.
            if self._is_connected:
                self._maintain()

        with self._dev_lock:
            try:
                self._dev.disconnect()
            except Exception:
                pass

    def _dispatch(self, method, args, kwargs):
        if method == "apply_config":
            return self._apply_config(*args, **kwargs)
        if method == "set_active_dpi":
            return self._set_active_dpi(*args, **kwargs)
        return getattr(self._dev, method)(*args, **kwargs)

    def _attempt_connect(self):
        try:
            ok = self._dev.connect()
        except Exception as exc:
            ok = False
            _log.exception("connect raised")
            self.error.emit(str(exc))
        if ok:
            self._is_connected = True
            self._last_check = time.time()
            self.connected.emit({
                "connection": "wired",
                "product": "SM809 (USB wired)",
                "configurable": True,
            })
            self._emit_live()

    def _maintain(self):
        now = time.time()
        if now - self._last_check < 1.5:
            return
        self._last_check = now
        if not self._dev.transport.connected and not self._dev.demo:
            self._teardown()
            return
        # keepalive: a cheap enumeration, without re-sending config
        if not self._dev.demo and not self._dev.present():
            self._teardown()

    def _teardown(self):
        was = self._is_connected
        self._is_connected = False
        try:
            self._dev.disconnect()
        except Exception:
            pass
        if was:
            self.disconnected.emit()

    def _drain_queue(self):
        while not self._q.empty():
            try:
                item = self._q.get_nowait()
            except queue.Empty:
                break
            if item is None:
                continue
            self.command_done.emit(item[0], False)
        self.busy_changed.emit(False)

    # -- commands -------------------------------------------------------------
    def _apply_config(self, config, pid):
        result = self._profiles.apply(pid, self._dev, config=config)
        if result is None:
            _log.error("apply requested for unknown profile %s", pid)
            self.error.emit("unknown profile")
            return False
        for warning in result.warnings:
            if warning in self._seen_warnings:
                continue
            self._seen_warnings.add(warning)
            _log.warning("%s", warning)
        if not result.ok:
            _log.error("apply failed: %s", result.error or "unknown error")
            self.error.emit(result.error or "apply failed")
            return False
        if result.changed_sections:
            _log.info(
                "applied %s (%d feature frame(s), %d block(s))",
                ", ".join(result.changed_sections),
                result.sent_packets,
                result.sent_blocks,
            )
        else:
            _log.debug("device already matches this profile; nothing sent")
        self._emit_live()
        return True

    def _set_active_dpi(self, pid, values, selected):
        idx = self._profiles.index_of(pid)
        if idx < 0:
            return False
        prof = self._profiles.data.profiles[idx]
        raw = [dpi_from_display(self._profiles.sensor, v) for v in values]
        if raw:
            prof.dpi_values = raw
            prof.stage_count = max(1, min(8, len(raw)))
        prof.stage = max(0, min(prof.stage_count - 1, int(selected)))
        self._profiles.data.selected = idx
        # Route through the store so it records the write generation (the UI's
        # debounced flush then has nothing left to do).
        self._profiles.save_profiles()
        ok = self._dev.set_stage(prof.stage)
        if ok:
            self.dpi_level_changed.emit(prof.stage)
        return ok

    # -- live events ----------------------------------------------------------
    def _emit_live(self):
        try:
            prof = self._dev.store.profile
        except Exception:
            return
        self.dpi_level_changed.emit(int(prof.stage))
        self.rate_changed.emit(rate_hz(prof.rate))

    def _on_profile_changed(self, changed):
        if changed == "disconnected":
            # Also raised on the HID monitor thread; let the worker tear down.
            self._lost.set()
            return
        if changed == "connected":
            if not self._is_connected:
                self._attempt_connect()
            return
        if changed == "mode":
            # profile.mode uses the UI layer's own encoding:
            # 0 = Office (slots 0-15), 1 = Game (slots 32-47).
            try:
                mode = int(self._dev.store.profile.mode)
            except Exception:
                mode = 0
            self.mode_changed.emit(0 if mode == 0 else 1)
            self._emit_live()
            return
        if changed in ("stage", "rate"):
            self._emit_live()

    def _on_lost(self):
        """Transport callback -- runs on the ``sm809-monitor`` thread.

        Never touch the device here.  The worker notices the flag at the top
        of its loop and performs the single, lock-ordered teardown.
        """
        self._lost.set()
