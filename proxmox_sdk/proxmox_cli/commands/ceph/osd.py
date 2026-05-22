"""Ceph OSD, CRUSH rule, and log commands."""

from __future__ import annotations

from typing import Any, Optional

import typer

from ._common import _run_get


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


def register(ceph_app: typer.Typer) -> None:
    ceph_app.command("osds")(osds)
    ceph_app.command("osd")(osd)


def register_tail(ceph_app: typer.Typer) -> None:
    ceph_app.command("rules")(rules)
    ceph_app.command("log")(log_cmd)
