"""Import-file detection and app-wide drag-and-drop routing.

The studio accepts exactly the files its importers can read:

* ``.pbin`` and ``.psf`` -- one wired profile record (``ProfileStore``);
* ``.mbin`` -- one vendor macro record (``app.macro_file``);
* ``.bin`` -- the vendor's headerless container name, classified by size:
  a full profile table record (>= ``PROFILE_SIZE``) or one/several macro
  records (a positive multiple of ``MACRO_SIZE``).

Anything else is ignored rather than treated as an error, so dropping a whole
folder cannot produce a wall of warnings.

The event filter only reacts to drags carrying local file URLs; the Profiles
list's internal row reorder (an abstract-item-model drag) therefore passes
straight through to the list.
"""

from __future__ import annotations

import os
import time

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtWidgets import QApplication, QWidget

from wired.model import MACRO_SIZE, PROFILE_SIZE

PROFILE_SUFFIXES = (".pbin", ".psf")
MACRO_SUFFIXES = (".mbin",)

PROFILE_FILTER = "Profiles (*.pbin *.bin *.psf)"
MACRO_FILTER = "Macros (*.mbin)"
ALL_SUPPORTED_FILTER = "Supported files (*.pbin *.bin *.psf *.mbin)"


def unique_paths(paths):
    """Absolute, de-duplicated local paths.

    Windows paths are case-insensitive, and dropping the same file twice (or
    selecting it twice through two extensions) must import it only once.
    """
    if isinstance(paths, (str, os.PathLike)):
        paths = [paths]
    out = []
    seen = set()
    for raw in paths or ():
        try:
            path = os.path.abspath(os.fspath(raw))
        except (TypeError, ValueError):
            continue
        key = os.path.normcase(path)
        if key in seen:
            continue
        seen.add(key)
        out.append(path)
    return out


def classify_path(path):
    """Return ``"profile"``, ``"macro"`` or ``None`` for one local file.

    ``.bin`` has no metadata to identify it, so its size decides: a full
    profile record first, then whole macro records.  Vendor ``macro.bin``
    (2 x 0x358) and ``profile.bin`` (0x1CC50) both classify correctly.
    """
    try:
        path = os.path.abspath(os.fspath(path))
        if not os.path.isfile(path):
            return None
        ext = os.path.splitext(path)[1].casefold()
        if ext in PROFILE_SUFFIXES:
            return "profile"
        if ext in MACRO_SUFFIXES:
            return "macro"
        if ext != ".bin":
            return None
        size = os.path.getsize(path)
    except (OSError, TypeError, ValueError):
        return None
    if size >= PROFILE_SIZE:
        return "profile"
    if size >= MACRO_SIZE and size % MACRO_SIZE == 0:
        return "macro"
    return None


def split_paths(paths):
    """Classify a batch into ``(profiles, macros, ignored_paths)``."""
    profiles, macros, ignored = [], [], []
    for path in unique_paths(paths):
        kind = classify_path(path)
        if kind == "profile":
            profiles.append(path)
        elif kind == "macro":
            macros.append(path)
        else:
            ignored.append(path)
    return profiles, macros, ignored


def supported_hint():
    """One short sentence for dialogs and UI hints."""
    return ".pbin, .bin and .psf profiles, or .mbin macros"


def file_names(paths, limit=None):
    """Base names for a summary, optionally collapsed to ``limit`` rows."""
    names = [os.path.basename(path) for path in paths]
    if limit is not None and len(names) > limit:
        names = names[:limit] + [f"…and {len(names) - limit} more"]
    return names


class FileDropRouter(QObject):
    """Accept supported import files dropped anywhere on a studio window.

    MainWindow installs one filter on the QApplication.  ``files_dropped``
    carries every local path in the drop; the window classifies the batch and
    reports per-file results, so a mixed drop still imports what it can.
    """

    files_dropped = Signal(list)

    def __init__(self, window):
        super().__init__(window)
        self._window = window
        self._app = QApplication.instance()
        self._drag_key = None
        self._drag_ok = False
        # A global filter can be bypassed by Qt's drag manager for some
        # receivers, so every surface of the window also filters the drag
        # itself.  A repeated drop event is emitted once (see ``_emit_once``).
        self._targets = [window]
        if self._app is not None:
            self._app.installEventFilter(self)
        window.setAcceptDrops(True)
        window.installEventFilter(self)
        for child in window.findChildren(QWidget):
            child.setAcceptDrops(True)
            child.installEventFilter(self)
            self._targets.append(child)
        self._last_drop = (None, 0.0)

    def uninstall(self):
        """Detach from the application and widgets (tests / window disposal)."""
        if self._app is not None:
            self._app.removeEventFilter(self)
        for widget in self._targets:
            try:
                widget.removeEventFilter(self)
            except RuntimeError:
                pass        # the C++ widget is already gone
        self._targets = []

    def _emit_once(self, paths):
        """Emit a drop once even when both the global and widget filters see it."""
        key = tuple(paths)
        last_key, last_at = self._last_drop
        now = time.monotonic()
        if key == last_key and now - last_at < 0.5:
            return False
        self._last_drop = (key, now)
        self.files_dropped.emit(paths)
        return True

    def offer(self, paths):
        """Route paths that arrived outside Qt's drag system (WM_DROPFILES).

        The elevated Windows bridge hands over plain paths; they get the same
        classification as a real drop, and a drop with nothing recognisable is
        ignored instead of opening an empty summary.
        """
        paths = unique_paths([p for p in paths if p])
        if not paths or not any(classify_path(path) for path in paths):
            return False
        return self._emit_once(paths)

    def _owns(self, obj):
        """True for the main window and its non-modal dialogs (Manage Apps)."""
        try:
            win = obj.window()
        except AttributeError:
            return False
        if win is self._window:
            return True
        return (isinstance(win, QWidget)
                and win.parentWidget() is self._window
                and not bool(getattr(win, "isModal", lambda: False)()))

    @staticmethod
    def _paths(event):
        mime = event.mimeData()
        if mime is None or not mime.hasUrls():
            return []
        local = [url.toLocalFile() for url in mime.urls() if url.isLocalFile()]
        return unique_paths(local)

    def eventFilter(self, obj, event):
        kind = event.type()
        if kind not in (QEvent.DragEnter, QEvent.DragMove, QEvent.Drop):
            return False
        if not self._owns(obj):
            return False

        paths = self._paths(event)
        if not paths:
            # No local files: internal list reorder, plain text or a remote
            # URL.  Leave the event to the widget under the cursor.
            return False

        if kind == QEvent.Drop:
            if not any(classify_path(path) for path in paths):
                return False
            event.setDropAction(Qt.CopyAction)
            event.accept()
            self._emit_once(paths)
            return True

        key = tuple(paths)
        if kind == QEvent.DragEnter or key != self._drag_key:
            self._drag_key = key
            self._drag_ok = any(classify_path(path) for path in paths)
        if not self._drag_ok:
            return False
        event.setDropAction(Qt.CopyAction)
        event.accept()
        return True
