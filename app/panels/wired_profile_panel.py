"""Load, preview, and explicitly apply profiles to the wired-only SM809."""

import configparser
from dataclasses import replace
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QComboBox, QFormLayout, QFileDialog, QHBoxLayout, QLabel, QMessageBox,
    QPushButton, QSpinBox, QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget,
)

from sm809wired import protocol as W
from sm809wired.actions import ACTIONS, MACRO_ACTIONS
from sm809wired.apply import build_apply, to_wire
from sm809wired.profile import N_SLOTS, Profile, parse_button_ini, read_profiles


BASELINE_REPLY = bytes.fromhex("83020ff240000000")
POLLING_RATES = (125, 250, 500, 1000)
LIGHTING_NAMES = (
    "Off", "Stars Twinkle", "Colorful Streaming", "Seven-color Stretch",
    "Seven-color Flash", "Colorful Breath", "Seven-color Explosion",
    "Colorful Coverage", "Red", "Green", "Blue", "Mode 11",
)
BUTTON_ACTION_NAMES = {
    0x00: "Disabled", 0x01: "Click", 0x02: "Menu", 0x03: "Scroll",
    0x04: "Forward", 0x05: "Backward", 0x06: "DPI cycle", 0x07: "DPI up",
    0x08: "DPI down", 0x09: "Double click", 0x0A: "Fire click",
    0x0B: "Scroll up", 0x0C: "Scroll down", 0x12: "Three click",
    0x15: "Shortcut", 0x16: "Macro (unsupported)", 0x19: "Gun (unsupported)",
    0x1A: "Mode switch", 0x20: "Cut", 0x21: "Copy", 0x22: "Paste",
    0x23: "Open", 0x24: "Save", 0x25: "Find", 0x26: "Redo",
    0x27: "New", 0x28: "Select all", 0x29: "Print", 0x2A: "Close window",
    0x2B: "Swap windows", 0x2C: "Show desktop", 0x2D: "Run command",
    0x2E: "Lock PC", 0x2F: "New document", 0x32: "Switch lighting",
    0x39: "Macro (unsupported)", 0x40: "Media player", 0x41: "Play/pause",
    0x42: "Stop", 0x43: "Previous track", 0x44: "Next track",
    0x45: "Volume up", 0x46: "Volume down", 0x47: "Mute",
    0x4F: "Email", 0x50: "Calculator", 0x51: "My computer",
    0x68: "Report rate up", 0x69: "Report rate down", 0x70: "Report rate cycle",
    0x71: "Juji", 0x79: "Gun (unsupported)",
}


def _read_key(data_ini_path: str) -> bytes:
    parser = configparser.ConfigParser(interpolation=None)
    parser.read_string(Path(data_ini_path).read_text(encoding="utf-8-sig", errors="replace"))
    try:
        vid = int(parser.get("Default", "VID"), 16)
        pid = int(parser.get("Default", "PID"), 16)
    except (configparser.Error, ValueError) as exc:
        raise ValueError("Data.ini must identify the wired SM809 as VID 04D9, PID A09F") from exc
    if (vid, pid) != (W.VID, W.PID):
        raise ValueError(f"Data.ini targets {vid:04X}:{pid:04X}, expected 04D9:A09F")
    password = parser.get("Default", "Password", fallback="")
    key = W.key_from_password(password)
    if key is None:
        raise ValueError("Data.ini must contain a six-character Default/Password value")
    return key


class _ApplyWorker(QObject):
    succeeded = Signal(str)
    failed = Signal(str)
    finished = Signal()

    def __init__(self, profile: Profile, button_ini: Any, key: bytes) -> None:
        super().__init__()
        self._profile = profile
        self._button_ini = button_ini
        self._key = key

    @Slot()
    def run(self) -> None:
        handle = None
        messages = []
        try:
            from sm809wired.device import open_interface, push_profile

            handle = open_interface()
            push_profile(handle, self._profile, self._button_ini, self._key,
                         log=messages.append)
            self.succeeded.emit("\n".join(messages) or "Profile applied.")
        except Exception as exc:
            self.failed.emit(str(exc))
        finally:
            if handle is not None:
                try:
                    handle.close()
                except Exception:
                    pass
            self.finished.emit()


