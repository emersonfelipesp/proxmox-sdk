"""Tests for the RGW Admin Ops direct provider client."""

from __future__ import annotations

import base64
import hashlib
import hmac

import pytest

from proxmox_sdk.ceph.providers._http import HttpResponse
from proxmox_sdk.ceph.providers.rgw import RGWAdminClient

from .conftest import RecordingTransport

BASE = "https://rgw.example.com:8080"
FIXED_DATE = "Mon, 02 Jan 2006 15:04:05 GMT"


def _client(routes: dict) -> tuple[RGWAdminClient, RecordingTransport]:
    transport = RecordingTransport(routes)
    client = RGWAdminClient(
        BASE,
        access_key="AKIA",
        secret_key="topsecret",
        transport=transport,
        clock=lambda: FIXED_DATE,
    )
    return client, transport


def _expected_sig(method: str, resource: str) -> str:
    string_to_sign = f"{method}\n\n\n{FIXED_DATE}\n{resource}"
    digest = hmac.new(b"topsecret", string_to_sign.encode(), hashlib.sha1).digest()
    return base64.b64encode(digest).decode()


async def test_requires_credentials() -> None:
    with pytest.raises(ValueError, match="access_key"):
        RGWAdminClient(BASE, access_key="", secret_key="x")


async def test_get_user_signs_request_with_sigv2() -> None:
    routes = {"GET /admin/user": {"user_id": "alice", "display_name": "Alice"}}
    client, transport = _client(routes)
    user = await client.get_user("alice")
    assert user.user_id == "alice"
    call = transport.calls[0]
    expected = f"AWS AKIA:{_expected_sig('GET', '/admin/user')}"
    assert call["headers"]["Authorization"] == expected
    assert call["headers"]["Date"] == FIXED_DATE
    assert call["params"]["uid"] == "alice"
    assert call["params"]["format"] == "json"


async def test_secret_key_never_leaks_into_calls() -> None:
    routes = {"GET /admin/metadata/user": ["alice", "bob"]}
    client, transport = _client(routes)
    uids = await client.list_user_ids()
    assert uids == ["alice", "bob"]
    serialized = repr(transport.calls)
    assert "topsecret" not in serialized


async def test_create_user_maps_dashed_params() -> None:
    routes = {"PUT /admin/user": {"user_id": "carol", "display_name": "Carol"}}
    client, transport = _client(routes)
    user = await client.create_user("carol", display_name="Carol", max_buckets=50)
    assert user.user_id == "carol"
    params = transport.calls[0]["params"]
    assert params["display-name"] == "Carol"
    assert params["max-buckets"] == 50


async def test_set_user_quota_uses_quota_subresource() -> None:
    routes = {"PUT /admin/user": {}}
    client, transport = _client(routes)
    await client.set_user_quota("dave", max_size=1024, max_objects=10)
    params = transport.calls[0]["params"]
    assert params["quota-type"] == "user"
    assert params["max-size"] == 1024
    assert "quota" in params


async def test_remove_user_requires_confirmation() -> None:
    routes = {"DELETE /admin/user": {}}
    client, _ = _client(routes)
    with pytest.raises(ValueError, match="destructive"):
        await client.remove_user("erin")
    assert await client.remove_user("erin", confirm_destroy=True) == {}


async def test_remove_bucket_requires_confirmation() -> None:
    routes = {"DELETE /admin/bucket": {}}
    client, _ = _client(routes)
    with pytest.raises(ValueError, match="destructive"):
        await client.remove_bucket("data")
    assert await client.remove_bucket("data", confirm_destroy=True) == {}


async def test_capabilities_available_when_reachable() -> None:
    routes = {"GET /admin/metadata/user": ["alice"]}
    client, _ = _client(routes)
    caps = await client.capabilities()
    assert caps.available is True
    assert caps.supports("rgw_user", "create") is True
    assert caps.supports("rgw_bucket", "delete") is True


async def test_capabilities_unavailable_on_error() -> None:
    routes = {"GET /admin/metadata/user": HttpResponse(status=403, text="denied")}
    client, _ = _client(routes)
    caps = await client.capabilities()
    assert caps.available is False
