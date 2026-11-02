"""Per-device Windows wheel direction for the wired SM809.

The SM809's wheel is wired opposite to the Windows convention: with Windows at
its default (``Down motion scrolls down``) the wheel reports the reverse
direction.  That is a property of this mouse, not of a profile: the vendor
driver has no wheel-direction control, and the firmware's hidden wheel slots
are not guaranteed to be what the optical encoder reads.

Windows does expose the correct per-device switch.  Each HID mouse has a
``Device Parameters\\FlipFlopWheel`` DWORD; when it is 1 the HID stack inverts
that device's wheel only.  This module reads that value, writes it for every
SM809 mouse collection, resets the global Windows scrolling-direction setting
to its default, and restarts the HID device so the change takes effect.

Writing ``HKLM`` needs administrator rights, so :func:`apply_elevated` starts a
short elevated copy of this module when the app is running unelevated.  Nothing
here runs automatically: the Performance tab asks before changing anything.

Only the SM809 instance is touched.  Other mice keep their own wheel direction,
and the vendor installation under Program Files is never read or written.
"""

from __future__ import annotations

import ctypes
import json
import logging
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path

try:  # Windows-only; the studio itself is Windows-only.
    import winreg
except ImportError:  # pragma: no cover - allows import on non-Windows test hosts
    winreg = None  # type: ignore[assignment]

_log = logging.getLogger("sm809.wheel")
if not logging.getLogger("sm809").handlers:
    logging.getLogger("sm809").addHandler(logging.NullHandler())

VID = "04D9"
PID = "A09F"
MOUSE_INTERFACE = "MI_00"
COLLECTION_PREFIX = f"VID_{VID}&PID_{PID}&{MOUSE_INTERFACE}".upper()

_ENUM_HID = r"SYSTEM\CurrentControlSet\Enum\HID"
_GLOBAL_MOUSE = r"Control Panel\Mouse"
_FLIP = "FlipFlopWheel"
_GLOBAL_REVERSE = "ReverseMouseWheelDirection"

# ShellExecuteEx flags.
_SEE_MASK_NOCLOSEPROCESS = 0x00000040
_SEE_MASK_NOASYNC = 0x00000100
_SW_HIDE = 0
_WAIT_OBJECT_0 = 0x00000000
_WAIT_TIMEOUT = 0x00000102
_ERROR_CANCELLED = 1223


@dataclass(frozen=True)
class WheelState:
    """What Windows currently has for the SM809 wheel."""

    instances: tuple[str, ...] = ()
    flipped: int = 0
    total: int = 0
    global_reverse: bool = False

    @property
    def inverted(self) -> bool:
        """True when every present SM809 mouse collection is inverted."""
        return bool(self.total) and self.flipped == self.total

    @property
    def partial(self) -> bool:
        return 0 < self.flipped < self.total

    def describe(self) -> str:
        if not self.total:
            return "The SM809 mouse is not connected."
        if self.inverted:
            return ("Fixed in Windows for this mouse. Windows' scrolling "
                    "direction can stay at its default.")
        if self.partial:
            return ("Only part of the SM809 HID stack is inverted; toggling "
                    "will normalize it.")
        return "Not fixed in Windows yet."


@dataclass(frozen=True)
class WheelResult:
    ok: bool
    message: str
    state: WheelState | None = None


# ---------------------------------------------------------------------------
# Registry discovery / read
# ---------------------------------------------------------------------------

def _instance_key(instance: str) -> str:
    """Registry path (relative to HKLM) for a full HID instance id.

    Device parameters live under the Enum hive, so the ``HID\\`` part is
    replaced by ``SYSTEM\\CurrentControlSet\\Enum\\HID\\`` -- not dropped.
    Dropping the hive prefix made every read fall back to "not inverted" and
    every write fail with ``WinError 2``.
    """
    text = instance
    if text.upper().startswith("HID\\"):
        text = text[4:]
    return f"{_ENUM_HID}\\{text}"


