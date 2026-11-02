"""System-wide mouse-button capture for macro recording (Windows only).

The official driver loads ``Hook.dll`` and installs a ``WH_MOUSE_LL`` hook while
a macro is being recorded, so clicks aimed at another application are captured
too.  This module provides the same capability with ctypes: the hook observes
button down/up messages, never consumes them, and is installed only for the
duration of a recording.

Wheel movement and pointer motion are ignored: the wired macro table stores
button edges only, matching the five-button table in the official driver.
"""

from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes

from PySide6.QtCore import QObject, QPoint, Signal
from PySide6.QtWidgets import QApplication

WH_MOUSE_LL = 14
HC_ACTION = 0
LLMHF_INJECTED = 0x01

WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MBUTTONDOWN = 0x0207
WM_MBUTTONUP = 0x0208
WM_XBUTTONDOWN = 0x020B
WM_XBUTTONUP = 0x020C

XBUTTON1 = 0x0001
XBUTTON2 = 0x0002


class _MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("pt", wintypes.POINT),
        ("mouseData", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),
    ]


def mouse_action(message: int, mouse_data: int = 0):
    """Map a Windows mouse message to ``(button, down)`` or ``None``.

    Buttons use the studio's macro numbering: 1 left, 2 right, 3 middle,
    4 back (X1) and 5 forward (X2).  Wheel and move messages return ``None``.
    """
    msg = int(message)
    if msg == WM_LBUTTONDOWN:
        return 1, True
    if msg == WM_LBUTTONUP:
        return 1, False
    if msg == WM_RBUTTONDOWN:
        return 2, True
    if msg == WM_RBUTTONUP:
        return 2, False
    if msg == WM_MBUTTONDOWN:
        return 3, True
    if msg == WM_MBUTTONUP:
        return 3, False
    if msg in (WM_XBUTTONDOWN, WM_XBUTTONUP):
        xbutton = (int(mouse_data) >> 16) & 0xFFFF
        if xbutton == XBUTTON1:
            return 4, msg == WM_XBUTTONDOWN
        if xbutton == XBUTTON2:
            return 5, msg == WM_XBUTTONDOWN
    return None


class MouseHook(QObject):
    """A low-level mouse-button hook that emits ``mouseEvent(button, down)``.

    The hook is installed on the GUI thread and driven by Qt's existing message
    loop.  ``set_ignore_widgets`` marks controls that must stay out of the
    macro (the recorder's own Stop button); every other click, including clicks
    inside the studio window, is reported.
    """

    mouseEvent = Signal(int, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._user32 = None
        self._hook = None
        self._proc = None
        self._ignore = []

    def set_ignore_widgets(self, *widgets):
        """Clicks on (or inside) these widgets are not emitted."""
        self._ignore = [w for w in widgets if w is not None]

    @property
    def active(self):
        return self._hook is not None

    # -- lifecycle ------------------------------------------------------------
    def start(self) -> bool:
        """Install the hook. Returns True when it is active afterwards."""
        if sys.platform != "win32":
            return False
        if self._hook is not None:
            return True
        try:
            user32 = ctypes.WinDLL("user32", use_last_error=True)
            lresult = ctypes.c_ssize_t
            hookproc = ctypes.WINFUNCTYPE(
                lresult, ctypes.c_int, ctypes.c_size_t, ctypes.c_void_p)
            user32.SetWindowsHookExW.restype = ctypes.c_void_p
            user32.SetWindowsHookExW.argtypes = (
                ctypes.c_int, hookproc, ctypes.c_void_p, ctypes.c_uint32)
            user32.CallNextHookEx.restype = lresult
            user32.CallNextHookEx.argtypes = (
                ctypes.c_void_p, ctypes.c_int, ctypes.c_size_t,
                ctypes.c_void_p)
            user32.UnhookWindowsHookEx.restype = wintypes.BOOL
            user32.UnhookWindowsHookEx.argtypes = (ctypes.c_void_p,)

            proc = hookproc(self._on_mouse)
            hook = user32.SetWindowsHookExW(WH_MOUSE_LL, proc, None, 0)
            if not hook:
                return False
            # Keep the callback alive for as long as the hook is installed.
            self._user32 = user32
            self._proc = proc
            self._hook = hook
            return True
        except Exception:
            self._user32 = None
            self._proc = None
            self._hook = None
            return False

    def stop(self) -> None:
        hook, user32 = self._hook, self._user32
        self._hook = None
        self._user32 = None
        self._proc = None
        if hook and user32 is not None:
            try:
                user32.UnhookWindowsHookEx(hook)
            except Exception:
                pass

    # -- callback -------------------------------------------------------------
    def _on_mouse(self, ncode, wparam, lparam):
        try:
            if ncode == HC_ACTION and lparam:
                info = ctypes.cast(
                    lparam, ctypes.POINTER(_MSLLHOOKSTRUCT)).contents
                action = mouse_action(wparam, info.mouseData)
                if (action is not None
                        and not (int(info.flags) & LLMHF_INJECTED)
                        and not self._over_ignored(info.pt)):
                    button, down = action
                    self.mouseEvent.emit(button, down)
        except Exception:
            # A hook callback must never raise into Windows.
            pass
        try:
            return self._user32.CallNextHookEx(None, ncode, wparam, lparam)
        except Exception:
            return 0

    def _over_ignored(self, pt) -> bool:
        """True when the click target is (inside) an ignored widget."""
        if not self._ignore:
            return False
        try:
            point = QPoint(int(pt.x), int(pt.y))
            widget = QApplication.widgetAt(point)
            while widget is not None:
                if any(widget is w for w in self._ignore):
                    return True
                widget = widget.parentWidget()
        except Exception:
            return False
        return False


__all__ = ["MouseHook", "mouse_action"]
