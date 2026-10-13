"""Export native HTTP/WebSocket caller-provider telemetry only to loopback."""

import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from fastapi import FastAPI, WebSocket
from fastapi.testclient import TestClient
from opentelemetry import _logs, metrics, trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.proto.collector.logs.v1.logs_service_pb2 import ExportLogsServiceRequest
from opentelemetry.proto.collector.metrics.v1.metrics_service_pb2 import ExportMetricsServiceRequest
from opentelemetry.proto.collector.trace.v1.trace_service_pb2 import ExportTraceServiceRequest
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import SimpleLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from proxmox_sdk import server_telemetry as native
from proxmox_sdk.mock.app import create_mock_app

payloads = []


class Collector(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        payloads.append((self.path, self.rfile.read(int(self.headers["Content-Length"]))))
        self.send_response(200)
        self.end_headers()

    def log_message(self, format: str, *args: object) -> None:
        pass


server = ThreadingHTTPServer(("127.0.0.1", 0), Collector)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
endpoint = f"http://127.0.0.1:{server.server_port}"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = ""
providers = {
    "tracer_provider": TracerProvider(),
    "meter_provider": MeterProvider(
        metric_readers=[
            PeriodicExportingMetricReader(
                OTLPMetricExporter(endpoint=endpoint + "/v1/metrics"), export_interval_millis=100000
            )
        ]
    ),
    "logger_provider": LoggerProvider(),
}
providers["tracer_provider"].add_span_processor(
    SimpleSpanProcessor(OTLPSpanExporter(endpoint=endpoint + "/v1/traces"))
)
configuration = {**providers, "auto_configure": False}
if sys.argv[1] == "global":
    trace.set_tracer_provider(providers["tracer_provider"])
    metrics.set_meter_provider(providers["meter_provider"])
    _logs.set_logger_provider(providers["logger_provider"])
    configuration = {"auto_configure": False}
app = (
    FastAPI(telemetry=configuration)
    if sys.argv[1] == "raw"
    else create_mock_app(telemetry=configuration)
)
# Caller log exporters follow sanitation registration; trace exporter was first.
providers["logger_provider"].add_log_record_processor(
    SimpleLogRecordProcessor(OTLPLogExporter(endpoint=endpoint + "/v1/logs"))
)


@app.get("/__privacy/{number}")
def number(number: int) -> dict[str, int]:
    return {"number": number}


@app.get("/__privacy_failure")
def failure() -> None:
    raise RuntimeError("exception-secret-canary")


@app.websocket("/__privacy_socket")
async def socket(connection: WebSocket) -> None:
    await connection.accept()
    raise RuntimeError("websocket-secret-canary")


try:
    for _ in range(2):
        with TestClient(app, raise_server_exceptions=False) as client:
            assert (
                client.get("/__privacy/path-secret-canary?token=query-secret-canary").status_code
                == 422
            )
            assert client.get("/__privacy_failure").status_code == 500
            try:
                with client.websocket_connect("/__privacy_socket") as connection:
                    connection.receive_text()
            except RuntimeError as error:
                assert str(error) == "websocket-secret-canary"
    for provider in providers.values():
        assert provider.force_flush()
    assert {path for path, _ in payloads} == {"/v1/traces", "/v1/metrics", "/v1/logs"}
    decoders = {
        "/v1/traces": ExportTraceServiceRequest,
        "/v1/metrics": ExportMetricsServiceRequest,
        "/v1/logs": ExportLogsServiceRequest,
    }
    for path, body in payloads:
        assert decoders[path].FromString(body).ListFields()
    exported = b"".join(body for _, body in payloads)
    for canary in (
        b"path-secret-canary",
        b"query-secret-canary",
        b"exception-secret-canary",
        b"websocket-secret-canary",
    ):
        assert (canary in exported) is (sys.argv[1] == "raw"), canary
    assert b"RuntimeError" in exported
    assert b"/__privacy/{number}" in exported
    assert (b"REDACTED" in exported) is (sys.argv[1] != "raw")
    # Manual caller providers remain usable after both application lifespans.
    before = len(payloads)
    with (
        providers["tracer_provider"].get_tracer("external").start_as_current_span("after-lifespan")
    ):
        pass
    assert len(payloads) == before + 1
    assert native._native_provider is None
    print(f"verified: empty caller {sys.argv[1]}")
finally:
    for provider in providers.values():
        provider.shutdown()
    server.shutdown()
    server.server_close()
    thread.join(timeout=5)
