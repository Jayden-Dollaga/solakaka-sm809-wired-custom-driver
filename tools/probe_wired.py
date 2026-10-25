"""
First hardware check for the wired-only SM809 (04d9:a09f).

Default mode is PASSIVE: it opens the 0xFF00/0xFF00 vendor interface and only
READS one feature report (no writes). Add --query to also send the same 8-byte
query the official app sends before reading (cmd 0x83 -- from static analysis,
not yet confirmed on hardware).

It prints the raw bytes plus decoded versions (assuming the official scrambling
with the shipped Data.ini password "FB1570", and assuming no scrambling) and
whether each has a valid checksum. A valid checksum after decoding is strong
evidence the framing is right (random data passes only 1 time in 256).

Run:  python tools/probe_wired.py
      python tools/probe_wired.py --query
      python tools/probe_wired.py --password ABCDEF      (if your Data.ini differs)
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import hid
except Exception as e:  # pragma: no cover
    print(f"hidapi not available: {e}\nInstall it with: pip install hidapi")
    sys.exit(1)

from sm809wired import protocol as W


def find_interface():
    cands = [d for d in hid.enumerate(W.VID, W.PID)
             if d.get("usage_page") == W.USAGE_PAGE and d.get("usage") == W.USAGE]
    return cands[0] if cands else None


def hx(b):
    return " ".join(f"{x:02X}" for x in b)


def report(label, raw, key):
    print(f"\n{label}")
    print(f"  raw ({len(raw)} bytes): {hx(raw)}")
    wire = bytes(raw[-8:]) if len(raw) >= 8 else b""
    if len(wire) != 8:
        print("  (not 8 bytes, skipping decode)")
        return
    print(f"  as plain    : valid checksum = {W.is_valid(wire)}")
    if key:
        dec = W.decode(wire, key)
        print(f"  descrambled : {hx(dec)}   valid checksum = {W.is_valid(dec)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--query", action="store_true", help="send the 0x83 query before reading")
    ap.add_argument("--password", default="FB1570", help="Data.ini Password (6 chars enables scrambling)")
    args = ap.parse_args()

    key = W.key_from_password(args.password)
    d = find_interface()
    if not d:
        print("No 04d9:a09f interface with usage_page=0xFF00 usage=0xFF00 found.\n"
              "Plug the mouse in directly and close the official app, then retry.")
        return 1
    path = d["path"].decode(errors="replace") if isinstance(d["path"], bytes) else d["path"]
    print(f"Using {path}")

    h = hid.device()
    h.open_path(d["path"])
    try:
        if args.query:
            plain = W.build_packet(W.CMD_QUERY_83)
            wire = W.encode(plain, key) if key else plain
            print(f"\nSending query: plain {hx(plain)}  wire {hx(wire)}")
            h.send_feature_report(bytes([W.REPORT_ID]) + wire)
            time.sleep(0.06)
        try:
            raw = bytes(h.get_feature_report(W.REPORT_ID, W.PACKET_LEN + 1))
        except Exception as e:
            print(f"get_feature_report failed: {e}")
            return 2
        report("Reply" if args.query else "Passive read", raw, key)
    finally:
        h.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
