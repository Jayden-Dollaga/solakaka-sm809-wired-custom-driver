# SM809 Mouse Software — Whole-App Rebuild Overview

Static reverse-engineering report. No part of this document derives from running the target; every statement is based on the shipped files (PE images, DuiLib XML, data files) and the Ghidra/REA analysis already stored under `analysis\`.

Status labels used throughout:

- **[C] Confirmed** — directly visible in disassembly/decompilation, a resource file, or a data file.
- **[I] Inferred** — follows from confirmed code but is one reasoning step away (e.g. meaning of a field, purpose of a flag).
- **[U] Unknown** — not resolvable from the available static evidence.

Evidence notation:

- `EXE:FUN_00418a40@0x00418a40 (FUN_00418a40__00418a40.c:118)` → file `analysis\dump\exe\pseudocode\FUN_00418a40__00418a40.c`, line 118.
- `DRV:FUN_10001c00@0x10001c00 (FUN_10001c00__10001c00.c:26)` → `analysis\dump\MSDriver\pseudocode\...`.
- `RES:res/main.xml:107` → resource XML line.
- `DAT:Data.ini:2` → shipped data file line.

---

## 1. Package inventory

Files in the install directory (root of the extracted package):

| File | Size / date | Role | Status |
|---|---|---|---|
| `SM809 mouse Software.exe` | 502,768 B, 2025-04-10 | Main GUI application (32-bit PE, MFC/DuiLib). | [C] `analysis\pe-headers.txt` |
| `MSDriver.dll` | 49,152 B, 2016-11-04 | HID transport DLL (SetupAPI + HID.DLL). | [C] `analysis\exports-MSDriver.json` |
| `Hook.dll` | 40,960 B, 2020-03-27 | Low-level keyboard/mouse hooks for macro recording. | [C] `analysis\dump\Hook\pseudocode` |
| `DuiLib.dll` | 1,564,672 B, 2024-09-09 | DirectUI framework (XML skin engine). | [C] imports/resources |
| `DuiLib_d.dll` | 1,479,168 B, 2022-10-27 | Debug build of DuiLib, unused by the release EXE. | [I] |
| `IsTask.dll` | 67,584 B, 2019-03-21 | Not referenced anywhere in the EXE (no string, no LoadLibrary). Vestigial. | [C] no `IsTask` string in `analysis\strings-exe.txt` |
| `msvcp140.dll`, `vcruntime140.dll`, `msvcp120.dll`, `msvcr120.dll` | — | VC++ runtimes. | [C] |
| `Data.ini` | 1,331 B | Device/profile defaults (VID, PID, sensor, password, button map). | [C] |
| `Data\Data.bin` | 8 B | Selected-profile index. | [C] |
| `Data\profile.bin` | 1,649,760 B | 14 × 0x1CC50 profile records. | [C] |
| `Data\Default.pbin` | 117,840 B | One 0x1CC50 factory-default profile. | [C] |
| `Data\macro.bin` | 1,712 B | 2 × 0x358 macro records. | [C] |
| `Data\gun.bin` | 0 B | Gun (recoil) records (0 × 0x240). | [C] |
| `res\*.xml`, `res\skins\*`, `Language\...\lan.xml` | — | DuiLib UI definitions and localized text. | [C] |
| `logo.ico`, `logo.png` | — | Icon / logo source. | [C] |

Extra static facts:

- Authenticode signer: `CN="Shenzhen Jinxin Electronics Co.,Ltd"`, TrustAsia ECC Code Signing CA G3, validity expired 2026-02-25. [C] `analysis\signature.txt`
- Leaked PDB path: `D:\G\Work\Me\Jack Ma\571\AP\Code(-3311-32KEY)\Bin\MouseDriver.pdb` (offset 0x2A98B). The `3311` in the build folder matches `Sensor=3311` (=0x0CEF) in `Data.ini`, so this EXE is the 0xCEF-sensor build with a 32-key variant. [C] path; [I] interpretation.

---

## 2. Process entry, single instance, window creation

`EXE:WinMain FUN_00408e50@0x00408e50`

1. **[C]** Creates named mutex `"Mosue Driver Configure Jack Ma"` (typo "Mosue" is in the binary). If it already exists, the second instance looks up the running window (`FindWindowW` for the app's window class) and sends message `0x40D` to it, then exits — this raises the existing window.
2. **[C]** `CoInitialize` / `OleInitialize` (GDI+ and shell dialog support).
3. **[C]** Allocates the main object (`operator new 0x1AF8`), runs the constructor `FUN_00414980`, then calls DuiLib `WindowImplBase::Create` with style `0x96C80000` and initial size 800×572 (`0x23C`).
4. **[C]** The window is shown only when `DAT_00432aa4 == 1` (device connected), there are no command-line arguments, and `CMainWnd+0x16D0 == 1`. Otherwise it starts hidden (tray-only).
5. **[C]** Standard modal message loop, then virtual `vtable+0x14(1)` (close) and `Term`.

**[I]** `FUN_004158d0` (startup body) is the DuiLib `OnCreate`/init virtual, because it is only reachable through the window vtable and is called once after `Create` with the window object.

**[C]** The window is created at 800×572 while `res\main.xml:2` declares `size="1280,750"`. DuiLib does not rescale to the XML size: the DLL contains no internal call to `SetInitSize`/`GetInitSize` (objdump xref scan), the EXE does not import them, and the XML layout is fluid (largest fixed child 320×100). The `disable_window_ver`/`ring_ver` overlays are hard-coded 1280×750 masks that over-cover the client area. See §15 item 1.

---

## 3. Runtime object model (what must be rebuilt first)

The whole UI is one `CMainWnd` object of 0x1AF8 bytes that *embeds* five page controllers and three sub-objects.

`EXE:FUN_00414980@0x00414980 (constructor)`, `EXE:FUN_004158d0@0x004158d0:78-89`

| Offset | Size | Member |
|---|---|---|
| +0x000, +0x010, +0x020, +0x024, +0x028, +0x02C | — | Six `CMainWnd` vtable pointers (DuiLib multiple inheritance). |
| +0x030 | — | `CPaintManagerUI` (all `FindControl` calls use `param_1+0x30`). [C] |
| +0x764 | — | `ReceiverImpl<int,SkinChangedParam>` vtable (skin-change receiver). [C] |
| +0x774 … +0x79C | 11 × 4 | `MSDriver.dll` procedure pointers, in this order: `Set_VIDPID`, `Open_DevMonitor`, `Close_DevMonitor`, `Open_FeatureDevice`, `Close_FeatureDevice`, `SetFeature`, `GetFeature`, `Open_ReportDevice`, `Close_ReportDevice`, `WriteUSB`, `ReadUSB`. [C] `FUN_004158d0:557-579` |
| +0x7A0 | 0x1C0 | `CButtonPage` (vtable at +0x7A0; paint manager +0x7B0; HWND +0x7B4). [C] |
| +0x960 | 0x138 | `CPerformancePage` (+0x970 PM, +0x974 HWND). [C] |
| +0xA98 | 0xA8 | `CLightPage` (+0xAA8 PM, +0xAAC HWND). [C] |
| +0xB40 | 0x2F8 | `CMacroPage` (+0xB50 PM, +0xB54 HWND; recording buffer +0xB64, 0x280 bytes = 40 events × 16). [C] |
| +0xEF8 | 0x190 | `CGunPage` (+0xF08 PM, +0xF0C HWND). [C] |
| +0x1584 | 4 | `HMODULE MSDriver.dll`. [C] |
| +0x1588 | 0x140 | 64 × 5-byte raw button map from `Data.ini [BUTTON]`. [C] `FUN_004158d0:243-279` |
| +0x16C8 | 8 | LOD (lift-off distance) byte per DPI stage; indexed by the active stage in command 0x04. [C] read at `FUN_00418a40:343`; filled at startup from `Data.ini Distance_Value` (see §5.3/§11.1). |
| +0x16D0 | 4 | Connected flag. |
| +0x16DC … +0x171C | 17 × 4 | Cached control pointers: exit/min/skin/setting/logo/key/performance/light/macro/gun buttons, profile combo, add/delete/menu profile, profile name edit, apply/reset, config_tab/main_tab. [C] `FUN_004158d0:471-516` |
| +0x1720 | 4 | `CMenuWnd*` context menu (created on tray right-click). [C] |
| +0x1724 | — | `CTrayIcon`. [C] |
| +0x1AF0 | 4 | Password-obfuscation enabled flag (1 when `Data.ini Password` has 6 chars). [C] |
| +0x1AF4 | 4 | `CDPIMsg*` DPI overlay window pointer. [C] |

The five page classes are DuiLib "virtual windows" registered in the constructor:

```
AddVirtualWnd(L"ButtonPage"), L"PerformancePage", L"LightPage", L"MacroPage", L"GunPage"
```
[C] `FUN_00414980:150-164`

**[I]** Each page is a `CNotifyPump` so `main.xml` can host the page XML inside a `TabLayout`/`TabPage` without separate HWNDs; the page objects own the controls through the shared `CPaintManagerUI`.

Page common fields (all five follow the same pattern):

- page+0x10 = `CPaintManagerUI*` (set to `mainWnd+0x30`), page+0x14 = main `HWND`.
- Page init function is `vtable+4`, called in page order button → performance → light → macro → gun. [C] `FUN_004158d0:532-536`

---

## 4. Startup sequence (rebuild order)

Everything below is driven by `EXE:FUN_004158d0@0x004158d0` unless stated otherwise.

1. **Bind page contexts** — set `+0x7B0/+0x970/+0xAA8/+0xB50/+0xF08 = mainWnd+0x30` and `+0x7B4/… = main HWND`. [C] lines 78-89
2. **Read `Data.ini`** (path = executable directory, `FUN_00401e90`; literal `Data.ini` at VA 0x42828C). All reads use the `[Default]` section. Helper `FUN_00405b80` is a `vswscanf` wrapper that parses hex/CSV strings into caller buffers. [C] lines 92-420

   Keys and semantics (values below are the shipped ones):

   | Key | Shipped value | Type / destination | Meaning |
   |---|---|---|---|
   | `VID` | `04d9` | 4-hex → `DAT_00432028` | USB vendor ID. [C] |
   | `PID` | `A09F` | 4-hex → `DAT_0043202C` | USB product ID. [C] |
   | `DPI` | `8` | int | Default number of enabled DPI stages. [I] |
   | `Sensor` | `3311` (=0x0CEF) | int → `DAT_00432AD8` | Sensor type; selects all DPI/limit logic. [C] |
   | `Distance` | `0` | int → `DAT_00432ACC` | Lift-off (LOD) feature present/enabled. [C] flag use at `FUN_00418a40:359`, `FUN_0041bd40:116` |
   | `Distance_Min` | `0` | `%02x` → `DAT_00432AD4` | Lower bound of the lift-off-distance slider. [C] `FUN_004158d0:194-240`, `FUN_0041c490:124` |
   | `Distance_Max` | `2` | `%02x` → `DAT_00432AD0` | Upper bound of the lift-off-distance slider. [C] `FUN_004158d0:194-240`, `FUN_0041c490:125` |
   | `Distance_Value` | `0,1,2,0,0,0,0,0` | CSV of 8 ints, each `%d` written to `CMainWnd+0x16C8+i` | LOD level code per DPI stage; command 0x04 sends `CMainWnd+0x16C8+activeStage`. [C] `FUN_004158d0:415-424`, `FUN_00418a40:343`, disasm `0x41654E` |
   | `Password` | `FB1570` | string | If length == 6, enables packet obfuscation and stores the 6 chars in `DAT_00432AB1..AB6`. [C] lines 327-345 |
   | `Ver_H`, `Ver_L` | `2`, `1` | int → `DAT_00432AC4`, `DAT_00432AC0` | Expected firmware version bytes. [C] |
   | `Update` | `0` | int → `DAT_00432ABC = (v!=0)` | Enable firmware check/updater on connect. [C] |
   | `[BUTTON]` keys `1..64` | e.g. `1=01,00,F0,00,1` | 5 hex bytes → `+0x1588 + 5*(n-1)` | Per-physical-button raw report fallback + "use computed" flag. [C] |

3. **Load the factory profile** `Data\Default.pbin` (0x1CC50 bytes) into `DAT_00432AE0`. [C] lines 290-296
4. **Parse all 64 button entries** into `+0x1588…+0x16C7`. [C] lines 243-279
5. **Create window icon** from `logo.ico`/embedded bitmap, set big/small icons (WM_SETICON 0x80). [C] lines 425-455
6. **Load language** `Language/lan.xml`; set caption text from resource key `mouse_name_text`; create tray icon with the same text as tooltip. [C] lines 456-531
7. **Cache control pointers** (`exit_btn`, `min_btn`, `skin_btn`, `setting_btn`, `logo_btn`, tab buttons, `profile_combo`, `btn_add_profile`, `btn_delete_profile`, `btn_menu_profile`, `edit_profile_name`, `btn_apply`, `btn_reset_profile`, `config_tab`, `main_tab`). [C] lines 471-516
8. **Init pages** via `vtable+4` for button/performance/light/macro/gun. [C] lines 532-536
9. **Load user data** `FUN_00416c70`: read `Data\Data.bin` (selected index), load profile list (`FUN_004037f0` reads `Data\profile.bin`; if missing, builds defaults from `Default.pbin`), load `Data\macro.bin` (0x358 records) and `Data\gun.bin` (0x240 records), fill `profile_combo`, select the saved profile, copy it into the working-profile buffer `DAT_0044F730`, refresh UI. [C] lines 537-538; `FUN_00416c70:59-232`
10. **Start worker thread** `CreateThread(FUN_00414910)` — the thread that applies profiles to the device/Windows on demand. [C] line 538
11. **Load `MSDriver.dll`** (path = exe dir + `MSDriver.dll`) and resolve the 11 exports into `+0x774…+0x79C`. [C] lines 543-580
12. **Open the device stack**:
    - `Set_VIDPID(VID, PID)`
    - `Open_DevMonitor(hwnd, 0x52D, 0x52E)`
    - `Open_FeatureDevice()`
    - `Open_ReportDevice()` → return value decides `DAT_00432AA4`
    - `CMainWnd+0x16D0 = 1`, then if connected: `FUN_004196b0` (0x83/0x8B/0x03 handshake), `FUN_0041bbc0` (AADD3B62 challenge), and if `Update` flag set, `FUN_0041b850` (firmware version check; on mismatch shows dialog and destroys the window to run the updater).
    [C] lines 584-601

---

## 5. UI structure and how the parts connect

### 5.1 Main window

- Skin: `res\main.xml` (1280×750). Top tabs: `key_btn` (button page), `performance_btn`, `light_btn`, `macro_btn`, `gun_btn`. Profile row: `profile_combo`, `btn_add_profile`, `btn_delete_profile`, `btn_menu_profile`, `edit_profile_name`, `btn_apply`, `btn_reset_profile`. Overlays: `ring_ver` (full-size translucent wait overlay containing a `<Ring name="ring">` spinner, line 107-108), `disable_window_ver` (blocker while modal), caption buttons `exit_btn`, `min_btn`, `logo_btn`, `setting_btn`, `skin_btn`.
- `EXE:FUN_004176f0@0x004176f0` is the `Notify` handler:
  - `click` → forwards to page dispatch (offset -0x20 = window base).
  - `selectchanged` on any combo → resets/updates downstream controls (combo pointers compared against +0x16C8/0x16CC/0x16D0/0x16D4/0x16D8, which are **page-object-relative** fields, i.e. window base +0x16E8… originally misread; treat as combo handles).
  - `itemselect` on `profile_combo` → sets `DAT_00432AA8`, points `DAT_00432AA0` at the chosen 0x1CC50 record, calls performance-page refresh and `FUN_00417540`.
  - `killfocus` on the name edit → `FUN_00417d10` (rename).
- `EXE:FUN_004178e0@0x004178e0` handles caption buttons: exit, minimize, profile menu (`CMenuWnd::Init("profilemenu.xml")` at the button position), reset (confirm with `reset_profile_text`, copy `Default` → selected, re-post apply, show ring overlay, enable `disable_window_ver`), apply (post `0x670` to the worker thread, show ring), website, ring toggle.

### 5.2 Button page (`key_btn`)

- Page class `CButtonPage`, skin `res\buttonpage.xml`, object base `+0x7A0`.
- `EXE:FUN_00406db0@0x00406db0` is the per-slot action menu:
  - Menu `buttonmenu.xml` lists all actions (confirmed by the `CompareNoCase` chain and `FUN_004081e0` label table).
  - Action code is stored at `buttonEntry + 0x219`.
  - Selecting `shortcut` builds `CShortcutWnd` (modal, `shortcut.xml`), writes key at `+0x22C`, modifier mask at `+0x22D`, action `0x15`.
  - Selecting `fire_click` builds `CFireClickWnd` (modal, `fireclick.xml`), reads back `+0x82C` (click count) and `+0x830` (interval), action `0x0A`. [C] lines 666-714
  - Selecting `select_macro` builds `CSelectMacroWnd` (`selectmacro.xml`), result into `+0x220`/`+0x224`/`+0x5A8`, action `0x16`.
  - `set_gun` opens `CSelectGunWnd` (`selectgun.xml`), result = gun index.
  - After a successful dialog the code sets `disable_window_ver` back to 0 and refreshes the label via `FUN_004081e0`.
- `EXE:FUN_004081e0@0x004081e0` maps action code → localized text key (`click_text`, `menu_text`, `scroll_text`, `fire_click_text`, …; for `shortcut` it formats the captured key with `FUN_00402370`; for macro it shows macro name).
- `EXE:FUN_00417540@0x00417540` refreshes the whole page from the selected profile: button labels, page mode option, performance values, light controls, and the LED options.
- Action code table (confirmed in `FUN_00406db0` / `FUN_004081e0`): `00 button_off`, `01 click`, `02 menu`, `03 scroll`, `04 forward`, `05 backward`, `06 dpi_cycle`, `07 dpi_up`, `08 dpi_down`, `09 double_click`, `0A fire_click`, `0B scroll_up`, `0C scroll_down`, `12 three_click`, `15 shortcut`, `16 select_macro`, `19 send_gun`(gun), `1A mode_switch`, `20 cut`, `21 copy`, `22 paste`, `23 open`, `24 save`, `25 find`, `26 redo`, `28 select_all`, `29 print`, `2A close_windows`, `2B swap_windows`, `2C show_desktop`, `2D run_command`, `2E lock_pc`, `2F new`, `32 light_mode_switch`, `39 set_left_macro`, `40 media_player`, `41 play_pause`, `42 media_stop`, `43 pre_track`, `44 next_track`, `45 volume_up`, `46 volume_down`, `47 mute`, `48 browser_home`, `49 browser_favorites`, `4A browser_forward`, `4B browser_backward`, `4C browser_stop`, `4D browser_refresh`, `4E browser_search`, `4F email`, `50 calculator`, `51 my_computer`, `68 report_up`, `69 report_down`, `70 report_cycle`, `71 juji`, `79 set_gun`.

### 5.3 Performance page (`performance_btn`)

- Skin `res\performancepage.xml`; object base `+0x960`; init `EXE:FUN_0041c490@0x0041c490`; refresh `EXE:FUN_0041c7f0@0x0041c7f0`.
- Control groups: profile DPI-stage combo (`max_dpi_combo`), report-rate radios `prate_N_option`, DPI-stage radios `mouse_dpi_btn_N`, DPI value labels `mouse_dpi_value_N`, DPI sliders `mouse_dpiN_slider`, per-stage LED color buttons `mouse_dpi_colorN`, Windows pointer sliders (`mouse_move_speed_slider`, `scroll_speed_slider`, `double_click_speed_slider`), checkboxes `enhance_pointer_checkbox` / `one_page_checkbox`, lift-off `lift_of_distance_slider`, `distance_checkbox`, `distance_slider_ver`, key response `key_response_slider`, label `label_key_respsonse`.
- Profile offsets consumed by the refresh: report rate `+0x80`, active stage `+0x84`, DPI values `+0x88 + 4*i` (8 values), LED colors `+0xD0 + 4*i` (8 COLORREF), mouse speed `+0x64`, scroll lines `+0x68`, double-click `+0x6C`, enhance pointer `+0x70`, one-page scroll `+0x74`, LOD `+0x130`, lift enable `+0x134`, key response ms `+0x138`, stage count `+0x139`. [C] `FUN_0041c7f0`
- `EXE:FUN_0041d110@0x0041d110` sets slider ranges and the "max DPI" label per sensor (table in §10).
- `EXE:FUN_0041d620@0x0041d620` enables stage 0..count-1 and disables the rest.
- `EXE:FUN_0041d0a0@0x0041d0a0` writes the stage count when the combo changes and clamps the active stage.
- LOD wiring (resolved): the slider `lift_of_distance_slider` (page+0x11C) gets its bounds from the hex INI keys — min = `Distance_Min` (global `0x432AD4`), max = `Distance_Max` (global `0x432AD0`) — `FUN_0041c490:124-125`. The 8 per-stage LOD bytes sent in command 0x04 are parsed from `Distance_Value` (8 decimal values, comma-separated) in `FUN_004158d0` and stored as bytes at `CMainWnd+0x16C8+i`; the parse uses `%d` × 8 into successive *byte* addresses (`lea 0x7..0(profile+0x16C8)` at `0x41654E-0x41656E`), so each parsed value's low byte lands in one stage slot. [C] `FUN_004158d0:415-424`, `FUN_00418a40:342-346`.

### 5.4 Light page (`light_btn`)

- Skin `res\lightpage.xml`; object base `+0xA98`; init `EXE:FUN_0040deb0@0x0040deb0`.
- 12 mode options (`light_mode_option_1..12`), `brightness_slider` (0..255), `frequency_slider` (0..4, the vendor "breathing" speed selector despite the name), `length_slider` (0..4, labelled "length"), color palette (`color_pallet`), eight cycle-color buttons (`btn_cycle_color_1..8`), two radios `option_color_mode_1/2` (Fixed / Cycle = 0/1), RGB edit boxes (`r_edit`, `g_edit`, `b_edit`), `btn_fix_color`.
- `EXE:FUN_0040eaf0@0x0040eaf0` decides which rows are visible per mode: the brightness row for every mode except 0 and 2; the breathing slider (`frequency_slider` -> profile `+0xF8`) only for modes 2,3,4,9,10; the length slider plus the Fixed/Cycle radios only for modes 6,7.
- `EXE:FUN_0040e4d0@0x0040e4d0` stores the controls into the profile: `brightness_slider` -> `+0xF4`, `frequency_slider` (breathing) -> `+0xF8`, `length_slider` -> `+0x100`, `option_color_mode_1/2` -> `+0xFC` (written as 0/1 only, `EXE:FUN_0040e460`).
- `EXE:FUN_0040e9c0@0x0040e9c0` pushes a COLORREF (`0x00BBGGRR`) into the three edit boxes as R = low byte, G = next, B = next. [C] → this fixes the RGB byte order used on the wire.
- Profile light block: mode `+0xF0` (0..11), brightness `+0xF4` (0..255), breathing `+0xF8` (0..4), colour mode `+0xFC` (0/1 only), length `+0x100` (0..4), fixed color `+0x104..+0x106`, 8 cycle colors `+0x110..+0x12F` (raw 32-byte COLORREF array).
- **`+0xFC` is a two-way index, not a frequency value:** `EXE:FUN_00417540@0x00417540` reads `param_1 + 0xb2C + profile[0xFC]*4` and calls the virtual method at `+0x1BC` on the resolved object. A committed byte above 1 indexes past the two-entry table and can leave the mouse unresponsive until the vendor driver rewrites the profile. Never expose this field as a range slider; the studio's old 1..255 "Frequency" slider was the cause of the reported lock-up (saved value 126).

### 5.5 Macro page (`macro_btn`)

- Skin `res\macropage.xml`; object base `+0xB40`; init `EXE:FUN_0040ee10@0x0040ee10` (also loads `Hook.dll` and resolves its exports; queries QPC frequency).
- Controls: `macro_combo`, `btn_add/delete/menu_macro`, `edit_macro_name`, `macro_delay_option_1..3`, `edit_default_delay`, `btn_record`, `macro_action_list`, move up/down, delete/clear, `edit_macro_action`, `edit_macro_delay`, `macro_key_hor`, `macro_delay_hor`, `macro_mouse_action_combo`, `edit_loop_time`, folder buttons, `macro_list`, `btn_insert_move`, `macro_mouse_move_hor`, `edit_macro_action_x/y`, `edit_insert_x/y`.
- Recording: `FUN_00410b80` (start), `FUN_00410ca0` (stop), `FUN_00410d10` (event intake from window messages 0x500/0x501), `FUN_004111b0` (insert 16-byte event at `page+0x24 + index*0x10`, shifting the tail upward), list editing `FUN_0040fb30`/`FUN_0040fb70` (delay clamps to 10..0xFFFF).
- 40-event cap (`page+0x2A4` count; buffer 0x280 bytes = 40 × 16). [C] constructor memset at `FUN_00414980:53` + insert logic.
- Event field layout (16 bytes at `page+0x24 + i*0x10`; the same unit appears at macro-record +0xD8 and button-entry +0x5AC): [C]

  | Offset | Size | Meaning |
  |---|---|---|
  | +0 | 1 | unused (never read by recorder, list UI or upload encoder) |
  | +1 | 1 | opcode / key id: `F0` left, `F1` right, `F2` middle, `F3`/`F4` X-buttons, `F6` inserted mouse-move, or a VK-mapped key id |
  | +2 | 1 | state: `1` press, `2` release, `0` no-edge (programmatically inserted move) |
  | +3 | 1 | unused |
  | +4 | u16 | delay in ms (default 10 after every insert, clamped to 0xFFFF) |
  | +8 | dword | payload A — X coordinate for move events, otherwise forwarded dword |
  | +12 | dword | payload B — Y coordinate for move events, otherwise forwarded dword |

  Evidence: intake writes opcode/state/delay at `FUN_00410d10:155-183` (disasm `0x410fea`/`0x410ff2`/`0x410fe1`); insert copies four dwords at `FUN_004111b0:36-40`; the list label reads the opcode byte at +1 (`FUN_00411ae0:32`, `this + idx*0x10 + 0x25`); the move-event insert sets `F6`, delay 10, X, Y at `FUN_0040f1e0:206-209`.
- Key id mapping: `FUN_004022f0` looks the message code up in a 12-byte-row table at VA `0x4255E0` (`vk, key_id, scan_code`); if the key id is in `[4, 0x45]` it re-resolves the id from the row whose stored scan code equals `MapVirtualKeyW(vk, 0)`, i.e. keyboard macros are stored physically (scan-code), not by character. [C] `FUN_004022f0:11-33`, dump at RVA 0x255E0 (`A→0x04`, `B→0x05`, …).
- Delay modes: `macro_delay_option_1..3` set `page+0x20` to `0/1/2`. [C] `FUN_0040f6e0:13-25`
  - `0` — no timing capture: every event gets the constant 10 ms.
  - `1` — fixed delay: the u16 from `edit_default_delay` (`page+0x2B8`, parsed with `_wtoi` at record start) is used for every event.
  - `2` — recorded timing: elapsed ms since the previous event, measured with `QueryPerformanceCounter` when `QueryPerformanceFrequency` succeeded at init (`page+0x2EC`) and with `GetTickCount` otherwise, capped at 0xFFFF. [C] `FUN_00410d10:110-155`, `FUN_0040ee10:174-175`
- Macro record file format: `Data\macro.bin`, record size `0x358`; name at +0x00 (wide string), loop count at +0xC8, event count at +0xCC, folder flag at +0xD4, event array at +0xD8 with 40 × 16 bytes = 0x280, which exactly fills the record (0xD8 + 0x280 = 0x358). [C] record copy at `FUN_004116c0:20-27` and `FUN_00406db0:800-804` (name 0x32 wchars, name2 at +0x64, count `pwVar12[0x66]` = +0xCC, events from +0xD8).

### 5.6 Gun page (`gun_btn`)

- Skin `res\gun.xml`; object base `+0xEF8`; init `EXE:FUN_0040a080@0x0040a080`.
- 30 bullet rows with `edit_zidan_x_N`, `edit_zidan_y_N`, `edit_zidan_delay_N`, up/down buttons; `gun_combo`, `gun_list`, `edit_gun_name`, folder add/delete/menu, `zidan_combo`.
- Gun record file `Data\gun.bin`, size `0x240`, loaded as a plain stream of records (`FUN_00416c70:172`). Layout confirmed from the "add gun"/"add gun folder" dialogs and defaults:
  - +0x00 `wchar_t name1[50]` (gun name), +0x64 `wchar_t name2[50]` (folder name) — both written with `wcscpy_s(...,50,...)`. [C] `FUN_0040b080:73-77`
  - +0xC8 byte = bullet count, initialized to `0x1E` (30). [C] `FUN_0040b080:72`
  - +0xD0 dword = 1 for folder records (the folder variant zeroes +0xD4..+0x23F instead of filling bullets). [C] `FUN_0040c9c0:65-70`
  - +0xD8 .. +0x23F: 30 × 12-byte bullet rows (`0xD8 + 30*12 = 0x240` exact). Row = int32 x @+0, int32 y @+4, u16 delay @+10, delay initialised to 10 for every row. [C] `FUN_0040b080:78-84` (init), `FUN_0041ab50:334-451` (reads x @row+0, y @row+4, delay @row+10). The 0x79 encoder transmits `abs(x)`, `abs(y)` as single bytes, so record values outside 0..255 truncate on the wire [I] whether the UI can produce them.

### 5.7 Modal windows and dialogs

All are stack-constructed `WindowImplBase` subclasses created with `CWindowWnd::Create(..., class="ShortcutWnd"/"SelectGunWnd"/..., style 0x90000000, 800,800)` then `CenterWindow` + `ShowModal`. The skin XML is returned by a virtual "GetSkinFile" function (single-line `CDuiString(L"xxx.xml")`).

| Class | Skin file | Trigger |
|---|---|---|
| `CFireClickWnd` | `fireclick.xml` (448×288) | Button action `fire_click` [C] `FUN_00406db0:674-714` |
| `CShortcutWnd` | `shortcut.xml` | Button action `shortcut` [C] `FUN_00406db0:620-664` |
| `CSelectMacroWnd` | `selectmacro.xml` | Button action `select_macro` [C] `FUN_00406db0:749-780` |
| `CSelectGunWnd` | `selectgun.xml` | Button action `set_gun` [C] `FUN_0041df70` |
| `CSelectColorWnd` | `selectcolor.xml` | `btn_fix_color` / LED color buttons [C] `FUN_0041d740` |
| rename dialog | `editname.xml` | profile/macro/gun rename [C] `FUN_00409330` |
| `CMsgWnd` | `msg.xml` | warnings/confirmations (`warning_title_text`, `no_connect_device_text`, `reset_profile_text`, `update_fw_text`) [C] `FUN_0041c340` |
| `CDPIMsg` | `dpi.xml` (150×150) | message `0x469` (DPI changed) [C] `FUN_004090b0`, `FUN_00415000` |

`CDPIMsg` creation (in `FUN_00415000`, message 0x469): builds the text `"DPI :" + FUN_00403d70(value)`, and if no overlay exists, allocates 0x7F0 bytes, constructs `CDPIMsg`, `Create` at 800×800 with style `0x90000000`, starts a 2-second timer (ID 0x34). The timer handler (WM_TIMER 0x113) kills the timer, closes and frees the overlay.

**Ring overlay**: `ring_ver` is part of `main.xml` (lines 107-108) with a DuiLib `<Ring>` control drawing `skins/ring.png`; shown when applying and hidden at the end of `FUN_00418a40`. `res\ring.xml` exists but no code path loading it was found — likely legacy. [C] main.xml; [I] unused.

**Fireclick/dpi/editname XML-name functions** have no direct callers in the decompiled dump because they are virtual `GetSkinFile` implementations; the mapping to windows is inferred from class vtables and matching control names. [I]

### 5.8 Menus and tray

- `CMenuWnd` instances load: `profilemenu.xml` (profile menu), `buttonmenu.xml` (button actions), `macromenu.xml` / `macrodirmenu.xml` (macro page), `gunmenu.xml` / `gundirmenu.xml` (gun page). [C] `FUN_004178e0:90`, `FUN_00406a40:64`, `FUN_0040f1e0:137/167`, `FUN_0040a3d0:76/99`
- Tray right-click (message `0x401`, wParam `0x205`) creates `CMenuWnd` at the cursor (`y - 50`) and calls `Init()`/`ResizeMenu()`. The XML name is not an explicit literal at the call site; `res\traymenu.xml` contains exactly the two commands handled by `0x403` (`configuration`, `exit`), so the tray menu is `traymenu.xml`. [C] message path; [I] XML binding.
- Menu items post message `0x403` to the main window with a buffer whose first wide string is the item name. `FUN_00415000` compares it case-insensitively against: `configuration`, `exit`, `import_profile`, `export_profile`, `rename_macro_dir`, `import_macro_dir`, `export_macro_dir`, `export_pw_macro_dir`, `rename_macro`, `import_macro`, `export_macro`, `export_pw_macro`, `rename_gun_dir`, `import_gun_dir`, `export_gun_dir`, `export_pw_gun_dir`, `rename_gun`, `import_gun`, `export_gun`, `export_pw_gun`, and otherwise forwards to the button page handler `FUN_00406db0`. [C]
- `configuration` → if connected and window hidden, show/un-minimize/foreground it; otherwise `FUN_0041b6f0` (modal "no device connected" warning). `exit` → `DestroyWindow`. [C]

### 5.9 Message map (`FUN_00415000`)

| Message | Payload | Effect |
|---|---|---|
| `0x002` WM_QUIT | — | `PostQuitMessage(0)`. |
| `0x401` WM_USER+1 (tray notify) | wParam `0x202` (dbl-click) or `0x205` (right-up) | Show window; or create tray menu. |
| `0x403` (menu click) | wParam = wide-string buffer | Command dispatch (above). |
| `0x40D` | — | Show/foreground existing window (second instance). |
| `0x467` | — | Refresh button page: `FUN_00408bc0(page, profile+0x14C)` then `FUN_004081e0` for slots 0..63. |
| `0x469` | lParam = DPI value | Show/update DPI overlay. |
| `0x500` / `0x501` | Hook.dll event | Macro recording intake (`FUN_00410d10`). |
| `0x52D` | wParam = event word, lParam = value | Device event (see §7). |
| `0x52E` | wParam = present flag | Device connect/disconnect. |
| `0x113` WM_TIMER | wParam `0x34` | Close DPI overlay. |

**[C]** No handler exists anywhere for `0x502` (mouse-move hook message) or `0x5F5` (device-removed message posted by `MSDriver!FUN_10002090`); they are sent but discarded. `ReadUSB` is also never called by the app.

---

## 6. Apply / save pipeline (the core interaction)

A profile change is committed in two steps:

1. UI handlers update the **working copy** `DAT_0044F730` and post `0x670` to the worker thread (apply / reset / ring toggle / profile select).
2. `EXE:FUN_00414910@0x00414910` (thread) gets `0x670` with wParam 0 and calls `EXE:FUN_00418a40@0x00418a40`.

`FUN_00418a40` steps (all **[C]**):

1. **Windows pointer settings** (only when the value differs from the cached last-applied global):
   - Double-click: `SetDoubleClickTime(900 - 70*profile[0x6C])` + `SystemParametersInfoW(SPI_SETDOUBLECLICKTIME=0x20, …)`.
   - Mouse speed: `SystemParametersInfoW(SPI_SETMOUSESPEED=0x71, 1, {1,2,4,6,8,10,12,14,16,18}, 3)` indexed by `profile[0x64]` (1..11).
   - Enhance pointer precision: `SystemParametersInfoW(SPI_SETMOUSE=4, 0, {enabled,6,10} or {0,0,0}, 3)` from `profile[0x70]`.
   - Wheel: `SystemParametersInfoW(SPI_SETWHEELSCROLLLINES=0x69, lines, lines, 3)`; if `profile[0x74] != 0`, lines = `-1` (one page per notch).
   - Lines 52-114.
2. **Commit data**: `memcpy(DAT_0044F730 → DAT_00432AA0, 0x1CC50)` (working copy becomes the selected profile). Line 115.
3. **Device handshake/status** `FUN_004196b0`:
   - SetFeature `{0x83, …}` (checksum).
   - GetFeature `{0x8B, …}` (checksum), reply de-obfuscated if password enabled, **discarded** (immediately overwritten).
   - SetFeature `{0x03, 0x00, 0x40, liftEnable ? 0x08 : 0x00, 0,0,0, checksum}`.
   - Lines 25-53.
4. **Frames sent via `MSDriver!SetFeature` (8 bytes each, checksum in byte 7, optional password obfuscation)**:

   | # | Frame | Source |
   |---|---|---|
   | 0x02 | `{02, mode+1, 0,0,0,0,0, sum}`; `mode = profile+0x14C` (0 = Office, 1 = Game; payload 1 = Office, 2 = Game) | `FUN_00418a40:117-126` |
   | 0x01 | `{01, rate, …}`; rate = 8 for index 0, 4 for 1, 2 for 2 (default), 1 for 3 | :130-151 |
   | 0x0B | `{0B, activeStage+1, …}`; active stage `profile+0x84` | :155-164 |
   | 0x0C | `{0C, R, G, B, …}`; R/G/B from `profile+0x104/105/106` (COLORREF low bytes) | :168-179 |
   | 0x0D | light effect (table below) | :183-246 |
   | 0x10 | `{10, 00, 18, …}` + 32-byte block 0 | :250-291 |
   | 0x10 | `{10, 01, 18, …}` + 32-byte block 1 | :293-334 |
   | — | `FUN_00419860` → 0x11 + DPI stage block | :336 |
   | — | `FUN_0041ab50` → 0x12 button chunks + 0x13 macro chunks | :337 |
   | 0x04 | `{04, lodCode, keyResponseMs, …}` — only if `DAT_00432ACC != 0`; lodCode = `CMainWnd[0x16C8 + profile[0x130]]` when `profile[0x130] < 8`, else 0 | :338-361 |
   | 0x08 | `{08, AA, CC, EE, …}` commit magic | :363-370 |
   | 0x07 | high-DPI bitmask (only for sensors D07/D2A/CEF, and inside `FUN_0041bd40` only sent if `Distance != 0`) | :372-374 |
5. **Persist**: `FUN_00402b20` writes `Data\Data.bin` (8 bytes: selected index + spare), `FUN_004035a0` writes all profiles to `Data\profile.bin`. Hide `ring_ver`. Lines 375-378.

Light frame 0x0D encoding (`profile+0xF0` = mode 0..11, `+0xF4` = brightness 0..255, `+0xF8` = vendor "frequency" slider 0..4, `+0xFC` = fixed/cycle colour mode 0/1 (stored 1→2), `+0x100` = vendor "length" slider 0..4). `FUN_00418a40` precomputes `4 − +0xF8` and `4 − +0x100`, so modes 2/3/4 use `+0xF8` directly while 6/7 use `4 − +0x100`:

| Mode | byte2 | byte3 |
|---|---|---|
| 0 | 0 | 0 |
| 1 | brightness | frequency |
| 2 | length (+0xF8) | frequency |
| 3, 4 | length (+0xF8) | brightness |
| 5 | brightness | frequency |
| 6, 7 | 4 − direction | frequency |
| 8 | brightness | (frequency != 0) |
| 9 | brightness | frequency \| ((4 − length) << 4) |
| 10 | brightness | 4 − length |
| 11 | brightness | frequency |
| other | 0 | 0 |

[C] `FUN_00418a40:183-246`

Timing: every successful `SetFeature` sleeps 20 ms (`FUN_00418a40`), every `WriteUSB` sleeps 10-20 ms; the 0x10 blocks are separated by 20 ms.

---

## 7. Device link (how the app talks to the mouse)

### 7.1 `MSDriver.dll` export surface

`C:\...\analysis\exports-MSDriver.json`:

| Export | Address | Implementation |
|---|---|---|
| `Set_VIDPID` | 0x100016d0 | Stores VID/PID into `DAT_10009de4/DAT_10009de0`. [C] |
| `Open_DevMonitor` | 0x100016f0 | Stores HWND/messages, creates event + main thread, waits 2000 ms, registers HID notifications (`FUN_10001590`), enumerates devices (`FUN_10001df0(0)`). [C] |
| `Close_DevMonitor` | 0x10001890 | Stops monitor thread, unregisters notifications. [C] |
| `Open_FeatureDevice` | 0x10001860 | **Stub** — bytes `B8 01 00 00 00 C3` (`return 1`). [C] export table + stub bytes |
| `Close_FeatureDevice` | 0x10001860 | Same stub address as above. [C] |
| `SetFeature` | 0x10001ad0 | 9-byte buffer, report ID 0, `HidD_SetFeature`. [C] |
| `GetFeature` | 0x10001b30 | `HidD_GetFeature`, copies 8 bytes back. [C] |
| `Open_ReportDevice` | 0x10001870 | `push 2; call FUN_10001df0` (mode 2), returns `!result`. [C] |
| `Close_ReportDevice` | 0x100018a0 | Closes the cached handle. [C] |
| `WriteUSB` | 0x100018c0 | 33-byte `WriteFile` (report ID 0 + 32 bytes), overlapped, 2000 ms timeout. [C] |
| `ReadUSB` | 0x100019d0 | 33-byte overlapped read; **never called by the app**. [C] |

**[C] Important correction to a natural but wrong reading of the API names:** the handle used for `SetFeature`/`GetFeature`/`WriteUSB` is opened by `Open_ReportDevice` via HID interface selector mode 2:

- `FUN_10001c00` opens `CreateFileA(path, 0xC0000000, 3, NULL, OPEN_EXISTING=3, FILE_FLAG_OVERLAPPED=0x40000000, NULL)`.
- Mode 0 (monitor) accepts UsagePage `0xFF01` + Usage `0xFF01` and VID/PID match.
- Mode 1 accepts UsagePage `0xFFFF` + Usage `0x00FF` (stored in `_DAT_10009ee8`, never used by this app).
- Mode 2 accepts UsagePage `0xFF00` + Usage `0xFF00` and is the one that succeeds and places the device struct into `DAT_10009de8`.
- VID/PID read from `HidP_GetCaps` output (`+0x4C` VID, `+0x4E` PID).

The shipped `Data.ini` values (`VID=04D9`, `PID=A09F`) are passed to `Set_VIDPID`, so the mouse must expose the three HID interfaces with those IDs.

### 7.2 Monitor thread and input reports

- `Open_DevMonitor(hwnd, 0x52D, 0x52E)` stores `hwnd`, event message `0x52D`, presence message `0x52E`.
- `FUN_10001df0(0)` enumerates all HID interfaces; for each match, `FUN_100014b0` registers device notifications, starts a per-device thread, and posts `FUN_10001470(1, index)` (`0x52E wParam=1`).
- Per-device thread `FUN_10001610` loops: `Sleep(10)`, `FUN_10002110(device)`.
- `FUN_10002110` does an overlapped `ReadFile` of `InputReportByteLength` into a buffer; if `buf[0] == 6` it posts
  `PostMessageA(hwnd, 0x52D, (buf[1] << 8) | buf[2], buf[3])`.
- Device removal `FUN_10002090` posts `0x5F5` and `0x52E wParam=0`.
- App side (`EXE:FUN_00415000`): `0x52D` → `FUN_004194a0(this, (wParam << 16) ^ (lParam & 0xFFFF))`; `0x52E` → online/offline event.
- `EXE:FUN_004194a0@0x004194a0` decodes the high word as the event and the low word as the value:
  - `0x7F00`, value 1 → device connected: sleep 500 ms, `Open_FeatureDevice` + `Open_ReportDevice`, set `+0x16D0=1`, re-run `FUN_004196b0` + `FUN_0041bbc0` (no firmware check on hot-plug).
  - `0x7F00`, value 2 → disconnected: `Close_FeatureDevice` + `Close_ReportDevice`, `+0x16D0=0`, hide main window.
  - `0x07xx` (1..8) → active DPI stage changed on the device: `profile[0x84] = value-1`, check the corresponding radio, post `0x469` with the stage DPI for the overlay, save profile.
  - `0x05xx` (1..8) → report rate changed: 8→0, 4→1, 2→2, 1→3; store `profile[0x80]`, check radio, save.
  - `0x08xx` (1..2) → work mode changed: `profile[0x14C] = value-1` (1 = Office, 2 = Game), update button page, save.

### 7.3 Wire formats

- **Feature packets** (both directions): 9 HID feature-report bytes = `[0x00 report ID][8-byte packet]`.
  - byte0 = command, bytes 1..6 = arguments, byte7 = checksum.
  - checksum = `(0 - (1 + sum(bytes0..6))) & 0xFF`. Verified against many frames, e.g. commit `08 AA CC EE` → sum 0x26C → byte7 = 0x94? **Correction from code**: the code computes `cVar8 = -0x6D - …` where 0x08+0xAA+0xCC+0xEE = 0x26C (low byte 0x6C), plus the fixed +1 = 0x6D → checksum = 0x93. Formula confirmed; arithmetic above is `0 - 0x6D = 0x93`. [C]
- **Bulk blocks** (`WriteUSB`): 33 HID output bytes = `[0x00 report ID][32-byte payload]`. No checksum on the block; the preceding feature packet selects the block.
- **Input reports**: report ID `0x06`, then `eventHigh, eventLow, value` → `0x52D (event, value)`.

### 7.4 Password obfuscation (applies only to feature packets)

`EXE:FUN_00414710@0x00414710` (encode) / `EXE:FUN_00414810@0x00414810` (decode), used only when `Data.ini Password` length == 6 (`CMainWnd+0x1AF0 == 1`). The 6 characters are the XOR keys `DAT_00432AB1..AB6`.

Encode, given plain 8-byte packet `p[0..7]`:

1. Permute: `n[0]=p[5], n[1]=p[4], n[2]=p[7], n[3]=p[6], n[4]=p[1], n[5]=p[0], n[6]=p[3], n[7]=p[2]`.
2. XOR: `n[1]^=k1; n[2]^=k2; n[3]^=k3; n[4]^=k4; n[5]^=k5; n[6]^=k6;` `n[0]` and `n[7]` unchanged. (Verified against the raw disassembly at `0x414746-0x41477b`; an earlier note here had the k5/k6 slots on the wrong indices.)
3. Rotate the whole 64-bit little-endian value left by 3 bits (cross-byte):
   `out[0]=(n0<<3|n1>>5)+0x25`, `out[1]=(n1<<3|n2>>5)-0x0A`, `out[2]=(n2<<3|n3>>5)-0x1C`,
   `out[3]=(n3<<3|n4>>5)+0x76`, `out[4]=(n4<<3|n5>>5)+0x47`, `out[5]=(n5<<3|n6>>5)+0x54`,
   `out[6]=(n6<<3|n7>>5)-0x1A`, `out[7]=(n7<<3|n0>>5)+0x76`. [C] lines 20-54

Decode is the exact inverse in `FUN_00414810` (rotate right by 3, subtract the same constants, XOR, inverse permutation). [C]

### 7.5 Device handshake (`FUN_0041bbc0`)

1. SetFeature the 8-byte packet `{00, AA, DD, 3B, 62, 00, 00, 0xDB}` (buffer byte 0 is zero; `AA DD 3B 62` sits at bytes 1..4); checksum = `0 - (1+AA+DD+3B+62) & 0xFF` = `0xDB`.
2. Sleep 30 ms; GetFeature (reply ignored).
3. SetFeature the **same packet obfuscated** (always, regardless of the password flag).
4. Sleep 30 ms; GetFeature; de-obfuscate reply; compare reply bytes 1..4 with `AA DD 3B 62`. On this mouse the accepted reply is `26 18 F5 02 40 0C 44 5E`, which decrypts to `00 AA DD 3B 62 00 00 00` with password `FB1570`. A wrong encoder still receives a feature report, so only the decrypt check distinguishes a real link.
5. Mismatch → `CMainWnd+0x16D0 = 0` (treated as not connected). [C] lines 27-62

---

## 8. Feature command reference

| Cmd | Direction | Payload (bytes 1..6) | Meaning | Evidence |
|---|---|---|---|---|
| `0x01` | Set | `rate` (8,4,2,1 for UI indices 0,1,2,3) | Report rate (ms). | [C] `FUN_00418a40:130-151` |
| `0x02` | Set | `mode+1` (1 = Office, 2 = Game) | Work mode. | [C] :117-126 |
| `0x03` | Set | `0, 0x40, bit3 = lift-off enabled, 0…` | Status/lift-off. Sent in every apply via `FUN_004196b0`. | [C] |
| `0x04` | Set | `lodCode, keyResponseMs` | Lift-off distance level + key response time. Only when `Distance != 0`. | [C] `FUN_00418a40:338-361` |
| `0x07` | Set | `0, bitmask of stages above sensor threshold` | "High DPI" flags for D07/D2A/CEF. Bit i set when stage i DPI > threshold (D07 160, D2A 200, CEF 120). Only sent when `Distance != 0` (implementation quirk). | [C] `FUN_0041bd40` |
| `0x08` | Set | `AA CC EE` (magic) | Commit/apply. | [C] :363-370 |
| `0x0B` | Set | `activeStage+1` | Currently selected DPI stage. | [C] :155-164 |
| `0x0C` | Set | `R, G, B` | Fixed LED color. | [C] :168-179 |
| `0x0D` | Set | light params (see table §6) | Effect mode/brightness/speed. | [C] :183-246 |
| `0x10` | Set + block | `blockIndex (0/1), 0x18`, then 32-byte WriteUSB | Program 8-color palette. Block 0 = cycle colors (`profile+0x110`), block 1 = per-stage DPI colors (`profile+0xD0`). | [C] :250-334 |
| `0x11` | Set + block | `stageCount (profile+0x139), 0x08`, then 32-byte WriteUSB | Program DPI stage table. | [C] `FUN_00419860:40-50` |
| `0x12` | Set + 2 blocks | `chunk 1..4, 0x40`, then 2 × 32 bytes | Program 64-button table (256 bytes). | [C] `FUN_0041ab50:438-469` |
| `0x13` | Set + 4 blocks | `chunk 1..N, 0x80`, then 4 × 32 bytes | Program macro table (N × 128 bytes). | [C] `FUN_0041ab50:473-502` |
| `0x80` | Set/Get | — | Read firmware version; reply byte1/2 compared to `Ver_H`/`Ver_L`. | [C] `FUN_0041b850` |
| `0x83` | Set | — | Handshake/status setup (semantics not further used). | [C] `FUN_004196b0` |
| `0x8B` | Get | — | Status read; reply discarded after de-obfuscation. | [C] `FUN_004196b0` |
| — | Set | `AA DD 3B 62` (plain + obfuscated) | Link handshake. | [C] `FUN_0041bbc0` |

**[U]** The semantic meaning of 0x83/0x8B beyond "handshake/status" is not determinable from the app alone.

---

## 9. The 32-byte block payloads

### 9.1 Palette blocks (cmd 0x10)

Header `[0x10, block, 0x18]`; `0x18` = 24 color bytes. The 32-byte payload is **8 × RGB triples followed by 8 zero bytes**. Source order is R,G,B per color (confirmed by `FUN_0040e9c0` reading a COLORREF low-byte as R and by the packet bytes at `profile+0x104/105/106`).

- Block 0 ← `profile+0x110..0x12F` (8 × 4-byte COLORREFs, only RGB used).
- Block 1 ← `profile+0xD0..0xEF` (8 × 4-byte COLORREFs).
[C] `FUN_00418a40:259-334`; the decompiler's overlapping 2/3-byte reads are stack aliasing; the resulting 24 data bytes + 8 zero padding interpretation is exact.

### 9.2 DPI stage block (cmd 0x11)

Header `[0x11, count, 0x08]`, then 32 bytes containing **8 one-byte stage codes** (rest zero).

For the shipped sensor `0x0CEF` (Sensor=3311), `FUN_00419860:1120-1168`:

```
code[i] = table[ index(dpi_i) ]        (byte at VA 0x425DE4 + 4*index)
index(dpi) = dpi            if dpi < 121
           = dpi / 2        otherwise
