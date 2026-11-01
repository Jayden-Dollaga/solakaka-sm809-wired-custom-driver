import random

import pytest

from sm809 import protocol as p
from sm809.model import MacroEvent, Profile


def test_checksum_commit_magic():
    packet = p.frame(0x08, (0xAA, 0xCC, 0xEE, 0, 0, 0))
    assert packet == bytes((0x08, 0xAA, 0xCC, 0xEE, 0, 0, 0, 0x93))


def test_handshake_layout():
    assert p.HANDSHAKE_PLAIN == bytes((0x00, 0xAA, 0xDD, 0x3B, 0x62, 0x00, 0x00, 0xDB))
    plain, encoded = p.handshake_packets(b"FB1570")
    assert plain == p.HANDSHAKE_PLAIN
    assert encoded != plain
    assert p.deobfuscate(encoded, b"FB1570") == plain


def test_obfuscation_matches_fun_414710():
    # Known vector captured from the shipped encoder: the handshake encrypted
    # with the shipped Data.ini password.
    assert p.obfuscate(p.HANDSHAKE_PLAIN, b"FB1570") == bytes.fromhex(
        "261aad02400c445e"
    )
    # Real SM809 feature reply for a correct challenge; it decrypts to the
    # handshake magic, which is what FUN_0041bbc0 compares against.
    reply = bytes.fromhex("2618f502400c445e")
    assert p.deobfuscate(reply, b"FB1570") == bytes.fromhex("00aadd3b62000000")


def test_obfuscation_roundtrip_random():
    rng = random.Random(1234)
    for _ in range(500):
        packet = bytes(rng.randrange(256) for _ in range(8))
        key = bytes(rng.randrange(32, 127) for _ in range(6))
        assert p.deobfuscate(p.obfuscate(packet, key), key) == packet


def test_obfuscation_roundtrip_known_key():
    key = b"FB1570"
    for cmd in range(256):
        packet = p.frame(cmd, (1, 2, 3, 4, 5, 6))
        assert p.deobfuscate(p.obfuscate(packet, key), key) == packet


@pytest.mark.parametrize(
    "event, expected",
    [
        (MacroEvent(0xF0, 0, 10, 0x1234, 0x5678),
         bytes((1, 0xFB, 0x34, 0x12, 0x78, 0x56))),
        (MacroEvent(0xF0, 1, 100, 0, 0), bytes((10 | 1, 0xF0))),
        (MacroEvent(0xF0, 2, 100, 0, 0), bytes((0x8B, 0xF0))),
        (MacroEvent(0xF0, 1, 2000, 0, 0), bytes((0, 0xF0, 0, 1, 0, 100))),
        (MacroEvent(0xF0, 2, 2000, 0, 0), bytes((0x80, 0xF0, 0, 1, 0, 100))),
        (MacroEvent(0xF0, 0, 2000, 0x1234, 0x5678),
         bytes((0, 0xFB, 0x34, 0x12, 0x78, 0x56, 0, 1, 0, 100))),
    ],
)
def test_macro_event_encoding(event, expected):
    assert p.encode_macro_event(event) == expected


def test_button_frames_and_dpi_table(default_profile, shipped_config):
    slots, macro_counter, gun_counter = p.build_button_slots(default_profile, shipped_config)
    assert len(slots) == 256
    assert macro_counter == 1
    assert gun_counter == 0
    # Shipped table's first four slots are computed Left/Right/Middle/DPI+.
    assert slots[0:16] == bytes((1, 0, 0xF0, 0, 1, 0, 0xF1, 0, 1, 0, 0xF2, 0, 7, 0, 1, 0))
    frames = p.button_frames(slots)
    assert len(frames) == 4
    header, block1, block2 = frames[0]
    assert header[:3] == bytes((0x12, 1, 0x40))
    assert header[7] == (-(1 + 0x12 + 1 + 0x40)) & 0xFF
    assert len(block1) == 32 and len(block2) == 32
    assert len(p.DPI_CODE_TABLE) == 121
    assert p.dpi_code(120, 0x0CEF) == 0x8F
    assert p.dpi_code(240, 0x0CEF) == 0x8F
    assert p.dpi_code(16, 0x0CEF) == 0x12
    block = p.build_dpi_block(default_profile, 0x0CEF)
    assert len(block) == 32
    assert block[0] == 0x0B


def test_light_frames():
    prof = Profile()
    prof.light_mode = 9
    prof.brightness = 0x80
    prof.length = 3
    prof.frequency = 2
    packet = p.light_frame(prof)
    assert packet[:3] == bytes((0x0D, 0x80, 0x32))
    prof.light_mode = 2
    prof.length = 3
    packet = p.light_frame(prof)
    assert packet[1] == 1 and packet[2] == 2
    # FUN_00418a40 rewrites a stored frequency of 1 to 2.
    prof.light_mode = 5
    prof.frequency = 1
    assert p.light_frame(prof)[2] == 2


def test_palette_block():
    block = p.palette_block([0x0000FF, 0x00FF00, 0xFF0000])
    assert block[:9] == bytes((0xFF, 0, 0, 0, 0xFF, 0, 0, 0, 0xFF))
    assert block[24:] == b"\0" * 8


def test_validation_and_describe(default_profile, shipped_config):
    assert p.validate_buttons(default_profile)
    text = "\n".join(p.describe_apply(default_profile, shipped_config))
    assert "report rate" in text
    assert "button table" in text
