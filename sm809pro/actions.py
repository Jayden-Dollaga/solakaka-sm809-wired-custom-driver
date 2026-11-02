"""Wired SM809 action vocabulary for the studio UI.

Every button action is a 3-byte tuple ``(action, p1, p2)`` in the wired
firmware's own vocabulary (see :mod:`wired.protocol`). Keyboard shortcuts are
``(0x15, modifier_mask, key_id)`` and rapid fire is
``(0x0A, interval_ms, count)``. Macro bindings are kept as ``dict`` objects in
the UI and embedded into the button entry on apply.

The wired SM809 has 16 physical buttons (numbered 1-16 in the reference
artwork) and 64 firmware slots. The vendor driver exposes two modes: Office
Mode edits slots 0-15 and Game Mode edits slots 32-47; the remaining groups
hold raw/wheel entries the vendor never shows. The vendor Keys page lists
each mode in *physical* order (side pad 1-9, thumb pair 10-11, primary 12-14,
DPI pair 15-16), while the profile stores them in a different slot order.
``PHYS_ORDER`` below encodes that vendor order.
"""

from __future__ import annotations

from pathlib import Path

NUM_BUTTONS = 16          # physical buttons shown per mode
SLOT_COUNT = 64           # firmware button table
LAYER_COUNT = 2           # Office Mode and Game Mode (vendor Keys page)
LAYER_SIZE = NUM_BUTTONS
LAYER_BASES = (0, 32)     # first firmware slot of each mode
LAYER_LABELS = ("Office Mode", "Game Mode")

# Vendor Keys-page order, recovered from res\buttonpage.xml: the controls are
# laid out as slots 6,7,8,9,10,11,13,14 (left) and 12,15,16,1,2,3,4,5 (right),
# i.e. 0-based (5,6,7,8,9,10,12,13,11,14,15,0,1,2,3,4).  Row numbers 1-16 in
# that page are the physical buttons in images\mouse.png, so
# PHYS_ORDER[phys - 1] is the slot inside a mode's 16-slot block.
PHYS_ORDER = (5, 6, 7, 8, 9, 10, 12, 13, 11, 14, 15, 0, 1, 2, 3, 4)
# Inverse: SLOT_ORDER[slot] is the 0-based physical row for that slot.
SLOT_ORDER = (11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 8, 6, 7, 9, 10)
# PERMUTE[slot] = 0-based physical button (same convention as the reference
# studio; psf_import relies on it).
PERMUTE = list(SLOT_ORDER)

# Modifier mask bits for 0x15 shortcuts.
MOD_CTRL = 0x01
MOD_SHIFT = 0x02
MOD_ALT = 0x04
MOD_WIN = 0x08

# USB HID keyboard usages. Wired key ids are HID-like, so these values can be
# stored directly in macro events and shortcut actions.
HID = {
    "a": 0x04, "b": 0x05, "c": 0x06, "d": 0x07, "e": 0x08, "f": 0x09,
    "g": 0x0A, "h": 0x0B, "i": 0x0C, "j": 0x0D, "k": 0x0E, "l": 0x0F,
    "m": 0x10, "n": 0x11, "o": 0x12, "p": 0x13, "q": 0x14, "r": 0x15,
    "s": 0x16, "t": 0x17, "u": 0x18, "v": 0x19, "w": 0x1A, "x": 0x1B,
    "y": 0x1C, "z": 0x1D,
    "1": 0x1E, "2": 0x1F, "3": 0x20, "4": 0x21, "5": 0x22,
    "6": 0x23, "7": 0x24, "8": 0x25, "9": 0x26, "0": 0x27,
    "enter": 0x28, "esc": 0x29, "backspace": 0x2A, "tab": 0x2B, "space": 0x2C,
    "del": 0x4C, "insert": 0x49, "home": 0x4A, "end": 0x4D,
    "page up": 0x4B, "page down": 0x4E, "print screen": 0x46, "pause": 0x48,
    "up": 0x52, "down": 0x51, "left": 0x50, "right": 0x4F,
    "f1": 0x3A, "f2": 0x3B, "f3": 0x3C, "f4": 0x3D, "f5": 0x3E, "f6": 0x3F,
    "f7": 0x40, "f8": 0x41, "f9": 0x42, "f10": 0x43, "f11": 0x44, "f12": 0x45,
    "f13": 0x68, "f14": 0x69, "f15": 0x6A, "f16": 0x6B, "f17": 0x6C, "f18": 0x6D,
    "f19": 0x6E, "f20": 0x6F, "f21": 0x70, "f22": 0x71, "f23": 0x72, "f24": 0x73,
    "-": 0x2D, "=": 0x2E, "[": 0x2F, "]": 0x30, "\\": 0x31,
    ";": 0x33, "'": 0x34, "`": 0x35, ",": 0x36, ".": 0x37, "/": 0x38,
    "caps lock": 0x39, "scroll lock": 0x47, "num lock": 0x53,
    "num /": 0x54, "num *": 0x55, "num -": 0x56, "num +": 0x57, "num enter": 0x58,
    "num 1": 0x59, "num 2": 0x5A, "num 3": 0x5B, "num 4": 0x5C, "num 5": 0x5D,
    "num 6": 0x5E, "num 7": 0x5F, "num 8": 0x60, "num 9": 0x61, "num 0": 0x62,
    "num .": 0x63, "menu": 0x65,
    # Left/right modifier keys as keys in their own right (the original
    # driver's "Key" field accepts LShift/RShift/LAlt/… just like any other
    # key). These are HID usages too, so they store directly in a 0x15
    # shortcut's key id and in macro events.
    "left ctrl": 0xE0, "left shift": 0xE1, "left alt": 0xE2, "left win": 0xE3,
    "right ctrl": 0xE4, "right shift": 0xE5, "right alt": 0xE6, "right win": 0xE7,
}

