"""PDM access-control commands."""

from __future__ import annotations

from typing import Any, Optional

import typer

from ._bridge import _format_options, _run_request

access_app = typer.Typer(name="access", help="Users, ACL, TFA.", no_args_is_help=True)
access_user_app = typer.Typer(name="user", help="User accounts.", no_args_is_help=True)
access_acl_app = typer.Typer(name="acl", help="Access control entries.", no_args_is_help=True)
access_tfa_app = typer.Typer(name="tfa", help="Two-factor auth.", no_args_is_help=True)

access_app.add_typer(access_user_app, name="user")
access_app.add_typer(access_acl_app, name="acl")
access_app.add_typer(access_tfa_app, name="tfa")


# ---------------------------------------------------------------------------
# Access (users / acl / tfa)
# ---------------------------------------------------------------------------


@access_user_app.command("list")
def user_list(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List PDM users."""
    _run_request(
        "GET",
        "/access/users",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_user_app.command("create")
def user_create(
    userid: str = typer.Argument(..., help="user@realm"),
    comment: Optional[str] = typer.Option(None, "--comment"),
    email: Optional[str] = typer.Option(None, "--email"),
    enable: Optional[bool] = typer.Option(None, "--enable/--disable"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Create a PDM user."""
    params: dict[str, Any] = {"userid": userid}
    if comment is not None:
        params["comment"] = comment
    if email is not None:
        params["email"] = email
    if enable is not None:
        params["enable"] = enable
    _run_request(
        "POST",
        "/access/users",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_user_app.command("update")
def user_update(
    userid: str = typer.Argument(...),
    comment: Optional[str] = typer.Option(None, "--comment"),
    email: Optional[str] = typer.Option(None, "--email"),
    enable: Optional[bool] = typer.Option(None, "--enable/--disable"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Update a PDM user."""
    params: dict[str, Any] = {}
    if comment is not None:
        params["comment"] = comment
    if email is not None:
        params["email"] = email
    if enable is not None:
        params["enable"] = enable
    _run_request(
        "PUT",
        f"/access/users/{userid}",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_user_app.command("delete")
def user_delete(
    userid: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Delete a PDM user."""
    _run_request(
        "DELETE",
        f"/access/users/{userid}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_user_app.command("passwd")
def user_passwd(
    userid: str = typer.Argument(...),
    password: str = typer.Option(..., "--password", prompt=True, hide_input=True),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Change the password of a PDM user."""
    _run_request(
        "PUT",
        f"/access/users/{userid}",
        params={"userid": userid, "password": password},
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_acl_app.command("list")
def acl_list(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List ACL entries."""
    _run_request(
        "GET",
        "/access/acl",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_acl_app.command("update")
def acl_update(
    path: str = typer.Option(..., "--path"),
    roles: str = typer.Option(..., "--roles"),
    users: Optional[str] = typer.Option(None, "--users"),
    groups: Optional[str] = typer.Option(None, "--groups"),
    propagate: Optional[bool] = typer.Option(None, "--propagate/--no-propagate"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Add or update an ACL entry."""
    params: dict[str, Any] = {"path": path, "roles": roles}
    if users is not None:
        params["users"] = users
    if groups is not None:
        params["groups"] = groups
    if propagate is not None:
        params["propagate"] = propagate
    _run_request(
        "PUT",
        "/access/acl",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_acl_app.command("delete")
def acl_delete(
    path: str = typer.Option(..., "--path"),
    roles: str = typer.Option(..., "--roles"),
    users: Optional[str] = typer.Option(None, "--users"),
    groups: Optional[str] = typer.Option(None, "--groups"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Remove an ACL entry."""
    params: dict[str, Any] = {"path": path, "roles": roles, "delete": 1}
    if users is not None:
        params["users"] = users
    if groups is not None:
        params["groups"] = groups
    _run_request(
        "PUT",
        "/access/acl",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_tfa_app.command("list")
def tfa_list(
    userid: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List TFA factors for a user."""
    _run_request(
        "GET",
        f"/access/tfa/{userid}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_tfa_app.command("add")
def tfa_add(
    userid: str = typer.Argument(...),
    type: str = typer.Option(..., "--type", help="totp, webauthn, recovery, …"),
    description: Optional[str] = typer.Option(None, "--description"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Add a TFA factor to a user."""
    params: dict[str, Any] = {"type": type}
    if description is not None:
        params["description"] = description
    _run_request(
        "POST",
        f"/access/tfa/{userid}",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_tfa_app.command("delete")
def tfa_delete(
    userid: str = typer.Argument(...),
    tfa_id: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Remove a TFA factor."""
    _run_request(
        "DELETE",
        f"/access/tfa/{userid}/{tfa_id}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )
