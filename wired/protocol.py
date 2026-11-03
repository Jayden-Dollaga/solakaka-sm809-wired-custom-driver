"""SM809 wire protocol: packets, obfuscation and 32-byte block encoders.

All formats come from the static analysis in analysis/OVERVIEW.md sections
6-9, cross-checked against the shipped executable's disassembly.
"""

from __future__ import annotations

import logging
import struct
from dataclasses import dataclass

from .config import DeviceConfig
from .model import (
    LIGHT_MODE_RANGE,
    LIGHT_VALUE_RANGES,
    MAX_BULLETS,
    MAX_EVENTS,
    Bullet,
    ButtonEntry,
    MacroEvent,
    Profile,
    RATE_PACKET,
    clamp_light_mode,
    clamp_light_value,
)


_light_log = logging.getLogger("sm809.lighting")
_macro_log = logging.getLogger("sm809.macros")


class PacketError(ValueError):
    pass


# ---------------------------------------------------------------------------
# Timing
# ---------------------------------------------------------------------------
# The firmware is a stateful USB-HID device: it needs a short settle window
# after each feature write or the controller can wedge.  These match the
# reference driver's documented values (60 ms per command, 120 ms between
# macro chunks).  Block writes keep the vendor's faster 20 ms pace (see
# DeviceService.pace); only macro data chunks use the longer macro delay.
CMD_SETTLE = 0.060
MACRO_CHUNK_DELAY = 0.120


# ---------------------------------------------------------------------------
# Framing and obfuscation
# ---------------------------------------------------------------------------

def checksum(packet: bytes | bytearray) -> int:
    return (-(1 + sum(packet[:7]))) & 0xFF


def frame(cmd: int, args: tuple[int, ...] | list[int] = ()) -> bytes:
    """Build an 8-byte feature packet (byte 7 is the checksum)."""
    if not 0 <= cmd <= 0xFF:
        raise ValueError("command must be one byte")
    payload = bytearray(8)
    payload[0] = cmd
    for i, value in enumerate(list(args)[:6], 1):
        payload[i] = int(value) & 0xFF
    payload[7] = checksum(payload)
    return bytes(payload)


def obfuscate(packet: bytes | bytearray, key: bytes) -> bytes:
    """FUN_00414710 - encode an 8-byte packet with the 6-character key."""
    if len(packet) != 8:
        raise ValueError("packet must be 8 bytes")
    k = bytes(key).ljust(6, b"\0")[:6]
    p = bytes(packet)
    # FUN_00414710: permute, XOR bytes 1..6 with key chars 1..6, then rotate.
    # Bytes 0 and 7 take no key XOR after the permutation.
    n = [
        p[5],
        p[4] ^ k[0],
        p[7] ^ k[1],
        p[6] ^ k[2],
        p[1] ^ k[3],
        p[0] ^ k[4],
        p[3] ^ k[5],
        p[2],
    ]
    constants = (0x25, -0x0A, -0x1C, 0x76, 0x47, 0x54, -0x1A, 0x76)
    out = bytearray(8)
    for i in range(8):
        nxt = n[(i + 1) % 8]
        out[i] = (((n[i] << 3) | (nxt >> 5)) + constants[i]) & 0xFF
    return bytes(out)


def deobfuscate(packet: bytes | bytearray, key: bytes) -> bytes:
    """FUN_00414810 - inverse of :func:`obfuscate`."""
    if len(packet) != 8:
        raise ValueError("packet must be 8 bytes")
    k = bytes(key).ljust(6, b"\0")[:6]
    p = bytes(packet)
    constants = (0x25, -0x0A, -0x1C, 0x76, 0x47, 0x54, -0x1A, 0x76)
    n = bytearray(8)
    for i in range(8):
        current = (p[i] - constants[i]) & 0xFF
        previous = (p[(i - 1) % 8] - constants[(i - 1) % 8]) & 0xFF
        n[i] = ((current >> 3) | (previous << 5)) & 0xFF
    out = bytearray(8)
    out[5] = n[0]
    out[4] = n[1] ^ k[0]
    out[7] = n[2] ^ k[1]
    out[6] = n[3] ^ k[2]
    out[1] = n[4] ^ k[3]
    out[0] = n[5] ^ k[4]
    out[3] = n[6] ^ k[5]
    out[2] = n[7]
    return bytes(out)


def wire_packet(cmd: int, args=(), key: bytes | None = None) -> bytes:
    """Build a packet and apply the optional password obfuscation."""
    packet = frame(cmd, args)
    if key:
        return obfuscate(packet, key)
    return packet


HANDSHAKE_PLAIN = frame(0x00, (0xAA, 0xDD, 0x3B, 0x62, 0x00, 0x00))
HANDSHAKE_EXPECTED = bytes((0x00, 0xAA, 0xDD, 0x3B, 0x62))


def handshake_packets(key: bytes) -> tuple[bytes, bytes]:
    """Return (plain, obfuscated) handshake packets.

    FUN_0041bbc0 sends the packet with a leading zero, then the same bytes
    obfuscated with the six-character password regardless of whether the
    password flag is enabled.
    """
    return HANDSHAKE_PLAIN, obfuscate(HANDSHAKE_PLAIN, key)


def handshake_reply_ok(raw_reply: bytes, key: bytes) -> bool:
    if len(raw_reply) < 8:
        return False
    try:
        reply = deobfuscate(raw_reply[:8], key)
    except Exception:
        return False
    return reply[1:5] == HANDSHAKE_EXPECTED[1:5]


