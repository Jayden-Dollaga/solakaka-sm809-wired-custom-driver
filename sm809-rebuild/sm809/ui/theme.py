"""Dark theme and shared widget styling for the rebuild UI."""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk

# Palette
BG = "#11141a"
SURFACE = "#1a1e27"
SURFACE_ALT = "#202633"
SURFACE_HI = "#283040"
BORDER = "#2c3545"
TEXT = "#e8edf5"
MUTED = "#8b97aa"
DIM = "#616d80"
ACCENT = "#4c8dff"
ACCENT_HOVER = "#6aa0ff"
ACCENT_DARK = "#2f6fe0"
GREEN = "#3ecf8e"
AMBER = "#e5a13c"
RED = "#e05c5c"
PURPLE = "#a78bfa"

FONTS: dict[str, tkfont.Font] = {}


def init_theme(root: tk.Tk) -> None:
    """Create named fonts and ttk styles. Safe to call once per process."""
    family = "Segoe UI"
    try:
        available = set(tkfont.families(root))
        if family not in available:
            family = "Helvetica"
    except Exception:
        pass
    FONTS["base"] = tkfont.Font(root=root, family=family, size=10)
    FONTS["small"] = tkfont.Font(root=root, family=family, size=9)
    FONTS["tiny"] = tkfont.Font(root=root, family=family, size=8)
    FONTS["bold"] = tkfont.Font(root=root, family=family, size=10, weight="bold")
    FONTS["h2"] = tkfont.Font(root=root, family=family, size=12, weight="bold")
    FONTS["h1"] = tkfont.Font(root=root, family=family, size=20, weight="bold")
    FONTS["mono"] = tkfont.Font(root=root, family="Consolas", size=9)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", background=BG, foreground=TEXT, font=FONTS["base"])
    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=SURFACE)
    style.configure("TLabel", background=BG, foreground=TEXT)
    style.configure("Muted.TLabel", background=BG, foreground=MUTED)
    style.configure("Surface.TLabel", background=SURFACE, foreground=TEXT)
    style.configure("SurfaceMuted.TLabel", background=SURFACE, foreground=MUTED)
    style.configure("H2.TLabel", background=BG, foreground=TEXT, font=FONTS["h2"])
    style.configure("SurfaceH2.TLabel", background=SURFACE, foreground=TEXT, font=FONTS["h2"])

    style.configure(
        "TButton",
        background=SURFACE_ALT,
        foreground=TEXT,
        bordercolor=BORDER,
        lightcolor=SURFACE_ALT,
        darkcolor=SURFACE_ALT,
        focuscolor=SURFACE_ALT,
        relief="flat",
        padding=(10, 6),
    )
    style.map(
        "TButton",
        background=[("active", SURFACE_HI), ("pressed", SURFACE_HI), ("disabled", SURFACE)],
        foreground=[("disabled", DIM)],
    )
    style.configure(
        "Accent.TButton",
        background=ACCENT,
        foreground="#ffffff",
        bordercolor=ACCENT,
        lightcolor=ACCENT,
        darkcolor=ACCENT,
        padding=(12, 7),
        font=FONTS["bold"],
    )
    style.map(
        "Accent.TButton",
        background=[("active", ACCENT_HOVER), ("pressed", ACCENT_DARK), ("disabled", SURFACE_HI)],
        foreground=[("disabled", DIM)],
    )
    style.configure(
        "Danger.TButton",
        background="#3a2226",
        foreground="#ffb3b3",
        bordercolor="#5a3036",
        lightcolor="#3a2226",
        darkcolor="#3a2226",
    )
    style.map("Danger.TButton", background=[("active", "#4a2b31")])

    style.configure(
        "TCheckbutton",
        background=SURFACE,
        foreground=TEXT,
        focuscolor=SURFACE,
        indicatorcolor=SURFACE_ALT,
        indicatorbackground=SURFACE_ALT,
    )
    style.map(
        "TCheckbutton",
        background=[("active", SURFACE)],
        indicatorcolor=[("selected", ACCENT), ("active", SURFACE_HI)],
    )
    style.configure(
        "TRadiobutton",
        background=SURFACE,
        foreground=TEXT,
        focuscolor=SURFACE,
        indicatorcolor=SURFACE_ALT,
        indicatorbackground=SURFACE_ALT,
    )
    style.map(
        "TRadiobutton",
        background=[("active", SURFACE)],
        indicatorcolor=[("selected", ACCENT), ("active", SURFACE_HI)],
    )

    style.configure(
        "TCombobox",
        fieldbackground=SURFACE_ALT,
        background=SURFACE_ALT,
        foreground=TEXT,
        arrowcolor=TEXT,
        bordercolor=BORDER,
        lightcolor=SURFACE_ALT,
        darkcolor=SURFACE_ALT,
        selectbackground=SURFACE_HI,
        selectforeground=TEXT,
        padding=(8, 4),
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", SURFACE_ALT), ("disabled", SURFACE)],
        foreground=[("disabled", DIM)],
        bordercolor=[("focus", ACCENT)],
    )
    root.option_add("*TCombobox*Listbox.background", SURFACE_ALT)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT_DARK)
    root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")

    style.configure(
        "TEntry",
        fieldbackground=SURFACE_ALT,
        foreground=TEXT,
        insertcolor=TEXT,
        bordercolor=BORDER,
        lightcolor=SURFACE_ALT,
        darkcolor=SURFACE_ALT,
        padding=(6, 4),
    )
    style.map("TEntry", bordercolor=[("focus", ACCENT)])

    style.configure(
        "TSpinbox",
        fieldbackground=SURFACE_ALT,
        background=SURFACE_ALT,
        foreground=TEXT,
        arrowcolor=TEXT,
        bordercolor=BORDER,
        lightcolor=SURFACE_ALT,
        darkcolor=SURFACE_ALT,
        padding=(4, 3),
    )
    style.map(
        "TSpinbox",
        bordercolor=[("focus", ACCENT)],
        fieldbackground=[("disabled", SURFACE)],
        foreground=[("disabled", DIM)],
        arrowcolor=[("disabled", DIM)],
    )

    style.configure(
        "Horizontal.TScale",
        background=SURFACE,
        troughcolor=SURFACE_ALT,
        bordercolor=SURFACE,
        lightcolor=ACCENT,
        darkcolor=ACCENT,
        sliderthickness=14,
    )
    style.map("Horizontal.TScale", background=[("active", SURFACE)])
    style.configure(
        "Vertical.TScrollbar",
        background=SURFACE_HI,
        troughcolor=SURFACE,
        bordercolor=SURFACE,
        arrowcolor=MUTED,
        gripcount=0,
    )
    style.map("Vertical.TScrollbar", background=[("active", "#38445a")])

    style.configure(
        "Treeview",
        background=SURFACE,
        fieldbackground=SURFACE,
        foreground=TEXT,
        bordercolor=BORDER,
        rowheight=26,
        font=FONTS["base"],
    )
    style.configure(
        "Treeview.Heading",
        background=SURFACE_ALT,
        foreground=MUTED,
        relief="flat",
        font=FONTS["small"],
        padding=(6, 5),
    )
    style.map(
        "Treeview",
        background=[("selected", ACCENT_DARK)],
        foreground=[("selected", "#ffffff")],
    )
    style.map("Treeview.Heading", background=[("active", SURFACE_HI)])
    style.layout("Treeview", [("Treeview.treearea", {"sticky": "nswe"})])

    style.configure(
        "Horizontal.TProgressbar",
        background=ACCENT,
        troughcolor=SURFACE_ALT,
        bordercolor=SURFACE_ALT,
        lightcolor=ACCENT,
        darkcolor=ACCENT,
    )
    style.configure("TSeparator", background=BORDER)


