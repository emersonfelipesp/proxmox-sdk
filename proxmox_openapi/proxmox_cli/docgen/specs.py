"""Load capture specifications for CLI doc generation."""

from __future__ import annotations

from .discovery import iter_discovered_help_specs
from .models import CaptureSpec


def load_all_capture_specs() -> list[CaptureSpec]:
    """Return all capture specs discovered from the current CLI tree."""
    return iter_discovered_help_specs()
