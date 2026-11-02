"""Physical mouse-movement capture for the Gun (recoil) recorder.

Games consume *raw* mouse input, and many lock or recentre the pointer.  A
screen-coordinate hook would then report no movement (or a constant clamped
position), so this module reads Windows Raw Input (``WM_INPUT``) instead.  It
attaches the input sink to a hidden window, which also receives reports while
the studio is in the background.

Only relative mouse movement is reported; button and wheel data are ignored.
The recorder never consumes input, so the game keeps receiving everything it
normally would.  Non-Windows systems report ``start() -> False`` and the UI
shows that recording is unavailable.
"""

from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes

from PySide6.QtCore import QObject

WM_INPUT = 0x00FF
RID_INPUT = 0x10000003
RIDEV_REMOVE = 0x00000001
RIDEV_INPUTSINK = 0x00000100
RIM_TYPEMOUSE = 0
MOUSE_MOVE_ABSOLUTE = 0x01
GWLP_WNDPROC = -4


class _RAWINPUTDEVICE(ctypes.Structure):
    _fields_ = [
        ("usUsagePage", wintypes.USHORT),
        ("usUsage", wintypes.USHORT),
        ("dwFlags", wintypes.DWORD),
        ("hwndTarget", wintypes.HWND),
    ]


class _RAWMOUSEBUTTONS(ctypes.Structure):
    _fields_ = [
        ("usButtonFlags", wintypes.USHORT),
        ("usButtonData", wintypes.USHORT),
    ]


class _RAWMOUSEBUTTONUNION(ctypes.Union):
    _fields_ = [
        ("ulButtons", wintypes.ULONG),
        ("buttons", _RAWMOUSEBUTTONS),
    ]


class _RAWMOUSE(ctypes.Structure):
    _fields_ = [
        ("usFlags", wintypes.USHORT),
        ("buttonUnion", _RAWMOUSEBUTTONUNION),
        ("ulRawButtons", wintypes.ULONG),
        ("lLastX", wintypes.LONG),
        ("lLastY", wintypes.LONG),
        ("ulExtraInformation", wintypes.ULONG),
    ]


class _RAWINPUTHEADER(ctypes.Structure):
    _fields_ = [
        ("dwType", wintypes.DWORD),
        ("dwSize", wintypes.DWORD),
        ("hDevice", wintypes.HANDLE),
        ("wParam", wintypes.WPARAM),
    ]


class _RAWINPUT(ctypes.Structure):
    _fields_ = [
        ("header", _RAWINPUTHEADER),
        ("mouse", _RAWMOUSE),
    ]


_WNDPROC = ctypes.WINFUNCTYPE(
    ctypes.c_ssize_t, wintypes.HWND, wintypes.UINT,
    wintypes.WPARAM, wintypes.LPARAM)


