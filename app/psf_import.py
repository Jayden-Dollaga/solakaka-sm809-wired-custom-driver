"""
app.psf_import -- read-only importer for the official software's .psf profiles.

The stock utility stores each profile as a UTF-16LE INI-style file (its
``config/default0..4.psf`` or an exported copy).  This module parses one into
the wired studio's config schema (see app.profile_store) so an existing setup
can be migrated.  It is READ-ONLY: it never writes a .psf.

Format notes (verified against the reference SM809 Pro captures):

- BUTTONS: ``Key{0..15}Value`` are 3-byte action codes in the reference
  device's protocol-slot order.  The reference has its OWN slot order (it is
  not the wired one), so ``_PSF_PERMUTE[n]`` maps Key n to the 0-based physical
  button and the action is then placed in the wired slot for that button.
- DPI: ``XYSetting{1..8}ValueX`` (newer) or ``XYSetting{n}Value`` (older) hold
  the 16-bit raw DPI, ``(raw + 1) * 100`` display DPI.  ``DPIOffOnFlagValue``
  is the enabled-stage bitmask and ``CurrentDPILevelValue`` the active stage.
  ``DPILevelIndication{0..7}Valuer`` are RRGGBB stage colours.
- POLLING: ``PollingRateValue`` first byte is the reference polling enum.
- LIGHTING: ``Lighting1ModeValue`` first byte is the reference effect id.
- AUTO-SWITCH: ``GameFile0/1/2`` -> match rules (usually blank).
- MACROS: ``MacroKey{n}Name`` / ``MacroActionNum`` / ``AllAction`` blocks are
  8-byte VK records; keyboard events decode to our HID macro events.

The reference and the wired SM809 use DIFFERENT button/lighting vocabularies,
so this importer translates the reference codes into wired actions.  Anything
with no wired equivalent (DPI-lock, host-side Run App, unknown consumer
usages) becomes Disabled and is reported in ``warnings`` instead of being
silently mangled.
"""

from __future__ import annotations

import copy
import os
import re

from sm809pro import actions as A
from sm809pro import defaults as D


class PsfError(Exception):
    pass


# The reference driver's slot -> 0-based physical button table.  It differs
# from the wired mouse's own SLOT_ORDER (buttons 6-8 and 15-16 sit in other
# slots), so .psf keys must be translated through THIS table first.
_PSF_PERMUTE = (11, 12, 13, 14, 15, 9, 10, 0, 1, 2, 3, 4, 5, 8, 6, 7)


# ---------------------------------------------------------------------------
# Reference (wireless Pro) -> wired translations
# ---------------------------------------------------------------------------
# Wireless mouse-class codes (0x10) -> wired mouse actions.
_MOUSE = {
    0x01: 0x01,   # left
    0x02: 0x02,   # right
    0x04: 0x03,   # middle
    0x10: 0x04,   # forward
    0x08: 0x05,   # back
}

# Wireless DPI-class (0x40) -> wired DPI actions.
_DPI = {0x01: 0x06, 0x02: 0x07, 0x03: 0x08}

# Wireless special-class (0x60) -> wired actions.  Run App (0x05) is a
# host-side launcher that the wired firmware does not implement.
_SPECIAL = {0x00: 0x00, 0x04: 0x32}

# Wireless consumer (0x80) -> wired action, keyed by (usage low, usage high).
_CONSUMER = {
    (0x83, 0x01): 0x40,   # media select
    (0xB6, 0x00): 0x43,   # previous track
    (0xB5, 0x00): 0x44,   # next track
    (0xB7, 0x00): 0x42,   # stop
    (0xCD, 0x00): 0x41,   # play / pause
    (0xE2, 0x00): 0x47,   # mute
    (0xE9, 0x00): 0x45,   # volume +
    (0xEA, 0x00): 0x46,   # volume -
    (0x8A, 0x01): 0x4F,   # email
    (0x92, 0x01): 0x50,   # calculator
    (0x94, 0x01): 0x51,   # my computer
    (0x23, 0x02): 0x48,   # browser home
    (0x2A, 0x02): 0x49,   # browser favourites
    (0x25, 0x02): 0x4A,   # browser forward
    (0x24, 0x02): 0x4B,   # browser backward
    (0x26, 0x02): 0x4C,   # browser stop
    (0x27, 0x02): 0x4D,   # browser refresh
    (0x21, 0x02): 0x4E,   # browser search
}

