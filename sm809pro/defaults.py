"""Factory defaults for the wired SM809 studio.

Values mirror ``Default.pbin`` shipped with the wired driver (8 DPI stages,
125 Hz, red LED, pointer speed 6, 3 scroll lines, 400 ms double-click).
"""

from __future__ import annotations

from . import actions as A

DPI_VALUES = [1000, 1600, 2400, 3200, 4800, 6400, 12000, 22800]
DPI_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255),
    (255, 255, 0), (0, 255, 255), (255, 83, 0), (255, 255, 255),
]
DPI_ENABLED_COUNT = 8
DPI_SELECTED = 1
DPI_MIN = 100
DPI_MAX = 24000

POLLING_HZ = 125
POLLING_SUPPORTED = [125, 250, 500, 1000]

# The wired profile stores a lift-off stage, but Data.ini has Distance=0 so the
# firmware never receives the 0x04/0x07 frames. The UI shows this as read-only.
LOD_MM = 16
LOD_SUPPORTED = False

LIGHTING_MODE = 4
LIGHTING_COLOR = (255, 0, 0)
LIGHTING_BRIGHTNESS = 255
# Vendor field names: LIGHTING_LENGTH is its Pulsation slider (+0xF8),
# LIGHTING_DIRECTION is its Length slider (+0x100), and LIGHTING_FREQUENCY is
# the Fix/Loop colour radio (+0xFC, 0 = Fix, 1 = Loop).
LIGHTING_LENGTH = 3
LIGHTING_FREQUENCY = 1
LIGHTING_DIRECTION = 2
# The eight Loop Color swatches from lightpage.xml / Default.pbin.  Note the
# orange: the loop palette uses (255,128,0), unlike the DPI stage palette's
# darker (255,83,0).  Both are COLORREFs at different profile offsets.
LIGHTING_CYCLE_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (255, 0, 255), (0, 255, 255), (255, 128, 0), (255, 255, 255),
]

POINTER_SPEED = 6
POINTER_SCROLL = 3
POINTER_DOUBLE = 5
POINTER_ENHANCE = False
POINTER_ONEPAGE = False
WHEEL_REVERSED = False

# Profile +0x138, shown on the official Performance page as 1-100 ms.
KEY_RESPONSE = 4

# Kept for code that still probes the old wireless sections.
POWER_SLEEP_MIN = 20
POWER_MOVE_WAKEUP = True
POWER_MOVE_LIGHTING = True
SENSOR_ANGLE_SNAP = False
SENSOR_MOTION_SYNC = True
SENSOR_RIPPLE = False


def button_codes():
    return A.default_button_codes()


def config():
    return {
        "buttons": button_codes(),
        "dpi": {
            "values": list(DPI_VALUES),
            "colors": [list(c) for c in DPI_COLORS],
            "enabled_count": DPI_ENABLED_COUNT,
            "selected": DPI_SELECTED,
        },
        "polling_hz": POLLING_HZ,
        "lod_mm": LOD_MM,
        "key_response": KEY_RESPONSE,
        "mode": 0,
        "lighting": {
            "mode": LIGHTING_MODE,
            "color": list(LIGHTING_COLOR),
            "colors": [list(c) for c in LIGHTING_CYCLE_COLORS],
            "brightness": LIGHTING_BRIGHTNESS,
            "length": LIGHTING_LENGTH,
            "frequency": LIGHTING_FREQUENCY,
            "direction": LIGHTING_DIRECTION,
        },
        "pointer": {
            "speed": POINTER_SPEED,
            "scroll": POINTER_SCROLL,
            "double": POINTER_DOUBLE,
            "enhance": POINTER_ENHANCE,
            "onepage": POINTER_ONEPAGE,
            "wheel_reverse": WHEEL_REVERSED,
        },
    }


apply_all = config
