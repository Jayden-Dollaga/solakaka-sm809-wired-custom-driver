"""Binary-compatible data model for profiles, macros and guns.

Layouts are taken from analysis/OVERVIEW.md sections 11.3 and 11.4 and are
verified against Data/Default.pbin, Data/profile.bin, Data/macro.bin and
Data/gun.bin shipped with the original application.
"""

from __future__ import annotations

import json
import os
import shutil
import struct
import threading
from dataclasses import dataclass
from pathlib import Path

PROFILE_SIZE = 0x1CC50
PROFILE_COUNT = 14
BUTTON_BASE = 0x150
BUTTON_STRIDE = 0x72C
BUTTON_COUNT = 64
# Wheel up/down are ordinary remappable slots.  Every profile ships with
# Scroll Up in the first slot of each pair and Scroll Down in the second.
WHEEL_SLOT_PAIRS = ((30, 31), (62, 63))
WHEEL_ACTION_UP = 0x0B
WHEEL_ACTION_DOWN = 0x0C
MACRO_SIZE = 0x358
GUN_SIZE = 0x240
MAX_EVENTS = 40
MAX_BULLETS = 30

# Profile scalar offsets
P_NAME = 0x000
P_SPEED = 0x064
P_SCROLL = 0x068
P_DOUBLE = 0x06C
P_ENHANCE = 0x070
P_ONEPAGE = 0x074
P_RATE = 0x080
P_STAGE = 0x084
P_DPI = 0x088
P_STAGE_COLORS = 0x0D0
P_LIGHT_MODE = 0x0F0
P_BRIGHTNESS = 0x0F4
P_LENGTH = 0x0F8
P_FREQ = 0x0FC
P_DIRECTION = 0x100
P_FIXED_RGB = 0x104
P_CYCLE_COLORS = 0x110
P_LOD = 0x130
P_LIFT = 0x134
P_KEY_RESPONSE = 0x138
P_STAGE_COUNT = 0x139
P_MODE = 0x14C

# LED parameter ranges accepted by the wired firmware.  +0xFC is NOT a
# frequency slider: the vendor's light page stores the fixed/cycle colour
# choice there (0 or 1) and both the vendor host code and the firmware index
# small tables with it -- see FUN_0040e460 (writer) and FUN_00417540 (reader,
# ``param_1 + 0xb2c + profile[0xFC] * 4``).  A value such as 126 is undefined
# behaviour and can wedge the mouse's lighting controller.
LIGHT_MODE_RANGE = (0, 11)
LIGHT_VALUE_RANGES = {
    "brightness": (0, 255),
    "length": (0, 4),      # vendor "frequency" slider, profile +0xF8
    "frequency": (0, 1),   # fixed (0) / cycling (1) colour mode, +0xFC
    "direction": (0, 4),   # vendor "length" slider, +0x100
}


def clamp_light_mode(value) -> int:
    lo, hi = LIGHT_MODE_RANGE
    return max(lo, min(hi, int(value)))


def clamp_light_value(name: str, value) -> int:
    lo, hi = LIGHT_VALUE_RANGES[name]
    return max(lo, min(hi, int(value)))


# Button entry-relative offsets
B_NAME = 0x064
B_ACTION = 0xC9
B_SELECTED_INDEX = 0xD0
B_MACRO_INDEX = 0xD4
B_SPARE = 0xD8
B_SHORTCUT_MODS = 0xDC
B_SHORTCUT_KEY = 0xDD
B_COUNT = 0xE2
B_LOOP = 0xE4
B_GUN_ROWS = 0x2F0
B_EVENTS = 0x45C
B_FIRE_COUNT = 0x6DC
B_FIRE_INTERVAL = 0x6E0

# Macro / gun record offsets.  The vendor stores the folder name first and
# the entry's own name second: Data/macro.bin record 1 is
# +0x00 "Minecraft" / +0x64 "Spear Lunge", and both rename handlers
# (FUN_00411bc0 and FUN_0040ba50) edit record+100 = +0x64.
M_FOLDER_NAME = 0x000
M_NAME = 0x064
M_LOOP = 0xC8
M_COUNT = 0xCC
M_PROTECTED = 0xD0
M_FOLDER = 0xD4
M_EVENTS = 0xD8
G_FOLDER_NAME = 0x000
G_NAME = 0x064
G_COUNT = 0xC8
G_FOLDER = 0xD0
G_ROWS = 0xD8

RATE_PACKET = (8, 4, 2, 1)
# Index matches RATE_PACKET: 0 = 125 Hz, 3 = 1000 Hz.
RATE_LABELS = ((0, "125 Hz (8 ms)"), (1, "250 Hz (4 ms)"), (2, "500 Hz (2 ms)"), (3, "1000 Hz (1 ms)"))


