"""
app.elevation -- run the studio with administrator rights, like the official
driver.

Some games and anti-cheat launchers only expose their foreground window (and
accept configuration) to an elevated process. Running the studio elevated
removes that class of "the profile did not switch" failures, matching the
vendor software's behaviour.

- The packaged exe requests elevation through its manifest
  (``uac_admin=True`` in SM809WiredStudio.spec), so Windows shows the UAC
  prompt before the app starts.
- A source run (``python run_app.py``) relaunches itself with ShellExecuteW
  "runas" once; ``--no-elevate`` skips that, and ``--demo`` never relaunches
  from source. (A packaged exe elevates through its manifest regardless.)
- If UAC is declined, the studio keeps running unelevated after a native
  warning; the Auto-Switch page then shows a reminder that elevated games may
  not be detected.
"""

import ctypes
import os
import subprocess
import sys

TRIED_ENV = "SM809_ELEVATION_TRIED"     # stops a relaunch loop if UAC is refused


def is_admin():
    """True when this process has administrator rights (always true off Windows)."""
    if os.name != "nt":
        return True
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def needs_elevation(argv, environ, admin=None):
    """Whether this process should ask for elevation before starting.

    Pure enough to test: ``argv`` is the argument list without the program
    name, ``environ`` is any mapping, and ``admin`` overrides the live check.
    """
    if os.name != "nt":
        return False
    if admin is None:
        admin = is_admin()
    if admin:
        return False
    args = list(argv)
    if "--demo" in args or "--no-elevate" in args:
        return False
    return environ.get(TRIED_ENV) != "1"


def relaunch_as_admin(args=None):
    """Start an elevated copy of this app. True when Windows accepted the request.

    A False result means the user declined UAC (or the launch failed); the
    caller decides whether to continue unelevated.
    """
    if os.name != "nt":
        return False
    args = list(sys.argv[1:] if args is None else args)
    if getattr(sys, "frozen", False):
        exe = sys.executable
        params = subprocess.list2cmdline(args)
    else:
        exe = sys.executable
        script = os.path.abspath(sys.argv[0])
        params = subprocess.list2cmdline([script] + args)
    shell32 = ctypes.windll.shell32
    shell32.ShellExecuteW.argtypes = [
        ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_wchar_p,
        ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_int]
    shell32.ShellExecuteW.restype = ctypes.c_void_p
    try:
        rc = shell32.ShellExecuteW(None, "runas", exe, params, None, 1)
    except Exception:
        return False
    return int(rc or 0) > 32         # ShellExecute returns <= 32 on failure


def ask_continue_unelevated():
    """Yes/No prompt after UAC was declined; True means keep running."""
    if os.name != "nt":
        return True
    MB_YESNO = 0x00000004
    MB_ICONWARNING = 0x00000030
    IDYES = 6
    text = (
        "SM809 Wired Studio is not running as administrator.\n\n"
        "Like the official driver, administrator rights are needed for "
        "auto-switch to detect games that run elevated (some anti-cheat "
        "titles). Ordinary apps and HID settings still work.\n\n"
        "Continue without administrator rights?")
    try:
        rc = ctypes.windll.user32.MessageBoxW(
            None, text, "SM809 Wired Studio",
            MB_YESNO | MB_ICONWARNING)
        return rc == IDYES
    except Exception:
        return True


def prepare_startup(argv):
    """Called before Qt starts. True = run this process, False = exit now.

    The elevated relaunch leaves this process to exit immediately; the child
    inherits TRIED_ENV so a refused prompt cannot loop.
    """
    if not needs_elevation(argv, os.environ):
        return True
    os.environ[TRIED_ENV] = "1"
    if relaunch_as_admin(list(argv)):
        return False
    return ask_continue_unelevated()
