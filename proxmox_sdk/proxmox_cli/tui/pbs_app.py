"""Proxmox Backup Server (PBS) module TUI: path browser seeded on PBS roots.

Initial scaffolding follows the PVE/Ceph pattern — the same generic path
browser with PBS-specific seed paths and labels. PBS-specific widgets
(datastore browser, job history, GC dashboard) are a follow-up.
"""

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

PBS_INITIAL_PATH = "/admin/datastore"

PBS_PROFILE = ModuleProfile(
    module="pbs",
    title="Proxmox Backup Server TUI",
    sub_title="Browse PBS resources — type a path and press Enter",
    default_initial_path=PBS_INITIAL_PATH,
    tree_root_label="/ (pbs)",
    tree_seed=(
        ("/admin/datastore", "Datastores"),
        ("/admin/sync", "Sync Jobs"),
        ("/admin/verify", "Verify Jobs"),
        ("/admin/gc", "Garbage Collection"),
        ("/admin/prune", "Prune Jobs"),
        ("/nodes", "Nodes"),
        ("/access", "Access"),
        ("/config", "Config"),
    ),
)


class PBSTuiApp(PathBrowserApp):
    PROFILE: ClassVar[ModuleProfile] = PBS_PROFILE


def run_pbs_tui(
    bridge: ProxmoxSDKBridge,
    *,
    mode: TuiMode,
    initial_path: str = PBS_INITIAL_PATH,
) -> object:
    app = PBSTuiApp(
        bridge=bridge,
        runtime=PathBrowserRuntime(mode=mode, initial_path=initial_path),
    )
    try:
        return app.run()
    finally:
        force_terminal_cleanup()


__all__ = ["PBS_INITIAL_PATH", "PBS_PROFILE", "PBSTuiApp", "run_pbs_tui"]
