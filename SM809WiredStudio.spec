# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for a portable, single-file SM809 Wired Studio.

Build from this folder with:

    pip install pyinstaller
    python -m PyInstaller --noconfirm SM809WiredStudio.spec

The result is ``dist/SM809WiredStudio.exe``.  At runtime the exe keeps its
writable ``data/``, ``config/`` and ``logs/`` folders beside itself; the
read-only ``images/`` tree and the clean factory seed are bundled inside the
exe.

Only ``seed/Data`` is bundled -- never the developer's ``data/``, ``config/``
or ``backups/`` folders, and never the vendor's sample profile library.  A
first launch therefore starts with exactly one default profile, built from
``seed/Data/Default.pbin``.
"""

from pathlib import Path

project_root = Path(SPECPATH)

datas = [
    (str(project_root / "images"), "images"),
    (str(project_root / "seed" / "Data"), "seed/Data"),
    (str(project_root / "seed" / "Data.ini"), "seed"),
]

a = Analysis(
    [str(project_root / "run_app.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter"],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="SM809WiredStudio",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / "images" / "icon.ico"),
)
