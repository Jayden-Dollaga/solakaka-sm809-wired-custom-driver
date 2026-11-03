"""
app.panels.performance_panel -- polling rate and Windows pointer behaviour.

On the wired SM809 the "performance" profile record stores the polling rate and
the Windows pointer settings that the official driver applies through
``SystemParametersInfoW``: pointer speed, wheel lines, double-click time,
enhance-pointer and page-scroll mode, plus the 1-100 ms key-response value.

Wheel direction is a *device* property on this mouse, not a profile value: the
encoder reports the opposite direction from the Windows default, and there is
no firmware-direction command.  The SCROLL DIRECTION card therefore flips the
per-device ``FlipFlopWheel`` flag for the SM809 only (with administrator
permission) and returns Windows' global scrolling direction to its default.
See :mod:`wired.wheel_direction`.

The slider ranges match the official Performance page: pointer speed 1-11,
scroll speed 1-11, double-click speed 0-10 and key response 1-100 ms. DPI
stages live on the DPI tab in this studio.

Lift-off distance is not configurable on this unit: ``Data.ini`` has
``Distance=0``, so the 0x04/0x07 frames are skipped exactly as the original
driver does.  There is no LOD control on this page.
"""

from __future__ import annotations

import logging

from PySide6.QtCore import Qt, Signal, QTimer, QThread
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QCheckBox, QFrame,
    QScrollArea, QSizePolicy, QMessageBox,
)

from ..widgets.controls import Card, Segmented
from sm809pro import defaults as _D
from wired import wheel_direction

_log = logging.getLogger("sm809.performance")

SUPPORTED_POLLING = list(_D.POLLING_SUPPORTED)


