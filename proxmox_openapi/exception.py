"""Exception classes for proxmox-openapi."""


class ProxmoxOpenAPIException(Exception):
    """Base exception for proxmox-openapi."""

    def __init__(
        self, message: str, detail: str | None = None, python_exception: str | None = None
    ):
        self.message = message
        self.detail = detail
        self.python_exception = python_exception
        super().__init__(self.message)


__all__ = ["ProxmoxOpenAPIException"]
