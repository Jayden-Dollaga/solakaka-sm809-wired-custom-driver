"""Auto-switch rules, the switcher loop, and the custom-apps panels.

The foreground watcher is faked everywhere: these tests must never look at the
real desktop, and no USB traffic is generated.
"""

import time

import pytest

from app.autoswitch import AutoSwitcher, match_profile, rule_for_app, rule_matches

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from app.panels.autoswitch_panel import AutoSwitchPanel
from app.panels.profiles_panel import ProfilesPanel


# --- pure rule matching ------------------------------------------------------
def test_empty_rule_never_matches():
    assert not rule_matches({}, "game.exe", "Game", "C:/games/game.exe")
    assert not rule_matches({"exe": "", "path": "", "title": ""},
                            "game.exe", "Game", "C:/games/game.exe")


def test_exe_rule_is_case_insensitive_and_requires_all_fields():
    rule = {"exe": "Game.EXE"}
    assert rule_matches(rule, "game.exe", "Anything", None)
    assert not rule_matches(rule, "other.exe", "Anything", None)
    both = {"exe": "game.exe", "title": "night"}
    assert rule_matches(both, "game.exe", "NIGHT raid", None)
    assert not rule_matches(both, "game.exe", "menu", None)


def test_path_rule_distinguishes_same_named_exes():
    rule = {"exe": "client-win64-shipping.exe", "path": "mygame"}
    assert rule_matches(rule, "client-win64-shipping.exe", "",
                        r"C:\Games\MyGame\Client-Win64-Shipping.exe")
    assert not rule_matches(rule, "client-win64-shipping.exe", "",
                            r"C:\Games\Other\Client-Win64-Shipping.exe")


def test_first_matching_profile_in_list_order_wins():
    profiles = [
        {"id": "a", "match_rules": [{"exe": "game.exe"}]},
        {"id": "b", "match_rules": [{"exe": "game.exe"}]},
        {"id": "c", "match_rules": [{"exe": "other.exe"}]},
    ]
    assert match_profile(profiles, "game.exe", "", None) == "a"
    assert match_profile(profiles, "other.exe", "", None) == "c"
    assert match_profile(profiles, "nothing.exe", "", None) is None


def test_a_stale_versioned_path_still_matches_by_exe():
    """Bloxstrap moves RobloxPlayerBeta.exe into a new version folder.

    The picker stored the old folder because two Roblox windows were running;
    before this fix the rule silently stopped matching after an update and
    auto-switch looked broken.
    """
    rule = {"exe": "robloxplayerbeta.exe",
            "path": r"c:\users\me\appdata\local\bloxstrap\versions\version-old"}
    profiles = [{"id": "ttk", "match_rules": [rule]},
                {"id": "other", "match_rules": []}]
    new_path = (r"C:\Users\Me\AppData\Local\Bloxstrap\Versions"
                r"\version-new\RobloxPlayerBeta.exe")
    assert rule_matches(rule, "robloxplayerbeta.exe", "Roblox", new_path) is False
    assert match_profile(profiles, "robloxplayerbeta.exe", "Roblox",
                         new_path) == "ttk"


def test_an_unreadable_path_does_not_disable_a_path_rule():
    """Anti-cheat can deny the full image name; the exe name still arrives."""
    rule = {"exe": "robloxplayerbeta.exe", "path": "version-"}
    profiles = [{"id": "ttk", "match_rules": [rule]}]
    assert match_profile(profiles, "robloxplayerbeta.exe", "Roblox", None) == "ttk"


def test_a_path_rule_does_not_hide_a_later_exe_rule():
    """Profile order still decides; the path pass is only about staleness."""
    profiles = [
        {"id": "exact", "match_rules": [
            {"exe": "client-win64-shipping.exe", "path": r"c:\games\b\client"}]},
        {"id": "loose", "match_rules": [{"exe": "client-win64-shipping.exe"}]},
    ]
    assert match_profile(profiles, "client-win64-shipping.exe", "",
                         r"C:\Games\B\Client-Win64-Shipping.exe") == "exact"
    # ...and an unrelated folder falls through to the exe-only profile.
    assert match_profile(profiles, "client-win64-shipping.exe", "",
                         r"C:\Games\C\Client-Win64-Shipping.exe") == "loose"


