"""CLI decorators for proxmox-sdk Typer commands.

Decorator order convention (outermost first):

    @app.command(...)
    @cli_error_handler
    def my_command(...): ...

`@cli_error_handler` must be the innermost decorator so the Typer command
registration sees the wrapped function (and so `typer.Exit` from inside the
wrapper propagates to Typer's invocation machinery).
"""

from __future__ import annotations

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

import typer

from .exceptions import ProxmoxCLIError

P = ParamSpec("P")
R = TypeVar("R")


def cli_error_handler(func: Callable[P, R]) -> Callable[P, R]:
    """Map raised exceptions to `typer.Exit` with consistent messaging.

    Mapping:
    - `typer.Exit` — re-raised unchanged (already a controlled exit).
    - `ProxmoxCLIError` — `Error: <message>` on stderr, exits with `e.exit_code`.
    - Any other `Exception` — `Error: <exc>` on stderr, exits with code 1.

    Removes the duplicated try/except boilerplate previously copy-pasted
    across every command in `proxmox_cli/commands/`.
    """

    @wraps(func)
    def _wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            return func(*args, **kwargs)
        except typer.Exit:
            raise
        except ProxmoxCLIError as exc:
            typer.echo(f"Error: {exc.message}", err=True)
            raise typer.Exit(code=exc.exit_code) from exc
        except Exception as exc:
            typer.echo(f"Error: {exc}", err=True)
            raise typer.Exit(code=1) from exc

    return _wrapper


__all__ = ["cli_error_handler"]
