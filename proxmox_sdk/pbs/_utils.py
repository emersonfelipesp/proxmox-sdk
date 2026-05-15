"""Shared response-shaping helpers for the read-only PBS facade."""

from __future__ import annotations

from typing import Any


def unwrap_data(data: Any) -> Any:
    """Unwrap the common PBS ``{"data": ...}`` response envelope."""
    if isinstance(data, dict) and len(data) == 1 and "data" in data:
        return data["data"]
    return data


def normalize_list(data: Any) -> list[Any]:
    """Return a response as a list without leaking transport envelope details."""
    data = unwrap_data(data)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    return [data]


__all__ = ["normalize_list", "unwrap_data"]
