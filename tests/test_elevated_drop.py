"""Elevated-window file drops and the reorder fallback (offline).

The studio elevates by default, and Windows' UIPI blocks Explorer's OLE drag
into a high-integrity window.  ``app.win_drop`` revokes Qt's OLE target and
listens for the legacy WM_DROPFILES message instead.  These tests pin the
message-to-paths decoding and the router/panel behaviour without touching a
real drag source.
"""

import ctypes
import os
from ctypes import wintypes

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QApplication

from app import win_drop
from app.file_import import FileDropRouter
from app.panels.profiles_panel import ProfilesPanel

pytestmark = pytest.mark.skipif(os.name != "nt", reason="Windows drop messages")


class DROPFILES(ctypes.Structure):
    _fields_ = [("pFiles", wintypes.DWORD),
                ("pt", wintypes.POINT),
                ("fNC", wintypes.BOOL),
                ("fWide", wintypes.BOOL)]


def make_hdrop(paths):
    """A DROPFILES block shaped like the one the shell passes in wParam."""
    payload = ("\0".join(paths) + "\0\0").encode("utf-16-le")
    head = DROPFILES()
    head.pFiles = ctypes.sizeof(DROPFILES)
    head.fWide = True
    buf = ctypes.create_string_buffer(ctypes.sizeof(head) + len(payload))
    ctypes.memmove(buf, ctypes.byref(head), ctypes.sizeof(head))
    ctypes.memmove(ctypes.addressof(buf) + ctypes.sizeof(head),
                   payload, len(payload))
    return buf, ctypes.addressof(buf)


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def test_drop_paths_reads_a_shell_hdrop():
    paths = [r"C:\Users\me\Desktop\Delta.pbin", r"C:\Users\me\Desktop\Aim.mbin"]
    keep, address = make_hdrop(paths)
    assert win_drop.drop_paths(address) == paths
    assert keep                     # the buffer must outlive the call


def test_drop_paths_ignores_an_empty_handle(qapp):
    assert win_drop.drop_paths(0) == []


class _RecordingRouter:
    def __init__(self):
        self.calls = []

    def offer(self, paths):
        self.calls.append(list(paths))
        return True


def test_bridge_routes_only_drops_for_its_own_windows(qapp):
    router = _RecordingRouter()
    bridge = win_drop.ElevatedDropBridge(router)
    bridge._hwnds = {0x1234}
    bridge._finish = lambda hdrop: None      # fabricated buffer, not a shell handle
    keep, address = make_hdrop([r"C:\tmp\profile.bin"])

    msg = wintypes.MSG()
    msg.hWnd = 0x1234
    msg.message = win_drop.WM_DROPFILES
    msg.wParam = address
    assert bridge.handle_message(msg) is True
    assert len(router.calls) == 1
    assert router.calls[0] == [r"C:\tmp\profile.bin"]

    # A message aimed at another window is left for Windows/Qt.
    msg.hWnd = 0x9999
    assert bridge.handle_message(msg) is False
    # A non-drop message is not ours either.
    msg.hWnd = 0x1234
    msg.message = win_drop.WM_COPYDATA
    assert bridge.handle_message(msg) is False
    assert len(router.calls) == 1
    assert keep


def test_drop_router_offer_rejects_files_it_cannot_import(qapp, tmp_path):
    seen = []
    panel = ProfilesPanel()
    router = FileDropRouter(panel)
    router.files_dropped.connect(seen.append)
    try:
        junk = tmp_path / "notes.txt"
        junk.write_text("not an import", encoding="utf-8")
        assert router.offer([str(junk)]) is False
        assert seen == []

        # A macro-sized .bin is recognised even without the .mbin suffix; the
        # whole batch is forwarded so the summary can list the ignored file.
        macro = tmp_path / "macro.bin"
        macro.write_bytes(b"\0" * (0x358 * 2))
        assert router.offer([str(junk), str(macro)]) is True
        assert seen and seen[-1] == [str(junk), str(macro)]
        # The very same batch again inside the debounce window is ignored.
        assert router.offer([str(junk), str(macro)]) is False
    finally:
        router.uninstall()
        panel.close()
        panel.deleteLater()


def test_elevated_drop_is_skipped_unless_windows_and_admin(monkeypatch, qapp):
    class Dummy:
        def winId(self):
            return 1

    monkeypatch.setattr(win_drop, "_platform_is_windows", lambda: False)
    assert win_drop.attach_elevated_drop(_RecordingRouter(), Dummy()) is None

    monkeypatch.setattr(win_drop, "_platform_is_windows", lambda: True)
    monkeypatch.setattr("app.elevation.is_admin", lambda: False)
    assert win_drop.attach_elevated_drop(_RecordingRouter(), Dummy()) is None


def test_move_buttons_reorder_profiles_and_keep_custom_order(qapp):
    panel = ProfilesPanel()
    order = []
    panel.order_changed.connect(order.append)
    panel.set_profiles(
        [{"id": a, "name": n, "match_rules": []}
         for a, n in (("a", "Alpha"), ("b", "Bravo"), ("c", "Charlie"))],
        active_id="a")
    try:
        panel.sort.setCurrentIndex(1)          # pretend a sort was applied
        panel.list.setCurrentRow(0)
        assert panel.up_btn.isEnabled() is False
        assert panel.down_btn.isEnabled() is True

        assert panel.move_selected(1) is True
        assert order[-1] == ["b", "a", "c"]
        assert panel.selected_id() == "a"
        assert panel.sort.currentData() == "custom"

        assert panel.move_selected(-1) is True
        assert order[-1] == ["a", "b", "c"]

        panel.list.setCurrentRow(panel.list.count() - 1)
        assert panel.down_btn.isEnabled() is False
        assert panel.move_selected(1) is False   # already last
    finally:
        panel.close()
        panel.deleteLater()


def test_native_drop_mode_switches_the_hint_and_disables_drag(qapp):
    panel = ProfilesPanel()
    try:
        assert panel.list.dragDropMode() == QAbstractItemView.InternalMove
        panel.set_native_drop_mode(True)
        assert panel.list.dragDropMode() == QAbstractItemView.NoDragDrop
        assert "administrator" in panel.subtitle.text()
        assert "Move up" in panel.subtitle.text()

        panel.set_native_drop_mode(False)
        assert panel.list.dragDropMode() == QAbstractItemView.InternalMove
        assert "Drag to reorder" in panel.subtitle.text()
    finally:
        panel.close()
        panel.deleteLater()
