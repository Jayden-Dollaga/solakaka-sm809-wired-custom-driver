"""Thin wired-device helpers for the studio.

Unlike the wireless reference package there is no mode auto-detection, status
listener or battery channel: an SM809 wired unit exposes one control interface
and pushes stage/rate/mode changes on its monitor interface.
"""

from __future__ import annotations

from pathlib import Path

from wired.config import DeviceConfig, load_config
from wired.device import DeviceError, DeviceService
from wired.model import DataStore
from wired.paths import DATA_DIR, ensure_data_dir

DEFAULT_DATA_DIR = DATA_DIR


def load_device_config(data_dir: Path | None = None) -> DeviceConfig:
    """Read Data.ini from the studio's own data directory."""
    root = ensure_data_dir() if data_dir is None else Path(data_dir)
    return load_config(Path(root) / "Data.ini")


def open_store(data_dir: Path | None = None) -> DataStore:
    root = ensure_data_dir() if data_dir is None else Path(data_dir)
    return DataStore(Path(root) / "Data")


def create_service(store: DataStore, config: DeviceConfig | None = None,
                   demo: bool = False) -> DeviceService:
    return DeviceService(config or load_device_config(), store, demo=demo)


def detect_modes(vid=None):
    """Compatibility shim: the wired studio only ever uses USB."""
    return [{"connection": "wired", "product": "SM809", "vid": vid}]


__all__ = [
    "DeviceConfig", "DeviceService", "DeviceError", "DataStore",
    "load_device_config", "open_store", "create_service", "detect_modes",
    "DEFAULT_DATA_DIR",
]