```

The lookup table has 121 entries (0..120); it is *not* the identity, it skips codes reserved by the firmware. Observed values (index:code, low byte of 4-byte entries):

```
0:50 1:00 2:02 3:03 4:04 5:05 6:06 7:07 8:09 9:0a 10:0b 11:0c 12:0d 13:0e
14:10 15:11 16:12 17:13 18:14 19:16 20:17 21:18 22:19 23:1a 24:1b 25:1d
26:1e 27:1f 28:20 29:21 30:23 31:25 32:26 33:27 34:28 35:29 36:2a 37:2c
38:2d 39:2e 40:2f 41:30 42:32 43:33 44:34 45:35 46:36 47:38 48:39 49:3a
50:3b 51:3c 52:3e 53:3f 54:40 55:41 56:42 57:44 58:45 59:46 60:47 61:48
62:4a 63:4b 64:4c 65:4d 66:4e 67:50 68:51 69:52 70:53 71:54 72:56 73:57
74:58 75:59 76:5a 77:5c 78:5d 79:5e 80:5f 81:60 82:62 83:63 84:64 85:65
86:66 87:68 88:69 89:6a 90:6b 91:6c 92:6e 93:6f 94:70 95:71 96:72 97:74
98:75 99:76 100:77 101:78 102:7a 103:7b 104:7c 105:7d 106:7e 107:80
108:81 109:82 110:83 111:84 112:86 113:87 114:88 115:89 116:8a 117:8c
118:8d 119:8e 120:8f
```

Reserved (skipped) codes in the table: `1,8,15,21,28,34,36,43,49,55,61,67,73,79,85,91,97,103,109,115` (plus higher ones outside the 121-entry range). [C] byte dump at file offset 0x251E4 (RVA 0x25DE4).

Other sensor branches live in `FUN_00419860:56-1119`. Confirmed examples:

- `0xCFD`: `stage0 → 0x8000` (i.e. byte 0x00/0x80 flags); for others, if dpi > 50: `flag 0x40`, dpi /= 2; code = dpi-1 (lines 56-70).
- `0xBEA`/`0x13BA`: small index tables (1..12 / 1..17).
- `0xD07`/`0xD2A`/`0xCEF` also get the 0x07 mask.
- **[U]** exact per-sensor packing for the remaining IDs is only partially transcribed; the code is fully present in the pseudocode file and must be mirrored per sensor if other `Data.ini` variants are supported.

### 9.3 Button table (cmd 0x12)

- 64 slots × 4 bytes = 256 bytes = 4 frames (`frame = 1..4`); each frame = 8-byte header `[0x12, frame, 0x40, 0,0,0,0, checksum]` followed by two 32-byte `WriteUSB` blocks (64 bytes). `Sleep(10)` between header and each block. [C] `FUN_0041ab50:452-476`
- Per slot `i`: action = `profile + i*0x72C + 0x219`, i.e. entry base `profile+0x150+i*0x72C` + `0xC9`. [C] `FUN_0041ab50:65-66`
- Mode flag is the 5th byte of the `Data.ini [BUTTON] n` entry, stored at `CMainWnd+0x1588+i*5+4` (i.e. `0x158C`). If it is `1`, the slot is **computed** from the static action-descriptor table; if it is `0`, the first four stored bytes (`0x1588..0x158B`) are copied verbatim. [C] `FUN_0041ab50:120-133`
- Descriptor table: VA **0x425118**, 61 records of `0x14` bytes, terminated by the loop bound `0x4255E0`. Record = five dwords: `action_id`, `A`, `B`, `C`, `D` (offsets +0/+4/+8/+12/+16). The search compares the record's action id with `entry+0xC9` and has **no early exit**, so a later duplicate would win (no duplicates exist). Full dump in **Appendix D**. [C] `FUN_0041ab50:68-80`, dump at file offset 0x24518 (RVA 0x25118).
- Computed slot = two 16-bit words assembled as `(A<<8)|B` and `(D<<8)|C`, then written as four bytes in the order **A, B, C, D** into one 256-byte staging buffer (64 slots × 4, base `ebp-0x1CC`). In this build every A/B/C/D value is < 0x100, so only the low byte of each dword is significant. [C] `FUN_0041ab50:120-133`, disasm `0x41ad02-0x41ad61` (stores to `-0x1CC/-0x1CB/-0x1CA/-0x1C9`; raw path copies `0x1588/0x1589/0x158A/0x158B`).
- Raw slot (`flag == 0`) = the first four stored bytes `0x1588..0x158B` copied verbatim. [C] `FUN_0041ab50:128-133`
- Special cases (override individual fields of the slot; A stays as tabled unless stated):
  - action `0x15` (shortcut): `B ← entry+0x22C` (key code), `C ← entry+0x22D` (modifier mask). [C] `FUN_0041ab50:82-90`
  - action `0x0A` (fire click): `B ← 0xF0`, `C ← entry+0x830`, `D ← entry+0x82C` (click count / interval). [C] `FUN_0041ab50:92-99`
  - action `0x16` (select macro): `B ← entry+0x224` (macro index); if tabled `A == 0x09`, `C ←` a running macro-slot counter (1..11). [C] `FUN_0041ab50:100-105`
  - action `0x39`/`0x79` (set-left-macro / set-gun): slot is synthesized as `08 00 (n+4) 00`, n = running counter starting at 0, i.e. `A=8, B=0, C=n+4, D=0`. [C] `FUN_0041ab50:106-119`
  - Raw mode (`flag == 0`) copies `entry+0x1588`'s four bytes byte-for-byte. [C] `FUN_0041ab50:128-133`

### 9.4 Macro table (cmd 0x13)

- Header `[0x13, frame 1..N, 0x80, 0,0,0,0, checksum]`, then four 32-byte blocks per frame = 128 bytes; `N = macro-bearing button count` (counter starts at 1, guard `< 0xC`, so at most 10 frames). Each macro button builds one 128-byte block and copies it to send-buffer offset `(n-2)*128`. [C] `FUN_0041ab50:93, 478-505`; copy at disasm `0x41af76-0x41af95` (`shl $7`, `rep movsl 0x20`).
- Source per macro-bearing slot: event/row count `u16 @ entry+0x232`, two header bytes packed in the dword `@ entry+0x234` (low byte first), then:
  - actions `0x16` (select macro) and `0x39` (set-left-macro): 16-byte events from `entry+0x5AC` (layout in §5.5: `+1` opcode, `+2` state, `+4` u16 delay, `+8`/`+12` payload dwords). [C] `FUN_0041ab50:138-330`
  - action `0x79` (set gun): 12-byte rows, first 15 at `entry+0x440`, remaining 15 at `entry+0x4F4` (the pointer bases 0x444/0x4F8 are read as `[-1]`/`[0]`); row = dword x, dword y, u16 delay at +10. [C] `FUN_0041ab50:334-451`
- Re-encoding into the 128-byte stream (per event, `d` = delay u16 at +4, `op` = opcode byte at +1, `st` = state byte at +2):
  - short form, `d/10 ≤ 0x7F` (i.e. `d < 0x4F7` ≈ 1271 ms): first byte `t = d/10`; `st=1` → `t|1`, `st=2` → `t|0x81`. Then:
    - `st=0`: `[t, 0xFB, A16lo, A16hi, B16lo, B16hi]` (6 bytes; only the low 16 bits of the two payload dwords are used).
    - `st=1/2`: `[t, op]` (2 bytes).
  - long form, `d > 0x4F6` (i.e. `d/10 > 127`): `q = d/20`, `r = (d%20+5)/10` (0..2, 10 ms granularity); `q` is emitted **high byte first**:
    - `st=1`: `[r|1, op, 0x00, 0x01, qhi, qlo]`; `st=2`: `[r|0x80, op, 0x00, 0x01, qhi, qlo]` (6 bytes).
    - `st=0`: `[0x00, 0xFB, A16lo, A16hi, B16lo, B16hi, 0x00, 0x01, qhi, qlo]` (10 bytes; `r` is computed but unused here).
    [C] `FUN_0041ab50:150-229`, disasm `0x41ade0-0x41af58` (threshold `cmp $0x4F6 / jbe`, `/10` at `0x41aef4`, `/20` + `%20` at `0x41adfc-0x41ae27`, stores at `0x41ae39-0x41af51`).
  - gun rows: first byte `delay/10 | 1`; `x==0 && y==0` → `[t, 0xF0, 0x81]`; otherwise `[t, 0xF0, 0x00, 0xFA, |x|, |y|, 0x81, 0xF0]` with x/y sent as absolute byte magnitudes. The first 15-row block ends with `[0xFE, (n+2)*2]`, the second block is prefixed by `0x01 0x00`. [C] `FUN_0041ab50:334-451`
- Marker vocabulary `0xF0/0xFA/0xFB/0x81/0xFE`; the state flags in the timing byte (`|1` press, `|0x81`/`|0x80` release) are the only semantic bits the app itself sets. The firmware meaning of the markers is not established from the app alone. [I]

---

## 10. Sensor table (DPI limits and display mapping)

From `EXE:FUN_0041d110@0x0041d110` (slider min/max and max-DPI label) and `EXE:FUN_00403d70@0x00403d70` (display value):

| Sensor (dec / hex) | Slider min..max | Max label | Display formula (stage → shown DPI) |
|---|---|---|---|
| 3325 / 0x0CFD | 2..100 | 10000 | stage × 100 |
| 3212 / 0x0C8C | 1..189 | 7560 | stage × 40 |
| 3050 / 0x0BEA | 1..12 | 4000 | table {250,500,750,1000,1250,1500,1750,2000,2500,3000,3500,4000} |
| 5050 / 0x13BA | 1..17 | 2750 | (no explicit mapping found → "%d") [U] |
| 3327 / 0x0CFF | 2..120 | 12000 | stage × 100 |
| 3335 / 0x0D07 | 1..160 | 19000 | stage × 100 (160 → "19000" only beyond range? code shows stage×100; 0xA0 → 19000 uses special case) |
| 36 / 0x24 | 1..80 | 8000 | stage × 100 |
| 37 / 0x25 | 1..120 | 12000 | stage × 100 |
| 38 / 0x26 | 1..160 | 16000 | stage × 100 |
| 60 / 0x3C | 1..240 | 24000 | stage × 100 |
| 6400 / 0x1900 | 4..248 | 12400 | stage > 200 ? (stage−100)×100 : stage×50 |
| 3104 / 0x0C20 | 16..212 | 8480 | stage × 40 |
| 3330 / 0x0D02 | 1..144 | 7200 | stage > 200 ? (stage−100)×100 : stage×50 |
| 3333 / 0x0D05 | 2..160 | 16000 | stage × 100 |
| 3370 / 0x0D2A | 1..290 | 19000 | stage × 50 |
| 3311 / 0x0CEF | 1..240 | 24000 | stage × 100 |

[C] ranges and labels from `FUN_0041d110`; formulas from `FUN_00403d70`. The shipped build uses 0x0CEF.

High-DPI bitmask (`FUN_0041bd40`): bit i = stage[i] DPI above threshold; thresholds: 0xD07 → 0xA0 (160), 0xD2A → 200, 0xCEF → 0x78 (120); for the last stage the code also sets bit 7 when the comparison overflows (specifics in lines 108-110).

---

## 11. Data model and persistence

### 11.1 `Data.ini` (shipped)

```
[Default]
VID=04d9  PID=A09F  DPI=8  Sensor=3311  Password=FB1570
Distance=0  Distance_Min=0  Distance_Max=2  Distance_Value=0,1,2,0,0,0,0,0
Ver_H=2  Ver_L=1  Update=0

