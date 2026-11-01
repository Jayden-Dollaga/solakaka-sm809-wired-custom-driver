"""Tkinter user interface for the SM809 rebuild."""

from __future__ import annotations

__all__ = ["App"]


def __getattr__(name: str):
    if name == "App":
        from .app import App

        return App
    raise AttributeError(name)
