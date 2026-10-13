"""Verify real native OTLP export against an isolated loopback collector."""

from __future__ import annotations

import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from fastapi import Body, FastAPI, WebSocket
from fastapi.testclient import TestClient
from opentelemetry import _logs, metrics, trace
from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import ExportLogsServiceRequest
from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceRequest
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider

payloads: dict[str, list[bytes]] = {}
headers: list[str | None] = []


class Collector(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        payloads.setdefault(self.path, []).append(
            self.rfile.read(int(self.headers["Content-Length"]))
        )
        headers.append(self.headers.get("X-Probe-Token"))
        self.send_response(200)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        pass


mode, factory = sys.argv[1:3]
os.environ["FASTAPI_OTEL_AUTO_CONFIGURE"] = "true"
if mode == "auto-off":
    os.environ["FASTAPI_OTEL_AUTO_CONFIGURE"] = "false"
if mode == "auto-absent":
    os.environ.pop("FASTAPI_OTEL_AUTO_CONFIGURE", None)
os.environ["TESTING"] = "1"
os.environ["PROXMOX_API_MODE"] = "mock"
os.environ["PROXMOX_MOCK_STORE"] = "dict"
server = ThreadingHTTPServer(("127.0.0.1", 0), Collector)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
endpoint = f"http://127.0.0.1:{server.server_port}"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = endpoint
if mode == "absent":
    os.environ.pop("OTEL_EXPORTER_OTLP_ENDPOINT")
os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = "x-probe-token=collector-header-canary"
os.environ["OTEL_SERVICE_NAME"] = "broker-probe"
if mode == "disabled":
    os.environ["OTEL_SDK_DISABLED"] = "true"
if mode == "empty":
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = ""
if mode == "signals":
    os.environ["OTEL_TRACES_EXPORTER"] = "none"
    os.environ["OTEL_LOGS_EXPORTER"] = "none"
    os.environ["OTEL_EXPORTER_OTLP_METRICS_ENDPOINT"] = endpoint + "/custom/metrics"
if mode == "metrics-disabled":
    os.environ["OTEL_METRICS_EXPORTER"] = "none"
if mode == "logs-only":
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = ""
    os.environ["OTEL_EXPORTER_OTLP_LOGS_ENDPOINT"] = endpoint + "/v1/logs"
    os.environ["OTEL_TRACES_EXPORTER"] = "none"
    os.environ["OTEL_METRICS_EXPORTER"] = "none"
if mode == "override":
    os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = endpoint + "/custom/traces"

providers = {}
if mode in {"explicit", "custom"}:
    resource = Resource.create({"service.name": "operator-provider"})
    providers = {
        "tracer_provider": TracerProvider(resource=resource),
        "meter_provider": MeterProvider(resource=resource),
        "logger_provider": LoggerProvider(resource=resource),
    }
    if mode == "custom":
        trace.set_tracer_provider(providers["tracer_provider"])
        metrics.set_meter_provider(providers["meter_provider"])
        _logs.set_logger_provider(providers["logger_provider"])

from proxmox_sdk import telemetry as client_telemetry  # noqa: E402

if mode in {"client-first", "client-only"}:
    client_telemetry._ensure_tracer(True)

if mode == "client-only":
    app = FastAPI(
        telemetry={"tracing": False, "metrics": False, "logs": False, "auto_configure": False}
    )
elif mode == "raw":
    app = FastAPI()
elif factory == "main":
    from proxmox_sdk.main import create_app

    app = create_app(telemetry=providers if mode == "explicit" else None)
elif factory == "pdm":
    from proxmox_sdk.pdm_mock_main import create_pdm_mock_app

    app = create_pdm_mock_app(telemetry=providers if mode == "explicit" else None)
else:
    os.environ["PROXMOX_MOCK_SERVICE"] = factory
    from proxmox_sdk.mock.app import create_mock_app

    app = create_mock_app(telemetry=providers if mode == "explicit" else None)
if mode == "server-first":
    client_telemetry._ensure_tracer(True)


@app.get("/__client")
async def client_request():
    from proxmox_sdk.sdk.api import ProxmoxSDK

    sdk = ProxmoxSDK.mock(otel_enabled=True)
    try:
        return await sdk.nodes.get()
    finally:
        await sdk.close()


@app.get("/__probe/{number}")
def read_number(number: int) -> dict[str, int]:
    return {"number": number}


@app.post("/__body")
def read_body(password: int = Body(embed=True)) -> dict[str, int]:
    return {"password": password}


@app.get("/__failure")
def error() -> None:
    raise RuntimeError("exception-secret-canary")


@app.websocket("/__socket")
async def socket(connection: WebSocket) -> None:
    await connection.accept()
    await connection.send_text("ready")
    await connection.close()


@app.websocket("/__socket_failure")
async def socket_failure(connection: WebSocket) -> None:
    await connection.accept()
    raise RuntimeError("websocket-exception-secret-canary")


def run_http_requests(client: TestClient) -> None:
    assert client.get("/__probe/7").json() == {"number": 7}
    assert client.get("/__probe/invalid").status_code == 422
    assert (
        client.get(
            "/__probe/path-secret-canary?streamToken=query-secret-canary",
            headers={
                "Authorization": "Bearer authorization-secret-canary",
                "Cookie": "session=cookie-secret-canary",
            },
        ).status_code
        == 422
    )
    assert (
        client.post("/__body", json={"password": "validation-body-secret-canary"}).status_code
        == 422
    )
    assert client.get("/__failure").status_code == 500
    if mode in {"client-first", "server-first", "custom", "explicit", "client-only"}:
        assert client.get("/__client").status_code == 200


def run_websocket_requests(client: TestClient) -> None:
    with client.websocket_connect("/__socket") as connection:
        assert connection.receive_text() == "ready"
    try:
        with client.websocket_connect("/__socket_failure") as connection:
            connection.receive_text()
    except RuntimeError as exc:
        assert str(exc) == "websocket-exception-secret-canary"


def run_requests() -> None:
    for _ in range(2):
        with TestClient(app, raise_server_exceptions=False) as client:
            run_http_requests(client)
            run_websocket_requests(client)


def decode_payloads() -> tuple[list, list, set[str], set[str]]:
    specifications = {
        "/v1/traces": (
            ExportTraceServiceRequest,
            "resource_spans",
            "scope_spans",
            "spans",
            "traces",
        ),
        "/custom/traces": (
            ExportTraceServiceRequest,
            "resource_spans",
            "scope_spans",
            "spans",
            "traces",
        ),
        "/v1/metrics": (
            ExportMetricsServiceRequest,
            "resource_metrics",
            "scope_metrics",
            "metrics",
            "metrics",
        ),
        "/custom/metrics": (
            ExportMetricsServiceRequest,
            "resource_metrics",
            "scope_metrics",
            "metrics",
            "metrics",
        ),
        "/v1/logs": (
            ExportLogsServiceRequest,
            "resource_logs",
            "scope_logs",
            "log_records",
            "logs",
        ),
    }
    records: dict[str, list] = {"traces": [], "metrics": [], "logs": []}
    resource_names: set[str] = set()
    for path, batches in payloads.items():
        decoder, resource_field, scope_field, record_field, signal = specifications[path]
        for payload in batches:
            decoded = decoder.FromString(payload)
            assert decoded.ListFields()
            for resource in getattr(decoded, resource_field):
                resource_names.update(
                    value.value.string_value
                    for value in resource.resource.attributes
                    if value.key == "service.name"
                )
                for scope in getattr(resource, scope_field):
                    records[signal].extend(getattr(scope, record_field))
    return (
        records["traces"],
        records["logs"],
        {metric.name for metric in records["metrics"]},
        resource_names,
    )


def close_test_providers() -> None:
    """Stop this isolated probe's SDK workers before closing its collector."""
    selected = [
        *providers.values(),
        trace.get_tracer_provider(),
        metrics.get_meter_provider(),
        _logs.get_logger_provider(),
    ]
    native = sys.modules.get("proxmox_sdk.server_telemetry")
    if native is not None:
        selected.append(native._native_provider)
    closed: set[int] = set()
    for provider in selected:
        if isinstance(provider, (TracerProvider, MeterProvider, LoggerProvider)):
            if id(provider) not in closed:
                provider.shutdown()
                closed.add(id(provider))


try:
    run_requests()
    if mode in {"client-first", "server-first", "custom", "explicit", "client-only"}:
        trace.get_tracer_provider().force_flush()
    if mode in {"disabled", "empty", "absent", "auto-off", "auto-absent"}:
        assert not payloads, payloads.keys()
    elif mode == "client-only":
        assert set(payloads) == {"/v1/traces"}
        spans, logs, metric_names, resources = decode_payloads()
        assert len(spans) == 2
        assert all(span.kind == 3 for span in spans)
        assert resources == {"broker-probe"}
        assert not logs and not metric_names
    elif mode == "signals":
        assert set(payloads) == {"/custom/metrics"}, payloads.keys()
        assert "http.server.request.duration" in decode_payloads()[2]
    elif mode == "metrics-disabled":
        assert set(payloads) == {"/v1/traces", "/v1/logs"}, payloads.keys()
        assert decode_payloads()[0]
        assert decode_payloads()[1]
        assert not decode_payloads()[2]
    elif mode == "logs-only":
        assert set(payloads) == {"/v1/logs"}, payloads.keys()
        assert decode_payloads()[1]
        assert b"exception-secret-canary" not in b"".join(payloads["/v1/logs"])
    else:
        trace_path = "/custom/traces" if mode == "override" else "/v1/traces"
        assert set(payloads) == {trace_path, "/v1/logs", "/v1/metrics"}, payloads.keys()
        spans, logs, metric_names, resource_names = decode_payloads()
        expected_resources = {"operator-provider"} if providers else {"broker-probe"}
        if mode == "explicit":
            expected_resources.add("broker-probe")
        assert resource_names == expected_resources
        assert sum(span.name == "GET /__probe/{number}" for span in spans) == 6
        assert sum(span.name == "WS /__socket" for span in spans) == 2
        assert sum(span.name == "WS /__socket_failure" for span in spans) == 2
        assert "http.server.request.duration" in metric_names
        assert len(logs) == 10, len(logs)
        assert any(record.event_name == "fastapi.validation.failed" for record in logs)
        assert any(record.event_name == "fastapi.websocket.exception" for record in logs)
        assert any(
            attribute.key == "exception.type" for record in logs for attribute in record.attributes
        )
        exported = b"".join(payload for batches in payloads.values() for payload in batches)
        for canary in [
            b"authorization-secret-canary",
            b"cookie-secret-canary",
            b"validation-body-secret-canary",
            b"collector-header-canary",
        ]:
            assert canary not in exported
        for canary in [
            b"path-secret-canary",
            b"query-secret-canary",
            b"exception-secret-canary",
            b"websocket-exception-secret-canary",
        ]:
            assert (canary in exported) is (mode == "raw"), canary
        if mode in {"client-first", "server-first", "custom", "explicit", "client-only"}:
            client_spans = [span for span in spans if span.kind == 3]
            assert len(client_spans) == 2, [(s.name, s.kind) for s in spans]
            server_spans = [s for s in spans if s.name == "GET /__client"]
            assert len(server_spans) == 2
            assert {s.trace_id for s in client_spans} == {s.trace_id for s in server_spans}
            assert all(any(s.span_id == c.parent_span_id for s in spans) for c in client_spans)
        if mode == "custom":
            assert trace.get_tracer_provider() is providers["tracer_provider"]
            assert metrics.get_meter_provider() is providers["meter_provider"]
            assert _logs.get_logger_provider() is providers["logger_provider"]
        if providers:
            with (
                providers["tracer_provider"]
                .get_tracer("ownership-probe")
                .start_as_current_span("still-owned") as span
            ):
                assert span.is_recording()
    assert all(value == "collector-header-canary" for value in headers)
finally:
    close_test_providers()
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)
    assert not thread.is_alive()
print(f"Native actual OTLP signals, privacy, and lifecycle verified: {factory} {mode}")
