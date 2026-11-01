"""
Offline tests for the ground-up wired-SM809 engine (no hardware, no private files).

  python tests/test_wired_engine.py

The two end-to-end tests rebuild a COMPLETE apply cycle (27 steps: every command packet,
palette, DPI table and all four button pages) from nothing but a profile record and the
Data.ini button list, and compare it byte-for-byte with a cycle captured from the official
app with USBPcap -- one in Office mode, one in Game mode.
"""
import base64
import os
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import wired_fixtures as F
from sm809wired import actions, protocol as W
from sm809wired.apply import build_apply, build_button_table, light_params, to_wire
from sm809wired.profile import N_SLOTS, RECORD_SIZE, parse_button_ini, parse_record
from sm809wired.tables import DPI_CODES, dpi_code, dpi_index

KEY = W.key_from_password("FB1570")
passed = failed = 0


def check(name, ok):
    global passed, failed
    print(("  PASS  " if ok else "  FAIL  ") + name)
    passed += bool(ok)
    failed += (not ok)


def load(b64):
    return parse_record(zlib.decompress(base64.b64decode(b64)))


office = load(F.PROFILE_OFFICE_B64)
game = load(F.PROFILE_GAME_B64)
ini = parse_button_ini(F.BUTTON_INI)
REPLY = bytes.fromhex("83020ff240000000")     # what the mouse answered to the 0x83 query

print("profile parsing")
check("record size is 0x1CC50 and 64 slots fill it exactly", RECORD_SIZE == 0x150 + 64 * 0x72C)
check("office profile fields", (office.name, office.polling_index, office.active_stage, office.light_mode,
                                 office.game_mode, office.stage_count) == ("Profile14", 3, 1, 4, False, 8))
check("game profile fields", (game.light_mode, game.game_mode) == (3, True))
check("DPI values", office.dpi_values == (10, 16, 24, 32, 48, 64, 120, 228))
check("Data.ini has 64 button entries", len(ini) == N_SLOTS)
try:
    parse_button_ini("[BUTTON]\n1=01,00,F0,00,1\n")
    check("incomplete Data.ini is rejected", False)
except ValueError:
    check("incomplete Data.ini is rejected", True)

print("DPI codes")
check("profile values -> wire codes 0B 12 1B 26 39 4C 8F 88",
      bytes(dpi_code(v) for v in office.dpi_values).hex() == "0b121b26394c8f88")
check("values above 120 use value//2 (228 -> index 114)", dpi_index(228) == 114 and dpi_index(120) == 120)
check("table has 121 entries", len(DPI_CODES) == 121)
for bad in (0, 242):
    try:
        dpi_code(bad)
        check(f"DPI value {bad} rejected", False)
    except ValueError:
        check(f"DPI value {bad} rejected", True)

print("button entries")
office_page1 = bytes.fromhex("0100f0000100f1000100f20007000100070002000008070000001f0000002000"
                             "0100f40000002200000023000100f30000002400000025000af0020003009401")
check("all 16 Office entries rebuilt from the profile", build_button_table(office, ini)[:64] == office_page1)
game_page = build_button_table(game, ini)[128:192]
check("Game page: Left/Right/Middle then 13 empty entries",
      game_page[:12] == bytes.fromhex("0100f0000100f1000100f200") and game_page[12:] == bytes(52))
for act in actions.MACRO_ACTIONS:
    try:
        actions.slot_entry(act)
        check(f"macro action 0x{act:02X} refuses to build", False)
    except NotImplementedError:
        check(f"macro action 0x{act:02X} refuses to build", True)
check("unknown action codes give 00 00 00 00", actions.slot_entry(0xFF) == bytes(4))

print("lighting parameters (profile values brightness=255 length=3 frequency=1 direction=2)")
captured = {0: (0, 0), 1: (0xFF, 2), 2: (3, 2), 3: (3, 0xFF), 4: (3, 0xFF), 5: (0xFF, 2),
            6: (2, 2), 7: (2, 2), 8: (0xFF, 1), 9: (0xFF, 0x12), 10: (0xFF, 1), 11: (0xFF, 2)}
check("all 12 light modes match the packets the official app sent",
      all(light_params(m, 255, 3, 1, 2) == v for m, v in captured.items()))
check("mode 4 with length 0/4 and brightness 0 (captured variants)",
      light_params(4, 0, 0, 1, 2) == (0, 0) and light_params(4, 255, 4, 1, 2) == (4, 255))


def compare(profile, expected):
    wire = to_wire(build_apply(profile, ini, REPLY), KEY)
    if len(wire) != len(expected):
        return False, f"{len(wire)} steps vs {len(expected)} captured"
    for i, ((k1, b1), (k2, h2)) in enumerate(zip(wire, expected)):
        if k1 != k2 or (k1 != "G" and b1.hex() != h2):
            return False, f"step {i} differs"
    return True, ""


print("end to end: rebuild a whole captured cycle")
ok, why = compare(office, F.EXPECTED_OFFICE)
check(f"Office profile -> all {len(F.EXPECTED_OFFICE)} steps identical to the capture {why}", ok)
ok, why = compare(game, F.EXPECTED_GAME)
check(f"Game profile   -> all {len(F.EXPECTED_GAME)} steps identical to the capture {why}", ok)
check("office sends 02 01, game sends 02 02",
      W.decode(to_wire(build_apply(office, ini, REPLY), KEY)[3][1], KEY)[1] == 1 and
      W.decode(to_wire(build_apply(game, ini, REPLY), KEY)[3][1], KEY)[1] == 2)
try:
    build_apply(office, ini, bytes(8))
    check("a reply that does not echo 0x83 is refused", False)
except ValueError:
    check("a reply that does not echo 0x83 is refused", True)

print("device sender with a fake HID device")
from sm809wired import device


class Fake:
    def __init__(self, reply):
        self.reply, self.sent = reply, []

    def send_feature_report(self, d):
        self.sent.append(("F", bytes(d)))
        return len(d)

    def write(self, d):
        self.sent.append(("B", bytes(d)))
        return len(d)

    def get_feature_report(self, rid, n):
        return list(bytes([0]) + W.encode(self.reply, KEY))

    def error(self):
        return ""


device.PACE_CMD = device.PACE_BLOCK = 0
device.time.sleep = lambda s: None
fake = Fake(REPLY)
device.push_profile(fake, office, ini, KEY, log=lambda *_: None)
fl = [e for e in fake.sent]
check("sent 1 query + 15 command packets and 11 blocks",
      sum(k == "F" for k, _ in fl) == 15 and sum(k == "B" for k, _ in fl) == 11)
check("feature reports are 9 bytes, blocks 33 bytes",
      all(len(d) == 9 for k, d in fl if k == "F") and all(len(d) == 33 for k, d in fl if k == "B"))
bad = Fake(W.build_packet(0x12))
try:
    device.push_profile(bad, office, ini, KEY, log=lambda *_: None)
    check("non-echo reply stops the push before any config is written", False)
except RuntimeError:
    check("non-echo reply stops the push before any config is written", len(bad.sent) == 1)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
