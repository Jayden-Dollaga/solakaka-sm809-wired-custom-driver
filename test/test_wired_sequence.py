"""
Offline test: rebuild the first apply-cycle the official app sent (taken from the
user's USBPcap capture) and compare byte-for-byte.  python test/test_wired_sequence.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wired_proto as P
from sm809wired import protocol as W

# (kind, hex) as captured: F = scrambled 8-byte feature report, B = 32-byte block,
# G = read of the reply.  Packet numbers 19025..19153 of testmouse_all_buttons_record.pcapng.
CAPTURED_CYCLE = [
    ("F", "2727d5fff4f56676"),
    ("G", ""),
    ("F", "252dbdff00faf6ee"),
    ("F", "272bd5ffe8fd6676"),
    ("F", "272b85ff30056676"),
    ("F", "272b65ff00356676"),
    ("F", "272b9504982d6676"),
    ("F", "272b55ffd02a5e8e"),
    ("F", "272a8dfff08d6636"),
    ("B", "ff000000ff000000ffffff00ff00ff00ffffff8000ffffff0000000000000000"),
    ("F", "272a85ffe88d6636"),
    ("B", "ff000000ff000000ffff00ffffff0000ffffff5300ffffff0000000000000000"),
    ("F", "272ac5ff308566b6"),
    ("B", "0b121b26394c8f88000000000000000000000000000000000000000000000000"),
    ("F", "272d55ffe87d6876"),
    ("B", "0100f0000100f1000100f20007000100070002000008070000001f0000002000"),
    ("B", "0100f40000002200000023000100f30000002400000025000af0020003009401"),
    ("F", "272d2dff007d6876"),
    ("B", "0b000000050003000b0000000800010000000000000000000000000000000000"),
    ("B", "0000000000000000000000000000000000000000000000000400010004000200"),
    ("F", "272d25fff87d6876"),
    ("B", "0100f0000100f1000100f20007000100070002000008070000001f0000002000"),
    ("B", "0100f40000002200000023000100f30000002400000025000af0020003009401"),
    ("F", "272d3dffd07d6876"),
    ("B", "0b000000050003000b0000000800010000000000000000000000000000000000"),
    ("B", "0000000000000000030083010000000000000000000000000400010004000200"),
    ("F", "272c6d024052dcd6"),
]

passed = failed = 0


def check(name, ok):
    global passed, failed
    print(("  PASS  " if ok else "  FAIL  ") + name)
    passed += ok
    failed += (not ok)


# In that cycle the user had: polling 125 Hz (raw 08), 2 DPI levels, office mode,
# lighting mode 4 with a=03 b=FF.
s = P.Settings(polling=125, dpi_levels=2, mode="office", light=(4, 0x03, 0xFF))
built = [(k, w.hex()) for k, w in P.wire_form(P.build_sequence(s))]
check("same number of steps as the captured cycle", len(built) == len(CAPTURED_CYCLE))
check("every step matches the capture byte-for-byte (G entries compare as empty)",
      [(k, h if k != "G" else "") for k, h in built] ==
      [(k, h if k != "G" else "") for k, h in CAPTURED_CYCLE])
check("all command packets carry valid checksums once descrambled",
      all(W.is_valid(W.decode(bytes.fromhex(h), P.KEY)) for k, h in built if k == "F"))

s2 = P.Settings(polling=500, dpi_levels=5, mode="game", light=(6, None, None))
seq2 = P.build_sequence(s2)
cmds = {p[0]: p for k, p in seq2 if k == "F"}
check("polling 500 -> cmd 01 = 02", cmds[0x01][1] == 0x02)
check("5 DPI levels -> cmd 0B = 05", cmds[0x0B][1] == 0x05)
check("game mode -> cmd 02 = 02", cmds[0x02][1] == 0x02)
check("light 6 uses the app's default params 02 02", cmds[0x0D][1:4] == bytes([6, 2, 2]))

for bad in (dict(polling=100), dict(dpi_levels=0), dict(dpi_levels=9), dict(mode="x"), dict(light=(12, None, None))):
    try:
        P.Settings(**bad)
        check(f"rejects {bad}", False)
    except ValueError:
        check(f"rejects {bad}", True)

# ---- full send path against a fake device (no hardware) ---------------------
class FakeHid:
    def __init__(self, reply):
        self.reply = reply
        self.log = []

    def send_feature_report(self, data):
        self.log.append(("F", bytes(data)))
        return len(data)

    def write(self, data):
        self.log.append(("B", bytes(data)))
        return len(data)

    def get_feature_report(self, rid, n):
        self.log.append(("G", b""))
        return list(bytes([0]) + W.encode(self.reply, P.KEY))

    def error(self):
        return "fake"


P.time.sleep = lambda x: None          # do not actually wait in tests
real_reply = W.build_packet(0x83, bytes([0x02, 0x0F, 0xFA, 0x40, 0x00, 0x00]))   # pretend a different device state
fake = FakeHid(real_reply)
P.push(fake, P.Settings(polling=1000, dpi_levels=3, mode="office", light=(5, None, None)), log=lambda *_: None)
fl = [e for e in fake.log if e[0] in ("F", "B")]
check("fake device got 15 command packets and 11 blocks",
      sum(k == "F" for k, _ in fl) == 15 and sum(k == "B" for k, _ in fl) == 11)
check("feature reports are 9 bytes (report ID 0 + 8) and blocks 33 bytes (ID 0 + 32)",
      all(len(d) == 9 for k, d in fl if k == "F") and all(len(d) == 33 for k, d in fl if k == "B"))
third = W.decode(fl[1][1][1:], P.KEY)            # 83, then the 03 packet
check("the 03 packet carries the device's real reply bytes 1-3, with byte 4 forced to 0x40 like the app",
      third[:7] == bytes([0x03]) + real_reply[1:4] + bytes([0x40]) + real_reply[5:7])

bad = FakeHid(W.build_packet(0x12))               # reply that does not echo 83
try:
    P.push(bad, P.Settings())
    check("aborts before writing config if the reply is not an echo of 83", False)
except RuntimeError:
    check("aborts before writing config if the reply is not an echo of 83",
          sum(k in ("F", "B") for k, _ in bad.log) == 1)      # only the 83 query went out

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
