"""
app.panels.autoswitch_panel -- the Auto-Switch settings tab (Milestone 3 step 3).

Replaces the old pop-up rule dialog: enable/disable auto-switch and edit each
profile's match rules inline. A rule matches the focused app by exe name, by a
full-path substring (to tell apart same-named exes like UE/Unity
Client-Win64-Shipping.exe), and/or a window-title substring. First matching
profile in list order wins; when nothing matches, the manually-chosen base
profile is restored (see app/autoswitch.py).

Signals:
  enable_toggled(bool)        -- the Enable auto-switch checkbox changed
  rules_changed(str, object)  -- (profile_id, [rules]) edited for a profile
"""

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QComboBox,
    QListWidget, QLineEdit, QPushButton, QScrollArea, QFrame,
)

from ..widgets.controls import Card
from ..autoswitch import ForegroundWatcher


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

        # rules card
        rules_card = Card("Rules", "First matching profile in the list wins. "
                          "Leave a field blank to ignore it.")
        sel_row = QHBoxLayout()
        sel_row.addWidget(QLabel("Rules for profile:"))
        self.profile_combo = QComboBox()
        self.profile_combo.currentIndexChanged.connect(self._load_rules)
        sel_row.addWidget(self.profile_combo, 1)
        rules_card.add(sel_row)

        self.rules_list = QListWidget()
        self.rules_list.setMinimumHeight(110)
        self.rules_list.setMaximumHeight(190)
        rules_card.add(self.rules_list)
        self.rules_empty = QLabel(
            "No rules for this profile yet. Add the target application's exe "
            "name below (or use Detect app) and it will match whenever that "
            "window is in front.")
        self.rules_empty.setProperty("cardHint", "true")
        self.rules_empty.setWordWrap(True)
        rules_card.add(self.rules_empty)

        fields_cap = QLabel("MATCH FIELDS — BLANK FIELDS ARE IGNORED")
        fields_cap.setProperty("groupLabel", "true")
        rules_card.add(fields_cap)

        in_row = QHBoxLayout()
        self.exe_edit = QLineEdit()
        self.exe_edit.setPlaceholderText("exe name, e.g. game.exe")
        self.exe_edit.setToolTip("Executable name; matched case-insensitively")
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("path contains (optional)")
        self.path_edit.setToolTip(
            "Part of the full path — use it to tell apart same-named exes")
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("title contains (optional)")
        self.title_edit.setToolTip("Part of the window title")
        in_row.addWidget(self.exe_edit, 2)
        in_row.addWidget(self.path_edit, 3)
        in_row.addWidget(self.title_edit, 2)
        rules_card.add(in_row)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("Add rule")
        add_btn.clicked.connect(self._add)
        detect_btn = QPushButton("Detect app (3s)…")
        detect_btn.clicked.connect(self._detect)
        detect_btn.setToolTip(
            "Switch to the game/app within 3 seconds; its details are filled in")
        rm_btn = QPushButton("Remove selected")
        rm_btn.clicked.connect(self._remove)
        btn_row.addWidget(add_btn)
        btn_row.addWidget(detect_btn)
        btn_row.addWidget(rm_btn)
        btn_row.addStretch(1)
        rules_card.add(btn_row)

        self.status = QLabel("")
        self.status.setProperty("cardHint", "true")
        self.status.setWordWrap(True)
        rules_card.add(self.status)

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
        self._load_rules()

    # -- external API ---------------------------------------------------------
    def set_profiles(self, profiles, select_id=None):
        """Populate from the store's profile list (each: id, name, match_rules)."""
        self._profiles = list(profiles)
        self._rules_by_pid = {p["id"]: [dict(r) for r in p.get("match_rules", [])]
                              for p in self._profiles}
        keep = select_id or (self.current_pid())
        self._loading = True
        self.profile_combo.clear()
        idx = 0
        for i, p in enumerate(self._profiles):
            self.profile_combo.addItem(p["name"], p["id"])
            if p["id"] == keep:
                idx = i
        self.profile_combo.setCurrentIndex(idx)
        self._loading = False
        self._load_rules()

    def set_enabled_state(self, on):
        self.enable_check.blockSignals(True)
        self.enable_check.setChecked(bool(on))
        self.enable_check.blockSignals(False)

    def current_pid(self):
        return self.profile_combo.currentData()

    # -- internals ------------------------------------------------------------
    def _on_enable(self, on):
        self.enable_toggled.emit(bool(on))

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
        self.rules_list.clear()
        rules = self._rules_by_pid.get(self.current_pid(), [])
        for r in rules:
            self.rules_list.addItem(self._rule_label(r))
        self.rules_empty.setVisible(not rules)
        # An empty list is just a large blank box; hide it so the match
        # fields and Add rule button stay in view until there is a rule.
        self.rules_list.setVisible(bool(rules))

    def _emit_rules(self):
        pid = self.current_pid()
        if pid is not None:
            self.rules_changed.emit(pid, list(self._rules_by_pid.get(pid, [])))

    def _add(self):
        pid = self.current_pid()
        if pid is None:
            return
        exe = self.exe_edit.text().strip().lower()
        path = self.path_edit.text().strip()
        title = self.title_edit.text().strip()
        if not (exe or path or title):
            self.status.setText(
                "Type an exe name, a path fragment or a window title first.")
            return
        self._rules_by_pid.setdefault(pid, []).append(
            {"exe": exe or None, "path": path or None, "title": title or None})
        self.exe_edit.clear()
        self.path_edit.clear()
        self.title_edit.clear()
        self.status.setText("")
        self._load_rules()
        self._emit_rules()

    def _remove(self):
        pid = self.current_pid()
        i = self.rules_list.currentRow()
        rules = self._rules_by_pid.get(pid, [])
        if 0 <= i < len(rules):
            del rules[i]
            self._load_rules()
            self._emit_rules()

    def _detect(self):
        self.status.setText("Switch to the target app now… capturing in 3 seconds.")
        QTimer.singleShot(3000, self._capture)

    def _capture(self):
        exe, title, path = self._watcher.current()
        if exe:
            self.exe_edit.setText(exe)
            self.path_edit.setText(path or "")
            self.status.setText(f"Detected: {exe}  —  {path or '(no path)'}")
            # confirm on the on-screen overlay too (games are fullscreen, so the
            # dialog isn't visible) -- MainWindow flashes the configured overlay
            self.app_detected.emit(exe, title or "")
        else:
            self.status.setText("Couldn't detect the foreground app.")
