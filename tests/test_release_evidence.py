"""Tests for the public release-evidence gate."""

from __future__ import annotations

import pytest

from tests import verify_release_evidence as evidence

MANIFEST_SHA256 = "a" * 64


def _body() -> str:
    items = "\n".join(f"- [x] **{item}**: recorded evidence" for item in evidence.REQUIRED_ITEMS)
    return (
        f"{evidence.MARKER}\n\n## Release evidence\n\n"
        f"Release version: `1.2.3`\n"
        f"Package-of-record manifest SHA256: `{MANIFEST_SHA256}`\n\n{items}\n"
    )


def test_complete_release_evidence_passes() -> None:
    evidence.verify_release_body(
        _body(),
        version="1.2.3",
        distribution_manifest_sha256=MANIFEST_SHA256,
    )


@pytest.mark.parametrize(
    "replacement",
    [
        ("- [x] **REQ**:", "- [ ] **REQ**:"),
        ("- [x] **TEST**: recorded evidence", ""),
        ("recorded evidence", "See Gitea issue #22"),
        ("Release version: `1.2.3`", "Release version: `9.9.9`"),
        (MANIFEST_SHA256, "b" * 64),
        ("Package-of-record manifest SHA256:", "Package manifest:"),
    ],
)
def test_incomplete_or_internal_release_evidence_fails(replacement: tuple[str, str]) -> None:
    old, new = replacement
    with pytest.raises(evidence.ReleaseEvidenceError):
        evidence.verify_release_body(
            _body().replace(old, new),
            version="1.2.3",
            distribution_manifest_sha256=MANIFEST_SHA256,
        )
