"""
app.recoil_player -- host-side playback for recoil patterns.

The wired SM809 firmware never executes recoil tables.  The vendor build hides
its Gun page, and its apply routine copies only macro tables into the upload
buffer (action 0x16); the ``Set Gun`` (0x79) block is assembled and discarded.
A button bound to "Recoil Control" therefore does nothing on the mouse.

This module plays the same pattern from Windows instead: while the chosen
trigger button is held, it injects relative mouse movement with ``SendInput``
so the cursor follows the rows.  Playback is opt-in and only runs while the
studio is alive.

The engine is deliberately injectable -- clock, button state and the move sink
can be replaced -- so its timing can be tested without a real mouse, a Windows
message loop, or any traffic to the device.
"""

from __future__ import annotations

import ctypes
import sys
import time
from ctypes import wintypes

from PySide6.QtCore import QObject, Qt, QTimer, Signal

# A 4 ms poll matches the fastest row delay users are likely to dial in while
# staying cheap: GetAsyncKeyState is a trivial user-mode call.
TICK_MS = 4

# (label, virtual-key) pairs.  The first five are the mouse buttons Windows
# reports as button state; a side button must still be bound to its normal
# function for the player to see it.
TRIGGERS = (
    ("Left", 0x01),
    ("Right", 0x02),
    ("Middle", 0x04),
    ("Side 1 (Back)", 0x05),
    ("Side 2 (Forward)", 0x06),
)
DEFAULT_TRIGGER = 0x05
HOST_PLAYBACK_AVAILABLE = sys.platform == "win32"

MOUSEEVENTF_MOVE = 0x0001
_INPUT_MOUSE = 0


class _MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_size_t),   # ULONG_PTR, 32/64-bit safe
    ]


class _INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("mi", _MOUSEINPUT),
    ]


def _now_ms() -> float:
    return time.perf_counter() * 1000.0


def _is_down(vk: int) -> bool:
    """Global physical button state, whether or not the studio has focus."""
    if not HOST_PLAYBACK_AVAILABLE:
        return False
    try:
        return bool(ctypes.windll.user32.GetAsyncKeyState(int(vk)) & 0x8000)
    except Exception:
        return False


def _send_move(dx: int, dy: int) -> None:
    """Inject one relative pointer move."""
    if not HOST_PLAYBACK_AVAILABLE:
        return
    try:
        inp = _INPUT()
        inp.type = _INPUT_MOUSE
        inp.mi.dx = int(dx)
        inp.mi.dy = int(dy)
        inp.mi.dwFlags = MOUSEEVENTF_MOVE
        ctypes.windll.user32.SendInput(
            1, ctypes.byref(inp), ctypes.sizeof(_INPUT))
    except Exception:
        pass


def clean_rows(rows) -> list[tuple[int, int, int]]:
    """``[(x, y, delay_ms), ...]`` with non-negative delays, junk dropped."""
    out: list[tuple[int, int, int]] = []
    for row in rows or ():
        try:
            x, y, delay = (list(row) + [0, 0, 10])[:3]
            out.append((int(x), int(y), max(0, int(delay))))
        except (TypeError, ValueError):
            continue
    return out


class RecoilPlayer(QObject):
    """Plays a recoil pattern while its trigger button is held.

    Rows are ``[x, y, delay]``: move by (x, y) pixels, then wait ``delay``
    milliseconds before the next row.  One pattern plays per press; releasing
    the trigger stops it, and holding it after the last row does not loop.
    Negative offsets are honored (unlike the firmware table, which stores only
    the magnitude).
    """

    active_changed = Signal(bool)

    def __init__(self, parent=None, *, clock=None, is_down=None,
                 send_move=None):
        super().__init__(parent)
        self._clock = clock or _now_ms
        self._is_down = is_down or _is_down
        self._send = send_move or _send_move
        self._rows: list[tuple[int, int, int]] = []
        self._trigger = DEFAULT_TRIGGER
        self._enabled = False
        self._active = False
        self._row = 0
        self._next_due = 0.0
        self._down_prev = False

        self._timer = QTimer(self)
        self._timer.setTimerType(Qt.PreciseTimer)
        self._timer.setInterval(TICK_MS)
        self._timer.timeout.connect(self.tick)

    # -- state ----------------------------------------------------------------
    @property
    def enabled(self) -> bool:
        return self._enabled

    @property
    def active(self) -> bool:
        return self._active

    @property
    def trigger(self) -> int:
        return self._trigger

    @property
    def rows(self) -> list[list[int]]:
        return [[x, y, d] for x, y, d in self._rows]

    # -- configuration --------------------------------------------------------
    def set_rows(self, rows) -> None:
        clean = clean_rows(rows)
        if clean == self._rows:
            return
        # Never keep injecting offsets from a pattern that is being edited.
        self._stop()
        self._rows = clean
        self._sync_timer()

    def set_trigger(self, vk) -> None:
        try:
            vk = int(vk)
        except (TypeError, ValueError):
            return
        if vk == self._trigger:
            return
        self._stop()
        self._trigger = vk
        self._down_prev = self._is_down(vk)   # a held button is not a new press

    def set_enabled(self, on: bool) -> None:
        on = bool(on)
        if on == self._enabled:
            return
        self._enabled = on
        if on:
            # Do not fire from a press that predates enabling playback.
            self._down_prev = self._is_down(self._trigger)
        else:
            self._stop()
            self._down_prev = False
        self._sync_timer()

    def _sync_timer(self) -> None:
        """Poll only while playback is enabled and a pattern exists."""
        if self._enabled and self._rows:
            if not self._timer.isActive():
                self._timer.start()
        else:
            self._timer.stop()

    # -- playback -------------------------------------------------------------
    def tick(self) -> None:
        """Poll the trigger and send any rows that are due."""
        if not self._enabled:
            return
        down = bool(self._is_down(self._trigger))
        if not down:
            self._down_prev = False
            self._stop()
            return
        if not self._down_prev:
            self._down_prev = True
            if self._rows:
                self._start()
        if not self._active:
            return
        now = self._clock()
        while self._row < len(self._rows) and now >= self._next_due:
            x, y, delay = self._rows[self._row]
            self._row += 1
            if x or y:
                self._send(x, y)
            self._next_due += delay
        if self._row >= len(self._rows):
            # One burst per press: stay stopped while the trigger is held.
            self._stop()

    def _start(self) -> None:
        self._active = True
        self._row = 0
        self._next_due = self._clock()
        self.active_changed.emit(True)

    def _stop(self) -> None:
        if not self._active:
            return
        self._active = False
        self._row = 0
        self.active_changed.emit(False)
