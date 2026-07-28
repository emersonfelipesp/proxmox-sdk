"""Strict response normalization at PDM domain boundaries."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from pydantic import BaseModel, ValidationError

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.pdm.errors import PDMResponseContractError

ModelT = TypeVar("ModelT", bound=BaseModel)

REDACTED_REMOTE_ERROR = "remote reported an error"
_RRD_CONSOLIDATIONS = {"MAX", "AVERAGE"}
_RRD_TIMEFRAMES = {"hour", "day", "week", "month", "year", "decade"}


def require_mapping(data: Any, *, operation: str) -> dict[str, Any]:
    """Return an unwrapped mapping or raise a redacted typed contract error."""

    value = unwrap_data(data)
    if not isinstance(value, Mapping):
        raise PDMResponseContractError(
            operation=operation,
            expected="an object",
            received=value,
        )
    return dict(value)


def require_list(data: Any, *, operation: str) -> list[Any]:
    """Return an unwrapped list without silently coercing other cardinalities."""

    value = unwrap_data(data)
    if not isinstance(value, list):
        raise PDMResponseContractError(
            operation=operation,
            expected="a list",
            received=value,
        )
    return value


def require_string(data: Any, *, operation: str) -> str:
    """Return an unwrapped string or raise a typed contract error."""

    value = unwrap_data(data)
    if not isinstance(value, str):
        raise PDMResponseContractError(
            operation=operation,
            expected="a string",
            received=value,
        )
    return value


def validate_model(
    model: type[ModelT],
    data: Any,
    *,
    operation: str,
) -> ModelT:
    """Validate one response object and translate Pydantic failures."""

    # Models deliberately permit forward-compatible extra fields. Apply the
    # error-field policy at this shared trust boundary so no typed successful
    # response can retain arbitrary upstream diagnostic or credential text.
    payload, _ = redact_optional_error(
        require_mapping(data, operation=operation),
        operation=operation,
    )
    contract_error: PDMResponseContractError | None = None
    try:
        return model.model_validate(payload)
    except ValidationError as exc:
        locations = sorted(
            {
                ".".join(str(segment) for segment in error["loc"])
                for error in exc.errors(include_url=False, include_input=False)
            }
        )
        detail = "invalid fields: " + ", ".join(locations) if locations else "invalid fields"
        contract_error = PDMResponseContractError(
            operation=operation,
            expected=f"a valid {model.__name__} object",
            received=payload,
            detail=detail,
        )

    # Raise outside the ``except`` suite so Python does not retain the raw
    # ValidationError (and its input payload) in ``__context__``.
    raise contract_error


def redact_optional_error(
    data: dict[str, Any],
    *,
    operation: str,
) -> tuple[dict[str, Any], bool]:
    """Validate and replace an optional upstream error with a safe marker."""

    error = data.get("error")
    if error is None:
        return data, False
    if not isinstance(error, str):
        raise PDMResponseContractError(
            operation=operation,
            expected="an optional string error field",
            received=error,
            detail="invalid fields: error",
        )
    redacted = dict(data)
    redacted["error"] = REDACTED_REMOTE_ERROR
    return redacted, True


def validate_rrd_query(timeframe: str, cf: str) -> dict[str, str]:
    """Validate the required captured-schema RRD query parameters."""

    if timeframe not in _RRD_TIMEFRAMES:
        raise ValueError(f"Unsupported PDM RRD timeframe {timeframe!r}")
    if cf not in _RRD_CONSOLIDATIONS:
        raise ValueError(f"Unsupported PDM RRD consolidation {cf!r}")
    return {"timeframe": timeframe, "cf": cf}


def validate_model_list(
    model: type[ModelT],
    data: Any,
    *,
    operation: str,
) -> list[ModelT]:
    """Validate a response list item-by-item with an indexed operation label."""

    items = require_list(data, operation=operation)
    return [
        validate_model(model, item, operation=f"{operation}[{index}]")
        for index, item in enumerate(items)
    ]


__all__ = [
    "REDACTED_REMOTE_ERROR",
    "redact_optional_error",
    "require_list",
    "require_mapping",
    "require_string",
    "validate_rrd_query",
    "validate_model",
    "validate_model_list",
]
