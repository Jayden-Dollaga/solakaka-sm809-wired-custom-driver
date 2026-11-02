"""Translation between the studio's JSON config and a wired Profile record.

The wired mouse stores one complete binary profile at a time (64 button slots,
8 DPI stages, LED parameters, Windows pointer settings, embedded macros). The
studio UI keeps the same shapes it always used for panels, but every value is
now translated to/from a :class:`wired.model.Profile`.

Only the host configuration is changed here; no hardware I/O happens in this
module.
"""

from __future__ import annotations

import logging
from typing import Callable, Iterable

from .keys import shortcut_name
from .model import (
    BUTTON_COUNT,
    LIGHT_VALUE_RANGES,
    MAX_BULLETS,
    MAX_EVENTS,
    Bullet,
    MacroEvent,
    Profile,
    clamp_light_mode,
    clamp_light_value,
    colorref_to_rgb,
    rgb_to_colorref,
    set_wheel_reversed,
    wheel_reversed,
)
from .protocol import (
    ACTION_INFO_MAP,
    LIGHT_MODE_LABELS,
    gun_fits,
    sensor_display_dpi,
    table_budget_messages,
)

_bind_log = logging.getLogger("sm809.bindings")

# The stored byte is the 0-based report-rate *option index*, not a frequency.
# FUN_00418a40 maps it to the 0x01 frame payload as index 0 -> 8 ms (125 Hz),
# 1 -> 4 ms (250 Hz), 2 -> 2 ms (500 Hz), 3 -> 1 ms (1000 Hz); the 0x05 monitor
# report maps the interval back to the same index (8/4/2/1 -> 0/1/2/3).
# Keep this in step with RATE_PACKET: payload = 1000 / index_to_hz[index].
RATE_TO_HZ = {0: 125, 1: 250, 2: 500, 3: 1000}
HZ_TO_RATE = {hz: idx for idx, hz in RATE_TO_HZ.items()}

MOUSE_OPCODE = {1: 0xF0, 2: 0xF1, 3: 0xF2, 4: 0xF3, 5: 0xF4, 6: 0xF7, 7: 0xF8}
MOUSE_FROM_OPCODE = {v: k for k, v in MOUSE_OPCODE.items()}
MOUSE_LABELS = {
    1: "Left", 2: "Right", 3: "Middle", 4: "Back", 5: "Forward",
    6: "Wheel Up", 7: "Wheel Down",
}

STATE_PRESS = 1
STATE_RELEASE = 2
STATE_NONE = 0


def rate_hz(rate: int) -> int:
    return RATE_TO_HZ.get(int(rate), 500)


def rate_index(hz: int) -> int:
    return HZ_TO_RATE.get(int(hz), 1)


def dpi_to_display(sensor: int, raw: int) -> int:
    """Firmware DPI stage value -> the DPI shown in the studio UI."""
    return int(sensor_display_dpi(int(sensor), int(raw)))


def dpi_from_display(sensor: int, display: int) -> int:
    """Studio DPI -> firmware stage value for the configured sensor."""
    display = max(100, int(display))
    if int(sensor) == 0x0CEF:
        return _clamp(round(display / 100.0), 0, 240)
    if int(sensor) == 0x0CFD:
        return _clamp(round(display / 100.0), 0, 120)
    if int(sensor) == 0x0C8C:
        return _clamp(round(display / 40.0), 0, 189)
    if int(sensor) == 0x0D2A:
        return _clamp(round(display / 50.0), 0, 290)
    # Unknown/identity sensors: the UI value is the stored stage value.
    return _clamp(round(display), 0, 40000)



def _clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, int(v)))


# ---------------------------------------------------------------------------
# Macro events: studio dicts <-> wired MacroEvent
# ---------------------------------------------------------------------------

