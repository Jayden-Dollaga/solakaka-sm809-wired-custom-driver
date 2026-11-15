"""Supported-file detection, drag-and-drop routing and batch import.

The batch importer is the single path behind the Import dialog, a drop and
the tests: profiles and macros can arrive together, one bad file must not
cancel the rest, and the profile limit is reported per file.
"""

import os
import shutil

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import QMimeData, QPointF, Qt, QUrl
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import QApplication, QWidget

from app import theme
from app.file_import import (
    FileDropRouter,
    classify_path,
    split_paths,
    unique_paths,
)
from app.main_window import MainWindow
from wired.model import MACRO_SIZE, Profile
from wired.paths import SEED_DIR


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    app.setStyleSheet(theme.stylesheet())
    yield app
    for widget in list(app.topLevelWidgets()):
        widget.close()
        widget.deleteLater()
    app.processEvents()
    app.quit()


def _vendor_records():
    raw = (SEED_DIR / "Data" / "macro.bin").read_bytes()
    assert len(raw) % MACRO_SIZE == 0
    return [raw[i:i + MACRO_SIZE] for i in range(0, len(raw), MACRO_SIZE)]


def _seed_data(root):
    """A private wired data folder so a GUI test never touches another one."""
    data = root / "Data"
    data.mkdir(parents=True)
    for name in ("Data.bin", "profile.bin", "Default.pbin", "macro.bin",
                 "gun.bin"):
        src = SEED_DIR / "Data" / name
        if src.exists():
            shutil.copy2(src, data / name)
    ini = SEED_DIR / "Data.ini"
    if ini.exists():
        shutil.copy2(ini, root / "Data.ini")
    return root


@pytest.fixture()
def isolated_window(qapp, tmp_path, monkeypatch):
    """A demo MainWindow whose profile/macro/gun state lives under tmp_path."""
    import app.gun_store as gun_store
    import app.macro_store as macro_store
    import app.profile_store as profile_store

    data = _seed_data(tmp_path / "data")
    cfg = tmp_path / "config"
    cfg.mkdir()
    monkeypatch.setattr(profile_store, "default_path",
                        lambda: str(cfg / "profiles.json"))
    monkeypatch.setattr(profile_store, "ensure_data_dir", lambda: data)
    monkeypatch.setattr(macro_store, "default_path",
                        lambda: str(cfg / "macros.json"))
    monkeypatch.setattr(gun_store, "default_path",
                        lambda: str(cfg / "guns.json"))
    win = MainWindow(demo=True)
    win.show()
    yield win
    win.close()
    win.deleteLater()
    qapp.processEvents()


# -- classification ----------------------------------------------------------

def test_classify_uses_extension_first_and_size_for_bin(tmp_path):
    # explicit suffixes always decide, whatever the size
    assert classify_path(SEED_DIR / "Data" / "Default.pbin") == "profile"
    assert classify_path(SEED_DIR / "Data" / "profile.bin") == "profile"
    assert classify_path(SEED_DIR / "Data" / "macro.bin") == "macro"

    # a macro-sized file with a profile suffix is still a profile attempt
    disguised = tmp_path / "macro.pbin"
    disguised.write_bytes((SEED_DIR / "Data" / "macro.bin").read_bytes())
    assert classify_path(disguised) == "profile"

    # .bin: full record -> profile, whole macro records -> macro
    one_macro = tmp_path / "one.bin"
    one_macro.write_bytes(_vendor_records()[1])
    assert classify_path(one_macro) == "macro"
    short = tmp_path / "short.bin"
    short.write_bytes(b"\0" * 100)
    assert classify_path(short) is None
    empty = tmp_path / "empty.bin"
    empty.write_bytes(b"")
    assert classify_path(empty) is None

    # names that only look similar are not accepted
    text = tmp_path / "notes.txt"
    text.write_bytes((SEED_DIR / "Data" / "Default.pbin").read_bytes())
    assert classify_path(text) is None
    assert classify_path(tmp_path / "missing.pbin") is None
    assert classify_path(str(tmp_path)) is None


def test_split_paths_deduplicates_and_keeps_unsupported(tmp_path):
    profile = str(SEED_DIR / "Data" / "Default.pbin")
    macro = str(SEED_DIR / "Data" / "macro.bin")
    junk = tmp_path / "readme.txt"
    junk.write_text("not a macro", encoding="utf-8")

    profiles, macros, ignored = split_paths(
        [profile, macro, profile, str(junk)])
    assert profiles == [os.path.abspath(profile)]
    assert macros == [os.path.abspath(macro)]
    assert ignored == [os.path.abspath(str(junk))]

    # the same file under two spellings imports once
    assert len(unique_paths([profile, profile])) == 1


# -- drop routing ------------------------------------------------------------

def _drag_event(mime, drop=False):
    if drop:
        return QDropEvent(QPointF(10, 10), Qt.CopyAction, mime,
                          Qt.LeftButton, Qt.NoModifier)
    return QDragEnterEvent(QPointF(10, 10), Qt.CopyAction, mime,
                           Qt.LeftButton, Qt.NoModifier)


