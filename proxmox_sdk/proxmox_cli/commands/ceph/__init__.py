"""Ceph subcommand group: read-only browsing of Proxmox Ceph endpoints."""

from __future__ import annotations

from typing import Optional

import typer

from proxmox_sdk.proxmox_cli.app import app
from proxmox_sdk.proxmox_cli.decorators import cli_error_handler
from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_sdk.proxmox_cli.tui_runner import launch_tui

from .._common import build_backend_config
from ._common import _run_get
from .fs import register as register_fs
from .mon import register as register_mon
from .osd import register as register_osd
from .osd import register_tail as register_osd_tail
from .pool import register as register_pool

ceph_app = typer.Typer(
    name="ceph",
    help="Browse Proxmox Ceph cluster, monitors, managers, OSDs, pools, and logs (PVE only, read-only).",
    no_args_is_help=True,
)
app.add_typer(ceph_app, name="ceph")


# ----- Cluster-scoped commands -----


@ceph_app.command("status")
def status(
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json", help="Shortcut for --output json"),
    yaml_output: bool = typer.Option(False, "--yaml", help="Shortcut for --output yaml"),
    markdown_output: bool = typer.Option(
        False, "--markdown", help="Shortcut for --output markdown"
    ),
) -> None:
    """Show Ceph cluster-wide health and status."""
    _run_get(
        "/cluster/ceph/status",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("metadata")
def metadata(
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show Ceph cluster metadata (versions, daemons summary)."""
    _run_get(
        "/cluster/ceph/metadata",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("flags")
def flags(
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List Ceph cluster-wide flags."""
    _run_get(
        "/cluster/ceph/flags",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("flag")
def flag(
    name: str = typer.Argument(..., help="Flag name (e.g. noout, nodown, pause)."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show a single Ceph flag by name."""
    _run_get(
        f"/cluster/ceph/flags/{name}",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


register_mon(ceph_app)
register_osd(ceph_app)
register_pool(ceph_app)
register_fs(ceph_app)
register_osd_tail(ceph_app)


# ----- TUI launcher -----


@ceph_app.command("tui")
@cli_error_handler
def tui(
    ctx: typer.Context,
    mode: Optional[str] = typer.Argument(
        None, help="Optional mode. Use 'mock' to run against the in-memory mock backend."
    ),
    path: str = typer.Option(
        "/cluster/ceph/status",
        "--path",
        "-p",
        help="Initial API path to load (must be a Ceph path).",
    ),
) -> None:
    """Launch the Proxmox TUI rooted on Ceph paths."""
    bridge: ProxmoxSDKBridge | None = None
    try:
        ctx_obj = ctx.obj or {}
        use_mock = mode == "mock"
        backend_cfg = build_backend_config(ctx_obj, use_mock=use_mock, service="PVE")
        bridge = ProxmoxSDKBridge.create(backend_cfg)
        launch_tui(
            bridge=bridge,
            mode="mock" if use_mock else "production",
            initial_path=path,
            initial_module="ceph",
        )
    finally:
        if bridge is not None:
            bridge.close()


__all__ = ["ceph_app"]
