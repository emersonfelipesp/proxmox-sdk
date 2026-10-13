"""Keep public native provider resource identity under operator control."""

import pytest

from proxmox_sdk import server_telemetry as native


@pytest.mark.parametrize("service_name", [None, "operator-proxmox-api"])
def test_native_service_identity_is_selected_by_the_operator(
    monkeypatch: pytest.MonkeyPatch, service_name: str | None
) -> None:
    """Retain explicit identity and the SDK fallback when no identity is supplied."""
    monkeypatch.setenv("OTEL_SDK_DISABLED", "false")
    monkeypatch.delenv("OTEL_RESOURCE_ATTRIBUTES", raising=False)
    monkeypatch.delenv("OTEL_SERVICE_NAME", raising=False)
    if service_name is not None:
        monkeypatch.setenv("OTEL_SERVICE_NAME", service_name)
    monkeypatch.setattr(native, "_native_provider", None)
    provider = native._native_tracer_provider()
    try:
        selected = provider.resource.attributes["service.name"]
        if service_name is None:
            assert str(selected).startswith("unknown_service")
        else:
            assert selected == service_name
    finally:
        provider.shutdown()
