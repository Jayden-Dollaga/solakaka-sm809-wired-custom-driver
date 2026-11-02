"""
app.macro_store -- the host-side macro LIBRARY (named macros, no slots).

Mirrors how the official software works: macros live in a host-side library
(its MacroLibraryFile.mlf), and a device SLOT is assigned only when a macro is
bound to a button. So the library here is unlimited; slot assignment + upload
happen at bind time (see MainWindow._resolve_bindings / device.apply_macro_buttons).

Each macro: {"id": <8-hex>, "name": str, "events": [..]} in the sm809pro.macros
event format. Persisted to JSON so the library survives restarts (a focused
preview of the Milestone 3 profile store, which will later absorb this).

The optional ``loop``, ``folder`` and ``protected`` keys mirror the vendor's
.mbin record metadata so a macro imported from the original driver keeps its
folder, repeat count and "protected export" flag when it is exported again.
"""

import json
import os
import uuid


def default_path():
    # Portable: <config dir>/macros.json -- the project config folder from
    # source, next to the .exe when frozen, or inside SM809_DATA_DIR when that
    # override is set (see app.paths.config_dir).
    from .paths import config_dir
    return os.path.join(config_dir(), "macros.json")


class MacroStore:
    def __init__(self, path=None):
        self.path = path or default_path()
        self._macros = []          # list of {"id","name","events"}
        self._dirty = False        # deferred (bulk) change not yet written
        self.load()

    # -- persistence ----------------------------------------------------------
    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self._macros = [self._record(m) for m in data
                                if isinstance(m, dict)]
        except Exception:
            self._macros = []
        self._dirty = False

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._macros, f, indent=2)
            self._dirty = False
        except Exception:
            pass

    def save_if_dirty(self):
        """One write after a bulk adoption done with ``persist=False``."""
        if self._dirty:
            self.save()

    @staticmethod
    def _record(m: dict) -> dict:
        try:
            loop = int(m.get("loop", 1))
        except (TypeError, ValueError):
            loop = 1
        return {
            "id": str(m.get("id") or uuid.uuid4().hex[:8]),
            "name": str(m.get("name", "Macro")),
            "events": list(m.get("events", [])),
            "loop": max(0, min(0xFFFF, loop)),
            "folder": str(m.get("folder", "") or ""),
            "protected": bool(m.get("protected", False)),
        }

    # -- queries --------------------------------------------------------------
    def all(self):
        return list(self._macros)

    def unique_name(self, base: str, exclude_id: str | None = None) -> str:
        """Return ``base`` or ``base (2)``/``base (3)``… unused in the library.

        The vendor's import uniquifies names in the selected folder; the studio
        uses one flat library, so uniqueness across the whole library is what
        keeps two imported files distinguishable in the list and in exports.
        """
        base = (base or "").strip() or "Macro"
        taken = {m["name"].casefold() for m in self._macros
                 if m["id"] != exclude_id}
        if base.casefold() not in taken:
            return base
        n = 2
        while f"{base} ({n})".casefold() in taken:
            n += 1
        return f"{base} ({n})"

    def get(self, mid):
        return next((m for m in self._macros if m["id"] == mid), None)

    def index_of(self, mid):
        for i, m in enumerate(self._macros):
            if m["id"] == mid:
                return i
        return -1

    # -- mutations (each persists) -------------------------------------------
    def add(self, name=None, events=None, loop=1, folder="", protected=False):
        m = {
            "id": uuid.uuid4().hex[:8],
            "name": name or "New Macro",
            "events": list(events or []),
            "loop": max(0, min(0xFFFF, int(loop))),
            "folder": str(folder or ""),
            "protected": bool(protected),
        }
        self._macros.append(m)
        self.save()
        return m

    def add_with_id(self, mid, name=None, events=None, persist=True):
        """Create (or update) a library record with a caller-chosen id.

        Used to adopt macros embedded in a wired profile, whose ids are stable
        (``dev:<profile id>:<slot>``) so button bindings keep pointing at one
        editable library entry.  Pass ``persist=False`` when adopting in bulk
        and call :meth:`save` once afterwards.  Nothing is written when the
        record already matches.
        """
        m = self.get(mid)
        changed = False
        if m is None:
            m = self._record({"id": str(mid),
                              "name": name or "Device Macro",
                              "events": []})
            self._macros.append(m)
            changed = True
        if name and (not m.get("name") or m["name"].startswith("Device Macro")):
            if m["name"] != name:
                m["name"] = name
                changed = True
        if events and not m.get("events"):
            m["events"] = list(events)
            changed = True
        if changed:
            self._dirty = True
            if persist:
                self.save()
        return m

    def delete(self, mid):
        self._macros = [m for m in self._macros if m["id"] != mid]
        self.save()

    def rename(self, mid, name):
        m = self.get(mid)
        if m is not None:
            m["name"] = name
            self.save()

    def set_events(self, mid, events):
        m = self.get(mid)
        if m is not None:
            m["events"] = list(events)
            self.save()

    def set_meta(self, mid, loop=None, folder=None, protected=None):
        """Update .mbin-only metadata without touching the events."""
        m = self.get(mid)
        if m is None:
            return
        changed = False
        if loop is not None and int(loop) != m.get("loop", 1):
            m["loop"] = max(0, min(0xFFFF, int(loop)))
            changed = True
        if folder is not None and str(folder) != m.get("folder", ""):
            m["folder"] = str(folder)
            changed = True
        if protected is not None and bool(protected) != m.get("protected", False):
            m["protected"] = bool(protected)
            changed = True
        if changed:
            self.save()