def ref_events_to_wired(events: Iterable[dict]) -> list[MacroEvent]:
    """Translate the macro editor's event list to wired events.

    A studio event carries ``next_delay`` *after* the event. Wired events store
    the delay *before* the event, so the accumulator shifts by one event.
    Consumer/media events are not part of the wired macro table and are dropped.
    """
    out: list[MacroEvent] = []
    pending = 0
    for ev in events or ():
        if not isinstance(ev, dict):
            continue
        kind = ev.get("type")
        if kind == "delay":
            pending += max(0, int(ev.get("ms", 0)))
            continue
        opcode = None
        if kind == "key":
            opcode = int(ev.get("keycode", 0)) & 0xFF
        elif kind == "mouse":
            opcode = MOUSE_OPCODE.get(int(ev.get("button", 1)))
        else:
            # media/consumer events have no wired macro opcode
            continue
        if not opcode:
            continue
        state = STATE_PRESS if ev.get("down", True) else STATE_RELEASE
        out.append(MacroEvent(
            opcode=opcode, state=state,
            delay=max(0, min(0xFFFF, pending)),
            # Vendor events carry opaque bytes the encoder copies back
            # verbatim; keep them when a macro came from a .mbin/profile.
            a=int(ev.get("a", 0) or 0) & 0xFFFFFFFF,
            b=int(ev.get("b", 0) or 0) & 0xFFFFFFFF,
            b0=int(ev.get("b0", 0) or 0) & 0xFF,
            b3=int(ev.get("b3", 0) or 0) & 0xFF,
            w6=int(ev.get("w6", 0) or 0) & 0xFFFF,
        ))
        if len(out) >= MAX_EVENTS:
            break
        pending = max(0, int(ev.get("next_delay", 0)))
    if pending and out:
        # trailing pause: wire it as an explicit delay record
        out.append(MacroEvent(opcode=0, state=STATE_NONE,
                              delay=max(0, min(0xFFFF, pending))))
    return out[:MAX_EVENTS]


def wired_events_to_ref(events: Iterable[MacroEvent]) -> list[dict]:
    """Translate wired macro records back to the editor's event dicts."""
    out: list[dict] = []
    for raw in events or ():
        ev = raw
        if ev.state == STATE_NONE or not ev.opcode:
            if ev.delay:
                out.append({"type": "delay", "ms": int(ev.delay)})
            continue
        delay = int(ev.delay)
        if delay:
            if out and out[-1].get("type") != "delay":
                out[-1]["next_delay"] = int(out[-1].get("next_delay", 0)) + delay
            else:
                out.append({"type": "delay", "ms": delay})
        down = ev.state == STATE_PRESS
        if ev.opcode in MOUSE_FROM_OPCODE:
            item = {"type": "mouse", "button": MOUSE_FROM_OPCODE[ev.opcode],
                    "down": down, "next_delay": 0}
        else:
            item = {"type": "key", "keycode": int(ev.opcode),
                    "down": down, "next_delay": 0}
        # Preserve the vendor's opaque event bytes so a macro imported from a
        # .mbin/profile exports and re-applies without losing them.
        for key, value in (("a", ev.a), ("b", ev.b), ("b0", ev.b0),
                           ("b3", ev.b3), ("w6", ev.w6)):
            if value:
                item[key] = int(value)
        out.append(item)
    return out


def macro_fits(events: Iterable[dict]) -> tuple[bool, str]:
    """Check the event list against the 40-event and 128-byte table limits."""
    wired = ref_events_to_wired(events)
    if len(wired) > MAX_EVENTS:
        return False, f"the device stores at most {MAX_EVENTS} macro events"
    # 128-byte table entry: 2-byte loop header + encoded events.
    size = 2
    for ev in wired:
        if ev.delay < 0x4F7:
            size += 6 if ev.state == STATE_NONE else 2
        else:
            size += 10 if ev.state == STATE_NONE else 6
    if size > 128:
        return False, "this macro is too long for the device's 128-byte table"
    return True, ""


def macro_binding_problem(events) -> str:
    """Return why a macro cannot be bound, or '' when it can.

    The device table holds 40 events and 128 encoded bytes.  ``macro_fits``
    alone misses two cases the picker used to accept: a macro with only delay
    rows (nothing to play) and a list holding more than 40 real events (the
    translator silently truncates it).  Both are rejected here before a
    binding is written, so the failure is visible instead of silent.
    """
    items = list(events or ())
    if not items:
        return "the macro has no events"
    actionable = 0
    for ev in items:
        if not isinstance(ev, dict):
            continue
        kind = ev.get("type")
        if kind == "key" and ev.get("keycode"):
            actionable += 1
        elif kind == "mouse" and MOUSE_OPCODE.get(int(ev.get("button", 1) or 1)):
            actionable += 1
    if actionable == 0:
        return "the macro has no key or mouse events"
    if actionable > MAX_EVENTS:
        return (f"the macro has {actionable} events; the device stores at "
                f"most {MAX_EVENTS}")
    ok, message = macro_fits(items)
    return "" if ok else message


# ---------------------------------------------------------------------------
# Gun (recoil) patterns: studio rows <-> wired Bullet records
# ---------------------------------------------------------------------------

