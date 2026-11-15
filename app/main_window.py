"""
app.main_window -- the application shell for the wired SM809 studio.

Top bar (device name + USB connection pill + live polling/DPI readout), a left
navigation rail with a Reset-to-Factory action in its footer, and the reference
stack of panels. Owns the wired DeviceController and the profile/macro stores.

Nav order: Buttons, Macro, Recoil Control, Lighting, Performance, Profiles.
DPI stages live inside Performance; per-app auto-switch opens as the Manage
Apps dialog from the Profiles tab.  Recoil Control is a developer preview and
is absent from the rail until the Settings switch is turned on.
"""

import copy
import logging
import os
from functools import lru_cache

from PySide6.QtCore import Qt, QTimer, QByteArray
from PySide6.QtGui import QAction, QIcon, QPixmap, QPainter, QColor, QGuiApplication
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QListWidget,
    QListWidgetItem, QStackedWidget, QFrame, QLabel, QPushButton, QMessageBox,
    QSizePolicy, QAbstractItemView, QComboBox, QInputDialog, QMenu,
    QFileDialog, QSystemTrayIcon, QDialog, QCheckBox, QSlider, QDialogButtonBox,
    QGroupBox, QRadioButton, QScrollArea, QSplitter,
)

from . import theme
from .controller import DeviceController
from sm809pro import actions as A
from .panels.dpi_panel import DpiPanel
from .panels.buttons_panel import ButtonsPanel
from .panels.lighting_panel import LightingPanel
from .panels.performance_panel import PerformancePanel
from .panels.macro_panel import MacroPanel
from .panels.gun_panel import GunPanel
from .panels.manage_apps_dialog import ManageAppsDialog
from .panels.profiles_panel import ProfilesPanel
from .file_import import (
    ALL_SUPPORTED_FILTER, FileDropRouter, MACRO_FILTER, PROFILE_FILTER,
    file_names, supported_hint, split_paths,
)
from .macro_store import MacroStore
from .gun_store import GunStore
from .profile_store import ProfileStore, PROFILE_LIMIT, default_config
from .autoswitch import AutoSwitcher
from .widgets.overlay import Overlay, AlertOverlay, POSITIONS, POSITION_LABELS
from .widgets.log_panel import LogPanel
from .paths import resource_path
from .widgets.action_picker import set_macro_resolver

_log = logging.getLogger("sm809.app")

# nav order requested by the user
NAV_ITEMS = ["Buttons", "Macro", "Recoil Control", "Lighting",
             "Performance", "Profiles"]


@lru_cache(maxsize=1)
def app_icon():
    """The application icon (window / taskbar / tray), bundled at
    images/icon.ico (resolved frozen-safe via _MEIPASS).

    Qt decodes the .ico on construction; the window, tray and entry point all
    ask for the same icon, so it is decoded once.
    """
    return QIcon(resource_path("images", "icon.ico"))


class Placeholder(QWidget):
    """A simple 'coming soon' panel for sections not yet built."""
    def __init__(self, name):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(10)
        t = QLabel(name)
        t.setProperty("panelTitle", "true")
        lay.addWidget(t)
        s = QLabel("This panel is coming soon.")
        s.setProperty("panelSubtitle", "true")
        lay.addWidget(s)
        lay.addStretch(1)


class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("topbar")
        self.setFixedHeight(56)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(20, 0, 20, 0)
        lay.setSpacing(12)

        self.name = QLabel("SOLAKAKA SM809 Wired — Studio")
        self.name.setObjectName("deviceName")
        lay.addWidget(self.name)

        lay.addStretch(1)

        # Apply exists only in manual mode: auto mode writes every edit as it
        # happens, so there is nothing to confirm.  Settings switches modes.
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.setObjectName("applyBtn")
        self.apply_btn.setProperty("pending", False)
        self.apply_btn.setProperty("manual", False)
        self.apply_btn.setToolTip("Manual apply: changes are staged until you click Apply.")
        self.apply_btn.hide()
        lay.addWidget(self.apply_btn)

        # live log: enabled from Settings; the panel itself has a close ×

        # upload spinner: visible only while a config write is in flight
        self.spinner = QLabel("")
        self.spinner.setObjectName("spinner")
        lay.addWidget(self.spinner)
        self._spin_frames = [chr(c) for c in
                             (0x280B, 0x2819, 0x2839, 0x2838, 0x283C,
                              0x2834, 0x2826, 0x2827, 0x2807, 0x280F)]
        self._spin_i = 0
        self._spin_timer = QTimer(self)
        self._spin_timer.setInterval(80)
        self._spin_timer.timeout.connect(self._tick_spinner)

        # connection indicator (grouped on the right with the live stats)
        self.conn_pill = QLabel("connecting…")
        lay.addWidget(self.conn_pill)
        self.conn_pill.setStyleSheet(self._conn_style(theme.TEXT_DIM))

        # battery / charge status (the wired mouse has no battery)
        self.battery = QLabel("")
        self.battery.setObjectName("battery")
        self.battery.hide()
        lay.addWidget(self.battery)

        # live stat groups: each is a tight caption+value unit so the groups
        # sit at even spacing across the bar (no stray spacer)
        rate_group, self.rate_readout = self._stat("POLLING RATE", "rateReadout")
        lay.addWidget(rate_group)
        dpi_group, self.dpi_readout = self._stat("DPI", "dpiReadout")
        lay.addWidget(dpi_group)

    def _conn_style(self, color):
        # match the battery readout: plain mono text, 12px, no pill background
        return f"color: {color}; font-family: {theme.FONT_MONO}; font-size: 12px;"

    def _repolish(self, widget):
        style = widget.style()
        style.unpolish(widget)
        style.polish(widget)

    def set_manual_apply(self, enabled):
        """Show Apply only in manual mode; auto mode writes as you edit."""
        enabled = bool(enabled)
        self.apply_btn.setProperty("manual", enabled)
        self.apply_btn.setVisible(enabled)
        self.set_pending(False)
        self._repolish(self.apply_btn)

    def set_pending(self, pending):
        """Mark staged edits so it is obvious the mouse has not been written."""
        pending = bool(pending)
        if bool(self.apply_btn.property("pending")) != pending:
            self.apply_btn.setProperty("pending", pending)
            self.apply_btn.setText("Apply •" if pending else "Apply")
            self._repolish(self.apply_btn)
        if pending:
            self.apply_btn.setToolTip(
                "Pending changes: click to write the current profile to the mouse.")
        else:
            self.apply_btn.setToolTip(
                "Manual apply: changes are staged until you click Apply.")

    def _stat(self, caption, value_obj_name):
        # a tightly-spaced caption+value pair; the bar then spaces groups evenly
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(6)
        cap = QLabel(caption)
        cap.setProperty("unit", "true")
        val = QLabel("—")
        val.setObjectName(value_obj_name)
        h.addWidget(cap)
        h.addWidget(val)
        return w, val

    def set_connection(self, info):
        conn = info.get("connection", "?")
        label = {"2.4GHz": "2.4 GHz", "wired": "USB Wired", "bluetooth": "Bluetooth"}.get(conn, conn)
        self.conn_pill.setText(f"● {label}")
        self.conn_pill.setStyleSheet(self._conn_style(theme.GOOD))
        self._conn_label = label
        if not info.get("configurable", True):
            self.conn_pill.setToolTip(f"Connected via {label} (read-only; settings changes require 2.4GHz dongle or USB wired)")
        else:
            self.conn_pill.setToolTip(f"Connected via {label}")

    def set_offline(self):
        # dongle/cable present but the mouse isn't responding
        self.conn_pill.setText("● mouse offline")
        self.conn_pill.setStyleSheet(self._conn_style(theme.WARN))
        self.conn_pill.setToolTip("2.4GHz dongle is plugged in, but mouse is offline or switched to Bluetooth.")
        self.battery.setText("")
        self.dpi_readout.setText("—")
        self.rate_readout.setText("—")

    def set_disconnected(self):
        self.conn_pill.setText("● not connected")
        self.conn_pill.setStyleSheet(self._conn_style(theme.BAD))
        self.conn_pill.setToolTip("Mouse not detected. Searching for connection…")
        self.battery.setText("")
        self.dpi_readout.setText("—")
        self.rate_readout.setText("—")

    def set_error(self, msg):
        self.conn_pill.setText("● not connected")
        self.conn_pill.setStyleSheet(self._conn_style(theme.BAD))
        self.conn_pill.setToolTip(msg)

    def set_battery(self, percent, charging=False):
        if percent is None:
            self.battery.setText("")
            return
        icon = "⚡" if charging else "▮"
        color = theme.GOOD if percent > 40 else theme.WARN if percent > 15 else theme.BAD
        if charging:
            color = theme.ACCENT_2
        self.battery.setText(f"{icon} {percent}%")
        self.battery.setStyleSheet(f"color: {color}; font-family: {theme.FONT_MONO}; font-size: 12px;")

    def set_dpi_readout(self, text):
        text = str(text)
        # live pushes repeat the same value after every apply; skip the relayout
        if self.dpi_readout.text() != text:
            self.dpi_readout.setText(text)

    def set_busy(self, busy):
        if busy:
            if not self._spin_timer.isActive():
                self._spin_timer.start()
                self._tick_spinner()
        else:
            self._spin_timer.stop()
            self.spinner.setText("")

    def _tick_spinner(self):
        self._spin_i = (self._spin_i + 1) % len(self._spin_frames)
        self.spinner.setText(f"{self._spin_frames[self._spin_i]} applying...")
        self.spinner.setStyleSheet(f"color: {theme.ACCENT_2};")

    def set_rate_readout(self, hz):
        text = f"{hz}" if hz is not None else "—"
        if self.rate_readout.text() != text:
            self.rate_readout.setText(text)


