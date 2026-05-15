"""Package version helpers."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

_DIST_NAME = "proxmox-sdk"
_UNKNOWN_VERSION = "0+unknown"
_cached: str | None = None


def get_version() -> str:
    """Return the installed distribution version.

    The source tree previously carried multiple hard-coded version constants,
    which drifted from ``pyproject.toml``. Reading package metadata keeps the
    API, CLI, and FastAPI surfaces aligned with the built distribution.
    """
    global _cached
    if _cached is None:
        try:
            _cached = version(_DIST_NAME)
        except PackageNotFoundError:
            _cached = _UNKNOWN_VERSION
    return _cached


__all__ = ["get_version"]
