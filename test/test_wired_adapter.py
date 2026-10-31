"""Offline test of the GUI adapter with a fake HID device.  python test/test_wired_adapter.py"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wired_adapter as A
import wired_proto as P
from sm809wired import protocol as W

passed = failed = 0


def check(name, ok):
    global passed, failed
    print(("  PASS  " if ok else "  FAIL  ") + name)
    passed += ok
    failed += (not ok)


class FakeHid:
    def __init__(self):
        self.sent = []

    def send_feature_report(self, d):
        self.sent.append(("F", bytes(d)))
        return len(d)

    def write(self, d):
        self.sent.append(("B", bytes(d)))
        return len(d)

    def get_feature_report(self, rid, n):
        return list(bytes([0]) + W.encode(W.build_packet(0x83, bytes([2, 0x0F, 0xF2, 0x40, 0, 0])), P.KEY))

    def close(self):
        pass

    def error(self):
        return ""


P.time.sleep = lambda x: None
P.open_interface = lambda: FakeHid()
A.log = lambda *_: None

d = A.SM809Wired()
check("not open before open()", not d.is_open)
check("open() succeeds with the fake device", d.open() and d.is_open and d.connection == "wired")
check("keepalive is read-only and True", d.keepalive_poll() is True and d._h.sent == [])

A.APPLY = False
check("dry run: polling call returns True", d.set_polling_rate(500) is True)
check("dry run: NOTHING was sent", d._h.sent == [])

A.APPLY = True
check("live: polling call returns True", d.set_polling_rate(500) is True)
sent = d._h.sent
check("live: full push went out (15 feature reports + 11 blocks)",
      sum(k == "F" for k, _ in sent) == 15 and sum(k == "B" for k, _ in sent) == 11)
polling = [W.decode(b[1:], P.KEY) for k, b in sent if k == "F"]
check("live: the 01 packet carries polling 500 -> 02", [p for p in polling if p[0] == 0x01][0][1] == 0x02)

n = len(sent)
check("same settings again -> skipped, nothing new sent", d.set_polling_rate(500) is True and len(d._h.sent) == n)
d.set_dpi([800, 1600, 3200, 6000], selected=0)
b = [W.decode(x[1:], P.KEY) for k, x in d._h.sent[n:] if k == "F"]
check("4 DPI values -> 4 DPI levels (cmd 0B = 04)", [p for p in b if p[0] == 0x0B][0][1] == 0x04)
check("set_active_dpi is unsupported (the mouse picks the active level)", d.set_active_dpi([800], 0) is False)

n = len(d._h.sent)
check("unsupported calls return False and send nothing",
      d.set_lighting(2, color=(0, 0, 255)) is False and d.set_keys({}) is False
      and d.factory_reset() is False and len(d._h.sent) == n)
check("bad polling value rejected", d.set_polling_rate(333) is False and len(d._h.sent) == n)

d.close()
check("closed", not d.is_open and d.keepalive_poll() is False)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
