from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from sm809.config import load_config
from sm809.device import DeviceService
from sm809.model import DataStore, Profile
from sm809.protocol import (
    build_button_slots,
    deobfuscate,
    status_frame,
)
from sm809.transport import HidTransport


@pytest.fixture()
def store(tmp_path: Path) -> DataStore:
    data = tmp_path / "data"
    (data / "Data").mkdir(parents=True)
    src = Path(__file__).resolve().parent.parent / "data" / "Data"
    for name in ("profile.bin", "Data.bin", "Default.pbin", "macro.bin", "gun.bin"):
        shutil.copy2(src / name, data / "Data" / name)
    return DataStore(data / "Data")


def _plain(config, packet: bytes) -> bytes:
    return deobfuscate(packet, config.key) if config.has_password else packet


def test_demo_connect_and_apply(store: DataStore, shipped_config):
    service = DeviceService(shipped_config, store, demo=True)
    assert service.connect()
    assert service.linked
    assert service.read_version() == (shipped_config.ver_h, shipped_config.ver_l)

    before_packets = len(service.transport.sent_packets)
    before_blocks = len(service.transport.sent_blocks)
    result = service.apply(apply_windows=False)
    assert result.ok, result.error
    assert result.sent_packets > 10
    assert result.sent_blocks >= 11

    packets = service.transport.sent_packets[before_packets:]
    cmds = [_plain(shipped_config, p)[0] for p in packets]
    # status -> mode -> rate -> stage -> fixed colour -> light -> palettes ->
    # DPI -> four button frames -> commit.  The 0x8B status token is only a
    # GetFeature buffer value in FUN_004196b0, so it is never transmitted.
    assert cmds[:8] == [0x83, 0x03, 0x02, 0x01, 0x0B, 0x0C, 0x0D, 0x10]
    assert cmds.count(0x10) == 2
    assert cmds.count(0x12) == 4
    assert cmds[-1] == 0x08
    assert 0x8B not in cmds

    commit = _plain(shipped_config, packets[-1])
    assert commit == bytes((0x08, 0xAA, 0xCC, 0xEE, 0, 0, 0, 0x93))

    blocks = service.transport.sent_blocks[before_blocks:]
    assert all(len(b) == 32 for b in blocks)
    slots, _, _ = build_button_slots(store.profile, shipped_config)
    # palette 0 + palette 1 + DPI = 3 blocks before the button table.
    assert blocks[3] == slots[:32]
    assert blocks[4] == slots[32:64]


def test_status_frame_positions(store: DataStore, shipped_config):
    store.profile.lift = 1
    packet = status_frame(store.profile)
    assert packet[0] == 0x03
    assert packet[3] == 0x08
    assert packet[4] == 0x40
    store.profile.lift = 0
    assert status_frame(store.profile)[3] == 0x00


def test_demo_reports_packets_with_password(store: DataStore, shipped_config):
    service = DeviceService(shipped_config, store, demo=True)
    assert service.connect()
    packet = service.raw_packet(0x08, (0xAA, 0xCC, 0xEE))
    # raw_packet is the plain builder; send_feature carries obfuscation.
    assert packet == bytes((0x08, 0xAA, 0xCC, 0xEE, 0, 0, 0, 0x93))


def test_device_event_updates_profile(store: DataStore, shipped_config):
    service = DeviceService(shipped_config, store, demo=True)
    seen: list[tuple[int, int]] = []
    changed: list[str] = []
    service.on_device_event = lambda e, v: seen.append((e, v))
    service.on_profile_changed = changed.append

    service._handle_event(0x0700, 3)
    assert store.profile.stage == 2
    service._handle_event(0x0500, 8)
    assert store.profile.rate == 0
    service._handle_event(0x0500, 1)
    assert store.profile.rate == 3
    service._handle_event(0x0800, 2)
    assert store.profile.mode == 1
    assert changed == ["stage", "rate", "rate", "mode"]
    assert len(seen) == 4


def test_apply_offline_is_still_saved(store: DataStore, shipped_config):
    service = DeviceService(shipped_config, store, demo=True)
    # Force the disconnected path by clearing the demo's linked flag and
    # replacing ensure with a failure.
    service.linked = False
    service.ensure = lambda: False  # type: ignore[assignment]
    store.profile.name = "Offline Profile"
    result = service.apply(apply_windows=False)
    assert result.ok
    assert any("Not connected" in w for w in result.warnings)
    reloaded = DataStore(store.data_dir)
    assert reloaded.profile.name == "Offline Profile"
