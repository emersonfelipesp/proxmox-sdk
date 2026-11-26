"""Generated Pydantic v2 schemas for Proxmox route group 'plugins'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr

GENERATED_FOR_PROXMOX_VERSION = "latest"
GENERATED_SOURCE_SHA256 = "83d00ff237bdfac0cb144eb603209f20654125dc40350c35447707fd330a0179"
GENERATED_AT = "2026-11-26T14:19:39.255287+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')


def _allowed_ints(allowed: tuple[int, ...]) -> AfterValidator:
    def validate(value: int) -> int:
        if value not in allowed:
            raise ValueError('value is not an allowed schema member')
        return value

    return AfterValidator(validate)

class GetPluginsResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index. response."""
    subdir: StrictStr | None = Field(None)

class GetPluginsResponse(RootModel[list[GetPluginsResponseItem]]):
    """List of items. index. Directory index. response."""
    root: list[GetPluginsResponseItem] = Field(...)

class GetPluginsStorageResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index. response."""
    subdir: StrictStr | None = Field(None)

class GetPluginsStorageResponse(RootModel[list[GetPluginsStorageResponseItem]]):
    """List of items. index. Directory index. response."""
    root: list[GetPluginsStorageResponseItem] = Field(...)

class GetPluginsStoragePluginResponseItem(ProxmoxBaseModel):
    """Model for index. List all available storage plugins and their metadata. response."""
    content: dict[str, object] | None = Field(None, description='The content types of the plugin.')
    display_name: StrictStr | None = Field(None, alias="display-name", description='The name of the storage type, if the plugin provides one.')
    origin: StrictStr | None = Field(None, description="Whether the plugin is shipped with Proxmox VE ('builtin') or installed separately ('custom').")
    schema: dict[str, object] | None = Field(None)
    type: StrictStr | None = Field(None, description='The storage type of the plugin.')

class GetPluginsStoragePluginResponse(RootModel[list[GetPluginsStoragePluginResponseItem]]):
    """List of items. index. List all available storage plugins and their metadata. response."""
    root: list[GetPluginsStoragePluginResponseItem] = Field(...)

class GetPluginsStoragePluginTypeResponse(ProxmoxBaseModel):
    """Model for info. Fetch metadata of a storage plugin. response."""
    content: dict[str, object] = Field(..., description='The content types of the plugin.')
    display_name: StrictStr | None = Field(None, alias="display-name", description='The name of the storage type, if the plugin provides one.')
    origin: StrictStr = Field(..., description="Whether the plugin is shipped with Proxmox VE ('builtin') or installed separately ('custom').")
    schema: dict[str, object] = Field(...)
    type: StrictStr = Field(..., description='The storage type of the plugin.')
