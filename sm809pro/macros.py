"""Macro helpers for the wired SM809 studio.

Macros are edited as a list of atomic events in the reference UI. The wired
firmware stores up to 40 events per button in a 128-byte macro table entry, so
:data:`MAX_MACRO_EVENTS` is 40 and long delays can use more of the entry.

Event dictionaries use the same shape as the studio editor:
    {"type": "key",   "keycode": <HID usage>, "down": bool, "next_delay": ms}
    {"type": "mouse", "button": 1..7,          "down": bool, "next_delay": ms}
    {"type": "delay", "ms": ms}
"""

from __future__ import annotations

from .actions import HID

# Wired firmware: 40 events per button macro (128-byte table entry).
MAX_MACRO_EVENTS = 40

MOUSE_BITS = {1: 0x01, 2: 0x02, 3: 0x04, 4: 0x08, 5: 0x10, 6: 0x20, 7: 0x40}

KEY_LCTRL = 0xE0
KEY_LSHIFT = 0xE1
KEY_LALT = 0xE2
KEY_LGUI = 0xE3


def _build_char_map():
    """char -> (HID usage, needs_shift) for printable ASCII (US layout)."""
    m = {}
    for i in range(26):
        m[chr(ord("a") + i)] = (0x04 + i, False)
        m[chr(ord("A") + i)] = (0x04 + i, True)
    for i, ch in enumerate("1234567890"):
        m[ch] = (0x1E + i if ch != "0" else 0x27, False)
    for i, ch in enumerate("!@#$%^&*()"):
        m[ch] = (0x1E + i if i < 9 else 0x27, True)
    m.update({
        "-": (0x2D, False), "_": (0x2D, True),
        "=": (0x2E, False), "+": (0x2E, True),
        "[": (0x2F, False), "{": (0x2F, True),
        "]": (0x30, False), "}": (0x30, True),
        "\\": (0x31, False), "|": (0x31, True),
        ";": (0x33, False), ":": (0x33, True),
        "'": (0x34, False), '"': (0x34, True),
        "`": (0x35, False), "~": (0x35, True),
        ",": (0x36, False), "<": (0x36, True),
        ".": (0x37, False), ">": (0x37, True),
        "/": (0x38, False), "?": (0x38, True),
        " ": (0x2C, False), "\t": (0x2B, False), "\n": (0x28, False),
    })
    return m


CHAR_MAP = _build_char_map()


def text_to_events(text: str, key_delay: int = 10) -> list:
    """Turn a literal string into press/release key events (US layout)."""
    evs = []
    for ch in text:
        entry = CHAR_MAP.get(ch) or CHAR_MAP.get(ch.lower())
        if entry is None:
            continue
        usage, shift = entry
        if shift:
            evs.append({"type": "key", "keycode": KEY_LSHIFT, "down": True, "next_delay": key_delay})
            evs.append({"type": "key", "keycode": usage, "down": True, "next_delay": key_delay})
            evs.append({"type": "key", "keycode": usage, "down": False, "next_delay": key_delay})
            evs.append({"type": "key", "keycode": KEY_LSHIFT, "down": False, "next_delay": key_delay})
        else:
            evs.append({"type": "key", "keycode": usage, "down": True, "next_delay": key_delay})
            evs.append({"type": "key", "keycode": usage, "down": False, "next_delay": key_delay})
        if len(evs) >= MAX_MACRO_EVENTS:
            del evs[MAX_MACRO_EVENTS:]
            break
    return evs


def macro_fits(events) -> tuple[bool, str]:
    from wired.bridge import macro_fits as _fits
    return _fits(events)


def to_wired(events):
    from wired.bridge import ref_events_to_wired
    return ref_events_to_wired(events)


def key_label(usage: int) -> str:
    from .actions import HID_NAMES
    if usage in HID_NAMES:
        return HID_NAMES[usage].title()
    return f"0x{usage:02X}"


__all__ = [
    "MAX_MACRO_EVENTS", "HID", "MOUSE_BITS", "CHAR_MAP", "text_to_events",
    "macro_fits", "to_wired", "key_label", "KEY_LCTRL", "KEY_LSHIFT",
    "KEY_LALT", "KEY_LGUI",
]
