"""
app.panels.macro_panel -- the macro LIBRARY editor.

Create, name, record, and edit macros. There are NO slots here: macros are a
named, unlimited library (app.macro_store, persisted to JSON). A device slot is
assigned and the macro is uploaded only when it's bound to a button in the
Buttons tab (upload-on-assign) -- mirroring the official MacroLibraryFile.mlf.

A macro is a list of timed key/mouse/consumer events (sm809pro.macros format).
The EVENTS area is a web-driver-style table: one row per atomic event with an
inline Type (Down/Up/Delay), Key, Delay(ms) and per-row reorder/delete actions.
"Tap" inserts a Down+Up pair (two rows) so each half can be edited separately.
Recording captures real inter-event timing, including keyboard input and
system-wide mouse-button clicks (left/right/middle/back/forward), so a sequence
can be recorded while clicking in the application being automated. Stop (not
Esc) ends a recording.
"""

import os

from PySide6.QtCore import Qt, Signal, QElapsedTimer, QEvent
from PySide6.QtGui import QColor, QPalette, QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QPushButton, QLineEdit, QComboBox, QSpinBox, QFrame,
    QScrollArea, QSizePolicy, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QToolButton, QMenu,
    QFileDialog, QInputDialog, QMessageBox,
)

from .. import theme
from ..macro_file import FILE_FILTER, MacroFileError, load_macro, save_macro, suggest_name
from ..mouse_hook import MouseHook
from ..widgets.controls import Card
from sm809pro import actions as A
from sm809pro import macros as M

INSERT_DEFAULT_DELAY = 50   # ms, default inter-event gap for a manual insert
TAP_GAP = 10                # ms between the down and up of a "tap"
TEXT_DEFAULT_DELAY = 20     # ms per key for type-text-to-keystrokes

ARROW_DOWN = "\u2193"
ARROW_UP = "\u2191"
CROSS = "\u2715"
DASH = "\u2014"
DOT = "\u25cf"
SQUARE = "\u25a0"
ELLIP = "\u2026"


# --- Qt.Key -> HID keyboard usage (for the recorder) ------------------------
def _build_qt_to_hid():
    m = {}
    for i in range(26):
        m[int(Qt.Key_A) + i] = 0x04 + i
    for i in range(1, 10):
        m[int(Qt.Key_0) + i] = 0x1E + (i - 1)
    m[int(Qt.Key_0)] = 0x27
    for i in range(12):
        m[int(Qt.Key_F1) + i] = 0x3A + i
    for i in range(12):
        if hasattr(Qt, f"Key_F{13 + i}"):
            m[int(getattr(Qt, f"Key_F{13 + i}"))] = 0x68 + i
    m.update({
        int(Qt.Key_Space): 0x2C, int(Qt.Key_Return): 0x28, int(Qt.Key_Enter): 0x28,
        int(Qt.Key_Tab): 0x2B, int(Qt.Key_Escape): 0x29, int(Qt.Key_Backspace): 0x2A,
        int(Qt.Key_Delete): 0x4C, int(Qt.Key_Insert): 0x49, int(Qt.Key_Home): 0x4A,
        int(Qt.Key_End): 0x4D, int(Qt.Key_PageUp): 0x4B, int(Qt.Key_PageDown): 0x4E,
        int(Qt.Key_Left): 0x50, int(Qt.Key_Right): 0x4F, int(Qt.Key_Up): 0x52,
        int(Qt.Key_Down): 0x51, int(Qt.Key_CapsLock): 0x39,
        int(Qt.Key_Print): 0x46, int(Qt.Key_ScrollLock): 0x47, int(Qt.Key_Pause): 0x48,
        int(Qt.Key_NumLock): 0x53, int(Qt.Key_Menu): 0x65,
        int(Qt.Key_Control): 0xE0, int(Qt.Key_Shift): 0xE1, int(Qt.Key_Alt): 0xE2,
        int(Qt.Key_Meta): 0xE3,
        int(Qt.Key_Minus): 0x2D, int(Qt.Key_Equal): 0x2E, int(Qt.Key_BracketLeft): 0x2F,
        int(Qt.Key_BracketRight): 0x30, int(Qt.Key_Backslash): 0x31,
        int(Qt.Key_Semicolon): 0x33, int(Qt.Key_Apostrophe): 0x34,
        int(Qt.Key_QuoteLeft): 0x35, int(Qt.Key_Comma): 0x36, int(Qt.Key_Period): 0x37,
        int(Qt.Key_Slash): 0x38,
        int(Qt.Key_Asterisk): 0x55, int(Qt.Key_Plus): 0x57,
    })
    return m


QT_TO_HID = _build_qt_to_hid()


