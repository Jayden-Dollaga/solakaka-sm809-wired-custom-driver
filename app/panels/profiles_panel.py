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
    manage_apps_requested = Signal(str)     # profile id -> open Manage Apps

    def __init__(self):
        super().__init__()
        self._loading = False
        self._rules_by_pid = {}     # pid -> auto-switch match rules

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
        self.subtitle = sub
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
        self.list.currentItemChanged.connect(self._on_current_changed)
        self.list.model().rowsMoved.connect(self._on_rows_moved)
        lay.addWidget(self.list, 1)

        # The list used to be a nameless empty box when nothing was stored or
        # the search hid everything; say what is going on instead.
        self.empty = QLabel("")
        self.empty.setProperty("cardHint", "true")
        self.empty.setWordWrap(True)
        self.empty.hide()
        lay.addWidget(self.empty)

        # Custom apps belong to one profile at a time; selecting a row shows
        # that profile's list so it is obvious where auto-switch rules live.
        apps_row = QHBoxLayout()
        self.apps_hint = QLabel("")
        self.apps_hint.setProperty("cardHint", "true")
        self.apps_hint.setWordWrap(True)
        apps_row.addWidget(self.apps_hint, 1)
        self.manage_apps_btn = QPushButton("Manage apps…")
        self.manage_apps_btn.setToolTip(
            "Open Manage Apps with this profile selected")
        self.manage_apps_btn.clicked.connect(self._on_manage_apps)
        apps_row.addWidget(self.manage_apps_btn)
        lay.addLayout(apps_row)

        # management actions (moved here from the rail menu)
        btns = QHBoxLayout()
        for label, sig in (("New", self.new_requested),
                           ("Duplicate", self.duplicate_requested),
                           ("Rename", self.rename_requested),
                           ("Delete", self.delete_requested)):
            b = QPushButton(label)
            b.clicked.connect(sig)
            btns.addWidget(b)
        # Qt's drag reorder needs an OLE drop target, which an elevated window
        # cannot have (see app.win_drop); these buttons keep the order usable.
        self.up_btn = QPushButton("Move up")
        self.up_btn.setToolTip("Move the selected profile one place earlier "
                               "(auto-switch checks profiles top to bottom)")
        self.up_btn.clicked.connect(lambda: self.move_selected(-1))
        self.down_btn = QPushButton("Move down")
        self.down_btn.setToolTip("Move the selected profile one place later")
        self.down_btn.clicked.connect(lambda: self.move_selected(1))
        btns.addWidget(self.up_btn)
        btns.addWidget(self.down_btn)
        btns.addStretch(1)
        lay.addLayout(btns)

        io_btns = QHBoxLayout()
        for label, sig, tip in (
                ("Import files…", self.import_requested,
                 "Import one or more .pbin / .bin / .psf profiles or .mbin "
                 "macros. You can also drag supported files anywhere onto "
                 "the window."),
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
                          "Import; export there, then use Import files… here. "
                          "Several files import at once, and dropping .pbin, "
                          ".bin, .psf or .mbin files anywhere on the window "
                          "imports them the same way.")
        transfer.setProperty("cardHint", "true")
        transfer.setWordWrap(True)
        lay.addWidget(transfer)

    # -- external -------------------------------------------------------------
    def set_profiles(self, profiles, active_id, sort_key="custom"):
        keep = self.selected_id()      # survive a refresh (e.g. after Rename)
        self._loading = True
        self._rules_by_pid = {p["id"]: [dict(r) for r in p.get("match_rules", [])]
                              for p in profiles}
        self.list.clear()
        active_row = keep_row = -1
        for p in profiles:
            it = QListWidgetItem(p["name"])
            it.setData(Qt.UserRole, p["id"])
            apps = self._app_names(p["id"])
            it.setToolTip(
                "Custom apps: " + ", ".join(apps) if apps
                else "No custom apps assigned (see Manage apps…)")
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
        self._update_apps_hint()
        self._sync_move_buttons()

    def selected_id(self):
        """The id of the highlighted list row (the management target), or None."""
        it = self.list.currentItem()
        return it.data(Qt.UserRole) if it is not None else None

    def show_active(self, pid):
        """Mark `pid` as the profile running on the mouse and select its row.

        Used by per-app auto-switch: opening a matched game must make this tab
        follow the switch, not keep showing the manual profile. The row is moved
        without emitting ``profile_selected`` (that would turn the switched
        profile into a new manual base for when auto-switch is turned off).
        """
        if not pid:
            return
        base = self.list.font()
        if base.pointSize() <= 0 and base.pixelSize() <= 0:
            base = QApplication.font()
        self._loading = True
        try:
            row = -1
            for i in range(self.list.count()):
                it = self.list.item(i)
                f = QFont(base)
                if it.data(Qt.UserRole) == pid:
                    f.setWeight(QFont.DemiBold)
                    row = i
                it.setFont(f)
            if row >= 0:
                if self.list.currentRow() != row:
                    self.list.setCurrentRow(row)
                self.list.scrollToItem(self.list.item(row))
        finally:
            self._loading = False
        self._update_apps_hint()

    def set_match_rules(self, pid, rules):
        """Update one profile's custom apps without rebuilding the whole list
        (the Manage Apps dialog just edited them; keep this tab in step)."""
        self._rules_by_pid[pid] = [dict(r) for r in rules]
        for i in range(self.list.count()):
            it = self.list.item(i)
            if it.data(Qt.UserRole) != pid:
                continue
            apps = self._app_names(pid)
            it.setToolTip(
                "Custom apps: " + ", ".join(apps) if apps
                else "No custom apps assigned (see Manage apps…)")
            break
        self._update_apps_hint()

    # -- custom-app summary ---------------------------------------------------
    def _app_names(self, pid):
        names = []
        for r in self._rules_by_pid.get(pid, []):
            label = (r.get("exe") or r.get("path") or r.get("title") or "").strip()
            if label and label not in names:
                names.append(label)
        return names

    def _update_apps_hint(self):
        pid = self.selected_id()
        item = self.list.currentItem()
        if not pid or item is None:
            self.apps_hint.setText("Select a profile to see its custom apps.")
            self.manage_apps_btn.setEnabled(False)
            return
        names = self._app_names(pid)
        if names:
            shown = ", ".join(names[:3])
            if len(names) > 3:
                shown += f" +{len(names) - 3} more"
            self.apps_hint.setText(
                f"Custom apps for {item.text()}: {shown}")
        else:
            self.apps_hint.setText(
                f"No custom apps for {item.text()}. Use Manage apps… to add the "
                "game(s) this profile should switch to.")
        self.manage_apps_btn.setEnabled(True)

    def _on_current_changed(self, *_):
        if self._loading:
            return
        self._update_apps_hint()
        self._sync_move_buttons()

    def _on_manage_apps(self):
        pid = self.selected_id()
        if pid:
            self.manage_apps_requested.emit(pid)

    def set_native_drop_mode(self, active):
        """Adapt to the elevated Windows drop bridge (no in-window OLE drags).

        When the app runs elevated Qt's drop target is revoked so Explorer can
        deliver file drops; that also disables drag-to-reorder, so the Move up
        / Move down buttons become the way to order profiles.
        """
        if active:
            self.list.setDragDropMode(QAbstractItemView.NoDragDrop)
            self.subtitle.setText(
                "Order sets auto-switch priority (first matching profile wins). "
                "This window runs as administrator, so reorder with Move up / "
                "Move down. Double-click to activate. The wired mouse stores up "
                "to 14 profiles.")
        else:
            self.list.setDragDropMode(QAbstractItemView.InternalMove)
            self.subtitle.setText(
                "Drag to reorder — order sets auto-switch priority (first "
                "matching profile wins). Double-click to activate. The wired "
                "mouse stores up to 14 profiles.")

    def move_selected(self, delta):
        """Move the highlighted profile one row (persists via order_changed)."""
        row = self.list.currentRow()
        target = row + int(delta)
        if row < 0 or not 0 <= target < self.list.count():
            return False
        self._loading = True
        try:
            item = self.list.takeItem(row)
            self.list.insertItem(target, item)
            self.list.setCurrentRow(target)
            self.list.scrollToItem(item)
        finally:
            self._loading = False
        # a manual move implies a custom order, exactly like a drag
        self.sort.blockSignals(True)
        self.sort.setCurrentIndex(0)
        self.sort.blockSignals(False)
        self._sync_move_buttons()
        self.order_changed.emit(self._ids_in_order())
        return True

    def _sync_move_buttons(self):
        row = self.list.currentRow()
        count = self.list.count()
        self.up_btn.setEnabled(row > 0)
        self.down_btn.setEnabled(0 <= row < count - 1)

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
                "files… to bring in .pbin, .bin or .psf profiles. You can "
                "also drag them onto the window.")
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
