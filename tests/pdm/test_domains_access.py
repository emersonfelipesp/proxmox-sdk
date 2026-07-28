"""Access control: users, ACL, TFA, API tokens."""

from __future__ import annotations

from proxmox_sdk.pdm import PDMClient

from .conftest import make_pdm_sdk


async def test_users_list_path():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/access/users": {"data": [{"userid": "root@pam", "enable": True}]}}
    )
    pdm = PDMClient(_sdk=sdk)
    users = await pdm.access.users.list()
    assert users[0].userid == "root@pam"
    assert backend.calls[0][1] == "/api2/json/access/users"


async def test_user_create_update_delete():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/access/users": {"data": None},
            "/api2/json/access/users/alice%40pdm": {"data": None},
        }
    )
    pdm = PDMClient(_sdk=sdk)
    await pdm.access.users.create(userid="alice@pdm", comment="ops")
    assert backend.calls[0][0] == "POST"
    assert (backend.calls[0][3] or {})["userid"] == "alice@pdm"

    await pdm.access.users.update("alice@pdm", comment="updated")
    assert backend.calls[1][0] == "PUT"

    await pdm.access.users.delete("alice@pdm")
    assert backend.calls[2][0] == "DELETE"


async def test_user_passwd_uses_user_update_endpoint():
    sdk, backend = make_pdm_sdk({"/api2/json/access/users/alice%40pdm": {"data": None}})
    pdm = PDMClient(_sdk=sdk)
    await pdm.access.users.passwd("alice@pdm", "newpw")
    assert backend.calls[0][0] == "PUT"
    assert backend.calls[0][1] == "/api2/json/access/users/alice%40pdm"
    body = backend.calls[0][3] or {}
    assert body["password"] == "newpw"


async def test_acl_list_update_delete():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/access/acl": {
                "data": [
                    {
                        "path": "/",
                        "ugid_type": "user",
                        "ugid": "root@pam",
                        "roleid": "Admin",
                        "propagate": True,
                    }
                ]
            },
        }
    )
    pdm = PDMClient(_sdk=sdk)
    acls = await pdm.access.acl.list()
    assert acls[0].roleid == "Admin"
    assert acls[0].type == "user"

    await pdm.access.acl.update(path="/remote/pve-a", roles="PDMAuditor", users="alice@pdm")
    assert backend.calls[1][0] == "PUT"
    assert "delete" not in (backend.calls[1][3] or {})

    await pdm.access.acl.delete(path="/remote/pve-a", roles="PDMAuditor", users="alice@pdm")
    assert (backend.calls[2][3] or {}).get("delete") == 1


async def test_tfa_list_add_delete():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/access/tfa/alice%40pdm": {
                "data": [{"id": "totp-1", "type": "totp", "enable": True}]
            },
            "/api2/json/access/tfa/alice%40pdm/totp-1": {"data": None},
        }
    )
    pdm = PDMClient(_sdk=sdk)
    entries = await pdm.access.tfa.list("alice@pdm")
    assert entries[0].type == "totp"

    await pdm.access.tfa.add("alice@pdm", type="totp", description="phone")
    assert backend.calls[1][0] == "POST"

    await pdm.access.tfa.delete("alice@pdm", "totp-1")
    assert backend.calls[2][0] == "DELETE"


async def test_api_tokens_crud():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/access/users/alice%40pdm/token": {
                "data": [{"tokenid": "alice@pdm!api", "token-name": "api", "enable": True}]
            },
            "/api2/json/access/users/alice%40pdm/token/api": {"data": None},
        }
    )
    pdm = PDMClient(_sdk=sdk)
    tokens = await pdm.access.tokens.list("alice@pdm")
    assert tokens[0].tokenid == "alice@pdm!api"
    assert tokens[0].token_name == "api"

    await pdm.access.tokens.create("alice@pdm", "api", comment="readonly")
    assert backend.calls[1][0] == "POST"

    await pdm.access.tokens.update("alice@pdm", "api", privsep=False)
    assert backend.calls[2][0] == "PUT"

    await pdm.access.tokens.delete("alice@pdm", "api")
    assert backend.calls[3][0] == "DELETE"
