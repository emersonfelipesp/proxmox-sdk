"""File upload and download utilities for Proxmox storage."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

import aiohttp

if TYPE_CHECKING:
    from proxmox_sdk.sdk.resource import ProxmoxResource

logger = logging.getLogger(__name__)

# Checksum algorithms ordered by preference (strongest first)
_CHECKSUM_ALGORITHMS = ["sha512", "sha256", "sha224", "sha384", "md5", "sha1"]

_HASHLIB_MAP = {
    "sha512": hashlib.sha512,
    "sha256": hashlib.sha256,
    "sha224": hashlib.sha224,
    "sha384": hashlib.sha384,
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
}


class Files:
    """High-level file operation utilities against Proxmox storage.

    Usage::

        from proxmox_sdk import ProxmoxSDK, Files

        async with ProxmoxSDK(...) as proxmox:
            f = Files(proxmox, node="pve1", storage="local")

            # Upload local ISO
            await f.upload_local_file_to_storage(
                "/path/to/debian.iso",
                do_checksum_check=True,
                blocking_status=True,
            )

            # Download from URL to Proxmox storage
            await f.download_file_to_storage(
                "https://cdimage.debian.org/debian-12.0.0-amd64-netinst.iso",
                blocking_status=True,
            )
    """

    def __init__(
        self,
        proxmox: ProxmoxResource,
        *,
        node: str,
        storage: str,
    ) -> None:
        self._proxmox = proxmox
        self._node = node
        self._storage = storage

    async def upload_local_file_to_storage(
        self,
        local_path: str,
        *,
        content_type: str | None = None,
        do_checksum_check: bool = False,
        blocking_status: bool = True,
        timeout: float = 300.0,
    ) -> dict[str, Any]:
        """Upload a local file to Proxmox storage.

        The content type is inferred from the file extension if not given:
        - ``.iso`` → ``iso``
        - ``.tar.gz``, ``.tar.zst``, ``.tar.xz`` → ``vztmpl``
        - anything else → ``iso``

        Args:
            local_path: Absolute path to the local file.
            content_type: Proxmox content type (``iso``, ``vztmpl``, ``backup``).
            do_checksum_check: Compute and verify SHA256 checksum after upload.
            blocking_status: Wait for the upload task to finish.
            timeout: Task wait timeout in seconds.

        Returns:
            Task status dict (if ``blocking_status``) or raw upload result.
        """
        path = Path(local_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {local_path}")

        resolved_content = content_type or _infer_content_type(path.name)

        upload_kwargs: dict[str, Any] = {
            "content": resolved_content,
        }

        if do_checksum_check:
            digest = _compute_file_checksum(local_path, "sha256")
            upload_kwargs["checksum"] = digest
            upload_kwargs["checksum-algorithm"] = "sha256"

        with path.open("rb") as fobj:
            upload_kwargs["filename"] = fobj
            task_id = (
                await self._proxmox.nodes(self._node)
                .storage(self._storage)
                .upload.post(**upload_kwargs)
            )

        if blocking_status and isinstance(task_id, str) and task_id.startswith("UPID"):
            from proxmox_sdk.sdk.tools.tasks import Tasks

            return await Tasks.blocking_status(self._proxmox, task_id, timeout=timeout)

        return {"task_id": task_id}

    async def download_file_to_storage(
        self,
        url: str,
        *,
        filename: str | None = None,
        content_type: str | None = None,
        checksum: str | None = None,
        checksum_algorithm: str | None = None,
        blocking_status: bool = True,
        timeout: float = 300.0,
    ) -> dict[str, Any]:
        """Tell Proxmox to download a file from a URL directly to storage.

        If ``checksum`` is not provided, attempts to auto-discover it from
        well-known checksum file patterns (``SHA512SUMS``, ``.sha256``, etc.).

        Args:
            url: Public URL of the file to download.
            filename: Override the filename (default: derived from URL).
            content_type: Proxmox content type (``iso``, ``vztmpl``, ``backup``).
            checksum: Hex digest for verification.
            checksum_algorithm: Algorithm for ``checksum`` (e.g. ``sha256``).
            blocking_status: Wait for the download task to finish.
            timeout: Task wait timeout.

        Returns:
            Task status dict (if ``blocking_status``) or raw API result.
        """
        resolved_filename = filename or url.rstrip("/").rsplit("/", 1)[-1]
        resolved_content = content_type or _infer_content_type(resolved_filename)

        resolved_checksum = checksum
        resolved_algorithm = checksum_algorithm

        if not resolved_checksum:
            discovered = await self._discover_checksum(url)
            if discovered:
                resolved_algorithm, resolved_checksum = discovered

        kwargs: dict[str, Any] = {
            "url": url,
            "filename": resolved_filename,
            "content": resolved_content,
        }
        if resolved_checksum:
            kwargs["checksum"] = resolved_checksum
        if resolved_algorithm:
            kwargs["checksum-algorithm"] = resolved_algorithm

        task_id = await (
            self._proxmox.nodes(self._node).storage(self._storage).download_url.post(**kwargs)
        )

        if blocking_status and isinstance(task_id, str) and task_id.startswith("UPID"):
            from proxmox_sdk.sdk.tools.tasks import Tasks

            return await Tasks.blocking_status(self._proxmox, task_id, timeout=timeout)

        return {"task_id": task_id}

    async def _discover_checksum(self, url: str) -> tuple[str, str] | None:
        """Try to discover a checksum for ``url`` from well-known locations.

        Strategies (tried in order for each algorithm):
        1. ``{url}.{algo}``  (e.g. file.iso.sha512)
        2. ``{url}.{ALGO}``  (e.g. file.iso.SHA512)
        3. ``{base_url}/SHA512SUMS``  (containing the filename)
        4. ``{base_url}/sha512sums``  (containing the filename)

        Returns:
            ``(algorithm, hex_digest)`` tuple, or ``None`` if not found.
        """
        filename = url.rstrip("/").rsplit("/", 1)[-1]
        base_url = url.rsplit("/", 1)[0]

        async with aiohttp.ClientSession() as session:
            for algo in _CHECKSUM_ALGORITHMS:
                # Strategy 1 & 2: sibling extension file
                for suffix in (algo, algo.upper()):
                    digest = await _fetch_single_hash(session, f"{url}.{suffix}")
                    if digest:
                        return algo, digest

                # Strategy 3 & 4: checksum index file
                for sums_name in (f"{algo.upper()}SUMS", f"{algo}sums"):
                    sums_url = f"{base_url}/{sums_name}"
                    digest = await _fetch_hash_from_sums(session, sums_url, filename)
                    if digest:
                        return algo, digest

        return None


# ------------------------------------------------------------------
# Module-level helpers
# ------------------------------------------------------------------


def _infer_content_type(filename: str) -> str:
    """Infer the Proxmox content type from a filename."""
    lower = filename.lower()
    if lower.endswith(".iso"):
        return "iso"
    if any(lower.endswith(ext) for ext in (".tar.gz", ".tar.zst", ".tar.xz", ".tar.bz2")):
        return "vztmpl"
    return "iso"


def _compute_file_checksum(path: str, algorithm: str) -> str:
    """Compute a hex-digest checksum for a local file."""
    hasher = _HASHLIB_MAP[algorithm]()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


async def _fetch_single_hash(session: aiohttp.ClientSession, url: str) -> str | None:
    """Fetch a URL and return its body as a stripped string if it looks like a hex digest."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return None
            text = (await resp.text()).strip().split()[0]
            if len(text) in (32, 40, 56, 64, 96, 128) and all(
                c in "0123456789abcdefABCDEF" for c in text
            ):
                return text.lower()
    except Exception:  # noqa: BLE001
        pass
    return None


async def _fetch_hash_from_sums(
    session: aiohttp.ClientSession,
    sums_url: str,
    filename: str,
) -> str | None:
    """Fetch a checksum index file and find the hash for ``filename``."""
    try:
        async with session.get(sums_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return None
            for line in (await resp.text()).splitlines():
                parts = line.split()
                if len(parts) >= 2:
                    digest, name = parts[0], parts[-1].lstrip("*")
                    if name == filename or name.endswith(f"/{filename}"):
                        return digest.lower()
    except Exception:  # noqa: BLE001
        pass
    return None


__all__ = ["Files"]
