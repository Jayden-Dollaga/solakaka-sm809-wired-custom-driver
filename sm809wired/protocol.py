"""
sm809wired.protocol -- wire framing for the wired-only SM809 (Holtek 04D9:A09F).

SOURCE: static analysis of the official "SM809 mouse Software" installer
(MSDriver.dll + the app's packet builders). Nothing here has been confirmed on
real hardware yet -- see tools/probe_wired.py for the first hardware check.

What the official app does:
  * Talks over HID *feature reports* on the vendor interface whose
    usage_page == 0xFF00 and usage == 0xFF00 (not the 0xFF01 one).
  * Report ID 0, 8 data bytes (so hidapi buffers are 9 bytes: 00 + 8).
  * Packet = [cmd, d1..d6, checksum], checksum = (0xFF - sum(first 7)) & 0xFF.
  * If Data.ini has a 6-character `Password` (the shipped one is "FB1570"),
    every packet is scrambled before sending and replies are unscrambled:
    byte shuffle + XOR with the password's ASCII bytes + 64-bit rotate-left-3
    + per-byte add/sub constants. encode()/decode() below were checked against
    the real scrambler routines (0x414710 / 0x414810) by CPU emulation on 3000
    random packets with random keys: 0 mismatches.
"""

VID = 0x04D9
PID = 0xA09F
USAGE_PAGE = 0xFF00     # command interface (interface 2 on the unit we saw)
USAGE = 0xFF00
PACKET_LEN = 8
REPORT_ID = 0x00

# Only IDs actually seen in the official app are listed; meanings are unknown
# unless noted. The app sends QUERY_83 and then reads one 8-byte reply.
CMD_QUERY_83 = 0x83

# Per-output-byte constants added by the scrambler (output = rotated + const).
_CONSTS = (0x25, -0x0A, -0x1C, 0x76, 0x47, 0x54, -0x1A, 0x76)
_MASK64 = (1 << 64) - 1


def checksum(first7: bytes) -> int:
    return (0xFF - sum(first7)) & 0xFF


def build_packet(cmd: int, data: bytes = b"") -> bytes:
    """Plain (unscrambled) 8-byte packet: [cmd, data padded to 6, checksum]."""
    if len(data) > 6:
        raise ValueError("at most 6 data bytes")
    body = bytes([cmd & 0xFF]) + bytes(data) + bytes(6 - len(data))
    return body + bytes([checksum(body)])


def is_valid(packet: bytes) -> bool:
    return len(packet) == PACKET_LEN and packet[7] == checksum(packet[:7])


def key_from_password(password: str):
    """The app only enables scrambling when the Data.ini Password is exactly 6
    characters; the key is those characters' low bytes. Returns None otherwise."""
    if len(password) != 6:
        return None
    return bytes(ord(c) & 0xFF for c in password)


def encode(packet: bytes, key: bytes) -> bytes:
    """Scramble a plain packet for the wire (official routine 0x414710)."""
    if len(packet) != PACKET_LEN or len(key) != 6:
        raise ValueError("need 8-byte packet and 6-byte key")
    p = packet
    r = [p[5], p[4], p[7], p[6], p[1], p[0], p[3], p[2]]
    for i in range(1, 7):
        r[i] ^= key[i - 1]
    big = int.from_bytes(bytes(r), "big")
    t = (((big << 3) | (big >> 61)) & _MASK64).to_bytes(8, "big")
    return bytes((t[i] + _CONSTS[i]) & 0xFF for i in range(8))


def decode(wire: bytes, key: bytes) -> bytes:
    """Inverse of encode() (official routine 0x414810)."""
    if len(wire) != PACKET_LEN or len(key) != 6:
        raise ValueError("need 8-byte packet and 6-byte key")
    t = bytes((wire[i] - _CONSTS[i]) & 0xFF for i in range(8))
    big = int.from_bytes(t, "big")
    r = list(((((big >> 3) | (big << 61)) & _MASK64)).to_bytes(8, "big"))
    for i in range(1, 7):
        r[i] ^= key[i - 1]
    p = [0] * 8
    p[5], p[4], p[7], p[6], p[1], p[0], p[3], p[2] = r
    return bytes(p)
