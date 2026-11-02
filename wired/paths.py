"""Portable application paths for the wired studio build.

The app keeps its own copied data directory. It NEVER reads or writes the
original installation under Program Files: the only seed source is the
``seed/`` folder shipped beside the source (or beside the .exe when frozen).

Set ``SM809_DATA_DIR`` to override the data folder (used by the tests).
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent

if getattr(sys, "frozen", False):
    # A PyInstaller bundle imports this module from its temporary extraction
    # folder, so ``Path(__file__)`` is not the user's folder.  Keep the
    # writable data directory beside the .exe (it must survive restarts), and
    # read the read-only seeds from the bundle instead.
    APP_DIR = Path(sys.executable).resolve().parent
    BUNDLE_DIR = Path(getattr(sys, "_MEIPASS", APP_DIR))
else:
    BUNDLE_DIR = APP_DIR

DATA_DIR = Path(os.environ.get("SM809_DATA_DIR", APP_DIR / "data")).resolve()
DEVICE_DATA_DIR = DATA_DIR / "Data"
SEED_DIR = BUNDLE_DIR / "seed"

_DATA_FILES = ("Data.bin", "profile.bin", "Default.pbin", "macro.bin", "gun.bin")


def ensure_data_dir() -> Path:
    """Create the portable data folder and seed it once from ``seed/``."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DEVICE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    ini = DATA_DIR / "Data.ini"
    if not ini.exists():
        src = SEED_DIR / "Data.ini"
        if src.exists():
            shutil.copy2(src, ini)
    for name in _DATA_FILES:
        dst = DEVICE_DATA_DIR / name
        if not dst.exists():
            src = SEED_DIR / "Data" / name
            if src.exists():
                shutil.copy2(src, dst)
    return DATA_DIR


def logo_path() -> Path:
    return DATA_DIR / "logo.png"


def is_frozen() -> bool:
    """True when running from a PyInstaller-style frozen bundle."""
    return bool(getattr(sys, "frozen", False))