# ---------------------------------------------------------------------------
# Action table
# ---------------------------------------------------------------------------

# action_id, A, B, C, D (Appendix D, VA 0x425118, 61 records)
ACTION_TABLE = (
    (0x01, 0x01, 0x00, 0xF0, 0x00), (0x02, 0x01, 0x00, 0xF1, 0x00),
    (0x03, 0x01, 0x00, 0xF2, 0x00), (0x09, 0x0A, 0xF0, 0x32, 0x02),
    (0x15, 0x00, 0x00, 0x00, 0x00), (0x19, 0x0C, 0x00, 0x00, 0x00),
    (0x12, 0x0A, 0xF0, 0x32, 0x03), (0x74, 0x08, 0x00, 0x03, 0x00),
    (0x1A, 0x08, 0x00, 0x01, 0x00), (0x00, 0x00, 0x00, 0x00, 0x00),
    (0x04, 0x01, 0x00, 0xF4, 0x00), (0x05, 0x01, 0x00, 0xF3, 0x00),
    (0x0B, 0x04, 0x00, 0x01, 0x00), (0x0C, 0x04, 0x00, 0x02, 0x00),
    (0x0D, 0x04, 0x00, 0x03, 0x00), (0x0E, 0x04, 0x00, 0x04, 0x00),
    (0x06, 0x07, 0x00, 0x03, 0x00), (0x71, 0x07, 0x00, 0x04, 0x02),
    (0x07, 0x07, 0x00, 0x01, 0x00), (0x08, 0x07, 0x00, 0x02, 0x00),
    (0x68, 0x05, 0x00, 0x01, 0x00), (0x69, 0x05, 0x00, 0x02, 0x00),
    (0x70, 0x05, 0x00, 0x03, 0x00), (0x16, 0x09, 0x00, 0x00, 0x00),
    (0x32, 0x0B, 0x00, 0x00, 0x00), (0x18, 0x06, 0x00, 0x00, 0x00),
    (0x0A, 0x0A, 0x00, 0x00, 0x00), (0x40, 0x03, 0x00, 0x83, 0x01),
    (0x43, 0x03, 0x00, 0xB6, 0x00), (0x44, 0x03, 0x00, 0xB5, 0x00),
    (0x41, 0x03, 0x00, 0xCD, 0x00), (0x42, 0x03, 0x00, 0xB7, 0x00),
    (0x47, 0x03, 0x00, 0xE2, 0x00), (0x45, 0x03, 0x00, 0xE9, 0x00),
    (0x46, 0x03, 0x00, 0xEA, 0x00), (0x50, 0x03, 0x00, 0x92, 0x01),
    (0x4F, 0x03, 0x00, 0x8A, 0x01), (0x49, 0x03, 0x00, 0x2A, 0x02),
    (0x4C, 0x03, 0x00, 0x26, 0x02), (0x51, 0x03, 0x00, 0x94, 0x01),
    (0x4D, 0x03, 0x00, 0x27, 0x02), (0x48, 0x03, 0x00, 0x23, 0x02),
    (0x4E, 0x03, 0x00, 0x21, 0x02), (0x4A, 0x03, 0x00, 0x25, 0x02),
    (0x4B, 0x03, 0x00, 0x24, 0x02), (0x21, 0x00, 0x01, 0x06, 0x00),
    (0x20, 0x00, 0x01, 0x1B, 0x00), (0x2F, 0x00, 0x01, 0x11, 0x00),
    (0x23, 0x00, 0x01, 0x12, 0x00), (0x22, 0x00, 0x01, 0x19, 0x00),
    (0x29, 0x00, 0x01, 0x13, 0x00), (0x26, 0x00, 0x01, 0x1C, 0x00),
    (0x24, 0x00, 0x01, 0x16, 0x00), (0x28, 0x00, 0x01, 0x04, 0x00),
    (0x27, 0x00, 0x01, 0x1D, 0x00), (0x25, 0x00, 0x01, 0x09, 0x00),
    (0x2C, 0x00, 0x08, 0x07, 0x00), (0x2D, 0x00, 0x08, 0x15, 0x00),
    (0x2B, 0x00, 0x04, 0x2B, 0x00), (0x2A, 0x00, 0x04, 0x3D, 0x00),
    (0x2E, 0x00, 0x08, 0x0F, 0x00),
)
ACTION_MAP = {row[0]: row for row in ACTION_TABLE}


@dataclass(frozen=True)
class ActionInfo:
    code: int
    label: str
    group: str
    needs: str = ""  # "", "shortcut", "fire", "macro", "gun", "left_macro"


