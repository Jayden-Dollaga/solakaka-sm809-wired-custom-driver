"""
app.widgets.log_panel -- the studio's live, closable log view.

The panel mirrors the same records that go to ``logs/studio.log`` and the
console. It is deliberately passive: closing it only hides the panel (the
bridge keeps a short history), and the top-bar **Log** button brings it back.
"""

from __future__ import annotations

import os

from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QTextCursor
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QSizePolicy,
    QVBoxLayout,
)

from ..log_bridge import LogBridge, install
from ..logging_setup import log_file_path


class LogPanel(QFrame):
    """A bottom-docked view of the live log with Clear / Open / Close."""

    close_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("logPanel")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 10)
        lay.setSpacing(6)

        head = QHBoxLayout()
        head.setSpacing(8)
        title = QLabel("LIVE LOG")
        title.setObjectName("logTitle")
        head.addWidget(title)
        head.addStretch(1)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setObjectName("logTool")
        self.clear_btn.setToolTip("Clear the panel (the log file is untouched)")
        self.clear_btn.clicked.connect(self.clear)
        head.addWidget(self.clear_btn)

        self.open_btn = QPushButton("Open log file")
        self.open_btn.setObjectName("logTool")
        self.open_btn.setToolTip(log_file_path())
        self.open_btn.clicked.connect(self.open_log_file)
        head.addWidget(self.open_btn)

        self.close_btn = QPushButton("\u00d7")
        self.close_btn.setObjectName("logClose")
        self.close_btn.setFixedWidth(26)
        self.close_btn.setToolTip("Close the log panel (turn it back on in Settings)")
        self.close_btn.clicked.connect(lambda: self.close_requested.emit())
        head.addWidget(self.close_btn)
        lay.addLayout(head)

        self.view = QPlainTextEdit()
        self.view.setObjectName("logView")
        self.view.setReadOnly(True)
        self.view.setUndoRedoEnabled(False)
        self.view.setMaximumBlockCount(3000)
        self.view.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.view.setMinimumHeight(80)
        self.view.setPlaceholderText("No log lines yet.")
        self.view.setFocusPolicy(Qt.NoFocus)
        lay.addWidget(self.view, 1)

        install()
        self._started = False

    def start(self):
        """Connect the live stream and backfill what happened before opening."""
        if self._started:
            return
        self._started = True
        bridge = LogBridge.instance()
        recent = bridge.recent()
        for line in recent:
            self.view.appendPlainText(line)
        if recent:
            self.view.moveCursor(QTextCursor.End)
        bridge.record.connect(self._append)

    def showEvent(self, event):
        self.start()
        super().showEvent(event)

    def _append(self, text):
        bar = self.view.verticalScrollBar()
        at_bottom = bar.value() >= bar.maximum() - 4
        self.view.appendPlainText(text)
        if at_bottom:
            bar.setValue(bar.maximum())

    def clear(self):
        self.view.clear()

    def open_log_file(self):
        """Open studio.log, or its folder when this build could not create it."""
        path = log_file_path()
        target = path if os.path.exists(path) else os.path.dirname(path)
        if os.path.exists(target):
            QDesktopServices.openUrl(QUrl.fromLocalFile(target))
