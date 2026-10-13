"""Native server providers coexist with independently owned SDK client export."""

from __future__ import annotations

import os
from threading import Lock
from weakref import WeakSet

from fastapi.telemetry import TelemetryConfig
from opentelemetry import _logs, trace
from opentelemetry._logs._internal import ProxyLoggerProvider
from opentelemetry.context import Context
from opentelemetry.sdk._logs import LoggerProvider, LogRecordProcessor, ReadWriteLogRecord
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import Span, SpanProcessor, TracerProvider

from proxmox_sdk import __version__, telemetry

_native_provider: TracerProvider | None = None
_provider_lock = Lock()
_log_privacy: WeakSet[LoggerProvider] = WeakSet()
_trace_privacy: WeakSet[TracerProvider] = WeakSet()


class ExceptionPrivacyProcessor(LogRecordProcessor):
    """Keep exception types without arbitrary exception content."""

    def on_emit(self, log_record: ReadWriteLogRecord) -> None:
        scope = log_record.instrumentation_scope
        if scope and scope.name == "fastapi":
            attributes = dict(log_record.log_record.attributes or {})
            attributes.pop("exception.message", None)
            attributes.pop("exception.stacktrace", None)
            log_record.log_record.attributes = attributes

    def shutdown(self) -> None:
        """This processor owns no resources."""

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """This processor never buffers records."""
        return True


class RequestPrivacyProcessor(SpanProcessor):
    """Redact concrete URL values before any exporter snapshots a span."""

    def on_start(self, span: Span, parent_context: Context | None = None) -> None:
        scope = span.instrumentation_scope
        if not scope or scope.name != "fastapi":
            return
        for key in ("url.path", "url.query"):
            if key in (span.attributes or {}):
                span.set_attribute(key, "REDACTED")


def _automatic_signal(configuration: TelemetryConfig, signal: str) -> bool:
    """Allocate implicit providers only when native environment setup is eligible."""
    automatic = configuration.get(
        "auto_configure", os.getenv("FASTAPI_OTEL_AUTO_CONFIGURE", "").lower() == "true"
    )
    if (
        telemetry._truthy(os.getenv("OTEL_SDK_DISABLED"))
        or not automatic
        or not configuration.get(signal, True)
    ):
        return False
    environment_signal = "TRACES" if signal == "tracing" else signal.upper()
    exporter = (os.getenv(f"OTEL_{environment_signal}_EXPORTER") or "otlp").strip().lower()
    endpoint = os.getenv(f"OTEL_EXPORTER_OTLP_{environment_signal}_ENDPOINT") or os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT"
    )
    return bool(endpoint) and exporter != "none"


def _native_tracer_provider() -> TracerProvider:
    """Keep library-owned server export separate from standalone client export."""
    global _native_provider
    with _provider_lock:
        if _native_provider is None:
            resource = Resource.create({"service.version": __version__})
            _native_provider = TracerProvider(resource=resource)
        return _native_provider


def _select_tracer(configuration: TelemetryConfig) -> trace.TracerProvider:
    """Preserve caller providers; isolate only providers owned by this library."""
    selected = configuration.get("tracer_provider")
    if selected is not None:
        return selected
    global_provider = trace.get_tracer_provider()
    if isinstance(global_provider, trace.ProxyTracerProvider):
        return (
            _native_tracer_provider()
            if _automatic_signal(configuration, "tracing")
            else global_provider
        )
    if global_provider is telemetry._CLIENT_PROVIDER:
        return (
            _native_tracer_provider()
            if _automatic_signal(configuration, "tracing")
            else trace.NoOpTracerProvider()
        )
    return global_provider


def _configure_log_privacy(configuration: TelemetryConfig) -> None:
    """Register native log filtering before native environment exporter setup."""
    selected = configuration.get("logger_provider")
    provider = selected if selected is not None else _logs.get_logger_provider()
    if (
        isinstance(provider, ProxyLoggerProvider)
        and selected is None
        and _automatic_signal(configuration, "logs")
    ):
        provider = LoggerProvider()
        _logs.set_logger_provider(provider)
    if isinstance(provider, LoggerProvider) and provider not in _log_privacy:
        provider.add_log_record_processor(ExceptionPrivacyProcessor())
        _log_privacy.add(provider)


def native_server_configuration(configuration: TelemetryConfig | None = None) -> TelemetryConfig:
    """Use native FastAPI signals without altering environment or caller exporters."""
    selected: TelemetryConfig = {} if configuration is None else configuration.copy()
    if telemetry._truthy(os.getenv("OTEL_SDK_DISABLED")):
        selected.update(
            {"tracing": False, "metrics": False, "logs": False, "auto_configure": False}
        )
    provider = _select_tracer(selected)
    selected["tracer_provider"] = provider
    if isinstance(provider, TracerProvider) and provider not in _trace_privacy:
        provider.add_span_processor(RequestPrivacyProcessor())
        _trace_privacy.add(provider)
    _configure_log_privacy(selected)
    return selected