ACTION_INFO = (
    ActionInfo(0x00, "Button Off", "Basic"),
    ActionInfo(0x01, "Left Click", "Basic"),
    ActionInfo(0x02, "Right Click", "Basic"),
    ActionInfo(0x03, "Middle Button", "Basic"),
    ActionInfo(0x04, "Forward", "Basic"),
    ActionInfo(0x05, "Backward", "Basic"),
    ActionInfo(0x06, "DPI Cycle", "Basic"),
    ActionInfo(0x07, "DPI +", "Basic"),
    ActionInfo(0x08, "DPI -", "Basic"),
    ActionInfo(0x09, "Double Click", "Basic"),
    ActionInfo(0x0A, "Fire Click", "Basic", "fire"),
    ActionInfo(0x0B, "Scroll Up", "Basic"),
    ActionInfo(0x0C, "Scroll Down", "Basic"),
    ActionInfo(0x12, "Three Click", "Basic"),
    ActionInfo(0x15, "Shortcut", "Basic", "shortcut"),
    ActionInfo(0x16, "Select Macro", "Basic", "macro"),
    ActionInfo(0x19, "Send Gun", "Advanced"),
    ActionInfo(0x1A, "Mode Switch", "Advanced"),
    ActionInfo(0x32, "Light Mode Switch", "Advanced"),
    ActionInfo(0x39, "Set Left Macro", "Advanced", "left_macro"),
    ActionInfo(0x79, "Set Gun", "Advanced", "gun"),
    ActionInfo(0x68, "Report +", "Advanced"),
    ActionInfo(0x69, "Report -", "Advanced"),
    ActionInfo(0x70, "Report Cycle", "Advanced"),
    ActionInfo(0x71, "Sniper Key", "Advanced"),
    ActionInfo(0x20, "Cut", "Windows"),
    ActionInfo(0x21, "Copy", "Windows"),
    ActionInfo(0x22, "Paste", "Windows"),
    ActionInfo(0x23, "Open", "Windows"),
    ActionInfo(0x24, "Save", "Windows"),
    ActionInfo(0x25, "Find", "Windows"),
    ActionInfo(0x26, "Redo", "Windows"),
    ActionInfo(0x28, "Select All", "Windows"),
    ActionInfo(0x29, "Print", "Windows"),
    ActionInfo(0x2A, "Close Window", "Windows"),
    ActionInfo(0x2B, "Swap Windows", "Windows"),
    ActionInfo(0x2C, "Show Desktop", "Windows"),
    ActionInfo(0x2D, "Run Command", "Windows"),
    ActionInfo(0x2E, "Lock PC", "Windows"),
    ActionInfo(0x2F, "New", "Windows"),
    ActionInfo(0x40, "Media Player", "Multimedia"),
    ActionInfo(0x41, "Play / Pause", "Multimedia"),
    ActionInfo(0x42, "Stop", "Multimedia"),
    ActionInfo(0x43, "Previous Track", "Multimedia"),
    ActionInfo(0x44, "Next Track", "Multimedia"),
    ActionInfo(0x45, "Volume +", "Multimedia"),
    ActionInfo(0x46, "Volume -", "Multimedia"),
    ActionInfo(0x47, "Mute", "Multimedia"),
    ActionInfo(0x48, "Browser Home", "Browser"),
    ActionInfo(0x49, "Browser Favorites", "Browser"),
    ActionInfo(0x4A, "Browser Forward", "Browser"),
    ActionInfo(0x4B, "Browser Backward", "Browser"),
    ActionInfo(0x4C, "Browser Stop", "Browser"),
    ActionInfo(0x4D, "Browser Refresh", "Browser"),
    ActionInfo(0x4E, "Browser Search", "Browser"),
    ActionInfo(0x4F, "Email", "Browser"),
    ActionInfo(0x50, "Calculator", "Browser"),
    ActionInfo(0x51, "My Computer", "Browser"),
)
ACTION_INFO_MAP = {a.code: a for a in ACTION_INFO}
ACTION_GROUPS = ("Basic", "Advanced", "Windows", "Multimedia", "Browser")


def action_label(code: int) -> str:
    info = ACTION_INFO_MAP.get(code)
    return info.label if info else f"Action 0x{code:02X}"


def action_group(code: int) -> str:
    info = ACTION_INFO_MAP.get(code)
    return info.group if info else "Advanced"


def action_needs(code: int) -> str:
    info = ACTION_INFO_MAP.get(code)
    return info.needs if info else ""


def validate_buttons(profile: Profile) -> bool:
    """The original refuses an apply with no Left Click / Send Gun action."""
    return any(b.action in (0x01, 0x19) for b in profile.buttons)


# ---------------------------------------------------------------------------
# Button table (0x12)
# ---------------------------------------------------------------------------

# FUN_00406db0 refuses a new macro once the mode already holds ten (0x16)
# buttons and a new gun once it holds three (0x39/0x79 counted together).
MACRO_TABLE_LIMIT = 10
GUN_TABLE_LIMIT = 3
# FUN_0041ab50 only assigns a macro slot while its counter is below 12,
# i.e. table indices 1..11 are addressable.
MACRO_TABLE_MAX_INDEX = 11


def macro_table_slots(profile: Profile) -> dict[int, tuple[str, int]]:
    """Map physical button slot -> ``(kind, 0x13 table index)``.

    FUN_0041ab50 numbers macro buttons densely from 1 and gun/left-macro
    buttons from 4, with two independent counters.  The shipped driver never
    copied gun tables into the upload buffer, so a gun pointing at a slot that
    a fourth macro already occupies never mattered there.  Our studio does
    upload gun tables, so it keeps the vendor numbering while the preferred
    slot is free and otherwise allocates the next unused index -- every
    descriptor always names the table we actually send.

    Empty actions are numbered too, exactly like the vendor encoder; this
    keeps later indices stable even when a macro has no events yet.
    """
    macros: list[int] = []
    guns: list[int] = []
    for index in range(64):
        action = profile.button(index).action
        if action == 0x16:
            macros.append(index)
        elif action in (0x39, 0x79):
            guns.append(index)
    macros = macros[:MACRO_TABLE_LIMIT]
    guns = guns[:GUN_TABLE_LIMIT]

    out: dict[int, tuple[str, int]] = {}
    for table_index, slot in enumerate(macros, 1):
        out[slot] = ("macro", table_index)

    used = set(range(1, len(macros) + 1))
    free = [i for i in range(4, MACRO_TABLE_MAX_INDEX + 1) if i not in used]
    free += [i for i in range(1, MACRO_TABLE_MAX_INDEX + 1)
             if i not in used and i not in free]
    for slot in guns:
        if not free:
            break
        out[slot] = ("gun", free.pop(0))
    return out


