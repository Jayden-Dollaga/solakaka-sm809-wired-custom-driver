"""Recoil table editor (experimental)."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .. import theme
from ...model import MAX_BULLETS, Bullet
from .. import dialogs
from ..widgets import Banner, hline, spin
from . import Page


class GunPage(Page):
    title = "Gun recoil"
    subtitle = "30-row recoil tables - experimental upload path"

    def build(self) -> None:
        self.current_index: int | None = None
        self._loaded_index: int | None = None
        self._loading = False

        outer = tk.Frame(self, bg=theme.BG, padx=22, pady=18)
        outer.pack(fill="both", expand=True)
        head = self.header(outer)
        head.pack(fill="x")
        theme.button(head, "Apply to mouse", self.app.apply_now, kind="primary").pack(side="right")

        banner = Banner(
            outer,
            "Experimental: the shipped application builds gun tables but never copies them "
            "into the upload buffer, and its Gun tab is hidden. This rebuild uploads 0x79 "
            "tables best-effort using the encoder recovered from the binary. Verify on hardware "
            "before relying on it.",
            color=theme.AMBER,
        )
        banner.pack(fill="x", pady=(10, 8))

        content = tk.Frame(outer, bg=theme.BG)
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=0, minsize=270)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        self._build_list(content)
        self._build_editor(content)

    def _build_list(self, parent) -> None:
        card = tk.Frame(parent, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                        highlightthickness=1, padx=12, pady=12)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(card, text="Gun library", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        hline(card, 6)
        wrap = tk.Frame(card, bg=theme.SURFACE)
        wrap.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(wrap, show="tree", selectmode="browse")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.tree.tag_configure("folder", foreground=theme.MUTED)
        self.tree.bind("<<TreeviewSelect>>", lambda _e: self._select_listed())

        buttons = tk.Frame(card, bg=theme.SURFACE)
        buttons.pack(fill="x", pady=(10, 0))
        theme.button(buttons, "New", self._new_gun, kind="secondary").pack(side="left")
        theme.button(buttons, "Folder", self._new_folder, kind="ghost").pack(side="left", padx=(6, 0))
        theme.button(buttons, "Rename", self._rename, kind="ghost").pack(side="left", padx=(6, 0))
        theme.button(buttons, "Delete", self._delete, kind="danger").pack(side="right")
        tk.Label(card, text="Assign a table to a button with the Set Gun action on the Buttons "
                            "page. The button copies the rows; re-assign after editing.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"],
                 wraplength=235, justify="left").pack(fill="x", pady=(10, 0))

    def _build_editor(self, parent) -> None:
        editor = tk.Frame(parent, bg=theme.BG)
        editor.grid(row=0, column=1, sticky="nsew")
        editor.grid_columnconfigure(0, weight=1)
        editor.grid_rowconfigure(1, weight=1)

        top = tk.Frame(editor, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                       highlightthickness=1, padx=16, pady=12)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        row = tk.Frame(top, bg=theme.SURFACE)
        row.pack(fill="x")
        tk.Label(row, text="Name", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        self.name_var = tk.StringVar()
        self.name_entry = theme.entry(row, self.name_var, width=32)
        self.name_entry.pack(side="left", padx=(8, 16))
        self.name_entry.bind("<Return>", lambda _e: self._name_changed())
        self.name_entry.bind("<FocusOut>", lambda _e: self._name_changed())
        tk.Label(row, text="Rows used", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        self.count_var = tk.IntVar(value=30)
        self.count_spin = spin(row, self.count_var, 0, MAX_BULLETS, width=5,
                               command=self._count_changed)
        self.count_spin.pack(side="left", padx=(8, 0))
        self.count_spin.bind("<Return>", lambda _e: self._count_changed())
        self.count_spin.bind("<FocusOut>", lambda _e: self._count_changed())

        table_card = tk.Frame(editor, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                              highlightthickness=1, padx=12, pady=12)
        table_card.grid(row=1, column=0, sticky="nsew")
        tk.Label(table_card, text="Bullet rows", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        tk.Label(table_card, text="The 0x79 encoder sends |x| and |y| as single bytes; values "
                                  "outside 0..255 truncate on the wire.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"]).pack(anchor="w")
        hline(table_card, 6)
        wrap = tk.Frame(table_card, bg=theme.SURFACE)
        wrap.pack(fill="both", expand=True)
        columns = ("n", "x", "y", "delay")
        self.rows = ttk.Treeview(wrap, columns=columns, show="headings", selectmode="browse")
        for column, text, width in (("n", "#", 44), ("x", "X", 100),
                                    ("y", "Y", 100), ("delay", "Delay (ms)", 120)):
            self.rows.heading(column, text=text)
            self.rows.column(column, width=width, anchor="center")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.rows.yview)
        self.rows.configure(yscrollcommand=vsb.set)
        self.rows.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.rows.tag_configure("unused", foreground=theme.DIM)
        self.rows.bind("<<TreeviewSelect>>", lambda _e: self._row_selected())

        editor_row = tk.Frame(table_card, bg=theme.SURFACE)
        editor_row.pack(fill="x", pady=(8, 0))
        tk.Label(editor_row, text="X", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        self.x_var = tk.IntVar(value=0)
        self.x_spin = spin(editor_row, self.x_var, 0, 255, width=6)
        self.x_spin.pack(side="left", padx=(4, 10))
        tk.Label(editor_row, text="Y", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        self.y_var = tk.IntVar(value=0)
        self.y_spin = spin(editor_row, self.y_var, 0, 255, width=6)
        self.y_spin.pack(side="left", padx=(4, 10))
        tk.Label(editor_row, text="Delay", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        self.delay_var = tk.IntVar(value=10)
        self.delay_spin = spin(editor_row, self.delay_var, 10, 65535, width=7)
        self.delay_spin.pack(side="left", padx=(4, 10))
        self.btn_update = theme.button(editor_row, "Update row", self._update_row, kind="secondary")
        self.btn_update.pack(side="left")
        self.btn_zero = theme.button(editor_row, "Clear row", self._clear_row, kind="ghost")
        self.btn_zero.pack(side="left", padx=(6, 0))
        self.btn_zero_all = theme.button(editor_row, "Clear all", self._clear_all, kind="danger")
        self.btn_zero_all.pack(side="right")

        self._set_editor_enabled(False)

    # -- list --------------------------------------------------------------
    def _populate_list(self) -> None:
        selected = self.current_index
        self.tree.delete(*self.tree.get_children())
        for index, rec in enumerate(self.store.guns):
            label = rec.name or f"Gun {index + 1}"
            if rec.is_folder:
                label = "[Folder] " + label
            self.tree.insert("", "end", iid=str(index), text=label,
                             tags=("folder",) if rec.is_folder else ())
        if selected is not None and 0 <= selected < len(self.store.guns):
            iid = str(selected)
            if self.tree.exists(iid):
                self.tree.selection_set(iid)
                self.tree.see(iid)

    def _select_listed(self) -> None:
        if self._loading:
            return
        self._flush_edits()
        sel = self.tree.selection()
        if not sel:
            return
        index = int(sel[0])
        rec = self.store.guns[index]
        if rec.is_folder:
            self.current_index = None
            self._loaded_index = None
            self.name_var.set("")
            self._populate_rows([])
            self._set_editor_enabled(False)
            return
        self._load(index)

    def _flush_edits(self) -> None:
        if self._loaded_index is not None:
            self._name_changed()

    def _load(self, index: int) -> None:
        self.current_index = index
        self._loaded_index = index
        rec = self.store.guns[index]
        self._loading = True
        try:
            self.name_var.set(rec.name)
            self.count_var.set(rec.count)
            self._populate_rows(rec.bullets, used=rec.count)
        finally:
            self._loading = False
        self._set_editor_enabled(True)

    def _new_gun(self) -> None:
        self.store.add_gun()
        index = len(self.store.guns) - 1
        self.current_index = index
        self._populate_list()
        self._load(index)
        self.name_entry.focus_set()
        self.name_entry.select_range(0, "end")
        self.app.mark_dirty("new gun table")

    def _new_folder(self) -> None:
        self.store.add_gun(folder=True)
        index = len(self.store.guns) - 1
        self.current_index = None
        self._loaded_index = None
        self._populate_list()
        self.tree.selection_set(str(index))
        self.tree.see(str(index))
        self.app.mark_dirty("new gun folder")

    def _rename(self) -> None:
        index = self.current_index
        if index is None:
            sel = self.tree.selection()
            if not sel:
                return
            index = int(sel[0])
        rec = self.store.guns[index]
        name = dialogs.ask_text(self.app, "Rename", "New name", rec.name)
        if not name:
            return
        rec.name = name
        self.store.save_guns()
        self.app.sync_gun(index)
        self._populate_list()
        if index == self.current_index:
            self._load(index)
        self.app.mark_dirty("renamed gun table")

    def _delete(self) -> None:
        index = self.current_index
        sel = self.tree.selection()
        if sel:
            index = int(sel[0])
        if index is None:
            return
        rec = self.store.guns[index]
        if not dialogs.ask_confirm(self.app, "Delete gun table", f"Delete '{rec.name}'?",
                                   ok_text="Delete", danger=True):
            return
        self.store.delete_gun(index)
        self.current_index = None
        self._loaded_index = None
        self._populate_list()
        self._populate_rows([])
        self._set_editor_enabled(False)
        self.app.mark_dirty("deleted gun table")

    # -- editing -----------------------------------------------------------
    def _name_changed(self) -> None:
        if self._loading or self._loaded_index is None:
            return
        index = self._loaded_index
        if not (0 <= index < len(self.store.guns)):
            return
        text = self.name_var.get().strip()
        if not text:
            return
        rec = self.store.guns[index]
        if rec.name == text:
            return
        rec.name = text
        self.store.save_guns()
        self.app.sync_gun(index)
        self._populate_list()
        self.app.mark_dirty("gun name")

    def _count_changed(self) -> None:
        if self._loading or self.current_index is None:
            return
        rec = self.store.guns[self.current_index]
        value = max(0, min(MAX_BULLETS, int(self.count_var.get())))
        if rec.count == value:
            return
        rec.count = value
        self.store.save_guns()
        self.app.sync_gun(self.current_index)
        self._populate_rows(rec.bullets, used=value)
        self.app.mark_dirty("gun row count")

    def _row_selected(self) -> None:
        sel = self.rows.selection()
        if not sel or self.current_index is None:
            return
        index = int(sel[0])
        rec = self.store.guns[self.current_index]
        if 0 <= index < len(rec.bullets):
            row = rec.bullets[index]
            self.x_var.set(max(0, min(255, row.x)))
            self.y_var.set(max(0, min(255, row.y)))
            self.delay_var.set(row.delay)

    def _selected_row(self) -> int | None:
        sel = self.rows.selection()
        return int(sel[0]) if sel else None

    def _update_row(self) -> None:
        index = self._selected_row()
        if index is None or self.current_index is None:
            return
        rec = self.store.guns[self.current_index]
        row = Bullet(int(self.x_var.get()), int(self.y_var.get()), int(self.delay_var.get()))
        rec.set_bullet(index, row)
        self.store.save_guns()
        self.app.sync_gun(self.current_index)
        self._populate_rows(rec.bullets, used=rec.count)
        self.rows.selection_set(str(index))
        self.app.mark_dirty("gun row")

    def _clear_row(self) -> None:
        index = self._selected_row()
        if index is None or self.current_index is None:
            return
        rec = self.store.guns[self.current_index]
        rec.set_bullet(index, Bullet(0, 0, 10))
        self.store.save_guns()
        self.app.sync_gun(self.current_index)
        self._populate_rows(rec.bullets, used=rec.count)
        self.rows.selection_set(str(index))
        self.x_var.set(0)
        self.y_var.set(0)
        self.delay_var.set(10)
        self.app.mark_dirty("gun row cleared")

    def _clear_all(self) -> None:
        if self.current_index is None:
            return
        rec = self.store.guns[self.current_index]
        if not dialogs.ask_confirm(self.app, "Clear table",
                                   f"Reset all 30 rows of '{rec.name}' to zero?",
                                   ok_text="Clear", danger=True):
            return
        # Reset the storage without changing how many rows the table uses.
        for i in range(MAX_BULLETS):
            rec.set_bullet(i, Bullet(0, 0, 10))
        self.store.save_guns()
        self.app.sync_gun(self.current_index)
        self._populate_rows(rec.bullets, used=rec.count)
        self.app.mark_dirty("gun table cleared")

    def _set_editor_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for widget in (self.name_entry, self.count_spin, self.x_spin, self.y_spin,
                       self.delay_spin, self.btn_update, self.btn_zero, self.btn_zero_all):
            widget.configure(state=state)

    def _populate_rows(self, rows, used: int | None = None) -> None:
        self.rows.delete(*self.rows.get_children())
        used = MAX_BULLETS if used is None else used
        rows = list(rows)
        for i in range(MAX_BULLETS):
            row = rows[i] if i < len(rows) else Bullet(0, 0, 10)
            tags = () if i < used else ("unused",)
            self.rows.insert("", "end", iid=str(i),
                             values=(i + 1, row.x, row.y, row.delay), tags=tags)

    # -- lifecycle ---------------------------------------------------------
    def refresh(self) -> None:
        self._loading = True
        try:
            self._populate_list()
            if self.current_index is not None and self.current_index < len(self.store.guns):
                rec = self.store.guns[self.current_index]
                if not rec.is_folder:
                    self._load(self.current_index)
                    return
            self._loaded_index = None
            self._set_editor_enabled(False)
        finally:
            self._loading = False
