"""Verify runtime schema contracts from a built proxmox-sdk wheel.

This file is an executable CI/release verifier rather than a pytest module.
It deliberately imports the extracted wheel from a temporary directory so an
editable source checkout cannot hide missing package data.
"""

from __future__ import annotations

import os
import stat
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

PDM_OPENAPI_MEMBER = "proxmox_sdk/generated/pdm/latest/openapi.json"

_INSTALLED_WHEEL_SMOKE = r"""
import asyncio
import os
from pathlib import Path

import proxmox_sdk
from proxmox_sdk.pdm import PDMClient
from proxmox_sdk.pdm.models import PDMRemote, PDMRemoteNode, PDMVersion
from proxmox_sdk.schema import available_pdm_sdk_versions, load_pdm_generated_openapi

expected_root = Path(os.environ["PROXMOX_SDK_WHEEL_ROOT"]).resolve()
package_file = Path(proxmox_sdk.__file__).resolve()
if not package_file.is_relative_to(expected_root):
    raise AssertionError(
        f"Imported proxmox_sdk from {package_file}, expected extracted wheel {expected_root}"
    )

versions = available_pdm_sdk_versions()
if "latest" not in versions:
    raise AssertionError(f"Packaged PDM versions do not include 'latest': {versions!r}")

schema = load_pdm_generated_openapi()
paths = schema.get("paths") if isinstance(schema, dict) else None
required_paths = {"/version", "/remotes/remote"}
if not isinstance(paths, dict) or not required_paths.issubset(paths):
    raise AssertionError(
        f"Packaged PDM OpenAPI schema lacks required paths: {required_paths!r}"
    )


async def smoke_pdm_client() -> None:
    client = PDMClient.mock()
    try:
        version = await client.version()
        if not isinstance(version, PDMVersion) or not version.version:
            raise AssertionError(f"PDM mock version is not typed/populated: {version!r}")
        remotes = await client.remotes.list()
        if not remotes or not all(isinstance(remote, PDMRemote) for remote in remotes):
            raise AssertionError(f"PDM mock remotes are not typed/populated: {remotes!r}")
        if not all(
            remote.nodes is None
            or all(isinstance(node, PDMRemoteNode) for node in remote.nodes)
            for remote in remotes
        ):
            raise AssertionError(f"PDM mock remote nodes are not typed: {remotes!r}")
    finally:
        await client.close()


asyncio.run(smoke_pdm_client())
"""


class WheelContractError(RuntimeError):
    """Raised when a built wheel does not satisfy its runtime schema contract."""


def _validate_member_path(info: zipfile.ZipInfo) -> None:
    """Reject unsafe archive members before extraction."""

    path = PurePosixPath(info.filename)
    if path.is_absolute() or ".." in path.parts:
        raise WheelContractError(f"Wheel contains an unsafe path: {info.filename!r}")
    mode = info.external_attr >> 16
    if stat.S_ISLNK(mode):
        raise WheelContractError(f"Wheel contains an unsupported symlink: {info.filename!r}")


def verify_wheel(wheel_path: Path) -> None:
    """Inspect and execute the PDM contract from one built wheel."""

    if not wheel_path.is_file() or wheel_path.suffix != ".whl":
        raise WheelContractError(f"Expected a wheel file, got {wheel_path}")

    with tempfile.TemporaryDirectory(prefix="proxmox-sdk-wheel-") as temp_dir:
        extracted_root = Path(temp_dir)
        with zipfile.ZipFile(wheel_path) as archive:
            members = archive.infolist()
            names = {info.filename for info in members}
            if PDM_OPENAPI_MEMBER not in names:
                raise WheelContractError(f"{wheel_path.name} does not contain {PDM_OPENAPI_MEMBER}")
            for info in members:
                _validate_member_path(info)
            archive.extractall(extracted_root)

        env = os.environ.copy()
        env.update(
            {
                "PROXMOX_SDK_WHEEL_ROOT": str(extracted_root),
                "PROXMOX_MOCK_STATE_PATH": str(extracted_root / "pdm-mock.sqlite3"),
                "PROXMOX_MOCK_STATE_NAMESPACE": "wheel_contract_pdm",
                "PROXMOX_MOCK_STORE": "dict",
                "PYTHONDONTWRITEBYTECODE": "1",
                "PYTHONNOUSERSITE": "1",
                "PYTHONPATH": str(extracted_root),
            }
        )
        completed = subprocess.run(
            [sys.executable, "-c", _INSTALLED_WHEEL_SMOKE],
            cwd=extracted_root,
            env=env,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            details = "\n".join(
                part.strip() for part in (completed.stdout, completed.stderr) if part.strip()
            )
            raise WheelContractError(
                f"Installed-wheel PDM smoke failed for {wheel_path.name}:\n{details}"
            )


def main(argv: list[str] | None = None) -> int:
    """Validate exactly one wheel supplied on the command line."""

    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 1:
        raise WheelContractError(
            "Usage: python tests/verify_wheel_contract.py path/to/proxmox_sdk.whl"
        )
    wheel_path = Path(arguments[0]).resolve()
    verify_wheel(wheel_path)
    print(f"Verified installed-wheel PDM contract: {wheel_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