def device_instances() -> list[str]:
    """Present and past SM809 mouse collection instance ids.

    The values live under ``HKLM\\SYSTEM\\CurrentControlSet\\Enum``, which is
    world-readable, so this works without elevation.  Only ``MI_00`` (the mouse
    collection) is selected; the keyboard and vendor collections are left alone.
    """
    if winreg is None:
        return []
    found: list[str] = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _ENUM_HID,
                            0, winreg.KEY_READ) as root:
            index = 0
            while True:
                try:
                    group = winreg.EnumKey(root, index)
                except OSError:
                    break
                index += 1
                if not group.upper().startswith(COLLECTION_PREFIX):
                    continue
                try:
                    with winreg.OpenKey(root, group) as collection:
                        sub = 0
                        while True:
                            try:
                                instance = winreg.EnumKey(collection, sub)
                            except OSError:
                                break
                            sub += 1
                            path = f"{group}\\{instance}"
                            try:
                                with winreg.OpenKey(
                                        root, path + r"\Device Parameters"):
                                    pass
                            except OSError:
                                continue
                            found.append(f"HID\\{path}")
                except OSError:
                    continue
    except OSError:
        return []
    return found


def _read_dword(root, path: str, name: str, default: int = 0) -> int:
    if winreg is None:
        return default
    try:
        with winreg.OpenKey(root, path, 0, winreg.KEY_READ) as key:
            value, _kind = winreg.QueryValueEx(key, name)
        return int(value)
    except (OSError, ValueError, TypeError):
        return default


def read_state() -> WheelState:
    """Read the per-device flip flags and the global Windows direction."""
    instances = device_instances()
    flipped = 0
    for instance in instances:
        path = _instance_key(instance) + r"\Device Parameters"
        if _read_dword(winreg.HKEY_LOCAL_MACHINE, path, _FLIP, 0):
            flipped += 1
    global_reverse = bool(
        winreg is not None
        and _read_dword(winreg.HKEY_CURRENT_USER, _GLOBAL_MOUSE,
                        _GLOBAL_REVERSE, 0))
    return WheelState(tuple(instances), flipped, len(instances), global_reverse)


# ---------------------------------------------------------------------------
# Apply (requires administrator)
# ---------------------------------------------------------------------------

def is_admin() -> bool:
    if sys.platform != "win32":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:  # pragma: no cover - defensive
        return False


def _set_dp_dword(instance: str, name: str, value: int) -> None:
    path = _instance_key(instance) + r"\Device Parameters"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0,
                        winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, name, 0, winreg.REG_DWORD, int(value))


def _set_global_default() -> None:
    with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, _GLOBAL_MOUSE, 0,
                            winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, _GLOBAL_REVERSE, 0, winreg.REG_DWORD, 0)
    _broadcast_mouse_settings()


def _broadcast_mouse_settings() -> None:
    """Ask running apps to re-read Control Panel\\Mouse.

    Without this the current session can keep the old global direction until
    the next sign-in, which would cancel the per-device inversion and leave
    the wheel still reversed.
    """
    if sys.platform != "win32":
        return
    try:
        user32 = ctypes.windll.user32
        user32.SendMessageTimeoutW.argtypes = [
            ctypes.c_void_p, ctypes.c_uint, ctypes.c_size_t,
            ctypes.c_wchar_p, ctypes.c_uint, ctypes.c_uint,
            ctypes.POINTER(ctypes.c_size_t),
        ]
        user32.SendMessageTimeoutW.restype = ctypes.c_size_t
        result = ctypes.c_size_t(0)
        user32.SendMessageTimeoutW(
            ctypes.c_void_p(0xFFFF),  # HWND_BROADCAST
            0x001A,                   # WM_SETTINGCHANGE
            0, _GLOBAL_MOUSE, 0x0002, 3000,  # SMTO_ABORTIFHUNG
            ctypes.byref(result))
    except Exception:  # pragma: no cover - cosmetic; the settings are written
        pass


