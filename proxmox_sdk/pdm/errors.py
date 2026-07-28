"""Typed failures for PDM response-contract violations."""

from __future__ import annotations

from typing import Any


class PDMResponseContractError(ValueError):
    """Raised when a PDM response cannot satisfy a documented SDK contract.

    The error intentionally reports shape and validation locations without
    interpolating response values, which may contain remote credentials or
    other operator-controlled data.
    """

    def __init__(
        self,
        *,
        operation: str,
        expected: str,
        received: Any,
        detail: str | None = None,
    ) -> None:
        self.operation = operation
        self.expected = expected
        self.received_type = type(received).__name__
        self.detail = detail
        message = (
            f"PDM response contract violation for {operation}: expected {expected}, "
            f"received {self.received_type}"
        )
        if detail:
            message = f"{message} ({detail})"
        super().__init__(message)


__all__ = ["PDMResponseContractError"]
