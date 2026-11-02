"""Shared test setup: one scratch data folder for the whole session."""

import os
import tempfile

# Isolate every test from the real app data and the vendor installation.
os.environ.setdefault("SM809_DATA_DIR",
                      tempfile.mkdtemp(prefix="sm809-pytest-data-"))
# The GUI tests run headless; no display is required.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# The offscreen platform on Windows starts without a font database, so every
# glyph becomes a square 11 px fallback and widget width measurements are
# meaningless.  Point it at the system fonts so layout tests see real metrics.
if os.name == "nt" and not os.environ.get("QT_QPA_FONTDIR"):
    _fonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    if os.path.isdir(_fonts):
        os.environ["QT_QPA_FONTDIR"] = _fonts