def u8(buf, off: int) -> int:
    return buf[off]


def set_u8(buf, off: int, value: int) -> None:
    buf[off] = value & 0xFF


def u16(buf, off: int) -> int:
    return struct.unpack_from("<H", buf, off)[0]


def set_u16(buf, off: int, value: int) -> None:
    struct.pack_into("<H", buf, off, max(0, min(0xFFFF, int(value))))


def u32(buf, off: int) -> int:
    return struct.unpack_from("<I", buf, off)[0]


def set_u32(buf, off: int, value: int) -> None:
    struct.pack_into("<I", buf, off, int(value) & 0xFFFFFFFF)


def read_wstr(buf, off: int, chars: int = 50) -> str:
    raw = bytes(buf[off:off + chars * 2])
    text = raw.decode("utf-16le", "ignore")
    return text.split("\0", 1)[0]


def write_wstr(buf, off: int, text: str, chars: int = 50) -> None:
    data = text.encode("utf-16le", "replace")[: (chars - 1) * 2]
    buf[off:off + chars * 2] = b"\0" * (chars * 2)
    buf[off:off + len(data)] = data


def colorref_to_rgb(value: int) -> tuple[int, int, int]:
    return value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF


def rgb_to_colorref(rgb: tuple[int, int, int]) -> int:
    r, g, b = (max(0, min(255, int(v))) for v in rgb)
    return r | (g << 8) | (b << 16)


@dataclass
class MacroEvent:
    """One 16-byte vendor macro event.

    The encoder (FUN_0041ab50) reads the opcode at +1, state at +2, delay at
    +4, and the two dwords at +8/+12.  Bytes +0, +3 and +6..+7 are not
    interpreted by the encoder but are copied verbatim by the vendor's macro
    select routine (FUN_00406db0); real records use them (``b0 1f 01 03 14 00
    5c 00 ...``), so they are kept here for byte-exact .mbin round-trips.
    """

    opcode: int = 0
    state: int = 0
    delay: int = 10
    a: int = 0
    b: int = 0
    b0: int = 0
    b3: int = 0
    w6: int = 0

    @classmethod
    def unpack(cls, buf, off: int) -> "MacroEvent":
        return cls(
            opcode=u8(buf, off + 1),
            state=u8(buf, off + 2),
            delay=u16(buf, off + 4),
            a=u32(buf, off + 8),
            b=u32(buf, off + 12),
            b0=u8(buf, off + 0),
            b3=u8(buf, off + 3),
            w6=u16(buf, off + 6),
        )

    def pack(self, buf, off: int) -> None:
        buf[off:off + 16] = b"\0" * 16
        set_u8(buf, off + 0, self.b0)
        set_u8(buf, off + 1, self.opcode)
        set_u8(buf, off + 2, self.state)
        set_u8(buf, off + 3, self.b3)
        set_u16(buf, off + 4, self.delay)
        set_u16(buf, off + 6, self.w6)
        set_u32(buf, off + 8, self.a)
        set_u32(buf, off + 12, self.b)


@dataclass
class Bullet:
    x: int = 0
    y: int = 0
    delay: int = 10

    @classmethod
    def unpack(cls, buf, off: int) -> "Bullet":
        return cls(
            x=struct.unpack_from("<i", buf, off)[0],
            y=struct.unpack_from("<i", buf, off + 4)[0],
            delay=u16(buf, off + 10),
        )

    def pack(self, buf, off: int) -> None:
        buf[off:off + 12] = b"\0" * 12
        struct.pack_into("<i", buf, off, self.x)
        struct.pack_into("<i", buf, off + 4, self.y)
        set_u16(buf, off + 10, self.delay)


class ButtonEntry:
    """View over one 0x72C-byte slot inside a Profile record."""

    def __init__(self, profile: "Profile", index: int):
        self.profile = profile
        self.index = index
        self.base = BUTTON_BASE + index * BUTTON_STRIDE

    @property
    def buf(self) -> bytearray:
        return self.profile.raw

    def _off(self, rel: int) -> int:
        return self.base + rel

    @property
    def name(self) -> str:
        return read_wstr(self.buf, self._off(B_NAME))

    @name.setter
    def name(self, value: str) -> None:
        write_wstr(self.buf, self._off(B_NAME), value)

    @property
    def action(self) -> int:
        return u8(self.buf, self._off(B_ACTION))

    @action.setter
    def action(self, value: int) -> None:
        set_u8(self.buf, self._off(B_ACTION), value)

    @property
    def selected_index(self) -> int:
        return u32(self.buf, self._off(B_SELECTED_INDEX))

    @selected_index.setter
    def selected_index(self, value: int) -> None:
        set_u32(self.buf, self._off(B_SELECTED_INDEX), value)

    @property
    def macro_index(self) -> int:
        return u8(self.buf, self._off(B_MACRO_INDEX))

    @macro_index.setter
    def macro_index(self, value: int) -> None:
        set_u8(self.buf, self._off(B_MACRO_INDEX), value)

    @property
    def shortcut_mods(self) -> int:
        return u8(self.buf, self._off(B_SHORTCUT_MODS))

    @shortcut_mods.setter
    def shortcut_mods(self, value: int) -> None:
        set_u8(self.buf, self._off(B_SHORTCUT_MODS), value)

    @property
    def shortcut_key(self) -> int:
        return u8(self.buf, self._off(B_SHORTCUT_KEY))

    @shortcut_key.setter
    def shortcut_key(self, value: int) -> None:
        set_u8(self.buf, self._off(B_SHORTCUT_KEY), value)

    @property
    def count(self) -> int:
        return u16(self.buf, self._off(B_COUNT))

    @count.setter
    def count(self, value: int) -> None:
        set_u16(self.buf, self._off(B_COUNT), max(0, min(MAX_EVENTS, value)))

    @property
    def loop(self) -> int:
        return u16(self.buf, self._off(B_LOOP))

    @loop.setter
    def loop(self, value: int) -> None:
        set_u16(self.buf, self._off(B_LOOP), value)

    @property
    def fire_count(self) -> int:
        return u32(self.buf, self._off(B_FIRE_COUNT))

    @fire_count.setter
    def fire_count(self, value: int) -> None:
        set_u32(self.buf, self._off(B_FIRE_COUNT), value)

    @property
    def fire_interval(self) -> int:
        return u32(self.buf, self._off(B_FIRE_INTERVAL))

    @fire_interval.setter
    def fire_interval(self, value: int) -> None:
        set_u32(self.buf, self._off(B_FIRE_INTERVAL), value)

    @property
    def events(self) -> list[MacroEvent]:
        return [MacroEvent.unpack(self.buf, self._off(B_EVENTS) + i * 16) for i in range(MAX_EVENTS)]

    def event_slice(self) -> list[MacroEvent]:
        return [MacroEvent.unpack(self.buf, self._off(B_EVENTS) + i * 16) for i in range(self.count)]

    def set_events(self, events: list[MacroEvent]) -> None:
        events = events[:MAX_EVENTS]
        self.count = len(events)
        for i, ev in enumerate(events):
            ev.pack(self.buf, self._off(B_EVENTS) + i * 16)
        for i in range(len(events), MAX_EVENTS):
            self.buf[self._off(B_EVENTS) + i * 16:self._off(B_EVENTS) + (i + 1) * 16] = b"\0" * 16

    @property
    def bullets(self) -> list[Bullet]:
        return [Bullet.unpack(self.buf, self._off(B_GUN_ROWS) + i * 12) for i in range(MAX_BULLETS)]

    def bullet_slice(self) -> list[Bullet]:
        return self.bullets[:min(self.count, MAX_BULLETS)]

    def set_bullets(self, rows: list[Bullet]) -> None:
        rows = rows[:MAX_BULLETS]
        self.count = len(rows)
        for i, row in enumerate(rows):
            row.pack(self.buf, self._off(B_GUN_ROWS) + i * 12)
        for i in range(len(rows), MAX_BULLETS):
            self.buf[self._off(B_GUN_ROWS) + i * 12:self._off(B_GUN_ROWS) + (i + 1) * 12] = b"\0" * 12


class Profile:
    def __init__(self, raw: bytes | bytearray | None = None):
        if raw is None:
            raw = bytes(PROFILE_SIZE)
        if len(raw) != PROFILE_SIZE:
            raise ValueError(f"profile record must be {PROFILE_SIZE} bytes, got {len(raw)}")
        self.raw = bytearray(raw)

    @classmethod
    def from_file(cls, path: Path) -> "Profile":
        return cls(path.read_bytes())

    def copy(self) -> "Profile":
        return Profile(bytes(self.raw))

    # -- scalar properties -------------------------------------------------
    @property
    def name(self) -> str:
        return read_wstr(self.raw, P_NAME)

    @name.setter
    def name(self, value: str) -> None:
        write_wstr(self.raw, P_NAME, value)

    def _get_u32(self, off: int) -> int:
        return u32(self.raw, off)

    def _set_u32(self, off: int, value: int) -> None:
        set_u32(self.raw, off, value)

    speed = property(lambda s: s._get_u32(P_SPEED), lambda s, v: s._set_u32(P_SPEED, v))
    scroll = property(lambda s: s._get_u32(P_SCROLL), lambda s, v: s._set_u32(P_SCROLL, v))
    double = property(lambda s: s._get_u32(P_DOUBLE), lambda s, v: s._set_u32(P_DOUBLE, v))
    enhance = property(lambda s: s._get_u32(P_ENHANCE), lambda s, v: s._set_u32(P_ENHANCE, v))
    onepage = property(lambda s: s._get_u32(P_ONEPAGE), lambda s, v: s._set_u32(P_ONEPAGE, v))
    rate = property(lambda s: s._get_u32(P_RATE), lambda s, v: s._set_u32(P_RATE, v))
    stage = property(lambda s: s._get_u32(P_STAGE), lambda s, v: s._set_u32(P_STAGE, v))
    light_mode = property(lambda s: s._get_u32(P_LIGHT_MODE), lambda s, v: s._set_u32(P_LIGHT_MODE, v))
    brightness = property(lambda s: s._get_u32(P_BRIGHTNESS), lambda s, v: s._set_u32(P_BRIGHTNESS, v))
    length = property(lambda s: s._get_u32(P_LENGTH), lambda s, v: s._set_u32(P_LENGTH, v))
    frequency = property(lambda s: s._get_u32(P_FREQ), lambda s, v: s._set_u32(P_FREQ, v))
    direction = property(lambda s: s._get_u32(P_DIRECTION), lambda s, v: s._set_u32(P_DIRECTION, v))
    lod = property(lambda s: s._get_u32(P_LOD), lambda s, v: s._set_u32(P_LOD, v))
    lift = property(lambda s: s._get_u32(P_LIFT), lambda s, v: s._set_u32(P_LIFT, v))
    mode = property(lambda s: s._get_u32(P_MODE), lambda s, v: s._set_u32(P_MODE, v))

    def sanitize_lighting(self) -> bool:
        """Clamp the LED fields to the ranges the wired firmware accepts.

        Older studio builds exposed profile +0xFC as a 1..255 "frequency"
        slider, so a saved profile can contain a value like 126.  The firmware
        (and the vendor UI) index a two-entry table with that byte, so such a
        record must never be applied or exported again.  Returns True when the
        record was repaired.
        """
        changed = False
        mode = clamp_light_mode(self.light_mode)
        if mode != self.light_mode:
            self.light_mode = mode
            changed = True
        for name in LIGHT_VALUE_RANGES:
            value = getattr(self, name)
            clamped = clamp_light_value(name, value)
            if clamped != value:
                setattr(self, name, clamped)
                changed = True
        return changed

    @property
    def key_response(self) -> int:
        return u8(self.raw, P_KEY_RESPONSE)

    @key_response.setter
    def key_response(self, value: int) -> None:
        set_u8(self.raw, P_KEY_RESPONSE, max(1, min(255, value)))

    @property
    def stage_count(self) -> int:
        return max(1, min(8, u8(self.raw, P_STAGE_COUNT)))

    @stage_count.setter
    def stage_count(self, value: int) -> None:
        set_u8(self.raw, P_STAGE_COUNT, max(1, min(8, value)))

    @property
    def dpi_values(self) -> list[int]:
        return [struct.unpack_from("<i", self.raw, P_DPI + i * 4)[0] for i in range(8)]

    @dpi_values.setter
    def dpi_values(self, values) -> None:
        values = list(values) + [0] * 8
        for i in range(8):
            struct.pack_into("<i", self.raw, P_DPI + i * 4, max(0, min(40000, int(values[i]))))

    @property
    def stage_colors(self) -> list[int]:
        return [u32(self.raw, P_STAGE_COLORS + i * 4) for i in range(8)]

    @stage_colors.setter
    def stage_colors(self, values) -> None:
        values = list(values) + [0] * 8
        for i in range(8):
            set_u32(self.raw, P_STAGE_COLORS + i * 4, values[i])

    @property
    def cycle_colors(self) -> list[int]:
        return [u32(self.raw, P_CYCLE_COLORS + i * 4) for i in range(8)]

    @cycle_colors.setter
    def cycle_colors(self, values) -> None:
        values = list(values) + [0] * 8
        for i in range(8):
            set_u32(self.raw, P_CYCLE_COLORS + i * 4, values[i])

    @property
    def fixed_rgb(self) -> tuple[int, int, int]:
        return self.raw[P_FIXED_RGB], self.raw[P_FIXED_RGB + 1], self.raw[P_FIXED_RGB + 2]

    @fixed_rgb.setter
    def fixed_rgb(self, rgb: tuple[int, int, int]) -> None:
        r, g, b = (max(0, min(255, int(v))) for v in rgb)
        self.raw[P_FIXED_RGB] = r
        self.raw[P_FIXED_RGB + 1] = g
        self.raw[P_FIXED_RGB + 2] = b

    def button(self, index: int) -> ButtonEntry:
        if not 0 <= index < BUTTON_COUNT:
            raise IndexError(index)
        return ButtonEntry(self, index)

    @property
    def buttons(self) -> list[ButtonEntry]:
        return [ButtonEntry(self, i) for i in range(BUTTON_COUNT)]


def wheel_reversed(profile: Profile) -> bool:
    """True when both wheel pairs carry Down/Up instead of Up/Down."""
    pairs = ((profile.button(up).action, profile.button(down).action)
             for up, down in WHEEL_SLOT_PAIRS)
    return all(up == WHEEL_ACTION_DOWN and down == WHEEL_ACTION_UP for up, down in pairs)


def set_wheel_reversed(profile: Profile, reversed_: bool) -> None:
    """Flip the physical wheel direction by swapping the two wheel actions.

    The firmware routes the wheel through the button table, so swapping the
    Scroll Up / Scroll Down actions is what inverts the reported direction.
    """
    up_action, down_action = (
        (WHEEL_ACTION_DOWN, WHEEL_ACTION_UP) if reversed_
        else (WHEEL_ACTION_UP, WHEEL_ACTION_DOWN)
    )
    for up, down in WHEEL_SLOT_PAIRS:
        profile.button(up).action = up_action
        profile.button(down).action = down_action


class MacroRecord:
    def __init__(self, raw: bytes | bytearray | None = None):
        if raw is None:
            raw = bytes(MACRO_SIZE)
        if len(raw) != MACRO_SIZE:
            raise ValueError(f"macro record must be {MACRO_SIZE} bytes")
        self.raw = bytearray(raw)

    @property
    def name(self) -> str:
        return read_wstr(self.raw, M_NAME)

    @name.setter
    def name(self, value: str) -> None:
        write_wstr(self.raw, M_NAME, value)

    @property
    def folder_name(self) -> str:
        return read_wstr(self.raw, M_FOLDER_NAME)

    @folder_name.setter
    def folder_name(self, value: str) -> None:
        write_wstr(self.raw, M_FOLDER_NAME, value)

    @property
    def protected(self) -> bool:
        """Vendor's "encrypted export" marker (+0xD0)."""
        return bool(u32(self.raw, M_PROTECTED))

    @protected.setter
    def protected(self, value: bool) -> None:
        set_u32(self.raw, M_PROTECTED, 1 if value else 0)

    @property
    def loop(self) -> int:
        return u16(self.raw, M_LOOP)

    @loop.setter
    def loop(self, value: int) -> None:
        set_u16(self.raw, M_LOOP, max(0, value))

    @property
    def count(self) -> int:
        return min(MAX_EVENTS, u16(self.raw, M_COUNT))

    @count.setter
    def count(self, value: int) -> None:
        set_u16(self.raw, M_COUNT, max(0, min(MAX_EVENTS, value)))

    @property
    def is_folder(self) -> bool:
        return bool(u32(self.raw, M_FOLDER))

    @is_folder.setter
    def is_folder(self, value: bool) -> None:
        set_u32(self.raw, M_FOLDER, 1 if value else 0)

    @property
    def events(self) -> list[MacroEvent]:
        return [MacroEvent.unpack(self.raw, M_EVENTS + i * 16) for i in range(self.count)]

    def set_events(self, events: list[MacroEvent]) -> None:
        events = events[:MAX_EVENTS]
        self.count = len(events)
        for i in range(MAX_EVENTS):
            self.raw[M_EVENTS + i * 16:M_EVENTS + (i + 1) * 16] = b"\0" * 16
        for i, ev in enumerate(events):
            ev.pack(self.raw, M_EVENTS + i * 16)


class GunRecord:
    def __init__(self, raw: bytes | bytearray | None = None):
        if raw is None:
            raw = bytes(GUN_SIZE)
        if len(raw) != GUN_SIZE:
            raise ValueError(f"gun record must be {GUN_SIZE} bytes")
        self.raw = bytearray(raw)

    @property
    def name(self) -> str:
        return read_wstr(self.raw, G_NAME)

    @name.setter
    def name(self, value: str) -> None:
        write_wstr(self.raw, G_NAME, value)

    @property
    def folder_name(self) -> str:
        return read_wstr(self.raw, G_FOLDER_NAME)

    @folder_name.setter
    def folder_name(self, value: str) -> None:
        write_wstr(self.raw, G_FOLDER_NAME, value)

    @property
    def count(self) -> int:
        return min(MAX_BULLETS, u8(self.raw, G_COUNT))

    @count.setter
    def count(self, value: int) -> None:
        set_u8(self.raw, G_COUNT, max(0, min(MAX_BULLETS, value)))

    @property
    def is_folder(self) -> bool:
        return bool(u32(self.raw, G_FOLDER))

    @is_folder.setter
    def is_folder(self, value: bool) -> None:
        set_u32(self.raw, G_FOLDER, 1 if value else 0)

    @property
    def bullets(self) -> list[Bullet]:
        return [Bullet.unpack(self.raw, G_ROWS + i * 12) for i in range(MAX_BULLETS)]

    def bullet_slice(self) -> list[Bullet]:
        return self.bullets[:self.count]

    def set_bullet(self, index: int, row: Bullet) -> None:
        if 0 <= index < MAX_BULLETS:
            row.pack(self.raw, G_ROWS + index * 12)

    def set_bullets(self, rows: list[Bullet]) -> None:
        rows = rows[:MAX_BULLETS]
        self.count = len(rows)
        for i in range(MAX_BULLETS):
            self.raw[G_ROWS + i * 12:G_ROWS + (i + 1) * 12] = b"\0" * 12
        for i, row in enumerate(rows):
            row.pack(self.raw, G_ROWS + i * 12)


