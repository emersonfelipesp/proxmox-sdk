"""PVE-via-PDM operations: nodes, qemu/lxc guests, resources, tasks.

All PDM guest operations require a ``remote`` in addition to ``vmid`` — the
PDM API multiplexes across registered PVE clusters.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.pdm import models as m
from proxmox_sdk.pdm._normalization import (
    require_list,
    require_mapping,
    validate_model,
    validate_model_list,
    validate_rrd_query,
)
from proxmox_sdk.pdm.errors import PDMResponseContractError

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK

_CONFIG_STATES = {"pending", "active"}
_PVE_RESOURCE_KINDS = {"vm", "storage", "node", "sdn"}
_PVE_RESOURCE_TYPES = {"storage", "qemu", "lxc", "node", "network"}


def _validate_pve_resource_type(
    resource: m.PDMResource,
    *,
    operation: str,
) -> m.PDMResource:
    """Reject global or unknown discriminators on the PVE-local surface."""

    if resource.type not in _PVE_RESOURCE_TYPES:
        raise PDMResponseContractError(
            operation=operation,
            expected="a PVE resource with a local schema discriminator",
            received=resource,
            detail="invalid fields: type",
        )
    return resource


class _GuestOps:
    """Shared qemu/lxc lifecycle + RRD + remote-migrate helpers."""

    _kind: str  # "qemu" or "lxc"

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    def _guest_resource(self, remote: str, vmid: int) -> Any:
        # Use getattr so "qemu"/"lxc" becomes a direct path segment, not a
        # sub-path via the non-existent /pve/remotes/{remote}/guests/{kind}/ prefix.
        # Correct paths: /pve/remotes/{remote}/qemu/{vmid}
        #                /pve/remotes/{remote}/lxc/{vmid}
        return getattr(self._sdk.pve.remotes(remote), self._kind)(vmid)

    async def list(self, remote: str) -> list[m.PDMGuest]:
        data = await getattr(self._sdk.pve.remotes(remote), self._kind).get()
        items: list[m.PDMGuest] = []
        operation = f"GET /pve/remotes/{{remote}}/{self._kind}"
        for index, entry in enumerate(require_list(data, operation=operation)):
            payload = require_mapping(entry, operation=f"{operation}[{index}]")
            payload.setdefault("remote", remote)
            payload.setdefault("type", self._kind)
            items.append(
                validate_model(
                    m.PDMGuest,
                    payload,
                    operation=f"{operation}[{index}]",
                )
            )
        return items

    async def config(
        self,
        remote: str,
        vmid: int,
        *,
        state: m.PDMGuestConfigState = "pending",
    ) -> m.PDMGuestConfig:
        if state not in _CONFIG_STATES:
            raise ValueError(f"Unsupported PDM guest configuration state {state!r}")
        data = await self._guest_resource(remote, vmid).config.get(state=state)
        return validate_model(
            m.PDMGuestConfig,
            data,
            operation=f"GET /pve/remotes/{{remote}}/{self._kind}/{{vmid}}/config",
        )

    async def start(self, remote: str, vmid: int) -> Any:
        return unwrap_data(await self._guest_resource(remote, vmid).start.post())

    async def stop(self, remote: str, vmid: int) -> Any:
        return unwrap_data(await self._guest_resource(remote, vmid).stop.post())

    async def shutdown(self, remote: str, vmid: int) -> Any:
        return unwrap_data(await self._guest_resource(remote, vmid).shutdown.post())

    async def migrate(
        self,
        remote: str,
        vmid: int,
        *,
        target: str,
        online: bool | None = None,
    ) -> Any:
        kwargs: dict[str, Any] = {"target": target}
        if online is not None:
            kwargs["online"] = online
        return unwrap_data(await self._guest_resource(remote, vmid).migrate.post(**kwargs))

    async def remote_migrate(
        self,
        remote: str,
        vmid: int,
        *,
        target_remote: str,
        target_vmid: int | None = None,
        target_node: str | None = None,
        online: bool | None = None,
    ) -> Any:
        kwargs: dict[str, Any] = {"target-remote": target_remote}
        if target_vmid is not None:
            kwargs["target-vmid"] = target_vmid
        if target_node is not None:
            kwargs["target-node"] = target_node
        if online is not None:
            kwargs["online"] = online
        return unwrap_data(
            await self._guest_resource(remote, vmid)("remote-migrate").post(**kwargs)
        )

    async def rrddata(
        self,
        remote: str,
        vmid: int,
        *,
        timeframe: m.PDMRRDTimeframe = "hour",
        cf: m.PDMRRDConsolidation = "AVERAGE",
    ) -> list[m.PDMRRDData]:
        params = validate_rrd_query(timeframe, cf)
        data = await self._guest_resource(remote, vmid).rrddata.get(**params)
        return validate_model_list(
            m.PDMRRDData,
            data,
            operation=f"GET /pve/remotes/{{remote}}/{self._kind}/{{vmid}}/rrddata",
        )


class _QemuOps(_GuestOps):
    _kind = "qemu"


class _LxcOps(_GuestOps):
    _kind = "lxc"


class PVEDomain:
    """All PDM operations targeting registered Proxmox VE remotes."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk
        self.qemu = _QemuOps(sdk)
        self.lxc = _LxcOps(sdk)

    async def nodes(self, remote: str) -> list[m.PDMNode]:
        data = await self._sdk.pve.remotes(remote).nodes.get()
        items: list[m.PDMNode] = []
        operation = "GET /pve/remotes/{remote}/nodes"
        for index, entry in enumerate(require_list(data, operation=operation)):
            payload = require_mapping(entry, operation=f"{operation}[{index}]")
            payload.setdefault("remote", remote)
            items.append(validate_model(m.PDMNode, payload, operation=f"{operation}[{index}]"))
        return items

    async def node_rrddata(
        self,
        remote: str,
        node: str,
        *,
        timeframe: m.PDMRRDTimeframe = "hour",
        cf: m.PDMRRDConsolidation = "AVERAGE",
    ) -> list[m.PDMRRDData]:
        params = validate_rrd_query(timeframe, cf)
        data = await self._sdk.pve.remotes(remote).nodes(node).rrddata.get(**params)
        return validate_model_list(
            m.PDMRRDData,
            data,
            operation="GET /pve/remotes/{remote}/nodes/{node}/rrddata",
        )

    async def resources(self, remote: str, *, type: str | None = None) -> list[m.PDMResource]:
        params: dict[str, Any] = {}
        if type is not None:
            if type not in _PVE_RESOURCE_KINDS:
                raise ValueError(f"Unsupported PDM PVE resource kind {type!r}")
            params["kind"] = type
        data = await self._sdk.pve.remotes(remote).resources.get(**params)
        items: list[m.PDMResource] = []
        operation = "GET /pve/remotes/{remote}/resources"
        for index, entry in enumerate(require_list(data, operation=operation)):
            payload = require_mapping(entry, operation=f"{operation}[{index}]")
            # This endpoint is path-bound to one remote and does not expose an
            # error envelope.  Drop untrusted error context and overwrite any
            # spoofed resource metadata before permissive model validation.
            payload.pop("error", None)
            payload["remote"] = remote
            payload["remote_error"] = None
            item_operation = f"{operation}[{index}]"
            items.append(
                _validate_pve_resource_type(
                    validate_model(m.PDMResource, payload, operation=item_operation),
                    operation=item_operation,
                )
            )
        return items

    async def tasks(self, remote: str) -> list[m.PDMTask]:
        data = await self._sdk.pve.remotes(remote).tasks.get()
        return validate_model_list(
            m.PDMTask,
            data,
            operation="GET /pve/remotes/{remote}/tasks",
        )