def test_a_path_only_rule_never_turns_into_a_wildcard():
    """With no exe/title left, a vanished folder must match nothing."""
    rule = {"path": r"C:\Games\Old\Client-Win64-Shipping.exe"}
    profiles = [{"id": "p", "match_rules": [rule]}]
    assert match_profile(profiles, "client-win64-shipping.exe", "",
                         r"C:\Games\Old\Client-Win64-Shipping.exe") == "p"
    assert match_profile(profiles, "client-win64-shipping.exe", "",
                         r"C:\Games\New\Client-Win64-Shipping.exe") is None
    assert match_profile(profiles, "client-win64-shipping.exe", "", None) is None


# --- rules built from the running-app picker ---------------------------------
APPS = [
    {"title": "Roblox", "exe": "robloxplayerbeta.exe",
     "path": r"C:\Apps\Roblox\RobloxPlayerBeta.exe"},
    {"title": "Game A", "exe": "client-win64-shipping.exe",
     "path": r"C:\Games\A\Client-Win64-Shipping.exe"},
    {"title": "Game B", "exe": "client-win64-shipping.exe",
     "path": r"C:\Games\B\Client-Win64-Shipping.exe"},
    {"title": "Calculator", "exe": "applicationframehost.exe",
     "path": r"C:\Windows\System32\ApplicationFrameHost.exe"},
]


def test_rule_for_app_uses_exe_alone_when_it_is_unique():
    assert rule_for_app(APPS, APPS[0]) == {
        "exe": "robloxplayerbeta.exe", "path": None, "title": None}


def test_rule_for_app_adds_path_for_same_named_exes():
    assert rule_for_app(APPS, APPS[1]) == {
        "exe": "client-win64-shipping.exe",
        "path": r"C:\Games\A\Client-Win64-Shipping.exe",
        "title": None}


def test_rule_for_app_adds_title_for_uwp_hosts():
    rule = rule_for_app(APPS, APPS[3])
    assert rule["exe"] == "applicationframehost.exe"
    assert rule["title"] == "calculator"


def test_rule_for_app_without_an_exe_is_empty():
    assert rule_for_app(APPS, {"title": "Ghost"}) == {
        "exe": None, "path": None, "title": None}



# --- the switcher loop -------------------------------------------------------
class FakeWatcher:
    def __init__(self, exe=None, title="", path=None):
        self.value = (exe, title, path)
        self.last_need_path = None
        self.last_need_title = None

    def set(self, exe, title="", path=None):
        self.value = (exe, title, path)

    def current(self, need_path=False, need_title=True):
        self.last_need_path = need_path
        self.last_need_title = need_title
        return self.value


class FakeStore:
    def __init__(self, profiles):
        self._profiles = profiles

    def all(self):
        return self._profiles


PROFILES = [
    {"id": "game", "match_rules": [{"exe": "game.exe"}]},
    {"id": "base", "match_rules": []},
]


def make_switcher(watcher, debounce=0, applied=None):
    store = FakeStore(PROFILES)
    applied = applied if applied is not None else ["base"]

    def apply(pid):
        applied[0] = pid

    sw = AutoSwitcher(store, apply, lambda: applied[0],
                      watcher=watcher, interval_ms=10_000,
                      debounce_ms=debounce)
    sw.set_base("base")
    return sw, applied


def test_switcher_keeps_the_last_match_when_focus_leaves():
    """No rule for the focused window -> keep what is on the mouse.

    Reverting to the manual base here used to apply a rule-less profile every
    time the user touched the desktop, Explorer or a chat window.
    """
    watcher = FakeWatcher()
    sw, applied = make_switcher(watcher)
    sw.set_enabled(True)              # base already applied -> nothing to do
    assert applied[0] == "base"

    watcher.set("game.exe", "My Game", "C:/games/game.exe")
    sw.poll()
    assert applied[0] == "game"

    watcher.set("explorer.exe", "Desktop", "C:/Windows/explorer.exe")
    sw.poll()
    assert applied[0] == "game"       # the last applied profile stays
    sw.poll()
    assert applied[0] == "game"

    # turning auto-switch off is what restores the manual base
    sw.set_enabled(False)
    assert applied[0] == "base"


