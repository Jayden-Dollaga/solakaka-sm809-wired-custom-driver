"""Elevation helpers: the studio runs at the same privilege level as the
official driver so elevated games/anti-cheat titles can be detected."""

import os

import pytest

from app import elevation

pytestmark = pytest.mark.skipif(os.name != "nt",
                                reason="elevation is a Windows feature")


def test_is_admin_returns_a_bool():
    assert isinstance(elevation.is_admin(), bool)


def test_needs_elevation_matrix():
    assert elevation.needs_elevation([], {}, admin=False) is True
    assert elevation.needs_elevation([], {}, admin=True) is False
    # dev/demo and an explicit opt-out never prompt
    assert elevation.needs_elevation(["--demo"], {}, admin=False) is False
    assert elevation.needs_elevation(["--no-elevate"], {}, admin=False) is False
    # once a relaunch was attempted, a refused UAC prompt must not loop
    assert elevation.needs_elevation(
        [], {elevation.TRIED_ENV: "1"}, admin=False) is False


def test_prepare_startup_runs_directly_when_already_elevated(monkeypatch):
    monkeypatch.setattr(elevation, "is_admin", lambda: True)
    assert elevation.prepare_startup([]) is True


def test_declined_uac_continues_and_marks_the_attempt(monkeypatch):
    monkeypatch.setattr(elevation, "needs_elevation",
                        lambda argv, env: True)
    monkeypatch.setattr(elevation, "relaunch_as_admin", lambda args: False)
    monkeypatch.setattr(elevation, "ask_continue_unelevated", lambda: True)
    monkeypatch.delenv(elevation.TRIED_ENV, raising=False)

    assert elevation.prepare_startup([]) is True
    assert os.environ.get(elevation.TRIED_ENV) == "1"


def test_quitting_at_the_uac_prompt_stops_startup(monkeypatch):
    monkeypatch.setattr(elevation, "needs_elevation",
                        lambda argv, env: True)
    monkeypatch.setattr(elevation, "relaunch_as_admin", lambda args: False)
    monkeypatch.setattr(elevation, "ask_continue_unelevated", lambda: False)
    monkeypatch.delenv(elevation.TRIED_ENV, raising=False)

    assert elevation.prepare_startup([]) is False
