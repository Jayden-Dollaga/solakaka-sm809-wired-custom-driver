# SM809 Control Center (clean-room rebuild)

A complete desktop replacement for the Solakaka SM809 wired mouse utility
(`SM809 mouse Software.exe`), rebuilt from the reverse-engineering notes in
[`../analysis/OVERVIEW.md`](../analysis/OVERVIEW.md).

The rebuild talks to the same HID interfaces, uses the same on-disk profile
format, and reproduces the original apply sequence — while fixing several
ship-build defects (see [Deviations](#deviations-and-fixes)). It keeps its own
portable data folder, so the original installation is never modified.

## Quick start

| Launcher | What it does |
| --- | --- |
| `start.bat` | Opens the app with real hardware when present (falls back to demo) |
| `start-demo.bat` | Opens the app in demo mode; no hardware access |
| `python run.py` | Same as `start.bat` |
| `python run.py --demo` | Force the simulated device |
| `python run.py --hardware` | Force the real HID transport |
| `python run.py --data-dir D:\path` | Use another portable data folder |

Requirements: Windows 10/11 and Python 3.10+ with tkinter (included in the
official python.org installer). No third-party packages are needed at runtime;
`pytest` is only required to run the test suite. Developed and tested with
Python 3.14.6 / Tk 8.6.

Typical first run: pick a profile, press **Connect**, press **Apply profile**
(or Ctrl+S). In demo mode the HID exchange is simulated and the status bar
reports the number of feature packets and 32-byte blocks that would be sent.

## Data folder

* Profiles live in `data/Data/profile.bin` (`0x1CC50` bytes × 14 records).
* `data/Data/Data.bin` stores the selected profile index.
* Macro records live in `data/Data/macro.bin` (`0x358` bytes each); gun
  records live in `data/Data/gun.bin` (`0x240` bytes each). Each profile's
  button records reference a macro/gun by index and carry their own event and
  bullet rows, matching the original layout.
* On first launch `sm809/paths.py` copies `../Data.ini` and `../Data/*.bin`
  from the original installation **once**. Everything afterwards is read and
  written inside `sm809-rebuild/data`.
* Override the location with `--data-dir` or the `SM809_DATA_DIR` environment
  variable.
* **More actions → Open data folder** opens the live folder.

Back up `data/` before experimenting; **More actions → Reload Data.ini** re-reads
`Data.ini` without restarting (use it after editing `Distance=`, `Sensor=`, or
the button defaults).

## Features

### Buttons (Ctrl+1)
* All 64 button slots, each mapped to one of the 61 actions recovered from the
  binary (Basic, Advanced, Windows, Multimedia, Browser).
* Shortcut capture (modifiers + key), Fire Click (count + interval), macro
  selection, Send Gun, DPI cycle / + / -, mode switch, light mode switch,
  sniper key, report-rate keys, and media/browser/window commands.
* Slots not marked *computed* in `Data.ini` are streamed as their raw 4-byte
  rows, exactly like the original.
* Profiles: new, duplicate, delete, rename, reset, import/export (`.pbin`),
  readable JSON export.

### Performance (Ctrl+2)
* 8 DPI stages with per-sensor limits, active-stage radio, polling rate
  (1000/500/250/125 Hz → 8/4/2/1 ms), game/office mode, lift-off distance,
  key response time, and the high-DPI mask for sensors that need it.
* Stage/rate/mode changes made on the mouse are reflected back through the
  monitor interface and persisted.

### Lighting (Ctrl+3)
* Light mode 0–11 with the parameter controls each mode actually consumes.
* Fixed RGB colour, per-stage palette, 8-colour cycling palette.
* Parameter labels are descriptive; the original resources do not name the
  effects, so no product names were invented.

### Macros (Ctrl+4)
* Record keyboard and mouse events with low-level Windows hooks
  (`WH_KEYBOARD_LL` / `WH_MOUSE_LL`), three timing modes (constant 10 ms,
  fixed delay, real timing), optional mouse-move capture.
* Edit delay/key/state per event, reorder/delete, loop count, 40-event device
  limit, upload through the `0x13` macro table.
* "Apply to all buttons using this macro" keeps every macro-bearing button in
  sync before uploading.

### Gun recoil (Ctrl+5)
* 30-row recoil table per gun button (delay, X, Y), 128-byte device block.
* Editing or renaming a table updates every profile button that references it
  before the next upload.
* **Experimental:** the shipped application builds this block but never copies
  it into the upload buffer (the Gun tab is hidden in the released build), so
  this layout is inferred from the encoder. Test with care on real hardware.

### Windows pointer settings
Applied before every profile upload, matching the original: double-click time,
pointer speed, button swap, wheel scroll lines / one-page mode.

## How the device conversation works

* Control interface: UsagePage `0xFF00`, Usage `0xFF00`; monitor interface:
  UsagePage `0xFF01`, Usage `0xFF01` (VID `04D9`, PID `A09F`).
* Feature reports: 9 bytes = report ID 0 + 8-byte packet. Bulk blocks:
  33 bytes = report ID 0 + 32 bytes. Every packet carries the checksum
  `-(1 + sum(packet[0..6])) & 0xFF`.
* With `Password=` in `Data.ini`, feature packets are obfuscated with the
  6-byte key (`FB1570` in the shipped config); replies are de-obfuscated.
  The permutation/XOR/rotate mapping mirrors `FUN_00414710` and its inverse
  `FUN_00414810` byte for byte.
* Monitor input reports start with report ID 6: `event = (b1<<8)|b2`,
  `value = b3` (`0x7F00` connect/disconnect, `0x07xx` stage, `0x05xx` rate,
  `0x08xx` mode).
* Apply order: Windows pointer settings → `0x83` then a `GetFeature` status
  read (the `0x8B` token is only the read buffer and is never transmitted) →
  `0x03` status →
  mode `0x02` → rate `0x01` → stage `0x0B` → fixed RGB `0x0C` → light `0x0D`
  → palette `0x10` (blocks 0 and 1) → DPI `0x11` → four `0x12` button frames
  (two 32-byte blocks each) → `0x13` macro blocks (four blocks each) →
  LOD/key response `0x04` (only when `Distance != 0`) → commit `0x08` →
  high-DPI mask `0x07` (only when `Distance != 0`) → save locally.
* Device diagnostics (**More actions → Device diagnostics…**) shows the
  parsed config, the profile summary, the computed apply plan, and live links.
  It is copyable for support.

## Hardware verification status

Validated on a real SM809 wired mouse (VID `04D9`, PID `A09F`):

* SetupAPI enumeration found the control interface at `0xFF00/0xFF00`
  (33-byte output, 9-byte feature) and the monitor interface at
  `0xFF01/0xFF01` (4-byte input).
* The handshake is genuinely validated: the device answers the obfuscated
  challenge with a feature report that decrypts to `00 AA DD 3B 62 ...`. A
  strict decrypt is required; an earlier build accepted the mouse while the
  obfuscation map was wrong, so the link was a false positive.
* A full profile upload now sends 15 feature packets and 11 blocks with no
  error. That is the shipped sequence: two status frames (the `0x8B` value is
  a read-buffer token, not a command), mode/rate/stage/colour/light, two
  palette blocks, the DPI table, four button frames and the commit magic.
* The corrected encoder reproduces the shipped executable's known vector:
  the handshake encrypts to `26 1a ad 02 40 0c 44 5e` with `FB1570`, and the
  mouse's status reply decrypts to the expected magic.

The LED result itself needs eyes on the hardware: this mouse has no light
readback and no input event is emitted after a light change. Apply light mode
0 ("Off") and confirm the illumination stops; if it does not, the remaining
suspect is firmware acceptance of the obfuscated command stream rather than
the frame contents.

Still verify on hardware before relying on them:

* Monitor event framing and on-device stage/rate/mode changes (the tested
  profile did not exercise them).
* Gun table upload (**experimental**, see above); no gun table was assigned
  in the tested profile.
* Firmware version query: this mouse answers `GetFeature` with its status
  report. With the shipped `Update=0` setting the app keeps the configured
  `2.1` instead of showing that reply as a version.
* LED parameter semantics beyond the byte layout.
* DPI lookup tables for sensors other than the shipped `0x0CEF` (`3311`).
* Windows pointer settings (`SystemParametersInfoW`); the live apply test
  deliberately did not change the desktop's pointer configuration.

The app degrades safely: if no device is found, **Apply** still saves the
profile locally and reports that it was not uploaded. Disconnecting, closing,
or applying with no link never blocks the UI.

## Deviations and fixes

* **Lift-off status byte:** the `0x03` status frame writes the lift flag at
  byte 3 (`0x08`) with the `0x40` marker at byte 4 — confirmed from
  `FUN_004196b0`. The ship build's UI state did not always match this.
* **Gun upload enabled:** the rebuild actually streams gun blocks; the
  original silently dropped them.
* **Unknown keys:** the recorder ignores virtual keys it cannot map (the
  original hook path could record key id 0).
* **Macro sync:** "Apply to all buttons using this macro" prevents stale
  per-button macro copies; the original left them out of sync.
* **Validation:** mapping no button to Left Click / Send Gun shows the same
  warning as the original, but the rebuild still lets you save the profile
  locally.
* **Portable data:** profiles are edited in the rebuild's own folder, never in
  the original installation.
* **Native recording:** recording uses low-level hooks directly instead of
  `Hook.dll`, producing the same 16-byte event records.

## Intentionally not included

These parts of the original are not reproduced because they are either absent
from the shipped package or their file formats were not audited. None of them
affect configuring or applying a profile:

* **Tray icon/menu** (`configuration` / `exit`). The window is a normal
  desktop window; closing it saves and exits.
* **Firmware updater**: the `Update\flashOnLine.exe` helper is not present in
  the shipped package, so the rebuild reports the firmware version but does
  not launch an updater.
* **Macro/gun library import/export and the "with password" export variants**:
  the original's file-dialog container format was not recovered. Individual
  macros and gun tables can be created, edited, and uploaded; profiles can be
  imported/exported as `.pbin`.
* **Localisation**: the shipped resources include multiple languages; the
  rebuild is English-only.

## Keyboard shortcuts

* `Ctrl+S` — apply the current profile.
* `Ctrl+1` … `Ctrl+5` — Buttons, Performance, Lighting, Macros, Gun recoil.

## Tests

```bat
python -m pytest -q -rs
```

38 tests cover the binary profile layout, packet/checksum encoders, macro
event encoding, apply sequencing, recorder event assembly, and the Tk UI
(profile CRUD, page switching, demo apply, macro/gun sync, disabled-button
theming).
UI tests need a visible desktop session; they use their own temporary data
folder.

## Project layout

```
sm809-rebuild/
  run.py                  launcher / CLI
  start.bat               real-hardware launcher
  start-demo.bat          demo launcher
  sm809/
    paths.py              portable data directory + first-run seeding
    config.py             Data.ini parser/writer
    model.py              profile/macro/gun binary records, DataStore
    protocol.py           packet encoders, action table, DPI/light/status
    transport.py          ctypes SetupAPI + hid.dll transport + demo
    device.py             connect/handshake/apply sequence, device events
    recorder.py           low-level macro recorder
    winspi.py             Windows pointer settings
    keys.py               virtual-key ↔ SM809 key-id mapping
    ui/                   Tk UI (app, theme, widgets, dialogs, pages)
  tests/                  pytest suite
  data/                   portable profiles and Data.ini (generated/seeded)
```

## Troubleshooting

* **"SM809 not found":** close `SM809 mouse Software.exe` (only one process
  can hold the HID interface), reconnect the mouse, and check Device Manager
  for VID `04D9` / PID `A09F`. `python run.py --hardware` forces the real path.
* **Apply says "Not connected":** the profile is saved locally; connect and
  apply again.
* **A profile shows `Action 0xFF`:** the stored slot contains an action code
  the original does not define either; remap it or choose *Button Off*.
* **Macro will not record:** run as a normal desktop user in the interactive
  session; some security software blocks low-level hooks.
* **High-DPI / lift-off settings do nothing:** `Distance=0` in `Data.ini`
  disables both `0x04` and `0x07`, exactly like the original. Set it to the
  sensor's supported nonzero value and use *Reload Data.ini*.
* **UI looks wrong after DPI change:** restart the app; Tk does not rescale
  live.

## Safety note

This is an unofficial rebuild. Keep the original utility and its `Data`
folder backed up. If a setting misbehaves on hardware, use the original
software (or **Reset**) to restore defaults. Do not run the rebuild and the
original utility at the same time.