def test_foreground_path_is_read_only_when_a_rule_needs_it():
    """Exe-only rules never open the game process (anti-cheat safety)."""
    watcher = FakeWatcher("game.exe", "My Game", "C:/games/game.exe")
    sw, _ = make_switcher(watcher)
    sw.set_enabled(True)
    assert watcher.last_need_path is False

    path_rule = [{"id": "p", "match_rules": [
        {"exe": "game.exe", "path": r"C:\Games\MyGame"}]}]
    switcher = AutoSwitcher(FakeStore(path_rule),
                            lambda pid: None, lambda: "p",
                            watcher=watcher, interval_ms=10_000,
                            debounce_ms=0)
    switcher.set_enabled(True)
    assert watcher.last_need_path is True
    switcher.set_enabled(False)


def test_window_title_is_read_only_when_a_rule_needs_it():
    """A title condition is the only reason to copy the window caption."""
    watcher = FakeWatcher("game.exe", "My Game", "C:/games/game.exe")
    sw, _ = make_switcher(watcher)
    sw.set_enabled(True)
    assert watcher.last_need_title is False

    title_rule = [{"id": "p", "match_rules": [
        {"exe": "game.exe", "title": "my game"}]}]
    switcher = AutoSwitcher(FakeStore(title_rule),
                            lambda pid: None, lambda: "p",
                            watcher=watcher, interval_ms=10_000,
                            debounce_ms=0)
    switcher.set_enabled(True)
    assert watcher.last_need_title is True
    assert watcher.last_need_path is False
    switcher.set_enabled(False)


def test_steady_foreground_does_not_reapply():
    watcher = FakeWatcher("game.exe", "My Game", "C:/games/game.exe")
    sw, applied = make_switcher(watcher)
    calls = []
    sw._apply = lambda pid: (calls.append(pid), applied.__setitem__(0, pid))
    sw.set_enabled(True)
    assert calls == ["game"]
    sw.poll()
    sw.poll()
    assert calls == ["game"]
    sw.set_enabled(False)


def test_debounce_waits_for_a_stable_foreground():
    watcher = FakeWatcher()
    sw, applied = make_switcher(watcher, debounce=60)
    sw.set_enabled(True)
    assert applied[0] == "base"

    watcher.set("game.exe", "My Game", "C:/games/game.exe")
    sw.poll()                        # starts the timer, no apply yet
    assert applied[0] == "base"
    time.sleep(0.08)
    sw.poll()
    assert applied[0] == "game"
    sw.set_enabled(False)


def test_debounce_cancels_when_focus_leaves_again():
    watcher = FakeWatcher()
    sw, applied = make_switcher(watcher, debounce=60)
    sw.set_enabled(True)
    watcher.set("game.exe", "My Game", "C:/games/game.exe")
    sw.poll()
    watcher.set("explorer.exe", "Desktop", "C:/Windows/explorer.exe")
    time.sleep(0.08)
    sw.poll()                        # no rule for the desktop -> pending cleared
    assert applied[0] == "base"
    sw.set_enabled(False)


def test_disabling_auto_switch_reverts_to_base():
    watcher = FakeWatcher("game.exe", "My Game", "C:/games/game.exe")
    sw, applied = make_switcher(watcher)
    sw.set_enabled(True)
    assert applied[0] == "game"
    sw.set_enabled(False)
    assert applied[0] == "base"


def test_stopping_for_shutdown_leaves_the_mouse_profile_alone():
    """Quitting must not queue a base-profile write as the worker shuts down."""
    watcher = FakeWatcher("game.exe", "My Game", "C:/games/game.exe")
    sw, applied = make_switcher(watcher)
    sw.set_enabled(True)
    assert applied[0] == "game"
    sw.stop()
    assert applied[0] == "game"
    assert not sw.is_enabled()
    sw.poll()                         # a stray timer tick is a no-op now
    assert applied[0] == "game"


