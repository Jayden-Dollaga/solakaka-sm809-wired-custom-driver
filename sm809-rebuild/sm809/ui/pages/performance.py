"""DPI, report rate and Windows pointer settings."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .. import theme
from ...model import RATE_LABELS
from ...protocol import (
    describe_apply,
    high_dpi_mask,
    sensor_display_dpi,
    sensor_limits,
    sensor_max_label,
)
from .. import dialogs
from ..widgets import ColorSwatch, ScrollFrame, SliderRow, hline
from . import Page


class PerformancePage(Page):
    title = "Performance"
    subtitle = "DPI stages, polling rate and Windows pointer behaviour"

    def build(self) -> None:
        self._loading = True
        outer = tk.Frame(self, bg=theme.BG, padx=22, pady=18)
        outer.pack(fill="both", expand=True)
        head = self.header(outer)
        head.pack(fill="x")
        theme.button(head, "Apply to mouse", self.app.apply_now, kind="primary").pack(side="right")
        theme.button(head, "Apply plan...", self._show_plan, kind="ghost").pack(
            side="right", padx=(0, 8))

        scroll = ScrollFrame(outer)
        scroll.pack(fill="both", expand=True, pady=(10, 0))
        body = scroll.body
        body.grid_columnconfigure(0, weight=3, uniform="perf")
        body.grid_columnconfigure(1, weight=2, uniform="perf")

        self._build_dpi(body)
        self._build_right(body)
        self._loading = False

    # -- left: DPI ---------------------------------------------------------
    def _build_dpi(self, parent) -> None:
        card = tk.Frame(parent, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                        highlightthickness=1, padx=16, pady=14)
        card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 10))
        top = tk.Frame(card, bg=theme.SURFACE)
        top.pack(fill="x")
        tk.Label(top, text="DPI stages", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(side="left")
        self.sensor_label = tk.Label(top, text="", bg=theme.SURFACE, fg=theme.MUTED,
                                     font=theme.FONTS["small"])
        self.sensor_label.pack(side="right")
        hline(card, 8)

        count_row = tk.Frame(card, bg=theme.SURFACE)
        count_row.pack(fill="x", pady=(2, 6))
        tk.Label(count_row, text="Number of stages", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["base"]).pack(side="left")
        self.count_var = tk.StringVar()
        self.count_box = ttk.Combobox(count_row, textvariable=self.count_var, width=4,
                                      state="readonly", values=[str(i) for i in range(1, 9)])
        self.count_box.pack(side="left", padx=(10, 0))
        self.count_box.bind("<<ComboboxSelected>>", lambda _e: self._count_changed())
        tk.Label(count_row, text="Click a stage radio to make it active.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"]).pack(side="left", padx=(12, 0))

        self.stage_var = tk.IntVar(value=0)
        self.stage_rows: list[dict] = []
        rows = tk.Frame(card, bg=theme.SURFACE)
        rows.pack(fill="x", pady=(4, 0))
        for i in range(8):
            row = tk.Frame(rows, bg=theme.SURFACE)
            row.pack(fill="x", pady=3)
            radio = tk.Radiobutton(
                row, variable=self.stage_var, value=i, command=self._stage_selected,
                bg=theme.SURFACE, fg=theme.TEXT, activebackground=theme.SURFACE,
                activeforeground=theme.TEXT, selectcolor=theme.ACCENT,
                highlightthickness=0, bd=0, cursor="hand2",
            )
            radio.pack(side="left", padx=(0, 6))
            swatch = ColorSwatch(row, (255, 0, 0),
                                 lambda i=i: self._pick_stage_color(i), size=(44, 24))
            swatch.pack(side="right", padx=(8, 0))
            minimum, maximum = sensor_limits(self.config.sensor)
            slider = SliderRow(
                row, f"Stage {i + 1}", minimum, maximum,
                self.profile.dpi_values[i],
                lambda v, i=i: self._set_dpi(i, v),
                fmt=lambda v: self._dpi_text(v),
            )
            slider.pack(side="left", fill="x", expand=True)
            self.stage_rows.append({"radio": radio, "slider": slider, "swatch": swatch})

        note = tk.Label(card, text="The slider value is the raw stage value stored in the "
                                   "profile; the caption shows the DPI the sensor reports.",
                        bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"],
                        wraplength=620, justify="left")
        note.pack(fill="x", pady=(8, 0))

        rate_card = self._card(parent, 1, 0, "Report rate")
        self.rate_var = tk.IntVar(value=2)
        grid = tk.Frame(rate_card, bg=theme.SURFACE)
        grid.pack(fill="x", pady=(4, 0))
        for i, (_idx, label) in enumerate(RATE_LABELS):
            ttk.Radiobutton(grid, text=label, variable=self.rate_var, value=i,
                            command=self._rate_changed).grid(
                row=i // 2, column=i % 2, sticky="w", padx=(0, 24), pady=4)

        windows = self._card(parent, 2, 0, "Windows pointer")
        self.speed = SliderRow(windows, "Pointer speed", 1, 11, 6, self._speed_changed,
                               fmt=lambda v: f"{v} / 11")
        self.speed.pack(fill="x", pady=(0, 8))
        self.double = SliderRow(windows, "Double-click time", 0, 10, 5,
                                self._double_changed,
                                fmt=lambda v: f"{900 - 70 * int(v)} ms")
        self.double.pack(fill="x", pady=(0, 8))
        self.scroll_lines = SliderRow(windows, "Wheel lines", 1, 11, 3,
                                      self._scroll_changed,
                                      fmt=lambda v: f"{v} lines")
        self.scroll_lines.pack(fill="x", pady=(0, 4))
        self.onepage_var = tk.IntVar()
        ttk.Checkbutton(windows, text="Scroll one page per notch", variable=self.onepage_var,
                        command=self._onepage_changed).pack(anchor="w", pady=(2, 6))
        self.enhance_var = tk.IntVar()
        ttk.Checkbutton(windows, text="Enhance pointer precision", variable=self.enhance_var,
                        command=self._enhance_changed).pack(anchor="w", pady=(2, 0))
        tk.Label(windows, text="These are applied to Windows when the profile is sent.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"]).pack(
            anchor="w", pady=(8, 0))

    # -- right -------------------------------------------------------------
    def _build_right(self, parent) -> None:
        lod = self._card(parent, 0, 1, "Lift-off distance and key response")
        self.lift_var = tk.IntVar()
        ttk.Checkbutton(lod, text="Enable lift-off distance", variable=self.lift_var,
                        command=self._lift_changed).pack(anchor="w", pady=(2, 6))
        self.lod = SliderRow(lod, "Lift-off level", self.config.distance_min or 0,
                             max(self.config.distance_max, (self.config.distance_min or 0) + 1),
                             self.profile.lod, self._lod_changed,
                             fmt=lambda v: f"level {v}")
        self.lod.pack(fill="x", pady=(0, 6))
        self.lod_note = tk.Label(lod, text="", bg=theme.SURFACE, fg=theme.DIM,
                                 font=theme.FONTS["tiny"], wraplength=360, justify="left")
        self.lod_note.pack(fill="x")
        self.key_response = SliderRow(lod, "Key response", 1, 100, self.profile.key_response,
                                      self._key_response_changed,
                                      fmt=lambda v: f"{v} ms")
        self.key_response.pack(fill="x", pady=(10, 0))
        self.distance_note = tk.Label(lod, text="", bg=theme.SURFACE, fg=theme.AMBER,
                                      font=theme.FONTS["tiny"], wraplength=360, justify="left")
        self.distance_note.pack(fill="x", pady=(8, 0))

        info = self._card(parent, 1, 1, "Sensor")
        self.info_labels: dict[str, tk.Label] = {}
        for key, label in (("sensor", "Sensor"), ("max", "Maximum"), ("active", "Active DPI"),
                           ("mask", "High-DPI mask"), ("buttons", "Computed button slots"),
                           ("mode", "Work mode")):
            row = tk.Frame(info, bg=theme.SURFACE)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label, bg=theme.SURFACE, fg=theme.MUTED,
                     font=theme.FONTS["small"]).pack(side="left")
            value = tk.Label(row, text="-", bg=theme.SURFACE, fg=theme.TEXT,
                             font=theme.FONTS["small"])
            value.pack(side="right")
            self.info_labels[key] = value
        tk.Label(info, text="The high-DPI mask is only sent when Data.ini Distance is non-zero, "
                            "matching the shipped application's quirk.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"],
                 wraplength=360, justify="left").pack(fill="x", pady=(8, 0))

        mode = self._card(parent, 2, 1, "Work mode")
        self.mode_var = tk.IntVar(value=0)
        ttk.Radiobutton(mode, text="Game", variable=self.mode_var, value=0,
                        command=self._mode_changed).pack(anchor="w", pady=2)
        ttk.Radiobutton(mode, text="Office", variable=self.mode_var, value=1,
                        command=self._mode_changed).pack(anchor="w", pady=2)
        tk.Label(mode, text="Sent as 0x02 with mode + 1.", bg=theme.SURFACE, fg=theme.DIM,
                 font=theme.FONTS["tiny"]).pack(anchor="w", pady=(6, 0))

    def _card(self, parent, row: int, col: int, title: str) -> tk.Frame:
        card = tk.Frame(parent, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                        highlightthickness=1, padx=16, pady=12)
        card.grid(row=row, column=col, sticky="nsew", padx=(0 if col == 0 else 8, 0),
                  pady=(0, 10))
        tk.Label(card, text=title, bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        hline(card, 6)
        return card

    # -- helpers -----------------------------------------------------------
    def _dpi_text(self, value: int) -> str:
        return f"{int(value)}  ->  {sensor_display_dpi(self.config.sensor, int(value)):,} DPI"

    def _set_dpi(self, index: int, value: int) -> None:
        if self._loading:
            return
        values = self.profile.dpi_values
        values[index] = int(value)
        self.profile.dpi_values = values
        self.app.mark_dirty(f"DPI stage {index + 1} = {value}")
        self._refresh_info()

    def _pick_stage_color(self, index: int) -> None:
        current = self.profile.stage_colors[index]
        from ...model import colorref_to_rgb, rgb_to_colorref
        rgb = dialogs.pick_color(self.app, colorref_to_rgb(current),
                                 f"Stage {index + 1} LED colour")
        if rgb is None:
            return
        colors = self.profile.stage_colors
        colors[index] = rgb_to_colorref(rgb)
        self.profile.stage_colors = colors
        self.stage_rows[index]["swatch"].set_rgb(rgb)
        self.app.mark_dirty(f"stage {index + 1} colour")

    def _stage_selected(self) -> None:
        if self._loading:
            return
        stage = int(self.stage_var.get())
        max_stage = self.profile.stage_count - 1
        if stage > max_stage:
            stage = max_stage
            self.stage_var.set(stage)
        self.profile.stage = stage
        self.app.mark_dirty(f"active stage {stage + 1}")
        self._refresh_info()

    def _count_changed(self) -> None:
        if self._loading:
            return
        self.profile.stage_count = int(self.count_var.get())
        if self.profile.stage >= self.profile.stage_count:
            self.profile.stage = self.profile.stage_count - 1
        self.app.mark_dirty("stage count")
        self.refresh()

    def _rate_changed(self) -> None:
        if self._loading:
            return
        self.profile.rate = int(self.rate_var.get())
        self.app.mark_dirty("report rate")

    def _speed_changed(self, value: int) -> None:
        if self._loading:
            return
        self.profile.speed = int(value)
        self.app.mark_dirty("Windows pointer speed")

    def _double_changed(self, value: int) -> None:
        if self._loading:
            return
        self.profile.double = int(value)
        self.app.mark_dirty("double-click time")

    def _scroll_changed(self, value: int) -> None:
        if self._loading:
            return
        self.profile.scroll = int(value)
        self.app.mark_dirty("wheel lines")

    def _onepage_changed(self) -> None:
        if self._loading:
            return
        self.profile.onepage = int(self.onepage_var.get())
        self.app.mark_dirty("one-page scroll")

    def _enhance_changed(self) -> None:
        if self._loading:
            return
        self.profile.enhance = int(self.enhance_var.get())
        self.app.mark_dirty("enhance pointer precision")

    def _lift_changed(self) -> None:
        if self._loading:
            return
        self.profile.lift = int(self.lift_var.get())
        self.app.mark_dirty("lift-off enable")

    def _lod_changed(self, value: int) -> None:
        if self._loading:
            return
        self.profile.lod = int(value)
        self.app.mark_dirty("lift-off level")
        self._refresh_info()

    def _key_response_changed(self, value: int) -> None:
        if self._loading:
            return
        self.profile.key_response = int(value)
        self.app.mark_dirty("key response")

    def _mode_changed(self) -> None:
        if self._loading:
            return
        self.profile.mode = int(self.mode_var.get())
        self.app.mark_dirty("work mode")

    # -- refresh -----------------------------------------------------------
    def refresh(self) -> None:
        self._loading = True
        try:
            prof = self.profile
            minimum, maximum = sensor_limits(self.config.sensor)
            self.sensor_label.configure(
                text=f"sensor 0x{self.config.sensor:04X}   max {sensor_max_label(self.config.sensor)} DPI")
            self.count_var.set(str(prof.stage_count))
            self.stage_var.set(prof.stage)
            for i, row in enumerate(self.stage_rows):
                row["slider"].set_range(minimum, maximum)
                row["slider"].set(prof.dpi_values[i])
                enabled = i < prof.stage_count
                row["slider"].set_enabled(enabled)
                row["radio"].configure(state="normal" if enabled else "disabled",
                                       fg=theme.TEXT if enabled else theme.DIM)
                row["swatch"].set_rgb(_colorref_rgb(prof.stage_colors[i]))
            self.rate_var.set(min(3, max(0, prof.rate)))
            self.speed.set(prof.speed)
            self.double.set(prof.double)
            self.scroll_lines.set(prof.scroll)
            self.onepage_var.set(1 if prof.onepage else 0)
            self.enhance_var.set(1 if prof.enhance else 0)
            self.lift_var.set(1 if prof.lift else 0)
            lod_min = self.config.distance_min
            lod_max = self.config.distance_max
            if lod_max <= lod_min:
                lod_max = lod_min + 1
            self.lod.set_range(lod_min, lod_max)
            if lod_min <= prof.lod <= lod_max:
                self.lod.set(prof.lod)
                self.lod_note.configure(text=f"Lift-off code for this level: "
                                             f"{self.config.distance_value_for_stage(prof.lod)}",
                                        fg=theme.DIM)
            else:
                self.lod.set(lod_min)
                self.lod_note.configure(
                    text=f"Profile value {prof.lod} is outside the slider range "
                         f"({lod_min}..{lod_max}); it transmits code 0.",
                    fg=theme.AMBER)
            self.key_response.set(prof.key_response)
            self.mode_var.set(1 if prof.mode else 0)
            if self.config.distance == 0:
                self.distance_note.configure(
                    text="Data.ini Distance=0: the 0x04 lift-off/key-response frame and the "
                         "0x07 high-DPI mask are skipped, exactly like the original.")
            else:
                self.distance_note.configure(
                    text=f"Distance={self.config.distance}: lift-off and high-DPI frames are sent.")
            self._refresh_info()
        finally:
            self._loading = False

    def _refresh_info(self) -> None:
        prof = self.profile
        computed = sum(1 for i in range(64) if self.config.button_is_computed(i))
        stage = min(prof.stage, 7)
        self.info_labels["sensor"].configure(text=f"0x{self.config.sensor:04X}")
        self.info_labels["max"].configure(text=f"{sensor_max_label(self.config.sensor)} DPI")
        self.info_labels["active"].configure(
            text=f"{sensor_display_dpi(self.config.sensor, prof.dpi_values[stage]):,} DPI")
        self.info_labels["mask"].configure(text=f"0x{high_dpi_mask(prof, self.config.sensor):02X}")
        self.info_labels["buttons"].configure(text=str(computed))
        self.info_labels["mode"].configure(text="Office" if prof.mode else "Game")

    def _show_plan(self) -> None:
        lines = describe_apply(self.profile, self.config)
        lines.append("")
        lines.append(f"Windows pointer: speed {self.profile.speed}/11, "
                     f"double-click {900 - 70 * self.profile.double} ms, "
                     f"wheel {'one page' if self.profile.onepage else str(self.profile.scroll) + ' lines'}, "
                     f"enhance {'on' if self.profile.enhance else 'off'}")
        dialogs.show_message(self.app, "Apply plan", "\n".join(lines), "info")


def _colorref_rgb(value: int) -> tuple[int, int, int]:
    return value & 0xFF, (value >> 8) & 0xFF, (value >> 16) & 0xFF
