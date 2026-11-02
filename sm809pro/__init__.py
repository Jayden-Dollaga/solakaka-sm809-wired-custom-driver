"""SM809 *wired* adapter package for the Solakaka studio UI.

The reference application was written for the wireless SM809 Pro. This package
keeps its import surface (``actions``, ``defaults``, ``macros``, ``protocol``)
but every translation now targets the wired firmware in :mod:`wired`.
"""

from __future__ import annotations

from . import actions, defaults, macros, protocol

__version__ = "1.0.0-wired"

__all__ = ["actions", "defaults", "macros", "protocol", "__version__"]
