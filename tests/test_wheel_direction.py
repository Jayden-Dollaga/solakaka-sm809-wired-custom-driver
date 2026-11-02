"""Per-device Windows wheel-direction helper.

These tests never write to HKLM.  The orchestration test replaces the writer
and the restart call, and the panel test replaces ``read_state``.
"""

import json
import subprocess
import sys

import pytest

from wired import wheel_direction as W


def test_devices_are_sm809_mouse_collections_only():
    instances = W.device_instances()
    for instance in instances:
        assert instance.startswith("HID\\")
        assert "VID_04D9&PID_A09F&MI_00" in instance.upper()
        assert "MI_01" not in instance.upper()


def test_read_state_agrees_with_instances():
    state = W.read_state()
    assert state.total == len(state.instances)
    assert 0 <= state.flipped <= state.total
    assert state.inverted == (state.total > 0 and state.flipped == state.total)
    assert isinstance(state.global_reverse, bool)
    assert state.describe()


def test_instance_paths_point_into_the_enum_hive():
    """Dropping the hive prefix made reads default to 0 and writes fail 2."""
    path = W._instance_key("HID\\VID_04D9&PID_A09F&MI_00\\abc")
    assert path == (
        r"SYSTEM\CurrentControlSet\Enum\HID"
        r"\VID_04D9&PID_A09F&MI_00\abc")


def test_device_parameters_key_opens_through_the_mapped_path():
    if W.winreg is None:
        pytest.skip("Windows only")
    instances = W.device_instances()
    if not instances:
        pytest.skip("SM809 not connected")
    import winreg

    path = W._instance_key(instances[0]) + r"\Device Parameters"
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0,
                        winreg.KEY_READ):
        pass


def test_apply_requires_admin_and_reports_cancel(monkeypatch):
    monkeypatch.setattr(W, "is_admin", lambda: False)
    monkeypatch.setattr(W, "_run_elevated",
                        lambda parameters, timeout_ms=180000:
                        (False, "Administrator permission was cancelled.", None))
    result = W.apply_elevated(True)
    assert result.ok is False
    assert "cancel" in result.message.lower()


def test_elevated_command_does_not_repeat_the_interpreter(monkeypatch):
    """lpFile already is python.exe.  Repeating it in lpParameters made the
    elevated Python run its own ``python.exe`` as a script and exit with a
    SyntaxError before it could write any status file."""
    if W.winreg is None or sys.platform != "win32":
        pytest.skip("Windows-only elevation path")
    captured = {}
    monkeypatch.setattr(W, "is_admin", lambda: False)

    def fake_run(parameters, timeout_ms=180000):
        captured["parameters"] = parameters
        return False, "stubbed", None

    monkeypatch.setattr(W, "_run_elevated", fake_run)
    result = W.apply_elevated(True)
    assert result.ok is False
    params = captured["parameters"]
    assert sys.executable not in params
    assert params.startswith("-m wired.wheel_direction")
    assert "--apply 1" in params
    assert "--status" in params


def test_child_reports_a_crash_instead_of_an_empty_file(tmp_path, monkeypatch):
    def boom(_invert):
        raise RuntimeError("boom")

    monkeypatch.setattr(W, "apply", boom)
    status = tmp_path / "status.json"
    code = W._child_main(["--apply", "1", "--status", str(status)])
    payload = json.loads(status.read_text(encoding="utf-8"))
    assert code == 1
    assert payload["ok"] is False
    assert "boom" in payload["message"]