class FlatButton(tk.Button):
    """tk.Button that also repaints itself when it becomes disabled."""

    def __init__(self, parent, text: str, command=None, *, kind: str = "secondary",
                 width: int | None = None, font_key: str = "base"):
        colors = {
            "primary": (ACCENT, "#ffffff", ACCENT_HOVER, ACCENT_DARK),
            "secondary": (SURFACE_ALT, TEXT, SURFACE_HI, SURFACE_HI),
            "ghost": (SURFACE, MUTED, SURFACE_ALT, SURFACE_ALT),
            "danger": ("#3a2226", "#ffb3b3", "#4a2b31", "#4a2b31"),
            "success": ("#1e3a2f", "#b6f0d3", "#264a3b", "#264a3b"),
        }
        self._bg, self._fg, self._hover, self._active = colors.get(kind, colors["secondary"])
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=self._bg,
            fg=self._fg,
            activebackground=self._active,
            activeforeground=self._fg,
            disabledforeground=DIM,
            relief="flat",
            bd=0,
            highlightthickness=0,
            padx=12,
            pady=6,
            cursor="hand2",
            font=FONTS.get(font_key, FONTS["base"]),
            overrelief="flat",
        )
        if width:
            self.configure(width=width)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def configure(self, cnf=None, **kw):
        state = kw.get("state")
        if state is None and isinstance(cnf, dict):
            state = cnf.get("state")
        super().configure(cnf, **kw)
        if state is not None:
            self._paint(state)

    config = configure

    def _paint(self, state) -> None:
        if str(state) == "disabled":
            super().configure(bg=SURFACE_ALT, fg=DIM, cursor="arrow")
        else:
            super().configure(bg=self._bg, fg=self._fg, cursor="hand2")

    def _on_enter(self, _event=None) -> None:
        if self["state"] != "disabled":
            super().configure(bg=self._hover)

    def _on_leave(self, _event=None) -> None:
        if self["state"] != "disabled":
            super().configure(bg=self._bg)


def button(parent, text: str, command=None, *, kind: str = "secondary",
           width: int | None = None, font_key: str = "base") -> FlatButton:
    """Flat button that keeps its colours on every platform theme."""
    return FlatButton(parent, text, command, kind=kind, width=width, font_key=font_key)


def entry(parent, textvariable=None, *, width: int = 12, justify: str = "left") -> tk.Entry:
    return tk.Entry(
        parent,
        textvariable=textvariable,
        width=width,
        bg=SURFACE_ALT,
        fg=TEXT,
        insertbackground=TEXT,
        disabledbackground=SURFACE,
        disabledforeground=DIM,
        relief="flat",
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        font=FONTS["base"],
        justify=justify,
    )


def label(parent, text: str, *, muted: bool = False, bold: bool = False,
          surface: bool = False, font_key: str | None = None, **kw) -> tk.Label:
    bg = SURFACE if surface else BG
    fg = MUTED if muted else TEXT
    f = FONTS[font_key] if font_key else (FONTS["bold"] if bold else FONTS["base"])
    return tk.Label(parent, text=text, bg=bg, fg=fg, font=f, **kw)


def card(parent, *, padding: int = 16, **kw) -> tk.Frame:
    frame = tk.Frame(
        parent,
        bg=SURFACE,
        highlightbackground=BORDER,
        highlightthickness=1,
        bd=0,
        **kw,
    )
    return frame


def separator(parent) -> tk.Frame:
    line = tk.Frame(parent, bg=BORDER, height=1)
    return line


def status_color(kind: str) -> str:
    return {"ok": GREEN, "warn": AMBER, "error": RED, "info": ACCENT}.get(kind, MUTED)
