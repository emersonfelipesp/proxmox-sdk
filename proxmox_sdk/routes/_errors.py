"""Decorator that translates uncaught exceptions in route closures.

The generated mock and real-proxy route factories both wrap their endpoint
bodies in the same shape of try/except: re-raise framework errors, otherwise
wrap the exception in :class:`ProxmoxOpenAPIException`. This module centralises
that pattern.

Compared to the previous inline blocks, two semantics are made explicit:

1. :class:`ProxmoxOpenAPIException` raised inside the body is re-raised
   verbatim — the previous real-route code re-wrapped it because it relied on
   a duck-typed ``hasattr(error, "status_code")`` check that fails for plain
   :class:`Exception` subclasses. The decorator now lists the pass-through
   classes explicitly.
2. The original Python error is always attached to the wrapped exception as
   ``python_exception=str(error)`` so the raw error text is preserved even
   when ``detail`` is set to a fixed description.
"""

from __future__ import annotations

import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from fastapi import HTTPException

from proxmox_sdk.exception import ProxmoxOpenAPIException

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def with_error_translation(
    method: str,
    path_template: str,
    *,
    message_prefix: str,
    detail: str | None = None,
) -> Callable[[F], F]:
    """Wrap *func* so uncaught exceptions surface as ``ProxmoxOpenAPIException``.

    Args:
        method: HTTP method recorded in the wrapped error message.
        path_template: Path template recorded in the wrapped error message.
        message_prefix: Human-readable description of the failing operation
            (e.g. ``"Proxmox API request"`` or ``"Generated Proxmox mock route"``).
        detail: Optional fixed detail string. The raw Python exception text is
            always attached via ``python_exception=str(error)``.
    """

    def _decorator(func: F) -> F:
        @functools.wraps(func)
        async def _wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return await func(*args, **kwargs)
            except (HTTPException, ProxmoxOpenAPIException):
                raise
            except Exception as error:
                raise ProxmoxOpenAPIException(
                    message=f"{message_prefix} failed for {method} {path_template}",
                    detail=detail,
                    python_exception=str(error),
                ) from error

        return _wrapper  # type: ignore[return-value]

    return _decorator


__all__ = ["with_error_translation"]
