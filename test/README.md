# test/ -- wired SM809 hardware experiments

Prototype for the wired-only SM809 (`04d9:a09f`), built from a USBPcap capture of the official app.
Only the offline test has been run so far; talking to a real mouse is the experiment.

    python test/test_wired_sequence.py          # offline, no hardware
    python test/wired_cli.py read               # read-only query
    python test/wired_cli.py set --polling 500  # DRY RUN (prints the packets)
    python test/wired_cli.py set --polling 500 --apply

Close the official app first. `set` is a full push (like the app): unspecified settings fall back
to defaults, and the button/DPI/palette tables captured from Profile14 are rewritten.
Revert anything by re-applying your profile in the official app.

Suggested order: `read` -> `set --polling 1000 --apply` (same as the likely current value)
-> `set --dpi-stage 3 --apply` -> `set --light 6 --apply`. Report what the mouse did each time.

## GUI launcher

    python test\run_app.py            # DRY RUN: the normal GUI opens, nothing is sent
    python test\run_app.py --apply    # live: polling rate + active DPI stage only

It swaps the GUI's device layer for `wired_adapter.py`. Profiles/macros for this launcher live in
`test/_gui_data/` (your real `config/` is not touched). Lighting, buttons, macros, LOD, power and
sensor flags are inert here and the console says so.

Note: cmd `0B` is the ACTIVE DPI stage (1..8). Profile byte +0x84 (0-based) feeds it; the number of DPI codes (+0x139) goes in the `11 08 08` header.