# Wireless polling byte -> Hz (POLLING_ENUM in the reference driver).
_PSF_POLLING = {1: 1000, 2: 500, 4: 250, 8: 125}

# Wireless lighting effect id -> (wired mode, optional fixed colour, note).
# The two firmwares number their effects differently, so this maps by look and
# feel rather than by index.  Fixed-colour modes become Standard + that colour.
_LIGHT_MAP = {
    0: (0, None, ""),                                   # Off
    1: (11, None, "Stars Twinkle -> Flying star"),      # sparkle
    2: (4, None, "Colorful Streaming -> Wave"),         # flowing colours
    3: (4, None, "Seven-color Stretch -> Wave"),
    4: (3, None, "Seven-color Flash -> Neon"),
    5: (2, None, "Colorful Breath -> Breathing"),
    6: (9, None, "Seven-color Explosion -> YO-YO"),
    7: (5, None, "Colorful Coverage -> Key reaction"),
    8: (1, (255, 0, 0), "Red -> Standard (red)"),
    9: (1, (0, 255, 0), "Green -> Standard (green)"),
    10: (1, (0, 0, 255), "Blue -> Standard (blue)"),
}
_REF_LIGHT_NAMES = {
    0: "Off", 1: "Stars Twinkle", 2: "Colorful Streaming",
    3: "Seven-color Stretch", 4: "Seven-color Flash", 5: "Colorful Breath",
    6: "Seven-color Explosion", 7: "Colorful Coverage", 8: "Red",
    9: "Green", 10: "Blue",
}


# Windows Virtual-Key -> USB HID usage. The .psf stores macro keystrokes as VK
# codes (decoded from macro.psf: a0 48 45 4c 4c 4f = Shift H E L L O = "Hello").
def _build_vk_to_hid():
    m = {}
    for i in range(26):                 # A-Z
        m[0x41 + i] = 0x04 + i
    for i in range(1, 10):              # 1-9
        m[0x30 + i] = 0x1E + (i - 1)
    m[0x30] = 0x27                      # 0
    m.update({
        0x0D: 0x28, 0x1B: 0x29, 0x08: 0x2A, 0x09: 0x2B, 0x20: 0x2C,  # enter esc bksp tab space
        0xBD: 0x2D, 0xBB: 0x2E, 0xDB: 0x2F, 0xDD: 0x30, 0xDC: 0x31,  # - = [ ] backslash
        0xBA: 0x33, 0xDE: 0x34, 0xC0: 0x35, 0xBC: 0x36, 0xBE: 0x37, 0xBF: 0x38,  # ; ' ` , . /
        0x14: 0x39,                                                  # caps lock
        0x2C: 0x46, 0x91: 0x47, 0x13: 0x48, 0x2D: 0x49, 0x24: 0x4A,  # prtsc scroll pause ins home
        0x21: 0x4B, 0x2E: 0x4C, 0x23: 0x4D, 0x22: 0x4E,              # pgup del end pgdn
        0x27: 0x4F, 0x25: 0x50, 0x28: 0x51, 0x26: 0x52,              # right left down up
        # modifiers (left/right + the generic VK_SHIFT/CONTROL/MENU)
        0xA0: 0xE1, 0xA1: 0xE5, 0xA2: 0xE0, 0xA3: 0xE4, 0xA4: 0xE2, 0xA5: 0xE6,
        0x5B: 0xE3, 0x5C: 0xE7, 0x10: 0xE1, 0x11: 0xE0, 0x12: 0xE2,
    })
    for i in range(12):                 # F1-F12
        m[0x70 + i] = 0x3A + i
    for i in range(10):                 # numpad 0-9 (NP1..NP9 = 0x59.., NP0 = 0x62)
        m[0x61 + i] = 0x59 + i
    m[0x60] = 0x62
    m.update({0x6F: 0x54, 0x6A: 0x55, 0x6D: 0x56, 0x6B: 0x57, 0x6E: 0x63, 0x90: 0x53})
    return m


