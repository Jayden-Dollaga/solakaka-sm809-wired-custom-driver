"""Import/export one macro in the original driver's .mbin format.

The vendor software exports exactly one 0x358-byte record with no file header
(FUN_00412cc0) and imports exactly one record (FUN_00412520).  Layout:

    +0x000  folder name   wchar[50]
    +0x064  macro name    wchar[50]
    +0x0C8  loop          u16
    +0x0CC  event count   u16 (0..40)
    +0x0D0  protected     u32 (1 = "protected" export, FUN_00412f40)
    +0x0D4  folder flag   u32 (1 = this record is a folder marker)
    +0x0D8  40 x 16-byte events

A plain export writes the record with +0x0D0 cleared.  The protected export
sets +0x0D0 = 1, exactly like the vendor menu item (FUN_00412f40).  The studio
keeps the opaque event bytes (see wired.model.MacroEvent) so importing a vendor
macro and exporting it again preserves the original record.
"""

from __future__ import annotations

import os
import re

from wired.bridge import (
    macro_binding_problem,
    ref_events_to_wired,
    wired_events_to_ref,
)
from wired.model import MACRO_SIZE, MacroRecord

__all__ = ["MacroFileError", "load_macro", "save_macro", "suggest_name"]

FILE_FILTER = "Macro Data (*.mbin);;All files (*)"


class MacroFileError(ValueError):
    """The file is not a usable vendor macro record."""


def _clean_stem(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0].strip()


def load_macro(path: str) -> dict:
    """Read the first record of a vendor .mbin file into a library item."""
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < MACRO_SIZE:
        raise MacroFileError(
            f"this file is {len(data)} bytes; a vendor macro record is "
            f"{MACRO_SIZE} bytes")
    # The vendor importer reads exactly one record; accept a file holding
    # several records by taking the first, and do not fail on trailing bytes.
    record = MacroRecord(data[:MACRO_SIZE])
    if record.is_folder:
        raise MacroFileError("this file is a folder marker, not a macro")
    name = record.name.strip() or _clean_stem(path) or "Imported Macro"
    return {
        "name": name,
        "folder": record.folder_name,
        "loop": record.loop,
        "protected": record.protected,
        "events": wired_events_to_ref(record.events),
        "source": os.path.basename(path),
    }


def save_macro(path: str, macro: dict, protected: bool = False) -> None:
    """Write one 0x358-byte record the original driver can import."""
    problem = macro_binding_problem(macro.get("events") or [])
    if problem:
        raise MacroFileError(
            f"this macro cannot be exported: {problem}")
    events = ref_events_to_wired(macro.get("events") or [])
    record = MacroRecord()
    record.is_folder = False
    record.folder_name = str(macro.get("folder") or "")
    record.name = str(macro.get("name") or "Macro")
    record.loop = max(0, min(0xFFFF, int(macro.get("loop", 1) or 0)))
    record.protected = bool(protected)
    record.set_events(events)
    with open(path, "wb") as f:
        f.write(bytes(record.raw))


def suggest_name(macro: dict) -> str:
    """A safe default file name for an export dialog."""
    name = str(macro.get("name") or "Macro").strip() or "Macro"
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip(" .")
    return (name or "Macro") + ".mbin"
