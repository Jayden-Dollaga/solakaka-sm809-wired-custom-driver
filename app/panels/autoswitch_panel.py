"""
app.panels.autoswitch_panel -- the Auto-Switch settings tab.

Master-detail rule editor: the left list shows every profile; clicking one
shows the apps assigned to it on the right. A rule matches the focused app by
exe name, by a full-path substring (to tell apart same-named exes like UE/Unity
Client-Win64-Shipping.exe), and/or a window-title substring. All filled fields
must match. First matching profile in list order wins; when nothing matches the
manually-chosen base profile is restored (see app/autoswitch.py).

"Add app…" opens a picker of running windows (like the NVIDIA Control Panel
program list) and assigns the chosen app immediately. "Detect app" does the
same for the current foreground window, for fullscreen games. A live foreground
readout at the bottom confirms what Windows reports and which profile (if any)
it currently matches.

Signals:
  enable_toggled(bool)        -- the Enable auto-switch checkbox changed
  rules_changed(str, object)  -- (profile_id, [rules]) edited for a profile
  app_detected(str, str)      -- (exe, title) captured by "Detect app"
"""

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QListWidget,
    QListWidgetItem, QPushButton, QScrollArea, QFrame,
)

from ..widgets.controls import Card
from ..autoswitch import ForegroundWatcher, match_profile
from ..elevation import is_admin
from .. import theme


