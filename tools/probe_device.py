"""
Read-only HID probe for SOLAKAKA SM809 variants (e.g. the wired-only edition).

Lists every HID interface that looks like the mouse, shows whether it exposes
the usage_page 0x0A vendor collection the driver uses for commands, and prints
the exact SM809_WIRED_IDS value to use. It never writes to the mouse.

Run:  python tools/probe_device.py            (enumerate only)
      python tools/probe_device.py --all      (list every HID device)
      python tools/probe_device.py --read     (also read feature report 5,
                                               the same read the driver does on open)
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import hid
except Exception as e:  # pragma: no cover
    print(f"hidapi not available: {e}\nInstall it with: pip install hidapi")
    sys.exit(1)

from sm809pro import protocol as P


def looks_like_mouse(d):
    text = " ".join(str(d.get(k) or "") for k in ("product_string", "manufacturer_string")).lower()
    return (d.get("vendor_id") == P.VID
            or (d.get("vendor_id"), d.get("product_id")) in P.EXTRA_WIRED_IDS
            or "sm809" in text or "solakaka" in text)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--all", action="store_true", help="list every HID device, not just likely matches")
    ap.add_argument("--read", action="store_true", help="read feature report 5 from each vendor interface")
    args = ap.parse_args()

    devs = [d for d in hid.enumerate(0, 0) if args.all or looks_like_mouse(d)]
    if not devs:
        print("No matching HID devices found. Plug the mouse in directly (no hub) and retry, "
              "or run with --all.")
        return 1

    groups = {}
    for d in devs:
        groups.setdefault((d["vendor_id"], d["product_id"]), []).append(d)

    for (vid, pid), items in sorted(groups.items()):
        first = items[0]
        vendor_cols = [d for d in items if d.get("usage_page") == 0x000A]
        print(f"\n=== {vid:04x}:{pid:04x}  {first.get('manufacturer_string') or '?'} / "
              f"{first.get('product_string') or '?'} ===")
        print(f"  known as: {P.connection_for(vid, pid)}   "
              f"command interface (usage_page 0x0A): {'YES' if vendor_cols else 'NO'} "
              f"({len(vendor_cols)} collection(s); status push needs 2)")
        for d in sorted(items, key=lambda x: str(x.get("path"))):
            path = d.get("path", b"")
            path = path.decode(errors="replace") if isinstance(path, bytes) else str(path)
            print(f"  - iface {d.get('interface_number')}  usage_page=0x{d.get('usage_page', 0):04X} "
                  f"usage=0x{d.get('usage', 0):04X}  {path}")
            if args.read and d.get("usage_page") == 0x000A:
                try:
                    h = hid.device()
                    h.open_path(d["path"])
                    raw = bytes(h.get_feature_report(P.REPORT_ID_STATUS_FEAT, 32))
                    h.close()
                    print(f"      report 5: {P.hexstr(raw)}   ascii: "
                          f"{''.join(chr(b) if 32 <= b < 127 else '.' for b in raw)}")
                except Exception as e:
                    print(f"      report 5 read failed: {e}")
        if (vid, pid) not in {(P.VID, P.PID_WIRED), (P.VID, P.PID_WIRELESS)} and vendor_cols:
            print(f"  -> to treat this as the wired mouse:  "
                  f"set SM809_WIRED_IDS={vid:04x}:{pid:04x}      (PowerShell: $env:SM809_WIRED_IDS=\"{vid:04x}:{pid:04x}\")")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