def gun_rows_to_wired(rows) -> list[Bullet]:
    """Coerce ``[[x, y, delay], ...]`` to wired Bullet records."""
    out: list[Bullet] = []
    for row in (rows or ())[:MAX_BULLETS]:
        try:
            x, y, delay = (list(row) + [0, 0, 10])[:3]
            out.append(Bullet(
                x=max(-255, min(255, int(x))),
                y=max(-255, min(255, int(y))),
                delay=max(0, min(0xFFFF, int(delay))),
            ))
        except (TypeError, ValueError):
            continue
    return out


def gun_rows_fit(rows) -> tuple[bool, str]:
    """Validate a pattern before it is embedded in a button entry."""
    return gun_fits(gun_rows_to_wired(rows))


def gun_binding_problem(rows) -> str:
    """Return why a recoil pattern cannot be bound, or '' when it can.

    A size-valid pattern whose offsets are all zero is accepted by the
    encoder but does nothing on the mouse; reject it at bind time so the user
    gets an explicit reason instead of a button that silently pauses.
    """
    ok, message = gun_rows_fit(rows)
    if not ok:
        return message
    wired = gun_rows_to_wired(rows)
    if all(row.x == 0 and row.y == 0 for row in wired):
        return "the pattern has no movement (every X/Y offset is zero)"
    return ""


# ---------------------------------------------------------------------------
# Button slots <-> bindings
# ---------------------------------------------------------------------------

def binding_from_entry(entry, slot: int, profile_id: str = "",
                       macro_names: dict[int, str] | None = None):
    action = int(entry.action)
    if action == 0x16 and int(entry.count):
        name = (entry.name or "").strip() or (macro_names or {}).get(int(entry.macro_index))
        if not name:
            name = f"Macro {slot + 1}"
        mid = f"dev:{profile_id}:{slot}" if profile_id else f"dev:{slot}"
        loop = int(entry.loop)
        return {
            "macro": mid,
            "name": name,
            "events": wired_events_to_ref(entry.event_slice()),
            "playmode": 2 if loop else 1,
            "repeat": loop,
        }
    if action == 0x79 and int(entry.count):
        name = (entry.name or "").strip() or f"Gun {slot + 1}"
        gid = f"dev:{profile_id}:{slot}" if profile_id else f"dev:{slot}"
        return {
            "gun": gid,
            "name": name,
            "rows": [[int(row.x), int(row.y), int(row.delay)]
                     for row in entry.bullet_slice()],
            "repeat": max(1, min(3, int(entry.loop) or 1)),
        }
    if action == 0x15:
        return (0x15, int(entry.shortcut_mods), int(entry.shortcut_key))
    if action == 0x0A:
        return (0x0A, int(entry.fire_interval), int(entry.fire_count))
    return (action & 0xFF, 0, 0)


def binding_to_entry(entry, binding, macro_events: Callable[[str], list | None] | None = None,
                     gun_rows: Callable[[str], list | None] | None = None):
    """Write one studio binding into a wired ButtonEntry."""
    entry.set_events([])
    entry.set_bullets([])
    entry.count = 0
    entry.loop = 0
    entry.macro_index = 0
    if isinstance(binding, dict):
        if "gun" in binding:
            rows = binding.get("rows")
            if rows is None and gun_rows is not None:
                rows = gun_rows(binding.get("gun"))
            wired = gun_rows_to_wired(rows)
            problem = gun_binding_problem(rows)
            if problem:
                # A pattern the firmware table cannot hold must not break the
                # whole profile write; disable just this button and say why.
                _bind_log.warning(
                    "slot %d gun binding disabled: %s",
                    int(getattr(entry, "index", -1)) + 1, problem)
                entry.action = 0x00
                return
            entry.action = 0x79
            entry.set_bullets(wired)
            entry.count = len(wired)
            entry.loop = max(1, min(3, int(binding.get("repeat", 1) or 1)))
            entry.selected_index = 0
            name = str(binding.get("name") or "").strip()
            if name:
                entry.name = name
            return
        if "macro" in binding:
            events = binding.get("events")
            if events is None and macro_events is not None:
                events = macro_events(binding.get("macro"))
            wired = ref_events_to_wired(events or [])
            problem = macro_binding_problem(events or [])
            if problem:
                _bind_log.warning(
                    "slot %d macro binding disabled: %s",
                    int(getattr(entry, "index", -1)) + 1, problem)
                entry.action = 0x00
                return
            entry.action = 0x16
            entry.count = len(wired)
            pm = int(binding.get("playmode", 1) or 1)
            rep = int(binding.get("repeat", 0) or 0)
            entry.loop = (0 if pm == 1 else max(0, rep)) & 0xFFFF
            name = str(binding.get("name") or "").strip()
            if name:
                entry.name = name
            entry.set_events(wired)
            return
        # host-only launcher (legacy import): the wired device has no such action
        entry.action = 0x00
        return
    try:
        t, p1, p2 = (list(binding) + [0, 0, 0])[:3]
    except Exception:
        entry.action = 0x00
        return
    t, p1, p2 = int(t) & 0xFF, int(p1) & 0xFF, int(p2) & 0xFF
    entry.action = t
    if t == 0x15:
        entry.shortcut_mods = p1
        entry.shortcut_key = p2
    elif t == 0x0A:
        entry.fire_interval = p1
        entry.fire_count = p2