class AutoSwitchPanel(QWidget):
    enable_toggled = Signal(bool)
    rules_changed = Signal(str, object)
    app_detected = Signal(str, str)        # (exe, title) captured by "Detect app"

    def __init__(self):
        super().__init__()
        self._profiles = []          # list of profile dicts (id, name, match_rules)
        self._rules_by_pid = {}      # pid -> list[rule]
        self._watcher = ForegroundWatcher()
        self._loading = False
        self._detect_pid = None      # profile targeted when Detect app was clicked

        lay = QVBoxLayout(self)
        lay.setContentsMargins(28, 24, 28, 24)
        lay.setSpacing(14)

        title = QLabel("Auto-Switch")
        title.setProperty("panelTitle", "true")
        lay.addWidget(title)
        sub = QLabel("Automatically switch profiles based on the focused application "
                     "— a feature the official software doesn't have.")
        sub.setProperty("panelSubtitle", "true")
        sub.setWordWrap(True)
        lay.addWidget(sub)

        # enable card
        enable_card = Card("Enable")
        self.enable_check = QCheckBox("Enable auto-switch")
        self.enable_check.toggled.connect(self._on_enable)
        enable_card.add(self.enable_check)
        hint = QLabel("When on, the active profile follows the foreground app. With "
                      "no rule match it reverts to the profile you picked manually "
                      "(the base). Keep the app running (it lives in the tray).")
        hint.setProperty("cardHint", "true")
        hint.setWordWrap(True)
        enable_card.add(hint)

        # The official driver runs with administrator rights. A non-elevated
        # studio cannot inspect some elevated games (anti-cheat launchers), so
        # say so where the feature is configured instead of failing silently.
        self.admin_hint = QLabel(
            "Not running as administrator — games that run elevated (some "
            "anti-cheat titles) may not be detected. Restart the studio as "
            "administrator to match the official driver.")
        self.admin_hint.setProperty("cardHint", "true")
        self.admin_hint.setStyleSheet(f"color: {theme.WARN};")
        self.admin_hint.setWordWrap(True)
        self.admin_hint.setVisible(not is_admin())
        enable_card.add(self.admin_hint)

        # custom-apps card: profile list on the left, that profile's apps on the right
        rules_card = Card("Custom apps", "Click a profile to see the apps assigned "
                          "to it. Add the game or program while it is running; "
                          "the first matching profile in list order wins.")

        body = QHBoxLayout()
        body.setSpacing(16)

        left = QVBoxLayout()
        left.setSpacing(6)
        cap = QLabel("PROFILES")
        cap.setProperty("unit", "true")
        left.addWidget(cap)
        self.profile_list = QListWidget()
        self.profile_list.setObjectName("autoswitchProfiles")
        self.profile_list.setMinimumWidth(150)
        self.profile_list.setMaximumWidth(240)
        self.profile_list.setMinimumHeight(200)
        self.profile_list.currentItemChanged.connect(self._load_rules)
        left.addWidget(self.profile_list, 1)
        body.addLayout(left)

        right = QVBoxLayout()
        right.setSpacing(8)
        self.profile_label = QLabel("Select a profile")
        self.profile_label.setStyleSheet("font-weight: 600; font-size: 13px;")
        right.addWidget(self.profile_label)

        self.rules_list = QListWidget()
        self.rules_list.setMinimumHeight(90)
        self.rules_list.setMaximumHeight(150)
        right.addWidget(self.rules_list)
        self.rules_empty = QLabel("")
        self.rules_empty.setProperty("cardHint", "true")
        self.rules_empty.setWordWrap(True)
        right.addWidget(self.rules_empty)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton("Add app…")
        self.add_btn.setToolTip(
            "Pick from the applications and games that are currently running")
        self.add_btn.clicked.connect(self._open_picker)
        self.detect_btn = QPushButton("Detect app (3s)…")
        self.detect_btn.clicked.connect(self._detect)
        self.detect_btn.setToolTip(
            "Switch to the game/app within 3 seconds; it is detected and "
            "assigned to the selected profile right away")
        self.rm_btn = QPushButton("Remove")
        self.rm_btn.setToolTip("Remove the selected app from this profile")
        self.rm_btn.clicked.connect(self._remove)
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.detect_btn)
        btn_row.addWidget(self.rm_btn)
        btn_row.addStretch(1)
        right.addLayout(btn_row)

        self.status = QLabel("")
        self.status.setProperty("cardHint", "true")
        self.status.setWordWrap(True)
        right.addWidget(self.status)

        self.foreground = QLabel("Foreground: —")
        self.foreground.setProperty("cardHint", "true")
        self.foreground.setWordWrap(True)
        right.addWidget(self.foreground)

        right.addStretch(1)
        body.addLayout(right, 1)
        rules_card.add(body)

        # The two cards need more height than the window's minimum, so the
        # page scrolls instead of cutting the rule fields off.
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        holder = QWidget()
        col = QVBoxLayout(holder)
        col.setContentsMargins(0, 0, 0, 0)
        col.setSpacing(14)
        col.addWidget(enable_card)
        col.addWidget(rules_card)
        col.addStretch(1)
        scroll.setWidget(holder)
        lay.addWidget(scroll, 1)

        # Live readout while this tab is visible: what Windows reports as the
        # foreground app and whether it currently matches a profile.
        self._fg_timer = QTimer(self)
        self._fg_timer.setInterval(1000)
        self._fg_timer.timeout.connect(self._tick_foreground)

        self._set_controls_enabled(False)
        self._load_rules()

    # -- external API ---------------------------------------------------------
    def set_profiles(self, profiles, select_id=None):
        """Populate from the store's profile list (each: id, name, match_rules)."""
        self._profiles = list(profiles)
        self._rules_by_pid = {p["id"]: [dict(r) for r in p.get("match_rules", [])]
                              for p in self._profiles}
        keep = select_id or self.current_pid()
        idx = 0
        self._loading = True
        self.profile_list.clear()
        for i, p in enumerate(self._profiles):
            it = QListWidgetItem(p["name"])
            it.setData(Qt.UserRole, p["id"])
            count = len(self._rules_by_pid.get(p["id"], []))
            it.setToolTip(f"{count} custom app{'s' if count != 1 else ''}")
            self.profile_list.addItem(it)
            if p["id"] == keep:
                idx = i
        if self._profiles:
            self.profile_list.setCurrentRow(idx)
        self._loading = False
        self._load_rules()

    def set_enabled_state(self, on):
        self.enable_check.blockSignals(True)
        self.enable_check.setChecked(bool(on))
        self.enable_check.blockSignals(False)

    def current_pid(self):
        it = self.profile_list.currentItem()
        return it.data(Qt.UserRole) if it is not None else None

    def select_profile(self, pid):
        """Show the apps of `pid` (used when the rail/Profiles list selects it)."""
        for i in range(self.profile_list.count()):
            if self.profile_list.item(i).data(Qt.UserRole) == pid:
                if self.profile_list.currentRow() != i:
                    self.profile_list.setCurrentRow(i)
                    self.profile_list.scrollToItem(self.profile_list.item(i))
                self._load_rules()
                return

    # -- internals ------------------------------------------------------------
    def _on_enable(self, on):
        self.enable_toggled.emit(bool(on))

    def _name_of(self, pid):
        return next((p["name"] for p in self._profiles if p["id"] == pid), "profile")

    def _rule_label(self, r):
        parts = []
        parts.append(r.get("exe") or "(any exe)")
        if r.get("path"):
            parts.append(f"path~“{r['path']}”")
        if r.get("title"):
            parts.append(f"title~“{r['title']}”")
        return "   ·   ".join(parts)

    def _load_rules(self, *_):
        if self._loading:
            return
        pid = self.current_pid()
        name = self._name_of(pid) if pid else None
        self.profile_label.setText(f"Apps for {name}" if name else "Select a profile")
        self.rules_list.clear()
        rules = self._rules_by_pid.get(pid, []) if pid else []
        for r in rules:
            self.rules_list.addItem(self._rule_label(r))
        self.rules_empty.setText(
            f"No custom apps for {name} yet. Start the game or app, then press "
            f"Add app… — or use Detect app (3s) while it is in front."
            if name else "Select a profile to manage its custom apps.")
        self.rules_empty.setVisible(not rules)
        # An empty list is just a large blank box; hide it until there is a rule.
        self.rules_list.setVisible(bool(rules))
        self._set_controls_enabled(pid is not None)

    def _set_controls_enabled(self, on):
        for w in (self.add_btn, self.detect_btn, self.rm_btn):
            w.setEnabled(bool(on))

    def _emit_rules(self, pid=None):
        pid = pid or self.current_pid()
        if pid is not None:
            self.rules_changed.emit(pid, list(self._rules_by_pid.get(pid, [])))

    @staticmethod
    def _normalise(rule):
        return {k: ((rule.get(k) or "").strip().lower() or None)
                for k in ("exe", "path", "title")}

    def _duplicate(self, pid, rule):
        for r in self._rules_by_pid.get(pid, []):
            if self._normalise(r) == rule:
                return True
        return False

    def _open_picker(self):
        """Pick a running window and assign it to the selected profile."""
        pid = self.current_pid()
        if pid is None:
            self.status.setText("Select a profile first.")
            return
        from .app_picker import AppPicker
        dlg = AppPicker(self)
        if not dlg.exec():
            return
        rule = dlg.selected_rule()
        if rule:
            self._add_rule(pid, rule)

    def _add_rule(self, pid, raw_rule):
        """Append a rule (from the picker or Detect app) to `pid`."""
        pid = pid or self.current_pid()
        if pid is None:
            self.status.setText("Select a profile first.")
            return False
        rule = self._normalise(raw_rule)
        if not any(rule.values()):
            self.status.setText("That app has no usable exe or window title.")
            return False
        if self._duplicate(pid, rule):
            self.status.setText(
                f"That app is already assigned to {self._name_of(pid)}.")
            return False
        self._rules_by_pid.setdefault(pid, []).append(rule)
        self.status.setText(
            f"Added {rule['exe'] or rule['path'] or rule['title']} to "
            f"{self._name_of(pid)}.")
        self._load_rules()
        self._emit_rules(pid)
        return True

    def _remove(self):
        pid = self.current_pid()
        i = self.rules_list.currentRow()
        rules = self._rules_by_pid.get(pid, []) if pid else []
        if 0 <= i < len(rules):
            del rules[i]
            self.status.setText(f"Removed an app from {self._name_of(pid)}.")
            self._load_rules()
            self._emit_rules(pid)
        else:
            self.status.setText("Select an app in the list first.")

    def _detect(self):
        pid = self.current_pid()
        if pid is None:
            self.status.setText("Select a profile first.")
            return
        self._detect_pid = pid
        self.status.setText("Switch to the target app now… capturing in 3 seconds.")
        QTimer.singleShot(3000, self._capture)

    def _capture(self):
        pid = self._detect_pid or self.current_pid()
        self._detect_pid = None
        exe, title, path = self._watcher.current()
        if not exe:
            self.status.setText("Couldn't detect the foreground app.")
            return
        if pid is not None and pid != self.current_pid():
            self.select_profile(pid)
        # confirm on the on-screen overlay too (games are fullscreen, so the
        # dialog isn't visible) -- MainWindow flashes the configured overlay
        self.app_detected.emit(exe, title or "")
        added = self._add_rule(pid, {"exe": exe, "path": path, "title": None})
        if added:
            self.status.setText(
                f"Detected {exe} and assigned it to {self._name_of(pid)}.")

    # -- live foreground readout ---------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
        self._tick_foreground()
        self._fg_timer.start()

    def hideEvent(self, event):
        self._fg_timer.stop()
        super().hideEvent(event)

    def _tick_foreground(self):
        exe, title, path = self._watcher.current()
        if not exe:
            self.foreground.setText("Foreground: unavailable")
            return
        targets = [{"id": p["id"], "match_rules": self._rules_by_pid.get(p["id"], [])}
                   for p in self._profiles]
        pid = match_profile(targets, exe, title, path)
        if pid:
            self.foreground.setText(
                f"Foreground: {exe} — matches {self._name_of(pid)}")
        else:
            self.foreground.setText(f"Foreground: {exe} — no profile match")
