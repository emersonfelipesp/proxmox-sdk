"""Generated Pydantic v2 schemas for Proxmox route group 'version'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr

GENERATED_FOR_PROXMOX_VERSION = "9.2"
GENERATED_SOURCE_SHA256 = "db7e80b8646db731814601617206e3835b5b572def655f18a27e0b22b6f31297"
GENERATED_AT = "2026-08-06T18:55:02.064681+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')


def _allowed_ints(allowed: tuple[int, ...]) -> AfterValidator:
    def validate(value: int) -> int:
        if value not in allowed:
            raise ValueError('value is not an allowed schema member')
        return value

    return AfterValidator(validate)

class GetVersionResponse(ProxmoxBaseModel):
    """Model for version. API version details, including some parts of the global datacenter config. response."""
    console: StrictStr | None = Field(None, description='The default console viewer to use.')
    release: StrictStr = Field(..., description='The current Proxmox VE point release in `x.y` format.')
    repoid: StrictStr = Field(..., description='The short git revision from which this version was build.')
    version: StrictStr = Field(..., description='The full pve-manager package version of this node.')
