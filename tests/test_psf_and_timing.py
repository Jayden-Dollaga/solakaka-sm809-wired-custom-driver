"""Offline tests for .psf migration, smart diffing and hardware timing.

Everything runs against a scratch copy of the seed data with the demo HID
transport, so no hardware is touched and the vendor installation is never
opened.
"""

import json
import os
import shutil
import time
from pathlib import Path

import pytest

from wired.config import DeviceConfig
from wired.device import DeviceService
from wired.model import rgb_to_colorref
from wired.protocol import (
    CMD_SETTLE,
    MACRO_CHUNK_DELAY,
    build_dpi_block,
    deobfuscate,
)
from wired.transport import HidTransport

from sm809pro import actions as A

from app.macro_store import MacroStore
from app.psf_import import import_psf
from app.profile_store import ProfileStore


# ---------------------------------------------------------------------------
# Synthetic official .psf (UTF-16LE INI)
# ---------------------------------------------------------------------------
# Key n -> reference slot n; _PSF_PERMUTE maps it to the 0-based physical
# button.  The comments show which physical row each key becomes.
_PSF_TEXT = """\
[Profile]
ProfileName=Imported PSF
PollingRateValue=02
DPIOffOnFlagValue=03
CurrentDPILevelValue=01
XYSetting1ValueX=09
XYSetting2ValueX=0F
DPILevelIndication0Valuer=FF0000
DPILevelIndication1Valuer=00FF00
Lighting1ModeValue=080000
GameFile0=C:\\Games\\game.exe
; Key8 -> physical 2 -> wired slot 6: left click
Key8Value=100100
; Key9 -> physical 3 -> wired slot 7: DPI +
Key9Value=400200
; Key10 -> physical 4 -> wired slot 8: right click
Key10Value=100200
; Key3 -> physical 15 -> wired slot 3: play macro psf3
Key3Value=900102
; Key4 -> physical 16 -> wired slot 4: Run App (no wired equivalent)
Key4Value=600500
[MacroKey3]
MacroKey3Name=Test Mac
MacroActionNum=4
AllAction=A00000000300000048000000030000004880000003000000A080000003000000
"""


@pytest.fixture
def seeded_store(tmp_path):
    from wired.paths import SEED_DIR

    dest = tmp_path / "data"
    shutil.copytree(SEED_DIR, dest)
    return ProfileStore(path=str(tmp_path / "profiles.json"), data_dir=dest)


def trim(store, keep=3):
    # The shipped seed is a single default profile; top up when a test needs
    # a populated library.
    while len(store.all()) < keep:
        store.add(f"Profile {len(store.all()) + 1}")
    while len(store.all()) > keep:
        store.delete(store.all()[-1]["id"])


def write_psf(tmp_path, name="import.psf", text=_PSF_TEXT):
    path = tmp_path / name
    path.write_text(text, encoding="utf-16-le")
    return path


# ---------------------------------------------------------------------------
# .psf parsing and translation
# ---------------------------------------------------------------------------
def test_psf_parse_maps_fields_to_wired_schema(tmp_path):
    data = import_psf(write_psf(tmp_path))
    cfg = data["config"]

    assert data["name"] == "Imported PSF"
    assert data["match_rules"] == [{"exe": "game.exe", "title": None}]
    assert cfg["polling_hz"] == 500
    assert cfg["dpi"] == {
        "values": [1000, 1600],
        "colors": [[255, 0, 0], [0, 255, 0]],
        "enabled_count": 2,
        "selected": 1,
    }
    # Reference "Red" is wired Standard with a fixed red colour.
    assert cfg["lighting"]["mode"] == 1
    assert cfg["lighting"]["color"] == [255, 0, 0]
    assert any("Lighting:" in w for w in data["warnings"])
    assert len(cfg["buttons"]) == 64


def test_psf_buttons_use_reference_slot_permutation(tmp_path):
    cfg = import_psf(write_psf(tmp_path))["config"]

    def row(phys):
        return cfg["buttons"][A.PHYS_ORDER[phys]]

    # Both layers receive the imported binding.
    for base in A.LAYER_BASES:
        assert cfg["buttons"][base + A.PHYS_ORDER[1]] == (0x01, 0, 0)   # left
        assert cfg["buttons"][base + A.PHYS_ORDER[2]] == (0x07, 0, 0)   # DPI +
        assert cfg["buttons"][base + A.PHYS_ORDER[3]] == (0x02, 0, 0)   # right
    # Run App has no wired action: disabled, and reported.
    assert row(15) == (0x00, 0, 0)
    assert any("Button 16" in w for w in import_psf(write_psf(tmp_path))["warnings"])


