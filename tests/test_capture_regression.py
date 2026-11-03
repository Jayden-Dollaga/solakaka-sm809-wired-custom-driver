"""Regression tests against REAL captured USB traffic from the official app.

capture_fixtures.py holds (a) the official app's "Profile14" record reduced to the fields
the protocol layer reads (Office-mode and Game-mode variants) and (b) one complete apply
cycle for each, exactly as captured with USBPcap (F = obfuscated feature frame, B = 32-byte
block, G = reply read).  Every frame the studio builds for those profiles must equal the
captured one -- this pins the wire format to what the real app does, not to a document.
"""
import base64
import zlib
from pathlib import Path

import pytest

import capture_fixtures as CF
from wired.config import load_config
from wired.device import DeviceService
from wired.model import Profile
from wired.paths import SEED_DIR
from wired.protocol import (
    build_button_slots, build_dpi_block, commit_frame, deobfuscate, fixed_color_frame,
    frame, light_frame, mode_frame, obfuscate, palette_block, rate_frame, stage_frame,
    status_frame,
)
from wired.transport import HidTransport
from app.profile_store import ProfileStore

KEY = b"FB1570"
REPLY = bytes.fromhex("83020ff240000000")   # what the mouse answered to the 0x83 query


def _profile(b64):
    return Profile(zlib.decompress(base64.b64decode(b64)))


def _plain(expected):
    out = []
    for kind, hexs in expected:
        raw = bytes.fromhex(hexs)
        out.append((kind, deobfuscate(raw, KEY) if kind == "F" else raw))
    return out


@pytest.fixture(scope="module")
def cfg():
    return load_config(Path(SEED_DIR) / "Data.ini")


@pytest.mark.parametrize("label,b64,expected,mode_byte", [
    ("office", CF.PROFILE_OFFICE_B64, CF.EXPECTED_OFFICE, 1),
    ("game", CF.PROFILE_GAME_B64, CF.EXPECTED_GAME, 2),
])
def test_frames_match_a_captured_apply_cycle(cfg, label, b64, expected, mode_byte):
    prof = _profile(b64)
    cap = _plain(expected)
    frames = {p[0]: p for k, p in cap if k == "F"}
    blocks = [b for k, b in cap if k == "B"]

    assert mode_frame(prof) == frames[0x02] and frames[0x02][1] == mode_byte
    assert rate_frame(prof) == frames[0x01]
    assert stage_frame(prof) == frames[0x0B]
    assert fixed_color_frame(prof) == frames[0x0C]
    assert light_frame(prof) == frames[0x0D]
    assert commit_frame() == frames[0x08]
    assert status_frame(prof, REPLY) == frames[0x03]

    assert palette_block(prof.cycle_colors) == blocks[0]
    assert palette_block(prof.stage_colors) == blocks[1]
    assert build_dpi_block(prof, cfg.sensor) == blocks[2]
    slots, _, _ = build_button_slots(prof, cfg)
    assert slots == b"".join(blocks[3:])


def test_status_frame_echoes_the_device_reply_like_the_official_app():
    prof = _profile(CF.PROFILE_OFFICE_B64)
    assert status_frame(prof, REPLY).hex(" ") == "03 02 0f f2 40 00 00 b9"


def test_status_frame_lift_off_flag_only_touches_bit_3():
    prof = _profile(CF.PROFILE_OFFICE_B64)
    prof.lift = 1
    assert status_frame(prof, REPLY)[3] == 0xFA          # 0xF2 | 0x08
    prof.lift = 0
    assert status_frame(prof, bytes.fromhex("830200ff40000000"))[3] == 0xF7 & 0xFF


def test_status_frame_falls_back_without_a_usable_reply():
    prof = _profile(CF.PROFILE_OFFICE_B64)
    legacy = frame(0x03, (0x00, 0x00, 0x00, 0x40, 0, 0))
    assert status_frame(prof) == legacy
    assert status_frame(prof, b"") == legacy
    assert status_frame(prof, bytes(8)) == legacy                    # does not echo 0x83
    assert status_frame(prof, bytes.fromhex("83020ff2")) == legacy   # too short


class _EchoTransport(HidTransport):
    """Demo transport whose reply to the 0x83 query is the one captured from the mouse."""

    def get_feature(self):
        return obfuscate(REPLY, self.config.key)


def test_device_sends_the_echoed_status_frame_on_the_wire(tmp_path):
    import shutil
    dest = tmp_path / "data"
    shutil.copytree(SEED_DIR, dest)
    store = ProfileStore(path=str(tmp_path / "profiles.json"), data_dir=dest)
    transport = _EchoTransport(store.device_config, demo=True)
    svc = DeviceService(store.device_config, store.data, demo=True, transport=transport)
    svc.status_frames()
    sent = [deobfuscate(p, store.device_config.key) for p in transport.sent_packets]
    assert sent[-2][0] == 0x83
    assert sent[-1].hex(" ") == "03 02 0f f2 40 00 00 b9"
