"""
sm809wired.profile -- reader for the official app's profile records (profile.bin / .pbin).

A profile record is 0x1CC50 bytes. profile.bin is N records back to back; an exported
.pbin is exactly one. Only fields that were checked against real USB captures or raw
files are parsed here; everything else is ignored.

Layout (record-absolute offsets), verified unless marked:
  +0x000  name, UTF-16LE
  +0x080  report-rate index 0..3   (-> 8,4,2,1 on the wire; 3 = code 1 seen in captures)
  +0x084  active DPI stage, 0-based (wire 0B = value + 1)
  +0x088  8 x int32 DPI values (stored as DPI/50)
  +0x0D0  8 x COLORREF per-stage colours   (block 0x10/01)   [byte order R,G,B,x]
  +0x0F0  light mode, +0xF4 brightness, +0xF8 length, +0xFC frequency, +0x100 direction
  +0x104  fixed colour R,G,B (wire 0C)
  +0x110  8 x COLORREF cycle colours       (block 0x10/00)
  +0x139  number of DPI codes (11 header) 1..8
  +0x14C  Office/Game flag: 0 = Office, 1 = Game (wire 02 = flag + 1)
  +0x150  64 button slots x 0x72C; inside a slot:
            +0xC9 action code, +0xDC / +0xDD shortcut bytes (modifier, key),
            +0x6DC fire count, +0x6E0 fire interval
"""
import struct
from dataclasses import dataclass, field
from typing import List, Tuple

RECORD_SIZE = 0x1CC50
SLOT_BASE = 0x150
SLOT_SIZE = 0x72C
N_SLOTS = 64
assert SLOT_BASE + N_SLOTS * SLOT_SIZE == RECORD_SIZE

RGB = Tuple[int, int, int]


@dataclass(frozen=True)
class Slot:
    action: int
    shortcut_b: int = 0     # wire B for action 0x15 (modifier mask)
    shortcut_c: int = 0     # wire C for action 0x15 (HID key code)
    fire_count: int = 0
    fire_interval: int = 0


@dataclass(frozen=True)
class Profile:
    name: str
    polling_index: int
    active_stage: int            # 0-based
    dpi_values: Tuple[int, ...]  # 8 values, DPI/50
    stage_count: int
    light_mode: int
    brightness: int
    length: int
    frequency: int
    direction: int
    fixed_rgb: RGB
    stage_colors: Tuple[RGB, ...]   # 8, go in block 0x10/01
    cycle_colors: Tuple[RGB, ...]   # 8, go in block 0x10/00
    game_mode: bool
    slots: Tuple[Slot, ...] = field(default_factory=tuple)


def _colors(buf: bytes, off: int) -> Tuple[RGB, ...]:
    return tuple((buf[off + 4 * i], buf[off + 4 * i + 1], buf[off + 4 * i + 2]) for i in range(8))


def parse_record(buf: bytes, offset: int = 0) -> Profile:
    if len(buf) - offset < RECORD_SIZE:
        raise ValueError("buffer is shorter than one profile record (0x1CC50 bytes)")
    r = buf[offset:offset + RECORD_SIZE]
    u32 = lambda o: struct.unpack_from("<I", r, o)[0]
    name = r[:0x64].decode("utf-16le", errors="replace").split("\0")[0]
    slots = []
    for i in range(N_SLOTS):
        s = SLOT_BASE + i * SLOT_SIZE
        slots.append(Slot(action=r[s + 0xC9], shortcut_b=r[s + 0xDC], shortcut_c=r[s + 0xDD],
                          fire_count=r[s + 0x6DC], fire_interval=r[s + 0x6E0]))
    return Profile(
        name=name,
        polling_index=u32(0x80),
        active_stage=u32(0x84) & 0xFF,
        dpi_values=struct.unpack_from("<8I", r, 0x88),
        stage_count=r[0x139],
        light_mode=u32(0xF0), brightness=u32(0xF4), length=u32(0xF8),
        frequency=u32(0xFC), direction=u32(0x100),
        fixed_rgb=(r[0x104], r[0x105], r[0x106]),
        stage_colors=_colors(r, 0xD0),
        cycle_colors=_colors(r, 0x110),
        game_mode=bool(r[0x14C]),
        slots=tuple(slots),
    )


def read_profiles(path: str) -> List[Profile]:
    """profile.bin (many records) or a single-record .pbin."""
    data = open(path, "rb").read()
    if len(data) % RECORD_SIZE:
        raise ValueError(f"{path}: size {len(data)} is not a multiple of {RECORD_SIZE}")
    return [parse_record(data, i * RECORD_SIZE) for i in range(len(data) // RECORD_SIZE)]


def read_selected_index(data_bin_path: str) -> int:
    """Data\\Data.bin: first dword = index of the selected profile."""
    return struct.unpack_from("<I", open(data_bin_path, "rb").read(), 0)[0]


def parse_button_ini(text: str):
    """[BUTTON] section of Data.ini -> list of 64 (4 raw bytes, computed_flag) tuples."""
    out = {}
    in_btn = False
    for line in text.replace("\r", "").split("\n"):
        line = line.strip()
        if line.startswith("["):
            in_btn = line.upper() == "[BUTTON]"
            continue
        if in_btn and "=" in line:
            k, v = line.split("=", 1)
            parts = [p.strip() for p in v.split(",")]
            if k.strip().isdigit() and len(parts) == 5:
                out[int(k)] = (bytes(int(p, 16) for p in parts[:4]), int(parts[4], 16))
    if sorted(out) != list(range(1, N_SLOTS + 1)):
        raise ValueError("Data.ini [BUTTON] must define entries 1..64")
    return [out[i] for i in range(1, N_SLOTS + 1)]