# Reverse names for display.
HID_NAMES = {v: k for k, v in HID.items()}


def kb(usage: int, mods: int = 0) -> tuple:
    """Keyboard shortcut action: (0x15, modifier_mask, key_id)."""
    return (0x15, mods & 0xFF, (usage or 0) & 0xFF)


def fire(interval_ms: int = 50, count: int = 0) -> tuple:
    """Rapid fire: (0x0A, interval, count). count=0 fires while held."""
    return (0x0A, interval_ms & 0xFF, count & 0xFF)


# Named single actions, straight from the wired ACTION_INFO table.
BTN = {
    "unset": (0x00, 0x00, 0x00),
    "disable": (0x00, 0x00, 0x00),
    "left": (0x01, 0x00, 0x00),
    "right": (0x02, 0x00, 0x00),
    "middle": (0x03, 0x00, 0x00),
    "forward": (0x04, 0x00, 0x00),
    "back": (0x05, 0x00, 0x00),
    "dpi_cycle": (0x06, 0x00, 0x00),
    "dpi_up": (0x07, 0x00, 0x00),
    "dpi_down": (0x08, 0x00, 0x00),
    "double": (0x09, 0x00, 0x00),
    "fire": fire(50, 0),
    "scroll_up": (0x0B, 0x00, 0x00),
    "scroll_down": (0x0C, 0x00, 0x00),
    "triple": (0x12, 0x00, 0x00),
    "mode_switch": (0x1A, 0x00, 0x00),
    "send_gun": (0x19, 0x00, 0x00),
    "set_gun": (0x79, 0x00, 0x00),
    "light_toggle": (0x32, 0x00, 0x00),
    "sniper": (0x71, 0x00, 0x00),
    "report_up": (0x68, 0x00, 0x00),
    "report_down": (0x69, 0x00, 0x00),
    "report_cycle": (0x70, 0x00, 0x00),
    # Windows
    "cut": (0x20, 0x00, 0x00),
    "copy": (0x21, 0x00, 0x00),
    "paste": (0x22, 0x00, 0x00),
    "open": (0x23, 0x00, 0x00),
    "save": (0x24, 0x00, 0x00),
    "find": (0x25, 0x00, 0x00),
    "undo": (0x26, 0x00, 0x00),
    "select_all": (0x28, 0x00, 0x00),
    "print": (0x29, 0x00, 0x00),
    "close_window": (0x2A, 0x00, 0x00),
    "swap_windows": (0x2B, 0x00, 0x00),
    "display_desktop": (0x2C, 0x00, 0x00),
    "run": (0x2D, 0x00, 0x00),
    "lock_pc": (0x2E, 0x00, 0x00),
    "new": (0x2F, 0x00, 0x00),
    # Multimedia
    "media_select": (0x40, 0x00, 0x00),
    "play_pause": (0x41, 0x00, 0x00),
    "stop": (0x42, 0x00, 0x00),
    "prev_track": (0x43, 0x00, 0x00),
    "next_track": (0x44, 0x00, 0x00),
    "vol_up": (0x45, 0x00, 0x00),
    "vol_down": (0x46, 0x00, 0x00),
    "mute": (0x47, 0x00, 0x00),
    # Browser / shell
    "browser_home": (0x48, 0x00, 0x00),
    "browser_favorites": (0x49, 0x00, 0x00),
    "browser_forward": (0x4A, 0x00, 0x00),
    "browser_back": (0x4B, 0x00, 0x00),
    "browser_stop": (0x4C, 0x00, 0x00),
    "browser_refresh": (0x4D, 0x00, 0x00),
    "browser_search": (0x4E, 0x00, 0x00),
    "email": (0x4F, 0x00, 0x00),
    "calculator": (0x50, 0x00, 0x00),
    "my_computer": (0x51, 0x00, 0x00),
}

