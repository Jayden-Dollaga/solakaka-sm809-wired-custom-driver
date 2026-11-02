"""Gun (recoil pattern) library, encoding budget and binding round-trips.

Everything here is offline: patterns are encoded into an in-memory Profile
record, and the store writes to a temporary JSON file. No USB traffic and no
vendor files are touched.
"""

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from wired import protocol as P
from wired.bridge import (
    binding_from_entry,
    config_to_profile,
    describe_binding,
    gun_rows_fit,
    profile_to_config,
)
from wired.model import MAX_BULLETS, Profile


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def row(x=0, y=0, delay=10):
    return [x, y, delay]


def test_gun_encoded_size_matches_firmware_table():
    # A zero row is a 4-byte advance (timing, 0xF0, 0x81, 0xF0); a real
    # offset row is 8 bytes.
    assert P.gun_encoded_size([row()]) == 6
    assert P.gun_encoded_size([row(3, -2)]) == 10
    assert P.gun_encoded_size([row(), row(3, -2)]) == 14

    # 30 idle rows still fit (the firmware's default table shape); the
    # >15-row marker adds four bytes.
    assert P.gun_encoded_size([row() for _ in range(MAX_BULLETS)]) == 126
    assert P.gun_fits([row() for _ in range(MAX_BULLETS)])[0]

    # 15 real rows fit; the 16th crosses the 128-byte table.
    fifteen = [row(i + 1, i + 1) for i in range(15)]
    sixteen = [row(i + 1, i + 1) for i in range(16)]
    assert P.gun_fits(fifteen)[0]
    ok, message = P.gun_fits(sixteen)
    assert not ok and "128" in message

    # an empty pattern has nothing to fire
    ok, message = P.gun_fits([])
    assert not ok and "at least one" in message

    assert gun_rows_fit(fifteen)[0]
    assert not gun_rows_fit(sixteen)[0]


def test_gun_block_rejects_oversized_pattern():
    from wired.model import Bullet

    prof = Profile()
    entry = prof.button(0)
    entry.action = 0x79
    entry.set_bullets([Bullet(i + 1, i + 1, 10) for i in range(16)])
    with pytest.raises(P.PacketError):
        P.build_gun_block(entry)

    entry.set_bullets([Bullet(i + 1, i + 1, 10) for i in range(15)])
    block = P.build_gun_block(entry)
    assert len(block) == 128


def test_zero_movement_gun_binding_is_rejected():
    """A size-valid but all-idle pattern would silently do nothing."""
    from wired.bridge import gun_binding_problem

    assert "no movement" in gun_binding_problem([row(), row()])
    assert gun_binding_problem([row(), row(1, 2)]) == ""

    # config_to_profile must disable the slot instead of writing a dead table
    config = {"buttons": [{"gun": "idle", "name": "Idle", "repeat": 1,
                           "rows": [row() for _ in range(30)]}]}
    entry = config_to_profile(Profile(), config).button(0)
    assert entry.action == 0x00
    assert entry.count == 0


def test_gun_store_clamps_sanitises_and_persists(tmp_path):
    from app.gun_store import GunStore, clean_rows, default_rows

    g = GunStore(path=str(tmp_path / "guns.json"))
    assert g.all() == []

    gun = g.add("AK")
    assert gun["name"] == "AK"
    assert len(gun["rows"]) == MAX_BULLETS

    # out-of-range values are clamped to the device limits
    g.set_row(gun["id"], 0, 999, -999, 99999, persist=False)
    assert gun["rows"][0] == [255, -255, 2550]
    assert g.dirty

    # more rows than the device carries are truncated, junk rows dropped
    dirty = ([row(i + 1, 0) for i in range(40)]
             + [["bad"], None, object()])
    assert len(clean_rows(dirty)) == MAX_BULLETS
    assert default_rows() == [row() for _ in range(MAX_BULLETS)]

    g.save_if_dirty()
    assert not g.dirty
    reloaded = GunStore(path=str(tmp_path / "guns.json"))
    assert reloaded.all()[0]["rows"][0] == [255, -255, 2550]


def test_gun_store_adopts_device_rows_without_overwriting_edits(tmp_path):
    from app.gun_store import GunStore

    g = GunStore(path=str(tmp_path / "guns.json"))
    first = [row(1, 1), row(2, -2)]
    adopted = g.add_with_id("dev:prof:0", "AK", first, persist=False)
    assert adopted["name"] == "AK"
    assert adopted["rows"] == first

    # a fresh/default record picks up a later scan
    g.set_rows("dev:prof:0", [row() for _ in range(MAX_BULLETS)], persist=False)
    g.add_with_id("dev:prof:0", "AK", [row(7, -7)], persist=False)
    assert g.get("dev:prof:0")["rows"][0] == [7, -7, 10]

    # a user-edited pattern is never clobbered by a profile scan
    custom = [row(9, 9, 20)]
    g.set_rows("dev:prof:0", custom, persist=False)
    g.add_with_id("dev:prof:0", "AK", [row(1, 1)], persist=False)
    assert g.get("dev:prof:0")["rows"] == custom

    # an unknown id is created on demand
    g.add_with_id("dev:prof:1", "M4", [row(4, 0)], persist=False)
    assert len(g.all()) == 2


