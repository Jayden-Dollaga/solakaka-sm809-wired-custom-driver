"""LED mode and colour page."""

from __future__ import annotations

import tkinter as tk

from .. import theme
from ...model import colorref_to_rgb, rgb_to_colorref
from ...protocol import light_mode_label, light_parameters
from .. import dialogs
from ..widgets import ColorSwatch, ScrollFrame, SliderRow, hline
from . import Page


class LightPage(Page):
    title = "Lighting"
    subtitle = "12 firmware modes, fixed colour and the 8-colour cycle palette"

    def build(self) -> None:
        self._loading = False
        outer = tk.Frame(self, bg=theme.BG, padx=22, pady=18)
        outer.pack(fill="both", expand=True)
        head = self.header(outer)
        head.pack(fill="x")
        theme.button(head, "Apply to mouse", self.app.apply_now, kind="primary").pack(side="right")

        scroll = ScrollFrame(outer)
        scroll.pack(fill="both", expand=True, pady=(10, 0))
        body = scroll.body
        body.grid_columnconfigure(0, weight=2, uniform="light")
        body.grid_columnconfigure(1, weight=3, uniform="light")

        # Mode list
        mode_card = self._card(body, 0, 0, "Effect mode")
        self.mode_var = tk.IntVar(value=0)
        for i in range(12):
            ttk_radio = tk.Radiobutton(
                mode_card, text=f"{i:02d}   {light_mode_label(i)}", variable=self.mode_var,
                value=i, command=self._mode_changed, bg=theme.SURFACE, fg=theme.TEXT,
                activebackground=theme.SURFACE, activeforeground=theme.TEXT,
                selectcolor=theme.ACCENT, highlightthickness=0, bd=0, anchor="w",
                font=theme.FONTS["base"], padx=6, pady=3, cursor="hand2",
            )
            ttk_radio.pack(fill="x")
        tk.Label(mode_card, text="The shipped resources do not contain localised effect names; "
                                 "these labels describe which parameters each mode consumes.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"],
                 wraplength=340, justify="left").pack(fill="x", pady=(8, 0))

        # Parameters
        param_card = self._card(body, 0, 1, "Effect parameters")
        self.mode_note = tk.Label(param_card, text="", bg=theme.SURFACE, fg=theme.ACCENT,
                                  font=theme.FONTS["small"], wraplength=520, justify="left")
        self.mode_note.pack(fill="x", pady=(0, 8))
        self.brightness = SliderRow(param_card, "Brightness", 0, 255, 255,
                                    self._brightness_changed, fmt=lambda v: f"{v} / 255")
        self.brightness.pack(fill="x", pady=(0, 8))
        self.frequency = SliderRow(param_card, "Frequency / speed", 0, 4, 3,
                                   self._frequency_changed, fmt=lambda v: f"{v} / 4")
        self.frequency.pack(fill="x", pady=(0, 8))
        self.length = SliderRow(param_card, "Length", 0, 4, 3, self._length_changed,
                                fmt=lambda v: f"{v} / 4")
        self.length.pack(fill="x", pady=(0, 8))
        self.direction = SliderRow(param_card, "Direction", 0, 4, 2, self._direction_changed,
                                   fmt=lambda v: f"{v} / 4")
        self.direction.pack(fill="x", pady=(0, 0))

        preview_row = tk.Frame(param_card, bg=theme.SURFACE)
        preview_row.pack(fill="x", pady=(12, 0))
        tk.Label(preview_row, text="Preview", bg=theme.SURFACE, fg=theme.MUTED,
                 font=theme.FONTS["small"]).pack(anchor="w")
        self.preview = tk.Canvas(preview_row, height=30, bg=theme.SURFACE_ALT,
                                 highlightthickness=1, highlightbackground=theme.BORDER)
        self.preview.pack(fill="x", pady=(4, 0))
        self.preview.bind("<Configure>", lambda _e: self._draw_preview())

        # Colours
        color_card = self._card(body, 1, 0, "Colours")
        fixed_row = tk.Frame(color_card, bg=theme.SURFACE)
        fixed_row.pack(fill="x", pady=(4, 8))
        self.fixed_swatch = ColorSwatch(fixed_row, (255, 0, 0), self._pick_fixed,
                                        size=(64, 32))
        self.fixed_swatch.pack(side="left")
        info = tk.Frame(fixed_row, bg=theme.SURFACE)
        info.pack(side="left", padx=(10, 0))
        tk.Label(info, text="Fixed colour (0x0C)", bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["bold"]).pack(anchor="w")
        self.fixed_text = tk.Label(info, text="", bg=theme.SURFACE, fg=theme.MUTED,
                                   font=theme.FONTS["small"])
        self.fixed_text.pack(anchor="w")
        theme.button(fixed_row, "Choose...", self._pick_fixed, kind="secondary").pack(
            side="right")

        hline(color_card, 8)
        tk.Label(color_card, text="Cycle palette (0x10 block 0)", bg=theme.SURFACE,
                 fg=theme.TEXT, font=theme.FONTS["bold"]).pack(anchor="w")
        tk.Label(color_card, text="Eight colours are always uploaded, even when the current "
                                  "mode does not cycle.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"],
                 wraplength=340, justify="left").pack(anchor="w", pady=(2, 8))
        palette = tk.Frame(color_card, bg=theme.SURFACE)
        palette.pack(fill="x")
        self.cycle_swatches: list[ColorSwatch] = []
        for i in range(8):
            wrap = tk.Frame(palette, bg=theme.SURFACE)
            wrap.grid(row=i // 4, column=i % 4, padx=3, pady=3, sticky="w")
            sw = ColorSwatch(wrap, (255, 255, 255), lambda i=i: self._pick_cycle(i),
                             size=(64, 30))
            sw.pack()
            tk.Label(wrap, text=f"Colour {i + 1}", bg=theme.SURFACE, fg=theme.MUTED,
                     font=theme.FONTS["tiny"]).pack()
            self.cycle_swatches.append(sw)

        stage_note = self._card(body, 2, 0, "Per-stage DPI colours")
        self.stage_text = tk.Label(stage_note, text="", bg=theme.SURFACE, fg=theme.MUTED,
                                   font=theme.FONTS["small"], justify="left", wraplength=340)
        self.stage_text.pack(fill="x")
        tk.Label(stage_note, text="Edit these on the Performance page. They are uploaded as "
                                  "0x10 block 1.",
                 bg=theme.SURFACE, fg=theme.DIM, font=theme.FONTS["tiny"],
                 wraplength=340, justify="left").pack(fill="x", pady=(4, 0))

    def _card(self, parent, row: int, col: int, title: str) -> tk.Frame:
        card = tk.Frame(parent, bg=theme.SURFACE, highlightbackground=theme.BORDER,
                        highlightthickness=1, padx=16, pady=12)
        card.grid(row=row, column=col, sticky="nsew", padx=(0 if col == 0 else 8, 0),
                  pady=(0, 10), rowspan=1)
        tk.Label(card, text=title, bg=theme.SURFACE, fg=theme.TEXT,
                 font=theme.FONTS["h2"]).pack(anchor="w")
        hline(card, 6)
        return card

    # -- callbacks ---------------------------------------------------------
    def _mode_changed(self) -> None:
        if getattr(self, "_loading", False):
            return
        self.profile.light_mode = int(self.mode_var.get())
        self.app.mark_dirty(f"light mode {self.profile.light_mode}")
        self._param_state()
        self._draw_preview()

    def _brightness_changed(self, value: int) -> None:
        if getattr(self, "_loading", False):
            return
        self.profile.brightness = int(value)
        self.app.mark_dirty("brightness")
        self._draw_preview()

    def _frequency_changed(self, value: int) -> None:
        if getattr(self, "_loading", False):
            return
        self.profile.frequency = int(value)
        self.app.mark_dirty("light frequency")

    def _length_changed(self, value: int) -> None:
        if getattr(self, "_loading", False):
            return
        self.profile.length = int(value)
        self.app.mark_dirty("light length")

    def _direction_changed(self, value: int) -> None:
        if getattr(self, "_loading", False):
            return
        self.profile.direction = int(value)
        self.app.mark_dirty("light direction")

    def _pick_fixed(self) -> None:
        rgb = dialogs.pick_color(self.app, self.profile.fixed_rgb, "Fixed LED colour")
        if rgb is None:
            return
        self.profile.fixed_rgb = rgb
        self.app.mark_dirty("fixed LED colour")
        self._refresh_colors()

    def _pick_cycle(self, index: int) -> None:
        current = colorref_to_rgb(self.profile.cycle_colors[index])
        rgb = dialogs.pick_color(self.app, current, f"Cycle colour {index + 1}")
        if rgb is None:
            return
        colors = self.profile.cycle_colors
        colors[index] = rgb_to_colorref(rgb)
        self.profile.cycle_colors = colors
        self.app.mark_dirty(f"cycle colour {index + 1}")
        self._refresh_colors()

    def _param_state(self) -> None:
        mode = self.profile.light_mode
        used = set(light_parameters(mode))
        labels = {
            "brightness": self.brightness,
            "frequency": self.frequency,
            "length": self.length,
            "direction": self.direction,
        }
        for name, slider in labels.items():
            active = name in used or (name == "frequency" and "toggle" in used)
            slider.label.configure(fg=theme.ACCENT if active else theme.DIM)
            slider.value_label.configure(fg=theme.ACCENT if active else theme.DIM)
            slider.scale.state(["!disabled"] if active else ["disabled"])
        names = []
        for name in used:
            names.append("toggle (frequency used as on/off)" if name == "toggle" else name)
        if names:
            self.mode_note.configure(
                text=f"Mode {mode} uses: " + ", ".join(names) + ". Greyed sliders are ignored "
                     f"by the firmware for this mode.")
        else:
            self.mode_note.configure(text=f"Mode {mode} sends zero parameters (effect off).")

    def _draw_preview(self) -> None:
        if not hasattr(self, "preview"):
            return
        r, g, b = self.profile.fixed_rgb
        scale = max(0, min(255, self.profile.brightness)) / 255.0
        color = f"#{int(r * scale):02x}{int(g * scale):02x}{int(b * scale):02x}"
        self.preview.delete("all")
        self.preview.configure(bg=theme.SURFACE_ALT)
        width = max(self.preview.winfo_width(), 60)
        self.preview.create_rectangle(0, 0, width, 30, fill=color, outline="")
        self.preview.create_text(width // 2, 15, text=f"RGB {r}, {g}, {b} @ {self.profile.brightness}",
                                 fill="#ffffff" if scale < 0.7 else "#111111",
                                 font=theme.FONTS["tiny"])

    def _refresh_colors(self) -> None:
        rgb = self.profile.fixed_rgb
        self.fixed_swatch.set_rgb(rgb)
        self.fixed_text.configure(text=f"R {rgb[0]}   G {rgb[1]}   B {rgb[2]}   (#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X})")
        for i, sw in enumerate(self.cycle_swatches):
            sw.set_rgb(colorref_to_rgb(self.profile.cycle_colors[i]))
        colors = [colorref_to_rgb(c) for c in self.profile.stage_colors]
        count = self.profile.stage_count
        self.stage_text.configure(
            text="\n".join(
                f"Stage {i + 1}:  #{r:02X}{g:02X}{b:02X}" + ("" if i < count else "  (unused)")
                for i, (r, g, b) in enumerate(colors)
            )
        )
        self._draw_preview()

    def refresh(self) -> None:
        self._loading = True
        try:
            prof = self.profile
            self.mode_var.set(max(0, min(11, prof.light_mode)))
            self.brightness.set(prof.brightness)
            self.frequency.set(prof.frequency)
            self.length.set(prof.length)
            self.direction.set(prof.direction)
            self._param_state()
            self._refresh_colors()
        finally:
            self._loading = False
