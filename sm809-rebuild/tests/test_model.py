import shutil
from pathlib import Path

import pytest

from sm809 import protocol as p
from sm809.config import load_config
from sm809.model import (
    GUN_SIZE,
    MACRO_SIZE,
    PROFILE_SIZE,
    Bullet,
    DataStore,
    GunRecord,
    MacroEvent,
    MacroRecord,
    Profile,
    read_wstr,
    u32,
)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


@pytest.fixture
def shipped_config():
    return load_config(DATA / "Data.ini")


@pytest.fixture
def default_profile():
    prof = Profile((DATA / "Data" / "Default.pbin").read_bytes())
    prof.name = "Test Profile"
    return prof


def test_config_values(shipped_config):
    assert shipped_config.vid == 0x04D9
    assert shipped_config.pid == 0xA09F
    assert shipped_config.sensor == 3311
    assert shipped_config.password == "FB1570"
    assert shipped_config.has_password
    assert len(shipped_config.buttons) == 64
    assert shipped_config.button_is_computed(0) is True
    assert shipped_config.button_is_computed(16) is False  # shipped slot 17 flag 0
    assert shipped_config.distance_values == [0, 1, 2, 0, 0, 0, 0, 0]


def test_default_profile_fields(default_profile):
    assert default_profile.name == "Test Profile"
    assert default_profile.speed == 6
    assert default_profile.scroll == 3
    assert default_profile.double == 5
    assert default_profile.rate == 3
    assert default_profile.stage_count == 8
    assert default_profile.dpi_values[:4] == [10, 16, 24, 32]
    assert default_profile.fixed_rgb == (0xFF, 0x00, 0x00)
    assert default_profile.button(0).action == 1
    assert default_profile.button(1).action == 2
    assert default_profile.button(4).action == 8


def test_profile_roundtrip(default_profile):
    blob = bytes(default_profile.raw)
    other = Profile(blob)
    assert other.name == "Test Profile"
    other.name = "Renamed"
    other.dpi_values = [100, 200, 300, 400, 500, 600, 700, 800]
    other.fixed_rgb = (1, 2, 3)
    other.button(10).action = 0x16
    other.button(10).set_events([MacroEvent(0xF0, 1, 25, 0, 0), MacroEvent(0xF0, 2, 25, 0, 0)])
    clone = Profile(bytes(other.raw))
    assert clone.name == "Renamed"
    assert clone.dpi_values[7] == 800
    assert clone.fixed_rgb == (1, 2, 3)
    assert clone.button(10).action == 0x16
    assert clone.button(10).count == 2
    assert clone.button(10).event_slice()[0].delay == 25


def test_macro_record_roundtrip():
    rec = MacroRecord()
    rec.name = "Recoil"
    rec.folder_name = ""
    rec.loop = 3
    rec.set_events([MacroEvent(0x41, 1, 10), MacroEvent(0x41, 2, 20)])
    other = MacroRecord(bytes(rec.raw))
    assert other.name == "Recoil"
    assert other.loop == 3
    assert other.count == 2
    assert other.events[1].delay == 20


def test_gun_record_roundtrip():
    rec = GunRecord()
    rec.name = "AK"
    rec.set_bullets([Bullet(1, -2, 10), Bullet(3, 4, 20)])
    other = GunRecord(bytes(rec.raw))
    assert other.name == "AK"
    assert other.count == 2
    assert other.bullets[0].x == 1 and other.bullets[0].y == -2
    assert other.bullets[1].delay == 20


def test_store_roundtrip(tmp_path):
    src = tmp_path / "data"
    src.mkdir()
    (src / "Data").mkdir()
    shutil.copy2(DATA / "Data.ini", src / "Data.ini")
    for name in ("Data.bin", "profile.bin", "Default.pbin", "macro.bin", "gun.bin"):
        shutil.copy2(DATA / "Data" / name, src / "Data" / name)
    store = DataStore(src / "Data")
    assert len(store.profiles) == 14
    # Selection and record counts come from whatever data set ships with the
    # app, so derive the expectations from the files instead of hard-coding.
    expected = int.from_bytes((src / "Data" / "Data.bin").read_bytes()[:4], "little")
    assert store.selected == expected
    assert store.profile.name
    assert len(store.macros) == (src / "Data" / "macro.bin").stat().st_size // MACRO_SIZE
    assert len(store.guns) == (src / "Data" / "gun.bin").stat().st_size // GUN_SIZE

    with pytest.raises(ValueError):
        store.add_profile("Too many")
    store.delete_profile(0)
    prof = store.add_profile("Added")
    assert prof.name == "Added"
    assert store.selected == len(store.profiles) - 1
    store.rename_profile("Renamed")
    store.save_profiles()
    store.save_macros()
    store.save_guns()

    reloaded = DataStore(src / "Data")
    assert len(reloaded.profiles) == 14
    assert reloaded.profile.name == "Renamed"
    reloaded.delete_profile(reloaded.selected)
    assert len(reloaded.profiles) == 13

    rec = reloaded.add_macro("Test Macro")
    rec.set_events([MacroEvent(0x41, 1, 10), MacroEvent(0x41, 2, 10)])
    reloaded.save_macros()
    gun = reloaded.add_gun("Test Gun")
    gun.set_bullets([Bullet(1, 1, 10)])
    reloaded.save_guns()
    again = DataStore(src / "Data")
    assert [m.name for m in again.macros][-1] == "Test Macro"
    assert again.macros[-1].count == 2
    assert again.guns[-1].name == "Test Gun"
    assert again.guns[-1].count == 1


def test_shipped_profile_names():
    blob = (DATA / "Data" / "profile.bin").read_bytes()
    assert len(blob) == PROFILE_SIZE * 14
    names = []
    for i in range(14):
        raw = blob[i * PROFILE_SIZE:(i + 1) * PROFILE_SIZE]
        names.append(read_wstr(raw, 0))
    assert all(names)
    assert len(set(names)) == 14
