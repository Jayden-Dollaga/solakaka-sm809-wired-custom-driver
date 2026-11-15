"""
app.panels.manage_apps_dialog -- the Manage Apps popup.

Per-app auto-switch used to be a page on the rail. Custom apps belong to one
profile at a time, so it now opens from the Profiles tab's "Manage apps…"
button as a dialog called **Manage Apps**. The dialog hosts the existing
AutoSwitchPanel (same rules, same signals) under that name.

The dialog is owned by MainWindow and reused: it keeps the foreground watcher
warm between openings, and the panel's show/hide events stop its polling timer
while the dialog is closed.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QHBoxLayout, QPushButton, QVBoxLayout,
)

from .. import theme
from .autoswitch_panel import AutoSwitchPanel

TITLE = "Manage Apps"
SUBTITLE = ("Choose the games and programs that switch to this profile "
            "automatically. Add an app while it is running — the first "
            "matching profile in list order wins.")


class ManageAppsDialog(QDialog):
    """Non-modal popup around the auto-switch rule editor."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(TITLE)
        self.setObjectName("manageAppsDialog")
        self.setModal(False)
        self.resize(780, 640)
        self.setMinimumSize(660, 520)
        # A normal top-level window: it can be moved aside while a game is
        # started for "Detect app", and stays open until the user closes it.
        self.setWindowFlag(Qt.Window, True)

        self.setStyleSheet(f"""
            QDialog {{ background: {theme.BG}; }}
            QPushButton {{
                background: {theme.SURFACE_2};
                border: 1px solid {theme.BORDER};
                border-radius: 6px;
                padding: 7px 16px;
                color: {theme.TEXT};
            }}
            QPushButton:hover {{ border-color: {theme.TEXT_DIM}; }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.panel = AutoSwitchPanel(title=TITLE, subtitle=SUBTITLE)
        root.addWidget(self.panel, 1)

        footer = QHBoxLayout()
        footer.setContentsMargins(28, 0, 28, 18)
        footer.addStretch(1)
        self.close_btn = QPushButton("Close")
        self.close_btn.setToolTip("Close Manage Apps (the settings are saved)")
        self.close_btn.clicked.connect(self.close)
        footer.addWidget(self.close_btn)
        root.addLayout(footer)

    def show_for(self, profiles, pid, enabled=None):
        """Show the dialog with `pid` selected in the profile list."""
        self.panel.set_profiles(profiles, pid)
        self.panel.select_profile(pid)
        if enabled is not None:
            self.panel.set_enabled_state(enabled)
        self.show()
        self.raise_()
        self.activateWindow()
