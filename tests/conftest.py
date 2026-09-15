"""Global test isolation and deadlock-prevention fixtures."""

from __future__ import annotations

import os
import re
from collections.abc import Mapping, Sequence

import pytest
from _pytest.config import Config
from _pytest.main import Session

pytest_plugins = ["pytester"]

_LIVE_CREDENTIAL_ENV_KEYS = (
    "PROXMOX_API_URL",
    "PROXMOX_API_TOKEN_ID",
    "PROXMOX_API_TOKEN_SECRET",
)

_RECOVERABLE_KEYS = ("PROXMOX_API_TOKEN_SECRET",)

MASKED_SENTINEL = "********"

_LIVE_CREDENTIALS_KEY = pytest.StashKey[dict[str, str]]()


_MARKER_IDENTIFIER = re.compile(r"(?<![\w.])live(?![\w.])")
_NEGATED_LIVE_ONLY = re.compile(r"^\(*\s*not\s+\(*\s*live\s*\)*$")


def live_suite_selected(markexpr: str, args: Sequence[str]) -> bool:
    """Return True when the live test suite is explicitly selected.

    The marker expression is scanned for the identifier ``live`` with token
    boundaries, so ``(live)``, ``live and not slow``, and ``(live) or ceph`` all
    count as a selection while ``live_ceph`` and ``not live`` do not.
    """
    expr = (markexpr or "").strip()
    if expr and _MARKER_IDENTIFIER.search(expr) and not _NEGATED_LIVE_ONLY.match(expr):
        return True
    for arg in args:
        parts = arg.replace("\\", "/").split("/")
        if "tests" in parts:
            idx = parts.index("tests")
            if idx + 1 < len(parts) and parts[idx + 1] == "live":
                return True
    return False


def snapshot_live_credentials(environ: Mapping[str, str]) -> dict[str, str]:
    """Return live-test credential env vars that are currently set."""
    return {key: environ[key] for key in _LIVE_CREDENTIAL_ENV_KEYS if key in environ}


def resolve_live_credentials(
    current: Mapping[str, str],
    snapshot: Mapping[str, str],
) -> dict[str, str]:
    """Resolve live credentials from the current environment and an optional snapshot.

    Only ``PROXMOX_API_TOKEN_SECRET`` is recovered from the snapshot when the
    current value equals ``MASKED_SENTINEL`` (as ``ProxmoxConfig.from_env`` does
    in-process). A deliberately-set sentinel for the secret is indistinguishable
    from that masking and is accepted for this test harness.
    """
    resolved: dict[str, str] = {}
    for key in _LIVE_CREDENTIAL_ENV_KEYS:
        if key not in current:
            continue
        value = current[key]
        if value == MASKED_SENTINEL and key in _RECOVERABLE_KEYS and key in snapshot:
            resolved[key] = snapshot[key]
        else:
            resolved[key] = value
    return resolved


def live_credentials(config: Config) -> dict[str, str]:
    """Return live credentials, recovering snapshot values for masked env vars."""
    snapshot = config.stash.get(_LIVE_CREDENTIALS_KEY, {})
    return resolve_live_credentials(os.environ, snapshot)


def pytest_configure(config: Config) -> None:
    """Keep generated mock state private to each pytest/xdist process."""
    markexpr = config.getoption("markexpr", default="") or ""
    if live_suite_selected(markexpr, config.args):
        config.stash[_LIVE_CREDENTIALS_KEY] = snapshot_live_credentials(os.environ)
    else:
        config.stash[_LIVE_CREDENTIALS_KEY] = {}

    worker = os.environ.get("PYTEST_XDIST_WORKER", "serial")
    base_namespace = os.environ.get("PROXMOX_MOCK_STATE_NAMESPACE", "pytest")
    os.environ["PROXMOX_MOCK_STATE_NAMESPACE"] = f"{base_namespace}_{worker}_{os.getpid()}"
    # Unit tests exercise SQLite explicitly where persistence is the subject.
    # The general HTTP suite needs process-local state so parallel workers can
    # never mutate or wait on the same SQLite database.
    os.environ.setdefault("PROXMOX_MOCK_STORE", "dict")


def pytest_sessionfinish(session: Session) -> None:
    """Drop any captured live credentials before the pytest process exits."""
    session.config.stash[_LIVE_CREDENTIALS_KEY] = {}