def _pnputil(*args: str, timeout: int = 20) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["pnputil", *args], capture_output=True, text=True, timeout=timeout,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def _pnputil_detail(proc: subprocess.CompletedProcess) -> str:
    lines = (proc.stderr or proc.stdout or "").strip().splitlines()
    return lines[-1] if lines else f"pnputil exit {proc.returncode}"


def _restart_device(instance: str, timeout: int = 20) -> str | None:
    """Restart one HID collection so FlipFlopWheel is re-read.  Returns an
    error string, or None on success.

    Windows reads ``Device Parameters`` when the node starts.  A plain
    restart normally re-reads them; some builds refuse it for an idle HID
    child, so a disable/enable cycle is used as the fallback.  Both make the
    mouse disappear for about a second.
    """
    try:
        proc = _pnputil("/restart-device", instance, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return f"{instance}: {exc}"
    if proc.returncode == 0:
        _log.debug("wheel: restarted %s", instance)
        return None

    first_error = _pnputil_detail(proc)
    _log.debug("wheel: restart-device failed for %s (%s); trying disable/enable",
               instance, first_error)
    try:
        off = _pnputil("/disable-device", instance, timeout=timeout)
        if off.returncode != 0:
            return f"{instance}: {first_error}"
        time.sleep(0.8)
        on = _pnputil("/enable-device", instance, timeout=timeout)
        if on.returncode != 0:
            # Never leave the mouse disabled: one more attempt after a pause.
            time.sleep(1.0)
            on = _pnputil("/enable-device", instance, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        _enable_best_effort(instance, timeout)
        return f"{instance}: {exc}"
    if on.returncode != 0:
        return (f"{instance}: {_pnputil_detail(on)} "
                "(the mouse may need to be reconnected)")
    _log.debug("wheel: disable/enable cycle completed for %s", instance)
    return None


def _enable_best_effort(instance: str, timeout: int = 20) -> None:
    """Make sure a failed disable/enable cycle does not strand the mouse."""
    try:
        _pnputil("/enable-device", instance, timeout=timeout)
    except Exception:  # pragma: no cover - already failing
        pass


def apply(invert: bool) -> WheelResult:
    """Set the per-device wheel direction and restore Windows' default.

    Must run elevated.  The global ``ReverseMouseWheelDirection`` value is
    always cleared so the mouse has exactly one inversion (the per-device one);
    otherwise a user's earlier Windows workaround would cancel it.

    The result is verified through the registry and retried once: restarting
    the collection can make Windows re-enumerate it under a new instance id,
    which starts with the flag unset.  Verification only proves what Windows
    will read at the next device start; if scrolling is still unchanged after
    the reconnect, signing out and back in (or one reboot) makes it take.
    """
    if winreg is None or sys.platform != "win32":
        return WheelResult(False, "This fix is only available on Windows.")
    if not is_admin():
        return WheelResult(False, "Administrator rights are required.")

    if not device_instances():
        return WheelResult(False, "The SM809 mouse is not connected.")

    _log.info("wheel: %s the per-device inversion for the SM809",
              "enabling" if invert else "clearing")
    problems: list[str] = []
    state = read_state()
    for attempt in (1, 2):
        instances = device_instances()
        if not instances:
            return WheelResult(False, "The SM809 mouse is not connected.")
        for instance in instances:
            try:
                _set_dp_dword(instance, _FLIP, 1 if invert else 0)
            except OSError as exc:
                problems.append(f"{instance}: {exc}")

        # Windows' own scrolling direction goes back to "Down motion scrolls
        # down"; the per-device flag is what makes the SM809 follow it.
        try:
            _set_global_default()
        except OSError as exc:
            problems.append(f"Windows scrolling direction: {exc}")

        for instance in instances:
            error = _restart_device(instance)
            if error:
                problems.append(error)

        state = read_state()
        if state.inverted == bool(invert):
            break
        if attempt == 1:
            _log.warning(
                "wheel: Windows still reports %s after the restart; "
                "re-enumerating and retrying once",
                "inverted" if state.inverted else "normal")

    if state.inverted == bool(invert):
        _log.info("wheel: %d/%d SM809 collection(s) now %s",
                  state.flipped, state.total,
                  "inverted" if invert else "at the Windows default")
        message = (
            "Scrolling is now inverted for the SM809 only. Windows' scrolling "
            "direction is back at its default.") if invert else (
            "The SM809 is back to the normal Windows wheel direction.")
        if problems:
            _log.warning("wheel: applied with restart warnings: %s",
                         "; ".join(problems[:4]))
            message += ("\n\nWindows reported a device-restart problem. If "
                        "scrolling has not changed, unplug and reconnect the "
                        "mouse or sign out of Windows once.")
        return WheelResult(True, message, state)

    _log.error("wheel: Windows kept the previous direction (%d/%d, target %s): %s",
               state.flipped, state.total, invert, "; ".join(problems[:4]))
    detail = ("\n" + "\n".join(problems[:4])) if problems else ""
    return WheelResult(
        False,
        "Windows still reports a different wheel direction." + detail +
        "\nUnplug and reconnect the mouse, then reopen the Performance tab. "
        "If it still does not change, sign out of Windows once so the HID "
        "stack reads the setting.",
        state)


# ---------------------------------------------------------------------------
# Elevation
# ---------------------------------------------------------------------------

class _SHELLEXECUTEINFOW(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("fMask", ctypes.c_ulong),
        ("hwnd", ctypes.c_void_p),
        ("lpVerb", ctypes.c_wchar_p),
        ("lpFile", ctypes.c_wchar_p),
        ("lpParameters", ctypes.c_wchar_p),
        ("lpDirectory", ctypes.c_wchar_p),
        ("nShow", ctypes.c_int),
        ("hInstApp", ctypes.c_void_p),
        ("lpIDList", ctypes.c_void_p),
        ("lpClass", ctypes.c_wchar_p),
        ("hkeyClass", ctypes.c_void_p),
        ("dwHotKey", ctypes.c_ulong),
        ("hIcon", ctypes.c_void_p),
        ("hProcess", ctypes.c_void_p),
    ]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _run_elevated(parameters: str, timeout_ms: int = 180000
                  ) -> tuple[bool, str, int | None]:
    """Run ``python -m wired.wheel_direction ...`` with the UAC prompt.

    ``lpFile`` already names the interpreter, so ``parameters`` must start at
    ``-m``: repeating the executable inside them made Python treat its own
    ``python.exe`` as the script to run, which died instantly with a
    ``SyntaxError`` and never wrote the status file.

    Returns (completed, error, exit code).  ``completed`` is False when the
    user cancels the prompt or the process cannot be started; it does not mean
    the child succeeded.  The caller reads the child's status file.
    """
    if sys.platform != "win32":
        return False, "This fix is only available on Windows."
    shell32 = ctypes.windll.shell32
    kernel32 = ctypes.windll.kernel32
    shell32.ShellExecuteExW.argtypes = [ctypes.POINTER(_SHELLEXECUTEINFOW)]
    shell32.ShellExecuteExW.restype = ctypes.c_int
    kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
    kernel32.WaitForSingleObject.restype = ctypes.c_ulong
    kernel32.GetExitCodeProcess.argtypes = [ctypes.c_void_p,
                                            ctypes.POINTER(ctypes.c_ulong)]
    kernel32.GetExitCodeProcess.restype = ctypes.c_int
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype = ctypes.c_int

    info = _SHELLEXECUTEINFOW()
    info.cbSize = ctypes.sizeof(info)
    info.fMask = _SEE_MASK_NOCLOSEPROCESS | _SEE_MASK_NOASYNC
    info.lpVerb = "runas"
    info.lpFile = sys.executable
    info.lpParameters = parameters
    info.lpDirectory = str(_project_root())
    info.nShow = _SW_HIDE

    if not shell32.ShellExecuteExW(ctypes.byref(info)):
        code = int(kernel32.GetLastError())
        if code == _ERROR_CANCELLED:
            return False, "Administrator permission was cancelled.", None
        return False, f"Could not start the elevated helper (error {code}).", None

    try:
        wait = kernel32.WaitForSingleObject(info.hProcess, int(timeout_ms))
        if wait == _WAIT_TIMEOUT:
            return False, "The elevated helper timed out.", None
        code = ctypes.c_ulong(0)
        kernel32.GetExitCodeProcess(info.hProcess, ctypes.byref(code))
        if wait != _WAIT_OBJECT_0:
            return False, f"The elevated helper did not finish (wait {wait}).", None
        # The status file is authoritative; the exit code only tells us that
        # the child ran.
        return True, "", int(code.value)
    finally:
        kernel32.CloseHandle(info.hProcess)


def apply_elevated(invert: bool) -> WheelResult:
    """Apply from the UI thread without blocking it.

    When the studio is already elevated this is a direct call.  Otherwise a
    hidden elevated copy of this module writes the registry and restarts the
    device; the result comes back through a small JSON status file.
    """
    if winreg is None or sys.platform != "win32":
        return WheelResult(False, "This fix is only available on Windows.")
    if is_admin():
        _log.info("wheel: running elevated in-process")
        return apply(invert)

    _log.info("wheel: requesting administrator permission for the per-device flag")
    handle, name = tempfile.mkstemp(prefix="sm809-wheel-", suffix=".json")
    import os
    os.close(handle)
    status = Path(name)
    # lpFile already is the interpreter.  Repeating sys.executable here made
    # the elevated Python run its own python.exe as if it were a script; it
    # exited with a SyntaxError before writing the status file.
    parameters = subprocess.list2cmdline([
        "-m", "wired.wheel_direction",
        "--apply", "1" if invert else "0", "--status", str(status),
    ])
    try:
        completed, error, exit_code = _run_elevated(parameters)
        if not completed:
            _log.warning("wheel: the elevated helper did not run: %s", error)
            return WheelResult(False, error, read_state())
        try:
            payload = json.loads(status.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _log.warning("wheel: the elevated helper left no status (exit %s)",
                         exit_code)
            detail = (f" (exit code {exit_code})"
                      if exit_code is not None else "")
            return WheelResult(
                False,
                f"The elevated helper finished without a result{detail}. "
                "Unplug and reconnect the mouse, then check the setting again.",
                read_state())
        result = WheelResult(bool(payload.get("ok")),
                             str(payload.get("message") or ""),
                             read_state())
        _log.info("wheel: elevated helper finished: ok=%s (exit %s)",
                  result.ok, exit_code)
        if result.ok:
            # Do this in the *current* user's hive as well: if UAC was
            # authorised with a different administrator account, the child's
            # HKCU write went to that account, not to the person using the app.
            try:
                _set_global_default()
            except OSError:
                pass
        return result
    finally:
        try:
            status.unlink()
        except OSError:
            pass


# ---------------------------------------------------------------------------
# Elevated entry point
# ---------------------------------------------------------------------------

def _child_main(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="wired.wheel_direction")
    parser.add_argument("--apply", choices=("0", "1"), required=True)
    parser.add_argument("--status")
    args = parser.parse_args(argv)
    status_path = Path(args.status) if args.status else None
    if status_path is not None:
        # Provisional record: if the helper is killed mid-apply, the parent
        # shows this instead of an empty file with no explanation.
        try:
            status_path.write_text(json.dumps({
                "ok": False,
                "message": "The elevated helper started but did not finish.",
            }), encoding="utf-8")
        except OSError:
            pass
    try:
        result = apply(args.apply == "1")
        payload = {"ok": result.ok, "message": result.message}
    except Exception as exc:  # pragma: no cover - surfaced in the status file
        payload = {"ok": False, "message": f"{type(exc).__name__}: {exc}"}
    if status_path is not None:
        try:
            status_path.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass
    return 0 if payload["ok"] else 1


if __name__ == "__main__":  # pragma: no cover - elevated helper
    raise SystemExit(_child_main(sys.argv[1:]))
