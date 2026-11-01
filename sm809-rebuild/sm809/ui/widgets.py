"""Reusable tkinter widgets for the SM809 rebuild."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from . import theme


class ScrollFrame(tk.Frame):
    """Vertically scrollable frame; put content in ``.body``."""

    def __init__(self, parent, *, bg: str = theme.BG):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.body = tk.Frame(self.canvas, bg=bg)
        self._window = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.body.bind("<Configure>", self._on_body)
        self.canvas.bind("<Configure>", self._on_canvas)

        # A single dispatcher on the toplevel handles the wheel for every child
        # widget, including labels and canvases that would swallow <Enter>.
        root = self.winfo_toplevel()
        for sequence in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            root.bind_all(sequence, self._wheel_dispatch, add="+")

    def _on_body(self, _event=None) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas(self, event) -> None:
        self.canvas.itemconfigure(self._window, width=event.width)

    def _is_inside(self, widget) -> bool:
        while widget is not None:
            if widget is self:
                return True
            widget = getattr(widget, "master", None)
        return False

    def _wheel_dispatch(self, event):
        try:
            if not self.winfo_ismapped() or not self._is_inside(event.widget):
                return None
        except (tk.TclError, AttributeError):
            return None
        self._on_wheel(event)
        return "break"

    def _on_wheel(self, event) -> None:
        if getattr(event, "num", None) == 4:
            delta = -1
        elif getattr(event, "num", None) == 5:
            delta = 1
        else:
            delta = -int(event.delta / 120) if event.delta else 0
        if delta:
            self.canvas.yview_scroll(delta, "units")

    def scroll_to_top(self) -> None:
        self.canvas.yview_moveto(0.0)


class ColorSwatch(tk.Frame):
    """Clickable colour box with a hex caption."""

    def __init__(self, parent, rgb=(255, 255, 255), command: Callable[[], None] | None = None,
                 *, size=(52, 28), bg: str = theme.SURFACE):
        super().__init__(parent, bg=bg, highlightbackground=theme.BORDER, highlightthickness=1)
        self.command = command
        self._rgb = (0, 0, 0)
        self.canvas = tk.Canvas(self, width=size[0], height=size[1], bg=bg,
                                highlightthickness=0, bd=0, cursor="hand2")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", lambda _e: self.command() if self.command else None)
        self.set_rgb(rgb)

    def set_rgb(self, rgb) -> None:
        self._rgb = tuple(max(0, min(255, int(v))) for v in rgb)
        r, g, b = self._rgb
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.canvas.configure(bg=hex_color)
        if sum(self._rgb) > 560:
            fg = "#111111"
        else:
            fg = "#ffffff"
        self.canvas.delete("all")
        self.canvas.create_text(26, 14, text=f"#{r:02X}{g:02X}{b:02X}", fill=fg,
                                font=theme.FONTS["tiny"])

    def get_rgb(self) -> tuple[int, int, int]:
        return self._rgb


class SliderRow(tk.Frame):
    """Label + integer value + horizontal slider."""

    def __init__(self, parent, text: str, from_: int, to: int, value: int,
                 command: Callable[[int], None] | None = None,
                 *, fmt: Callable[[int], str] | None = None,
                 surface: bool = True, width: int | None = None):
        bg = theme.SURFACE if surface else theme.BG
        super().__init__(parent, bg=bg)
        self.command = command
        self.fmt = fmt or (lambda v: str(v))
        self._min = int(from_)
        self._max = max(int(to), int(from_) + 1)
        self._silent = True
        self._last = None

        top = tk.Frame(self, bg=bg)
        top.pack(fill="x")
        self.label = tk.Label(top, text=text, bg=bg, fg=theme.TEXT, font=theme.FONTS["base"])
        self.label.pack(side="left")
        self.value_label = tk.Label(top, text=self.fmt(int(value)), bg=bg, fg=theme.ACCENT,
                                    font=theme.FONTS["bold"])
        self.value_label.pack(side="right")

        self.var = tk.DoubleVar(value=max(self._min, min(self._max, int(value))))
        self.scale = ttk.Scale(self, from_=self._min, to=self._max,
                               variable=self.var, command=self._changed,
                               orient="horizontal")
        self.scale.pack(fill="x", pady=(4, 0))
        if width:
            self.configure(width=width)
        self._last = int(round(self.var.get()))
        self._silent = False

    def _changed(self, _raw=None) -> None:
        value = int(round(self.var.get()))
        if value != self._last:
            self._last = value
            self.value_label.configure(text=self.fmt(value))
            if not self._silent and self.command:
                self.command(value)

    def set(self, value: int, *, notify: bool = False) -> None:
        value = max(self._min, min(self._max, int(value)))
        self._silent = True
        self.var.set(value)
        self._silent = False
        self._last = value
        self.value_label.configure(text=self.fmt(value))
        if notify and self.command:
            self.command(value)

    def get(self) -> int:
        return int(round(self.var.get()))

    def set_range(self, from_: int, to: int) -> None:
        self._min = int(from_)
        self._max = max(int(to), int(from_) + 1)
        self.scale.configure(from_=self._min, to=self._max)

    def set_enabled(self, enabled: bool) -> None:
        state = ["!disabled"] if enabled else ["disabled"]
        self.scale.state(state)
        self.value_label.configure(fg=theme.ACCENT if enabled else theme.DIM)
        self.label.configure(fg=theme.TEXT if enabled else theme.DIM)


class Badge(tk.Label):
    def __init__(self, parent, text: str, color: str = theme.MUTED, *, bg: str = theme.SURFACE):
        super().__init__(parent, text=text, bg=bg, fg=color, font=theme.FONTS["tiny"],
                         padx=8, pady=3)


class Banner(tk.Frame):
    """Coloured information strip."""

    def __init__(self, parent, text: str, *, color: str = theme.AMBER,
                 bg: str = theme.SURFACE, wrap: int = 900):
        super().__init__(parent, bg=bg)
        self._bg = bg
        self.bar = tk.Frame(self, bg=color, width=4)
        self.bar.pack(side="left", fill="y")
        self.label = tk.Label(self, text=text, bg=bg, fg=theme.TEXT, justify="left",
                              anchor="w", wraplength=wrap, font=theme.FONTS["small"],
                              padx=12, pady=8)
        self.label.pack(side="left", fill="both", expand=True)

    def set_text(self, text: str, color: str | None = None) -> None:
        self.label.configure(text=text)
        if color:
            self.bar.configure(bg=color)


def spin(parent, var, from_: int, to: int, *, width: int = 6, increment: int = 1,
         command: Callable | None = None) -> ttk.Spinbox:
    box = ttk.Spinbox(parent, from_=from_, to=to, textvariable=var, width=width,
                      increment=increment, command=command,
                      style="TSpinbox")
    return box


def hline(parent, pad: int = 0) -> tk.Frame:
    line = tk.Frame(parent, bg=theme.BORDER, height=1)
    line.pack(fill="x", pady=pad)
    return line
