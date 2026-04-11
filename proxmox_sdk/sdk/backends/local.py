"""Local pvesh backend — executes pvesh directly on the Proxmox host."""

from __future__ import annotations

import asyncio
import io
import shutil
import tempfile
from typing import TYPE_CHECKING, Any

from proxmox_sdk.sdk.backends._cli_base import CliResponse, CommandBaseBackend
from proxmox_sdk.sdk.exceptions import ResourceException

if TYPE_CHECKING:
    from proxmox_sdk.sdk.services import ServiceConfig


class LocalBackend(CommandBaseBackend):
    """Execute Proxmox API calls via ``pvesh`` on the local Proxmox host.

    No network or authentication needed — uses the local file system
    permissions of the running process.  Must be run on a Proxmox host.

    Example::

        backend = LocalBackend(service_config=SERVICES["PVE"])
        nodes = await backend.request("GET", "/api2/json/nodes")

    File upload uploads the file to a temporary path on the host and
    passes that path to pvesh.
    """

    def __init__(
        self,
        *,
        service_config: ServiceConfig,
        sudo: bool = False,
    ) -> None:
        super().__init__(service_config=service_config, sudo=sudo)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Handle file upload specially before delegating to parent."""
        # Separate file objects from regular params
        if data and any(isinstance(v, io.IOBase) for v in data.values()):
            return await self._upload_and_request(method, path, params=params, data=data)
        return await super().request(method, path, params=params, data=data)

    async def _execute_command(self, command: list[str]) -> CliResponse:
        """Run the pvesh command via asyncio subprocess."""
        try:
            proc = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            exit_code = proc.returncode or 0
            status_code = self._detect_status_code(
                stderr.decode("utf-8", errors="replace"), exit_code
            )
            return CliResponse(
                status_code=status_code,
                exit_code=exit_code,
                content=stdout,
            )
        except FileNotFoundError as exc:
            cli = self._service_config.cli_name or "pvesh"
            raise ResourceException(
                status_code=503,
                status_message="Service Unavailable",
                content=f"'{cli}' not found — is this a Proxmox host?",
            ) from exc

    async def _upload_and_request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Write file to a temp path then call pvesh with the temp filename."""
        resolved_data = dict(data or {})
        tmp_paths: list[str] = []

        try:
            for key, value in list(resolved_data.items()):
                if isinstance(value, io.IOBase):
                    with tempfile.NamedTemporaryFile(delete=False) as tmp:
                        shutil.copyfileobj(value, tmp)
                        tmp_paths.append(tmp.name)
                        resolved_data[key] = tmp.name

            return await super().request(method, path, params=params, data=resolved_data)
        finally:
            import os

            for p in tmp_paths:
                try:
                    os.unlink(p)
                except OSError:
                    pass


__all__ = ["LocalBackend"]
