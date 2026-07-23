"""Global test isolation and deadlock-prevention fixtures."""

from __future__ import annotations

import os


def pytest_configure() -> None:
    """Keep generated mock state private to each pytest/xdist process."""

    worker = os.environ.get("PYTEST_XDIST_WORKER", "serial")
    base_namespace = os.environ.get("PROXMOX_MOCK_STATE_NAMESPACE", "pytest")
    os.environ["PROXMOX_MOCK_STATE_NAMESPACE"] = f"{base_namespace}_{worker}_{os.getpid()}"
    # Unit tests exercise SQLite explicitly where persistence is the subject.
    # The general HTTP suite needs process-local state so parallel workers can
    # never mutate or wait on the same SQLite database.
    os.environ.setdefault("PROXMOX_MOCK_STORE", "dict")
