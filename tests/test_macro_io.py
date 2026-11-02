"""Vendor .mbin import/export and library rename rules (offline).

The vendor exports exactly one 0x358-byte record (FUN_00412cc0) and imports
exactly one (FUN_00412520).  These tests pin that byte layout against the
macro.bin shipped in the portable seed, and cover the rename/uniquify rules the
macro and gun libraries share.
"""

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from app.macro_file import (
    FILE_FILTER,
    MacroFileError,
    load_macro,
    save_macro,
    suggest_name,
)
from app.macro_store import MacroStore
from app.gun_store import GunStore
from wired.model import MACRO_SIZE, MacroRecord
from wired.paths import SEED_DIR

VENDOR = SEED_DIR / "Data" / "macro.bin"


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def vendor_records() -> list[bytes]:
    raw = VENDOR.read_bytes()
    assert len(raw) % MACRO_SIZE == 0
    return [raw[i:i + MACRO_SIZE]
            for i in range(0, len(raw), MACRO_SIZE)]


def test_vendor_macro_round_trips_byte_for_byte(tmp_path):
    """Importing and re-exporting a vendor record must not alter one byte.

    Event bytes +0/+3/+6..7 are opaque to the encoder but real records use
    them, so the translator keeps them instead of rebuilding a "clean" event.
    """
    records = vendor_records()
    assert len(records) >= 2
    source = records[1]                     # "Spear Lunge" in folder Minecraft
    assert MacroRecord(source).name == "Spear Lunge"

    src = tmp_path / "spear.mbin"
    src.write_bytes(source)
    macro = load_macro(str(src))

    assert macro["name"] == "Spear Lunge"
    assert macro["folder"] == "Minecraft"
    assert macro["loop"] == 1
    assert macro["protected"] is False
    assert len(macro["events"]) == 7        # 6 vendor events + leading delay

    out = tmp_path / "copy.mbin"
    save_macro(str(out), macro)
    assert out.read_bytes() == source


def test_protected_export_sets_only_the_vendor_flag(tmp_path):
    source = vendor_records()[1]
    src = tmp_path / "spear.mbin"
    src.write_bytes(source)
    macro = load_macro(str(src))

    plain = tmp_path / "plain.mbin"
    protected = tmp_path / "protected.mbin"
    save_macro(str(plain), macro)
    save_macro(str(protected), macro, protected=True)

    plain_raw = plain.read_bytes()
    protected_raw = protected.read_bytes()
    assert plain_raw == source
    assert MacroRecord(protected_raw).protected is True
    diff = [i for i, (a, b) in enumerate(zip(plain_raw, protected_raw)) if a != b]
    assert diff == [0xD0]                   # the "encrypted export" flag


def test_folder_marker_is_not_imported(tmp_path):
    marker = vendor_records()[0]
    assert MacroRecord(marker).is_folder is True
    path = tmp_path / "folder.mbin"
    path.write_bytes(marker)
    with pytest.raises(MacroFileError, match="folder marker"):
        load_macro(str(path))


def test_import_accepts_trailing_records_and_falls_back_to_the_stem(tmp_path):
    records = vendor_records()
    path = tmp_path / "unnamed.mbin"
    # A macro record with no stored name; the vendor importer names it from
    # the file.  Whole-file concatenation is accepted because the first
    # record is the one FUN_00412520 reads.
    blank = bytearray(records[1])
    blank[0x64:0xC8] = b"\0" * 0x64
    blank[0xCC:0xCE] = b"\0\0"
    path.write_bytes(bytes(blank) + records[0])

    macro = load_macro(str(path))
    assert macro["name"] == "unnamed"
    assert macro["events"] == []
    assert macro["folder"] == "Minecraft"


def test_short_file_and_unexportable_macro_are_refused(tmp_path):
    short = tmp_path / "short.mbin"
    short.write_bytes(b"\0" * 100)
    with pytest.raises(MacroFileError, match="vendor macro record"):
        load_macro(str(short))

    # Nothing actionable to play -> refuse rather than write a dead record.
    with pytest.raises(MacroFileError, match="cannot be exported"):
        save_macro(str(tmp_path / "empty.mbin"),
                   {"name": "Empty", "events": []})

    # 40 long events overflow the device's 128-byte table.
    too_long = {"name": "Long", "events": [
        {"type": "key", "keycode": 0x04, "down": True, "next_delay": 5000}
        for _ in range(40)]}
    with pytest.raises(MacroFileError, match="128"):
        save_macro(str(tmp_path / "long.mbin"), too_long)
    assert not (tmp_path / "long.mbin").exists()


