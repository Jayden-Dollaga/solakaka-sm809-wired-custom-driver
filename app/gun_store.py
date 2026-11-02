"""
app.gun_store -- the host-side GUN (recoil pattern) library.

A gun is the wired firmware's recoil table: 30 bullet rows, each with an
X/Y cursor offset and a delay.  It has no slots of its own; like a macro it is
copied into the button entry that uses the ``Set Gun`` action (0x79), so it
travels with the profile and survives a .pbin round-trip.

The library itself is a named, unlimited JSON library (``config/guns.json``),
mirroring :mod:`app.macro_store`.  Device slots are implicit: the bound button
carries the rows, and stable ids (``dev:<profile>:<slot>``) are used when rows
are adopted from an imported profile so the editor keeps pointing at one entry.
"""

from __future__ import annotations

import json
import os
import uuid

MAX_ROWS = 30
X_MIN, X_MAX = -255, 255
Y_MIN, Y_MAX = -255, 255
DELAY_MIN, DELAY_MAX = 0, 2550
DELAY_STEP = 10


def default_path():
    from .paths import config_dir
    return os.path.join(config_dir(), "guns.json")


def default_rows():
    """A fresh pattern: the firmware's 30-row shape with no movement."""
    return [[0, 0, 10] for _ in range(MAX_ROWS)]


def clean_rows(rows) -> list[list[int]]:
    """Coerce stored rows to ``[[x, y, delay], ...]`` inside device limits."""
    out: list[list[int]] = []
    for row in rows or ():
        try:
            x, y, delay = (list(row) + [0, 0, 10])[:3]
            out.append([
                max(X_MIN, min(X_MAX, int(x))),
                max(Y_MIN, min(Y_MAX, int(y))),
                max(DELAY_MIN, min(DELAY_MAX, int(delay))),
            ])
        except (TypeError, ValueError):
            continue
        if len(out) >= MAX_ROWS:
            break
    return out


class GunStore:
    def __init__(self, path=None):
        self.path = path or default_path()
        self._guns: list[dict] = []      # {"id","name","rows"}
        self._dirty = False
        self.load()

    # -- persistence ----------------------------------------------------------
    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self._guns = [
                    {
                        "id": str(g.get("id") or uuid.uuid4().hex[:8]),
                        "name": str(g.get("name", "Gun")),
                        "rows": clean_rows(g.get("rows")) or default_rows(),
                    }
                    for g in data if isinstance(g, dict)
                ]
        except Exception:
            self._guns = []
        self._dirty = False

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._guns, f, indent=2)
            self._dirty = False
        except Exception:
            pass

    def save_if_dirty(self):
        if self._dirty:
            self.save()

    @property
    def dirty(self):
        return self._dirty

    # -- queries --------------------------------------------------------------
    def all(self):
        return list(self._guns)

    def get(self, gid):
        return next((g for g in self._guns if g["id"] == gid), None)

    def index_of(self, gid):
        for i, g in enumerate(self._guns):
            if g["id"] == gid:
                return i
        return -1

    def unique_name(self, base: str, exclude_id: str | None = None) -> str:
        """Return ``base`` or ``base (2)``/``base (3)``… unused in the library."""
        base = (base or "").strip() or "Gun"
        taken = {g["name"].casefold() for g in self._guns
                 if g["id"] != exclude_id}
        if base.casefold() not in taken:
            return base
        n = 2
        while f"{base} ({n})".casefold() in taken:
            n += 1
        return f"{base} ({n})"

    # -- mutations ------------------------------------------------------------
    def add(self, name=None):
        g = {
            "id": uuid.uuid4().hex[:8],
            "name": name or "New Gun",
            "rows": default_rows(),
        }
        self._guns.append(g)
        self.save()
        return g

    def add_with_id(self, gid, name=None, rows=None, persist=True):
        """Adopt rows embedded in a wired profile under a stable id."""
        g = self.get(gid)
        adopted = clean_rows(rows)
        changed = False
        if g is None:
            g = {"id": str(gid), "name": name or "Device Gun",
                 "rows": adopted or default_rows()}
            self._guns.append(g)
            changed = True
        if name and (not g.get("name") or g["name"].startswith("Device Gun")):
            if g["name"] != name:
                g["name"] = name
                changed = True
        if adopted and adopted != clean_rows(g.get("rows")):
            # Fill a fresh/default record from the profile; a pattern the user
            # has edited is never overwritten by a later profile scan.
            if g.get("name", "").startswith("Device Gun") or \
                    clean_rows(g.get("rows")) == default_rows():
                g["rows"] = adopted
                changed = True
        if changed:
            self._dirty = True
            if persist:
                self.save()
        return g

    def delete(self, gid):
        self._guns = [g for g in self._guns if g["id"] != gid]
        self.save()

    def rename(self, gid, name):
        g = self.get(gid)
        if g is not None and g["name"] != name:
            g["name"] = name
            self.save()

    def set_rows(self, gid, rows, persist=True):
        g = self.get(gid)
        if g is not None:
            g["rows"] = clean_rows(rows)
            if persist:
                self.save()
            else:
                self._dirty = True

    def set_row(self, gid, index, x, y, delay, persist=True):
        """Update one bullet row; used by the inline editor."""
        g = self.get(gid)
        if g is None or not 0 <= int(index) < len(g["rows"]):
            return
        g["rows"][int(index)] = [
            max(X_MIN, min(X_MAX, int(x))),
            max(Y_MIN, min(Y_MAX, int(y))),
            max(DELAY_MIN, min(DELAY_MAX, int(delay))),
        ]
        if persist:
            self.save()
        else:
            self._dirty = True
