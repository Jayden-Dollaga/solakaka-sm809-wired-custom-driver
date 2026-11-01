"""Button remapping page (64 slots)."""

from __future__ import annotations

import tkinter as tk

from .. import theme
from ...keys import shortcut_name
from ...protocol import action_label, action_needs
from .. import dialogs
from ..widgets import ScrollFrame
from . import Page


class KeysPage(Page):
    title = "Buttons"
    subtitle = "All 64 button slots - click a slot to change its action"

    def build(self) -> None:
        outer = tk.Frame(self, bg=theme.BG, padx=22, pady=18)
        outer.pack(fill="both", expand=True)
        self.header(outer).pack(fill="x")

        toolbar = tk.Frame(outer, bg=theme.BG)
        toolbar.pack(fill="x", pady=(10, 8))
        tk.Label(toolbar, text="Filter", bg=theme.BG, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        self.filter_var = tk.StringVar()
        entry = theme.entry(toolbar, self.filter_var, width=28)
        entry.pack(side="left", padx=(8, 0))
        entry.bind("<KeyRelease>", lambda _e: self._schedule_rebuild())
        theme.button(toolbar, "Reload from profile", self.refresh, kind="ghost").pack(side="right")
        self.counter = tk.Label(toolbar, text="", bg=theme.BG, fg=theme.MUTED,
                                font=theme.FONTS["small"])
        self.counter.pack(side="right", padx=(0, 12))

        self.scroll = ScrollFrame(outer)
        self.scroll.pack(fill="both", expand=True)
        self.grid = self.scroll.body
        for col in range(4):
            self.grid.grid_columnconfigure(col, weight=1, uniform="slot")
        self._rebuild_job = None
        self.cards: list[tk.Frame] = []

    # -- rebuild -----------------------------------------------------------
    def _schedule_rebuild(self) -> None:
        if self._rebuild_job:
            try:
                self.after_cancel(self._rebuild_job)
            except Exception:
                pass
        self._rebuild_job = self.after(150, self.refresh)

    def refresh(self) -> None:
        self._rebuild_job = None
        for child in self.grid.winfo_children():
            child.destroy()
        self.cards = []
        query = self.filter_var.get().strip().lower()
        shown = 0
        row = 0
        col = 0
        for index in range(64):
            entry = self.profile.button(index)
            label = action_label(entry.action)
            detail = self._detail(index)
            haystack = f"{index + 1} {label} {detail}".lower()
            if query and query not in haystack:
                continue
            card = self._card(index, label, detail)
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            self.cards.append(card)
            shown += 1
            col += 1
            if col >= 4:
                col = 0
                row += 1
        if not shown:
            tk.Label(self.grid, text="No button matches the filter.", bg=theme.BG,
                     fg=theme.MUTED).grid(row=0, column=0, columnspan=4, pady=30)
        self.counter.configure(text=f"{shown} / 64 slots")

    def _detail(self, index: int) -> str:
        entry = self.profile.button(index)
        code = entry.action
        if code == 0x15:
            return shortcut_name(entry.shortcut_key, entry.shortcut_mods)
        if code == 0x0A:
            return f"{entry.fire_count} clicks / {entry.fire_interval} ms"
        if code in (0x16, 0x39):
            name = "Macro"
            idx = entry.macro_index
            if 1 <= idx <= len(self.store.macros):
                name = self.store.macros[idx - 1].name
            return f"{name} ({entry.count} events, loop {entry.loop})"
        if code == 0x79:
            return f"Gun table ({entry.count} rows) - experimental"
        if code == 0x00:
            return "Nothing"
        needs = action_needs(code)
        return needs.replace("_", " ") if needs else "Mapped"

    def _card(self, index: int, label: str, detail: str) -> tk.Frame:
        card = tk.Frame(self.grid, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                        highlightthickness=1, bd=0, padx=10, pady=8)
        top = tk.Frame(card, bg=theme.SURFACE)
        top.pack(fill="x")
        badge = tk.Label(top, text=f"{index + 1:02d}", bg=theme.SURFACE_ALT,
                         fg=theme.ACCENT, font=theme.FONTS["tiny"], padx=6, pady=2)
        badge.pack(side="left")
        label_widget = tk.Label(top, text=label, bg=theme.SURFACE, fg=theme.TEXT,
                                font=theme.FONTS["bold"], anchor="w", justify="left",
                                wraplength=150)
        label_widget.pack(side="left", padx=(8, 0), fill="x", expand=True)
        detail_widget = tk.Label(card, text=detail, bg=theme.SURFACE, fg=theme.MUTED,
                                 font=theme.FONTS["tiny"], anchor="w", justify="left",
                                 wraplength=190)
        detail_widget.pack(fill="x", pady=(6, 0))

        def enter(_e=None):
            card.configure(highlightbackground=theme.ACCENT)
            for w in (card, top, label_widget, detail_widget):
                w.configure(bg=theme.SURFACE_ALT)
            label_widget.configure(bg=theme.SURFACE_ALT)
            detail_widget.configure(bg=theme.SURFACE_ALT)

        def leave(_e=None):
            card.configure(highlightbackground=theme.BORDER)
            for w in (card, top, label_widget, detail_widget):
                w.configure(bg=theme.SURFACE)

        def click(_e=None):
            self._edit(index)

        def menu(event):
            self._context(index, event)

        for widget in (card, top, label_widget, detail_widget, badge):
            widget.configure(cursor="hand2")
            widget.bind("<Button-1>", click)
            widget.bind("<Button-3>", menu)
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
        return card

    # -- editing -----------------------------------------------------------
    def _context(self, index: int, event) -> None:
        menu = tk.Menu(self, tearoff=0, bg=theme.SURFACE_ALT, fg=theme.TEXT,
                       activebackground=theme.ACCENT_DARK, activeforeground="#ffffff",
                       bd=0)
        menu.add_command(label="Choose action...", command=lambda: self._edit(index))
        menu.add_command(label="Set Button Off", command=lambda: self._set_off(index))
        menu.add_separator()
        menu.add_command(label="Copy action to all slots", command=lambda: self._copy_all(index))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _set_off(self, index: int) -> None:
        self.profile.button(index).action = 0x00
        self.app.mark_dirty("button cleared")
        self.refresh()

    def _copy_all(self, index: int) -> None:
        source = self.profile.button(index)
        if not dialogs.ask_confirm(self.app, "Copy action",
                                   f"Copy button {index + 1} to every other slot?",
                                   ok_text="Copy"):
            return
        for i in range(64):
            if i == index:
                continue
            target = self.profile.button(i)
            target.action = source.action
            target.shortcut_key = source.shortcut_key
            target.shortcut_mods = source.shortcut_mods
            target.selected_index = source.selected_index
            target.macro_index = source.macro_index
            target.count = source.count
            target.loop = source.loop
            target.name = source.name
            target.fire_count = source.fire_count
            target.fire_interval = source.fire_interval
            if source.action in (0x16, 0x39):
                target.set_events(source.event_slice())
            if source.action == 0x79:
                target.set_bullets(source.bullet_slice())
        self.app.mark_dirty("copied button action")
        self.refresh()

    def _edit(self, index: int) -> None:
        entry = self.profile.button(index)
        code = dialogs.pick_action(self.app, entry.action)
        if code is None:
            return
        needs = action_needs(code)
        if needs == "shortcut":
            result = dialogs.capture_shortcut(self.app, entry.shortcut_key, entry.shortcut_mods)
            if result is None:
                return
            entry.shortcut_key, entry.shortcut_mods = result
            entry.action = 0x15
        elif needs == "fire":
            result = dialogs.ask_fire(self.app, entry.fire_count or 3, entry.fire_interval or 50)
            if result is None:
                return
            entry.fire_count, entry.fire_interval = result
            entry.action = 0x0A
        elif needs in ("macro", "left_macro"):
            items = self.store.macro_names()
            picked = dialogs.pick_record(
                self.app, "Select macro", items,
                current=(entry.macro_index - 1) if entry.macro_index else None,
                empty_text="Create a macro on the Macro page first.",
            )
            if picked is None:
                return
            rec = self.store.macros[picked]
            entry.selected_index = picked
            entry.name = rec.name
            entry.macro_index = picked + 1
            entry.count = rec.count
            entry.loop = rec.loop
            entry.set_events(rec.events)
            entry.action = 0x16 if needs == "macro" else 0x39
        elif needs == "gun":
            items = self.store.gun_names()
            picked = dialogs.pick_record(
                self.app, "Select gun table", items,
                empty_text="Create a gun table on the Gun page first.",
            )
            if picked is None:
                return
            rec = self.store.guns[picked]
            entry.selected_index = picked
            entry.name = rec.name
            entry.set_bullets(rec.bullet_slice())
            entry.loop = 1
            entry.action = 0x79
        else:
            entry.action = code
        self.app.mark_dirty(f"button {index + 1} = {action_label(entry.action)}")
        self.refresh()
