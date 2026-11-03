#!/usr/bin/env python3
"""
run_app.py -- launch the SM809 Wired Studio desktop app.

    python run_app.py            # normal launch (wired SM809), elevated like the driver
    python run_app.py --demo     # offline demo: no USB I/O, no elevation
    python run_app.py --no-elevate  # run this process without asking for admin

Single-instance: the app lives in the tray, so launching it again does NOT start
a second copy -- it signals the running instance to show its window and exits.
"""
import logging
import platform
import sys

from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtNetwork import QLocalServer, QLocalSocket

from app import theme
from app.logging_setup import setup_logging
from app.main_window import MainWindow, app_icon

_INSTANCE_KEY = "SM809WiredStudio_single_instance"


def _hand_off_if_running() -> bool:
    """If another instance is already running, tell it to show and return True."""
    sock = QLocalSocket()
    sock.connectToServer(_INSTANCE_KEY)
    if sock.waitForConnected(250):
        sock.write(b"show")
        sock.flush()
        sock.waitForBytesWritten(250)
        sock.disconnectFromServer()
        return True
    return False


def _listen_for_relaunch(win) -> QLocalServer:
    """Become the primary instance: listen so a future launch can raise our
    window instead of starting a new copy."""
    QLocalServer.removeServer(_INSTANCE_KEY)   # clear any stale socket
    server = QLocalServer()
    server.listen(_INSTANCE_KEY)

    def _on_new_connection():
        conn = server.nextPendingConnection()
        if conn is not None:
            conn.readAll()
            conn.disconnectFromServer()
        # restore from tray + bring to the foreground
        if hasattr(win, "_show_from_tray"):
            win._show_from_tray()
        else:
            win.showNormal()
            win.raise_()
            win.activateWindow()

    server.newConnection.connect(_on_new_connection)
    return server


def main():
    # Same privilege level as the official driver: a source run relaunches
    # itself elevated (the packaged exe asks through its manifest). --demo and
    # --no-elevate skip this; declining UAC keeps going with a warning.
    from app.elevation import prepare_startup
    if not prepare_startup(sys.argv[1:]):
        return

    # Diagnostics first: Qt's own warnings (and anything that fails during
    # startup) should land in logs/studio.log, not a bare stderr line.
    verbose = ("--verbose" in sys.argv or "-v" in sys.argv)
    log_path = setup_logging(verbose=verbose)
    # Stream the same records into the optional in-app log panel.
    from app.log_bridge import install as install_log_bridge
    install_log_bridge(logging.DEBUG if verbose else logging.INFO)
    log = logging.getLogger("sm809.app")
    demo = "--demo" in sys.argv
    log.info("SM809 Wired Studio starting (demo=%s)", demo)
    log.info("python %s | %s", platform.python_version(), platform.platform())
    from app.paths import app_dir, config_dir
    log.info("app dir: %s", app_dir())
    log.info("profile config: %s", config_dir())
    if log_path:
        log.info("diagnostics: %s", log_path)

    # crisp rendering on high-dpi displays
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    app.setApplicationName("SM809 Wired Studio")
    app.setWindowIcon(app_icon())

    # if we're a second launch, surface the running instance and quit
    if _hand_off_if_running():
        return

    pal = theme.dark_palette()
    if pal is not None:
        app.setPalette(pal)
    app.setStyleSheet(theme.stylesheet())

    # Qt's first widget/style warm-up can take a couple of seconds on Windows;
    # show a splash so startup never looks frozen.
    splash_pm = QPixmap(380, 110)
    splash_pm.fill(QColor(theme.BG))
    splash = QSplashScreen(splash_pm)
    splash.showMessage("SM809 Wired Studio\nStarting\u2026",
                       Qt.AlignCenter, QColor(theme.ACCENT))
    splash.show()
    app.processEvents()

    # --demo keeps every write in memory/on disk only; no USB traffic happens.
    # --verbose switches to manual apply: edits reach the mouse only when the
    # top-bar Apply button is clicked (vendor-driver behaviour, for debugging).
    win = MainWindow(demo=demo, verbose=verbose)
    win._single_instance_server = _listen_for_relaunch(win)   # keep a reference
    # --minimized / --tray (used by "Start with Windows"): stay in the tray on
    # launch. Only honoured when a tray exists, else show so it's not unreachable.
    minimized = ("--minimized" in sys.argv or "--tray" in sys.argv)
    if minimized and getattr(win, "tray", None) is not None:
        splash.close()
        win.tray.showMessage("SM809 Wired Studio", "Running in the tray.",
                             win.tray.MessageIcon.Information, 2000)
    else:
        win.show()
        splash.finish(win)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
