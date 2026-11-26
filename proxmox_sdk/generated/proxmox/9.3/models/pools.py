"""Generated Pydantic v2 schemas for Proxmox route group 'pools'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr

GENERATED_FOR_PROXMOX_VERSION = "9.3"
GENERATED_SOURCE_SHA256 = "f1246f2c85d8ae75e2f67085eb773d628f984d25f8372488c7e42e842b693152"
GENERATED_AT = "2026-11-26T14:18:58.794724+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')


def _allowed_ints(allowed: tuple[int, ...]) -> AfterValidator:
    def validate(value: int) -> int:
        if value not in allowed:
            raise ValueError('value is not an allowed schema member')
        return value

    return AfterValidator(validate)

class DeletePoolsRequest(ProxmoxBaseModel):
    """Model for delete_pool. Delete pool. request."""
    poolid: StrictStr = Field(...)

class DeletePoolsResponse(RootModel[None]):
    """Model for delete_pool. Delete pool. response."""
    root: None = Field(...)

class GetPoolsResponseItem(ProxmoxBaseModel):
    """Model for index. List pools or get pool configuration. response."""
    comment: StrictStr | None = Field(None)
    members: list[dict[str, object]] | None = Field(None)
    poolid: StrictStr | None = Field(None)

class GetPoolsResponse(RootModel[list[GetPoolsResponseItem]]):
    """List of items. index. List pools or get pool configuration. response."""
    root: list[GetPoolsResponseItem] = Field(...)

class PostPoolsRequest(ProxmoxBaseModel):
    """Model for create_pool. Create new pool. request."""
    comment: StrictStr | None = Field(None)
    poolid: StrictStr = Field(...)

class PostPoolsResponse(RootModel[None]):
    """Model for create_pool. Create new pool. response."""
    root: None = Field(...)

class PutPoolsRequest(ProxmoxBaseModel):
    """Model for update_pool. Update pool. request."""
    allow_move: bool | None = Field(None, alias="allow-move", description='Allow adding a guest even if already in another pool. The guest will be removed from its current pool and added to this one.')
    comment: StrictStr | None = Field(None)
    delete: bool | None = Field(None, description='Remove the passed VMIDs, storage IDs and/or network resources instead of adding them.')
    network: StrictStr | None = Field(None, description="List of network resources to add or remove from this pool. 'vnet/<zone>/<vnet>' allows network devices on the VNet without VLAN tag or trunks, a trailing '/<tag>' allows that VLAN tag, and '/*' allows the VNet with or without any VLAN tag. This only controls the network device configuration, a device without VLAN tag can still carry tagged guest traffic on a VLAN-aware VNet.")
    poolid: StrictStr = Field(...)
    storage: StrictStr | None = Field(None, description='List of storage IDs to add or remove from this pool.')
    vms: StrictStr | None = Field(None, description='List of guest VMIDs to add or remove from this pool.')

class PutPoolsResponse(RootModel[None]):
    """Model for update_pool. Update pool. response."""
    root: None = Field(...)

class DeletePoolsPoolidResponse(RootModel[None]):
    """Model for delete_pool_deprecated. Delete pool (deprecated, no support for nested pools, use 'DELETE /pools/?poolid={poolid}'). response."""
    root: None = Field(...)

class GetPoolsPoolidResponse(ProxmoxBaseModel):
    """Model for read_pool. Get pool configuration (deprecated, no support for nested pools, use 'GET /pools/?poolid={poolid}'). response."""
    comment: StrictStr | None = Field(None)
    members: list[dict[str, object]] = Field(...)

class PutPoolsPoolidRequest(ProxmoxBaseModel):
    """Model for update_pool_deprecated. Update pool data (deprecated, no support for nested pools - use 'PUT /pools/?poolid={poolid}' instead). request."""
    allow_move: bool | None = Field(None, alias="allow-move", description='Allow adding a guest even if already in another pool. The guest will be removed from its current pool and added to this one.')
    comment: StrictStr | None = Field(None)
    delete: bool | None = Field(None, description='Remove the passed VMIDs, storage IDs and/or network resources instead of adding them.')
    network: StrictStr | None = Field(None, description="List of network resources to add or remove from this pool. 'vnet/<zone>/<vnet>' allows network devices on the VNet without VLAN tag or trunks, a trailing '/<tag>' allows that VLAN tag, and '/*' allows the VNet with or without any VLAN tag. This only controls the network device configuration, a device without VLAN tag can still carry tagged guest traffic on a VLAN-aware VNet.")
    storage: StrictStr | None = Field(None, description='List of storage IDs to add or remove from this pool.')
    vms: StrictStr | None = Field(None, description='List of guest VMIDs to add or remove from this pool.')

class PutPoolsPoolidResponse(RootModel[None]):
    """Model for update_pool_deprecated. Update pool data (deprecated, no support for nested pools - use 'PUT /pools/?poolid={poolid}' instead). response."""
    root: None = Field(...)
