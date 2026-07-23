"""Validate the product-facing release evidence required before public promotion."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

MARKER = "<!-- proxmox-sdk-release-evidence:v1 -->"
REQUIRED_ITEMS = (
    "REQ",
    "ARCH",
    "IMPL",
    "STATIC",
    "TEST",
    "COVERAGE",
    "DEFECTS",
    "SECURITY",
    "OPS",
    "RECOVERY",
    "APPROVAL",
)
_INTERNAL_REFERENCE = re.compile(
    r"git\.nmulti\.cloud|\bgitea\b|\b(?:issue|pr)\s*#\d+\b",
    re.IGNORECASE,
)


class ReleaseEvidenceError(RuntimeError):
    """Raised when required release evidence is missing or unsafe to publish."""


def verify_release_body(
    body: str,
    *,
    version: str,
    distribution_manifest_sha256: str,
) -> None:
    """Require a complete NASA-aligned checklist without internal references."""

    if MARKER not in body:
        raise ReleaseEvidenceError(f"Missing release evidence marker: {MARKER}")
    if f"Release version: `{version}`" not in body:
        raise ReleaseEvidenceError(f"Release evidence does not identify version {version}")
    manifest_match = re.search(
        r"(?m)^Package-of-record manifest SHA256: `([0-9a-f]{64})`\s*$",
        body,
    )
    if manifest_match is None:
        raise ReleaseEvidenceError("Release evidence has no valid package-record manifest SHA256")
    if manifest_match.group(1) != distribution_manifest_sha256:
        raise ReleaseEvidenceError(
            "Package-record manifest SHA256 does not match the rebuilt distribution manifest"
        )
    if _INTERNAL_REFERENCE.search(body):
        raise ReleaseEvidenceError("Release evidence contains a blocked internal reference")
    if re.search(r"(?m)^\s*-\s*\[\s\]", body):
        raise ReleaseEvidenceError("Release evidence contains an incomplete checkbox")

    missing = [
        item
        for item in REQUIRED_ITEMS
        if re.search(
            rf"(?m)^\s*-\s*\[[xX]\]\s*\*\*{re.escape(item)}\*\*:\s*\S",
            body,
        )
        is None
    ]
    if missing:
        raise ReleaseEvidenceError(f"Missing completed release evidence items: {missing}")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--body-file", type=Path, required=True)
    parser.add_argument("--distribution-manifest", type=Path, required=True)
    parser.add_argument("--version", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Validate a release body file."""

    args = _parse_args(list(sys.argv[1:] if argv is None else argv))
    body = args.body_file.read_text(encoding="utf-8")
    manifest_sha256 = hashlib.sha256(args.distribution_manifest.read_bytes()).hexdigest()
    verify_release_body(
        body,
        version=args.version,
        distribution_manifest_sha256=manifest_sha256,
    )
    print(f"Release evidence is complete for {args.version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
