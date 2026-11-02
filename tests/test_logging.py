"""Logging and diagnostics tests.

The studio used to rely on bare print() calls, so a write that the firmware
accepted but mishandled left no trace.  These tests pin down the replacement:
a rotating file log, collapsing of repeated console lines, and failure
messages that name the exact frame / section involved.
"""

import io
import logging
import shutil
from types import SimpleNamespace

import pytest

from app.controller import DeviceController
from app.logging_setup import RepeatCollapsingHandler, setup_logging
from wired.config import DeviceConfig
from wired.device import ApplyResult, DeviceError, DeviceService
from wired.model import Profile
from wired.paths import SEED_DIR
from wired.protocol import frame, light_frame
from wired.transport import HidTransport

from app.profile_store import ProfileStore


# ---------------------------------------------------------------------------
# Setup / file output
# ---------------------------------------------------------------------------
def test_setup_logging_writes_debug_file(tmp_path):
    path = setup_logging(log_dir=str(tmp_path), install_hooks=False,
                         install_qt=False)
    assert path is not None
    log = logging.getLogger("sm809.test")
    log.info("visible marker")
    log.debug("debug marker")

    root = logging.getLogger("sm809")
    for handler in root.handlers:
        handler.flush()

    text = (tmp_path / "studio.log").read_text(encoding="utf-8")
    assert "visible marker" in text
    assert "debug marker" in text          # the file keeps DEBUG detail


def test_setup_logging_replaces_its_own_handlers(tmp_path):
    setup_logging(log_dir=str(tmp_path / "one"), install_hooks=False,
                  install_qt=False)
    setup_logging(log_dir=str(tmp_path / "two"), install_hooks=False,
                  install_qt=False)
    owned = [h for h in logging.getLogger("sm809").handlers
             if getattr(h, "_sm809_owned", False)]
    assert len(owned) == 2                 # one console + one file, not four
    logging.getLogger("sm809.test").info("second location")
    for handler in owned:
        handler.flush()
    assert "second location" in (tmp_path / "two" / "studio.log").read_text(
        encoding="utf-8")


# ---------------------------------------------------------------------------
# Console collapsing
# ---------------------------------------------------------------------------
def _record(message, level=logging.INFO):
    return logging.LogRecord("sm809.test", level, __file__, 1, message, None, None)


def test_repeat_collapsing_handler_folds_identical_lines():
    stream = io.StringIO()
    handler = RepeatCollapsingHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))

    handler.emit(_record("same line"))
    handler.emit(_record("same line"))
    handler.emit(_record("same line"))
    handler.emit(_record("different"))
    handler.flush()

    lines = stream.getvalue().splitlines()
    assert lines[0] == "same line"
    assert lines[1].strip() == "... previous message repeated 2 more times"
    assert lines[2] == "different"
    assert len(lines) == 3                 # exactly one summary, not a flood


def test_repeat_collapsing_handler_flushes_tail_on_flush():
    stream = io.StringIO()
    handler = RepeatCollapsingHandler(stream)
    handler.setFormatter(logging.Formatter("%(message)s"))

    handler.emit(_record("warning"))
    handler.emit(_record("warning"))
    handler.emit(_record("warning"))
    handler.flush()

    lines = stream.getvalue().splitlines()
    assert lines[0] == "warning"
    assert "repeated 2 more times" in lines[1]
    # flushing again must not repeat the summary
    handler.flush()
    assert len(stream.getvalue().splitlines()) == 2


# ---------------------------------------------------------------------------
# Actionable failures
# ---------------------------------------------------------------------------
class _FailingTransport:
    demo = False
    connected = False
    on_event = None
    on_disconnect = None

    def __init__(self):
        self.sent_packets = []
        self.sent_blocks = []

    def open(self):
        return False

    def close(self):
        pass

    def enumerate(self):
        return False

    def set_feature(self, packet):
        return False

    def get_feature(self):
        return b""

    def write_block(self, block):
        return False


def test_set_feature_failure_names_the_frame():
    cfg = DeviceConfig(password="")        # no obfuscation: raw bytes in the log
    svc = DeviceService(cfg, transport=_FailingTransport(), pace=0, settle=0)
    packet = frame(0x0D, (9, 200, 0x22, 0, 0, 0))

    with pytest.raises(DeviceError) as info:
        svc.send_feature(packet)
    message = str(info.value)
    assert "SetFeature failed for frame" in message
    assert "0d 09 c8 22" in message


# ---------------------------------------------------------------------------
# Apply diagnostics
# ---------------------------------------------------------------------------
@pytest.fixture
def store(tmp_path):
    dest = tmp_path / "data"
    shutil.copytree(SEED_DIR, dest)
    return ProfileStore(path=str(tmp_path / "profiles.json"), data_dir=dest)


def test_apply_logs_the_encoded_lighting_values(store, caplog):
    cfg = store.device_config
    svc = DeviceService(cfg, store.data, demo=True,
                        transport=HidTransport(cfg, demo=True))
    assert svc.connect()

    prof = store.data.profile
    prof.light_mode = 9
    prof.brightness = 200
    prof.length = 3          # breathing
    prof.frequency = 1       # colour mode -> encoded as 2
    prof.direction = 2

    with caplog.at_level(logging.DEBUG, logger="sm809.device"):
        result = svc.apply(apply_windows=False, persist=False)

    assert result.ok
    text = "\n".join(r.getMessage() for r in caplog.records)
    assert "apply profile:" in text
    assert "light mode=9" in text
    # mode 9: brightness, then colour mode | ((4 - breathing) << 4)
    assert "lighting frame: 0d 09 c8 12" in text


def test_encoder_warns_when_it_must_clamp(caplog):
    prof = Profile()
    prof.light_mode = 200
    prof.brightness = 999
    with caplog.at_level(logging.WARNING, logger="sm809.lighting"):
        light_frame(prof)
    text = "\n".join(r.getMessage() for r in caplog.records)
    assert "lighting effect 200 is out of range" in text
    assert "brightness=999 is out of range" in text


def test_repeated_apply_warnings_are_logged_once(store, caplog):
    """Distance=0 and the gun-note describe standing config, not each write."""
    ctrl = DeviceController(store)

    class _Profiles:
        def apply(self, pid, dev, config=None):
            return ApplyResult(ok=True, warnings=["Distance=0 note"],
                               changed_sections=[])

    ctrl._profiles = _Profiles()
    ctrl._dev = SimpleNamespace(store=store.data)

    with caplog.at_level(logging.WARNING, logger="sm809.controller"):
        assert ctrl._apply_config({}, "pid")
        assert ctrl._apply_config({}, "pid")

    warnings = [r.getMessage() for r in caplog.records
                if r.levelno == logging.WARNING]
    assert warnings == ["Distance=0 note"]
