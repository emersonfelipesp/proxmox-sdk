"""Ceph monitor, manager, and MDS commands."""

from __future__ import annotations

from typing import Optional

import typer

from ._common import _run_get


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


def register(ceph_app: typer.Typer) -> None:
    ceph_app.command("monitors")(monitors)
    ceph_app.command("managers")(managers)
    ceph_app.command("mds")(mds)
