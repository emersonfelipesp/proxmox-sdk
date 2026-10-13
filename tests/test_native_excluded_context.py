"""Real shipping factories preserve native context across excluded nested requests."""

from typing import Any

import httpx
import pytest
from fastapi import FastAPI
from fastapi.telemetry import get_telemetry_data
from fastapi.testclient import TestClient
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter


def shipping_factory(factory: str, telemetry: dict[str, Any]) -> FastAPI:
    """Select the actual public factory without contacting a managed service."""
    if factory == "main":
        from proxmox_sdk.main import create_app

        return create_app(telemetry=telemetry)
    if factory == "pdm":
        from proxmox_sdk.pdm_mock_main import create_pdm_mock_app

        return create_pdm_mock_app(telemetry=telemetry)
    from proxmox_sdk.mock.app import create_mock_app

    return create_mock_app(telemetry=telemetry)


def exclude_nested(scope: dict[str, Any]) -> bool:
    """Exclude the nested native request while leaving its caller observable."""
    return scope["path"].startswith("/__nested")


def nested_routes(app: FastAPI, observations: list[Any]) -> None:
    """Observe both ordinary and exceptional excluded endpoint execution."""

    @app.get("/__nested/normal")
    async def normal() -> dict[str, bool]:
        observations.append(get_telemetry_data())
        return {"complete": True}

    @app.get("/__nested/error")
    async def failure() -> None:
        observations.append(get_telemetry_data())
        raise RuntimeError("excluded-nested-error-canary")


def outer_route(app: FastAPI, nested: FastAPI, checks: list[dict[str, Any]]) -> None:
    """Call the excluded application in the active real native request context."""

    @app.get("/__outer/{mode}")
    async def outer(mode: str) -> dict[str, int]:
        before = get_telemetry_data()
        transport = httpx.ASGITransport(app=nested, raise_app_exceptions=False)
        async with httpx.AsyncClient(
            transport=transport, base_url="http://nested.invalid"
        ) as client:
            response = await client.get("/__nested/" + mode)
        checks.append(
            {"before": before, "after": get_telemetry_data(), "status": response.status_code}
        )
        return {"nested_status": response.status_code}


def verify_completed(
    observations: list[Any],
    checks: list[dict[str, Any]],
    provider: TracerProvider,
    exporter: InMemorySpanExporter,
) -> None:
    """Require excluded context restoration, positive native spans and caller ownership."""
    assert observations == [None, None]
    assert all(row["before"] is not None and row["after"] is row["before"] for row in checks)
    assert get_telemetry_data() is None
    assert provider.force_flush()
    spans = exporter.get_finished_spans()
    assert sum(span.name == "GET /__outer/{mode}" for span in spans) == 2
    assert not any("/__nested" in span.name for span in spans)
    with provider.get_tracer("caller-owned").start_as_current_span("after-lifespan") as span:
        assert span.is_recording()


@pytest.mark.parametrize("factory", ("main", "pve", "pbs", "pdm"))
@pytest.mark.parametrize("mode,status", (("normal", 200), ("error", 500)))
def test_shipping_excluded_nested_context(
    factory: str, mode: str, status: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Require real outer spans, nested exclusion, context restoration and caller ownership."""
    monkeypatch.setenv("TESTING", "1")
    monkeypatch.setenv("OTEL_SDK_DISABLED", "false")
    monkeypatch.setenv("PROXMOX_API_MODE", "mock")
    monkeypatch.setenv("PROXMOX_MOCK_STORE", "dict")
    monkeypatch.setenv("PROXMOX_MOCK_SERVICE", factory)
    exporter = InMemorySpanExporter()
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(exporter))
    configuration = {
        "auto_configure": False,
        "tracer_provider": provider,
        "metrics": False,
        "logs": False,
    }
    outer = shipping_factory(factory, configuration)
    nested = shipping_factory(factory, {**configuration, "exclude": exclude_nested})
    observations: list[Any] = []
    checks: list[dict[str, Any]] = []
    nested_routes(nested, observations)
    outer_route(outer, nested, checks)
    try:
        for unused in range(2):
            with TestClient(outer) as client:
                response = client.get("/__outer/" + mode)
                assert response.status_code == 200
                assert response.json() == {"nested_status": status}
        verify_completed(observations, checks, provider, exporter)
    finally:
        provider.shutdown()
