"""Generated Pydantic v2 schemas for Proxmox route group 'version'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, RootModel

GENERATED_FOR_PROXMOX_VERSION = "9.2"
GENERATED_SOURCE_SHA256 = "db7e80b8646db731814601617206e3835b5b572def655f18a27e0b22b6f31297"
GENERATED_AT = "2026-05-23T21:58:59.250679+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')

class GetVersionResponse(ProxmoxBaseModel):
    """Model for version. API version details, including some parts of the global datacenter config. response."""
    console: str | None = Field(None, description='The default console viewer to use.')
    release: str = Field(..., description='The current Proxmox VE point release in `x.y` format.')
    repoid: str = Field(..., description='The short git revision from which this version was build.')
    version: str = Field(..., description='The full pve-manager package version of this node.')
