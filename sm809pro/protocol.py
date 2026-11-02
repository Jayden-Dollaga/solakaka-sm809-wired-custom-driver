"""Wired SM809 protocol helpers exposed to the studio UI.

The heavy lifting lives in :mod:`wired.protocol`. This module keeps the names
the reference panels import (lighting modes/parameters, polling conversion and
DPI decoding) while every value now describes the wired firmware.
"""

from __future__ import annotations

from wired import protocol as _wp
from wired.bridge import HZ_TO_RATE, RATE_TO_HZ
from wired.protocol import (
    ACTION_GROUPS,
    ACTION_INFO,
    ACTION_INFO_MAP,
    LIGHT_MODE_LABELS,
    LIGHT_MODE_RANGE,
    LIGHT_PARAMETERS,
    LIGHT_UI_CONTROLS,
    LIGHT_VALUE_RANGES,
    sensor_display_dpi,
)

# mode id -> human label (0..11)
LIGHTING_MODES = dict(sorted(LIGHT_MODE_LABELS.items()))
# mode id -> tuple of parameter names the 0x0D frame consumes
LIGHTING_PARAMETERS = dict(LIGHT_PARAMETERS)
# mode id -> controls the vendor Light page shows (FUN_0040eaf0)
LIGHTING_UI_CONTROLS = dict(LIGHT_UI_CONTROLS)

# Legacy polling names used by the .psf importer.  The wired firmware stores a
# rate index and the studio shows Hz.
POLLING_REVERSE = dict(HZ_TO_RATE)
POLLING_FORWARD = dict(RATE_TO_HZ)


def raw_to_dpi(raw: int) -> int:
    """Decode a stored wired DPI stage value for the default sensor (3311)."""
    return sensor_display_dpi(0x0CEF, int(raw))


def dpi_to_raw(display: int) -> int:
    from wired.bridge import dpi_from_display
    return dpi_from_display(0x0CEF, int(display))


def light_mode_label(mode: int) -> str:
    return LIGHT_MODE_LABELS.get(int(mode), f"Mode {int(mode)}")


def light_parameters(mode: int) -> tuple[str, ...]:
    return LIGHT_PARAMETERS.get(int(mode), ())


def light_ui_controls(mode: int) -> tuple[str, ...]:
    return LIGHT_UI_CONTROLS.get(int(mode), ())


__all__ = [
    "LIGHTING_MODES", "LIGHTING_PARAMETERS", "LIGHTING_UI_CONTROLS",
    "POLLING_REVERSE", "POLLING_FORWARD", "raw_to_dpi", "dpi_to_raw",
    "light_mode_label", "light_parameters", "light_ui_controls",
    "sensor_display_dpi", "ACTION_GROUPS", "ACTION_INFO",
    "ACTION_INFO_MAP", "LIGHT_MODE_RANGE", "LIGHT_VALUE_RANGES",
]
