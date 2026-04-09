"""Discover all CLI --help paths by walking the Typer/Click command tree."""

from __future__ import annotations

import click
from typer.main import get_command

from proxmox_sdk.proxmox_cli.cli import app as proxmox_app

from .models import CaptureSpec


def _section_for_prefix(prefix: list[str]) -> str:
    if not prefix:
        return "Top-level"
    return prefix[0].replace("-", " ").title()


def _title_for_argv(argv: list[str]) -> str:
    return "proxmox " + " ".join(argv)


def iter_discovered_help_specs(root_app: object | None = None) -> list[CaptureSpec]:
    """Return one capture spec per command/group, each ending with ``--help``."""
    typer_app = root_app if root_app is not None else proxmox_app
    group = get_command(typer_app)
    if not isinstance(group, click.Group):
        return []

    def walk(g: click.Group, prefix: list[str]) -> list[CaptureSpec]:
        rows: list[CaptureSpec] = [
            CaptureSpec(
                section=_section_for_prefix(prefix),
                title=_title_for_argv(prefix + ["--help"]),
                argv=prefix + ["--help"],
            )
        ]
        for name in sorted(g.commands):
            cmd = g.commands[name]
            path = prefix + [name]
            if isinstance(cmd, click.Group):
                rows.extend(walk(cmd, path))
            else:
                rows.append(
                    CaptureSpec(
                        section=_section_for_prefix(path),
                        title=_title_for_argv(path + ["--help"]),
                        argv=path + ["--help"],
                    )
                )
        return rows

    return walk(group, [])
