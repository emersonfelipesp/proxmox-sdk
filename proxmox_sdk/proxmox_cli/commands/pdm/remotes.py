"""PDM remote commands."""

from __future__ import annotations

from typing import Any, Optional

import typer

from ._bridge import _format_options, _run_request

remote_app = typer.Typer(name="remote", help="Manage PDM remotes.", no_args_is_help=True)


# ---------------------------------------------------------------------------
# Remote commands
# ---------------------------------------------------------------------------


@remote_app.command("list")
def remote_list(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List registered PDM remotes."""
    _run_request(
        "GET",
        "/remotes/remote",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@remote_app.command("version")
def remote_version(
    remote: str = typer.Argument(..., help="Remote id."),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Query the version of a registered remote."""
    _run_request(
        "GET",
        f"/remotes/remote/{remote}/version",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@remote_app.command("add")
def remote_add(
    id: str = typer.Argument(..., help="Remote id."),
    type: str = typer.Option(..., "--type", "-t", help="Remote type (pve or pbs)."),
    authid: Optional[str] = typer.Option(None, "--authid"),
    token: Optional[str] = typer.Option(None, "--token"),
    fingerprint: Optional[str] = typer.Option(None, "--fingerprint"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Register a new PVE or PBS remote with PDM."""
    params: dict[str, Any] = {"id": id, "type": type}
    if authid is not None:
        params["authid"] = authid
    if token is not None:
        params["token"] = token
    if fingerprint is not None:
        params["fingerprint"] = fingerprint
    _run_request(
        "POST",
        "/remotes/remote",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@remote_app.command("update")
def remote_update(
    remote: str = typer.Argument(..., help="Remote id."),
    token: Optional[str] = typer.Option(None, "--token"),
    fingerprint: Optional[str] = typer.Option(None, "--fingerprint"),
    authid: Optional[str] = typer.Option(None, "--authid"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Update a registered remote."""
    params: dict[str, Any] = {}
    if token is not None:
        params["token"] = token
    if fingerprint is not None:
        params["fingerprint"] = fingerprint
    if authid is not None:
        params["authid"] = authid
    _run_request(
        "PUT",
        f"/remotes/remote/{remote}",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@remote_app.command("remove")
def remote_remove(
    remote: str = typer.Argument(..., help="Remote id."),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Unregister a remote."""
    _run_request(
        "DELETE",
        f"/remotes/remote/{remote}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )
