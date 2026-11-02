"""
app.autoswitch -- per-app profile auto-switching (Milestone 3 step 3, the
headline feature; the official software has NO auto-switch).

Watches the foreground window and switches the active mouse profile by rule,
modelled on Razer Synapse's "base profile" behaviour:

- The user's MANUAL selection is the BASE profile (sticky, persisted).
- When the foreground app matches a profile's rule, switch to that profile
  (a temporary override).
- When focus moves to an app that matches NO rule, REVERT to the base profile.
- If the base profile itself matches the app, nothing visibly changes.

Rules live on each profile as `match_rules = [{"exe": "game.exe", "title": None},
...]`. First match in PROFILE LIST ORDER wins (reorder profiles to set priority).
A switch only fires when the target differs from what is currently applied, so a
steady foreground never re-pushes config to the device.

Foreground detection is behind an injectable `watcher` so the core logic is
testable headless and the OS-specific part can be swapped per platform (Windows
implemented; macOS/Linux land in the M3 step 6 port).
"""

import logging
import os
import time

from PySide6.QtCore import QObject, QTimer, Signal

_log = logging.getLogger("sm809.autoswitch")


# --- foreground-window detection --------------------------------------------
class ForegroundWatcher:
    """Returns (exe_basename_lower, window_title, full_path) for the focused
    window, or (None, None, None) if it can't be determined. Windows impl; other
    platforms return Nones until the port lands. The full path lets rules tell
    apart same-named exes (e.g. many UE/Unity games ship Client-Win64-Shipping.exe)."""

    def __init__(self):
        self._impl = _win_foreground if os.name == "nt" else _null_foreground

    def current(self):
        try:
            return self._impl()
        except Exception:
            return (None, None, None)


def _null_foreground():
    return (None, None, None)


def _process_exe_name(kernel32, ctypes, wintypes, pid):
    """Toolhelp fallback: exe name for `pid` without opening the process.

    OpenProcess can be denied for a game running elevated (or behind an
    anti-cheat), which used to leave exe/path empty and made every rule fail.
    A process snapshot only needs the exe name, which Windows exposes anyway.
    """
    class PROCESSENTRY32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", wintypes.DWORD),
            ("cntUsage", wintypes.DWORD),
            ("th32ProcessID", wintypes.DWORD),
            ("th32DefaultHeapID", ctypes.c_void_p),
            ("th32ModuleID", wintypes.DWORD),
            ("cntThreads", wintypes.DWORD),
            ("th32ParentProcessID", wintypes.DWORD),
            ("pcPriClassBase", ctypes.c_long),
            ("dwFlags", wintypes.DWORD),
            ("szExeFile", wintypes.WCHAR * 260),
        ]

    TH32CS_SNAPPROCESS = 0x00000002
    kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
    kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
    kernel32.Process32FirstW.argtypes = [wintypes.HANDLE,
                                         ctypes.POINTER(PROCESSENTRY32W)]
    kernel32.Process32NextW.argtypes = [wintypes.HANDLE,
                                        ctypes.POINTER(PROCESSENTRY32W)]
    snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    invalid = ctypes.c_void_p(-1).value
    if not snap or snap == invalid:
        return None
    try:
        entry = PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
        if not kernel32.Process32FirstW(snap, ctypes.byref(entry)):
            return None
        while True:
            if entry.th32ProcessID == pid:
                name = (entry.szExeFile or "").strip().lower()
                return name or None
            if not kernel32.Process32NextW(snap, ctypes.byref(entry)):
                return None
    finally:
        kernel32.CloseHandle(snap)


