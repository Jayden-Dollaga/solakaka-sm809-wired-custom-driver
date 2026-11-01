"""Main window and application coordinator for the SM809 rebuild.

The window owns:

* the portable data store (its own copy of profile.bin and friends),
* the device service (HID link, apply engine, monitor events),
* the five page controllers,
* profile management and the apply / connect workflows.

Threads never touch widgets directly.  Background work posts callables through
:meth:`App.post`, which drains a queue from the Tk event loop.
"""

from __future__ import annotations

import collections
import os
import queue
import sys
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk

from . import theme
from ..config import load_config
from ..device import ApplyResult, DeviceService
from ..model import PROFILE_COUNT, DataStore, Profile
from ..paths import DATA_DIR, ensure_data_dir, logo_path
from ..protocol import SENSOR_INFO, sensor_display_dpi, sensor_max_label
from ..transport import IS_WINDOWS, describe_interfaces
from . import dialogs
from .pages.gun import GunPage
from .pages.keys import KeysPage
from .pages.light import LightPage
from .pages.macro import MacroPage
from .pages.performance import PerformancePage


PAGE_CLASSES = (
    ("keys", "Buttons", KeysPage),
    ("performance", "Performance", PerformancePage),
    ("light", "Lighting", LightPage),
    ("macro", "Macros", MacroPage),
    ("gun", "Gun recoil", GunPage),
)


