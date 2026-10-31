"""
Prototype for the wired-only SM809 (04d9:a09f) -- builds and sends the same
"full push" the official app sends every time a setting changes.

EVERYTHING HERE COMES FROM A USBPcap CAPTURE OF THE OFFICIAL APP. It has only
been tested offline (test/test_wired_sequence.py rebuilds a captured cycle
byte-for-byte). Sending it to a real mouse is the experiment.

Sequence per push (packet kinds: F = 8-byte scrambled feature report on
interface 2, B = 32-byte plain output block, G = read the reply):
  F 83 query -> G reply -> F 03 (reply echoed) -> F 02 mode -> F 01 polling ->
  F 0B dpi stage -> F 0C FF -> F 0D lighting -> F 10 00 18 + B -> F 10 01 18 + B ->
  F 11 08 08 + B -> F 12 01..04 40 each followed by two B -> F 08 AA CC EE

Fields verified by single-variable changes in the capture:
  01 = polling   08/04/02/01  (Hz labels 125/250/500/1000 come from the app code)
  02 = mode      01 office / 02 game  (capture + .pbin flag; game mode untested)
  0B = ACTIVE DPI stage, 1..8. Evidence: the profile byte at +0x84 (0-based active stage)
       is 1 in Profile14 and the app sent 0B 02; the profile's separate byte at +0x139
       (the number of DPI codes, 8) is what goes into the `11 08 08` header instead.
  0D = lighting  mode 0..11, two parameter bytes
Everything else (palettes, DPI table, button tables, 0C, 03) is replayed
exactly as captured from Jayden's "Profile14" -- so a push also restores that
button layout / DPI table / palette.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sm809wired import protocol as W

KEY = W.key_from_password("FB1570")

# ---- captured, replayed verbatim -------------------------------------------
PALETTE_A = bytes.fromhex(
    "ff000000ff000000ffffff00ff00ff00ffffff8000ffffff0000000000000000")
PALETTE_B = bytes.fromhex(
    "ff000000ff000000ffff00ffffff0000ffffff5300ffffff0000000000000000")
DPI_TABLE = bytes.fromhex(
    "0b121b26394c8f88000000000000000000000000000000000000000000000000")
TABLE_1_LO = bytes.fromhex(
    "0100f0000100f1000100f20007000100070002000008070000001f0000002000")
TABLE_1_HI = bytes.fromhex(
    "0100f40000002200000023000100f30000002400000025000af0020003009401")
TABLE_2_LO = bytes.fromhex(
    "0b000000050003000b0000000800010000000000000000000000000000000000")
TABLE_2_HI = bytes.fromhex(
    "0000000000000000000000000000000000000000000000000400010004000200")
TABLE_3_LO = bytes.fromhex(
    "0100f0000100f1000100f20007000100070002000008070000001f0000002000")
TABLE_3_HI = bytes.fromhex(
    "0100f40000002200000023000100f30000002400000025000af0020003009401")
TABLE_4_LO = bytes.fromhex(
    "0b000000050003000b0000000800010000000000000000000000000000000000")
TABLE_4_HI = bytes.fromhex(
    "0000000000000000030083010000000000000000000000000400010004000200")

POLLING_RAW = {125: 0x08, 250: 0x04, 500: 0x02, 1000: 0x01}
MODE_RAW = {"office": 0x01, "game": 0x02}

# (a, b) parameter bytes the app sent with each lighting mode in the capture.
LIGHT_DEFAULTS = {
    0x00: (0x00, 0x00), 0x01: (0xFF, 0x02), 0x02: (0x03, 0x02), 0x03: (0x03, 0xFF),
    0x04: (0x03, 0xFF), 0x05: (0xFF, 0x02), 0x06: (0x02, 0x02), 0x07: (0x02, 0x02),
    0x08: (0xFF, 0x01), 0x09: (0xFF, 0x12), 0x0A: (0xFF, 0x01), 0x0B: (0xFF, 0x02),
}

BASELINE_REPLY = bytes.fromhex("8302 0ff2 4000 0000".replace(" ", ""))  # what the mouse answered to 83

PACE_CMD = 0.032     # the app waits ~32 ms after each command packet
PACE_BLOCK = 0.016   # ~16 ms between 32-byte blocks


class Settings:
    def __init__(self, polling=1000, dpi_stage=2, mode="office", light=(0x01, 0x00, 0x00)):
        if polling not in POLLING_RAW:
            raise ValueError(f"polling must be one of {sorted(POLLING_RAW)}")
        if not 1 <= dpi_stage <= 8:
            raise ValueError("dpi_stage must be 1..8")
        if mode not in MODE_RAW:
            raise ValueError("mode must be office or game")
        lm, la, lb = light
        if not 0 <= lm <= 0x0B:
            raise ValueError("light mode must be 0..11")
        da, db = LIGHT_DEFAULTS[lm]
        self.polling, self.dpi_stage, self.mode = polling, dpi_stage, mode
        self.light = (lm, da if la is None else la, db if lb is None else lb)

    def describe(self):
        lm, a, b = self.light
        return (f"polling {self.polling} Hz (raw {POLLING_RAW[self.polling]:02X}), "
                f"DPI stage {self.dpi_stage}, mode {self.mode}, light {lm} (a={a:02X}, b={b:02X})")


def build_sequence(s: Settings, reply: bytes = BASELINE_REPLY):
    """Return the push as a list of (kind, bytes). F = *plain* 8-byte packet to be
    scrambled, B = 32-byte block, G = read one reply (bytes empty)."""
    def f(cmd, *data):
        return ("F", W.build_packet(cmd, bytes(data)))

    lm, la, lb = s.light
    seq = [
        f(0x83),
        ("G", b""),
        # the official app writes the settings page back with byte 4 forced to 0x40
        f(0x03, *reply[1:4], 0x40, *reply[5:7]),
        f(0x02, MODE_RAW[s.mode]),
        f(0x01, POLLING_RAW[s.polling]),
        f(0x0B, s.dpi_stage),
        f(0x0C, 0xFF),
        f(0x0D, lm, la, lb),
        f(0x10, 0x00, 0x18), ("B", PALETTE_A),
        f(0x10, 0x01, 0x18), ("B", PALETTE_B),
        f(0x11, 0x08, 0x08), ("B", DPI_TABLE),
        f(0x12, 0x01, 0x40), ("B", TABLE_1_LO), ("B", TABLE_1_HI),
        f(0x12, 0x02, 0x40), ("B", TABLE_2_LO), ("B", TABLE_2_HI),
        f(0x12, 0x03, 0x40), ("B", TABLE_3_LO), ("B", TABLE_3_HI),
        f(0x12, 0x04, 0x40), ("B", TABLE_4_LO), ("B", TABLE_4_HI),
        f(0x08, 0xAA, 0xCC, 0xEE),
    ]
    return seq


def wire_form(seq):
    """What actually goes on the wire: F packets scrambled, B blocks as-is."""
    return [(k, W.encode(b, KEY) if k == "F" else b) for k, b in seq]


def open_interface():
    import hid
    cands = [d for d in hid.enumerate(W.VID, W.PID)
             if d.get("usage_page") == W.USAGE_PAGE and d.get("usage") == W.USAGE]
    if not cands:
        raise RuntimeError("04d9:a09f interface 0xFF00/0xFF00 not found (plug in directly, close the official app)")
    h = hid.device()
    h.open_path(cands[0]["path"])
    return h


def send_feature(h, wire8):
    n = h.send_feature_report(bytes([W.REPORT_ID]) + wire8)
    if n < 0:
        raise RuntimeError(f"send_feature_report failed: {h.error()}")


def send_block(h, block32):
    n = h.write(bytes([0x00]) + block32)       # report ID 0 + 32 bytes = 33, same as the app
    if n != 33:
        raise RuntimeError(f"output write returned {n}, expected 33 ({h.error()})")


def push(h, s: Settings, log=print):
    """Send the full sequence. Aborts on the first problem (nothing is retried)."""
    seq = build_sequence(s)
    i = 0
    while i < len(seq):
        kind, data = seq[i]
        if kind == "G":
            time.sleep(0.005)
            raw = bytes(h.get_feature_report(W.REPORT_ID, W.PACKET_LEN + 1))[-8:]
            reply = W.decode(raw, KEY)
            log(f"  reply: {reply.hex(' ')}")
            if not W.is_reply_to(0x83, reply):
                raise RuntimeError("reply to 83 query did not echo 0x83 -- stopping before any config write")
            seq = build_sequence(s, reply)          # the 03 packet now echoes the real reply
        elif kind == "F":
            send_feature(h, W.encode(data, KEY))
            time.sleep(PACE_CMD)
        else:
            send_block(h, data)
            time.sleep(PACE_BLOCK)
        i += 1
    time.sleep(0.2)