[BUTTON]
1=01,00,F0,00,1   …   64=04,00,02,00,1
```
`[BUTTON]` entries are 5 hex bytes: four raw code bytes + one flag (1 = use computed action mapping, 0 = send raw bytes). [C] `FUN_004158d0:243-279`, `FUN_0041ab50:121-133`

### 11.2 `Data\Data.bin`

8 bytes. The first dword is the selected profile index (`DAT_00432AA8`); shipped file `0d 00 00 00 00 00 00 00` → index 13 (last of 14 profiles). [C] `FUN_00416c70:73-82`, `FUN_00402b20`

### 11.3 Profile record (`0x1CC50`) — layout

| Offset | Contents | Status |
|---|---|---|
| +0x000 | Profile name (wide string, referenced as `wchar_t*`) | [C] `FUN_00416c70:202` |
| +0x064 | Mouse speed index (1..11) | [C] |
| +0x068 | Wheel scroll lines | [C] |
| +0x06C | Double-click speed index (0..10) | [C] |
| +0x070 | Enhance pointer precision (0/1) | [C] |
| +0x074 | One-page wheel scroll (0/1) | [C] |
| +0x080 | Report-rate index (0..3) | [C] |
| +0x084 | Active DPI stage index (0..7) | [C] |
| +0x088..+0x0A4 | 8 DPI stage values (int32) | [C] |
| +0x0C8? | (spare) | [U] |
| +0x0D0..+0x0EF | 8 per-stage LED colors (COLORREF) | [C] |
| +0x0F0 | Light mode (0..11; indexed at `CMainWnd+0xab4 + mode*4` in `FUN_00417540`) | [C] |
| +0x0F4 | Brightness (0..255) | [C] |
| +0x0F8 | Vendor "frequency" slider / speed (0..4) | [C] |
| +0x0FC | Fixed(0)/cycle(1) colour mode — a two-entry table index, never 0..255 (`FUN_0040e460` writes it, `FUN_00417540` indexes `+0xb2c + value*4`) | [C] |
| +0x100 | Vendor "length" slider / direction (0..4) | [C] |
| +0x104..+0x106 | Fixed color R,G,B (COLORREF) | [C] |
| +0x110..+0x12F | 8 cycle colors (COLORREF) | [C] |
| +0x130 | LOD level index (0..7) | [C] |
| +0x134 | Lift-off enabled (0/1) | [C] |
| +0x138 | Key response time (ms) | [C] |
| +0x139 | Enabled DPI stage count (1..8) | [C] |
| +0x14C | Work mode: 0 = Office Mode (slots 0-15), 1 = Game Mode (slots 32-47) | [C] |
| +0x150 .. +0x1CC4F | 64 button entries × 0x72C (0x150 + 64×0x72C = 0x1CC50 exactly) | [C] arithmetic |

Button entry (0x72C):

| Offset (entry-relative) | Contents |
|---|---|
| +0x064..+0x0C7 | 50-wchar display name (copy of the selected macro/gun name; zeroed, then `wcscpy_s`) [C] |
| +0x0C9 | Action code [C] |
| +0x0D0 | Selected index in the macro/gun list [C] |
| +0x0D4 | Macro slot index sent for action `0x16` (`0xFF` = none) [C] |
| +0x0D8..+0x0DB | no observed reader or writer [U] |
| +0x0DC/+0x0DD | Shortcut key / modifier mask [C] |
| +0x0E2 | Event/row count (u16) [C] |
| +0x0E4 | Loop count (u16) [C] |
| +0x2F0..+0x457 | 30 gun bullets × 12 bytes (int32 x, int32 y, u16 delay) [C] |
| +0x458 | Dword written on macro selection (`0xFF` or a value); consumer not found [U] |
| +0x45C..+0x6DB | 40 macro events × 16 bytes [C] |
| +0x6DC/+0x6E0 | Fire-click count / interval [C] |
| +0x6E4..+0x72B | no observed reader or writer [U] |

Note: the decompiler prints profile-absolute offsets (`0x219`, `0x220`, `0x224`, `0x22C`, `0x232`, `0x234`, `0x440`, `0x5A8`, `0x5AC`, `0x82C`, `0x830`); subtract the button base `0x150` to get the entry-relative values above. [C] arithmetic from `FUN_0041ab50`, `FUN_00406db0`.

Evidence for the entry fields: name/index/slot/count writes at `FUN_00406db0:792-798`; action and shortcut at `FUN_0041ab50:65-66,100-105`; gun rows and macro events at `FUN_0041ab50:138-451`. The 16-byte macro event layout is resolved in §5.5.

### 11.4 Macro record (`0x358`) and gun record (`0x240`)

- Both files are plain record streams with no file header: `macro.bin` = N × `0x358`, `gun.bin` = N × `0x240` (`FUN_00416c70:120-188`). [C]
- Macro record (`0x358`): two wide names at +0x00 and +0x64 (50 wchars each, same header as gun), folder flag dword +0xD4 = 1 (created by `FUN_004131f0:68`), loop count u16 +0xC8, event count u16 +0xCC, 40 × 16-byte events from +0xD8 (0xD8 + 0x280 = 0x358). The event bytes are the same unit as `page+0x24` (copied verbatim by `FUN_004116c0:20-27`, then into the button entry at +0x5AC by `FUN_00406db0:800-804`), so the §5.5 field layout applies directly. [C]
- Gun record (`0x240`): confirmed in §5.6 — names at +0/+0x64, count 0x1E at +0xC8, dir flag at +0xD0, 30 × 12-byte bullets from +0xD8 (0xD8 + 0x168 = 0x240). [C]

### 11.5 Save/load functions

| Function | Effect | Evidence |
|---|---|---|
| `FUN_00402b20` | Writes `Data\Data.bin` (8 bytes selected index) | [C] |
| `FUN_004035a0` | Writes all profile records to `Data\profile.bin` | [C] |
| `FUN_004037f0` | Loads `Data\profile.bin` into profile pointer array; if missing, generates defaults (`FUN_00403af0`) | [C] |
| `FUN_00416c70` | Startup data loader / profile combo builder | [C] |
| `FUN_00418a40` end | Calls `FUN_00402b20` + `FUN_004035a0` after every apply | [C] |

`macro.bin`/`gun.bin` are written by the macro/gun page handlers (path literals `Data\macro.bin`, `Data\gun.bin` present at VA 0x424290 / 0x4242C4); the exact writer functions were not individually re-verified in this pass. [C] paths; [I] writers

### 11.6 Import / export / rename

Handled by message `0x403` commands, implemented in the page objects:

- Profiles: `FUN_004183f0` (import), `FUN_004187c0` (export).
- Macro dir/set: `FUN_00413970` (rename dir), `FUN_00413c70` (import dir), `FUN_004140e0` (export dir), `FUN_004143e0` (export with password), `FUN_00411bc0` (rename macro), `FUN_00412520` (import macro), `FUN_00412cc0` (export macro), `FUN_00412f40` (export with password).
- Gun dir/set: `FUN_0040d0f0`, `FUN_0040d3f0`, `FUN_0040d860`, `FUN_0040db60`, `FUN_0040ba50`, `FUN_0040bcf0`, `FUN_0040c490`, `FUN_0040c710`.

[C] dispatch in `FUN_00415000`; file-dialog internals not audited here. [I] "with password" = encrypts exported file using the same 6-char password (naming only).

---

## 12. Macro recording (Hook.dll)

Exports used by the app (macro page and shortcut dialog load the DLL and map procedures):

`InstallHook`, `InstallMouseHook`, `EnableMouseHook`, `EnableHook`, `MouseMoveHook`, `RemoveHook`, `RemoveMouseHook`, `hookproc`, `mousehookproc`.

Behaviour (from `analysis\dump\Hook\pseudocode`):

- `InstallHook` sets a `WH_KEYBOARD_LL` (0xD) hook; `InstallMouseHook` sets `WH_MOUSE_LL` (0xE).
- Callbacks post to the app window: keyboard events as message `0x500`, mouse events as `0x501`; `0x502` (mouse move) is defined but the app never handles it. [C] app-side absence.
- A numpad remap table translates numpad scancodes before posting.
- When the configured target window is foreground, the hook returns 1 to consume the event; otherwise it passes it through. [C] `hookproc`/`mousehookproc`.
- App intake `FUN_00410d10(page, wParam, lParam)`: mouse messages are mapped to a small table at page+0xF0..0xF4; keyboard goes through `FUN_004022f0`; timing uses `QueryPerformanceCounter`; events are inserted with `FUN_004111b0` (16 bytes, `memmove` shift, count at page+0x2A4).
- Start/stop recording: `FUN_00410b80` / `FUN_00410ca0`.

Resolved: the 16-byte event layout and the three delay modes are documented in §5.5. Remaining open point is only the firmware's interpretation of the emitted timing/marker bytes, not the app-side encoding. [I]

---

## 13. Firmware check / updater

`EXE:FUN_0041b850@0x0041b850` (only called at startup when `Update != 0` and connected):

1. SetFeature `0x80` (read version).
2. GetFeature; compare reply byte1 with `DAT_00432AC4` (Ver_H) and byte2 with `DAT_00432AC0` (Ver_L).
3. Mismatch → modal `msg.xml` with `warning_title_text` / `update_fw_text`.
4. On OK → `CDuiString::Format("%s\\Update\\flashOnLine.exe", exeDir)` and `ShellExecuteW(..., SW_SHOW)`; returns 0, and the caller destroys the main window so the updater runs alone.
5. Match → returns non-zero, app continues.

[C] as summarized above; the `Update` directory and `flashOnLine.exe` are not present in the shipped package. `FUN_0041b6f0` is the generic one-shot "no device connected" warning using `msg.xml`.

---

## 14. Rebuild plan (ordered)

1. **Shell first**: DuiLib (or any DirectUI clone) window with `main.xml`, tab switching, caption buttons, tray icon, modal message window. Reproduce the 800×572 window vs 1280×750 layout behaviour (resolve §15.1).
2. **Data layer**: implement `Data.ini` parsing exactly (hex VID/PID, sensor int, 6-char password, 64 × 5-byte button map, Distance_Value CSV); implement `0x1CC50` profile record with the offset map of §11.3; `Data.bin`, `profile.bin`, `Default.pbin`, `macro.bin` (`0x358`), `gun.bin` (`0x240`).
3. **Transport**: implement a `MSDriver`-equivalent using SetupAPI/HID: enumerate by VID/PID and usage page/usage (`0xFF01/0xFF01` monitor, `0xFF00/0xFF00` control), 9-byte feature I/O with report ID 0, 33-byte overlapped output, input-report reader on report ID 6, presence notifications.
4. **Protocol layer**: 8-byte frames + checksum; optional 6-char password obfuscation; handshake `AA DD 3B 62` (plain + obfuscated); commit magic `08 AA CC EE`; all commands of §8; 32-byte block transfers of §9.
5. **Pages**: button page (64 slots, action menu, shortcut/fire-click/macro/gun/color dialogs), performance page (DPI stages/colors/sliders/Windows pointer settings), light page (12 modes + palettes), macro page (record/edit/upload), gun page (30 bullets).
6. **Apply engine**: the `0x670` worker thread and the exact `FUN_00418a40` sequence, including the Windows `SystemParametersInfoW` calls and 20 ms pacing.
7. **Device-event sync**: 0x52D/0x52E handling, DPI overlay (`0x469`, 2 s), on-device DPI/rate/mode changes updating the profile and saving.
8. **Macro hooks**: `Hook.dll` equivalent with LL hooks, message protocol, 16-byte event storage, 40-event cap, upload encoder.
9. **Firmware flow** and tray/import/export/persistence.

**Acceptance tests** (must pass without the original EXE):

- Handshake succeeds and commit produces a visible mouse change (DPI stage, LED).
- Button remap changes are reflected after unplug/replug (values persisted in the device).
- Drag of DPI slider → correct stage count and per-stage codes for a 0xCEF mouse.
- Windows pointer speed/double-click/wheel values match what the original app writes for each slider position.
- All settings survive app restart (profile.bin/Data.bin) and profile import/export round-trips.
- Macro record/playback with 1..40 events; loop count respected.

---

## 15. Open questions (do not paper over)

Items 1–7 are now closed or closed except for a firmware-side detail; they are kept here with the evidence so a rebuilder knows what is settled. Items 8–11 are genuinely open.

1. **Window sizing — closed [C].** `CWindowWnd::Create` is called with `cx=800, cy=0x23C (572)` (`EXE:FUN_00408e50`), and `DuiLib.dll` contains no internal call to `SetInitSize`/`GetInitSize` (objdump xref scan) while the EXE does not import them. The `size="1280,750"` in `main.xml` is the nominal design size: the root layout is fluid (largest fixed child = 320×100; all other sizing is float/percentage), and the two overlay layouts `disable_window_ver`/`ring_ver` are hard-coded 1280×750 translucent masks anchored top-left, which simply over-cover the 800×572 client area. Note the process has no `dpiAware` manifest entry, so the OS may still virtualize the physical window on a scaled display (unverified; static only).
2. **LOD table — closed [C].** `Distance_Value` is parsed in `FUN_004158d0` with eight `%d` conversions into the byte addresses `profile+0x16C8 .. +0x16CF` (`lea 0x7..0(%esi),%edi` at `0x41654E`; `esi` = `CMainWnd`), so the low byte of each parsed number lands in one stage slot. Command 0x04 reads `CMainWnd+0x16C8+stage` (`FUN_00418a40:343`).
3. **`Distance_Min`/`Distance_Max` — closed [C].** Parsed as `%02x` into globals `0x432AD4` (min) and `0x432AD0` (max) at `EXE:0x415DEA` / `0x415EE4`, then used as `SetMinValue` / `SetMaxValue` of the `lift_of_distance_slider` progress control (`performancePage+0x11C`) in `FUN_0041c490:124-125`.
4. **Button payload — closed [C].** The descriptor table base is `0x425118` (not 0x42511C): 61 records × 0x14 bytes of five dwords `action_id, A, B, C, D`, full dump in Appendix D. Computed slot = bytes **A, B, C, D** in that order (from `(A<<8)|B` and `(D<<8)|C` words); raw slot = stored bytes `0x1588..0x158B`; mode flag = byte `0x158C`. The decompiler's stack-alias cast obscured this on the first pass; the dword dump and the per-field write targets (`FUN_0041ab50:120-127`) now fix the order. The only open point is the firmware-side meaning of the `A` category values. [I]
5. **Macro upload opcode encoding** (0x13 stream) — markers and length rules are now documented in §9.4; the firmware meaning of each marker is [I/U].
6. **Macro event fields — closed [C].** The 16-byte unit is `+1` opcode, `+2` state (1 press / 2 release / 0 no-edge), `+4` u16 delay ms, `+8`/`+12` payload dwords (X/Y for move events); the three delay modes map to `page+0x20 = 0/1/2` (constant 10 ms / fixed `edit_default_delay` / measured with QPC-or-GetTickCount). See §5.5. The only residual unknown is how the firmware decodes the emitted timing/marker bytes. [I]
7. **Gun record — closed except byte scaling [C/I].** `+0`/`+0x64` name1/name2 (50 wchars each), `+0xC8` count 0x1E, `+0xD0` folder flag (1 = folder record, no rows), `+0xD8` 30 × 12-byte rows; row = int32 x, int32 y, u16 delay (default 10). The 0x79 encoder sends `abs(x)`/`abs(y)` as single bytes and `delay/10|1` as the timing byte (§9.4). Whether the UI can produce coordinates outside 0..255 (which would truncate) is [I].
8. **`0x83`/`0x8B` semantics**; the reply is discarded by this app. [U]
9. **`ReadUSB`, message `0x502`, message `0x5F5`, `IsTask.dll`, `DuiLib_d.dll`, `ring.xml`** are all dead/vestigial in this build. [C] absence; [I] intent
10. **Per-sensor DPI packing** other than 0xCEF/0xCFD is present but not fully transcribed; mirror `FUN_00419860` branch by branch if other `Data.ini` sensor variants must be supported. [I]
11. **`[BUTTON]` raw-vs-computed flag** meaning is confirmed functionally (1 = computed from action table), but why the shipped file sets flag 0 for slots 17-20/49-52 and still lists action-like bytes is [I: those slots are explicitly forced to raw codes].

---

## Appendix A — Key function map (EXE)

| Function | Address | Role |
|---|---|---|
| `FUN_00408e50` | 0x00408e50 | WinMain, mutex, window creation, message loop |
| `FUN_00414980` | 0x00414980 | `CMainWnd` constructor (all offsets/vtables) |
| `FUN_00414df0` | 0x00414df0 | Destructor (unloads Hook.dll, removes virtual windows) |
| `FUN_00415000` | 0x00415000 | Main window message handler + `0x403` command dispatch |
| `FUN_004158d0` | 0x004158d0 | OnCreate/startup: INI, data, driver load, connect |
| `FUN_00416c70` | 0x00416c70 | Load Data.bin/profile/macro/gun, build combos |
| `FUN_004176f0` | 0x004176f0 | DuiLib Notify (clicks, combos, profile select) |
| `FUN_004178e0` | 0x004178e0 | Caption buttons / profile menu / apply / reset |
| `FUN_00414910` | 0x00414910 | Worker thread (0x670 → apply) |
| `FUN_00418a40` | 0x00418a40 | Apply profile: Windows settings + full packet sequence |
| `FUN_004196b0` | 0x004196b0 | 0x83/0x8B/0x03 frames |
| `FUN_0041bbc0` | 0x0041bbc0 | `AA DD 3B 62` handshake |
| `FUN_0041b850` | 0x0041b850 | Firmware version check / updater launch |
| `FUN_0041b6f0` | 0x0041b6f0 | "No device" warning |
| `FUN_004194a0` | 0x004194a0 | Device event dispatch (0x52D/0x52E) |
| `FUN_004195a0` | 0x004195a0 | On-device setting change → UI + save |
| `FUN_00419860` | 0x00419860 | DPI stage table upload |
| `FUN_0041ab50` | 0x0041ab50 | Button + macro table upload |
| `FUN_0041bd40` | 0x0041bd40 | High-DPI bitmask |
| `FUN_00414710` / `FUN_00414810` | 0x00414710 / 0x00414810 | Password obfuscation / de-obfuscation |
| `FUN_00403d70` | 0x00403d70 | DPI display value per sensor |
| `FUN_0041d110` | 0x0041d110 | Sensor slider limits/labels |
| `FUN_00402b20` / `FUN_004035a0` | — | Save Data.bin / profile.bin |
| `FUN_004037f0` | 0x004037f0 | Load profile.bin |
| `FUN_00406db0` / `FUN_004081e0` | — | Button action menu / label mapping |
| `FUN_0041c490` / `FUN_0041c7f0` | — | Performance page init / refresh |
| `FUN_0040deb0` / `FUN_0040eaf0` / `FUN_0040e9c0` | — | Light page init / mode visibility / color UI |
| `FUN_0040ee10` / `FUN_00410b80` / `FUN_00410ca0` / `FUN_00410d10` / `FUN_004111b0` | — | Macro page init / record start/stop/intake/insert |
| `FUN_0040a080` | 0x0040a080 | Gun page init |
| `FUN_004017560?` — see `FUN_00417540` | 0x00417540 | Full UI refresh from selected profile |

## Appendix B — Key function map (MSDriver.dll)

| Function | Address | Role |
|---|---|---|
| `Set_VIDPID` | 0x100016d0 | Store VID/PID |
| `Open_DevMonitor` | 0x100016f0 | Start monitor thread + notifications |
| `FUN_10001df0` | 0x10001df0 | HID enumeration by interface mode (0/1/2) |
| `FUN_10001c00` | 0x10001c00 | Open one interface, match usage page/usage and VID/PID |
| `FUN_100014b0` | 0x100014b0 | Per-device setup + thread + presence post |
| `FUN_10001610` | 0x10001610 | Per-device loop (`Sleep(10)` + read) |
| `FUN_10002110` | 0x10002110 | Report read + `PostMessage(0x52D, event, value)` |
| `FUN_10002090` | 0x10002090 | Device removal / cleanup (posts 0x5F5 + 0x52E 0) |
| `SetFeature` | 0x10001ad0 | 9-byte HID feature write |
| `GetFeature` | 0x10001b30 | 9-byte HID feature read |
| `WriteUSB` | 0x100018c0 | 33-byte overlapped output |
| `ReadUSB` | 0x100019d0 | 33-byte overlapped input (unused) |

## Appendix C — Resources

`res\`: `main.xml`, `buttonpage.xml`, `performancepage.xml`, `lightpage.xml`, `macropage.xml`, `gun.xml`, `traymenu.xml`, `profilemenu.xml`, `buttonmenu.xml`, `macromenu.xml`, `macrodirmenu.xml`, `gunmenu.xml`, `gundirmenu.xml`, `macrolistitem.xml`, `selectcolor.xml`, `selectmacro.xml`, `selectgun.xml`, `fireclick.xml`, `shortcut.xml`, `msg.xml`, `dpi.xml`, `editname.xml`, `ring.xml`, `skins\*`.
Language: `Language\...\lan.xml` (loaded from `Language/lan.xml`), text keys such as `mouse_name_text`, `warning_title_text`, `no_connect_device_text`, `reset_profile_text`, `update_fw_text`, and all button action labels.

## Appendix D — Action descriptor table (VA 0x425118, 61 × 0x14 bytes)

Dumped from file offset 0x24518 (RVA 0x25118, `.rdata`). Each record is five little-endian dwords: `action_id`, `A`, `B`, `C`, `D`. The code reads only the low byte of each value (`FUN_0041ab50:68-80`), and in this build every value is < 0x100. The lookup is a linear scan with no early exit; action ids are unique. Column `slot` is the 4-byte payload written for a computed-mode button (`A B C D`).

| # | action_id | A | B | C | D | slot bytes |
|---|---|---|---|---|---|---|
| 0 | 0x01 | 0x01 | 0x00 | 0xF0 | 0x00 | `01 00 F0 00` |
| 1 | 0x02 | 0x01 | 0x00 | 0xF1 | 0x00 | `01 00 F1 00` |
| 2 | 0x03 | 0x01 | 0x00 | 0xF2 | 0x00 | `01 00 F2 00` |
| 3 | 0x09 | 0x0A | 0xF0 | 0x32 | 0x02 | `0A F0 32 02` |
| 4 | 0x15 | 0x00 | 0x00 | 0x00 | 0x00 | `00 00 00 00` |
| 5 | 0x19 | 0x0C | 0x00 | 0x00 | 0x00 | `0C 00 00 00` |
| 6 | 0x12 | 0x0A | 0xF0 | 0x32 | 0x03 | `0A F0 32 03` |
| 7 | 0x74 | 0x08 | 0x00 | 0x03 | 0x00 | `08 00 03 00` |
| 8 | 0x1A | 0x08 | 0x00 | 0x01 | 0x00 | `08 00 01 00` |
| 9 | 0x00 | 0x00 | 0x00 | 0x00 | 0x00 | `00 00 00 00` |
| 10 | 0x04 | 0x01 | 0x00 | 0xF4 | 0x00 | `01 00 F4 00` |
| 11 | 0x05 | 0x01 | 0x00 | 0xF3 | 0x00 | `01 00 F3 00` |
| 12 | 0x0B | 0x04 | 0x00 | 0x01 | 0x00 | `04 00 01 00` |
| 13 | 0x0C | 0x04 | 0x00 | 0x02 | 0x00 | `04 00 02 00` |
| 14 | 0x0D | 0x04 | 0x00 | 0x03 | 0x00 | `04 00 03 00` |
| 15 | 0x0E | 0x04 | 0x00 | 0x04 | 0x00 | `04 00 04 00` |
| 16 | 0x06 | 0x07 | 0x00 | 0x03 | 0x00 | `07 00 03 00` |
| 17 | 0x71 | 0x07 | 0x00 | 0x04 | 0x02 | `07 00 04 02` |
| 18 | 0x07 | 0x07 | 0x00 | 0x01 | 0x00 | `07 00 01 00` |
| 19 | 0x08 | 0x07 | 0x00 | 0x02 | 0x00 | `07 00 02 00` |
| 20 | 0x68 | 0x05 | 0x00 | 0x01 | 0x00 | `05 00 01 00` |
| 21 | 0x69 | 0x05 | 0x00 | 0x02 | 0x00 | `05 00 02 00` |
| 22 | 0x70 | 0x05 | 0x00 | 0x03 | 0x00 | `05 00 03 00` |
| 23 | 0x16 | 0x09 | 0x00 | 0x00 | 0x00 | `09 00 00 00` |
| 24 | 0x32 | 0x0B | 0x00 | 0x00 | 0x00 | `0B 00 00 00` |
| 25 | 0x18 | 0x06 | 0x00 | 0x00 | 0x00 | `06 00 00 00` |
| 26 | 0x0A | 0x0A | 0x00 | 0x00 | 0x00 | `0A 00 00 00` |
| 27 | 0x40 | 0x03 | 0x00 | 0x83 | 0x01 | `03 00 83 01` |
| 28 | 0x43 | 0x03 | 0x00 | 0xB6 | 0x00 | `03 00 B6 00` |
| 29 | 0x44 | 0x03 | 0x00 | 0xB5 | 0x00 | `03 00 B5 00` |
| 30 | 0x41 | 0x03 | 0x00 | 0xCD | 0x00 | `03 00 CD 00` |
| 31 | 0x42 | 0x03 | 0x00 | 0xB7 | 0x00 | `03 00 B7 00` |
| 32 | 0x47 | 0x03 | 0x00 | 0xE2 | 0x00 | `03 00 E2 00` |
| 33 | 0x45 | 0x03 | 0x00 | 0xE9 | 0x00 | `03 00 E9 00` |
| 34 | 0x46 | 0x03 | 0x00 | 0xEA | 0x00 | `03 00 EA 00` |
| 35 | 0x50 | 0x03 | 0x00 | 0x92 | 0x01 | `03 00 92 01` |
| 36 | 0x4F | 0x03 | 0x00 | 0x8A | 0x01 | `03 00 8A 01` |
| 37 | 0x49 | 0x03 | 0x00 | 0x2A | 0x02 | `03 00 2A 02` |
| 38 | 0x4C | 0x03 | 0x00 | 0x26 | 0x02 | `03 00 26 02` |
| 39 | 0x51 | 0x03 | 0x00 | 0x94 | 0x01 | `03 00 94 01` |
| 40 | 0x4D | 0x03 | 0x00 | 0x27 | 0x02 | `03 00 27 02` |
| 41 | 0x48 | 0x03 | 0x00 | 0x23 | 0x02 | `03 00 23 02` |
| 42 | 0x4E | 0x03 | 0x00 | 0x21 | 0x02 | `03 00 21 02` |
| 43 | 0x4A | 0x03 | 0x00 | 0x25 | 0x02 | `03 00 25 02` |
| 44 | 0x4B | 0x03 | 0x00 | 0x24 | 0x02 | `03 00 24 02` |
| 45 | 0x21 | 0x00 | 0x01 | 0x06 | 0x00 | `00 01 06 00` |
| 46 | 0x20 | 0x00 | 0x01 | 0x1B | 0x00 | `00 01 1B 00` |
| 47 | 0x2F | 0x00 | 0x01 | 0x11 | 0x00 | `00 01 11 00` |
| 48 | 0x23 | 0x00 | 0x01 | 0x12 | 0x00 | `00 01 12 00` |
| 49 | 0x22 | 0x00 | 0x01 | 0x19 | 0x00 | `00 01 19 00` |
| 50 | 0x29 | 0x00 | 0x01 | 0x13 | 0x00 | `00 01 13 00` |
| 51 | 0x26 | 0x00 | 0x01 | 0x1C | 0x00 | `00 01 1C 00` |
| 52 | 0x24 | 0x00 | 0x01 | 0x16 | 0x00 | `00 01 16 00` |
| 53 | 0x28 | 0x00 | 0x01 | 0x04 | 0x00 | `00 01 04 00` |
| 54 | 0x27 | 0x00 | 0x01 | 0x1D | 0x00 | `00 01 1D 00` |
| 55 | 0x25 | 0x00 | 0x01 | 0x09 | 0x00 | `00 01 09 00` |
| 56 | 0x2C | 0x00 | 0x08 | 0x07 | 0x00 | `00 08 07 00` |
| 57 | 0x2D | 0x00 | 0x08 | 0x15 | 0x00 | `00 08 15 00` |
| 58 | 0x2B | 0x00 | 0x04 | 0x2B | 0x00 | `00 04 2B 00` |
| 59 | 0x2A | 0x00 | 0x04 | 0x3D | 0x00 | `00 04 3D 00` |
| 60 | 0x2E | 0x00 | 0x08 | 0x0F | 0x00 | `00 08 0F 00` |

Patterns visible in the dump: `A` is a coarse function class and `C` (sometimes `D`) is the code inside it — mouse buttons are `A=1` with the wire opcode in `C` (`F0` left, `F1` right, `F2` middle, `F3`/`F4` X-buttons); wheel steps are `A=4`, `C=1..4`; fixed-function shortcuts are `A=0`, `B` selecting a sub-table with the key index in `C`; the `0x40..0x51` block is one class (`A=3`) with per-key codes in `C`; `0x15` (shortcut) and `0x00` (empty) are fully overridden by the code. The action id is only ever compared against `entry+0xC9`, so a rebuild can ship this table verbatim. Mapping each id to its `lan.xml` label requires following the menu-command chain in `FUN_00406db0`; that label mapping is not transcribed here. [C] bytes; [I] class meaning.
