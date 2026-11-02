"""
app.panels.buttons_panel -- the button remapping panel for the wired SM809.

The vendor driver exposes two modes -- Office Mode (firmware slots 0-15) and
Game Mode (slots 32-47) -- each with the same 16 physical buttons. Rows are
numbered like the mouse artwork, not like the firmware slots: the manufacturer
lists them as slots 6,7,8,9,10,11,13,14 on the left and 12,15,16,1,2,3,4,5 on
the right (see ``sm809pro.actions.PHYS_ORDER``).

Changes auto-apply to the mouse on each pick; the panel emits all 64 bindings,
which the main window/controller write as one complete profile.
"""

import copy

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QSizePolicy,
)

from .. import theme
from ..widgets.action_picker import describe_action, pick_action
from ..widgets.controls import Segmented
from sm809pro import actions as A
from wired.bridge import table_budget_problem

from ..paths import resource_path
_IMG = resource_path("images", "mouse.png")

LEFT_COLUMN = [1, 2, 3, 4, 5, 6, 7, 8, 9]   # side macro pad
RIGHT_GROUPS = {
    "Thumb Pair": [10, 11],
    "Primary": [12, 13, 14],
    "Top Pair": [15, 16],
}


def _hline():
    f = QFrame()
    f.setProperty("sep", "true")
    f.setFrameShape(QFrame.NoFrame)
    return f


def _group_label(text):
    gl = QLabel(text.upper())
    gl.setProperty("groupLabel", "true")
    return gl


class ButtonRow(QFrame):
    """One physical button in the current layer (number badge + action)."""
    changed = Signal(int)          # 0-based firmware slot

    def __init__(self, phys: int, slot: int, code, get_macros=None,
                 get_guns=None):
        super().__init__()
        self.phys = phys
        self.slot = slot
        self._code = code
        self._get_macros = get_macros or (lambda: [])
        self._get_guns = get_guns or (lambda: [])
        self.setObjectName("btnRow")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 7, 10, 7)
        lay.setSpacing(10)

        badge = QLabel(f"{phys}")
        badge.setObjectName("btnBadge")
        badge.setAlignment(Qt.AlignCenter)
        badge.setFixedSize(24, 24)
        badge.setToolTip(f"Physical button {phys} · firmware slot {slot + 1}")
        lay.addWidget(badge)

        self.action_btn = QPushButton(describe_action(self._code))
        self.action_btn.setObjectName("actionField")
        self.action_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.action_btn.clicked.connect(self._open_picker)
        lay.addWidget(self.action_btn, 1)

    def set_slot(self, slot):
        self.slot = slot
        self.set_code(self._code)

    def _open_picker(self):
        result = pick_action(self._code, self.window(), phys=self.slot,
                             macros=self._get_macros(),
                             guns=self._get_guns())
        if result is not None:
            self.set_code(result)
            self.changed.emit(self.slot)

    def set_code(self, code):
        self._code = copy.deepcopy(code) if isinstance(code, dict) else tuple(code)
        self.action_btn.setText(describe_action(self._code))

    def refresh_label(self):
        self.action_btn.setText(describe_action(self._code))

    def code(self):
        return self._code


class _ReferenceImage(QLabel):
    """The mouse artwork, scaled to the column width.

    The fixed 260 px pixmap used to give the reference column a hard minimum
    that pushed the whole grid past the viewport at the window's minimum
    width.  It now follows the column down to 128 px and never exceeds 260 —
    128 px leaves the grid a few pixels of slack inside the 820 px window.
    """
    MIN_W = 128
    MAX_W = 260

    def __init__(self, path):
        super().__init__()
        self._pm = QPixmap(path)
        self._shown = 0
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(self.MIN_W)
        self.setMaximumWidth(self.MAX_W)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    def minimumSizeHint(self):
        return QSize(self.MIN_W, 0)

    def has_image(self):
        return not self._pm.isNull()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._pm.isNull():
            return
        w = max(self.MIN_W, min(self.MAX_W, self.width()))
        if w != self._shown:
            self._shown = w
            self.setPixmap(self._pm.scaledToWidth(w, Qt.SmoothTransformation))


