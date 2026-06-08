"""RGW (RADOS Gateway) Admin Ops API client.

The RGW Admin Ops API (``/admin/*``) manages S3/Swift realms, zones, users,
buckets, quotas, and usage.  It authenticates with S3-style **AWS Signature v2**
(HMAC-SHA1) using an admin user's access/secret key pair.

Secret keys are used *only* to compute the request signature and are never
logged, echoed, or stored on returned models.  Reads expose user/bucket
inventory; writes are idempotent helpers and destructive ops require
``confirm_destroy=True``.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import hmac
from collections.abc import Callable
from email.utils import formatdate
from typing import Any

from proxmox_sdk.ceph._confirm import require_confirm
from proxmox_sdk.ceph.providers import models as m
from proxmox_sdk.ceph.providers._http import (
    DEFAULT_TIMEOUT,
    AsyncTransport,
    BaseHttpProvider,
    HttpResponse,
    JSONValue,
)
from proxmox_sdk.ceph.providers.capability import ProviderCapability
from proxmox_sdk.sdk.exceptions import ProxmoxSDKError

#: RGW Admin Ops sub-resources that AWS SigV2 requires inside the signed
#: canonical resource (not just the query string). ``quota`` is the only one
#: this client currently uses, but the set keeps the signing rule explicit.
_SIGNED_SUBRESOURCES: tuple[str, ...] = ("quota",)


class RGWAdminClient(BaseHttpProvider):
    """Async client for the RGW Admin Ops API (AWS SigV2 signed)."""

    provider = "rgw_admin"

    def __init__(
        self,
        base_url: str,
        *,
        access_key: str,
        secret_key: str,
        admin_path: str = "admin",
        verify_ssl: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        transport: AsyncTransport | None = None,
        clock: Callable[[], str] | None = None,
    ) -> None:
        super().__init__(base_url, verify_ssl=verify_ssl, timeout=timeout, transport=transport)
        if not access_key or not secret_key:
            raise ValueError("RGW Admin Ops requires access_key and secret_key")
        self._access_key = access_key
        self._secret_key = secret_key
        self._admin_path = admin_path.strip("/")
        self._clock = clock or (lambda: formatdate(usegmt=True))

    # -- signing ------------------------------------------------------------- #
    def _resource_path(self, resource: str) -> str:
        resource = resource.lstrip("/")
        return f"/{self._admin_path}/{resource}" if resource else f"/{self._admin_path}"

    def _sign(self, method: str, canonical_resource: str, date: str) -> str:
        string_to_sign = f"{method}\n\n\n{date}\n{canonical_resource}"
        digest = hmac.new(
            self._secret_key.encode("utf-8"),
            string_to_sign.encode("utf-8"),
            hashlib.sha1,
        ).digest()
        return base64.b64encode(digest).decode("ascii")

    def _auth_headers(self, method: str, canonical_resource: str) -> dict[str, str]:
        date = self._clock()
        signature = self._sign(method, canonical_resource, date)
        return {
            "Date": date,
            "Authorization": f"AWS {self._access_key}:{signature}",
            "Accept": "application/json",
        }

    @staticmethod
    def _canonical_resource(path: str, params: dict[str, Any]) -> str:
        """Append any signed sub-resources (e.g. ``?quota``) to the resource.

        AWS SigV2 requires recognised sub-resources to be part of the signed
        canonical resource, not just the query string. Omitting them makes RGW
        compute a different signature and reject the request with HTTP 403.
        """
        subresources = sorted(k for k in _SIGNED_SUBRESOURCES if k in params)
        if not subresources:
            return path
        return f"{path}?{'&'.join(subresources)}"

    async def _request(
        self,
        method: str,
        resource: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> HttpResponse:
        path = self._resource_path(resource)
        merged_params: dict[str, Any] = {"format": "json"}
        if params:
            merged_params.update(params)
        headers = self._auth_headers(method, self._canonical_resource(path, merged_params))
        if json is not None:
            headers["Content-Type"] = "application/json"
        response = await self._transport.request(
            method, self._url(path), headers=headers, params=merged_params, json=json
        )
        self._raise_for_status(response, context=f"rgw_admin {method} {path}")
        return response

    @staticmethod
    def _as_list(body: Any) -> list[Any]:
        return body if isinstance(body, list) else []

    # -- user reads ---------------------------------------------------------- #
    async def list_user_ids(self) -> list[str]:
        response = await self._request("GET", "metadata/user")
        return [str(uid) for uid in self._as_list(response.json_body)]

    async def get_user(self, uid: str) -> m.RGWUser:
        response = await self._request("GET", "user", params={"uid": uid})
        body = response.json_body if isinstance(response.json_body, dict) else {}
        return m.RGWUser.model_validate(body)

    async def list_users(self) -> list[m.RGWUser]:
        uids = await self.list_user_ids()
        results = await asyncio.gather(
            *(self.get_user(uid) for uid in uids), return_exceptions=True
        )
        users: list[m.RGWUser] = []
        for result in results:
            if isinstance(result, m.RGWUser):
                users.append(result)
            elif isinstance(result, ProxmoxSDKError):
                continue  # skip transient per-user errors
            elif isinstance(result, BaseException):
                raise result
        return users

    # -- bucket reads -------------------------------------------------------- #
    async def list_buckets(self) -> list[str]:
        response = await self._request("GET", "bucket")
        return [str(b) for b in self._as_list(response.json_body)]

    async def get_bucket(self, bucket: str) -> m.RGWBucket:
        response = await self._request("GET", "bucket", params={"bucket": bucket, "stats": "true"})
        body = response.json_body if isinstance(response.json_body, dict) else {}
        return m.RGWBucket.model_validate(body)

    async def usage(self, *, show_summary: bool = True) -> m.RGWUsage:
        response = await self._request(
            "GET", "usage", params={"show-summary": "true" if show_summary else "false"}
        )
        body = response.json_body if isinstance(response.json_body, dict) else {}
        return m.RGWUsage.model_validate(body)

    # -- user writes --------------------------------------------------------- #
    async def create_user(self, uid: str, *, display_name: str, **fields: Any) -> m.RGWUser:
        params = {"uid": uid, "display-name": display_name, **_str_params(fields)}
        response = await self._request("PUT", "user", params=params)
        body = response.json_body if isinstance(response.json_body, dict) else {}
        return m.RGWUser.model_validate(body)

    async def modify_user(self, uid: str, **fields: Any) -> m.RGWUser:
        params = {"uid": uid, **_str_params(fields)}
        response = await self._request("POST", "user", params=params)
        body = response.json_body if isinstance(response.json_body, dict) else {}
        return m.RGWUser.model_validate(body)

    async def set_user_suspended(self, uid: str, *, suspended: bool) -> m.RGWUser:
        return await self.modify_user(uid, suspended=suspended)

    async def set_user_quota(
        self, uid: str, *, max_size: int | None = None, max_objects: int | None = None
    ) -> JSONValue:
        params: dict[str, Any] = {"uid": uid, "quota-type": "user", "enabled": "true"}
        if max_size is not None:
            params["max-size"] = max_size
        if max_objects is not None:
            params["max-objects"] = max_objects
        response = await self._request("PUT", "user", params={**params, "quota": ""})
        return response.json_body

    async def remove_user(
        self, uid: str, *, purge_data: bool = False, confirm_destroy: bool = False
    ) -> JSONValue:
        require_confirm("remove_user", confirm_destroy)
        params = {"uid": uid, "purge-data": "true" if purge_data else "false"}
        response = await self._request("DELETE", "user", params=params)
        return response.json_body

    # -- bucket writes ------------------------------------------------------- #
    async def link_bucket(self, *, bucket: str, uid: str) -> JSONValue:
        response = await self._request("PUT", "bucket", params={"bucket": bucket, "uid": uid})
        return response.json_body

    async def set_bucket_quota(
        self, uid: str, *, max_size: int | None = None, max_objects: int | None = None
    ) -> JSONValue:
        params: dict[str, Any] = {"uid": uid, "quota-type": "bucket", "enabled": "true"}
        if max_size is not None:
            params["max-size"] = max_size
        if max_objects is not None:
            params["max-objects"] = max_objects
        response = await self._request("PUT", "user", params={**params, "quota": ""})
        return response.json_body

    async def remove_bucket(
        self, bucket: str, *, purge_objects: bool = False, confirm_destroy: bool = False
    ) -> JSONValue:
        require_confirm("remove_bucket", confirm_destroy)
        params = {"bucket": bucket, "purge-objects": "true" if purge_objects else "false"}
        response = await self._request("DELETE", "bucket", params=params)
        return response.json_body

    # -- capability detection ----------------------------------------------- #
    async def capabilities(self) -> ProviderCapability:
        try:
            await self.list_user_ids()
        except ProxmoxSDKError as exc:
            return ProviderCapability(
                provider=self.provider,
                available=False,
                notes=[f"rgw admin ops unavailable: {exc}"],
            )
        return ProviderCapability(
            provider=self.provider,
            available=True,
            read=True,
            write=True,
            operations={
                "rgw_user:create": True,
                "rgw_user:update": True,
                "rgw_user:suspend": True,
                "rgw_user:delete": True,
                "rgw_bucket:create": True,
                "rgw_bucket:update": True,
                "rgw_bucket:delete": True,
                "rgw_user:quota": True,
                "rgw_bucket:quota": True,
            },
        )


def _str_params(fields: dict[str, Any]) -> dict[str, Any]:
    """Map snake_case kwargs to the RGW admin ``dash-case`` query params."""

    out: dict[str, Any] = {}
    for key, value in fields.items():
        if value is None:
            continue
        out[key.replace("_", "-")] = value
    return out
