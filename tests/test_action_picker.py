"""The Assign action dialog must follow the vendor's button menu.

The original software's right-click action menu (res/buttonmenu.xml and
Language/lan.xml) groups actions into a fixed set of submenus.  The studio
keeps its modern two-pane picker but must show the same groups and order,
with the Recoil Control pane added (the vendor hides its gun entries on the
wired build) and the vendor's "Select A Macro" shortened to "Macro".
"""

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from app.widgets import action_picker as ap
from sm809pro import actions as A


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app
    for widget in list(app.topLevelWidgets()):
        widget.close()
        widget.deleteLater()
    app.processEvents()
    app.quit()


# Top-level order is the vendor menu order, with the studio's Recoil Control
# pane after Macro (where the vendor hides Select A Gun) and no Send Gun.  The
# macro group is labelled "Macro" instead of the vendor's "Select A Macro".
VENDOR_ORDER = [
    "Basic function", "High order function", "Fire Click", "Button Off",
    "Shortcut", "Macro", "Recoil Control", "DPI", "Report", "Multimedia",
    "Windows", "Office", "Advance Function",
]

# Submenu contents and order, exactly as res/buttonmenu.xml lists them.
VENDOR_SUBMENUS = {
    "Basic function": [
        "Left Click", "Right Click", "Middle Button", "Forward", "Backward",
        "Scroll Up", "Scroll Down",
    ],
    "High order function": [
        "Double Click", "Three Click", "Light Mode Switch", "Sniper Key",
    ],
    "Button Off": ["Button Off"],
    "DPI": ["DPI Cycle", "DPI +", "DPI -"],
    "Report": ["Report Cycle", "Report +", "Report -"],
    "Multimedia": [
        "Media Player", "Play / Pause", "Stop", "Previous Track",
        "Next Track", "Volume +", "Volume -", "Mute",
    ],
    "Windows": [
        "Browser Home", "Browser Favorites", "Browser Forward",
        "Browser Backward", "Browser Stop", "Browser Refresh",
        "Browser Search", "Email", "Calculator", "My Computer",
    ],
    "Office": [
        "Cut", "Copy", "Paste", "Open", "Save", "Find", "Redo",
        "Select All", "New", "Print",
    ],
    "Advance Function": [
        "Swap Windows", "Close Window", "Show Desktop", "Lock PC",
        "Run Command", "Mode Switch",
    ],
}


def _open(code=(0, 0, 0)):
    # These tests exercise the vendor menu with the Recoil Control preview
    # turned on; the default-hidden case has its own test below.
    return ap.ActionPicker(code, developer=True)


def test_category_order_matches_the_vendor_menu():
    assert list(ap.CATEGORY_ORDER) == VENDOR_ORDER


def test_each_submenu_matches_the_vendor_menu():
    for name, labels in VENDOR_SUBMENUS.items():
        assert [label for label, _ in ap.ACTION_TREE[name]] == labels


def test_send_gun_is_not_offered(qapp):
    """The vendor hides Send Gun and this firmware has no gun table for it."""
    labels = [label for items in ap.ACTION_TREE.values() for label, _ in items]
    assert "Send Gun" not in labels
    dlg = _open()
    try:
        assert [dlg.cats.item(i).text() for i in range(dlg.cats.count())] \
            .count("Send Gun") == 0
    finally:
        dlg.close()
        dlg.deleteLater()


def test_dialog_lists_the_groups_and_submenu_items(qapp):
    dlg = _open()
    try:
        shown = [dlg.cats.item(i).text() for i in range(dlg.cats.count())]
        assert shown == VENDOR_ORDER

        dlg.cats.setCurrentRow(VENDOR_ORDER.index("Windows"))
        labels = [dlg.list_pane.item(i).text()
                  for i in range(dlg.list_pane.count())]
        assert labels == VENDOR_SUBMENUS["Windows"]
    finally:
        dlg.close()
        dlg.deleteLater()


def test_button_off_assigns_the_off_code(qapp):
    dlg = _open()
    try:
        dlg.cats.setCurrentRow(VENDOR_ORDER.index("Button Off"))
        assert dlg._current_code() == A.BTN["disable"]
        assert ap.describe_action(A.BTN["disable"]) == "Button Off"
    finally:
        dlg.close()
        dlg.deleteLater()


def test_shortcut_macro_and_gun_open_their_editors(qapp):
    dlg = _open()
    try:
        for name, pane in (("Shortcut", 1), ("Fire Click", 2),
                           ("Macro", 3), ("Recoil Control", 4)):
            dlg.cats.setCurrentRow(VENDOR_ORDER.index(name))
            assert dlg.stack.currentIndex() == pane
    finally:
        dlg.close()
        dlg.deleteLater()


def test_existing_binding_reopens_the_matching_vendor_group(qapp):
    """Re-opening a bound action must land on its vendor group, e.g. a
    browser action under Windows, not under a generic "Browser" pane."""
    dlg = _open(A.BTN["browser_home"])
    try:
        assert dlg.cats.currentRow() == VENDOR_ORDER.index("Windows")
        assert dlg.list_pane.currentItem().text() == "Browser Home"
    finally:
        dlg.close()
        dlg.deleteLater()


def test_existing_fire_click_binding_reopens_its_editor(qapp):
    """Fire Click is a custom pane; a saved 0x0A binding must reopen there
    with its interval/count instead of falling back to Basic function."""
    dlg = _open(A.fire(20, 3))
    try:
        assert dlg.cats.currentRow() == VENDOR_ORDER.index("Fire Click")
        assert dlg.stack.currentIndex() == 2
        assert dlg.fire_editor.interval.value() == 20
        assert dlg.fire_editor.count.value() == 3
    finally:
        dlg.close()
        dlg.deleteLater()


def test_existing_macro_binding_reopens_the_macro_editor(qapp):
    """The macro group is the studio-labelled Macro pane; a saved binding
    must reopen there, not under Shortcut or Basic function."""
    binding = {"macro": "m-1", "name": "Burst", "playmode": 1, "repeat": 0,
               "events": []}
    dlg = _open(binding)
    try:
        assert dlg.cats.currentRow() == VENDOR_ORDER.index("Macro")
        assert dlg.stack.currentIndex() == 3
    finally:
        dlg.close()
        dlg.deleteLater()


def test_recoil_control_is_a_hidden_developer_category(qapp):
    """Recoil Control is a work in progress: no category until Settings
    enables developer features."""
    dlg = ap.ActionPicker((0, 0, 0))
    try:
        shown = [dlg.cats.item(i).text() for i in range(dlg.cats.count())]
        assert "Recoil Control" not in shown
        assert shown == [n for n in VENDOR_ORDER if n != "Recoil Control"]
    finally:
        dlg.close()
        dlg.deleteLater()


def test_existing_recoil_binding_reopens_the_recoil_control_editor(qapp):
    """A saved pattern binding reopens under Recoil Control, even when the
    pattern is embedded in the profile rather than in the library, and even
    while developer features are off (old profiles stay inspectable)."""
    binding = {"gun": "g-1", "name": "AK", "rows": [[1, 2, 10]], "repeat": 2}
    dlg = ap.ActionPicker(binding)
    try:
        assert dlg.cats.currentRow() == VENDOR_ORDER.index("Recoil Control")
        assert dlg.stack.currentIndex() == 4
        assert dlg.gun_editor.gun.currentText() == "AK"
    finally:
        dlg.close()
        dlg.deleteLater()