def test_alt_tab_and_minimize_follow_the_app_in_front():
    """Game -> Alt-Tab/minimize -> another game -> desktop -> back.

    This is the user's real scenario: playing Minecraft, Alt-Tabbing to Delta
    Force or Roblox, and back. Each foreground app selects its own profile; the
    moment Windows reports no foreground window during a minimize/Alt-Tab does
    NOT count as "no match" (that would bounce through the base and write the
    mouse twice per switch).
    """
    profiles = [
        {"id": "minecraft", "match_rules": [{"exe": "javaw.exe"}]},
        {"id": "delta", "match_rules": [{"exe": "deltaforce.exe"}]},
        {"id": "roblox", "match_rules": [{"exe": "robloxplayerbeta.exe"}]},
        {"id": "base", "match_rules": []},
    ]
    applied = ["base"]
    watcher = FakeWatcher("javaw.exe", "Minecraft", r"C:\Games\MC\javaw.exe")
    sw = AutoSwitcher(FakeStore(profiles),
                      lambda pid: applied.__setitem__(0, pid),
                      lambda: applied[0], watcher=watcher,
                      interval_ms=10_000, debounce_ms=0)
    sw.set_base("base")
    sw.set_enabled(True)
    assert applied[0] == "minecraft"

    # Alt-Tab straight into another game: that game's profile wins.
    watcher.set("deltaforce.exe", "Delta Force",
                r"C:\Games\Delta\DeltaForce.exe")
    sw.poll()
    assert applied[0] == "delta"

    watcher.set("robloxplayerbeta.exe", "Roblox",
                r"C:\Apps\Roblox\RobloxPlayerBeta.exe")
    sw.poll()
    assert applied[0] == "roblox"

    # Minimizing reports no foreground for a moment: hold, do not change.
    watcher.set(None, "", None)
    sw.poll()
    assert applied[0] == "roblox"

    # A real non-matching window (desktop/taskbar) also holds the last
    # profile; only a rule match moves the mouse.
    watcher.set("explorer.exe", "Program Manager", r"C:\Windows\explorer.exe")
    sw.poll()
    assert applied[0] == "roblox"

    # Restoring the game switches back to it.
    watcher.set("javaw.exe", "Minecraft", r"C:\Games\MC\javaw.exe")
    sw.poll()
    assert applied[0] == "minecraft"
    sw.set_enabled(False)
    assert applied[0] == "base"


# --- panels ------------------------------------------------------------------
@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app
    for widget in list(app.topLevelWidgets()):
        widget.close()
        widget.deleteLater()
    app.processEvents()
    app.quit()


PROFILE_LIST = [
    {"id": "p1", "name": "Desktop", "match_rules": []},
    {"id": "p2", "name": "Night Raid",
     "match_rules": [{"exe": "nikke.exe", "path": None, "title": None}]},
]


def test_autoswitch_panel_shows_apps_of_the_selected_profile(qapp):
    panel = AutoSwitchPanel()
    panel.set_profiles(PROFILE_LIST)

    assert panel.current_pid() == "p1"
    assert panel.profile_label.text() == "Apps for Desktop"
    assert panel.rules_list.count() == 0
    assert not panel.rules_empty.isHidden()

    panel.select_profile("p2")
    assert panel.current_pid() == "p2"
    assert panel.profile_label.text() == "Apps for Night Raid"
    assert panel.rules_list.count() == 1
    assert "nikke.exe" in panel.rules_list.item(0).text()
    assert panel.rules_empty.isHidden()

    # Enabling while NOTHING has a rule must not look on-but-idle silently.
    panel.set_profiles([{"id": "p1", "name": "Desktop", "match_rules": []}])
    panel.set_enabled_state(True)
    assert "never trigger" in panel.status.text()
    panel.set_enabled_state(False)
    assert panel.status.text() == ""
    panel.deleteLater()


