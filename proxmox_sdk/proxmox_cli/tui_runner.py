"""Runtime launcher for Textual TUI.

Delegates to :mod:`proxmox_sdk.proxmox_cli.tui.runner` so the user can switch
between module TUIs (PVE / Ceph / PBS / PDM) without restarting the process.
"""

from __future__ import annotations

from typing import Literal

from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge

TuiMode = Literal["production", "mock"]
ModuleName = Literal["pve", "ceph", "pbs", "pdm"]


def launch_tui(
    bridge: ProxmoxSDKBridge,
    *,
    mode: TuiMode,
    initial_path: str = "/nodes",
    initial_module: ModuleName = "pve",
) -> None:
    """Launch the Textual TUI and surface dependency errors with clear guidance.

    Keeps the legacy ``(bridge, mode, initial_path)`` signature so existing CLI
    commands and tests don't need to change; the optional ``initial_module``
    selects which module's TUI opens first when the user can switch in-app.
    """
    try:
        from proxmox_sdk.proxmox_cli.tui.runner import run_module_tui
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "Textual dependency is missing. Install CLI extras: pip install proxmox-sdk[cli]"
            ) from exc
        raise

    run_module_tui(
        bridge=bridge,
        mode=mode,
        initial_module=initial_module,
        initial_path=initial_path,
    )