def test_psf_macro_is_decoded_and_bound(tmp_path):
    data = import_psf(write_psf(tmp_path))
    mac = data["macros"][0]
    assert mac["name"] == "Test Mac"
    assert mac["playmode"] == 1 and mac["repeat"] == 2
    assert [e["keycode"] for e in mac["events"]] == [0xE1, 0x0B, 0x0B, 0xE1]
    assert [e["down"] for e in mac["events"]] == [True, True, False, False]

    for base in A.LAYER_BASES:
        binding = data["config"]["buttons"][base + A.PHYS_ORDER[14]]
        assert isinstance(binding, dict)
        assert binding["macro"] == "psf3"
        assert binding["name"] == "Test Mac"


def test_psf_parser_rejects_non_psf(tmp_path):
    from app.psf_import import PsfError

    path = tmp_path / "x.psf"
    path.write_text("not a profile", encoding="utf-16-le")
    with pytest.raises(PsfError):
        import_psf(path)


def test_store_import_psf_adopts_macros_and_writes_json(tmp_path, seeded_store):
    trim(seeded_store, keep=3)
    path = write_psf(tmp_path)
    macros = MacroStore(path=str(tmp_path / "macros.json"))

    prof, warnings = seeded_store.import_psf(path, macros)

    assert prof["name"] == "Imported PSF"
    assert seeded_store.get(prof["id"]) is not None
    cfg = seeded_store.config(prof["id"])
    binding = cfg["buttons"][A.PHYS_ORDER[14]]
    assert isinstance(binding, dict)
    # The wired record only carries name/events, so the library id is the
    # stable dev:<profile>:<slot> one.
    assert binding["macro"].startswith("dev:")
    adopted = macros.get(binding["macro"])
    assert adopted is not None and adopted["name"] == "Test Mac"
    assert len(adopted["events"]) == 4
    # Both layers were adopted too.
    assert macros.get(cfg["buttons"][A.LAYER_BASES[1] + A.PHYS_ORDER[14]]["macro"])
    assert cfg["polling_hz"] == 500
    assert any("Button 16" in w for w in warnings)

    # The readable mirror carries the complete config.
    side = json.loads((tmp_path / "profiles.json").read_text(encoding="utf-8"))
    entry = next(e for e in side["profiles"] if e["id"] == prof["id"])
    assert entry["config"]["polling_hz"] == 500
    assert len(entry["config"]["buttons"]) == 64
    assert entry["config"]["dpi"]["values"] == [1000, 1600]


def test_json_mirror_is_portable_across_reload(tmp_path, seeded_store):
    trim(seeded_store, keep=2)
    side = json.loads((tmp_path / "profiles.json").read_text(encoding="utf-8"))
    assert len(side["profiles"]) == 2
    for entry in side["profiles"]:
        assert len(entry["config"]["buttons"]) == 64

    again = ProfileStore(path=str(tmp_path / "profiles.json"),
                         data_dir=seeded_store.data_dir)
    assert [p["id"] for p in again.all()] == [p["id"] for p in seeded_store.all()]


# ---------------------------------------------------------------------------
# Smart diffing
# ---------------------------------------------------------------------------
@pytest.fixture
def live_service(seeded_store):
    trim(seeded_store, keep=3)
    cfg = seeded_store.device_config
    transport = HidTransport(cfg, demo=True)
    svc = DeviceService(cfg, seeded_store.data, demo=True, transport=transport)
    assert svc.connect()
    return svc, transport


def apply_sections(svc):
    result = svc.apply(apply_windows=False, persist=False)
    assert result.ok
    return result


def test_identical_apply_sends_no_hid_traffic(live_service):
    svc, tr = live_service
    first = apply_sections(svc)
    assert first.changed_sections            # full write on first link

    before = len(tr.sent_packets), len(tr.sent_blocks)
    again = apply_sections(svc)
    assert again.changed_sections == []
    assert (len(tr.sent_packets), len(tr.sent_blocks)) == before


