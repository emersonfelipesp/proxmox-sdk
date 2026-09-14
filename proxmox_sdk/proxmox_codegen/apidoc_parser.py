"""Parser utilities for Proxmox API viewer `apidoc.js` payloads."""

from __future__ import annotations

import json
import ssl
import warnings
from typing import Any
from urllib.error import URLError
from urllib.request import HTTPErrorProcessor, HTTPSHandler, Request, build_opener

from proxmox_sdk.sdk.exceptions import ProxmoxRedirectError

PROXMOX_API_VIEWER_URL = "https://pve.proxmox.com/pve-docs/api-viewer/"
PROXMOX_APIDOC_JS_URL = "https://pve.proxmox.com/pve-docs/api-viewer/apidoc.js"

PDM_API_VIEWER_URL = "https://pdm.proxmox.com/docs/api-viewer/"
PDM_APIDOC_JS_URL = "https://pdm.proxmox.com/docs/api-viewer/apidoc.js"


class _RefuseRedirects(HTTPErrorProcessor):
    """Reject every urllib 3xx response before redirect handling or body reads."""

    def http_response(self, request: Any, response: Any) -> Any:
        if 300 <= response.code < 400:
            status = response.code
            location = response.headers.get("Location")
            response.close()
            raise ProxmoxRedirectError(status, location)
        return super().http_response(request, response)

    https_response = http_response


def _open_url(
    url: str | Request,
    timeout: int,
    *,
    context: ssl.SSLContext | None = None,
) -> Any:
    """Open ``url`` with redirect following disabled."""
    handlers: list[Any] = [_RefuseRedirects()]
    if context is not None:
        handlers.append(HTTPSHandler(context=context))
    return build_opener(*handlers).open(url, timeout=timeout)


def fetch_apidoc_js(
    url: str | Request = PROXMOX_APIDOC_JS_URL,
    timeout: int = 60,
    allow_insecure: bool = False,
) -> str:
    """Download the upstream Proxmox `apidoc.js` source file.

    Args:
        url: URL or prepared urllib request for the apidoc.js file.
        timeout: Request timeout in seconds.
        allow_insecure: If True, retry with SSL verification disabled when the
            initial request fails due to an SSL error. This should only be used
            in controlled/offline environments. Emits a :class:`UserWarning`
            when active. Defaults to False.

    Raises:
        URLError: On network errors, or SSL errors when ``allow_insecure=False``.
        ProxmoxRedirectError: If the endpoint returns any HTTP 3xx response,
            including ``304 Not Modified``.
    """
    try:
        with _open_url(url, timeout) as response:
            return response.read().decode("utf-8")
    except URLError as error:
        if not isinstance(getattr(error, "reason", None), ssl.SSLError):
            raise
        if not allow_insecure:
            raise URLError(
                f"SSL verification failed for {url!r}. "
                "If you are fetching from a host with a self-signed certificate, "
                "pass allow_insecure=True (NOT recommended for production)."
            ) from error
        warnings.warn(
            f"SSL verification disabled for {url!r}. "
            "This bypasses certificate validation and should only be used in "
            "trusted/offline environments.",
            UserWarning,
            stacklevel=2,
        )
        insecure_context = ssl.create_default_context()
        insecure_context.check_hostname = False
        insecure_context.verify_mode = ssl.CERT_NONE
        with _open_url(url, timeout, context=insecure_context) as response:
            return response.read().decode("utf-8")


def extract_api_schema_text(apidoc_source: str) -> str:  # noqa: C901
    """Extract the JSON array literal assigned to ``apiSchema = [...]``.

    Supports both ``const apiSchema =`` (PVE/PBS/PMG) and ``var apiSchema =``
    (PDM) declaration styles.
    """

    marker_index = -1
    for marker in ("const apiSchema =", "var apiSchema ="):
        marker_index = apidoc_source.find(marker)
        if marker_index >= 0:
            break
    if marker_index < 0:
        raise ValueError(
            "Unable to locate `const apiSchema =` or `var apiSchema =` marker in apidoc source."
        )

    start_index = apidoc_source.find("[", marker_index)
    if start_index < 0:
        raise ValueError("Unable to find start array token `[` for apiSchema.")

    depth = 0
    in_string = False
    escaped = False
    end_index = -1

    for idx in range(start_index, len(apidoc_source)):
        char = apidoc_source[idx]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue

        if char == '"':
            in_string = True
            continue

        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                end_index = idx
                break

    if end_index < 0:
        raise ValueError("Unable to find matching closing bracket for apiSchema array.")

    return apidoc_source[start_index : end_index + 1]


def parse_api_schema(apidoc_source: str) -> list[dict[str, object]]:
    """Parse Proxmox API viewer schema tree from `apidoc.js` source."""

    schema_text = extract_api_schema_text(apidoc_source)
    parsed = json.loads(schema_text)
    if not isinstance(parsed, list):
        raise ValueError("Parsed apiSchema is not a list.")
    return parsed


def flatten_api_schema(schema_tree: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    """Flatten tree nodes into a path-keyed endpoint map."""

    output: dict[str, dict[str, object]] = {}

    def walk(node: dict[str, object]) -> None:
        path = node.get("path")
        if path:
            output[path] = {
                "path": path,
                "text": node.get("text"),
                "leaf": node.get("leaf"),
                "info": node.get("info", {}),
            }
        for child in node.get("children", []) or []:
            walk(child)

    for root in schema_tree:
        walk(root)

    return output


__all__ = [
    "PROXMOX_API_VIEWER_URL",
    "PROXMOX_APIDOC_JS_URL",
    "PDM_API_VIEWER_URL",
    "PDM_APIDOC_JS_URL",
    "fetch_apidoc_js",
    "extract_api_schema_text",
    "parse_api_schema",
    "flatten_api_schema",
]
