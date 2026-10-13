"""Mock API module for Proxmox OpenAPI."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

from proxmox_sdk.mock.schema_helpers import (
    deep_merge,
    merge_with_schema_defaults,
    resolved_schema,
    sample_value_for_schema,
    schema_fingerprint,
    schema_kind,
)
from proxmox_sdk.mock.state import (
    MockStateStore,
    SharedMemoryMockStore,
    SQLiteMockStore,
    mock_state_owner_pid,
    reset_shared_mock_state,
    shared_mock_store,
)

if TYPE_CHECKING:
    from proxmox_sdk.mock.app import create_mock_app
    from proxmox_sdk.mock.routes import (
        generated_proxmox_mock_route_state,
        register_generated_proxmox_mock_routes,
    )

__all__ = [
    "create_mock_app",
    "generated_proxmox_mock_route_state",
    "register_generated_proxmox_mock_routes",
    "deep_merge",
    "merge_with_schema_defaults",
    "sample_value_for_schema",
    "schema_fingerprint",
    "schema_kind",
    "resolved_schema",
    "MockStateStore",
    "SharedMemoryMockStore",
    "SQLiteMockStore",
    "mock_state_owner_pid",
    "reset_shared_mock_state",
    "shared_mock_store",
]


_SERVER_EXPORTS = {
    "create_mock_app": "proxmox_sdk.mock.app",
    "generated_proxmox_mock_route_state": "proxmox_sdk.mock.routes",
    "register_generated_proxmox_mock_routes": "proxmox_sdk.mock.routes",
}


def __getattr__(name: str) -> Any:
    """Load optional HTTP server dependencies only when explicitly requested."""
    module = _SERVER_EXPORTS.get(name)
    if module is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    value = getattr(import_module(module), name)
    globals()[name] = value
    return value
