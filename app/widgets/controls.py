"""
app.widgets.controls -- small reusable themed controls used by the settings
panels (Lighting, Performance, DPI): a Card container, a Segmented selector
and a numeric value box that sliders keep in sync.
"""

from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QFrame, QWidget, QVBoxLayout, QHBoxLayout, QBoxLayout, QLayout, QLabel,
    QPushButton, QButtonGroup, QSizePolicy, QLineEdit,
)


class ResponsiveRow(QWidget):
    """Two clusters on one line while they fit; stacked when they do not.

    A card that is narrow (the 820 px window minimum) cannot hold both
    clusters side by side without clipping.  Laying them out unconditionally
    in a QHBoxLayout forces the minimum width of both, which produces a
    horizontal scrollbar; this widget advertises only the wider cluster as its
    minimum, so the card shrinks and the clusters stack instead.
    """

    def __init__(self, left, right, gap=16, parent=None):
        super().__init__(parent)
        self._left = left
        self._right = right
        self._gap = gap
        self._stacked = None
        left.setParent(self)
        right.setParent(self)
        lay = QBoxLayout(QBoxLayout.LeftToRight, self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(gap)
        lay.addWidget(left)
        lay.addWidget(right, 0, Qt.AlignLeft)
        self._lay = lay
        self._apply(False)

    def _apply(self, stacked):
        if stacked == self._stacked:
            return
        self._stacked = stacked
        self._lay.setDirection(QBoxLayout.TopToBottom if stacked
                               else QBoxLayout.LeftToRight)
        # Stacked clusters hug the left edge; on one line the right cluster
        # keeps its own alignment so an expanding label can use the space.
        self._lay.setAlignment(
            self._right, Qt.AlignLeft if stacked else Qt.Alignment())
        self.updateGeometry()

    def resizeEvent(self, event):
        need = (self._left.minimumSizeHint().width()
                + max(self._right.minimumSizeHint().width(),
                      self._right.minimumSize().width())
                + self._gap)
        self._apply(self.width() < need)
        super().resizeEvent(event)

    def minimumSizeHint(self):
        hint = self._lay.minimumSize()
        hint.setWidth(max(self._left.minimumSizeHint().width(),
                          self._right.minimumSizeHint().width()))
        return QSize(hint)


class NumericValueBox(QLineEdit):
    """An editable integer readout for a slider row.

    Dragging a slider to an exact number is fiddly, so the value itself is
    editable: click it, type digits and press Enter (or Tab away).  A
    QIntValidator rejects letters at the keystroke level and lets in-range
    digits through, and nothing is emitted until the edit is committed (a
    number outside the range settles on the nearest bound), so a half-typed
    number never reaches the mouse.  Focusing the box selects the current
    value so typing replaces it.

    A QSpinBox would be the natural widget, but applying a stylesheet border
    to one with hidden buttons collapses its internal editor to 1 px wide in
    Qt; a validated line edit keeps the readout framed and editable.
    """

    committed = Signal(int)          # user finished editing (Enter/Tab away)

    def __init__(self, value: int, minimum: int, maximum: int, width: int = 86):
        super().__init__(str(int(value)))
        self._value = int(value)
        self._min = int(minimum)
        self._max = int(maximum)
        self.setValidator(QIntValidator(self._min, self._max, self))
        self.setInputMethodHints(Qt.ImhDigitsOnly)
        self.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.setFixedWidth(width)
        self.editingFinished.connect(self._commit)

    def value(self) -> int:
        return self._value

    def setValue(self, value: int):
        """Show `value` without emitting `committed` (slider/profile pushes)."""
        self._value = max(self._min, min(self._max, int(value)))
        text = str(self._value)
        if self.text() != text:
            self.setText(text)

    def focusInEvent(self, e):
        super().focusInEvent(e)
        # Click/Tab into the box: replace the old value instead of inserting
        # in the middle of it.
        self.selectAll()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            # Qt suppresses editingFinished when the validator reports
            # Intermediate (for example a lone "0" for a 1-11 slider), which
            # would leave that text sitting in the box. Commit and clamp
            # ourselves so Enter always settles the value.
            self._commit()
            e.accept()
            return
        super().keyPressEvent(e)

    def focusOutEvent(self, e):
        # Tab/click away commits the same way, including intermediate text.
        self._commit()
        super().focusOutEvent(e)

    def _commit(self):
        text = self.text().strip()
        try:
            value = int(text) if text else self._value
        except ValueError:
            value = self._value
        value = max(self._min, min(self._max, value))
        changed = value != self._value
        self.setValue(value)         # also repairs empty/partial/out-of-range
        if changed:
            self.committed.emit(value)


class Card(QFrame):
    """A titled settings card (surface panel with a heading + optional hint)."""
    def __init__(self, title, hint=None):
        super().__init__()
        self.setProperty("card", "true")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 16, 20, 18)
        lay.setSpacing(12)

        head = QLabel(title)
        head.setProperty("cardTitle", "true")
        lay.addWidget(head)
        if hint:
            h = QLabel(hint)
            h.setProperty("cardHint", "true")
            h.setWordWrap(True)
            lay.addWidget(h)

        self.body = QVBoxLayout()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.setSpacing(12)
        lay.addLayout(self.body)

    def add(self, w):
        if isinstance(w, QLayout):
            self.body.addLayout(w)
        else:
            self.body.addWidget(w)
        return w


class Segmented(QWidget):
    """A horizontal segmented selector (mutually-exclusive pill buttons).

    options: list of (label, value). Emits `changed(value)` on user click.
    """
    changed = Signal(object)

    def __init__(self, options, value=None):
        super().__init__()
        self._buttons = {}           # value -> QPushButton
        self._value = None
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        for label, val in options:
            b = QPushButton(label)
            b.setProperty("segment", "true")
            b.setCheckable(True)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda _=False, v=val: self._on_click(v))
            self._group.addButton(b)
            self._buttons[val] = b
            lay.addWidget(b)
        lay.addStretch(1)
        if value is not None:
            self.set_value(value, emit=False)

    def _restyle(self):
        for val, b in self._buttons.items():
            sel = (val == self._value)
            b.setChecked(sel)
            b.setProperty("selected", "true" if sel else None)
            b.style().unpolish(b)
            b.style().polish(b)

    def _on_click(self, value):
        if value == self._value:
            self._restyle()  # keep the visual in sync (can't unselect)
            return
        self._value = value
        self._restyle()
        self.changed.emit(value)

    def value(self):
        return self._value

    def set_value(self, value, emit=False):
        if value not in self._buttons:
            return
        if value == self._value:
            # already selected: skip the unpolish/polish pass (this is called
            # after every live device push, not just on user edits)
            if emit:
                self.changed.emit(value)
            return
        self._value = value
        self._restyle()
        if emit:
            self.changed.emit(value)

    def setEnabled(self, on):  # noqa: N802 (Qt naming)
        super().setEnabled(on)
        for b in self._buttons.values():
            b.setEnabled(on)
