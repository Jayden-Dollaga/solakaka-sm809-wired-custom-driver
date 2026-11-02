"""Performance-page parity and mouse-click macro recording (headless)."""

import time

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def wait_for(app, predicate, timeout=2.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.02)
    return False


def test_mouse_message_mapping():
    from app.mouse_hook import mouse_action

    assert mouse_action(0x0201) == (1, True)       # left down
    assert mouse_action(0x0202) == (1, False)      # left up
    assert mouse_action(0x0204) == (2, True)       # right
    assert mouse_action(0x0207) == (3, True)       # middle
    assert mouse_action(0x020B, 1 << 16) == (4, True)    # back (X1)
    assert mouse_action(0x020C, 2 << 16) == (5, False)   # forward (X2)
    assert mouse_action(0x020A, 120) is None       # wheel is not a macro edge
    assert mouse_action(0x0200, 0) is None         # move


def test_performance_ranges_match_official_page(qapp):
    from app.panels.performance_panel import PerformancePanel

    panel = PerformancePanel()
    assert (panel.speed.minimum(), panel.speed.maximum()) == (1, 11)
    assert (panel.scroll_lines.minimum(), panel.scroll_lines.maximum()) == (1, 11)
    assert (panel.double.minimum(), panel.double.maximum()) == (0, 10)
    assert (panel.key_response.minimum(), panel.key_response.maximum()) == (1, 100)
    assert panel.scroll_lines.value() == 3
    assert panel.key_response.value() == 4

    seen = []
    panel.key_response_changed.connect(seen.append)
    panel.key_response.setValue(12)
    assert wait_for(qapp, lambda: seen)
    assert seen[-1] == 12
    assert panel.key_response_value.text() == "12 ms"

    # loading a profile refreshes the widget without emitting an edit
    panel.set_state(key_response=7, pointer={
        "speed": 8, "scroll": 5, "double": 2,
        "enhance": True, "onepage": True, "wheel_reverse": True,
    })
    assert panel.key_response.value() == 7
    assert panel.scroll_lines.value() == 5
    assert panel.double.value() == 2
    assert panel.double_value.text() == "2"
    panel.deleteLater()


def test_macro_recorder_captures_mouse_buttons(qapp, tmp_path):
    from app.macro_store import MacroStore
    from app.panels.macro_panel import MacroPanel

    panel = MacroPanel(MacroStore(str(tmp_path / "macros.json")))
    panel.new_macro()
    # Enter the recording state without installing the global hook: the intake
    # path itself is what this test covers.
    panel._recording = True
    panel._rec_start_idx = 0
    panel._rec_last_t = None
    panel._rec_timer.restart()

    panel._on_record_key(0x04, True)
    panel._on_record_mouse(1, True)
    panel._on_record_mouse(1, False)
    panel._on_record_mouse(4, True)
    panel._on_record_mouse(4, False)
    panel._recording = False

    events = panel._cur()["events"]
    assert [(e["type"], e.get("button")) for e in events] == [
        ("key", None), ("mouse", 1), ("mouse", 1), ("mouse", 4), ("mouse", 4),
    ]
    assert [e["down"] for e in events] == [True, True, False, True, False]
    assert panel.events_table.rowCount() == len(events)
    assert panel.events_table.cellWidget(1, 2).currentData() == 1

    # an unknown button (e.g. wheel) never reaches the table
    panel._recording = True
    panel._rec_start_idx = len(events)
    panel._on_record_mouse(6, True)
    panel._recording = False
    assert len(panel._cur()["events"]) == len(events)
    panel.close()
    panel.deleteLater()
