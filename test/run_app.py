"""
Launch the existing SM809 GUI with the WIRED prototype behind it.

    python test\run_app.py            # DRY RUN: GUI works, nothing is sent to the mouse
    python test\run_app.py --apply    # really sends (polling rate + active DPI stage only)

Close the official app and any other copy of this GUI first.

What it does: swaps the GUI's device layer for test/wired_adapter.py before the
GUI starts. Your real config/ folder is NOT used -- profiles and macros for this
launcher live in test/_gui_data/.

Only polling rate and the active DPI stage do anything; every other control is inert and the
console log says so. Do not use the tray's "Start with Windows" toggle from here.
"""
import os
import runpy
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
os.chdir(ROOT)

import wired_adapter as A          # noqa: E402

A.APPLY = "--apply" in sys.argv
sys.argv = [a for a in sys.argv if a != "--apply"]

# Keep this launcher's profiles/macros away from the real app's config/ folder.
DATA = os.path.join(HERE, "_gui_data")
os.makedirs(DATA, exist_ok=True)
import app.profile_store as _ps     # noqa: E402
import app.macro_store as _ms       # noqa: E402
_ps.default_path = lambda: os.path.join(DATA, "profiles.json")
_ms.default_path = lambda: os.path.join(DATA, "macros.json")

# Swap the device layer.
import app.controller as C          # noqa: E402
C.SM809Pro = A.SM809Wired
C.StatusListener = A.NullStatusListener
C.detect_modes = lambda vid=None: []

print(f"[wired] starting GUI -- {'LIVE (--apply)' if A.APPLY else 'DRY RUN (add --apply to send)'}", flush=True)
runpy.run_path(os.path.join(ROOT, "run_app.py"), run_name="__main__")
