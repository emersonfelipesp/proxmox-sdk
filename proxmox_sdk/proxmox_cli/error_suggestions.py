"""Enhanced error handling with recovery suggestions."""

from __future__ import annotations

from typing import Optional

_SERVICE_COMMON_PATHS: dict[str, list[str]] = {
    "PVE": [
        "/nodes",
        "/nodes/{node}",
        "/nodes/{node}/qemu",
        "/nodes/{node}/qemu/{vmid}",
        "/nodes/{node}/lxc",
        "/nodes/{node}/lxc/{vmid}",
        "/clusters",
        "/clusters/resources",
        "/storage",
        "/access",
        "/access/users",
        "/access/roles",
    ],
    "PBS": [
        "/admin/datastore",
        "/admin/datastore/{name}",
        "/admin",
        "/config",
        "/access",
        "/access/users",
        "/access/roles",
        "/nodes",
        "/status",
        "/tape",
    ],
}


class ErrorSuggester:
    """Provides helpful suggestions for common errors."""

    # Default PVE paths for backward compatibility
    COMMON_PATHS = _SERVICE_COMMON_PATHS["PVE"]

    @staticmethod
    def suggest_for_path_error(path: str, service: str = "PVE") -> Optional[str]:
        """Suggest corrections for path errors.

        Args:
            path: Invalid path attempted
            service: Proxmox service type (PVE, PBS, PMG)

        Returns:
            Suggestion string or None
        """
        if service == "PBS":
            if "datastore" in path.lower() or "store" in path.lower():
                return "Did you mean /admin/datastore? Try: proxmox ls /admin/datastore"
            elif "node" in path.lower():
                return "Did you mean /nodes? Try: proxmox ls /nodes"
            return None

        # PVE suggestions
        if "node" in path.lower():
            return "Did you mean /nodes? Try: proxmox ls /nodes"
        elif "qemu" in path.lower():
            return "Did you mean /nodes/{node}/qemu? Try: proxmox ls /nodes/pve1/qemu"
        elif "lxc" in path.lower():
            return "Did you mean /nodes/{node}/lxc? Try: proxmox ls /nodes/pve1/lxc"
        return None

    @staticmethod
    def suggest_for_auth_error(error_msg: str) -> Optional[str]:
        """Suggest fixes for authentication errors.

        Args:
            error_msg: Error message

        Returns:
            Suggestion string or None
        """
        if "401" in error_msg or "Unauthorized" in error_msg:
            return (
                "Authentication failed. Check your credentials:\n"
                "  - Token-based (recommended): proxmox --user admin@pam --token-value <token>\n"
                "  - Password-based: proxmox --user admin@pam --password <pass>"
            )
        elif "403" in error_msg or "Forbidden" in error_msg:
            return "Access denied. Check your token permissions or user role."
        return None

    @staticmethod
    def suggest_for_connection_error(error_msg: str, service: str = "PVE") -> Optional[str]:
        """Suggest fixes for connection errors.

        Args:
            error_msg: Error message
            service: Proxmox service type (PVE, PBS, PMG)

        Returns:
            Suggestion string or None
        """
        default_port = "8007" if service == "PBS" else "8006"
        if "refused" in error_msg.lower() or "timeout" in error_msg.lower():
            return (
                "Connection failed. Check:\n"
                "  - Host is reachable: proxmox --host <host> --help\n"
                f"  - Port is correct (default {default_port}): proxmox --port {default_port}\n"
                "  - Proxy/firewall allows connections"
            )
        elif "ssl" in error_msg.lower():
            return (
                "SSL verification failed. Try:\n"
                "  - Use a valid certificate\n"
                "  - Disable verification (insecure): proxmox --verify-ssl false"
            )
        return None
