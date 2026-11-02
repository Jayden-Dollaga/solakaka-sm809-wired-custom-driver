"""app.logging_setup -- useful diagnostics for the studio.

The first build printed a handful of ``[sm809] ...`` lines and nothing else:
no timestamps, no levels, no file, and the same warning repeated on every
apply.  When the lighting tab left the mouse unresponsive there was nothing
to look at afterwards, because every HID write had "succeeded" -- the
firmware wedged on the *value*, not on an I/O error.

This module gives the app:

- a concise console at INFO (``--verbose`` switches it to DEBUG) where
  identical consecutive lines collapse into one ``previous message repeated``
  note instead of scrolling the terminal,
- a rotating DEBUG log at ``<app dir>/logs/studio.log`` (2 MB x 3) with
  timestamps, levels, thread names and full tracebacks,
- crash hooks for the UI thread and worker threads, and
- Qt's own warnings routed into the same file (the benign
  ``QFont::setPointSize`` chatter is demoted to DEBUG).

Call ``setup_logging()`` once, before creating the QApplication.
"""

from __future__ import annotations

import logging
import logging.handlers
import os
import sys
import tempfile
import threading

from . import paths

_LOG_NAME = "sm809"
_FILE_NAME = "studio.log"
_MAX_BYTES = 2_000_000
_BACKUP_COUNT = 3

_OWNED = "_sm809_owned"
_hooks_installed = False
_qt_installed = False


class RepeatCollapsingHandler(logging.StreamHandler):
    """Console handler that folds identical consecutive records.

    A slider drag or a reconnect loop can repeat one warning dozens of times.
    The first line is printed, subsequent identical ones are counted, and a
    single ``previous message repeated N more times`` line is written before
    the next different message (or at shutdown).
    """

    def __init__(self, stream=None):
        super().__init__(stream)
        self._last_key = None
        self._last_record = None
        self._repeats = 0

    def emit(self, record: logging.LogRecord) -> None:
        try:
            key = (record.levelno, record.getMessage())
        except Exception:  # pragma: no cover - defensive
            key = None
        if key is not None and key == self._last_key:
            self._repeats += 1
            self._last_record = record
            return
        self._flush_repeats()
        self._last_key = key
        self._last_record = record
        super().emit(record)

    def _flush_repeats(self) -> None:
        if not self._repeats or self._last_record is None:
            return
        count = self._repeats
        self._repeats = 0
        record = logging.LogRecord(
            self._last_record.name,
            self._last_record.levelno,
            self._last_record.pathname,
            self._last_record.lineno,
            "  ... previous message repeated %d more time%s",
            (count, "" if count == 1 else "s"),
            None,
        )
        # Keep the timestamp of the repeated message, not of the summary.
        record.created = self._last_record.created
        record.msecs = self._last_record.msecs
        record.relativeCreated = self._last_record.relativeCreated
        try:
            self.stream.write(self.format(record) + self.terminator)
            self.stream.flush()
        except Exception:
            # The console can already be closed during interpreter shutdown;
            # a failed summary line must not print a logging traceback.
            pass

    def flush(self) -> None:
        # StreamHandler.emit() flushes after every record, so this must not
        # clear _last_key: that would make every repeat look like a new line.
        self._flush_repeats()
        super().flush()


def default_log_dir() -> str:
    """``<app dir>/logs``, or a temp folder when that is not writable."""
    primary = os.path.join(paths.app_dir(), "logs")
    try:
        os.makedirs(primary, exist_ok=True)
        probe = os.path.join(primary, ".write-test")
        with open(probe, "w", encoding="ascii") as fh:
            fh.write("ok")
        os.remove(probe)
        return primary
    except OSError:
        fallback = os.path.join(tempfile.gettempdir(), "sm809-wired-studio-logs")
        os.makedirs(fallback, exist_ok=True)
        return fallback


def _console_handler(verbose: bool) -> logging.Handler:
    handler = RepeatCollapsingHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)-7s %(message)s", datefmt="%H:%M:%S"))
    setattr(handler, _OWNED, True)
    return handler


def _file_handler(directory: str) -> logging.Handler | None:
    try:
        os.makedirs(directory, exist_ok=True)
        handler = logging.handlers.RotatingFileHandler(
            os.path.join(directory, _FILE_NAME),
            maxBytes=_MAX_BYTES,
            backupCount=_BACKUP_COUNT,
            encoding="utf-8",
        )
    except OSError:
        return None
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s.%(msecs)03d %(levelname)-7s [%(threadName)s] "
        "%(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"))
    setattr(handler, _OWNED, True)
    return handler


def setup_logging(
    verbose: bool = False,
    log_dir: str | None = None,
    *,
    install_hooks: bool = True,
    install_qt: bool = True,
) -> str | None:
    """Install the studio's handlers.  Safe to call more than once.

    ``install_hooks`` / ``install_qt`` exist so tests can exercise the file
    and console output without replacing process-wide exception handlers.
    Returns the log-file path (``None`` if the file could not be opened).
    """
    root = logging.getLogger(_LOG_NAME)
    for handler in list(root.handlers):
        if getattr(handler, _OWNED, False):
            root.removeHandler(handler)
            try:
                handler.close()
            except Exception:
                pass

    root.setLevel(logging.DEBUG)
    root.addHandler(_console_handler(verbose))

    directory = log_dir or default_log_dir()
    file_handler = _file_handler(directory)
    path = None
    if file_handler is not None:
        root.addHandler(file_handler)
        path = os.path.join(directory, _FILE_NAME)

    if install_hooks:
        _install_excepthooks()
    if install_qt:
        _install_qt_handler()
    return path


# -- crash reporting ---------------------------------------------------------
def _install_excepthooks() -> None:
    global _hooks_installed
    if _hooks_installed:
        return
    _hooks_installed = True
    crash = logging.getLogger(f"{_LOG_NAME}.crash")

    def excepthook(exc_type, exc, tb):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc, tb)
            return
        crash.critical("uncaught exception", exc_info=(exc_type, exc, tb))
        sys.__excepthook__(exc_type, exc, tb)

    def thread_excepthook(args):
        if args.exc_type is SystemExit:
            return
        name = args.thread.name if args.thread is not None else "?"
        crash.critical(
            "uncaught exception in thread %s", name,
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )
        threading.__excepthook__(args)

    sys.excepthook = excepthook
    threading.excepthook = thread_excepthook


# -- Qt messages -------------------------------------------------------------
def _install_qt_handler() -> None:
    """Send Qt's own warnings to the log instead of a bare stderr line."""
    global _qt_installed
    if _qt_installed:
        return
    try:
        from PySide6.QtCore import QtMsgType, qInstallMessageHandler
    except Exception:
        return

    qt_log = logging.getLogger("qt")

    def handler(mode, context, message):
        if "QFont::setPointSize" in message:
            # Harmless: Qt resolving a stylesheet font before a screen exists.
            level = logging.DEBUG
        elif mode == QtMsgType.QtDebugMsg:
            level = logging.DEBUG
        elif mode == QtMsgType.QtInfoMsg:
            level = logging.INFO
        elif mode == QtMsgType.QtWarningMsg:
            level = logging.WARNING
        else:
            level = logging.ERROR
        qt_log.log(level, "%s", message)

    qInstallMessageHandler(handler)
    _qt_installed = True