def test_autoswitch_panel_adds_and_rejects_duplicate_rules(qapp):
    panel = AutoSwitchPanel()
    panel.set_profiles(PROFILE_LIST)
    emitted = []
    panel.rules_changed.connect(lambda pid, rules: emitted.append((pid, rules)))

    assert panel._add_rule("p1", {"exe": "  GAME.EXE "})

    pid, rules = emitted[-1]
    assert pid == "p1"
    assert rules == [{"exe": "game.exe", "path": None, "title": None}]

    # same rule again in any case/spacing is refused, not appended twice
    assert not panel._add_rule("p1", {"exe": "game.exe"})
    assert "already assigned" in panel.status.text()
    assert len(emitted[-1][1]) == 1
    panel.deleteLater()


def test_detect_captures_and_assigns_the_app(qapp):
    panel = AutoSwitchPanel()
    panel.set_profiles(PROFILE_LIST)
    panel.select_profile("p2")
    panel._watcher = FakeWatcher("game.exe", "My Game",
                                 "C:/Games/MyGame/game.exe")
    emitted = []
    panel.rules_changed.connect(lambda pid, rules: emitted.append((pid, rules)))
    detected = []
    panel.app_detected.connect(lambda exe, title: detected.append((exe, title)))

    panel._detect_pid = "p2"
    panel._capture()

    assert detected == [("game.exe", "My Game")]
    assert emitted, "detecting an app must assign it without a second click"
    pid, rules = emitted[-1]
    assert pid == "p2"
    assert rules[-1] == {"exe": "game.exe", "path": "c:/games/mygame/game.exe",
                          "title": None}
    assert "Detected game.exe" in panel.status.text()

    # capturing the same app again does not duplicate the rule
    before = panel.rules_list.count()
    panel._detect_pid = "p2"
    panel._capture()
    assert panel.rules_list.count() == before
    assert "already assigned" in panel.status.text()
    panel.deleteLater()


def test_remove_selected_rule_emits_change(qapp):
    panel = AutoSwitchPanel()
    panel.set_profiles(PROFILE_LIST)
    panel.select_profile("p2")
    emitted = []
    panel.rules_changed.connect(lambda pid, rules: emitted.append((pid, rules)))

    panel.rules_list.setCurrentRow(0)
    panel._remove()
    assert emitted[-1] == ("p2", [])
    panel.deleteLater()


def test_profiles_panel_follows_the_auto_switched_profile(qapp):
    """Opening a matched app must move this tab's marker and selection to the
    profile on the mouse, without turning it into a manual selection."""
    from PySide6.QtGui import QFont

    panel = ProfilesPanel()
    panel.set_profiles(PROFILE_LIST, active_id="p1")
    emitted = []
    panel.profile_selected.connect(emitted.append)
    assert panel.selected_id() == "p1"

    panel.show_active("p2")
    assert panel.selected_id() == "p2"
    assert panel.list.currentRow() == 1
    assert "nikke.exe" in panel.apps_hint.text()
    assert panel.list.item(1).font().weight() == QFont.DemiBold
    assert panel.list.item(0).font().weight() != QFont.DemiBold
    # a programmatic sync must NOT look like the user activating a profile
    assert emitted == []

    # focus left the game: the marker and row go back to the manual base
    panel.show_active("p1")
    assert panel.selected_id() == "p1"
    assert panel.list.item(0).font().weight() == QFont.DemiBold
    assert panel.list.item(1).font().weight() != QFont.DemiBold
    assert emitted == []
    panel.deleteLater()


def test_profiles_panel_shows_custom_apps_and_opens_manager(qapp):
    panel = ProfilesPanel()
    panel.set_profiles(PROFILE_LIST, active_id="p1")

    # "Night Raid" owns one app; select it and read the summary
    panel.list.setCurrentRow(1)
    assert "nikke.exe" in panel.apps_hint.text()

    panel.list.setCurrentRow(0)
    assert "No custom apps for Desktop" in panel.apps_hint.text()

    wanted = []
    panel.manage_apps_requested.connect(wanted.append)
    panel._on_manage_apps()
    assert wanted == ["p1"]

    # an edit made on the Auto-Switch tab updates this summary immediately
    panel.set_match_rules("p1", [{"exe": "newgame.exe", "path": None,
                                  "title": None}])
    assert "newgame.exe" in panel.apps_hint.text()
    panel.deleteLater()


