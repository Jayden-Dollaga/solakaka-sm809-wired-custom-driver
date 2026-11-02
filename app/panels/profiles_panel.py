"""
app.panels.profiles_panel -- the Profiles management tab.

A searchable, sortable, drag-to-reorder list of profiles. The list ORDER is the
auto-switch match priority (first matching profile wins), so reordering here
directly controls which profile takes precedence. Double-click a profile to make
it active. CRUD lives in the rail's profile menu; this tab is for organising.

Signals:
  profile_selected(str)  -- activate this profile id (double-click)
  order_changed(object)  -- new list of profile ids after a manual drag
  sort_changed(str)      -- a predefined sort was chosen (az|za|latest|oldest|custom)
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QListWidget, QListWidgetItem, QAbstractItemView, QPushButton,
)

SORTS = [
    ("Custom order", "custom"),
    ("Alphabetical (A to Z)", "az"),
    ("Alphabetical (Z to A)", "za"),
    ("Latest", "latest"),
    ("Oldest", "oldest"),
]


class ProfilesPanel(QWidget):
    profile_selected = Signal(str)
    order_changed = Signal(object)
    sort_changed = Signal(str)
    new_requested = Signal()
    duplicate_requested = Signal()
    rename_requested = Signal()
    delete_requested = Signal()
    import_requested = Signal()
    export_requested = Signal()

    def __init__(self):
        super().__init__()
        self._loading = False

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(12)

        title = QLabel("Profiles")
        title.setProperty("panelTitle", "true")
        lay.addWidget(title)
        sub = QLabel("Drag to reorder — order sets auto-switch priority (first "
                     "matching profile wins). Double-click to activate. The wired "
                     "mouse stores up to 14 profiles.")
        sub.setProperty("panelSubtitle", "true")
        sub.setWordWrap(True)
        lay.addWidget(sub)

        self.search = QLineEdit()
        self.search.setClearButtonEnabled(True)
        self.search.setPlaceholderText("Search profiles…")
        self.search.textChanged.connect(self._apply_filter)
        lay.addWidget(self.search)

        srow = QHBoxLayout()
        srow.setSpacing(10)
        cap = QLabel("SORT BY")
        cap.setProperty("unit", "true")
        srow.addWidget(cap)
        self.sort = QComboBox()
        for label, key in SORTS:
            self.sort.addItem(label, key)
        self.sort.setMaximumWidth(320)
        self.sort.currentIndexChanged.connect(self._on_sort)
        srow.addWidget(self.sort, 1)
        srow.addStretch(2)
        lay.addLayout(srow)

        self.list = QListWidget()
        self.list.setObjectName("profileList")
        self.list.setDragDropMode(QAbstractItemView.InternalMove)
        self.list.setDefaultDropAction(Qt.MoveAction)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.itemDoubleClicked.connect(self._on_activate)
        self.list.model().rowsMoved.connect(self._on_rows_moved)
        lay.addWidget(self.list, 1)

        # The list used to be a nameless empty box when nothing was stored or
        # the search hid everything; say what is going on instead.
        self.empty = QLabel("")
        self.empty.setProperty("cardHint", "true")
        self.empty.setWordWrap(True)
        self.empty.hide()
        lay.addWidget(self.empty)

        # management actions (moved here from the rail menu)
        btns = QHBoxLayout()
        for label, sig in (("New", self.new_requested),
                           ("Duplicate", self.duplicate_requested),
                           ("Rename", self.rename_requested),
                           ("Delete", self.delete_requested)):
            b = QPushButton(label)
            b.clicked.connect(sig)
            btns.addWidget(b)
        btns.addStretch(1)
        lay.addLayout(btns)

        io_btns = QHBoxLayout()
        for label, sig, tip in (
                ("Import profile…", self.import_requested,
                 "Import a .pbin exported from the official SM809 driver "
                 "(profile menu (…) → Export), another wired .bin, or a "
                 "wireless-Pro .psf export."),
                ("Export .pbin…", self.export_requested,
                 "Save this profile as a .pbin. The official driver can load "
                 "it with its profile menu (…) → Import.")):
            b = QPushButton(label)
            b.clicked.connect(sig)
            if tip:
                b.setToolTip(tip)
            io_btns.addWidget(b)
        io_btns.addStretch(1)
        lay.addLayout(io_btns)

        transfer = QLabel("The .pbin format is shared with the official driver: "
                          "export here, then use the driver's profile menu (…) → "
                          "Import; export there, then use Import profile… here.")
        transfer.setProperty("cardHint", "true")
        transfer.setWordWrap(True)
        lay.addWidget(transfer)

    # -- external -------------------------------------------------------------
    def set_profiles(self, profiles, active_id, sort_key="custom"):
        keep = self.selected_id()      # survive a refresh (e.g. after Rename)
        self._loading = True
        self.list.clear()
        active_row = keep_row = -1
        for p in profiles:
            it = QListWidgetItem(p["name"])
            it.setData(Qt.UserRole, p["id"])
            if p["id"] == active_id:
                # A fresh item's font() has pointSize -1 ("inherit"), and Qt
                # logs QFont::setPointSize: Point size <= 0 when that is made
                # concrete.  Resolve against the list's real font first.
                base = self.list.font()
                if base.pointSize() <= 0 and base.pixelSize() <= 0:
                    base = QApplication.font()
                f = QFont(base)
                f.setWeight(QFont.DemiBold)
                it.setFont(f)
                active_row = self.list.count()
            if p["id"] == keep:
                keep_row = self.list.count()
            self.list.addItem(it)
        # Selecting a row makes it obvious which profile the mouse is on; it
        # also gives Rename/Delete/Export a sensible target.
        row = keep_row if keep_row >= 0 else active_row
        if row >= 0:
            self.list.setCurrentRow(row)
            self.list.scrollToItem(self.list.item(row))
        elif self.list.count():
            self.list.setCurrentRow(0)
        # reflect the persisted sort choice
        si = self.sort.findData(sort_key)
        self.sort.blockSignals(True)
        self.sort.setCurrentIndex(si if si >= 0 else 0)
        self.sort.blockSignals(False)
        self._loading = False
        self._apply_filter(self.search.text())

    def selected_id(self):
        """The id of the highlighted list row (the management target), or None."""
        it = self.list.currentItem()
        return it.data(Qt.UserRole) if it is not None else None

    # -- internals ------------------------------------------------------------
    def _ids_in_order(self):
        return [self.list.item(i).data(Qt.UserRole) for i in range(self.list.count())]

    def _apply_filter(self, text):
        t = (text or "").strip().lower()
        visible = 0
        for i in range(self.list.count()):
            it = self.list.item(i)
            hidden = bool(t) and t not in it.text().lower()
            it.setHidden(hidden)
            if not hidden:
                visible += 1
        if self.list.count() == 0:
            self.empty.setText(
                "No profiles yet. Use New below to create one, or Import "
                "profile… to bring in a .pbin from the official driver.")
        elif visible == 0:
            self.empty.setText(
                f"No profile matches “{text.strip()}”. Clear the search to "
                "see every profile again.")
        else:
            self.empty.setText("")
        self.empty.setVisible(visible == 0)

    def _on_activate(self, item):
        pid = item.data(Qt.UserRole)
        if pid:
            self.profile_selected.emit(pid)

    def _on_rows_moved(self, *_):
        if self._loading:
            return
        # a manual drag implies a custom order
        self.sort.blockSignals(True)
        self.sort.setCurrentIndex(0)
        self.sort.blockSignals(False)
        self.order_changed.emit(self._ids_in_order())

    def _on_sort(self, _idx):
        if self._loading:
            return
        key = self.sort.currentData()
        if key and key != "custom":
            self.sort_changed.emit(key)
