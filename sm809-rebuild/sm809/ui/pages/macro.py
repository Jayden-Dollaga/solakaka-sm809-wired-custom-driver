"""Macro recording and event editor."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .. import theme
from ...model import MAX_EVENTS, MacroEvent
from ...recorder import (
    MOUSE_MOVE,
    STATE_NONE,
    MacroRecorder,
    RecorderSettings,
    event_label,
)
from .. import dialogs
from ..widgets import hline, spin
from . import Page


class MacroPage(Page):
    title = "Macros"
    subtitle = "Record up to 40 events, edit delays and assign macros to buttons"

    def build(self) -> None:
        self.current_index: int | None = None
        self._loaded_index: int | None = None
        self._loading = False
        self._recording = False
        self._rec_target: int | None = None
        self.recorder = MacroRecorder()

        outer = tk.Frame(self, bg=theme.BG, padx=22, pady=18)
        outer.pack(fill="both", expand=True)
        head = self.header(outer)
        head.pack(fill="x")
        theme.button(head, "Apply to mouse", self.app.apply_now, kind="primary").pack(side="right")

        content = tk.Frame(outer, bg=theme.BG)
        content.pack(fill="both", expand=True, pady=(10, 0))
        content.grid_columnconfigure(0, weight=0, minsize=280)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        self._build_list(content)
        self._build_editor(content)

    # -- left list ---------------------------------------------------------
    def _build_list(self, parent) -> None:
        card = tk.Frame(parent, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                        highlightthickness=1, padx=12, pady=12)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(card, text="Macro library", bg=theme.SURFACE, fg=theme.TEXT,
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
        self.btn_new = theme.button(buttons, "New", self._new_macro, kind="secondary")
        self.btn_new.pack(side="left")
        self.btn_folder = theme.button(buttons, "Folder", self._new_folder, kind="ghost")
        self.btn_folder.pack(side="left", padx=(6, 0))
        self.btn_rename = theme.button(buttons, "Rename", self._rename, kind="ghost")
        self.btn_rename.pack(side="left", padx=(6, 0))
        self.btn_delete = theme.button(buttons, "Delete", self._delete, kind="danger")
        self.btn_delete.pack(side="right")
        tk.Label(card, text="Assign a macro from the Buttons page. Editing a macro also updates "
                            "every button that already uses it.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"],
                 wraplength=240, justify="left").pack(fill="x", pady=(10, 0))

    # -- right editor ------------------------------------------------------
    def _build_editor(self, parent) -> None:
        editor = tk.Frame(parent, bg=theme.BG)
        editor.grid(row=0, column=1, sticky="nsew")
        editor.grid_columnconfigure(0, weight=1)
        editor.grid_rowconfigure(2, weight=1)

        # Name / loop
        top = tk.Frame(editor, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                       highlightthickness=1, padx=16, pady=12)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        row = tk.Frame(top, bg=theme.SURFACE)
        row.pack(fill="x")
        tk.Label(row, text="Name", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        self.name_var = tk.StringVar()
        self.name_entry = theme.entry(row, self.name_var, width=34)
        self.name_entry.pack(side="left", padx=(8, 16))
        self.name_entry.bind("<Return>", lambda _e: self._name_changed())
        self.name_entry.bind("<FocusOut>", lambda _e: self._name_changed())
        tk.Label(row, text="Loop", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        self.loop_var = tk.IntVar(value=1)
        self.loop_spin = spin(row, self.loop_var, 0, 9999, width=6,
                              command=self._loop_changed)
        self.loop_spin.pack(side="left", padx=(8, 0))
        self.loop_spin.bind("<Return>", lambda _e: self._loop_changed())
        self.loop_spin.bind("<FocusOut>", lambda _e: self._loop_changed())
        self.count_label = tk.Label(row, text="", bg=theme.SURFACE, fg=theme.MUTED,
                                    font=theme.FONTS["small"])
        self.count_label.pack(side="right")

        # Recording controls
        rec = tk.Frame(editor, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                       highlightthickness=1, padx=16, pady=12)
        rec.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        head = tk.Frame(rec, bg=theme.SURFACE)
        head.pack(fill="x")
        tk.Label(head, text="Recording", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(side="left")
        self.record_status = tk.Label(head, text="Idle", bg=theme.SURFACE, fg=theme.MUTED,
                                      font=theme.FONTS["small"])
        self.record_status.pack(side="right")
        self.btn_record = theme.button(head, "Record", self._start_recording, kind="primary")
        self.btn_record.pack(side="right", padx=(0, 8))
        self.btn_stop = theme.button(head, "Stop", self._stop_recording, kind="danger")
        self.btn_stop.pack(side="right", padx=(0, 8))

        mode_row = tk.Frame(rec, bg=theme.SURFACE)
        mode_row.pack(fill="x", pady=(10, 4))
        tk.Label(mode_row, text="Delay", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left", padx=(0, 8))
        self.mode_var = tk.IntVar(value=0)
        ttk.Radiobutton(mode_row, text="Constant 10 ms", variable=self.mode_var, value=0,
                        command=self._mode_changed).pack(side="left", padx=(0, 12))
        ttk.Radiobutton(mode_row, text="Fixed", variable=self.mode_var, value=1,
                        command=self._mode_changed).pack(side="left", padx=(0, 6))
        self.fixed_var = tk.IntVar(value=10)
        self.fixed_spin = spin(mode_row, self.fixed_var, 10, 65535, width=6)
        self.fixed_spin.pack(side="left", padx=(0, 12))
        ttk.Radiobutton(mode_row, text="Recorded timing", variable=self.mode_var, value=2,
                        command=self._mode_changed).pack(side="left")
        self.moves_var = tk.IntVar(value=0)
        ttk.Checkbutton(mode_row, text="Capture mouse movement", variable=self.moves_var
                        ).pack(side="right")
        tk.Label(rec, text="Recording is global: keyboard and mouse buttons are captured from "
                           "all applications. The click that presses Stop is part of the macro.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"],
                 wraplength=620, justify="left").pack(fill="x", pady=(6, 0))
        self._mode_changed()

        # Event table
        event_card = tk.Frame(editor, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                              highlightthickness=1, padx=12, pady=12)
        event_card.grid(row=2, column=0, sticky="nsew")
        header = tk.Frame(event_card, bg=theme.SURFACE)
        header.pack(fill="x")
        tk.Label(header, text="Events", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(side="left")
        self.event_count = tk.Label(header, text="0 / 40", bg=theme.SURFACE, fg=theme.MUTED,
                                    font=theme.FONTS["small"])
        self.event_count.pack(side="right")
        hline(event_card, 6)

        wrap = tk.Frame(event_card, bg=theme.SURFACE)
        wrap.pack(fill="both", expand=True)
        columns = ("n", "event", "delay", "x", "y")
        self.events_tree = ttk.Treeview(wrap, columns=columns, show="headings",
                                        selectmode="browse", height=12)
        headings = (("#", 44), ("Event", 300), ("Delay (ms)", 90), ("X", 70), ("Y", 70))
        for column, (text, width) in zip(columns, headings):
            self.events_tree.heading(column, text=text)
            self.events_tree.column(column, width=width, anchor="w" if column == "event" else "center")
        vsb = ttk.Scrollbar(wrap, orient="vertical", command=self.events_tree.yview)
        self.events_tree.configure(yscrollcommand=vsb.set)
        self.events_tree.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")
        self.events_tree.bind("<<TreeviewSelect>>", lambda _e: self._event_selected())
        self.events_tree.bind("<Double-1>", lambda _e: self._event_selected())

        tools = tk.Frame(event_card, bg=theme.SURFACE)
        tools.pack(fill="x", pady=(8, 0))
        self.btn_up = theme.button(tools, "Up", lambda: self._move_event(-1), kind="ghost")
        self.btn_up.pack(side="left")
        self.btn_down = theme.button(tools, "Down", lambda: self._move_event(1), kind="ghost")
        self.btn_down.pack(side="left", padx=(4, 0))
        self.btn_del = theme.button(tools, "Delete", self._delete_event, kind="ghost")
        self.btn_del.pack(side="left", padx=(4, 0))
        self.btn_clear = theme.button(tools, "Clear", self._clear_events, kind="danger")
        self.btn_clear.pack(side="left", padx=(4, 0))
        tk.Label(tools, text="Delay", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left", padx=(16, 4))
        self.delay_var = tk.IntVar(value=10)
        self.delay_spin = spin(tools, self.delay_var, 10, 65535, width=7)
        self.delay_spin.pack(side="left")
        theme.button(tools, "Set", self._set_delay, kind="secondary").pack(side="left", padx=(6, 0))

        insert = tk.Frame(event_card, bg=theme.SURFACE)
        insert.pack(fill="x", pady=(6, 0))
        tk.Label(insert, text="Insert mouse move", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left")
        tk.Label(insert, text="X", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left", padx=(10, 2))
        self.move_x = tk.IntVar(value=0)
        spin(insert, self.move_x, -32768, 32767, width=7).pack(side="left")
        tk.Label(insert, text="Y", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(side="left", padx=(8, 2))
        self.move_y = tk.IntVar(value=0)
        spin(insert, self.move_y, -32768, 32767, width=7).pack(side="left")
        theme.button(insert, "Insert", self._insert_move, kind="secondary").pack(
            side="left", padx=(8, 0))
        tk.Label(insert, text="Inserted after the selected event; delay 10 ms, no button edge.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"]).pack(side="left", padx=(10, 0))

        self._set_editor_enabled(False)

    # -- list --------------------------------------------------------------
    def _populate_list(self) -> None:
        selected = self.current_index
        self.tree.delete(*self.tree.get_children())
        for index, rec in enumerate(self.store.macros):
            label = rec.name or f"Macro {index + 1}"
            if rec.is_folder:
                label = "[Folder] " + label
            self.tree.insert("", "end", iid=str(index), text=label,
                             tags=("folder",) if rec.is_folder else ())
        if selected is not None and 0 <= selected < len(self.store.macros):
            iid = str(selected)
            if self.tree.exists(iid):
                self.tree.selection_set(iid)
                self.tree.see(iid)

    def _select_listed(self) -> None:
        if self._loading or self._recording:
            return
        self._flush_edits()
        sel = self.tree.selection()
        if not sel:
            return
        index = int(sel[0])
        rec = self.store.macros[index]
        if rec.is_folder:
            self.current_index = None
            self._loaded_index = None
            self._set_editor_enabled(False)
            self.name_var.set("")
            self._populate_events([])
            self.event_count.configure(text="Folder selected")
            self.count_label.configure(text="")
            return
        self._load(index)

    def _flush_edits(self) -> None:
        """Commit name/loop edits before the selection moves to another record."""
        if self._loaded_index is not None:
            self._name_changed()
            self._loop_changed()

    def _load(self, index: int) -> None:
        self.current_index = index
        self._loaded_index = index
        rec = self.store.macros[index]
        self._loading = True
        try:
            self.name_var.set(rec.name)
            self.loop_var.set(rec.loop)
            self._populate_events(rec.events)
            self.count_label.configure(text=f"{rec.count} / 40 events")
        finally:
            self._loading = False
        self._set_editor_enabled(True)

    def _new_macro(self) -> None:
        if self._recording:
            return
        rec = self.store.add_macro()
        self.current_index = len(self.store.macros) - 1
        self._populate_list()
        self._load(self.current_index)
        self.name_entry.focus_set()
        self.name_entry.select_range(0, "end")
        self.app.mark_dirty("new macro")

    def _new_folder(self) -> None:
        if self._recording:
            return
        self.store.add_macro(folder=True)
        index = len(self.store.macros) - 1
        self.current_index = None
        self._loaded_index = None
        self._populate_list()
        self.tree.selection_set(str(index))
        self.tree.see(str(index))
        self.app.mark_dirty("new macro folder")

    def _rename(self) -> None:
        index = self.current_index
        if index is None:
            sel = self.tree.selection()
            if not sel:
                return
            index = int(sel[0])
        rec = self.store.macros[index]
        name = dialogs.ask_text(self.app, "Rename", "New name", rec.name)
        if not name:
            return
        rec.name = name
        self.store.save_macros()
        self.app.sync_macro(index)
        self._populate_list()
        if index == self.current_index:
            self._load(index)
        self.app.mark_dirty("renamed macro")

    def _delete(self) -> None:
        if self._recording:
            return
        index = self.current_index
        sel = self.tree.selection()
        if sel:
            index = int(sel[0])
        if index is None:
            return
        rec = self.store.macros[index]
        if not dialogs.ask_confirm(self.app, "Delete macro",
                                   f"Delete '{rec.name}'? Buttons that use it keep their "
                                   "last uploaded copy until you reassign them.",
                                   ok_text="Delete", danger=True):
            return
        self.store.delete_macro(index)
        self.current_index = None
        self._loaded_index = None
        self._populate_list()
        self._set_editor_enabled(False)
        self._populate_events([])
        self.event_count.configure(text="0 / 40")
        self.app.mark_dirty("deleted macro")

    # -- editor callbacks --------------------------------------------------
    def _name_changed(self) -> None:
        if self._loading or self._recording or self._loaded_index is None:
            return
        index = self._loaded_index
        if not (0 <= index < len(self.store.macros)):
            return
        text = self.name_var.get().strip()
        if not text:
            return
        rec = self.store.macros[index]
        if rec.name == text:
            return
        rec.name = text
        self.store.save_macros()
        self.app.sync_macro(index)
        self._populate_list()
        self.app.mark_dirty("macro name")

    def _loop_changed(self) -> None:
        if self._loading or self._recording or self._loaded_index is None:
            return
        index = self._loaded_index
        if not (0 <= index < len(self.store.macros)):
            return
        rec = self.store.macros[index]
        value = max(0, min(9999, int(self.loop_var.get())))
        if rec.loop == value:
            return
        rec.loop = value
        self.store.save_macros()
        self.app.sync_macro(index)
        self.app.mark_dirty("macro loop")

    def _mode_changed(self) -> None:
        fixed = int(self.mode_var.get()) == 1
        self.fixed_spin.state(["!disabled"] if fixed else ["disabled"])

    def _start_recording(self) -> None:
        if self._recording:
            return
        if self.current_index is None:
            self._new_macro()
            if self.current_index is None:
                return
        rec = self.store.macros[self.current_index]
        if rec.is_folder:
            dialogs.show_message(self.app, "Recording", "Select a macro, not a folder.", "warn")
            return
        settings = RecorderSettings(
            mode=int(self.mode_var.get()),
            fixed_delay=max(10, int(self.fixed_var.get())),
            capture_moves=bool(self.moves_var.get()),
        )
        self.recorder.on_event = self._recording_event
        self._rec_target = self.current_index
        if not self.recorder.start(settings):
            dialogs.show_message(self.app, "Recording failed",
                                 self.recorder.last_error or "Could not install hooks.", "error")
            return
        self._recording = True
        self.record_status.configure(text="Recording", fg=theme.RED)
        self.btn_record.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self._set_editor_enabled(False)
        self._populate_events([])
        self.event_count.configure(text="0 / 40")

    def _recording_event(self, snapshot: list[MacroEvent]) -> None:
        self.app.post(lambda: self._recording_progress(snapshot))

    def _recording_progress(self, snapshot: list[MacroEvent]) -> None:
        if not self._recording:
            return
        self._populate_events(snapshot)
        self.event_count.configure(text=f"{len(snapshot)} / 40")
        self.record_status.configure(text=f"Recording {len(snapshot)} / 40", fg=theme.RED)
        if len(snapshot) >= MAX_EVENTS:
            self.app.post(self._stop_recording)

    def _stop_recording(self) -> None:
        if not self._recording:
            return
        events = self.recorder.stop()
        self.recorder.on_event = None
        self._recording = False
        self.btn_record.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        index = self._rec_target
        self._rec_target = None
        if index is not None and 0 <= index < len(self.store.macros):
            rec = self.store.macros[index]
            rec.set_events(events)
            self.store.save_macros()
            self.app.sync_macro(index)
            self.current_index = index
            self._populate_list()
            self._load(index)
        self.record_status.configure(text=f"Stopped ({len(events)} events)", fg=theme.GREEN)
        self._set_editor_enabled(True)
        self.app.mark_dirty("recorded macro")

    def _set_editor_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for widget in (self.name_entry, self.loop_spin):
            widget.configure(state=state)
        for btn in (self.btn_up, self.btn_down, self.btn_del, self.btn_clear):
            btn.configure(state=state)
        self.btn_record.configure(state="normal" if not self._recording else "disabled")
        self.btn_stop.configure(state="normal" if self._recording else "disabled")
        if not enabled:
            self.event_count.configure(text="No macro selected")

    # -- events ------------------------------------------------------------
    def _populate_events(self, events: list[MacroEvent]) -> None:
        selected = self.events_tree.selection()
        keep = int(selected[0]) if selected else None
        self.events_tree.delete(*self.events_tree.get_children())
        for i, event in enumerate(events):
            self.events_tree.insert(
                "", "end", iid=str(i),
                values=(i + 1, event_label(event), event.delay,
                        event.a if event.opcode == MOUSE_MOVE else "",
                        event.b if event.opcode == MOUSE_MOVE else ""),
            )
        if keep is not None and self.events_tree.exists(str(keep)):
            self.events_tree.selection_set(str(keep))
        elif events:
            self.events_tree.selection_set("0")
        if self.current_index is not None and not self._recording:
            try:
                rec = self.store.macros[self.current_index]
                self.count_label.configure(text=f"{rec.count} / 40 events")
            except IndexError:
                pass

    def _selected_index(self) -> int | None:
        sel = self.events_tree.selection()
        return int(sel[0]) if sel else None

    def _event_selected(self) -> None:
        index = self._selected_index()
        if index is None or self.current_index is None:
            return
        rec = self.store.macros[self.current_index]
        if 0 <= index < len(rec.events):
            self.delay_var.set(rec.events[index].delay)

    def _save_events(self, events: list[MacroEvent]) -> None:
        if self.current_index is None:
            return
        rec = self.store.macros[self.current_index]
        rec.set_events(events)
        self.store.save_macros()
        self.app.sync_macro(self.current_index)
        self._populate_events(events)
        self.count_label.configure(text=f"{rec.count} / 40 events")
        self.app.mark_dirty("macro events")

    def _set_delay(self) -> None:
        index = self._selected_index()
        if index is None or self.current_index is None:
            return
        rec = self.store.macros[self.current_index]
        events = rec.events
        if not (0 <= index < len(events)):
            return
        events[index].delay = max(10, min(65535, int(self.delay_var.get())))
        self._save_events(events)

    def _delete_event(self) -> None:
        index = self._selected_index()
        if index is None or self.current_index is None:
            return
        rec = self.store.macros[self.current_index]
        events = rec.events
        if 0 <= index < len(events):
            del events[index]
            self._save_events(events)

    def _clear_events(self) -> None:
        if self.current_index is None:
            return
        rec = self.store.macros[self.current_index]
        if not rec.count:
            return
        if not dialogs.ask_confirm(self.app, "Clear macro",
                                   f"Remove all {rec.count} events from '{rec.name}'?",
                                   ok_text="Clear", danger=True):
            return
        self._save_events([])
        self.event_count.configure(text="0 / 40")

    def _move_event(self, delta: int) -> None:
        index = self._selected_index()
        if index is None or self.current_index is None:
            return
        rec = self.store.macros[self.current_index]
        events = rec.events
        target = index + delta
        if not (0 <= target < len(events)):
            return
        events[index], events[target] = events[target], events[index]
        self._save_events(events)
        self.events_tree.selection_set(str(target))

    def _insert_move(self) -> None:
        if self.current_index is None:
            return
        rec = self.store.macros[self.current_index]
        events = rec.events
        if len(events) >= MAX_EVENTS:
            dialogs.show_message(self.app, "Macro full", "A macro can hold 40 events.", "warn")
            return
        event = MacroEvent(opcode=MOUSE_MOVE, state=STATE_NONE, delay=10,
                           a=int(self.move_x.get()), b=int(self.move_y.get()))
        index = self._selected_index()
        if index is None or index + 1 >= len(events):
            events.append(event)
        else:
            events.insert(index + 1, event)
        self._save_events(events)

    # -- page lifecycle ----------------------------------------------------
    def refresh(self) -> None:
        self._loading = True
        try:
            self._populate_list()
            if self.current_index is not None and self.current_index < len(self.store.macros):
                rec = self.store.macros[self.current_index]
                if not rec.is_folder:
                    self._loaded_index = self.current_index
                    self.name_var.set(rec.name)
                    self.loop_var.set(rec.loop)
                    self._populate_events(rec.events)
                    self._set_editor_enabled(True)
                    return
            self._loaded_index = None
            self._set_editor_enabled(False)
        finally:
            self._loading = False
