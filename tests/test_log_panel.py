"""The in-app live log panel: streaming, history, clear, and close."""

import logging

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from app import theme
from app.log_bridge import install
from app.widgets.log_panel import LogPanel


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    app.setStyleSheet(theme.stylesheet())
    yield app
    for widget in list(app.topLevelWidgets()):
        widget.close()
        widget.deleteLater()
    app.processEvents()
    app.quit()


def _log(msg):
    # WARNING guarantees the record passes the default root level.
    logging.getLogger("sm809.autoswitch").warning(msg)


def test_log_panel_streams_new_records(qapp):
    install()
    panel = LogPanel()
    panel.start()
    panel.show()
    try:
        _log("probe-live-123")
        qapp.processEvents()
        assert "probe-live-123" in panel.view.toPlainText()
    finally:
        panel.close()


def test_log_panel_backfills_records_from_before_it_opened(qapp):
    install()
    _log("probe-history-456")
    panel = LogPanel()
    panel.start()
    try:
        assert "probe-history-456" in panel.view.toPlainText()
    finally:
        panel.close()


def test_log_panel_clear_and_close(qapp):
    install()
    panel = LogPanel()
    panel.start()
    panel.show()
    try:
        _log("probe-clear-789")
        qapp.processEvents()
        assert "probe-clear-789" in panel.view.toPlainText()

        panel.clear_btn.click()
        assert panel.view.toPlainText() == ""

        closed = []
        panel.close_requested.connect(lambda: closed.append(True))
        panel.close_btn.click()
        assert closed == [True]
    finally:
        panel.close()