def table_budget_messages(macros: int, guns: int) -> list[str]:
    """Explain macro/gun bindings the shared 1..11 table range cannot hold.

    Macros and guns both live in the same 0x13 table slots.  The vendor rules
    allow ten macros and three guns per profile, but thirteen tables cannot fit
    in eleven indices, so the surplus descriptors are left unpointed (C = 0)
    and the bound button stays silent on the mouse.  Surfacing that turns a
    "the macro/gun just doesn't work" report into an actionable message.
    """
    out: list[str] = []
    if macros > MACRO_TABLE_LIMIT:
        out.append(
            f"{macros} macros are bound, but the firmware runs at most "
            f"{MACRO_TABLE_LIMIT} per profile; the last "
            f"{macros - MACRO_TABLE_LIMIT} will not work.")
    if guns > GUN_TABLE_LIMIT:
        out.append(
            f"{guns} gun/left-macro buttons are bound, but the firmware runs "
            f"at most {GUN_TABLE_LIMIT} per profile; the last "
            f"{guns - GUN_TABLE_LIMIT} will not work.")
    total = macros + guns
    if total > MACRO_TABLE_MAX_INDEX:
        out.append(
            f"{total} macro/gun tables are bound, but only "
            f"{MACRO_TABLE_MAX_INDEX} can be uploaded; the last "
            f"{total - MACRO_TABLE_MAX_INDEX} will not work. Remove a macro "
            f"or gun binding in this profile.")
    return out


def table_budget_warnings(profile: Profile) -> list[str]:
    """Same messages for a built Profile record (used by the apply path)."""
    macros = sum(1 for i in range(64)
                 if profile.button(i).action == 0x16)
    guns = sum(1 for i in range(64)
               if profile.button(i).action in (0x39, 0x79))
    return table_budget_messages(macros, guns)


def build_button_slots(profile: Profile, config: DeviceConfig) -> tuple[bytes, int, int]:
    """Return (256-byte staging table, macro slot counter, gun slot counter)."""
    staging = bytearray(256)
    tables = macro_table_slots(profile)
    macro_counter = 1
    gun_counter = 0
    for index in range(64):
        entry = profile.button(index)
        action = entry.action
        if config.button_is_computed(index):
            row = ACTION_MAP.get(action)
            if row is None:
                a = b = c = d = 0
            else:
                a, b, c, d = row[1], row[2], row[3], row[4]
            if action == 0x15:
                b = entry.shortcut_mods
                c = entry.shortcut_key
            elif action == 0x0A:
                b = 0xF0
                c = entry.fire_interval & 0xFF
                d = entry.fire_count & 0xFF
            elif action == 0x16:
                b = entry.macro_index
                assigned = tables.get(index)
                if assigned is not None and assigned[0] == "macro":
                    c = assigned[1]
                    macro_counter += 1
                else:
                    # More than ten macros in one layer: the vendor refuses
                    # the extra binding, so leave the descriptor unpointed
                    # instead of referencing a table we cannot upload.
                    c = 0
            elif action in (0x39, 0x79):
                assigned = tables.get(index)
                if assigned is not None and assigned[0] == "gun":
                    a, b, c, d = 0x08, 0x00, assigned[1], 0x00
                    gun_counter += 1
                else:
                    a, b, c, d = 0x08, 0x00, 0x00, 0x00
            staging[index * 4:index * 4 + 4] = bytes((a, b, c, d))
        else:
            raw = config.raw_button(index)
            staging[index * 4:index * 4 + 4] = bytes(raw[:4])
    return bytes(staging), macro_counter, gun_counter


def button_frames(slots: bytes) -> list[tuple[bytes, bytes, bytes]]:
    """Four frames of header + two 32-byte blocks."""
    if len(slots) != 256:
        raise ValueError("button table must be 256 bytes")
    out = []
    for i in range(4):
        payload = slots[i * 64:(i + 1) * 64]
        out.append((frame(0x12, (i + 1, 0x40, 0, 0, 0)), payload[:32], payload[32:64]))
    return out


# ---------------------------------------------------------------------------
# Macro table (0x13)
# ---------------------------------------------------------------------------

def encode_macro_event(event: MacroEvent) -> bytes:
    """Encode one 16-byte event into the 0x13 event stream."""
    delta = event.delay & 0xFFFF
    state = event.state
    if delta < 0x4F7:
        tenths = delta // 10
        if state == 0:
            a = event.a & 0xFFFF
            b = event.b & 0xFFFF
            return bytes((tenths, 0xFB, a & 0xFF, a >> 8, b & 0xFF, b >> 8))
        timing = tenths | (1 if state == 1 else 0x81)
        return bytes((timing, event.opcode & 0xFF))
    q = delta // 20
    r = (delta % 20 + 5) // 10
    if state == 0:
        a = event.a & 0xFFFF
        b = event.b & 0xFFFF
        return bytes((0x00, 0xFB, a & 0xFF, a >> 8, b & 0xFF, b >> 8,
                      0x00, 0x01, (q >> 8) & 0xFF, q & 0xFF))
    timing = r | (0x80 if state == 2 else 0)
    return bytes((timing, event.opcode & 0xFF, 0x00, 0x01, (q >> 8) & 0xFF, q & 0xFF))


