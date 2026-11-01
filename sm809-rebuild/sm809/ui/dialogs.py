"""Modal dialogs used by the SM809 rebuild UI."""

from __future__ import annotations

import sys
import tkinter as tk
from tkinter import ttk
from typing import Iterable

from ..keys import (
    MOD_ALT,
    MOD_CTRL,
    MOD_SHIFT,
    MOD_WIN,
    key_name,
    normalize_vk,
    shortcut_name,
)
from ..model import colorref_to_rgb, rgb_to_colorref
from ..protocol import (
    ACTION_GROUPS,
    ACTION_INFO,
    ACTION_INFO_MAP,
    ACTION_MAP,
    action_label,
    action_needs,
)
from . import theme
from .widgets import ColorSwatch, SliderRow, spin


class Modal(tk.Toplevel):
    def __init__(self, parent, title: str, *, width: int | None = None,
                 height: int | None = None, surface: bool = True):
        super().__init__(parent, bg=theme.BG)
        self.withdraw()
        self.title(title)
        self.transient(parent)
        self.resizable(False, False)
        self.result = None
        self._parent = parent
        self._want = (width, height)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind("<Escape>", lambda _e: self.cancel())
        outer = tk.Frame(self, bg=theme.SURFACE if surface else theme.BG, padx=18, pady=16)
        outer.pack(fill="both", expand=True)
        self.body = outer

    def show(self):
        self.update_idletasks()
        width = self._want[0] or self.winfo_reqwidth()
        height = self._want[1] or self.winfo_reqheight()
        try:
            px, py = self._parent.winfo_rootx(), self._parent.winfo_rooty()
            pw, ph = self._parent.winfo_width(), self._parent.winfo_height()
        except Exception:
            px = py = 0
            pw = ph = 0
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, px + (pw - width) // 2)
        y = max(0, py + (ph - height) // 2)
        x = min(x, max(0, sw - width - 20))
        y = min(y, max(0, sh - height - 60))
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()
        self.lift()
        try:
            self.grab_set()
            self.focus_force()
        except tk.TclError:
            pass
        self.wait_window(self)

    def cancel(self) -> None:
        self.result = None
        self.destroy()

    def footer(self, ok_text: str = "OK", *, extra: list[tuple[str, object]] | None = None,
               ok_kind: str = "primary") -> tk.Frame:
        bar = tk.Frame(self.body, bg=theme.SURFACE)
        bar.pack(fill="x", side="bottom", pady=(14, 0))
        ok = theme.button(bar, ok_text, self.accept, kind=ok_kind)
        ok.pack(side="right")
        cancel = theme.button(bar, "Cancel", self.cancel, kind="ghost")
        cancel.pack(side="right", padx=(0, 8))
        for text, command in extra or []:
            btn = theme.button(bar, text, command, kind="secondary")
            btn.pack(side="left")
        return bar

    def accept(self) -> None:
        self.destroy()


# ---------------------------------------------------------------------------
# Simple dialogs
# ---------------------------------------------------------------------------

class MessageDialog(Modal):
    def __init__(self, parent, title: str, text: str, kind: str = "info"):
        super().__init__(parent, title, width=460)
        color = {"info": theme.ACCENT, "warn": theme.AMBER, "error": theme.RED}[kind]
        head = tk.Frame(self.body, bg=theme.SURFACE)
        head.pack(fill="x")
        dot = tk.Canvas(head, width=34, height=34, bg=theme.SURFACE, highlightthickness=0)
        dot.create_oval(5, 5, 29, 29, fill=color, outline="")
        dot.create_text(17, 17, text="i" if kind == "info" else "!", fill="#ffffff",
                        font=theme.FONTS["bold"])
        dot.pack(side="left", padx=(0, 12))
        tk.Label(head, text=title, bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(side="left")
        tk.Label(self.body, text=text, bg=theme.SURFACE, fg=theme.TEXT,
                 wraplength=410, justify="left", anchor="w",
                 font=theme.FONTS["base"]).pack(fill="x", pady=(12, 16))
        theme.button(self.body, "Close", self.accept, kind="primary").pack(side="right")
        self.show()


def show_message(parent, title: str, text: str, kind: str = "info") -> None:
    MessageDialog(parent, title, text, kind)


class ConfirmDialog(Modal):
    def __init__(self, parent, title: str, text: str, *, ok_text: str = "Continue",
                 danger: bool = False):
        super().__init__(parent, title, width=460)
        tk.Label(self.body, text=title, bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        tk.Label(self.body, text=text, bg=theme.SURFACE, fg=theme.TEXT, wraplength=410,
                 justify="left", anchor="w").pack(fill="x", pady=(10, 16))
        bar = tk.Frame(self.body, bg=theme.SURFACE)
        bar.pack(fill="x")
        theme.button(bar, ok_text, self._yes, kind="danger" if danger else "primary").pack(side="right")
        theme.button(bar, "Cancel", self.cancel, kind="ghost").pack(side="right", padx=(0, 8))
        self.show()

    def _yes(self):
        self.result = True
        self.destroy()


def ask_confirm(parent, title: str, text: str, *, ok_text: str = "Continue",
                danger: bool = False) -> bool:
    return bool(ConfirmDialog(parent, title, text, ok_text=ok_text, danger=danger).result)


class TextDialog(Modal):
    def __init__(self, parent, title: str, prompt: str, initial: str = "",
                 *, limit: int = 49):
        super().__init__(parent, title, width=420)
        tk.Label(self.body, text=title, bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        tk.Label(self.body, text=prompt, bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(anchor="w", pady=(6, 8))
        self.var = tk.StringVar(value=initial)
        self.edit = theme.entry(self.body, self.var, width=44)
        self.edit.pack(fill="x")
        self.edit.bind("<Return>", lambda _e: self._ok())
        self.limit = limit
        self.footer("Save")
        self.after(80, lambda: (self.edit.focus_set(), self.edit.select_range(0, "end")))
        self.show()

    def _ok(self):
        text = self.var.get().strip()
        if not text:
            self.edit.configure(highlightbackground=theme.RED, highlightcolor=theme.RED)
            return
        self.result = text[: self.limit]
        self.destroy()

    def accept(self) -> None:
        self._ok()


def ask_text(parent, title: str, prompt: str, initial: str = "", *, limit: int = 49) -> str | None:
    return TextDialog(parent, title, prompt, initial, limit=limit).result


# ---------------------------------------------------------------------------
# Action picker
# ---------------------------------------------------------------------------

class ActionDialog(Modal):
    def __init__(self, parent, current: int = 0x01):
        super().__init__(parent, "Choose an action", width=620, height=560)
        tk.Label(self.body, text="Button action", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        tk.Label(self.body, text="Pick what this mouse button does. Shortcut, macro and "
                                 "gun actions ask for their parameters next.",
                 bg=theme.SURFACE, fg=theme.MUTED, font=theme.FONTS["small"]
                 ).pack(anchor="w", pady=(4, 10))

        search_bar = tk.Frame(self.body, bg=theme.SURFACE)
        search_bar.pack(fill="x")
        self.search = tk.StringVar()
        box = theme.entry(search_bar, self.search, width=42)
        box.pack(side="left")
        box.bind("<KeyRelease>", lambda _e: self._populate())
        tk.Label(search_bar, text="Search", bg=theme.SURFACE, fg=theme.DIM,
                 font=theme.FONTS["small"]).pack(side="left", padx=(8, 0))

        wrap = tk.Frame(self.body, bg=theme.SURFACE)
        wrap.pack(fill="both", expand=True, pady=(10, 0))
        self.tree = ttk.Treeview(wrap, show="tree", selectmode="browse")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", lambda _e: self._describe())
        self.tree.bind("<Double-1>", lambda _e: self._choose())
        self.tree.bind("<Return>", lambda _e: self._choose())

        self.desc = tk.Label(self.body, text="", bg=theme.SURFACE, fg=theme.MUTED,
                             font=theme.FONTS["small"], anchor="w", justify="left")
        self.desc.pack(fill="x", pady=(8, 0))

        bar = tk.Frame(self.body, bg=theme.SURFACE)
        bar.pack(fill="x", pady=(12, 0))
        theme.button(bar, "Select", self._choose, kind="primary").pack(side="right")
        theme.button(bar, "Cancel", self.cancel, kind="ghost").pack(side="right", padx=(0, 8))

        self._populate(current)
        self.show()

    def _populate(self, select: int | None = None) -> None:
        query = self.search.get().strip().lower()
        self.tree.delete(*self.tree.get_children())
        for group in ACTION_GROUPS:
            rows = [a for a in ACTION_INFO if a.group == group and
                    (not query or query in a.label.lower() or query in group.lower())]
            if not rows:
                continue
            parent = self.tree.insert("", "end", iid=f"g:{group}", text=group, open=True)
            for info in rows:
                iid = f"a:{info.code}"
                suffix = ""
                if info.needs:
                    suffix = f"   [{info.needs.replace('_', ' ')}]"
                self.tree.insert(parent, "end", iid=iid,
                                 text=f"{info.label}{suffix}   0x{info.code:02X}")
                if select is not None and info.code == select:
                    self.tree.selection_set(iid)
                    self.tree.see(iid)
                    self.tree.focus(iid)

    def _selected(self) -> int | None:
        sel = self.tree.selection()
        if not sel:
            return None
        iid = sel[0]
        if not iid.startswith("a:"):
            return None
        return int(iid[2:], 16)

    def _describe(self) -> None:
        code = self._selected()
        if code is None:
            info = ACTION_INFO_MAP.get(code) if code is not None else None
            self.desc.configure(text="")
            return
        info = ACTION_MAP.get(code)
        if info:
            detail = f"Action 0x{code:02X}  -  {action_label(code)}"
            needs = action_needs(code)
            if needs:
                detail += f"  (needs {needs.replace('_', ' ')})"
            self.desc.configure(text=detail)

    def _choose(self) -> None:
        code = self._selected()
        if code is None:
            self.tree.focus_set()
            return
        self.result = code
        self.destroy()


def pick_action(parent, current: int = 0x01) -> int | None:
    return ActionDialog(parent, current).result


# ---------------------------------------------------------------------------
# Shortcut capture
# ---------------------------------------------------------------------------

MODIFIER_VKS = {0x10, 0x11, 0x12, 0x5B, 0x5C, 0x5D, 0xA0, 0xA1, 0xA2, 0xA3, 0xA4, 0xA5}


class ShortcutDialog(Modal):
    def __init__(self, parent, key: int = 0, mods: int = 0):
        super().__init__(parent, "Shortcut", width=440)
        tk.Label(self.body, text="Assign a keyboard shortcut", bg=theme.SURFACE,
                 fg=theme.TEXT, font=theme.FONTS["h2"]).pack(anchor="w")
        tk.Label(self.body, text="Press the key combination now. Modifier keys are captured "
                                 "automatically; a single key is allowed.",
                 bg=theme.SURFACE, fg=theme.MUTED, font=theme.FONTS["small"],
                 wraplength=390, justify="left").pack(anchor="w", pady=(4, 12))
        self.key = key
        self.mods = mods
        self.capture = tk.Label(self.body, text=shortcut_name(key, mods), bg=theme.SURFACE_ALT,
                                fg=theme.ACCENT, font=theme.FONTS["h2"], padx=20, pady=18)
        self.capture.pack(fill="x")
        tk.Label(self.body, text="The shortcut is uploaded as modifier mask + virtual-key code.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"]).pack(anchor="w", pady=(6, 0))
        bar = tk.Frame(self.body, bg=theme.SURFACE)
        bar.pack(fill="x", pady=(14, 0))
        theme.button(bar, "Save", self.accept, kind="primary").pack(side="right")
        theme.button(bar, "Cancel", self.cancel, kind="ghost").pack(side="right", padx=(0, 8))
        theme.button(bar, "Clear", self._clear, kind="secondary").pack(side="left")
        self.bind("<KeyPress>", self._on_key)
        self.show()

    def _mods_now(self) -> int:
        if sys.platform != "win32":
            return 0
        try:
            import ctypes
            u = ctypes.windll.user32
            mods = 0
            if u.GetAsyncKeyState(0x11) & 0x8000:
                mods |= MOD_CTRL
            if u.GetAsyncKeyState(0x10) & 0x8000:
                mods |= MOD_SHIFT
            if u.GetAsyncKeyState(0x12) & 0x8000:
                mods |= MOD_ALT
            if u.GetAsyncKeyState(0x5B) & 0x8000 or u.GetAsyncKeyState(0x5C) & 0x8000:
                mods |= MOD_WIN
            return mods
        except Exception:
            return 0

    def _on_key(self, event) -> None:
        vk = normalize_vk(int(event.keycode))
        if vk in MODIFIER_VKS or vk == 0:
            return
        self.key = vk
        self.mods = self._mods_now()
        self.capture.configure(text=shortcut_name(self.key, self.mods))
        return "break"

    def _clear(self) -> None:
        self.key = 0
        self.mods = 0
        self.capture.configure(text="Shortcut")

    def accept(self) -> None:
        self.result = (self.key, self.mods)
        self.destroy()


def capture_shortcut(parent, key: int = 0, mods: int = 0) -> tuple[int, int] | None:
    return ShortcutDialog(parent, key, mods).result


# ---------------------------------------------------------------------------
# Fire click
# ---------------------------------------------------------------------------

class FireClickDialog(Modal):
    def __init__(self, parent, count: int = 3, interval: int = 50):
        super().__init__(parent, "Fire click", width=400)
        tk.Label(self.body, text="Fire click", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        tk.Label(self.body, text="Hold the button to repeat left clicks. The mouse receives "
                                 "the count and interval as single bytes.",
                 bg=theme.SURFACE, fg=theme.MUTED, font=theme.FONTS["small"],
                 wraplength=350, justify="left").pack(anchor="w", pady=(4, 12))
        grid = tk.Frame(self.body, bg=theme.SURFACE)
        grid.pack(fill="x")
        tk.Label(grid, text="Clicks", bg=theme.SURFACE, fg=theme.TEXT).grid(row=0, column=0, sticky="w")
        self.count = tk.IntVar(value=max(1, min(255, count)))
        spin(grid, self.count, 1, 255, width=8).grid(row=0, column=1, sticky="w", padx=(12, 0))
        tk.Label(grid, text="Interval (ms)", bg=theme.SURFACE, fg=theme.TEXT).grid(row=1, column=0, sticky="w", pady=(8, 0))
        self.interval = tk.IntVar(value=max(1, min(255, interval)))
        spin(grid, self.interval, 1, 255, width=8).grid(row=1, column=1, sticky="w", padx=(12, 0), pady=(8, 0))
        self.footer("Save")
        self.show()

    def accept(self):
        self.result = (max(1, int(self.count.get())), max(1, int(self.interval.get())))
        self.destroy()


def ask_fire(parent, count: int = 3, interval: int = 50):
    return FireClickDialog(parent, count, interval).result


# ---------------------------------------------------------------------------
# Record picker
# ---------------------------------------------------------------------------

class SelectRecordDialog(Modal):
    def __init__(self, parent, title: str, items: list[tuple[int, str]],
                 current: int | None = None, *, empty_text: str = "No records"):
        super().__init__(parent, title, width=420, height=380)
        tk.Label(self.body, text=title, bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        if not items:
            tk.Label(self.body, text=empty_text, bg=theme.SURFACE, fg=theme.MUTED).pack(
                anchor="w", pady=20)
            theme.button(self.body, "Close", self.accept, kind="primary").pack(side="right")
        else:
            wrap = tk.Frame(self.body, bg=theme.SURFACE)
            wrap.pack(fill="both", expand=True, pady=(10, 12))
            self.listbox = tk.Listbox(
                wrap, bg=theme.SURFACE_ALT, fg=theme.TEXT, selectbackground=theme.ACCENT_DARK,
                selectforeground="#ffffff", relief="flat", bd=0, highlightthickness=1,
                highlightbackground=theme.BORDER, activestyle="none",
                font=theme.FONTS["base"], exportselection=False,
            )
            vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.listbox.yview)
            self.listbox.configure(yscrollcommand=vsb.set)
            self.listbox.pack(side="left", fill="both", expand=True)
            vsb.pack(side="right", fill="y")
            self.items = items
            for i, (_idx, name) in enumerate(items):
                self.listbox.insert("end", f"{i + 1}.  {name}")
                if current is not None and _idx == current:
                    self.listbox.selection_set(i)
            self.listbox.bind("<Double-1>", lambda _e: self._ok())
            self.listbox.bind("<Return>", lambda _e: self._ok())
            bar = tk.Frame(self.body, bg=theme.SURFACE)
            bar.pack(fill="x")
            theme.button(bar, "Select", self._ok, kind="primary").pack(side="right")
            theme.button(bar, "Cancel", self.cancel, kind="ghost").pack(side="right", padx=(0, 8))
        self.show()

    def _ok(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.result = self.items[sel[0]][0]
        self.destroy()


def pick_record(parent, title: str, items: list[tuple[int, str]],
                current: int | None = None, *, empty_text: str = "") -> int | None:
    return SelectRecordDialog(parent, title, items, current, empty_text=empty_text).result


# ---------------------------------------------------------------------------
# Colour picker
# ---------------------------------------------------------------------------

PRESETS = [
    (255, 0, 0), (255, 64, 0), (255, 160, 0), (255, 255, 0),
    (128, 255, 0), (0, 255, 0), (0, 255, 160), (0, 255, 255),
    (0, 128, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255),
    (255, 0, 128), (255, 255, 255), (160, 160, 160), (0, 0, 0),
]


class ColorDialog(Modal):
    def __init__(self, parent, rgb=(255, 0, 0), title: str = "Choose colour"):
        super().__init__(parent, title, width=470)
        tk.Label(self.body, text=title, bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        preview_row = tk.Frame(self.body, bg=theme.SURFACE)
        preview_row.pack(fill="x", pady=(10, 8))
        self.swatch = ColorSwatch(preview_row, rgb)
        self.swatch.pack(side="left")
        self.hex_var = tk.StringVar()
        hex_entry = theme.entry(preview_row, self.hex_var, width=9)
        hex_entry.pack(side="left", padx=(10, 0))
        hex_entry.bind("<Return>", lambda _e: self._from_hex())
        theme.button(preview_row, "Apply hex", self._from_hex, kind="secondary").pack(
            side="left", padx=(8, 0))
        tk.Label(preview_row, text="RGB sliders write 0x00BBGGRR to the profile.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"]).pack(side="left", padx=(10, 0))

        self.sliders: dict[str, SliderRow] = {}
        for name, value in zip(("R", "G", "B"), rgb):
            row = SliderRow(self.body, name, 0, 255, value, self._from_sliders)
            row.pack(fill="x", pady=(6, 0))
            self.sliders[name] = row

        palette = tk.Frame(self.body, bg=theme.SURFACE)
        palette.pack(fill="x", pady=(12, 0))
        for i, color in enumerate(PRESETS):
            sw = ColorSwatch(palette, color, lambda c=color: self._set(c), size=(38, 24))
            sw.grid(row=i // 8, column=i % 8, padx=2, pady=2)

        bar = tk.Frame(self.body, bg=theme.SURFACE)
        bar.pack(fill="x", pady=(14, 0))
        theme.button(bar, "Save", self.accept, kind="primary").pack(side="right")
        theme.button(bar, "Cancel", self.cancel, kind="ghost").pack(side="right", padx=(0, 8))
        self._set(rgb)
        self.show()

    def _set(self, rgb) -> None:
        r, g, b = (max(0, min(255, int(v))) for v in rgb)
        self.swatch.set_rgb((r, g, b))
        self.hex_var.set(f"{r:02X}{g:02X}{b:02X}")
        for name, value in zip(("R", "G", "B"), (r, g, b)):
            self.sliders[name].set(value)

    def _from_sliders(self, _value=None) -> None:
        rgb = tuple(self.sliders[n].get() for n in ("R", "G", "B"))
        self._set(rgb)

    def _from_hex(self) -> None:
        text = self.hex_var.get().strip().lstrip("#")
        if len(text) == 6:
            try:
                r = int(text[0:2], 16)
                g = int(text[2:4], 16)
                b = int(text[4:6], 16)
                self._set((r, g, b))
            except ValueError:
                pass

    def accept(self):
        self.result = tuple(self.sliders[n].get() for n in ("R", "G", "B"))
        self.destroy()


def pick_color(parent, rgb=(255, 0, 0), title: str = "Choose colour"):
    return ColorDialog(parent, rgb, title).result


# ---------------------------------------------------------------------------
# Busy and DPI overlays
# ---------------------------------------------------------------------------

class BusyWindow(tk.Toplevel):
    def __init__(self, parent, text: str = "Sending profile to the mouse..."):
        super().__init__(parent, bg=theme.SURFACE)
        self.overrideredirect(True)
        self.transient(parent)
        self.configure(highlightbackground=theme.ACCENT, highlightthickness=1)
        self._parent = parent
        self._alive = True
        frame = tk.Frame(self, bg=theme.SURFACE, padx=24, pady=18)
        frame.pack()
        tk.Label(frame, text="Applying profile", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        self.text = tk.Label(frame, text=text, bg=theme.SURFACE, fg=theme.MUTED,
                             font=theme.FONTS["small"], wraplength=340, justify="left")
        self.text.pack(anchor="w", pady=(4, 10))
        self.bar = ttk.Progressbar(frame, mode="indeterminate", length=340)
        self.bar.pack(fill="x")
        self.bar.start(12)
        self.update_idletasks()
        try:
            px, py = parent.winfo_rootx(), parent.winfo_rooty()
            pw, ph = parent.winfo_width(), parent.winfo_height()
            w, h = 400, 110
            self.geometry(f"{w}x{h}+{px + (pw - w) // 2}+{py + (ph - h) // 2}")
            self.grab_set()
        except tk.TclError:
            pass
        self.lift()

    def close(self) -> None:
        if not self._alive:
            return
        self._alive = False
        try:
            self.bar.stop()
            self.grab_release()
        except tk.TclError:
            pass
        self.destroy()


class DpiOverlay(tk.Toplevel):
    """Small top-most toast shown when the mouse changes DPI stage."""

    def __init__(self, parent):
        super().__init__(parent, bg=theme.SURFACE)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(highlightbackground=theme.ACCENT, highlightthickness=1)
        self._job = None
        frame = tk.Frame(self, bg=theme.SURFACE, padx=22, pady=14)
        frame.pack()
        tk.Label(frame, text="DPI", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(anchor="w")
        self.value = tk.Label(frame, text="", bg=theme.SURFACE, fg=theme.TEXT,
                              font=theme.FONTS["h1"])
        self.value.pack(anchor="w")
        self.withdraw()

    def show_value(self, text: str) -> None:
        self.value.configure(text=text)
        sw = self.winfo_screenwidth()
        self.update_idletasks()
        w = self.winfo_reqwidth()
        self.geometry(f"+{sw - w - 36}+48")
        self.deiconify()
        self.lift()
        if self._job:
            try:
                self.after_cancel(self._job)
            except Exception:
                pass
        self._job = self.after(1800, self.withdraw)
