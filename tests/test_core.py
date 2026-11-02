"""Offline tests for the wired SM809 studio core.

No hardware I/O is performed: every test works on a temporary copy of the
shipped seed data. The original vendor installation is never touched.
"""

import ctypes
import os
import shutil
import tempfile
from pathlib import Path

# wired.paths resolves DATA_DIR at import time, so point it at a scratch folder
# before importing anything from the wired/sm809pro/app packages.
_SCRATCH = Path(tempfile.mkdtemp(prefix="sm809-tests-"))
os.environ["SM809_DATA_DIR"] = str(_SCRATCH)

import pytest

from wired import transport as T
from wired.bridge import (
    dpi_from_display,
    dpi_to_display,
    rate_hz,
    rate_index,
)
from wired.model import PROFILE_COUNT, PROFILE_SIZE, Profile
from wired.paths import DATA_DIR, DEVICE_DATA_DIR, SEED_DIR, ensure_data_dir
from wired.protocol import rate_frame, sensor_display_dpi

from app.profile_store import ProfileStore, default_config


@pytest.fixture(scope="module")
def seeded():
    root = ensure_data_dir()
    assert (root / "Data" / "profile.bin").exists()
    return root


@pytest.fixture
def store(tmp_path):
    """A ProfileStore over an isolated copy of the seed data."""
    dest = tmp_path / "data"
    shutil.copytree(SEED_DIR, dest)
    return ProfileStore(path=str(tmp_path / "profiles.json"), data_dir=dest)


def trim(store, keep=3):
    """Leave exactly `keep` profiles.

    The shipped seed contains a single default profile, so top up first when a
    test needs a populated library.
    """
    while len(store.all()) < keep:
        store.add(f"Profile {len(store.all()) + 1}")
    while len(store.all()) > keep:
        store.delete(store.all()[-1]["id"])
    assert len(store.all()) == keep


def test_seed_is_copied_and_device_files_exist(seeded):
    assert seeded == DATA_DIR
    assert (seeded / "Data.ini").exists()
    for name in ("Data.bin", "profile.bin", "Default.pbin", "macro.bin", "gun.bin"):
        assert (DEVICE_DATA_DIR / name).exists(), name
    # the seed stays intact as the pristine copy
    assert (SEED_DIR / "Data" / "Default.pbin").exists()


def test_seed_ships_only_the_factory_default_profile():
    """A new install starts with one default profile, never the vendor's
    sample profile library."""
    from wired.model import DataStore

    store = DataStore(SEED_DIR / "Data")
    assert len(store.profiles) == 1
    assert store.profiles[0].name == "Profile"
    # the profile must match the factory template the app resets to
    default = (SEED_DIR / "Data" / "Default.pbin").read_bytes()[:PROFILE_SIZE]
    seeded = store.profiles[0].raw
    assert bytes(seeded[0x64:]) == default[0x64:]   # everything after the name


def test_profile_store_reads_wired_profiles(store):
    profiles = store.all()
    assert 1 <= len(profiles) <= PROFILE_COUNT
    active = store.active()
    assert active is not None
    cfg = active["config"]
    assert len(cfg["buttons"]) == 64
    assert 1 <= cfg["dpi"]["enabled_count"] <= 8
    assert cfg["polling_hz"] in (125, 250, 500, 1000)
    assert 0 <= cfg["lighting"]["mode"] <= 11
    assert {"speed", "scroll", "double", "enhance", "onepage",
            "wheel_reverse"} <= set(cfg["pointer"])


def test_profile_limit(store):
    trim(store, keep=PROFILE_COUNT - 2)
    store.add("Extra A")
    store.add("Extra B")
    assert store.at_limit()
    with pytest.raises(ValueError):
        store.add("One Too Many")


