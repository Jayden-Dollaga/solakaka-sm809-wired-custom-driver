"""Profile library backed by the wired SM809's binary profile table.

The studio keeps the same public API it always used (``all/get/add/...``), but
the source of truth is now :class:`wired.model.DataStore`: ``profile.bin`` holds
up to 14 complete wired profiles. A small sidecar JSON (``config/profiles.json``)
adds what the wired format has no room for -- stable UI ids, auto-switch match
rules, creation order and app settings -- so the UI keeps working across
restarts and profile reordering.

Conversions between the wired ``Profile`` record and the studio config dict
(buttons, DPI, lighting, pointer) live in :mod:`wired.bridge`.
"""

from __future__ import annotations

import json
import os
import uuid
from pathlib import Path

from sm809pro import defaults as D

from wired.bridge import config_to_profile, profile_to_config
from wired.device import DeviceService
from wired.model import PROFILE_COUNT, DataStore
from wired.paths import DATA_DIR, ensure_data_dir

PROFILE_LIMIT = PROFILE_COUNT


def default_path():
    from .paths import config_dir
    return os.path.join(config_dir(), "profiles.json")


def default_config():
    """Factory config for the wired SM809 (from ``Default.pbin``)."""
    return D.config()


class ProfileStore:
    """A DataStore adapter with stable ids and auto-switch metadata."""

    def __init__(self, path=None, data_dir=None, device_config=None,
                 macro_events=None, gun_rows=None):
        self.path = path or default_path()
        self.data_dir = Path(data_dir) if data_dir else ensure_data_dir()
        if data_dir is not None:
            self.data_dir.mkdir(parents=True, exist_ok=True)
        self.data = DataStore(self.data_dir / "Data")
        if device_config is None:
            from sm809pro.device import load_device_config
            device_config = load_device_config(self.data_dir)
        self.device_config = device_config
        self.sensor = int(device_config.sensor)
        # Optional callable: macro id -> list of studio events (set by MainWindow
        # once the MacroStore exists).
        self.macro_events = macro_events
        # Optional callable: gun id -> list of [x, y, delay] rows.
        self.gun_rows = gun_rows
        self._meta: list[dict] = []     # parallel to self.data.profiles
        self._active = None
        self._settings: dict = {}
        self._seq = 0
        # Generation counter for deferred edits: set_config(persist=False)
        # bumps it; save_profiles() records the generation it wrote. A worker
        # apply that persisted an older snapshot therefore does not hide a
        # newer edit from the debounced flush.
        self._edit_gen = 0
        self._saved_gen = 0
        self.load()

    # -- persistence ----------------------------------------------------------
    def load(self):
        side = {}
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                side = json.load(f)
            if not isinstance(side, dict):
                side = {}
        except Exception:
            side = {}

        old_meta = list(side.get("profiles", []))
        self._settings = dict(side.get("settings", {}))
        self._meta = self._reconcile(old_meta)

        wanted = side.get("active")
        if wanted not in {m["id"] for m in self._meta}:
            wanted = self._meta[0]["id"] if self._meta else None
        self._active = wanted
        for i, m in enumerate(self._meta):
            if not isinstance(m.get("created"), (int, float)):
                m["created"] = i
        self._seq = max([m["created"] for m in self._meta], default=0)
        # Repair LED bytes written by older studio builds before anything can
        # export or apply them: +0xFC is the 0/1 fixed/cycle colour mode, not a
        # 1..255 slider.  This is a one-time write; subsequent loads are clean.
        repaired = False
        for prof in self.data.profiles:
            repaired = prof.sanitize_lighting() or repaired
        if repaired:
            self.data.save_profiles()
        self.save()

    def _reconcile(self, old_meta: list[dict]) -> list[dict]:
        """Match sidecar records to the (possibly edited) binary profiles."""
        used: set[int] = set()
        out: list[dict] = []
        for i, prof in enumerate(self.data.profiles):
            match = None
            # exact position + name first (normal case)
            if (i < len(old_meta) and i not in used
                    and str(old_meta[i].get("name", "")) == prof.name):
                match = old_meta[i]
                used.add(i)
            if match is None:
                for j, meta in enumerate(old_meta):
                    if j not in used and str(meta.get("name", "")) == prof.name:
                        match = meta
                        used.add(j)
                        break
            match = match or {}
            out.append({
                "id": str(match.get("id") or uuid.uuid4().hex[:8]),
                "name": prof.name,
                "match_rules": list(match.get("match_rules", [])),
                "created": match.get("created", i),
            })
        return out

    def save(self):
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            # The binary profile table is authoritative for the mouse, but
            # config/profiles.json is also a human-readable, portable mirror:
            # every profile carries its full config so the file can be read,
            # diffed or copied even without profile.bin.
            profiles = []
            for i, meta in enumerate(self._meta):
                entry = {
                    "id": meta.get("id"),
                    "name": meta.get("name"),
                    "match_rules": list(meta.get("match_rules", [])),
                    "created": meta.get("created"),
                }
                if i < len(self.data.profiles):
                    try:
                        entry["config"] = self._config(i, meta["id"])
                    except Exception:
                        pass
                profiles.append(entry)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump({"active": self._active, "profiles": profiles,
                           "settings": self._settings}, f, indent=2)
        except Exception:
            pass

    def save_profiles(self):
        """Write the full binary profile table (all slots, ~1.65 MB)."""
        self.data.save_profiles()
        # The table now contains every in-memory edit.
        self._saved_gen = self._edit_gen

    def flush(self):
        """Settle deferred work at a quiet point (timer, hide, quit).

        Writes the binary table only if an edit is unsaved, and always refreshes
        the portable JSON mirror so it never lags behind a worker apply.
        """
        if self.profiles_dirty:
            self.save_profiles()
        self.save()

    @property
    def profiles_dirty(self):
        return self._edit_gen != self._saved_gen

    # -- app-level settings ---------------------------------------------------
    def get_setting(self, key, default=None):
        return self._settings.get(key, default)

    def set_setting(self, key, value):
        self._settings[key] = value
        self.save()

    def set_settings(self, values):
        """Update several settings and write the sidecar once (dialog accept)."""
        self._settings.update(values or {})
        self.save()

    # -- helpers --------------------------------------------------------------
    def _index(self, pid):
        for i, m in enumerate(self._meta):
            if m["id"] == pid:
                return i
        return -1

    def _profile(self, pid):
        idx = self._index(pid)
        return (idx, self.data.profiles[idx]) if idx >= 0 else (-1, None)

    def _config(self, idx, pid):
        prof = self.data.profiles[idx]
        # Button entries carry their own display name next to an embedded macro;
        # pass those through so the UI shows meaningful macro labels.
        macro_names = {}
        for i in range(len(prof.buttons)):
            entry = prof.button(i)
            if int(entry.action) == 0x16 and int(entry.count) and entry.name:
                macro_names[int(entry.macro_index)] = entry.name
        return profile_to_config(prof, pid, macro_names=macro_names,
                                 sensor=self.sensor)

    def _dict(self, idx, include_config=True):
        meta = self._meta[idx]
        out = {
            "id": meta["id"],
            "name": self.data.profiles[idx].name,
            "match_rules": list(meta.get("match_rules", [])),
            "created": meta.get("created"),
            "index": idx,
        }
        if include_config:
            out["config"] = self._config(idx, meta["id"])
        return out

    def _disambiguate(self, name, exclude_id=None):
        used = {m["name"].lower() for m in self._meta if m["id"] != exclude_id}
        used |= {p.name.lower() for i, p in enumerate(self.data.profiles)
                 if self._meta[i]["id"] != exclude_id}
        name = (name or "Profile").strip() or "Profile"
        if name.lower() not in used:
            return name
        n = 1
        while f"{name} ({n})".lower() in used:
            n += 1
        return f"{name} ({n})"

    def _write_config(self, prof, config):
        config_to_profile(prof, config or {},
                          macro_events=self.macro_events,
                          gun_rows=self.gun_rows,
                          sensor=self.sensor)

    # -- queries --------------------------------------------------------------
    def all(self):
        return [self._dict(i) for i in range(len(self.data.profiles))]

    def summaries(self):
        """Lightweight id/name/rule records (no per-profile config conversion).

        The combo, tray menu and auto-switcher only need these, so the 200 ms
        foreground poll no longer rebuilds the full button/DPI/lighting config
        of every profile."""
        out = []
        for i, meta in enumerate(self._meta):
            if i >= len(self.data.profiles):
                break
            out.append({
                "id": meta["id"],
                "name": self.data.profiles[i].name,
                "match_rules": list(meta.get("match_rules", [])),
                "created": meta.get("created"),
                "index": i,
            })
        return out

    def match_targets(self):
        """Just the info rule matching needs: profile id + match rules."""
        return [{"id": m["id"], "match_rules": list(m.get("match_rules", []))}
                for m in self._meta]

    def embedded_macros(self):
        """Yield ``(dev_id, name, events)`` for macros stored inside the wired
        button table.

        Scans the raw records directly instead of building every profile's full
        config, which is what made startup macro adoption expensive.
        """
        from wired.bridge import BUTTON_COUNT, binding_from_entry

        for i, meta in enumerate(self._meta):
            if i >= len(self.data.profiles):
                break
            prof = self.data.profiles[i]
            pid = meta["id"]
            for slot in range(BUTTON_COUNT):
                binding = binding_from_entry(prof.button(slot), slot, pid)
                if isinstance(binding, dict) and binding.get("macro"):
                    yield binding["macro"], binding.get("name"), binding.get("events")

    def embedded_guns(self):
        """Yield ``(dev_id, name, rows, repeat)`` for recoil patterns stored
        inside the wired button table (action 0x79)."""
        from wired.bridge import BUTTON_COUNT, binding_from_entry

        for i, meta in enumerate(self._meta):
            if i >= len(self.data.profiles):
                break
            prof = self.data.profiles[i]
            pid = meta["id"]
            for slot in range(BUTTON_COUNT):
                binding = binding_from_entry(prof.button(slot), slot, pid)
                if isinstance(binding, dict) and binding.get("gun"):
                    yield (binding["gun"], binding.get("name"),
                           binding.get("rows"), binding.get("repeat"))

    def get(self, pid):
        idx = self._index(pid)
        return self._dict(idx) if idx >= 0 else None

    def index_of(self, pid):
        return self._index(pid)

    @property
    def active_id(self):
        return self._active

    def active(self):
        return self.get(self._active) if self._active else None

    def config(self, pid):
        idx = self._index(pid)
        return self._config(idx, pid) if idx >= 0 else None

    def at_limit(self):
        return len(self.data.profiles) >= PROFILE_LIMIT

    # -- mutations (each persists) -------------------------------------------
    def set_active(self, pid, persist=True):
        """Remember the active profile. ``persist=False`` lets a manual switch
        update the UI immediately and batch the sidecar write with the debounced
        profile flush."""
        if self._index(pid) >= 0:
            self._active = pid
            if persist:
                self.save()

    def unique_name(self, name, exclude_id=None):
        return self._disambiguate(name, exclude_id)

    def add(self, name=None, config=None, match_rules=None):
        if self.at_limit():
            raise ValueError(f"the wired SM809 stores at most {PROFILE_LIMIT} profiles")
        name = self._disambiguate(name or "New Profile")
        self.data.add_profile(name)
        idx = len(self.data.profiles) - 1
        self._write_config(self.data.profiles[idx], config or default_config())
        self.save_profiles()
        self._seq += 1
        self._meta.append({"id": uuid.uuid4().hex[:8], "name": name,
                           "match_rules": list(match_rules or []),
                           "created": self._seq})
        self.save()
        return self._dict(idx)

    def duplicate(self, pid, name=None):
        idx = self._index(pid)
        if idx < 0:
            return None
        if self.at_limit():
            raise ValueError(f"the wired SM809 stores at most {PROFILE_LIMIT} profiles")
        src = self.data.profiles[idx]
        copy = self.data.duplicate_profile(idx)   # inserts after, selects copy
        if name:
            copy.name = self._disambiguate(name)
        meta = self._meta[idx]
        self._seq += 1
        self._meta.insert(idx + 1, {
            "id": uuid.uuid4().hex[:8],
            "name": copy.name,
            "match_rules": list(meta.get("match_rules", [])),
            "created": self._seq,
        })
        self.save_profiles()
        self.save()
        return self._dict(idx + 1)

    def reorder(self, ids):
        order = []
        for pid in ids:
            i = self._index(pid)
            if i >= 0 and i not in order:
                order.append(i)
        order += [i for i in range(len(self._meta)) if i not in order]
        if not order:
            return
        self.data.reorder_profiles(order)
        self._meta = [self._meta[i] for i in order]
        self.save()

    def sort_by(self, key):
        if key == "az":
            order = sorted(range(len(self._meta)),
                           key=lambda i: self._meta[i]["name"].lower())
        elif key == "za":
            order = sorted(range(len(self._meta)),
                           key=lambda i: self._meta[i]["name"].lower(),
                           reverse=True)
        elif key == "latest":
            order = sorted(range(len(self._meta)),
                           key=lambda i: self._meta[i].get("created") or 0,
                           reverse=True)
        elif key == "oldest":
            order = sorted(range(len(self._meta)),
                           key=lambda i: self._meta[i].get("created") or 0)
        else:
            return
        self.data.reorder_profiles(order)
        self._meta = [self._meta[i] for i in order]
        self.save()

    def delete(self, pid):
        idx = self._index(pid)
        if idx < 0:
            return
        if len(self.data.profiles) <= 1:
            raise ValueError("the last profile cannot be deleted")
        self.data.delete_profile(idx)
        self._meta.pop(idx)
        if self._active == pid:
            self._active = self._meta[0]["id"] if self._meta else None
        self.save()

    def rename(self, pid, name):
        idx = self._index(pid)
        if idx < 0:
            return
        name = self._disambiguate(name, exclude_id=pid)
        self.data.rename_profile_at(idx, name)
        self._meta[idx]["name"] = name
        self.save()

    def set_config(self, pid, config, persist=True):
        """Commit a config into its wired record.

        ``persist=False`` updates memory only and marks the table dirty; the
        caller flushes it later (MainWindow debounces slider/binding edits so
        a full 1.65 MB table write is not repeated on every UI event).
        """
        idx = self._index(pid)
        if idx < 0:
            return
        prof = self.data.profiles[idx]
        self._write_config(prof, config)
        self._edit_gen += 1
        if persist:
            self.save_profiles()

    def set_match_rules(self, pid, rules):
        idx = self._index(pid)
        if idx >= 0:
            self._meta[idx]["match_rules"] = list(rules)
            self.save()

    def reset_config(self, pid):
        """Restore one profile to the wired factory defaults (name kept)."""
        idx = self._index(pid)
        if idx < 0:
            return None
        self.data.reset_profile(idx)
        self.save()
        return self._dict(idx)

    # -- device apply ---------------------------------------------------------
    def apply(self, pid, service: DeviceService, config=None,
              apply_windows=True):
        """Write one profile in full and make it the device's current record."""
        idx = self._index(pid)
        if idx < 0:
            return None
        prof = self.data.profiles[idx]
        if config is not None:
            self._write_config(prof, config)
            # ``service.apply(persist=True)`` writes the whole table after the
            # frames go out, so saving here would write the same ~1.65 MB twice.
        self.data.selected = idx
        # Snapshot the edit generation BEFORE the write: if a newer deferred
        # edit lands while the worker is busy, it stays dirty and the debounced
        # flush will still persist it.
        written_gen = self._edit_gen
        result = service.apply(prof, apply_windows=apply_windows, persist=True)
        if result is not None and result.ok:
            self._saved_gen = max(self._saved_gen, written_gen)
        return result

    # -- import / export ------------------------------------------------------
    def export_pbin(self, pid, path):
        idx = self._index(pid)
        if idx < 0:
            raise ValueError("unknown profile")
        self.data.export_profile(Path(path), idx)

    def import_pbin(self, path):
        if self.at_limit():
            raise ValueError(f"the wired SM809 stores at most {PROFILE_LIMIT} profiles")
        prof = self.data.import_profile(Path(path))
        self._seq += 1
        self._meta.append({"id": uuid.uuid4().hex[:8], "name": prof.name,
                           "match_rules": [], "created": self._seq})
        self.save()
        return self._dict(len(self.data.profiles) - 1)

    def import_psf(self, path, macro_store=None):
        """Import an official .psf profile.

        Returns ``(profile_dict, warnings)``.  When ``macro_store`` is given,
        the embedded sequences are adopted into the library under the stable
        ``dev:<profile>:<slot>`` ids the wired record reads back as, so the
        imported macros stay editable.
        """
        from .psf_import import import_psf as parse_psf

        if self.at_limit():
            raise ValueError(f"the wired SM809 stores at most {PROFILE_LIMIT} profiles")
        data = parse_psf(path)

        prof = self.add(data["name"], config=data["config"],
                        match_rules=data.get("match_rules"))

        # The wired record embeds a macro's name and events, but not the host
        # library id.  Read the persisted bindings back and adopt their stable
        # ``dev:<profile>:<slot>`` ids, exactly like macros that were already
        # on the mouse, so the imported sequence stays editable.
        if macro_store is not None:
            saved = self.config(prof["id"]) or {}
            for binding in saved.get("buttons", []):
                if isinstance(binding, dict) and binding.get("macro"):
                    macro_store.add_with_id(binding["macro"],
                                            binding.get("name"),
                                            binding.get("events"),
                                            persist=False)
            macro_store.save_if_dirty()      # one write for the whole import
        return prof, list(data.get("warnings", []))
