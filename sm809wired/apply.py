"""
sm809wired.apply -- build the packet sequence the official app sends for one profile.

build_apply() returns a list of (kind, bytes):
    "F"  plain 8-byte feature packet (scramble with protocol.encode before sending)
    "B"  32-byte output block (sent as-is on the interrupt-OUT endpoint)
    "G"  read the device's reply to the 0x83 query (pass it back in as `reply`)

Order (from the app's Apply routine, FUN_00418a40, and the capture):
  83, G, 03, 02, 01, 0B, 0C, 0D, 10/00+B, 10/01+B, 11+B, 12 x4 (+2 B each), 08
The optional 04 / 07 packets (lift-off distance, high-DPI mask) are only sent by the app
when Data.ini Distance != 0, which is 0 on this unit, so they are not built here.
Macro tables (0x13) are not built either (macro actions raise NotImplementedError).

Verified byte-for-byte against captured cycles for Profile14 in Office and Game mode
(tests/test_wired_engine.py). Lighting parameters are verified at the profile's stored
values only (see light_params); any sensor other than Sensor=3311 is NOT supported.
"""
from . import protocol as W
from .actions import slot_entry
from .profile import N_SLOTS, Profile
from .tables import dpi_code

POLLING_CODES = (8, 4, 2, 1)     # report-rate index 0..3 -> wire byte


def light_params(mode, brightness, length, frequency, direction):
    """Bytes 2 and 3 of the 0D packet, from the stored profile fields (+0xF4 brightness,
    +0xF8 length, +0xFC frequency, +0x100 direction).

    Calibrated against captures: with the stored values brightness=255, length=3,
    frequency=1, direction=2 every light mode 0..11 reproduces the packet the app sent,
    and mode 4 additionally with length 0/3/4 and brightness 0/255. Observed rules:
      * frequency 1 is sent as 2
      * modes 2/3/4 send the stored length as-is (the guide's '4 - length' is applied to
        an already inverted value)
      * modes 9/10 use (4 - length)
    Values other than those above are extrapolated, not verified."""
    f = 2 if frequency == 1 else frequency
    inv = (4 - length) & 0xFF
    if mode in (1, 5, 11):
        return brightness, f
    if mode == 2:
        return length, f
    if mode in (3, 4):
        return length, brightness
    if mode in (6, 7):
        return direction, f
    if mode == 8:
        return brightness, 1 if frequency != 0 else 0
    if mode == 9:
        return brightness, f | (inv << 4)
    if mode == 10:
        return brightness, inv
    return 0, 0


def _block(colors):
    raw = b"".join(bytes(c) for c in colors)
    return (raw + bytes(32))[:32]


def build_button_table(profile: Profile, button_ini) -> bytes:
    """256 bytes = 64 slots x 4. button_ini = protocol-independent list from
    profile.parse_button_ini(): raw slots (flag 0) are copied from Data.ini."""
    out = bytearray()
    for i in range(N_SLOTS):
        raw, flag = button_ini[i]
        if flag == 0:
            out += raw
        else:
            s = profile.slots[i]
            out += slot_entry(s.action, s.shortcut_b, s.shortcut_c, s.fire_count, s.fire_interval)
    return bytes(out)


def build_apply(profile: Profile, button_ini, reply: bytes):
    """`reply` = descrambled 8-byte reply to the 0x83 query (its bytes 1-3 and 5-6 are
    written back in the 03 packet, byte 4 forced to 0x40, like the app does)."""
    if not W.is_reply_to(0x83, reply):
        raise ValueError("reply does not echo 0x83")
    p = profile

    def f(cmd, *data):
        return ("F", W.build_packet(cmd, bytes(data)))

    b2, b3 = light_params(p.light_mode, p.brightness, p.length, p.frequency, p.direction)
    codes = bytes(dpi_code(v) for v in p.dpi_values)
    table = build_button_table(p, button_ini)

    seq = [
        f(0x83), ("G", b""),
        f(0x03, *reply[1:4], 0x40, *reply[5:7]),
        f(0x02, 2 if p.game_mode else 1),            # 01 = Office, 02 = Game (verified)
        f(0x01, POLLING_CODES[p.polling_index]),
        f(0x0B, p.active_stage + 1),
        f(0x0C, *p.fixed_rgb),
        f(0x0D, p.light_mode, b2 & 0xFF, b3 & 0xFF),
        f(0x10, 0x00, 0x18), ("B", _block(p.cycle_colors)),
        f(0x10, 0x01, 0x18), ("B", _block(p.stage_colors)),
        f(0x11, p.stage_count, 0x08), ("B", (codes + bytes(32))[:32]),
    ]
    for page in range(4):
        chunk = table[page * 64:(page + 1) * 64]
        seq.append(f(0x12, page + 1, 0x40))
        seq.append(("B", chunk[:32]))
        seq.append(("B", chunk[32:]))
    seq.append(f(0x08, 0xAA, 0xCC, 0xEE))
    return seq


def to_wire(seq, key):
    """Scramble the F packets; B blocks and G markers are unchanged."""
    return [(k, W.encode(b, key) if k == "F" else b) for k, b in seq]