def validate_binding(binding) -> str:
    """Return an empty string when the binding is usable on wired hardware."""
    if isinstance(binding, dict):
        if "runapp" in binding:
            return "Run App is a host-only action and is not available on the wired SM809"
        if "gun" in binding:
            rows = binding.get("rows")
            if rows is None:
                return "the gun pattern data is missing"
            return gun_binding_problem(rows)
        if "macro" in binding:
            events = binding.get("events")
            if events is None:
                return "the macro data is missing"
            return macro_binding_problem(events)
        return "unsupported binding"
    try:
        return ""
    except Exception:
        return "invalid action"


def table_budget_problem(bindings) -> str:
    """One user-facing sentence when the config binds too many tables.

    Mirrors what :func:`binding_to_entry` will actually enable: a macro or gun
    whose data fails validation is disabled there and therefore does not
    occupy a table, so it must not be counted here either.
    """
    macros = guns = 0
    for binding in bindings or []:
        if isinstance(binding, dict):
            if "macro" in binding:
                if not macro_binding_problem(binding.get("events") or []):
                    macros += 1
            elif "gun" in binding:
                rows = binding.get("rows")
                if rows is not None and not gun_binding_problem(rows):
                    guns += 1
            continue
        try:
            action = int(list(binding)[0])
        except Exception:
            continue
        if action == 0x16:
            macros += 1
        elif action in (0x39, 0x79):
            guns += 1
    return " ".join(table_budget_messages(macros, guns))


# ---------------------------------------------------------------------------
# Whole profile <-> config
# ---------------------------------------------------------------------------

def default_pointer(profile: Profile) -> dict:
    return {
        "speed": int(profile.speed) or 6,
        "scroll": int(profile.scroll) or 3,
        "double": int(profile.double),
        "enhance": bool(profile.enhance),
        "onepage": bool(profile.onepage),
        "wheel_reverse": wheel_reversed(profile),
    }


def profile_to_config(profile: Profile, profile_id: str = "",
                      macro_names: dict[int, str] | None = None,
                      sensor: int = 0x0CEF) -> dict:
    count = _clamp(profile.stage_count, 1, 8)
    values = [dpi_to_display(sensor, v) for v in profile.dpi_values[:count]]
    colors = [list(colorref_to_rgb(c)) for c in profile.stage_colors[:count]]
    return {
        "buttons": [binding_from_entry(profile.button(i), i, profile_id, macro_names)
                    for i in range(BUTTON_COUNT)],
        "dpi": {
            "values": values,
            "colors": colors,
            "enabled_count": count,
            "selected": _clamp(profile.stage, 0, count - 1),
        },
        "polling_hz": rate_hz(profile.rate),
        "lod_mm": int(profile.lod),
        "key_response": int(profile.key_response),
        "mode": int(profile.mode),
        # Clamp on the way out too: a record written by an older studio build
        # can hold e.g. frequency=126, and the UI must never display or echo
        # that value back to the device.
        "lighting": {
            "mode": clamp_light_mode(profile.light_mode),
            "color": list(profile.fixed_rgb),
            # The eight Loop Color swatches (+0x110).  Kept separate from the
            # DPI stage palette (+0xD0): the vendor ships a different orange
            # in each one.
            "colors": [list(colorref_to_rgb(c)) for c in profile.cycle_colors],
            "brightness": clamp_light_value("brightness", profile.brightness),
            "length": clamp_light_value("length", profile.length),
            "frequency": clamp_light_value("frequency", profile.frequency),
            "direction": clamp_light_value("direction", profile.direction),
        },
        "pointer": default_pointer(profile),
    }


