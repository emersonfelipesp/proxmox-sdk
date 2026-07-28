"""Global resource and subscription endpoints (cross-remote)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk.pdm import models as m
from proxmox_sdk.pdm._normalization import (
    REDACTED_REMOTE_ERROR,
    redact_optional_error,
    require_list,
    require_mapping,
    validate_model,
)
from proxmox_sdk.pdm.errors import PDMResponseContractError

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK

_RESOURCE_TYPE_ALIASES = {"vm": "qemu", "ct": "lxc"}
_RESOURCE_TYPES = {"storage", "qemu", "lxc", "network", "datastore", "node"}
_GLOBAL_RESOURCE_TYPES = {
    "pve-storage",
    "pve-qemu",
    "pve-lxc",
    "pve-node",
    "pve-network",
    "pbs-node",
    "pbs-datastore",
}


def _resource_type_parameter(resource_type: str) -> str:
    """Map ergonomic legacy names to the captured ``resource-type`` enum."""

    normalized = _RESOURCE_TYPE_ALIASES.get(resource_type, resource_type)
    if normalized not in _RESOURCE_TYPES:
        expected = ", ".join(sorted(_RESOURCE_TYPES | set(_RESOURCE_TYPE_ALIASES)))
        raise ValueError(
            f"Unsupported PDM resource type {resource_type!r}; expected one of {expected}"
        )
    return normalized


def _normalize_resource_envelope(
    data: Any,
    *,
    operation: str,
    reject_remote_error: bool,
) -> tuple[str, str | None, list[m.PDMResource]]:
    """Normalize a schema-defined per-remote resource envelope."""

    envelope, has_error = redact_optional_error(
        require_mapping(data, operation=operation),
        operation=operation,
    )
    remote = envelope.get("remote")
    if not isinstance(remote, str) or not remote.strip():
        raise PDMResponseContractError(
            operation=operation,
            expected="an object with a non-empty remote identifier",
            received=envelope,
            detail="invalid fields: remote",
        )
    error = REDACTED_REMOTE_ERROR if has_error else None
    resources: list[m.PDMResource] = []
    resource_values = require_list(
        envelope.get("resources"),
        operation=f"{operation}.resources",
    )
    for index, item in enumerate(resource_values):
        item_operation = f"{operation}.resources[{index}]"
        payload = require_mapping(item, operation=item_operation)
        # The envelope owns both the remote identity and its failure state.  PDM
        # resource models intentionally allow forward-compatible extra fields,
        # so raw nested error fields must be removed before validation and a
        # caller-provided ``remote_error`` must never override our redaction.
        payload.pop("error", None)
        payload["remote"] = remote
        payload["remote_error"] = error
        resource = validate_model(m.PDMResource, payload, operation=item_operation)
        if resource.type not in _GLOBAL_RESOURCE_TYPES:
            raise PDMResponseContractError(
                operation=item_operation,
                expected="a resource with a global schema discriminator",
                received=resource,
                detail="invalid fields: type",
            )
        resources.append(resource)
    if reject_remote_error and has_error and not resources:
        raise PDMResponseContractError(
            operation=operation,
            expected="resources or a successful per-remote resource envelope",
            received=envelope,
            detail="remote reported an error without usable resources",
        )
    return remote, error, resources


class GlobalResourcesDomain:
    """Aggregated resource queries that span every registered remote."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self, *, type: str | None = None) -> list[m.PDMResource]:
        params: dict[str, Any] = {}
        if type is not None:
            params["resource-type"] = _resource_type_parameter(type)
        data = await self._sdk.resources.list.get(**params)
        operation = "GET /resources/list"
        resources: list[m.PDMResource] = []
        for index, envelope in enumerate(require_list(data, operation=operation)):
            _, _, items = _normalize_resource_envelope(
                envelope,
                operation=f"{operation}[{index}]",
                reject_remote_error=True,
            )
            resources.extend(items)
        return resources

    async def status(self) -> m.PDMResourceStatus:
        data = await self._sdk.resources.status.get()
        operation = "GET /resources/status"
        remote, error, resources = _normalize_resource_envelope(
            data,
            operation=operation,
            reject_remote_error=False,
        )
        return validate_model(
            m.PDMResourceStatus,
            {
                "remote": remote,
                "error": error,
                "resources": [resource.model_dump() for resource in resources],
            },
            operation=operation,
        )


class SubscriptionsDomain:
    """Fleet-wide subscription state."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PDMSubscription]:
        data = await self._sdk.resources.subscription.get()
        operation = "GET /resources/subscription"
        subscriptions: list[m.PDMSubscription] = []
        for index, item in enumerate(require_list(data, operation=operation)):
            item_operation = f"{operation}[{index}]"
            payload, _ = redact_optional_error(
                require_mapping(item, operation=item_operation),
                operation=item_operation,
            )
            subscriptions.append(
                validate_model(m.PDMSubscription, payload, operation=item_operation)
            )
        return subscriptions
