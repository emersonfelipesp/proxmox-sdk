"""Run CLI commands via subprocess and write capture artifacts."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, TextIO

from .models import build_slug, truncate
from .specs import load_all_capture_specs


def resolve_proxmox_command() -> list[str]:
    """Resolve the proxmox executable used during capture."""
    exe = os.environ.get("PROXMOX_DOCGEN_EXE", "").strip()
    if exe:
        return [exe]
    found = shutil.which("proxmox")
    if found:
        return [found]
    return [sys.executable, "-m", "proxmox_sdk.proxmox_cli.cli"]


def invoke_proxmox_subprocess(
    spec_argv: list[str],
    *,
    timeout: float = 120.0,
) -> tuple[int, str, float]:
    """Execute one proxmox CLI invocation and return status/output/time."""
    cmd = [*resolve_proxmox_command(), *spec_argv]
    env = os.environ.copy()
    env.setdefault("NO_COLOR", "1")
    env.setdefault("TERM", "dumb")

    started = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.perf_counter() - started
        return 124, "--- timeout ---\n(subprocess capture exceeded limit)\n", elapsed
    except Exception as exc:
        elapsed = time.perf_counter() - started
        return 1, f"--- exception ---\n{type(exc).__name__}: {exc}\n", elapsed

    elapsed = time.perf_counter() - started
    out = proc.stdout or ""
    err = proc.stderr or ""
    if err.strip():
        out = f"{out}\n--- stderr ---\n{err}" if out.strip() else f"--- stderr ---\n{err}"
    return proc.returncode, out, elapsed


def generate_command_capture_docs(
    *,
    output: Path,
    raw_dir: Path,
    max_lines: int = 200,
    max_chars: int = 120_000,
    log: TextIO | None = None,
) -> int:
    """Write capture Markdown plus raw JSON artifacts."""
    log = log or sys.stderr
    output.parent.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "proxmox_invocation": resolve_proxmox_command(),
    }

    lines: list[str] = [
        "# Proxmox CLI - captured command input and output",
        "",
        "This file is machine-generated. Regenerate with:",
        "",
        "```bash",
        "cd /path/to/proxmox-sdk",
        "uv sync --group dev --group docs --extra cli",
        "uv run proxmox docs generate-capture",
        "# or: uv run python docs/generate_command_docs.py",
        "```",
        "",
        "## Generation metadata",
        "",
        f"- **UTC time:** `{meta['generated_at']}`",
        f"- **Subprocess command:** `{' '.join(meta['proxmox_invocation'])}`",
        "",
        "---",
        "",
    ]

    section_last = ""
    artifacts: list[dict[str, Any]] = []

    for spec in load_all_capture_specs():
        if spec.section != section_last:
            lines.append(f"## {spec.section}")
            lines.append("")
            section_last = spec.section

        cmd_display = "proxmox " + " ".join(spec.argv)
        code, out, elapsed = invoke_proxmox_subprocess(spec.argv)
        truncated, did_trunc = truncate(out, max_lines, max_chars)
        slug = build_slug(spec.section, spec.title)

        art_core = {
            "section": spec.section,
            "title": spec.title,
            "argv": list(spec.argv),
            "exit_code": code,
            "elapsed_seconds": round(elapsed, 3),
            "truncated": did_trunc,
        }
        artifacts.append(art_core)

        art_path = raw_dir / f"{len(artifacts):03d}-{slug}.json"
        art_path.write_text(
            json.dumps({**art_core, "stdout_full": out}, indent=2),
            encoding="utf-8",
        )

        lines.append(f"### {spec.title}")
        lines.append("")
        lines.append("**Input:**")
        lines.append("")
        lines.append("```bash")
        lines.append(cmd_display)
        lines.append("```")
        lines.append("")
        lines.append(f"**Exit code:** `{code}`  ·  **Wall time (s):** `{elapsed:.3f}`")
        if did_trunc:
            lines.append("")
            lines.append(
                f"*Output truncated for this doc (max {max_lines} lines / {max_chars} chars).*"
            )
        lines.append("")
        lines.append("**Output:**")
        lines.append("")
        lines.append("```text")
        lines.append(truncated.rstrip() or "(empty)")
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    (raw_dir / "index.json").write_text(
        json.dumps({"meta": meta, "runs": artifacts}, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {output}", file=log)
    print(f"Wrote {len(artifacts)} raw JSON files under {raw_dir}", file=log)
    return 0
