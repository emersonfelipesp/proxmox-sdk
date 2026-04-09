"""Dataclasses and helpers used by the CLI doc capture pipeline."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CaptureSpec:
    """One CLI invocation to execute and capture."""

    section: str
    title: str
    argv: list[str]
    notes: str = ""


@dataclass(slots=True)
class CaptureRunMeta:
    """Metadata for one completed capture run."""

    section: str
    title: str
    argv: list[str]
    exit_code: int
    elapsed_seconds: float
    truncated: bool


def build_slug(section: str, title: str, max_len: int = 80) -> str:
    """Create a filesystem-safe slug from section and title."""
    raw = f"{section}-{title}"[:max_len].lower().replace(" ", "-").replace("/", "-")
    slug = "".join(c if c.isalnum() or c == "-" else "-" for c in raw)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "capture"


def truncate(text: str, max_lines: int, max_chars: int) -> tuple[str, bool]:
    """Truncate output text for Markdown rendering only."""
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n... (truncated by character limit)\n", True
    lines = text.splitlines()
    if len(lines) > max_lines:
        head = "\n".join(lines[:max_lines])
        hidden = len(lines) - max_lines
        return head + f"\n\n... ({hidden} more lines truncated)\n", True
    return text, False
