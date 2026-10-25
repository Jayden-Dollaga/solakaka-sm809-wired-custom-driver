"""Offline tests for sm809wired.protocol (no hardware).  python tests/test_wired_protocol.py"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sm809wired import protocol as W

passed = failed = 0


def check(name, ok):
    global passed, failed
    print(("  PASS  " if ok else "  FAIL  ") + name)
    passed += ok
    failed += (not ok)


KEY = W.key_from_password("FB1570")
check("key is ASCII of the 6-char password", KEY == b"FB1570")
check("non-6-char password disables scrambling", W.key_from_password("abc") is None)

q = W.build_packet(W.CMD_QUERY_83)
check("0x83 query packet = 83 00 00 00 00 00 00 7c", q.hex(" ") == "83 00 00 00 00 00 00 7c")
check("checksum validates", W.is_valid(q) and not W.is_valid(q[:7] + b"\x00"))

# Known-answer vector: produced by emulating the official app's own scrambler
# routine (0x414710) with key "FB1570" -- not by this module.
check("known-answer: encode(query, FB1570)",
      W.encode(q, KEY).hex(" ") == "27 27 d5 ff f4 f5 66 76")
check("known-answer: decode back", W.decode(bytes.fromhex("2727d5fff4f56676"), KEY) == q)

rnd = random.Random(1)
ok = True
for _ in range(2000):
    p = bytes(rnd.randrange(256) for _ in range(8))
    k = bytes(rnd.randrange(256) for _ in range(6))
    ok &= W.decode(W.encode(p, k), k) == p
check("encode/decode round-trip (2000 random)", ok)

print(f"\n{passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
