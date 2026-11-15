"""Host-side recoil playback: timing, trigger edges and safety limits.

The player is driven with a fake clock, button state and move sink, so these
tests never inject input, never touch the device, and do not depend on wall
time.
"""

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from app.recoil_player import RecoilPlayer, clean_rows


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


class Rig:
    """A player wired to a mutable clock and a fake held button."""

    def __init__(self):
        self.now = 1000.0
        self.down = False
        self.sent = []
        self.events = []
        self.player = RecoilPlayer(
            clock=lambda: self.now,
            is_down=lambda _vk: self.down,
            send_move=lambda x, y: self.sent.append((x, y)),
        )
        self.player.active_changed.connect(self.events.append)

    def hold(self):
        self.down = True

    def release(self):
        self.down = False


@pytest.fixture
def rig():
    r = Rig()
    r.player.set_enabled(True)
    try:
        yield r
    finally:
        r.player.set_enabled(False)


def test_disabled_player_ignores_the_trigger(qapp):
    r = Rig()
    r.player.set_rows([[5, 2, 10], [1, 1, 10]])
    r.hold()
    r.player.tick()
    assert r.sent == []
    assert not r.player.active
    assert not r.player.enabled


def test_hold_plays_rows_at_their_delays(rig):
    rig.player.set_rows([[5, 2, 30], [3, 0, 10], [-2, 4, 0]])
    rig.hold()
    rig.player.tick()                    # first row is immediate
    assert rig.sent == [(5, 2)]
    assert rig.player.active

    rig.now += 29
    rig.player.tick()
    assert rig.sent == [(5, 2)]

    rig.now += 1                         # first delay elapsed
    rig.player.tick()
    assert rig.sent == [(5, 2), (3, 0)]

    rig.now += 10
    rig.player.tick()                    # last row has no delay
    assert rig.sent == [(5, 2), (3, 0), (-2, 4)]
    assert not rig.player.active
    assert rig.events == [True, False]


def test_zero_delay_pattern_fires_in_one_tick(rig):
    rig.player.set_rows([[1, 1, 0], [2, 2, 0], [3, 3, 0]])
    rig.hold()
    rig.player.tick()
    assert rig.sent == [(1, 1), (2, 2), (3, 3)]
    assert not rig.player.active


def test_holding_after_the_last_row_does_not_replay(rig):
    rig.player.set_rows([[4, 0, 10]])
    rig.hold()
    rig.player.tick()
    rig.player.tick()
    rig.player.tick()
    assert rig.sent == [(4, 0)]
    assert not rig.player.active

    # A fresh press restarts from the first row.
    rig.release()
    rig.player.tick()
    rig.hold()
    rig.player.tick()
    assert rig.sent == [(4, 0), (4, 0)]
    # The single row is sent and completes inside that same tick.
    assert rig.events == [True, False, True, False]


def test_releasing_mid_pattern_stops_it(rig):
    rig.player.set_rows([[1, 0, 100], [2, 0, 100]])
    rig.hold()
    rig.player.tick()
    assert rig.sent == [(1, 0)]
    rig.release()
    rig.player.tick()
    assert not rig.player.active

    # The next press starts over at the first row, not where it stopped.
    rig.hold()
    rig.player.tick()
    assert rig.sent == [(1, 0), (1, 0)]


def test_zero_offset_rows_only_wait(rig):
    rig.player.set_rows([[0, 0, 10], [7, 7, 10]])
    rig.hold()
    rig.player.tick()
    assert rig.sent == []               # idle row, no injection
    rig.now += 10
    rig.player.tick()
    assert rig.sent == [(7, 7)]


def test_enabling_while_the_button_is_held_waits_for_a_new_press():
    r = Rig()
    r.player.set_rows([[2, 2, 10]])
    r.hold()
    r.player.set_enabled(True)          # pressed before playback was enabled
    try:
        r.player.tick()
        assert r.sent == []
        r.release()
        r.player.tick()
        r.hold()
        r.player.tick()
        assert r.sent == [(2, 2)]
    finally:
        r.player.set_enabled(False)


def test_editing_the_pattern_stops_active_playback(rig):
    rig.player.set_rows([[1, 0, 100], [2, 0, 100]])
    rig.hold()
    rig.player.tick()
    assert rig.player.active
    rig.player.set_rows([[9, 9, 100]])
    assert not rig.player.active
    assert rig.events == [True, False]

    # Still held: editing alone must not restart the new pattern.
    rig.player.tick()
    assert rig.sent == [(1, 0)]


def test_changing_trigger_stops_playback(rig):
    rig.player.set_rows([[1, 0, 100], [2, 0, 100]])
    rig.hold()
    rig.player.tick()
    assert rig.player.trigger == 0x05
    rig.player.set_trigger(0x02)
    assert not rig.player.active
    assert rig.player.trigger == 0x02
    rig.player.tick()                   # the fake rig reports both buttons held
    assert rig.sent == [(1, 0)]


def test_empty_pattern_never_activates(rig):
    rig.hold()
    rig.player.tick()
    assert not rig.player.active
    assert rig.sent == []
    assert rig.events == []


def test_trigger_can_be_changed_and_disabled(rig):
    rig.player.set_trigger(0x01)
    assert rig.player.trigger == 0x01
    rig.player.set_trigger("bad")       # ignored, not an exception
    assert rig.player.trigger == 0x01
    rig.player.set_enabled(False)
    assert not rig.player.enabled
    rig.hold()
    rig.player.tick()
    assert rig.sent == []


def test_clean_rows_keeps_signs_and_rejects_junk():
    assert clean_rows([[5, -3, 20], [0, 0, 0]]) == [(5, -3, 20), (0, 0, 0)]
    assert clean_rows([[1, 2, -50]]) == [(1, 2, 0)]    # delay cannot be negative
    assert clean_rows([["bad"], None, object()]) == []
    assert clean_rows([[1, 2]]) == [(1, 2, 0)]         # missing delay = 0
    assert clean_rows(None) == []
