"""Tests for `proxmox_sdk.proxmox_cli.decorators.cli_error_handler`."""

from __future__ import annotations

import pytest
import typer

from proxmox_sdk.proxmox_cli.decorators import cli_error_handler
from proxmox_sdk.proxmox_cli.exceptions import (
    AuthenticationError,
    BackendError,
    ProxmoxCLIError,
)


def test_passes_through_return_value() -> None:
    @cli_error_handler
    def cmd() -> str:
        return "ok"

    assert cmd() == "ok"


def test_typer_exit_propagates_unchanged() -> None:
    @cli_error_handler
    def cmd() -> None:
        raise typer.Exit(code=7)

    with pytest.raises(typer.Exit) as exc_info:
        cmd()
    assert exc_info.value.exit_code == 7


def test_proxmox_cli_error_maps_to_typer_exit_with_message(capsys) -> None:
    @cli_error_handler
    def cmd() -> None:
        raise ProxmoxCLIError("something broke", exit_code=5)

    with pytest.raises(typer.Exit) as exc_info:
        cmd()
    assert exc_info.value.exit_code == 5
    err = capsys.readouterr().err
    assert "Error: something broke" in err


def test_subclassed_proxmox_cli_error_preserves_exit_code(capsys) -> None:
    @cli_error_handler
    def cmd() -> None:
        raise AuthenticationError("bad token")

    with pytest.raises(typer.Exit) as exc_info:
        cmd()
    assert exc_info.value.exit_code == 3
    err = capsys.readouterr().err
    assert "Authentication failed: bad token" in err


def test_backend_error_preserves_exit_code(capsys) -> None:
    @cli_error_handler
    def cmd() -> None:
        raise BackendError("unreachable", backend="https")

    with pytest.raises(typer.Exit) as exc_info:
        cmd()
    assert exc_info.value.exit_code == 4
    err = capsys.readouterr().err
    assert "Backend error (https): unreachable" in err


def test_unknown_exception_maps_to_exit_code_1(capsys) -> None:
    @cli_error_handler
    def cmd() -> None:
        raise RuntimeError("unexpected")

    with pytest.raises(typer.Exit) as exc_info:
        cmd()
    assert exc_info.value.exit_code == 1
    err = capsys.readouterr().err
    assert "Error: unexpected" in err


def test_wrapper_preserves_function_metadata() -> None:
    @cli_error_handler
    def my_command(path: str) -> str:
        """Original docstring."""
        return path

    assert my_command.__name__ == "my_command"
    assert my_command.__doc__ == "Original docstring."
    assert my_command("foo") == "foo"