class DataStore:
    """Owns profile.bin / Data.bin / macro.bin / gun.bin in the portable data dir."""

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        # The monitor thread saves profile.bin when the mouse changes stage or
        # rate while the UI thread may be saving too; serialise those writes.
        self._save_lock = threading.RLock()
        self.default_raw = bytes(PROFILE_SIZE)
        self.profiles: list[Profile] = []
        self.selected = 0
        self.macros: list[MacroRecord] = []
        self.guns: list[GunRecord] = []
        self.load()

    # -- paths -------------------------------------------------------------
    @property
    def profiles_path(self) -> Path:
        return self.data_dir / "profile.bin"

    @property
    def selected_path(self) -> Path:
        return self.data_dir / "Data.bin"

    @property
    def macros_path(self) -> Path:
        return self.data_dir / "macro.bin"

    @property
    def guns_path(self) -> Path:
        return self.data_dir / "gun.bin"

    @property
    def default_path(self) -> Path:
        return self.data_dir / "Default.pbin"

    # -- load / save -------------------------------------------------------
    def load(self) -> None:
        if self.default_path.exists():
            raw = self.default_path.read_bytes()
            if len(raw) >= PROFILE_SIZE:
                self.default_raw = raw[:PROFILE_SIZE]
        else:
            self.default_raw = bytes(PROFILE_SIZE)
            tmp = Profile(self.default_raw)
            tmp.name = "Profile 1"
            # +0x88 stores the vendor's raw stage value (displayed as x100),
            # not the DPI the UI shows: 4 -> 400, 120 -> 12000.
            tmp.dpi_values = [4, 8, 12, 16, 24, 32, 64, 120]
            tmp.stage_count = 8
            tmp.stage = 0
            tmp.rate = 2
            tmp.speed = 6
            tmp.scroll = 3
            tmp.double = 5
            # Light page defaults from Default.pbin: Wave, full intensity,
            # Pulsation 3, Length 2, Loop Color with the vendor's eight
            # swatches and a red Fix Color.
            tmp.light_mode = 4
            tmp.brightness = 255
            tmp.length = 3
            tmp.frequency = 1
            tmp.direction = 2
            tmp.fixed_rgb = (255, 0, 0)
            tmp.cycle_colors = [
                rgb_to_colorref(c) for c in (
                    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                    (255, 0, 255), (0, 255, 255), (255, 128, 0),
                    (255, 255, 255),
                )
            ]
            self.default_raw = bytes(tmp.raw)

        self.profiles = []
        if self.profiles_path.exists():
            blob = self.profiles_path.read_bytes()
            for i in range(0, len(blob) // PROFILE_SIZE):
                self.profiles.append(Profile(blob[i * PROFILE_SIZE:(i + 1) * PROFILE_SIZE]))
        if not self.profiles:
            base = Profile(self.default_raw)
            base.name = "Profile 1"
            self.profiles = [base]
            self.save_profiles()

        self.selected = 0
        if self.selected_path.exists():
            blob = self.selected_path.read_bytes()
            if len(blob) >= 4:
                self.selected = u32(blob, 0)
        self.selected = max(0, min(len(self.profiles) - 1, self.selected))

        self.macros = []
        if self.macros_path.exists():
            blob = self.macros_path.read_bytes()
            for i in range(0, len(blob) // MACRO_SIZE):
                self.macros.append(MacroRecord(blob[i * MACRO_SIZE:(i + 1) * MACRO_SIZE]))
        self.guns = []
        if self.guns_path.exists():
            blob = self.guns_path.read_bytes()
            for i in range(0, len(blob) // GUN_SIZE):
                self.guns.append(GunRecord(blob[i * GUN_SIZE:(i + 1) * GUN_SIZE]))

    def _atomic_write(self, path: Path, data: bytes) -> None:
        # Unique staging name: the monitor thread and the UI thread can save
        # at the same time, and two writers must not share one .tmp file.
        tmp = path.with_name(f"{path.name}.{os.getpid()}.{threading.get_ident()}.tmp")
        with self._save_lock:
            try:
                with open(tmp, "wb") as fh:
                    fh.write(data)
                    fh.flush()
                    os.fsync(fh.fileno())
                tmp.replace(path)
            finally:
                try:
                    tmp.unlink(missing_ok=True)
                except OSError:
                    pass

    def save_profiles(self) -> None:
        with self._save_lock:
            self._atomic_write(self.profiles_path,
                               b"".join(bytes(p.raw) for p in self.profiles))
            self.save_selected()

    def save_selected(self) -> None:
        with self._save_lock:
            self._atomic_write(self.selected_path, struct.pack("<II", self.selected, 0))

    def save_macros(self) -> None:
        with self._save_lock:
            self._atomic_write(self.macros_path,
                               b"".join(bytes(m.raw) for m in self.macros))

    def save_guns(self) -> None:
        with self._save_lock:
            self._atomic_write(self.guns_path,
                               b"".join(bytes(g.raw) for g in self.guns))

    # -- profile operations ------------------------------------------------
    @property
    def profile(self) -> Profile:
        return self.profiles[self.selected]

    def select(self, index: int) -> Profile:
        self.selected = max(0, min(len(self.profiles) - 1, int(index)))
        return self.profile

    def add_profile(self, name: str | None = None) -> Profile:
        if len(self.profiles) >= PROFILE_COUNT:
            raise ValueError(f"at most {PROFILE_COUNT} profiles are supported")
        prof = Profile(self.default_raw)
        prof.name = name or self._unique_profile_name()
        self.profiles.append(prof)
        self.selected = len(self.profiles) - 1
        self.save_profiles()
        return prof

    def delete_profile(self, index: int) -> None:
        if len(self.profiles) <= 1:
            raise ValueError("the last profile cannot be deleted")
        del self.profiles[index]
        if self.selected >= len(self.profiles):
            self.selected = len(self.profiles) - 1
        self.save_profiles()

    def reset_profile(self, index: int | None = None) -> Profile:
        idx = self.selected if index is None else index
        name = self.profiles[idx].name
        prof = Profile(self.default_raw)
        prof.name = name
        self.profiles[idx] = prof
        self.save_profiles()
        return prof

    def rename_profile(self, name: str) -> None:
        self.profile.name = name
        self.save_profiles()

    def rename_profile_at(self, index: int, name: str) -> None:
        """Rename any profile record, keeping the selected one selected."""
        if 0 <= index < len(self.profiles):
            self.profiles[index].name = name
            self.save_profiles()

    def duplicate_profile(self, index: int | None = None) -> Profile:
        """Copy one record, insert it after the source and select the copy."""
        idx = self.selected if index is None else int(index)
        if not 0 <= idx < len(self.profiles):
            raise IndexError(idx)
        if len(self.profiles) >= PROFILE_COUNT:
            raise ValueError(f"at most {PROFILE_COUNT} profiles are supported")
        copy = self.profiles[idx].copy()
        base = copy.name.strip() or "Profile"
        used = {p.name for p in self.profiles}
        name = f"{base} copy"
        n = 2
        while name in used:
            name = f"{base} copy {n}"
            n += 1
        copy.name = name
        self.profiles.insert(idx + 1, copy)
        self.selected = idx + 1
        self.save_profiles()
        return copy

    def reorder_profiles(self, order: list[int]) -> None:
        """Reorder records by original indices, preserving the selected profile."""
        if sorted(int(i) for i in order) != list(range(len(self.profiles))):
            raise ValueError("order must list every profile once")
        active = self.profile
        self.profiles = [self.profiles[int(i)] for i in order]
        self.selected = self.profiles.index(active)
        self.save_profiles()

    def sort_profiles(self, key: str = "name") -> None:
        """Sort records by display name (A-Z). Other keys are a no-op."""
        if key != "name":
            return
        active = self.profile
        self.profiles.sort(key=lambda p: p.name.casefold())
        self.selected = self.profiles.index(active)
        self.save_profiles()

    def _unique_profile_name(self) -> str:
        used = {p.name for p in self.profiles}
        n = len(self.profiles) + 1
        while f"Profile {n}" in used:
            n += 1
        return f"Profile {n}"

    def export_profile(self, path: Path, index: int | None = None) -> None:
        idx = self.selected if index is None else index
        Path(path).write_bytes(bytes(self.profiles[idx].raw))

    def import_profile(self, path: Path) -> Profile:
        blob = Path(path).read_bytes()
        if len(blob) < PROFILE_SIZE:
            raise ValueError("not a profile file")
        if len(self.profiles) >= PROFILE_COUNT:
            raise ValueError(f"at most {PROFILE_COUNT} profiles are supported")
        prof = Profile(blob[:PROFILE_SIZE])
        # Never adopt an out-of-range LED byte from a foreign .pbin: the
        # firmware indexes a two-entry table with profile +0xFC.
        prof.sanitize_lighting()
        if not prof.name.strip():
            prof.name = self._unique_profile_name()
        self.profiles.append(prof)
        self.selected = len(self.profiles) - 1
        self.save_profiles()
        return prof

    def export_json(self) -> dict:
        prof = self.profile
        return {
            "name": prof.name,
            "speed": prof.speed,
            "scroll": prof.scroll,
            "double": prof.double,
            "enhance": prof.enhance,
            "onepage": prof.onepage,
            "rate": prof.rate,
            "stage": prof.stage,
            "dpi": prof.dpi_values,
            "stage_colors": prof.stage_colors,
            "light": {
                "mode": prof.light_mode,
                "brightness": prof.brightness,
                "length": prof.length,
                "frequency": prof.frequency,
                "direction": prof.direction,
                "fixed_rgb": prof.fixed_rgb,
                "cycle_colors": prof.cycle_colors,
            },
            "lod": prof.lod,
            "lift": prof.lift,
            "key_response": prof.key_response,
            "stage_count": prof.stage_count,
            "mode": prof.mode,
            "buttons": [
                {
                    "index": i + 1,
                    "action": b.action,
                    "macro_index": b.macro_index,
                    "shortcut": [b.shortcut_key, b.shortcut_mods],
                    "fire": [b.fire_count, b.fire_interval],
                }
                for i, b in enumerate(prof.buttons)
            ],
        }

    def export_json_file(self, path: Path) -> None:
        Path(path).write_text(json.dumps(self.export_json(), indent=2), encoding="utf-8")

    # -- macro / gun operations -------------------------------------------
    def add_macro(self, name: str | None = None, folder: bool = False) -> MacroRecord:
        rec = MacroRecord()
        rec.is_folder = folder
        label = name or self._unique_name(
            "Macro", [m.name for m in self.macros if not m.is_folder])
        # A folder record carries its label in the first name field; a macro
        # carries its own name in the second one (vendor layout).
        if folder:
            rec.folder_name = label
        else:
            rec.name = label
        rec.loop = 1
        self.macros.append(rec)
        self.save_macros()
        return rec

    def add_gun(self, name: str | None = None, folder: bool = False) -> GunRecord:
        rec = GunRecord()
        rec.is_folder = folder
        label = name or self._unique_name(
            "Gun", [g.name for g in self.guns if not g.is_folder])
        if folder:
            rec.folder_name = label
        else:
            rec.name = label
        rec.set_bullets([Bullet(0, 0, 10) for _ in range(MAX_BULLETS)])
        self.guns.append(rec)
        self.save_guns()
        return rec

    def delete_macro(self, index: int) -> None:
        del self.macros[index]
        self.save_macros()

    def delete_gun(self, index: int) -> None:
        del self.guns[index]
        self.save_guns()

    def macro_names(self) -> list[tuple[int, str]]:
        return [(i, m.name) for i, m in enumerate(self.macros) if not m.is_folder]

    def gun_names(self) -> list[tuple[int, str]]:
        return [(i, g.name) for i, g in enumerate(self.guns) if not g.is_folder]

    @staticmethod
    def _unique_name(prefix: str, used: list[str]) -> str:
        existing = set(used)
        n = 1
        while f"{prefix} {n}" in existing:
            n += 1
        return f"{prefix} {n}"

    def backup(self, destination: Path) -> None:
        destination.mkdir(parents=True, exist_ok=True)
        for p in (self.profiles_path, self.selected_path, self.macros_path, self.guns_path, self.default_path):
            if p.exists():
                shutil.copy2(p, destination / p.name)