def config_to_profile(profile: Profile, config: dict,
                      macro_events: Callable[[str], list | None] | None = None,
                      gun_rows: Callable[[str], list | None] | None = None,
                      sensor: int = 0x0CEF) -> Profile:
    """Mutate ``profile`` from a studio config dict and return it."""
    dpi = config.get("dpi", {}) or {}
    values = [dpi_from_display(sensor, v) for v in dpi.get("values", [])][:8]
    if not values:
        values = list(profile.dpi_values)
    count = _clamp(dpi.get("enabled_count", len(values)) or len(values), 1, 8)
    values = (values + [values[-1] if values else 800] * 8)[:8]
    profile.dpi_values = values
    profile.stage_count = count
    profile.stage = _clamp(dpi.get("selected", 0), 0, count - 1)

    colors = dpi.get("colors") or []
    stage_colors = list(profile.stage_colors)
    for i, rgb in enumerate(colors[:8]):
        try:
            stage_colors[i] = rgb_to_colorref(tuple(rgb))
        except Exception:
            pass
    profile.stage_colors = stage_colors

    profile.rate = rate_index(config.get("polling_hz", rate_hz(profile.rate)))
    if config.get("lod_mm") is not None:
        profile.lod = _clamp(int(config["lod_mm"]), 0, 8)
    if config.get("key_response") is not None:
        profile.key_response = _clamp(int(config["key_response"]), 1, 255)
    if config.get("mode") is not None:
        profile.mode = 1 if int(config["mode"]) else 0

    light = config.get("lighting", {}) or {}
    if light:
        profile.light_mode = clamp_light_mode(light.get("mode", profile.light_mode))
        rgb = light.get("color")
        if rgb:
            profile.fixed_rgb = tuple(rgb)
        cycle = light.get("colors")
        if cycle:
            colors = list(profile.cycle_colors)
            for i, entry in enumerate(list(cycle)[:8]):
                try:
                    colors[i] = rgb_to_colorref(tuple(entry))
                except Exception:
                    pass
            profile.cycle_colors = colors
        for key in LIGHT_VALUE_RANGES:
            if light.get(key) is not None:
                setattr(profile, key, clamp_light_value(key, light[key]))
    # Repair a hostile/inherited record even when the config carries no
    # lighting block: +0xFC is a 0/1 table index, not a free byte.
    profile.sanitize_lighting()

    ptr = config.get("pointer", {}) or {}
    if ptr:
        profile.speed = _clamp(ptr.get("speed", profile.speed), 1, 11)
        profile.scroll = _clamp(ptr.get("scroll", profile.scroll), 1, 32767)
        profile.double = _clamp(ptr.get("double", profile.double), 0, 10)
        profile.enhance = 1 if ptr.get("enhance") else 0
        profile.onepage = 1 if ptr.get("onepage") else 0

    bindings = config.get("buttons") or []
    for slot in range(BUTTON_COUNT):
        binding = bindings[slot] if slot < len(bindings) else (0x00, 0, 0)
        binding_to_entry(profile.button(slot), binding, macro_events, gun_rows)

    reverse = bool((config.get("pointer") or {}).get("wheel_reverse", False))
    set_wheel_reversed(profile, reverse)
    return profile


def describe_binding(binding) -> str:
    if isinstance(binding, dict):
        if "runapp" in binding:
            import os
            return f"Run App: {os.path.basename(binding.get('runapp') or '')}"
        if "gun" in binding:
            name = binding.get("name") or "Gun"
            rep = max(1, min(3, int(binding.get("repeat", 1) or 1)))
            return f"Gun: {name} (x{rep})"
        name = binding.get("name") or "Macro"
        pm = int(binding.get("playmode", 1))
        rep = int(binding.get("repeat", 0))
        mode = f"x{rep}" if pm == 2 else "hold"
        return f"Macro: {name} ({mode})"
    try:
        t, p1, p2 = (list(binding) + [0, 0, 0])[:3]
    except Exception:
        return "(unassigned)"
    t, p1, p2 = int(t), int(p1), int(p2)
    if t == 0x15:
        return "Shortcut: " + shortcut_name(p2, p1)
    if t == 0x0A:
        return f"Fire click ({p1} ms x{p2 or '∞'})"
    info = ACTION_INFO_MAP.get(t)
    return info.label if info else f"Action 0x{t:02X}"


def dpi_display(sensor: int, value: int) -> int:
    return sensor_display_dpi(sensor, value)


def light_label(mode: int) -> str:
    return LIGHT_MODE_LABELS.get(int(mode), f"Mode {int(mode)}")
