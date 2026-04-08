"""Test that all modules can be imported successfully."""


def test_import_main():
    """Test that main module can be imported."""
    import proxmox_openapi.main

    assert proxmox_openapi.main is not None


def test_import_mock_main():
    """Test that mock_main module can be imported."""
    import proxmox_openapi.mock_main

    assert proxmox_openapi.mock_main is not None


def test_import_schema():
    """Test that schema module can be imported."""
    import proxmox_openapi.schema

    assert proxmox_openapi.schema is not None


def test_import_exception():
    """Test that exception module can be imported."""
    import proxmox_openapi.exception

    assert proxmox_openapi.exception is not None


def test_import_logger():
    """Test that logger module can be imported."""
    import proxmox_openapi.logger

    assert proxmox_openapi.logger is not None


# proxmox/ sub-package


def test_import_proxmox_client():
    import proxmox_openapi.proxmox.client

    assert proxmox_openapi.proxmox.client is not None


# sdk/auth/


def test_import_sdk_auth_base():
    import proxmox_openapi.sdk.auth.base

    assert proxmox_openapi.sdk.auth.base is not None


# sdk/backends/


def test_import_sdk_backends_cli_base():
    import proxmox_openapi.sdk.backends._cli_base

    assert proxmox_openapi.sdk.backends._cli_base is not None


# proxmox_cli/ top-level modules


def test_import_proxmox_cli_app():
    import proxmox_openapi.proxmox_cli.app

    assert proxmox_openapi.proxmox_cli.app is not None


def test_import_proxmox_cli_batch():
    import proxmox_openapi.proxmox_cli.batch

    assert proxmox_openapi.proxmox_cli.batch is not None


def test_import_proxmox_cli_cache():
    import proxmox_openapi.proxmox_cli.cache

    assert proxmox_openapi.proxmox_cli.cache is not None


def test_import_proxmox_cli_completion():
    import proxmox_openapi.proxmox_cli.completion

    assert proxmox_openapi.proxmox_cli.completion is not None


def test_import_proxmox_cli_config_commands():
    import proxmox_openapi.proxmox_cli.config_commands

    assert proxmox_openapi.proxmox_cli.config_commands is not None


def test_import_proxmox_cli_doc_commands():
    import proxmox_openapi.proxmox_cli.doc_commands

    assert proxmox_openapi.proxmox_cli.doc_commands is not None


def test_import_proxmox_cli_docgen_capture():
    import proxmox_openapi.proxmox_cli.docgen_capture

    assert proxmox_openapi.proxmox_cli.docgen_capture is not None


def test_import_proxmox_cli_error_suggestions():
    import proxmox_openapi.proxmox_cli.error_suggestions

    assert proxmox_openapi.proxmox_cli.error_suggestions is not None


def test_import_proxmox_cli_exceptions():
    import proxmox_openapi.proxmox_cli.exceptions

    assert proxmox_openapi.proxmox_cli.exceptions is not None


def test_import_proxmox_cli_install():
    import proxmox_openapi.proxmox_cli.install

    assert proxmox_openapi.proxmox_cli.install is not None


def test_import_proxmox_cli_output():
    import proxmox_openapi.proxmox_cli.output

    assert proxmox_openapi.proxmox_cli.output is not None


def test_import_proxmox_cli_performance():
    import proxmox_openapi.proxmox_cli.performance

    assert proxmox_openapi.proxmox_cli.performance is not None


def test_import_proxmox_cli_release():
    import proxmox_openapi.proxmox_cli.release

    assert proxmox_openapi.proxmox_cli.release is not None


def test_import_proxmox_cli_sdk_bridge():
    import proxmox_openapi.proxmox_cli.sdk_bridge

    assert proxmox_openapi.proxmox_cli.sdk_bridge is not None


def test_import_proxmox_cli_tui_runner():
    import proxmox_openapi.proxmox_cli.tui_runner

    assert proxmox_openapi.proxmox_cli.tui_runner is not None


def test_import_proxmox_cli_utils():
    import proxmox_openapi.proxmox_cli.utils

    assert proxmox_openapi.proxmox_cli.utils is not None


# proxmox_cli/commands/


def test_import_proxmox_cli_commands_common():
    import proxmox_openapi.proxmox_cli.commands._common

    assert proxmox_openapi.proxmox_cli.commands._common is not None


def test_import_proxmox_cli_commands_create():
    import proxmox_openapi.proxmox_cli.commands.create

    assert proxmox_openapi.proxmox_cli.commands.create is not None


def test_import_proxmox_cli_commands_delete():
    import proxmox_openapi.proxmox_cli.commands.delete

    assert proxmox_openapi.proxmox_cli.commands.delete is not None


def test_import_proxmox_cli_commands_get():
    import proxmox_openapi.proxmox_cli.commands.get

    assert proxmox_openapi.proxmox_cli.commands.get is not None


def test_import_proxmox_cli_commands_help():
    import proxmox_openapi.proxmox_cli.commands.help

    assert proxmox_openapi.proxmox_cli.commands.help is not None


def test_import_proxmox_cli_commands_ls():
    import proxmox_openapi.proxmox_cli.commands.ls

    assert proxmox_openapi.proxmox_cli.commands.ls is not None


def test_import_proxmox_cli_commands_set():
    import proxmox_openapi.proxmox_cli.commands.set

    assert proxmox_openapi.proxmox_cli.commands.set is not None


def test_import_proxmox_cli_commands_tui():
    import proxmox_openapi.proxmox_cli.commands.tui

    assert proxmox_openapi.proxmox_cli.commands.tui is not None


def test_import_proxmox_cli_commands_usage():
    import proxmox_openapi.proxmox_cli.commands.usage

    assert proxmox_openapi.proxmox_cli.commands.usage is not None


# proxmox_cli/docgen/


def test_import_proxmox_cli_docgen_discovery():
    import proxmox_openapi.proxmox_cli.docgen.discovery

    assert proxmox_openapi.proxmox_cli.docgen.discovery is not None


def test_import_proxmox_cli_docgen_engine():
    import proxmox_openapi.proxmox_cli.docgen.engine

    assert proxmox_openapi.proxmox_cli.docgen.engine is not None


def test_import_proxmox_cli_docgen_models():
    import proxmox_openapi.proxmox_cli.docgen.models

    assert proxmox_openapi.proxmox_cli.docgen.models is not None


def test_import_proxmox_cli_docgen_specs():
    import proxmox_openapi.proxmox_cli.docgen.specs

    assert proxmox_openapi.proxmox_cli.docgen.specs is not None