def test_apply_writes_the_device_flag_and_clears_global(monkeypatch):
    instance = "HID\\VID_04D9&PID_A09F&MI_00\\fake&0&0000"
    writes = []
    global_writes = []
    restarts = []

    monkeypatch.setattr(W, "is_admin", lambda: True)
    monkeypatch.setattr(W, "device_instances", lambda: [instance])
    monkeypatch.setattr(W, "_set_dp_dword",
                        lambda inst, name, value: writes.append((inst, name, value)))
    monkeypatch.setattr(W, "_set_global_default",
                        lambda: global_writes.append(True))
    monkeypatch.setattr(W, "_restart_device",
                        lambda inst, timeout=20: restarts.append(inst) or None)
    monkeypatch.setattr(
        W, "read_state",
        lambda: W.WheelState((instance,), 1, 1, False))

    result = W.apply(True)
    assert result.ok is True
    assert writes == [(instance, "FlipFlopWheel", 1)]
    assert global_writes == [True]          # Windows back to its default
    assert restarts == [instance]

    writes.clear()
    restarts.clear()
    monkeypatch.setattr(
        W, "read_state",
        lambda: W.WheelState((instance,), 0, 1, False))
    result = W.apply(False)
    assert result.ok is True
    assert writes == [(instance, "FlipFlopWheel", 0)]
    assert restarts == [instance]


def test_restart_falls_back_to_disable_enable(monkeypatch):
    calls = []

    def fake_pnputil(*args, timeout=20):
        calls.append(args)
        if args[0] == "/restart-device":
            return subprocess.CompletedProcess(args, 1, "", "Access is denied.")
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(W, "_pnputil", fake_pnputil)
    monkeypatch.setattr(W.time, "sleep", lambda _seconds: None)
    assert W._restart_device("HID\\fake") is None
    assert calls == [("/restart-device", "HID\\fake"),
                     ("/disable-device", "HID\\fake"),
                     ("/enable-device", "HID\\fake")]


def test_apply_retries_when_windows_reenumerates(monkeypatch):
    """A restart can create a new instance id that starts with the flag unset."""
    old = "HID\\VID_04D9&PID_A09F&MI_00\\old"
    new = "HID\\VID_04D9&PID_A09F&MI_00\\new"
    instance_sets = iter([[old], [old], [new], [new]])
    states = iter([W.WheelState((old,), 0, 1, False),
                   W.WheelState((old,), 0, 1, False),
                   W.WheelState((new,), 1, 1, False)])
    writes = []

    monkeypatch.setattr(W, "is_admin", lambda: True)
    monkeypatch.setattr(W, "device_instances", lambda: next(instance_sets))
    monkeypatch.setattr(W, "_set_dp_dword",
                        lambda inst, name, value: writes.append((inst, value)))
    monkeypatch.setattr(W, "_set_global_default", lambda: None)
    monkeypatch.setattr(W, "_restart_device", lambda inst, timeout=20: None)
    monkeypatch.setattr(W, "read_state", lambda: next(states))

    result = W.apply(True)
    assert result.ok is True
    assert writes == [(old, 1), (new, 1)]


def test_panel_reflects_the_windows_state(qapp, monkeypatch):
    from app.panels.performance_panel import PerformancePanel

    monkeypatch.setattr(
        W, "read_state",
        lambda: W.WheelState(("HID\\fake",), 0, 1, False))
    panel = PerformancePanel()
    try:
        assert panel.win_fix.isEnabled()
        assert panel.win_fix.isChecked() is False
        assert "Not fixed" in panel.win_fix_status.text()

        monkeypatch.setattr(
            W, "read_state",
            lambda: W.WheelState(("HID\\fake",), 1, 1, False))
        panel.refresh_wheel_fix()
        assert panel.win_fix.isChecked() is True
        assert "Fixed" in panel.win_fix_status.text()
    finally:
        panel.deleteLater()


def test_panel_cancel_reverts_the_checkbox(qapp, monkeypatch):
    from PySide6.QtWidgets import QMessageBox

    from app.panels.performance_panel import PerformancePanel

    monkeypatch.setattr(
        W, "read_state",
        lambda: W.WheelState(("HID\\fake",), 0, 1, False))
    monkeypatch.setattr(QMessageBox, "question",
                        lambda *args, **kwargs: QMessageBox.Cancel)
    panel = PerformancePanel()
    try:
        panel.win_fix.setChecked(True)      # asks; user cancels
        assert panel.win_fix.isChecked() is False
        assert panel._wheel_worker is None
    finally:
        panel.deleteLater()


@pytest.fixture(scope="module")
def qapp():
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    yield app
