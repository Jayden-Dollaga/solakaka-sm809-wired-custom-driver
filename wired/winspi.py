"""Windows pointer settings used by the Performance page.

The original calls SystemParametersInfoW with a few malformed argument shapes
(notably SPI_SETMOUSE). This rebuild keeps the same user-visible mapping but
passes the documented values, so the sliders behave as labelled.
"""

from __future__ import annotations

import ctypes
import sys

SPI_SETMOUSE = 0x0004
SPI_SETDOUBLECLICKTIME = 0x0020
SPI_SETWHEELSCROLLLINES = 0x0069
SPI_SETMOUSESPEED = 0x0071
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02
FLAGS = SPIF_UPDATEINIFILE | SPIF_SENDCHANGE

MOUSE_SPEED_TABLE = (1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20)


def _user32():
    if sys.platform != "win32":
        return None
    return ctypes.windll.user32


def double_click_ms(index: int) -> int:
    return 900 - 70 * max(0, min(10, int(index)))


def mouse_speed_value(index: int) -> int:
    return MOUSE_SPEED_TABLE[max(1, min(11, int(index))) - 1]


def set_double_click_time(index: int, user32=None) -> int:
    user32 = user32 or _user32()
    ms = double_click_ms(index)
    if user32 is None:
        return ms
    user32.SetDoubleClickTime(ms)
    user32.SystemParametersInfoW(SPI_SETDOUBLECLICKTIME, ms, None, FLAGS)
    return ms


def set_mouse_speed(index: int, user32=None) -> int:
    user32 = user32 or _user32()
    speed = mouse_speed_value(index)
    if user32 is None:
        return speed
    user32.SystemParametersInfoW(SPI_SETMOUSESPEED, speed, None, FLAGS)
    return speed


def set_enhance_pointer(enabled: bool, user32=None) -> None:
    user32 = user32 or _user32()
    if user32 is None:
        return
    values = (ctypes.c_int * 3)(6, 10, 1) if enabled else (ctypes.c_int * 3)(0, 0, 0)
    user32.SystemParametersInfoW(SPI_SETMOUSE, 0, ctypes.byref(values), FLAGS)


def set_wheel_lines(lines: int, one_page: bool, user32=None) -> int:
    user32 = user32 or _user32()
    value = -1 if one_page else max(-1, min(32767, int(lines)))
    if user32 is None:
        return value
    user32.SystemParametersInfoW(SPI_SETWHEELSCROLLLINES, value & 0xFFFFFFFF, None, FLAGS)
    return value


class PointerSettings:
    """Applies only values that changed since the last apply."""

    def __init__(self) -> None:
        self._last: dict[str, object] = {}

    def apply(self, speed: int, scroll: int, double: int, enhance: bool, onepage: bool) -> list[str]:
        changes: list[str] = []
        if self._last.get("double") != double:
            ms = set_double_click_time(double)
            self._last["double"] = double
            changes.append(f"double-click time {ms} ms")
        if self._last.get("speed") != speed:
            value = set_mouse_speed(speed)
            self._last["speed"] = speed
            changes.append(f"pointer speed {value}/20")
        if self._last.get("enhance") != bool(enhance):
            set_enhance_pointer(bool(enhance))
            self._last["enhance"] = bool(enhance)
            changes.append(f"enhance precision {'on' if enhance else 'off'}")
        if self._last.get("wheel") != (scroll, bool(onepage)):
            set_wheel_lines(scroll, bool(onepage))
            self._last["wheel"] = (scroll, bool(onepage))
            changes.append("wheel scroll lines " + ("one page" if onepage else str(scroll)))
        return changes
