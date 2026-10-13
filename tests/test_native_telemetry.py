"""Actual native export and standalone client coexistence stay offline."""

import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "factory,mode",
    [(factory, "enabled") for factory in ("main", "pve", "pbs", "pdm")]
    + [
        ("pve", mode)
        for mode in (
            "disabled",
            "auto-off",
            "auto-absent",
            "empty",
            "absent",
            "signals",
            "metrics-disabled",
            "logs-only",
            "override",
            "explicit",
            "custom",
            "raw",
            "client-first",
            "server-first",
            "client-only",
        )
    ],
)
def test_native_export_and_provider_coexistence(factory: str, mode: str) -> None:
    """Decode real local exports and require each request span exactly once."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("OTEL_")}
    env.pop("PROXMOX_OTEL_ENABLED", None)
    env.pop("FASTAPI_OTEL_AUTO_CONFIGURE", None)
    result = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("native_telemetry_probe.py")), mode, factory],
        env=env,
        text=True,
        capture_output=True,
        timeout=90,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"verified: {factory} {mode}" in result.stdout