def test_app_picker_browses_an_exe_from_disk(qapp, tmp_path):
    from app.panels.app_picker import AppPicker

    exe = tmp_path / "MyGame.exe"
    exe.write_bytes(b"MZ")
    dlg = AppPicker(apps=[])

    app = dlg._add_path(str(exe))
    assert app == {"title": "MyGame", "exe": "mygame.exe", "path": str(exe)}
    assert dlg.list.count() == 1
    assert dlg.list.currentItem().text().startswith("MyGame")
    # the exe is unique, so the rule survives the game being moved/updated
    assert dlg.selected_rule() == {
        "exe": "mygame.exe", "path": None, "title": None}

    # browsing an exe that is already listed reuses that entry
    before = dlg.list.count()
    dlg._add_path(str(exe))
    assert dlg.list.count() == before
    dlg.deleteLater()


def test_app_picker_filters_running_windows_and_builds_the_rule(qapp):
    from app.panels.app_picker import AppPicker

    dlg = AppPicker(apps=APPS)
    assert dlg.list.count() == len(APPS)
    assert "robloxplayerbeta.exe" in dlg.list.item(0).text()

    dlg.search.setText("roblox")
    qapp.processEvents()
    visible = [dlg.list.item(i) for i in range(dlg.list.count())
               if not dlg.list.item(i).isHidden()]
    assert len(visible) == 1
    assert dlg.selected_rule() == {
        "exe": "robloxplayerbeta.exe", "path": None, "title": None}

    dlg.search.setText("client-win64")
    qapp.processEvents()
    rule = dlg.selected_rule()
    assert rule["exe"] == "client-win64-shipping.exe"
    assert rule["path"] in (r"C:\Games\A\Client-Win64-Shipping.exe",
                            r"C:\Games\B\Client-Win64-Shipping.exe")

    dlg.search.setText("no-such-app")
    qapp.processEvents()
    assert not dlg.empty.isHidden()
    assert not dlg.ok_btn.isEnabled()

    dlg.search.clear()
    qapp.processEvents()
    assert dlg.ok_btn.isEnabled()
    dlg.deleteLater()


def test_app_picker_can_include_task_manager_processes(qapp):
    """Background processes are offered by name, without opening them."""
    from app.panels.app_picker import AppPicker

    procs = [
        {"title": "bloxstrap.exe", "exe": "bloxstrap.exe", "path": None,
         "pid": 10, "instances": 1, "process": True},
        {"title": "python.exe", "exe": "python.exe", "path": None,
         "pid": 11, "instances": 3, "process": True},
        # already has a window entry -> not duplicated
        {"title": "robloxplayerbeta.exe", "exe": "robloxplayerbeta.exe",
         "path": None, "pid": 12, "instances": 1, "process": True},
    ]
    dlg = AppPicker(apps=APPS, processes=procs)
    assert dlg.list.count() == len(APPS)      # processes are opt-in

    dlg.show_processes.setChecked(True)
    assert dlg.list.count() == len(APPS) + 2  # launcher + python only
    labels = [dlg.list.item(i).text() for i in range(dlg.list.count())]
    assert any("bloxstrap.exe" in t and "background process" in t
               for t in labels)
    assert any("python.exe" in t and "3 processes" in t for t in labels)

    dlg.search.setText("bloxstrap")
    qapp.processEvents()
    assert dlg.selected_rule() == {
        "exe": "bloxstrap.exe", "path": None, "title": None}

    # unticking restores the window-only list
    dlg.show_processes.setChecked(False)
    assert dlg.list.count() == len(APPS)
    dlg.deleteLater()


def test_admin_hint_only_shown_when_unelevated(qapp, monkeypatch):
    import app.panels.autoswitch_panel as panel_module

    monkeypatch.setattr(panel_module, "is_admin", lambda: False)
    panel = panel_module.AutoSwitchPanel()
    assert not panel.admin_hint.isHidden()
    panel.deleteLater()

    monkeypatch.setattr(panel_module, "is_admin", lambda: True)
    elevated = panel_module.AutoSwitchPanel()
    assert elevated.admin_hint.isHidden()
    elevated.deleteLater()