def build_macro_block(entry: ButtonEntry, *, byte_order_loop: bool = True) -> bytes:
    """Build one 128-byte macro table entry for a macro-bearing button."""
    block = bytearray(128)
    loop = entry.loop & 0xFFFF
    # FUN_0041ab50:140-141 builds the header with CONCAT11(low, high), which
    # lands on the stack as high byte then low byte: the loop count is stored
    # big-endian.  Keep the flag so the choice stays explicit and testable.
    block[0] = (loop >> 8) if byte_order_loop else (loop & 0xFF)
    block[1] = (loop & 0xFF) if byte_order_loop else ((loop >> 8) & 0xFF)
    offset = 2
    events = entry.event_slice()
    if len(events) > MAX_EVENTS:
        raise PacketError("macro has more than 40 events")
    for event in events:
        encoded = encode_macro_event(event)
        if offset + len(encoded) > 128:
            raise PacketError("macro is too large for the device (128-byte table entry)")
        block[offset:offset + len(encoded)] = encoded
        offset += len(encoded)
    return bytes(block)


def _gun_row_parts(row) -> tuple[int, int, int]:
    """Return ``(x, y, delay)`` for a Bullet or a ``[x, y, delay]`` list."""
    if isinstance(row, Bullet):
        return int(row.x), int(row.y), int(row.delay)
    values = (list(row) + [0, 0, 10])[:3]
    return int(values[0]), int(values[1]), int(values[2])


def gun_encoded_size(rows) -> int:
    """Bytes one recoil pattern consumes in the 128-byte 0x13 table entry.

    FUN_0041ab50 writes a 4-byte row ``(timing, 0xF0, 0x81, 0xF0)`` for a
    zero offset and an 8-byte row for a real one.  The old 3-byte count made
    the editor believe a 16th real bullet fit when the firmware table was
    already full at fifteen.
    """
    rows = list(rows or ())[:MAX_BULLETS]
    size = 2                      # loop header
    for row in rows:
        x, y, _delay = _gun_row_parts(row)
        size += 4 if x == 0 and y == 0 else 8
    if len(rows) > 15:
        size += 4                 # end-of-first-half + start-of-second-half
    return size


def gun_fits(rows) -> tuple[bool, str]:
    """Check a recoil pattern against the device's 128-byte table limit."""
    rows = list(rows or ())[:MAX_BULLETS]
    if not rows:
        return False, "a gun pattern needs at least one bullet row"
    size = gun_encoded_size(rows)
    if size > 128:
        return False, (f"this pattern needs {size} bytes; the device table "
                       "holds 128 (remove rows or use shorter offsets)")
    return True, ""


