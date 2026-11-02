"""
app.panels.gun_panel -- the recoil-pattern (Gun) library editor.

The wired firmware calls these tables "guns": a bullet pattern of X/Y cursor
offsets and delays.  The official driver's Gun page was hidden in the shipped
build, but the action (``Set Gun``, 0x79), the button-entry layout and the
128-byte encoder all exist.  This panel exposes the same 30-row table with a
host-side named library, and the Buttons tab binds a pattern with ``Set Gun``.

We deliberately keep the editor row-based (not a live recorder): a recoil
pattern is a handful of exact offsets, and the firmware table has a hard
128-byte budget.  The size readout shows that budget before anything is bound.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton,
    QLineEdit, QSpinBox, QFrame, QScrollArea, QSizePolicy,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QInputDialog, QMenu, QToolButton,
)

from .. import theme
from ..widgets.controls import Card, ResponsiveRow
from ..gun_store import (
    DELAY_MAX, DELAY_STEP, MAX_ROWS, X_MAX, X_MIN, Y_MAX, Y_MIN,
)
from ..recoil_recorder import RecoilRecorder
from wired.protocol import gun_encoded_size, gun_fits

SAVE_DEBOUNCE_MS = 300
DOT = "\u25cf"
SQUARE = "\u25a0"
ELLIP = "\u2026"


class _NoWheelSpin(QSpinBox):
    """Ignore the mouse wheel so scrolling the table never edits a value."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, event):
        event.ignore()


