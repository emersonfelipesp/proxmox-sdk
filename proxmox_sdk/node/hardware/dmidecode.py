"""Parsers for ``dmidecode -t 1`` (system) and ``dmidecode -t 3`` (chassis).

``dmidecode`` output is line-oriented and indented with tabs/spaces. Sections
are separated by blank lines and start with a ``Handle 0x...`` line followed
by the section title (e.g. ``System Information``, ``Chassis Information``).
Field lines look like ``\\tKey: Value`` (one tab, key, colon, space, value).

The parsers are intentionally forgiving:

* They tolerate ``# dmidecode 3.x`` header lines, ``SMBIOS ... present.``
  banners, and ``Getting SMBIOS data from sysfs.`` chatter that always precede
  real sections.
* They tolerate missing fields (``Not Specified``, ``To Be Filled By O.E.M.``)
  by mapping them to ``None`` rather than the literal sentinel.
* They tolerate multiple sections of the same type (some servers report two
  chassis sections) by using the first match.
"""

from __future__ import annotations

import re
from collections.abc import Iterable

from proxmox_sdk.node.hardware.facts import ChassisFacts, SystemFacts

_PLACEHOLDER_VALUES: frozenset[str] = frozenset(
    s.lower()
    for s in (
        "",
        "not specified",
        "not present",
        "to be filled by o.e.m.",
        "system manufacturer",
        "system product name",
        "system serial number",
        "system version",
        "default string",
        "0",
        "none",
        "unknown",
    )
)

_HEIGHT_RE = re.compile(r"(?P<n>\d+)\s*U", re.IGNORECASE)


def _clean(value: str | None) -> str | None:
    if value is None:
        return None
    s = value.strip()
    if s.lower() in _PLACEHOLDER_VALUES:
        return None
    return s


def _iter_sections(text: str) -> Iterable[tuple[str, dict[str, str]]]:
    """Yield ``(section_title, {key: value})`` for each dmidecode section."""
    lines = text.splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # A section starts on the line *after* a "Handle 0x..." line.
        if line.startswith("Handle "):
            i += 1
            if i >= n:
                break
            title = lines[i].strip()
            i += 1
            fields: dict[str, str] = {}
            while i < n:
                row = lines[i]
                if not row.strip():
                    break
                # Field lines are indented; non-indented lines that aren't a
                # handle are section trailers (e.g. "Contained Elements").
                stripped = row.lstrip("\t ")
                if stripped == row:
                    # Not indented: end of section unless it's a continuation.
                    break
                if ":" in stripped:
                    key, _, val = stripped.partition(":")
                    fields[key.strip()] = val.strip()
                # else: lines like "Description: foo" sub-items — ignored.
                i += 1
            if title:
                yield title, fields
        else:
            i += 1


def _parse_height_u(value: str | None) -> int | None:
    if not value:
        return None
    m = _HEIGHT_RE.search(value)
    if not m:
        return None
    try:
        return int(m.group("n"))
    except ValueError:  # pragma: no cover - regex guarantees \d+
        return None


def parse_dmidecode_system(text: str) -> SystemFacts:
    """Parse ``dmidecode -t 1`` output into :class:`SystemFacts`."""
    for title, fields in _iter_sections(text):
        if title == "System Information":
            return SystemFacts(
                manufacturer=_clean(fields.get("Manufacturer")),
                product_name=_clean(fields.get("Product Name")),
                serial_number=_clean(fields.get("Serial Number")),
                uuid=_clean(fields.get("UUID")),
                sku_number=_clean(fields.get("SKU Number")),
                family=_clean(fields.get("Family")),
                version=_clean(fields.get("Version")),
            )
    return SystemFacts()


def parse_dmidecode_chassis(text: str) -> ChassisFacts:
    """Parse ``dmidecode -t 3`` output into :class:`ChassisFacts`."""
    for title, fields in _iter_sections(text):
        if title == "Chassis Information":
            return ChassisFacts(
                manufacturer=_clean(fields.get("Manufacturer")),
                type=_clean(fields.get("Type")),
                serial_number=_clean(fields.get("Serial Number")),
                version=_clean(fields.get("Version")),
                asset_tag=_clean(fields.get("Asset Tag")),
                height_u=_parse_height_u(fields.get("Height")),
                sku_number=_clean(fields.get("SKU Number")),
            )
    return ChassisFacts()


__all__ = ["parse_dmidecode_chassis", "parse_dmidecode_system"]
