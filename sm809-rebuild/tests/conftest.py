import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sm809.config import load_config  # noqa: E402
from sm809.model import Profile  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


@pytest.fixture
def shipped_config():
    return load_config(DATA / "Data.ini")


@pytest.fixture
def default_profile():
    prof = Profile((DATA / "Data" / "Default.pbin").read_bytes())
    prof.name = "Test Profile"
    return prof
