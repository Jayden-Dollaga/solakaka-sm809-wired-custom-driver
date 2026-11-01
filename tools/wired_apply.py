r"""
Apply one of the official app's profiles to the wired SM809 -- without the official app.

Reads (never writes) the official app's files:
    <install>\Data\profile.bin   all profiles        (or a single exported .pbin)
    <install>\Data\Data.bin      selected profile index
    <install>\Data.ini           raw button slots

DRY RUN by default: prints the profile and every packet it would send.
Add --apply to send (asks to confirm unless --yes). Close the official app first.

  python tools/wired_apply.py --install "C:\Program Files (x86)\SM809 mouse Software" --list
  python tools/wired_apply.py --install "C:\...\SM809 mouse Software"                 (selected profile, dry run)
  python tools/wired_apply.py --install "C:\...\SM809 mouse Software" --index 3 --apply
  python tools/wired_apply.py --pbin Original_profile.pbin --data-ini Data.ini

Hardware testing is limited to one apply of the extracted factory profile on one
04d9:a09f unit, followed by a successful 0x83 query. Other profiles/settings have
not been read back. Apply sends the full profile, including all four button pages,
DPI table, and light colours, so it overwrites the mouse's current configuration.
Macro buttons are not supported and stop the run before anything is sent.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sm809wired import protocol as W
from sm809wired.apply import build_apply, to_wire
from sm809wired.profile import parse_button_ini, read_profiles, read_selected_index

KEY = W.key_from_password("FB1570")
BASELINE_REPLY = bytes.fromhex("83020ff240000000")   # only used for the dry-run printout


def hx(b):
    return " ".join(f"{x:02X}" for x in b)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--install", help="official app folder (contains Data\\ and Data.ini)")
    ap.add_argument("--pbin", help="a single exported profile instead of Data\\profile.bin")
    ap.add_argument("--data-ini", help="path to Data.ini (default: <install>\\Data.ini)")
    ap.add_argument("--index", type=int, help="profile index (default: the app's selected one)")
    ap.add_argument("--list", action="store_true", help="list profiles and exit")
    ap.add_argument("--apply", action="store_true", help="really send (default is a dry run)")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    a = ap.parse_args()

    if a.pbin:
        profiles = read_profiles(a.pbin)
        sel = 0
    elif a.install:
        profiles = read_profiles(os.path.join(a.install, "Data", "profile.bin"))
        sel = read_selected_index(os.path.join(a.install, "Data", "Data.bin"))
    else:
        ap.error("give --install or --pbin")
    ini_path = a.data_ini or (os.path.join(a.install, "Data.ini") if a.install else None)
    if not ini_path:
        ap.error("--data-ini is required with --pbin")

    if a.list:
        for i, p in enumerate(profiles):
            print(f"{i:2d}{' *' if i == sel else '  '} {p.name}")
        print("(* = selected in the official app)")
        return 0

    idx = sel if a.index is None else a.index
    if not 0 <= idx < len(profiles):
        print(f"error: profile index {idx} out of range 0..{len(profiles) - 1}")
        return 2
    p = profiles[idx]
    ini = parse_button_ini(open(ini_path, errors="replace").read())
    print(f"Profile {idx}: {p.name!r}  polling idx {p.polling_index}, active DPI stage {p.active_stage + 1}, "
          f"light mode {p.light_mode}, {'Game' if p.game_mode else 'Office'} mode")
    try:
        seq = build_apply(p, ini, BASELINE_REPLY)
    except NotImplementedError as e:
        print(f"\nstopped before sending anything: {e}")
        return 3
    for (k, plain), (_, wire) in zip(seq, to_wire(seq, KEY)):
        if k == "F":
            print(f"  F {hx(plain)}  ->  {hx(wire)}")
        elif k == "B":
            print(f"  B {hx(plain[:16])} ...")
        else:
            print("  G read reply")
    if not a.apply:
        print("\nDRY RUN -- nothing sent. Add --apply to send.")
        return 0
    if not a.yes and input(f"\nSend profile '{p.name}' to the mouse? [y/N] ").strip().lower() != "y":
        print("aborted")
        return 1
    from sm809wired.device import open_interface, push_profile
    h = open_interface()
    try:
        push_profile(h, p, ini, KEY)
    finally:
        h.close()
    print("done. Check the mouse; re-apply in the official app to restore if anything looks wrong.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