def test_lighting_only_change_carries_the_whole_led_group(live_service):
    """The effect frame travels with the colour state it samples.

    The vendor always writes 0x0C (fixed colour), 0x0D (effect) and the two
    0x10 palette blocks in one download.  Sending only 0x0D let Slide with
    Loop Color sample colour state left over from an earlier profile, which
    made its fade start halfway through or skip entirely.
    """
    svc, tr = live_service
    apply_sections(svc)

    svc.store.profile.light_mode = 8       # Slide, Loop Color
    packets_before, blocks_before = len(tr.sent_packets), len(tr.sent_blocks)
    result = apply_sections(svc)

    assert result.changed_sections == ["color", "lighting", "palette"]
    # status pair + fixed colour + effect + two palette headers + commit
    assert len(tr.sent_packets) - packets_before == 7
    assert len(tr.sent_blocks) - blocks_before == 2
    plain = _plain_frames(svc, tr.sent_packets[packets_before:])
    commands = [p[0] for p in plain]
    assert commands.index(0x0C) < commands.index(0x0D) < commands.index(0x10)


def test_colour_and_palette_changes_also_carry_the_led_group(live_service):
    svc, tr = live_service
    apply_sections(svc)

    svc.store.profile.fixed_rgb = (0, 255, 0)
    packets_before, blocks_before = len(tr.sent_packets), len(tr.sent_blocks)
    result = apply_sections(svc)
    assert result.changed_sections == ["color", "lighting", "palette"]
    assert len(tr.sent_packets) - packets_before == 7
    assert len(tr.sent_blocks) - blocks_before == 2

    colors = list(svc.store.profile.cycle_colors)
    colors[0] = rgb_to_colorref((1, 2, 3))
    svc.store.profile.cycle_colors = colors
    packets_before, blocks_before = len(tr.sent_packets), len(tr.sent_blocks)
    result = apply_sections(svc)
    assert result.changed_sections == ["color", "lighting", "palette"]
    assert len(tr.sent_packets) - packets_before == 7
    assert len(tr.sent_blocks) - blocks_before == 2


def test_dpi_only_change_sends_dpi_section(live_service):
    svc, tr = live_service
    apply_sections(svc)

    values = svc.store.profile.dpi_values
    values[0] = values[0] + 100
    svc.store.profile.dpi_values = values
    packets_before, blocks_before = len(tr.sent_packets), len(tr.sent_blocks)
    result = apply_sections(svc)

    assert result.changed_sections == ["dpi"]
    # status pair + DPI header + re-asserted stage + commit, one block
    assert len(tr.sent_packets) - packets_before == 5
    assert len(tr.sent_blocks) - blocks_before == 1


def _plain_frames(svc, packets):
    if svc.config.has_password:
        return [deobfuscate(p, svc.config.key) for p in packets]
    return [bytes(p) for p in packets]


def test_stage_only_change_carries_the_dpi_table(live_service):
    """A host stage change must re-send 0x11 + 0x0B + 0x08, not just 0x0B.

    The wired firmware only adopts the stage inside the vendor's DPI sequence
    (FUN_00418a40 always writes the 0x11 table before 0x0B and commits after).
    Sending the bare stage frame left the sensor on the previous stage, so
    every DPI label except the previously applied one looked wrong.
    """
    svc, tr = live_service
    apply_sections(svc)
    prof = svc.store.profile
    target = 0 if prof.stage != 0 else 1
    prof.stage = target
    packets_before, blocks_before = len(tr.sent_packets), len(tr.sent_blocks)

    result = apply_sections(svc)

    assert result.changed_sections == ["stage", "dpi"]
    # status pair + stage + DPI header + re-asserted stage + commit
    assert len(tr.sent_packets) - packets_before == 6
    assert len(tr.sent_blocks) - blocks_before == 1
    plain = _plain_frames(svc, tr.sent_packets[packets_before:])
    assert any(p[0] == 0x11 for p in plain)
    assert tr.sent_blocks[-1] == build_dpi_block(prof, svc.config.sensor)
    assert plain[-2][0] == 0x0B and plain[-2][1] == target + 1
    assert plain[-1][0] == 0x08 and plain[-1][1:4] == b"\xaa\xcc\xee"


