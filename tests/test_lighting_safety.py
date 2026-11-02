"""Regression tests for the lighting-tab incident.

A 1..255 "Frequency" slider used to write profile +0xFC.  That byte is the
vendor's fixed/cycle colour radio: FUN_0040e460 only ever stores 0 or 1, and
both the vendor host (FUN_00417540 indexes a two-entry control table with it)
and the firmware treat it as a small index.  An out-of-range byte such as the
legacy saved value 126 could wedge the mouse until the official driver rewrote
the profile.

Every path that can reach the device or an exported .pbin is covered here:
light-frame encoding, palette blocks, the config bridge and profile loading.
"""

import shutil

from wired.bridge import config_to_profile, profile_to_config
from wired.model import Profile
from wired.protocol import light_frame, palette_block


# ---------------------------------------------------------------------------
# 0x0D light frame
# ---------------------------------------------------------------------------
def test_light_frame_clamps_every_value():
    prof = Profile()
    prof.light_mode = 200
    prof.brightness = 999
    prof.length = 99
    prof.frequency = 126
    prof.direction = 255
    packet = light_frame(prof)
    assert packet[0] == 0x0D
    assert packet[1] == 11          # mode clamped to 0..11
    assert packet[2] == 255         # brightness clamped to 0..255
    # mode 11: byte3 = frequency; 126 clamps to 1, which the vendor maps to 2
    assert packet[3] == 2


def test_light_frame_mode_2_uses_stored_frequency_slider():
    prof = Profile()
    prof.light_mode = 2
    prof.length = 3
    prof.frequency = 0
    # FUN_00418a40 precomputes 4 - +0xF8 and subtracts it again here, so the
    # byte is the stored value itself (the old code double-inverted it).
    assert light_frame(prof)[2] == 3


def test_light_frame_modes_3_4_use_stored_slider_and_brightness():
    prof = Profile()
    prof.light_mode = 3
    prof.length = 1
    prof.brightness = 77
    packet = light_frame(prof)
    assert packet[2] == 1
    assert packet[3] == 77


def test_light_frame_trailing_length_is_inverted():
    prof = Profile()
    prof.light_mode = 6
    prof.direction = 1
    prof.frequency = 1
    packet = light_frame(prof)
    assert packet[2] == 3           # 4 - direction
    assert packet[3] == 2           # stored 1 maps to 2


def test_light_frame_mode_9_packs_frequency_and_length():
    prof = Profile()
    prof.light_mode = 9
    prof.brightness = 120
    prof.length = 2
    prof.frequency = 1
    packet = light_frame(prof)
    assert packet[2] == 120
    assert packet[3] == (2 | ((4 - 2) << 4))


# ---------------------------------------------------------------------------
# 0x10 palette blocks
# ---------------------------------------------------------------------------
def test_palette_block_packs_rgb_triples_like_the_vendor():
    """FUN_00418a40 drops each COLORREF pad byte (OVERVIEW 9.1)."""
    colors = [0x0000FF, 0x00FF00, 0xFF0000, 0x00FFFF,
              0xFF00FF, 0xFFFF00, 0x0080FF, 0xFFFFFF]
    block = palette_block(colors)
    assert len(block) == 32
    assert block == bytes([
        0xFF, 0x00, 0x00,   # red
        0x00, 0xFF, 0x00,   # green
        0x00, 0x00, 0xFF,   # blue
        0xFF, 0xFF, 0x00,   # yellow
        0xFF, 0x00, 0xFF,   # magenta
        0x00, 0xFF, 0xFF,   # cyan
        0xFF, 0x80, 0x00,   # orange-ish
        0xFF, 0xFF, 0xFF,   # white
    ]) + b"\x00" * 8


def test_palette_block_skips_the_colorref_pad_byte():
    block = palette_block([0x00ABCDEF])
    assert len(block) == 32
    assert block[:3] == b"\xEF\xCD\xAB"
    assert block[3:] == b"\x00" * 29


# ---------------------------------------------------------------------------
# Config bridge
# ---------------------------------------------------------------------------
def test_bridge_clamps_a_hostile_config():
    prof = Profile()
    config = {"lighting": {"mode": 99, "brightness": 999, "length": 99,
                           "frequency": 126, "direction": 255}}
    config_to_profile(prof, config)
    assert prof.light_mode == 11
    assert prof.brightness == 255
    assert prof.length == 4
    assert prof.frequency == 1
    assert prof.direction == 4


def test_profile_to_config_never_echoes_legacy_frequency():
    prof = Profile()
    prof.frequency = 126
    cfg = profile_to_config(prof)
    assert cfg["lighting"]["frequency"] == 1


def test_sanitize_lighting_repairs_and_reports():
    prof = Profile()
    prof.frequency = 126
    prof.direction = 200
    assert prof.sanitize_lighting() is True
    assert prof.frequency == 1
    assert prof.direction == 4
    assert prof.sanitize_lighting() is False


def test_import_pbin_sanitizes_led_bytes(tmp_path):
    from wired.model import PROFILE_COUNT, DataStore
    from wired.paths import SEED_DIR

    dest = tmp_path / "Data"
    shutil.copytree(SEED_DIR / "Data", dest)
    store = DataStore(dest)
    if len(store.profiles) >= PROFILE_COUNT:
        store.delete_profile(-1)        # make room under the 14-profile limit

    bad = Profile()
    bad.name = "Legacy"
    bad.frequency = 126
    path = tmp_path / "legacy.pbin"
    path.write_bytes(bytes(bad.raw))

    prof = store.import_profile(path)
    assert prof.frequency == 1


def test_store_load_repairs_a_corrupt_profile(tmp_path):
    from app.profile_store import ProfileStore
    from wired.paths import SEED_DIR

    dest = tmp_path / "data"
    shutil.copytree(SEED_DIR, dest)
    store = ProfileStore(path=str(tmp_path / "profiles.json"), data_dir=dest)
    pid = store.active_id
    idx = store.index_of(pid)
    store.data.profiles[idx].frequency = 126
    store.data.save_profiles()

    again = ProfileStore(path=str(tmp_path / "profiles.json"), data_dir=dest)
    assert again.data.profiles[again.index_of(pid)].frequency == 1
    assert again.config(pid)["lighting"]["frequency"] == 1