def test_config_round_trip(store):
    pid = store.active_id
    cfg = store.config(pid)
    cfg["lighting"].update({"mode": 9, "brightness": 120, "frequency": 1,
                            "length": 2, "direction": 1, "color": [10, 20, 30]})
    cfg["polling_hz"] = 1000
    cfg["pointer"].update({"speed": 8, "scroll": 4, "double": 6,
                           "enhance": True, "onepage": True})
    cfg["buttons"][0] = (0x15, 0x01, 0x06)       # Ctrl+C
    cfg["buttons"][1] = (0x0A, 30, 4)            # fire click
    cfg["buttons"][2] = {
        "macro": "dev:test:2",
        "name": "Test Macro",
        "playmode": 2,
        "repeat": 5,
        "events": [
            {"type": "key", "keycode": 0x04, "down": True, "next_delay": 20},
            {"type": "key", "keycode": 0x04, "down": False, "next_delay": 0},
        ],
    }
    store.set_config(pid, cfg)

    idx = store.index_of(pid)
    prof = store.data.profiles[idx]
    assert prof.light_mode == 9
    assert prof.brightness == 120
    assert prof.frequency == 1
    assert prof.rate == rate_index(1000)
    assert prof.button(0).shortcut_mods == 1
    assert prof.button(0).shortcut_key == 0x06
    assert prof.button(1).action == 0x0A
    assert prof.button(1).fire_interval == 30
    entry = prof.button(2)
    assert entry.action == 0x16
    assert entry.count == 2
    assert entry.loop == 5
    assert entry.name == "Test Macro"

    # a fresh store over the same files yields the same config
    again = ProfileStore(path=str(store.path), data_dir=store.data_dir)
    cfg2 = again.config(pid)
    assert cfg2["lighting"]["mode"] == 9
    assert cfg2["polling_hz"] == 1000
    assert tuple(cfg2["buttons"][0]) == (0x15, 1, 0x06)
    assert cfg2["buttons"][2]["name"] == "Test Macro"
    assert cfg2["buttons"][2]["events"][0]["keycode"] == 0x04


def test_wheel_reverse_swaps_wheel_slots(store):
    pid = store.active_id
    cfg = store.config(pid)
    assert not cfg["pointer"]["wheel_reverse"]
    cfg["pointer"]["wheel_reverse"] = True
    store.set_config(pid, cfg)
    prof = store.data.profiles[store.index_of(pid)]
    assert prof.button(30).action == 0x0C
    assert prof.button(31).action == 0x0B
    assert store.config(pid)["pointer"]["wheel_reverse"] is True

    cfg = store.config(pid)
    cfg["pointer"]["wheel_reverse"] = False
    store.set_config(pid, cfg)
    prof = store.data.profiles[store.index_of(pid)]
    assert prof.button(30).action == 0x0B
    assert prof.button(31).action == 0x0C


def test_dpi_conversion_matches_sensor():
    sensor = 0x0CEF
    assert dpi_to_display(sensor, 16) == 1600
    assert dpi_from_display(sensor, 1600) == 16
    assert sensor_display_dpi(sensor, 228) == 22800
    assert rate_hz(0) == 125 and rate_hz(3) == 1000
    assert rate_index(500) == 2


def test_polling_rate_sends_the_firmware_interval():
    """1000 Hz must send a 1 ms interval, not the 8 ms one.

    The wired firmware's 0x01 payload is the poll interval in milliseconds
    (FUN_00418a40: option 0 -> 8, 1 -> 4, 2 -> 2, 3 -> 1), so an inverted
    table makes the mouse poll at 125 Hz while the UI says 1000.
    """
    profile = Profile()
    for hz, interval in ((125, 8), (250, 4), (500, 2), (1000, 1)):
        profile.rate = rate_index(hz)
        packet = rate_frame(profile)
        assert packet[0] == 0x01
        assert packet[1] == interval, f"{hz} Hz -> {packet[1]} ms"


def test_factory_default_config_is_wired_shaped():
    cfg = default_config()
    assert len(cfg["buttons"]) == 64
    assert cfg["lighting"]["mode"] in range(12)
    assert cfg["pointer"]["speed"] in range(1, 12)