def test_suggest_name_sanitises_windows_characters():
    assert suggest_name({"name": 'A/B:C*D?"E'}) == "A_B_C_D__E.mbin"
    assert suggest_name({"name": "  .  "}) == "Macro.mbin"
    assert FILE_FILTER.startswith("Macro Data (*.mbin)")


def test_import_metadata_and_unique_names_persist(tmp_path):
    records = vendor_records()
    src = tmp_path / "spear.mbin"
    src.write_bytes(records[1])
    data = load_macro(str(src))

    store = MacroStore(str(tmp_path / "macros.json"))
    first = store.add(store.unique_name(data["name"]), data["events"],
                      loop=data["loop"], folder=data["folder"])
    # importing the same file twice must not produce two identical names
    second = store.add(store.unique_name(data["name"]), data["events"],
                       loop=data["loop"], folder=data["folder"],
                       protected=True)
    assert first["name"] == "Spear Lunge"
    assert second["name"] == "Spear Lunge (2)"
    assert second["folder"] == "Minecraft"
    assert second["loop"] == 1
    assert second["protected"] is True

    # rename keeps the rest of the record untouched and survives a reload
    store.rename(first["id"], "Spear (edited)")
    store.set_meta(first["id"], loop=3, folder="Loadout")
    again = MacroStore(str(tmp_path / "macros.json"))
    got = again.get(first["id"])
    assert got["name"] == "Spear (edited)"
    assert got["loop"] == 3
    assert got["folder"] == "Loadout"
    assert got["events"] == data["events"]


def test_gun_store_rename_and_unique_names(tmp_path):
    store = GunStore(str(tmp_path / "guns.json"))
    first = store.add(store.unique_name("AK"))
    second = store.add(store.unique_name("AK"))
    assert first["name"] == "AK"
    assert second["name"] == "AK (2)"

    store.rename(first["id"], "AK-47")
    # renaming to a taken name through unique_name is what the panel does
    assert store.unique_name("AK-47", exclude_id=second["id"]) == "AK-47 (2)"
    store.rename(second["id"],
                 store.unique_name("AK-47", exclude_id=second["id"]))

    again = GunStore(str(tmp_path / "guns.json"))
    assert sorted(g["name"] for g in again.all()) == ["AK-47", "AK-47 (2)"]


def test_blank_inline_rename_never_erases_the_stored_name(qapp, tmp_path):
    from app.panels.gun_panel import GunPanel
    from app.panels.macro_panel import MacroPanel

    macro_store = MacroStore(str(tmp_path / "macros.json"))
    macros = MacroPanel(macro_store)
    macros.new_macro()
    mid = macro_store.all()[0]["id"]
    macros.name_edit.clear()                # live edit ignores blanks
    assert macro_store.get(mid)["name"] == "Macro 1"
    macros._commit_name()                   # leaving the field restores it
    assert macro_store.get(mid)["name"] == "Macro 1"
    assert macros.name_edit.text() == "Macro 1"

    # typing a name another macro already owns is uniquified on commit
    macros.new_macro()
    second = macro_store.all()[1]["id"]
    macros.name_edit.setText("Macro 1")
    macros._commit_name()
    assert macro_store.get(second)["name"] == "Macro 1 (2)"
    assert "Macro 1 (2)" in macros.macro_list.item(1).text()
    macros.close()
    macros.deleteLater()

    gun_store = GunStore(str(tmp_path / "guns.json"))
    guns = GunPanel(gun_store)
    guns.new_gun()
    gid = gun_store.all()[0]["id"]
    guns.name_edit.clear()
    guns._commit_name()
    assert gun_store.get(gid)["name"] == "Gun 1"
    assert guns.name_edit.text() == "Gun 1"
    guns.close()
    guns.deleteLater()
