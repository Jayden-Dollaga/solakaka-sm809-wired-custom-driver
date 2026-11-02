"""Macro/gun table encoding, descriptor pairing and the 0x13 upload path.

The vendor encoder (FUN_0041ab50) numbers tables independently of the button
list, so these tests pin the two places a mismatch is silent on hardware: the
descriptor's table index and the 0x13 header that selects the table.  A table
that cannot fit is replaced by an empty entry instead of aborting the apply.
"""

import shutil

import pytest

from wired.config import DeviceConfig
from wired.device import DeviceService
from wired.model import Bullet, MacroEvent, Profile
from wired.paths import SEED_DIR
from wired.protocol import (
    build_button_slots,
    build_gun_block,
    build_macro_block,
    deobfuscate,
    macro_blocks,
    macro_table_slots,
    table_budget_messages,
    table_budget_warnings,
)
from wired.transport import HidTransport

from app.profile_store import ProfileStore


def key_event(opcode=0x04, state=1, delay=10):
    return MacroEvent(opcode=opcode, state=state, delay=delay)


def real_rows(count):
    return [Bullet(i + 1, i + 1, 10) for i in range(count)]


def full_config():
    """A config where all 64 slots are studio-controlled, like a full profile."""
    return DeviceConfig(buttons=[[0, 0, 0, 0, 1] for _ in range(64)])


