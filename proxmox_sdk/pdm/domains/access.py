"""User, ACL, TFA, and API token management under ``/access``."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.pdm import models as m
from proxmox_sdk.pdm._normalization import validate_model, validate_model_list

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class _UsersOps:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PDMUser]:
        data = await self._sdk.access.users.get()
        return validate_model_list(m.PDMUser, data, operation="GET /access/users")

    async def get(self, userid: str) -> m.PDMUser:
        data = await self._sdk.access.users(userid).get()
        return validate_model(
            m.PDMUser,
            data,
            operation="GET /access/users/{userid}",
        )

    async def create(self, *, userid: str, **fields: Any) -> Any:
        payload = {"userid": userid, **fields}
        return unwrap_data(await self._sdk.access.users.post(**payload))

    async def update(self, userid: str, **changes: Any) -> Any:
        return unwrap_data(await self._sdk.access.users(userid).put(**changes))

    async def delete(self, userid: str) -> Any:
        return unwrap_data(await self._sdk.access.users(userid).delete())

    async def passwd(self, userid: str, password: str) -> Any:
        # PDM has no /access/password endpoint (unlike PVE).  Use the standard
        # user-update path: PUT /access/users/{userid} with the password field.
        return unwrap_data(await self._sdk.access.users(userid).put(password=password))


class _ACLOps:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PDMACLEntry]:
        data = await self._sdk.access.acl.get()
        return validate_model_list(m.PDMACLEntry, data, operation="GET /access/acl")

    async def update(
        self,
        *,
        path: str,
        roles: str,
        users: str | None = None,
        groups: str | None = None,
        propagate: bool | None = None,
    ) -> Any:
        payload: dict[str, Any] = {"path": path, "roles": roles}
        if users is not None:
            payload["users"] = users
        if groups is not None:
            payload["groups"] = groups
        if propagate is not None:
            payload["propagate"] = propagate
        return unwrap_data(await self._sdk.access.acl.put(**payload))

    async def delete(
        self,
        *,
        path: str,
        roles: str,
        users: str | None = None,
        groups: str | None = None,
    ) -> Any:
        payload: dict[str, Any] = {"path": path, "roles": roles, "delete": 1}
        if users is not None:
            payload["users"] = users
        if groups is not None:
            payload["groups"] = groups
        return unwrap_data(await self._sdk.access.acl.put(**payload))


class _TFAOps:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self, userid: str) -> list[m.PDMTFAEntry]:
        data = await self._sdk.access.tfa(userid).get()
        return validate_model_list(
            m.PDMTFAEntry,
            data,
            operation="GET /access/tfa/{userid}",
        )

    async def add(self, userid: str, **payload: Any) -> Any:
        return unwrap_data(await self._sdk.access.tfa(userid).post(**payload))

    async def delete(self, userid: str, tfa_id: str) -> Any:
        return unwrap_data(await self._sdk.access.tfa(userid)(tfa_id).delete())


class _TokenOps:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self, userid: str) -> list[m.PDMAPIToken]:
        data = await self._sdk.access.users(userid).token.get()
        return validate_model_list(
            m.PDMAPIToken,
            data,
            operation="GET /access/users/{userid}/token",
        )

    async def create(self, userid: str, tokenid: str, **fields: Any) -> Any:
        return unwrap_data(await self._sdk.access.users(userid).token(tokenid).post(**fields))

    async def update(self, userid: str, tokenid: str, **changes: Any) -> Any:
        return unwrap_data(await self._sdk.access.users(userid).token(tokenid).put(**changes))

    async def delete(self, userid: str, tokenid: str) -> Any:
        return unwrap_data(await self._sdk.access.users(userid).token(tokenid).delete())


class AccessDomain:
    """Composite access-control facade exposing user/ACL/TFA/token sub-domains."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk
        self.users = _UsersOps(sdk)
        self.acl = _ACLOps(sdk)
        self.tfa = _TFAOps(sdk)
        self.tokens = _TokenOps(sdk)
