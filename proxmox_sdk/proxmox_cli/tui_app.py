"""Backwards-compatible shim — the PVE TUI lives in :mod:`proxmox_cli.tui.pve_app`.

Previously this module hosted ``ProxmoxTuiApp`` and ``run_proxmox_tui`` directly.
That code has been split into per-module TUIs under ``proxmox_cli.tui`` to enable
in-app view switching (PVE ↔ Ceph ↔ PBS ↔ PDM). The names below are preserved as
aliases so existing imports and tests keep working.
"""

from __future__ import annotations

from proxmox_sdk.proxmox_cli.tui.base import (
    PathBrowserRuntime as TuiRuntime,
)
from proxmox_sdk.proxmox_cli.tui.base import (
    PathNode,
)
from proxmox_sdk.proxmox_cli.tui.pve_app import (
    PVETuiApp as ProxmoxTuiApp,
)
from proxmox_sdk.proxmox_cli.tui.pve_app import (
    run_pve_tui as run_proxmox_tui,
)

__all__ = ["ProxmoxTuiApp", "PathNode", "TuiRuntime", "run_proxmox_tui"]
