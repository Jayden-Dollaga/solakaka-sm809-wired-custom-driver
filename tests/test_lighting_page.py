"""Parity tests for the vendor Light page.

The reference is ``res/lightpage.xml`` plus the visibility handler
FUN_0040eaf0 in ``SM809 mouse Software.exe``.  These tests pin the effect
order, which controls each mode shows, the factory defaults in Default.pbin
and the Fix/Loop colour plumbing through the config bridge.
"""

import struct
import time

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from sm809pro import defaults as D
from sm809pro import protocol as P
from wired.bridge import config_to_profile, profile_to_config
from wired.model import Profile, rgb_to_colorref
from wired.paths import SEED_DIR
from wired.protocol import LIGHT_UI_CONTROLS, palette_block


# ---------------------------------------------------------------------------
# Vendor tables
# ---------------------------------------------------------------------------
def test_ui_controls_match_fun_0040eaf0():
    """Modes and sections shown by the official Light page."""
    assert LIGHT_UI_CONTROLS == {
        0: (),
        1: ("brightness", "colour"),          # Standard: Intensity + Color
        2: ("length", "colour"),              # Breathing: Pulsation + Color
        3: ("brightness", "length"),          # Neon: Intensity + Pulsation
        4: ("brightness", "length"),          # Wave
        5: ("brightness", "colour"),          # Key reaction
        6: ("direction", "colour"),           # Trailing: Length + Color
        7: ("direction", "colour"),           # Drag back and forth
        8: ("brightness", "colour"),          # Slide
        9: ("brightness", "length", "colour"),  # YO-YO
        10: ("brightness", "length"),         # Marbles
        11: ("brightness",),                  # Flying star
    }
    assert P.LIGHTING_MODES[4] == "Wave"
    assert P.LIGHTING_MODES[7] == "Drag back and forth"


def test_defaults_match_vendor_default_pbin():
    """The studio defaults are the factory record shipped by the driver."""
    raw = (SEED_DIR / "Data" / "Default.pbin").read_bytes()
    light = [struct.unpack_from("<I", raw, off)[0]
             for off in (0x0F0, 0x0F4, 0x0F8, 0x0FC, 0x100)]
    assert light == [D.LIGHTING_MODE, D.LIGHTING_BRIGHTNESS, D.LIGHTING_LENGTH,
                     D.LIGHTING_FREQUENCY, D.LIGHTING_DIRECTION]
    assert light == [4, 255, 3, 1, 2]      # Wave, full, Pulsation 3, Loop, Length 2
    assert tuple(raw[0x104:0x107]) == D.LIGHTING_COLOR
    cycle = [tuple(raw[0x110 + i * 4:0x110 + i * 4 + 3]) for i in range(8)]
    assert cycle == [tuple(c) for c in D.LIGHTING_CYCLE_COLORS]
    assert cycle[6] == (255, 128, 0)       # loop orange, not the DPI 255,83,0

    cfg = D.config()["lighting"]
    assert cfg["mode"] == 4
    assert cfg["frequency"] == 1           # Loop Color selected
    assert cfg["colors"] == [list(c) for c in D.LIGHTING_CYCLE_COLORS]


# ---------------------------------------------------------------------------
# Config bridge: the eight loop swatches
# ---------------------------------------------------------------------------
def test_loop_colours_round_trip_through_the_bridge():
    prof = Profile()
    prof.cycle_colors = [rgb_to_colorref(c) for c in D.LIGHTING_CYCLE_COLORS]
    cfg = profile_to_config(prof)
    assert cfg["lighting"]["colors"] == [list(c) for c in D.LIGHTING_CYCLE_COLORS]

    replaced = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12],
                [13, 14, 15], [16, 17, 18], [19, 20, 21], [22, 23, 24]]
    cfg["lighting"]["colors"] = replaced
    config_to_profile(prof, cfg)
    assert prof.cycle_colors == [rgb_to_colorref(tuple(c)) for c in replaced]
    assert profile_to_config(prof)["lighting"]["colors"] == replaced
    # And the packed palette block carries those colours to the device.
    assert palette_block(prof.cycle_colors)[:3] == bytes([1, 2, 3])