def test_export_import_pbin_matches_official_driver(store, tmp_path):
    """The .pbin the official driver exports/imports is one 0x1CC50 record."""
    pid = store.active_id
    name = store.get(pid)["name"]
    # exercise the profile fields the Performance page owns, including the
    # key-response byte that the original stores at +0x138
    prof = store.data.profiles[store.index_of(pid)]
    prof.key_response = 17
    prof.speed = 9
    prof.scroll = 7
    prof.double = 4

    out = tmp_path / "exported.pbin"
    store.export_pbin(pid, out)
    assert out.stat().st_size == PROFILE_SIZE
    blob = out.read_bytes()
    # the driver reads the profile name from the first wide string
    assert name.encode("utf-16-le") in blob[:200]

    # make room, then import the exported record
    if len(store.all()) < 2:
        store.add("Import Target")
    victim = store.all()[-1]["id"]
    if victim == pid:
        victim = store.all()[0]["id"]
    store.delete(victim)
    imported = store.import_pbin(out)
    assert imported["name"] == name
    cfg = store.get(imported["id"])["config"]
    assert cfg["key_response"] == 17
    assert cfg["pointer"]["speed"] == 9
    assert cfg["pointer"]["scroll"] == 7
    assert cfg["pointer"]["double"] == 4
    assert Profile.from_file(out).key_response == 17


def test_profile_operations(store):
    trim(store, keep=5)
    first = store.add("Alpha")
    second = store.add("Beta")
    assert store.get(first["id"])["name"] == "Alpha"
    store.rename(second["id"], "Beta Renamed")
    assert store.get(second["id"])["name"] == "Beta Renamed"
    dup = store.duplicate(first["id"])
    assert dup is not None and dup["name"].startswith("Alpha")
    before = len(store.all())
    store.delete(dup["id"])
    assert len(store.all()) == before - 1


# -- overlapped monitor reads -------------------------------------------------
# ReadFile on a FILE_FLAG_OVERLAPPED HID handle reports ERROR_IO_PENDING for
# every report that has not arrived yet.  Treating that as a hard failure used
# to free the OVERLAPPED/frame while the kernel still owned it (exit 139 a
# second after "device linked").  These tests pin the decision table down
# without touching hardware.

def _fake_overlapped_lib(monkeypatch, *, last_error, wait_result,
                         completion_ok=True, read_len=4):
    calls = {"wait": 0, "cancel": 0, "close_event": 0}

    class FakeKernel32:
        def CreateEventW(self, *args):
            return 1

        def CloseHandle(self, handle):
            calls["close_event"] += 1

        def ReadFile(self, handle, buf, size, read, ov):
            return 0                      # FALSE: see GetLastError

        def WaitForSingleObject(self, event, ms):
            calls["wait"] += 1
            calls["wait_ms"] = ms
            return wait_result

        def CancelIoEx(self, handle, ov):
            calls["cancel"] += 1
            return 1

        def GetOverlappedResult(self, handle, ov, read, wait):
            if completion_ok:
                read._obj.value = read_len
                return 1
            return 0

    lib = T.HidLibrary.__new__(T.HidLibrary)
    lib.kernel32 = FakeKernel32()
    monkeypatch.setattr(ctypes, "get_last_error", lambda: last_error)
    return lib, calls


def test_monitor_read_waits_on_io_pending(monkeypatch):
    lib, calls = _fake_overlapped_lib(
        monkeypatch, last_error=T.ERROR_IO_PENDING, wait_result=T.WAIT_OBJECT_0
    )
    data = lib.read_input_once(1, 500)
    assert data is not None and len(data) == 4
    assert calls["wait"] == 1 and calls["wait_ms"] == 500
    assert calls["cancel"] == 0
    assert calls["close_event"] == 1


def test_monitor_read_timeout_cancels_before_freeing(monkeypatch):
    lib, calls = _fake_overlapped_lib(
        monkeypatch, last_error=T.ERROR_IO_PENDING,
        wait_result=T.WAIT_TIMEOUT, completion_ok=False,
    )
    assert lib.read_input_once(1, 500) is None
    assert calls["wait"] == 1
    assert calls["cancel"] == 1          # kernel finished before we returned
    assert calls["close_event"] == 1


