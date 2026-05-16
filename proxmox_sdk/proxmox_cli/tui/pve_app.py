"""Proxmox VE (PVE) module TUI: generic path browser seeded on /nodes."""

from __future__ import annotations

from typing import ClassVar

from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_sdk.proxmox_cli.tui.base import (
    ModuleProfile,
    PathBrowserApp,
    PathBrowserRuntime,
    TuiMode,
    force_terminal_cleanup,
)

PVE_INITIAL_PATH = "/nodes"

PVE_PROFILE = ModuleProfile(
    module="pve",
    title="Proxmox VE TUI",
    sub_title="Type a path and press Enter - Use tree or / to search",
    default_initial_path=PVE_INITIAL_PATH,
    tree_root_label="/ (root)",
    tree_seed=(
        ("/nodes", "Nodes"),
        ("/nodes/{node}/qemu", "Virtual Machines"),
        ("/nodes/{node}/lxc", "Containers"),
        ("/cluster", "Cluster"),
        ("/cluster/ceph/status", "Ceph (cluster)"),
        ("/nodes/{node}/ceph", "Ceph (node)"),
        ("/storage", "Storage"),
        ("/access", "Access"),
    ),
)


class PVETuiApp(PathBrowserApp):
    PROFILE: ClassVar[ModuleProfile] = PVE_PROFILE


# Backwards-compatible alias — earlier code and tests import ``ProxmoxTuiApp``.
ProxmoxTuiApp = PVETuiApp


def run_pve_tui(
    bridge: ProxmoxSDKBridge,
    *,
    mode: TuiMode,
    initial_path: str = PVE_INITIAL_PATH,
) -> object:
    """Run the PVE TUI once and return the app's exit result.

    The runner loop in :mod:`proxmox_sdk.proxmox_cli.tui.runner` inspects
    the result to decide whether to swap to another module's TUI.
    """
    app = PVETuiApp(
        bridge=bridge,
        runtime=PathBrowserRuntime(mode=mode, initial_path=initial_path),
    )
    try:
        return app.run()
    finally:
        force_terminal_cleanup()


__all__ = [
    "PVE_INITIAL_PATH",
    "PVE_PROFILE",
    "PVETuiApp",
    "ProxmoxTuiApp",
    "run_pve_tui",
]