def _mime(paths=None, kind="files"):
    mime = QMimeData()
    if paths is not None:
        mime.setUrls([QUrl.fromLocalFile(path) for path in paths])
    else:
        mime.setData("application/x-qabstractitemmodeldatalist", b"\0")
    return mime


def test_drop_router_accepts_supported_files_and_passes_other_drags(qapp):
    window = QWidget()
    window.resize(320, 200)
    window.show()
    router = FileDropRouter(window)
    got = []
    router.files_dropped.connect(got.append)
    try:
        supported = [str(SEED_DIR / "Data" / "Default.pbin")]

        files = _mime(supported)
        enter = _drag_event(files)
        assert router.eventFilter(window, enter) is True
        assert enter.isAccepted()
        assert enter.dropAction() == Qt.CopyAction

        drop = _drag_event(files, drop=True)
        assert router.eventFilter(window, drop) is True
        assert got == [[os.path.abspath(supported[0])]]

        # the same drop event seen by a second filter is not emitted twice
        router.eventFilter(window, _drag_event(files, drop=True))
        assert len(got) == 1

        # an unsupported file keeps the normal no-drop cursor
        junk = _mime([str(SEED_DIR / "Data" / "gun.bin")])
        unsupported = _drag_event(junk)
        assert router.eventFilter(window, unsupported) is False
        assert not unsupported.isAccepted()

        # internal list reorder has no URLs and is left entirely alone
        internal = _mime(None)
        reorder = _drag_event(internal)
        assert router.eventFilter(window, reorder) is False
        assert not reorder.isAccepted()
    finally:
        router.uninstall()
        window.close()
        window.deleteLater()


def test_drop_router_is_wired_to_the_studio_window(isolated_window,
                                                   monkeypatch):
    win = isolated_window
    assert isinstance(win._drop_router, FileDropRouter)
    # the filter is attached to the page surfaces, not just the top level
    assert win.macro_panel.macro_list.acceptDrops()

    got = []
    monkeypatch.setattr(win, "import_files", got.append)
    mime = _mime([str(SEED_DIR / "Data" / "Default.pbin")])
    drop = _drag_event(mime, drop=True)
    assert win._drop_router.eventFilter(win.macro_panel.macro_list, drop)
    assert got and got[0][0].endswith("Default.pbin")


# -- batch import ------------------------------------------------------------

def test_batch_import_profiles_macros_and_isolated_failures(isolated_window,
                                                            tmp_path):
    win = isolated_window
    before_profiles = len(win.profiles.summaries())
    before_macros = len(win.store.all())
    records = _vendor_records()

    alpha = tmp_path / "alpha.pbin"
    beta = tmp_path / "beta.pbin"
    for path, name in ((alpha, "Dropped Alpha"), (beta, "Dropped Beta")):
        prof = Profile.from_file(SEED_DIR / "Data" / "Default.pbin")
        prof.name = name
        path.write_bytes(bytes(prof.raw))

    # one .mbin and the same record as a vendor-style .bin
    spear = tmp_path / "spear.mbin"
    spear.write_bytes(records[1])
    spear_bin = tmp_path / "spear.bin"
    spear_bin.write_bytes(records[1])

    broken = tmp_path / "broken.mbin"
    broken.write_bytes(b"\0" * 100)
    notes = tmp_path / "notes.txt"
    notes.write_text("not importable", encoding="utf-8")

    result = win.import_files(
        [str(alpha), str(beta), str(spear), str(spear_bin), str(broken),
         str(notes)], notify=False)

    assert [p["name"] for p in result["profiles"]] == ["Dropped Alpha",
                                                       "Dropped Beta"]
    assert len(result["macros"]) == 2
    # duplicate vendored names are uniquified inside the batch
    assert [m["name"] for m in result["macros"]] == ["Spear Lunge",
                                                     "Spear Lunge (2)"]
    assert len(result["errors"]) == 1
    assert result["errors"][0][0] == "broken.mbin"
    assert [os.path.basename(p) for p in result["ignored"]] == ["notes.txt"]
    assert result["skipped"] == 0

    # both profiles landed; only the LAST one is applied to the mouse
    assert len(win.profiles.summaries()) == before_profiles + 2
    assert win._applied_id == result["profiles"][-1]["id"]
    assert win.profiles.active_id == result["profiles"][-1]["id"]
    assert win.profile_combo.currentData() == win._applied_id

    # both macros are in the library and visible in the panel list
    assert len(win.store.all()) == before_macros + 2
    assert win.macro_panel.macro_list.count() == len(win.store.all())
    assert win.gun_panel is not None


def test_batch_import_reports_the_profile_limit(isolated_window, tmp_path,
                                                monkeypatch):
    win = isolated_window
    before = len(win.profiles.summaries())
    monkeypatch.setattr(win.profiles, "at_limit", lambda: True)
    path = tmp_path / "extra.pbin"
    shutil.copy2(SEED_DIR / "Data" / "Default.pbin", path)

    result = win.import_files([str(path)], notify=False)

    assert result["profiles"] == []
    assert result["skipped"] == 1
    assert result["errors"] == []
    assert len(win.profiles.summaries()) == before
