"""
app.panels.app_picker -- choose a running application for a profile's
custom-app list, the way the NVIDIA Control Panel's program list works.

"Add app" on the Auto-Switch page opens this dialog, so the user picks the
program by name instead of typing exe/path/title fields. The dialog builds the
narrowest rule that still identifies the selection (see rule_for_app): usually
just the exe name, with the path or window title added only when another running
app shares the same exe.

`apps` is injectable so tests can run without enumerating the real desktop.
**Browse…** picks an .exe from disk for programs that are not running, building
the same kind of rule from the chosen path.
"""

import os

from PySide6.QtCore import QFileInfo, QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog, QFileDialog, QFileIconProvider, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QVBoxLayout,
)

from .. import theme
from ..autoswitch import list_running_apps, rule_for_app


class AppPicker(QDialog):
    def __init__(self, parent=None, apps=None):
        super().__init__(parent)
        self.setWindowTitle("Add app")
        self.setModal(True)
        self.resize(620, 500)
        self._apps = list(apps) if apps is not None else list_running_apps()
        self._icons = QFileIconProvider()
        self._last_dir = ""          # remembered while the dialog is open

        self.setStyleSheet(f"""
            QDialog {{ background: {theme.BG}; }}
            QLabel {{ color: {theme.TEXT_DIM}; }}
            QLineEdit {{
                background: {theme.SURFACE_2}; border: 1px solid {theme.BORDER};
                border-radius: 6px; padding: 7px 10px; color: {theme.TEXT};
            }}
            QListWidget {{
                background: {theme.SURFACE}; border: 1px solid {theme.BORDER};
                border-radius: 8px; outline: 0; padding: 4px;
            }}
            QListWidget::item {{ padding: 8px 10px; border-radius: 6px;
                color: {theme.TEXT_DIM}; }}
            QListWidget::item:hover {{ background: {theme.SURFACE_2}; color: {theme.TEXT}; }}
            QListWidget::item:selected {{ background: {theme.SURFACE_2};
                color: {theme.TEXT}; border-left: 2px solid {theme.ACCENT}; }}
            QPushButton {{ background: {theme.SURFACE_2};
                border: 1px solid {theme.BORDER}; border-radius: 6px;
                padding: 7px 16px; color: {theme.TEXT}; }}
            QPushButton:hover {{ border-color: {theme.TEXT_DIM}; }}
            QPushButton#ok {{ background: {theme.ACCENT};
                border: 1px solid {theme.ACCENT}; color: #1a1008;
                font-weight: 600; }}
            QPushButton#ok:hover {{ background: #ff7d4d; }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(10)

        title = QLabel("Choose a running app")
        title.setStyleSheet(
            f"color: {theme.TEXT}; font-size: 15px; font-weight: 600;")
        root.addWidget(title)
        hint = QLabel("Start the game or app first, then pick it here. The rule "
                      "follows that program whenever it is in front.")
        hint.setWordWrap(True)
        root.addWidget(hint)

        self.search = QLineEdit()
        self.search.setClearButtonEnabled(True)
        self.search.setPlaceholderText("Search running apps…")
        self.search.textChanged.connect(self._apply_filter)
        root.addWidget(self.search)

        self.list = QListWidget()
        self.list.setIconSize(QSize(22, 22))
        self.list.setSpacing(1)
        self.list.setTextElideMode(Qt.ElideRight)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list.itemDoubleClicked.connect(lambda *_: self._accept())
        self.list.currentItemChanged.connect(self._sync_ok)
        root.addWidget(self.list, 1)

        self.empty = QLabel("")
        self.empty.setWordWrap(True)
        self.empty.hide()
        root.addWidget(self.empty)

        footer = QHBoxLayout()
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.setToolTip("Look for running windows again")
        self.refresh_btn.clicked.connect(self._refresh)
        footer.addWidget(self.refresh_btn)
        self.browse_btn = QPushButton("Browse…")
        self.browse_btn.setToolTip(
            "Pick an application's .exe from disk — it does not need to be "
            "running")
        self.browse_btn.clicked.connect(self._browse)
        footer.addWidget(self.browse_btn)
        footer.addStretch(1)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        footer.addWidget(cancel)
        self.ok_btn = QPushButton("Add app")
        self.ok_btn.setObjectName("ok")
        self.ok_btn.clicked.connect(self._accept)
        footer.addWidget(self.ok_btn)
        root.addLayout(footer)

        self._populate()
        self.search.setFocus()

    # -- data -----------------------------------------------------------------
    def _icon(self, app):
        path = app.get("path")
        if path:
            info = QFileInfo(path)
            if info.exists():
                return self._icons.icon(info)
        return QIcon()

    def _label(self, app):
        return f"{app['title']}   ({app['exe']})"

    def _populate(self):
        self.list.clear()
        for app in self._apps:
            it = QListWidgetItem(self._icon(app), self._label(app))
            it.setData(Qt.UserRole, app)
            it.setToolTip(app.get("path") or app.get("exe") or "")
            self.list.addItem(it)
        if self.list.count():
            self.list.setCurrentRow(0)
        self._apply_filter(self.search.text())

    def _refresh(self):
        self._apps = list_running_apps()
        self._populate()

    def _browse(self):
        """Choose an .exe that is not running and add it straight away."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose an application", self._last_dir,
            "Applications (*.exe);;All files (*)")
        if not path:
            return
        self._last_dir = os.path.dirname(path)
        if self._add_path(path) is not None:
            self.accept()

    def _add_path(self, path):
        """Register a browsed exe (or reuse the running entry) and select it."""
        path = os.path.normpath(path)
        exe = os.path.basename(path).lower()
        if not exe:
            return None
        app = next(
            (a for a in self._apps
             if (a.get("exe") or "").lower() == exe
             and (a.get("path") or "").lower() == path.lower()), None)
        if app is None:
            app = {"title": os.path.splitext(os.path.basename(path))[0],
                   "exe": exe, "path": path}
            self._apps.append(app)
            self._populate()
        self.search.clear()
        self._select_app(app)
        return app

    def _select_app(self, app):
        for i in range(self.list.count()):
            it = self.list.item(i)
            a = it.data(Qt.UserRole) or {}
            if ((a.get("path") or "").lower()
                    == (app.get("path") or "").lower()
                    and (a.get("exe") or "").lower() == app.get("exe")):
                it.setHidden(False)
                self.list.setCurrentRow(i)
                self.list.scrollToItem(it)
                return

    def _apply_filter(self, text):
        needle = (text or "").strip().lower()
        visible = 0
        for i in range(self.list.count()):
            it = self.list.item(i)
            app = it.data(Qt.UserRole) or {}
            hay = f"{app.get('title','')} {app.get('exe','')}".lower()
            it.setHidden(bool(needle) and needle not in hay)
            if not it.isHidden():
                visible += 1
        if not self._apps:
            self.empty.setText(
                "No running windows found. Start the app, then press Refresh.")
        elif visible == 0:
            self.empty.setText(
                f"No running app matches “{text.strip()}”. Clear the search "
                "or press Refresh.")
        else:
            self.empty.setText("")
        self.empty.setVisible(visible == 0)
        self.list.setVisible(visible > 0)
        if self.list.currentItem() is not None and self.list.currentItem().isHidden():
            for i in range(self.list.count()):
                if not self.list.item(i).isHidden():
                    self.list.setCurrentRow(i)
                    break
        self._sync_ok()

    def _sync_ok(self, *_):
        it = self.list.currentItem()
        self.ok_btn.setEnabled(it is not None and not it.isHidden())

    # -- result ---------------------------------------------------------------
    def selected_app(self):
        it = self.list.currentItem()
        if it is None or it.isHidden():
            return None
        return it.data(Qt.UserRole)

    def selected_rule(self):
        """The match rule for the highlighted app, or None."""
        app = self.selected_app()
        if app is None:
            return None
        return rule_for_app(self._apps, app)

    def _accept(self):
        if self.selected_app() is not None:
            self.accept()
