"""Exception classes for proxmox-sdk."""


class ProxmoxOpenAPIException(Exception):
    """Base exception for proxmox-sdk."""

    def __init__(
        self, message: str, detail: str | None = None, python_exception: str | None = None
    ):
        self.message = message
        self.detail = detail
        self.python_exception = python_exception
        super().__init__(self.message)


__all__ = ["ProxmoxOpenAPIException"]
