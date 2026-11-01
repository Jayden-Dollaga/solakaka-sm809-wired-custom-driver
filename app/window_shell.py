"""Application window composition: status bar, navigation rail, and pages."""

from collections.abc import Callable, Sequence

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QFrame, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QStackedWidget, QVBoxLayout, QWidget,
)


class AppShell(QWidget):
    def __init__(
        self,
        topbar: QWidget,
        profile_bar: QWidget,
        nav_items: Sequence[str],
        panels: Sequence[QWidget],
        on_navigate: Callable[[int], None],
        on_reset: Callable[[], None],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("root")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)
        outer.addWidget(topbar)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        outer.addLayout(body, 1)

        rail = QFrame()
        rail.setObjectName("railFrame")
        rail.setFixedWidth(180)
        rail.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        rail_layout = QVBoxLayout(rail)
        rail_layout.setContentsMargins(0, 0, 0, 0)
        rail_layout.setSpacing(0)
        rail_layout.addWidget(profile_bar)

        self.nav = QListWidget()
        self.nav.setObjectName("nav")
        self.nav.setFrameShape(QFrame.NoFrame)
        for name in nav_items:
            QListWidgetItem(name, self.nav)
        self.nav.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nav.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nav.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.nav.setSelectionMode(QAbstractItemView.SingleSelection)
        rail_layout.addWidget(self.nav, 0)
        rail_layout.addStretch(1)

        separator = QFrame()
        separator.setProperty("sep", "true")
        separator.setFrameShape(QFrame.NoFrame)
        rail_layout.addWidget(separator)
        rail_layout.addSpacing(10)

        self.reset_btn = QPushButton("Reset to Factory")
        self.reset_btn.setObjectName("resetBtn")
        self.reset_btn.clicked.connect(on_reset)
        rail_layout.addWidget(self.reset_btn, 0)
        rail_layout.addSpacing(14)
        body.addWidget(rail)

        self.stack = QStackedWidget()
        for panel in panels:
            self.stack.addWidget(panel)
        body.addWidget(self.stack, 1)

        self._fit_nav_height()
        self.nav.setCurrentRow(0)
        self.nav.currentRowChanged.connect(on_navigate)

    def _fit_nav_height(self) -> None:
        """Set the nav list's height to exactly fit all rows."""
        count = self.nav.count()
        if count == 0:
            return
        row_height = self.nav.sizeHintForRow(0)
        if row_height <= 0:
            row_height = 40
        self.nav.setFixedHeight(row_height * count + 20)