def test_set_stage_writes_the_vendor_dpi_sequence(live_service):
    """The quick stage switch (DPI page radios) uses the same DPI sequence."""
    svc, tr = live_service
    apply_sections(svc)
    prof = svc.store.profile
    prof.stage_count = 8          # the seed profile may enable a single stage
    prof.stage = 0
    packets_before, blocks_before = len(tr.sent_packets), len(tr.sent_blocks)

    assert svc.set_stage(1)

    plain = _plain_frames(svc, tr.sent_packets[packets_before:])
    commands = [p[0] for p in plain]
    assert commands[0] == 0x83
    assert 0x11 in commands
    assert len(tr.sent_blocks) - blocks_before == 1
    assert tr.sent_blocks[-1] == build_dpi_block(prof, svc.config.sensor)
    assert plain[-2][0] == 0x0B and plain[-2][1] == 2
    assert plain[-1][0] == 0x08 and plain[-1][1:4] == b"\xaa\xcc\xee"


def test_disconnect_forces_full_rewrite(live_service):
    svc, _tr = live_service
    apply_sections(svc)
    svc.disconnect()
    assert svc.connect()
    assert "buttons" in apply_sections(svc).changed_sections


def test_mode_change_rewrites_the_complete_profile(live_service):
    """A layer switch travels with the full download, exactly like the vendor.

    The wired firmware ignores a lone 0x02 frame (the vendor app only ever
    changes the mode inside FUN_00418a40's complete sequence), so the studio
    must re-send every section -- including the 0x12 button table -- when the
    mode changes instead of trusting the diff.
    """
    svc, tr = live_service
    svc.store.profile.mode = 0
    apply_sections(svc)                 # cached state: Office
    blocks_before = len(tr.sent_blocks)

    svc.store.profile.mode = 1          # user clicks Game
    result = apply_sections(svc)

    assert result.changed_sections[0] == "mode"
    assert "buttons" in result.changed_sections
    assert "dpi" in result.changed_sections
    # palette (2 blocks) + DPI table (1) + 0x12 table (8) at minimum.
    assert len(tr.sent_blocks) - blocks_before >= 8


def test_stale_mode_report_cannot_undo_a_mode_write(live_service):
    """An echo describing the layer being left must not flip the selection."""
    svc, _tr = live_service
    svc.store.profile.mode = 0
    apply_sections(svc)
    seen = []
    svc.on_profile_changed = seen.append

    # The 0x02 Office frame just went out, but the monitor still reports Game.
    svc._mode_expected = 0
    svc._mode_expected_at = time.monotonic()
    svc._handle_event(0x0800, 2)
    assert svc.store.profile.mode == 0
    assert seen == []

    # Well after the write, a genuine physical switch is followed.
    svc._mode_expected_at = time.monotonic() - 10.0
    svc._handle_event(0x0800, 2)
    assert svc.store.profile.mode == 1
    assert seen == ["mode"]


# ---------------------------------------------------------------------------
# Mandatory hardware timing
# ---------------------------------------------------------------------------
class _StubTransport:
    """A non-demo transport that records nothing and needs no HID library."""

    demo = False
    connected = True

    def __init__(self):
        self.sent_packets = []
        self.sent_blocks = []
        self.on_event = None
        self.on_disconnect = None

    def open(self):
        return True

    def close(self):
        pass

    def set_feature(self, packet):
        self.sent_packets.append(bytes(packet))
        return True

    def get_feature(self):
        return b""

    def write_block(self, block):
        self.sent_blocks.append(bytes(block))
        return True


def test_settle_and_macro_delays_are_mandatory(monkeypatch):
    from wired import device as DV

    assert CMD_SETTLE == pytest.approx(0.060)
    assert MACRO_CHUNK_DELAY == pytest.approx(0.120)

    svc = DeviceService(DeviceConfig(), None, demo=False,
                        transport=_StubTransport())
    assert svc.demo is False
    assert svc.cmd_settle == pytest.approx(CMD_SETTLE)
    assert svc.macro_chunk_delay == pytest.approx(MACRO_CHUNK_DELAY)

    slept = []
    monkeypatch.setattr(DV.time, "sleep", slept.append)
    svc.send_feature(b"\x00" * 8)
    assert slept == [pytest.approx(CMD_SETTLE)]
    slept.clear()
    svc.send_block(b"\x00" * 32)
    assert slept == [pytest.approx(0.02)]      # vendor block pace


