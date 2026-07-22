"""Source-level guards for the built-package schema contract."""

from __future__ import annotations

import tomllib
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def test_pdm_generated_artifacts_are_declared_as_package_data() -> None:
    config = tomllib.loads((REPOSITORY_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_data = config["tool"]["setuptools"]["package-data"]["proxmox_sdk"]

    assert "generated/pdm/**/*.json" in package_data
    assert "generated/pdm/**/*.py" in package_data
    assert (REPOSITORY_ROOT / "proxmox_sdk/generated/pdm/latest/openapi.json").is_file()
