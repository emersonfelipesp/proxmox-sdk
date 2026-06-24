"""Optional OpenTelemetry tracing support for SDK and FastAPI requests."""

from __future__ import annotations

import os
import socket
import threading
import uuid
from typing import Any

from proxmox_sdk import __version__
from proxmox_sdk.sdk.backends.base import AbstractBackend

_TRUE_VALUES = frozenset({"1", "true", "yes", "on"})
_TRACER: Any | None = None
_OTEL_IMPORT_FAILED = False
_BOOTSTRAP_LOCK = threading.Lock()


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in _TRUE_VALUES


def is_enabled(config: Any | None = None) -> bool:
    """Return whether proxmox-sdk telemetry is explicitly enabled."""
    if _truthy(os.environ.get("OTEL_SDK_DISABLED")):
        return False

    if isinstance(config, bool):
        config_enabled = config
    else:
        config_enabled = bool(getattr(config, "otel_enabled", False))

    return config_enabled or _truthy(os.environ.get("PROXMOX_OTEL_ENABLED"))


def _load_otel() -> dict[str, Any] | None:
    global _OTEL_IMPORT_FAILED

    if _OTEL_IMPORT_FAILED:
        return None

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.trace import SpanKind, Status, StatusCode
    except ImportError:
        _OTEL_IMPORT_FAILED = True
        return None

    return {
        "BatchSpanProcessor": BatchSpanProcessor,
        "OTLPSpanExporter": OTLPSpanExporter,
        "Resource": Resource,
        "SpanKind": SpanKind,
        "Status": Status,
        "StatusCode": StatusCode,
        "TracerProvider": TracerProvider,
        "trace": trace,
    }


def _provider_is_default_proxy(provider: Any) -> bool:
    provider_type = type(provider)
    return (
        provider_type.__name__ == "ProxyTracerProvider"
        and provider_type.__module__ == "opentelemetry.trace"
    )


def _traces_exporter_enabled() -> bool:
    configured = os.environ.get("OTEL_TRACES_EXPORTER")
    if not configured:
        return True

    exporters = {part.strip().lower() for part in configured.split(",") if part.strip()}
    if "none" in exporters:
        return False
    return "otlp" in exporters


def _otlp_http_protocol_enabled() -> bool:
    protocol = (
        os.environ.get("OTEL_EXPORTER_OTLP_TRACES_PROTOCOL")
        or os.environ.get("OTEL_EXPORTER_OTLP_PROTOCOL")
        or "http/protobuf"
    )
    return protocol.strip().lower() == "http/protobuf"


def _resource_attributes(resource_factory: Any) -> Any:
    service_name = os.environ.get("OTEL_SERVICE_NAME") or "proxmox-sdk"
    return resource_factory.create(
        {
            "service.name": service_name,
            "service.version": __version__,
            "service.instance.id": f"{socket.gethostname()}:{os.getpid()}:{uuid.uuid4()}",
        }
    )


def _ensure_tracer(config: Any | None = None) -> Any | None:
    if not is_enabled(config):
        return None

    global _TRACER
    if _TRACER is not None:
        return _TRACER

    with _BOOTSTRAP_LOCK:
        if _TRACER is not None:
            return _TRACER

        otel = _load_otel()
        if otel is None:
            return None

        trace = otel["trace"]
        provider = trace.get_tracer_provider()
        if _provider_is_default_proxy(provider):
            try:
                provider = otel["TracerProvider"](
                    resource=_resource_attributes(otel["Resource"]),
                )
                if _traces_exporter_enabled() and _otlp_http_protocol_enabled():
                    exporter = otel["OTLPSpanExporter"]()
                    provider.add_span_processor(otel["BatchSpanProcessor"](exporter))
                trace.set_tracer_provider(provider)
            except Exception:
                return None

        try:
            _TRACER = trace.get_tracer("proxmox_sdk", __version__)
        except Exception:
            return None

        return _TRACER


def _load_fastapi_instrumentor() -> Any | None:
    if _load_otel() is None:
        return None

    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except ImportError:
        return None
    return FastAPIInstrumentor


def _safe_error(exc: BaseException) -> Exception:
    return Exception(f"{type(exc).__name__}: Proxmox request failed")


class TracingBackend(AbstractBackend):
    """Decorator that emits one OpenTelemetry CLIENT span per backend request."""

    def __new__(
        cls,
        inner: AbstractBackend,
        *_: Any,
        **__: Any,
    ) -> TracingBackend:
        if cls is TracingBackend and hasattr(inner, "get_tokens"):
            return super().__new__(_TicketCapableTracingBackend)
        return super().__new__(cls)

    def __init__(
        self,
        inner: AbstractBackend,
        *,
        backend_name: str,
        service_name: str,
        otel_enabled: bool | None = None,
    ) -> None:
        self._inner = inner
        self._backend_name = backend_name
        self._service_name = service_name
        self._otel_enabled = otel_enabled

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__"):
            raise AttributeError(name)
        return getattr(self._inner, name)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        tracer = _ensure_tracer(self._otel_enabled)
        if tracer is None:
            return await self._inner.request(method, path, params=params, data=data)

        otel = _load_otel()
        if otel is None:
            return await self._inner.request(method, path, params=params, data=data)

        method_upper = method.upper()
        attributes = {
            "http.request.method": method_upper,
            "url.path": path,
            "proxmox.backend": self._backend_name,
            "proxmox.service": self._service_name,
        }

        with tracer.start_as_current_span(
            f"proxmox {method_upper}",
            kind=otel["SpanKind"].CLIENT,
            attributes=attributes,
            record_exception=False,
            set_status_on_exception=False,
        ) as span:
            try:
                return await self._inner.request(method, path, params=params, data=data)
            except Exception as exc:
                span.record_exception(_safe_error(exc))
                span.set_status(
                    otel["Status"](
                        otel["StatusCode"].ERROR,
                        f"{type(exc).__name__}: Proxmox request failed",
                    )
                )
                raise

    async def close(self) -> None:
        await self._inner.close()


class _TicketCapableTracingBackend(TracingBackend):
    async def get_tokens(self) -> tuple[str, str]:
        return await self._inner.get_tokens()


def instrument_fastapi_app(app: Any, config: Any | None = None) -> Any:
    """Instrument a FastAPI app when proxmox-sdk telemetry is enabled."""
    if not is_enabled(config):
        return app

    _ensure_tracer(config)
    instrumentor = _load_fastapi_instrumentor()
    if instrumentor is None:
        return app

    app_state = getattr(app, "state", None)
    if app_state is not None and getattr(app_state, "_proxmox_otel_instrumented", False):
        return app

    try:
        instrumentor().instrument_app(app)
    except Exception:
        return app

    if app_state is not None:
        app_state._proxmox_otel_instrumented = True
    return app


__all__ = ["TracingBackend", "instrument_fastapi_app", "is_enabled"]
