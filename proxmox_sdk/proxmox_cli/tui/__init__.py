"""Per-module Textual TUIs for proxmox-sdk with in-app view switching.

Each module (PVE, Ceph, PBS, PDM) exposes its own Textual App. A shared
runtime loop (:mod:`proxmox_sdk.proxmox_cli.tui.runner`) instantiates the
next app whenever the active app exits with a `SWITCH_TO_*` sentinel,
so the user can change the active TUI view without restarting the
process.

Pattern mirrors ``netbox_tui`` (``netbox_tui/chrome.py`` sentinels,
``netbox_tui/app.py::run_tui`` loop, per-app ``view_select`` widget).
"""

from __future__ import annotations

from proxmox_sdk.proxmox_cli.tui.chrome import (
    MODULE_ORDER,
    SWITCH_TO_CEPH,
    SWITCH_TO_PBS,
    SWITCH_TO_PDM,
    SWITCH_TO_PVE,
    VIEW_SELECT_OPTIONS,
    sentinel_for_module,
)
from proxmox_sdk.proxmox_cli.tui.runner import run_module_tui

__all__ = [
    "MODULE_ORDER",
    "SWITCH_TO_CEPH",
    "SWITCH_TO_PBS",
    "SWITCH_TO_PDM",
    "SWITCH_TO_PVE",
    "VIEW_SELECT_OPTIONS",
    "run_module_tui",
    "sentinel_for_module",
]
