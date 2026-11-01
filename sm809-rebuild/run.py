"""Launch the SM809 Control Center.

Usage:
    python run.py              connect to real hardware when present
    python run.py --demo       simulate the mouse (no hardware needed)
    python run.py --data-dir D use another portable data folder
"""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="sm809",
        description="SM809 wired mouse control center (clean-room rebuild).",
    )
    parser.add_argument("--demo", action="store_true",
                        help="simulate the HID device; nothing is written to hardware")
    parser.add_argument("--hardware", action="store_true",
                        help="force the real HID transport")
    parser.add_argument("--data-dir", type=Path, default=None,
                        help="use this portable data folder instead of ./data")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    demo = True if args.demo else (False if args.hardware else None)
    try:
        from sm809.ui.app import App
    except Exception:
        traceback.print_exc()
        print("\nThe rebuild needs Python 3.10+ with tkinter (included with the "
              "official Windows installer).")
        return 1
    try:
        app = App(demo=demo, data_dir=args.data_dir)
    except Exception:
        traceback.print_exc()
        print("\nCould not open the main window. If this is a headless session, "
              "run the tests with 'pytest' instead.")
        return 1
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