class _RawInputSink:
    """A hidden window that owns the raw-input registration."""

    def __init__(self, owner):
        self.owner = owner
        self._user32 = None
        self._hwnd = None
        self._proc = None

    @property
    def active(self):
        return self._hwnd is not None

    def start(self) -> bool:
        if sys.platform != "win32":
            return False
        if self._hwnd is not None:
            return True
        try:
            user32 = ctypes.WinDLL("user32", use_last_error=True)
            user32.CreateWindowExW.restype = wintypes.HWND
            user32.CreateWindowExW.argtypes = (
                wintypes.DWORD, wintypes.LPCWSTR, wintypes.LPCWSTR,
                wintypes.DWORD, ctypes.c_int, ctypes.c_int,
                ctypes.c_int, ctypes.c_int, wintypes.HWND, wintypes.HMENU,
                wintypes.HINSTANCE, wintypes.LPVOID)
            user32.DefWindowProcW.restype = ctypes.c_ssize_t
            user32.DefWindowProcW.argtypes = (
                wintypes.HWND, wintypes.UINT, wintypes.WPARAM,
                wintypes.LPARAM)
            user32.DestroyWindow.argtypes = (wintypes.HWND,)
            user32.RegisterRawInputDevices.restype = wintypes.BOOL
            user32.RegisterRawInputDevices.argtypes = (
                ctypes.POINTER(_RAWINPUTDEVICE), wintypes.UINT,
                wintypes.UINT)
            user32.GetRawInputData.restype = wintypes.UINT
            user32.GetRawInputData.argtypes = (
                wintypes.HANDLE, wintypes.UINT, ctypes.c_void_p,
                ctypes.POINTER(wintypes.UINT), wintypes.UINT)
            setter = getattr(user32, "SetWindowLongPtrW", None)
            if setter is None:
                setter = user32.SetWindowLongW
            setter.restype = ctypes.c_void_p
            setter.argtypes = (
                wintypes.HWND, ctypes.c_int, ctypes.c_void_p)

            hwnd = user32.CreateWindowExW(
                0, "STATIC", "SM809RecoilSink", 0,
                0, 0, 0, 0, None, None, None, None)
            if not hwnd:
                return False
            proc = _WNDPROC(self._wndproc)
            setter(hwnd, GWLP_WNDPROC,
                   ctypes.cast(proc, ctypes.c_void_p))
            device = _RAWINPUTDEVICE(
                0x01, 0x02, RIDEV_INPUTSINK, hwnd)
            if not user32.RegisterRawInputDevices(
                    ctypes.byref(device), 1, ctypes.sizeof(_RAWINPUTDEVICE)):
                user32.DestroyWindow(hwnd)
                return False
            self._user32 = user32
            self._hwnd = hwnd
            self._proc = proc          # keep the callback alive
            return True
        except Exception:
            self._user32 = None
            self._hwnd = None
            self._proc = None
            return False

    def stop(self) -> None:
        user32, hwnd, proc = self._user32, self._hwnd, self._proc
        self._user32 = None
        self._hwnd = None
        self._proc = None
        if user32 is None or not hwnd:
            return
        try:
            device = _RAWINPUTDEVICE(0x01, 0x02, RIDEV_REMOVE, None)
            user32.RegisterRawInputDevices(
                ctypes.byref(device), 1, ctypes.sizeof(_RAWINPUTDEVICE))
        except Exception:
            pass
        try:
            user32.DestroyWindow(hwnd)
        except Exception:
            pass
        # ``proc`` stays referenced until the window is gone.
        del proc

    # -- window procedure -----------------------------------------------------
    def _wndproc(self, hwnd, msg, wparam, lparam):
        try:
            if msg == WM_INPUT and self.owner is not None:
                dx, dy = self._read(lparam)
                if dx or dy:
                    self.owner.feed(dx, dy)
        except Exception:
            # A window procedure must never raise into Windows.
            pass
        try:
            return self._user32.DefWindowProcW(hwnd, msg, wparam, lparam)
        except Exception:
            return 0

    def _read(self, lparam):
        data = _RAWINPUT()
        size = wintypes.UINT(ctypes.sizeof(_RAWINPUT))
        got = self._user32.GetRawInputData(
            lparam, RID_INPUT, ctypes.byref(data), ctypes.byref(size),
            ctypes.sizeof(_RAWINPUTHEADER))
        if got in (0, 0xFFFFFFFF):
            return 0, 0
        if data.header.dwType != RIM_TYPEMOUSE:
            return 0, 0
        if data.mouse.usFlags & MOUSE_MOVE_ABSOLUTE:
            # Touch / remote-desktop absolute packets are not physical deltas.
            return 0, 0
        return int(data.mouse.lLastX), int(data.mouse.lLastY)


class RecoilRecorder(QObject):
    """Accumulate raw mouse deltas between UI samples.

    ``feed`` is public so tests and fallback sources can inject movement
    without Windows.  ``take_delta`` returns and clears the accumulator.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sink = _RawInputSink(self)
        self._dx = 0
        self._dy = 0

    @property
    def active(self):
        return self._sink.active

    def start(self) -> bool:
        self._dx = 0
        self._dy = 0
        return self._sink.start()

    def stop(self) -> None:
        self._sink.stop()
        self._dx = 0
        self._dy = 0

    def feed(self, dx, dy) -> None:
        self._dx += int(dx)
        self._dy += int(dy)

    def take_delta(self) -> tuple[int, int]:
        dx, dy = self._dx, self._dy
        self._dx = 0
        self._dy = 0
        return dx, dy


__all__ = ["RecoilRecorder"]