VK_TO_HID = _build_vk_to_hid()


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
def parse_psf_text(text):
    """Flatten a .psf into {key: value}. Keys are unique enough across the file
    (Key0Value, XYSetting1ValueX, ...) that a flat dict is sufficient; section
    headers and indentation (tabs) are ignored."""
    d = {}
    for line in text.lstrip("\ufeff").splitlines():
        line = line.strip()
        if not line or line.startswith("[") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        d[k.strip()] = v.strip()
    return d


def read_psf_text(path):
    try:
        with open(path, "r", encoding="utf-16-le") as f:
            text = f.read()
    except Exception as e:
        raise PsfError(f"Could not read .psf (expected UTF-16LE): {e}")
    if "Key0Value" not in text and "DPIOffOnFlagValue" not in text:
        raise PsfError("This does not look like an SM809 .psf profile.")
    return text


def read_psf(path):
    return parse_psf_text(read_psf_text(path))


def decode_macro_events(blob):
    """Decode a .psf AllAction blob (8-byte records) to our macro event list.

    Record = [VK, up?(0x80 in byte1), 0, 0, type(0x03=keyboard), 0, delay_hi,
    delay_lo]. Verified vs macro.psf ("Hello" via VK codes a0/48/45/4c/4f).
    Only keyboard events are decoded (the only type seen); others are skipped.
    """
    try:
        b = bytes.fromhex(blob)
    except (TypeError, ValueError):
        return []
    events = []
    for i in range(0, len(b) - 7, 8):
        rec = b[i:i + 8]
        if not any(rec):
            break
        vk, flag, etype = rec[0], rec[1], rec[4]
        delay = (rec[6] << 8) | rec[7]
        if etype in (0x00, 0x03):           # keyboard
            hid = VK_TO_HID.get(vk)
            if hid is None:
                continue
            events.append({"type": "key", "keycode": hid,
                           "down": not (flag & 0x80), "next_delay": delay})
    return events


_MACRO_BLOCK = re.compile(
    r"MacroKey(\d+)Name=([^\r\n]*)[\s\S]*?MacroActionNum=(\d+)"
    r"[\s\S]*?AllAction=([0-9A-Fa-f]+)")


def to_macros(text, d):
    """Extract per-key macros bound on a 0x90 (play-macro) button.

    Returns ``{tempid, name, events, phys, playmode, repeat}`` records where
    ``phys`` is the 1-based physical button.  Macros with no decodable events
    are skipped; the caller turns their buttons into Disabled + a warning.
    """
    out = []
    for m in _MACRO_BLOCK.finditer(text):
        n, name, num, blob = (int(m.group(1)), m.group(2).strip(),
                              int(m.group(3)), m.group(4))
        val = d.get(f"Key{n}Value", "")
        if num == 0 or not val.startswith("90") or len(val) < 6:
            continue
        try:
            code = bytes.fromhex(val[:6])
        except ValueError:
            continue
        events = decode_macro_events(blob)
        if not events:
            continue
        out.append({"tempid": f"psf{n}", "name": name or f"Imported {n}",
                    "events": events, "phys": _PSF_PERMUTE[n] + 1,
                    "playmode": ((code[1] >> 4) & 0x0F) or 1,
                    "repeat": code[2]})
    return out


# ---------------------------------------------------------------------------
# Field decoders
# ---------------------------------------------------------------------------
def _hexbyte(s, default=0):
    """First byte of a hex field. .psf packs multi-byte values big-endian, e.g.
    Lighting1ModeValue=080000 -> 0x08.  The single-byte fields
    (DPIOffOnFlagValue=3F) also take the first two chars correctly."""
    try:
        return int(str(s).strip()[:2], 16) & 0xFF
    except (TypeError, ValueError):
        return default