class _WheelFixWorker(QThread):
    """Run the elevated helper off the UI thread (UAC can wait indefinitely)."""

    result = Signal(bool, str)

    def __init__(self, invert, parent=None):
        super().__init__(parent)
        self._invert = bool(invert)

    def run(self):
        try:
            result = wheel_direction.apply_elevated(self._invert)
            self.result.emit(result.ok, result.message)
        except Exception as exc:  # pragma: no cover - defensive
            self.result.emit(False, f"{type(exc).__name__}: {exc}")


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
            "wheel_reverse": _D.WHEEL_REVERSED,
        }
        self._key_response = int(_D.KEY_RESPONSE)
        self._wheel_worker = None
        self._wheel_state = wheel_direction.WheelState()
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
        sub = QLabel("Polling rate and Windows pointer behaviour, matching the "
                     "official Performance page. DPI stages are configured on the "
                     "DPI tab. Changes apply to the mouse automatically.")
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

        self.enhance = QCheckBox("Enhance pointer precision")
        self.enhance.setChecked(bool(self._pointer["enhance"]))
        self.enhance.toggled.connect(self._on_pointer_slider)
        ptr_card.add(self.enhance)

        self.scroll_lines, scroll_row, self.scroll_value = self._slider_row(
            ptr_card, "Mouse scroll speed", 1, 11, self._pointer["scroll"])
        self.scroll_lines.valueChanged.connect(self._on_pointer_slider)

        self.onepage = QCheckBox("Scroll one page at a time")
        self.onepage.setChecked(bool(self._pointer["onepage"]))
        self.onepage.toggled.connect(self._on_pointer_slider)
        ptr_card.add(self.onepage)

        self.double, double_row, self.double_value = self._slider_row(
            ptr_card, "Double-click speed", 0, 10, self._pointer["double"])
        self.double.valueChanged.connect(self._on_pointer_slider)
        self._sync_double_tooltip()

        self.key_response, key_row, self.key_response_value = self._slider_row(
            ptr_card, "Key response", 1, 100, self._key_response,
            f"{self._key_response} ms")
        self.key_response.valueChanged.connect(self._on_key_response)

        hint = QLabel("Key response is stored in the profile for every unit; "
                      "this unit's Data.ini has Distance=0, so the official "
                      "driver also skips the 0x04 frame that carries it.")
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        ptr_card.add(hint)
        col.addWidget(ptr_card)

        # The SM809 encoder runs opposite to the Windows convention.  Windows
        # has a per-device FlipFlopWheel switch, so fix this mouse alone rather
        # than asking the user to invert scrolling for every mouse.
        wheel_card = Card(
            "SCROLL DIRECTION",
            "This mouse's wheel reports the opposite direction from the "
            "Windows default. Leave Windows at “Down motion scrolls down”; "
            "this flips the SM809 only.")
        self.win_fix = QCheckBox(
            "Invert scrolling for this mouse (per-device Windows setting)")
        self.win_fix.setToolTip(
            "Sets FlipFlopWheel for the SM809 HID mouse collection and returns "
            "Windows' global scrolling direction to its default. Requires "
            "administrator permission once; the mouse reconnects.")
        self.win_fix.toggled.connect(self._on_win_fix)
        wheel_card.add(self.win_fix)
        self.win_fix_status = QLabel("Checking Windows settings…")
        self.win_fix_status.setProperty("cardHint", "true")
        self.win_fix_status.setWordWrap(True)
        wheel_card.add(self.win_fix_status)
        self.win_fix_hint = QLabel(
            "Other mice are not affected. If you previously set Windows to "
            "“Down motion scrolls up” as a workaround, this returns it to the "
            "default. The mouse disconnects for about a second while Windows "
            "reloads it. If scrolling is still unchanged afterwards, unplug "
            "and reconnect the mouse, or sign out of Windows once — Windows "
            "reads this per-device value when the mouse starts. If you use a "
            "profile imported from another machine, keep its firmware "
            "wheel-swap option off when this is on.")
        self.win_fix_hint.setProperty("cardHint", "true")
        self.win_fix_hint.setWordWrap(True)
        wheel_card.add(self.win_fix_hint)
        # First card: this is the fix for the mouse's inverted encoder, and it
        # should be visible without scrolling.
        col.insertWidget(0, wheel_card)

        col.addStretch(1)
        scroll.setWidget(holder)
        root.addWidget(scroll, 1)
        self.refresh_wheel_fix()

    # -- helpers --------------------------------------------------------------
    def set_manual_apply(self, manual):
        """Reflect the manual/auto apply mode in the helper text."""
        if manual:
            self._sub.setText(
                "Polling rate and Windows pointer behaviour, matching the "
                "official Performance page. DPI stages are configured on the "
                "DPI tab. Changes are staged until you press Apply in the top bar.")
        else:
            self._sub.setText(
                "Polling rate and Windows pointer behaviour, matching the "
                "official Performance page. DPI stages are configured on the "
                "DPI tab. Changes apply to the mouse automatically.")

    def _slider_row(self, card, label, lo, hi, value, value_text=None):
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
        val = QLabel(value_text if value_text is not None else str(int(value)))
        val.setProperty("monoValue", "true")
        val.setFixedWidth(88)
        val.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        row.addWidget(val)
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
            # Kept for profiles imported from a machine that used the old
            # firmware-slot swap.  There is no UI for it any more; the Windows
            # per-device fix supersedes it.
            "wheel_reverse": bool(self._pointer.get("wheel_reverse", False)),
        })
        self.speed_value.setText(str(self._pointer["speed"]))
        self.scroll_value.setText(str(self._pointer["scroll"]))
        self.double_value.setText(str(self._pointer["double"]))
        self._sync_double_tooltip()
        self._timer.start()

    def _emit_pointer(self):
        self.pointer_changed.emit(dict(self._pointer))

    def _on_key_response(self, value):
        self._key_response = max(1, min(100, int(value)))
        self.key_response_value.setText(f"{self._key_response} ms")
        if not self._suspend:
            self._key_timer.start()

    def _emit_key_response(self):
        self.key_response_changed.emit(int(self._key_response))

    # -- Windows scroll direction --------------------------------------------
    def refresh_wheel_fix(self):
        """Reflect the current per-device FlipFlopWheel state (read-only)."""
        if self._wheel_worker is not None:
            return
        state = wheel_direction.read_state()
        self._wheel_state = state
        self.win_fix.blockSignals(True)
        self.win_fix.setChecked(state.inverted)
        self.win_fix.blockSignals(False)
        self.win_fix.setEnabled(bool(state.instances))
        self.win_fix_status.setText(state.describe())
        _log.debug("wheel state: %d/%d inverted, global reverse=%s, %d instance(s)",
                   state.flipped, state.total, state.global_reverse,
                   len(state.instances))

    def _on_win_fix(self, checked):
        if self._wheel_worker is not None:
            return
        target = bool(checked)
        # Re-read first: Windows can forget the value after a reconnect, and a
        # stale view would make the box silently disagree with reality.
        self._wheel_state = wheel_direction.read_state()
        if target == self._wheel_state.inverted:
            self._revert_win_fix()
            return
        if not self._wheel_state.instances:
            _log.warning("wheel: toggle ignored, the SM809 is not connected")
            self._revert_win_fix()
            self.refresh_wheel_fix()
            return

        if target:
            title = "Fix reversed scrolling?"
            body = ("This sets the per-device wheel direction for the SM809 "
                    "and returns Windows' scrolling direction to its default "
                    "(“Down motion scrolls down”). Other mice are not affected.")
        else:
            title = "Restore the normal Windows wheel direction?"
            body = ("This clears the per-device inversion for the SM809. "
                    "Windows' scrolling direction stays at its default.")

        _log.info("wheel: user requests %s", "inversion" if target else "the default")
        answer = QMessageBox.question(
            self, title,
            body + "\n\nWindows will ask for administrator permission. The "
                   "mouse reconnects for a second while the change is applied.",
            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if answer != QMessageBox.Ok:
            _log.info("wheel: confirmation dismissed")
            self._revert_win_fix()
            return

        self.win_fix.setEnabled(False)
        self.win_fix_status.setText("Applying the per-device setting…")
        worker = _WheelFixWorker(target, self)
        worker.result.connect(self._on_win_fix_done)
        self._wheel_worker = worker
        worker.start()

    def _revert_win_fix(self):
        self.win_fix.blockSignals(True)
        self.win_fix.setChecked(self._wheel_state.inverted)
        self.win_fix.blockSignals(False)

    def _on_win_fix_done(self, ok, message):
        self._wheel_worker = None
        _log.info("wheel: apply finished ok=%s: %s", ok, message.splitlines()[0]
                  if message else "")
        self.refresh_wheel_fix()
        if ok:
            QMessageBox.information(self, "Scroll direction updated", message)
        else:
            QMessageBox.warning(self, "Scroll direction not changed", message)

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
                    "wheel_reverse": bool(pointer.get("wheel_reverse",
                                                      self._pointer["wheel_reverse"])),
                })
                p = self._pointer
                self.speed.setValue(p["speed"])
                self.speed_value.setText(str(p["speed"]))
                self.scroll_lines.setValue(p["scroll"])
                self.scroll_value.setText(str(self.scroll_lines.value()))
                self.double.setValue(p["double"])
                self.double_value.setText(str(self.double.value()))
                self._sync_double_tooltip()
                self.enhance.setChecked(p["enhance"])
                self.onepage.setChecked(p["onepage"])
            if key_response is not None:
                self._key_response = max(1, min(100, int(key_response)))
                self.key_response.setValue(self._key_response)
                self.key_response_value.setText(f"{self._key_response} ms")
        finally:
            self._suspend = False
