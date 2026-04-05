"""Public facade for Proxmox CLI documentation capture."""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

from .docgen.engine import generate_command_capture_docs as _generate_command_capture_docs


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def resolve_capture_paths(output: Path | None, raw_dir: Path | None) -> tuple[Path, Path]:
    """Resolve default output paths under docs/generated when available."""
    docs_dir = _repo_root() / "docs"
    default_out = docs_dir / "generated" / "proxmox-command-capture.md"

    if not docs_dir.is_dir():
        if output is None or raw_dir is None:
            raise FileNotFoundError(
                "Cannot infer default paths: no docs/ directory next to proxmox_openapi. "
                "Run from the proxmox-openapi checkout or pass --output and --raw-dir."
            )
        return output, raw_dir

    if output is None:
        output = default_out
    if raw_dir is None:
        raw_dir = output.parent / "raw"
    return output, raw_dir


def generate_command_capture_docs(
    *,
    output: Path,
    raw_dir: Path,
    max_lines: int = 200,
    max_chars: int = 120_000,
    log: TextIO | None = None,
) -> int:
    """Write capture markdown and raw artifacts. Returns process exit code."""
    return _generate_command_capture_docs(
        output=output,
        raw_dir=raw_dir,
        max_lines=max_lines,
        max_chars=max_chars,
        log=log,
    )
