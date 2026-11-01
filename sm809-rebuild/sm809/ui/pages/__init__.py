"""Page controllers for the main window."""

from __future__ import annotations

import tkinter as tk

from .. import theme


class Page(tk.Frame):
    title = ""
    subtitle = ""

    def __init__(self, parent, app):
        super().__init__(parent, bg=theme.BG)
        self.app = app
        self.build()

    @property
    def store(self):
        return self.app.store

    @property
    def config(self):
        return self.app.config

    @property
    def profile(self):
        return self.app.store.profile

    def build(self) -> None:
        raise NotImplementedError

    def refresh(self) -> None:
        pass

    def on_show(self) -> None:
        pass

    def header(self, parent) -> tk.Frame:
        bar = tk.Frame(parent, bg=theme.BG)
        tk.Label(bar, text=self.title, bg=theme.BG, fg=theme.TEXT,
                 font=theme.FONTS["h1"]).pack(side="left")
        if self.subtitle:
            tk.Label(bar, text=self.subtitle, bg=theme.BG, fg=theme.MUTED,
                     font=theme.FONTS["small"]).pack(side="left", padx=(14, 0), pady=(8, 0))
        return bar