def _bool01(s, default=False):
    if s is None:
        return default
    return s.strip() not in ("0", "00", "", "false", "False")


def _translate_code(code):
    """Reference 3-byte action -> wired 3-byte tuple, or None if unsupported."""
    try:
        t, p1, p2 = int(code[0]) & 0xFF, int(code[1]) & 0xFF, int(code[2]) & 0xFF
    except Exception:
        return None
    if t == 0x10:
        return (_MOUSE[p1], 0, 0) if p1 in _MOUSE else None
    if t == 0x30:
        if p1 == 0x32 and p2 == 0x03:
            return (0x12, 0, 0)                 # Three Click
        return (0x0A, p1, p2)                   # Fire Click
    if t == 0x40:
        return (_DPI[p1], 0, 0) if p1 in _DPI else None
    if t == 0x50:
        return None                             # reference DPI lock
    if t == 0x60:
        return (_SPECIAL[p1], 0, 0) if p1 in _SPECIAL else None
    if t == 0x70:
        return (0x15, p1, p2)                   # keyboard shortcut
    if t == 0x80:
        wired = _CONSUMER.get((p1, p2))
        return (wired, 0, 0) if wired is not None else None
    if t == 0xFF:
        return (0x00, 0, 0)                     # unset
    return None


def _buttons(d, warnings):
    """Build a wired 64-slot binding list from the .psf Key0..15 entries.

    The reference profile has one 16-button layer; the wired mouse has Office
    and Game layers.  The imported actions are written to BOTH layers so they
    work whichever mode the mouse is in.
    """
    codes = [copy.deepcopy(c) for c in D.button_codes()]
    for n in range(A.NUM_BUTTONS):
        v = d.get(f"Key{n}Value")
        if not v or len(v) < 6:
            continue
        try:
            raw = bytes.fromhex(v[:6])
        except ValueError:
            continue
        label = d.get(f"Key{n}Name") or f"physical {_PSF_PERMUTE[n] + 1}"
        if raw[0] == 0x90:
            # Macro binding: resolved by the caller when the macro decodes.
            continue
        wired = _translate_code(raw)
        if wired is None:
            warnings.append(
                f"Button {_PSF_PERMUTE[n] + 1} ({label}): action "
                f"{raw.hex().upper()} has no wired SM809 equivalent; disabled.")
            wired = (0x00, 0, 0)
        phys = _PSF_PERMUTE[n]
        for base in A.LAYER_BASES:
            codes[base + A.PHYS_ORDER[phys]] = wired
    return codes


def _dpi(d):
    flag = _hexbyte(d.get("DPIOffOnFlagValue", "FF"), 0xFF)
    enabled = bin(flag).count("1") or D.DPI_ENABLED_COUNT
    enabled = max(1, min(8, enabled))
    values = []
    for i in range(1, enabled + 1):
        raw = d.get(f"XYSetting{i}ValueX") or d.get(f"XYSetting{i}Value")
        if raw is None:
            values.append(D.DPI_VALUES[i - 1])
            continue
        try:
            # The reference stores (dpi / 100) - 1.
            values.append((int(raw, 16) + 1) * 100)
        except ValueError:
            values.append(D.DPI_VALUES[i - 1])
    values = [max(D.DPI_MIN, min(D.DPI_MAX, int(v))) for v in values]
    colors = []
    for i in range(enabled):
        c = d.get(f"DPILevelIndication{i}Valuer", "FFFFFF")
        try:
            colors.append([int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)])
        except ValueError:
            colors.append([255, 255, 255])
    selected = _hexbyte(d.get("CurrentDPILevelValue", "0"), 0)
    selected = max(0, min(enabled - 1, selected))
    return {"values": values, "colors": colors,
            "enabled_count": enabled, "selected": selected}


