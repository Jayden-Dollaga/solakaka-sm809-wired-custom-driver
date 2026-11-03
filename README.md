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

### Feature summary

| Area | What the studio does |
| --- | --- |
| Profiles | 14 full device profiles; quick switch, new/duplicate/rename/delete, drag-to-order, search, five sort modes, `.pbin` import/export, one-way `.psf` migration, JSON mirror |
| Buttons | 64 firmware slots; Office and Game layers; all vendor actions (mouse, DPI, quick, shortcuts, fire, macro, gun, Windows, multimedia, browser); left/right modifier keys; Detect Key |
| Macros | Named library; event editor with timing; text expansion; system-wide keyboard/mouse recorder; `.mbin` import/export (plain or protected); paste, clear, move, delete |
| Gun | Named recoil-pattern library; 30-row table; Raw Input recorder; X/Y/delay editor; flip/clear; 128-byte budget; 1x/2x/3x binding |
| DPI | Eight stages, 100-24,000 DPI; enable/skip stages; per-stage LED colour; active-stage click; live device feedback |
| Lighting | Twelve vendor effects; only the controls each effect uses; Fix/Loop colour; eight-colour palette; clamping; debounced complete LED writes |
| Performance | Polling 125/250/500/1000 Hz; Windows pointer speed, scroll speed, double-click, acceleration, page scroll; key response; per-device wheel direction fix |
| Auto-switch | Per-profile app rules (exe, path, title); running-window picker; 3-second detect; browse for an exe; priority ordering; debounced, non-redundant switching; elevated-game fallback |
| Shell | Always-local PySide6 UI; auto or manual apply; live closable log; system tray; start with Windows; single instance; splash; window geometry restore |
| Overlay | Click-through HUD for profile, DPI and polling changes; nine anchors; monitor follow/pin; opacity, size and hold time |
| Diagnostics | DEBUG log file with rotation; repeat collapsing; GUI log stream; structured apply/device/error records; crash hooks |

---

## Contents

