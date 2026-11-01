from __future__ import annotations

from sm809.model import MAX_EVENTS, MacroEvent
from sm809.recorder import (
    MOUSE_LEFT,
    MOUSE_MOVE,
    STATE_NONE,
    STATE_PRESS,
    STATE_RELEASE,
    MacroRecorder,
    RecorderSettings,
    event_label,
)


def _armed(mode: int = 0, fixed: int = 10, moves: bool = False) -> MacroRecorder:
    rec = MacroRecorder()
    rec.settings = RecorderSettings(mode=mode, fixed_delay=fixed, capture_moves=moves)
    rec.recording = True
    return rec


def test_key_and_mouse_events():
    rec = _armed()
    rec.dispatch_key(0x41, True)
    rec.dispatch_key(0x41, False)
    rec.dispatch_mouse(MOUSE_LEFT, True)
    events = rec.snapshot()
    assert [e.state for e in events] == [STATE_PRESS, STATE_RELEASE, STATE_PRESS]
    assert events[0].opcode == 0x04  # A key id
    assert events[2].opcode == MOUSE_LEFT
    assert all(e.delay == 10 for e in events)


def test_fixed_delay_mode():
    rec = _armed(mode=1, fixed=250)
    rec.dispatch_key(0x42, True)
    rec.dispatch_key(0x42, False)
    assert [e.delay for e in rec.snapshot()] == [250, 250]


def test_event_cap():
    rec = _armed()
    for i in range(MAX_EVENTS + 5):
        rec.dispatch_key(0x41, True)
    assert len(rec.snapshot()) == MAX_EVENTS


def test_move_capture_is_optional():
    rec = _armed(moves=False)
    rec.dispatch_move(12, 34)
    assert rec.snapshot() == []

    rec = _armed(moves=True)
    rec.dispatch_move(12, 34)
    rec.dispatch_move(13, 34)  # throttled by move_interval_ms
    events = rec.snapshot()
    assert len(events) == 1
    assert events[0].opcode == MOUSE_MOVE
    assert events[0].state == STATE_NONE
    assert (events[0].a, events[0].b) == (12, 34)


def test_callback_receives_snapshot():
    rec = _armed()
    seen: list[int] = []
    rec.on_event = lambda snapshot: seen.append(len(snapshot))
    rec.dispatch_key(0x41, True)
    rec.dispatch_key(0x41, False)
    assert seen == [1, 2]


def test_event_labels():
    assert event_label(MacroEvent(MOUSE_LEFT, STATE_PRESS)) == "Left Down"
    assert event_label(MacroEvent(MOUSE_MOVE, STATE_NONE, a=5, b=7)) == "Move to (5, 7)"
    label = event_label(MacroEvent(0x04, STATE_RELEASE))
    assert "Up" in label
