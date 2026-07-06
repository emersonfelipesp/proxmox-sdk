"""Regression tests: config CLI commands must load existing config before use.

Previously ``config-add`` / ``config-remove`` / ``config-set-default`` created a
fresh empty ``ConfigManager`` and then ``save_config()``, silently overwriting
the file and dropping every other profile. ``batch`` likewise never loaded the
config, so it ignored the configured default profile.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from proxmox_sdk.proxmox_cli.cli import app
from proxmox_sdk.proxmox_cli.config import BackendConfig, ConfigManager


def _seed_profile(cfg_path: Path, name: str, host: str) -> None:
    mgr = ConfigManager()
    mgr.add_profile(name, BackendConfig(name=name, host=host, user="root@pam"))
    mgr.save_config(cfg_path)


def test_config_add_preserves_existing_profiles(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = tmp_path / "config.json"
    monkeypatch.setattr(ConfigManager, "DEFAULT_CONFIG_PATHS", [cfg])
    _seed_profile(cfg, "prod", "prod.example.com")

    result = CliRunner().invoke(
        app,
        ["config-add", "dev", "--host", "dev.example.com", "--user", "admin@pam"],
    )
    assert result.exit_code == 0, result.output

    profiles = json.loads(cfg.read_text())["profiles"]
    assert "prod" in profiles  # would be dropped without the load-before-save fix
    assert "dev" in profiles


def test_config_remove_preserves_other_profiles(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = tmp_path / "config.json"
    monkeypatch.setattr(ConfigManager, "DEFAULT_CONFIG_PATHS", [cfg])
    _seed_profile(cfg, "prod", "prod.example.com")
    # add a second profile through the manager
    mgr = ConfigManager()
    mgr.load_config()
    mgr.add_profile("staging", BackendConfig(name="staging", host="staging.example.com"))
    mgr.save_config()

    result = CliRunner().invoke(app, ["config-remove", "staging"], input="y\n")
    assert result.exit_code == 0, result.output

    profiles = json.loads(cfg.read_text())["profiles"]
    assert "prod" in profiles  # survivor must remain
    assert "staging" not in profiles


def test_config_list_reads_existing_profiles(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = tmp_path / "config.json"
    monkeypatch.setattr(ConfigManager, "DEFAULT_CONFIG_PATHS", [cfg])
    _seed_profile(cfg, "prod", "prod.example.com")

    result = CliRunner().invoke(app, ["config-list", "--json"])
    assert result.exit_code == 0, result.output
    assert "prod" in result.output  # empty without the load fix


def test_batch_uses_configured_default_profile(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cfg = tmp_path / "config.json"
    monkeypatch.setattr(ConfigManager, "DEFAULT_CONFIG_PATHS", [cfg])
    _seed_profile(cfg, "default", "configured.example.com")

    captured: dict[str, object] = {}

    class _DummyBridge:
        def close(self) -> None: ...

    def _fake_create(config: BackendConfig) -> _DummyBridge:
        captured["host"] = config.host
        return _DummyBridge()

    monkeypatch.setattr(
        "proxmox_sdk.proxmox_cli.batch.ProxmoxSDKBridge.create", staticmethod(_fake_create)
    )

    batch_file = tmp_path / "ops.json"
    batch_file.write_text(json.dumps({"operations": [{"action": "get", "path": "/nodes"}]}))

    result = CliRunner().invoke(app, ["batch", str(batch_file), "--dry-run"])
    assert result.exit_code == 0, result.output
    # Without loading config, host would be the empty-profile default, not this.
    assert captured["host"] == "configured.example.com"
