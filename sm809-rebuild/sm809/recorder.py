"""Macro recorder built on WH_KEYBOARD_LL / WH_MOUSE_LL.

The shipped application records through Hook.dll and posts 0x500/0x501 to the
main window.  This module installs the same low-level hooks directly and
produces the identical 16-byte :class:`~sm809.model.MacroEvent` layout.

The hook thread only appends events; UI callbacks are delivered from that
thread and must be marshalled by the caller (tkinter ``after``).
"""

from __future__ import annotations

import ctypes
import ctypes.wintypes as wt
import sys
import threading
import time
from dataclasses import dataclass
from typing import Callable

from .keys import key_id_for_vk, key_id_name, key_name
from .model import MAX_EVENTS, MacroEvent

WH_KEYBOARD_LL = 13
WH_MOUSE_LL = 14

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105

WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_XBUTTONDOWN = 0x020B
WM_XBUTTONUP = 0x020C

MOUSE_LEFT = 0xF0
MOUSE_RIGHT = 0xF1
MOUSE_MIDDLE = 0xF2
MOUSE_X1 = 0xF3
MOUSE_X2 = 0xF4
MOUSE_MOVE = 0xF6

STATE_PRESS = 1
STATE_RELEASE = 2
STATE_NONE = 0

IS_WINDOWS = sys.platform == "win32"


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wt.DWORD),
        ("scanCode", wt.DWORD),
        ("flags", wt.DWORD),
        ("time", wt.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class POINT(ctypes.Structure):
    _fields_ = [("x", wt.LONG), ("y", wt.LONG)]


class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", POINT),
        ("mouseData", wt.DWORD),
        ("flags", wt.DWORD),
        ("time", wt.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


class MSG(ctypes.Structure):
    _fields_ = [
        ("hwnd", wt.HWND),
        ("message", wt.UINT),
        ("wParam", wt.WPARAM),
        ("lParam", wt.LPARAM),
        ("time", wt.DWORD),
        ("pt", POINT),
        ("lPrivate", wt.DWORD),
    ]


@dataclass
class RecorderSettings:
    mode: int = 0                 # 0 = constant 10 ms, 1 = fixed, 2 = timing
    fixed_delay: int = 10
    capture_moves: bool = False
    move_interval_ms: int = 40


class MacroRecorder:
    """Low-level recorder; safe to use without Windows for event assembly."""

    def __init__(self) -> None:
        self.settings = RecorderSettings()
        self.events: list[MacroEvent] = []
        self.recording = False
        self.available = IS_WINDOWS
        self.last_error = ""
        self.on_event: Callable[[list[MacroEvent]], None] | None = None
        self.on_stopped: Callable[[list[MacroEvent]], None] | None = None

        self._lock = threading.RLock()
        self._last_time = 0.0
        self._last_move = 0.0
        self._thread: threading.Thread | None = None
        self._thread_id = 0
        self._ready = threading.Event()
        self._kbd_hook = None
        self._mouse_hook = None
        self._kbd_proc = None
        self._mouse_proc = None
        self._user32 = None
        self._kernel32 = None

    # -- recording lifecycle ----------------------------------------------
    def start(self, settings: RecorderSettings | None = None) -> bool:
        """Begin recording. Returns False when the hooks could not be set."""
        with self._lock:
            if self.recording:
                return True
            if not IS_WINDOWS:
                self.last_error = "low-level hooks require Windows"
                return False
            if settings is not None:
                self.settings = settings
            self.settings.fixed_delay = max(10, min(0xFFFF, self.settings.fixed_delay))
            self.events = []
            self.last_error = ""
            self._ready.clear()
            self.recording = True
            self._last_time = time.perf_counter()
            self._last_move = 0.0
            self._thread = threading.Thread(target=self._hook_thread, name="sm809-recorder", daemon=True)
            self._thread.start()
        if not self._ready.wait(2.0):
            self.recording = False
            self.last_error = self.last_error or "hook thread did not start"
            return False
        return self._kbd_hook is not None and self._mouse_hook is not None

    def stop(self) -> list[MacroEvent]:
        with self._lock:
            was = self.recording
            self.recording = False
        if was and self._thread_id:
            try:
                self._user32.PostThreadMessageW(self._thread_id, 0x0012, 0, 0)
            except Exception:
                pass
        if self._thread is not None:
            self._thread.join(timeout=2.0)
            self._thread = None
        self._remove_hooks()
        snapshot = self.snapshot()
        if was and self.on_stopped:
            try:
                self.on_stopped(snapshot)
            except Exception:
                pass
        return snapshot

    def snapshot(self) -> list[MacroEvent]:
        with self._lock:
            return [MacroEvent(e.opcode, e.state, e.delay, e.a, e.b) for e in self.events]

    @property
    def count(self) -> int:
        with self._lock:
            return len(self.events)

    # -- event assembly (also unit-tested off-Windows) ---------------------
    def dispatch_key(self, vk: int, pressed: bool) -> None:
        if not self.recording:
            return
        key_id = key_id_for_vk(vk)
        if not key_id:
            return
        self._append(key_id, STATE_PRESS if pressed else STATE_RELEASE)

    def dispatch_mouse(self, opcode: int, pressed: bool) -> None:
        if not self.recording:
            return
        self._append(opcode, STATE_PRESS if pressed else STATE_RELEASE)

    def dispatch_move(self, x: int, y: int) -> None:
        if not self.recording or not self.settings.capture_moves:
            return
        now = time.perf_counter()
        if self._last_move and (now - self._last_move) * 1000.0 < self.settings.move_interval_ms:
            return
        self._last_move = now
        self._append(MOUSE_MOVE, STATE_NONE, x, y)

    def _next_delay(self) -> int:
        mode = self.settings.mode
        if mode == 0:
            return 10
        if mode == 1:
            return max(10, min(0xFFFF, self.settings.fixed_delay))
        now = time.perf_counter()
        delta = int(round((now - self._last_time) * 1000.0))
        self._last_time = now
        return max(10, min(0xFFFF, delta))

    def _append(self, opcode: int, state: int, a: int = 0, b: int = 0) -> None:
        with self._lock:
            if not self.recording or len(self.events) >= MAX_EVENTS:
                return
            delay = self._next_delay()
            event = MacroEvent(opcode=opcode, state=state, delay=delay,
                               a=int(a) & 0xFFFFFFFF, b=int(b) & 0xFFFFFFFF)
            self.events.append(event)
            snapshot = [MacroEvent(e.opcode, e.state, e.delay, e.a, e.b) for e in self.events]
        if self.on_event:
            try:
                self.on_event(snapshot)
            except Exception:
                pass

    # -- win32 hook plumbing ----------------------------------------------
    def _hook_thread(self) -> None:
        try:
            self._user32 = ctypes.WinDLL("user32", use_last_error=True)
            self._kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            user32 = self._user32
            kernel32 = self._kernel32

            HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_ssize_t, ctypes.c_int,
                                          wt.WPARAM, wt.LPARAM)
            self._kbd_proc = HOOKPROC(self._keyboard_proc)
            self._mouse_proc = HOOKPROC(self._mouse_proc_fn)

            user32.SetWindowsHookExW.restype = ctypes.c_void_p
            user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC,
                                                 ctypes.c_void_p, wt.DWORD]
            user32.CallNextHookEx.restype = ctypes.c_ssize_t
            user32.CallNextHookEx.argtypes = [ctypes.c_void_p, ctypes.c_int,
                                              wt.WPARAM, wt.LPARAM]
            user32.UnhookWindowsHookEx.argtypes = [ctypes.c_void_p]
            user32.GetMessageW.argtypes = [ctypes.POINTER(MSG), wt.HWND, wt.UINT, wt.UINT]
            user32.PostThreadMessageW.argtypes = [wt.DWORD, wt.UINT, wt.WPARAM, wt.LPARAM]

            kernel32.GetModuleHandleW.restype = ctypes.c_void_p
            kernel32.GetModuleHandleW.argtypes = [wt.LPCWSTR]
            kernel32.GetCurrentThreadId.restype = wt.DWORD

            module = kernel32.GetModuleHandleW(None)
            self._thread_id = kernel32.GetCurrentThreadId()
            self._kbd_hook = user32.SetWindowsHookExW(WH_KEYBOARD_LL, self._kbd_proc, module, 0)
            self._mouse_hook = user32.SetWindowsHookExW(WH_MOUSE_LL, self._mouse_proc, module, 0)
            if not self._kbd_hook or not self._mouse_hook:
                self.last_error = f"SetWindowsHookEx failed (error {ctypes.get_last_error()})"
                self._ready.set()
                self._remove_hooks()
                return
            self._ready.set()

            msg = MSG()
            while True:
                result = user32.GetMessageW(ctypes.byref(msg), None, 0, 0)
                if result == 0 or result == -1:
                    break
                user32.TranslateMessage(ctypes.byref(msg))
                user32.DispatchMessageW(ctypes.byref(msg))
        except Exception as exc:  # pragma: no cover - Windows only
            self.last_error = f"recorder thread failed: {exc}"
            self._ready.set()
        finally:
            self._remove_hooks()
            self._thread_id = 0

    def _remove_hooks(self) -> None:
        if self._user32 is None:
            return
        try:
            if self._kbd_hook:
                self._user32.UnhookWindowsHookEx(self._kbd_hook)
            if self._mouse_hook:
                self._user32.UnhookWindowsHookEx(self._mouse_hook)
        except Exception:
            pass
        self._kbd_hook = None
        self._mouse_hook = None

    # -- hook callbacks ----------------------------------------------------
    def _keyboard_proc(self, n_code, w_param, l_param):  # pragma: no cover - Windows
        if n_code >= 0 and self.recording:
            try:
                info = ctypes.cast(l_param, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
                if w_param in (WM_KEYDOWN, WM_SYSKEYDOWN):
                    self.dispatch_key(info.vkCode, True)
                elif w_param in (WM_KEYUP, WM_SYSKEYUP):
                    self.dispatch_key(info.vkCode, False)
            except Exception:
                pass
        return self._user32.CallNextHookEx(None, n_code, w_param, l_param)

    def _mouse_proc_fn(self, n_code, w_param, l_param):  # pragma: no cover - Windows
        if n_code >= 0 and self.recording:
            try:
                info = ctypes.cast(l_param, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
                if w_param == WM_MOUSEMOVE:
                    self.dispatch_move(info.pt.x, info.pt.y)
                elif w_param in (WM_LBUTTONDOWN, WM_LBUTTONUP):
                    self.dispatch_mouse(MOUSE_LEFT, w_param == WM_LBUTTONDOWN)
                elif w_param in (WM_RBUTTONDOWN, WM_RBUTTONUP):
                    self.dispatch_mouse(MOUSE_RIGHT, w_param == WM_RBUTTONDOWN)
                elif w_param in (WM_MBUTTONDOWN, WM_MBUTTONUP):
                    self.dispatch_mouse(MOUSE_MIDDLE, w_param == WM_MBUTTONDOWN)
                elif w_param in (WM_XBUTTONDOWN, WM_XBUTTONUP):
                    button = (info.mouseData >> 16) & 0xFFFF
                    opcode = MOUSE_X2 if button == 2 else MOUSE_X1
                    self.dispatch_mouse(opcode, w_param == WM_XBUTTONDOWN)
            except Exception:
                pass
        return self._user32.CallNextHookEx(None, n_code, w_param, l_param)


def event_label(event: MacroEvent) -> str:
    """List label matching the original's action list."""
    if event.state == STATE_NONE:
        if event.opcode == MOUSE_MOVE:
            return f"Move to ({event.a}, {event.b})"
        if event.opcode == 0xFB:
            return f"Move to ({event.a}, {event.b})"
        return f"Event 0x{event.opcode:02X}"
    if event.opcode in (MOUSE_LEFT, MOUSE_RIGHT, MOUSE_MIDDLE, MOUSE_X1, MOUSE_X2):
        names = {MOUSE_LEFT: "Left", MOUSE_RIGHT: "Right", MOUSE_MIDDLE: "Middle",
                 MOUSE_X1: "Mouse 4", MOUSE_X2: "Mouse 5"}
        base = names.get(event.opcode, f"Mouse 0x{event.opcode:02X}")
        action = "Down" if event.state == STATE_PRESS else "Up"
        return f"{base} {action}"
    name = key_id_name(event.opcode)
    if name == f"key {event.opcode:02X}":
        vk = event.opcode
        alt = key_name(vk)
        if alt != f"VK 0x{vk:02X}":
            name = alt
    action = "Down" if event.state == STATE_PRESS else "Up"
    return f"{name} {action}"