def test_gun_binding_round_trips_through_a_profile():
    rows = [row(3, -2, 20), row(-1, 4, 30), row()]
    config = {
        "buttons": [{"gun": "abc123", "name": "AK", "rows": rows,
                     "repeat": 2}],
    }
    prof = config_to_profile(Profile(), config)
    entry = prof.button(0)

    assert entry.action == 0x79
    assert entry.count == 3
    assert entry.loop == 2
    assert entry.name == "AK"
    assert [[r.x, r.y, r.delay] for r in entry.bullet_slice()] == rows

    binding = binding_from_entry(entry, 0, "prof")
    assert binding["gun"] == "dev:prof:0"
    assert binding["name"] == "AK"
    assert binding["rows"] == rows
    assert binding["repeat"] == 2
    assert describe_binding(binding) == "Gun: AK (x2)"

    # the studio preview reads the same binding back out of the profile
    again = profile_to_config(prof, "prof")
    assert again["buttons"][0]["gun"] == "dev:prof:0"
    assert again["buttons"][0]["rows"] == rows
    # a second write is idempotent
    config_to_profile(prof, again)
    assert prof.button(0).action == 0x79
    assert prof.button(0).count == 3


def test_oversized_gun_binding_disables_the_slot():
    config = {
        "buttons": [{"gun": "big", "name": "Too big", "repeat": 3,
                     "rows": [row(i + 1, i + 1) for i in range(30)]}],
    }
    prof = config_to_profile(Profile(), config)
    entry = prof.button(0)
    assert entry.action == 0x00
    assert entry.count == 0


def test_gun_rows_are_resolved_from_the_library_when_not_embedded():
    config = {"buttons": [{"gun": "lib1", "name": "Lib", "repeat": 1}]}
    prof = config_to_profile(
        Profile(), config,
        gun_rows=lambda gid: [row(5, 5)] if gid == "lib1" else None)
    assert prof.button(0).action == 0x79
    assert prof.button(0).count == 1

    # a binding that resolves to nothing is disabled, not fatal
    prof2 = config_to_profile(
        Profile(), {"buttons": [{"gun": "missing"}]},
        gun_rows=lambda gid: None)
    assert prof2.button(0).action == 0x00


def test_recoil_recorder_accumulates_deltas():
    from app.recoil_recorder import RecoilRecorder

    rec = RecoilRecorder()
    rec.feed(2, -1)
    rec.feed(3, 4)
    assert rec.take_delta() == (5, 3)
    assert rec.take_delta() == (0, 0)      # the accumulator is cleared
    rec.feed(-7, 0)
    assert rec.take_delta() == (-7, 0)


def test_gun_panel_records_and_trims_trailing_idle_rows(qapp, tmp_path):
    from app.gun_store import GunStore
    from app.panels.gun_panel import GunPanel

    store = GunStore(path=str(tmp_path / "guns.json"))
    panel = GunPanel(store)
    panel.ARM_MS = 10**9                  # drive sampling by hand
    panel.recorder.start = lambda: True
    panel.recorder.stop = lambda: None

    panel.new_gun()
    gid = store.all()[0]["id"]
    panel.bullets.setValue(4)
    panel.record_interval.setValue(100)
    panel._start_recording()
    assert panel._recording
    assert panel.record_btn.text().endswith("Stop")
    panel._begin_sampling(panel._record_token)

    panel.recorder.feed(2, -1)
    panel._record_sample()
    panel.recorder.feed(3, 0)
    panel._record_sample()
    panel._record_sample()                # idle shot, kept in the middle
    panel.recorder.feed(0, 4)
    panel._record_sample()                # reaches the bullet count

    rows = store.get(gid)["rows"]
    assert rows == [[2, -1, 100], [3, 0, 100], [0, 0, 100], [0, 4, 100]]
    assert not panel._recording
    assert panel.record_btn.text().endswith("Record")
    assert panel.bullets.isEnabled()
    assert "Recorded 4" in panel.record_status.text()

    # flipping an axis negates that column and persists it
    panel._flip_axis(1)
    assert [r[1] for r in store.get(gid)["rows"]] == [1, 0, 0, -4]
    panel._flip_axis(0)
    assert [r[0] for r in store.get(gid)["rows"]] == [-2, -3, 0, 0]

    # a recording with no movement leaves the tuned pattern untouched
    panel.bullets.setValue(3)
    before = [list(r) for r in store.get(gid)["rows"]]
    panel._start_recording()
    panel._begin_sampling(panel._record_token)
    panel._record_sample()
    panel._record_sample()
    panel._record_sample()
    assert store.get(gid)["rows"] == before
    assert "No movement" in panel.record_status.text()


def test_gun_panel_recording_stops_at_the_byte_budget(qapp, tmp_path):
    from app.gun_store import GunStore
    from app.panels.gun_panel import GunPanel

    store = GunStore(path=str(tmp_path / "guns.json"))
    panel = GunPanel(store)
    panel.ARM_MS = 10**9
    panel.recorder.start = lambda: True
    panel.recorder.stop = lambda: None
    panel.new_gun()
    gid = store.all()[0]["id"]
    panel.bullets.setValue(30)
    panel._start_recording()
    panel._begin_sampling(panel._record_token)
    for i in range(30):
        panel.recorder.feed(i + 1, i + 1)
        panel._record_sample()
        if not panel._recording:
            break
    rows = store.get(gid)["rows"]
    assert len(rows) == 15                # 15 offset rows fit in 128 bytes
    assert not panel._recording
    assert "128" in panel.record_status.text()
