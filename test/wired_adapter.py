"""
GUI adapter: lets the existing SM809 Pro GUI drive the wired-only SM809 (04d9:a09f)
through the prototype in wired_proto.py.

The GUI's controller only talks to a duck-typed device object (open/close/
keepalive_poll/set_*), so this class stands in for sm809pro.SM809Pro. Only what
the capture of the official app proved is implemented:

  set_polling_rate(hz)           -> cmd 01 (125/250/500/1000)
  set_dpi(levels, ...)           -> cmd 0B, sets the NUMBER of DPI levels in use (1..8)
                                    from len(levels); the DPI *values* are ignored for now
Everything else the GUI can ask for (lighting, LOD, power, sensor flags, buttons,
macros, factory reset) returns False and sends nothing.

DRY RUN BY DEFAULT: nothing is sent to the mouse unless APPLY is True
(python test/run_app.py --apply). Every send is a FULL push like the official
app does, with unspecified fields at the defaults in wired_proto.Settings.
"""
import threading

import wired_proto as P
from sm809wired import protocol as W

APPLY = False


def log(msg):
    print(f"[wired] {msg}", flush=True)


class NullStatusListener:
    """The wired unit has no status-push interface we understand yet."""
    def __init__(self, *a, **kw):
        self._alive = None

    def start(self):
        pass

    def stop(self):
        pass


class SM809Wired:
    def __init__(self, vid=W.VID, pid=None, sensor=None):
        self.vid = W.VID
        self.pid = None
        self.connection = "wired"
        self.configurable = True
        self.interface_info = None
        self._h = None
        self._lock = threading.RLock()
        self.state = dict(polling=1000, dpi_levels=2, mode="office", light=(0x01, 0x00, 0x00))
        self._last = None

    # -- connection -----------------------------------------------------------
    @property
    def is_open(self) -> bool:
        return self._h is not None

    def open(self) -> bool:
        with self._lock:
            if self._h is not None:
                return True
            try:
                self._h = P.open_interface()
            except Exception as e:
                self._h = None
                return False
            self.pid = W.PID
            self.interface_info = {"product_string": "SM809 Wired (04d9:a09f)"}
            log(f"connected ({'LIVE: --apply' if APPLY else 'DRY RUN: nothing will be sent'})")
            return True

    def close(self):
        with self._lock:
            if self._h is not None:
                try:
                    self._h.close()
                except Exception:
                    pass
            self._h = None

    def keepalive_poll(self) -> bool:
        """Read-only. Returns False if the handle is dead so the GUI reconnects."""
        with self._lock:
            if self._h is None:
                return False
            try:
                self._h.get_feature_report(W.REPORT_ID, W.PACKET_LEN + 1)
                return True
            except Exception:
                return False

    def read_status(self):
        return None

    # -- supported ------------------------------------------------------------
    def _push(self, why):
        s = P.Settings(**self.state)
        desc = s.describe()
        with self._lock:
            if self._h is None:
                return False
            if desc == self._last:
                log(f"{why}: unchanged, skipping ({desc})")
                return True
            if not APPLY:
                log(f"{why}: DRY RUN, would push: {desc}")
                return True
            log(f"{why}: pushing: {desc}")
            P.push(self._h, s, log=log)
            self._last = desc
            log("push finished")
            return True

    def set_polling_rate(self, hz: int) -> bool:
        if hz not in P.POLLING_RAW:
            log(f"set_polling_rate({hz}): unsupported value, ignored")
            return False
        self.state["polling"] = hz
        return self._push(f"set_polling_rate({hz})")

    def set_dpi(self, dpi_levels, selected=0, colors=None) -> bool:
        n = max(1, min(8, len(dpi_levels)))
        log("set_dpi: DPI values ignored for now; setting the number of DPI levels only")
        self.state["dpi_levels"] = n
        return self._push(f"set_dpi({n} levels)")


def _unsupported(name):
    def fn(self, *a, **kw):
        log(f"{name}: not supported on the wired unit yet, ignored")
        return False
    fn.__name__ = name
    return fn


for _n in ("set_lod", "set_lighting", "set_power", "set_sensor_flags", "set_keys",
           "set_active_dpi", "set_keys_default", "apply_macro_buttons", "upload_macro", "upload_macros",
           "erase_macros", "factory_reset", "factory_restore", "set_dpi_colors",
           "send_command", "send_raw"):
    setattr(SM809Wired, _n, _unsupported(_n))
