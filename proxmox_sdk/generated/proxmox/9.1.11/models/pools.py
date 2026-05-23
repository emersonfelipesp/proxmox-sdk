"""Generated Pydantic v2 schemas for Proxmox route group 'pools'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, RootModel

GENERATED_FOR_PROXMOX_VERSION = "9.1.11"
GENERATED_SOURCE_SHA256 = "6fb57e0668c0d043fb9f7e8baf387b320c3948acf634ae439f0d748ea744ad63"
GENERATED_AT = "2026-05-23T21:58:59.668705+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')

class DeletePoolsRequest(ProxmoxBaseModel):
    """Model for delete_pool. Delete pool. request."""
    poolid: str = Field(...)

class DeletePoolsResponse(RootModel[None]):
    """Model for delete_pool. Delete pool. response."""
    root: None = Field(...)

class GetPoolsResponseItem(ProxmoxBaseModel):
    """Model for index. List pools or get pool configuration. response."""
    comment: str | None = Field(None)
    members: list[dict[str, object]] | None = Field(None)
    poolid: str | None = Field(None)

class GetPoolsResponse(RootModel[list[GetPoolsResponseItem]]):
    """List of items. index. List pools or get pool configuration. response."""
    root: list[GetPoolsResponseItem] = Field(...)

class PostPoolsRequest(ProxmoxBaseModel):
    """Model for create_pool. Create new pool. request."""
    comment: str | None = Field(None)
    poolid: str = Field(...)

class PostPoolsResponse(RootModel[None]):
    """Model for create_pool. Create new pool. response."""
    root: None = Field(...)

class PutPoolsRequest(ProxmoxBaseModel):
    """Model for update_pool. Update pool. request."""
    allow_move: bool | None = Field(None, alias="allow-move", description='Allow adding a guest even if already in another pool. The guest will be removed from its current pool and added to this one.')
    comment: str | None = Field(None)
    delete: bool | None = Field(None, description='Remove the passed VMIDs and/or storage IDs instead of adding them.')
    poolid: str = Field(...)
    storage: str | None = Field(None, description='List of storage IDs to add or remove from this pool.')
    vms: str | None = Field(None, description='List of guest VMIDs to add or remove from this pool.')

class PutPoolsResponse(RootModel[None]):
    """Model for update_pool. Update pool. response."""
    root: None = Field(...)

class DeletePoolsPoolidResponse(RootModel[None]):
    """Model for delete_pool_deprecated. Delete pool (deprecated, no support for nested pools, use 'DELETE /pools/?poolid={poolid}'). response."""
    root: None = Field(...)

class GetPoolsPoolidResponse(ProxmoxBaseModel):
    """Model for read_pool. Get pool configuration (deprecated, no support for nested pools, use 'GET /pools/?poolid={poolid}'). response."""
    comment: str | None = Field(None)
    members: list[dict[str, object]] = Field(...)

class PutPoolsPoolidRequest(ProxmoxBaseModel):
    """Model for update_pool_deprecated. Update pool data (deprecated, no support for nested pools - use 'PUT /pools/?poolid={poolid}' instead). request."""
    allow_move: bool | None = Field(None, alias="allow-move", description='Allow adding a guest even if already in another pool. The guest will be removed from its current pool and added to this one.')
    comment: str | None = Field(None)
    delete: bool | None = Field(None, description='Remove the passed VMIDs and/or storage IDs instead of adding them.')
    storage: str | None = Field(None, description='List of storage IDs to add or remove from this pool.')
    vms: str | None = Field(None, description='List of guest VMIDs to add or remove from this pool.')

class PutPoolsPoolidResponse(RootModel[None]):
    """Model for update_pool_deprecated. Update pool data (deprecated, no support for nested pools - use 'PUT /pools/?poolid={poolid}' instead). response."""
    root: None = Field(...)
