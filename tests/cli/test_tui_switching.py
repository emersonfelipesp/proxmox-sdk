"""Smoke tests for the per-module TUI runner loop.

The runner reads the sentinel returned by ``App.run()`` and instantiates the
matching module's app. Here we monkey-patch the app classes with a stub
``run()`` that returns a scripted sequence of sentinels, and assert the
runner dispatches to the right class on each switch.
"""

from __future__ import annotations

from typing import Any

import pytest

pytest.importorskip("textual")

from proxmox_sdk.proxmox_cli.tui import chrome  # noqa: E402
from proxmox_sdk.proxmox_cli.tui import runner as runner_module  # noqa: E402


class _StubApp:
    """Stand-in for a Textual App: records construction and returns a scripted result."""

    SCRIPT: list[object] = []
    INSTANCES: list["_StubApp"] = []

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        _StubApp.INSTANCES.append(self)

    def run(self) -> object:
        return _StubApp.SCRIPT.pop(0)


@pytest.fixture(autouse=True)
def _reset_stubs() -> None:
    _StubApp.SCRIPT = []
    _StubApp.INSTANCES = []


def _patch_apps(monkeypatch: pytest.MonkeyPatch) -> dict[str, type]:
    """Replace the four module-app classes with separate stub subclasses."""
    stubs: dict[str, type] = {}
    for module, attr in (
        ("pve", "PVETuiApp"),
        ("ceph", "CephTuiApp"),
        ("pbs", "PBSTuiApp"),
        ("pdm", "PDMTuiApp"),
    ):
        cls = type(f"Stub_{module}", (_StubApp,), {"MODULE": module})
        stubs[module] = cls
        monkeypatch.setattr(runner_module, attr, cls)
    return stubs


def test_runner_exits_when_app_returns_none(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_apps(monkeypatch)
    _StubApp.SCRIPT = [None]
    runner_module.run_module_tui(bridge=object(), mode="mock", initial_module="pve")
    assert len(_StubApp.INSTANCES) == 1


def test_runner_swaps_between_modules(monkeypatch: pytest.MonkeyPatch) -> None:
    stubs = _patch_apps(monkeypatch)
    _StubApp.SCRIPT = [
        chrome.SWITCH_TO_CEPH,
        chrome.SWITCH_TO_PBS,
        chrome.SWITCH_TO_PDM,
        None,
    ]
    runner_module.run_module_tui(bridge=object(), mode="production", initial_module="pve")

    visited = [type(inst).MODULE for inst in _StubApp.INSTANCES]  # type: ignore[attr-defined]
    assert visited == ["pve", "ceph", "pbs", "pdm"]
    assert all(isinstance(inst, stubs[m]) for inst, m in zip(_StubApp.INSTANCES, visited))


def test_sentinel_to_module_roundtrip() -> None:
    for module in chrome.MODULE_ORDER:
        sentinel = chrome.sentinel_for_module(module)
        assert chrome.module_for_sentinel(sentinel) == module


def test_unknown_sentinel_returns_none() -> None:
    assert chrome.module_for_sentinel("not-a-real-sentinel") is None
    assert chrome.module_for_sentinel(None) is None


def test_runner_ignores_self_sentinel(monkeypatch: pytest.MonkeyPatch) -> None:
    _patch_apps(monkeypatch)
    # If a misbehaving app returns its own sentinel, the runner should stop
    # instead of looping forever.
    _StubApp.SCRIPT = [chrome.SWITCH_TO_PVE]
    runner_module.run_module_tui(bridge=object(), mode="mock", initial_module="pve")
    assert len(_StubApp.INSTANCES) == 1


class _NoopBridge:
    """Bridge stand-in that returns ``None`` for every operation."""

    def get(self, *a: Any, **kw: Any) -> Any:
        return None

    def list_children(self, *a: Any, **kw: Any) -> Any:
        return None

    def post(self, *a: Any, **kw: Any) -> Any:
        return None

    def put(self, *a: Any, **kw: Any) -> Any:
        return None

    def delete(self, *a: Any, **kw: Any) -> Any:
        return None

    def close(self) -> None:
        return None


@pytest.mark.asyncio
async def test_path_browser_apps_mount_and_emit_switch_sentinel() -> None:
    """Each path-browser app mounts cleanly and exits with the right sentinel
    when the View selector changes."""
    from textual.widgets import Select

    from proxmox_sdk.proxmox_cli.tui.base import PathBrowserRuntime
    from proxmox_sdk.proxmox_cli.tui.ceph_app import CephTuiApp
    from proxmox_sdk.proxmox_cli.tui.pbs_app import PBSTuiApp
    from proxmox_sdk.proxmox_cli.tui.pve_app import PVETuiApp

    cases = (
        (PVETuiApp, "/nodes", "pdm", chrome.SWITCH_TO_PDM),
        (CephTuiApp, "/cluster/ceph/status", "pbs", chrome.SWITCH_TO_PBS),
        (PBSTuiApp, "/admin/datastore", "ceph", chrome.SWITCH_TO_CEPH),
    )

    for app_cls, initial_path, switch_to, expected_sentinel in cases:
        app = app_cls(
            bridge=_NoopBridge(),
            runtime=PathBrowserRuntime(mode="mock", initial_path=initial_path),
        )
        async with app.run_test() as pilot:
            select = pilot.app.query_one("#view_select", Select)
            select.value = switch_to
            await pilot.pause()
        assert app.return_value == expected_sentinel, app_cls.__name__
