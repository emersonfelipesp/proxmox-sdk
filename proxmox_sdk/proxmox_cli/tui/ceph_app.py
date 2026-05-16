"""Ceph module TUI: path browser seeded on /cluster/ceph/status."""

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

CEPH_INITIAL_PATH = "/cluster/ceph/status"

CEPH_PROFILE = ModuleProfile(
    module="ceph",
    title="Proxmox Ceph TUI",
    sub_title="Browse Ceph cluster and node paths — type a path and press Enter",
    default_initial_path=CEPH_INITIAL_PATH,
    tree_root_label="/ (ceph)",
    tree_seed=(
        ("/cluster/ceph", "Cluster Ceph"),
        ("/cluster/ceph/status", "Ceph Status"),
        ("/cluster/ceph/flags", "Ceph Flags"),
        ("/cluster/ceph/metadata", "Ceph Metadata"),
        ("/nodes/{node}/ceph", "Node Ceph"),
        ("/nodes/{node}/ceph/osd", "OSDs"),
        ("/nodes/{node}/ceph/mon", "Monitors"),
        ("/nodes/{node}/ceph/mgr", "Managers"),
        ("/nodes/{node}/ceph/pool", "Pools"),
    ),
)


class CephTuiApp(PathBrowserApp):
    PROFILE: ClassVar[ModuleProfile] = CEPH_PROFILE


def run_ceph_tui(
    bridge: ProxmoxSDKBridge,
    *,
    mode: TuiMode,
    initial_path: str = CEPH_INITIAL_PATH,
) -> object:
    app = CephTuiApp(
        bridge=bridge,
        runtime=PathBrowserRuntime(mode=mode, initial_path=initial_path),
    )
    try:
        return app.run()
    finally:
        force_terminal_cleanup()


__all__ = ["CEPH_INITIAL_PATH", "CEPH_PROFILE", "CephTuiApp", "run_ceph_tui"]
