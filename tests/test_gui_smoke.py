"""Headless demo-mode smoke test for the full studio window.

The window runs the same controller/apply pipeline as the real app, but
``demo=True`` routes every write into the in-memory demo transport. No USB
traffic is generated.
"""

import time

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from app import theme
from app.main_window import MainWindow


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    app.setStyleSheet(theme.stylesheet())
    yield app
    # Destroy every window while the application object is still alive.  When
    # several MainWindows have existed, letting Python finalize the
    # QApplication first and the widget wrappers afterwards crashed the
    # interpreter (exit 139) during shutdown.
    for widget in list(app.topLevelWidgets()):
        widget.close()
        widget.deleteLater()
    app.processEvents()
    app.quit()


def wait_for(app, predicate, timeout=8.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        app.processEvents()
        if predicate():
            return True
        time.sleep(0.03)
    return False


def test_main_window_applies_profile_and_edits(qapp, tmp_path, monkeypatch):
    import app.gun_store as gun_store
    import app.macro_store as macro_store
    import app.profile_store as profile_store

    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    monkeypatch.setattr(profile_store, "default_path",
                        lambda: str(cfg_dir / "profiles.json"))
    monkeypatch.setattr(macro_store, "default_path",
                        lambda: str(cfg_dir / "macros.json"))
    monkeypatch.setattr(gun_store, "default_path",
                        lambda: str(cfg_dir / "guns.json"))

    win = MainWindow(demo=True)
    win.show()
    try:
        # the worker connects and pushes the active profile
        assert wait_for(qapp, lambda: win._pushed_pid is not None)
        assert wait_for(qapp, lambda: "Wired" in win.topbar.conn_pill.text())
        assert win._current_config is not None
        pid = win._applied_id
        idx = win.profiles.index_of(pid)
        prof = win.profiles.data.profiles[idx]

        # lighting: only the parameters of the selected mode are sent
        win._apply_lighting(9, (10, 20, 30),
                            {"brightness": 120, "length": 2,
                             "frequency": 1, "direction": 1})
        assert prof.light_mode == 9
        assert prof.brightness == 120
        assert prof.fixed_rgb == (10, 20, 30)
        assert prof.frequency == 1

        # an identical lighting edit is a no-op (no extra full-profile write)
        pushed = win._pushed_config
        win._apply_lighting(9, (10, 20, 30),
                            {"brightness": 120, "length": 2,
                             "frequency": 1, "direction": 1})
        assert win._pushed_config is pushed

        # a legacy/out-of-range colour mode is clamped before it can reach
        # the device (+0xFC is a 0/1 table index, see FUN_00417540)
        win._apply_lighting(9, (10, 20, 30),
                            {"brightness": 120, "length": 2,
                             "frequency": 126, "direction": 1})
        assert prof.frequency == 1

        # polling + pointer settings
        win._apply_polling(1000)
        win._apply_pointer({"speed": 8, "scroll": 4, "double": 6,
                            "enhance": True, "onepage": False})
        assert prof.rate == 3            # 1000 Hz -> firmware index 3 (1 ms)
        assert prof.speed == 8
        assert prof.button(30).action == 0x0B   # normal Scroll Up

        # the official Performance page's key-response slider is persisted
        win._apply_key_response(17)
        assert win._current_config["key_response"] == 17
        assert prof.key_response == 17

        # bind a macro to slot 0 and verify it is embedded in the profile
        m = win.store.add("GUI Macro")
        win.store.set_events(m["id"], [
            {"type": "key", "keycode": 0x04, "down": True, "next_delay": 15},
            {"type": "key", "keycode": 0x04, "down": False, "next_delay": 0},
        ])
        win.buttons_panel.set_binding(0, {"macro": m["id"], "playmode": 2,
                                          "repeat": 3})
        win._apply_buttons(win.buttons_panel.bindings())
        entry = prof.button(0)
        assert entry.action == 0x16
        assert entry.count == 2
        assert entry.loop == 3
        assert entry.name == "GUI Macro"

        # deleting the macro resets the slot to its factory action
        win.store.delete(m["id"])
        win._on_library_changed()
        assert prof.button(0).action != 0x16
        assert win._current_config["buttons"][0][0] != 0x16

        # bind a gun (recoil) pattern: rows and repeat embed in the profile
        g = win.guns.add("Smoke Gun")
        rows = [[2, -1, 15], [3, 0, 20], [-1, 2, 30]]
        win.guns.set_rows(g["id"], rows)
        win.gun_panel._refresh_list()
        win.gun_panel.gun_list.setCurrentRow(win.guns.index_of(g["id"]))
        win.buttons_panel.set_binding(0, {"gun": g["id"],
                                          "name": g["name"],
                                          "rows": rows, "repeat": 2})
        win._apply_buttons(win.buttons_panel.bindings())
        entry = prof.button(0)
        assert entry.action == 0x79
        assert entry.count == 3
        assert entry.loop == 2
        assert entry.name == "Smoke Gun"
        assert [[r.x, r.y, r.delay] for r in entry.bullet_slice()] == rows

        # a startup/import scan rebuilds the library from the embedded table
        win.guns.delete(g["id"])
        win._adopt_device_guns()
        adopted = win.guns.get(f"dev:{win._applied_id}:0")
        assert adopted is not None
        assert adopted["rows"] == rows

        # deleting the pattern resets the bound slot to its factory action
        win._on_gun_library_changed()
        assert prof.button(0).action != 0x79
        assert win._current_config["buttons"][0][0] != 0x79

        # a new profile starts from factory defaults and can be removed
        if win.profiles.at_limit():
            spare = win.profiles.all()[-1]["id"]
            if spare == win.profiles.active_id:
                spare = win.profiles.all()[0]["id"]
            win.profiles.delete(spare)
        added = win.profiles.add("Smoke Profile")
        assert win.profiles.get(added["id"]) is not None
        win.profiles.delete(added["id"])
        assert win.profiles.get(added["id"]) is None
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_lighting_slider_is_debounced(qapp):
    """A drag must produce one device write, not one per slider tick."""
    from app.panels.lighting_panel import LightingPanel

    panel = LightingPanel(mode=4, color=(255, 0, 0),
                          params={"brightness": 255, "length": 3,
                                  "frequency": 1, "direction": 2})
    emitted = []
    panel.apply_requested.connect(
        lambda mode, colour, params: emitted.append((mode, colour, params)))

    for value in range(10, 200, 10):
        panel.brightness.setValue(value)
    assert emitted == []                 # nothing sent while the drag is live
    assert wait_for(qapp, lambda: emitted, timeout=2.0)
    qapp.processEvents()
    assert len(emitted) == 1
    assert emitted[0][2]["brightness"] == 190


def test_lighting_state_clamps_and_cancels_pending(qapp):
    """Loading a profile cancels a queued edit and clamps odd stored values."""
    from app.panels.lighting_panel import LightingPanel

    panel = LightingPanel(mode=4, color=(255, 0, 0),
                          params={"brightness": 255, "length": 3,
                                  "frequency": 1, "direction": 2})
    emitted = []
    panel.apply_requested.connect(lambda *a: emitted.append(a))
    panel.brightness.setValue(40)        # queues
    panel.set_state(2, (0, 255, 0),
                    {"brightness": 999, "length": 99,
                     "frequency": None, "direction": 9})
    assert panel.brightness.value() == 255     # clamped to 0..255
    assert panel.length.value() == 4           # vendor Pulsation 0..4
    assert panel.direction.value() == 4        # vendor Length 0..4
    assert panel.color_mode() == 1             # None keeps the previous value
    time.sleep(0.4)
    qapp.processEvents()
    assert emitted == []                 # the queued edit was discarded

    # a legacy frequency=126 must load as one of the two valid options
    panel.set_state(4, None, {"frequency": 126})
    assert panel.color_mode() == 1
    assert panel.loop_radio.isChecked()

    # an out-of-range stored mode is clamped before the radios render it
    panel.set_state(200, None, {})
    assert panel.current_mode() in range(12)


def test_buttons_mode_selects_the_device_layer(qapp):
    """Picking Office/Game must switch the mouse's work mode, not just the view."""
    from app.panels.buttons_panel import ButtonsPanel

    panel = ButtonsPanel()
    seen = []
    panel.mode_changed.connect(seen.append)
    panel.set_mode(1)
    panel.layers.set_value(1, emit=False)
    panel._on_layer(0)                   # user clicks Office
    assert seen == [0]
    assert panel.current_mode() == 0
    panel.set_mode(1)                    # external sync must not re-emit
    assert seen == [0]


def _make_window(qapp, tmp_path, monkeypatch, verbose=False):
    import app.gun_store as gun_store
    import app.macro_store as macro_store
    import app.profile_store as profile_store

    cfg_dir = tmp_path / "config"
    cfg_dir.mkdir()
    monkeypatch.setattr(profile_store, "default_path",
                        lambda: str(cfg_dir / "profiles.json"))
    monkeypatch.setattr(macro_store, "default_path",
                        lambda: str(cfg_dir / "macros.json"))
    monkeypatch.setattr(gun_store, "default_path",
                        lambda: str(cfg_dir / "guns.json"))
    win = MainWindow(demo=True, verbose=verbose)
    win.show()
    if verbose:
        # manual mode never pushes on connect: wait for the worker link only
        assert wait_for(qapp, lambda: win._current_config is not None)
        assert wait_for(qapp, lambda: "Wired" in win.topbar.conn_pill.text())
        assert win._pushed_pid is None
    else:
        assert wait_for(qapp, lambda: win._pushed_pid is not None)
    return win


def test_window_mode_and_dpi_osd(qapp, tmp_path, monkeypatch):
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        assert win._dpi_osd is True

        # selecting a layer also selects that work mode in the profile
        # (profile mode and UI layer share the same encoding: 0 = Office,
        # 1 = Game)
        def applied_mode():
            pkt = win.ctrl._dev._applied.get("mode")
            return pkt[1] if pkt else None   # 1 = Office, 2 = Game on the wire

        win.buttons_panel._on_layer(1)          # Game
        assert win._current_config["mode"] == 1
        assert wait_for(qapp, lambda: win.profiles.data.profile.mode == 1)
        assert wait_for(qapp, lambda: applied_mode() == 2)
        blocks_before = len(win.ctrl._dev.transport.sent_blocks)

        win.buttons_panel._on_layer(0)          # Office
        assert win._current_config["mode"] == 0
        assert wait_for(qapp, lambda: win.profiles.data.profile.mode == 0)
        # Switching layer must re-send the complete profile (0x12 included):
        # the firmware does not honour a lone 0x02 frame.
        assert wait_for(qapp, lambda: (applied_mode() == 1
                                       and "buttons" in win.ctrl._dev._written))
        assert (len(win.ctrl._dev.transport.sent_blocks) - blocks_before) >= 8

        # a physical mode-button event arrives as the same layer number
        win._on_mode_push(1)                    # hardware switched to Game
        assert win.buttons_panel.current_mode() == 1
        assert win._current_config["mode"] == 1

        # a hardware DPI stage change flashes a DPI card even with the general
        # overlay disabled
        win._overlay_enabled = False
        win._dpi_osd = True
        flashed = []
        win.overlay.flash = lambda value, caption="DPI", hold_ms=None: \
            flashed.append((value, caption))
        win._prev_dpi_level = 0
        win._on_dpi_push(1)
        level_one = win.dpi_panel.rows[1].dpi()
        assert flashed == [(f"{level_one}", "DPI")]
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_dpi_push_reads_the_enabled_row(qapp, tmp_path, monkeypatch):
    """A status push with a disabled stage above it must show the DPI of the
    row that is actually highlighted."""
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        panel = win.dpi_panel
        # the bundled seed profile has a single stage; give the panel a prefix
        from sm809pro import defaults as D
        panel.set_values(list(D.DPI_VALUES[:4]), list(D.DPI_COLORS[:4]),
                         enabled_count=4)
        panel.rows[0].toggle.setChecked(False)      # disable stage 1
        panel._apply_timer.stop()                   # isolate the push under test
        win._prev_dpi_level = None

        win._on_dpi_push(0)                          # first enabled stage

        assert panel.rows[1]._active
        assert not panel.rows[0]._active
        assert win.topbar.dpi_readout.text() == str(panel.rows[1].dpi())
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_controller_mode_event_reports_the_same_layer(
        qapp, tmp_path, monkeypatch):
    """A physical mode-button event must not come back inverted.

    The device event sets ``profile.mode`` with the profile encoding
    (0 = Office, 1 = Game); the UI layer uses the same numbers, so the
    controller must forward it unchanged.
    """
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        seen = []
        win.ctrl.mode_changed.connect(seen.append)
        win.profiles.data.profile.mode = 1
        win.ctrl._on_profile_changed("mode")
        win.profiles.data.profile.mode = 0
        win.ctrl._on_profile_changed("mode")
        assert seen == [1, 0]
        assert win.buttons_panel.current_mode() == 0
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_verbose_manual_apply_stages_until_the_button(
        qapp, tmp_path, monkeypatch):
    """--verbose shows the top-bar Apply button and defers device writes."""
    from sm809pro import actions as A

    win = _make_window(qapp, tmp_path, monkeypatch, verbose=True)
    try:
        assert win.manual_apply
        assert not win.topbar.apply_btn.isHidden()
        assert win.topbar.apply_btn.text() == "Apply"

        events = []
        win.ctrl.call = lambda *a, **k: events.append((a, k))
        assert events == []                     # no connect push

        # the panel starts on the layer the profile is actually running
        panel = win.buttons_panel
        assert panel.current_mode() == win._current_config["mode"]
        slot = panel.rows[6].slot                  # side pad row 6
        assert slot == A.slot_for_physical(6, panel.current_mode())

        win.buttons_panel.set_binding(slot, (0x0B, 0, 0))   # Scroll Up
        win.buttons_panel._on_button_changed(slot)

        # the edit is in the profile (so it survives a restart) ...
        assert list(win._current_config["buttons"][slot]) == [0x0B, 0, 0]
        assert win.profiles.data.profile.button(slot).action == 0x0B
        # ... but nothing has been written to the mouse
        assert events == []
        assert win.topbar.apply_btn.property("pending") is True
        assert win.topbar.apply_btn.text() == "Apply •"

        win.topbar.apply_btn.click()
        assert [a[0] for a, _ in events] == ["apply_config"]
        assert win.topbar.apply_btn.property("pending") is False
        assert win.topbar.apply_btn.text() == "Apply"
        assert win._pushed_pid is not None
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_apply_button_only_exists_in_manual_mode(qapp, tmp_path, monkeypatch):
    """Auto-apply writes as you edit, so no Apply button is shown."""
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        assert not win.manual_apply
        assert win.topbar.apply_btn.isHidden()
        assert win.topbar.apply_btn.property("manual") is False

        # switching to manual makes the button appear
        win.set_manual_apply(True)
        assert not win.topbar.apply_btn.isHidden()
        assert win.topbar.apply_btn.text() == "Apply"

        writes = []
        win.ctrl.call = lambda *a, **k: writes.append(a[0])
        win.topbar.apply_btn.click()
        assert writes == ["apply_config"]

        # back to auto: the button goes away again
        win.set_manual_apply(False)
        assert win.topbar.apply_btn.isHidden()
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_apply_mode_setting_persists_and_flushes_pending(
        qapp, tmp_path, monkeypatch):
    """Settings can switch every page to manual, and back to auto without
    losing a staged edit."""
    from sm809pro import actions as A

    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        win.set_manual_apply(True)
        assert win.manual_apply
        assert win.profiles.get_setting("manual_apply") is True
        assert win.topbar.apply_btn.property("manual") is True
        assert not win.topbar.apply_btn.isHidden()

        writes = []
        win.ctrl.call = lambda *a, **k: writes.append(a[0])
        panel = win.buttons_panel
        slot = panel.rows[6].slot
        win.buttons_panel.set_binding(slot, (0x0B, 0, 0))
        win.buttons_panel._on_button_changed(slot)
        assert writes == []                       # staged, not sent
        assert win._pending_apply

        # switching to auto-apply must write what was staged
        win.set_manual_apply(False)
        assert not win.manual_apply
        assert win.profiles.get_setting("manual_apply") is False
        assert writes == ["apply_config"]
        assert not win._pending_apply
        assert win.topbar.apply_btn.property("pending") is False
        assert win.topbar.apply_btn.isHidden()
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_log_panel_is_controlled_from_settings(
        qapp, tmp_path, monkeypatch):
    """The log has no top-bar or tray toggle: Settings turns it on, the panel
    × closes it."""
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        assert win.log_panel.isHidden()
        assert not hasattr(win.topbar, "log_btn")
        assert not hasattr(win, "tray_log")

        win._set_log_visible(True)          # Settings enables it
        assert not win.log_panel.isHidden()
        assert win.profiles.get_setting("show_log") is True

        win.log_panel.close_btn.click()     # the panel's × closes it
        assert win.log_panel.isHidden()
        assert win.profiles.get_setting("show_log") is False
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_connect_push_does_not_reset_a_pending_pointer_edit(
        qapp, tmp_path, monkeypatch):
    """A slider moved while the device connects must survive the connect push.

    ``_on_connected`` used to reseed every panel, which cancelled the 250 ms
    debounce and silently reverted the edit (the old wheel checkbox showed the
    same race).
    """
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        win.performance_panel.speed.setValue(9)
        win.performance_panel._timer.stop()          # keep the edit pending
        assert win.performance_panel.speed.value() == 9

        win.apply_profile(win._current_config, force=True, reseed=False)
        assert win.performance_panel.speed.value() == 9

        # A real profile load still seeds the panels from the stored config.
        win.apply_profile(win._current_config, force=True)
        assert (win.performance_panel.speed.value()
                == win._current_config["pointer"]["speed"])
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_controller_coalesces_queued_profile_writes():
    """Only the newest waiting full-profile snapshot is executed."""
    import queue

    from app.controller import DeviceController

    ctrl = DeviceController.__new__(DeviceController)
    ctrl._q = queue.Queue()
    ctrl.call("apply_config", {"n": 1})
    ctrl.call("apply_config", {"n": 2})
    ctrl.call("apply_config", {"n": 3})
    ctrl.call("poll")
    ctrl.call("apply_config", {"n": 4})
    items = list(ctrl._q.queue)
    assert [item[0] for item in items] == ["apply_config", "poll"]
    assert items[0][1] == ({"n": 4},)


def test_gun_panel_edits_and_flags_oversize(qapp, tmp_path):
    from app.gun_store import GunStore
    from app.panels.gun_panel import GunPanel

    store = GunStore(path=str(tmp_path / "guns.json"))
    panel = GunPanel(store)
    emitted = []
    panel.library_changed.connect(lambda: emitted.append(True))

    panel.new_gun()
    gid = store.all()[0]["id"]
    assert panel.gun_list.count() == 1

    panel.bullets.setValue(4)
    assert len(store.get(gid)["rows"]) == 4
    panel.table.cellWidget(0, 1).setValue(5)
    panel.table.cellWidget(0, 2).setValue(-3)
    panel.table.cellWidget(0, 3).setValue(20)
    assert store.get(gid)["rows"][0] == [5, -3, 20]
    panel.name_edit.setText("AK")
    assert store.get(gid)["name"] == "AK"
    panel._flush()
    assert emitted
    assert (tmp_path / "guns.json").exists()

    # 16 offset rows exceed the firmware's 128-byte table
    panel.bullets.setValue(16)
    for i in range(16):
        panel.table.cellWidget(i, 1).setValue(i + 1)
        panel.table.cellWidget(i, 2).setValue(i + 1)
    assert "128" in panel.size_label.text()
    assert "128" in panel.size_label.toolTip()

    panel.delete_gun()
    assert store.all() == []


def test_gun_panel_header_never_overlaps_or_clips(qapp, tmp_path):
    """The pattern controls keep their airy two-row shape without clipping.

    The count/budget pair shares a line with the edit tools and the recorder
    gets its own line.  On a narrow card the two clusters stack instead of
    the byte counter being drawn over "Clear offsets" and the Flip buttons
    running off the right edge.
    """
    from PySide6.QtCore import QRect
    from PySide6.QtWidgets import QPushButton

    from app import theme
    from app.gun_store import GunStore
    from app.panels.gun_panel import GunPanel

    store = GunStore(path=str(tmp_path / "guns.json"))
    store.add("AK")
    panel = GunPanel(store)
    panel.setStyleSheet(theme.stylesheet())
    panel.resize(panel.minimumSizeHint())
    panel.show()
    qapp.processEvents()

    card = panel.table.parentWidget()
    clear_btn = next(b for b in panel.findChildren(QPushButton)
                     if b.text() == "Clear offsets")
    widgets = (panel.size_label, panel.bullets, panel.record_btn,
               panel.record_interval, clear_btn, panel.flip_x_btn,
               panel.flip_y_btn, panel.record_status)

    def in_card(w):
        return QRect(w.mapTo(card, w.rect().topLeft()), w.size())

    # narrow card: the clusters stack, and every control stays inside
    boxes = [in_card(w) for w in widgets]
    for box in boxes:
        assert box.width() > 0 and box.height() > 0
        assert card.rect().contains(box)
    for i, first in enumerate(boxes):
        for second in boxes[i + 1:]:
            assert not first.intersects(second)
    assert in_card(clear_btn).top() > in_card(panel.bullets).top()
    assert in_card(panel.record_btn).top() > in_card(clear_btn).bottom()

    # at the page width of the default 1000 px window the clusters share one
    # line again: count + budget on the left, the edit tools on the right
    panel.resize(820, 624)
    qapp.processEvents()
    bullets = in_card(panel.bullets)
    size = in_card(panel.size_label)
    clear = in_card(clear_btn)
    assert size.top() == bullets.top()
    assert clear.top() == bullets.top()
    assert clear.left() > size.right()
    assert (clear.left() < in_card(panel.flip_x_btn).left()
            < in_card(panel.flip_y_btn).left())
    assert in_card(panel.record_btn).top() > bullets.bottom()
    assert (in_card(panel.record_btn).top()
            == in_card(panel.record_interval).top())
    assert (in_card(panel.record_btn).left()
            < in_card(panel.record_interval).left())


def test_no_page_needs_horizontal_scrolling_at_minimum_size(
        qapp, tmp_path, monkeypatch):
    """Every page must fit the window's advertised minimum width.

    Cards and toolbars used to force their own minimum width past the
    viewport, so a horizontal scrollbar appeared on Buttons, Macro, Recoil Control and
    Auto-Switch at 820x560.  This also guards the DPI subtitle, which was a
    single unwrapped line before.
    """
    from PySide6.QtWidgets import QScrollArea

    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        win._set_developer(True)      # include the Recoil Control preview page
        win.resize(win.minimumSize())
        qapp.processEvents()
        assert win.width() <= 900, "the window minimum grew past a 900 px screen"
        for row in range(win.stack.count()):
            win.nav.setCurrentRow(row)
            qapp.processEvents()
            page = win.stack.currentWidget()
            assert page.minimumSizeHint().width() <= page.width(), (
                f"{type(page).__name__} asks for "
                f"{page.minimumSizeHint().width()} px but has {page.width()}")
            for scroll in page.findChildren(QScrollArea):
                bar = scroll.horizontalScrollBar()
                assert bar.maximum() == 0, (
                    f"{type(page).__name__} needs {bar.maximum()} px of "
                    f"horizontal scrolling at {win.width()}x{win.height()}")
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_recoil_control_is_hidden_until_developer_features_are_enabled(
        qapp, tmp_path, monkeypatch):
    """Recoil Control is a work-in-progress preview: the rail entry, its page
    and the picker category stay out of the normal UI until Settings turns the
    developer switch on.  Turning it back off stops host playback too."""
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        names = [win.nav.item(i).text() for i in range(win.nav.count())]
        assert "Recoil Control" not in names
        assert names == ["Buttons", "Macro", "Lighting", "Performance",
                         "Profiles"]
        assert "DPI" not in names and "Auto-Switch" not in names

        # DPI stages live on the Performance page, not on their own page
        win._select_page("Performance")
        assert win.stack.currentWidget() is win.performance_panel
        assert win.performance_panel.isAncestorOf(win.dpi_panel)
        assert win.stack.indexOf(win.dpi_panel) == -1

        # auto-switch content is hosted by the Manage Apps dialog instead
        assert all(win.stack.widget(i) is not win.autoswitch_panel
                   for i in range(win.stack.count()))

        # a saved playback preference stays dormant while the tab is hidden
        win.profiles.set_setting("recoil_host_enabled", True)
        win.gun_panel._sync_player()
        assert not win.gun_panel.player.enabled

        win._set_developer(True)
        names = [win.nav.item(i).text() for i in range(win.nav.count())]
        assert names == ["Buttons", "Macro", "Recoil Control", "Lighting",
                         "Performance", "Profiles"]
        win._select_page("Recoil Control")
        assert win.stack.currentWidget() is win.gun_panel
        assert win.gun_panel.host_enable.isChecked()
        assert win.gun_panel.player.enabled
        assert win.profiles.get_setting("developer_features") is True

        # turning developer features off while on the preview page falls back
        # to Buttons and stops the engine
        win._set_developer(False)
        assert win.stack.currentWidget() is win.buttons_panel
        assert not win.gun_panel.player.enabled
        assert win.profiles.get_setting("developer_features") is False
        assert win.buttons_panel._developer is False
    finally:
        win.gun_panel.player.set_enabled(False)
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_manage_apps_opens_the_popup_for_the_selected_profile(
        qapp, tmp_path, monkeypatch):
    """The Profiles tab's Manage apps… button opens the auto-switch content as
    a popup named Manage Apps, preselected to the clicked profile."""
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        pid = win.profiles.active_id
        assert pid is not None

        win._select_page("Profiles")
        win._on_manage_apps(pid)
        qapp.processEvents()

        dlg = win.manage_apps_dialog
        assert dlg.isVisible()
        assert dlg.windowTitle() == "Manage Apps"
        assert dlg.panel is win.autoswitch_panel
        assert dlg.panel.title_label.text() == "Manage Apps"
        assert dlg.panel.current_pid() == pid
        # the popup is not part of the rail/stack
        assert "Manage Apps" not in [
            win.nav.item(i).text() for i in range(win.nav.count())]
        assert all(win.stack.widget(i) is not dlg.panel
                   for i in range(win.stack.count()))

        # its cards still fit the dialog's own minimum width
        from PySide6.QtWidgets import QScrollArea
        dlg.resize(dlg.minimumSize())
        qapp.processEvents()
        for scroll in dlg.panel.findChildren(QScrollArea):
            assert scroll.horizontalScrollBar().maximum() == 0

        dlg.close()
        qapp.processEvents()
        assert not dlg.isVisible()
        # the live foreground readout only polls while the dialog is open
        assert not dlg.panel._fg_timer.isActive()
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_settings_dialog_offers_the_developer_switch(qapp, tmp_path, monkeypatch):
    """The only way to reveal Recoil Control is the Settings checkbox."""
    from PySide6.QtWidgets import QCheckBox, QDialog

    win = _make_window(qapp, tmp_path, monkeypatch)
    monkeypatch.setattr(QDialog, "exec", lambda self: QDialog.Rejected)
    try:
        win._settings()
        dlg = next(w for w in win.findChildren(QDialog)
                   if w.windowTitle() == "Settings")
        boxes = {c.text(): c for c in dlg.findChildren(QCheckBox)}
        dev = boxes["Enable developer features (work in progress)"]
        assert not dev.isChecked()          # off by default

        win._set_developer(True)
        win._settings()
        dlgs = [w for w in win.findChildren(QDialog)
                if w.windowTitle() == "Settings"]
        dev = {c.text(): c for c in dlgs[-1].findChildren(QCheckBox)}[
            "Enable developer features (work in progress)"]
        assert dev.isChecked()
    finally:
        win.gun_panel.player.set_enabled(False)
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_profiles_select_the_active_row_and_explain_empty_lists(qapp):
    """The active profile is visibly selected; empty/search states say why."""
    from app.panels.profiles_panel import ProfilesPanel

    panel = ProfilesPanel()
    panel.show()
    try:
        profiles = [{"id": "office", "name": "Office"},
                    {"id": "gaming", "name": "Gaming"}]
        panel.set_profiles(profiles, active_id="gaming")
        qapp.processEvents()
        assert panel.selected_id() == "gaming"
        assert panel.list.currentRow() == 1

        # A refresh keeps the row the user picked, even when another profile
        # is active (the management buttons act on the selected row).
        panel.list.setCurrentRow(0)
        panel.set_profiles(profiles, active_id="gaming")
        assert panel.selected_id() == "office"

        # No rows: explain how to add one instead of showing an empty box.
        panel.set_profiles([], active_id=None)
        qapp.processEvents()
        assert not panel.empty.isHidden()
        assert "No profiles yet" in panel.empty.text()
        assert "Import files" in panel.empty.text()

        # A search with no match keeps the list and says the filter is why.
        panel.set_profiles(profiles, active_id="gaming")
        panel.search.setText("zzz")
        qapp.processEvents()
        assert not panel.empty.isHidden()
        assert "No profile matches" in panel.empty.text()
        panel.search.clear()
        assert panel.empty.isHidden()
    finally:
        panel.close()
        panel.deleteLater()


def test_auto_switch_moves_the_rail_combo_and_profiles_tab(
        qapp, tmp_path, monkeypatch):
    """A matched app must switch the profile EVERYWHERE: the mouse, the rail
    PROFILE combo and the Profiles tab. The manual base stays untouched, but
    unmatched windows keep the last matched profile (no base revert).

    This is the real-world gap: the profile was applied but both selections
    kept showing the base, so auto-switch looked like it had done nothing.
    It also chains app-to-app (the Alt-Tab/minimize case): game one -> game
    two -> minimized -> desktop (holds) -> back.
    """
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        base = win.profiles.active_id
        game = win.profiles.add(
            "Game Mode", config=win.profiles.config(base),
            match_rules=[{"exe": "smoke-game.exe", "path": None, "title": None}])
        other = win.profiles.add(
            "Second Game", config=win.profiles.config(base),
            match_rules=[{"exe": "smoke-other.exe", "path": None,
                          "title": None}])
        win._refresh_profile_combo()
        assert win.profile_combo.currentData() == base
        assert win.profiles_panel.selected_id() == base

        class Watcher:
            value = ("explorer.exe", "Desktop", r"C:\Windows\explorer.exe")

            def current(self, need_path=False, need_title=True):
                return self.value

        watcher = Watcher()
        win._auto._watcher = watcher
        win._auto._debounce_ms = 0          # switch on the first poll
        win._toggle_autoswitch(True)

        # the first game comes to the foreground
        watcher.value = ("smoke-game.exe", "Smoke Game",
                         r"C:\Games\Smoke\smoke-game.exe")
        win._auto.poll()
        assert win._applied_id == game["id"]
        assert win._pushed_pid == game["id"]       # written to the mouse
        assert win.profile_combo.currentData() == game["id"]
        assert win.profiles_panel.selected_id() == game["id"]
        # ...but the manual base did not move (auto-switch is an override)
        assert win.profiles.active_id == base

        # a refresh (rename, reorder, rule edit) must not snap it back to base
        win._refresh_profile_combo()
        assert win.profile_combo.currentData() == game["id"]
        assert win.profiles_panel.selected_id() == game["id"]

        # Alt-Tab straight into another game: that profile takes over.
        watcher.value = ("smoke-other.exe", "Second Game",
                         r"C:\Games\Other\smoke-other.exe")
        win._auto.poll()
        assert win._applied_id == other["id"]
        assert win._pushed_pid == other["id"]
        assert win.profile_combo.currentData() == other["id"]
        assert win.profiles_panel.selected_id() == other["id"]

        # minimize: Windows briefly reports no foreground. Hold the profile
        # instead of bouncing through the base and writing the mouse twice.
        watcher.value = (None, "", None)
        win._auto.poll()
        assert win._applied_id == other["id"]
        assert win.profile_combo.currentData() == other["id"]

        # a real non-matching window (desktop/taskbar) HOLDS the last profile:
        # it must never push a rule-less profile to the mouse
        watcher.value = ("explorer.exe", "Desktop", r"C:\Windows\explorer.exe")
        win._auto.poll()
        assert win._applied_id == other["id"]
        assert win.profile_combo.currentData() == other["id"]
        assert win.profiles_panel.selected_id() == other["id"]
        assert win.profiles.active_id == base

        # restoring the first game switches back to it
        watcher.value = ("smoke-game.exe", "Smoke Game",
                         r"C:\Games\Smoke\smoke-game.exe")
        win._auto.poll()
        assert win._applied_id == game["id"]
        assert win.profiles_panel.selected_id() == game["id"]
    finally:
        win._auto.set_enabled(False)
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_auto_switch_announces_with_the_overlay_not_a_tray_toast(
        qapp, tmp_path, monkeypatch):
    """The applied profile is announced by the on-screen overlay.

    The tray toast is gone; the switch card still appears when the ambient
    overlay (DPI/rate) is off, and the dedicated "Announce profile switches"
    setting can silence it without bringing the toast back.
    """
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        win._overlay_enabled = False       # the ambient overlay is off
        win._overlay_switch = True
        base = win.profiles.active_id
        game = win.profiles.add(
            "Overlay Game", config=win.profiles.config(base),
            match_rules=[{"exe": "overlay-game.exe"}])
        other = win.profiles.add(
            "Overlay Two", config=win.profiles.config(base))
        win._refresh_profile_combo()

        flashes, toasts = [], []
        win.overlay.flash_lines = (
            lambda lines, hold_ms=None: flashes.append([tuple(x) for x in lines]))
        if win.tray is not None:
            win.tray.showMessage = lambda *a, **k: toasts.append(a)

        class Watcher:
            def current(self, need_path=False, need_title=True):
                return ("overlay-game.exe", "Overlay Game",
                        r"C:\Games\Overlay\overlay-game.exe")

        win._auto._watcher = Watcher()
        win._auto._debounce_ms = 0
        win._toggle_autoswitch(True)
        win._auto.poll()
        assert win._applied_id == game["id"]
        assert [("Switching to", "Overlay Game")] in flashes
        assert toasts == []

        # the finished-apply notice is the profile card (ambient overlay off)
        flashes.clear()
        win._overlay_pending = True        # simulate the apply queue draining
        win._on_busy_overlay(False)
        assert flashes == [[("Profile", "Overlay Game")]]

        # turning the dedicated switch off silences the card, not the toast
        win._overlay_switch = False
        flashes.clear()
        win._apply_by_id(other["id"])
        assert flashes == []
        assert toasts == []
    finally:
        win._auto.set_enabled(False)
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_failed_apply_is_retried_and_settles_the_switch_card(
        qapp, tmp_path, monkeypatch):
    """A failed write must not poison the "already pushed" cache.

    After a failure the next identical selection (the next rule match, or a
    manual Apply) has to reach the mouse again, and the in-flight switch card
    has to be replaced by a truthful "Not applied" notice instead of hanging on
    "Switching to ..." forever.
    """
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        win._overlay_enabled = False
        win._overlay_switch = True
        flashes, calls = [], []
        win.overlay.flash_lines = (
            lambda lines, hold_ms=None: flashes.append([tuple(x) for x in lines]))
        win.ctrl.call = lambda *a, **k: calls.append(a)

        base = win.profiles.active_id
        game = win.profiles.add(
            "Fail Game", config=win.profiles.config(base),
            match_rules=[{"exe": "fail-game.exe"}])
        win._apply_by_id(game["id"])
        assert win._pushed_pid == game["id"]
        assert win._overlay_pending is True
        assert flashes == [[("Switching to", "Fail Game")]]

        win._on_command_done("apply_config", False)
        assert win._pushed_pid is None
        assert win._pushed_config is None
        assert win._overlay_pending is False
        assert flashes[-1] == [("Not applied", "Fail Game")]

        # the identical retry is written again instead of being deduped away
        win._apply_by_id(game["id"])
        assert win._pushed_pid == game["id"]
        assert len(calls) == 2
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_skipped_apply_never_leaves_the_switch_card_pending(
        qapp, tmp_path, monkeypatch):
    """Selecting a profile already on the mouse settles the card immediately.

    The dedupe path returns False (nothing queued), so there is no busy signal
    coming to clear a pending "Switching to ..." notice.
    """
    win = _make_window(qapp, tmp_path, monkeypatch)
    try:
        win._overlay_enabled = False
        win._overlay_switch = True
        calls = []
        win.ctrl.call = lambda *a, **k: calls.append(a)
        flashes = []
        win.overlay.flash_lines = (
            lambda lines, hold_ms=None: flashes.append([tuple(x) for x in lines]))

        base = win.profiles.active_id
        twin = win.profiles.add("Twin", config=win.profiles.config(base))
        # Pretend the twin is what the mouse already has; the UI still shows base.
        win._pushed_pid = twin["id"]
        win._pushed_config = win.profiles.config(twin["id"])
        win._applied_id = base

        win._apply_by_id(twin["id"])
        assert calls == []                   # identical config -> no device write
        assert win._overlay_pending is False
        assert flashes == [[("Switching to", "Twin")], [("Profile", "Twin")]]
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()


def test_gun_how_to_steps_expand_on_demand(qapp, tmp_path):
    """The workflow guide is still there, but no longer hides the editor."""
    from app.gun_store import GunStore
    from app.panels.gun_panel import GunPanel

    store = GunStore(path=str(tmp_path / "guns.json"))
    store.add("AK")
    panel = GunPanel(store)
    panel._refresh_list()
    panel.gun_list.setCurrentRow(0)
    try:
        assert panel.how_steps.isHidden()
        assert "5 steps" in panel.how_toggle.text()

        panel.how_toggle.click()
        qapp.processEvents()
        assert not panel.how_steps.isHidden()
        assert "Hide" in panel.how_toggle.text()
        assert "Enable host playback" in panel.how_steps.text()
        assert "wired mouse will not execute it" in panel.how_steps.text()

        panel.how_toggle.click()
        assert panel.how_steps.isHidden()
    finally:
        panel.close()
        panel.deleteLater()


def test_autoswitch_hides_the_empty_rules_box(qapp):
    """With no rules, show guidance and the fields, not a large blank list."""
    from app.panels.autoswitch_panel import AutoSwitchPanel

    panel = AutoSwitchPanel()
    try:
        panel.set_profiles([{"id": "p1", "name": "Office",
                             "match_rules": []}])
        qapp.processEvents()
        assert panel.rules_list.isHidden()
        assert not panel.rules_empty.isHidden()
        assert "No custom apps" in panel.rules_empty.text()

        panel._add_rule("p1", {"exe": "game.exe"})
        qapp.processEvents()
        assert not panel.rules_list.isHidden()
        assert panel.rules_empty.isHidden()
        assert panel.rules_list.count() == 1
    finally:
        panel.close()
        panel.deleteLater()


def test_action_picker_offers_recoil_patterns(qapp, tmp_path):
    from app.gun_store import GunStore
    from app.widgets.action_picker import CATEGORY_ORDER, ActionPicker

    store = GunStore(path=str(tmp_path / "guns.json"))
    g = store.add("AK")
    store.set_rows(g["id"], [[5, -5, 20]])

    picker = ActionPicker((0, 0, 0), guns=store.all(), developer=True)
    try:
        picker.cats.setCurrentRow(CATEGORY_ORDER.index("Recoil Control"))
        assert picker.stack.currentIndex() == 4
        picker.gun_editor.repeat.setCurrentIndex(2)      # 3x
        code = picker._current_code()
        assert code["gun"] == g["id"]
        assert code["name"] == "AK"
        assert code["repeat"] == 3
        assert code["rows"] == [[5, -5, 20]]
    finally:
        picker.close()


def test_shortcut_and_macro_offer_left_right_modifier_keys(qapp):
    """LShift/RShift/LAlt/… must be selectable as keys, like the vendor driver."""
    from PySide6.QtCore import Qt
    from sm809pro import actions as A
    from app.widgets.action_picker import _ComboEditor, describe_action

    expected = [
        ("left ctrl", 0xE0), ("left shift", 0xE1), ("left alt", 0xE2),
        ("left win", 0xE3), ("right ctrl", 0xE4), ("right shift", 0xE5),
        ("right alt", 0xE6), ("right win", 0xE7),
    ]
    for name, usage in expected:
        assert A.HID[name] == usage

    editor = _ComboEditor()
    for _name, usage in expected:
        assert editor.key.findData(usage) >= 0
    editor.key.setCurrentIndex(editor.key.findData(A.HID["left alt"]))
    assert editor.code() == (0x15, 0, 0xE2)
    assert describe_action(editor.code()) == "Key: LEFT ALT"

    # Detect Key captures the exact left/right side instead of a generic flag.
    class FakeEvent:
        def __init__(self, key, vk):
            self._key, self._vk = key, vk
        def key(self):
            return self._key
        def nativeVirtualKey(self):
            return self._vk

    editor._handle_key_press(FakeEvent(Qt.Key_Alt, 0xA5))    # Right Alt
    assert editor.code() == (0x15, 0, 0xE6)
    editor._handle_key_press(FakeEvent(Qt.Key_Shift, 0xA0))  # Left Shift
    assert editor.code() == (0x15, 0, 0xE1)
    editor.deleteLater()

    from app.panels.macro_panel import KEY_INSERT_CHOICES
    macro_codes = dict(KEY_INSERT_CHOICES)
    assert macro_codes["Right Shift"] == 0xE5
    assert macro_codes["Left Alt"] == 0xE2
    assert macro_codes["Right Win"] == 0xE7


def test_buttons_panel_reports_shared_table_budget(qapp):
    """Macro/gun tables share indices 1..11; the panel must say so."""
    from sm809pro import actions as A
    from app.panels.buttons_panel import ButtonsPanel

    panel = ButtonsPanel()
    key = {"type": "key", "keycode": 0x04, "down": True, "next_delay": 10}
    codes = [A.BTN["unset"]] * A.SLOT_COUNT
    for i in range(10):
        codes[i] = {"macro": f"m{i}", "events": [dict(key)]}
    for i in range(10, 13):
        codes[i] = {"gun": f"g{i}", "rows": [[1, 1, 10]]}

    panel.set_codes(codes)
    assert "13 macro / recoil tables" in panel.budget.text()
    assert "last 2 will not work" in panel.budget.text()
    assert panel.budget.styleSheet()          # visible warning styling

    # Eleven tables fit exactly; two macros released the third gun's slot.
    codes[9] = A.BTN["unset"]
    codes[10] = A.BTN["unset"]
    panel.set_codes(codes)
    assert panel.budget.text() == ""
    panel.deleteLater()


def test_new_profile_dialog_prefills_the_next_number(qapp, tmp_path, monkeypatch):
    """New Profile suggests Profile N by position, even after custom renames."""
    from PySide6.QtWidgets import QInputDialog

    win = _make_window(qapp, tmp_path, monkeypatch)
    seen = []

    def fake_get_text(parent, title, label, text=""):
        seen.append((title, text))
        return text, True

    monkeypatch.setattr(QInputDialog, "getText", staticmethod(fake_get_text))
    try:
        # GUI tests share one scratch device table, so derive the expected
        # number from the current count instead of assuming a fresh seed.
        start = len(win.profiles.summaries())
        # The active profile gets a custom name; it keeps its position.
        win.profiles.rename(win.profiles.active_id, "Valorant")
        win._refresh_profile_combo()

        win._profile_new()
        assert seen[-1] == ("New profile", f"Profile {start + 1}")
        assert win.profiles.get(win.profiles.active_id)["name"] == \
            f"Profile {start + 1}"

        # Rename the new one: the next suggestion follows the count, not names.
        win.profiles.rename(win.profiles.active_id, "Delta Force")
        win._refresh_profile_combo()
        win._profile_new()
        assert seen[-1] == ("New profile", f"Profile {start + 2}")
        assert win.profiles.get(win.profiles.active_id)["name"] == \
            f"Profile {start + 2}"
    finally:
        win._force_quit = True
        win.close()
        qapp.processEvents()