def test_hostile_loop_colours_cannot_escape_the_profile():
    prof = Profile()
    prof.cycle_colors = [rgb_to_colorref(c) for c in D.LIGHTING_CYCLE_COLORS]
    cfg = {"lighting": {"colors": ["nope", [300, -5, 999], None]}}
    config_to_profile(prof, cfg)
    # Invalid entries are ignored; valid bytes are clamped by rgb_to_colorref.
    assert prof.cycle_colors[0] == rgb_to_colorref(D.LIGHTING_CYCLE_COLORS[0])
    assert prof.cycle_colors[1] == rgb_to_colorref((255, 0, 255))
    assert prof.cycle_colors[2] == rgb_to_colorref(D.LIGHTING_CYCLE_COLORS[2])
    assert len(prof.cycle_colors) == 8


# ---------------------------------------------------------------------------
# Panel
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def make_panel():
    from app.panels.lighting_panel import LightingPanel
    return LightingPanel()


def test_panel_starts_on_the_vendor_defaults(qapp):
    panel = make_panel()
    assert panel.current_mode() == 4
    assert panel.mode_combo.currentData() == 4
    assert panel.mode_combo.count() == 12
    assert [panel.mode_combo.itemText(i) for i in range(12)] == [
        P.LIGHTING_MODES[m] for m in range(12)]
    assert panel.brightness.value() == 255
    assert panel.length.value() == 3        # Pulsation
    assert panel.direction.value() == 2     # Length
    assert panel.color_mode() == 1          # Loop Color
    assert panel.loop_radio.isChecked() and not panel.fix_radio.isChecked()
    assert panel._colors == [tuple(c) for c in D.LIGHTING_CYCLE_COLORS]
    assert len(panel.loop_swatches) == 8

    # Wave shows Intensity + Pulsation.  The vendor hides Color Setting for
    # Wave (FUN_0040eaf0), even though the stored Loop palette is intact.
    assert panel._param_boxes["brightness"].isVisibleTo(panel)
    assert panel._param_boxes["length"].isVisibleTo(panel)
    assert not panel._param_boxes["direction"].isVisibleTo(panel)
    assert not panel.color_section.isVisibleTo(panel)
    # Standard is one of the modes that does show it.
    panel.set_state(1, None, {})
    assert panel.color_section.isVisibleTo(panel)


def test_effect_dropdown_switches_mode_and_visibility(qapp):
    panel = make_panel()
    emitted = []
    panel.apply_requested.connect(
        lambda mode, colour, params: emitted.append(mode))
    panel.set_state(1, None, {})
    panel.mode_combo.setCurrentIndex(panel.mode_combo.findData(9))
    deadline = time.time() + 2.0
    while not emitted and time.time() < deadline:
        qapp.processEvents()
    assert panel.current_mode() == 9
    assert panel._param_boxes["brightness"].isVisibleTo(panel)
    assert panel._param_boxes["length"].isVisibleTo(panel)
    assert panel.color_section.isVisibleTo(panel)
    assert emitted[-1] == 9


def test_panel_visibility_follows_each_effect(qapp):
    panel = make_panel()
    for mode, controls in LIGHT_UI_CONTROLS.items():
        panel.set_state(mode, None, {})
        assert panel.current_mode() == mode
        for key, box in panel._param_boxes.items():
            assert box.isVisibleTo(panel) == (key in controls), (mode, key)
        assert panel.color_section.isVisibleTo(panel) == ("colour" in controls), mode


def test_loop_radio_and_swatches_are_applied(qapp):
    panel = make_panel()
    emitted = []
    panel.apply_requested.connect(
        lambda mode, colour, params: emitted.append((mode, colour, dict(params))))
    panel.set_state(9, (10, 20, 30),
                    {"brightness": 120, "length": 4, "frequency": 0,
                     "direction": 1, "colors": [list(c) for c in D.LIGHTING_CYCLE_COLORS]})
    panel.loop_radio.click()                # switch to Loop Color
    deadline = time.time() + 2.0
    while not emitted and time.time() < deadline:
        qapp.processEvents()
    assert emitted, "the debounced apply never fired"
    mode, colour, params = emitted[-1]
    assert mode == 9
    assert colour == (10, 20, 30)
    assert params["frequency"] == 1
    assert params["colors"] == [list(c) for c in D.LIGHTING_CYCLE_COLORS]