def _pid_app(pid):
    """(exe_basename_lower, full_path) for a process, or (None, None).

    OpenProcess may be denied for an elevated game or anti-cheat title, so the
    Toolhelp snapshot is used as a fallback: the list picker and matching still
    get the exe name even when the full path is unavailable.
    """
    import ctypes
    from ctypes import wintypes

    kernel32 = ctypes.windll.kernel32
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    full_path = None
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if handle:
        try:
            kernel32.QueryFullProcessImageNameW.argtypes = [
                wintypes.HANDLE, wintypes.DWORD,
                wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
            kernel32.QueryFullProcessImageNameW.restype = wintypes.BOOL
            size = wintypes.DWORD(32768)
            nbuf = ctypes.create_unicode_buffer(size.value)
            if kernel32.QueryFullProcessImageNameW(handle, 0, nbuf, ctypes.byref(size)):
                full_path = nbuf.value
        finally:
            kernel32.CloseHandle(handle)
    exe = os.path.basename(full_path).lower() if full_path else None
    if not exe:
        exe = _process_exe_name(kernel32, ctypes, wintypes, pid)
    return (exe, full_path)


def _win_foreground():
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32

    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return (None, None, None)

    # window title
    user32.GetWindowTextLengthW.restype = ctypes.c_int
    length = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    title = buf.value or ""

    # owning process id -> exe name / full path
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    exe, full_path = _pid_app(pid.value)
    return (exe, title, full_path)


# --- running-app list for the picker ----------------------------------------
# Windows UWP apps all run inside ApplicationFrameHost.exe, so the exe alone
# cannot tell Calculator from Photos; those entries also match on the title.
UWP_HOST_EXES = {"applicationframehost.exe"}


def list_running_apps():
    """Visible top-level windows as ``{title, exe, path}`` dicts, sorted by
    title. Used by the "Add app" picker; empty on non-Windows platforms or if
    the enumeration fails (the picker then says so instead of crashing)."""
    if os.name != "nt":
        return []
    try:
        return _win_list_apps()
    except Exception:
        _log.debug("running-app enumeration failed", exc_info=True)
        return []


def rule_for_app(apps, app):
    """The narrowest rule that still targets `app` from the running-app list.

    - exe name unique in the list -> match the exe only, so moving or updating
      the app (for example a versioned game folder) does not break the rule;
    - several running apps share the exe -> also match the full path;
    - UWP host windows -> also match the window title.
    """
    exe = (app.get("exe") or "").strip().lower()
    path = (app.get("path") or "").strip()
    title = (app.get("title") or "").strip()
    rule = {"exe": exe or None, "path": None, "title": None}
    if not exe:
        return rule
    if exe in UWP_HOST_EXES:
        rule["path"] = path or None
        rule["title"] = title.lower() or None
        return rule
    same = [a for a in apps
            if (a.get("exe") or "").strip().lower() == exe]
    if len(same) > 1:
        rule["path"] = path or None
    return rule


def _win_list_apps():
    import ctypes
    from ctypes import wintypes

    user32 = ctypes.windll.user32
    user32.GetWindowTextLengthW.restype = ctypes.c_int

    GWL_EXSTYLE = -20
    WS_EX_TOOLWINDOW = 0x00000080
    get_long = getattr(user32, "GetWindowLongPtrW", None)
    if get_long is not None:
        get_long.restype = ctypes.c_longlong
    else:
        get_long = user32.GetWindowLongW
        get_long.restype = ctypes.c_long
    get_long.argtypes = [wintypes.HWND, ctypes.c_int]

    # shell surfaces and IME helpers show up as invisible system windows
    skip_titles = {"program manager", "default ime", "msctfime ui",
                   "windows input experience", "microsoft text input application"}

    apps = {}
    seen_pids = {}

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def _visit(hwnd, _lparam):
        if not user32.IsWindowVisible(hwnd):
            return True
        length = user32.GetWindowTextLengthW(hwnd)
        if length <= 0:
            return True
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        title = (buf.value or "").strip()
        if not title or title.lower() in skip_titles:
            return True
        if get_long(hwnd, GWL_EXSTYLE) & WS_EX_TOOLWINDOW:
            return True

        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if pid.value in seen_pids:
            exe, path = seen_pids[pid.value]
        else:
            exe, path = _pid_app(pid.value)
            seen_pids[pid.value] = (exe, path)
        if not exe:
            return True
        path_lower = (path or "").lower()
        if exe in UWP_HOST_EXES:
            key = (exe, path_lower, title.lower())
        else:
            # one picker row per program: Chrome or VS Code windows collapse
            key = (exe, path_lower)
        if key not in apps:
            apps[key] = {"title": title, "exe": exe, "path": path}
        return True

    user32.EnumWindows.argtypes = [type(_visit), wintypes.LPARAM]
    user32.EnumWindows(_visit, 0)
    return sorted(apps.values(), key=lambda a: a["title"].lower())





# --- rule matching (pure) ----------------------------------------------------
def rule_matches(rule, exe, title, path=None):
    """A rule matches when ALL of its specified (non-empty) conditions hold:
      - exe:   basename equals the foreground exe (case-insensitive)
      - path:  substring of the foreground full path (case-insensitive) -- this
               distinguishes same-named exes (e.g. UE/Unity Client-Win64-Shipping.exe)
      - title: substring of the foreground window title (case-insensitive)
    A rule with no conditions set never matches."""
    want_exe = (rule.get("exe") or "").strip().lower()
    want_path = (rule.get("path") or "").strip().lower()
    want_title = (rule.get("title") or "").strip().lower()
    if not (want_exe or want_path or want_title):
        return False
    if want_exe and (not exe or exe.lower() != want_exe):
        return False
    if want_path and (not path or want_path not in path.lower()):
        return False
    if want_title and (not title or want_title not in title.lower()):
        return False
    return True


def match_profile(profiles, exe, title, path=None):
    """First profile (in list order) with a rule matching the foreground, or None."""
    for p in profiles:
        for r in p.get("match_rules", []):
            if rule_matches(r, exe, title, path):
                return p["id"]
    return None


# --- the switcher ------------------------------------------------------------
class AutoSwitcher(QObject):
    """Polls the foreground window and requests profile switches.

    Wiring: `apply` is called with a profile id when a switch should happen;
    `get_applied` returns the id of the profile currently on the device (so we
    skip redundant re-applies). The base profile is set via set_base() whenever
    the user manually picks a profile.
    """

    switched = Signal(str)        # emitted with the profile id we switched TO

    def __init__(self, store, apply, get_applied, watcher=None,
                 interval_ms=200, debounce_ms=200, parent=None):
        super().__init__(parent)
        self._store = store
        self._apply = apply
        self._get_applied = get_applied
        self._watcher = watcher or ForegroundWatcher()
        self._base_id = None
        self._enabled = False
        self._last_fg = None          # (exe, path) for change-only debug logging
        # debounce: apply only after the target stays put for this long, so fast
        # alt-tabbing through apps doesn't flood the (stateful) device with a full
        # profile-apply per transient window. 0 = switch immediately.
        self._debounce_ms = debounce_ms
        self._pending = None          # candidate target awaiting the debounce
        self._pending_since = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(interval_ms)
        self._timer.timeout.connect(self.poll)

    def set_base(self, pid):
        """The manually-selected, sticky profile to revert to on no-match."""
        self._base_id = pid

    @property
    def base_id(self):
        return self._base_id

    def set_enabled(self, on):
        self._enabled = bool(on)
        self._pending = None
        if self._enabled:
            self._timer.start()
            self.poll()                     # start watching (debounce still applies)
        else:
            self._timer.stop()
            # leaving auto-switch reverts to the manual base profile
            if self._base_id and self._get_applied() != self._base_id:
                self._switch(self._base_id)

    def is_enabled(self):
        return self._enabled

    def poll(self):
        if not self._enabled:
            return
        exe, title, path = self._watcher.current()
        if (exe, path) != self._last_fg:
            self._last_fg = (exe, path)
            _log.debug("foreground: %s | %s", exe or "(unknown)",
                       path or "(no path)")
        # Only id + rules are needed for matching. A ProfileStore exposes
        # ``match_targets`` so the 200 ms poll does not rebuild every profile's
        # full button/DPI/lighting config; simpler stores still work via all().
        source = getattr(self._store, "match_targets", None)
        targets = source() if callable(source) else self._store.all()
        target = match_profile(targets, exe, title, path) or self._base_id
        # already on the right profile -> nothing pending
        if not target or target == self._get_applied():
            self._pending = None
            return
        if self._debounce_ms <= 0:
            self._pending = None
            self._switch(target)
            return
        # debounce: only switch once the target has been stable long enough, so
        # rapid app-switching collapses to a single apply on the app you land on
        now = time.monotonic()
        if target != self._pending:
            self._pending = target
            self._pending_since = now
            return
        if (now - self._pending_since) * 1000.0 >= self._debounce_ms:
            self._pending = None
            self._switch(target)

    def _switch(self, pid):
        _log.info("auto-switch: applying profile %s", pid)
        self._apply(pid)
        self.switched.emit(pid)
