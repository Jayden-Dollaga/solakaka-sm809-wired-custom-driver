"""Typed entry for the Performance sliders.

The pointer and key-response readouts are editable like the DPI value boxes:
click the number, type digits and press Enter.  Letters and half-typed input
must never reach the pointer settings, and the slider is the one source of
truth once the value is committed.
"""

import time

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def _panel():
    from app.panels.performance_panel import PerformancePanel

    return PerformancePanel()


def _type_into(box, text, commit=True):
    box.setFocus()
    box.selectAll()
    QTest.keyClicks(box, text)
    if commit:
        QTest.keyClick(box, Qt.Key_Return)


def wait_for(app, predicate, timeout=2.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.02)
    return False


def test_typing_move_speed_moves_the_slider_and_applies(qapp):
    panel = _panel()
    seen = []
    panel.pointer_changed.connect(seen.append)

    _type_into(panel.speed_value, "9")

    assert panel.speed.value() == 9
    assert panel.speed_value.value() == 9
    assert wait_for(qapp, lambda: seen)
    assert seen[-1]["speed"] == 9
    panel.deleteLater()


def test_typing_scroll_and_double_click_speeds(qapp):
    panel = _panel()

    _type_into(panel.scroll_value, "8")
    _type_into(panel.double_value, "0")

    assert panel.scroll_lines.value() == 8
    assert panel.double.value() == 0           # zero is a valid double-click
    assert panel.double_value.text() == "0"
    panel.deleteLater()


def test_out_of_range_input_clamps_on_commit(qapp):
    """Move speed is 1-11: typed text outside the range settles on the bound
    when it is committed (the validator lets intermediate numbers through)."""
    panel = _panel()

    _type_into(panel.speed_value, "0")         # below the official minimum
    assert panel.speed.value() == 1
    assert panel.speed_value.text() == "1"

    _type_into(panel.speed_value, "19")        # above the official maximum
    assert panel.speed.value() == 11
    assert panel.speed_value.text() == "11"
    panel.deleteLater()


def test_letters_cannot_replace_a_performance_value(qapp):
    panel = _panel()
    before = (panel.speed.value(), panel.speed_value.value(),
              panel.speed_value.text())

    _type_into(panel.speed_value, "abc")

    assert (panel.speed.value(), panel.speed_value.value()) == before[:2]
    assert panel.speed_value.text() == before[2]
    panel.deleteLater()


def test_half_typed_value_waits_for_commit(qapp):
    panel = _panel()

    _type_into(panel.speed_value, "9", commit=False)

    assert panel.speed.value() == 6            # untouched until Enter/Tab away
    assert panel.speed_value.value() == 6
    panel.deleteLater()


def test_key_response_typed_ms_is_what_gets_applied(qapp):
    panel = _panel()
    seen = []
    panel.key_response_changed.connect(seen.append)

    _type_into(panel.key_response_value, "37")

    assert panel.key_response.value() == 37
    assert panel.key_response_value.value() == 37
    assert wait_for(qapp, lambda: seen)
    assert seen[-1] == 37
    panel.deleteLater()


def test_slider_keeps_the_performance_boxes_in_sync(qapp):
    panel = _panel()

    panel.speed.setValue(10)
    panel.key_response.setValue(55)

    assert panel.speed_value.text() == "10"
    assert panel.key_response_value.text() == "55"
    panel.deleteLater()


def test_profile_load_refreshes_the_boxes_without_emitting(qapp):
    panel = _panel()
    edits = []
    panel.pointer_changed.connect(edits.append)
    panel.key_response_changed.connect(edits.append)

    panel.set_state(key_response=21, pointer={
        "speed": 7, "scroll": 4, "double": 3,
        "enhance": True, "onepage": False,
    })

    assert panel.speed_value.text() == "7"
    assert panel.scroll_value.text() == "4"
    assert panel.double_value.text() == "3"
    assert panel.key_response_value.text() == "21"
    assert edits == []                        # loading a profile is not an edit
    panel.deleteLater()