def test_demo_mode_never_sleeps():
    svc = DeviceService(DeviceConfig(), None, demo=True,
                        transport=HidTransport(DeviceConfig(), demo=True))
    assert svc.demo is True
    assert svc.cmd_settle == 0.0
    assert svc.macro_chunk_delay == 0.0


def test_data_dir_override_isolates_config(tmp_path, monkeypatch):
    """A scratch SM809_DATA_DIR keeps every host file in the scratch folder."""
    from app import paths

    monkeypatch.setenv("SM809_DATA_DIR", str(tmp_path / "elsewhere"))
    base = os.path.abspath(str(tmp_path / "elsewhere"))
    assert paths.data_dir() == base
    assert paths.config_dir() == os.path.join(base, "config")

    monkeypatch.delenv("SM809_DATA_DIR")
    assert paths.data_dir() == os.path.join(paths.app_dir(), "data")
    assert paths.config_dir() == os.path.join(paths.app_dir(), "data", "config")


def test_every_host_library_file_lives_in_the_data_folder(tmp_path, monkeypatch):
    """Deleting data/ must remove profiles, macros, guns and app settings."""
    from app import paths
    from app.gun_store import default_path as guns_path
    from app.macro_store import default_path as macros_path
    from app.profile_store import default_path as profiles_path

    monkeypatch.setenv("SM809_DATA_DIR", str(tmp_path / "portable"))
    data = paths.data_dir()
    assert os.path.isdir(data) is False          # the sandbox starts empty
    for path in (profiles_path(), macros_path(), guns_path()):
        assert os.path.commonpath([data, os.path.abspath(path)]) == data


def test_legacy_config_is_copied_into_the_data_folder_once(tmp_path):
    """An upgrade imports the old <app>/config library exactly once."""
    from app import paths

    legacy = tmp_path / "app" / "config"
    legacy.mkdir(parents=True)
    (legacy / "profiles.json").write_text('{"settings": {}}', encoding="utf-8")
    target = tmp_path / "data" / "config"
    marker = tmp_path / "data" / ".factory-reset"

    got = paths._migrate_legacy_config(legacy, target, True, marker)
    assert got == target
    assert (target / "profiles.json").read_text(encoding="utf-8") == \
        '{"settings": {}}'

    # The live library wins from then on; the old copy never overwrites it.
    (target / "profiles.json").write_text('{"settings": {"changed": 1}}',
                                          encoding="utf-8")
    assert paths._migrate_legacy_config(legacy, target, True, marker) is None
    assert '"changed"' in (target / "profiles.json").read_text(encoding="utf-8")

    # Deleting only the library afterwards is a reset too: no re-import.
    shutil.rmtree(target)
    assert paths._migrate_legacy_config(legacy, target, True, marker) is None
    assert not target.exists()


def test_deleted_data_folder_is_a_reset_not_a_migration(tmp_path):
    """A missing data/ means factory reset, even if an old library lingers."""
    from app import paths

    legacy = tmp_path / "app" / "config"
    legacy.mkdir(parents=True)
    (legacy / "profiles.json").write_text('{"settings": {"old": 1}}',
                                          encoding="utf-8")
    target = tmp_path / "data" / "config"
    marker = tmp_path / "data" / ".factory-reset"

    assert paths._migrate_legacy_config(legacy, target, False, marker) is None
    assert marker.is_file()
    assert not target.exists()

    # Even a crash before the first settings write must not revive it.
    assert paths._migrate_legacy_config(legacy, target, True, marker) is None
    assert not target.exists()


def test_env_override_never_imports_the_real_library(tmp_path, monkeypatch):
    """Sandboxes and second portable copies start clean, not from the app dir."""
    from app import paths

    legacy = tmp_path / "app" / "config"
    legacy.mkdir(parents=True)
    (legacy / "profiles.json").write_text("{}", encoding="utf-8")
    sandbox = tmp_path / "sandbox"

    monkeypatch.setattr(paths, "app_dir", lambda: str(tmp_path / "app"))
    monkeypatch.setattr(paths, "_DATA_EXISTED_AT_START", True)
    monkeypatch.setenv("SM809_DATA_DIR", str(sandbox))
    assert paths.migrate_legacy_config() is None
    assert not (sandbox / "config").exists()
