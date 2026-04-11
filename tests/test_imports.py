"""Test that all modules can be imported successfully."""

import importlib

import pytest


@pytest.mark.parametrize(
    "module_path",
    [
        "proxmox_sdk.main",
        "proxmox_sdk.mock_main",
        "proxmox_sdk.schema",
        "proxmox_sdk.exception",
        "proxmox_sdk.logger",
        # proxmox/
        "proxmox_sdk.proxmox.client",
        # sdk/auth/
        "proxmox_sdk.sdk.auth.base",
        # sdk/backends/
        "proxmox_sdk.sdk.backends._cli_base",
        # proxmox_cli/
        "proxmox_sdk.proxmox_cli.app",
        "proxmox_sdk.proxmox_cli.batch",
        "proxmox_sdk.proxmox_cli.cache",
        "proxmox_sdk.proxmox_cli.completion",
        "proxmox_sdk.proxmox_cli.config_commands",
        "proxmox_sdk.proxmox_cli.doc_commands",
        "proxmox_sdk.proxmox_cli.docgen_capture",
        "proxmox_sdk.proxmox_cli.exceptions",
        "proxmox_sdk.proxmox_cli.install",
        "proxmox_sdk.proxmox_cli.output",
        "proxmox_sdk.proxmox_cli.performance",
        "proxmox_sdk.proxmox_cli.release",
        "proxmox_sdk.proxmox_cli.sdk_bridge",
        "proxmox_sdk.proxmox_cli.tui_runner",
        "proxmox_sdk.proxmox_cli.utils",
        # proxmox_cli/commands/
        "proxmox_sdk.proxmox_cli.commands._common",
        "proxmox_sdk.proxmox_cli.commands.create",
        "proxmox_sdk.proxmox_cli.commands.delete",
        "proxmox_sdk.proxmox_cli.commands.get",
        "proxmox_sdk.proxmox_cli.commands.help",
        "proxmox_sdk.proxmox_cli.commands.ls",
        "proxmox_sdk.proxmox_cli.commands.set",
        "proxmox_sdk.proxmox_cli.commands.tui",
        "proxmox_sdk.proxmox_cli.commands.usage",
        # proxmox_cli/docgen/
        "proxmox_sdk.proxmox_cli.docgen.discovery",
        "proxmox_sdk.proxmox_cli.docgen.engine",
        "proxmox_sdk.proxmox_cli.docgen.models",
        "proxmox_sdk.proxmox_cli.docgen.specs",
    ],
)
def test_import(module_path: str) -> None:
    mod = importlib.import_module(module_path)
    assert mod is not None