# ---------------------------------------------------------------------------
# Table headers
# ---------------------------------------------------------------------------
def test_macro_header_is_big_endian_loop_count():
    """FUN_0041ab50:140-141 composes CONCAT11(low, high) -> big-endian bytes."""
    prof = Profile()
    entry = prof.button(0)
    entry.action = 0x16
    entry.loop = 0x0102
    entry.set_events([key_event(delay=23)])
    block = build_macro_block(entry)

    assert block[0] == 0x01 and block[1] == 0x02
    # first event follows the 2-byte header: timing | press, opcode
    assert block[2] == (23 // 10) | 1
    assert block[3] == 0x04


def test_gun_header_and_split_marker_follow_the_vendor_counter():
    prof = Profile()
    entry = prof.button(0)
    entry.action = 0x79
    entry.loop = 0x0102
    # 14 real + 2 idle = 16 rows and exactly 126 encoded bytes, the only
    # >15-row shape that still fits the 128-byte table.
    entry.set_bullets(real_rows(14) + [Bullet(0, 0, 10), Bullet(0, 0, 10)])

    first = build_gun_block(entry, ordinal=1)
    assert first[0] == 0x01 and first[1] == 0x02
    # First half holds 15 rows (14 real + 1 idle), then the split marker.
    marker = 2 + 14 * 8 + 4
    assert first[marker:marker + 2] == bytes((6, 0xFE))
    assert first[marker + 2:marker + 4] == bytes((0x00, 0x01))
    # the remaining idle row is the 4-byte vendor shape
    assert first[marker + 4:marker + 8] == bytes((0x01, 0xF0, 0x81, 0xF0))
    assert first[marker + 8:] == bytes(128 - marker - 8)

    second = build_gun_block(entry, ordinal=2)
    assert second[marker:marker + 2] == bytes((8, 0xFE))
    third = build_gun_block(entry, ordinal=3)
    assert third[marker:marker + 2] == bytes((10, 0xFE))


def test_left_macro_0x39_uses_macro_events_and_shares_the_gun_counter():
    prof = Profile()
    left = prof.button(3)
    left.action = 0x39                   # "Set Left Macro": macro events
    left.loop = 1
    left.set_events([key_event(opcode=0x05, delay=10)])

    gun = prof.button(4)
    gun.action = 0x79
    gun.loop = 1
    gun.set_bullets(real_rows(14) + [Bullet(0, 0, 10), Bullet(0, 0, 10)])

    blocks = dict(macro_blocks(prof))
    tables = macro_table_slots(prof)
    assert tables[3] == ("gun", 4)       # 0x39 occupies a gun-range table
    assert tables[4] == ("gun", 5)

    left_block = blocks[4]
    assert left_block[2] == (10 // 10) | 1
    assert left_block[3] == 0x05         # an opcode, not a 0xF0 gun marker

    # The 0x39 button incremented the vendor's shared counter first, so the
    # gun's split marker is the second one: (2 + 2) * 2 = 8.
    gun_block = blocks[5]
    marker = 2 + 14 * 8 + 4
    assert gun_block[marker:marker + 2] == bytes((8, 0xFE))


# ---------------------------------------------------------------------------
# Descriptor <-> table pairing
# ---------------------------------------------------------------------------
def test_every_descriptor_points_at_the_table_that_is_uploaded():
    prof = Profile()
    for slot in (0, 1):
        entry = prof.button(slot)
        entry.action = 0x16
        entry.loop = 1
        entry.set_events([key_event()])
    gun = prof.button(2)
    gun.action = 0x79
    gun.loop = 1
    gun.set_bullets([Bullet(2, 3, 10), Bullet(1, 1, 10)])

    tables = macro_table_slots(prof)
    staging, _counter, _guns = build_button_slots(prof, full_config())
    uploaded = dict(macro_blocks(prof))

    assert tables[0] == ("macro", 1)
    assert tables[1] == ("macro", 2)
    assert tables[2] == ("gun", 4)
    for slot, (_kind, index) in tables.items():
        assert staging[slot * 4 + 2] == index
        assert index in uploaded

    # The gun block carries the descriptor's repeat count and the first row.
    gblock = uploaded[4]
    assert gblock[2] == 0x01             # timing | press
    assert gblock[6:8] == bytes((2, 3))  # |x|, |y|


def test_limits_refuse_extra_macros_and_guns_without_dropping_others():
    cfg = full_config()

    # Eleven macros: the vendor keeps ten, the eleventh descriptor names no
    # table (C=0) but the ten accepted ones still point at tables 1..10.
    prof = Profile()
    for slot in range(11):
        entry = prof.button(slot)
        entry.action = 0x16
        entry.loop = 1
        entry.set_events([key_event()])
    tables = macro_table_slots(prof)
    staging, _macros, _guns = build_button_slots(prof, cfg)
    assert [slot for slot in range(10) if slot in tables] == list(range(10))
    assert 10 not in tables
    assert [staging[s * 4 + 2] for s in range(10)] == list(range(1, 11))
    assert staging[10 * 4 + 2] == 0

    # Four guns with no macros: three take tables 4..6, the fourth is left
    # unpointed exactly like the vendor's three-gun limit.
    prof = Profile()
    for slot in range(4):
        entry = prof.button(slot)
        entry.action = 0x79
        entry.loop = 1
        entry.set_bullets([Bullet(1, 1, 10)])
    tables = macro_table_slots(prof)
    staging, _macros, _guns = build_button_slots(prof, cfg)
    assert [tables[s] for s in range(3)] == [("gun", 4), ("gun", 5), ("gun", 6)]
    assert 3 not in tables
    assert staging[3 * 4:3 * 4 + 4] == bytes((0x08, 0x00, 0x00, 0x00))


def test_shared_table_budget_is_reported_not_silent():
    """Ten macros plus three guns cannot fit in indices 1..11.

    The vendor allows each cap on its own, but the two kinds share the same
    table range, so the surplus gun descriptors end up with C=0.  The apply
    path must say that instead of leaving a bound button inexplicably dead.
    """
    prof = Profile()
    for slot in range(10):
        entry = prof.button(slot)
        entry.action = 0x16
        entry.loop = 1
        entry.set_events([key_event()])
    for slot in range(10, 13):
        entry = prof.button(slot)
        entry.action = 0x79
        entry.loop = 1
        entry.set_bullets([Bullet(1, 1, 10)])

    tables = macro_table_slots(prof)
    assert tables[10] == ("gun", 11)
    assert 11 not in tables and 12 not in tables

    warnings = table_budget_warnings(prof)
    assert any("13 macro/gun tables" in w for w in warnings)
    assert any("last 2 will not work" in w for w in warnings)

    # Within the caps but still too many tables: only the shared limit fires.
    assert table_budget_messages(9, 2) == []
    shared = table_budget_messages(9, 3)
    assert len(shared) == 1 and "only 11 can be uploaded" in shared[0]

    # Each per-kind cap is reported independently.
    assert any("at most 10" in w for w in table_budget_messages(11, 0))
    assert any("at most 3" in w for w in table_budget_messages(0, 4))


def test_config_budget_counts_only_bindings_that_can_be_written():
    """The Buttons panel must count with the same rules as the encoder."""
    from wired.bridge import table_budget_problem

    key = {"type": "key", "keycode": 0x04, "down": True, "next_delay": 10}
    macros = [{"macro": f"m{i}", "events": [dict(key)]} for i in range(10)]
    guns = [{"gun": f"g{i}", "rows": [[1, 1, 10]]} for i in range(3)]
    assert "last 2" in table_budget_problem(macros + guns)

    # An all-zero gun and an empty macro are disabled by the bridge, so they
    # release their table again; the remaining surplus is only one gun.
    zero_gun = {"gun": "zero", "rows": [[0, 0, 10]]}
    empty_macro = {"macro": "empty", "events": []}
    problem = table_budget_problem(macros + guns[:2] + [zero_gun, empty_macro])
    assert "last 1" in problem and "last 2" not in problem

    # Exactly eleven tables fit: no message, so the label stays empty.
    assert table_budget_problem(macros[:8] + guns) == ""


def test_unencodable_table_becomes_empty_instead_of_aborting():
    prof = Profile()
    good = prof.button(5)
    good.action = 0x16
    good.loop = 1
    good.set_events([key_event()])

    bad = prof.button(6)
    bad.action = 0x16
    bad.loop = 1
    # 40 long-delay events encode to 242 bytes, past the 128-byte table.
    bad.set_events([key_event(delay=5000) for _ in range(40)])

    gun = prof.button(7)
    gun.action = 0x79
    gun.loop = 1
    gun.set_bullets([Bullet(2, 3, 10)])

    blocks = dict(macro_blocks(prof))
    tables = macro_table_slots(prof)
    assert tables[5] == ("macro", 1)
    assert tables[6] == ("macro", 2)
    assert tables[7] == ("gun", 4)
    assert blocks[1] != bytes(128)       # good macro intact
    assert blocks[2] == bytes(128)       # bad macro safely blank
    assert blocks[4] != bytes(128)       # gun still uploaded


def test_apply_warns_when_table_budget_is_exceeded(demo):
    svc, _transport, _store = demo
    prof = svc.store.profile
    for index in range(64):
        prof.button(index).action = 0x00
    for slot in range(10):
        entry = prof.button(slot)
        entry.action = 0x16
        entry.loop = 1
        entry.set_events([key_event()])
    for slot in range(10, 13):
        entry = prof.button(slot)
        entry.action = 0x79
        entry.loop = 1
        entry.set_bullets([Bullet(1, 1, 10)])

    result = svc.apply(apply_windows=False, persist=False)
    assert result.ok, result.error
    assert any("13 macro/gun tables" in w for w in result.warnings)


# ---------------------------------------------------------------------------
# Apply path: 0x13 header then four blocks per table
# ---------------------------------------------------------------------------
@pytest.fixture
def demo(tmp_path):
    dest = tmp_path / "data"
    shutil.copytree(SEED_DIR, dest)
    store = ProfileStore(path=str(tmp_path / "profiles.json"), data_dir=dest)
    cfg = store.device_config
    transport = HidTransport(cfg, demo=True)
    svc = DeviceService(cfg, store.data, demo=True, transport=transport)
    assert svc.connect()
    return svc, transport, store


def _plain(svc, packets):
    if svc.config.has_password:
        return [deobfuscate(p, svc.config.key) for p in packets]
    return [bytes(p) for p in packets]


def test_apply_selects_each_table_with_its_descriptor_index(demo):
    svc, transport, _store = demo
    prof = svc.store.profile
    good = prof.button(0)
    good.action = 0x16
    good.loop = 1
    good.set_events([key_event(), key_event(state=2)])
    bad = prof.button(1)
    bad.action = 0x16
    bad.loop = 1
    bad.set_events([key_event(delay=5000) for _ in range(40)])
    gun = prof.button(2)
    gun.action = 0x79
    gun.loop = 1
    gun.set_bullets([Bullet(2, 3, 10), Bullet(1, 1, 10)])

    result = svc.apply(apply_windows=False, persist=False)
    assert result.ok, result.error

    plain = _plain(svc, transport.sent_packets)
    headers = [p for p in plain if p[0] == 0x13]
    assert [p[1] for p in headers] == [1, 2, 4]
    assert all(p[2] == 0x80 for p in headers)

    tables = dict(macro_blocks(prof))
    # The unusable macro still has a header and a blank table; it must not
    # shift or suppress the tables that follow it.
    assert tables[2] == bytes(128)
    assert tables[1] != bytes(128) and tables[4] != bytes(128)

    sent = [bytes(b) for b in transport.sent_blocks]
    chunks = [block[o:o + 32] for _index, block in sorted(tables.items())
              for o in range(0, 128, 32)]
    assert len(chunks) == 12
    for n in range(0, 12, 4):
        group = chunks[n:n + 4]
        start = next((i for i in range(len(sent) - 3)
                      if sent[i:i + 4] == group), None)
        assert start is not None, f"table {n // 4} blocks were not uploaded"