def build_gun_block(entry: ButtonEntry, ordinal: int = 1) -> bytes:
    """Encode the 30-row recoil table.

    The original builds this block but never copies it into the upload buffer
    (the Gun tab is hidden in the shipped build), so this layout is inferred
    from the encoder and is marked experimental.
    """
    block = bytearray(128)
    loop = entry.loop & 0xFFFF
    # Same big-endian header as the macro block (FUN_0041ab50:319-320).
    block[0] = (loop >> 8) & 0xFF
    block[1] = loop & 0xFF
    offset = 2
    rows = entry.bullet_slice()[:MAX_BULLETS]
    ok, message = gun_fits(rows)
    if not ok:
        raise PacketError(message)

    def put_row(row: Bullet) -> None:
        nonlocal offset
        tenths = (row.delay // 10) & 0xFF
        if row.x == 0 and row.y == 0:
            # Vendor zero row: (timing|1, 0xF0, 0x81, 0xF0).  The trailing
            # 0xF0 is required; without it every following row shifts by one
            # byte and the firmware reads garbage offsets.
            data = bytes((tenths | 1, 0xF0, 0x81, 0xF0))
        else:
            data = bytes((tenths | 1, 0xF0, 0x00, 0xFA,
                          abs(row.x) & 0xFF, abs(row.y) & 0xFF, 0x81, 0xF0))
        if offset + len(data) > 128:
            raise PacketError("gun table is too large for the device")
        block[offset:offset + len(data)] = data
        offset += len(data)

    first = rows[:15]
    second = rows[15:]
    for row in first:
        put_row(row)
    if second:
        if offset + 2 <= 128:
            # FUN_0041ab50: the descriptor pass increments its gun counter for
            # every 0x39/0x79 button it meets, and the split marker is written
            # afterwards as (counter + 2) * 2.  The first pattern therefore
            # marks with 6, the second with 8, the third with 10.  ``ordinal``
            # is 1-based and counts 0x39 and 0x79 together, matching that pass.
            block[offset] = ((ordinal + 2) * 2) & 0xFF
            block[offset + 1] = 0xFE
            offset += 2
        # second half marker observed in the encoder
        if offset + 2 <= 128:
            block[offset] = 0x00
            block[offset + 1] = 0x01
            offset += 2
        for row in second:
            put_row(row)
    return bytes(block)


def macro_blocks(profile: Profile) -> list[tuple[int, bytes]]:
    """Return ``(0x13 table index, 128-byte block)`` in upload order.

    Indices come from :func:`macro_table_slots`, so a button descriptor always
    points at the table that actually carries its macro or gun.  A binding the
    firmware cannot hold (more than 40 events, or more encoded bytes than the
    128-byte entry) is replaced by an empty table instead of raising: one bad
    macro must never abort the whole apply and leave the mouse half-written.
    """
    tables = macro_table_slots(profile)
    gun_slots = [i for i in range(64)
                 if profile.button(i).action in (0x39, 0x79)]
    gun_ordinal = {slot: n for n, slot in enumerate(gun_slots, 1)}
    out: list[tuple[int, bytes]] = []
    for slot, (kind, table_index) in tables.items():
        entry = profile.button(slot)
        block = bytes(128)
        if entry.count:
            try:
                # 0x39 ("Set Left Macro") shares the 0x13 block number range
                # with guns but carries macro events, not recoil rows.
                if entry.action in (0x16, 0x39):
                    block = build_macro_block(entry)
                else:
                    block = build_gun_block(entry, gun_ordinal.get(slot, 1))
            except PacketError as exc:
                _macro_log.warning(
                    "button %d %s table %d disabled: %s",
                    slot + 1, kind, table_index, exc)
        out.append((table_index, block))
    out.sort(key=lambda item: item[0])
    return out


def macro_frames(profile: Profile) -> list[tuple[bytes, bytes]]:
    """Each frame is (header, 128-byte payload split into four 32-byte blocks)."""
    return [(frame(0x13, (index, 0x80, 0, 0, 0)), block)
            for index, block in macro_blocks(profile)]


# ---------------------------------------------------------------------------
# DPI table (0x11)
# ---------------------------------------------------------------------------

# Code lookup for the shipped 3311 / 0x0CEF sensor; index 0..120.
DPI_CODE_TABLE = bytes((
    0x50, 0x00, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x09, 0x0A, 0x0B, 0x0C,
    0x0D, 0x0E, 0x10, 0x11, 0x12, 0x13, 0x14, 0x16, 0x17, 0x18, 0x19, 0x1A,
    0x1B, 0x1D, 0x1E, 0x1F, 0x20, 0x21, 0x23, 0x25, 0x26, 0x27, 0x28, 0x29,
    0x2A, 0x2C, 0x2D, 0x2E, 0x2F, 0x30, 0x32, 0x33, 0x34, 0x35, 0x36, 0x38,
    0x39, 0x3A, 0x3B, 0x3C, 0x3E, 0x3F, 0x40, 0x41, 0x42, 0x44, 0x45, 0x46,
    0x47, 0x48, 0x4A, 0x4B, 0x4C, 0x4D, 0x4E, 0x50, 0x51, 0x52, 0x53, 0x54,
    0x56, 0x57, 0x58, 0x59, 0x5A, 0x5C, 0x5D, 0x5E, 0x5F, 0x60, 0x62, 0x63,
    0x64, 0x65, 0x66, 0x68, 0x69, 0x6A, 0x6B, 0x6C, 0x6E, 0x6F, 0x70, 0x71,
    0x72, 0x74, 0x75, 0x76, 0x77, 0x78, 0x7A, 0x7B, 0x7C, 0x7D, 0x7E, 0x80,
    0x81, 0x82, 0x83, 0x84, 0x86, 0x87, 0x88, 0x89, 0x8A, 0x8C, 0x8D, 0x8E,
    0x8F,
))


def dpi_code(dpi: int, sensor: int) -> int:
    dpi = max(0, int(dpi))
    if sensor == 0x0CEF:
        index = dpi if dpi < 121 else dpi // 2
        if 0 <= index < len(DPI_CODE_TABLE):
            return DPI_CODE_TABLE[index]
        return 0x8F
    if sensor == 0x0CFD:
        if dpi <= 50:
            return 0x00
        return max(0, (dpi // 2) - 1) & 0xFF
    index = min(120, dpi if dpi < 121 else dpi // 2)
    return DPI_CODE_TABLE[index]


def build_dpi_block(profile: Profile, sensor: int) -> bytes:
    block = bytearray(32)
    for i in range(8):
        block[i] = dpi_code(profile.dpi_values[i], sensor)
    return bytes(block)


# ---------------------------------------------------------------------------
# Light / palette / status / high-DPI
# ---------------------------------------------------------------------------

LIGHT_THRESHOLD_SENSORS = (0x0D07, 0x0D2A, 0x0CEF)
HIGH_DPI_THRESHOLD = {0x0D07: 0xA0, 0x0D2A: 200, 0x0CEF: 0x78}

# Which controls the 0x0D frame actually consumes for each mode.  Keys are the
# Profile/LED fields: "length" is the vendor's 0..4 Frequency slider (+0xF8),
# "direction" is its 0..4 Length slider (+0x100), and "frequency" is the
# binary fixed/cycle colour mode (+0xFC) that the vendor exposes as two radio
# buttons.  Keeping the historical config keys avoids breaking saved files;
# the panel shows the vendor's labels.
LIGHT_PARAMETERS = {
    0: (),
    1: ("brightness", "frequency"),
    2: ("length", "frequency"),
    3: ("length", "brightness"),
    4: ("length", "brightness"),
    5: ("brightness", "frequency"),
    6: ("direction", "frequency"),
    7: ("direction", "frequency"),
    8: ("brightness", "toggle"),
    9: ("brightness", "frequency", "length"),
    10: ("brightness", "length"),
    11: ("brightness", "frequency"),
}

# Which controls the vendor's Light page *shows* for each mode.  This is not
# the same as LIGHT_PARAMETERS: FUN_0040eaf0 hides the whole Color Setting
# section for Neon, Wave, Marbles and Flying star even though the firmware
# still reads +0xFC when it builds those frames.  Values use the Profile field
# names so the panel can map them directly; "colour" stands for the Color
# Setting section (Fix Colour radio, Loop Colour radio and eight swatches).
LIGHT_UI_CONTROLS = {
    0: (),
    1: ("brightness", "colour"),
    2: ("length", "colour"),
    3: ("brightness", "length"),
    4: ("brightness", "length"),
    5: ("brightness", "colour"),
    6: ("direction", "colour"),
    7: ("direction", "colour"),
    8: ("brightness", "colour"),
    9: ("brightness", "length", "colour"),
    10: ("brightness", "length"),
    11: ("brightness",),
}

# Vendor effect names.  The driver lists the twelve effects in two columns:
# left column modes 0-5, right column modes 6-11.
LIGHT_MODE_LABELS = {
    0: "Off",
    1: "Standard",
    2: "Breathing",
    3: "Neon",
    4: "Wave",
    5: "Key reaction",
    6: "Trailing",
    7: "Drag back and forth",
    8: "Slide",
    9: "YO-YO",
    10: "Marbles",
    11: "Flying star",
}


def light_parameters(mode: int) -> tuple[str, ...]:
    return LIGHT_PARAMETERS.get(int(mode), ())


def light_mode_label(mode: int) -> str:
    return LIGHT_MODE_LABELS.get(int(mode), f"Mode {int(mode)}")


def light_frame(profile: Profile) -> bytes:
    """Encode the 0x0D light frame exactly as FUN_00418a40 does.

    Every field is clamped here as a last line of defence: a profile record
    edited or imported by anything other than this studio must never reach the
    firmware with an out-of-range LED byte.  ``frequency`` is the fixed/cycle
    colour mode (+0xFC, 0 or 1); the vendor maps 1 to 2 before encoding.
    """
    raw_mode = profile.light_mode
    mode = clamp_light_mode(raw_mode)
    if mode != raw_mode:
        _light_log.warning("lighting effect %s is out of range; encoded as %d",
                           raw_mode, mode)

    def checked(name):
        raw = getattr(profile, name)
        value = clamp_light_value(name, raw)
        if value != raw:
            # This is the last line of defence: a corrupt field that reached
            # the encoder is worth a log line, because the firmware has no way
            # to reject a semantically invalid LED byte.
            _light_log.warning("lighting %s=%s is out of range; encoded as %s",
                               name, raw, value)
        return value

    brightness = checked("brightness")
    length = checked("length")
    frequency = checked("frequency")
    if frequency == 1:
        frequency = 2
    direction = checked("direction")
    byte2 = 0
    byte3 = 0
    if mode == 0:
        pass
    elif mode == 1:
        byte2, byte3 = brightness, frequency
    elif mode == 2:
        # The vendor precomputes ``4 - +0xF8`` and subtracts it again here, so
        # byte 2 is the stored value itself (not 4 - length).
        byte2, byte3 = length, frequency
    elif mode in (3, 4):
        byte2, byte3 = length, brightness
    elif mode == 5:
        byte2, byte3 = brightness, frequency
    elif mode in (6, 7):
        byte2, byte3 = (4 - direction) & 0xFF, frequency
    elif mode == 8:
        byte2, byte3 = brightness, 1 if frequency else 0
    elif mode == 9:
        byte2, byte3 = brightness, (frequency | (((4 - length) & 0x0F) << 4)) & 0xFF
    elif mode == 10:
        byte2, byte3 = brightness, (4 - length) & 0xFF
    elif mode == 11:
        byte2, byte3 = brightness, frequency
    # FUN_00418a40 writes the mode at byte 1: [0x0D, mode, byte2, byte3, 0, 0, 0, chk].
    return frame(0x0D, (mode, byte2, byte3, 0, 0, 0))


def palette_block(colors: list[int]) -> bytes:
    """Pack eight COLORREFs into the vendor's 24-byte RGB block.

    FUN_00418a40 does not copy the eight 4-byte COLORREFs at profile
    +0x110 / +0xD0 verbatim.  It rebuilds the payload byte by byte, dropping
    each entry's pad byte, so the first 24 bytes are R1 G1 B1 ... R8 G8 B8
    followed by eight zero bytes.  Sending the COLORREFs as-is introduced a
    pad byte after every colour, which shifted entries 2..8 by one byte and
    made the mouse show a different colour than the studio swatch.
    """
    out = bytearray()
    values = [int(c) & 0xFFFFFFFF for c in list(colors)[:8]]
    values.extend([0] * (8 - len(values)))
    for value in values:
        out += struct.pack("<I", value)[:3]
    out += b"\x00" * 8
    return bytes(out)


def high_dpi_mask(profile: Profile, sensor: int) -> int:
    threshold = HIGH_DPI_THRESHOLD.get(sensor)
    if threshold is None:
        return 0
    mask = 0
    stages = profile.dpi_values
    limit = profile.stage_count
    for i in range(min(8, limit)):
        if stages[i] > threshold:
            mask |= 1 << i
    return mask & 0xFF


def status_frame(profile: Profile, reply: bytes | None = None) -> bytes:
    """The 0x03 status set that follows the 0x83 query (FUN_004196b0).

    On the wire the official app does NOT send constants here: in every USB
    capture (52 apply cycles, Office and Game mode) the frame is
    ``03 02 0F F2 40 00 00 <chk>``, i.e. bytes 1-3 and 5-6 are copied from the
    device's own reply to the 0x83 query (``83 02 0F F2 40 00 00``), byte 3 keeps
    the reply's other bits with bit 3 following the lift-off flag, and byte 4 is
    forced to the 0x40 marker.  Pass the de-obfuscated reply to reproduce that.
    Without a usable reply (demo mode, short or foreign reply) this falls back to
    the old constant frame.
    """
    lift = 0x08 if profile.lift == 1 else 0x00
    if reply is not None and len(reply) >= 7 and reply[0] == 0x83:
        return frame(0x03, (reply[1], reply[2], (reply[3] & 0xF7) | lift,
                            0x40, reply[5], reply[6]))
    return frame(0x03, (0x00, 0x00, lift, 0x40, 0, 0))


def lod_frame(profile: Profile, config: DeviceConfig) -> bytes:
    stage = profile.lod
    code = config.distance_value_for_stage(stage) if 0 <= stage < 8 else 0
    return frame(0x04, (code, profile.key_response & 0xFF, 0, 0, 0))


def mode_frame(profile: Profile) -> bytes:
    return frame(0x02, ((profile.mode & 0xFF) + 1, 0, 0, 0, 0))


def rate_frame(profile: Profile) -> bytes:
    idx = max(0, min(3, profile.rate))
    return frame(0x01, (RATE_PACKET[idx], 0, 0, 0, 0))


def stage_frame(profile: Profile) -> bytes:
    return frame(0x0B, ((profile.stage & 0xFF) + 1, 0, 0, 0, 0))


def fixed_color_frame(profile: Profile) -> bytes:
    r, g, b = profile.fixed_rgb
    return frame(0x0C, (r, g, b, 0, 0, 0))


def palette_header(block_index: int) -> bytes:
    return frame(0x10, (block_index & 0xFF, 0x18, 0, 0, 0))


def dpi_header(profile: Profile) -> bytes:
    return frame(0x11, (profile.stage_count & 0xFF, 0x08, 0, 0, 0))


def commit_frame() -> bytes:
    return frame(0x08, (0xAA, 0xCC, 0xEE, 0, 0, 0))


def high_dpi_frame(profile: Profile, sensor: int) -> bytes:
    return frame(0x07, (0x00, high_dpi_mask(profile, sensor), 0, 0, 0))


# ---------------------------------------------------------------------------
# Sensor display helpers
# ---------------------------------------------------------------------------

SENSOR_INFO = {
    0x0CFD: (2, 100, "10000", lambda s: s * 100),
    0x0C8C: (1, 189, "7560", lambda s: s * 40),
    0x0BEA: (1, 12, "4000", lambda s: (250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000)[max(0, min(11, s - 1))]),
    0x13BA: (1, 17, "2750", lambda s: s),
    0x0CFF: (2, 120, "12000", lambda s: s * 100),
    0x0D07: (1, 160, "19000", lambda s: s * 100),
    0x24: (1, 80, "8000", lambda s: s * 100),
    0x25: (1, 120, "12000", lambda s: s * 100),
    0x26: (1, 160, "16000", lambda s: s * 100),
    0x3C: (1, 240, "24000", lambda s: s * 100),
    0x1900: (4, 248, "12400", lambda s: (s - 100) * 100 if s > 200 else s * 50),
    0x0C20: (16, 212, "8480", lambda s: s * 40),
    0x0D02: (1, 144, "7200", lambda s: (s - 100) * 100 if s > 200 else s * 50),
    0x0D05: (2, 160, "16000", lambda s: s * 100),
    0x0D2A: (1, 290, "19000", lambda s: s * 50),
    0x0CEF: (1, 240, "24000", lambda s: s * 100),
}


def sensor_limits(sensor: int) -> tuple[int, int]:
    info = SENSOR_INFO.get(sensor)
    if info:
        return info[0], info[1]
    return 1, 240


def sensor_max_label(sensor: int) -> str:
    info = SENSOR_INFO.get(sensor)
    return info[2] if info else "24000"


def sensor_display_dpi(sensor: int, stage_value: int) -> int:
    info = SENSOR_INFO.get(sensor)
    if not info:
        return stage_value * 100
    try:
        return int(info[3](stage_value))
    except Exception:
        return stage_value


def describe_apply(profile: Profile, config: DeviceConfig) -> list[str]:
    """Human-readable apply plan used by the diagnostics panel."""
    lines = []
    lines.append(f"mode -> {profile.mode + 1} "
                 f"({'game' if profile.mode else 'office'})")
    lines.append(f"report rate -> {RATE_PACKET[max(0, min(3, profile.rate))]} ms")
    lines.append(f"active DPI stage -> {profile.stage + 1}")
    lines.append(f"DPI stages -> {profile.stage_count}: {profile.dpi_values[:profile.stage_count]}")
    lines.append(f"LED color -> RGB{profile.fixed_rgb}")
    lines.append(f"light mode -> {profile.light_mode}")
    lines.append(f"button table -> {sum(1 for i in range(64) if config.button_is_computed(i))} computed slots")
    if config.distance:
        lines.append(f"LOD -> code {config.distance_value_for_stage(profile.lod)}, key response {profile.key_response} ms")
    lines.append(f"high-DPI mask -> 0x{high_dpi_mask(profile, config.sensor):02X}")
    return lines
