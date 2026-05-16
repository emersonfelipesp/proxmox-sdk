"""Shared chrome for per-module TUIs: switch sentinels and view selector options.

Mirrors ``netbox_tui/chrome.py``: each Textual app exits with one of the
``SWITCH_TO_*`` strings as its run result; the runner loop reads the sentinel
and starts the matching module's TUI in-process.
"""

from __future__ import annotations

from typing import Literal

ModuleName = Literal["pve", "ceph", "pbs", "pdm"]

SWITCH_TO_PVE: str = "switch-to-pve-tui"
SWITCH_TO_CEPH: str = "switch-to-ceph-tui"
SWITCH_TO_PBS: str = "switch-to-pbs-tui"
SWITCH_TO_PDM: str = "switch-to-pdm-tui"

MODULE_ORDER: tuple[ModuleName, ...] = ("pve", "ceph", "pbs", "pdm")

_MODULE_TO_SENTINEL: dict[ModuleName, str] = {
    "pve": SWITCH_TO_PVE,
    "ceph": SWITCH_TO_CEPH,
    "pbs": SWITCH_TO_PBS,
    "pdm": SWITCH_TO_PDM,
}

_SENTINEL_TO_MODULE: dict[str, ModuleName] = {v: k for k, v in _MODULE_TO_SENTINEL.items()}

VIEW_SELECT_OPTIONS: tuple[tuple[str, str], ...] = (
    ("PVE", "pve"),
    ("Ceph", "ceph"),
    ("PBS", "pbs"),
    ("PDM", "pdm"),
)


def sentinel_for_module(module: ModuleName) -> str:
    return _MODULE_TO_SENTINEL[module]


def module_for_sentinel(sentinel: object) -> ModuleName | None:
    if not isinstance(sentinel, str):
        return None
    return _SENTINEL_TO_MODULE.get(sentinel)