def _polling(d):
    raw = _hexbyte(d.get("PollingRateValue", "02"), 0)
    if raw in _PSF_POLLING:
        return _PSF_POLLING[raw]
    # 17/18/20 are 2000/4000/8000 Hz on the reference; the wired mouse tops
    # out at 1000 Hz.
    return 1000 if raw in (17, 18, 20) else D.POLLING_HZ


def _lighting(d, warnings):
    ref_mode = _hexbyte(d.get("Lighting1ModeValue", "00"), 0)
    wired_mode, color, note = _LIGHT_MAP.get(ref_mode, (0, None, ""))
    if ref_mode not in _LIGHT_MAP:
        warnings.append(
            f"Lighting effect {ref_mode} is not in the reference table; "
            "lighting was turned off.")
    elif note:
        warnings.append(
            f"Lighting: {note} (the two firmwares number effects differently).")
    light = dict(D.config()["lighting"])
    light["mode"] = wired_mode
    if color is not None:
        light["color"] = list(color)
    return light


def to_config(d, warnings=None):
    """Map a parsed .psf dict to the wired studio's profile config schema."""
    warnings = warnings if warnings is not None else []
    return {
        "buttons": _buttons(d, warnings),
        "dpi": _dpi(d),
        "polling_hz": _polling(d),
        "lod_mm": D.LOD_MM,          # wired LOD is a code, not millimetres
        "key_response": 4,
        "mode": 0,
        "lighting": _lighting(d, warnings),
        "pointer": {
            "speed": D.POINTER_SPEED,
            "scroll": D.POINTER_SCROLL,
            "double": D.POINTER_DOUBLE,
            "enhance": D.POINTER_ENHANCE,
            "onepage": D.POINTER_ONEPAGE,
            "wheel_reverse": D.WHEEL_REVERSED,
        },
    }


def to_match_rules(d):
    """GameFile0/1/2 -> match rules (exe basename). Usually blank: the stock
    app has no auto-switch UI, so these are filled in OUR app."""
    rules = []
    for i in range(3):
        g = (d.get(f"GameFile{i}") or "").strip()
        if g:
            rules.append({"exe": os.path.basename(g).lower(), "title": None})
    return rules


def import_psf(path):
    """Parse a .psf file into a profile-ready dict:

        {"name": str, "match_rules": [...], "config": {...},
         "macros": [...], "warnings": [...]}

    ``macros`` are decoded library macros with temporary ids (``psf<n>``);
    the caller remaps them to real MacroStore ids and updates the matching
    button bindings.  Raises PsfError on unreadable / non-.psf input.
    """
    text = read_psf_text(path)
    d = parse_psf_text(text)
    name = (d.get("ProfileName")
            or os.path.splitext(os.path.basename(path))[0]).strip()
    warnings = []
    config = to_config(d, warnings)
    macros = to_macros(text, d)

    # Point each macro button at its temporary macro id.  Buttons whose 0x90
    # code had no decodable macro block stay disabled.
    macro_slots = set()
    for mac in macros:
        phys0 = mac["phys"] - 1
        macro_slots.add(phys0)
        binding = {"macro": mac["tempid"], "name": mac["name"],
                   "events": mac["events"], "playmode": mac["playmode"],
                   "repeat": mac["repeat"]}
        for base in A.LAYER_BASES:
            config["buttons"][base + A.PHYS_ORDER[phys0]] = copy.deepcopy(binding)
    for n in range(A.NUM_BUTTONS):
        v = d.get(f"Key{n}Value", "")
        if v.startswith("90") and _PSF_PERMUTE[n] not in macro_slots:
            warnings.append(
                f"Button {_PSF_PERMUTE[n] + 1}: macro data could not be decoded; "
                "the button was disabled.")
            phys0 = _PSF_PERMUTE[n]
            for base in A.LAYER_BASES:
                config["buttons"][base + A.PHYS_ORDER[phys0]] = (0x00, 0, 0)

    return {"name": name or "Imported", "match_rules": to_match_rules(d),
            "config": config, "macros": macros, "warnings": warnings}
