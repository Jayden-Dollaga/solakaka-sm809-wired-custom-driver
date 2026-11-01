# sm809wired -- engine for the wired-only SM809 (04d9:a09f)

Built from USB captures of the official app, its files, and the rebuild guide.
One apply of the extracted factory profile completed on one `04d9:a09f` unit, and
a post-apply `0x83` query echoed. Other profiles and setting readback remain unverified.

| Module | What it does |
|---|---|
| `protocol.py` | 8-byte packets, checksum, the app's packet scrambling (key = `Data.ini` Password) |
| `tables.py` | DPI value -> wire code table (sensor 3311), taken from the exe |
| `actions.py` | button action code -> 4-byte entry (the app's 61-record descriptor table) |
| `profile.py` | reads `profile.bin` / `.pbin` records and `Data.ini [BUTTON]` (read-only) |
| `apply.py` | builds the full apply sequence for a profile (the app's Apply routine) |
| `device.py` | sends it (feature reports + output blocks) with the app's timing |

Try it (dry run unless `--apply`): `python tools/wired_apply.py --install "<official app folder>" --list`

## Verified (byte-for-byte against captures, `tests/test_wired_engine.py`)
- A complete 27-step apply cycle for Profile14 in Office mode and in Game mode: command packets,
  both colour palettes, the DPI block, and all four button pages.
- All 12 light modes at the profile's stored values; DPI codes for all eight stages;
  all 16 button entries incl. six keyboard keys and the fire key.

## Not verified / not implemented
- Profiles beyond the single factory-profile apply above, and independent readback
  of settings after a write.
- Macro buttons (actions 0x16, 0x39, 0x79) and the 0x13 macro pages: refuse to build.
- Lighting parameter values away from the captured ones (extrapolated).
- Other sensors' DPI packings; the optional 04 / 07 packets (only sent when `Distance != 0`).
- Where the shortcut *modifier* is stored for custom keys (all six captured keys have none).
- Windows pointer settings the official app also changes (mouse speed, double-click, wheel).
