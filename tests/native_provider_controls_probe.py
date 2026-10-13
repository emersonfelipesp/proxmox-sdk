"""Observe native ASGI lifecycle and actual selected-provider exported records."""

import os
import sys

from fastapi.testclient import TestClient
from opentelemetry import _logs, trace
from opentelemetry.sdk._logs import LoggerProvider
from opentelemetry.sdk._logs.export import InMemoryLogRecordExporter, SimpleLogRecordProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from proxmox_sdk import server_telemetry as native
from proxmox_sdk.mock.app import create_mock_app

mode = sys.argv[1]
os.environ["FASTAPI_OTEL_AUTO_CONFIGURE"] = "true"
os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://127.0.0.1:1"
# No native transport may run in this identity/memory probe.
for signal in ("TRACES", "METRICS", "LOGS"):
    os.environ[f"OTEL_{signal}_EXPORTER"] = "none"
configuration = {}
if mode == "disabled-flags":
    configuration.update(tracing=False, logs=False, metrics=False)
if mode == "auto":
    configuration["auto_configure"] = False
if mode == "empty":
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = ""
if mode == "absent":
    os.environ.pop("OTEL_EXPORTER_OTLP_ENDPOINT")
if mode.endswith("-off"):
    configuration[{"trace-off": "tracing", "logs-off": "logs", "metrics-off": "metrics"}[mode]] = (
        False
    )
if mode == "fallback":
    os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = ""
    os.environ["OTEL_TRACES_EXPORTER"] = "otlp"
    # Verify selection only; do not start native exporters against an unused port.
    selected = native.native_server_configuration()
    assert isinstance(selected["tracer_provider"], TracerProvider)
    print(f"verified: {mode}")
    sys.exit(0)
if mode in {"disabled-flags", "auto", "empty", "absent"}:
    for signal in ("TRACES", "METRICS", "LOGS"):
        os.environ[f"OTEL_{signal}_EXPORTER"] = "otlp"
if mode.endswith("-off"):
    signal = {"trace-off": "TRACES", "logs-off": "LOGS", "metrics-off": "METRICS"}[mode]
    os.environ[f"OTEL_{signal}_EXPORTER"] = "otlp"
exporter = InMemorySpanExporter()
provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(exporter))
if mode in {"caller", "global-caller"}:
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = ""
    configuration.update(tracer_provider=provider, auto_configure=False)
if mode == "global-caller":
    trace.set_tracer_provider(provider)
    configuration.pop("tracer_provider")
if mode in {"client", "explicit-client"}:
    native.telemetry._CLIENT_PROVIDER = provider
    trace.set_tracer_provider(provider)
    if mode == "explicit-client":
        configuration.update(tracer_provider=provider, auto_configure=False)
if mode == "callbacks":
    logs = InMemoryLogRecordExporter()
    logger_provider = LoggerProvider()
    logger_provider.add_log_record_processor(native.ExceptionPrivacyProcessor())
    logger_provider.add_log_record_processor(SimpleLogRecordProcessor(logs))
    provider.add_span_processor(native.RequestPrivacyProcessor())
    os.environ["OTEL_SDK_DISABLED"] = "true"
    with provider.get_tracer("fastapi").start_as_current_span(
        "disabled-callback", attributes={"url.query": "original"}
    ):
        pass
    assert exporter.get_finished_spans()[0].attributes["url.query"] == "REDACTED"
    logger_provider.get_logger("fastapi").emit(
        body="static", attributes={"exception.message": "original"}
    )
    assert "exception.message" not in logs.get_finished_logs()[0].log_record.attributes
    os.environ["OTEL_SDK_DISABLED"] = "false"
    logger_provider.get_logger("external").emit(
        body="static", attributes={"exception.message": "external"}
    )
    assert logs.get_finished_logs()[-1].log_record.attributes["exception.message"] == "external"
    logger_provider.get_logger("fastapi").emit(
        body="static", attributes={"exception.message": "secret", "exception.type": "RuntimeError"}
    )
    assert dict(logs.get_finished_logs()[-1].log_record.attributes) == {
        "exception.type": "RuntimeError"
    }
    print(f"verified: {mode}")
    sys.exit(0)
before_logger = _logs.get_logger_provider()
app = create_mock_app(telemetry=configuration)
with TestClient(app) as client:
    assert client.get("/openapi.json?token=query-secret-canary").status_code == 200
assert _logs.get_logger_provider() is before_logger
if mode in {"caller", "global-caller", "explicit-client"}:
    spans = exporter.get_finished_spans()
    assert spans
    assert all("query-secret-canary" not in str(span.attributes) for span in spans)
    assert any(span.attributes.get("url.query") == "REDACTED" for span in spans)
    with provider.get_tracer("external").start_as_current_span(
        "after-lifespan", attributes={"url.query": "external-value"}
    ):
        pass
    assert exporter.get_finished_spans()[-1].attributes["url.query"] == "external-value"
elif mode == "client":
    assert not exporter.get_finished_spans()
assert native._native_provider is None
if hasattr(native, "_native_meter"):
    assert native._native_meter is None
print(f"verified: {mode}")