class MouseReference(QFrame):
    """The numbered mouse image, shown for physical-button reference."""
    def __init__(self):
        super().__init__()
        self.setObjectName("mouseRef")
        self.setMaximumWidth(286)      # 260 px artwork + frame margins
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 12, 12, 12)
        lay.setSpacing(8)
        cap = QLabel("REFERENCE")
        cap.setProperty("groupLabel", "true")
        cap.setAlignment(Qt.AlignHCenter)
        lay.addWidget(cap)
        img = _ReferenceImage(_IMG)
        if img.has_image():
            lay.addWidget(img, 0)
        else:
            missing = QLabel("(mouse.png not found)")
            missing.setProperty("panelSubtitle", "true")
            lay.addWidget(missing)
        lay.addStretch(1)


class ButtonsPanel(QWidget):
    """Two-mode remap panel: 16 physical rows per mode, four firmware groups."""
    apply_requested = Signal(object)
    reset_requested = Signal()
    # The selected layer IS the mouse's work mode (0 = Office, 1 = Game). The
    # wired firmware only uses the slots of the active layer, so the two must
    # never drift apart: picking a layer also selects that mode on the mouse.
    mode_changed = Signal(int)

    _SUB_AUTO = ("Click any button to assign an action. Numbers match the "
                 "reference image; Office Mode and Game Mode match the "
                 "vendor driver. Changes apply automatically.")
    _SUB_MANUAL = ("Click any button to assign an action. Numbers match the "
                   "reference image; Office Mode and Game Mode match the "
                   "vendor driver. Changes are staged until you press Apply "
                   "in the top bar.")
    _HINT_AUTO = ("The selected mode is also the mode the mouse uses, so "
                  "assignments take effect immediately. Wheel Up/Down and "
                  "other firmware-only slots are preserved automatically and "
                  "are not shown here.")
    _HINT_MANUAL = ("The selected mode is also the mode the mouse uses once "
                    "applied. Wheel Up/Down and other firmware-only slots are "
                    "preserved automatically and are not shown here.")

    def __init__(self, codes=None, get_macros=None, get_guns=None):
        super().__init__()
        base = codes or A.default_button_codes()
        self._bindings = [copy.deepcopy(c) if isinstance(c, dict) else tuple(c)
                          for c in (list(base) + [A.BTN["unset"]] * A.SLOT_COUNT)[:A.SLOT_COUNT]]
        self._layer = 0
        self._get_macros = get_macros or (lambda: [])
        self._get_guns = get_guns or (lambda: [])

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(14)

        title = QLabel("Button Assignment")
        title.setProperty("panelTitle", "true")
        root.addWidget(title)
        sub = QLabel(self._SUB_AUTO)
        sub.setProperty("panelSubtitle", "true")
        sub.setWordWrap(True)
        root.addWidget(sub)
        self._sub = sub

        layer_row = QHBoxLayout()
        layer_row.setSpacing(10)
        cap = QLabel("MODE")
        cap.setProperty("unit", "true")
        layer_row.addWidget(cap)
        self.layers = Segmented([(A.LAYER_LABELS[i], i) for i in range(A.LAYER_COUNT)],
                                value=0)
        self.layers.changed.connect(self._on_layer)
        layer_row.addWidget(self.layers, 1)
        root.addLayout(layer_row)

        hint = QLabel(self._HINT_AUTO)
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        root.addWidget(hint)
        self._hint = hint
        # Macros and guns share the firmware's 1..11 table range; say so as
        # soon as the layer holds more tables than can be uploaded.
        self.budget = QLabel("")
        self.budget.setProperty("cardHint", "true")
        self.budget.setWordWrap(True)
        root.addWidget(self.budget)
        root.addWidget(_hline())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        holder = QWidget()
        cols = QHBoxLayout(holder)
        cols.setContentsMargins(0, 0, 0, 0)
        cols.setSpacing(20)

        self.rows = {}

        left = QVBoxLayout()
        left.setSpacing(8)
        left.addWidget(_group_label("Side Macro Pad"))
        for phys in LEFT_COLUMN:
            row = ButtonRow(phys, A.slot_for_physical(phys, 0),
                            self._bindings[A.slot_for_physical(phys, 0)],
                            get_macros=self._get_macros,
                            get_guns=self._get_guns)
            row.changed.connect(self._on_button_changed)
            self.rows[phys] = row
            left.addWidget(row)
        left.addStretch(1)
        left_w = QWidget(); left_w.setLayout(left)
        cols.addWidget(left_w, 1)

        right = QVBoxLayout()
        right.setSpacing(8)
        for group_name, phys_list in RIGHT_GROUPS.items():
            right.addWidget(_group_label(group_name))
            for phys in phys_list:
                row = ButtonRow(phys, A.slot_for_physical(phys, 0),
                                self._bindings[A.slot_for_physical(phys, 0)],
                                get_macros=self._get_macros,
                                get_guns=self._get_guns)
                row.changed.connect(self._on_button_changed)
                self.rows[phys] = row
                right.addWidget(row)
        right.addStretch(1)
        right_w = QWidget(); right_w.setLayout(right)
        cols.addWidget(right_w, 1)

        cols.addWidget(MouseReference(), 2)
        scroll.setWidget(holder)
        root.addWidget(scroll, 1)

        self._load_layer()
        self._refresh_budget()

    # -- mode -----------------------------------------------------------------
    def set_manual_apply(self, manual):
        """Reflect manual (--verbose) apply mode in the helper text."""
        manual = bool(manual)
        self._sub.setText(self._SUB_MANUAL if manual else self._SUB_AUTO)
        self._hint.setText(self._HINT_MANUAL if manual else self._HINT_AUTO)

    def _on_layer(self, layer):
        layer = int(layer)
        if layer == self._layer:
            self._load_layer()
            return
        self._layer = layer
        self._load_layer()
        # Side effect: the firmware runs only the selected layer.
        self.mode_changed.emit(layer)

    def set_mode(self, layer):
        """Reflect the device's work mode without re-applying anything."""
        layer = 0 if int(layer) == 0 else 1
        same = (layer == self._layer)
        self._layer = layer
        self.layers.set_value(layer, emit=False)
        if not same:
            # set_codes() already refreshed every row for the current layer;
            # only a real layer change needs to re-bind the rows.
            self._load_layer()

    def current_mode(self):
        return self._layer

    def _load_layer(self):
        for phys, row in self.rows.items():
            slot = A.slot_for_physical(phys, self._layer)
            row.slot = slot
            row.set_code(self._bindings[slot])

    def _on_button_changed(self, slot):
        row = next((r for r in self.rows.values() if r.slot == slot), None)
        if row is None:
            return
        self._bindings[slot] = row.code()
        self._refresh_budget()
        self._emit_apply()

    def _emit_apply(self):
        self.apply_requested.emit(self.bindings())

    # -- external -------------------------------------------------------------
    def _refresh_budget(self):
        problem = table_budget_problem(self._bindings)
        self.budget.setText(problem)
        self.budget.setStyleSheet(
            f"color: {theme.WARN};" if problem else "")

    def set_codes(self, codes):
        if len(codes) < A.SLOT_COUNT:
            codes = list(codes) + [A.BTN["unset"]] * (A.SLOT_COUNT - len(codes))
        self._bindings = [copy.deepcopy(c) if isinstance(c, dict) else tuple(c)
                          for c in codes[:A.SLOT_COUNT]]
        self._load_layer()
        self._refresh_budget()

    def bindings(self):
        """The current 64-slot binding list (tuples and/or macro dicts)."""
        return [copy.deepcopy(c) if isinstance(c, dict) else tuple(c)
                for c in self._bindings]

    def set_binding(self, slot, code):
        """Set one slot's binding (0-based firmware slot)."""
        if 0 <= slot < A.SLOT_COUNT:
            self._bindings[slot] = copy.deepcopy(code) if isinstance(code, dict) else tuple(code)
            for row in self.rows.values():
                if row.slot == slot:
                    row.set_code(self._bindings[slot])
                    break

    def refresh_labels(self):
        for row in self.rows.values():
            row.refresh_label()
