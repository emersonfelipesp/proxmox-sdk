"""Ceph subcommand group: read-only browsing of Proxmox Ceph endpoints."""

from __future__ import annotations

import logging
from typing import Any, Optional

import typer

from proxmox_sdk.proxmox_cli.app import app
from proxmox_sdk.proxmox_cli.decorators import cli_error_handler
from proxmox_sdk.proxmox_cli.output import get_context_options
from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_sdk.proxmox_cli.tui_runner import launch_tui

from ._common import build_backend_config, create_formatter, ensure_service, prepare_command

logger = logging.getLogger(__name__)

ceph_app = typer.Typer(
    name="ceph",
    help="Browse Proxmox Ceph cluster, monitors, managers, OSDs, pools, and logs (PVE only, read-only).",
    no_args_is_help=True,
)
app.add_typer(ceph_app, name="ceph")


@cli_error_handler
def _run_get(
    path: str,
    *,
    params: dict[str, Any] | None,
    output: Optional[str],
    json_output: bool,
    yaml_output: bool,
    markdown_output: bool,
) -> None:
    ctx_obj = get_context_options()
    config_mgr, bridge = prepare_command(ctx_obj)
    try:
        ensure_service(bridge, "PVE")
        formatter = create_formatter(
            config_mgr,
            output,
            json_output=json_output,
            yaml_output=yaml_output,
            markdown_output=markdown_output,
            ctx_obj=ctx_obj,
        )
        result = bridge.get(path, params=params)
        formatter.print_output(result)
    finally:
        bridge.close()


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


# ----- Node-scoped commands -----


@ceph_app.command("monitors")
def monitors(
    node: str = typer.Argument(..., help="Proxmox node name."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List Ceph monitors on a node."""
    _run_get(
        f"/nodes/{node}/ceph/mon",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("managers")
def managers(
    node: str = typer.Argument(..., help="Proxmox node name."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List Ceph managers on a node."""
    _run_get(
        f"/nodes/{node}/ceph/mgr",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("mds")
def mds(
    node: str = typer.Argument(..., help="Proxmox node name."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List Ceph metadata servers on a node."""
    _run_get(
        f"/nodes/{node}/ceph/mds",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("osds")
def osds(
    node: str = typer.Argument(..., help="Proxmox node name."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List Ceph OSDs on a node."""
    _run_get(
        f"/nodes/{node}/ceph/osd",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("osd")
def osd(
    node: str = typer.Argument(..., help="Proxmox node name."),
    osdid: str = typer.Argument(..., help="OSD id (numeric)."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show a single Ceph OSD on a node."""
    _run_get(
        f"/nodes/{node}/ceph/osd/{osdid}",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("pools")
def pools(
    node: str = typer.Argument(..., help="Proxmox node name."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List Ceph pools on a node."""
    _run_get(
        f"/nodes/{node}/ceph/pool",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("pool")
def pool(
    node: str = typer.Argument(..., help="Proxmox node name."),
    name: str = typer.Argument(..., help="Pool name."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show a single Ceph pool on a node."""
    _run_get(
        f"/nodes/{node}/ceph/pool/{name}",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("fs")
def fs(
    node: str = typer.Argument(..., help="Proxmox node name."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List CephFS filesystems on a node."""
    _run_get(
        f"/nodes/{node}/ceph/fs",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("rules")
def rules(
    node: str = typer.Argument(..., help="Proxmox node name."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List CRUSH rules on a node."""
    _run_get(
        f"/nodes/{node}/ceph/rules",
        params=None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


@ceph_app.command("log")
def log_cmd(
    node: str = typer.Argument(..., help="Proxmox node name."),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Max log lines to return."),
    start: Optional[int] = typer.Option(None, "--start", help="Starting offset (0-based)."),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output format."),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show recent Ceph log lines on a node."""
    params: dict[str, Any] = {}
    if limit is not None:
        params["limit"] = limit
    if start is not None:
        params["start"] = start
    _run_get(
        f"/nodes/{node}/ceph/log",
        params=params or None,
        output=output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
    )


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
