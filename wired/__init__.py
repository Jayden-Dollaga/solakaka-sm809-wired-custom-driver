"""Wired SM809 (VID 04D9 / PID A09F) device core.

This package is the proven protocol/data layer reused by the wired studio UI.
It owns the 14-profile binary store, 64-slot button table, macro encoder,
Data.ini parser, Windows pointer settings and the apply engine.
"""

from . import config, device, keys, model, paths, protocol, transport, winspi

__version__ = "1.0.0"

__all__ = [
    "config", "device", "keys", "model", "paths", "protocol", "transport",
    "winspi",
]