def _build_usage_names():
    n = {v: k.title() for k, v in A.HID.items()}
    for i in range(26):
        n[0x04 + i] = chr(ord("A") + i)
    for i in range(1, 25):
        usage = (0x39 + i) if i <= 12 else (0x68 + (i - 13))
        n[usage] = f"F{i}"
    n.update({
        0xE0: "L Ctrl", 0xE1: "L Shift", 0xE2: "L Alt", 0xE3: "L Win",
        0xE4: "R Ctrl", 0xE5: "R Shift", 0xE6: "R Alt", 0xE7: "R Win",
        0x28: "Enter", 0x29: "Esc", 0x2A: "Backspace", 0x2B: "Tab", 0x2C: "Space",
        0x4C: "Delete", 0x49: "Insert", 0x4A: "Home", 0x4D: "End",
        0x4B: "PgUp", 0x4E: "PgDn", 0x46: "PrtSc", 0x48: "Pause",
        0x50: "Left", 0x4F: "Right", 0x52: "Up", 0x51: "Down",
        0x39: "Caps", 0x47: "ScrollLock", 0x53: "NumLock",
        0x65: "Menu",
        0x2D: "-", 0x2E: "=", 0x2F: "[", 0x30: "]", 0x31: "\\", 0x33: ";",
        0x34: "'", 0x35: "`", 0x36: ",", 0x37: ".", 0x38: "/",
    })
    return n


USAGE_NAMES = _build_usage_names()
MOUSE_LABELS = {1: "Left", 2: "Right", 3: "Middle", 4: "Back", 5: "Forward"}
MOUSE_CHOICES = [("Left", 1), ("Right", 2), ("Middle", 3), ("Back", 4), ("Forward", 5)]
CONSUMER_CHOICES = [
    ("Play/Pause", 0xCD), ("Next Track", 0xB5), ("Prev Track", 0xB6),
    ("Stop", 0xB7), ("Volume +", 0xE9), ("Volume -", 0xEA), ("Mute", 0xE2),
]
CONSUMER_LABELS = {c: n for n, c in CONSUMER_CHOICES}


def usage_label(u):
    return USAGE_NAMES.get(u, f"0x{u:02X}")


def _key_insert_choices():
    out = [
        ("Left Ctrl", 0xE0), ("Left Shift", 0xE1), ("Left Alt", 0xE2),
        ("Left Win", 0xE3),
        ("Right Ctrl", 0xE4), ("Right Shift", 0xE5), ("Right Alt", 0xE6),
        ("Right Win", 0xE7),
    ]
    out += [(chr(ord("A") + i), 0x04 + i) for i in range(26)]
    out += [(str(d), A.HID[str(d)]) for d in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]]
    out += [
        ("Enter", 0x28), ("Tab", 0x2B), ("Space", 0x2C), ("Esc", 0x29),
        ("Backspace", 0x2A), ("Delete", 0x4C), ("Insert", 0x49),
        ("Home", 0x4A), ("End", 0x4D), ("Page Up", 0x4B), ("Page Down", 0x4E),
        ("Print Screen", 0x46), ("Pause", 0x48),
        ("Up", 0x52), ("Down", 0x51), ("Left", 0x50), ("Right", 0x4F),
    ]
    out += [(f"F{i}", 0x39 + i) for i in range(1, 13)]
    out += [(f"F{i}", 0x68 + (i - 13)) for i in range(13, 25)]
    out += [
        ("-", 0x2D), ("=", 0x2E), ("[", 0x2F), ("]", 0x30), ("\\", 0x31),
        (";", 0x33), ("'", 0x34), ("`", 0x35), (",", 0x36), (".", 0x37), ("/", 0x38),
    ]
    out += [
        ("Caps Lock", 0x39), ("Scroll Lock", 0x47), ("Num Lock", 0x53),
    ]
    out += [
        ("Num /", 0x54), ("Num *", 0x55), ("Num -", 0x56), ("Num +", 0x57), ("Num Enter", 0x58),
        ("Num 1", 0x59), ("Num 2", 0x5A), ("Num 3", 0x5B), ("Num 4", 0x5C), ("Num 5", 0x5D),
        ("Num 6", 0x5E), ("Num 7", 0x5F), ("Num 8", 0x60), ("Num 9", 0x61), ("Num 0", 0x62),
        ("Num .", 0x63),
    ]
    out += [("Menu", 0x65)]
    return out


KEY_INSERT_CHOICES = _key_insert_choices()

INSERT_TYPES = [
    ("Key - tap", ("key", "tap")),
    ("Key - hold (down)", ("key", "down")),
    ("Key - release (up)", ("key", "up")),
    ("Mouse - tap", ("mouse", "tap")),
    ("Mouse - hold (down)", ("mouse", "down")),
    ("Mouse - release (up)", ("mouse", "up")),
    ("Delay (pause)", ("delay", "tap")),
]

# per-event category -> (Key-column choices, the event field holding the code)
CAT_CHOICES = {"key": KEY_INSERT_CHOICES, "mouse": MOUSE_CHOICES, "consumer": CONSUMER_CHOICES}
CAT_FIELD = {"key": "keycode", "mouse": "button", "consumer": "code"}


