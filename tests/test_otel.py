"""Offline tests for optional OpenTelemetry tracing."""

from __future__ import annotations

import asyncio
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _install_span_exporter(monkeypatch: pytest.MonkeyPatch) -> tuple[Any, Any]:
    pytest.importorskip("opentelemetry.sdk.trace")

    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
    from opentelemetry.trace import SpanKind

    monkeypatch.setenv("PROXMOX_OTEL_ENABLED", "true")
    monkeypatch.setenv("OTEL_TRACES_EXPORTER", "none")
    monkeypatch.delenv("OTEL_SDK_DISABLED", raising=False)

    import proxmox_sdk.telemetry as telemetry

    monkeypatch.setattr(telemetry, "_TRACER", None)
    monkeypatch.setattr(telemetry, "_OTEL_IMPORT_FAILED", False)

    provider = trace.get_tracer_provider()
    if provider.__class__.__name__ == "ProxyTracerProvider":
        provider = TracerProvider()
        trace.set_tracer_provider(provider)

    add_span_processor = getattr(provider, "add_span_processor", None)
    if not callable(add_span_processor):
        pytest.skip("global OpenTelemetry provider does not accept span processors")

    exporter = InMemorySpanExporter()
    add_span_processor(SimpleSpanProcessor(exporter))
    return exporter, SpanKind


def _run_python(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-c", script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_sync_mock_request_emits_one_client_span(monkeypatch: pytest.MonkeyPatch) -> None:
    exporter, span_kind = _install_span_exporter(monkeypatch)

    from proxmox_sdk.sdk.api import ProxmoxSDK

    sdk = ProxmoxSDK.sync_mock()
    try:
        sdk.nodes.get()
    finally:
        sdk.close()

    client_spans = [span for span in exporter.get_finished_spans() if span.kind == span_kind.CLIENT]
    assert len(client_spans) == 1
    span = client_spans[0]
    assert span.name == "proxmox GET"
    assert span.attributes["http.request.method"] == "GET"
    assert span.attributes["url.path"] == "/api2/json/nodes"
    assert span.attributes["proxmox.backend"] == "mock"
    assert span.attributes["proxmox.service"] == "PVE"


def test_tracing_backend_preserves_ticket_capability(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_span_exporter(monkeypatch)

    from proxmox_sdk.sdk.api import ProxmoxSDK
    from proxmox_sdk.sdk.backends.base import TicketCapableBackend
    from proxmox_sdk.telemetry import TracingBackend

    mock_sdk = ProxmoxSDK.mock()
    https_sdk = ProxmoxSDK(
        host="pve.example.com",
        user="root@pam",
        token_name="cli",
        token_value="token-secret",
    )
    try:
        assert isinstance(mock_sdk._backend, TracingBackend)
        assert not isinstance(mock_sdk._backend, TicketCapableBackend)
        assert not hasattr(mock_sdk._backend, "get_tokens")

        assert isinstance(https_sdk._backend, TracingBackend)
        assert isinstance(https_sdk._backend, TicketCapableBackend)
        assert hasattr(https_sdk._backend, "get_tokens")
    finally:
        asyncio.run(mock_sdk.close())
        asyncio.run(https_sdk.close())


def test_fastapi_request_emits_server_span(monkeypatch: pytest.MonkeyPatch) -> None:
    exporter, span_kind = _install_span_exporter(monkeypatch)
    monkeypatch.setenv("TESTING", "1")
    monkeypatch.setenv("PROXMOX_API_MODE", "mock")
    monkeypatch.setenv("PROXMOX_MOCK_STORE", "dict")

    from fastapi.testclient import TestClient

    from proxmox_sdk.main import create_app

    app = create_app()
    exporter.clear()

    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert any(span.kind == span_kind.SERVER for span in exporter.get_finished_spans())


def test_disabled_tracing_emits_zero_spans(monkeypatch: pytest.MonkeyPatch) -> None:
    exporter, _ = _install_span_exporter(monkeypatch)
    monkeypatch.delenv("PROXMOX_OTEL_ENABLED", raising=False)
    exporter.clear()

    from proxmox_sdk.sdk.api import ProxmoxSDK

    sdk = ProxmoxSDK.sync_mock()
    try:
        sdk.nodes.get()
    finally:
        sdk.close()

    assert exporter.get_finished_spans() == ()


def test_enabled_tracing_without_otel_imports_raises_nothing() -> None:
    script = """
import asyncio
import builtins
import os
from typing import Any

os.environ["PROXMOX_OTEL_ENABLED"] = "1"

real_import = builtins.__import__

def blocked_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == "opentelemetry" or name.startswith("opentelemetry."):
        raise ImportError("blocked optional OpenTelemetry import")
    return real_import(name, globals, locals, fromlist, level)

builtins.__import__ = blocked_import

from proxmox_sdk.sdk.backends.base import AbstractBackend
from proxmox_sdk.telemetry import TracingBackend

class Backend(AbstractBackend):
    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        return {"ok": True}

    async def close(self) -> None:
        return None

async def main() -> None:
    backend = TracingBackend(Backend(), backend_name="custom", service_name="PVE")
    assert await backend.request("GET", "/api2/json/nodes") == {"ok": True}
    await backend.close()

asyncio.run(main())
print("ok")
"""
    result = _run_python(script)

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "ok"


def test_base_import_does_not_import_opentelemetry() -> None:
    script = """
import sys
import proxmox_sdk

loaded = any(name == "opentelemetry" or name.startswith("opentelemetry.") for name in sys.modules)
print(loaded)
"""
    result = _run_python(script)

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "False"


def test_span_data_excludes_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    exporter, _ = _install_span_exporter(monkeypatch)

    from proxmox_sdk.sdk.api import ProxmoxSDK
    from proxmox_sdk.sdk.backends.base import AbstractBackend

    secret_values = (
        "secret-password-value",
        "secret-token-value",
        "secret-ticket-value",
        "secret-csrf-value",
    )

    class FailingBackend(AbstractBackend):
        async def request(
            self,
            method: str,
            path: str,
            *,
            params: dict[str, Any] | None = None,
            data: dict[str, Any] | None = None,
        ) -> Any:
            raise RuntimeError(secret_values[0])

        async def close(self) -> None:
            return None

    sdk = ProxmoxSDK(_backend=FailingBackend(), otel_enabled=True)
    try:
        with pytest.raises(RuntimeError):
            asyncio.run(
                sdk.nodes.post(
                    password=secret_values[0],
                    token_value=secret_values[1],
                    PVEAuthCookie=secret_values[2],
                    CSRFPreventionToken=secret_values[3],
                )
            )

        for span in exporter.get_finished_spans():
            values = list(span.attributes.values())
            for event in span.events:
                values.extend((event.attributes or {}).values())
            joined = "\n".join(str(value) for value in values)
            for secret in secret_values:
                assert secret not in joined
    finally:
        asyncio.run(sdk.close())
