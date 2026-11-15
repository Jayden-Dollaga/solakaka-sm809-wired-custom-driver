"""Native Windows drop bridge for the elevated studio.

The studio relaunches itself elevated (``app.elevation``), and Windows' UIPI
forbids an OLE drag from a medium-integrity Explorer into a high-integrity
window.  Qt receives external drops through an OLE drop target, so in the
normal (elevated) configuration every drag was silently refused: the dialog
import worked, dragging did not.

Windows still delivers the legacy ``WM_DROPFILES`` message across integrity
levels, but only if

* the window calls ``DragAcceptFiles``,
* the message is allowed through UIPI with ``ChangeWindowMessageFilterEx``
  (``WM_DROPFILES``, ``WM_COPYDATA`` and ``WM_COPYGLOBALDATA``), and
* no OLE drop target is registered on the window -- otherwise Explorer keeps
  using OLE and the drop is refused before any message is sent.

``RevokeDragDrop`` therefore removes Qt's OLE target for the top-level window
and this module feeds the dropped paths into the regular
``FileDropRouter``/``MainWindow.import_files`` path.  The cost is Qt's own
in-window drag-and-drop (profile reordering) while elevated, so the Profiles
page offers Move up / Move down controls in that mode.

Everything is gated on Windows + an elevated process + a real ``windows``
platform plugin, so the offscreen test suite never touches the native APIs.
"""

from __future__ import annotations

import ctypes
import logging
import os
from ctypes import wintypes

from PySide6.QtCore import QAbstractNativeEventFilter, QTimer
from PySide6.QtGui import QGuiApplication

_log = logging.getLogger("sm809.drop")

WM_DROPFILES = 0x0233
WM_COPYDATA = 0x004A
WM_COPYGLOBALDATA = 0x0049          # undocumented but required by Explorer
MSGFLT_ALLOW = 1

_UIPI_MESSAGES = (WM_DROPFILES, WM_COPYDATA, WM_COPYGLOBALDATA)


def _shell32():
    return ctypes.WinDLL("shell32", use_last_error=True)


def _user32():
    return ctypes.WinDLL("user32", use_last_error=True)


def _ole32():
    return ctypes.WinDLL("ole32", use_last_error=True)


def drop_paths(hdrop):
    """The local paths carried by a WM_DROPFILES ``hDrop`` value.

    ``DragQueryFileW`` is the documented accessor and works on the HDROP the
    shell passes to the window; the tests hand it a hand-built DROPFILES block
    in this process's memory, which it reads the same way.
    """
    if not hdrop:
        return []
    shell32 = _shell32()
    shell32.DragQueryFileW.argtypes = [
        wintypes.HANDLE, wintypes.UINT, wintypes.LPWSTR, wintypes.UINT]
    shell32.DragQueryFileW.restype = wintypes.UINT
    handle = wintypes.HANDLE(int(hdrop))
    try:
        count = int(shell32.DragQueryFileW(handle, 0xFFFFFFFF, None, 0))
    except Exception:
        return []
    paths = []
    for index in range(max(0, count)):
        length = int(shell32.DragQueryFileW(handle, index, None, 0))
        if length <= 0:
            continue
        buf = ctypes.create_unicode_buffer(length + 1)
        written = int(shell32.DragQueryFileW(handle, index, buf, length + 1))
        if written:
            paths.append(buf.value)
    return paths


class ElevatedDropBridge(QAbstractNativeEventFilter):
    """Turn legacy WM_DROPFILES messages into ``router.files_dropped``."""

    def __init__(self, router):
        super().__init__()
        self._router = router
        self._app = QGuiApplication.instance()
        self._hwnds = set()
        self._installed = False
        self._shell32 = _shell32()
        # HDROP is pointer-sized; without argtypes ctypes would truncate it.
        self._shell32.DragAcceptFiles.argtypes = [wintypes.HWND, wintypes.BOOL]
        self._shell32.DragFinish.argtypes = [wintypes.HANDLE]
        self._shell32.DragFinish.restype = None

    # -- installation ---------------------------------------------------------
    def attach(self, window):
        """Register one top-level window for legacy file drops."""
        try:
            hwnd = int(window.winId())
        except Exception:
            return False
        if not hwnd:
            return False
        self._prepare(hwnd)
        self._hwnds.add(hwnd)
        if not self._installed and self._app is not None:
            self._app.installNativeEventFilter(self)
            self._installed = True
        # Qt may register its OLE drop target after the window is shown; a
        # second revocation shortly afterwards keeps the legacy path in use.
        QTimer.singleShot(500, self.refresh)
        return True

    def refresh(self):
        """Re-apply the registration (Qt may register its OLE target late)."""
        for hwnd in list(self._hwnds):
            self._prepare(hwnd)

    def _prepare(self, hwnd):
        user32 = _user32()
        user32.ChangeWindowMessageFilterEx.argtypes = [
            wintypes.HWND, wintypes.UINT, wintypes.DWORD, ctypes.c_void_p]
        user32.ChangeWindowMessageFilterEx.restype = wintypes.BOOL
        for message in _UIPI_MESSAGES:
            user32.ChangeWindowMessageFilterEx(hwnd, message, MSGFLT_ALLOW, None)
        self._shell32.DragAcceptFiles(wintypes.HWND(hwnd), True)
        # Without this Explorer keeps using OLE; cross-integrity OLE is
        # refused and no WM_DROPFILES is ever sent.
        ole32 = _ole32()
        try:
            ole32.RevokeDragDrop.argtypes = [wintypes.HWND]
            ole32.RevokeDragDrop.restype = ctypes.c_long
            ole32.RevokeDragDrop(wintypes.HWND(hwnd))
        except Exception:
            pass

    def detach(self):
        if self._installed and self._app is not None:
            self._app.removeNativeEventFilter(self)
        self._installed = False
        for hwnd in list(self._hwnds):
            try:
                self._shell32.DragAcceptFiles(wintypes.HWND(hwnd), False)
            except Exception:
                pass
        self._hwnds.clear()

    # -- messages -------------------------------------------------------------
    def event_type(self):
        """The Qt native event type that carries a Windows ``MSG``."""
        return b"windows_generic_MSG"

    def handle_message(self, msg):
        """Handle one ``MSG``; True when it was a drop for our windows."""
        if not self._hwnds or int(msg.message) != WM_DROPFILES:
            return False
        if int(msg.hWnd) not in self._hwnds:
            return False
        hdrop = int(msg.wParam)
        try:
            paths = drop_paths(hdrop)
        finally:
            self._finish(hdrop)
        if paths:
            self._router.offer(paths)
        return True

    def _finish(self, hdrop):
        """Release the shell's drop handle (faked in the offline tests)."""
        try:
            self._shell32.DragFinish(wintypes.HANDLE(hdrop))
        except Exception:
            pass

    def nativeEventFilter(self, event_type, message):
        try:
            if event_type != self.event_type():
                return False, 0
            msg = wintypes.MSG.from_address(int(message))
        except Exception:
            return False, 0
        return (True, 0) if self.handle_message(msg) else (False, 0)


def _platform_is_windows():
    try:
        return QGuiApplication.platformName() == "windows"
    except Exception:
        return False


def attach_elevated_drop(router, window):
    """Install the bridge when this process really needs it, else None."""
    if os.name != "nt" or not _platform_is_windows():
        return None
    from .elevation import is_admin
    if not is_admin():
        return None
    bridge = ElevatedDropBridge(router)
    if not bridge.attach(window):
        return None
    _log.info("elevated: file drops use the Windows WM_DROPFILES path")
    return bridge