def event_label(ev) -> str:
    """One-line description of an event (kept for diagnostics/tests)."""
    t = ev["type"]
    if t == "delay":
        return f"||  Delay {ev.get('ms', 0)} ms"
    nd = ev.get("next_delay", 0)
    arrow = ARROW_DOWN if ev.get("down", True) else ARROW_UP
    if t == "key":
        desc = f"Key {usage_label(ev['keycode'])}"
    elif t == "mouse":
        desc = f"Mouse {MOUSE_LABELS.get(ev['button'], ev['button'])}"
    else:
        desc = f"Media {CONSUMER_LABELS.get(ev.get('code', 0), hex(ev.get('code', 0)))}"
    tail = f"+{nd}ms" if nd else ""
    return f"{arrow}  {desc:<18} {tail:>7}"


class _NoWheelCombo(QComboBox):
    """A combo that ignores the scroll wheel, so scrolling the events list
    never accidentally changes a row's value. Click to open; keys still work."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, e):
        e.ignore()


class _NoWheelSpin(QSpinBox):
    """A spinbox that ignores the scroll wheel (use the arrows or type)."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, e):
        e.ignore()


class _Recorder(QFrame):
    """A framed surface that captures live keystrokes with timing.

    While armed it grabs the keyboard, so every key down/up routes here (Esc
    included, so it's recordable). Stop is via the Record toggle button only.
    """
    keyEvent = Signal(int, bool)

    _IDLE = ('Click "Record Input", then type or click the mouse — including '
             'in another app. Captures real timing. Click Stop to finish.')

    def __init__(self):
        super().__init__()
        self.setProperty("card", "true")
        self.setFocusPolicy(Qt.StrongFocus)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 12, 16, 12)
        lay.setSpacing(4)
        self.status = QLabel(self._IDLE)
        self.status.setProperty("cardHint", "true")
        self.status.setWordWrap(True)
        lay.addWidget(self.status)

    def start(self, mouse=True):
        self.setFocus()
        self.grabKeyboard()
        tail = " or click any mouse button" if mouse else ""
        if not mouse:
            tail = " (mouse capture unavailable)"
        self.status.setText(
            f"{DOT} Recording {DASH} type your keys{tail}{ELLIP} "
            "(click Stop to finish)")
        self.status.setStyleSheet(f"color: {theme.ACCENT};")

    def stop(self):
        self.releaseKeyboard()
        self.status.setText(self._IDLE)
        self.status.setStyleSheet("")

    def keyPressEvent(self, e):
        if e.isAutoRepeat():
            return
        u = QT_TO_HID.get(e.key())
        if u is not None:
            self.keyEvent.emit(u, True)

    def keyReleaseEvent(self, e):
        if e.isAutoRepeat():
            return
        u = QT_TO_HID.get(e.key())
        if u is not None:
            self.keyEvent.emit(u, False)


