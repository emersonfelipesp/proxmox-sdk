"""Backwards-compatible shim — the PDM TUI lives in :mod:`proxmox_cli.tui.pdm_app`.

Previously this module hosted the PDM TUI classes directly. The code now lives
under ``proxmox_cli.tui`` alongside the other per-module TUIs; the symbols
below are re-exported so existing imports and tests keep working.
"""

from __future__ import annotations

from proxmox_sdk.proxmox_cli.tui.pdm_app import (
    ConfirmModal,
    PDMActionPanel,
    PDMGuestPanel,
    PDMTuiApp,
    PDMTuiRuntime,
    RemoteEntry,
    _add_guest_children,
    _as_list,
    run_pdm_tui,
    run_pdm_tui_once,
)

__all__ = [
    "ConfirmModal",
    "PDMActionPanel",
    "PDMGuestPanel",
    "PDMTuiApp",
    "PDMTuiRuntime",
    "RemoteEntry",
    "_add_guest_children",
    "_as_list",
    "run_pdm_tui",
    "run_pdm_tui_once",
]
