"""
app.autoswitch -- per-app profile auto-switching (Milestone 3 step 3, the
headline feature; the official software has NO auto-switch).

Watches the foreground window and switches the active mouse profile by rule.

- The profile on the mouse is STICKY: whatever is applied stays applied when
  focus moves to a window that no profile claims (desktop, Explorer, Chrome,
  the studio itself).  There is no revert-to-base bounce, which used to look
  like "it applied a profile with no apps attached" every time an unruled
  window was focused.
- When the foreground app matches a profile's rule, switch to that profile.
- The last rule-matched profile stays until another rule matches, even after
  the game is closed or alt-tabbed away.  The manual base is only used when
  auto-switch is switched OFF (then the studio returns to what the user picked).

Rules live on each profile as `match_rules = [{"exe": "game.exe", "title": None},
...]`. First match in PROFILE LIST ORDER wins (reorder profiles to set priority).
A switch only fires when the target differs from what is currently applied, so a
steady foreground never re-pushes config to the device.

A rule's full `path` is a PREFERENCE, not a hard requirement: the picker adds
one when several running windows share an exe name (or for UWP hosts), but
launchers like Bloxstrap move the exe into a new versioned folder on every
update, and an elevated/anti-cheat game may deny the path entirely.  Matching
therefore tries rules with every condition first, then retries ignoring `path`,
so a stale or unreadable path cannot silently disable a rule.

Alt-Tab and minimize are just foreground changes: from one game to another the
profile follows the window actually in front. While Windows reports no
foreground window (a minimize/Alt-Tab transition), the current profile is held
rather than bouncing through the base and switching twice.

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
class _WinApi:
    """ctypes bindings for the handful of Windows calls detection needs.

    Building ``PROCESSENTRY32W`` and assigning ``argtypes``/``restype`` on
    every poll (and every picker refresh) is pure overhead, so it happens once.
    Pinning the prototypes also makes the 64-bit ``HWND`` parameters explicit:
    without them ctypes narrows them to a C int, which can truncate a handle.
    """

    def __init__(self):
        import ctypes
        from ctypes import wintypes

        self.ctypes = ctypes
        self.wintypes = wintypes
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.user32 = ctypes.WinDLL("user32", use_last_error=True)

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

        self.PROCESSENTRY32W = PROCESSENTRY32W
        self.WNDENUMPROC = ctypes.WINFUNCTYPE(
            wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        k = self.kernel32
        u = self.user32
        k.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        k.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k.Process32FirstW.argtypes = [wintypes.HANDLE,
                                      ctypes.POINTER(PROCESSENTRY32W)]
        k.Process32FirstW.restype = wintypes.BOOL
        k.Process32NextW.argtypes = [wintypes.HANDLE,
                                     ctypes.POINTER(PROCESSENTRY32W)]
        k.Process32NextW.restype = wintypes.BOOL
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        k.CloseHandle.restype = wintypes.BOOL
        k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL,
                                  wintypes.DWORD]
        k.OpenProcess.restype = wintypes.HANDLE
        k.QueryFullProcessImageNameW.argtypes = [
            wintypes.HANDLE, wintypes.DWORD,
            wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        k.QueryFullProcessImageNameW.restype = wintypes.BOOL

        u.GetForegroundWindow.restype = wintypes.HWND
        u.GetForegroundWindow.argtypes = []
        u.GetWindowTextLengthW.argtypes = [wintypes.HWND]
        u.GetWindowTextLengthW.restype = ctypes.c_int
        u.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR,
                                     ctypes.c_int]
        u.GetWindowTextW.restype = ctypes.c_int
        u.GetWindowThreadProcessId.argtypes = [
            wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
        u.GetWindowThreadProcessId.restype = wintypes.DWORD
        u.IsWindowVisible.argtypes = [wintypes.HWND]
        u.IsWindowVisible.restype = wintypes.BOOL
        u.EnumWindows.argtypes = [self.WNDENUMPROC, wintypes.LPARAM]
        u.EnumWindows.restype = wintypes.BOOL
        get_long = getattr(u, "GetWindowLongPtrW", None)
        if get_long is not None:
            get_long.argtypes = [wintypes.HWND, ctypes.c_int]
            get_long.restype = ctypes.c_longlong
        else:
            u.GetWindowLongW.argtypes = [wintypes.HWND, ctypes.c_int]
            u.GetWindowLongW.restype = ctypes.c_long
        self.get_long = get_long or u.GetWindowLongW


_WIN_API = None


def _win_api():
    global _WIN_API
    if _WIN_API is None:
        _WIN_API = _WinApi()
    return _WIN_API


class ForegroundWatcher:
    """Returns (exe_basename_lower, window_title, full_path) for the focused
    window, or (None, None, None) if it can't be determined. Windows impl; other
    platforms return Nones until the port lands. The full path lets rules tell
    apart same-named exes (e.g. many UE/Unity games ship Client-Win64-Shipping.exe).

    The exe name comes from a Toolhelp process snapshot -- the same source Task
    Manager uses -- so the game process is never opened. The image path is only
    queried when a rule actually needs it (`need_path=True`), and the result is
    cached per process id: a steady foreground causes no repeated handle opens,
    which keeps the detection non-invasive for anti-cheat-protected games.

    Likewise the window title is only read when some rule matches on one
    (`need_title=True`), so the common exe-only setup costs one foreground
    query plus the cached process id per poll.
    """

    def __init__(self):
        self._impl = _win_foreground if os.name == "nt" else None
        self._cache = {}

    def current(self, need_path=False, need_title=True):
        if self._impl is None:
            return (None, None, None)
        try:
            return self._impl(bool(need_path), bool(need_title), self._cache)
        except Exception:
            return (None, None, None)


def _snapshot_entries(api):
    """Yield ``(pid, exe_name)`` for every process, Task Manager style.

    Uses CreateToolhelp32Snapshot, which lists process names without opening
    any process. That is the least invasive way to identify a running game and
    avoids touching anti-cheat-protected processes. Yields nothing when the
    snapshot cannot be created.
    """
    ctypes, wintypes = api.ctypes, api.wintypes
    TH32CS_SNAPPROCESS = 0x00000002
    snap = api.kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
    invalid = ctypes.c_void_p(-1).value
    if not snap or snap == invalid:
        return
    try:
        entry = api.PROCESSENTRY32W()
        entry.dwSize = ctypes.sizeof(api.PROCESSENTRY32W)
        if not api.kernel32.Process32FirstW(snap, ctypes.byref(entry)):
            return
        while True:
            name = (entry.szExeFile or "").strip().lower()
            if name:
                yield (entry.th32ProcessID, name)
            if not api.kernel32.Process32NextW(snap, ctypes.byref(entry)):
                return
    finally:
        api.kernel32.CloseHandle(snap)


def _process_exe_name(api, pid):
    """Toolhelp exe name for `pid` without opening the process.

    OpenProcess can be denied for a game running elevated (or behind an
    anti-cheat), which used to leave exe/path empty and made every rule fail.
    A process snapshot only needs the exe name, which Windows exposes anyway.
    """
    for entry_pid, name in _snapshot_entries(api):
        if entry_pid == pid:
            return name
    return None


def _pid_app(pid, need_path=True):
    """(exe_basename_lower, full_path) for a process, or (None, None).

    The exe name is always available from a Toolhelp snapshot (no handle on the
    target process, like Task Manager's process list). The full image path needs
    OpenProcess/QueryFullProcessImageName, which is only attempted when a rule
    has a path condition; an elevated/anti-cheat game may deny it, in which case
    the exe name still comes back from the snapshot.
    """
    api = _win_api()
    ctypes = api.ctypes
    wintypes = api.wintypes
    full_path = None
    if need_path:
        PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
        handle = api.kernel32.OpenProcess(
            PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
        if handle:
            try:
                size = wintypes.DWORD(32768)
                nbuf = ctypes.create_unicode_buffer(size.value)
                if api.kernel32.QueryFullProcessImageNameW(
                        handle, 0, nbuf, ctypes.byref(size)):
                    full_path = nbuf.value
            finally:
                api.kernel32.CloseHandle(handle)
    exe = os.path.basename(full_path).lower() if full_path else None
    if not exe:
        exe = _process_exe_name(api, pid)
    return (exe, full_path)


def _win_foreground(need_path=False, need_title=True, cache=None):
    api = _win_api()
    ctypes = api.ctypes
    wintypes = api.wintypes

    hwnd = api.user32.GetForegroundWindow()
    if not hwnd:
        return (None, None, None)

    # Window title: only when a rule can use it. GetWindowText allocates a
    # buffer and copies the string, so skipping it saves two user32 calls on
    # every poll for the common exe-only rule.
    title = ""
    if need_title:
        length = api.user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(max(0, length) + 1)
        api.user32.GetWindowTextW(hwnd, buf, length + 1)
        title = buf.value or ""

    # owning process id -> exe name / full path
    pid = wintypes.DWORD()
    api.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    cached = (cache or {}).get("proc")
    if (cached and cached["pid"] == pid.value
            and (not need_path or cached["path_tried"])):
        exe, full_path = cached["exe"], cached["path"]
    else:
        exe, full_path = _pid_app(pid.value, need_path)
        if cache is not None:
            # path_tried remembers a denied path query so a steady anti-cheat
            # game is not opened again on every 200 ms poll.
            cache["proc"] = {"pid": pid.value, "exe": exe,
                             "path": full_path, "path_tried": bool(need_path)}
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


def list_processes():
    """Running process names, the way Task Manager lists them.

    The app picker uses this for programs that have no visible window (game
    launchers, background clients) and for anti-cheat titles whose window may
    be protected. A Toolhelp snapshot exposes the name without opening the
    process, so every entry builds an exe-only rule. Empty off Windows.
    """
    if os.name != "nt":
        return []
    try:
        return _win_list_processes()
    except Exception:
        _log.debug("process enumeration failed", exc_info=True)
        return []


def _win_list_processes():
    api = _win_api()
    counts, first_pid = {}, {}
    for pid, name in _snapshot_entries(api):
        if not pid or name in ("system", "[system process]", "idle",
                               "system idle process"):
            continue
        counts[name] = counts.get(name, 0) + 1
        first_pid.setdefault(name, pid)
    return [{"title": name, "exe": name, "path": None,
             "pid": first_pid[name], "instances": counts[name],
             "process": True}
            for name in sorted(counts)]



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
    if exe in UWP_HOST_EXES and not app.get("process"):
        # A process-list entry has no window title to copy, so it stays
        # exe-only; a real UWP window entry also matches its title.
        rule["path"] = path or None
        rule["title"] = title.lower() or None
        return rule
    same = [a for a in apps
            if (a.get("exe") or "").strip().lower() == exe]
    if len(same) > 1:
        rule["path"] = path or None
    return rule


def _win_list_apps():
    api = _win_api()
    ctypes = api.ctypes
    wintypes = api.wintypes
    user32 = api.user32

    GWL_EXSTYLE = -20
    WS_EX_TOOLWINDOW = 0x00000080
    get_long = api.get_long

    # shell surfaces and IME helpers show up as invisible system windows
    skip_titles = {"program manager", "default ime", "msctfime ui",
                   "windows input experience", "microsoft text input application"}

    apps = {}
    seen_pids = {}

    @api.WNDENUMPROC
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

    user32.EnumWindows(_visit, 0)
    return sorted(apps.values(), key=lambda a: a["title"].lower())





# --- rule matching (pure) ----------------------------------------------------
def rule_matches(rule, exe, title, path=None, require_path=True):
    """A rule matches when ALL of its specified (non-empty) conditions hold:
      - exe:   basename equals the foreground exe (case-insensitive)
      - path:  substring of the foreground full path (case-insensitive) -- this
               distinguishes same-named exes (e.g. UE/Unity Client-Win64-Shipping.exe)
      - title: substring of the foreground window title (case-insensitive)
    A rule with no conditions set never matches.

    ``require_path=False`` ignores the path condition while still checking
    exe/title; :func:`match_profile` uses it as the fallback pass so a stale
    versioned folder (Bloxstrap) or an unreadable path (elevated game) does
    not disable an otherwise valid rule.
    """
    want_exe = (rule.get("exe") or "").strip().lower()
    want_path = (rule.get("path") or "").strip().lower()
    want_title = (rule.get("title") or "").strip().lower()
    if not (want_exe or want_path or want_title):
        return False
    if want_exe and (not exe or exe.lower() != want_exe):
        return False
    if require_path and want_path and (not path or want_path not in path.lower()):
        return False
    if want_title and (not title or want_title not in title.lower()):
        return False
    return True


def _rule_path_unavailable(want_path, foreground_path):
    """True when a stored path condition cannot be applied any more.

    - the watcher could not read the foreground image name (elevated game);
    - the stored absolute path no longer exists (a launcher moved the exe into
      a new versioned folder, e.g. Bloxstrap).  Bare fragments (a user-typed
      ``"mygame"`` substring) are never treated as stale.
    """
    if not foreground_path:
        return True
    if want_path and os.path.isabs(want_path):
        try:
            return not os.path.exists(want_path)
        except OSError:
            return False
    return False


def match_profile(profiles, exe, title, path=None):
    """First profile (in list order) whose rule matches, or None.

    Profile order decides priority.  A rule's stored path is honoured first;
    when that path can no longer be checked (no readable foreground path, or
    the absolute path is gone because the app moved to a new versioned folder)
    the rule is retried on exe/title alone.  Two same-named games that both
    still exist keep their path separation.
    """
    for p in profiles:
        for r in p.get("match_rules", []):
            if rule_matches(r, exe, title, path):
                return p["id"]
    for p in profiles:
        for r in p.get("match_rules", []):
            want_path = (r.get("path") or "").strip()
            if not want_path:
                continue        # would already have matched above
            # A path-only rule must not turn into a wildcard once its folder is
            # gone: there is nothing left to identify the app by.
            if not ((r.get("exe") or "").strip()
                    or (r.get("title") or "").strip()):
                continue
            if not _rule_path_unavailable(want_path, path):
                continue
            if rule_matches(r, exe, title, path, require_path=False):
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
        """The manual selection that auto-switch returns to when turned OFF.

        It is not a fallback for unmatched apps any more: the profile that is
        applied stays applied until another rule matches.
        """
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

    def stop(self):
        """Stop watching without touching the device.

        Used on real application shutdown: turning auto-switch off restores the
        manual profile, but quitting must leave the profile that is on the mouse
        alone (and must not queue an apply while the worker is shutting down).
        """
        self._enabled = False
        self._pending = None
        self._timer.stop()

    def poll(self):
        if not self._enabled:
            return
        # Only id + rules are needed for matching. A ProfileStore exposes
        # ``match_targets`` so the 200 ms poll does not rebuild every profile's
        # full button/DPI/lighting config; simpler stores still work via all().
        source = getattr(self._store, "match_targets", None)
        targets = source() if callable(source) else self._store.all()
        # Ask for the full image path only when some rule uses one. Without a
        # path rule the watcher can identify the app from the process snapshot
        # alone, never opening the game process (anti-cheat friendly).  The
        # window title is read on the same principle.
        rules = [r for p in targets for r in p.get("match_rules", [])]
        need_path = any((r.get("path") or "").strip() for r in rules)
        need_title = any((r.get("title") or "").strip() for r in rules)
        exe, title, path = self._watcher.current(
            need_path=need_path, need_title=need_title)
        if (exe, path) != self._last_fg:
            self._last_fg = (exe, path)
            _log.debug("foreground: %s | %s", exe or "(unknown)",
                       path or "(no path)")
        if not exe:
            # Windows reports no foreground window for a moment while a game is
            # minimized or an Alt-Tab switch is in flight. Hold the profile that
            # is applied and drop any pending target: treating the gap as "no
            # match" would revert to the base and immediately switch again --
            # two full mouse writes (and a visible flash) per app change.
            self._pending = None
            return
        target = match_profile(targets, exe, title, path)
        if not target:
            # No profile claims this window. Hold whatever is on the mouse:
            # the user expects the last applied profile to stay, and reverting
            # here is what silently applied a rule-less profile on every
            # desktop/Explorer/chat window.
            self._pending = None
            return
        # already on the right profile -> nothing pending
        if target == self._get_applied():
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