class WiredProfilePanel(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._profiles: list[Profile] = []
        self._button_ini = None
        self._key = None
        self._preview_valid = False
        self._apply_thread = None
        self._worker = None
        self._button_combos: list[QComboBox] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(12)

        title = QLabel("Wired-only profile")
        title.setProperty("panelTitle", "true")
        layout.addWidget(title)

        subtitle = QLabel(
            "Holtek 04D9:A09F profiles use a separate protocol and overwrite the full mouse configuration."
        )
        subtitle.setProperty("panelSubtitle", "true")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        file_row = QHBoxLayout()
        self.profile_file_button = QPushButton("Load profile file…")
        self.profile_file_button.clicked.connect(self._choose_profile_file)
        file_row.addWidget(self.profile_file_button)
        self.profile_file_label = QLabel("No profile file loaded")
        self.profile_file_label.setToolTip("")
        file_row.addWidget(self.profile_file_label, 1)
        layout.addLayout(file_row)

        data_row = QHBoxLayout()
        self.data_ini_button = QPushButton("Load Data.ini…")
        self.data_ini_button.clicked.connect(self._choose_data_ini)
        data_row.addWidget(self.data_ini_button)
        self.data_ini_label = QLabel("Data.ini not loaded")
        self.data_ini_label.setToolTip("")
        data_row.addWidget(self.data_ini_label, 1)
        layout.addLayout(data_row)

        self.profile_combo = QComboBox()
        self.profile_combo.currentIndexChanged.connect(self._on_profile_selected)
        layout.addWidget(self.profile_combo)

        self.editor_tabs = QTabWidget()
        settings_page = QWidget()
        settings_form = QFormLayout(settings_page)

        self.mode_combo = QComboBox()
        self.mode_combo.addItem("Office", False)
        self.mode_combo.addItem("Game", True)
        settings_form.addRow("Mode", self.mode_combo)

        self.polling_combo = QComboBox()
        for index, rate in enumerate(POLLING_RATES):
            self.polling_combo.addItem(f"{rate} Hz", index)
        settings_form.addRow("Polling rate", self.polling_combo)

        self.active_stage_combo = QComboBox()
        settings_form.addRow("Active DPI stage", self.active_stage_combo)

        self.dpi_spins: list[QSpinBox] = []
        for stage in range(8):
            spin = QSpinBox()
            spin.setRange(100, 12000)
            spin.setSingleStep(50)
            spin.setSuffix(" DPI")
            self.dpi_spins.append(spin)
            settings_form.addRow(f"Stage {stage + 1}", spin)

        self.light_mode_combo = QComboBox()
        for mode, name in enumerate(LIGHTING_NAMES):
            self.light_mode_combo.addItem(name, mode)
        settings_form.addRow("Lighting", self.light_mode_combo)

        self.brightness_spin = self._byte_spin()
        self.length_spin = QSpinBox()
        self.length_spin.setRange(0, 4)
        self.frequency_spin = self._byte_spin()
        self.direction_spin = self._byte_spin()
        self.fixed_rgb_spins = [self._byte_spin() for _ in range(3)]
        settings_form.addRow("Brightness", self.brightness_spin)
        settings_form.addRow("Effect length", self.length_spin)
        settings_form.addRow("Effect frequency", self.frequency_spin)
        settings_form.addRow("Effect direction", self.direction_spin)
        color_row = QWidget()
        color_layout = QHBoxLayout(color_row)
        color_layout.setContentsMargins(0, 0, 0, 0)
        for label, spin in zip(("R", "G", "B"), self.fixed_rgb_spins):
            color_layout.addWidget(QLabel(label))
            color_layout.addWidget(spin)
        settings_form.addRow("Fixed color", color_row)
        self.editor_tabs.addTab(settings_page, "Settings")

        buttons_page = QWidget()
        buttons_layout = QVBoxLayout(buttons_page)
        self.buttons_table = QTableWidget(N_SLOTS, 2)
        self.buttons_table.setHorizontalHeaderLabels(("Slot", "Action"))
        self.buttons_table.verticalHeader().setVisible(False)
        self.buttons_table.setColumnWidth(0, 160)
        self.buttons_table.horizontalHeader().setStretchLastSection(True)
        buttons_layout.addWidget(self.buttons_table)
        self.editor_tabs.addTab(buttons_page, "Buttons")
        layout.addWidget(self.editor_tabs, 2)

        for control in (
            self.mode_combo, self.polling_combo, self.active_stage_combo,
            *self.dpi_spins, self.light_mode_combo, self.brightness_spin,
            self.length_spin, self.frequency_spin, self.direction_spin,
            *self.fixed_rgb_spins,
        ):
            if isinstance(control, QComboBox):
                control.currentIndexChanged.connect(self._on_settings_changed)
            else:
                control.valueChanged.connect(self._on_settings_changed)

        self.status = QLabel("Load a .pbin or profile.bin and its matching Data.ini.")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setLineWrapMode(QTextEdit.NoWrap)
        self.preview.setPlaceholderText("The dry-run packet sequence will appear here.")
        layout.addWidget(self.preview, 1)

        action_row = QHBoxLayout()
        action_row.addStretch(1)
        self.apply_btn = QPushButton("Apply full profile to wired mouse…")
        self.apply_btn.setEnabled(False)
        self.apply_btn.clicked.connect(self._confirm_apply)
        action_row.addWidget(self.apply_btn)
        layout.addLayout(action_row)

    @staticmethod
    def _byte_spin() -> QSpinBox:
        spin = QSpinBox()
        spin.setRange(0, 255)
        return spin

    @property
    def is_applying(self) -> bool:
        return self._apply_thread is not None and self._apply_thread.isRunning()

    def load_profile_file(self, path: str) -> bool:
        try:
            profiles = read_profiles(path)
            if not profiles:
                raise ValueError("The selected file contains no profile records")
        except (OSError, ValueError) as exc:
            self._profiles = []
            self.profile_combo.clear()
            self.profile_file_label.setText("Profile file could not be loaded")
            self.profile_file_label.setToolTip(path)
            self.status.setText(str(exc))
            self._refresh_preview()
            return False

        self._profiles = profiles
        self.profile_file_label.setText(Path(path).name)
        self.profile_file_label.setToolTip(path)
        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        for index, profile in enumerate(profiles):
            self.profile_combo.addItem(f"{index + 1}. {profile.name}", index)
        self.profile_combo.blockSignals(False)

        self._button_ini = None
        self._key = None
        self.data_ini_label.setText("Data.ini not loaded")
        self.data_ini_label.setToolTip("")
        path_obj = Path(path)
        candidate = path_obj.parent.parent / "Data.ini" if path_obj.parent.name.lower() == "data" else path_obj.parent / "Data.ini"
        if candidate.is_file():
            self.load_data_ini_file(str(candidate))
        else:
            self._on_profile_selected()
        return True

    def load_data_ini_file(self, path: str) -> bool:
        try:
            text = Path(path).read_text(encoding="utf-8-sig", errors="replace")
            button_ini = parse_button_ini(text)
            key = _read_key(path)
        except (OSError, ValueError, configparser.Error) as exc:
            self._button_ini = None
            self._key = None
            self.data_ini_label.setText("Data.ini could not be loaded")
            self.data_ini_label.setToolTip(path)
            self.status.setText(str(exc))
            self._on_profile_selected()
            return False

        self._button_ini = button_ini
        self._key = key
        self.data_ini_label.setText(Path(path).name)
        self.data_ini_label.setToolTip(path)
        self._on_profile_selected()
        return True

    def _on_profile_selected(self, *_args: Any) -> None:
        index = self.profile_combo.currentData()
        if index is None or not self._profiles:
            self._refresh_preview()
            return

        profile = self._profiles[index]
        controls = [
            self.mode_combo, self.polling_combo, self.active_stage_combo,
            *self.dpi_spins, self.light_mode_combo, self.brightness_spin,
            self.length_spin, self.frequency_spin, self.direction_spin,
            *self.fixed_rgb_spins,
        ]
        for control in controls:
            control.blockSignals(True)
        self.mode_combo.setCurrentIndex(self.mode_combo.findData(profile.game_mode))
        self.polling_combo.setCurrentIndex(self.polling_combo.findData(profile.polling_index))
        self.active_stage_combo.clear()
        for stage in range(max(1, min(profile.stage_count, 8))):
            self.active_stage_combo.addItem(f"Stage {stage + 1}", stage)
        self.active_stage_combo.setCurrentIndex(
            max(0, min(profile.active_stage, self.active_stage_combo.count() - 1))
        )
        for spin, value in zip(self.dpi_spins, profile.dpi_values):
            spin.setValue(max(100, min(12000, value * 50)))
        for stage, spin in enumerate(self.dpi_spins):
            spin.setEnabled(stage < profile.stage_count)
        self.light_mode_combo.setCurrentIndex(self.light_mode_combo.findData(profile.light_mode))
        self.brightness_spin.setValue(max(0, min(255, profile.brightness)))
        self.length_spin.setValue(max(0, min(4, profile.length)))
        self.frequency_spin.setValue(max(0, min(255, profile.frequency)))
        self.direction_spin.setValue(max(0, min(255, profile.direction)))
        for spin, value in zip(self.fixed_rgb_spins, profile.fixed_rgb):
            spin.setValue(value)
        for control in controls:
            control.blockSignals(False)

        self._populate_button_table(profile)
        self._refresh_preview()

    def _populate_button_table(self, profile: Profile) -> None:
        self._button_combos = []
        self.buttons_table.clearContents()
        for slot_index, slot in enumerate(profile.slots):
            page = slot_index // 16 + 1
            button = slot_index % 16 + 1
            self.buttons_table.setItem(
                slot_index, 0,
                QTableWidgetItem(f"Page {page}, button {button}"),
            )
            combo = QComboBox()
            actions = sorted(ACTIONS)
            for action in actions:
                if action in MACRO_ACTIONS and action != slot.action:
                    continue
                label = BUTTON_ACTION_NAMES.get(action, f"Action 0x{action:02X}")
                combo.addItem(f"{label} (0x{action:02X})", action)
            current_index = combo.findData(slot.action)
            if current_index < 0:
                combo.addItem(f"Unsupported action 0x{slot.action:02X}", slot.action)
                current_index = combo.count() - 1
            combo.setCurrentIndex(current_index)

            editable = self._button_ini is not None and self._button_ini[slot_index][1] != 0
            combo.setEnabled(editable)
            if not editable:
                combo.setToolTip("This slot is copied directly from Data.ini and is not profile-editable.")
            else:
                def on_action_changed(_index: int, index: int = slot_index) -> None:
                    self._on_button_action_changed(index)
                combo.currentIndexChanged.connect(on_action_changed)
            self._button_combos.append(combo)
            self.buttons_table.setCellWidget(slot_index, 1, combo)

    def _on_settings_changed(self, *_args: Any) -> None:
        index = self.profile_combo.currentData()
        if index is None or not self._profiles:
            return
        profile = self._profiles[index]
        dpi_values = tuple(spin.value() // 50 for spin in self.dpi_spins)
        slots = list(profile.slots)
        if self._button_ini is not None:
            for slot_index, combo in enumerate(self._button_combos):
                if self._button_ini[slot_index][1] != 0:
                    slots[slot_index] = replace(
                        slots[slot_index], action=int(combo.currentData())
                    )
        updated = replace(
            profile,
            game_mode=bool(self.mode_combo.currentData()),
            polling_index=int(self.polling_combo.currentData()),
            active_stage=int(self.active_stage_combo.currentData()),
            dpi_values=dpi_values,
            light_mode=int(self.light_mode_combo.currentData()),
            brightness=self.brightness_spin.value(),
            length=self.length_spin.value(),
            frequency=self.frequency_spin.value(),
            direction=self.direction_spin.value(),
            fixed_rgb=tuple(spin.value() for spin in self.fixed_rgb_spins),
            slots=tuple(slots),
        )
        self._profiles[index] = updated
        self._refresh_preview()

    def _on_button_action_changed(self, slot_index: int) -> None:
        index = self.profile_combo.currentData()
        if index is None or self._button_ini is None:
            return
        if self._button_ini[slot_index][1] == 0:
            return
        profile = self._profiles[index]
        slots = list(profile.slots)
        slots[slot_index] = replace(
            slots[slot_index], action=int(self._button_combos[slot_index].currentData())
        )
        self._profiles[index] = replace(profile, slots=tuple(slots))
        self._refresh_preview()

    def _choose_profile_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open wired SM809 profile", "",
            "Profile files (*.pbin *.bin);;All files (*)",
        )
        if path:
            self.load_profile_file(path)

    def _choose_data_ini(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Open matching Data.ini", "", "INI files (Data.ini *.ini);;All files (*)",
        )
        if path:
            self.load_data_ini_file(path)

    def _refresh_preview(self, *_args: Any) -> None:
        self._preview_valid = False
        self.apply_btn.setEnabled(False)
        if not self._profiles:
            self.preview.clear()
            return
        if self._button_ini is None or self._key is None:
            self.preview.setPlainText("Load the matching Data.ini to build a packet preview.")
            return

        index = self.profile_combo.currentData()
        if index is None:
            self.preview.clear()
            return
        profile = self._profiles[index]
        try:
            sequence = build_apply(profile, self._button_ini, BASELINE_REPLY)
            wire_sequence = to_wire(sequence, self._key)
        except (ValueError, NotImplementedError) as exc:
            self.preview.setPlainText(f"This profile cannot be applied safely:\n{exc}")
            self.status.setText("Preview unavailable; no device commands were sent.")
            return

        lines = [
            f"Profile: {profile.name}",
            f"Mode: {'Game' if profile.game_mode else 'Office'}; active DPI stage: {profile.active_stage + 1}",
            "Preview uses the captured 0x83 reply; apply reads the mouse's actual reply.",
            "",
        ]
        for (kind, plain), (_, wire) in zip(sequence, wire_sequence):
            if kind == "F":
                lines.append(f"F  {plain.hex(' ').upper()}  ->  {wire.hex(' ').upper()}")
            elif kind == "B":
                lines.append(f"B  {plain[:16].hex(' ').upper()} ... ({len(plain)} bytes)")
            else:
                lines.append("G  read query reply")
        lines.extend(("", "DRY RUN: no device commands have been sent."))
        self.preview.setPlainText("\n".join(lines))
        self.status.setText("Preview ready. Applying writes the full profile, button tables, DPI table, and lighting palettes.")
        self._preview_valid = True
        self.apply_btn.setEnabled(not self.is_applying)

    def _confirm_apply(self) -> None:
        if not self._profiles or self._button_ini is None or self._key is None:
            return
        confirmation = QMessageBox(self)
        confirmation.setWindowTitle("Full-profile hardware write")
        confirmation.setText(
            "This sends a full profile to the wired mouse and overwrites its current configuration. "
            "One factory-profile apply and post-write query were verified on one 04D9:A09F unit; "
            "other profiles and setting readback remain unverified. Continue only if this is your device."
        )
        confirmation.setIcon(QMessageBox.Warning)
        confirmation.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        confirmation.setDefaultButton(QMessageBox.Cancel)
        if confirmation.exec() != QMessageBox.Yes:
            return

        index = self.profile_combo.currentData()
        if index is None:
            return
        self._start_apply(self._profiles[index])

    def _start_apply(self, profile: Profile) -> None:
        if not self._preview_valid or self._button_ini is None or self._key is None or self.is_applying:
            return
        self._set_busy(True)
        thread = QThread(self)
        worker = _ApplyWorker(profile, self._button_ini, self._key)
        worker.moveToThread(thread)
        thread.started.connect(worker.run)
        worker.succeeded.connect(self._apply_succeeded)
        worker.failed.connect(self._apply_failed)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(self._apply_finished)
        thread.finished.connect(thread.deleteLater)
        self._apply_thread = thread
        self._worker = worker
        thread.start()

    def _set_busy(self, busy: bool) -> None:
        for widget in (self.profile_file_button, self.data_ini_button, self.profile_combo):
            widget.setEnabled(not busy)
        self.apply_btn.setEnabled(False if busy else self._preview_valid)
        if busy:
            self.status.setText("Applying full profile to the wired mouse…")

    def _apply_succeeded(self, message: str) -> None:
        self.status.setText("Profile applied. " + message)

    def _apply_failed(self, message: str) -> None:
        self.status.setText(f"Apply failed: {message}")

    def _apply_finished(self) -> None:
        self._apply_thread = None
        self._worker = None
        self._set_busy(False)