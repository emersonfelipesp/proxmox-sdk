"""Runtime loop that swaps between module TUIs in-process.

Each module's app exits with a ``SWITCH_TO_*`` sentinel when the user picks
a different view from the topbar. :func:`run_module_tui` catches the
sentinel and starts the next module's app reusing the same SDK bridge —
no shell-level relaunch.

Mirrors the netbox-sdk pattern from ``netbox_tui/app.py::run_tui``.
"""

from __future__ import annotations

from typing import Literal

from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_sdk.proxmox_cli.tui.base import PathBrowserRuntime, force_terminal_cleanup
from proxmox_sdk.proxmox_cli.tui.ceph_app import CEPH_INITIAL_PATH, CephTuiApp
from proxmox_sdk.proxmox_cli.tui.chrome import ModuleName, module_for_sentinel
from proxmox_sdk.proxmox_cli.tui.pbs_app import PBS_INITIAL_PATH, PBSTuiApp
from proxmox_sdk.proxmox_cli.tui.pdm_app import PDMTuiApp, PDMTuiRuntime
from proxmox_sdk.proxmox_cli.tui.pve_app import PVE_INITIAL_PATH, PVETuiApp

TuiMode = Literal["production", "mock"]


def _make_app(
    module: ModuleName, bridge: ProxmoxSDKBridge, *, mode: TuiMode, initial_path: str | None
) -> object:
    # Resolve via module globals so tests can monkey-patch the per-module
    # app classes (PVETuiApp / CephTuiApp / PBSTuiApp / PDMTuiApp) on this
    # module without our dispatch holding stale references.
    if module == "pdm":
        return PDMTuiApp(bridge=bridge, runtime=PDMTuiRuntime(mode=mode))
    path_browser_classes: dict[ModuleName, tuple[type, str]] = {
        "pve": (PVETuiApp, PVE_INITIAL_PATH),
        "ceph": (CephTuiApp, CEPH_INITIAL_PATH),
        "pbs": (PBSTuiApp, PBS_INITIAL_PATH),
    }
    app_cls, default_path = path_browser_classes[module]
    path = initial_path or default_path
    return app_cls(bridge=bridge, runtime=PathBrowserRuntime(mode=mode, initial_path=path))


def run_module_tui(
    bridge: ProxmoxSDKBridge,
    *,
    mode: TuiMode,
    initial_module: ModuleName = "pve",
    initial_path: str | None = None,
) -> None:
    """Run module TUIs in a loop, swapping when an app exits with a SWITCH sentinel.

    :param initial_path: only honoured the first time, and only for path-browser
        modules (pve/ceph/pbs). After a view switch, each module starts at its
        own default path. PDM ignores ``initial_path`` entirely.
    """
    current: ModuleName = initial_module
    current_initial_path: str | None = initial_path

    try:
        while True:
            app = _make_app(current, bridge, mode=mode, initial_path=current_initial_path)
            result = app.run()  # type: ignore[attr-defined]
            next_module = module_for_sentinel(result)
            if next_module is None or next_module == current:
                return
            current = next_module
            # After a switch, fall back to the target module's default seed path.
            current_initial_path = None
    finally:
        force_terminal_cleanup()


__all__ = ["run_module_tui"]
