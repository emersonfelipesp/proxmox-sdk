"""Ceph pool commands."""

from __future__ import annotations

from typing import Optional

import typer

from ._common import _run_get


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


def register(ceph_app: typer.Typer) -> None:
    ceph_app.command("pools")(pools)
    ceph_app.command("pool")(pool)
