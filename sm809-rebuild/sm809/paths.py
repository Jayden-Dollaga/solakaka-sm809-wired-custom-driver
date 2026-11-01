"""Portable application paths.

The rebuild keeps its own data directory so the original installation is never
modified. On first launch it seeds itself from ../Data.ini and ../Data/*.bin
when those files exist.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.environ.get("SM809_DATA_DIR", APP_DIR / "data")).resolve()
DEVICE_DATA_DIR = DATA_DIR / "Data"


def ensure_data_dir(original_root: Path | None = None) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DEVICE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    if original_root is None:
        original_root = APP_DIR.parent
    ini = DATA_DIR / "Data.ini"
    if not ini.exists():
        src = original_root / "Data.ini"
        if src.exists():
            shutil.copy2(src, ini)
    for name in ("Data.bin", "profile.bin", "Default.pbin", "macro.bin", "gun.bin"):
        dst = DEVICE_DATA_DIR / name
        if not dst.exists():
            src = original_root / "Data" / name
            if src.exists():
                shutil.copy2(src, dst)
    return DATA_DIR


def logo_path() -> Path:
    return DATA_DIR / "logo.png"