ACTION_LABELS = {
    "unset": "Disabled",
    "left": "Left Click", "right": "Right Click", "middle": "Middle Click",
    "forward": "Forward", "back": "Backward", "double": "Double Click",
    "scroll_up": "Scroll Up", "scroll_down": "Scroll Down",
    "triple": "Three Click", "dpi_cycle": "DPI Cycle", "dpi_up": "DPI +",
    "dpi_down": "DPI -", "fire": "Fire Click", "mode_switch": "Mode Switch",
    "send_gun": "Send Gun", "set_gun": "Set Gun",
    "light_toggle": "Light Mode Switch",
    "sniper": "Sniper Key", "report_up": "Report +", "report_down": "Report -",
    "report_cycle": "Report Cycle", "cut": "Cut", "copy": "Copy", "paste": "Paste",
    "open": "Open", "save": "Save", "find": "Find", "undo": "Redo",
    "select_all": "Select All", "print": "Print", "close_window": "Close Window",
    "swap_windows": "Swap Windows", "display_desktop": "Show Desktop",
    "run": "Run Command", "lock_pc": "Lock PC", "new": "New",
    "media_select": "Media Player", "play_pause": "Play / Pause",
    "stop": "Stop", "prev_track": "Previous Track", "next_track": "Next Track",
    "vol_up": "Volume +", "vol_down": "Volume -", "mute": "Mute",
    "browser_home": "Browser Home", "browser_favorites": "Browser Favorites",
    "browser_forward": "Browser Forward", "browser_back": "Browser Backward",
    "browser_stop": "Browser Stop", "browser_refresh": "Browser Refresh",
    "browser_search": "Browser Search", "email": "Email",
    "calculator": "Calculator", "my_computer": "My Computer",
}

# Legacy name kept for small imports/tests; wired hardware has no DPI lock or
# host-side Run App action.
FACTORY_DEFAULTS = [BTN["unset"]] * NUM_BUTTONS


def slot_for_physical(phys: int, mode: int = 0) -> int:
    """0-based firmware slot for a 1-based physical button in a mode."""
    base = LAYER_BASES[max(0, min(LAYER_COUNT - 1, int(mode)))]
    row = max(1, min(NUM_BUTTONS, int(phys))) - 1
    return base + PHYS_ORDER[row]


def physical_to_slots(codes_by_physical) -> list:
    """Reorder a 16-entry physical list into the slot order the device expects."""
    def get(phys0):
        c = codes_by_physical[phys0] if phys0 < len(codes_by_physical) else None
        if c is None:
            return BTN["unset"]
        return dict(c) if isinstance(c, dict) else tuple(c)
    return [get(SLOT_ORDER[s]) for s in range(NUM_BUTTONS)]


# ---------------------------------------------------------------------------
# Factory slots
# ---------------------------------------------------------------------------

_DEFAULT_CODES = None


def _fallback_codes():
    codes = [BTN["unset"]] * SLOT_COUNT
    # Physical order 1-16 (same list the vendor Keys page shows).
    physical = [
        BTN["display_desktop"], kb(HID["2"]), kb(HID["3"]), BTN["forward"],
        kb(HID["5"]), kb(HID["6"]), kb(HID["7"]), kb(HID["8"]), BTN["back"],
        fire(2, 0), BTN["my_computer"], BTN["left"], BTN["right"], BTN["middle"],
        BTN["dpi_up"], BTN["dpi_down"],
    ]
    codes[:16] = physical_to_slots(physical)
    codes[30] = BTN["scroll_up"]
    codes[31] = BTN["scroll_down"]
    codes[62] = BTN["scroll_up"]
    codes[63] = BTN["scroll_down"]
    return codes


def default_button_codes():
    """The wired factory button table (read from ``Default.pbin`` if present)."""
    global _DEFAULT_CODES
    if _DEFAULT_CODES is not None:
        return [dict(c) if isinstance(c, dict) else tuple(c) for c in _DEFAULT_CODES]
    codes = None
    try:
        from wired.bridge import binding_from_entry
        from wired.model import Profile
        from wired.paths import DEVICE_DATA_DIR, SEED_DIR

        for candidate in (DEVICE_DATA_DIR / "Default.pbin",
                          SEED_DIR / "Data" / "Default.pbin"):
            if candidate.exists():
                prof = Profile.from_file(Path(candidate))
                codes = [binding_from_entry(prof.button(i), i, "default")
                         for i in range(SLOT_COUNT)]
                break
    except Exception:
        codes = None
    _DEFAULT_CODES = codes or _fallback_codes()
    return [dict(c) if isinstance(c, dict) else tuple(c) for c in _DEFAULT_CODES]


def default_button_code(slot: int):
    codes = default_button_codes()
    if 0 <= slot < len(codes):
        return codes[slot]
    return BTN["unset"]


def macro_slot_for(slot: int) -> int:
    """Firmware slot index used when embedding a macro for a button slot."""
    return max(0, min(15, int(slot)))
