"""
app.panels.lighting_panel -- the wired SM809 Light page.

This mirrors the vendor's Light tab (``res/lightpage.xml`` and the visibility
handler ``FUN_0040eaf0``):

* twelve effects, chosen from a single Effect dropdown (vendor order 0-11);
* Parameter Setting with the vendor's three sliders --
  Intensity (profile +0xF4, 0..255, Low/High),
  Pulsation (+0xF8, 0..4, Slow/Fast) and
  Length (+0x100, 0..4, Short/Long);
* Color Setting with a Fix Color radio + swatch (fixed RGB, +0x104), a Loop
  Color radio + eight editable swatches (COLORREFs at +0x110), and the
  Fix/Loop choice itself stored in +0xFC.

The config keys are historical and kept for saved-file compatibility:
``brightness`` -> +0xF4, ``length`` -> +0xF8 (vendor Pulsation),
``direction`` -> +0x100 (vendor Length), ``frequency`` -> +0xFC (0 Fix,
1 Loop), ``color`` -> fixed RGB and ``colors`` -> the eight loop colours.
``wired.protocol.LIGHT_UI_CONTROLS`` carries the vendor's per-mode visibility;
it hides the Color Setting for Neon, Wave, Marbles and Flying star even though
the firmware still reads the stored colour byte when it builds those frames.
"""

import logging

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QSlider, QPushButton, QRadioButton, QButtonGroup, QScrollArea,
    QComboBox, QSizePolicy,
)

from .. import theme
from ..widgets.controls import Card
from ..widgets.color_picker import pick_color
from sm809pro import protocol as P
from sm809pro import defaults as _D

_log = logging.getLogger("sm809.ui")

# Config key -> vendor control name, for warnings the user can act on.
_LABELS = {
    "brightness": "Intensity",
    "length": "Pulsation",
    "frequency": "Colour mode",
    "direction": "Length",
}

# lightpage.xml order: 0-11, shown in the Effect dropdown in that order.
_EFFECT_ORDER = tuple(range(12))

# key, caption, left endpoint, right endpoint (vendor's labels).
_PARAM_ROWS = (
    ("brightness", "Intensity", "Low", "High"),
    ("length", "Pulsation", "Slow", "Fast"),
    ("direction", "Length", "Short", "Long"),
)


def _hline():
    f = QFrame()
    f.setProperty("sep", "true")
    f.setFrameShape(QFrame.NoFrame)
    return f


def _section(text):
    label = QLabel(text)
    label.setProperty("sectionTitle", "true")
    return label


def _clamp_param(key, value):
    lo, hi = P.LIGHT_VALUE_RANGES[key]
    return max(lo, min(hi, int(value)))


def _clamp_mode(value):
    lo, hi = P.LIGHT_MODE_RANGE
    return max(lo, min(hi, int(value)))


def _normalize_colors(colors):
    """Return exactly eight RGB triples, falling back to the vendor palette."""
    out = [tuple(c) for c in _D.LIGHTING_CYCLE_COLORS]
    if not colors:
        return out
    for i, entry in enumerate(list(colors)[:8]):
        try:
            rgb = tuple(max(0, min(255, int(v))) for v in list(entry)[:3])
        except (TypeError, ValueError):
            continue
        if len(rgb) == 3:
            out[i] = rgb
    return out


