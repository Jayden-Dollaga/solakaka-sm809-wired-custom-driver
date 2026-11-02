"""Regression tests for DPI stage selection with disabled (gapped) stages.

The wired firmware numbers DPI stages only among the enabled ones (a prefix
count), while the panel always shows eight fixed rows.  Clicking a stage or
receiving a device push must map between the two numbering schemes without the
highlight jumping to a disabled row.
"""

import pytest

pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from app.panels import dpi_panel as dpi_mod
from sm809pro import defaults as D


@pytest.fixture(scope="module")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


def _panel(enabled=6):
    return dpi_mod.DpiPanel(dpi=list(D.DPI_VALUES),
                            colors=list(D.DPI_COLORS),
                            enabled_count=enabled)


def _active_rows(panel):
    return [i for i, row in enumerate(panel.rows) if row._active]


def test_clicking_first_enabled_stage_keeps_highlight(qapp):
    """Stage 1 disabled: clicking the first visible enabled row must keep the
    outline there, not move it back to disabled row 0."""
    panel = _panel()
    panel.rows[0].toggle.setChecked(False)
    emitted = []
    panel.active_dpi_requested.connect(lambda dpis, sel: emitted.append(sel))

    panel.rows[1]._on_idx_clicked(None)          # first enabled row

    assert emitted == [0]                         # device-relative index
    assert _active_rows(panel) == [1]             # highlight stays on row 1
    assert panel.active_row() is panel.rows[1]


def test_device_push_maps_relative_stage_to_enabled_row(qapp):
    """The status push reports a relative stage; the highlight must land on the
    matching enabled row, not on the same-numbered disabled row."""
    panel = _panel()
    panel.rows[0].toggle.setChecked(False)
    panel.set_active_stage(0)                     # first enabled stage
    assert _active_rows(panel) == [1]
    panel.set_active_stage(1)                     # second enabled stage
    assert _active_rows(panel) == [2]
    assert panel.active_row() is panel.rows[2]


def test_clicking_disabled_stage_is_ignored(qapp):
    panel = _panel()
    panel.rows[0].toggle.setChecked(False)
    emitted = []
    panel.active_dpi_requested.connect(lambda *a: emitted.append(a))
    panel.rows[0]._on_idx_clicked(None)
    assert emitted == []


def test_disabling_active_stage_moves_highlight_immediately(qapp):
    """No 250 ms window where a disabled row keeps the active outline."""
    panel = _panel()
    panel.rows[2]._on_idx_clicked(None)
    assert _active_rows(panel) == [2]

    panel.rows[2].toggle.setChecked(False)

    assert _active_rows(panel) == [0]             # first still-enabled row
    enabled = panel._enabled_indices()
    assert enabled[panel._active_relative()] == 0


def test_apply_compacts_gaps_to_prefix_and_reports_relative(qapp):
    """Gaps are compacted for the firmware, and `selected` follows the
    compaction so the device latches the row the user is looking at."""
    panel = _panel()
    panel.rows[0].toggle.setChecked(False)        # gap above the selection
    panel.rows[2]._on_idx_clicked(None)
    panel._apply_timer.stop()

    applied = []
    panel.apply_requested.connect(lambda *a: applied.append(a))
    panel._emit_apply()

    dpis, _colors, selected = applied[0]
    enabled = panel._enabled_indices()
    assert dpis == [panel.rows[i].dpi() for i in enabled]
    assert selected == enabled.index(2) == 1


def test_profile_load_uses_relative_selected(qapp):
    """Loading a profile passes a relative `selected`; the highlight must map
    it through the enabled prefix written by set_values."""
    panel = _panel()
    panel.set_values(list(D.DPI_VALUES[:4]), list(D.DPI_COLORS[:4]),
                     enabled_count=4)
    panel.set_active_stage(2)                     # third enabled stage

    assert _active_rows(panel) == [2]
    assert [r.is_enabled() for r in panel.rows[:4]] == [True] * 4
    assert not panel.rows[4].is_enabled()


def test_last_enabled_stage_cannot_be_disabled(qapp):
    """The mouse always has one stage; don't leave the panel with none."""
    panel = _panel(enabled=1)
    panel.rows[0].toggle.setChecked(False)
    assert panel.rows[0].toggle.isChecked()
    assert _active_rows(panel) == [0]


def test_out_of_range_push_clamps_to_last_enabled_stage(qapp):
    panel = _panel(enabled=3)
    panel.set_active_stage(99)
    assert _active_rows(panel) == [2]
