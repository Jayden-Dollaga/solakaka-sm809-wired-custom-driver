# SM809 Wired Studio

A complete desktop configuration studio for the **wired SOLAKAKA SM809** gaming
mouse. It replaces the official configuration utility with a faster, fully local
PySide6 interface and adds features the official wired build hides or lacks,
including per-app profile switching and the recoil-pattern (Gun) editor.

- **Device:** wired SOLAKAKA SM809 only (VID `0x04D9`, PID `0xA09F`).
- **Platform:** Windows (HID, Raw Input and Windows pointer APIs).
- **Data:** the app works on its own copy of the device data in `data/`. It never
  reads or writes the original installation under
  `C:\Program Files (x86)\SM809 mouse Software`.

The wireless SM809 Pro is a different mouse with a different protocol. Its
battery, connection-mode, lift-off and sensor-flag controls do not exist on the
wired model and are not part of this app.

---

## Contents

- [Quick start](#quick-start)
- [Application shell](#application-shell)
- [Profiles](#profiles)
- [Button assignment](#button-assignment)
- [Macro library](#macro-library)
- [Gun (recoil) patterns](#gun-recoil-patterns)
- [DPI stages](#dpi-stages)
- [Lighting](#lighting)
- [Performance and pointer](#performance-and-pointer)
- [Per-app auto-switching](#per-app-auto-switching)
- [On-screen overlay and tray](#on-screen-overlay-and-tray)
- [Hardware and firmware notes](#hardware-and-firmware-notes)
- [Files and formats](#files-and-formats)
- [Diagnostics and logs](#diagnostics-and-logs)
- [Limitations](#limitations)
- [Safety](#safety)
- [Tests](#tests)
- [Project layout](#project-layout)

---

## Quick start

Requirements: Windows 10 or 11 and Python 3.11-3.14 (the range the installer
accepts).

```bat
install_requirements.bat        :: prompts to create .venv, then installs requirements.txt
.venv\Scripts\python run_app.py
```

Or with an existing Python installation:

```bash
python -m pip install PySide6
python run_app.py            # wired hardware, auto-apply
python run_app.py --demo     # offline demo: no USB I/O is performed
python run_app.py --verbose  # DEBUG detail + manual Apply mode
```

`--verbose` switches the studio to **manual apply**, like the official driver:
button, key, DPI, lighting and performance edits are saved to the active profile
but nothing is written to the mouse until you click **Apply** in the top bar.
The button shows `Apply •` while changes are pending. A normal launch keeps
auto-apply.

`--minimized` (or `--tray`) starts straight in the tray; this is what **Start
with Windows** registers.

On first launch the studio creates `data/` and copies the initial device data
from `seed/`. Delete `data/` to start again from the seed; `config/` holds your
profile, macro and gun libraries and is not recreated.

Set `SM809_DATA_DIR` to use a different data folder. The host-side
`config/profiles.json`, `config/macros.json` and `config/guns.json` are created
inside that folder too, so a scratch or second portable copy never writes into
the main one.

---

## Application shell

- **Left rail:** profile quick-switch at the top, the eight feature pages
  (Buttons, Macro, Gun, DPI, Lighting, Performance, Auto-Switch, Profiles), and
  **Reset to Factory** in the footer. The rail scrolls at the 560 px minimum
  window height instead of clipping the last entries.
- **Top bar:** device name, connection indicator, live **POLLING RATE** and
  **DPI** readouts, an upload spinner while a write is in flight, and the
  manual **Apply** button in `--verbose` mode.
- **Live readouts:** the polling rate and DPI values update from the mouse's
  monitor interface, including changes made with the physical DPI buttons or a
  mode-switch button.
- **Connection watchdog:** the wired HID session is re-opened automatically
  (about every 1.5 s) when the cable is plugged back in; there is no modal
  reconnect dialog.
- **Close to tray:** closing the window keeps the app running so auto-switch
  stays active. Quit from the tray menu; pending profile saves are flushed and
  the window size/position are stored before hiding.
- **Single instance:** launching the app again signals the running copy to
  show its window instead of starting a second process.
- **Splash screen:** shown during startup so Qt's first-widget warm-up never
  looks like a freeze.

---

## Profiles

The wired mouse stores **14 complete profiles**. A profile contains the button
mapping, DPI stages and colours, polling rate, lighting, Windows pointer
settings, key response and the embedded macros/guns its buttons use.

- **Quick switch:** choose a profile in the rail combo, or double-click a row
  in the Profiles list. The manually selected profile is the **base profile**
  for auto-switch.
- **Management:** New, Duplicate, Rename and Delete. A new profile is refused
  with a clear message when all 14 records are used; names are kept unique.
- **Search and sort:** search by name; sort by Custom order, A to Z, Z to A,
  Latest or Oldest. Sorting rewrites the stored order, which also changes
  auto-switch priority.
- **Drag to reorder:** profile list order is match priority. The active profile
  is shown in bold and stays selected across renames and refreshes.
- **Portable JSON mirror:** `config/profiles.json` keeps stable UI ids, match
  rules, order and app settings, plus a complete settings mirror for every
  profile. It can be read, diffed or copied without the binary table.
- **Import/Export `.pbin`:** the studio reads and writes the same single-record
  `0x1CC50`-byte format as the official software. Export here → import in the
  official profile menu; export there → **Import profile…** here. Buttons, DPI
  stages/colours, polling, lighting, pointer settings, key response and embedded
  macros/guns travel with the record. Imported macros and gun patterns are added
  to the editable libraries.
- **Import `.psf`:** a one-way migration of a vendor text export (UTF-16LE).
  Keymaps, DPI stages, polling rate, lighting and macro events are translated to
  the wired vocabulary, including the vendor slot order. Host-only actions with
  no wired equivalent are disabled with a migration note.
- **Reset to Factory:** restores the active profile to the wired factory
  defaults (1000-22800 DPI stages, 125 Hz, the Wave effect in red, pointer
  defaults) and keeps its name. It asks for confirmation and writes the change
  to the mouse.
- **Automatic writes:** edits reach the in-memory profile immediately and are
  written to the mouse automatically (or staged in `--verbose` mode). The
  sidecar JSON is saved after a 600 ms pause and on hide/quit; the device write
  covers the same data, so batching loses nothing.

---

## Button assignment

The firmware stores **64 button slots**. The vendor software exposes two work
modes, and this studio matches them:

- **Office Mode** — firmware slots 1-16 (indices 0-15).
- **Game Mode** — firmware slots 33-48 (indices 32-47).
- The remaining slots hold wheel and raw fallbacks and are preserved
  automatically. They are not shown in the UI.
- Rows are numbered 1-16 like the mouse artwork, in the vendor's order
  (slots 6-11, 13-14 on the left; 12, 15, 16, 1-5 on the right), not in raw
  slot order.
- Picking a mode also selects that work mode on the mouse for real. The panel
  and the device never drift apart; a mode change writes a complete profile
  because the firmware ignores a lone `0x02` frame.

Each row opens the action picker. Available actions:

- **Mouse:** Left, Right, Middle, Forward, Backward, Double Click, Scroll Up,
  Scroll Down.
- **DPI:** DPI +, DPI -, DPI Cycle, Sniper Key.
- **Quick:** Three Click, Fire Key, Mode Switch, Send Gun, Light Mode Switch,
  Report +, Report -, Report Cycle, Disable.
- **Key Combination:** any keyboard key via the full HID list, plus the
  left/right modifier keys (**Left/Right Ctrl, Shift, Alt, Win**) as keys in
  their own right. **Detect Key** captures the exact side you press (for example
  `LAlt`) instead of a generic modifier; the four modifier checkboxes remain a
  shorthand for combining a modifier with another key.
- **Fire Key:** rapid-fire interval 1-255 ms and click count 0-255
  (0 = fire while the button is held).
- **Macro:** choose a macro from the library and a play mode — **Repeat while
  held**, or **Play N times** (1-255).
- **Gun:** choose a recoil pattern and a repeat of 1x, 2x or 3x.
- **Windows:** Cut, Copy, Paste, Open, Save, Find, Redo, Select All, Print, New,
  Close Window, Swap Windows, Show Desktop, Run Command, Lock PC.
- **Multimedia:** Media Player, Play/Pause, Stop, Previous Track, Next Track,
  Volume +, Volume -, Mute.
- **Browser:** Browser Home, Favorites, Forward, Backward, Stop, Refresh,
  Search, Email, Calculator, My Computer.

Behaviour:

- A pick applies automatically as one complete profile write; `--verbose`
  stages it until **Apply**.
- **Shared table budget:** macros and guns draw from the same firmware table
  indices 1-11. The vendor caps macro buttons at ten and gun buttons at three
  per layer, but ten macros plus three guns are thirteen tables and cannot all
  be uploaded. The panel shows a live warning naming how many bindings will
  stay silent, and the apply log repeats it. Remove a macro or gun binding to
  free a slot.
- The firmware expects at least one button mapped to **Left Click** or
  **Send Gun**; the original software refuses such a profile. The studio writes
  it but records the same warning.
- Macro and gun bindings are validated before they are accepted: an empty or
  oversized macro, or a gun pattern with no movement, is rejected instead of
  being bound.

---

## Macro library

Macros are named sequences of key and mouse events with per-event timing. The
library lives in `config/macros.json` and is not limited by the 14 device
profiles; a macro is copied into the button entry that uses it.

- **Editor:** each row is one event — Type (Key, Mouse button, Delay), Detail,
  Down/Up, and a delay in milliseconds. Use **Insert event** to add after the
  selected row, **Add text** to expand a string into key events with a configurable
  per-key delay, and **Clear** to empty the macro.
- **Record Input:** records keys typed while the studio has focus and mouse
  button edges system-wide through a Windows low-level hook, with real timing.
  The Stop button's own click is excluded, so stopping never becomes part of
  the macro. Click **Stop** to finish.
- **Limits:** 40 events per macro and a 128-byte encoded firmware table. The
  editor shows the live count and enforces both.
- **Playback:** bind the macro to a button on the Buttons tab. It is embedded in
  that button entry (`0x16`), so the mouse plays it from its own memory and the
  studio does not need to be running.
- **Import/Export `.mbin`:** the library menu and right-click offer the official
  single-record format (856 bytes). Plain export is byte-identical to the
  vendor output; **Export protected** sets the vendor's protected flag
  (`+0xD0`). Imports keep the macro's folder, repeat count and protected flag; a
  folder marker is rejected. Duplicate names get a ` (2)` suffix instead of
  overwriting.
- **Rename:** library menu, right-click, F2, or by editing the name field.
  Names are unique across the library; a blank field restores the stored name.
- **Adoption:** macros found in the mouse's profiles are imported into the
  library under stable ids (`dev:<profile>:<slot>`) and stay editable.
- **Budget:** see the shared 1-11 macro/gun table limit above.

---

## Gun (recoil) patterns

The official software's **Gun** page is hidden in the wired build, but the
`Set Gun` action (`0x79`), the per-button table and the 128-byte encoder are
present in the firmware. The studio exposes a named pattern library in
`config/guns.json`.

Each pattern has up to **30 bullet rows**, each with an X and Y cursor offset
(-255 to 255) and a delay from 0 to 2550 ms in 10 ms steps. The table shows
`#`, `X`, `Y` and `Delay (ms)`, plus the live encoded size (`n / 128 bytes`).

### Recording a pattern

1. Set **Bullets** (1-30) and the **Shot interval** (10-2000 ms in 10 ms steps).
2. Click **Record**. The recorder arms for three seconds, then captures relative
   mouse movement through Windows Raw Input — it keeps working when a game locks
   or recentres the pointer and while the studio is in the background. It never
   consumes input, so the game still receives everything.
3. Switch to the game and fire while pulling against the recoil. One row is
   written per shot interval; recording stops when the bullet count is reached
   or the 128-byte budget is exhausted. Trailing idle rows are trimmed, and a
   capture with no movement leaves the existing pattern untouched.
4. Click **Stop** to finish early.

### Editing and encoding

- **Clear offsets** keeps the delays and sets every X/Y offset to zero.
- **Flip X** and **Flip Y** negate the stored offset column for games with
  inverted controls. They do not make the firmware pull left/up.
- **Offsets have no sign in the firmware.** The encoder transmits `|X|` and
  `|Y|`, so every row pulls right and down regardless of the sign typed. Keep X
  and Y positive for ordinary right/down compensation.
- A real offset row costs 8 bytes, an idle row 4 bytes, and the table holds 128
  bytes including a 2-byte header. Fifteen real rows fit; a longer pattern may
  use the vendor's second-half marker only while idle rows keep it inside the
  budget. The editor flags an oversized or impossible pattern.
- A pattern whose offsets are all zero cannot move the crosshair and is
  rejected when bound.
- The shipped driver never uploaded gun tables, so the block encoder is
  inferred from the vendor binary. Verify a small pattern on the hardware
  before relying on it.

### Binding

- Bind a pattern on the **Buttons** tab with the **Gun** action and a 1x/2x/3x
  repeat. The mouse plays the stored rows itself; the studio does not need to
  be running.
- One Office/Game layer holds at most **three** gun buttons; `Set Left Macro`
  (`0x39`) shares that three-button range and counts toward the limit.
- Gun tables come from the same eleven slots macros use, so a layer full of
  macros can starve a gun. The Buttons tab shows the shared budget warning.
- Patterns found in the mouse's profiles are adopted under
  `dev:<profile>:<slot>` and stay editable.

The Gun page also contains a collapsible **HOW TO USE** card with the same
five-step workflow, kept behind a button so the pattern editor stays visible at
the default window size.

---

## DPI stages

- **Eight stage rows**, each 100-24,000 DPI in 100 DPI steps. Values snap to the
  nearest step. The default stages are 1000, 1600, 2400, 3200, 4800, 6400,
  12000 and 22800 DPI.
- **Enable checkbox:** uncheck a stage to skip it when cycling through DPI
  stages. Disabled rows are dimmed.
- **Active stage:** click a stage's number badge to make it the live DPI. Only
  enabled stages can be activated.
- **LED colour:** each stage has its own colour swatch, shown on the mouse when
  that stage is active.
- **Live feedback:** the current stage is reflected in the top-bar DPI readout
  and, if enabled, the on-screen overlay. Changes made with the physical DPI
  buttons are picked up from the device.
- **Button actions:** DPI +, DPI -, DPI Cycle and Sniper Key can be assigned on
  the Buttons tab.

---

## Lighting

The **LIGHT SETTING** card covers the side-button lighting and follows the
vendor Light page:

- **Twelve effects:** Off, Standard, Breathing, Neon, Wave, Key reaction,
  Trailing, Drag back and forth, Slide, YO-YO, Marbles, Flying star.
- **Only the controls an effect consumes are shown** — Intensity, Pulsation,
  Length, or the Color Setting section — matching the vendor page instead of
  presenting dead sliders.
- **Intensity** 0-255, **Pulsation** 0-4, **Length** 0-4.
- **Color Setting:** Fix Color with one swatch, or Loop Color with eight palette
  swatches. Either opens the colour picker.
- **Clamping:** every LED value is clamped in the UI, the config bridge and the
  frame encoder. A profile saved by an older build with an out-of-range value
  (for example a bad loop/frequency byte) is repaired on load and can never be
  applied or exported in an invalid state.
- **Smooth applying:** edits are debounced by 250 ms, so dragging a slider does
  not flood the HID link.
- **Complete group writes:** a lighting or colour edit always sends the full LED
  group in the vendor's order — fixed colour (`0C`), effect (`0D`), then both
  palette blocks (`10`) — because effects such as Slide and Loop sample colour
  state that must arrive in the same download. The Fix/Loop value (`+0xFC`) is
  clamped to 0 or 1, and the palette is copied as eight raw 4-byte COLORREFs.

---

## Performance and pointer

The Performance page mirrors the official page's ranges and stores the values in
the wired profile.

### Polling rate

- 125, 250, 500 or 1000 Hz.
- The firmware stores the 0-based option index (`+0x80`, also the `0x01` report
  interval: 8/4/2/1 ms), not the frequency. The bridge maps 0→125 Hz … 3→1000 Hz
  exactly like the vendor build, so selecting 1000 Hz really sends a 1 ms
  interval.

### Windows pointer

- **Mouse move speed** 1-11.
- **Mouse scroll speed** 1-11.
- **Double-click speed** 0-10; the tooltip shows the Windows double-click time.
- **Enhance pointer precision** on/off.
- **Scroll one page at a time** on/off.
- **Key response** 1-100 ms, stored at profile `+0x138`. `Data.ini` has
  `Distance=0`, so the official driver and this studio both skip the `0x04`
  frame that would carry it; the value still travels with the profile.
- Pointer settings are applied through the Windows pointer API when the profile
  is written.
- There is **no lift-off distance control**: this unit's `Data.ini` has
  `Distance=0`, so the `0x04`/`0x07` frames are skipped exactly as the official
  driver does.

### Scroll direction (this mouse)

The SM809 encoder reports the opposite direction from the Windows default, and
there is no firmware direction command. The **SCROLL DIRECTION** card fixes this
per device:

- **Invert scrolling for this mouse** asks for administrator permission once,
  sets `FlipFlopWheel` for the SM809 HID mouse collection, and returns Windows'
  global *Scrolling direction* to "Down motion scrolls down".
- Only the SM809 is affected; other mice keep their own direction.
- The mouse disconnects for about a second while Windows reloads it. If
  scrolling is still unchanged, unplug/reconnect the mouse or sign out of
  Windows once — Windows reads this value when the device starts.
- Turning the option off restores the normal Windows direction for this mouse.
- Every attempt, restart and verification result is written to
  `logs/studio.log` under `sm809.wheel`.

---

## Per-app auto-switching

The headline feature the official wired software does not have.

- Each profile can hold one or more **match rules**: executable name, full path,
  or part of the window title. Blank fields are ignored; matching is
  case-insensitive.
- **Detect app (3s)…** waits three seconds, then fills the fields from the
  foreground window and flashes the result in the on-screen overlay.
- **Priority:** first match in profile-list order wins. Drag profiles to
  reorder or sort the list.
- **Base profile:** the profile you selected manually is sticky. When a focused
  app matches a rule, that profile is applied temporarily; when focus moves to
  an app with no rule, the base profile returns.
- **No redundant writes:** a switch fires only when the target profile differs
  from the one already applied, so a steady foreground never re-pushes config.
- **Debounce:** the foreground window is polled every 200 ms and must remain
  stable for 200 ms, so fast Alt-Tab passes do not rewrite the mouse.
- Auto-switch can be enabled on its page or from the tray menu, and the setting
  persists. Switching is announced by a tray notification and, if enabled, the
  overlay.

---

## On-screen overlay and tray

### Overlay

A frameless, always-on-top, click-through HUD for profile, DPI and polling-rate
changes.

- **Show on change:** profile name, DPI (including the mouse's physical DPI
  buttons), polling rate — each independently toggleable.
- **Position:** nine anchors (top/mid/bottom × left/center/right).
- **Multi-monitor:** follow the monitor under the cursor, or pin the HUD to a
  chosen monitor.
- **Appearance:** opacity 30-100%, size 60-200%, duration on screen 0.3-5.0 s.
- **Preview** from the settings dialog; all choices persist across runs.
- The HUD never writes to the device; it only displays existing signals.

### Tray

- **Show window**, and a **Profiles** submenu with the active profile
  checkmarked.
- **Enable auto-switch**.
- **Show on-screen overlay**, **DPI on-screen display**, **Overlay settings…**.
- **Start with Windows** (per-user `HKCU\...\Run`, no administrator rights;
  launches with `--minimized`).
- **Quit**.
- Closing the window hides it to the tray; the app keeps running so auto-switch
  stays active. Double-clicking/triggering the tray icon reopens the window.
- Window size and position are restored on the next launch.

---

## Hardware and firmware notes

| Item | Value |
| --- | --- |
| Device | SOLAKAKA SM809 (wired) |
| VID / PID | `0x04D9` / `0xA09F` |
| Control interface | `0xFF00 / 0xFF00` |
| Monitor interface | `0xFF01 / 0xFF01` |
| Sensor | `3311` (`0x0CEF`), 100 DPI per raw step |
| Profiles | 14 records of `0x1CC50` bytes |
| Buttons | 64 slots; Office/Game modes of 16 |
| Macro table | 40 events, 128 encoded bytes |
| Gun table | 30 rows, 128 encoded bytes per button |
| Lighting | 12 modes |
| Polling | 125/250/500/1000 Hz, stored as a 0-based index |

The wired mouse has no battery, wireless/Bluetooth connection mode, hardware
lift-off distance control, power management or sensor-flag controls; those parts
of the reference UI are not present in this app.

### Timing and smart diffing

- Every HID feature write is followed by a **60 ms** settle window
  (`CMD_SETTLE`), and every 32-byte macro chunk by **120 ms**
  (`MACRO_CHUNK_DELAY`) while macro memory is programmed. Ordinary block writes
  keep the vendor's 20 ms pace. Demo mode skips all delays.
- Applies are diffed section by section against what this link last wrote. A
  switch that only changes DPI sends just those frames; applying an identical
  profile sends no HID traffic at all.
- The diff cache resets on connect/disconnect and after a failed write, when the
  device state is unknown.
- A full switch with many sections or macros takes roughly 0.5-1.5 s. That is
  firmware programming time, not a hang; the top-bar spinner stays visible until
  the write queue drains.
- Full-profile write snapshots are coalesced: if several are waiting, only the
  newest is sent, so a slider drag does not build a backlog that makes the
  pointer stutter.

---

## Files and formats

### Data folder

- `data/Data.ini` and `data/Data/{Data,profile,Default,macro,gun}.bin` are the
  portable copy of the device data, seeded once from `seed/`.
- `SM809_DATA_DIR` moves both this folder and the host-side `config/` folder,
  giving you a second, fully isolated portable copy.

### Host-side libraries

- `config/profiles.json` — profile metadata, match rules, order, app settings
  and a complete human-readable settings mirror for every profile.
- `config/macros.json` — the named macro library.
- `config/guns.json` — the named recoil-pattern library.
- Settings such as auto-switch, overlay appearance, DPI OSD, profile sort and
  window geometry live in `profiles.json`.

### File formats

- **`.pbin`** — one complete profile record, `0x1CC50` bytes (117,840). Shared
  with the official software, including embedded macros and gun patterns.
- **`.mbin`** — one 856-byte vendor macro record, including its folder name,
  loop count and protected flag. Folder markers are rejected.
- **`.psf`** — vendor UTF-16LE text export, imported one-way as a migration
  source. The studio never writes `.psf`.
- **`.bin`** — raw wired profile table accepted by **Import profile…**.

### Logs

- `logs/studio.log`, rotating at 2 MB with three backups.

---

## Diagnostics and logs

Every run writes `logs/studio.log` next to the app at DEBUG level. The console
shows INFO and above; identical consecutive lines collapse into
`... previous message repeated N more times` instead of scrolling, so standing
notes such as `Data.ini Distance=0` appear once per session. `--verbose` mirrors
DEBUG to the console as well.

The log records:

- connect / disconnect, handshake result and firmware version;
- one line per apply with the changed sections and packet/block counts;
  changing Office/Game mode forces a complete download because the firmware
  ignores a lone `0x02` frame;
- every monitor event (`device event 0x.... value=...`), plus the
  `ignoring stale mode report` note when an echo of the layer being left arrives
  right after a mode write;
- at DEBUG, decoded LED values and the exact encoded `0D` lighting and `10`
  palette frames, plus every feature frame written;
- at DEBUG, the full 256-byte `12` button table (four lines) and every 32-byte
  block, so a binding can be traced to its firmware slot (Office = slots 0-15,
  Game = slots 32-47);
- failures as `apply failed in '<section>' after writing ...: <reason>`, where
  the reason names the frame or block the firmware rejected;
- uncaught exceptions from the UI thread, worker threads and Qt itself with full
  tracebacks.

Out-of-range LED fields are repaired and reported: a legacy profile with
`frequency: 126` logs a warning naming the stored value and the safe one used.

Useful troubleshooting:

- **Mouse not detected:** check the cable, close the official software (it may
  hold the HID interface), and watch the top-bar connection dot. The app retries
  automatically.
- **Settings revert after a reconnect:** Windows may have reset the per-device
  wheel value; the SCROLL DIRECTION card re-reads it each time the page is
  opened.
- **A bound macro/gun does nothing:** check the Buttons budget warning and the
  apply log; a table beyond index 11 is left unpointed.
- **Lighting looks wrong:** inspect the encoded `0D`/`10` frames at DEBUG; the
  studio always writes the complete LED group.

---

## Limitations

- **Windows only.** HID access, Raw Input, the pointer API and "Start with
  Windows" are Windows implementations.
- **Wired SM809 only.** It targets VID `0x04D9` / PID `0xA09F`. It does not
  support the wireless SM809 Pro; `--demo` is the only mode without the mouse.
- **Source distribution.** There is no packaged installer or prebuilt `.exe`
  in this repository; run it with Python or build your own bundle.
- **No LOD, battery, wireless status, power management or sensor flags.** Those
  controls belong to the wireless hardware and are intentionally absent.
- **Firmware table budget.** Ten macro buttons and three gun buttons share
  eleven uploadable table slots; a layer cannot hold all thirteen. The UI warns
  and names the bindings that will be silent.
- **Gun offsets are magnitudes.** The firmware pulls right/down; sign handling
  is only an editor convenience.
- **Gun row budget.** The 128-byte table fits fifteen real rows; longer patterns
  are possible only with enough idle rows to stay inside the budget.
- **Gun encoder is inferred.** The shipped driver never uploaded gun tables and
  the encoder was reconstructed from the vendor binary. Verify a small pattern
  on the hardware before relying on it.
- **Wheel fix needs UAC once.** It changes a Windows per-device setting and may
  require a reconnect or one sign-out to take effect.
- **`.psf` migration is one-way.** Host-only vendor actions have no wired
  equivalent and are disabled with a note.
- **Single instance.** The tray-based design intentionally prevents a second
  copy from running.
- **Hardware writes are automatic** in the default mode (on connect, on
  auto-switch and on each edit). Use `--verbose` for staged, manual Apply.

---

## Safety

- The original vendor installation is never opened or modified. All device data
  comes from the copied `data/` folder or `seed/`.
- The app writes the mouse only when you change a setting, when a configured
  profile is applied on connect, or when auto-switch selects a profile.
- `--demo` performs the full pipeline in memory and writes only local data
  files, so the UI can be exercised without a mouse attached.
- `--verbose` stages edits and requires an explicit **Apply**.
- **Reset to Factory** asks for confirmation before overwriting the active
  profile.
- Macro and gun tables are validated and budgeted before upload; impossible or
  empty bindings are rejected instead of overwriting firmware memory.

---

## Tests

```bash
# from this folder: the studio suite only
python -m pytest tests

# from the repository root: studio + legacy wired rebuild in one process
python -m pytest
```

The suite is fully offline: tests copy the seed data to a temporary folder and
use the demo HID transport, so neither the vendor installation nor the mouse is
touched. The root `pytest.ini` puts both project roots on `sys.path` so the two
suites run together without shadowing each other's `wired`/`app`/`sm809`
packages.

---

## Project layout

```
sm809-wired-studio/
├── app/                  # PySide6 UI shell (wired semantics)
│   ├── controller.py     # background wired DeviceService worker + Qt signals
│   ├── logging_setup.py  # console + rotating log, repeat collapsing, crash hooks
│   ├── main_window.py    # shell, panels, tray, overlay, auto-switch
│   ├── profile_store.py  # wired DataStore adapter + stable UI metadata
│   ├── psf_import.py     # official .psf -> wired profile migration
│   ├── recoil_recorder.py# raw-input mouse movement capture for the Gun tab
│   ├── panels/           # Buttons, Macro, Gun, DPI, Lighting, Performance, ...
│   └── widgets/          # action picker, colour picker, overlay HUD
├── wired/                # wired SM809 core (copied, self-contained)
│   ├── protocol.py       # feature frames, actions, lighting tables
│   ├── model.py          # profile / button / macro binary records
│   ├── bridge.py         # studio config <-> wired Profile translation
│   ├── device.py         # apply engine (ordered frames, commit)
│   ├── transport.py      # SetupAPI / hid.dll feature + block I/O
│   └── paths.py          # portable data folder, seed copy
├── sm809pro/             # thin adapter used by the UI (actions, defaults, macros)
├── seed/                 # initial Data.ini + Data/*.bin copied on first run
├── data/                 # created on first run (git-ignored)
├── config/               # profiles.json / macros.json / guns.json (UI metadata)
├── logs/                 # studio.log + rotations (created on first run)
├── tests/
└── run_app.py
```