- [Quick start](#quick-start)
- [Command-line and environment reference](#command-line-and-environment-reference)
- [Application shell](#application-shell)
- [Settings dialog](#settings-dialog)
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
- [Building the portable EXE](#building-the-portable-exe)
- [Project layout](#project-layout)
- [Architecture and data flow](#architecture-and-data-flow)
- [Complete function reference](#complete-function-reference)

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
python run_app.py            # wired hardware, saved apply mode
python run_app.py --demo     # offline demo: no USB I/O is performed
python run_app.py --verbose  # DEBUG detail + start in manual apply
```

Edits are written to the mouse immediately by default (**auto-apply**), so no
**Apply** button is shown. Use **Settings…** in the tray menu to switch to
**manual apply** for every page, like the official driver: button, key, DPI,
lighting and performance edits are saved to the active profile but nothing is
written to the mouse until you click the top-bar **Apply** button, which only
exists in that mode and shows `Apply •` while changes are pending. The choice
is saved, so it survives restarts; `--verbose` simply starts a session in
manual apply with DEBUG logging.

`--minimized` (or `--tray`) starts straight in the tray; this is what **Start
with Windows** registers.

On first launch the studio creates `data/` and copies the initial device data
from `seed/`. The seed contains exactly one factory-default profile named
**Profile** (built from `Default.pbin`); the vendor installer's sample profile
library is never shipped. Delete `data/` to start again from the seed; `config/`
holds your profile, macro and gun libraries and is not recreated.

Set `SM809_DATA_DIR` to use a different data folder. The host-side
`config/profiles.json`, `config/macros.json` and `config/guns.json` are created
inside that folder too, so a scratch or second portable copy never writes into
the main one.

## Command-line and environment reference

`run_app.py` and the packaged exe accept the same flags:

| Flag | Effect |
| --- | --- |
| *(none)* | Normal start against the wired mouse, using the saved apply mode. |
| `--demo` | Offline demo. The full controller/apply pipeline runs against an in-memory transport, so no USB traffic is generated. Never relaunches elevated from source. |
| `--verbose` / `-v` | DEBUG level on the console and in the in-app log; also starts the session in manual apply. The file log is always DEBUG. |
| `--minimized` / `--tray` | Start in the tray without showing the window. Used by **Start with Windows**; ignored when no system tray is available. |
| `--no-elevate` | From source, skip the automatic administrator relaunch. Ignored by the packaged exe, which elevates through its manifest. |

| Variable | Effect |
| --- | --- |
| `SM809_DATA_DIR` | Use this folder for both `data/` (device tables) and `config/` (host libraries). Ideal for tests, demos and a second portable copy. |
| `SM809_ELEVATION_TRIED=1` | Internal loop guard: set before an elevated relaunch so a declined UAC prompt cannot relaunch forever. |

The application also creates and uses:

- `logs/studio.log` (rotating at 2 MB, three backups), always at DEBUG.
- `SM809WiredStudio_single_instance`, a Qt local-socket name; a second launch
  asks the running copy to show its window and then exits.

### Administrator rights

Like the official SM809 driver, the studio asks for administrator rights so it
can read the foreground window of games that run elevated. Windows does not let
a normal process inspect an elevated one, so without this the auto-switch
watcher cannot see anti-cheat or other admin-only titles and those apps would
never trigger a profile.

- **Packaged exe:** `SM809WiredStudio.spec` embeds a `requireAdministrator`
  manifest (`uac_admin=True`), so Windows shows the consent prompt every time
  the exe starts.
- **From source:** `run_app.py` checks `IsUserAnAdmin()` at startup and, when
  needed, relaunches itself once through `ShellExecuteW("runas", ...)`. Accept
  the UAC prompt to continue with full detection.
- If you decline the prompt, the studio asks whether to continue without
  administrator rights. Continuing works for most apps, but elevated games are
  not detected; the Auto-Switch page shows an orange reminder in that state.
- `--demo` never relaunches from source, and `--no-elevate` skips the relaunch on
  purpose. (The packaged exe always elevates through its manifest, even in demo
  mode.) A `SM809_ELEVATION_TRIED=1` environment sentinel prevents a relaunch
  loop if UAC is dismissed.

Note that **Start with Windows** writes a normal `HKCU\...\Run` entry. Because
the exe requires administrator rights, Windows may show a UAC prompt at sign-in;
if that is annoying, launch the studio manually or keep the auto-start task but
expect the prompt.

---

## Application shell

- **Left rail:** profile quick-switch at the top, the eight feature pages
  (Buttons, Macro, Gun, DPI, Lighting, Performance, Auto-Switch, Profiles), and
  **Reset to Factory** in the footer. The rail scrolls at the 560 px minimum
  window height instead of clipping the last entries.
- **Top bar:** device name, the **Apply** button (manual mode only), the
  connection indicator, live **POLLING RATE** and **DPI** readouts, and an
  upload spinner while a write is in flight.
- **Apply modes:** **Auto-apply** writes each edit immediately and shows no
  Apply button; **Manual apply** stages every page's edits and reveals the
  **Apply** button, which shows `Apply •` while changes are pending. Change the
  mode in **Settings…** (tray menu); the choice is saved.
- **Live log:** turn it on in **Settings…** and a closable bottom panel
  appears, streaming the same records as `logs/studio.log` (INFO normally,
  DEBUG with `--verbose`). The panel has **Clear**, **Open log file**, and a
  close `×`; turning it back on is done from **Settings…**, and the panel state
  is remembered. **Settings…** also contains the overlay controls that used to
  live in their own dialog.
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

## Settings dialog

**Settings…** in the tray menu is the single place for application behaviour.
It is a scrollable dialog with three groups and writes one sidecar update on
**OK**; **Cancel** reverts any overlay preview it made.

### Applying changes

- **Auto-apply — write every change immediately** (default).
- **Manual apply — stage changes, then press Apply**.
- The choice applies to every page and is stored as `manual_apply`.
- The top-bar **Apply** button exists only in manual mode. It shows
  `Apply •` while edits are staged, and clicking it writes the complete current
  profile. Switching from manual to auto writes any staged edits immediately.
- `--verbose` starts a session in manual mode; the setting still wins on later
  normal launches.

### Live log

- **Show the live log panel** adds a dock at the bottom of the window.
- The panel is resizable through the splitter above it.
- Its header has **Clear** (view only), **Open log file** (opens
  `logs/studio.log`, or its folder if the build could not create it) and **×**
  (close the panel).
- Visibility is stored as `show_log`; reopening is done from this dialog.
- The panel backfills at most 1500 recent records when first opened and keeps
  the newest 3000 lines in the view.

### On-screen overlay

- **Show on-screen overlay** — master switch (`overlay`).
- **SHOW ON CHANGE** — Profile name, DPI (including the mouse's physical DPI
  buttons), Polling rate (`overlay_show`).
- **Position** — nine anchors: top/mid/bottom × left/center/right
  (`overlay_pos`).
- **Show on the monitor under the cursor** — follow the cursor, or pin the HUD
  to the monitor chosen in the **Monitor** combo
  (`overlay_follow_cursor`, `overlay_monitor`).
- **Transparency (opacity)** 30-100 % (`overlay_opacity`).
- **Size** 60-200 % (`overlay_scale`).
- **Duration on screen** 0.3-5.0 s (`overlay_hold`).
- **Preview** flashes the currently enabled fields without writing to the mouse.

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
  written to the mouse automatically (or staged when manual apply is selected
  in **Settings…**). The sidecar JSON is saved after a 600 ms pause and on
  hide/quit; the device write covers the same data, so batching loses nothing.

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

- A pick applies automatically as one complete profile write; manual apply
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
  stages. Disabled rows are dimmed. The mouse stores the stages as one
  continuous list, so enabled rows keep their order but gaps are closed when
  the profile is written (stage 2 stays selected even if stage 1 is disabled).
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

- Each profile can hold one or more **custom apps**: executable name, full
  path, or part of the window title. Blank fields are ignored; every filled
  field must match, case-insensitively.
- **Custom apps** page: click a profile on the left to see the apps assigned to
  it on the right. The same list is reachable from **Profiles → Manage apps…**.
- **Add app…** opens a searchable list of every running window, with icons and
  exe names (like the NVIDIA Control Panel program list), and assigns the
  chosen app immediately. The rule uses the exe name alone when it is unique,
  adds the full path only when another running app shares the exe (e.g. UE's
  `Client-Win64-Shipping.exe`), and adds the window title for UWP apps that all
  run inside `ApplicationFrameHost.exe`.
- **Detect app (3s)…** does the same for the foreground window without using
  the list — useful for a fullscreen game. A second capture of the same app is
  not duplicated. The overlay confirms what was captured.
- **Browse…** in the Add app dialog chooses an application's `.exe` from disk,
  so games and launchers that are not currently running can be added too.
- **Live readout:** while the page is open it shows the current foreground exe
  and whether it matches a profile.
- **Priority:** first match in profile-list order wins. Drag profiles to
  reorder or sort the list.
- **Base profile:** the profile you selected manually is sticky. When a focused
  app matches a rule, that profile is applied temporarily; when focus moves to
  an app with no rule, the base profile returns.
- **No redundant writes:** a switch fires only when the target profile differs
  from the one already applied, so a steady foreground never re-pushes config.
- **Debounce:** the foreground window is polled every 200 ms and must remain
  stable for 200 ms, so fast Alt-Tab passes do not rewrite the mouse.
- **Elevated games:** if Windows denies process-query access (some launchers or
  anti-cheat titles), the watcher falls back to a process snapshot, so exe-name
  and title rules still match.
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
- **Show on-screen overlay** and **DPI on-screen display** toggles.
- **Settings…** — the single place for apply mode (auto/manual), the live log,
  and every overlay appearance control.
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
- Each apply starts with the vendor's status pair: a `0x83` query, then a `0x03`
  frame whose bytes 1-3 and 5-6 echo the device's reply, byte 3 carrying the
  lift-off flag while keeping the reply's other bits, and byte 4 fixed at `0x40`.
  Without a usable reply (demo/offline, short or foreign reply) the constant
  legacy frame is sent instead. Captured Office/Game cycles are pinned by
  `tests/test_capture_regression.py`.
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
- Settings such as auto-switch, apply mode, log panel visibility, overlay
  appearance, DPI OSD, profile sort and window geometry live in
  `profiles.json`.

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

The same records can be watched without a console: **Settings… → Live log**
shows a live bottom panel (INFO by default, DEBUG with `--verbose`). Close it
with `×`; **Clear** only clears the view, and **Open log file** opens
`logs/studio.log` for the full history. The panel's visibility is remembered,
and there is no separate log button in the top bar or tray menu — Settings is
the only switch. Apply mode lives in the same dialog.

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
- **Auto-switch does not fire:** make sure the app appears in the selected
  profile's **Custom apps** list (start it first, then use **Add app…**, or
  **Detect app (3s)** while it is in front), auto-switch is enabled, and the
  studio is still running in the tray. If the game runs as administrator,
  restart the studio elevated too; an elevated window is invisible to a normal
  process. The live **Foreground** line shows what Windows reports; run with
  `--verbose` and look for DEBUG `sm809.autoswitch` foreground lines if
  matching still fails.

---

## Limitations

- **Windows only.** HID access, Raw Input, the pointer API and "Start with
  Windows" are Windows implementations.
- **Wired SM809 only.** It targets VID `0x04D9` / PID `0xA09F`. It does not
  support the wireless SM809 Pro; `--demo` is the only mode without the mouse.
- **Packaging.** There is no installer: the portable single-file
  `SM809WiredStudio.exe` (built with `build_exe.bat`, attached to the GitHub
  release) is the supported way to run it without Python. A source checkout
  needs Python and the dependencies in `requirements.txt`.
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
  auto-switch and on each edit). Select manual apply in **Settings…** for
  staged edits and an explicit **Apply**.

---

## Safety

- The original vendor installation is never opened or modified. All device data
  comes from the copied `data/` folder or `seed/`.
- The app writes the mouse only when you change a setting, when a configured
  profile is applied on connect, or when auto-switch selects a profile.
- `--demo` performs the full pipeline in memory and writes only local data
  files, so the UI can be exercised without a mouse attached.
- Manual apply stages edits and requires an explicit **Apply**.
- **Reset to Factory** asks for confirmation before overwriting the active
  profile.
- Macro and gun tables are validated and budgeted before upload; impossible or
  empty bindings are rejected instead of overwriting firmware memory.

---

## Building the portable EXE

`SM809WiredStudio.spec` builds one self-contained, windowed executable with
PyInstaller. Build from the folder that contains the spec:

```bat
.venv\Scripts\python -m pip install pyinstaller
.venv\Scripts\python -m PyInstaller --noconfirm --clean SM809WiredStudio.spec
```

`build_exe.bat` wraps this for releases. It refuses to run while
`SM809WiredStudio.exe` is open, then deletes `build\SM809WiredStudio`, `dist\`
and the working `data\` folder before invoking PyInstaller with `--clean`.
`data\` is recreated from `seed\` on the next launch, so a fresh exe starts with
the single factory **Profile**. Your source `config\` libraries are never
deleted.

### What the spec bundles

All read-only resources resolve through `sys._MEIPASS` at runtime
(`app/paths.py`, `wired/paths.py`):

| Bundled path | Purpose |
| --- | --- |
| `images/icon.ico` | Window, taskbar, tray and Explorer icon (also the `icon=` build argument) |
| `images/mouse.png` | Numbered mouse artwork on the Buttons page |
| `images/check.png` | Check mark for themed checkboxes/radios |
| `seed/Data.ini` | Device configuration: sensor, button defaults, empty password, `Distance=0` |
| `seed/Data/Data.bin` | Device state/selection record |
| `seed/Data/Default.pbin` | Factory profile template used by **Reset to Factory** |
| `seed/Data/profile.bin` | Initial single-profile table (`0x1CC50` bytes) |
| `seed/Data/macro.bin` | Factory macro table (two records) |
| `seed/Data/gun.bin` | Factory gun table (empty) |

The spec checks every path above before building and aborts with a readable
error if one is missing. It uses explicit file entries rather than whole
folders, so a stray file in `seed/` can never ship inside a release.

### What the spec deliberately leaves out

- The developer's `data/`, `config/`, `logs/` and `backups/` folders. They are
  never packed, so no personal profiles, macros, guns or settings travel with a
  release.
- The vendor installation under `C:\Program Files (x86)\SM809 mouse Software`
  and its sample profile library.
- `tests/`, `analysis/`, `.venv/`, `build/` and `dist/`.
- The unused root files `seed/Data.bin` and `seed/profile.bin` (the app seeds
  only from `seed/Data.ini` and `seed/Data/*`).

### Build configuration

- **One-file, windowed:** `console=False`; unhandled exceptions still show
  PyInstaller's traceback dialog (`disable_windowed_traceback=False`), while
  normal diagnostics go to `logs/studio.log` and the in-app log.
- **No hidden imports:** every package (`app`, `sm809pro`, `wired`) is reached
  through static imports from `run_app.py`. HID access is ctypes against
  `hid.dll`/SetupAPI, so `binaries=[]`.
- **No UPX:** packing is disabled because it can trip antivirus software and
  break Qt DLLs.
- **Administrator manifest:** `uac_admin=True` embeds `requireAdministrator`,
  matching the official driver. Windows therefore shows a UAC prompt on every
  start, even with `--demo`; source runs behave differently (see
  [Administrator rights](#administrator-rights)).
- **Icon:** `images/icon.ico` is embedded by PyInstaller and also bundled for
  the runtime `QIcon`.
- **`tkinter` excluded:** it belonged to the early prototype and is never
  imported.
- **PYZ archive:** `noarchive=False` keeps modules compressed in the archive;
  `optimize=0` preserves normal bytecode and docstrings.

### Output and first run

The result is `dist\SM809WiredStudio.exe` (roughly 52 MB). Close any running
copy before overwriting it. On first launch the exe creates, beside itself:

```
data/Data.ini
data/Data/{Data,profile,Default,macro,gun}.bin
config/{profiles,macros,guns}.json
logs/studio.log
```

Those folders survive moving or replacing the exe. The first start takes a few
seconds while the bundle unpacks to a temporary folder; later starts are
faster. All command-line flags and environment variables work exactly as from
source.

To smoke-test a build without a mouse, run
`dist\SM809WiredStudio.exe --demo`; it still elevates through the manifest but
performs no USB I/O.

### Release checklist

1. Run `python -m pytest` and confirm the full suite passes.
2. Bump the version/tag, then run `build_exe.bat`.
3. Launch `dist\SM809WiredStudio.exe --demo` and exercise the pages, Settings,
   log panel and tray.
4. Verify the exe size/icon and that a first run starts with exactly one
   factory **Profile**.
5. Attach `dist\SM809WiredStudio.exe` to the GitHub release with the release
   notes and checksum.

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

### Coverage by file

The studio suite contains **181 tests**:

| File | Tests | Focus |
| --- | ---: | --- |
| `test_core.py` | 17 | Seed/data, profile limits, config round-trip, `.pbin` parity, wheel swap, monitor reads, key/slot ordering |
| `test_gui_smoke.py` | 22 | Full window in demo mode, every page at minimum width, lighting debounce, mode/DPI push, Apply modes, log panel, shared table budget |
| `test_autoswitch.py` | 21 | Rule matching, priority, debounce/revert, running-app picker, 3-second detect, browse, elevation hint |
| `test_capture_regression.py` | 6 | Byte-exact Office/Game apply cycles captured from the official app with USBPcap, including the echoed 0x03 status frame |
| `test_dpi_stage_selection.py` | 8 | Disabled stages, relative selection, device pushes, clamping |
| `test_elevation.py` | 5 | Admin detection, relaunch matrix, declined UAC, sentinel |
| `test_guns.py` | 11 | Encoding budget, zero-movement rejection, store adoption, binding round-trip, recorder trimming |
| `test_lighting_page.py` | 8 | Vendor Light-page controls, defaults, loop colours, panel visibility |
| `test_lighting_safety.py` | 12 | Frame clamping, palette packing, hostile configs, legacy repair |
| `test_log_panel.py` | 3 | Live streaming, history backfill, clear/close |
| `test_logging.py` | 8 | Debug file, handler replacement, repeat collapsing, apply diagnostics |
| `test_macro_io.py` | 9 | Byte-identical `.mbin` round-trip, protected flag, folder rejection, unique names |
| `test_macro_protocol.py` | 10 | Event/table encoding, descriptor pairing, shared 1-11 budget, upload path |
| `test_performance_and_macros.py` | 3 | Official ranges, mouse-message mapping, mouse-button recording |
| `test_psf_and_timing.py` | 18 | `.psf` migration, JSON portability, section diffing, mandatory delays, data-dir isolation |
| `test_smoothness.py` | 8 | Deferred saves, cheap summaries, no-op guards, autoswitch targets |
| `test_wheel_direction.py` | 12 | Registry mapping, elevated helper, retries, panel state/revert |

GUI tests use `QT_QPA_PLATFORM=offscreen` through the test fixtures and never
open a real device; hardware behaviour is validated manually with the mouse
attached.

---

## Project layout

```
sm809-wired-studio/
├── run_app.py                 # entry point: elevation, logging, single instance, splash
├── SM809WiredStudio.spec      # PyInstaller one-file build definition
├── build_exe.bat              # clean release build (refuses to run while the app is open)
├── install_requirements.bat   # create .venv and install requirements.txt
├── requirements.txt           # PySide6
├── README.md
│
├── app/                       # PySide6 desktop shell
│   ├── __init__.py
│   ├── main_window.py         # TopBar + MainWindow: rail, pages, apply pipeline, tray, settings
│   ├── controller.py          # DeviceController: background DeviceService worker and Qt signals
│   ├── profile_store.py       # ProfileStore: wired DataStore adapter, sidecar metadata, import/export
│   ├── autoswitch.py          # ForegroundWatcher, rule matching, app picker helpers, AutoSwitcher
│   ├── autostart.py           # per-user Start with Windows registry entry
│   ├── elevation.py           # UAC detection, self-relaunch, declined-UAC handling
│   ├── log_bridge.py          # logging -> Qt signal bridge for the live log panel
│   ├── logging_setup.py       # rotating file log, repeat collapsing, crash/Qt hooks
│   ├── macro_store.py         # named macro library (config/macros.json)
│   ├── macro_file.py          # vendor .mbin import/export (856-byte records)
│   ├── gun_store.py           # named recoil-pattern library (config/guns.json)
│   ├── psf_import.py          # one-way vendor .psf profile migration
│   ├── recoil_recorder.py     # Raw Input mouse-delta capture for the Gun recorder
│   ├── mouse_hook.py          # system-wide low-level mouse-button hook for macro recording
│   ├── paths.py               # frozen-aware app/config/resource paths
│   ├── theme.py               # Precision Instrument palette, fonts and QSS
│   │
│   ├── panels/
│   │   ├── __init__.py
│   │   ├── buttons_panel.py   # 64-slot Office/Game remap grid + mouse reference
│   │   ├── macro_panel.py     # macro library, event editor, recorder, .mbin I/O
│   │   ├── gun_panel.py       # recoil-pattern library, recorder, row editor
│   │   ├── dpi_panel.py       # eight DPI stages, enable flags, colours, active stage
│   │   ├── lighting_panel.py  # vendor Light page: effects, parameters, palette
│   │   ├── performance_panel.py # polling, pointer settings, key response, wheel fix
│   │   ├── autoswitch_panel.py# per-profile custom apps, detect, live foreground readout
│   │   ├── profiles_panel.py  # profile list, search, sort, drag order, management actions
│   │   └── app_picker.py      # NVIDIA-style running-window picker + Browse for an exe
│   │
│   └── widgets/
│       ├── __init__.py
│       ├── action_picker.py   # action categories, shortcut/fire/macro/gun editors
│       ├── color_picker.py    # themed preset + HSV/RGB/hex colour picker
│       ├── controls.py        # ResponsiveRow, Card, Segmented
│       ├── log_panel.py       # dockable live log view (Clear / Open / ×)
│       └── overlay.py         # click-through HUD and persistent alert overlay
│
├── sm809pro/                  # thin adapter layer used by the UI
│   ├── __init__.py
│   ├── actions.py             # 3-byte action helpers, physical<->firmware slot mapping
│   ├── defaults.py            # factory button table and complete profile config
│   ├── device.py              # open store/service, load Data.ini, demo mode
│   ├── macros.py              # text expansion, HID conversion, key labels
│   └── protocol.py            # DPI conversion and lighting labels for the sensor
│
├── wired/                     # self-contained wired-SM809 device core
│   ├── __init__.py
│   ├── protocol.py            # packets, obfuscation, checksum, frame/block encoders
│   ├── model.py               # Profile, ButtonEntry, MacroEvent, Bullet, DataStore
│   ├── bridge.py              # studio config <-> wired Profile translation and budgets
│   ├── device.py              # DeviceService: connect, handshake, diffed apply, events
│   ├── transport.py           # SetupAPI + hid.dll feature/block I/O, monitor reads
│   ├── config.py              # Data.ini parser/writer
│   ├── keys.py                # virtual-key <-> firmware key-id mapping (111 rows)
│   ├── paths.py               # portable data folder and one-time seed copy
│   ├── winspi.py              # Windows pointer settings (speed, wheel, double-click)
│   └── wheel_direction.py     # per-device FlipFlopWheel fix + elevated helper
│
├── seed/                      # clean factory data copied once on first launch
│   ├── Data.ini
│   ├── Data/{Data,profile,Default,macro,gun}.bin
│   ├── Data.bin               # unused legacy copy (not bundled)
│   └── profile.bin            # unused legacy copy (not bundled)
│
├── images/
│   ├── icon.ico               # window/taskbar/tray/Explorer icon
│   ├── mouse.png              # numbered Buttons-page artwork
│   └── check.png              # themed checkbox/radio check mark
│
├── data/                      # created on first run (git-ignored)
├── config/                    # profiles.json / macros.json / guns.json (git-ignored)
├── logs/                      # studio.log + rotations (created on first run)
├── backups/                   # optional manual backups (never bundled)
├── build/ dist/               # PyInstaller work/output (git-ignored)
└── tests/                     # 181 offline tests (see above)
```

---

## Architecture and data flow

### Layers

1. **`wired/` — device core.** Binary-compatible records (`Profile`,
   `ButtonEntry`, `MacroRecord`, `GunRecord`), the `DataStore` file layer, the
   wire protocol/encoders, `DeviceService` (connect, handshake, diffed apply,
   monitor events), the ctypes HID transport, Data.ini parsing, key mapping,
   Windows pointer settings and the wheel-direction fix. It has no Qt imports
   and can be tested headlessly.
2. **`sm809pro/` — adapter layer.** Small helpers that translate between UI
   concepts and the wired core: action tuples, factory defaults, slot mapping,
   text-to-macro conversion, DPI/light labels.
3. **`app/` — PySide6 shell.** Panels emit intent signals; `MainWindow` merges
   them into one studio config dict, persists it through `ProfileStore`, and
   queues device writes through `DeviceController` (a QThread worker owning
   `DeviceService`).
4. **`run_app.py`** — elevation, logging, Qt bootstrap, splash, single-instance
   socket and argument handling.

### Startup

```
run_app.main
  -> app.elevation.prepare_startup      # UAC relaunch unless --demo/--no-elevate
  -> app.logging_setup.setup_logging    # console + rotating DEBUG file
  -> app.log_bridge.install             # logging -> Qt signal
  -> QApplication + theme palette/QSS
  -> single-instance hand-off           # second launch raises the first, then exits
  -> splash
  -> MainWindow
       -> ProfileStore()                # opens data/Data, reads sidecar JSON
       -> MacroStore(), GunStore()      # config/macros.json, config/guns.json
       -> adopt embedded macros/guns    # dev:<profile>:<slot> ids
       -> build panels, wire signals
       -> AutoSwitcher, overlay, tray, log panel
       -> DeviceController.start()      # worker thread connects/retries
       -> restore geometry
```

On connect the controller reads the device status (mode, DPI stage, rate,
firmware version) and `MainWindow` pushes the active profile so the mouse and
the UI start from the same state.

### Edit -> apply path

```
panel signal (apply_requested / polling_changed / ...)
  -> MainWindow._update_config(section, value)
       -> merge into self._current_config
       -> ProfileStore.set_config(persist=False)  # binary record + dirty flag
       -> 600 ms debounced save of profile.bin
       -> auto mode: apply_profile(force=False) | manual mode: mark pending
  -> ProfileStore.apply(pid, service, config)
       -> wired.bridge.config_to_profile   # config dict -> wired Profile
       -> DeviceController.call("apply_config")
            -> DeviceService.apply(profile)
                 -> _apply_sequence        # diff each section vs last write
                 -> protocol frames/blocks # buttons, DPI, lighting, macros, guns
                 -> transport.set_feature / write_block
                 -> commit frame, settle delays, status refresh
```

- **Diffing:** `DeviceService` remembers what this link last wrote; identical
  sections send no traffic, and a reconnect clears the cache.
- **Coalescing:** full-profile snapshots are queued and only the newest is sent;
  lighting edits are debounced 250 ms, profile persistence 600 ms.
- **Manual mode:** no device call happens until **Apply**; switching to auto
  flushes the staged config.
- **Demo mode:** `HidTransport` answers in memory; no delays and no USB I/O.

### Persistence

| File | Written by | Contents |
| --- | --- | --- |
| `data/Data/profile.bin` | `DataStore` through `ProfileStore` | 14 complete `0x1CC50` records (authoritative for the mouse) |
| `data/Data/Data.bin` | `DataStore` | Selected record index |
| `data/Data/macro.bin` | `DataStore` | Device macro table |
| `data/Data/gun.bin` | `DataStore` | Device gun table |
| `config/profiles.json` | `ProfileStore` | Stable ids, names, match rules, order, active id, app settings, full config mirror |
| `config/macros.json` | `MacroStore` | Named macros with events, loop, folder, protected flag |
| `config/guns.json` | `GunStore` | Named patterns with rows |
| `logs/studio.log` | `logging_setup` | DEBUG diagnostics, rotating 2 MB × 4 |

### Auto-switch loop

`AutoSwitcher` is a 200 ms timer feeding `ForegroundWatcher` (GetForegroundWindow
plus process query, with a Toolhelp snapshot fallback). The foreground must stay
stable for 200 ms before a rule is applied. `match_profile()` walks profiles in
list order and returns the first match. `_apply_by_id()` writes the matched
profile without changing the manually selected **base** profile; when the
foreground no longer matches, the base profile is restored. A switch only fires
when the target differs from the profile already applied.

---

## Complete function reference

Every public module-level function and public class method is listed below.
Names starting with `_` are internal helpers and are intentionally omitted;
Qt signals are noted where panels expose them to `MainWindow`.

### Entry point

| Symbol | Purpose |
| --- | --- |
| `run_app.main()` | Elevation, logging, Qt setup, single-instance hand-off, splash, window creation, event loop |
| `run_app._hand_off_if_running()` | Ask an existing instance to show itself; `True` when this launch should exit |
| `run_app._listen_for_relaunch(win)` | Own the local socket and raise `win` on a later launch |

### `app.main_window`

| Symbol | Purpose |
| --- | --- |
| `app_icon()` | Load `images/icon.ico` frozen-safely; used by window, taskbar and tray |
| `TopBar.set_manual_apply(enabled)` | Show/hide **Apply** according to the apply mode |
| `TopBar.set_pending(pending)` | Switch between `Apply` and `Apply •` and update the tooltip |
| `TopBar.set_connection(info)` | Connection pill and capability text |
| `TopBar.set_offline()` / `set_disconnected()` | Grey/red connection states |
| `TopBar.set_error(msg)` | Red "not connected" pill with the error in its tooltip |
| `TopBar.set_battery(percent, charging)` | Battery text (unused by the wired mouse, kept for parity) |
| `TopBar.set_dpi_readout(text)` / `set_rate_readout(hz)` | Live DPI/polling readouts |
| `TopBar.set_busy(busy)` | Animated apply spinner |
| `MainWindow.apply_profile(config, force, pid, reseed)` | Seed every panel and write the complete wired profile |
| `MainWindow.set_manual_apply(enabled, persist=True)` | Switch modes for all pages; flush staged edits when going auto |
| `MainWindow.closeEvent(e)` | Hide to tray, flush saves, persist geometry, honour explicit quit |
| `Placeholder` | Simple "coming soon" page (retained for future sections) |

`MainWindow` internal slots, grouped by feature: navigation and profile bar
(`_on_nav`, `_build_profile_bar`, `_refresh_profile_combo`, `_sync_combo`,
`_select_profile`, `_apply_by_id`, `_on_auto_switched`); profile lifecycle
(`_profile_new`, `_profile_duplicate`, `_profile_rename`, `_profile_delete`,
`_profile_import`, `_profile_import_pbin`, `_profile_import_psf`,
`_profile_export_pbin`, `_confirm_reset`, `_on_profile_reorder`,
`_on_profile_sort`, `_on_rules_changed`, `_on_manage_apps`,
`_on_app_detected`); panel writes (`_apply_dpi`, `_apply_active_dpi`,
`_apply_buttons_mode`, `_apply_buttons`, `_apply_lighting`, `_apply_polling`,
`_apply_pointer`, `_apply_key_response`, `_update_config`,
`_mark_pending`, `_manual_apply_now`, `_persist_and_push`,
`_schedule_profile_save`, `_flush_profile_save`, `_seed_panels`,
`_seed_readouts`); device events (`_on_connected`, `_on_error`,
`_on_mode_push`, `_on_dpi_push`,
`_on_rate_push`, `_on_command_done`, `_on_busy_overlay`); libraries
(`_on_library_changed`, `_resync_macros`, `_on_gun_library_changed`,
`_resync_guns`, `_adopt_device_macros`, `_adopt_device_guns`,
`_adopt_config_guns`); shell (`_setup_tray`, `_show_from_tray`,
`_rebuild_tray_profiles`, `_toggle_autoswitch`, `_toggle_overlay`,
`_toggle_dpi_osd`, `_toggle_autostart`, `_set_log_visible`,
`_close_log_panel`, `_settings`, `_restore_window_geometry`,
`_save_window_geometry`).

### `app.controller`

| Symbol | Purpose |
| --- | --- |
| `DeviceController(demo=False)` | QThread worker owning one `DeviceService` |
| `.demo()` | True in demo mode |
| `.start()` | Start the worker thread and connection loop |
| `.call(method, *args, **kwargs)` | Queue a device call; result arrives via `command_done` |
| `.shutdown()` | Stop the worker, close the device and join the thread |
| Signals | `connected(info)`, `disconnected()`, `error(msg)`, `dpi_level_changed(level)`, `rate_changed(hz)`, `mode_changed(layer)`, `command_done(method, ok)`, `busy_changed(busy)` |

### `app.profile_store`

| Symbol | Purpose |
| --- | --- |
| `default_path()` | `config/profiles.json` next to the app or under `SM809_DATA_DIR` |
| `default_config()` | Wired factory config (from `Default.pbin`) |
| `ProfileStore(path=None, data_dir=None, device_config=None, macro_events=None, gun_rows=None)` | Sidecar-backed adapter over `wired.model.DataStore` |
| `.load()` / `.save()` / `.flush()` | Read/repair metadata; write the JSON mirror; settle deferred work |
| `.save_profiles()` | Write the full binary table (all slots) |
| `.get_setting(key, default)` / `.set_setting(key, value)` / `.set_settings(values)` | Persistent application settings |
| `.all()` / `.summaries()` / `.match_targets()` | Profiles (full config / light metadata / rule-only views) |
| `.get(pid)` / `.index_of(pid)` / `.config(pid)` | Lookups |
| `.active_id()` / `.active()` / `.set_active(pid, persist=True)` | Sticky base profile |
| `.unique_name(name, exclude_id=None)` | `Name`, `Name (2)`, ... |
| `.add(name, config, match_rules)` / `.duplicate(pid, name)` / `.delete(pid)` / `.rename(pid, name)` | Lifecycle (14-profile limit) |
| `.reorder(ids)` / `.sort_by(key)` | Match-priority order and sorting |
| `.set_config(pid, config, persist=True)` | Commit a config into the wired record |
| `.set_match_rules(pid, rules)` | Auto-switch rules |
| `.reset_config(pid)` | Factory reset of one record, name kept |
| `.apply(pid, service, config, apply_windows=True)` | Full write through `DeviceService` |
| `.embedded_macros()` / `.embedded_guns()` | Adopt device tables into editable libraries |
| `.export_pbin(pid, path)` / `.import_pbin(path)` / `.import_psf(path, macro_store)` | File interchange |

### `app.autoswitch`

| Symbol | Purpose |
| --- | --- |
| `ForegroundWatcher.current()` | `(exe, title, full_path)` for the focused window |
| `list_running_apps()` | Visible top-level windows as `{title, exe, path}` |
| `rule_for_app(apps, app)` | Narrowest usable rule for one running app |
| `rule_matches(rule, exe, title, path)` | All non-empty conditions must match case-insensitively |
| `match_profile(profiles, exe, title, path)` | First matching profile in list order |
| `AutoSwitcher(store, apply, get_applied, watcher=None, interval_ms=200, debounce_ms=200)` | Poll/debounce/switch engine |
| `.set_base(pid)` / `.base_id()` | Sticky manual profile |
| `.set_enabled(on)` / `.is_enabled()` | Master switch |
| `.poll()` | One foreground sample (timer calls this) |

### `app.autostart`, `app.elevation`, `app.paths`

| Symbol | Purpose |
| --- | --- |
| `autostart.supported()` / `launch_command()` / `is_enabled()` / `set_enabled(on)` | Per-user `HKCU\...\Run` entry, launching with `--minimized` |
| `elevation.is_admin()` | Administrator check |
| `elevation.needs_elevation(argv, environ, admin=None)` | Relaunch decision matrix |
| `elevation.relaunch_as_admin(args=None)` | `ShellExecuteW("runas", ...)`; `True` when accepted |
| `elevation.ask_continue_unelevated()` | Yes/No prompt after a declined UAC |
| `elevation.prepare_startup(argv)` | Pre-Qt gate: continue in-process or exit for the elevated child |
| `paths.is_frozen()` / `app_dir()` / `config_dir()` / `resource_path(*parts)` | Frozen-aware file locations |

### `app` logging and diagnostics

| Symbol | Purpose |
| --- | --- |
| `logging_setup.setup_logging(verbose=False, log_dir=None)` | Install console + rotating DEBUG file + crash/Qt hooks; returns the log path |
| `logging_setup.default_log_dir()` / `log_file_path()` | `logs/` and `logs/studio.log` |
| `logging_setup.RepeatCollapsingHandler` | Folds identical consecutive console lines |
| `log_bridge.LogBridge.instance()` / `.publish(text)` / `.recent()` | Singleton log stream for the GUI |
| `log_bridge.install(level=INFO)` | Attach the bridge to `sm809` and `qt` loggers once |

### `app` libraries and files

| Symbol | Purpose |
| --- | --- |
| `macro_store.default_path()` | `config/macros.json` |
| `MacroStore.all()` / `.get(mid)` / `.index_of(mid)` | Library lookups |
| `.add(name, events, loop=1, folder="", protected=False)` / `.add_with_id(mid, name, events, persist=True)` | Create/adopt |
| `.delete(mid)` / `.rename(mid, name)` / `.set_events(mid, events)` / `.set_meta(mid, loop, folder, protected)` | Mutations |
| `.save()` / `.save_if_dirty()` / `.unique_name(base, exclude_id=None)` | Persistence and naming |
| `gun_store.default_path()` | `config/guns.json` |
| `gun_store.default_rows()` / `clean_rows(rows)` | Factory 30-row shape and sanitising |
| `GunStore.all()` / `.get(gid)` / `.index_of(gid)` | Library lookups |
| `.add(name)` / `.add_with_id(gid, name, rows, persist=True)` / `.delete(gid)` / `.rename(gid, name)` | Lifecycle |
| `.set_rows(gid, rows, persist=True)` / `.set_row(gid, index, x, y, delay, persist=True)` | Row editing |
| `.save()` / `.save_if_dirty()` / `.unique_name(base, exclude_id=None)` | Persistence and naming |
| `macro_file.load_macro(path)` / `save_macro(path, macro, protected)` / `suggest_name(macro)` | Vendor `.mbin` I/O |
| `macro_file.MacroFileError` | Unusable record |
| `psf_import.parse_psf_text(text)` / `read_psf_text(path)` / `read_psf(path)` | Read official `.psf` text |
| `decode_macro_events(blob)` / `to_macros(text, data)` | Macro decoding |
| `to_config(data, warnings)` / `to_match_rules(data)` / `import_psf(path)` | Wired config migration |
| `psf_import.PsfError` | Not a usable `.psf` |

### `app` recording and input

| Symbol | Purpose |
| --- | --- |
| `recoil_recorder.RecoilRecorder.start()` / `.stop()` / `.active()` | Own the Raw Input sink |
| `.feed(dx, dy)` / `.take_delta()` | Accumulate and drain relative movement |
| `mouse_hook.mouse_action(message, mouse_data)` | Map a Windows message to `(button, down)` |
| `mouse_hook.MouseHook.start()` / `.stop()` / `.active()` | Low-level button hook |
| `.set_ignore_widgets(widgets)` | Exclude the recorder's own Stop button and other widgets |
| Signal | `mouseEvent(button, down)` |

### `app.theme`

| Symbol | Purpose |
| --- | --- |
| `dark_palette()` | Application-wide dark `QPalette` |
| `stylesheet()` | Global QSS for every widget, page, dialog and log |

### `app.panels`

| Panel | Public API and signals |
| --- | --- |
| `ButtonsPanel` | `set_manual_apply(manual)`, `set_mode(layer)`, `current_mode()`, `set_codes(codes)`, `bindings()`, `set_binding(slot, code)`, `refresh_labels()`; signals `apply_requested(bindings)`, `mode_changed(layer)`; helpers `ButtonRow`, `MouseReference` |
| `MacroPanel` | `new_macro()`, `delete_macro()`, `rename_macro_dialog()`, `import_macro_dialog()`, `export_macro_dialog(protected=False)`, `insert_event(category, code, mode, delay)`, `add_text_events(text, delay)`; signal `library_changed()`; `_Recorder` captures keystrokes |
| `GunPanel` | `new_gun()`, `delete_gun()`, `rename_gun_dialog()`; signal `library_changed()`; recorder, row editor and HOW TO USE card |
| `DpiPanel` | `active_row()`, `set_active_stage(level)`, `set_values(dpi, colors, enabled_count)`; signals `apply_requested(dpi, colors, selected)`, `active_dpi_requested(dpi, selected)`; rows are `StageRow`/`Swatch` |
| `LightingPanel` | `current_mode()`, `color_mode()`, `set_state(mode, color, params)`; signal `apply_requested(mode, color, params)`; 250 ms debounce |
| `PerformancePanel` | `set_manual_apply(manual)`, `refresh_wheel_fix()`, `set_state(polling_hz, pointer, key_response)`; signals `polling_changed(hz)`, `pointer_changed(pointer)`, `key_response_changed(ms)`; `_WheelFixWorker` runs the UAC helper off-thread |
| `AutoSwitchPanel` | `set_profiles(profiles, select_id=None)`, `set_enabled_state(on)`, `current_pid()`, `select_profile(pid)`; signals `enable_toggled(on)`, `rules_changed(pid, rules)`, `app_detected(exe, title)` |
| `ProfilesPanel` | `set_profiles(profiles, active_id, sort_key)`, `selected_id()`, `set_match_rules(pid, rules)`; signals `profile_selected(pid)`, `order_changed(ids)`, `sort_changed(key)`, `new_requested()`, `duplicate_requested()`, `rename_requested()`, `delete_requested()`, `import_requested()`, `export_requested()`, `manage_apps_requested(pid)` |
| `AppPicker` | `selected_app()`, `selected_rule()`; Browse for an `.exe`, filter, icons |

### `app.widgets`

| Widget | Public API |
| --- | --- |
| `ActionPicker` | `result_code()`, `pick_action(current_code, parent, phys, macros, guns)`; categories, search, preview, factory-default reset |
| `set_macro_resolver(fn)` / `describe_action(code)` | Macro name resolution and label rendering |
| `ColorPicker` | `selected_rgb()`; `pick_color(rgb, parent)` returns `(r,g,b)` or `None`; preset grid + HSV/RGB/hex editor |
| `ResponsiveRow` / `Card` / `Segmented` | Reusable layout/card/segmented-control helpers |
| `LogPanel` | `start()`, `clear()`, `open_log_file()`; signal `close_requested()` |
| `Overlay` | `set_appearance(position, opacity_pct, scale_pct, hold_ms, follow_cursor, monitor_index)`, `flash(value, caption, hold_ms=None)`, `flash_lines(lines, hold_ms=None)` |
| `AlertOverlay` | `set_appearance(...)`, `alert(caption, value, accent)`; persistent until dismissed |
| `place_widget(widget, pos, follow_cursor, monitor_index, margin=24)` | Position a HUD on the target monitor |

### `sm809pro`

| Symbol | Purpose |
| --- | --- |
| `actions.kb(usage, mods=0)` | Keyboard shortcut action tuple |
| `actions.fire(interval_ms=1, count=0)` | Rapid-fire action tuple |
| `actions.slot_for_physical(phys, mode)` | 1-based physical button -> firmware slot |
| `actions.physical_to_slots(codes)` / `default_button_codes()` / `default_button_code(slot)` | Vendor slot order and factory table |
| `actions.macro_slot_for(slot)` | Table index for an embedded macro |
| `defaults.button_codes()` / `defaults.config()` | Factory config pieces |
| `device.load_device_config(data_dir)` / `open_store(data_dir)` / `create_service(store, config, demo=False)` / `detect_modes(vid)` | Device helpers |
| `macros.text_to_events(text, key_delay=...)` / `macro_fits(events)` / `to_wired(events)` / `key_label(usage)` | Macro conversion |
| `protocol.raw_to_dpi(raw)` / `dpi_to_raw(display)` | Sensor DPI conversion |
| `protocol.light_mode_label(mode)` / `light_parameters(mode)` / `light_ui_controls(mode)` | Vendor Light-page metadata |

### `wired.protocol`

`checksum`, `frame`, `obfuscate`, `deobfuscate`, `wire_packet`,
`handshake_packets`, `handshake_reply_ok`, `action_label`, `action_group`,
`action_needs`, `validate_buttons`, `macro_table_slots`,
`table_budget_messages`, `table_budget_warnings`, `build_button_slots`,
`button_frames`, `encode_macro_event`, `build_macro_block`, `gun_encoded_size`,
`gun_fits`, `build_gun_block`, `macro_blocks`, `macro_frames`, `dpi_code`,
`build_dpi_block`, `light_parameters`, `light_mode_label`, `light_frame`,
`palette_block`, `high_dpi_mask`, `status_frame`, `lod_frame`, `mode_frame`,
`rate_frame`, `stage_frame`, `fixed_color_frame`, `palette_header`,
`dpi_header`, `commit_frame`, `high_dpi_frame`, `sensor_limits`,
`sensor_max_label`, `sensor_display_dpi`, `describe_apply`; classes
`PacketError`, `ActionInfo`.

### `wired.model`

| Symbol | Purpose |
| --- | --- |
| `clamp_light_mode(value)` / `clamp_light_value(name, value)` | LED range repair |
| `u8`, `set_u8`, `u16`, `set_u16`, `u32`, `set_u32` | Little-endian buffer access |
| `read_wstr`, `write_wstr`, `colorref_to_rgb`, `rgb_to_colorref` | Record string/colour helpers |
| `MacroEvent.unpack/pack`, `Bullet.unpack/pack` | 16-byte event and 8-byte bullet records |
| `ButtonEntry` | View over one `0x72C` slot: `action`, `selected_index`, `macro_index`, `shortcut_mods`, `shortcut_key`, `count`, `loop`, `fire_count`, `fire_interval`, `events`, `set_events`, `bullets`, `set_bullets` |
| `Profile` | `from_file`, `copy`, `name`, `sanitize_lighting`, `key_response`, `stage_count`, `dpi_values`, `stage_colors`, `cycle_colors`, `fixed_rgb`, `button(index)`, `buttons()` |
| `wheel_reversed(profile)` / `set_wheel_reversed(profile, value)` | Swap the physical wheel actions |
| `MacroRecord` | `name`, `folder_name`, `protected`, `loop`, `count`, `is_folder`, `events`, `set_events` |
| `GunRecord` | `name`, `folder_name`, `count`, `is_folder`, `bullets`, `set_bullet`, `set_bullets` |
| `DataStore(data_dir)` | `load`, `save_profiles`, `save_selected`, `save_macros`, `save_guns`, `profile`, `select`, `add_profile`, `delete_profile`, `reset_profile`, `rename_profile`, `rename_profile_at`, `duplicate_profile`, `reorder_profiles`, `sort_profiles`, `export_profile`, `import_profile`, `export_json`, `export_json_file`, `add_macro`, `add_gun`, `delete_macro`, `delete_gun`, `macro_names`, `gun_names`, `backup` |

### `wired.bridge`

`rate_hz`, `rate_index`, `dpi_to_display`, `dpi_from_display`,
`ref_events_to_wired`, `wired_events_to_ref`, `macro_fits`,
`macro_binding_problem`, `gun_rows_to_wired`, `gun_rows_fit`,
`gun_binding_problem`, `binding_from_entry`, `binding_to_entry`,
`validate_binding`, `table_budget_problem`, `default_pointer`,
`profile_to_config`, `config_to_profile`, `describe_binding`, `dpi_display`,
`light_label`.

### `wired.device`

| Symbol | Purpose |
| --- | --- |
| `DeviceService(config, store)` | Link owner and apply engine |
| `.connect()` / `.disconnect()` / `.ensure()` / `.present()` / `.status()` | Connection lifecycle |
| `.handshake()`, `.status_frames()`, `.read_version()`, `.version_matches()` | Startup sequences |
| `.send_feature(packet)` / `.read_feature()` / `.send_block(block)` / `.raw_packet(cmd, args)` / `.packet_checksum(packet)` | Low-level I/O |
| `.apply(profile)` | Complete diffed profile write |
| `.set_stage(stage)` | Vendor DPI-stage sequence |
| `.log(text, level="debug")` | Optional diagnostic callback |
| `DeviceError`, `ApplyResult`, `DeviceStatus` | Error/result/status records |

### `wired.transport`, `config`, `keys`

| Symbol | Purpose |
| --- | --- |
| `HidLibrary` | `enumerate`, `find`, `find_control`, `find_monitor`, `open`, `close`, `set_feature`, `get_feature`, `write_block`, `cancel_io`, `read_input_once` |
| `HidTransport(config)` | `connected`, `enumerate`, `open`, `close`, `set_feature`, `get_feature`, `write_block`, `inject_event`; demo replies built in |
| `describe_interfaces(config)` | Human-readable HID interface report |
| `load_config(path)` / `DeviceConfig.save(path)` / `to_ini_text()` | `Data.ini` parsing/writing; `sensor`, `key`, `raw_button`, `button_is_computed`, `distance_value_for_stage` |
| `key_name(vk)`, `key_id_for_vk(vk)`, `vk_for_key_id(id)`, `key_id_name(id)`, `shortcut_name(key, mods)`, `normalize_vk(vk)` | Vendor key mapping |

### `wired.winspi`, `wheel_direction`, `paths`

| Symbol | Purpose |
| --- | --- |
| `winspi.double_click_ms(index)` / `mouse_speed_value(index)` | UI index -> Windows values |
| `winspi.set_double_click_time`, `set_mouse_speed`, `set_enhance_pointer`, `set_wheel_lines` | Apply pointer settings |
| `winspi.PointerSettings.apply(speed, scroll, double, enhance, onepage)` | Apply only changed values |
| `wheel_direction.device_instances()` / `read_state()` | SM809 wheel registry state |
| `wheel_direction.apply(invert)` / `apply_elevated(invert)` | Per-device `FlipFlopWheel`, with UAC helper |
| `WheelState.inverted` / `.partial` / `.describe()`; `WheelResult` | Result reporting |
| `paths.ensure_data_dir()` / `logo_path()` / `is_frozen()` | Portable data and seed copy |