class GunPanel(QWidget):
    """Named recoil-pattern library. Emits library_changed after edits settle."""
    library_changed = Signal()
    ARM_MS = 3000

    def __init__(self, store):
        super().__init__()
        self.store = store
        self._cur_id = None
        self._suspend = False

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(SAVE_DEBOUNCE_MS)
        self._save_timer.timeout.connect(self._flush)

        self.recorder = RecoilRecorder(self)
        self._record_timer = QTimer(self)
        self._record_timer.timeout.connect(self._record_sample)
        self._recording = False
        self._record_token = 0
        self._record_rows = []
        self._record_total = 0
        self._record_interval = 100
        self._record_moved = False
        self._record_gid = None

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(16)

        title = QLabel("Gun Patterns")
        title.setProperty("panelTitle", "true")
        root.addWidget(title)
        sub = QLabel("A recoil pattern is the down/right pull the mouse adds "
                     "while you fire. Build one here, bind it to a side button "
                     "in the Buttons tab, then apply. It travels inside the "
                     "profile, so it survives a .pbin export/import.")
        sub.setProperty("panelSubtitle", "true")
        sub.setWordWrap(True)
        root.addWidget(sub)
        root.addWidget(self._sep())

        body = QHBoxLayout()
        body.setSpacing(18)
        root.addLayout(body, 1)
        body.addWidget(self._build_left())
        body.addWidget(self._build_editor(), 1)

        self._refresh_list()
        self._load_editor()

    # -- helpers --------------------------------------------------------------
    @staticmethod
    def _sep():
        f = QFrame()
        f.setProperty("sep", "true")
        f.setFrameShape(QFrame.NoFrame)
        return f

    def _cur(self):
        return self.store.get(self._cur_id) if self._cur_id else None

    # -- left column ----------------------------------------------------------
    def _build_left(self):
        col = QWidget()
        col.setFixedWidth(224)
        lay = QVBoxLayout(col)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        cap = QLabel("GUN LIBRARY")
        cap.setProperty("groupLabel", "true")
        lay.addWidget(cap)

        self.gun_list = QListWidget()
        self.gun_list.currentRowChanged.connect(self._on_list_row)
        self.gun_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.gun_list.customContextMenuRequested.connect(self._list_menu)
        lay.addWidget(self.gun_list, 1)
        # F2 renames the selected pattern, like the original driver's
        # "Rename Gun Name" entry.
        QShortcut(QKeySequence("F2"), self.gun_list,
                  activated=self.rename_gun_dialog)

        row = QHBoxLayout()
        row.setSpacing(8)
        new_btn = QPushButton("+ New")
        new_btn.clicked.connect(self.new_gun)
        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self.delete_gun)
        menu_btn = QToolButton()
        menu_btn.setText(ELLIP)
        menu_btn.setToolTip("Rename or delete a pattern")
        menu_btn.setPopupMode(QToolButton.InstantPopup)
        menu = QMenu(menu_btn)
        menu.addAction("Rename…", self.rename_gun_dialog)
        menu.addSeparator()
        menu.addAction("Delete", self.delete_gun)
        menu_btn.setMenu(menu)
        row.addWidget(new_btn)
        row.addWidget(del_btn)
        row.addWidget(menu_btn)
        lay.addLayout(row)

        self.status = QLabel("")
        self.status.setProperty("cardHint", "true")
        self.status.setWordWrap(True)
        lay.addWidget(self.status)

        hint = QLabel("Saved automatically. Bind a pattern in the Buttons tab "
                      "with the Gun category, then press Apply.")
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        lay.addWidget(hint)
        return col

    # -- right editor ---------------------------------------------------------
    def _build_editor(self):
        self.editor = QWidget()
        self.editor.setObjectName("gunEditor")
        lay = QVBoxLayout(self.editor)
        lay.setContentsMargins(0, 0, 4, 0)
        lay.setSpacing(14)

        top = QHBoxLayout()
        top.setSpacing(10)
        top.addWidget(QLabel("Name"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Pattern name")
        self.name_edit.textChanged.connect(self._on_name_changed)
        self.name_edit.editingFinished.connect(self._commit_name)
        top.addWidget(self.name_edit, 1)
        lay.addLayout(top)

        how = Card(
            "HOW TO USE",
            "The Gun tab only edits the pattern. The button that runs it is "
            "assigned in the Buttons tab (Gun category).")
        steps = QLabel(
            "1.  Create a pattern here and tune X / Y / Delay (start with a "
            "few rows and small positive offsets).\n"
            "2.  Open Buttons, click the mouse button you want to use, choose "
            "Gun, select this pattern and a repeat count (1-3), then click OK.\n"
            "3.  Click Apply. The pattern is embedded in that button and "
            "uploaded with the profile.\n"
            "4.  In the game, hold (or tap) that button while firing; the "
            "mouse replays the rows.\n"
            "5.  Tune the rows until the crosshair stays on target. Flip X / "
            "Flip Y reverse a whole column while you experiment.")
        steps.setWordWrap(True)
        steps.setProperty("cardHint", "true")
        # The five steps used to push the pattern table below the fold at the
        # default window size.  Keep the short summary in the card header and
        # expand the steps on demand; nothing is removed.
        steps.hide()
        self.how_steps = steps
        self.how_toggle = QPushButton("Show the 5 steps")
        self.how_toggle.setCheckable(True)
        self.how_toggle.setToolTip("Expand the step-by-step workflow")
        self.how_toggle.toggled.connect(self._toggle_how_to)
        how.add(self.how_toggle)
        how.add(steps)
        lay.addWidget(how)

        pattern = Card(
            "RECOIL PATTERN",
            "Each row pulls the crosshair by X / Y units, then waits Delay "
            "before the next row. The firmware transmits the magnitude of both "
            "offsets, so keep them positive (0-127) for a normal right/down "
            "pull; the Sign note below warns when a row cannot be sent as "
            "typed. Record your own compensation by firing while armed.")
        # The header keeps its airy two-row shape: the count/budget pair and
        # the edit tools share a line, then the recorder gets its own.  Each
        # line is a ResponsiveRow so the narrow card stacks its two clusters
        # instead of drawing the counter over "Clear offsets" or clipping the
        # Flip buttons.
        count = QWidget()
        count_lay = QHBoxLayout(count)
        count_lay.setContentsMargins(0, 0, 0, 0)
        count_lay.setSpacing(8)
        count_lay.addWidget(QLabel("Bullets"))
        self.bullets = _NoWheelSpin()
        self.bullets.setRange(1, MAX_ROWS)
        self.bullets.setValue(MAX_ROWS)
        self.bullets.setFixedWidth(76)
        self.bullets.setAlignment(Qt.AlignCenter)
        self.bullets.valueChanged.connect(self._on_bullet_count)
        count_lay.addWidget(self.bullets)
        count_lay.addStretch(1)
        self.size_label = QLabel("0 / 128 bytes")
        self.size_label.setProperty("cardHint", "true")
        self.size_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        count_lay.addWidget(self.size_label)
        count.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        tools = QWidget()
        tools_lay = QHBoxLayout(tools)
        tools_lay.setContentsMargins(0, 0, 0, 0)
        tools_lay.setSpacing(8)
        clear_btn = QPushButton("Clear offsets")
        clear_btn.setProperty("compact", "true")
        clear_btn.setToolTip("Keep the delays but set every X/Y offset to zero")
        clear_btn.clicked.connect(self._clear_offsets)
        tools_lay.addWidget(clear_btn)
        self.flip_x_btn = QPushButton("Flip X")
        self.flip_x_btn.setProperty("compact", "true")
        self.flip_x_btn.setToolTip("Negate every X offset")
        self.flip_x_btn.clicked.connect(lambda: self._flip_axis(0))
        tools_lay.addWidget(self.flip_x_btn)
        self.flip_y_btn = QPushButton("Flip Y")
        self.flip_y_btn.setProperty("compact", "true")
        self.flip_y_btn.setToolTip("Negate every Y offset")
        self.flip_y_btn.clicked.connect(lambda: self._flip_axis(1))
        tools_lay.addWidget(self.flip_y_btn)
        tools.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        pattern.add(ResponsiveRow(count, tools))

        rec = QWidget()
        rec_lay = QHBoxLayout(rec)
        rec_lay.setContentsMargins(0, 0, 0, 0)
        rec_lay.setSpacing(8)
        self.record_btn = QPushButton(f"{DOT} Record")
        self.record_btn.setMinimumWidth(96)
        self.record_btn.setToolTip(
            "Capture raw mouse movement for the current bullet count. Raw "
            "input works while a game has the pointer locked; the studio does "
            "not need focus during the capture.")
        self.record_btn.clicked.connect(self._toggle_record)
        rec_lay.addWidget(self.record_btn)
        interval_label = QLabel("Shot interval")
        interval_label.setToolTip("Milliseconds between recorded bullets")
        rec_lay.addWidget(interval_label)
        self.record_interval = _NoWheelSpin()
        self.record_interval.setRange(10, 2000)
        self.record_interval.setSingleStep(10)
        self.record_interval.setValue(100)
        self.record_interval.setSuffix(" ms")
        self.record_interval.setFixedWidth(92)
        self.record_interval.setAlignment(Qt.AlignCenter)
        rec_lay.addWidget(self.record_interval)
        rec.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)

        # The status shares the recorder line while there is room; on a narrow
        # card it drops below instead of squeezing into a one-word column.
        self.record_status = QLabel(
            "Records one row per interval until the bullet count is reached.")
        self.record_status.setProperty("cardHint", "true")
        self.record_status.setWordWrap(True)
        # Keep enough width for the status to stay readable; below that the
        # row stacks it under the recorder instead of a one-word column.
        self.record_status.setMinimumWidth(150)
        self.record_status.setSizePolicy(QSizePolicy.Expanding,
                                         QSizePolicy.Preferred)
        pattern.add(ResponsiveRow(rec, self.record_status, gap=12))

        self.table = QTableWidget(0, 4)
        self.table.setObjectName("gunRows")
        self.table.setHorizontalHeaderLabels(["#", "X", "Y", "Delay (ms)"])
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(38)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setMinimumHeight(240)
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Fixed)
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setSectionResizeMode(2, QHeaderView.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.Stretch)
        hh.setHighlightSections(False)
        self.table.setColumnWidth(0, 44)
        pattern.add(self.table)

        self.pattern_note = QLabel("")
        self.pattern_note.setProperty("cardHint", "true")
        self.pattern_note.setWordWrap(True)
        pattern.add(self.pattern_note)
        lay.addWidget(pattern, 1)

        hint = QLabel(
            "The bound button replays this pattern on the mouse. The 128-byte "
            "table entry holds an 8-byte row per real offset and a 4-byte row "
            "per zero offset. At most 3 gun/left-macro buttons are allowed per "
            "mode, and gun tables share the firmware's eleven macro/gun table "
            "slots — a profile packed with macros can leave no room for a gun. "
            "The Buttons tab shows that budget warning. The shipped driver "
            "never uploaded gun tables, so this path is experimental — verify "
            "a small pattern on the hardware before relying on it.")
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        lay.addWidget(hint)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        # The editor is sized to fit the 820 px minimum window; if a larger
        # system font or DPI makes it wider, scroll rather than clip a card.
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.viewport().setAutoFillBackground(False)
        scroll.setWidget(self.editor)
        self.editor.setAutoFillBackground(False)
        return scroll

    # -- library list ---------------------------------------------------------
    @staticmethod
    def _item_text(g):
        return f"{g['name']}  ({len(g.get('rows') or [])})"

    def _refresh_list(self):
        self.gun_list.blockSignals(True)
        self.gun_list.clear()
        for g in self.store.all():
            self.gun_list.addItem(self._item_text(g))
        self.gun_list.blockSignals(False)

    def _refresh_list_item(self):
        i = self.store.index_of(self._cur_id)
        g = self._cur()
        it = self.gun_list.item(i) if i >= 0 else None
        if it and g:
            it.setText(self._item_text(g))

    def new_gun(self):
        if self._recording:
            self._finish_recording("pattern changed")
        name = self.store.unique_name(f"Gun {len(self.store.all()) + 1}")
        g = self.store.add(name)
        self._refresh_list()
        self.gun_list.setCurrentRow(self.store.index_of(g["id"]))
        self.library_changed.emit()

    def delete_gun(self):
        if self._recording:
            self._finish_recording("pattern deleted")
        if not self._cur_id:
            return
        idx = self.store.index_of(self._cur_id)
        self.store.delete(self._cur_id)
        self._cur_id = None
        self._refresh_list()
        n = len(self.store.all())
        if n:
            self.gun_list.setCurrentRow(min(idx, n - 1))
        else:
            self._load_editor()
        self.library_changed.emit()

    def _on_list_row(self, row):
        if self._recording:
            self._finish_recording("pattern changed")
        self._flush()
        guns = self.store.all()
        self._cur_id = guns[row]["id"] if 0 <= row < len(guns) else None
        self._load_editor()

    # -- rename ---------------------------------------------------------------
    def _list_menu(self, pos):
        item = self.gun_list.itemAt(pos)
        if item is not None:
            self.gun_list.setCurrentRow(self.gun_list.row(item))
        has_current = self._cur() is not None
        menu = QMenu(self)
        rename = menu.addAction("Rename…", self.rename_gun_dialog)
        rename.setEnabled(has_current)
        menu.addSeparator()
        delete = menu.addAction("Delete", self.delete_gun)
        delete.setEnabled(has_current)
        menu.exec(self.gun_list.viewport().mapToGlobal(pos))

    def rename_gun_dialog(self):
        g = self._cur()
        if g is None:
            return
        name, ok = QInputDialog.getText(
            self, "Rename gun pattern", "Pattern name:", text=g["name"])
        if not ok:
            return
        name = self.store.unique_name(name, exclude_id=g["id"])
        if name == g["name"]:
            return
        self._flush()
        self.store.rename(self._cur_id, name)
        self._suspend = True
        self.name_edit.setText(name)
        self._suspend = False
        self._refresh_list_item()
        self.status.setText(f"Renamed to “{name}”.")
        self.library_changed.emit()

    def _commit_name(self):
        """Keep the inline name unique and never store a blank name."""
        g = self._cur()
        if g is None or self._suspend:
            return
        if not self.name_edit.text().strip():
            self._suspend = True
            self.name_edit.setText(g["name"])
            self._suspend = False
            return
        name = self.store.unique_name(g["name"], exclude_id=g["id"])
        if name == g["name"]:
            return
        self.store.rename(g["id"], name)
        self._suspend = True
        self.name_edit.setText(name)
        self._suspend = False
        self._refresh_list_item()
        self._save_timer.start()
        self.library_changed.emit()

    # -- editor ---------------------------------------------------------------
    def _load_editor(self):
        self._suspend = True
        try:
            g = self._cur()
            self.editor.setEnabled(g is not None)
            if g is None:
                self.name_edit.clear()
                self.table.setRowCount(0)
                self.bullets.setValue(MAX_ROWS)
                self._refresh_size()
                return
            self.name_edit.setText(g["name"])
            self.bullets.setValue(len(g["rows"]))
            self._refresh_rows(g["rows"])
            self._refresh_size()
        finally:
            self._suspend = False

    def _on_name_changed(self, text):
        if self._suspend or not self._cur_id:
            return
        if not text.strip():
            return                  # keep the stored name until editing ends
        self.store.rename(self._cur_id, text)
        self._refresh_list_item()
        self._save_timer.start()

    def _on_bullet_count(self, count):
        if self._suspend or not self._cur_id:
            return
        g = self._cur()
        if g is None:
            return
        rows = [list(r) for r in g["rows"]][:int(count)]
        while len(rows) < int(count):
            rows.append([0, 0, 10])
        self.store.set_rows(self._cur_id, rows, persist=False)
        self._refresh_rows(rows)
        self._refresh_size()
        self._save_timer.start()

    def _refresh_rows(self, rows):
        self.table.setRowCount(0)
        for i, row in enumerate(rows):
            x, y, delay = (list(row) + [0, 0, 10])[:3]
            r = self.table.rowCount()
            self.table.insertRow(r)

            num = QTableWidgetItem(str(r + 1))
            num.setTextAlignment(Qt.AlignCenter)
            num.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.table.setItem(r, 0, num)

            sx = _NoWheelSpin()
            sx.setRange(X_MIN, X_MAX)
            sx.setValue(int(x))
            sx.valueChanged.connect(lambda _v, i=r: self._on_row_changed(i))
            self.table.setCellWidget(r, 1, sx)

            sy = _NoWheelSpin()
            sy.setRange(Y_MIN, Y_MAX)
            sy.setValue(int(y))
            sy.valueChanged.connect(lambda _v, i=r: self._on_row_changed(i))
            self.table.setCellWidget(r, 2, sy)

            sd = _NoWheelSpin()
            sd.setRange(0, DELAY_MAX)
            sd.setSingleStep(DELAY_STEP)
            sd.setValue(int(delay))
            sd.valueChanged.connect(lambda _v, i=r: self._on_row_changed(i))
            self.table.setCellWidget(r, 3, sd)

    def _on_row_changed(self, index):
        if self._suspend or not self._cur_id:
            return
        g = self._cur()
        if g is None or not 0 <= index < self.table.rowCount():
            return
        x = self.table.cellWidget(index, 1).value()
        y = self.table.cellWidget(index, 2).value()
        delay = self.table.cellWidget(index, 3).value()
        self.store.set_row(self._cur_id, index, x, y, delay, persist=False)
        self._refresh_size()
        self._save_timer.start()

    def _toggle_how_to(self, expanded):
        self.how_steps.setVisible(bool(expanded))
        self.how_toggle.setText("Hide the steps" if expanded
                                else "Show the 5 steps")

    def _clear_offsets(self):
        g = self._cur()
        if g is None:
            return
        rows = [[0, 0, int(r[2])] for r in g["rows"]]
        self.store.set_rows(self._cur_id, rows, persist=False)
        self._refresh_rows(rows)
        self._refresh_size()
        self._save_timer.start()

    def _flip_axis(self, axis):
        if self._recording:
            return
        g = self._cur()
        if g is None:
            return
        rows = []
        for row in g["rows"]:
            x, y, delay = (list(row) + [0, 0, 10])[:3]
            if axis == 0:
                x = -int(x)
            else:
                y = -int(y)
            rows.append([x, y, delay])
        self.store.set_rows(self._cur_id, rows, persist=False)
        self._refresh_rows(rows)
        self._refresh_size()
        self._save_timer.start()

    # -- recording ------------------------------------------------------------
    def _toggle_record(self):
        if self._recording:
            self._finish_recording("stopped")
        else:
            self._start_recording()

    def _start_recording(self):
        g = self._cur()
        if g is None:
            self.record_status.setText("Select or create a pattern first.")
            return
        if not self.recorder.start():
            self.record_status.setText(
                "Raw mouse capture is unavailable on this system; recording "
                "needs Windows.")
            return
        self._flush()
        self._recording = True
        self._record_token += 1
        token = self._record_token
        self._record_gid = g["id"]
        self._record_rows = []
        self._record_moved = False
        self._record_total = max(1, self.bullets.value())
        self._record_interval = max(10, self.record_interval.value())
        self.record_btn.setText(f"{SQUARE} Stop")
        self.bullets.setEnabled(False)
        self.record_interval.setEnabled(False)
        self.flip_x_btn.setEnabled(False)
        self.flip_y_btn.setEnabled(False)
        self.record_status.setText(
            f"Starting in {self.ARM_MS // 1000} s — switch to the game and "
            f"fire {self._record_total} bullets.")
        QTimer.singleShot(self.ARM_MS, lambda: self._begin_sampling(token))

    def _begin_sampling(self, token):
        if not self._recording or token != self._record_token:
            return
        # Movement made while arming/alt-tabbing is not part of the pattern.
        self.recorder.take_delta()
        self._record_timer.start(self._record_interval)
        self.record_status.setText(
            f"Recording 0/{self._record_total} bullets at "
            f"{self._record_interval} ms — fire now.")

    def _record_sample(self):
        if not self._recording:
            return
        dx, dy = self.recorder.take_delta()
        dx = max(X_MIN, min(X_MAX, int(dx)))
        dy = max(Y_MIN, min(Y_MAX, int(dy)))
        if dx or dy:
            self._record_moved = True
        rows = self._record_rows + [[dx, dy, self._record_interval]]
        ok, message = gun_fits(rows)
        if not ok:
            # Keep the rows captured so far; the last sample would overflow.
            self._finish_recording(message)
            return
        self._record_rows = rows
        self._refresh_rows(rows)
        self._refresh_size()
        self.record_status.setText(
            f"Recording {len(rows)}/{self._record_total} bullets at "
            f"{self._record_interval} ms — fire now.")
        if len(rows) >= self._record_total:
            self._finish_recording("done")

    def _finish_recording(self, reason="stopped"):
        if not self._recording:
            return
        self._record_token += 1
        self._record_timer.stop()
        self.recorder.stop()
        self._recording = False
        self.record_btn.setText(f"{DOT} Record")
        self.bullets.setEnabled(True)
        self.record_interval.setEnabled(True)
        self.flip_x_btn.setEnabled(True)
        self.flip_y_btn.setEnabled(True)
        rows = [list(r) for r in self._record_rows]
        while len(rows) > 1 and rows[-1][0] == 0 and rows[-1][1] == 0:
            rows.pop()
        gid = self._record_gid
        moved = self._record_moved
        self._record_rows = []
        self._record_gid = None
        if not moved:
            # Do not wipe a pattern the user tuned when nothing was captured.
            self.record_status.setText(
                "No movement captured — the previous pattern was left "
                "unchanged.")
            self._load_editor()
            return
        if not rows:
            rows = [[0, 0, self._record_interval]]
        self.store.set_rows(gid, rows, persist=False)
        self._refresh_list_item()
        self._load_editor()
        self._refresh_size()
        if reason == "done":
            self.record_status.setText(
                f"Recorded {len(rows)} bullets at {self._record_interval} ms. "
                "Review the rows or flip axes if needed.")
        elif reason == "stopped":
            self.record_status.setText(
                f"Recorded {len(rows)} bullets. Review the rows or flip axes "
                "if needed.")
        else:
            self.record_status.setText(
                f"Recording stopped: {reason}. {len(rows)} rows were kept.")
        self._save_timer.start()
        self.library_changed.emit()

    def _refresh_size(self):
        g = self._cur()
        if g is None:
            self.size_label.setText("— / 128 bytes")
            self.size_label.setStyleSheet(f"color: {theme.TEXT_DIM};")
            self.size_label.setToolTip(
                "Select a pattern, or create one with + New.")
            self.pattern_note.setText("")
            self.pattern_note.setStyleSheet("")
            return
        rows = g.get("rows") or []
        size = gun_encoded_size(rows)
        ok, message = gun_fits(rows)
        self.size_label.setText(f"{size} / 128 bytes")
        self.size_label.setStyleSheet(
            f"color: {theme.WARN};" if not ok else f"color: {theme.TEXT_DIM};")
        self.size_label.setToolTip(
            message or "This pattern fits the device's 128-byte table entry.")
        self._refresh_pattern_note(rows, ok, message)

    def _refresh_pattern_note(self, rows, fits, message):
        """Explain the two patterns that look fine but do nothing on hardware."""
        notes = []
        negative = 0
        for row in rows or ():
            x, y, _delay = (list(row) + [0, 0, 10])[:3]
            if int(x) < 0 or int(y) < 0:
                negative += 1
        if negative:
            notes.append(
                f"{negative} row(s) use a negative offset. The firmware "
                "transmits |X| and |Y| without a sign, so those rows pull the "
                "same way as their positive values — keep X/Y >= 0 for a "
                "predictable right/down recoil compensation.")
        if rows and all((list(r) + [0, 0, 10])[0] == 0
                        and (list(r) + [0, 0, 10])[1] == 0 for r in rows):
            notes.append(
                "Every offset is zero, so this pattern does nothing. Set at "
                "least one X or Y offset.")
        if not fits:
            notes.append(message)
        self.pattern_note.setText("  ".join(notes))
        self.pattern_note.setStyleSheet(
            f"color: {theme.WARN};" if notes else f"color: {theme.TEXT_DIM};")

    def _flush(self):
        """Persist a burst of row edits, then let bound buttons re-sync."""
        if not self._save_timer.isActive() and not self.store.dirty:
            return
        self._save_timer.stop()
        self.store.save()
        self.library_changed.emit()

    def hideEvent(self, event):
        if self._recording:
            self._finish_recording("panel hidden")
        self._flush()
        super().hideEvent(event)
