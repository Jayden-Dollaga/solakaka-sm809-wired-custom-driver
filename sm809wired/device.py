"""
sm809wired.device -- send a built apply sequence to the wired SM809 (04d9:a09f).

Feature packets go out as 9-byte HID feature reports (report ID 0 + 8) on the
usage_page 0xFF00 / usage 0xFF00 interface; the 32-byte blocks are 33-byte output
writes (report ID 0 + 32). Pacing follows the official app (about 32 ms after a command
packet, 16 ms between blocks).

One factory-profile apply completed on one 04d9:a09f unit, and a post-apply 0x83
query echoed. Other profiles and setting readback remain unverified. push() stops
at the first problem and never retries.
"""
import time

from . import protocol as W
from .apply import build_apply, to_wire

PACE_CMD = 0.032
PACE_BLOCK = 0.016


def find_interface():
    """Return the wired-only command-interface descriptor without opening it."""
    try:
        import hid
    except Exception:
        return None
    cands = [d for d in hid.enumerate(W.VID, W.PID)
             if d.get("usage_page") == W.USAGE_PAGE and d.get("usage") == W.USAGE]
    return cands[0] if cands else None


def open_interface():
    import hid
    interface = find_interface()
    if interface is None:
        raise RuntimeError("04d9:a09f interface 0xFF00/0xFF00 not found "
                           "(plug in directly and close the official app)")
    h = hid.device()
    h.open_path(interface["path"])
    return h


def query_reply(h, key):
    """Send the 0x83 query and return the descrambled 8-byte reply."""
    h.send_feature_report(bytes([W.REPORT_ID]) + W.encode(W.build_packet(0x83), key))
    time.sleep(0.005)
    raw = bytes(h.get_feature_report(W.REPORT_ID, W.PACKET_LEN + 1))[-8:]
    return W.decode(raw, key)


def push_profile(h, profile, button_ini, key, log=print):
    """Query the mouse, then send the full apply sequence for `profile`."""
    reply = query_reply(h, key)
    log(f"  reply: {reply.hex(' ')}")
    if not W.is_reply_to(0x83, reply):
        raise RuntimeError("reply to the 83 query did not echo 0x83 -- stopping before any config write")
    wire = to_wire(build_apply(profile, button_ini, reply), key)
    # wire[0] is the 83 query we already sent, wire[1] the reply marker
    for kind, data in wire[2:]:
        if kind == "F":
            n = h.send_feature_report(bytes([W.REPORT_ID]) + data)
            if n < 0:
                raise RuntimeError(f"send_feature_report failed: {h.error()}")
            time.sleep(PACE_CMD)
        else:
            n = h.write(bytes([0x00]) + data)
            if n != 33:
                raise RuntimeError(f"output write returned {n}, expected 33 ({h.error()})")
            time.sleep(PACE_BLOCK)
    time.sleep(0.2)