class MacroPanel(QWidget):
    """Named macro library editor. Emits library_changed on any mutation."""
    library_changed = Signal()

    def __init__(self, store):
        super().__init__()
        self.store = store
        self._cur_id = None
        self._suspend = False
        self._recording = False
        self._rec_timer = QElapsedTimer()
        self._mouse_hook = MouseHook(self)
        self._mouse_hook.mouseEvent.connect(self._on_record_mouse)

        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(16)

        title = QLabel("Macros")
        title.setProperty("panelTitle", "true")
        root.addWidget(title)
        sub = QLabel("Build a named macro here, then bind a button to it in the "
                     "Buttons tab. Macros upload to the mouse when assigned.")
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

    def _index_of(self, ev):
        m = self._cur()
        if not m:
            return -1
        for i, e in enumerate(m["events"]):
            if e is ev:
                return i
        return -1

    def eventFilter(self, obj, event):
        # clicking/focusing any cell widget selects its row, so the highlight
        # (and thus the Insert target) follows where the user is working
        if event.type() in (QEvent.FocusIn, QEvent.MouseButtonPress):
            ev = getattr(obj, "_ev", None)
            if ev is not None:
                r = self._index_of(ev)
                if r >= 0 and r != self.events_table.currentRow():
                    self.events_table.selectRow(r)
        return super().eventFilter(obj, event)

    # -- left column ----------------------------------------------------------
    def _build_left(self):
        col = QWidget()
        col.setFixedWidth(224)
        lay = QVBoxLayout(col)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        cap = QLabel("MACRO LIBRARY")
        cap.setProperty("groupLabel", "true")
        lay.addWidget(cap)

        self.macro_list = QListWidget()
        self.macro_list.currentRowChanged.connect(self._on_list_row)
        self.macro_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.macro_list.customContextMenuRequested.connect(self._list_menu)
        lay.addWidget(self.macro_list, 1)
        # F2 renames the selected macro; it works while the list has focus.
        QShortcut(QKeySequence("F2"), self.macro_list,
                  activated=self.rename_macro_dialog)

        row = QHBoxLayout()
        row.setSpacing(8)
        new_btn = QPushButton("+ New")
        new_btn.clicked.connect(self.new_macro)
        del_btn = QPushButton("Delete")
        del_btn.clicked.connect(self.delete_macro)
        menu_btn = QToolButton()
        menu_btn.setText(ELLIP)
        menu_btn.setToolTip("Rename, import or export a macro")
        menu_btn.setPopupMode(QToolButton.InstantPopup)
        menu = QMenu(menu_btn)
        menu.addAction("Rename…", self.rename_macro_dialog)
        menu.addSeparator()
        menu.addAction("Import .mbin…", self.import_macro_dialog)
        menu.addAction("Export .mbin…", self.export_macro_dialog)
        menu.addAction("Export protected .mbin…",
                       lambda: self.export_macro_dialog(protected=True))
        menu_btn.setMenu(menu)
        row.addWidget(new_btn)
        row.addWidget(del_btn)
        row.addWidget(menu_btn)
        lay.addLayout(row)

        self.status = QLabel("")
        self.status.setProperty("cardHint", "true")
        self.status.setWordWrap(True)
        lay.addWidget(self.status)

        hint = QLabel("Saved automatically. Assign a macro to a button in the "
                      "Buttons tab to load it onto the mouse. Import/Export "
                      "uses the original driver's .mbin format.")
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        lay.addWidget(hint)
        return col

    # -- right editor (scrollable) -------------------------------------------
    def _build_editor(self):
        self.editor = QWidget()
        lay = QVBoxLayout(self.editor)
        lay.setContentsMargins(0, 0, 4, 0)
        lay.setSpacing(14)

        top = QHBoxLayout()
        top.setSpacing(10)
        top.addWidget(QLabel("Name"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Macro name")
        self.name_edit.textChanged.connect(self._on_name_changed)
        self.name_edit.editingFinished.connect(self._commit_name)
        top.addWidget(self.name_edit, 1)
        lay.addLayout(top)

        build = Card("BUILD MACRO")
        self.record_btn = QPushButton(f"{DOT} Record Input")
        self.record_btn.clicked.connect(self._toggle_record)
        self._mouse_hook.set_ignore_widgets(self.record_btn)
        build.add(self.record_btn)
        self.recorder = _Recorder()
        self.recorder.keyEvent.connect(self._on_record_key)
        build.add(self.recorder)

        build.add(self._sep())

        # Two lines per insert: the event pickers on one, the timing and the
        # button on the next.  One long line was wider than the editor at the
        # default window size, so "Insert" and the delay were clipped.
        pick = QHBoxLayout()
        pick.setSpacing(8)
        self.type_combo = _NoWheelCombo()
        self.type_combo.setObjectName("macroPicker")
        for label, data in INSERT_TYPES:
            self.type_combo.addItem(label, data)
        self.type_combo.currentIndexChanged.connect(self._on_type_changed)
        self.type_combo.setToolTip(
            "What the inserted event does: press, release or wait")
        pick.addWidget(self.type_combo, 1)
        self.detail_combo = _NoWheelCombo()
        self.detail_combo.setObjectName("macroPicker")
        self.detail_combo.setToolTip("Key, mouse button or media key to send")
        pick.addWidget(self.detail_combo, 1)
        build.add(pick)

        ins = QHBoxLayout()
        ins.setSpacing(8)
        ins.addWidget(QLabel("Delay"))
        self.delay_spin = _NoWheelSpin()
        self.delay_spin.setRange(0, 4095)
        self.delay_spin.setValue(INSERT_DEFAULT_DELAY)
        self.delay_spin.setSuffix(" ms")
        self.delay_spin.setFixedWidth(108)
        self.delay_spin.setToolTip(
            "Wait stored with this event, in milliseconds")
        ins.addWidget(self.delay_spin)
        ins.addStretch(1)
        add_btn = QPushButton("Insert event")
        add_btn.setToolTip("Add this event after the selected row")
        add_btn.clicked.connect(self._do_insert)
        ins.addWidget(add_btn)
        build.add(ins)

        txt = QHBoxLayout()
        txt.setSpacing(8)
        self.text_edit = QLineEdit()
        self.text_edit.setPlaceholderText(f"Type text to insert as keystrokes{ELLIP}")
        self.text_edit.returnPressed.connect(self._do_add_text)
        txt.addWidget(self.text_edit, 1)
        build.add(txt)

        txt_opts = QHBoxLayout()
        txt_opts.setSpacing(8)
        txt_opts.addWidget(QLabel("Per key"))
        self.text_delay = _NoWheelSpin()
        self.text_delay.setRange(1, 4095)
        self.text_delay.setValue(TEXT_DEFAULT_DELAY)
        self.text_delay.setSuffix(" ms")
        self.text_delay.setFixedWidth(108)
        self.text_delay.setToolTip(
            "Typing speed: gap between each generated keystroke, in milliseconds")
        txt_opts.addWidget(self.text_delay)
        txt_opts.addStretch(1)
        text_btn = QPushButton("Add text")
        text_btn.clicked.connect(self._do_add_text)
        txt_opts.addWidget(text_btn)
        build.add(txt_opts)

        lay.addWidget(build)

        head = QHBoxLayout()
        ev_cap = QLabel("EVENTS")
        ev_cap.setProperty("groupLabel", "true")
        head.addWidget(ev_cap)
        head.addStretch(1)
        self.events_count = QLabel(self._count_text(0))
        self.events_count.setProperty("cardHint", "true")
        head.addWidget(self.events_count)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear_events)
        head.addWidget(clear_btn)
        lay.addLayout(head)

        self.events_table = QTableWidget(0, 5)
        self.events_table.setObjectName("macroEvents")
        self.events_table.setHorizontalHeaderLabels(["#", "Type", "Key", "Delay (ms)", ""])
        self.events_table.verticalHeader().setVisible(False)
        self.events_table.verticalHeader().setDefaultSectionSize(44)
        self.events_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.events_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.events_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.events_table.setShowGrid(False)
        self.events_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.events_table.setMinimumHeight(220)
        hh = self.events_table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.Fixed)
        hh.setSectionResizeMode(1, QHeaderView.Fixed)
        hh.setSectionResizeMode(2, QHeaderView.Stretch)
        hh.setSectionResizeMode(3, QHeaderView.Fixed)
        hh.setSectionResizeMode(4, QHeaderView.Fixed)
        hh.setHighlightSections(False)
        self.events_table.setColumnWidth(0, 34)
        self.events_table.setColumnWidth(1, 82)
        self.events_table.setColumnWidth(3, 84)
        self.events_table.setColumnWidth(4, 92)
        # selected-row highlight uses the app's "active surface" color; the
        # in-cell widgets are transparent (theme) so this shows behind them
        pal = self.events_table.palette()
        for grp in (QPalette.Active, QPalette.Inactive):
            pal.setColor(grp, QPalette.Highlight, QColor(theme.SURFACE_2))
            pal.setColor(grp, QPalette.HighlightedText, QColor(theme.TEXT))
        self.events_table.setPalette(pal)
        lay.addWidget(self.events_table, 1)

        hint = QLabel("Each row is one event. Switch Down/Up/Delay in the Type "
                      "column, edit the key and timing inline, reorder or remove with "
                      "the row actions. Insert / Tap / Add Text add events after the "
                      "selected row. Recording captures mouse buttons system-wide; "
                      "the Stop button's own click is ignored.")
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        lay.addWidget(hint)

        self._on_type_changed()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.editor)
        self._editor_scroll = scroll
        return scroll

    # -- library list ---------------------------------------------------------
    @staticmethod
    def _item_text(m):
        folder = (m.get("folder") or "").strip()
        prefix = f"{folder} / " if folder else ""
        return f"{prefix}{m['name']}  ({len(m['events'])})"

    def _refresh_list(self):
        self.macro_list.blockSignals(True)
        self.macro_list.clear()
        for m in self.store.all():
            self.macro_list.addItem(self._item_text(m))
        self.macro_list.blockSignals(False)

    def _refresh_list_item(self):
        i = self.store.index_of(self._cur_id)
        m = self._cur()
        it = self.macro_list.item(i) if i >= 0 else None
        if it and m:
            it.setText(self._item_text(m))

    def new_macro(self):
        name = self.store.unique_name(f"Macro {len(self.store.all()) + 1}")
        m = self.store.add(name)
        self._refresh_list()
        self.macro_list.setCurrentRow(self.store.index_of(m["id"]))
        self.library_changed.emit()

    def delete_macro(self):
        if not self._cur_id:
            return
        idx = self.store.index_of(self._cur_id)
        self.store.delete(self._cur_id)
        self._cur_id = None
        self._refresh_list()
        n = len(self.store.all())
        if n:
            self.macro_list.setCurrentRow(min(idx, n - 1))
        else:
            self._load_editor()
        self.library_changed.emit()

    def _on_list_row(self, row):
        macros = self.store.all()
        self._cur_id = macros[row]["id"] if 0 <= row < len(macros) else None
        self._load_editor()

    # -- rename / import / export --------------------------------------------
    def _list_menu(self, pos):
        item = self.macro_list.itemAt(pos)
        if item is not None:
            self.macro_list.setCurrentRow(self.macro_list.row(item))
        has_current = self._cur() is not None
        menu = QMenu(self)
        rename = menu.addAction("Rename…", self.rename_macro_dialog)
        rename.setEnabled(has_current)
        menu.addSeparator()
        menu.addAction("Import .mbin…", self.import_macro_dialog)
        export = menu.addAction("Export .mbin…", self.export_macro_dialog)
        export.setEnabled(has_current)
        protected = menu.addAction(
            "Export protected .mbin…",
            lambda: self.export_macro_dialog(protected=True))
        protected.setEnabled(has_current)
        menu.addSeparator()
        delete = menu.addAction("Delete", self.delete_macro)
        delete.setEnabled(has_current)
        menu.exec(self.macro_list.viewport().mapToGlobal(pos))

    def rename_macro_dialog(self):
        m = self._cur()
        if m is None:
            return
        name, ok = QInputDialog.getText(
            self, "Rename macro", "Macro name:", text=m["name"])
        if not ok:
            return
        name = self.store.unique_name(name, exclude_id=m["id"])
        if name == m["name"]:
            return
        self.store.rename(m["id"], name)
        self._suspend = True
        self.name_edit.setText(name)
        self._suspend = False
        self._refresh_list_item()
        self.status.setText(f"Renamed to “{name}”.")
        self.library_changed.emit()

    def _commit_name(self):
        """Make the inline name field unique once editing finishes."""
        m = self._cur()
        if m is None or self._suspend:
            return
        if not self.name_edit.text().strip():
            # a blank field never renames anything; put the stored name back
            self._suspend = True
            self.name_edit.setText(m["name"])
            self._suspend = False
            return
        name = self.store.unique_name(m["name"], exclude_id=m["id"])
        if name != m["name"]:
            self.store.rename(m["id"], name)
            self._suspend = True
            self.name_edit.setText(name)
            self._suspend = False
            self._refresh_list_item()
            self.library_changed.emit()

    def import_macro_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Import macro", "", FILE_FILTER)
        if not path:
            return
        try:
            data = load_macro(path)
        except (OSError, MacroFileError) as exc:
            QMessageBox.warning(self, "Import macro", str(exc))
            return
        name = self.store.unique_name(data["name"])
        m = self.store.add(name, data["events"], loop=data.get("loop", 1),
                           folder=data.get("folder", ""),
                           protected=data.get("protected", False))
        self._refresh_list()
        self.macro_list.setCurrentRow(self.store.index_of(m["id"]))
        self.status.setText(
            f"Imported “{os.path.basename(path)}” as “{name}” "
            f"({len(m['events'])} events).")
        self.library_changed.emit()

    def export_macro_dialog(self, protected=False):
        m = self._cur()
        if m is None:
            QMessageBox.information(self, "Export macro",
                                    "Select a macro first.")
            return
        start = os.path.join(os.path.expanduser("~"), suggest_name(m))
        path, _ = QFileDialog.getSaveFileName(
            self, "Export macro", start, FILE_FILTER)
        if not path:
            return
        if not path.lower().endswith(".mbin"):
            path += ".mbin"
        try:
            save_macro(path, m, protected=protected)
        except (OSError, MacroFileError) as exc:
            QMessageBox.warning(self, "Export macro", str(exc))
            return
        kind = "protected " if protected else ""
        self.status.setText(
            f"Exported {kind}“{m['name']}” to {os.path.basename(path)}.")

    # -- editor load ----------------------------------------------------------
    def _load_editor(self):
        self._suspend = True
        try:
            m = self._cur()
            self.editor.setEnabled(m is not None)
            if m is None:
                self.name_edit.clear()
                self.events_table.setRowCount(0)
                self.events_count.setText(self._count_text(0))
                return
            self.name_edit.setText(m["name"])
            self._refresh_events()
            if m["events"]:
                self.events_table.selectRow(len(m["events"]) - 1)
        finally:
            self._suspend = False

    def _on_name_changed(self, text):
        if self._suspend or not self._cur_id:
            return
        if not text.strip():
            return                      # keep the stored name until editing ends
        self.store.rename(self._cur_id, text)
        self._refresh_list_item()
        self.library_changed.emit()

    # -- events table ---------------------------------------------------------
    def _refresh_events(self):
        t = self.events_table
        t.setRowCount(0)
        m = self._cur()
        n = len(m["events"]) if m else 0
        self.events_count.setText(self._count_text(n))
        # warn-color only when at the cap, normal otherwise
        self.events_count.setStyleSheet(
            f"color: {theme.WARN};" if n >= M.MAX_MACRO_EVENTS else "")
        self.events_count.setProperty("cardHint", "true")
        if not m:
            return
        for ev in m["events"]:
            self._append_row(ev)

    def _append_row(self, ev):
        """Build one editable table row bound (by closure) to event dict `ev`."""
        t = self.events_table
        r = t.rowCount()
        t.insertRow(r)
        is_delay = ev["type"] == "delay"

        num = QTableWidgetItem(str(r + 1))
        num.setTextAlignment(Qt.AlignCenter)
        num.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        t.setItem(r, 0, num)

        # Type: Down / Up / Delay
        type_cb = _NoWheelCombo()
        type_cb.addItems(["Down", "Up", "Delay"])
        type_cb.setCurrentText("Delay" if is_delay else ("Down" if ev.get("down", True) else "Up"))
        type_cb.currentTextChanged.connect(lambda txt, e=ev: self._on_row_type(e, txt))
        t.setCellWidget(r, 1, type_cb)

        # Key / Button / Media (disabled for a pure Delay)
        key_cb = _NoWheelCombo()
        cat = ev["type"]
        if cat in CAT_CHOICES:
            for name, code in CAT_CHOICES[cat]:
                key_cb.addItem(name, code)
            self._select_data(key_cb, ev.get(CAT_FIELD[cat], 0))
            field = CAT_FIELD[cat]
            key_cb.currentIndexChanged.connect(
                lambda _i, e=ev, cb=key_cb, f=field: self._set_code(e, f, cb.currentData()))
        else:
            key_cb.addItem(DASH)
            key_cb.setEnabled(False)
        t.setCellWidget(r, 2, key_cb)

        # Delay (ms) -- next_delay for normal events, ms for a Delay row
        delay_sb = _NoWheelSpin()
        delay_sb.setRange(0, 4095)
        delay_sb.setValue(ev.get("ms", 0) if is_delay else ev.get("next_delay", 0))
        delay_sb.valueChanged.connect(lambda v, e=ev: self._set_delay(e, v))
        t.setCellWidget(r, 3, delay_sb)

        # Actions: up / down / delete
        actions = QWidget()
        al = QHBoxLayout(actions)
        al.setContentsMargins(2, 2, 2, 2)
        al.setSpacing(3)
        up = QToolButton(); up.setText(ARROW_UP)
        up.clicked.connect(lambda _=False, e=ev: self._row_move(e, -1))
        dn = QToolButton(); dn.setText(ARROW_DOWN)
        dn.clicked.connect(lambda _=False, e=ev: self._row_move(e, 1))
        rm = QToolButton(); rm.setText(CROSS)
        rm.clicked.connect(lambda _=False, e=ev: self._row_delete(e))
        for b in (up, dn, rm):
            al.addWidget(b)
        al.addStretch(1)
        t.setCellWidget(r, 4, actions)

        for w in (type_cb, key_cb, delay_sb):
            w._ev = ev
            w.installEventFilter(self)

    @staticmethod
    def _select_data(cb, data):
        i = cb.findData(data)
        if i >= 0:
            cb.setCurrentIndex(i)

    def _save_only(self):
        """In-place edit (key/delay/down flip): persist + notify, no rebuild."""
        if self._suspend:
            return
        self.store.save()
        self.library_changed.emit()

    def _on_row_type(self, ev, txt):
        if self._suspend:
            return
        if txt == "Delay":
            if ev["type"] != "delay":
                d = ev.get("next_delay", 0)
                ev.clear()
                ev.update({"type": "delay", "ms": d})
                self._commit(select_index=self._index_of(ev))
        else:
            down = (txt == "Down")
            if ev["type"] == "delay":
                ms = ev.get("ms", 0)
                ev.clear()
                ev.update({"type": "key", "keycode": 0x04, "down": down, "next_delay": ms})
                self._commit(select_index=self._index_of(ev))
            else:
                ev["down"] = down            # plain flip; row already shows it
                self._save_only()

    def _set_code(self, ev, field, data):
        if data is None:
            return
        ev[field] = int(data)
        self._save_only()

    def _set_delay(self, ev, val):
        if ev["type"] == "delay":
            ev["ms"] = int(val)
        else:
            ev["next_delay"] = int(val)
        self._save_only()

    def _row_move(self, ev, delta):
        m = self._cur()
        if not m:
            return
        i = self._index_of(ev)
        j = i + delta
        if 0 <= i < len(m["events"]) and 0 <= j < len(m["events"]):
            m["events"][i], m["events"][j] = m["events"][j], m["events"][i]
            self._commit(select_index=j)

    def _row_delete(self, ev):
        m = self._cur()
        if not m:
            return
        i = self._index_of(ev)
        if 0 <= i < len(m["events"]):
            m["events"].pop(i)
            n = len(m["events"])
            self._commit(select_index=(min(i, n - 1) if n else None))

    # -- commit / insert ------------------------------------------------------
    def _commit(self, select_index=None):
        self.store.save()
        self._refresh_events()
        self._refresh_list_item()
        if select_index is not None and 0 <= select_index < self.events_table.rowCount():
            self.events_table.selectRow(select_index)
        self.library_changed.emit()

    def _count_text(self, n):
        s = f"{n} / {M.MAX_MACRO_EVENTS} events"
        return s + "  (max)" if n >= M.MAX_MACRO_EVENTS else s

    def _room(self):
        """How many more events fit before the device per-slot limit."""
        m = self._cur()
        return M.MAX_MACRO_EVENTS - (len(m["events"]) if m else 0)

    def _insert_at(self):
        pos = self.events_table.currentRow()
        m = self._cur()
        n = len(m["events"]) if m else 0
        return (pos + 1) if pos >= 0 else n

    def insert_event(self, category, code, mode="tap", delay=INSERT_DEFAULT_DELAY):
        """Insert event(s) AFTER the selected one. category: key|mouse|consumer|delay.
        mode 'tap' inserts a Down+Up pair (two rows)."""
        m = self._cur()
        if not m:
            return
        delay = max(0, min(4095, int(delay)))
        new = []
        if category == "delay":
            new.append({"type": "delay", "ms": delay})
        else:
            field = CAT_FIELD[category]

            def mk(down, nd):
                return {"type": category, field: int(code), "down": down, "next_delay": nd}

            if mode == "tap":
                new = [mk(True, TAP_GAP), mk(False, delay)]
            elif mode == "down":
                new = [mk(True, delay)]
            else:
                new = [mk(False, delay)]
        if len(new) > self._room():
            self._warn_limit()
            return
        at = self._insert_at()
        m["events"][at:at] = new
        self._commit(select_index=at + len(new) - 1)

    def add_text_events(self, text, delay=TEXT_DEFAULT_DELAY):
        m = self._cur()
        if not m or not text:
            return
        d = max(1, min(4095, int(delay)))
        evs = M.text_to_events(text, key_delay=d)
        room = self._room()
        if room <= 0:
            self._warn_limit()
            return
        if len(evs) > room:
            evs = evs[:room]            # truncate to fit the device limit
            self._warn_limit()
        at = self._insert_at()
        m["events"][at:at] = evs
        self._commit(select_index=at + len(evs) - 1)

    def _warn_limit(self):
        self.events_count.setText(
            f"{M.MAX_MACRO_EVENTS} / {M.MAX_MACRO_EVENTS} events  (max reached)")
        self.events_count.setStyleSheet(f"color: {theme.WARN};")

    def _on_type_changed(self, *_):
        cat, _mode = self.type_combo.currentData()
        self.detail_combo.clear()
        if cat == "key":
            for name, u in KEY_INSERT_CHOICES:
                self.detail_combo.addItem(name, u)
        elif cat == "mouse":
            for name, b in MOUSE_CHOICES:
                self.detail_combo.addItem(name, b)
        elif cat == "consumer":
            for name, c in CONSUMER_CHOICES:
                self.detail_combo.addItem(name, c)
        self.detail_combo.setEnabled(cat != "delay")

    def _do_insert(self):
        cat, mode = self.type_combo.currentData()
        code = self.detail_combo.currentData() if cat != "delay" else None
        self.insert_event(cat, code, mode=mode, delay=self.delay_spin.value())

    def _do_add_text(self):
        text = self.text_edit.text()
        if not text:
            return
        self.add_text_events(text, self.text_delay.value())
        self.text_edit.clear()

    def _clear_events(self):
        m = self._cur()
        if not m or not m["events"]:
            return
        m["events"].clear()
        self._commit()

    # -- recording ------------------------------------------------------------
    def _toggle_record(self):
        if self._recording:
            self._stop_recording()
        else:
            self._start_recording()

    def _start_recording(self):
        if not self._cur():
            return
        self._recording = True
        m = self._cur()
        self._rec_start_idx = len(m["events"])
        self._rec_last_t = None
        self._rec_timer.restart()
        self.record_btn.setText(f"{SQUARE} Stop Recording")
        mouse_ok = self._mouse_hook.start()
        self.recorder.start(mouse=mouse_ok)

    def _stop_recording(self):
        if not self._recording:
            return
        self._recording = False
        # Unhook before the final commit: releasing the Stop button itself must
        # never reach the macro (the hook also ignores this process).
        self._mouse_hook.stop()
        self.recorder.stop()
        self.record_btn.setText(f"{DOT} Record Input")
        m = self._cur()
        if m and len(m["events"]) > self._rec_start_idx:
            self._commit(select_index=len(m["events"]) - 1)

    def _on_record_key(self, usage, down):
        self._record_event({"type": "key", "keycode": int(usage),
                            "down": bool(down), "next_delay": 0})

    def _on_record_mouse(self, button, down):
        """Intake for the system-wide mouse hook (buttons 1..5)."""
        button = int(button)
        if button not in MOUSE_LABELS:
            return
        self._record_event({"type": "mouse", "button": button,
                            "down": bool(down), "next_delay": 0})

    def _record_event(self, ev):
        """Append one recorded event and back-fill the previous delay."""
        if not self._recording:
            return
        m = self._cur()
        if not m:
            return
        # stop automatically once the device per-slot limit is reached
        if len(m["events"]) >= M.MAX_MACRO_EVENTS:
            self._stop_recording()
            self._warn_limit()
            return
        now = self._rec_timer.elapsed()
        evs = m["events"]
        # back-fill next_delay on the previous event now that we know the gap,
        # and reflect it live in that row's delay spinbox
        if self._rec_last_t is not None and len(evs) > self._rec_start_idx:
            gap = max(0, min(4095, now - self._rec_last_t))
            evs[-1]["next_delay"] = gap
            last_row = self.events_table.rowCount() - 1
            sb = self.events_table.cellWidget(last_row, 3)
            if isinstance(sb, QSpinBox):
                sb.blockSignals(True)
                sb.setValue(gap)
                sb.blockSignals(False)
        evs.append(ev)
        self._append_row(ev)
        self.events_table.scrollToBottom()
        self.events_count.setText(self._count_text(len(evs)))
        self._rec_last_t = now

    def hideEvent(self, e):
        if self._recording:
            self._stop_recording()
        else:
            self._mouse_hook.stop()
        super().hideEvent(e)

    def closeEvent(self, e):
        if self._recording:
            self._stop_recording()
        else:
            self._mouse_hook.stop()
        super().closeEvent(e)