class MainWindow(QMainWindow):
    def __init__(self, demo=False, verbose=False):
        super().__init__()
        self.demo = bool(demo)
        self.verbose = bool(verbose)
        # Apply mode is a saved setting (auto by default). --verbose still
        # starts in manual mode for diagnostics; the Settings dialog can change
        # it for this and future sessions.
        self._pending_apply = False
        self.setWindowTitle("SOLAKAKA SM809 Wired — Studio")
        self.setWindowIcon(app_icon())
        self.resize(1000, 680)
        self.setMinimumSize(820, 560)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # profile store (host-side source of truth; makes bindings persist)
        self.profiles = ProfileStore()
        self.manual_apply = bool(
            self.verbose or self.profiles.get_setting("manual_apply", False))
        # Recoil Control is still a work in progress.  Its rail page and picker
        # category stay hidden until the Settings switch is turned on.
        self.developer = bool(
            self.profiles.get_setting("developer_features", False))
        self._current_config = None
        self._pushed_pid = None      # profile id most recently written to the device
        self._pushed_config = None   # exact config of that write (to skip no-ops)
        self._loading_profile = False
        self._profile_mru = []      # recently-active profile ids (most-recent first)

        self.topbar = TopBar()
        self.topbar.set_manual_apply(self.manual_apply)
        self.topbar.apply_btn.clicked.connect(self._manual_apply_now)
        outer.addWidget(self.topbar)

        # Body (rail + panels) and the optional log panel share a splitter, so
        # the log can be resized or closed without disturbing the pages.
        body_host = QWidget()
        body = QHBoxLayout(body_host)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.body_split = QSplitter(Qt.Vertical)
        self.body_split.setChildrenCollapsible(False)
        self.body_split.addWidget(body_host)
        self.body_split.setStretchFactor(0, 1)
        outer.addWidget(self.body_split, 1)

        # ---- left rail: full-height surface; nav at top, reset near bottom ----
        rail = QFrame()
        rail.setObjectName("railFrame")
        rail.setFixedWidth(180)
        rail.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        rail_lay = QVBoxLayout(rail)
        rail_lay.setContentsMargins(0, 0, 0, 0)
        rail_lay.setSpacing(0)

        # profile selector at the top of the rail
        rail_lay.addWidget(self._build_profile_bar())

        self.nav = QListWidget()
        self.nav.setObjectName("nav")
        self.nav.setFrameShape(QFrame.NoFrame)
        # Rail rows are a filtered view of NAV_ITEMS; each row stores its
        # stack index so hidden pages do not shift the mapping.
        self._populate_nav()
        self.nav.currentRowChanged.connect(self._on_nav)
        # The rail gives the list all the space left by the profile bar and
        # the footer.  A short window (its 560 px minimum) cannot show eight
        # 55 px rows plus the footer, so let the list scroll instead of
        # drawing the footer over the last entries.
        self.nav.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.nav.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nav.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.nav.setSelectionMode(QAbstractItemView.SingleSelection)
        rail_lay.addWidget(self.nav, 1)

        sep = QFrame()
        sep.setProperty("sep", "true")
        sep.setFrameShape(QFrame.NoFrame)
        rail_lay.addWidget(sep)
        rail_lay.addSpacing(10)

        self.reset_btn = QPushButton("Reset to Factory")
        self.reset_btn.setObjectName("resetBtn")
        self.reset_btn.clicked.connect(self._confirm_reset)
        rail_lay.addWidget(self.reset_btn, 0)
        rail_lay.addSpacing(14)

        body.addWidget(rail)

        # ---- stacked panels (order matches NAV_ITEMS) ----
        self.stack = QStackedWidget()
        body.addWidget(self.stack, 1)

        self.store = MacroStore()
        self.guns = GunStore()
        set_macro_resolver(lambda mid: (self.store.get(mid) or {}).get("name", "Macro"))
        self.profiles.macro_events = lambda mid: (self.store.get(mid) or {}).get("events")
        self.profiles.gun_rows = lambda gid: (self.guns.get(gid) or {}).get("rows")
        self.buttons_panel = ButtonsPanel(get_macros=self.store.all,
                                          get_guns=self.guns.all,
                                          developer=self.developer)
        self.buttons_panel.set_manual_apply(self.manual_apply)
        self.macro_panel = MacroPanel(self.store)
        self.gun_panel = GunPanel(self.guns, self.profiles.get_setting,
                                  self.profiles.set_setting)
        self.gun_panel.set_developer(self.developer)
        self.dpi_panel = DpiPanel(embedded=True)
        self.lighting_panel = LightingPanel()
        self.performance_panel = PerformancePanel()
        self.performance_panel.add_dpi_section(self.dpi_panel)
        self.performance_panel.set_manual_apply(self.manual_apply)
        # Auto-switch is not a page any more: the Profiles tab's "Manage apps…"
        # opens this dialog, and the panel below is its content.
        self.manage_apps_dialog = ManageAppsDialog(self)
        self.autoswitch_panel = self.manage_apps_dialog.panel
        self.profiles_panel = ProfilesPanel()
        self.stack.addWidget(self.buttons_panel)         # 0 Buttons
        self.stack.addWidget(self.macro_panel)            # 1 Macro
        self.stack.addWidget(self.gun_panel)              # 2 Gun
        self.stack.addWidget(self.lighting_panel)         # 3 Lighting
        self.stack.addWidget(self.performance_panel)      # 4 Performance
        self.stack.addWidget(self.profiles_panel)         # 5 Profiles
        self.nav.setCurrentRow(0)

        # ---- controller ----
        # Adopt macros/guns embedded in the wired profiles into the editable
        # libraries (their ids are stable: dev:<profile id>:<slot>).
        self._adopt_device_macros()
        self._adopt_device_guns()

        self.ctrl = DeviceController(self.profiles, demo=demo)
        self.ctrl.connected.connect(self._on_connected)
        self.ctrl.disconnected.connect(self.topbar.set_disconnected)
        self.ctrl.error.connect(self._on_error)
        self.ctrl.dpi_level_changed.connect(self._on_dpi_push)
        self.ctrl.rate_changed.connect(self._on_rate_push)
        self.ctrl.mode_changed.connect(self._on_mode_push)
        self.ctrl.command_done.connect(self._on_command_done)
        self.ctrl.busy_changed.connect(self.topbar.set_busy)
        self.ctrl.busy_changed.connect(self._on_busy_overlay)

        self.dpi_panel.apply_requested.connect(self._apply_dpi)
        self.dpi_panel.active_dpi_requested.connect(self._apply_active_dpi)
        self.buttons_panel.apply_requested.connect(self._apply_buttons)
        self.buttons_panel.mode_changed.connect(self._apply_buttons_mode)
        self.lighting_panel.apply_requested.connect(self._apply_lighting)
        self.performance_panel.polling_changed.connect(self._apply_polling)
        self.performance_panel.pointer_changed.connect(self._apply_pointer)
        self.performance_panel.key_response_changed.connect(self._apply_key_response)
        self.macro_panel.library_changed.connect(self._on_library_changed)
        self.gun_panel.library_changed.connect(self._on_gun_library_changed)
        self.autoswitch_panel.enable_toggled.connect(self._toggle_autoswitch)
        self.autoswitch_panel.rules_changed.connect(self._on_rules_changed)
        self.autoswitch_panel.app_detected.connect(self._on_app_detected)
        self.profiles_panel.profile_selected.connect(self._select_profile)
        self.profiles_panel.order_changed.connect(self._on_profile_reorder)
        self.profiles_panel.sort_changed.connect(self._on_profile_sort)
        self.profiles_panel.new_requested.connect(self._profile_new)
        self.profiles_panel.duplicate_requested.connect(self._profile_duplicate)
        self.profiles_panel.rename_requested.connect(self._profile_rename)
        self.profiles_panel.delete_requested.connect(self._profile_delete)
        self.profiles_panel.import_requested.connect(self._profile_import)
        self.profiles_panel.export_requested.connect(self._profile_export_pbin)
        self.profiles_panel.manage_apps_requested.connect(self._on_manage_apps)

        # debounce a device re-sync when a bound macro's body is edited
        self._macro_resync = QTimer(self)
        self._macro_resync.setSingleShot(True)
        self._macro_resync.setInterval(500)
        self._macro_resync.timeout.connect(self._resync_macros)

        # same for a bound recoil pattern edited in the Gun tab
        self._gun_resync = QTimer(self)
        self._gun_resync.setSingleShot(True)
        self._gun_resync.setInterval(500)
        self._gun_resync.timeout.connect(self._resync_guns)

        # debounce disk persistence of profile edits: live sliders/bindings
        # change the in-memory wired record instantly, but a full table write is
        # ~1.65 MB, so batch it into one short write after the user pauses.
        self._persist_timer = QTimer(self)
        self._persist_timer.setSingleShot(True)
        self._persist_timer.setInterval(600)
        self._persist_timer.timeout.connect(self._flush_profile_save)

        # seed every panel from the active profile (display only; the device is
        # pushed once it connects, see _on_connected). This is what makes button
        # bindings + all settings survive restarts.
        active = self.profiles.active()
        self._applied_id = active["id"] if active else None   # what's on the device
        self._cur_dpi = None
        self._cur_rate = None
        self._cur_profile = active["name"] if active else None
        if active is not None:
            self._current_config = copy.deepcopy(active["config"])
            self._seed_panels(self._current_config)
        self._refresh_profile_combo()

        # Drop supported files anywhere on the window (or the non-modal
        # Manage Apps dialog). The router only claims drags carrying local
        # file URLs, so the Profiles list keeps its internal reorder drag.
        self._drop_router = FileDropRouter(self)
        self._drop_router.files_dropped.connect(self._files_dropped)

        # on-screen overlay HUD (optional): flashes DPI / profile / rate changes.
        self.overlay = Overlay()
        self.alert_overlay = AlertOverlay()
        self._overlay_enabled = bool(self.profiles.get_setting("overlay", False))
        self._overlay_show = dict(self.profiles.get_setting(
            "overlay_show", {"profile": True, "dpi": True, "rate": False}))
        # Profile switches are announced on the overlay instead of a Windows
        # tray toast. This stays available even when the ambient overlay is
        # off (DPI/rate cards), so the switch notice has its own switch.
        self._overlay_switch = bool(self.profiles.get_setting(
            "overlay_switch", True))
        # The original driver always shows a "DPI : <value>" card when the
        # stage changes (including the physical DPI buttons). Keep that on by
        # default and independent of the optional profile/polling overlay.
        self._dpi_osd = bool(self.profiles.get_setting(
            "dpi_osd", self._overlay_show.get("dpi", True)))
        self._apply_overlay_appearance()
        self._prev_dpi_level = None
        self._prev_rate = None
        self._prev_overlay_pid = self._applied_id
        self._overlay_pending = False    # flash the overlay when an apply finishes

        # per-app auto-switch (the headline feature). Base = the manual profile;
        # see app/autoswitch.py. Apply by id WITHOUT changing the manual base.
        self._auto = AutoSwitcher(self.profiles, self._apply_by_id,
                                  lambda: self._applied_id)
        self._auto.set_base(self._applied_id)
        self._auto.switched.connect(self._on_auto_switched)

        # Live log panel: hidden until Settings enables it.
        self.log_panel = LogPanel()
        self.log_panel.close_requested.connect(self._close_log_panel)
        self.body_split.addWidget(self.log_panel)
        self.body_split.setStretchFactor(1, 0)
        self._show_log = bool(self.profiles.get_setting("show_log", self.verbose))
        self._set_log_visible(self._show_log, persist=False)

        self._setup_tray()
        if self.profiles.get_setting("auto_switch", False):
            self._auto.set_enabled(True)
            self._sync_autoswitch_ui(True)
        self._sync_overlay_ui(self._overlay_enabled)
        self._sync_dpi_osd_ui(self._dpi_osd)

        self._restore_window_geometry()
        self.ctrl.start()

    # -- nav ------------------------------------------------------------------
    def _nav_entries(self):
        """The rail entries for the current feature set.

        Recoil Control is a developer preview: its page and picker category
        exist but stay out of the normal UI until Settings enables them.
        """
        return [name for name in NAV_ITEMS
                if name != "Recoil Control" or self.developer]

    def _populate_nav(self):
        """Rebuild the rail without emitting a page change."""
        self.nav.blockSignals(True)
        self.nav.clear()
        for name in self._nav_entries():
            item = QListWidgetItem(name, self.nav)
            # the stack keeps every page, so store the real index on the row
            item.setData(Qt.UserRole, NAV_ITEMS.index(name))
        self.nav.blockSignals(False)

    def _page_name(self):
        item = self.nav.currentItem()
        return item.text() if item is not None else None

    def _select_page(self, name):
        """Show the named page; returns False when it is currently hidden."""
        for row in range(self.nav.count()):
            if self.nav.item(row).text() == name:
                self.nav.setCurrentRow(row)
                return True
        return False

    def _on_nav(self, row):
        item = self.nav.item(row) if 0 <= row < self.nav.count() else None
        idx = item.data(Qt.UserRole) if item is not None else None
        if idx is not None and 0 <= int(idx) < self.stack.count():
            self.stack.setCurrentIndex(int(idx))

    def _set_developer(self, on, persist=True):
        """Show/hide the Recoil Control preview page and picker category."""
        on = bool(on)
        if on == self.developer:
            return
        current = self._page_name()
        self.developer = on
        self.buttons_panel.set_developer(on)
        self.gun_panel.set_developer(on)
        self._populate_nav()
        # Stay on the same page where possible; a page that just disappeared
        # (Recoil Control) falls back to the first entry.
        if not self._select_page(current or "Buttons"):
            self.nav.setCurrentRow(0)
        if persist:
            self.profiles.set_setting("developer_features", on)

    # -- profiles -------------------------------------------------------------
    def _build_profile_bar(self):
        """A compact profile QUICK-SWITCH combo pinned at the top of the nav rail.
        Profile management (New/Duplicate/Rename/Delete/Import) lives in the
        Profiles tab."""
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setContentsMargins(12, 14, 12, 10)
        lay.setSpacing(6)
        cap = QLabel("PROFILE")
        cap.setProperty("unit", "true")
        lay.addWidget(cap)

        self.profile_combo = QComboBox()
        self.profile_combo.setObjectName("profileCombo")
        self.profile_combo.currentIndexChanged.connect(self._on_profile_selected)
        lay.addWidget(self.profile_combo)
        return w

    def _refresh_profile_combo(self):
        """Rebuild the combo from the store without triggering a profile apply."""
        # one cheap summary list feeds the combo, Manage Apps and Profiles tabs
        # (loading every full config three times made this noticeably slow).
        profiles = self.profiles.summaries()
        # Show the profile that is actually on the mouse. When auto-switch has
        # overridden the manual base, a refresh (rename, reorder, rule edit…)
        # must not snap the combo or the Profiles tab back to the base.
        shown = self._shown_profile_id(profiles)
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        shown_idx = 0
        for i, p in enumerate(profiles):
            self.profile_combo.addItem(p["name"], p["id"])
            if p["id"] == shown:
                shown_idx = i
        self.profile_combo.setCurrentIndex(shown_idx)
        self.profile_combo.blockSignals(False)
        # keep the Manage Apps panel + Profiles tab in sync
        if hasattr(self, "autoswitch_panel"):
            self.autoswitch_panel.set_profiles(profiles,
                                               self.profiles.active_id)
        if hasattr(self, "profiles_panel"):
            self.profiles_panel.set_profiles(
                profiles, shown,
                self.profiles.get_setting("profile_sort", "custom"))

    def _shown_profile_id(self, profiles=None):
        """The profile the rail combo + Profiles tab should highlight: the one
        applied to the mouse (auto-switch override) and otherwise the manual
        base. Falls back to the base if the applied id no longer exists."""
        ids = {p["id"] for p in (profiles if profiles is not None
                                 else self.profiles.summaries())}
        if self._applied_id in ids:
            return self._applied_id
        return self.profiles.active_id

    def _on_profile_reorder(self, ids):
        self.profiles.reorder(ids)
        self.profiles.set_setting("profile_sort", "custom")
        self._refresh_profile_combo()
        if self._auto is not None and self._auto.is_enabled():
            self._auto.poll()      # match priority changed -> re-evaluate

    def _on_profile_sort(self, key):
        self.profiles.sort_by(key)
        self.profiles.set_setting("profile_sort", key)
        self._refresh_profile_combo()
        if self._auto is not None and self._auto.is_enabled():
            self._auto.poll()

    def _on_rules_changed(self, pid, rules):
        self.profiles.set_match_rules(pid, rules)
        if hasattr(self, "profiles_panel"):
            self.profiles_panel.set_match_rules(pid, rules)
        if getattr(self, "_auto", None) is not None and self._auto.is_enabled():
            self._auto.poll()   # let a just-added rule take effect immediately

    def _on_app_detected(self, exe, title):
        """Flash the on-screen overlay to confirm what 'Detect app' captured --
        shown even if the overlay is otherwise disabled (the user explicitly
        asked to detect), and inheriting the overlay's appearance settings."""
        lines = [("Detected App", exe)]
        if title:
            lines.append(("Window", title if len(title) <= 28 else title[:27] + "…"))
        self.overlay.flash_lines(lines)

    def _on_manage_apps(self, pid):
        """Open the Manage Apps popup with this profile selected."""
        if not pid:
            return
        self.manage_apps_dialog.show_for(
            self.profiles.summaries(), pid, self._auto.is_enabled())
        self._attach_native_drop(self.manage_apps_dialog)

    # -- drop support while elevated -----------------------------------------
    def enable_native_drop(self):
        """Install the legacy drop bridge when Windows refuses OLE drops.

        The studio elevates by default, and a high-integrity window cannot
        receive Explorer's OLE drag (UIPI).  ``app.win_drop`` revokes the OLE
        drop target and listens for WM_DROPFILES instead; the router then
        imports the paths exactly like a normal drop.
        """
        if getattr(self, "_native_drop", None) is not None:
            return self._native_drop
        from .win_drop import attach_elevated_drop
        bridge = attach_elevated_drop(self._drop_router, self)
        self._native_drop = bridge
        if bridge is not None:
            # in-window drag reordering needs the OLE target we just revoked
            self.profiles_panel.set_native_drop_mode(True)
        return bridge

    def _attach_native_drop(self, window):
        bridge = getattr(self, "_native_drop", None)
        if bridge is not None:
            bridge.attach(window)

    def showEvent(self, event):
        super().showEvent(event)
        if not getattr(self, "_native_drop_checked", False):
            self._native_drop_checked = True
            # winId()/the OLE target only exist once the window is shown
            QTimer.singleShot(0, self.enable_native_drop)

    def _on_profile_selected(self, idx):
        # a MANUAL selection from the combo -> this becomes the sticky base
        if idx < 0:
            return
        pid = self.profile_combo.itemData(idx)
        if self.profiles.get(pid) is None:
            return
        self._select_profile(pid)

    def _select_profile(self, pid):
        """Manually activate a profile: it becomes the auto-switch base AND is
        applied to the device. Records the profile we're leaving in the MRU so a
        later delete can fall back to it (alt-tab style)."""
        prev = self.profiles.active_id
        if prev and prev != pid:
            self._profile_mru = [prev] + [x for x in self._profile_mru if x not in (prev, pid)]
        self.profiles.set_active(pid, persist=False)
        self._schedule_profile_save()      # batched sidecar write
        if getattr(self, "_auto", None) is not None:
            self._auto.set_base(pid)
        # Keep the Manage Apps dialog (if open) on the profile the user just
        # picked, so its custom-app list is the one they expect to see.
        if hasattr(self, "autoswitch_panel"):
            self.autoswitch_panel.select_profile(pid)
        self._apply_by_id(pid)

    def _apply_by_id(self, pid):
        """Apply the profile `pid` to panels + device and mark it as what's
        currently on the device. Does NOT change the manual base (auto-switch
        matches stay until another rule matches). Updates the combo display
        silently."""
        prof = self.profiles.get(pid)
        if prof is None:
            return
        changed = (pid != self._applied_id)
        self._applied_id = pid
        self._sync_combo(pid)
        self._cur_profile = prof["name"]
        # The overlay IS the switch notification (there is no tray toast).
        # ``overlay_switch`` is its own switch so a profile change is announced
        # even when the ambient DPI/polling overlay is turned off.
        notify = (changed and self._overlay_switch
                  and pid != self._prev_overlay_pid)
        if notify:
            # immediate "Switching to X" feedback while the writes are in flight
            # (useful when auto-switching from a fullscreen game); the detailed
            # card replaces it once the apply finishes (_on_busy_overlay).
            self.overlay.flash_lines([("Switching to", prof["name"])], hold_ms=5000)
        self._prev_overlay_pid = pid
        queued = self.apply_profile(prof["config"], pid=pid)
        # Only wait for the done signal when a write was actually queued.  A
        # profile already on the device (or a skipped push) would otherwise
        # leave the card on "Switching to…" until the next unrelated apply.
        if notify:
            self._overlay_pending = bool(queued)
            if not queued:
                self._overlay_flash(switch=True)

    def _overlay_flash(self, switch=False):
        """Flash the overlay for a finished apply.

        ``switch=True`` is the profile-switch notification; it obeys the
        dedicated ``overlay_switch`` setting so it works with the ambient
        overlay off. Otherwise this is the DPI/polling status card, which
        needs the ambient overlay enabled and follows "Profile name".
        """
        show = self._overlay_show
        lines = []
        if switch:
            if self._overlay_switch and self._cur_profile:
                lines.append(("Profile", self._cur_profile))
        elif self._overlay_enabled:
            if show.get("profile", True) and self._cur_profile:
                lines.append(("Profile", self._cur_profile))
            if show.get("dpi", True) and self._cur_dpi is not None:
                lines.append(("DPI", self._cur_dpi))
            if show.get("rate", False) and self._cur_rate is not None:
                lines.append(("Polling Rate", f"{self._cur_rate} Hz"))
        if lines:
            self.overlay.flash_lines(lines)

    def _on_busy_overlay(self, busy):
        """When the device write queue drains after a profile apply, flash the
        overlay -- so it confirms the profile is DONE applying, not just queued."""
        if not busy and self._overlay_pending:
            self._overlay_pending = False
            self._overlay_flash(switch=True)

    def _apply_overlay_appearance(self):
        """Push the saved overlay appearance settings to BOTH overlays (the
        transient HUD and the persistent battery alert)."""
        kw = dict(
            position=self.profiles.get_setting("overlay_pos", "bottom-center"),
            opacity_pct=self.profiles.get_setting("overlay_opacity", 92),
            scale_pct=self.profiles.get_setting("overlay_scale", 100),
            hold_ms=self.profiles.get_setting("overlay_hold", 1400),
            follow_cursor=self.profiles.get_setting("overlay_follow_cursor", True),
            monitor_index=self.profiles.get_setting("overlay_monitor", 0))
        self.overlay.set_appearance(**kw)
        self.alert_overlay.set_appearance(**kw)   # ignores hold_ms

    def _sync_combo(self, pid):
        """Point the combo at `pid` without triggering a manual selection."""
        self.profile_combo.blockSignals(True)
        for i in range(self.profile_combo.count()):
            if self.profile_combo.itemData(i) == pid:
                self.profile_combo.setCurrentIndex(i)
                break
        self.profile_combo.blockSignals(False)

    def _on_auto_switched(self, pid):
        """A rule matched: make the UI follow the profile now on the mouse.

        Auto-switch no longer reverts when focus leaves the app, so this only
        runs for real matches. The manual base is NOT changed -- it is what
        turning auto-switch off returns to -- this only moves the rail combo
        and the Profiles tab, which previously kept showing the base and made
        auto-switch look like it had done nothing.

        The on-screen overlay announces the switch (see _apply_by_id); there
        is deliberately no Windows tray toast for it any more.
        """
        prof = self.profiles.get(pid)
        if prof is None:
            return
        _log.info("auto-switch: UI now on %r", prof["name"])
        self._sync_combo(pid)
        if hasattr(self, "profiles_panel"):
            self.profiles_panel.show_active(pid)

    def apply_profile(self, config, force=False, pid=None, reseed=True):
        """Load a config into every panel and write the complete wired profile.

        The wired firmware receives whole profiles (there is no per-section
        command), so every change is one ordered ``apply_config`` call. The
        worker thread keeps the UI responsive while the frames are sent.

        ``reseed=False`` is for the connect-time push: the panels already show
        the same config, and reseeding them would cancel an edit the user made
        while the device was connecting (its 250 ms debounce has not fired yet).
        """
        config = copy.deepcopy(config)
        self._current_config = config
        if reseed:
            self._seed_panels(config)          # refresh the UI (no I/O)

        target = pid or self._applied_id or self.profiles.active_id
        if target is None or self._loading_profile:
            return False
        previous = self._pushed_config if self._pushed_pid == target else None
        if force or previous is None or previous != config:
            self._pushed_pid = target
            self._pushed_config = copy.deepcopy(config)
            self.ctrl.call("apply_config", copy.deepcopy(config), target)
            return True
        return False

    def _seed_panels(self, config):
        """Set every panel from a config dict WITHOUT emitting apply signals."""
        self._loading_profile = True
        try:
            # Patterns embedded in this profile become editable library entries
            # before the Buttons tab renders their labels.
            self._adopt_config_guns(config)
            dpi = config.get("dpi", {}) or {}
            self.buttons_panel.set_codes(config.get("buttons", []))
            # profile mode and UI layer share the same encoding:
            # 0 = Office Mode (slots 0-15), 1 = Game Mode (slots 32-47).
            self.buttons_panel.set_mode(int(config.get("mode", 0)))
            self.dpi_panel.set_values(dpi.get("values", []),
                                      dpi.get("colors"),
                                      enabled_count=dpi.get("enabled_count"))
            self.dpi_panel.set_active_stage(dpi.get("selected", 0))
            light = config.get("lighting", {}) or {}
            light_params = {k: light.get(k) for k in
                            ("brightness", "length", "frequency", "direction")}
            light_params["colors"] = light.get("colors")
            self.lighting_panel.set_state(
                light.get("mode", 0), tuple(light.get("color", (255, 0, 0))),
                light_params)
            self.performance_panel.set_state(
                polling_hz=config.get("polling_hz"),
                pointer=config.get("pointer"),
                key_response=config.get("key_response"))
        finally:
            self._loading_profile = False
        self._seed_readouts(config)

    def _seed_readouts(self, config):
        """Reflect a config's active DPI stage and polling rate in the top bar."""
        if not config:
            return
        dpi = config.get("dpi") or {}
        values = dpi.get("values") or []
        if values:
            sel = max(0, min(int(dpi.get("selected", 0)), len(values) - 1))
            self._cur_dpi = int(values[sel])
            self.topbar.set_dpi_readout(f"{self._cur_dpi}")
        rate = config.get("polling_hz")
        if rate:
            self._cur_rate = int(rate)
            self.topbar.set_rate_readout(self._cur_rate)

    def _schedule_profile_save(self):
        """Batch a config edit into one table write after a short pause."""
        self._persist_timer.start()

    def _flush_profile_save(self):
        """Write any deferred profile edit now (timer, tray hide, quit)."""
        self._persist_timer.stop()
        self.profiles.flush()

    def _persist_and_push(self):
        """Persist the in-memory config into its wired profile and queue a
        complete device write. The wired firmware has no partial commands.

        In manual-apply mode the profile is updated on disk but the mouse
        write is deferred until the top-bar Apply button is clicked.
        """
        pid = self._applied_id or self.profiles.active_id
        if pid is None or self._current_config is None:
            return
        # The worker writes the table after the frames go out, so this only
        # updates memory; a debounced flush covers failed/absent applies.
        self.profiles.set_config(pid, self._current_config, persist=False)
        self._schedule_profile_save()
        if self.manual_apply:
            self._mark_pending()
            return
        self._pushed_pid = pid
        self._pushed_config = copy.deepcopy(self._current_config)
        self.ctrl.call("apply_config", copy.deepcopy(self._current_config), pid)

    def _mark_pending(self):
        """Flag that edits are staged but not yet written to the mouse."""
        if not self.manual_apply:
            return
        if not self._pending_apply:
            self._pending_apply = True
            self.topbar.set_pending(True)
            _log.info("edit staged; click Apply to write it to the mouse")

    def set_manual_apply(self, enabled, persist=True):
        """Switch between auto-apply and manual-apply for every page.

        Turning auto-apply on writes any staged edits immediately, so the user
        never ends up with changes that only exist on disk.
        """
        enabled = bool(enabled)
        pending = self._pending_apply
        self.manual_apply = enabled
        if persist:
            self.profiles.set_setting("manual_apply", enabled)
        self.topbar.set_manual_apply(enabled)
        self.buttons_panel.set_manual_apply(enabled)
        self.performance_panel.set_manual_apply(enabled)
        _log.info("apply mode: %s", "manual" if enabled else "auto")
        if pending and not enabled:
            _log.info("auto-apply selected; writing staged changes now")
            self._pending_apply = False
            self.topbar.set_pending(False)
            if self._current_config is not None:
                self.apply_profile(self._current_config, force=True, reseed=False)

    def _manual_apply_now(self):
        """Write the current (or staged) config to the mouse now."""
        if self._current_config is None:
            return
        if self._pending_apply:
            _log.info("manual apply requested")
        # The panels already show this state, so do not reseed them.
        self._pending_apply = False
        self.topbar.set_pending(False)
        self.apply_profile(self._current_config, force=True, reseed=False)

    def _update_config(self, section, value):
        """Record a live edit into the applied profile and persist it. This is how
        button bindings + every other setting survive restarts."""
        if self._current_config is None or self._loading_profile:
            return
        if self._current_config.get(section) == value:
            return          # nothing changed -> no profile upload, no disk write
        self._current_config[section] = value
        self._persist_and_push()

    def _profile_new(self):
        # Prefill the positional number (Profile 2, Profile 3, ...) so pressing
        # Enter keeps counting even when existing profiles have custom names.
        name, ok = QInputDialog.getText(
            self, "New profile", "Profile name:",
            text=self.profiles.next_default_name())
        if not ok or not name.strip():
            return
        # a new profile starts from FACTORY DEFAULTS (not a copy of the current
        # one -- use Duplicate for that)
        try:
            p = self.profiles.add(name.strip(), config=default_config())
        except ValueError as exc:
            QMessageBox.information(self, "New profile", str(exc))
            return
        self._refresh_profile_combo()
        self._select_profile(p["id"])

    def _adopt_device_macros(self):
        """Make macros embedded in wired profiles editable in the library."""
        for mid, name, events in self.profiles.embedded_macros():
            self.store.add_with_id(mid, name, events, persist=False)
        # one library write for the whole batch, and none when nothing changed
        self.store.save_if_dirty()

    def _adopt_device_guns(self):
        """Make recoil patterns embedded in wired profiles editable too."""
        for gid, name, rows, _repeat in self.profiles.embedded_guns():
            self.guns.add_with_id(gid, name, rows, persist=False)
        self.guns.save_if_dirty()

    def _adopt_config_guns(self, config):
        """Adopt gun bindings from a config before its labels are rendered."""
        for binding in (config or {}).get("buttons") or ():
            if isinstance(binding, dict) and binding.get("gun"):
                self.guns.add_with_id(binding["gun"], binding.get("name"),
                                      binding.get("rows"), persist=False)
        self.guns.save_if_dirty()

    def _target_profile_id(self):
        """Management actions (Duplicate/Rename/Delete) target the row SELECTED in
        the Profiles tab, falling back to the active profile."""
        pid = self.profiles_panel.selected_id() if hasattr(self, "profiles_panel") else None
        return pid if (pid and self.profiles.get(pid)) else self.profiles.active_id

    def _profile_duplicate(self):
        cur = self._target_profile_id()
        if not cur:
            return
        try:
            p = self.profiles.duplicate(cur)
        except ValueError as exc:
            QMessageBox.information(self, "Duplicate profile", str(exc))
            return
        if p is not None:
            self._refresh_profile_combo()
            self._select_profile(p["id"])

    def _profile_rename(self):
        cur = self.profiles.get(self._target_profile_id())
        if cur is None:
            return
        name, ok = QInputDialog.getText(self, "Rename profile", "Profile name:",
                                        text=cur["name"])
        if ok and name.strip():
            self.profiles.rename(cur["id"], name.strip())
            self._refresh_profile_combo()

    def _profile_delete(self):
        cur = self.profiles.get(self._target_profile_id())
        if cur is None:
            return
        if len(self.profiles.summaries()) <= 1:
            QMessageBox.information(self, "Delete profile",
                                    "Can't delete the only profile.")
            return
        box = QMessageBox(self)
        box.setWindowTitle("Delete profile")
        box.setText(f"Delete profile “{cur['name']}”?")
        box.setIcon(QMessageBox.Warning)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.Cancel)
        if box.exec() != QMessageBox.Yes:
            return
        was_active = (cur["id"] == self.profiles.active_id)
        idx = self.profiles.index_of(cur["id"])
        try:
            self.profiles.delete(cur["id"])
        except ValueError as exc:
            QMessageBox.information(self, "Delete profile", str(exc))
            return
        remaining = self.profiles.summaries()
        if not remaining:
            return
        ids = {p["id"] for p in remaining}
        self._profile_mru = [x for x in self._profile_mru if x in ids]
        self._refresh_profile_combo()
        # deleting a NON-active profile leaves the active one alone; deleting the
        # active one falls back to the last profile set (MRU), else the neighbour.
        if was_active:
            target = self._profile_mru[0] if self._profile_mru else \
                remaining[max(0, min(idx - 1, len(remaining) - 1))]["id"]
            self.profiles.set_active(target)
            if self._auto is not None:
                self._auto.set_base(target)
            self._apply_by_id(target)

    def _profile_import(self):
        """Pick one or more files for the shared batch importer."""
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Import files", "",
            f"{ALL_SUPPORTED_FILTER};;{PROFILE_FILTER};;{MACRO_FILTER};;"
            "All files (*)")
        if paths:
            self.import_files(paths)

    def _files_dropped(self, paths):
        """A supported drop landed somewhere on the window."""
        self.import_files(paths)

    def import_files(self, paths, notify=True):
        """Import a mixed batch of profiles and macros with per-file isolation.

        This is the single path used by the Import dialog, drag-and-drop and
        tests.  One unreadable file never cancels the rest of the batch; the
        profile limit is checked per file; and the batch is applied to the
        mouse once (the last imported profile), not once per file.

        Returns ``{"profiles", "macros", "errors", "ignored", "warnings",
        "skipped"}``.  ``errors`` holds ``(file name, message)`` pairs.
        """
        profile_paths, macro_paths, ignored = split_paths(paths)

        imported_profiles = []
        warnings = []
        errors = []
        skipped = 0
        for path in profile_paths:
            if self.profiles.at_limit():
                skipped += 1
                continue
            try:
                if path.casefold().endswith(".psf"):
                    prof, notes = self.profiles.import_psf(path, self.store)
                    imported_profiles.append(prof)
                    warnings.extend(
                        f"{os.path.basename(path)}: {note}" for note in notes)
                else:
                    imported_profiles.append(self.profiles.import_pbin(path))
            except Exception as exc:
                errors.append((os.path.basename(path), str(exc)))

        imported_macros = []
        if macro_paths:
            imported_macros, macro_errors = self.macro_panel.import_macro_files(
                macro_paths, report=False)
            errors.extend(macro_errors)

        if imported_profiles:
            # The records embed macros and recoil patterns; adopt them so they
            # are editable, then select/apply the last imported profile once.
            self._adopt_device_macros()
            self._adopt_device_guns()
            self._refresh_profile_combo()
            self.macro_panel._refresh_list()
            self.gun_panel._refresh_list()
            last = imported_profiles[-1]
            self._select_profile(last["id"])
            self.profiles_panel.show_active(last["id"])

        if imported_profiles or imported_macros or skipped or errors:
            _log.info(
                "Import batch: %d profile(s), %d macro(s), %d skipped, "
                "%d unsupported, %d failed",
                len(imported_profiles), len(imported_macros), skipped,
                len(ignored), len(errors))

        if notify:
            self._show_import_summary(imported_profiles, imported_macros,
                                      errors, ignored, skipped, warnings)
        return {
            "profiles": imported_profiles,
            "macros": imported_macros,
            "errors": errors,
            "ignored": ignored,
            "warnings": warnings,
            "skipped": skipped,
        }

    def _show_import_summary(self, profiles, macros, errors, ignored, skipped,
                             warnings):
        """One dialog for the whole batch; long detail goes to the detail pane."""
        if not (profiles or macros or errors or skipped):
            names = file_names(ignored, 8)
            extra = ("\n\nIgnored:\n" + "\n".join(f"• {n}" for n in names)
                     if names else "")
            QMessageBox.information(
                self, "Nothing imported",
                "No importable files were selected.\n\n"
                f"The studio reads {supported_hint()}.{extra}")
            return

        lines = []
        if profiles:
            if len(profiles) == 1:
                lines.append(f"Imported and applied “{profiles[0]['name']}”.")
            else:
                lines.append(
                    f"Imported {len(profiles)} profiles and applied "
                    f"“{profiles[-1]['name']}” (the last one).")
        if macros:
            lines.append(f"Imported {len(macros)} macro"
                         f"{'' if len(macros) == 1 else 's'} into the library.")
        if skipped:
            lines.append(f"Skipped {skipped} profile"
                         f"{'' if skipped == 1 else 's'}: the mouse stores at "
                         f"most {PROFILE_LIMIT}.")
        if ignored:
            lines.append(f"Ignored {len(ignored)} unsupported file"
                         f"{'' if len(ignored) == 1 else 's'}.")
        if errors:
            lines.append(f"{len(errors)} file{'' if len(errors) == 1 else 's'} "
                         "could not be imported.")

        details = []
        if ignored:
            details.append("Ignored (unsupported):\n" + "\n".join(
                f"• {name}" for name in file_names(ignored)))
        if errors:
            details.append("Could not import:\n" + "\n".join(
                f"• {name}: {why}" for name, why in errors))
        if warnings:
            details.append("Migration notes:\n" + "\n".join(
                f"• {note}" for note in warnings))

        box = QMessageBox(self)
        box.setWindowTitle("Import finished" if not errors
                           else "Import finished with warnings")
        box.setIcon(QMessageBox.Warning if errors else QMessageBox.Information)
        box.setText("\n".join(lines) or "Nothing was imported.")
        if errors:
            box.setInformativeText(
                "The other files in the batch were still imported.")
        if details:
            box.setDetailedText("\n\n".join(details))
        box.exec()

    def _profile_export_pbin(self):
        pid = self._target_profile_id()
        prof = self.profiles.get(pid) if pid else None
        if prof is None:
            return
        safe = "".join(c if c.isalnum() or c in " -_" else "_"
                       for c in prof["name"]).strip() or "profile"
        path, _ = QFileDialog.getSaveFileName(
            self, "Export wired profile", f"{safe}.pbin",
            "SM809 wired profile (*.pbin);;All files (*)")
        if not path:
            return
        try:
            self.profiles.export_pbin(pid, path)
        except Exception as exc:
            QMessageBox.warning(self, "Export failed", str(exc))
            return
        QMessageBox.information(
            self, "Profile exported",
            f"Saved “{prof['name']}” as a .pbin.\n\n"
            "The official driver can load this file with its profile menu (…) "
            "→ Import. The format is byte-for-byte the same 0x1CC50 record the "
            "driver exports.")

    # -- controller handlers --------------------------------------------------
    def _on_connected(self, info):
        self.topbar.set_connection(info)
        # The wired device is write-only for config, so push the active profile
        # now so the hardware matches our persisted settings (mirrors the
        # official app). force=True: on connect the device state is unknown.
        # In manual-apply mode nothing is written until Apply is clicked.
        if (not self.manual_apply and info.get("configurable", True)
                and self._current_config is not None):
            self.apply_profile(self._current_config, force=True, reseed=False)

    def _on_error(self, msg):
        self.topbar.set_error(msg)

    def _on_mode_push(self, layer):
        """The mouse switched Office/Game on its own (physical mode button).

        Follow it: the Keys page must show the layer the firmware actually
        runs, otherwise a new assignment would be written into the inactive
        half of the button table and appear to do nothing.
        """
        layer = 0 if int(layer) == 0 else 1
        self.buttons_panel.set_mode(layer)
        if self._current_config is None:
            return
        if int(self._current_config.get("mode", 0)) != layer:
            _log.info("mouse reports a switch to %s mode",
                      "Game" if layer else "Office")
        self._current_config["mode"] = layer   # 0 = Office, 1 = Game
        pid = self._applied_id or self.profiles.active_id
        if pid is not None:
            # Persist only -- the device already made this change.
            self.profiles.set_config(pid, self._current_config, persist=False)
            self._schedule_profile_save()

    def _on_dpi_push(self, level):
        # `level` is the device's stage number (index among enabled stages);
        # the panel maps it to the right row.
        self.dpi_panel.set_active_stage(level)
        row = self.dpi_panel.active_row()
        if row is not None:
            dpi = row.dpi()
            self.topbar.set_dpi_readout(f"{dpi}")
            self._cur_dpi = dpi
            # Flash a single "DPI" card on a real stage change (skip the first
            # push at connect). This mirrors the vendor driver's 0x469 overlay
            # and works even when the general profile/rate overlay is off.
            changed = (self._prev_dpi_level is not None
                       and level != self._prev_dpi_level)
            if changed and self._dpi_osd:
                self.overlay.flash(f"{dpi}", "DPI")
            self._prev_dpi_level = level

    def _on_rate_push(self, hz):
        self.topbar.set_rate_readout(hz)
        # keep the Performance panel's selector in sync with the live rate
        self.performance_panel.set_state(polling_hz=hz)
        self._cur_rate = hz
        if (self._overlay_enabled and self._overlay_show.get("rate", False)
                and self._prev_rate is not None and hz != self._prev_rate):
            self._overlay_flash()
        self._prev_rate = hz

    def _on_command_done(self, method, ok):
        if method != "apply_config" or ok:
            return
        # The mouse did not take this config. Forget the dedupe snapshot so an
        # identical retry (the next rule match, or a manual Apply) is written
        # again instead of being skipped as "already pushed".
        failed_pid = self._pushed_pid
        self._pushed_pid = None
        self._pushed_config = None
        # Never leave a "Switching to ..." card up when the write failed: settle
        # it with a truthful notice and let the next attempt announce itself.
        if self._overlay_pending:
            self._overlay_pending = False
            self._prev_overlay_pid = None
            prof = self.profiles.get(failed_pid) if failed_pid else None
            name = prof["name"] if prof is not None else self._cur_profile
            if self._overlay_switch and name:
                self.overlay.flash_lines([("Not applied", name)], hold_ms=4000)
        # A failed manual apply keeps the staged state marked as pending so the
        # user can fix the problem and press Apply again.
        if self.manual_apply:
            self._mark_pending()

    # -- actions --------------------------------------------------------------
    def _apply_dpi(self, dpi_values, colors, selected):
        if self._current_config is None or self._loading_profile:
            return
        colors = [list(c) for c in (colors or [])][:len(dpi_values)]
        self._current_config["dpi"] = {
            "values": [int(v) for v in dpi_values],
            "colors": colors,
            "enabled_count": len(dpi_values),
            "selected": int(selected),
        }
        self._persist_and_push()

    def _apply_active_dpi(self, dpi_values, selected):
        # Switch the live DPI stage.  The wired service re-sends the 0x11 DPI
        # table + 0x0B stage + commit, the sequence the firmware needs to latch
        # the new stage (a bare 0x0B frame is ignored).
        pid = self._applied_id or self.profiles.active_id
        if pid is None or self._current_config is None or self._loading_profile:
            return
        dpi = dict(self._current_config.get("dpi") or {})
        colors = [list(c) for c in (dpi.get("colors") or [])][:len(dpi_values)]
        dpi.update({
            "values": [int(v) for v in dpi_values],
            "colors": colors,
            "enabled_count": len(dpi_values),
            "selected": int(selected),
        })
        self._current_config["dpi"] = dpi
        self.profiles.set_config(pid, self._current_config, persist=False)
        self._schedule_profile_save()
        if self.manual_apply:
            # The pending Apply writes the stage together with everything else.
            self._mark_pending()
            return
        self.ctrl.call("set_active_dpi", pid, list(dpi_values), int(selected))

    def _apply_buttons_mode(self, layer):
        """Switch the mouse to the Office/Game layer being edited.

        The wired firmware only runs one layer at a time, and the vendor driver
        treats the Keys page's mode picker as the device's work mode. Keeping
        them in step is what makes an assignment on physical button 15/16 (DPI
        by default) actually take effect.
        """
        if self._current_config is None or self._loading_profile:
            return
        mode = 0 if int(layer) == 0 else 1   # 0 = Office, 1 = Game
        if int(self._current_config.get("mode", 0)) == mode:
            return
        self._update_config("mode", mode)

    def _apply_buttons(self, bindings):
        """Store all 64 bindings, resolving macro ids to embedded events.

        The wired firmware embeds the macro table inside the bound button entry
        (action 0x16), so no separate upload slot bookkeeping is needed.
        """
        if self._current_config is None or self._loading_profile:
            return
        stored = []
        for slot, b in enumerate(list(bindings)[:A.SLOT_COUNT]):
            if isinstance(b, dict) and "macro" in b:
                m = self.store.get(b["macro"])
                if m is None:
                    stored.append(list(A.BTN["unset"]))
                    continue
                item = dict(b)
                item["name"] = m.get("name") or item.get("name") or f"Macro {slot + 1}"
                item["events"] = list(m.get("events") or [])
                stored.append(item)
            elif isinstance(b, dict):
                stored.append(dict(b))
            else:
                stored.append(list(b) if b else list(A.BTN["unset"]))
        while len(stored) < A.SLOT_COUNT:
            stored.append(list(A.BTN["unset"]))
        self._current_config["buttons"] = stored
        self._persist_and_push()

    def _on_library_changed(self):
        # If a bound macro was deleted, restore that slot's factory action;
        # a body or name edit to a bound macro re-syncs to the device
        # (debounced). Binding dicts are refreshed from the library first so the
        # rows show current macro names.
        defaults = A.default_button_codes()
        reset_any = False
        for slot, b in enumerate(self.buttons_panel.bindings()):
            if isinstance(b, dict) and "macro" in b:
                m = self.store.get(b["macro"])
                if m is None:
                    fallback = defaults[slot]
                    if isinstance(fallback, dict) and "macro" in fallback:
                        self.store.add_with_id(fallback["macro"],
                                               fallback.get("name"),
                                               fallback.get("events"))
                    self.buttons_panel.set_binding(slot, fallback)
                    reset_any = True
                else:
                    item = dict(b)
                    item["name"] = m.get("name") or item.get("name")
                    item["events"] = list(m.get("events") or [])
                    self.buttons_panel.set_binding(slot, item)
        self.buttons_panel.refresh_labels()
        if reset_any:
            self._apply_buttons(self.buttons_panel.bindings())
        else:
            self._macro_resync.start()

    def _resync_macros(self):
        bindings = self.buttons_panel.bindings()
        if any(isinstance(b, dict) and "macro" in b for b in bindings):
            self._apply_buttons(bindings)

    def _on_gun_library_changed(self):
        """Refresh bound patterns; reset a slot whose pattern was deleted."""
        defaults = A.default_button_codes()
        reset_any = False
        bound = False
        for slot, b in enumerate(self.buttons_panel.bindings()):
            if not (isinstance(b, dict) and "gun" in b):
                continue
            g = self.guns.get(b["gun"])
            if g is None:
                fallback = defaults[slot]
                self.buttons_panel.set_binding(slot, fallback)
                reset_any = True
                continue
            item = dict(b)
            item["name"] = g.get("name") or item.get("name")
            item["rows"] = [list(r) for r in g.get("rows") or []]
            self.buttons_panel.set_binding(slot, item)
            bound = True
        self.buttons_panel.refresh_labels()
        if reset_any:
            self._apply_buttons(self.buttons_panel.bindings())
        elif bound:
            self._gun_resync.start()

    def _resync_guns(self):
        bindings = self.buttons_panel.bindings()
        if any(isinstance(b, dict) and "gun" in b for b in bindings):
            self._apply_buttons(bindings)

    def _apply_lighting(self, mode, color, params):
        if self._current_config is None or self._loading_profile:
            return
        light = dict(self._current_config.get("lighting") or {})
        light["mode"] = int(mode)
        light["color"] = [int(c) for c in color]
        for key in ("brightness", "length", "frequency", "direction"):
            if key in (params or {}):
                light[key] = int(params[key])
        if (params or {}).get("colors") is not None:
            light["colors"] = [[int(v) for v in c[:3]]
                               for c in params["colors"]]
        self._update_config("lighting", light)

    def _apply_polling(self, hz):
        if self._current_config is None or self._loading_profile:
            return
        self._update_config("polling_hz", int(hz))

    def _apply_pointer(self, pointer):
        if self._current_config is None or self._loading_profile:
            return
        self._update_config("pointer", dict(pointer))

    def _apply_key_response(self, ms):
        """Store the official Performance page's 1-100 ms key-response value."""
        if self._current_config is None or self._loading_profile:
            return
        self._update_config("key_response", max(1, min(100, int(ms))))

    def _confirm_reset(self):
        pid = self._applied_id or self.profiles.active_id
        if pid is None:
            return
        box = QMessageBox(self)
        box.setWindowTitle("Reset to Factory")
        box.setText("Reset this profile to factory defaults?")
        box.setInformativeText("This restores the button layout, DPI stages, colors, "
                               "polling rate, lighting, and pointer settings for the "
                               "active profile — like the official Restore. Your saved "
                               "macros are kept.")
        box.setIcon(QMessageBox.Warning)
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.Cancel)
        if box.exec() == QMessageBox.Yes:
            restored = self.profiles.reset_config(pid)
            if restored is None:
                return
            self._adopt_device_macros()
            self._adopt_device_guns()
            cfg = copy.deepcopy(restored["config"])
            self._current_config = cfg
            self._seed_panels(cfg)
            self.apply_profile(cfg, force=True, pid=pid)

    # -- auto-switch + tray ---------------------------------------------------
    def _tray_icon(self):
        """The app icon for the tray; falls back to a painted accent dot if the
        icon file can't be loaded."""
        ic = app_icon()
        if not ic.isNull():
            return ic
        pm = QPixmap(32, 32)
        pm.fill(QColor(theme.BG))
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QColor(theme.ACCENT))
        p.setPen(QColor(theme.ACCENT))
        p.drawEllipse(8, 8, 16, 16)
        p.end()
        return QIcon(pm)

    def _setup_tray(self):
        self.tray = None
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        self._force_quit = False
        from PySide6.QtWidgets import QApplication
        QApplication.setQuitOnLastWindowClosed(False)
        self.tray = QSystemTrayIcon(self._tray_icon(), self)
        self.tray.setToolTip("SM809 Wired Studio")
        menu = QMenu()
        menu.addAction("Show window", self._show_from_tray)

        # Profiles submenu -- rebuilt each time it opens so it tracks renames/adds
        self.tray_profiles_menu = QMenu("Profiles", menu)
        self.tray_profiles_menu.aboutToShow.connect(self._rebuild_tray_profiles)
        menu.addMenu(self.tray_profiles_menu)

        self.tray_autoswitch = QAction("Enable auto-switch", self, checkable=True)
        self.tray_autoswitch.toggled.connect(self._toggle_autoswitch)
        menu.addAction(self.tray_autoswitch)
        self.tray_overlay = QAction("Show on-screen overlay", self, checkable=True)
        self.tray_overlay.toggled.connect(self._toggle_overlay)
        menu.addAction(self.tray_overlay)
        self.tray_dpi_osd = QAction("DPI on-screen display", self, checkable=True)
        self.tray_dpi_osd.setChecked(self._dpi_osd)
        self.tray_dpi_osd.toggled.connect(self._toggle_dpi_osd)
        menu.addAction(self.tray_dpi_osd)
        menu.addAction("Settings…", self._settings)
        menu.addSeparator()
        from . import autostart
        if autostart.supported():
            self.tray_autostart = QAction("Start with Windows", self, checkable=True)
            self.tray_autostart.setChecked(autostart.is_enabled())
            self.tray_autostart.toggled.connect(self._toggle_autostart)
            menu.addAction(self.tray_autostart)
            menu.addSeparator()
        menu.addAction("Quit", self._quit_from_tray)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(
            lambda r: self._show_from_tray()
            if r == QSystemTrayIcon.Trigger else None)
        self.tray.show()

    def _show_from_tray(self):
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _rebuild_tray_profiles(self):
        """Populate the tray Profiles submenu; the manual base is checkmarked."""
        m = self.tray_profiles_menu
        m.clear()
        for p in self.profiles.summaries():
            act = QAction(p["name"], m, checkable=True)
            act.setChecked(p["id"] == self.profiles.active_id)
            act.triggered.connect(lambda _=False, pid=p["id"]: self._select_profile(pid))
            m.addAction(act)

    def _quit_from_tray(self):
        self._force_quit = True
        self.close()

    def _toggle_autoswitch(self, on):
        if self._auto.is_enabled() == bool(on):
            self._sync_autoswitch_ui(on)
            return
        self._auto.set_enabled(on)
        self.profiles.set_setting("auto_switch", bool(on))
        rules = sum(len(p.get("match_rules", []))
                    for p in self.profiles.match_targets())
        # The diagnostics log is the only record after a gaming session; say
        # how many rules exist so "it never switched" is explainable.
        _log.info("auto-switch %s (%d custom-app rule(s))",
                  "enabled" if on else "disabled", rules)
        self._sync_autoswitch_ui(on)

    def _sync_autoswitch_ui(self, on):
        act = getattr(self, "tray_autoswitch", None)
        if act is not None and act.isChecked() != bool(on):
            act.blockSignals(True)
            act.setChecked(bool(on))
            act.blockSignals(False)
        if hasattr(self, "autoswitch_panel"):
            self.autoswitch_panel.set_enabled_state(on)

    def _toggle_overlay(self, on):
        self._overlay_enabled = bool(on)
        self.profiles.set_setting("overlay", self._overlay_enabled)
        self._sync_overlay_ui(on)
        if on:
            self.overlay.flash("ON", "OVERLAY")     # confirm it's visible
        else:
            self.overlay.hide()

    def _toggle_dpi_osd(self, on):
        """Show/hide the DPI card without touching the general overlay."""
        self._dpi_osd = bool(on)
        self._overlay_show["dpi"] = self._dpi_osd
        self.profiles.set_settings({"dpi_osd": self._dpi_osd,
                                    "overlay_show": self._overlay_show})
        self._sync_dpi_osd_ui(self._dpi_osd)
        if on:
            value = self._cur_dpi if self._cur_dpi is not None else "DPI"
            self.overlay.flash(f"{value}", "DPI")     # confirm it's visible

    def _sync_dpi_osd_ui(self, on):
        act = getattr(self, "tray_dpi_osd", None)
        if act is not None and act.isChecked() != bool(on):
            act.blockSignals(True)
            act.setChecked(bool(on))
            act.blockSignals(False)

    def _toggle_autostart(self, on):
        from . import autostart
        autostart.set_enabled(on)
        # reflect the real registry state (revert the check if it failed)
        actual = autostart.is_enabled()
        if hasattr(self, "tray_autostart") and self.tray_autostart.isChecked() != actual:
            self.tray_autostart.blockSignals(True)
            self.tray_autostart.setChecked(actual)
            self.tray_autostart.blockSignals(False)

    def _sync_overlay_ui(self, on):
        act = getattr(self, "tray_overlay", None)
        if act is not None and act.isChecked() != bool(on):
            act.blockSignals(True)
            act.setChecked(bool(on))
            act.blockSignals(False)

    def _set_log_visible(self, on, persist=True):
        """Show/hide the bottom log panel (enabled from Settings)."""
        on = bool(on)
        self._show_log = on
        if on:
            self.log_panel.start()
            self.log_panel.show()
            sizes = self.body_split.sizes()
            if len(sizes) != 2 or sizes[1] < 100:
                total = sum(sizes) or max(self.height() - 56, 560)
                self.body_split.setSizes([max(240, total - 190), 190])
        else:
            self.log_panel.hide()
        if persist:
            self.profiles.set_setting("show_log", on)

    def _close_log_panel(self):
        self._set_log_visible(False)

    def _settings(self):
        """All studio settings: apply mode, live log, and the overlay HUD."""
        dlg = QDialog(self)
        dlg.setWindowTitle("Settings")
        dlg.resize(500, 700)

        shell = QVBoxLayout(dlg)
        shell.setSpacing(10)

        scroll = QScrollArea()
        scroll.setObjectName("settingsScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        content = QWidget()
        lay = QVBoxLayout(content)
        lay.setContentsMargins(14, 10, 14, 10)
        lay.setSpacing(12)
        scroll.setWidget(content)
        shell.addWidget(scroll, 1)

        # -- apply mode: one choice for every page and setting --
        apply_grp = QGroupBox("Applying changes")
        al = QVBoxLayout(apply_grp)
        rb_auto = QRadioButton("Auto-apply \u2014 write every change immediately")
        rb_manual = QRadioButton("Manual apply \u2014 stage changes, then press Apply")
        (rb_manual if self.manual_apply else rb_auto).setChecked(True)
        al.addWidget(rb_auto)
        al.addWidget(rb_manual)
        apply_hint = QLabel(
            "This setting applies to every page. In manual apply the Apply "
            "button appears in the top bar; auto-apply hides it because every "
            "edit is written straight away.")
        apply_hint.setProperty("cardHint", "true")
        apply_hint.setWordWrap(True)
        al.addWidget(apply_hint)
        lay.addWidget(apply_grp)

        # -- live log panel --
        log_grp = QGroupBox("Live log")
        ll = QVBoxLayout(log_grp)
        show_log = QCheckBox("Show the live log panel")
        show_log.setChecked(self._show_log)
        ll.addWidget(show_log)
        log_hint = QLabel(
            "The panel mirrors logs/studio.log while the studio runs. Close it "
            "with ×; turn it back on here.")
        log_hint.setProperty("cardHint", "true")
        log_hint.setWordWrap(True)
        ll.addWidget(log_hint)
        open_log = QPushButton("Open log file")
        open_log.clicked.connect(self.log_panel.open_log_file)
        ll.addWidget(open_log, 0, Qt.AlignLeft)
        lay.addWidget(log_grp)

        # -- overlay --
        overlay_grp = QGroupBox("On-screen overlay")
        ol = QVBoxLayout(overlay_grp)

        enable = QCheckBox("Show on-screen overlay")
        enable.setChecked(self._overlay_enabled)
        ol.addWidget(enable)

        # The switch notice replaces the old Windows tray toast. It has its own
        # switch because it is useful even when the ambient overlay is off.
        notify = QCheckBox("Announce profile switches on the overlay")
        notify.setChecked(self._overlay_switch)
        notify.setToolTip(
            "Shows the profile that was applied over the game. This replaces "
            "the tray notification and also works when the overlay above is "
            "unchecked.")
        ol.addWidget(notify)
        notify_hint = QLabel(
            "Replaces the Windows tray notification. The card uses the "
            "position, size and duration below.")
        notify_hint.setProperty("cardHint", "true")
        notify_hint.setWordWrap(True)
        ol.addWidget(notify_hint)

        cap = QLabel("SHOW ON CHANGE")
        cap.setProperty("groupLabel", "true")
        ol.addWidget(cap)
        cb_prof = QCheckBox("Profile name")
        cb_prof.setChecked(self._overlay_show.get("profile", True))
        cb_dpi = QCheckBox("DPI (including the mouse's DPI buttons)")
        cb_dpi.setChecked(self._dpi_osd)
        cb_rate = QCheckBox("Polling rate")
        cb_rate.setChecked(self._overlay_show.get("rate", False))
        for c in (cb_prof, cb_dpi, cb_rate):
            ol.addWidget(c)

        prow = QHBoxLayout()
        prow.addWidget(QLabel("Position"))
        pos = QComboBox()
        for p in POSITIONS:
            pos.addItem(POSITION_LABELS[p], p)
        i = pos.findData(self.profiles.get_setting("overlay_pos", "bottom-center"))
        pos.setCurrentIndex(i if i >= 0 else POSITIONS.index("bottom-center"))
        prow.addWidget(pos, 1)
        ol.addLayout(prow)

        # monitor: follow the cursor's monitor, or pin to a chosen one
        follow = QCheckBox("Show on the monitor under the cursor")
        follow.setChecked(bool(self.profiles.get_setting("overlay_follow_cursor", True)))
        ol.addWidget(follow)
        mrow = QHBoxLayout()
        mrow.addWidget(QLabel("Monitor"))
        mon = QComboBox()
        for si, scr in enumerate(QGuiApplication.screens()):
            g = scr.geometry()
            tag = " (primary)" if scr is QGuiApplication.primaryScreen() else ""
            mon.addItem(f"Monitor {si + 1} — {g.width()}x{g.height()}{tag}", si)
        mon.setCurrentIndex(min(int(self.profiles.get_setting("overlay_monitor", 0)),
                                max(0, mon.count() - 1)))
        mon.setEnabled(not follow.isChecked())
        follow.toggled.connect(lambda on: mon.setEnabled(not on))
        mrow.addWidget(mon, 1)
        ol.addLayout(mrow)

        op_lbl = QLabel()
        op = QSlider(Qt.Horizontal); op.setRange(30, 100)
        op.setValue(int(self.profiles.get_setting("overlay_opacity", 92)))
        op.valueChanged.connect(lambda v: op_lbl.setText(f"Transparency (opacity): {v}%"))
        op.valueChanged.emit(op.value())
        ol.addWidget(op_lbl); ol.addWidget(op)

        sc_lbl = QLabel()
        sc = QSlider(Qt.Horizontal); sc.setRange(60, 200)
        sc.setValue(int(self.profiles.get_setting("overlay_scale", 100)))
        sc.valueChanged.connect(lambda v: sc_lbl.setText(f"Size: {v}%"))
        sc.valueChanged.emit(sc.value())
        ol.addWidget(sc_lbl); ol.addWidget(sc)

        dur_lbl = QLabel()
        dur = QSlider(Qt.Horizontal); dur.setRange(3, 50)   # 0.3s .. 5.0s (x100ms)
        dur.setValue(int(self.profiles.get_setting("overlay_hold", 1400)) // 100)
        dur.valueChanged.connect(lambda v: dur_lbl.setText(f"Duration on screen: {v / 10:.1f} s"))
        dur.valueChanged.emit(dur.value())
        ol.addWidget(dur_lbl); ol.addWidget(dur)

        def _preview():
            self.overlay.set_appearance(pos.currentData(), op.value(), sc.value(),
                                        hold_ms=dur.value() * 100,
                                        follow_cursor=follow.isChecked(),
                                        monitor_index=mon.currentData() or 0)
            lines = []
            if cb_prof.isChecked():
                lines.append(("Profile", self._cur_profile
                              or (self.profiles.active() or {}).get("name", "Default")))
            if cb_dpi.isChecked():
                lines.append(("DPI", self._cur_dpi if self._cur_dpi is not None else 1600))
            if cb_rate.isChecked():
                lines.append(("Polling Rate", f"{self._cur_rate or 1000} Hz"))
            self.overlay.flash_lines(lines or [("Overlay", "nothing selected")])

        prev = QPushButton("Preview")
        prev.clicked.connect(_preview)
        ol.addWidget(prev)
        lay.addWidget(overlay_grp)

        # -- developer previews --
        dev_grp = QGroupBox("Developer")
        dl = QVBoxLayout(dev_grp)
        dev_cb = QCheckBox("Enable developer features (work in progress)")
        dev_cb.setChecked(self.developer)
        dl.addWidget(dev_cb)
        dev_hint = QLabel(
            "Recoil Control is still being developed and is hidden by default. "
            "Turn this on to show its tab and offer recoil patterns when "
            "assigning a mouse button. Host playback in that tab is a preview: "
            "the wired mouse itself never runs recoil tables.")
        dev_hint.setProperty("cardHint", "true")
        dev_hint.setWordWrap(True)
        dl.addWidget(dev_hint)
        lay.addWidget(dev_grp)
        lay.addStretch(1)

        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(dlg.accept); bb.rejected.connect(dlg.reject)
        shell.addWidget(bb)

        if dlg.exec() == QDialog.Accepted:
            manual = rb_manual.isChecked()
            show_live_log = show_log.isChecked()
            self._overlay_show = {"profile": cb_prof.isChecked(),
                                  "dpi": cb_dpi.isChecked(), "rate": cb_rate.isChecked()}
            self._dpi_osd = cb_dpi.isChecked()
            self._sync_dpi_osd_ui(self._dpi_osd)
            self._overlay_switch = notify.isChecked()
            # one sidecar write for the whole dialog, not one per control
            self.profiles.set_settings({
                "manual_apply": manual,
                "show_log": show_live_log,
                "dpi_osd": self._dpi_osd,
                "overlay_switch": notify.isChecked(),
                "overlay_show": self._overlay_show,
                "overlay_pos": pos.currentData(),
                "overlay_opacity": op.value(),
                "overlay_scale": sc.value(),
                "overlay_hold": dur.value() * 100,
                "overlay_follow_cursor": follow.isChecked(),
                "overlay_monitor": mon.currentData() or 0,
                "developer_features": dev_cb.isChecked(),
            })
            self.set_manual_apply(manual, persist=False)
            self._set_log_visible(show_live_log, persist=False)
            self._set_developer(dev_cb.isChecked(), persist=False)
            self._apply_overlay_appearance()      # applies to overlay + alert overlay
            if enable.isChecked() != self._overlay_enabled:
                self._toggle_overlay(enable.isChecked())
        else:
            self._apply_overlay_appearance()      # revert preview tweaks to saved

    # -- window geometry ------------------------------------------------------
    def _restore_window_geometry(self):
        """Reopen at the last size/position (Qt keeps it on-screen)."""
        saved = self.profiles.get_setting("window_geometry")
        if not saved:
            return
        try:
            self.restoreGeometry(QByteArray.fromBase64(str(saved).encode("ascii")))
        except Exception:
            pass

    def _save_window_geometry(self):
        try:
            self.profiles.set_setting(
                "window_geometry",
                bytes(self.saveGeometry().toBase64()).decode("ascii"))
        except Exception:
            pass

    def closeEvent(self, e):
        # with a tray icon, closing hides to tray (keeps auto-switch running)
        if self.tray is not None and not getattr(self, "_force_quit", False):
            # never lose a pending debounced edit, even when closing to the tray
            self._flush_profile_save()
            self._save_window_geometry()
            # The Manage Apps popup belongs to the studio window; do not leave
            # it floating on the desktop while the studio sits in the tray.
            if getattr(self, "manage_apps_dialog", None) is not None:
                self.manage_apps_dialog.hide()
            e.ignore()
            self.hide()
            self.tray.showMessage(
                "Still running", "Auto-switch stays active. Quit from the tray icon.",
                QSystemTrayIcon.Information, 2000)
            return
        # Real quit: stop auto-switch and the device worker before flushing.
        # A queued apply rewrites the same profile buffers this flush
        # serialises, so letting the two threads overlap can persist a
        # half-applied record.
        if self._auto is not None:
            # stop() (not set_enabled(False)): quitting must leave the profile
            # currently on the mouse in place instead of restoring the manual
            # one as the device worker shuts down.
            self._auto.stop()
        self.ctrl.shutdown()
        self._flush_profile_save()
        self._save_window_geometry()
        if self.tray is not None:
            self.tray.hide()
        if getattr(self, "overlay", None) is not None:
            self.overlay.hide()
        if getattr(self, "alert_overlay", None) is not None:
            self.alert_overlay.hide()
        super().closeEvent(e)
        if getattr(self, "_force_quit", False):
            from PySide6.QtWidgets import QApplication
            QApplication.quit()
