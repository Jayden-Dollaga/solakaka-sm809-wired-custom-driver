"""
app.panels.performance_panel -- polling rate and Windows pointer behaviour.

On the wired SM809 the "performance" profile record stores the polling rate and
the Windows pointer settings that the official driver applies through
``SystemParametersInfoW``: pointer speed, wheel lines, double-click time,
enhance-pointer and page-scroll mode, plus the 1-100 ms key-response value.

Scroll direction follows the normal Windows convention.  The earlier
per-device ``FlipFlopWheel`` workaround lived here while the encoder on one unit
reported the opposite direction; it was removed after that hardware fault was
fixed, and every profile now applies the standard wheel direction.

The slider ranges match the official Performance page: pointer speed 1-11,
scroll speed 1-11, double-click speed 0-10 and key response 1-100 ms. DPI
stages live at the bottom of this same page (`add_dpi_section`, fed by
``DpiPanel(embedded=True)``).

Lift-off distance is not configurable on this unit: ``Data.ini`` has
``Distance=0``, so the 0x04/0x07 frames are skipped exactly as the original
driver does.  There is no LOD control on this page.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QFrame,
    QScrollArea, QSizePolicy,
)

from ..widgets.controls import Card, NumericValueBox, Segmented
from sm809pro import defaults as _D

SUPPORTED_POLLING = list(_D.POLLING_SUPPORTED)


def _hline():
    f = QFrame()
    f.setProperty("sep", "true")
    f.setFrameShape(QFrame.NoFrame)
    return f


class PerformancePanel(QWidget):
    """Polling + pointer settings; auto-applies with a short debounce."""
    polling_changed = Signal(int)          # hz
    pointer_changed = Signal(dict)         # speed/scroll/double/enhance/onepage/reverse
    key_response_changed = Signal(int)     # milliseconds (1-100)

    APPLY_DEBOUNCE_MS = 250
    KEY_RESPONSE_DEBOUNCE_MS = 250

    def __init__(self):
        super().__init__()
        self._suspend = False
        self._pointer = {
            "speed": _D.POINTER_SPEED,
            "scroll": _D.POINTER_SCROLL,
            "double": _D.POINTER_DOUBLE,
            "enhance": _D.POINTER_ENHANCE,
            "onepage": _D.POINTER_ONEPAGE,
        }
        self._key_response = int(_D.KEY_RESPONSE)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(self.APPLY_DEBOUNCE_MS)
        self._timer.timeout.connect(self._emit_pointer)
        self._key_timer = QTimer(self)
        self._key_timer.setSingleShot(True)
        self._key_timer.setInterval(self.KEY_RESPONSE_DEBOUNCE_MS)
        self._key_timer.timeout.connect(self._emit_key_response)

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(18)

        title = QLabel("Performance")
        title.setProperty("panelTitle", "true")
        root.addWidget(title)
        sub = QLabel("Polling rate, Windows pointer behaviour and DPI stages, "
                     "matching the official Performance page. Changes apply to "
                     "the mouse automatically.")
        sub.setProperty("panelSubtitle", "true")
        sub.setWordWrap(True)
        root.addWidget(sub)
        self._sub = sub
        root.addWidget(_hline())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        holder = QWidget()
        col = QVBoxLayout(holder)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(16)
        self._col = col

        poll_card = Card("POLLING RATE", "The wired SM809 supports up to 1000 Hz.")
        self.polling = Segmented([(f"{hz}Hz", hz) for hz in SUPPORTED_POLLING],
                                 value=_D.POLLING_HZ)
        self.polling.changed.connect(self._on_polling)
        poll_card.add(self.polling)
        col.addWidget(poll_card)

        ptr_card = Card("WINDOWS POINTER",
                        "Stored in the profile and applied through the Windows "
                        "pointer API when the profile is written. Slider ranges "
                        "match the official driver.")
        self.speed, speed_row, self.speed_value = self._slider_row(
            ptr_card, "Mouse move speed", 1, 11, self._pointer["speed"])
        self.speed.valueChanged.connect(self._on_pointer_slider)
        self.speed_value.committed.connect(self.speed.setValue)

        self.enhance = QCheckBox("Enhance pointer precision")
        self.enhance.setChecked(bool(self._pointer["enhance"]))
        self.enhance.toggled.connect(self._on_pointer_slider)
        ptr_card.add(self.enhance)

        self.scroll_lines, scroll_row, self.scroll_value = self._slider_row(
            ptr_card, "Mouse scroll speed", 1, 11, self._pointer["scroll"])
        self.scroll_lines.valueChanged.connect(self._on_pointer_slider)
        self.scroll_value.committed.connect(self.scroll_lines.setValue)

        self.onepage = QCheckBox("Scroll one page at a time")
        self.onepage.setChecked(bool(self._pointer["onepage"]))
        self.onepage.toggled.connect(self._on_pointer_slider)
        ptr_card.add(self.onepage)

        self.double, double_row, self.double_value = self._slider_row(
            ptr_card, "Double-click speed", 0, 10, self._pointer["double"])
        self.double.valueChanged.connect(self._on_pointer_slider)
        self.double_value.committed.connect(self.double.setValue)
        self._sync_double_tooltip()

        self.key_response, key_row, self.key_response_value = self._slider_row(
            ptr_card, "Key response", 1, 100, self._key_response, unit="ms")
        self.key_response.valueChanged.connect(self._on_key_response)
        self.key_response_value.committed.connect(self.key_response.setValue)

        hint = QLabel("Key response is stored in the profile for every unit; "
                      "this unit's Data.ini has Distance=0, so the official "
                      "driver also skips the 0x04 frame that carries it.")
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        ptr_card.add(hint)
        col.addWidget(ptr_card)

        col.addStretch(1)
        scroll.setWidget(holder)
        root.addWidget(scroll, 1)

    # -- helpers --------------------------------------------------------------
    def add_dpi_section(self, panel):
        """Place the DPI stage editor on this page, below the pointer card.

        DPI used to be its own rail page.  Its stage rows are short enough to
        live here, and keeping one page for "how the mouse behaves" makes the
        rail shorter without hiding anything.  `panel` is an embedded
        DpiPanel (no header or scroll of its own).
        """
        card = Card("DPI STAGES",
                    "Click a stage number to make it the active DPI, or type a "
                    "value in the number box. Uncheck a stage to skip it while "
                    "cycling DPI; its indicator colour stays with the profile.")
        card.add(panel)
        # insert before the trailing stretch so the page stays top-aligned
        self._col.insertWidget(self._col.count() - 1, card)
        self._dpi_card = card
        return card

    def set_manual_apply(self, manual):
        """Reflect the manual/auto apply mode in the helper text."""
        if manual:
            self._sub.setText(
                "Polling rate, Windows pointer behaviour and DPI stages, "
                "matching the official Performance page. Changes are staged "
                "until you press Apply in the top bar.")
        else:
            self._sub.setText(
                "Polling rate, Windows pointer behaviour and DPI stages, "
                "matching the official Performance page. Changes apply to the "
                "mouse automatically.")

    def _slider_row(self, card, label, lo, hi, value, unit=""):
        row = QHBoxLayout()
        row.setSpacing(12)
        cap = QLabel(label)
        cap.setProperty("cardHint", "true")
        cap.setFixedWidth(130)
        row.addWidget(cap)
        s = QSlider(Qt.Horizontal)
        s.setRange(lo, hi)
        s.setSingleStep(1)
        s.setValue(int(value))
        s.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        if hi - lo <= 11:
            # small official pages show one tick per position
            s.setTickPosition(QSlider.TicksBelow)
            s.setTickInterval(1)
        row.addWidget(s, 1)
        # The readout is editable, like the DPI boxes: type a value and press
        # Enter instead of hunting for it with the slider.
        val = NumericValueBox(int(value), lo, hi, width=64)
        val.setObjectName("perfValue")
        val.setToolTip(
            f"Type a value ({lo}-{hi}) and press Enter.\n"
            "Letters are ignored; the slider follows.")
        row.addWidget(val)
        if unit:
            u = QLabel(unit)
            u.setProperty("unit", "true")
            u.setFixedWidth(24)
            row.addWidget(u)
        card.add(row)
        return s, row, val

    @staticmethod
    def _double_ms(index):
        return 900 - 70 * int(index)

    def _sync_double_tooltip(self):
        self.double.setToolTip(
            f"Windows double-click time: {self._double_ms(self.double.value())} ms")

    def _on_polling(self, hz):
        if not self._suspend:
            self.polling_changed.emit(int(hz))

    def _on_pointer_slider(self, *_):
        if self._suspend:
            return
        self._pointer.update({
            "speed": int(self.speed.value()),
            "scroll": int(self.scroll_lines.value()),
            "double": int(self.double.value()),
            "enhance": bool(self.enhance.isChecked()),
            "onepage": bool(self.onepage.isChecked()),
        })
        self.speed_value.setValue(self._pointer["speed"])
        self.scroll_value.setValue(self._pointer["scroll"])
        self.double_value.setValue(self._pointer["double"])
        self._sync_double_tooltip()
        self._timer.start()

    def _emit_pointer(self):
        self.pointer_changed.emit(dict(self._pointer))

    def _on_key_response(self, value):
        self._key_response = max(1, min(100, int(value)))
        self.key_response_value.setValue(self._key_response)
        if not self._suspend:
            self._key_timer.start()

    def _emit_key_response(self):
        self.key_response_changed.emit(int(self._key_response))

    # -- external -------------------------------------------------------------
    def set_state(self, polling_hz=None, pointer=None,
                  key_response=None, **legacy):
        """Load values from outside without applying them."""
        self._suspend = True
        try:
            if polling_hz is not None:
                self.polling.set_value(int(polling_hz))
            if pointer:
                self._pointer.update({
                    "speed": int(pointer.get("speed", self._pointer["speed"])),
                    "scroll": int(pointer.get("scroll", self._pointer["scroll"])),
                    "double": int(pointer.get("double", self._pointer["double"])),
                    "enhance": bool(pointer.get("enhance", self._pointer["enhance"])),
                    "onepage": bool(pointer.get("onepage", self._pointer["onepage"])),
                })
                p = self._pointer
                self.speed.setValue(p["speed"])
                self.speed_value.setValue(self.speed.value())
                self.scroll_lines.setValue(p["scroll"])
                self.scroll_value.setValue(self.scroll_lines.value())
                self.double.setValue(p["double"])
                self.double_value.setValue(self.double.value())
                self._sync_double_tooltip()
                self.enhance.setChecked(p["enhance"])
                self.onepage.setChecked(p["onepage"])
            if key_response is not None:
                self._key_response = max(1, min(100, int(key_response)))
                self.key_response.setValue(self._key_response)
                self.key_response_value.setValue(self._key_response)
        finally:
            self._suspend = False
