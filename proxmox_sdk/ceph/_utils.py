"""Shared response-shaping helpers for the read-only Ceph facade."""

from __future__ import annotations

from typing import Any, Literal


def _unwrap(data: Any) -> Any:
    if isinstance(data, dict) and len(data) == 1 and "data" in data:
        return data["data"]
    return data


def _normalize_list(data: Any, *, dict_mode: Literal["values", "items"] = "values") -> list[Any]:
    data = _unwrap(data)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        if dict_mode == "items":
            return [{"name": key, "value": value} for key, value in data.items()]
        return list(data.values())
    return [data]


__all__ = ["_normalize_list", "_unwrap"]
