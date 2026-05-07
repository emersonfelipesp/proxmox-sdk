"""Integrity guard for the generated Pydantic schema artifact.

Recomputes ``SHA-256(openapi.json)`` and asserts equality with
``GENERATED_SOURCE_SHA256`` declared at the top of
``proxmox_sdk/generated/proxmox/latest/pydantic_models.py``.

When the OpenAPI source legitimately changes, regenerate the models and bump
``GENERATED_SOURCE_SHA256`` (and ``GENERATED_AT``) to match the new source.
"""

import hashlib
from pathlib import Path

from proxmox_sdk.generated.proxmox.latest.pydantic_models import (
    GENERATED_AT,
    GENERATED_FOR_PROXMOX_VERSION,
    GENERATED_SOURCE_SHA256,
)

OPENAPI_PATH = (
    Path(__file__).resolve().parent.parent
    / "proxmox_sdk"
    / "generated"
    / "proxmox"
    / "latest"
    / "openapi.json"
)


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def test_generated_constants_are_strings() -> None:
    assert isinstance(GENERATED_FOR_PROXMOX_VERSION, str)
    assert isinstance(GENERATED_SOURCE_SHA256, str)
    assert isinstance(GENERATED_AT, str)
    assert len(GENERATED_SOURCE_SHA256) == 64


def test_openapi_source_matches_generated_sha256() -> None:
    assert OPENAPI_PATH.is_file(), f"missing source spec: {OPENAPI_PATH}"
    actual = _sha256(OPENAPI_PATH)
    assert actual == GENERATED_SOURCE_SHA256, (
        "openapi.json drifted from the SHA-256 pinned in pydantic_models.py.\n"
        "Either regenerate the artifact or update GENERATED_SOURCE_SHA256.\n"
        f"  pinned:   {GENERATED_SOURCE_SHA256}\n"
        f"  computed: {actual}\n"
    )
