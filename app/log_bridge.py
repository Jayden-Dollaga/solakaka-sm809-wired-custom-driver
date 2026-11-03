"""
app.log_bridge -- stream the studio's Python log into the GUI.

The log panel is optional and can be closed at any time, but the bridge stays
installed so reopening the panel shows a history instead of only new lines.
Records from worker threads are forwarded with a Qt signal, which Qt delivers
on the GUI thread.

``install()`` is idempotent: calling it from run_app (to capture startup lines)
and again from the panel is safe.
"""

from __future__ import annotations

import logging
from collections import deque

from PySide6.QtCore import QObject, Signal

_RECENT_LINES = 1500
_installed = False


class LogBridge(QObject):
    """Singleton messenger between logging handlers and the log panel."""

    record = Signal(str)

    _instance = None

    def __init__(self):
        super().__init__()
        self._recent = deque(maxlen=_RECENT_LINES)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = LogBridge()
        return cls._instance

    def publish(self, text):
        self._recent.append(text)
        self.record.emit(text)

    def recent(self):
        """Lines logged before a panel existed (oldest first)."""
        return list(self._recent)


class _BridgeHandler(logging.Handler):
    """Format a record and push it to the GUI bridge."""

    def emit(self, record):
        try:
            text = self.format(record)
            LogBridge.instance().publish(text)
        except Exception:       # never let logging break the app
            pass


def install(level=logging.INFO):
    """Attach the GUI bridge to the studio and Qt loggers once.

    ``--verbose`` passes DEBUG so the panel mirrors the console detail; the
    log file always keeps full DEBUG either way.
    """
    global _installed
    if _installed:
        return
    fmt = logging.Formatter(
        "%(asctime)s %(levelname)-7s %(message)s", datefmt="%H:%M:%S")

    studio = _BridgeHandler()
    studio.setLevel(level)
    studio.setFormatter(fmt)
    logging.getLogger("sm809").addHandler(studio)

    # Qt's own warnings are useful, but its debug chatter is not.
    qt = _BridgeHandler()
    qt.setLevel(logging.WARNING)
    qt.setFormatter(fmt)
    logging.getLogger("qt").addHandler(qt)

    _installed = True
