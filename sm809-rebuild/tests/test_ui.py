"""Smoke tests for the tkinter interface.

These tests open a withdrawn Tk window. They are skipped on machines without a
display/Tk, so the rest of the suite still runs in headless environments.
"""

from __future__ import annotations

import time

import pytest


tkinter = pytest.importorskip("tkinter")


@pytest.fixture(scope="module")
def app(tmp_path_factory):
    try:
        probe = tkinter.Tk()
        probe.destroy()
    except tkinter.TclError:
        pytest.skip("no display available")

    import sm809.ui.app as app_module

    original_message = app_module.dialogs.show_message
    original_confirm = app_module.dialogs.ask_confirm
    app_module.dialogs.show_message = lambda *a, **k: None
    app_module.dialogs.ask_confirm = lambda *a, **k: True

    instance = app_module.App(demo=True, data_dir=tmp_path_factory.mktemp("ui-data"))
    instance.withdraw()
    instance.update()
    yield instance
    try:
        if instance.winfo_exists():
            instance._on_close()
    except tkinter.TclError:
        pass
    finally:
        app_module.dialogs.show_message = original_message
        app_module.dialogs.ask_confirm = original_confirm


def test_all_pages_switch(app):
    for key in ("keys", "performance", "light", "macro", "gun"):
        app._show_page(key)
        app.update()
        assert app._current_page == key
        assert app._pages[key].winfo_ismapped() or not app.winfo_ismapped()


def test_profile_operations(app):
    before = len(app.store.profiles)
    app._new_profile()
    app.update()
    assert len(app.store.profiles) == before + 1
    app.profile_name_var.set("Smoke test profile")
    app._commit_profile_name()
    app.update()
    assert app.store.profile.name == "Smoke test profile"

    app._duplicate_profile()
    app.update()
    assert len(app.store.profiles) == before + 2
    assert app.store.profile.name != "Smoke test profile"

    app._delete_profile()
    app.update()
    assert len(app.store.profiles) == before + 1


def test_mark_dirty_and_apply(app):
    app.mark_dirty("unit test")
    assert app._dirty is True
    assert "Not applied" in app.sync_label.cget("text")

    app._show_page("performance")
    app._toggle_connection()
    app.update()
    assert app.service.linked and app.service.demo

    app.apply_now()
    deadline = time.time() + 15
    while app._applying and time.time() < deadline:
        app.update()
        time.sleep(0.005)
    app.update()

    assert app._applying is False
    assert app._dirty is False
    assert app.sync_label.cget("text") == "Synced"
    assert app.service.transport.sent_packets
    assert app.service.transport.sent_blocks


def test_sync_macro_updates_referencing_buttons(app):
    record = app.store.add_macro("Sync me")
    from sm809.model import MacroEvent

    record.set_events([MacroEvent(opcode=4, state=1, delay=12)])
    entry = app.store.profile.button(0)
    entry.action = 0x16
    entry.selected_index = len(app.store.macros) - 1
    entry.macro_index = len(app.store.macros)

    app.sync_macro(len(app.store.macros) - 1)

    assert entry.action == 0x16
    assert entry.count == 1
    assert entry.event_slice()[0].opcode == 4
    assert entry.name == "Sync me"


def test_sync_gun_updates_referencing_buttons(app):
    from sm809.model import Bullet

    record = app.store.add_gun("Gun sync")
    index = len(app.store.guns) - 1
    record.set_bullets([Bullet(3, 4, 20), Bullet(5, 6, 30)])
    entry = app.store.profile.button(1)
    entry.action = 0x79
    entry.selected_index = index
    entry.set_bullets([Bullet(0, 0, 10)])

    app.sync_gun(index)

    assert entry.action == 0x79
    assert entry.count == 2
    assert entry.bullet_slice()[0].x == 3
    assert entry.bullet_slice()[1].delay == 30
    assert entry.name == "Gun sync"


def test_disabled_flat_button_repaints(app):
    from sm809.ui import theme

    btn = app._pages["macro"].btn_record
    btn.configure(state="disabled")
    disabled_fg = btn.cget("fg")
    assert disabled_fg == theme.DIM
    btn.configure(state="normal")
    assert btn.cget("fg") != disabled_fg
