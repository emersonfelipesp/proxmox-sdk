"""Shared response-shaping helpers for read-only SDK facades."""

from __future__ import annotations

from typing import Any, Literal


def unwrap_data(data: Any) -> Any:
    """Unwrap the common Proxmox ``{"data": ...}`` response envelope."""
    if isinstance(data, dict) and len(data) == 1 and "data" in data:
        return data["data"]
    return data


def normalize_list(data: Any, *, dict_mode: Literal["values", "items"] = "values") -> list[Any]:
    """Return a response as a list without leaking transport envelope details.

    ``dict_mode`` controls how dict payloads are flattened:

    - ``"values"`` (default): return ``list(data.values())``.
    - ``"items"``: return ``[{"name": key, "value": value}, ...]``.
    """
    data = unwrap_data(data)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if dict_mode == "items":
            return [{"name": key, "value": value} for key, value in data.items()]
        return list(data.values())
    return [data]


__all__ = ["normalize_list", "unwrap_data"]
