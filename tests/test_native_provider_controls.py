"""Fresh-process native provider controls and selected-provider privacy contracts."""

import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "mode",
    [
        "disabled-flags",
        "auto",
        "none",
        "empty",
        "absent",
        "trace-off",
        "logs-off",
        "metrics-off",
        "fallback",
        "caller",
        "global-caller",
        "client",
        "explicit-client",
        "callbacks",
    ],
)
def test_native_provider_controls(mode: str) -> None:
    """Exercise real application lifespan in an isolated process."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("OTEL_")}
    env.pop("NETBOX_TOKEN", None)
    env.pop("NETBOX_URL", None)
    result = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("native_provider_controls_probe.py")), mode],
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"verified: {mode}" in result.stdout


@pytest.mark.parametrize("selection", ["explicit", "global", "raw"])
def test_empty_caller_loopback_export(selection: str) -> None:
    """Decode actual HTTP/WebSocket signal exports with manual caller ownership."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("OTEL_")}
    env.pop("NETBOX_TOKEN", None)
    env.pop("NETBOX_URL", None)
    result = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("native_empty_caller_probe.py")), selection],
        env=env,
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert f"verified: empty caller {selection}" in result.stdout


@pytest.mark.parametrize("automatic", ["yes", "on", "1", " true ", "TRUE"])
def test_native_automatic_predicate_preserves_proxy_eligibility(automatic: str) -> None:
    """Match native parsing before allocating any implicit server providers."""
    program = """
import os
from fastapi import FastAPI
from opentelemetry import _logs, trace
from opentelemetry._logs._internal import ProxyLoggerProvider
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.trace import TracerProvider
from proxmox_sdk.server_telemetry import native_server_configuration
before_trace = trace.get_tracer_provider()
before_logs = _logs.get_logger_provider()
assert isinstance(before_trace, trace.ProxyTracerProvider)
assert isinstance(before_logs, ProxyLoggerProvider)
configuration = native_server_configuration()
app = FastAPI(telemetry=configuration)
expected = os.environ["FASTAPI_OTEL_AUTO_CONFIGURE"].lower() == "true"
assert app._telemetry["auto_configure"] is expected
if expected:
    assert isinstance(configuration["tracer_provider"], TracerProvider)
    assert isinstance(_logs.get_logger_provider(), LoggerProvider)
else:
    assert configuration["tracer_provider"] is before_trace
    assert trace.get_tracer_provider() is before_trace
    assert _logs.get_logger_provider() is before_logs
print("native predicate and provider allocation verified")
"""
    environment = {
        key: value
        for key, value in os.environ.items()
        if not key.startswith(("OTEL_", "FASTAPI_OTEL_", "PROXMOX_OTEL_"))
    }
    environment["FASTAPI_OTEL_AUTO_CONFIGURE"] = automatic
    environment["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://127.0.0.1:1"
    result = subprocess.run(
        [sys.executable, "-c", program],
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "native predicate and provider allocation verified" in result.stdout
