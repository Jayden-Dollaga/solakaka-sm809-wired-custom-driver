# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build definition for **SM809 Wired Studio**.

SM809 Wired Studio is a portable, single-file PySide6 desktop application for
the wired SOLAKAKA SM809 gaming mouse (VID ``0x04D9`` / PID ``0xA09F``).  It
reads and writes the vendor's own binary profile table and exposes the complete
vendor feature set plus per-app auto-switching, a recoil-pattern (Gun) editor
and a live in-app log.

Build
-----
From this folder (the folder that contains this spec):

    python -m pip install PySide6 pyinstaller
    python -m PyInstaller --noconfirm --clean SM809WiredStudio.spec

``build_exe.bat`` wraps the same command, refuses to run while the studio is
open, and also clears the working ``build\\``, ``dist\\`` and ``data\\`` folders
so a release build never contains a developer's profiles.

Result
------
``dist/SM809WiredStudio.exe`` - one self-contained windowed executable with an
embedded ``requireAdministrator`` manifest and the application icon.  The first
start takes a few seconds while PyInstaller unpacks the bundle to a temporary
folder; later starts are faster.

What is bundled (read-only, extracted to ``sys._MEIPASS``)
---------------------------------------------------------
``images/icon.ico``
    Window, taskbar, tray and Explorer icon.
``images/mouse.png``
    Numbered reference artwork on the Buttons page.
``images/check.png``
    Check mark used by the themed checkboxes/radios.
``seed/Data.ini``
    Device configuration (sensor, button defaults, no password, Distance=0).
``seed/Data/Data.bin``
    Device state/selection record.
``seed/Data/Default.pbin``
    Factory profile template (``0x1CC50`` bytes) used by "Reset to Factory".
``seed/Data/profile.bin``
    The initial single-profile table copied into ``data/Data/`` on first run.
``seed/Data/macro.bin``
    Factory macro table (2 records).
``seed/Data/gun.bin``
    Factory gun table (empty).

What is *not* bundled
---------------------
- The developer's ``data/``, ``config/``, ``logs/`` and ``backups/`` folders.
  They are created beside the exe at runtime and survive moving/upgrading it.
- The vendor's sample profile library, the original installation under
  ``C:\\Program Files (x86)\\SM809 mouse Software`` and anything in it.
- ``tests/``, ``analysis/``, ``.venv/`` and the build folders.
- The unused root ``seed/Data.bin`` / ``seed/profile.bin`` files; the app only
  seeds from ``seed/Data.ini`` and ``seed/Data/*`` (see ``wired/paths.py``).

Runtime layout (portable, beside the exe)
-----------------------------------------
    SM809WiredStudio.exe
    data/
      Data.ini
      Data/{Data,profile,Default,macro,gun}.bin
    config/
      profiles.json    profile metadata, match rules, app settings + mirror
      macros.json      named macro library
      guns.json        named recoil-pattern library
    logs/
      studio.log       rotating 2 MB x 4 files, DEBUG by default

``SM809_DATA_DIR`` relocates both ``data/`` and ``config/`` for a fully isolated
portable copy.  ``SM809_ELEVATION_TRIED=1`` is an internal loop guard.

Parent process / single instance
--------------------------------
The app is tray-based and single-instance: the exe listens on the local socket
``SM809WiredStudio_single_instance``; a second launch asks the running copy to
show its window and exits.  Nothing in the bundle is written at runtime.
"""

from pathlib import Path

project_root = Path(SPECPATH)

# ---------------------------------------------------------------------------
# Read-only resources copied into the bundle.
#
# Seed files are kept as explicit entries rather than whole folders so that a
# stray file in ``seed/`` can never ship inside a release.  Update this list if
# the device-data set changes.
# ---------------------------------------------------------------------------
_RESOURCES = {
    "images/icon.ico": "images",
    "images/mouse.png": "images",
    "images/check.png": "images",
    "seed/Data.ini": "seed",
    "seed/Data/Data.bin": "seed/Data",
    "seed/Data/Default.pbin": "seed/Data",
    "seed/Data/profile.bin": "seed/Data",
    "seed/Data/macro.bin": "seed/Data",
    "seed/Data/gun.bin": "seed/Data",
}

_missing = [rel for rel in _RESOURCES if not (project_root / rel).is_file()]
if _missing:
    raise SystemExit(
        "SM809WiredStudio.spec: required resource(s) are missing:\n  "
        + "\n  ".join(_missing)
    )

datas = [(str(project_root / rel), dest) for rel, dest in _RESOURCES.items()]

# ---------------------------------------------------------------------------
# Python side.
#
# Every application module is imported statically from ``run_app.py``:
#   run_app -> app.main_window -> app.controller -> wired.device
#                                -> app.profile_store -> wired.model / bridge
#                                -> every app.panels.* and app.widgets.*
#   run_app -> app.elevation / app.logging_setup / app.log_bridge / app.paths
#   app.panels.performance_panel -> wired.wheel_direction
# so the dependency graph needs no hidden imports.  ``sm809pro`` and ``wired``
# are ordinary packages on ``pathex``.
#
# ``binaries`` stays empty: HID access is implemented with ctypes against the
# Windows ``hid.dll`` / SetupAPI, with no third-party HID extension module.
# Qt's own DLLs and platform plugins are collected by PyInstaller's PySide6
# hooks.  ``tkinter`` belongs to the old prototype and is excluded.
# ---------------------------------------------------------------------------
analysis = Analysis(
    [str(project_root / "run_app.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter"],
    noarchive=False,          # keep modules in the PYZ archive (smaller exe)
    optimize=0,               # use the source bytecode; no docstring stripping
)

pyz = PYZ(analysis.pure)

# ---------------------------------------------------------------------------
# One-file executable.
#
# console=False      -> windowed app (no console window); diagnostics go to
#                       logs/studio.log and the optional in-app log panel.
# disable_windowed_traceback=False
#                    -> PyInstaller shows its unhandled-exception dialog instead
#                       of failing silently if something breaks before logging.
# uac_admin=True     -> embed requireAdministrator, matching the official
#                       driver.  Auto-switch must be able to query elevated
#                       games (anti-cheat launchers) and HID writes must not be
#                       blocked by a game's security layer.  Windows shows a
#                       UAC consent prompt on every start, as it does for the
#                       vendor software; "Start with Windows" therefore uses a
#                       per-user Run entry.
# icon=...           -> Explorer/taskbar icon; the same .ico is bundled above
#                       for the QIcon at runtime.
# upx=False          -> UPX packing is avoided: it can trip antivirus and is
#                       known to break some Qt DLLs.
# runtime_tmpdir=None-> let PyInstaller use the default temporary directory for
#                       the unpacked bundle; nothing is written beside the exe
#                       until first launch creates data/config/logs.
# ---------------------------------------------------------------------------
exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
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
    uac_admin=True,
)
