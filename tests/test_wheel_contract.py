"""Security regressions for the installed-wheel verifier."""

from __future__ import annotations

import stat
import zipfile

import pytest

from tests.verify_wheel_contract import WheelContractError, _validate_member_path


@pytest.mark.parametrize(
    "member_name", ["../outside.py", "package/../../outside.py", "/absolute.py"]
)
def test_wheel_contract_rejects_unsafe_member_paths(member_name: str) -> None:
    with pytest.raises(WheelContractError, match="unsafe path"):
        _validate_member_path(zipfile.ZipInfo(member_name))


def test_wheel_contract_rejects_symlink_members() -> None:
    member = zipfile.ZipInfo("proxmox_sdk/generated/pdm/latest/openapi.json")
    member.create_system = 3
    member.external_attr = (stat.S_IFLNK | 0o777) << 16

    with pytest.raises(WheelContractError, match="unsupported symlink"):
        _validate_member_path(member)


def test_wheel_contract_accepts_regular_package_members() -> None:
    member = zipfile.ZipInfo("proxmox_sdk/generated/pdm/latest/openapi.json")
    member.create_system = 3
    member.external_attr = (stat.S_IFREG | 0o644) << 16

    _validate_member_path(member)