def test_monitor_read_hard_error_returns_without_waiting(monkeypatch):
    lib, calls = _fake_overlapped_lib(
        monkeypatch, last_error=87, wait_result=T.WAIT_OBJECT_0
    )
    assert lib.read_input_once(1, 500) is None
    assert calls["wait"] == 0
    assert calls["cancel"] == 0
    assert calls["close_event"] == 1


def test_keys_page_matches_vendor_physical_order():
    """Physical rows follow res\buttonpage.xml, not firmware slot order."""
    from sm809pro import actions as A

    office = [5, 6, 7, 8, 9, 10, 12, 13, 11, 14, 15, 0, 1, 2, 3, 4]
    assert [A.slot_for_physical(p, 0) for p in range(1, 17)] == office
    assert [A.slot_for_physical(p, 1) for p in range(1, 17)] == [32 + s for s in office]
    # PERMUTE keeps the reference studio's direction: slot -> 0-based physical.
    for slot in range(16):
        assert A.PHYS_ORDER[A.PERMUTE[slot]] == slot


def test_factory_keys_map_to_reference_numbers(seeded):
    from sm809pro import actions as A

    codes = A.default_button_codes()
    by_row = [codes[A.PHYS_ORDER[i]] for i in range(16)]
    expected = [
        A.BTN["display_desktop"], (0x15, 0, A.HID["2"]), (0x15, 0, A.HID["3"]),
        A.BTN["forward"], (0x15, 0, A.HID["5"]), (0x15, 0, A.HID["6"]),
        (0x15, 0, A.HID["7"]), (0x15, 0, A.HID["8"]), A.BTN["back"],
        (0x0A, 2, 0), A.BTN["my_computer"], A.BTN["left"], A.BTN["right"],
        A.BTN["middle"], A.BTN["dpi_up"], A.BTN["dpi_down"],
    ]
    assert by_row == expected
    # Reordering a physical list lands each action in its firmware slot.
    slots = A.physical_to_slots(by_row)
    assert slots[A.PHYS_ORDER[0]] == A.BTN["display_desktop"]
    assert slots[A.PHYS_ORDER[11]] == A.BTN["left"]


def test_button_table_edits_land_in_the_selected_layer(seeded):
    """An edit on the Keys page must reach the slot of the layer being edited.

    Office Mode uses firmware slots 0-15 and Game Mode 32-47 (buttonpage.xml
    and FUN_00406880).  The studio used to flip that mapping, so edits landed
    in the layer the mouse was not running and appeared to be ignored.  This
    pins both the layer mapping and the 0x12 table encoding that carries it.
    """
    from sm809pro import actions as A
    from wired.bridge import binding_to_entry
    from wired.config import load_config
    from wired.protocol import build_button_slots, mode_frame

    prof = Profile.from_file(DEVICE_DATA_DIR / "Default.pbin")
    cfg = load_config(DATA_DIR / "Data.ini")

    office_slot = A.slot_for_physical(6, 0)     # side pad row 6 -> slot 10
    game_slot = A.slot_for_physical(12, 1)      # primary left -> slot 32
    assert (office_slot, game_slot) == (10, 32)
    binding_to_entry(prof.button(office_slot), (0x0B, 0, 0))   # Scroll Up
    binding_to_entry(prof.button(game_slot), (0x0C, 0, 0))     # Scroll Down

    slots, _, _ = build_button_slots(prof, cfg)
    assert slots[office_slot * 4:office_slot * 4 + 4] == bytes((0x04, 0, 0x01, 0))
    assert slots[game_slot * 4:game_slot * 4 + 4] == bytes((0x04, 0, 0x02, 0))

    # 0x02 payload carries mode+1: 1 = Office, 2 = Game.
    prof.mode = 0
    assert mode_frame(prof)[1] == 1
    prof.mode = 1
    assert mode_frame(prof)[1] == 2