class LightingPanel(QWidget):
    """Vendor-style Light page (effect, parameters, Fix/Loop colour)."""
    apply_requested = Signal(int, tuple, dict)    # mode, fixed rgb, params

    # Dragging a slider changes the value dozens of times per second. The wired
    # firmware has no partial update: every emit rewrites the whole profile over
    # HID (~600 ms of traffic), which makes the pointer stutter. Coalesce edits
    # so only the value the user settles on is written -- same policy as the DPI
    # panel.
    APPLY_DEBOUNCE_MS = 250

    def __init__(self, mode=None, color=None, params=None):
        super().__init__()
        self._suspend = False
        self._mode = _clamp_mode(_D.LIGHTING_MODE if mode is None else mode)
        self._color = tuple(color) if color else tuple(_D.LIGHTING_COLOR)
        p = dict(params or {})

        def _default(key, fallback):
            value = p.get(key)
            return int(fallback if value is None else value)

        defaults = {
            "brightness": _D.LIGHTING_BRIGHTNESS,
            "length": _D.LIGHTING_LENGTH,
            "frequency": _D.LIGHTING_FREQUENCY,
            "direction": _D.LIGHTING_DIRECTION,
        }
        self._params = {
            key: _clamp_param(key, _default(key, fallback))
            for key, fallback in defaults.items()
        }
        self._colors = _normalize_colors(p.get("colors"))

        self._apply_timer = QTimer(self)
        self._apply_timer.setSingleShot(True)
        self._apply_timer.setInterval(self.APPLY_DEBOUNCE_MS)
        self._apply_timer.timeout.connect(self._emit)

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(14)

        title = QLabel("Lighting")
        title.setProperty("panelTitle", "true")
        root.addWidget(title)
        sub = QLabel("Side-button lighting. Effects, parameters and colours "
                     "follow the official SM809 Light page.")
        sub.setProperty("panelSubtitle", "true")
        sub.setWordWrap(True)
        root.addWidget(sub)
        root.addWidget(_hline())

        card = Card("LIGHT SETTING")

        # -- effect selector (twelve vendor modes in one dropdown) ------------
        effect_col = QVBoxLayout()
        effect_col.setSpacing(6)
        effect_caption = QLabel("Effect")
        effect_caption.setProperty("cardHint", "true")
        effect_col.addWidget(effect_caption)
        self.mode_combo = QComboBox()
        for mode in _EFFECT_ORDER:
            self.mode_combo.addItem(P.LIGHTING_MODES[mode], mode)
        self.mode_combo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)
        effect_col.addWidget(self.mode_combo)
        card.add(effect_col)

        # -- parameter settings ----------------------------------------------
        card.add(_section("PARAMETER SETTING"))
        self._param_boxes = {}
        for key, caption, low, high in _PARAM_ROWS:
            box = QWidget()
            lay = QVBoxLayout(box)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(3)
            cap = QLabel(caption)
            cap.setProperty("paramLabel", "true")
            lay.addWidget(cap)
            s = QSlider(Qt.Horizontal)
            s.setRange(*P.LIGHT_VALUE_RANGES[key])
            s.setSingleStep(1)
            s.setValue(self._params[key])
            s.valueChanged.connect(lambda v, k=key: self._on_param(k, v))
            lay.addWidget(s)
            ends = QHBoxLayout()
            ends.setContentsMargins(0, 0, 0, 0)
            left = QLabel(low)
            left.setProperty("endpoint", "true")
            right = QLabel(high)
            right.setProperty("endpoint", "true")
            ends.addWidget(left)
            ends.addStretch(1)
            ends.addWidget(right)
            lay.addLayout(ends)
            card.add(box)
            self._param_boxes[key] = box
            # ``brightness`` / ``length`` / ``direction`` remain public: the
            # GUI tests and any external automation drive these sliders.
            setattr(self, key, s)

        # -- Color Setting (Fix Color + Loop Color) ---------------------------
        self.color_section = QWidget()
        cv = QVBoxLayout(self.color_section)
        cv.setContentsMargins(0, 0, 0, 0)
        cv.setSpacing(8)
        cv.addWidget(_section("COLOR SETTING"))

        # The vendor stacks the two radio groups vertically:
        #   Fix Color:  [swatch]
        #   Loop Color: [8 swatches]
        self.color_group = QButtonGroup(self)
        self.fix_radio = QRadioButton("Fix Color:")
        self.loop_radio = QRadioButton("Loop Color:")
        for radio, value in ((self.fix_radio, 0), (self.loop_radio, 1)):
            radio.setCursor(Qt.PointingHandCursor)
            radio.clicked.connect(
                lambda _checked=False, v=value: self._on_color_mode(v))
            self.color_group.addButton(radio, value)

        fix_label_row = QHBoxLayout()
        fix_label_row.addWidget(self.fix_radio)
        fix_label_row.addStretch(1)
        cv.addLayout(fix_label_row)

        fix_row = QHBoxLayout()
        fix_row.setContentsMargins(28, 0, 0, 0)
        self.fix_swatch = self._swatch(self._color, -1)
        fix_row.addWidget(self.fix_swatch)
        fix_row.addStretch(1)
        cv.addLayout(fix_row)

        loop_label_row = QHBoxLayout()
        loop_label_row.addWidget(self.loop_radio)
        loop_label_row.addStretch(1)
        cv.addLayout(loop_label_row)

        loop_row = QHBoxLayout()
        loop_row.setContentsMargins(28, 0, 0, 0)
        loop_row.setSpacing(10)
        self.loop_swatches = []
        for i in range(8):
            sw = self._swatch(self._colors[i], i)
            self.loop_swatches.append(sw)
            loop_row.addWidget(sw)
        loop_row.addStretch(1)
        cv.addLayout(loop_row)
        card.add(self.color_section)

        hint = QLabel("The same limits as the official driver: Intensity 0-255, "
                      "Pulsation and Length 0-4. Changes are sent once you pause, "
                      "so dragging stays smooth.")
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        card.add(hint)

        # The vendor Light page is fixed-height; here the window can shrink to
        # the app minimum, where YO-YO (two sliders plus the colour palette)
        # would otherwise be clipped. Keep the header fixed and scroll the card,
        # like the DPI and Performance pages do with their lists.
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        holder = QWidget()
        holder.setObjectName("scrollHolder")
        holder_lay = QVBoxLayout(holder)
        holder_lay.setContentsMargins(0, 0, 0, 0)
        holder_lay.setSpacing(0)
        holder_lay.addWidget(card)
        holder_lay.addStretch(1)
        scroll.setWidget(holder)
        root.addWidget(scroll, 1)

        self._load(self._mode, self._color, self._params, emit=False)

    # -- helpers --------------------------------------------------------------
    def _slider(self, key):
        return getattr(self, key)

    def _swatch(self, rgb, slot):
        btn = QPushButton()
        btn.setFixedSize(38, 26)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setFocusPolicy(Qt.NoFocus)
        label = "Fix Colour" if slot < 0 else f"Loop Colour {slot + 1}"
        btn.setAccessibleName(label)
        btn.clicked.connect(lambda _checked=False, i=slot: self._pick_swatch(i))
        self._paint_swatch(btn, rgb, label)
        return btn

    def _paint_swatch(self, btn, rgb, label=None):
        r, g, b = rgb
        btn.setStyleSheet(
            f"QPushButton {{ background: rgb({r},{g},{b}); "
            f"border: 1px solid {theme.BORDER}; border-radius: 4px; }}"
            f"QPushButton:hover {{ border: 2px solid {theme.ACCENT}; }}"
        )
        if label is None:
            label = btn.accessibleName() or "Colour"
        btn.setToolTip(f"{label}  #{r:02X}{g:02X}{b:02X}  (click to edit)")

    def _pick_swatch(self, slot):
        if slot < 0:
            rgb = pick_color(self._color, self.window())
            if rgb is None:
                return
            self._color = tuple(rgb)
            self._paint_swatch(self.fix_swatch, self._color)
        else:
            rgb = pick_color(self._colors[slot], self.window())
            if rgb is None:
                return
            self._colors[slot] = tuple(rgb)
            self._paint_swatch(self.loop_swatches[slot], self._colors[slot])
        self._schedule_emit()

    def _sync_colour_mode(self):
        loop = self._params["frequency"] == 1
        self.loop_radio.setChecked(loop)
        self.fix_radio.setChecked(not loop)

    def _sync_visibility(self):
        needed = set(P.LIGHT_UI_CONTROLS.get(self._mode, ()))
        for key, box in self._param_boxes.items():
            box.setVisible(key in needed)
        self.color_section.setVisible("colour" in needed)

    def _load(self, mode, color, params, emit=False):
        # A profile switch must never let an edit queued for the previous
        # profile land on the new one.
        self._apply_timer.stop()
        self._suspend = True
        try:
            self._mode = _clamp_mode(mode)
            if self._mode != int(mode):
                _log.warning("lighting: stored effect %s is outside 0..11; "
                             "using %d", mode, self._mode)
            index = self.mode_combo.findData(self._mode)
            if index >= 0 and index != self.mode_combo.currentIndex():
                self.mode_combo.setCurrentIndex(index)
            if color:
                self._color = tuple(color)
                self._paint_swatch(self.fix_swatch, self._color)
            if params:
                self._colors = _normalize_colors(params.get("colors", self._colors))
                for i, sw in enumerate(self.loop_swatches):
                    self._paint_swatch(sw, self._colors[i])
            for key, value in (params or {}).items():
                if key not in self._params or value is None:
                    continue
                # A stored value that is out of range (e.g. an imported or
                # legacy profile) must land on a usable, firmware-safe position
                # instead of being sent through unchanged.
                original = value
                value = _clamp_param(key, value)
                if value != original:
                    lo, hi = P.LIGHT_VALUE_RANGES[key]
                    _log.warning(
                        "lighting: stored %s=%s for '%s' is outside %d..%d; "
                        "using %d (the profile will be repaired on apply)",
                        key, original, _LABELS.get(key, key), lo, hi, value)
                self._params[key] = value
                if key != "frequency":       # frequency = Fix/Loop radio
                    self._slider(key).setValue(value)
            self._sync_colour_mode()
            self._sync_visibility()
        finally:
            self._suspend = False
        if emit:
            self._schedule_emit()

    def _on_param(self, key, value):
        lo, hi = P.LIGHT_VALUE_RANGES[key]
        self._params[key] = max(lo, min(hi, int(value)))
        if not self._suspend:
            self._schedule_emit()

    def _on_mode_changed(self, _index):
        if self._suspend:
            return
        mode = self.mode_combo.currentData()
        if mode is None:
            return
        self._mode = _clamp_mode(mode)
        self._sync_visibility()
        self._schedule_emit()

    def _on_color_mode(self, value):
        if self._suspend:
            return
        self._params["frequency"] = 0 if int(value) == 0 else 1
        self._sync_colour_mode()
        self._schedule_emit()

    def _schedule_emit(self):
        """Queue one apply; a burst of edits turns into a single write."""
        if self._suspend:
            return
        self._apply_timer.start()

    def _emit(self):
        if self._suspend:
            return
        params = dict(self._params)
        params["colors"] = [list(c) for c in self._colors]
        self.apply_requested.emit(self._mode, tuple(self._color), params)

    # -- external -------------------------------------------------------------
    def current_mode(self):
        return self._mode

    def color_mode(self):
        """0 = Fix Color, 1 = Loop Color (profile +0xFC)."""
        return self._params["frequency"]

    def set_state(self, mode, color=None, params=None):
        """Load lighting state from outside without applying it."""
        self._load(mode, color, params or self._params, emit=False)
