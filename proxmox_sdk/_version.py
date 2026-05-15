"""Package version helpers."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

_DIST_NAME = "proxmox-sdk"
_UNKNOWN_VERSION = "0+unknown"


def get_version() -> str:
    """Return the installed distribution version.

    The source tree previously carried multiple hard-coded version constants,
    which drifted from ``pyproject.toml``. Reading package metadata keeps the
    API, CLI, and FastAPI surfaces aligned with the built distribution.
    """
    try:
        return version(_DIST_NAME)
    except PackageNotFoundError:
        return _UNKNOWN_VERSION


__all__ = ["get_version"]
