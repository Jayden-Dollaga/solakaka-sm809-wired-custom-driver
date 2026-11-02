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

    def set(self, exe, title="", path=None):
        self.value = (exe, title, path)

    def current(self):
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


def test_switcher_switches_on_match_and_reverts_to_base():
    watcher = FakeWatcher()
    sw, applied = make_switcher(watcher)
    sw.set_enabled(True)              # base already applied -> nothing to do
    assert applied[0] == "base"

    watcher.set("game.exe", "My Game", "C:/games/game.exe")
    sw.poll()
    assert applied[0] == "game"

    watcher.set("explorer.exe", "Desktop", "C:/Windows/explorer.exe")
    sw.poll()
    assert applied[0] == "base"
    sw.set_enabled(False)


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
    sw.poll()                        # target changed back to base -> nothing
    assert applied[0] == "base"
    sw.set_enabled(False)


def test_disabling_auto_switch_reverts_to_base():
    watcher = FakeWatcher("game.exe", "My Game", "C:/games/game.exe")
    sw, applied = make_switcher(watcher)
    sw.set_enabled(True)
    assert applied[0] == "game"
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
