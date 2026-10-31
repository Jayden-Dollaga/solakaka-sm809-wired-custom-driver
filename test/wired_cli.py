"""
Hardware experiment CLI for the wired-only SM809 (04d9:a09f).

DEFAULT IS A DRY RUN: it prints exactly what would be sent and touches nothing.
Add --apply to really send (asks for confirmation unless --yes).

Examples
  python test/wired_cli.py read                      read-only 0x83 query
  python test/wired_cli.py set --polling 500         dry run
  python test/wired_cli.py set --polling 500 --apply
  python test/wired_cli.py set --dpi-levels 3 --apply     (number of DPI levels in use, 1..8)
  python test/wired_cli.py set --light 6 --apply
  python test/wired_cli.py set --mode game --apply   (button layout changes! use --mode office to go back)

Every `set` is a FULL push like the official app does, so settings you do not
pass fall back to: polling 1000, DPI levels 2, mode office, light 1 / Standard (params 00 00).
It also rewrites the button tables, DPI table and light palettes with the ones
captured from the official app (Profile14).
Close the official app first.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wired_proto as P
from sm809wired import protocol as W


def hx(b):
    return " ".join(f"{x:02X}" for x in b)


def cmd_read(args):
    h = P.open_interface()
    try:
        plain = W.build_packet(W.CMD_QUERY_83)
        P.send_feature(h, W.encode(plain, P.KEY))
        import time
        time.sleep(0.06)
        raw = bytes(h.get_feature_report(W.REPORT_ID, W.PACKET_LEN + 1))[-8:]
        dec = W.decode(raw, P.KEY)
        print(f"reply: {hx(dec)}   echoes 0x83: {W.is_reply_to(0x83, dec)}")
    finally:
        h.close()
    return 0


def cmd_set(args):
    # default = the lighting in the user's own proxy log (Standard, params 00 00)
    light = (0x01, 0x00, 0x00) if args.light is None else (args.light, args.light_a, args.light_b)
    try:
        s = P.Settings(polling=args.polling, dpi_levels=args.dpi_levels, mode=args.mode, light=light)
    except ValueError as e:
        print(f"error: {e}")
        return 2
    seq = P.build_sequence(s)
    wire = P.wire_form(seq)
    print("Settings:", s.describe())
    print(f"Sequence: {sum(k=='F' for k,_ in seq)} command packets, "
          f"{sum(k=='B' for k,_ in seq)} data blocks, 1 read\n")
    for (k, plain), (_, w) in zip(seq, wire):
        if k == "F":
            print(f"  F plain {hx(plain)}  ->  wire {hx(w)}")
        elif k == "B":
            print(f"  B block {hx(plain[:16])} ...")
        else:
            print("  G read reply (the 03 packet will echo the real reply)")
    if not args.apply:
        print("\nDRY RUN -- nothing sent. Add --apply to send.")
        return 0
    if args.mode == "game":
        print("\nNOTE: game mode changes which buttons work on the mouse. Switch back with --mode office.")
    if not args.yes:
        if input("\nSend this to the mouse? [y/N] ").strip().lower() != "y":
            print("aborted")
            return 1
    h = P.open_interface()
    try:
        P.push(h, s)
    finally:
        h.close()
    print("done. Check the mouse. If something looks wrong, re-apply in the official app.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("read", help="send the 0x83 query and show the decoded reply (no config written)")
    st = sub.add_parser("set", help="build (and optionally send) a full push")
    st.add_argument("--polling", type=int, default=1000, help="125/250/500/1000")
    st.add_argument("--dpi-levels", type=int, default=2, help="number of DPI levels in use, 1..8")
    st.add_argument("--mode", choices=["office", "game"], default="office")
    st.add_argument("--light", type=lambda x: int(x, 0), default=None, help="lighting mode 0..11")
    st.add_argument("--light-a", type=lambda x: int(x, 0), default=None, help="first parameter byte (default per mode)")
    st.add_argument("--light-b", type=lambda x: int(x, 0), default=None, help="second parameter byte (default per mode)")
    st.add_argument("--apply", action="store_true", help="actually send (default is a dry run)")
    st.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    args = ap.parse_args()
    return cmd_read(args) if args.cmd == "read" else cmd_set(args)


if __name__ == "__main__":
    sys.exit(main())
