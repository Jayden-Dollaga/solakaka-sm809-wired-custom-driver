"""Offline regression tests for UI smoothness work.

Covers deferred profile persistence (one batched table write instead of three
blocking ones), the cheap summary path used by the 200 ms auto-switch poll and
the combo/tray menus, no-op macro adoption, and no-op UI restyles.
"""

import shutil
from types import SimpleNamespace

import pytest

from app.autoswitch import AutoSwitcher
from app.macro_store import MacroStore
from app.profile_store import ProfileStore


@pytest.fixture
def seeded_store(tmp_path):
    from wired.paths import SEED_DIR

    dest = tmp_path / "data"
    shutil.copytree(SEED_DIR, dest)
    return ProfileStore(path=str(tmp_path / "profiles.json"), data_dir=dest)


# ---------------------------------------------------------------------------
# Deferred persistence
# ---------------------------------------------------------------------------
def test_deferred_config_edit_writes_once_on_flush(seeded_store, tmp_path):
    store = seeded_store
    pid = store.active_id
    writes = []
    real = store.data.save_profiles
    store.data.save_profiles = lambda: (writes.append(1), real())[1]

    cfg = store.config(pid)
    cfg["lighting"]["brightness"] = 77
    store.set_config(pid, cfg, persist=False)

    # memory is updated immediately, the 1.65 MB table is not written
    assert writes == []
    assert store.profiles_dirty
    assert store.data.profiles[store.index_of(pid)].brightness == 77

    store.flush()
    assert len(writes) == 1
    assert not store.profiles_dirty
    # the portable JSON mirror is refreshed in the same flush
    assert '"brightness": 77' in (tmp_path / "profiles.json").read_text()

    # a second flush is a no-op
    store.flush()
    assert len(writes) == 1


def test_default_set_config_still_persists_immediately(seeded_store):
    store = seeded_store
    pid = store.active_id
    cfg = store.config(pid)
    cfg["polling_hz"] = 500
    store.set_config(pid, cfg)
    assert not store.profiles_dirty
    assert ProfileStore(path=str(store.path),
                        data_dir=store.data_dir).config(pid)["polling_hz"] == 500


def test_apply_relies_on_service_persist(seeded_store):
    """ProfileStore.apply must not write the table itself: the service's
    persist=True pass already writes the same bytes."""
    store = seeded_store
    pid = store.active_id
    writes = []
    real = store.data.save_profiles
    store.data.save_profiles = lambda: (writes.append(1), real())[1]

    class FakeService:
        def apply(self, prof, apply_windows=True, persist=True):
            self.persist = persist
            return SimpleNamespace(ok=True, warnings=[])

    svc = FakeService()
    cfg = store.config(pid)
    cfg["lighting"]["brightness"] = 42
    store.apply(pid, svc, config=cfg)

    assert svc.persist is True
    assert writes == []                     # the (fake) service owns the write
    assert not store.profiles_dirty


def test_embedded_macros_scans_raw_records(seeded_store):
    """Startup adoption reads the raw button table (no full config build)."""
    store = seeded_store
    pid = store.active_id
    cfg = store.config(pid)
    cfg["buttons"][0] = {
        "macro": f"dev:{pid}:0",
        "name": "Adopted",
        "playmode": 2,
        "repeat": 3,
        "events": [
            {"type": "key", "keycode": 0x04, "down": True, "next_delay": 10},
            {"type": "key", "keycode": 0x04, "down": False, "next_delay": 0},
        ],
    }
    store.set_config(pid, cfg)

    found = [m for m in store.embedded_macros()
             if m[0] == f"dev:{pid}:0"]
    assert found
    mid, name, events = found[0]
    assert name == "Adopted"
    assert events[0]["keycode"] == 0x04


# ---------------------------------------------------------------------------
# Cheap summaries
# ---------------------------------------------------------------------------
def test_summaries_skip_config_conversion(seeded_store):
    store = seeded_store
    first = store.summaries()[0]
    assert "config" not in first
    assert {"id", "name", "match_rules", "created", "index"} <= set(first)

    pid = first["id"]
    store.set_match_rules(pid, [{"exe": "game.exe"}])
    assert store.match_targets()[0] == {
        "id": pid, "match_rules": [{"exe": "game.exe"}]}


def test_autoswitch_poll_uses_match_targets():
    applied = []

    class Store:
        def match_targets(self):
            return [{"id": "p-game",
                     "match_rules": [{"exe": "game.exe"}]}]

        def all(self):                       # must never be called
            raise AssertionError("poll rebuilt every full profile config")

    class Watcher:
        def current(self):
            return ("game.exe", "Game", "C:/Games/game.exe")

    auto = AutoSwitcher(Store(), lambda pid: applied.append(pid),
                        lambda: None, watcher=Watcher(), debounce_ms=0)
    auto.set_base("p-base")
    auto._enabled = True                     # no timer needed for a direct poll
    auto.poll()
    assert applied == ["p-game"]


# ---------------------------------------------------------------------------
# No-op writes / restyles
# ---------------------------------------------------------------------------
def test_macro_add_with_id_only_saves_on_change(tmp_path):
    store = MacroStore(path=str(tmp_path / "macros.json"))
    writes = []
    real = store.save
    store.save = lambda: (writes.append(1), real())[1]

    store.add_with_id("dev:p:0", "Macro", [{"type": "key", "keycode": 4}])
    assert len(writes) == 1                  # created
    store.add_with_id("dev:p:0", "Macro", [{"type": "key", "keycode": 4}])
    assert len(writes) == 1                  # unchanged -> no disk write
    store.add_with_id("dev:p:1", "Other", [{"type": "key", "keycode": 5}],
                      persist=False)
    assert len(writes) == 1                  # bulk adoption defers
    store.save_if_dirty()
    assert len(writes) == 2
    store.save_if_dirty()
    assert len(writes) == 2                  # nothing pending any more


def test_dpi_highlight_and_segmented_are_noops_when_unchanged():
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication
    from app.panels.dpi_panel import DpiPanel
    from app.widgets.controls import Segmented

    app = QApplication.instance() or QApplication([])

    panel = DpiPanel()
    calls = []
    # wrap after construction: the initial highlight is already applied
    for i, row in enumerate(panel.rows):
        orig = row.set_active

        def wrapped(active, idx=i, fn=orig):
            calls.append((idx, active))
            fn(active)

        row.set_active = wrapped

    panel.set_active_stage(1)                # already active (factory default)
    assert calls == []
    panel.set_active_stage(2)                # real switch: two rows repolish
    assert calls == [(1, False), (2, True)]

    seg = Segmented([("a", 1), ("b", 2)], value=1)
    repaints = []
    real_restyle = seg._restyle
    seg._restyle = lambda: (repaints.append(1), real_restyle())[1]
    seg.set_value(1)                         # unchanged
    assert repaints == []
    seg.set_value(2)
    assert repaints == [1]
    app.processEvents()
