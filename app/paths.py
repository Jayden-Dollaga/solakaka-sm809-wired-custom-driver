"""
app.paths -- frozen-aware filesystem paths.

Works both when run from source and when bundled by PyInstaller:

- `app_dir()` is where the app lives: the project root from source, or the
  folder containing the .exe when frozen.
- `data_dir()` is the single writable home for everything the studio keeps:
  the device tables (``Data/``) and the host-side library
  (``config/profiles.json``, ``config/macros.json``, ``config/guns.json``).
  Delete the whole folder and the next launch starts from the factory seed
  with default settings -- a true factory reset. Set ``SM809_DATA_DIR`` to use
  another folder (tests, demos, a second portable copy).
- `config_dir()` is the host-side library inside that data folder.
- `resource_path(*parts)` resolves a bundled READ-ONLY resource (e.g. images/),
  using PyInstaller's `sys._MEIPASS` extraction dir when frozen, else the project
  root.
"""

import os
import shutil
import sys

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The migration decision below needs to know whether data/ existed before this
# process created anything.  Older builds kept profiles.json / macros.json /
# guns.json in <app>/config, outside data/, so deleting data/ did not reset the
# studio.  The first launch after this change imports a legacy library into
# data/config -- but only if data/ existed before the launch.  A missing data/
# means the user deleted it on purpose, so migrating the old library back would
# defeat the reset.


def is_frozen():
    return bool(getattr(sys, "frozen", False))


def app_dir():
    if is_frozen():
        return os.path.dirname(os.path.abspath(sys.executable))
    return _PROJECT_ROOT


def data_dir():
    """The one writable folder: device tables + host-side library."""
    override = os.environ.get("SM809_DATA_DIR")
    if override:
        return os.path.abspath(override)
    return os.path.join(app_dir(), "data")


# Snapshot before any seeding: ensure_data_dir() creates data/ on first launch,
# and that creation must not look like "the user still had a data folder".
_DATA_EXISTED_AT_START = os.path.isdir(data_dir())


def config_dir():
    """Where profiles.json / macros.json / guns.json live.

    Always ``<data dir>/config`` so the host library is part of the same
    portable folder as the device tables and is removed by a factory reset.
    """
    return os.path.join(data_dir(), "config")


# Marker written into data/ once the legacy-folder question is settled for this
# data folder.  It closes the crash window between "factory reset detected" and
# the first profiles.json write, and makes deleting data/config later a real
# library reset instead of a re-import of the old folder.
_INIT_MARKER = ".config-initialized"


def _write_marker(marker, reason):
    try:
        os.makedirs(os.path.dirname(marker), exist_ok=True)
        with open(marker, "w", encoding="utf-8") as f:
            f.write(reason + "\n")
    except OSError:
        pass


def _migrate_legacy_config(legacy, target, data_existed, marker):
    """Copy an old <app>/config library into <data>/config exactly once.

    Returns the target path when files were copied, else None.  Kept free of
    globals so tests can exercise every branch with scratch folders.
    """
    if os.path.exists(marker):
        return None
    if not data_existed:
        # data/ was gone at launch: honour the reset and never look back.
        _write_marker(marker, "The data folder was deleted on purpose; "
                              "host settings start from factory defaults.")
        return None
    if os.path.isdir(target):
        # The data folder already owns a library (first launch after the
        # upgrade wrote it): the old folder must never overwrite it.
        _write_marker(marker, "Host settings already live in the data folder.")
        return None
    if os.path.abspath(legacy) == os.path.abspath(target):
        return None
    if not os.path.isdir(legacy):
        return None
    try:
        shutil.copytree(legacy, target)
    except OSError:
        # A half-written library is worse than starting clean: the stores
        # create their defaults when the files are absent.
        shutil.rmtree(target, ignore_errors=True)
        return None
    _write_marker(marker, "Imported the old config folder once; it is no "
                          "longer read after this point.")
    return target


def migrate_legacy_config():
    """One-time upgrade path for libraries written before the data change.

    Skipped when ``SM809_DATA_DIR`` is set: sandboxes and second portable
    copies must never import the real library.  The old folder is left in
    place as a manual backup; only a copy moves into the data folder.
    """
    if os.environ.get("SM809_DATA_DIR"):
        return None
    return _migrate_legacy_config(
        os.path.join(app_dir(), "config"),
        config_dir(),
        _DATA_EXISTED_AT_START,
        os.path.join(data_dir(), _INIT_MARKER),
    )


def resource_path(*parts):
    base = getattr(sys, "_MEIPASS", None) or _PROJECT_ROOT
    return os.path.join(base, *parts)