class App(tk.Tk):
    def __init__(self, *, demo: bool | None = None, data_dir: Path | None = None):
        super().__init__()
        self.withdraw()
        self._closing = False
        self._applying = False
        self._dirty = False
        self._loading_profiles = False
        self._poll_job = None
        self._queue: queue.Queue = queue.Queue()
        self._queue_job = None
        self._busy: dialogs.BusyWindow | None = None
        self._overlay: dialogs.DpiOverlay | None = None
        self._log_lines: collections.deque[str] = collections.deque(maxlen=300)
        self._pages: dict[str, object] = {}
        self._tab_buttons: dict[str, tk.Button] = {}
        self._current_page = ""

        if data_dir is None:
            ensure_data_dir()
            self.data_dir = DATA_DIR
        else:
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            (self.data_dir / "Data").mkdir(parents=True, exist_ok=True)

        self.config = load_config(self.data_dir / "Data.ini")
        self.store = DataStore(self.data_dir / "Data")

        self._demo = True if not IS_WINDOWS else bool(demo)
        self._build_service()

        theme.init_theme(self)
        self.configure(bg=theme.BG)
        self.title("SM809 Control Center")
        self.minsize(1100, 700)
        self._center_window()
        self._build_ui()
        self._load_logo()
        self._refresh_profiles()
        self._refresh_device()
        self._refresh_sidebar_info()
        for page in self._pages.values():
            page.refresh()
        self._show_page("keys")
        self._overlay = dialogs.DpiOverlay(self)

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.bind("<Control-s>", self._hotkey_apply)
        for index, (key, _label, _cls) in enumerate(PAGE_CLASSES, start=1):
            self.bind(f"<Control-Key-{index}>", lambda _e, k=key: self._show_page(k))
        self._queue_job = self.after(40, self._drain_queue)
        self._poll_device()
        self.deiconify()
        self.lift()
        if self._demo:
            self._set_status(
                "Demo mode is on. Press Connect to simulate the mouse, then Apply.",
                "info",
            )
        else:
            self._set_status(
                "Ready. Connect the mouse and press Apply, or tick Demo mode to explore.",
                "info",
            )

    # ------------------------------------------------------------------
    # construction
    # ------------------------------------------------------------------
    def _center_window(self) -> None:
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        width = min(1320, max(1100, sw - 100))
        height = min(860, max(700, sh - 120))
        x = max(0, (sw - width) // 2)
        y = max(0, (sh - height) // 2 - 10)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_service(self) -> None:
        service = DeviceService(self.config, self.store, demo=self._demo)
        service.on_log = lambda text: self.post(lambda: self._append_log(text))
        service.on_device_event = lambda event, value: self.post(
            lambda: self._device_event(event, value)
        )
        service.on_profile_changed = lambda kind: self.post(
            lambda: self._profile_changed(kind)
        )
        service.on_disconnect = lambda: self.post(self._transport_lost)
        self.service = service

    def _build_ui(self) -> None:
        self._build_header()
        tk.Frame(self, bg=theme.BORDER, height=1).pack(fill="x")

        body = tk.Frame(self, bg=theme.BG)
        body.pack(fill="both", expand=True)
        self._build_sidebar(body)

        main = tk.Frame(body, bg=theme.BG)
        main.pack(side="left", fill="both", expand=True)
        self._build_tabs(main)
        self._page_host = tk.Frame(main, bg=theme.BG)
        self._page_host.pack(fill="both", expand=True)

        for key, _label, cls in PAGE_CLASSES:
            self._pages[key] = cls(self._page_host, self)

        self._build_statusbar()

    def _build_header(self) -> None:
        header = tk.Frame(self, bg=theme.SURFACE)
        header.pack(fill="x")
        inner = tk.Frame(header, bg=theme.SURFACE, padx=20, pady=12)
        inner.pack(fill="x")

        brand = tk.Frame(inner, bg=theme.SURFACE)
        brand.pack(side="left")
        self._logo_holder = tk.Frame(
            brand, bg=theme.SURFACE, width=48, height=48,
            highlightbackground=theme.BORDER, highlightthickness=1,
        )
        self._logo_holder.pack(side="left")
        self._logo_holder.pack_propagate(False)

        titles = tk.Frame(brand, bg=theme.SURFACE)
        titles.pack(side="left", padx=(12, 0))
        tk.Label(titles, text="SM809 Control Center", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h1"]).pack(anchor="w")
        tk.Label(titles, text="Wired mouse utility rebuild  -  profiles, DPI, lighting, "
                              "macros and recoil tables",
                 bg=theme.SURFACE, fg=theme.MUTED, font=theme.FONTS["small"]
                 ).pack(anchor="w", pady=(2, 0))

        self.apply_btn = theme.button(inner, "Apply profile   Ctrl+S", self.apply_now,
                                      kind="primary")
        self.apply_btn.pack(side="right")
        self.connect_btn = theme.button(inner, "Connect", self._toggle_connection,
                                        kind="secondary")
        self.connect_btn.pack(side="right", padx=(0, 10))

        self._pill = tk.Frame(inner, bg=theme.SURFACE_ALT, padx=12, pady=7,
                              highlightbackground=theme.BORDER, highlightthickness=1)
        self._pill.pack(side="right", padx=(0, 12))
        dot = tk.Canvas(self._pill, width=12, height=12, bg=theme.SURFACE_ALT,
                        highlightthickness=0, bd=0)
        dot.pack(side="left", padx=(0, 8))
        self._pill_dot = dot
        self._pill_oval = dot.create_oval(2, 2, 10, 10, fill=theme.MUTED, outline="")
        text = tk.Frame(self._pill, bg=theme.SURFACE_ALT)
        text.pack(side="left")
        self._pill_title = tk.Label(text, text="Not connected", bg=theme.SURFACE_ALT,
                                    fg=theme.TEXT, font=theme.FONTS["bold"])
        self._pill_title.pack(anchor="w")
        self._pill_sub = tk.Label(text, text="VID 04D9 / PID A09F", bg=theme.SURFACE_ALT,
                                  fg=theme.MUTED, font=theme.FONTS["tiny"])
        self._pill_sub.pack(anchor="w")

    def _build_sidebar(self, parent) -> None:
        side = tk.Frame(parent, bg=theme.SURFACE, width=268)
        side.pack(side="left", fill="y")
        side.pack_propagate(False)

        inner = tk.Frame(side, bg=theme.SURFACE, padx=14, pady=14)
        inner.pack(fill="both", expand=True)

        title = tk.Frame(inner, bg=theme.SURFACE)
        title.pack(fill="x")
        tk.Label(title, text="Profiles", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(side="left")
        self.profile_count = tk.Label(title, text="", bg=theme.SURFACE, fg=theme.MUTED,
                                      font=theme.FONTS["small"])
        self.profile_count.pack(side="right")

        wrap = tk.Frame(inner, bg=theme.SURFACE)
        wrap.pack(fill="x", pady=(8, 0))
        self.profile_list = tk.Listbox(
            wrap, height=10, exportselection=False, activestyle="none",
            bg=theme.SURFACE_ALT, fg=theme.TEXT,
            selectbackground=theme.ACCENT_DARK, selectforeground="#ffffff",
            highlightthickness=1, highlightbackground=theme.BORDER,
            relief="flat", bd=0, font=theme.FONTS["base"],
        )
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.profile_list.yview)
        self.profile_list.configure(yscrollcommand=vsb.set)
        self.profile_list.pack(side="left", fill="x", expand=True)
        vsb.pack(side="right", fill="y")
        self.profile_list.bind("<<ListboxSelect>>", self._profile_selected)

        row = tk.Frame(inner, bg=theme.SURFACE)
        row.pack(fill="x", pady=(8, 0))
        theme.button(row, "New", self._new_profile, kind="secondary").pack(side="left")
        theme.button(row, "Duplicate", self._duplicate_profile, kind="ghost").pack(
            side="left", padx=(6, 0))
        theme.button(row, "Delete", self._delete_profile, kind="danger").pack(side="right")

        tk.Label(inner, text="Profile name", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(anchor="w", pady=(12, 4))
        name_row = tk.Frame(inner, bg=theme.SURFACE)
        name_row.pack(fill="x")
        self.profile_name_var = tk.StringVar()
        self.profile_name = theme.entry(name_row, self.profile_name_var, width=18)
        self.profile_name.pack(side="left", fill="x", expand=True)
        self.profile_name.bind("<Return>", lambda _e: self._commit_profile_name())
        self.profile_name.bind("<FocusOut>", lambda _e: self._commit_profile_name())
        theme.button(name_row, "Rename", self._commit_profile_name, kind="ghost").pack(
            side="left", padx=(6, 0))

        theme.separator(inner).pack(fill="x", pady=12)

        actions = tk.Frame(inner, bg=theme.SURFACE)
        actions.pack(fill="x")
        for i, (text, command) in enumerate((
            ("Reset", self._reset_profile),
            ("Export", self._export_profile),
            ("Import", self._import_profile),
        )):
            theme.button(actions, text, command, kind="ghost").pack(
                side="left", padx=(0 if i == 0 else 6, 0))
        theme.button(inner, "More actions", self._sidebar_menu, kind="secondary").pack(
            fill="x", pady=(8, 0))

        device = tk.Frame(inner, bg=theme.SURFACE_ALT, padx=12, pady=10,
                          highlightbackground=theme.BORDER, highlightthickness=1)
        device.pack(side="bottom", fill="x", pady=(12, 0))
        tk.Label(device, text="DEVICE", bg=theme.SURFACE_ALT, fg=theme.DIM,
                 font=theme.FONTS["tiny"]).pack(anchor="w")
        self.side_device = tk.Label(device, text="Not connected", bg=theme.SURFACE_ALT,
                                    fg=theme.TEXT, font=theme.FONTS["bold"])
        self.side_device.pack(anchor="w")
        self.side_firmware = tk.Label(device, text="", bg=theme.SURFACE_ALT, fg=theme.MUTED,
                                      font=theme.FONTS["small"])
        self.side_firmware.pack(anchor="w")
        self.side_sensor = tk.Label(device, text="", bg=theme.SURFACE_ALT, fg=theme.MUTED,
                                    font=theme.FONTS["small"], justify="left")
        self.side_sensor.pack(anchor="w", pady=(4, 0))
        self.side_path = tk.Label(device, text="", bg=theme.SURFACE_ALT, fg=theme.DIM,
                                  font=theme.FONTS["tiny"], wraplength=210,
                                  justify="left", anchor="w")
        self.side_path.pack(anchor="w", pady=(6, 0))

    def _build_tabs(self, parent) -> None:
        bar = tk.Frame(parent, bg=theme.BG, padx=18, pady=10)
        bar.pack(fill="x")
        for key, label, _cls in PAGE_CLASSES:
            btn = tk.Button(
                bar, text=label, command=lambda k=key: self._show_page(k),
                bg=theme.BG, fg=theme.MUTED, activebackground=theme.SURFACE_ALT,
                activeforeground=theme.TEXT, relief="flat", bd=0,
                highlightthickness=0, padx=16, pady=8, cursor="hand2",
                font=theme.FONTS["base"],
            )
            btn.pack(side="left")
            self._tab_buttons[key] = btn
        tk.Frame(parent, bg=theme.BORDER, height=1).pack(fill="x", padx=18, pady=(6, 0))

    def _build_statusbar(self) -> None:
        bar = tk.Frame(self, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                       highlightthickness=1)
        bar.pack(fill="x", side="bottom")
        inner = tk.Frame(bar, bg=theme.SURFACE, padx=14, pady=5)
        inner.pack(fill="x")

        self._status_dot = tk.Canvas(inner, width=10, height=10, bg=theme.SURFACE,
                                     highlightthickness=0, bd=0)
        self._status_dot.pack(side="left", padx=(0, 8))
        self._status_oval = self._status_dot.create_oval(2, 2, 8, 8, fill=theme.MUTED,
                                                         outline="")
        self.status_var = tk.StringVar(value="Ready.")
        self.status_label = tk.Label(inner, textvariable=self.status_var, bg=theme.SURFACE,
                                     fg=theme.TEXT, font=theme.FONTS["small"], anchor="w")
        self.status_label.pack(side="left")

        self.sync_label = tk.Label(inner, text="", bg=theme.SURFACE, fg=theme.MUTED,
                                   font=theme.FONTS["small"])
        self.sync_label.pack(side="right", padx=(10, 0))
        self._demo_var = tk.IntVar(value=1 if self._demo else 0)
        self._demo_check = tk.Checkbutton(
            inner, text="Demo mode", variable=self._demo_var, command=self._demo_toggled,
            bg=theme.SURFACE, fg=theme.MUTED, activebackground=theme.SURFACE,
            activeforeground=theme.TEXT, selectcolor=theme.SURFACE_ALT,
            highlightthickness=0, bd=0, font=theme.FONTS["small"], cursor="hand2",
        )
        self._demo_check.pack(side="right", padx=(16, 4))
        if not IS_WINDOWS:
            self._demo_check.configure(state="disabled")
        tk.Label(inner, text=f"Data: {self.data_dir}", bg=theme.SURFACE, fg=theme.DIM,
                 font=theme.FONTS["tiny"]).pack(side="right", padx=(16, 0))

    def _load_logo(self) -> None:
        try:
            image = tk.PhotoImage(file=str(logo_path()), master=self)
            factor = max(1, image.width() // 42)
            if factor > 1:
                image = image.subsample(factor, factor)
            tk.Label(self._logo_holder, image=image, bg=theme.SURFACE, bd=0).pack(
                fill="both", expand=True)
            self._logo_image = image
            try:
                self.iconphoto(True, image)
            except tk.TclError:
                pass
        except Exception:
            tk.Label(self._logo_holder, text="SM", bg=theme.SURFACE_ALT, fg=theme.ACCENT,
                     font=theme.FONTS["h2"]).pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # pages
    # ------------------------------------------------------------------
    def _show_page(self, key: str) -> None:
        if key not in self._pages or key == self._current_page:
            page = self._pages.get(key)
            if page is not None:
                page.refresh()
                page.on_show()
            return
        if self._current_page:
            self._pages[self._current_page].pack_forget()
        page = self._pages[key]
        page.pack(fill="both", expand=True)
        self._current_page = key
        for name, button in self._tab_buttons.items():
            active = name == key
            button.configure(
                bg=theme.SURFACE_ALT if active else theme.BG,
                fg=theme.ACCENT if active else theme.MUTED,
                font=theme.FONTS["bold"] if active else theme.FONTS["base"],
            )
        page.refresh()
        page.on_show()

    def _refresh_current_page(self) -> None:
        page = self._pages.get(self._current_page)
        if page is not None:
            page.refresh()
            page.on_show()

    def _refresh_page_if(self, key: str) -> None:
        if self._current_page != key:
            return
        page = self._pages.get(key)
        if page is not None:
            page.refresh()

    # ------------------------------------------------------------------
    # status / dirty state
    # ------------------------------------------------------------------
    def _set_status(self, text: str, kind: str = "info") -> None:
        if self._closing:
            return
        self.status_var.set(text)
        color = {
            "info": theme.TEXT, "muted": theme.MUTED, "ok": theme.GREEN,
            "warn": theme.AMBER, "error": theme.RED,
        }.get(kind, theme.TEXT)
        self.status_label.configure(fg=color)
        self._status_dot.itemconfigure(self._status_oval, fill=theme.status_color(kind))

    def _set_sync(self, text: str, color: str = theme.MUTED) -> None:
        if hasattr(self, "sync_label"):
            self.sync_label.configure(text=text, fg=color)

    def mark_dirty(self, reason: str = "profile edited") -> None:
        self._dirty = True
        if self._closing:
            return
        self._set_sync("Not applied", theme.AMBER)
        self._set_status(f"Modified: {reason}. Press Apply to send it to the mouse.", "warn")
        self._refresh_title()

    def _refresh_title(self) -> None:
        if self._closing:
            return
        name = self.store.profile.name or "Profile"
        star = " *" if self._dirty else ""
        self.title(f"SM809 Control Center - {name}{star}")

    def _append_log(self, text: str) -> None:
        self._log_lines.append(f"{time.strftime('%H:%M:%S')}  {text}")

    # ------------------------------------------------------------------
    # background queue
    # ------------------------------------------------------------------
    def post(self, callback) -> None:
        try:
            self._queue.put(callback)
        except Exception:
            pass

    def _drain_queue(self) -> None:
        self._queue_job = None
        if self._closing:
            return
        while True:
            try:
                callback = self._queue.get_nowait()
            except queue.Empty:
                break
            try:
                callback()
            except Exception as exc:
                self._append_log(f"UI callback failed: {exc}")
        if not self._closing:
            self._queue_job = self.after(40, self._drain_queue)

    # ------------------------------------------------------------------
    # profile management
    # ------------------------------------------------------------------
    def _unique_profile_name(self) -> str:
        used = {p.name for p in self.store.profiles}
        n = len(self.store.profiles) + 1
        while f"Profile {n}" in used:
            n += 1
        return f"Profile {n}"

    def _refresh_profiles(self) -> None:
        self._loading_profiles = True
        try:
            self.profile_list.delete(0, "end")
            for profile in self.store.profiles:
                self.profile_list.insert("end", profile.name or "Unnamed profile")
            selected = self.store.selected
            if 0 <= selected < self.profile_list.size():
                self.profile_list.selection_clear(0, "end")
                self.profile_list.selection_set(selected)
                self.profile_list.activate(selected)
                self.profile_list.see(selected)
            self.profile_count.configure(
                text=f"{len(self.store.profiles)} / {PROFILE_COUNT}")
            self.profile_name_var.set(self.store.profile.name)
        finally:
            self._loading_profiles = False
        self._refresh_title()

    def _profile_selected(self, _event=None) -> None:
        if self._loading_profiles or self._closing:
            return
        selection = self.profile_list.curselection()
        if not selection:
            return
        index = int(selection[0])
        if index == self.store.selected:
            return
        self._flush_pending_edits()
        try:
            self.store.save_profiles()
        except Exception as exc:
            self._set_status(f"Could not save the current profile: {exc}", "error")
            return
        self.store.select(index)
        self.store.save_selected()
        self._dirty = False
        self._refresh_profiles()
        self._refresh_current_page()
        self._set_sync("Loaded", theme.MUTED)
        name = self.store.profile.name
        self._set_status(f"Profile '{name}' selected. Apply to send it to the mouse.", "info")
        self._refresh_title()

    def _profiles_changed(self, message: str) -> None:
        self._refresh_profiles()
        self._refresh_current_page()
        self._refresh_title()
        self._set_status(message, "info")

    def _new_profile(self) -> None:
        self._flush_pending_edits()
        try:
            self.store.add_profile()
        except ValueError as exc:
            dialogs.show_message(self, "Profile limit", str(exc), "warn")
            return
        self._dirty = False
        self._profiles_changed("New profile created from Default.pbin.")
        self._set_sync("Loaded", theme.MUTED)

    def _duplicate_profile(self) -> None:
        if len(self.store.profiles) >= PROFILE_COUNT:
            dialogs.show_message(self, "Profile limit",
                                 f"At most {PROFILE_COUNT} profiles are supported.", "warn")
            return
        self._flush_pending_edits()
        copy = Profile(self.store.profile.raw)
        copy.name = self._unique_profile_name()
        self.store.profiles.append(copy)
        self.store.selected = len(self.store.profiles) - 1
        self.store.save_profiles()
        self._dirty = False
        self._profiles_changed(f"Duplicated profile as '{copy.name}'.")
        self._set_sync("Loaded", theme.MUTED)

    def _delete_profile(self) -> None:
        index = self.store.selected
        profile = self.store.profile
        if len(self.store.profiles) <= 1:
            dialogs.show_message(self, "Cannot delete",
                                 "The last profile cannot be deleted.", "warn")
            return
        if not dialogs.ask_confirm(
            self, "Delete profile",
            f"Delete '{profile.name or 'Unnamed profile'}'? This only affects this "
            "portable data folder, never the original installation.",
            ok_text="Delete", danger=True,
        ):
            return
        try:
            self.store.delete_profile(index)
        except ValueError as exc:
            dialogs.show_message(self, "Cannot delete", str(exc), "warn")
            return
        self._dirty = False
        self._profiles_changed("Profile deleted.")
        self._set_sync("Loaded", theme.MUTED)

    def _reset_profile(self) -> None:
        if not dialogs.ask_confirm(
            self, "Reset profile",
            f"Restore '{self.store.profile.name}' from Default.pbin? Name is kept; "
            "all buttons, DPI, lighting and macro assignments are replaced.",
            ok_text="Reset", danger=True,
        ):
            return
        self.store.reset_profile()
        self._profiles_changed("Profile reset to Default.pbin.")
        self.mark_dirty("profile reset")

    def _commit_profile_name(self) -> None:
        if self._loading_profiles or self._closing:
            return
        name = self.profile_name_var.get().strip()
        if not name:
            self.profile_name_var.set(self.store.profile.name)
            return
        if name == self.store.profile.name:
            return
        try:
            self.store.rename_profile(name)
        except Exception as exc:
            self._set_status(f"Rename failed: {exc}", "error")
            return
        self._refresh_profiles()
        self._set_status("Profile renamed (names are local to this folder).", "info")

    def _export_profile(self) -> None:
        self._flush_pending_edits()
        try:
            self.store.save_profiles()
        except Exception:
            pass
        name = (self.store.profile.name or "profile").replace("/", "_").replace("\\", "_")
        path = filedialog.asksaveasfilename(
            parent=self, title="Export profile", defaultextension=".pbin",
            initialfile=f"{name}.pbin",
            filetypes=(("SM809 profile", "*.pbin"), ("All files", "*.*")),
        )
        if not path:
            return
        try:
            self.store.export_profile(Path(path))
        except Exception as exc:
            dialogs.show_message(self, "Export failed", str(exc), "error")
            return
        self._set_status(f"Exported profile to {path}", "ok")

    def _export_json(self) -> None:
        name = (self.store.profile.name or "profile").replace("/", "_").replace("\\", "_")
        path = filedialog.asksaveasfilename(
            parent=self, title="Export readable profile", defaultextension=".json",
            initialfile=f"{name}.json",
            filetypes=(("JSON", "*.json"), ("All files", "*.*")),
        )
        if not path:
            return
        try:
            self.store.export_json_file(Path(path))
        except Exception as exc:
            dialogs.show_message(self, "Export failed", str(exc), "error")
            return
        self._set_status(f"Exported readable profile to {path}", "ok")

    def _import_profile(self) -> None:
        path = filedialog.askopenfilename(
            parent=self, title="Import profile",
            filetypes=(("SM809 profile", "*.pbin"), ("All files", "*.*")),
        )
        if not path:
            return
        self._flush_pending_edits()
        try:
            profile = self.store.import_profile(Path(path))
        except Exception as exc:
            dialogs.show_message(self, "Import failed", str(exc), "error")
            return
        self._dirty = False
        self._profiles_changed(f"Imported '{profile.name}'.")
        self._set_sync("Loaded", theme.MUTED)

    def _sidebar_menu(self) -> None:
        menu = tk.Menu(self, tearoff=0, bg=theme.SURFACE_ALT, fg=theme.TEXT,
                       activebackground=theme.ACCENT_DARK, activeforeground="#ffffff",
                       bd=0)
        menu.add_command(label="Export readable JSON...", command=self._export_json)
        menu.add_separator()
        menu.add_command(label="Device diagnostics...", command=self._show_diagnostics)
        menu.add_command(label="Open data folder", command=self._open_data_folder)
        menu.add_command(label="Reload Data.ini", command=self._reload_data_ini)
        menu.add_separator()
        menu.add_command(label="About this rebuild", command=self._show_about)
        try:
            menu.tk_popup(self.profile_list.winfo_rootx(),
                          self.profile_list.winfo_rooty() + self.profile_list.winfo_height())
        finally:
            menu.grab_release()

    # ------------------------------------------------------------------
    # device
    # ------------------------------------------------------------------
    def _refresh_device(self) -> None:
        if self._closing:
            return
        service = self.service
        linked = service.linked
        if linked and service.demo:
            color = theme.PURPLE
            title = "Demo link"
            sub = "simulated device, no hardware writes"
        elif linked:
            color = theme.GREEN
            title = "Connected"
            sub = f"firmware {service.version[0]}.{service.version[1]}  -  control 0xFF00"
        else:
            color = theme.MUTED
            title = "Not connected"
            sub = f"VID {self.config.vid:04X} / PID {self.config.pid:04X}"
        try:
            self._pill_dot.itemconfigure(self._pill_oval, fill=color)
            self._pill_title.configure(text=title)
            self._pill_sub.configure(text=sub)
        except tk.TclError:
            return
        self.connect_btn.configure(
            text="Disconnect" if linked else ("Connect (demo)" if self._demo else "Connect"))
        self._refresh_sidebar_info()

    def _refresh_sidebar_info(self) -> None:
        if not hasattr(self, "side_device"):
            return
        service = self.service
        if service.linked:
            self.side_device.configure(
                text="Demo link" if service.demo else "Connected",
                fg=theme.PURPLE if service.demo else theme.GREEN)
            self.side_firmware.configure(
                text=f"firmware {service.version[0]}.{service.version[1]}")
        else:
            self.side_device.configure(text="Not connected", fg=theme.MUTED)
            self.side_firmware.configure(text="firmware unknown")
        self.side_sensor.configure(
            text=(f"sensor 0x{self.config.sensor:04X}  -  max "
                  f"{sensor_max_label(self.config.sensor)} DPI\n"
                  f"{len(self.store.profiles)} profiles  -  "
                  f"{len(self.store.macros)} macros  -  {len(self.store.guns)} gun tables"))
        try:
            shown = str(self.data_dir)
            self.side_path.configure(text=shown)
        except tk.TclError:
            pass

    def _toggle_connection(self) -> None:
        if self._applying or self._closing:
            return
        if self.service.linked:
            self.service.disconnect()
            self._refresh_device()
            self._set_status("Disconnected from the mouse.", "muted")
            return
        self._set_status("Connecting to the SM809...", "info")
        self.update_idletasks()
        ok = self.service.connect()
        self._refresh_device()
        if ok:
            version = self.service.version
            if self.service.demo:
                self._set_status(
                    f"Demo link ready (simulated firmware {version[0]}.{version[1]}).",
                    "ok")
            else:
                self._set_status(
                    f"Connected. Firmware {version[0]}.{version[1]}.", "ok")
            self._append_log("link established")
            self._refresh_sidebar_info()
            return
        message = self.service.last_error or "SM809 not found."
        self._set_status(message, "error")
        dialogs.show_message(
            self, "Connection failed",
            message + "\n\nCheck the USB cable and that no other SM809 utility is "
            "running. To explore the software without hardware, tick 'Demo mode' "
            "in the status bar.",
            "error",
        )

    def _demo_toggled(self) -> None:
        if self._applying:
            self._demo_var.set(1 if self._demo else 0)
            return
        target = bool(self._demo_var.get())
        if target == self._demo:
            return
        if self.service.linked:
            self.service.disconnect()
        self._demo = target
        self._build_service()
        self._refresh_device()
        if target:
            self._set_status("Demo mode enabled. Apply simulates the HID exchange.", "info")
        else:
            self._set_status("Demo mode disabled. Connect real hardware when ready.", "info")

    def _transport_lost(self) -> None:
        if self._closing:
            return
        self._refresh_device()
        self._set_status("Device disconnected.", "warn")

    def _poll_device(self) -> None:
        self._poll_job = None
        if self._closing:
            return
        service = self.service
        if service.linked and not service.demo:
            try:
                if not service.transport.connected or not service.present():
                    service.disconnect()
                    self._refresh_device()
                    self._set_status("Device unplugged or no longer present.", "warn")
            except Exception:
                pass
        self._poll_job = self.after(4000, self._poll_device)

    def _device_event(self, event: int, value: int) -> None:
        if self._closing:
            return
        if event == 0x7F00:
            self._refresh_device()
            if value == 1:
                self._set_status("Mouse connected.", "ok")
            elif value == 2:
                self._set_status("Mouse disconnected.", "warn")
            return
        if 0x0700 <= event <= 0x07FF:
            profile = self.store.profile
            stage = max(1, min(8, value)) - 1
            dpi = sensor_display_dpi(self.config.sensor, profile.dpi_values[min(stage, 7)])
            try:
                if self._overlay is not None:
                    self._overlay.show_value(f"Stage {stage + 1}  -  {dpi:,} DPI")
            except tk.TclError:
                pass
            self._refresh_page_if("performance")
            self._refresh_page_if("light")
            self._set_status(f"Mouse selected DPI stage {stage + 1} ({dpi:,} DPI).", "info")
            return
        if 0x0500 <= event <= 0x05FF:
            self._refresh_page_if("performance")
            self._set_status(f"Mouse changed report rate (value {value}).", "info")
            return
        if 0x0800 <= event <= 0x08FF:
            self._refresh_page_if("performance")
            mode = "Office" if self.store.profile.mode else "Game"
            self._set_status(f"Mouse changed work mode to {mode}.", "info")
            return
        self._append_log(f"device event 0x{event:04X} value {value}")

    def _profile_changed(self, kind: str) -> None:
        self._append_log(f"device updated profile field: {kind}")
        self._refresh_page_if("performance")
        self._refresh_page_if("light")

    # ------------------------------------------------------------------
    # apply
    # ------------------------------------------------------------------
    def _flush_pending_edits(self) -> None:
        for key in ("macro", "gun"):
            page = self._pages.get(key)
            flush = getattr(page, "_flush_edits", None)
            if callable(flush):
                try:
                    flush()
                except Exception:
                    pass

    def apply_now(self) -> None:
        if self._closing:
            return
        if self._applying:
            self._set_status("An apply is already running.", "warn")
            return
        self._flush_pending_edits()
        try:
            self.store.save_profiles()
        except Exception as exc:
            self._set_status(f"Could not save the profile: {exc}", "error")
            return

        self._applying = True
        self.apply_btn.configure(state="disabled")
        self._set_status("Applying profile to the mouse...", "info")
        try:
            self._busy = dialogs.BusyWindow(
                self, "Sending status, buttons, DPI, lighting and macros...")
        except tk.TclError:
            self._busy = None

        def worker() -> None:
            try:
                result = self.service.apply(self.store.profile)
            except Exception as exc:  # pragma: no cover - defensive
                result = ApplyResult(ok=False, error=str(exc))
            self.post(lambda: self._apply_done(result))

        threading.Thread(target=worker, name="sm809-apply", daemon=True).start()

    def _apply_done(self, result: ApplyResult) -> None:
        if self._closing:
            return
        self._applying = False
        self.apply_btn.configure(state="normal")
        if self._busy is not None:
            try:
                self._busy.close()
            except tk.TclError:
                pass
            self._busy = None

        if result.error:
            self._set_sync("Not applied", theme.RED)
            self._set_status(f"Apply failed: {result.error}", "error")
            if "SetFeature" in result.error or "WriteUSB" in result.error:
                self.service.disconnect()
                self._refresh_device()
            dialogs.show_message(
                self, "Apply failed",
                result.error + "\n\nThe profile is still saved in this data folder. "
                "Reconnect the mouse and try again.",
                "error",
            )
            return

        linked = self.service.linked
        if linked:
            self._dirty = False
            self._set_sync("Synced", theme.GREEN)
            self._set_status(
                f"Applied to the mouse: {result.sent_packets} feature packets, "
                f"{result.sent_blocks} data blocks.", "ok")
        else:
            self._set_sync("Saved locally", theme.AMBER)
            self._set_status("Device not connected. Profile saved locally only.", "warn")

        self._refresh_device()
        self._refresh_title()
        visible = [w for w in result.warnings if not w.startswith("Data.ini Distance=0")]
        if visible:
            dialogs.show_message(
                self, "Applied with notes" if linked else "Saved locally",
                "\n\n".join(visible), "warn", )

    # ------------------------------------------------------------------
    # diagnostics
    # ------------------------------------------------------------------
    def _diagnostics_text(self) -> str:
        service = self.service
        profile = self.store.profile
        lines = [
            "SM809 Control Center - diagnostics",
            time.strftime("%Y-%m-%d %H:%M:%S"),
            f"Python {sys.version.split()[0]} on {sys.platform}",
            "",
            f"Demo mode: {'yes' if self._demo else 'no'}",
            f"Linked: {'yes' if service.linked else 'no'}",
            f"Firmware: {service.version[0]}.{service.version[1]} "
            f"(Data.ini expects {self.config.ver_h}.{self.config.ver_l})",
            f"VID/PID: {self.config.vid:04X}/{self.config.pid:04X}",
            f"Password: {'yes' if self.config.has_password else 'no'}",
            f"Distance: {self.config.distance} "
            f"(lift-off frames {'enabled' if self.config.distance else 'skipped'})",
            f"Sensor: 0x{self.config.sensor:04X}  "
            f"max {sensor_max_label(self.config.sensor)} DPI",
            "",
            f"Data folder: {self.data_dir}",
            f"Profiles: {len(self.store.profiles)} (selected {self.store.selected + 1})",
            f"Macros: {len(self.store.macros)}   Gun tables: {len(self.store.guns)}",
            f"Profile: {profile.name!r}",
            f"Stage: {profile.stage + 1}/{profile.stage_count}  rate index {profile.rate}  "
            f"mode {'Office' if profile.mode else 'Game'}",
            f"DPI stages: {profile.dpi_values[: profile.stage_count]}",
            "",
            "HID interfaces:",
        ]
        if self._demo:
            lines.append("  (demo mode - hardware is not enumerated)")
        elif not IS_WINDOWS:
            lines.append("  (HID transport requires Windows)")
        else:
            try:
                lines.extend("  " + line for line in describe_interfaces(self.config).splitlines())
            except Exception as exc:
                lines.append(f"  enumeration failed: {exc}")
        lines.append("")
        lines.append("Recent log:")
        recent = list(self._log_lines)[-18:]
        if recent:
            lines.extend("  " + line for line in recent)
        else:
            lines.append("  (empty)")
        return "\n".join(lines)

    def _show_diagnostics(self) -> None:
        self._set_status("Scanning HID interfaces...", "info")
        self.update_idletasks()
        text = self._diagnostics_text()
        self._set_status("Diagnostics ready.", "info")
        self._show_text("Device diagnostics", text)

    def _show_about(self) -> None:
        text = (
            "SM809 Control Center\n"
            "A clean-room rebuild of the Solakaka SM809 wired mouse utility.\n\n"
            "The rebuild follows analysis/OVERVIEW.md and the disassembly of the\n"
            "shipped executable: the same HID frames, apply order, profile layout\n"
            "and file formats. Corrections applied where the original is visibly\n"
            "buggy (status packet byte order, shortcut mask/key placement, macro\n"
            "header loop order, gun upload).\n\n"
            "Differences worth knowing:\n"
            "  - This app uses its own data folder; the original is untouched.\n"
            "  - Gun tables are uploaded best-effort; the shipped app never did.\n"
            "  - Windows pointer settings use the documented SPI arguments.\n"
            "  - Macro recording uses documented hooks and the same key table.\n\n"
            "Hardware-specific behaviour (LED timing, sensor response, recoil\n"
            "tables) could not be verified without the mouse."
        )
        self._show_text("About this rebuild", text)

    def _show_text(self, title: str, text: str) -> None:
        win = tk.Toplevel(self, bg=theme.BG)
        win.title(title)
        win.transient(self)
        win.geometry("760x560")
        win.minsize(560, 360)
        try:
            win.grab_set()
        except tk.TclError:
            pass
        frame = tk.Frame(win, bg=theme.SURFACE, padx=16, pady=14)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(frame, text=title, bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        wrap = tk.Frame(frame, bg=theme.SURFACE)
        wrap.pack(fill="both", expand=True, pady=(10, 10))
        view = tk.Text(wrap, bg=theme.SURFACE_ALT, fg=theme.TEXT, relief="flat", bd=0,
                       highlightthickness=1, highlightbackground=theme.BORDER,
                       insertbackground=theme.TEXT, font=theme.FONTS["mono"],
                       wrap="word", padx=10, pady=8)
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=view.yview)
        view.configure(yscrollcommand=vsb.set)
        view.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        view.insert("1.0", text)
        view.configure(state="disabled")
        bar = tk.Frame(frame, bg=theme.SURFACE)
        bar.pack(fill="x")

        def copy() -> None:
            self.clipboard_clear()
            self.clipboard_append(text)

        theme.button(bar, "Close", win.destroy, kind="primary").pack(side="right")
        theme.button(bar, "Copy", copy, kind="secondary").pack(side="right", padx=(0, 8))
        win.protocol("WM_DELETE_WINDOW", win.destroy)
        win.bind("<Escape>", lambda _e: win.destroy())

    def _open_data_folder(self) -> None:
        if IS_WINDOWS:
            try:
                os.startfile(str(self.data_dir))  # type: ignore[attr-defined]
                return
            except Exception as exc:
                dialogs.show_message(self, "Open folder", str(exc), "error")
                return
        dialogs.show_message(self, "Data folder", str(self.data_dir), "info")

    def _reload_data_ini(self) -> None:
        try:
            config = load_config(self.data_dir / "Data.ini")
        except Exception as exc:
            dialogs.show_message(self, "Data.ini", f"Could not reload: {exc}", "error")
            return
        if self.service.linked:
            self.service.disconnect()
        self.config = config
        self.service.config = config
        self.service.transport.config = config
        for page in self._pages.values():
            try:
                page.refresh()
            except Exception:
                pass
        self._refresh_device()
        self._append_log("Data.ini reloaded")
        self._set_status("Data.ini reloaded. Reconnect the mouse if it was linked.", "info")

    # ------------------------------------------------------------------
    # macros
    # ------------------------------------------------------------------
    def sync_macro(self, index: int) -> None:
        """Copy a macro record into every profile button that references it."""
        if not (0 <= index < len(self.store.macros)):
            return
        record = self.store.macros[index]
        if record.is_folder:
            return
        events = record.events
        for i in range(64):
            entry = self.store.profile.button(i)
            if entry.action not in (0x16, 0x39):
                continue
            if entry.selected_index == index or entry.macro_index == index + 1:
                entry.name = record.name
                entry.loop = record.loop
                entry.set_events(events)
        if self._current_page == "keys":
            self._pages["keys"].refresh()

    def sync_gun(self, index: int) -> None:
        """Copy a gun table into every profile button that references it."""
        if not (0 <= index < len(self.store.guns)):
            return
        record = self.store.guns[index]
        if record.is_folder:
            return
        rows = record.bullet_slice()
        for i in range(64):
            entry = self.store.profile.button(i)
            if entry.action == 0x79 and entry.selected_index == index:
                entry.name = record.name
                entry.loop = 1
                entry.set_bullets(rows)
        if self._current_page == "keys":
            self._pages["keys"].refresh()

    # ------------------------------------------------------------------
    # misc
    # ------------------------------------------------------------------
    def _hotkey_apply(self, _event=None):
        self.apply_now()
        return "break"

    def _on_close(self) -> None:
        if self._applying:
            dialogs.show_message(
                self, "Apply in progress",
                "Wait for the profile upload to finish before closing.", "warn")
            return
        self._closing = True
        macro_page = self._pages.get("macro")
        if macro_page is not None and getattr(macro_page, "_recording", False):
            try:
                macro_page._stop_recording()
            except Exception:
                try:
                    macro_page.recorder.stop()
                except Exception:
                    pass
        if self._poll_job is not None:
            try:
                self.after_cancel(self._poll_job)
            except Exception:
                pass
            self._poll_job = None
        if self._queue_job is not None:
            try:
                self.after_cancel(self._queue_job)
            except Exception:
                pass
            self._queue_job = None
        try:
            self._flush_pending_edits()
            self.store.save_profiles()
            self.store.save_macros()
            self.store.save_guns()
        except Exception:
            pass
        try:
            self.service.disconnect()
        except Exception:
            pass
        if self._overlay is not None:
            try:
                self._overlay.destroy()
            except Exception:
                pass
        self.destroy()
