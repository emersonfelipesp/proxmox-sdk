"""Generated Pydantic v2 schemas from Proxmox OpenAPI output.

Do not edit by hand. The integrity guard below pins this artifact to the
``openapi.json`` it was generated from; ``tests/test_generated_integrity.py``
re-hashes the source spec on every run and fails if the two drift.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr

GENERATED_FOR_PROXMOX_VERSION = "9.1.11"
GENERATED_SOURCE_SHA256 = "6fb57e0668c0d043fb9f7e8baf387b320c3948acf634ae439f0d748ea744ad63"
GENERATED_AT = "2026-08-06T18:55:02.223780+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')


def _allowed_ints(allowed: tuple[int, ...]) -> AfterValidator:
    def validate(value: int) -> int:
        if value not in allowed:
            raise ValueError('value is not an allowed schema member')
        return value

    return AfterValidator(validate)

class GetAccessResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index. response."""
    subdir: StrictStr | None = Field(None)

class GetAccessResponse(RootModel[list[GetAccessResponseItem]]):
    """List of items. index. Directory index. response."""
    root: list[GetAccessResponseItem] = Field(...)

class GetAccessAclResponseItem(ProxmoxBaseModel):
    """Model for read_acl. Get Access Control List (ACLs). response."""
    path: StrictStr | None = Field(None, description='Access control path')
    propagate: bool | None = Field(None, description='Allow to propagate (inherit) permissions.')
    roleid: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)
    ugid: StrictStr | None = Field(None)

class GetAccessAclResponse(RootModel[list[GetAccessAclResponseItem]]):
    """List of items. read_acl. Get Access Control List (ACLs). response."""
    root: list[GetAccessAclResponseItem] = Field(...)

class PutAccessAclRequest(ProxmoxBaseModel):
    """Model for update_acl. Update Access Control List (add or remove permissions). request."""
    delete: bool | None = Field(None, description='Remove permissions (instead of adding it).')
    groups: StrictStr | None = Field(None, description='List of groups.')
    path: StrictStr = Field(..., description='Access control path')
    propagate: bool | None = Field(None, description='Allow to propagate (inherit) permissions.')
    roles: StrictStr = Field(..., description='List of roles.')
    tokens: StrictStr | None = Field(None, description='List of API tokens.')
    users: StrictStr | None = Field(None, description='List of users.')

class PutAccessAclResponse(RootModel[None]):
    """Model for update_acl. Update Access Control List (add or remove permissions). response."""
    root: None = Field(...)

class GetAccessDomainsResponseItem(ProxmoxBaseModel):
    """Model for index. Authentication domain index. response."""
    comment: StrictStr | None = Field(None, description='A comment. The GUI use this text when you select a domain (Realm) on the login window.')
    realm: StrictStr | None = Field(None)
    tfa: StrictStr | None = Field(None, description='Two-factor authentication provider.')
    type: StrictStr | None = Field(None)

class GetAccessDomainsResponse(RootModel[list[GetAccessDomainsResponseItem]]):
    """List of items. index. Authentication domain index. response."""
    root: list[GetAccessDomainsResponseItem] = Field(...)

class PostAccessDomainsRequest(ProxmoxBaseModel):
    """Model for create. Add an authentication server. request."""
    acr_values: StrictStr | None = Field(None, alias="acr-values", description='Specifies the Authentication Context Class Reference values that theAuthorization Server is being requested to use for the Auth Request.')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    base_dn: StrictStr | None = Field(None, description='LDAP base domain name')
    bind_dn: StrictStr | None = Field(None, description='LDAP bind domain name')
    capath: StrictStr | None = Field(None, description='Path to the CA certificate store')
    case_sensitive: bool | None = Field(None, alias="case-sensitive", description='username is case-sensitive')
    cert: StrictStr | None = Field(None, description='Path to the client certificate')
    certkey: StrictStr | None = Field(None, description='Path to the client certificate key')
    check_connection: bool | None = Field(None, alias="check-connection", description='Check bind connection to the server.')
    client_id: StrictStr | None = Field(None, alias="client-id", description='OpenID Client ID')
    client_key: StrictStr | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: StrictStr | None = Field(None, description='Description.')
    default: bool | None = Field(None, description='Use this as default realm')
    domain: StrictStr | None = Field(None, description='AD domain name')
    filter: StrictStr | None = Field(None, description='LDAP filter for user sync.')
    group_classes: StrictStr | None = Field(None, description='The objectclasses for groups.')
    group_dn: StrictStr | None = Field(None, description='LDAP base domain name for group sync. If not set, the base_dn will be used.')
    group_filter: StrictStr | None = Field(None, description='LDAP filter for group sync.')
    group_name_attr: StrictStr | None = Field(None, description='LDAP attribute representing a groups name. If not set or found, the first value of the DN will be used as name.')
    groups_autocreate: bool | None = Field(None, alias="groups-autocreate", description='Automatically create groups if they do not exist.')
    groups_claim: StrictStr | None = Field(None, alias="groups-claim", description='OpenID claim used to retrieve groups with.')
    groups_overwrite: bool | None = Field(None, alias="groups-overwrite", description='All groups will be overwritten for the user on login.')
    issuer_url: StrictStr | None = Field(None, alias="issuer-url", description='OpenID Issuer Url')
    mode: StrictStr | None = Field(None, description='LDAP protocol mode.')
    password: StrictStr | None = Field(None, description="LDAP bind password. Will be stored in '/etc/pve/priv/realm/<REALM>.pw'.")
    port: int | None = Field(None, description='Server port.')
    prompt: StrictStr | None = Field(None, description='Specifies whether the Authorization Server prompts the End-User for reauthentication and consent.')
    query_userinfo: bool | None = Field(None, alias="query-userinfo", description='Enables querying the userinfo endpoint for claims values.')
    realm: StrictStr = Field(..., description='Authentication domain ID')
    scopes: StrictStr | None = Field(None, description="Specifies the scopes (user details) that should be authorized and returned, for example 'email' or 'profile'.")
    secure: bool | None = Field(None, description="Use secure LDAPS protocol. DEPRECATED: use 'mode' instead.")
    server1: StrictStr | None = Field(None, description='Server IP address (or DNS name)')
    server2: StrictStr | None = Field(None, description='Fallback Server IP address (or DNS name)')
    sslversion: StrictStr | None = Field(None, description="LDAPS TLS/SSL version. It's not recommended to use version older than 1.2!")
    sync_defaults_options: StrictStr | None = Field(None, alias="sync-defaults-options", description='The default options for behavior of synchronizations.')
    sync_attributes: StrictStr | None = Field(None, description="Comma separated list of key=value pairs for specifying which LDAP attributes map to which PVE user field. For example, to map the LDAP attribute 'mail' to PVEs 'email', write  'email=mail'. By default, each PVE user field is represented  by an LDAP attribute of the same name.")
    tfa: StrictStr | None = Field(None, description='Use Two-factor authentication.')
    type: StrictStr = Field(..., description='Realm type.')
    user_attr: StrictStr | None = Field(None, description='LDAP user attribute name')
    user_classes: StrictStr | None = Field(None, description='The objectclasses for users.')
    username_claim: StrictStr | None = Field(None, alias="username-claim", description='OpenID claim used to generate the unique username.')
    verify: bool | None = Field(None, description="Verify the server's SSL certificate")

class PostAccessDomainsResponse(RootModel[None]):
    """Model for create. Add an authentication server. response."""
    root: None = Field(...)

class DeleteAccessDomainsRealmRequest(RootModel[dict[str, object]]):
    """Model for delete. Delete an authentication server. request."""
    root: dict[str, object] = Field(...)

class DeleteAccessDomainsRealmResponse(RootModel[None]):
    """Model for delete. Delete an authentication server. response."""
    root: None = Field(...)

class GetAccessDomainsRealmResponse(RootModel[dict[str, object]]):
    """Model for read. Get auth server configuration. response."""
    root: dict[str, object] = Field(...)

class PutAccessDomainsRealmRequest(ProxmoxBaseModel):
    """Model for update. Update authentication server settings. request."""
    acr_values: StrictStr | None = Field(None, alias="acr-values", description='Specifies the Authentication Context Class Reference values that theAuthorization Server is being requested to use for the Auth Request.')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    base_dn: StrictStr | None = Field(None, description='LDAP base domain name')
    bind_dn: StrictStr | None = Field(None, description='LDAP bind domain name')
    capath: StrictStr | None = Field(None, description='Path to the CA certificate store')
    case_sensitive: bool | None = Field(None, alias="case-sensitive", description='username is case-sensitive')
    cert: StrictStr | None = Field(None, description='Path to the client certificate')
    certkey: StrictStr | None = Field(None, description='Path to the client certificate key')
    check_connection: bool | None = Field(None, alias="check-connection", description='Check bind connection to the server.')
    client_id: StrictStr | None = Field(None, alias="client-id", description='OpenID Client ID')
    client_key: StrictStr | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: StrictStr | None = Field(None, description='Description.')
    default: bool | None = Field(None, description='Use this as default realm')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    domain: StrictStr | None = Field(None, description='AD domain name')
    filter: StrictStr | None = Field(None, description='LDAP filter for user sync.')
    group_classes: StrictStr | None = Field(None, description='The objectclasses for groups.')
    group_dn: StrictStr | None = Field(None, description='LDAP base domain name for group sync. If not set, the base_dn will be used.')
    group_filter: StrictStr | None = Field(None, description='LDAP filter for group sync.')
    group_name_attr: StrictStr | None = Field(None, description='LDAP attribute representing a groups name. If not set or found, the first value of the DN will be used as name.')
    groups_autocreate: bool | None = Field(None, alias="groups-autocreate", description='Automatically create groups if they do not exist.')
    groups_claim: StrictStr | None = Field(None, alias="groups-claim", description='OpenID claim used to retrieve groups with.')
    groups_overwrite: bool | None = Field(None, alias="groups-overwrite", description='All groups will be overwritten for the user on login.')
    issuer_url: StrictStr | None = Field(None, alias="issuer-url", description='OpenID Issuer Url')
    mode: StrictStr | None = Field(None, description='LDAP protocol mode.')
    password: StrictStr | None = Field(None, description="LDAP bind password. Will be stored in '/etc/pve/priv/realm/<REALM>.pw'.")
    port: int | None = Field(None, description='Server port.')
    prompt: StrictStr | None = Field(None, description='Specifies whether the Authorization Server prompts the End-User for reauthentication and consent.')
    query_userinfo: bool | None = Field(None, alias="query-userinfo", description='Enables querying the userinfo endpoint for claims values.')
    scopes: StrictStr | None = Field(None, description="Specifies the scopes (user details) that should be authorized and returned, for example 'email' or 'profile'.")
    secure: bool | None = Field(None, description="Use secure LDAPS protocol. DEPRECATED: use 'mode' instead.")
    server1: StrictStr | None = Field(None, description='Server IP address (or DNS name)')
    server2: StrictStr | None = Field(None, description='Fallback Server IP address (or DNS name)')
    sslversion: StrictStr | None = Field(None, description="LDAPS TLS/SSL version. It's not recommended to use version older than 1.2!")
    sync_defaults_options: StrictStr | None = Field(None, alias="sync-defaults-options", description='The default options for behavior of synchronizations.')
    sync_attributes: StrictStr | None = Field(None, description="Comma separated list of key=value pairs for specifying which LDAP attributes map to which PVE user field. For example, to map the LDAP attribute 'mail' to PVEs 'email', write  'email=mail'. By default, each PVE user field is represented  by an LDAP attribute of the same name.")
    tfa: StrictStr | None = Field(None, description='Use Two-factor authentication.')
    user_attr: StrictStr | None = Field(None, description='LDAP user attribute name')
    user_classes: StrictStr | None = Field(None, description='The objectclasses for users.')
    verify: bool | None = Field(None, description="Verify the server's SSL certificate")

class PutAccessDomainsRealmResponse(RootModel[None]):
    """Model for update. Update authentication server settings. response."""
    root: None = Field(...)

class PostAccessDomainsRealmSyncRequest(ProxmoxBaseModel):
    """Model for sync. Syncs users and/or groups from the configured LDAP to user.cfg. NOTE: Synced groups will have the name 'name-$realm', so make sure those groups do not exist to prevent overwriting. request."""
    dry_run: bool | None = Field(None, alias="dry-run", description='If set, does not write anything.')
    enable_new: bool | None = Field(None, alias="enable-new", description='Enable newly synced users immediately.')
    full: bool | None = Field(None, description="DEPRECATED: use 'remove-vanished' instead. If set, uses the LDAP Directory as source of truth, deleting users or groups not returned from the sync and removing all locally modified properties of synced users. If not set, only syncs information which is present in the synced data, and does not delete or modify anything else.")
    purge: bool | None = Field(None, description="DEPRECATED: use 'remove-vanished' instead. Remove ACLs for users or groups which were removed from the config during a sync.")
    remove_vanished: StrictStr | None = Field(None, alias="remove-vanished", description="A semicolon-separated list of things to remove when they or the user vanishes during a sync. The following values are possible: 'entry' removes the user/group when not returned from the sync. 'properties' removes the set properties on existing user/group that do not appear in the source (even custom ones). 'acl' removes acls when the user/group is not returned from the sync. Instead of a list it also can be 'none' (the default).")
    scope: StrictStr | None = Field(None, description='Select what to sync.')

class PostAccessDomainsRealmSyncResponse(RootModel[StrictStr]):
    """Model for sync. Syncs users and/or groups from the configured LDAP to user.cfg. NOTE: Synced groups will have the name 'name-$realm', so make sure those groups do not exist to prevent overwriting. response."""
    root: StrictStr = Field(..., description='Worker Task-UPID')

class GetAccessGroupsResponseItem(ProxmoxBaseModel):
    """Model for index. Group index. response."""
    comment: StrictStr | None = Field(None)
    groupid: StrictStr | None = Field(None)
    users: StrictStr | None = Field(None, description='list of users which form this group')

class GetAccessGroupsResponse(RootModel[list[GetAccessGroupsResponseItem]]):
    """List of items. index. Group index. response."""
    root: list[GetAccessGroupsResponseItem] = Field(...)

class PostAccessGroupsRequest(ProxmoxBaseModel):
    """Model for create_group. Create new group. request."""
    comment: StrictStr | None = Field(None)
    groupid: StrictStr = Field(...)

class PostAccessGroupsResponse(RootModel[None]):
    """Model for create_group. Create new group. response."""
    root: None = Field(...)

class DeleteAccessGroupsGroupidRequest(RootModel[dict[str, object]]):
    """Model for delete_group. Delete group. request."""
    root: dict[str, object] = Field(...)

class DeleteAccessGroupsGroupidResponse(RootModel[None]):
    """Model for delete_group. Delete group. response."""
    root: None = Field(...)

class GetAccessGroupsGroupidResponse(ProxmoxBaseModel):
    """Model for read_group. Get group configuration. response."""
    comment: StrictStr | None = Field(None)
    members: list[StrictStr] = Field(...)

class PutAccessGroupsGroupidRequest(ProxmoxBaseModel):
    """Model for update_group. Update group data. request."""
    comment: StrictStr | None = Field(None)

class PutAccessGroupsGroupidResponse(RootModel[None]):
    """Model for update_group. Update group data. response."""
    root: None = Field(...)

class GetAccessOpenidResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index. response."""
    subdir: StrictStr | None = Field(None)

class GetAccessOpenidResponse(RootModel[list[GetAccessOpenidResponseItem]]):
    """List of items. index. Directory index. response."""
    root: list[GetAccessOpenidResponseItem] = Field(...)

class PostAccessOpenidAuthUrlRequest(ProxmoxBaseModel):
    """Model for auth_url. Get the OpenId Authorization Url for the specified realm. request."""
    realm: StrictStr = Field(..., description='Authentication domain ID')
    redirect_url: StrictStr = Field(..., alias="redirect-url", description='Redirection Url. The client should set this to the used server url (location.origin).')

class PostAccessOpenidAuthUrlResponse(RootModel[StrictStr]):
    """Model for auth_url. Get the OpenId Authorization Url for the specified realm. response."""
    root: StrictStr = Field(..., description='Redirection URL.')

class PostAccessOpenidLoginRequest(ProxmoxBaseModel):
    """Model for login. Verify OpenID authorization code and create a ticket. request."""
    code: StrictStr = Field(..., description='OpenId authorization code.')
    redirect_url: StrictStr = Field(..., alias="redirect-url", description='Redirection Url. The client should set this to the used server url (location.origin).')
    state: StrictStr = Field(..., description='OpenId state.')

class PostAccessOpenidLoginResponse(ProxmoxBaseModel):
    """Model for login. Verify OpenID authorization code and create a ticket. response."""
    csrfprevention_token: StrictStr = Field(..., alias="CSRFPreventionToken")
    cap: dict[str, object] = Field(...)
    clustername: StrictStr | None = Field(None)
    ticket: StrictStr = Field(...)
    username: StrictStr = Field(...)

class PutAccessPasswordRequest(ProxmoxBaseModel):
    """Model for change_password. Change user password. request."""
    confirmation_password: StrictStr | None = Field(None, alias="confirmation-password", description='The current password of the user performing the change.')
    password: StrictStr = Field(..., description='The new password.')
    userid: StrictStr = Field(..., description='Full User ID, in the `name@realm` format.')

class PutAccessPasswordResponse(RootModel[None]):
    """Model for change_password. Change user password. response."""
    root: None = Field(...)

class GetAccessPermissionsResponse(RootModel[dict[str, object]]):
    """Model for permissions. Retrieve effective permissions of given user/token. response."""
    root: dict[str, object] = Field(...)

class GetAccessRolesResponseItem(ProxmoxBaseModel):
    """Model for index. Role index. response."""
    privs: StrictStr | None = Field(None)
    roleid: StrictStr | None = Field(None)
    special: bool | None = Field(None)

class GetAccessRolesResponse(RootModel[list[GetAccessRolesResponseItem]]):
    """List of items. index. Role index. response."""
    root: list[GetAccessRolesResponseItem] = Field(...)

class PostAccessRolesRequest(ProxmoxBaseModel):
    """Model for create_role. Create new role. request."""
    privs: StrictStr | None = Field(None)
    roleid: StrictStr = Field(...)

class PostAccessRolesResponse(RootModel[None]):
    """Model for create_role. Create new role. response."""
    root: None = Field(...)

class DeleteAccessRolesRoleidRequest(RootModel[dict[str, object]]):
    """Model for delete_role. Delete role. request."""
    root: dict[str, object] = Field(...)

class DeleteAccessRolesRoleidResponse(RootModel[None]):
    """Model for delete_role. Delete role. response."""
    root: None = Field(...)

class GetAccessRolesRoleidResponse(ProxmoxBaseModel):
    """Model for read_role. Get role configuration. response."""
    datastore_allocate: bool | None = Field(None, alias="Datastore.Allocate")
    datastore_allocate_space: bool | None = Field(None, alias="Datastore.AllocateSpace")
    datastore_allocate_template: bool | None = Field(None, alias="Datastore.AllocateTemplate")
    datastore_audit: bool | None = Field(None, alias="Datastore.Audit")
    group_allocate: bool | None = Field(None, alias="Group.Allocate")
    mapping_audit: bool | None = Field(None, alias="Mapping.Audit")
    mapping_modify: bool | None = Field(None, alias="Mapping.Modify")
    mapping_use: bool | None = Field(None, alias="Mapping.Use")
    permissions_modify: bool | None = Field(None, alias="Permissions.Modify")
    pool_allocate: bool | None = Field(None, alias="Pool.Allocate")
    pool_audit: bool | None = Field(None, alias="Pool.Audit")
    realm_allocate: bool | None = Field(None, alias="Realm.Allocate")
    realm_allocate_user: bool | None = Field(None, alias="Realm.AllocateUser")
    sdn_allocate: bool | None = Field(None, alias="SDN.Allocate")
    sdn_audit: bool | None = Field(None, alias="SDN.Audit")
    sdn_use: bool | None = Field(None, alias="SDN.Use")
    sys_access_network: bool | None = Field(None, alias="Sys.AccessNetwork")
    sys_audit: bool | None = Field(None, alias="Sys.Audit")
    sys_console: bool | None = Field(None, alias="Sys.Console")
    sys_incoming: bool | None = Field(None, alias="Sys.Incoming")
    sys_modify: bool | None = Field(None, alias="Sys.Modify")
    sys_power_mgmt: bool | None = Field(None, alias="Sys.PowerMgmt")
    sys_syslog: bool | None = Field(None, alias="Sys.Syslog")
    user_modify: bool | None = Field(None, alias="User.Modify")
    vm_allocate: bool | None = Field(None, alias="VM.Allocate")
    vm_audit: bool | None = Field(None, alias="VM.Audit")
    vm_backup: bool | None = Field(None, alias="VM.Backup")
    vm_clone: bool | None = Field(None, alias="VM.Clone")
    vm_config_cdrom: bool | None = Field(None, alias="VM.Config.CDROM")
    vm_config_cpu: bool | None = Field(None, alias="VM.Config.CPU")
    vm_config_cloudinit: bool | None = Field(None, alias="VM.Config.Cloudinit")
    vm_config_disk: bool | None = Field(None, alias="VM.Config.Disk")
    vm_config_hwtype: bool | None = Field(None, alias="VM.Config.HWType")
    vm_config_memory: bool | None = Field(None, alias="VM.Config.Memory")
    vm_config_network: bool | None = Field(None, alias="VM.Config.Network")
    vm_config_options: bool | None = Field(None, alias="VM.Config.Options")
    vm_console: bool | None = Field(None, alias="VM.Console")
    vm_guest_agent_audit: bool | None = Field(None, alias="VM.GuestAgent.Audit")
    vm_guest_agent_file_read: bool | None = Field(None, alias="VM.GuestAgent.FileRead")
    vm_guest_agent_file_system_mgmt: bool | None = Field(None, alias="VM.GuestAgent.FileSystemMgmt")
    vm_guest_agent_file_write: bool | None = Field(None, alias="VM.GuestAgent.FileWrite")
    vm_guest_agent_unrestricted: bool | None = Field(None, alias="VM.GuestAgent.Unrestricted")
    vm_migrate: bool | None = Field(None, alias="VM.Migrate")
    vm_power_mgmt: bool | None = Field(None, alias="VM.PowerMgmt")
    vm_replicate: bool | None = Field(None, alias="VM.Replicate")
    vm_snapshot: bool | None = Field(None, alias="VM.Snapshot")
    vm_snapshot_rollback: bool | None = Field(None, alias="VM.Snapshot.Rollback")

class PutAccessRolesRoleidRequest(ProxmoxBaseModel):
    """Model for update_role. Update an existing role. request."""
    append: bool | None = Field(None)
    privs: StrictStr | None = Field(None)

class PutAccessRolesRoleidResponse(RootModel[None]):
    """Model for update_role. Update an existing role. response."""
    root: None = Field(...)

class GetAccessTfaResponseItem(ProxmoxBaseModel):
    """Model for list_tfa. List TFA configurations of users. response."""
    entries: list[dict[str, object]] | None = Field(None)
    tfa_locked_until: int | None = Field(None, alias="tfa-locked-until", description='Contains a timestamp until when a user is locked out of 2nd factors.')
    totp_locked: bool | None = Field(None, alias="totp-locked", description='True if the user is currently locked out of TOTP factors.')
    userid: StrictStr | None = Field(None, description='User this entry belongs to.')

class GetAccessTfaResponse(RootModel[list[GetAccessTfaResponseItem]]):
    """List of items. list_tfa. List TFA configurations of users. response."""
    root: list[GetAccessTfaResponseItem] = Field(..., description='The list tuples of user and TFA entries.')

class GetAccessTfaUseridResponseItem(ProxmoxBaseModel):
    """Model for list_user_tfa. List TFA configurations of users. response."""
    created: int | None = Field(None, description='Creation time of this entry as unix epoch.')
    description: StrictStr | None = Field(None, description='User chosen description for this entry.')
    enable: bool | None = Field(None, description='Whether this TFA entry is currently enabled.')
    id: StrictStr | None = Field(None, description='The id used to reference this entry.')
    type: StrictStr | None = Field(None, description='TFA Entry Type.')

class GetAccessTfaUseridResponse(RootModel[list[GetAccessTfaUseridResponseItem]]):
    """List of items. list_user_tfa. List TFA configurations of users. response."""
    root: list[GetAccessTfaUseridResponseItem] = Field(..., description="A list of the user's TFA entries.")

class PostAccessTfaUseridRequest(ProxmoxBaseModel):
    """Model for add_tfa_entry. Add a TFA entry for a user. request."""
    challenge: StrictStr | None = Field(None, description='When responding to a u2f challenge: the original challenge string')
    description: StrictStr | None = Field(None, description='A description to distinguish multiple entries from one another')
    password: StrictStr | None = Field(None, description='The current password of the user performing the change.')
    totp: StrictStr | None = Field(None, description='A totp URI.')
    type: StrictStr = Field(..., description='TFA Entry Type.')
    value: StrictStr | None = Field(None, description='The current value for the provided totp URI, or a Webauthn/U2F challenge response')

class PostAccessTfaUseridResponse(ProxmoxBaseModel):
    """Model for add_tfa_entry. Add a TFA entry for a user. response."""
    challenge: StrictStr | None = Field(None, description='When adding u2f entries, this contains a challenge the user must respond to in order to finish the registration.')
    id: StrictStr = Field(..., description='The id of a newly added TFA entry.')
    recovery: list[StrictStr] | None = Field(None, description='When adding recovery codes, this contains the list of codes to be displayed to the user')

class DeleteAccessTfaUseridIdRequest(ProxmoxBaseModel):
    """Model for delete_tfa. Delete a TFA entry by ID. request."""
    password: StrictStr | None = Field(None, description='The current password of the user performing the change.')

class DeleteAccessTfaUseridIdResponse(RootModel[None]):
    """Model for delete_tfa. Delete a TFA entry by ID. response."""
    root: None = Field(...)

class GetAccessTfaUseridIdResponse(ProxmoxBaseModel):
    """Model for get_tfa_entry. Fetch a requested TFA entry if present. response."""
    created: int = Field(..., description='Creation time of this entry as unix epoch.')
    description: StrictStr = Field(..., description='User chosen description for this entry.')
    enable: bool | None = Field(None, description='Whether this TFA entry is currently enabled.')
    id: StrictStr = Field(..., description='The id used to reference this entry.')
    type: StrictStr = Field(..., description='TFA Entry Type.')

class PutAccessTfaUseridIdRequest(ProxmoxBaseModel):
    """Model for update_tfa_entry. Add a TFA entry for a user. request."""
    description: StrictStr | None = Field(None, description='A description to distinguish multiple entries from one another')
    enable: bool | None = Field(None, description='Whether the entry should be enabled for login.')
    password: StrictStr | None = Field(None, description='The current password of the user performing the change.')

class PutAccessTfaUseridIdResponse(RootModel[None]):
    """Model for update_tfa_entry. Add a TFA entry for a user. response."""
    root: None = Field(...)

class GetAccessTicketResponse(RootModel[None]):
    """Model for get_ticket. Dummy. Useful for formatters which want to provide a login page. response."""
    root: None = Field(...)

class PostAccessTicketRequest(ProxmoxBaseModel):
    """Model for create_ticket. Create or verify authentication ticket. request."""
    new_format: bool | None = Field(None, alias="new-format", description='This parameter is now ignored and assumed to be 1.')
    otp: StrictStr | None = Field(None, description='One-time password for Two-factor authentication.')
    password: StrictStr = Field(..., description='The secret password. This can also be a valid ticket.')
    path: StrictStr | None = Field(None, description="Verify ticket, and check if user have access 'privs' on 'path'")
    privs: StrictStr | None = Field(None, description="Verify ticket, and check if user have access 'privs' on 'path'")
    realm: StrictStr | None = Field(None, description='You can optionally pass the realm using this parameter. Normally the realm is simply added to the username <username>@<realm>.')
    tfa_challenge: StrictStr | None = Field(None, alias="tfa-challenge", description='The signed TFA challenge string the user wants to respond to.')
    username: StrictStr = Field(..., description='User name')

class PostAccessTicketResponse(ProxmoxBaseModel):
    """Model for create_ticket. Create or verify authentication ticket. response."""
    csrfprevention_token: StrictStr | None = Field(None, alias="CSRFPreventionToken")
    clustername: StrictStr | None = Field(None)
    ticket: StrictStr | None = Field(None)
    username: StrictStr = Field(...)

class GetAccessUsersResponseItem(ProxmoxBaseModel):
    """Model for index. User index. response."""
    comment: StrictStr | None = Field(None)
    email: StrictStr | None = Field(None)
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: StrictStr | None = Field(None)
    groups: StrictStr | None = Field(None)
    keys: StrictStr | None = Field(None, description='Keys for two factor auth (yubico).')
    lastname: StrictStr | None = Field(None)
    realm_type: StrictStr | None = Field(None, alias="realm-type", description='The type of the users realm')
    tfa_locked_until: int | None = Field(None, alias="tfa-locked-until", description='Contains a timestamp until when a user is locked out of 2nd factors.')
    tokens: list[dict[str, object]] | None = Field(None)
    totp_locked: bool | None = Field(None, alias="totp-locked", description='True if the user is currently locked out of TOTP factors.')
    userid: StrictStr | None = Field(None, description='Full User ID, in the `name@realm` format.')

class GetAccessUsersResponse(RootModel[list[GetAccessUsersResponseItem]]):
    """List of items. index. User index. response."""
    root: list[GetAccessUsersResponseItem] = Field(...)

class PostAccessUsersRequest(ProxmoxBaseModel):
    """Model for create_user. Create new user. request."""
    comment: StrictStr | None = Field(None)
    email: StrictStr | None = Field(None)
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: StrictStr | None = Field(None)
    groups: StrictStr | None = Field(None)
    keys: StrictStr | None = Field(None, description='Keys for two factor auth (yubico).')
    lastname: StrictStr | None = Field(None)
    password: StrictStr | None = Field(None, description='Initial password.')
    userid: StrictStr = Field(..., description='Full User ID, in the `name@realm` format.')

class PostAccessUsersResponse(RootModel[None]):
    """Model for create_user. Create new user. response."""
    root: None = Field(...)

class DeleteAccessUsersUseridRequest(RootModel[dict[str, object]]):
    """Model for delete_user. Delete user. request."""
    root: dict[str, object] = Field(...)

class DeleteAccessUsersUseridResponse(RootModel[None]):
    """Model for delete_user. Delete user. response."""
    root: None = Field(...)

class GetAccessUsersUseridResponse(ProxmoxBaseModel):
    """Model for read_user. Get user configuration. response."""
    comment: StrictStr | None = Field(None)
    email: StrictStr | None = Field(None)
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: StrictStr | None = Field(None)
    groups: list[StrictStr] | None = Field(None)
    keys: StrictStr | None = Field(None, description='Keys for two factor auth (yubico).')
    lastname: StrictStr | None = Field(None)
    tokens: dict[str, object] | None = Field(None)

class PutAccessUsersUseridRequest(ProxmoxBaseModel):
    """Model for update_user. Update user configuration. request."""
    append: bool | None = Field(None)
    comment: StrictStr | None = Field(None)
    email: StrictStr | None = Field(None)
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: StrictStr | None = Field(None)
    groups: StrictStr | None = Field(None)
    keys: StrictStr | None = Field(None, description='Keys for two factor auth (yubico).')
    lastname: StrictStr | None = Field(None)

class PutAccessUsersUseridResponse(RootModel[None]):
    """Model for update_user. Update user configuration. response."""
    root: None = Field(...)

class GetAccessUsersUseridTfaResponse(ProxmoxBaseModel):
    """Model for read_user_tfa_type. Get user TFA types (Personal and Realm). response."""
    realm: StrictStr | None = Field(None, description='The type of TFA the users realm has set, if any.')
    types: list[StrictStr] | None = Field(None, description="Array of the user configured TFA types, if any. Only available if 'multiple' was not passed.")
    user: StrictStr | None = Field(None, description="The type of TFA the user has set, if any. Only set if 'multiple' was not passed.")

class GetAccessUsersUseridTokenResponseItem(ProxmoxBaseModel):
    """Model for token_index. Get user API tokens. response."""
    comment: StrictStr | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')
    tokenid: StrictStr | None = Field(None, description='User-specific token identifier.')

class GetAccessUsersUseridTokenResponse(RootModel[list[GetAccessUsersUseridTokenResponseItem]]):
    """List of items. token_index. Get user API tokens. response."""
    root: list[GetAccessUsersUseridTokenResponseItem] = Field(...)

class DeleteAccessUsersUseridTokenTokenidRequest(RootModel[dict[str, object]]):
    """Model for remove_token. Remove API token for a specific user. request."""
    root: dict[str, object] = Field(...)

class DeleteAccessUsersUseridTokenTokenidResponse(RootModel[None]):
    """Model for remove_token. Remove API token for a specific user. response."""
    root: None = Field(...)

class GetAccessUsersUseridTokenTokenidResponse(ProxmoxBaseModel):
    """Model for read_token. Get specific API token information. response."""
    comment: StrictStr | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')

class PostAccessUsersUseridTokenTokenidRequest(ProxmoxBaseModel):
    """Model for generate_token. Generate a new API token for a specific user. NOTE: returns API token value, which needs to be stored as it cannot be retrieved afterwards! request."""
    comment: StrictStr | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')

class PostAccessUsersUseridTokenTokenidResponse(ProxmoxBaseModel):
    """Model for generate_token. Generate a new API token for a specific user. NOTE: returns API token value, which needs to be stored as it cannot be retrieved afterwards! response."""
    full_tokenid: StrictStr = Field(..., alias="full-tokenid", description='The full token id.')
    info: dict[str, object] = Field(...)
    value: StrictStr = Field(..., description='API token value used for authentication.')

class PutAccessUsersUseridTokenTokenidRequest(ProxmoxBaseModel):
    """Model for update_token_info. Update API token for a specific user. request."""
    comment: StrictStr | None = Field(None)
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')

class PutAccessUsersUseridTokenTokenidResponse(ProxmoxBaseModel):
    """Model for update_token_info. Update API token for a specific user. response."""
    comment: StrictStr | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')

class PutAccessUsersUseridUnlockTfaRequest(RootModel[dict[str, object]]):
    """Model for unlock_tfa. Unlock a user's TFA authentication. request."""
    root: dict[str, object] = Field(...)

class PutAccessUsersUseridUnlockTfaResponse(RootModel[bool]):
    """Model for unlock_tfa. Unlock a user's TFA authentication. response."""
    root: bool = Field(...)

class PostAccessVncticketRequest(ProxmoxBaseModel):
    """Model for verify_vnc_ticket. verify VNC authentication ticket. request."""
    authid: StrictStr = Field(..., description='UserId or token')
    path: StrictStr = Field(..., description="Verify ticket, and check if user have access 'privs' on 'path'")
    port: int | None = Field(None, description='Verify that the ticket is valid for this port.')
    privs: StrictStr = Field(..., description="Verify ticket, and check if user have access 'privs' on 'path'")
    vncticket: StrictStr = Field(..., description='The VNC ticket.')

class PostAccessVncticketResponse(RootModel[None]):
    """Model for verify_vnc_ticket. verify VNC authentication ticket. response."""
    root: None = Field(...)

class GetClusterResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Cluster index. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterAcmeResponse(RootModel[list[dict[str, object]]]):
    """Model for index. ACMEAccount index. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterAcmeAccountResponse(RootModel[list[dict[str, object]]]):
    """Model for account_index. ACMEAccount index. response."""
    root: list[dict[str, object]] = Field(...)

class PostClusterAcmeAccountRequest(ProxmoxBaseModel):
    """Model for register_account. Register a new ACME account with CA. request."""
    contact: StrictStr = Field(..., description='Contact email addresses.')
    directory: StrictStr | None = Field(None, description='URL of ACME CA directory endpoint.')
    eab_hmac_key: StrictStr | None = Field(None, alias="eab-hmac-key", description='HMAC key for External Account Binding.')
    eab_kid: StrictStr | None = Field(None, alias="eab-kid", description='Key Identifier for External Account Binding.')
    name: StrictStr | None = Field(None, description='ACME account config file name.')
    tos_url: StrictStr | None = Field(None, description='URL of CA TermsOfService - setting this indicates agreement.')

class PostClusterAcmeAccountResponse(RootModel[StrictStr]):
    """Model for register_account. Register a new ACME account with CA. response."""
    root: StrictStr = Field(...)

class DeleteClusterAcmeAccountNameRequest(RootModel[dict[str, object]]):
    """Model for deactivate_account. Deactivate existing ACME account at CA. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterAcmeAccountNameResponse(RootModel[StrictStr]):
    """Model for deactivate_account. Deactivate existing ACME account at CA. response."""
    root: StrictStr = Field(...)

class GetClusterAcmeAccountNameResponse(ProxmoxBaseModel):
    """Model for get_account. Return existing ACME account information. response."""
    account: dict[str, object] | None = Field(None)
    directory: StrictStr | None = Field(None, description='URL of ACME CA directory endpoint.')
    location: StrictStr | None = Field(None)
    tos: StrictStr | None = Field(None)

class PutClusterAcmeAccountNameRequest(ProxmoxBaseModel):
    """Model for update_account. Update existing ACME account information with CA. Note: not specifying any new account information triggers a refresh. request."""
    contact: StrictStr | None = Field(None, description='Contact email addresses.')

class PutClusterAcmeAccountNameResponse(RootModel[StrictStr]):
    """Model for update_account. Update existing ACME account information with CA. Note: not specifying any new account information triggers a refresh. response."""
    root: StrictStr = Field(...)

class GetClusterAcmeChallengeSchemaResponseItem(ProxmoxBaseModel):
    """Model for challengeschema. Get schema of ACME challenge types. response."""
    id: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None, description='Human readable name, falls back to id')
    schema: dict[str, object] | None = Field(None)
    type: StrictStr | None = Field(None)

class GetClusterAcmeChallengeSchemaResponse(RootModel[list[GetClusterAcmeChallengeSchemaResponseItem]]):
    """List of items. challengeschema. Get schema of ACME challenge types. response."""
    root: list[GetClusterAcmeChallengeSchemaResponseItem] = Field(...)

class GetClusterAcmeDirectoriesResponseItem(ProxmoxBaseModel):
    """Model for get_directories. Get named known ACME directory endpoints. response."""
    name: StrictStr | None = Field(None)
    url: StrictStr | None = Field(None, description='URL of ACME CA directory endpoint.')

class GetClusterAcmeDirectoriesResponse(RootModel[list[GetClusterAcmeDirectoriesResponseItem]]):
    """List of items. get_directories. Get named known ACME directory endpoints. response."""
    root: list[GetClusterAcmeDirectoriesResponseItem] = Field(...)

class GetClusterAcmeMetaResponse(ProxmoxBaseModel):
    """Model for get_meta. Retrieve ACME Directory Meta Information response."""
    caa_identities: list[StrictStr] | None = Field(None, alias="caaIdentities", description='Hostnames referring to the ACME servers.')
    external_account_required: bool | None = Field(None, alias="externalAccountRequired", description='EAB Required')
    terms_of_service: StrictStr | None = Field(None, alias="termsOfService", description='ACME TermsOfService URL.')
    website: StrictStr | None = Field(None, description='URL to more information about the ACME server.')

class GetClusterAcmePluginsResponseItem(ProxmoxBaseModel):
    """Model for index. ACME plugin index. response."""
    api: StrictStr | None = Field(None, description='API plugin name')
    data: StrictStr | None = Field(None, description='DNS plugin data. (base64 encoded)')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    plugin: StrictStr | None = Field(None, description='Unique identifier for ACME plugin instance.')
    type: StrictStr | None = Field(None, description='ACME challenge type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.')

class GetClusterAcmePluginsResponse(RootModel[list[GetClusterAcmePluginsResponseItem]]):
    """List of items. index. ACME plugin index. response."""
    root: list[GetClusterAcmePluginsResponseItem] = Field(...)

class PostClusterAcmePluginsRequest(ProxmoxBaseModel):
    """Model for add_plugin. Add ACME plugin configuration. request."""
    api: StrictStr | None = Field(None, description='API plugin name')
    data: StrictStr | None = Field(None, description='DNS plugin data. (base64 encoded)')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    id: StrictStr = Field(..., description='ACME Plugin ID name')
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    type: StrictStr = Field(..., description='ACME challenge type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.')

class PostClusterAcmePluginsResponse(RootModel[None]):
    """Model for add_plugin. Add ACME plugin configuration. response."""
    root: None = Field(...)

class DeleteClusterAcmePluginsIdRequest(RootModel[dict[str, object]]):
    """Model for delete_plugin. Delete ACME plugin configuration. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterAcmePluginsIdResponse(RootModel[None]):
    """Model for delete_plugin. Delete ACME plugin configuration. response."""
    root: None = Field(...)

class GetClusterAcmePluginsIdResponse(ProxmoxBaseModel):
    """Model for get_plugin_config. Get ACME plugin configuration. response."""
    api: StrictStr | None = Field(None, description='API plugin name')
    data: StrictStr | None = Field(None, description='DNS plugin data. (base64 encoded)')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    plugin: StrictStr = Field(..., description='Unique identifier for ACME plugin instance.')
    type: StrictStr = Field(..., description='ACME challenge type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.')

class PutClusterAcmePluginsIdRequest(ProxmoxBaseModel):
    """Model for update_plugin. Update ACME plugin configuration. request."""
    api: StrictStr | None = Field(None, description='API plugin name')
    data: StrictStr | None = Field(None, description='DNS plugin data. (base64 encoded)')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation. Allows to cope with a long TTL of DNS records.')

class PutClusterAcmePluginsIdResponse(RootModel[None]):
    """Model for update_plugin. Update ACME plugin configuration. response."""
    root: None = Field(...)

class GetClusterAcmeTosResponse(RootModel[StrictStr]):
    """Model for get_tos. Retrieve ACME TermsOfService URL from CA. Deprecated, please use /cluster/acme/meta. response."""
    root: StrictStr = Field(..., description='ACME TermsOfService URL.')

class GetClusterBackupResponseItem(ProxmoxBaseModel):
    """Model for index. List vzdump backup schedule. response."""
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    comment: StrictStr | None = Field(None, description='Description for the Job.')
    compress: StrictStr | None = Field(None, description='Compress dump file.')
    dumpdir: StrictStr | None = Field(None, description='Store resulting files to specified directory.')
    enabled: bool | None = Field(None, description='Enable or disable the job.')
    exclude: StrictStr | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[StrictStr] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: dict[str, object] | None = Field(None, description='Options for backup fleecing (VM only).')
    id: StrictStr | None = Field(None, description='The job ID.')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: StrictStr | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: StrictStr | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: StrictStr | None = Field(None, description='Backup mode.')
    next_run: int | None = Field(None, alias="next-run", description='UNIX timestamp when this backup job will be executed next')
    node: StrictStr | None = Field(None, description='Only run if executed on this node.')
    notes_template: StrictStr | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: StrictStr | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: StrictStr | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: dict[str, object] | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: StrictStr | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: dict[str, object] | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    repeat_missed: bool | None = Field(None, alias="repeat-missed", description='If true, the job will be run as soon as possible if it was missed while the scheduler was not running.')
    schedule: StrictStr | None = Field(None, description='Backup schedule. The format is a subset of `systemd` calendar events.')
    script: StrictStr | None = Field(None, description='Use specified hook script.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: StrictStr | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: StrictStr | None = Field(None, description='Store temporary files to specified directory.')
    vmid: StrictStr | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class GetClusterBackupResponse(RootModel[list[GetClusterBackupResponseItem]]):
    """List of items. index. List vzdump backup schedule. response."""
    root: list[GetClusterBackupResponseItem] = Field(...)

class PostClusterBackupRequest(ProxmoxBaseModel):
    """Model for create_job. Create new vzdump backup job. request."""
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    comment: StrictStr | None = Field(None, description='Description for the Job.')
    compress: StrictStr | None = Field(None, description='Compress dump file.')
    dow: StrictStr | None = Field(None, description="Deprecated: Use 'schedule' instead. Day of week selection. 'starttime' and 'dow' will be converted into 'schedule' if used.")
    dumpdir: StrictStr | None = Field(None, description='Store resulting files to specified directory.')
    enabled: bool | None = Field(None, description='Enable or disable the job.')
    exclude: StrictStr | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[StrictStr] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: StrictStr | None = Field(None, description='Options for backup fleecing (VM only).')
    id: StrictStr | None = Field(None, description='Job ID (will be autogenerated).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: StrictStr | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: StrictStr | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: StrictStr | None = Field(None, description='Backup mode.')
    node: StrictStr | None = Field(None, description='Only run if executed on this node.')
    notes_template: StrictStr | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: StrictStr | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: StrictStr | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: StrictStr | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: StrictStr | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    repeat_missed: bool | None = Field(None, alias="repeat-missed", description='If true, the job will be run as soon as possible if it was missed while the scheduler was not running.')
    schedule: StrictStr | None = Field(None, description='Backup schedule. The format is a subset of `systemd` calendar events.')
    script: StrictStr | None = Field(None, description='Use specified hook script.')
    starttime: StrictStr | None = Field(None, description="Deprecated: Use 'schedule' instead. Job Start time. 'starttime' and 'dow' will be converted into 'schedule' if used.")
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: StrictStr | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: StrictStr | None = Field(None, description='Store temporary files to specified directory.')
    vmid: StrictStr | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class PostClusterBackupResponse(RootModel[None]):
    """Model for create_job. Create new vzdump backup job. response."""
    root: None = Field(...)

class GetClusterBackupInfoResponseItem(ProxmoxBaseModel):
    """Model for index. Index for backup info related endpoints response."""
    subdir: StrictStr | None = Field(None, description='API sub-directory endpoint')

class GetClusterBackupInfoResponse(RootModel[list[GetClusterBackupInfoResponseItem]]):
    """List of items. index. Index for backup info related endpoints response."""
    root: list[GetClusterBackupInfoResponseItem] = Field(..., description='Directory index.')

class GetClusterBackupInfoNotBackedUpResponseItem(ProxmoxBaseModel):
    """Model for get_guests_not_in_backup. Shows all guests which are not covered by any backup job. response."""
    name: StrictStr | None = Field(None, description='Name of the guest')
    type: StrictStr | None = Field(None, description='Type of the guest.')
    vmid: int | None = Field(None, description='VMID of the guest.')

class GetClusterBackupInfoNotBackedUpResponse(RootModel[list[GetClusterBackupInfoNotBackedUpResponseItem]]):
    """List of items. get_guests_not_in_backup. Shows all guests which are not covered by any backup job. response."""
    root: list[GetClusterBackupInfoNotBackedUpResponseItem] = Field(..., description='Contains the guest objects.')

class DeleteClusterBackupIdRequest(RootModel[dict[str, object]]):
    """Model for delete_job. Delete vzdump backup job definition. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterBackupIdResponse(RootModel[None]):
    """Model for delete_job. Delete vzdump backup job definition. response."""
    root: None = Field(...)

class GetClusterBackupIdResponse(ProxmoxBaseModel):
    """Model for read_job. Read vzdump backup job definition. response."""
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    comment: StrictStr | None = Field(None, description='Description for the Job.')
    compress: StrictStr | None = Field(None, description='Compress dump file.')
    dumpdir: StrictStr | None = Field(None, description='Store resulting files to specified directory.')
    enabled: bool | None = Field(None, description='Enable or disable the job.')
    exclude: StrictStr | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[StrictStr] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: dict[str, object] | None = Field(None, description='Options for backup fleecing (VM only).')
    id: StrictStr = Field(..., description='The job ID.')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: StrictStr | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: StrictStr | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: StrictStr | None = Field(None, description='Backup mode.')
    next_run: int | None = Field(None, alias="next-run", description='UNIX timestamp when this backup job will be executed next')
    node: StrictStr | None = Field(None, description='Only run if executed on this node.')
    notes_template: StrictStr | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: StrictStr | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: StrictStr | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: dict[str, object] | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: StrictStr | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: dict[str, object] | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    repeat_missed: bool | None = Field(None, alias="repeat-missed", description='If true, the job will be run as soon as possible if it was missed while the scheduler was not running.')
    schedule: StrictStr | None = Field(None, description='Backup schedule. The format is a subset of `systemd` calendar events.')
    script: StrictStr | None = Field(None, description='Use specified hook script.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: StrictStr | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: StrictStr | None = Field(None, description='Store temporary files to specified directory.')
    vmid: StrictStr | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class PutClusterBackupIdRequest(ProxmoxBaseModel):
    """Model for update_job. Update vzdump backup job definition. request."""
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    comment: StrictStr | None = Field(None, description='Description for the Job.')
    compress: StrictStr | None = Field(None, description='Compress dump file.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dow: StrictStr | None = Field(None, description="Deprecated: Use 'schedule' instead. Day of week selection. 'starttime' and 'dow' will be converted into 'schedule' if used.")
    dumpdir: StrictStr | None = Field(None, description='Store resulting files to specified directory.')
    enabled: bool | None = Field(None, description='Enable or disable the job.')
    exclude: StrictStr | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[StrictStr] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: StrictStr | None = Field(None, description='Options for backup fleecing (VM only).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: StrictStr | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: StrictStr | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: StrictStr | None = Field(None, description='Backup mode.')
    node: StrictStr | None = Field(None, description='Only run if executed on this node.')
    notes_template: StrictStr | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: StrictStr | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: StrictStr | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: StrictStr | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: StrictStr | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    repeat_missed: bool | None = Field(None, alias="repeat-missed", description='If true, the job will be run as soon as possible if it was missed while the scheduler was not running.')
    schedule: StrictStr | None = Field(None, description='Backup schedule. The format is a subset of `systemd` calendar events.')
    script: StrictStr | None = Field(None, description='Use specified hook script.')
    starttime: StrictStr | None = Field(None, description="Deprecated: Use 'schedule' instead. Job Start time. 'starttime' and 'dow' will be converted into 'schedule' if used.")
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: StrictStr | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: StrictStr | None = Field(None, description='Store temporary files to specified directory.')
    vmid: StrictStr | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class PutClusterBackupIdResponse(RootModel[None]):
    """Model for update_job. Update vzdump backup job definition. response."""
    root: None = Field(...)

class GetClusterBackupIdIncludedVolumesResponse(ProxmoxBaseModel):
    """Model for get_volume_backup_included. Returns included guests and the backup status of their disks. Optimized to be used in ExtJS tree views. response."""
    children: list[dict[str, object]] = Field(...)

class GetClusterBulkActionResponse(RootModel[list[dict[str, object]]]):
    """Model for index. List resource types. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterBulkActionGuestResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Bulk action index. response."""
    root: list[dict[str, object]] = Field(...)

class PostClusterBulkActionGuestMigrateRequest(ProxmoxBaseModel):
    """Model for migrate. Bulk migrate all guests on the cluster. request."""
    max_workers: int | None = Field(None, alias="max-workers", description='Defines the maximum number of tasks running concurrently.')
    maxworkers: int | None = Field(None, description="Defines the maximum number of tasks running concurrently. Deprecated, use 'max-workers' instead.")
    online: bool | None = Field(None, description='Enable live migration for VMs and restart migration for CTs.')
    target: StrictStr = Field(..., description='Target node.')
    vms: list[int] | None = Field(None, description='Only consider guests from this list of VMIDs.')
    with_local_disks: bool | None = Field(None, alias="with-local-disks", description='Enable live storage migration for local disk')

class PostClusterBulkActionGuestMigrateResponse(RootModel[StrictStr]):
    """Model for migrate. Bulk migrate all guests on the cluster. response."""
    root: StrictStr = Field(..., description='UPID of the worker')

class PostClusterBulkActionGuestShutdownRequest(ProxmoxBaseModel):
    """Model for shutdown. Bulk shutdown all guests on the cluster. request."""
    force_stop: bool | None = Field(None, alias="force-stop", description='Makes sure the Guest stops after the timeout.')
    max_workers: int | None = Field(None, alias="max-workers", description='Defines the maximum number of tasks running concurrently.')
    maxworkers: int | None = Field(None, description="Defines the maximum number of tasks running concurrently. Deprecated, use 'max-workers' instead.")
    timeout: int | None = Field(None, description='Default shutdown timeout in seconds if none is configured for the guest.')
    vms: list[int] | None = Field(None, description='Only consider guests from this list of VMIDs.')

class PostClusterBulkActionGuestShutdownResponse(RootModel[StrictStr]):
    """Model for shutdown. Bulk shutdown all guests on the cluster. response."""
    root: StrictStr = Field(..., description='UPID of the worker')

class PostClusterBulkActionGuestStartRequest(ProxmoxBaseModel):
    """Model for start. Bulk start or resume all guests on the cluster. request."""
    max_workers: int | None = Field(None, alias="max-workers", description='Defines the maximum number of tasks running concurrently.')
    maxworkers: int | None = Field(None, description="Defines the maximum number of tasks running concurrently. Deprecated, use 'max-workers' instead.")
    timeout: int | None = Field(None, description='Default start timeout in seconds. Only valid for VMs. (default depends on the guest configuration).')
    vms: list[int] | None = Field(None, description='Only consider guests from this list of VMIDs.')

class PostClusterBulkActionGuestStartResponse(RootModel[StrictStr]):
    """Model for start. Bulk start or resume all guests on the cluster. response."""
    root: StrictStr = Field(..., description='UPID of the worker')

class PostClusterBulkActionGuestSuspendRequest(ProxmoxBaseModel):
    """Model for suspend. Bulk suspend all guests on the cluster. request."""
    max_workers: int | None = Field(None, alias="max-workers", description='Defines the maximum number of tasks running concurrently.')
    maxworkers: int | None = Field(None, description="Defines the maximum number of tasks running concurrently. Deprecated, use 'max-workers' instead.")
    statestorage: StrictStr | None = Field(None, description='The storage for the VM state.')
    to_disk: bool | None = Field(None, alias="to-disk", description='If set, suspends the guests to disk. Will be resumed on next start.')
    vms: list[int] | None = Field(None, description='Only consider guests from this list of VMIDs.')

class PostClusterBulkActionGuestSuspendResponse(RootModel[StrictStr]):
    """Model for suspend. Bulk suspend all guests on the cluster. response."""
    root: StrictStr = Field(..., description='UPID of the worker')

class GetClusterCephResponse(RootModel[list[dict[str, object]]]):
    """Model for cephindex. Cluster ceph index. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterCephFlagsResponseItem(ProxmoxBaseModel):
    """Model for get_all_flags. get the status of all ceph flags response."""
    description: StrictStr | None = Field(None, description='Flag description.')
    name: StrictStr | None = Field(None, description='Flag name.')
    value: bool | None = Field(None, description='Flag value.')

class GetClusterCephFlagsResponse(RootModel[list[GetClusterCephFlagsResponseItem]]):
    """List of items. get_all_flags. get the status of all ceph flags response."""
    root: list[GetClusterCephFlagsResponseItem] = Field(...)

class PutClusterCephFlagsRequest(ProxmoxBaseModel):
    """Model for set_flags. Set/Unset multiple ceph flags at once. request."""
    nobackfill: bool | None = Field(None, description='Backfilling of PGs is suspended.')
    nodeep_scrub: bool | None = Field(None, alias="nodeep-scrub", description='Deep Scrubbing is disabled.')
    nodown: bool | None = Field(None, description='OSD failure reports are being ignored, such that the monitors will not mark OSDs down.')
    noin: bool | None = Field(None, description='OSDs that were previously marked out will not be marked back in when they start.')
    noout: bool | None = Field(None, description='OSDs will not automatically be marked out after the configured interval.')
    norebalance: bool | None = Field(None, description='Rebalancing of PGs is suspended.')
    norecover: bool | None = Field(None, description='Recovery of PGs is suspended.')
    noscrub: bool | None = Field(None, description='Scrubbing is disabled.')
    notieragent: bool | None = Field(None, description='Cache tiering activity is suspended.')
    noup: bool | None = Field(None, description='OSDs are not allowed to start.')
    pause: bool | None = Field(None, description='Pauses read and writes.')

class PutClusterCephFlagsResponse(RootModel[StrictStr]):
    """Model for set_flags. Set/Unset multiple ceph flags at once. response."""
    root: StrictStr = Field(...)

class GetClusterCephFlagsFlagResponse(RootModel[bool]):
    """Model for get_flag. Get the status of a specific ceph flag. response."""
    root: bool = Field(...)

class PutClusterCephFlagsFlagRequest(ProxmoxBaseModel):
    """Model for update_flag. Set or clear (unset) a specific ceph flag request."""
    value: bool = Field(..., description='The new value of the flag')

class PutClusterCephFlagsFlagResponse(RootModel[None]):
    """Model for update_flag. Set or clear (unset) a specific ceph flag response."""
    root: None = Field(...)

class GetClusterCephMetadataResponse(ProxmoxBaseModel):
    """Model for metadata. Get ceph metadata. response."""
    mds: dict[str, object] = Field(..., description='Metadata servers configured in the cluster and their properties.')
    mgr: dict[str, object] = Field(..., description='Managers configured in the cluster and their properties.')
    mon: dict[str, object] = Field(..., description='Monitors configured in the cluster and their properties.')
    node: dict[str, object] = Field(..., description='Ceph version installed on the nodes.')
    osd: list[object] = Field(..., description='OSDs configured in the cluster and their properties.')

class GetClusterCephStatusResponse(RootModel[dict[str, object]]):
    """Model for status. Get ceph status. response."""
    root: dict[str, object] = Field(...)

class GetClusterConfigResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class PostClusterConfigRequest(ProxmoxBaseModel):
    """Model for create. Generate new cluster configuration. If no links given, default to local IP address as link0. request."""
    clustername: StrictStr = Field(..., description='The name of the cluster.')
    link_n: StrictStr | None = Field(None, alias="link[n]", description='Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)')
    nodeid: int | None = Field(None, description='Node id for this node.')
    token_coefficient: int | None = Field(None, alias="token-coefficient", description="Coefficient used to determine Corosync's token timeout. See the corosync.conf(5) manual for more details.")
    votes: int | None = Field(None, description='Number of votes for this node.')

class PostClusterConfigResponse(RootModel[StrictStr]):
    """Model for create. Generate new cluster configuration. If no links given, default to local IP address as link0. response."""
    root: StrictStr = Field(...)

class GetClusterConfigApiversionResponse(RootModel[int]):
    """Model for join_api_version. Return the version of the cluster join API available on this node. response."""
    root: int = Field(..., description='Cluster Join API version, currently 1')

class GetClusterConfigJoinResponse(ProxmoxBaseModel):
    """Model for join_info. Get information needed to join this cluster over the connected node. response."""
    config_digest: StrictStr = Field(...)
    nodelist: list[dict[str, object]] = Field(...)
    preferred_node: StrictStr = Field(..., description='The cluster node name.')
    totem: dict[str, object] = Field(...)

class PostClusterConfigJoinRequest(ProxmoxBaseModel):
    """Model for join. Joins this node into an existing cluster. If no links are given, default to IP resolved by node's hostname on single link (fallback fails for clusters with multiple links). request."""
    fingerprint: StrictStr = Field(..., description='Certificate SHA 256 fingerprint.')
    force: bool | None = Field(None, description='Do not throw error if node already exists.')
    hostname: StrictStr = Field(..., description='Hostname (or IP) of an existing cluster member.')
    link_n: StrictStr | None = Field(None, alias="link[n]", description='Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)')
    nodeid: int | None = Field(None, description='Node id for this node.')
    password: StrictStr = Field(..., description='Superuser (root) password of peer node.')
    votes: int | None = Field(None, description='Number of votes for this node')

class PostClusterConfigJoinResponse(RootModel[StrictStr]):
    """Model for join. Joins this node into an existing cluster. If no links are given, default to IP resolved by node's hostname on single link (fallback fails for clusters with multiple links). response."""
    root: StrictStr = Field(...)

class GetClusterConfigNodesResponseItem(ProxmoxBaseModel):
    """Model for nodes. Corosync node list. response."""
    node: StrictStr | None = Field(None)

class GetClusterConfigNodesResponse(RootModel[list[GetClusterConfigNodesResponseItem]]):
    """List of items. nodes. Corosync node list. response."""
    root: list[GetClusterConfigNodesResponseItem] = Field(...)

class DeleteClusterConfigNodesNodeRequest(RootModel[dict[str, object]]):
    """Model for delnode. Removes a node from the cluster configuration. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterConfigNodesNodeResponse(RootModel[None]):
    """Model for delnode. Removes a node from the cluster configuration. response."""
    root: None = Field(...)

class PostClusterConfigNodesNodeRequest(ProxmoxBaseModel):
    """Model for addnode. Adds a node to the cluster configuration. This call is for internal use. request."""
    apiversion: int | None = Field(None, description='The JOIN_API_VERSION of the new node.')
    force: bool | None = Field(None, description='Do not throw error if node already exists.')
    link_n: StrictStr | None = Field(None, alias="link[n]", description='Address and priority information of a single corosync link. (up to 8 links supported; link0..link7)')
    new_node_ip: StrictStr | None = Field(None, description='IP Address of node to add. Used as fallback if no links are given.')
    nodeid: int | None = Field(None, description='Node id for this node.')
    votes: int | None = Field(None, description='Number of votes for this node')

class PostClusterConfigNodesNodeResponse(ProxmoxBaseModel):
    """Model for addnode. Adds a node to the cluster configuration. This call is for internal use. response."""
    corosync_authkey: StrictStr = Field(...)
    corosync_conf: StrictStr = Field(...)
    warnings: list[StrictStr] = Field(...)

class GetClusterConfigQdeviceResponse(RootModel[dict[str, object]]):
    """Model for status. Get QDevice status response."""
    root: dict[str, object] = Field(...)

class GetClusterConfigTotemResponse(RootModel[dict[str, object]]):
    """Model for totem. Get corosync totem protocol settings. response."""
    root: dict[str, object] = Field(...)

class GetClusterFirewallResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterFirewallAliasesResponseItem(ProxmoxBaseModel):
    """Model for get_aliases. List aliases response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None)

class GetClusterFirewallAliasesResponse(RootModel[list[GetClusterFirewallAliasesResponseItem]]):
    """List of items. get_aliases. List aliases response."""
    root: list[GetClusterFirewallAliasesResponseItem] = Field(...)

class PostClusterFirewallAliasesRequest(ProxmoxBaseModel):
    """Model for create_alias. Create IP or Network Alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    name: StrictStr = Field(..., description='Alias name.')

class PostClusterFirewallAliasesResponse(RootModel[None]):
    """Model for create_alias. Create IP or Network Alias. response."""
    root: None = Field(...)

class DeleteClusterFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for remove_alias. Remove IP or Network alias. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterFirewallAliasesNameResponse(RootModel[None]):
    """Model for remove_alias. Remove IP or Network alias. response."""
    root: None = Field(...)

class GetClusterFirewallAliasesNameResponse(RootModel[dict[str, object]]):
    """Model for read_alias. Read alias. response."""
    root: dict[str, object] = Field(...)

class PutClusterFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for update_alias. Update IP or Network alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    rename: StrictStr | None = Field(None, description='Rename an existing alias.')

class PutClusterFirewallAliasesNameResponse(RootModel[None]):
    """Model for update_alias. Update IP or Network alias. response."""
    root: None = Field(...)

class GetClusterFirewallGroupsResponseItem(ProxmoxBaseModel):
    """Model for list_security_groups. List security groups. response."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    group: StrictStr | None = Field(None, description='Security Group name.')

class GetClusterFirewallGroupsResponse(RootModel[list[GetClusterFirewallGroupsResponseItem]]):
    """List of items. list_security_groups. List security groups. response."""
    root: list[GetClusterFirewallGroupsResponseItem] = Field(...)

class PostClusterFirewallGroupsRequest(ProxmoxBaseModel):
    """Model for create_security_group. Create new security group. request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    group: StrictStr = Field(..., description='Security Group name.')
    rename: StrictStr | None = Field(None, description="Rename/update an existing security group. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing group.")

class PostClusterFirewallGroupsResponse(RootModel[None]):
    """Model for create_security_group. Create new security group. response."""
    root: None = Field(...)

class DeleteClusterFirewallGroupsGroupRequest(RootModel[dict[str, object]]):
    """Model for delete_security_group. Delete security group. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterFirewallGroupsGroupResponse(RootModel[None]):
    """Model for delete_security_group. Delete security group. response."""
    root: None = Field(...)

class GetClusterFirewallGroupsGroupResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetClusterFirewallGroupsGroupResponse(RootModel[list[GetClusterFirewallGroupsGroupResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetClusterFirewallGroupsGroupResponseItem] = Field(...)

class PostClusterFirewallGroupsGroupRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostClusterFirewallGroupsGroupResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteClusterFirewallGroupsGroupPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterFirewallGroupsGroupPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetClusterFirewallGroupsGroupPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutClusterFirewallGroupsGroupPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutClusterFirewallGroupsGroupPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class GetClusterFirewallIpsetResponseItem(ProxmoxBaseModel):
    """Model for ipset_index. List IPSets response."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None, description='IP set name.')

class GetClusterFirewallIpsetResponse(RootModel[list[GetClusterFirewallIpsetResponseItem]]):
    """List of items. ipset_index. List IPSets response."""
    root: list[GetClusterFirewallIpsetResponseItem] = Field(...)

class PostClusterFirewallIpsetRequest(ProxmoxBaseModel):
    """Model for create_ipset. Create new IPSet request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr = Field(..., description='IP set name.')
    rename: StrictStr | None = Field(None, description="Rename an existing IPSet. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing IPSet.")

class PostClusterFirewallIpsetResponse(RootModel[None]):
    """Model for create_ipset. Create new IPSet response."""
    root: None = Field(...)

class DeleteClusterFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for delete_ipset. Delete IPSet request."""
    force: bool | None = Field(None, description='Delete all members of the IPSet, if there are any.')

class DeleteClusterFirewallIpsetNameResponse(RootModel[None]):
    """Model for delete_ipset. Delete IPSet response."""
    root: None = Field(...)

class GetClusterFirewallIpsetNameResponseItem(ProxmoxBaseModel):
    """Model for get_ipset. List IPSet content response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class GetClusterFirewallIpsetNameResponse(RootModel[list[GetClusterFirewallIpsetNameResponseItem]]):
    """List of items. get_ipset. List IPSet content response."""
    root: list[GetClusterFirewallIpsetNameResponseItem] = Field(...)

class PostClusterFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for create_ip. Add IP or Network to IPSet. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    nomatch: bool | None = Field(None)

class PostClusterFirewallIpsetNameResponse(RootModel[None]):
    """Model for create_ip. Add IP or Network to IPSet. response."""
    root: None = Field(...)

class DeleteClusterFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for remove_ip. Remove IP or Network from IPSet. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for remove_ip. Remove IP or Network from IPSet. response."""
    root: None = Field(...)

class GetClusterFirewallIpsetNameCidrResponse(RootModel[dict[str, object]]):
    """Model for read_ip. Read IP or Network settings from IPSet. response."""
    root: dict[str, object] = Field(...)

class PutClusterFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for update_ip. Update IP or Network settings request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class PutClusterFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for update_ip. Update IP or Network settings response."""
    root: None = Field(...)

class GetClusterFirewallMacrosResponseItem(ProxmoxBaseModel):
    """Model for get_macros. List available macros response."""
    descr: StrictStr | None = Field(None, description='More verbose description (if available).')
    macro: StrictStr | None = Field(None, description='Macro name.')

class GetClusterFirewallMacrosResponse(RootModel[list[GetClusterFirewallMacrosResponseItem]]):
    """List of items. get_macros. List available macros response."""
    root: list[GetClusterFirewallMacrosResponseItem] = Field(...)

class GetClusterFirewallOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get Firewall options. response."""
    ebtables: bool | None = Field(None, description='Enable ebtables rules cluster wide.')
    enable: int | None = Field(None, description='Enable or disable the firewall cluster wide.')
    log_ratelimit: StrictBool | Annotated[StrictInt, Field(ge=0, le=1)] | StrictStr | None = Field(None, description='Log ratelimiting settings')
    policy_forward: StrictStr | None = Field(None, description='Forward policy.')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')

class PutClusterFirewallOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set Firewall options. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    ebtables: bool | None = Field(None, description='Enable ebtables rules cluster wide.')
    enable: int | None = Field(None, description='Enable or disable the firewall cluster wide.')
    log_ratelimit: StrictStr | None = Field(None, description='Log ratelimiting settings')
    policy_forward: StrictStr | None = Field(None, description='Forward policy.')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')

class PutClusterFirewallOptionsResponse(RootModel[None]):
    """Model for set_options. Set Firewall options. response."""
    root: None = Field(...)

class GetClusterFirewallRefsResponseItem(ProxmoxBaseModel):
    """Model for refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    comment: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None)
    ref: StrictStr | None = Field(None)
    scope: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class GetClusterFirewallRefsResponse(RootModel[list[GetClusterFirewallRefsResponseItem]]):
    """List of items. refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    root: list[GetClusterFirewallRefsResponseItem] = Field(...)

class GetClusterFirewallRulesResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetClusterFirewallRulesResponse(RootModel[list[GetClusterFirewallRulesResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetClusterFirewallRulesResponseItem] = Field(...)

class PostClusterFirewallRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostClusterFirewallRulesResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteClusterFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterFirewallRulesPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetClusterFirewallRulesPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutClusterFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutClusterFirewallRulesPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class GetClusterHaResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index. response."""
    id: StrictStr | None = Field(None)

class GetClusterHaResponse(RootModel[list[GetClusterHaResponseItem]]):
    """List of items. index. Directory index. response."""
    root: list[GetClusterHaResponseItem] = Field(...)

class GetClusterHaGroupsResponseItem(ProxmoxBaseModel):
    """Model for index. Get HA groups. (deprecated in favor of HA rules) response."""
    group: StrictStr | None = Field(None)

class GetClusterHaGroupsResponse(RootModel[list[GetClusterHaGroupsResponseItem]]):
    """List of items. index. Get HA groups. (deprecated in favor of HA rules) response."""
    root: list[GetClusterHaGroupsResponseItem] = Field(...)

class PostClusterHaGroupsRequest(ProxmoxBaseModel):
    """Model for create. Create a new HA group. (deprecated in favor of HA rules) request."""
    comment: StrictStr | None = Field(None, description='Description.')
    group: StrictStr = Field(..., description='The HA group identifier.')
    nodes: StrictStr = Field(..., description='List of cluster node names with optional priority.')
    nofailback: bool | None = Field(None, description='The CRM tries to run services on the node with the highest priority. If a node with higher priority comes online, the CRM migrates the service to that node. Enabling nofailback prevents that behavior.')
    restricted: bool | None = Field(None, description='Resources bound to restricted groups may only run on nodes defined by the group.')
    type: StrictStr | None = Field(None, description='Group type.')

class PostClusterHaGroupsResponse(RootModel[None]):
    """Model for create. Create a new HA group. (deprecated in favor of HA rules) response."""
    root: None = Field(...)

class DeleteClusterHaGroupsGroupRequest(RootModel[dict[str, object]]):
    """Model for delete. Delete ha group configuration. (deprecated in favor of HA rules) request."""
    root: dict[str, object] = Field(...)

class DeleteClusterHaGroupsGroupResponse(RootModel[None]):
    """Model for delete. Delete ha group configuration. (deprecated in favor of HA rules) response."""
    root: None = Field(...)

class GetClusterHaGroupsGroupResponse(RootModel[dict[str, object]]):
    """Model for read. Read ha group configuration. (deprecated in favor of HA rules) response."""
    root: dict[str, object] = Field(...)

class PutClusterHaGroupsGroupRequest(ProxmoxBaseModel):
    """Model for update. Update ha group configuration. (deprecated in favor of HA rules) request."""
    comment: StrictStr | None = Field(None, description='Description.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nodes: StrictStr | None = Field(None, description='List of cluster node names with optional priority.')
    nofailback: bool | None = Field(None, description='The CRM tries to run services on the node with the highest priority. If a node with higher priority comes online, the CRM migrates the service to that node. Enabling nofailback prevents that behavior.')
    restricted: bool | None = Field(None, description='Resources bound to restricted groups may only run on nodes defined by the group.')

class PutClusterHaGroupsGroupResponse(RootModel[None]):
    """Model for update. Update ha group configuration. (deprecated in favor of HA rules) response."""
    root: None = Field(...)

class GetClusterHaResourcesResponseItem(ProxmoxBaseModel):
    """Model for index. List HA resources. response."""
    sid: StrictStr | None = Field(None)

class GetClusterHaResourcesResponse(RootModel[list[GetClusterHaResourcesResponseItem]]):
    """List of items. index. List HA resources. response."""
    root: list[GetClusterHaResourcesResponseItem] = Field(...)

class PostClusterHaResourcesRequest(ProxmoxBaseModel):
    """Model for create. Create a new HA resource. request."""
    comment: StrictStr | None = Field(None, description='Description.')
    failback: bool | None = Field(None, description='Automatically migrate HA resource to the node with the highest priority according to their node affinity  rules, if a node with a higher priority than the current node comes online.')
    group: StrictStr | None = Field(None, description='The HA group identifier.')
    max_relocate: int | None = Field(None, description='Maximal number of resource relocate tries when a resource fails to start.')
    max_restart: int | None = Field(None, description='Maximal number of tries to restart the resource on a node after its start failed. When reached, the HA manager will try to relocate the resource to an eligible node.')
    sid: StrictStr = Field(..., description='HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).')
    state: StrictStr | None = Field(None, description='Requested resource state.')
    type: StrictStr | None = Field(None, description='Resource type.')

class PostClusterHaResourcesResponse(RootModel[None]):
    """Model for create. Create a new HA resource. response."""
    root: None = Field(...)

class DeleteClusterHaResourcesSidRequest(ProxmoxBaseModel):
    """Model for delete. Delete resource configuration. request."""
    purge: bool | None = Field(None, description='Remove this resource from rules that reference it, deleting the rule if this resource is the only resource in the rule')

class DeleteClusterHaResourcesSidResponse(RootModel[None]):
    """Model for delete. Delete resource configuration. response."""
    root: None = Field(...)

class GetClusterHaResourcesSidResponse(ProxmoxBaseModel):
    """Model for read. Read resource configuration. response."""
    comment: StrictStr | None = Field(None, description='Description.')
    digest: StrictStr = Field(..., description='Can be used to prevent concurrent modifications.')
    failback: bool | None = Field(None, description='The HA resource is automatically migrated to the node with the highest priority according to their node affinity rule, if a node with a higher priority than the current node comes online.')
    group: StrictStr | None = Field(None, description='The HA group identifier.')
    max_relocate: int | None = Field(None, description='Maximal number of service relocate tries when a service fails to start.')
    max_restart: int | None = Field(None, description='Maximal number of tries to restart the service on a node after its start failed.')
    sid: StrictStr = Field(..., description='HA resource ID. This consists of a resource type followed by a resource specific name, separated with colon (example: vm:100 / ct:100). For virtual machines and containers, you can simply use the VM or CT id as a shortcut (example: 100).')
    state: StrictStr | None = Field(None, description='Requested resource state.')
    type: StrictStr = Field(..., description='The type of the resources.')

class PutClusterHaResourcesSidRequest(ProxmoxBaseModel):
    """Model for update. Update resource configuration. request."""
    comment: StrictStr | None = Field(None, description='Description.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    failback: bool | None = Field(None, description='Automatically migrate HA resource to the node with the highest priority according to their node affinity  rules, if a node with a higher priority than the current node comes online.')
    group: StrictStr | None = Field(None, description='The HA group identifier.')
    max_relocate: int | None = Field(None, description='Maximal number of resource relocate tries when a resource fails to start.')
    max_restart: int | None = Field(None, description='Maximal number of tries to restart the resource on a node after its start failed. When reached, the HA manager will try to relocate the resource to an eligible node.')
    state: StrictStr | None = Field(None, description='Requested resource state.')

class PutClusterHaResourcesSidResponse(RootModel[None]):
    """Model for update. Update resource configuration. response."""
    root: None = Field(...)

class PostClusterHaResourcesSidMigrateRequest(ProxmoxBaseModel):
    """Model for migrate. Request resource migration (online) to another node. request."""
    node: StrictStr = Field(..., description='Target node.')

class PostClusterHaResourcesSidMigrateResponse(ProxmoxBaseModel):
    """Model for migrate. Request resource migration (online) to another node. response."""
    blocking_resources: list[dict[str, object]] | None = Field(None, alias="blocking-resources", description='HA resources, which are blocking the given HA resource from being migrated to the requested target node.')
    comigrated_resources: list[object] | None = Field(None, alias="comigrated-resources", description='HA resources, which are migrated to the same requested target node as the given HA resource, because these are in positive affinity with the HA resource.')
    requested_node: StrictStr = Field(..., alias="requested-node", description='Node, which was requested to be migrated to.')
    sid: StrictStr = Field(..., description='HA resource, which is requested to be migrated.')

class PostClusterHaResourcesSidRelocateRequest(ProxmoxBaseModel):
    """Model for relocate. Request resource relocation to another node. This stops the service on the old node, and restarts it on the target node. request."""
    node: StrictStr = Field(..., description='Target node.')

class PostClusterHaResourcesSidRelocateResponse(ProxmoxBaseModel):
    """Model for relocate. Request resource relocation to another node. This stops the service on the old node, and restarts it on the target node. response."""
    blocking_resources: list[dict[str, object]] | None = Field(None, alias="blocking-resources", description='HA resources, which are blocking the given HA resource from being relocated to the requested target node.')
    comigrated_resources: list[StrictStr] | None = Field(None, alias="comigrated-resources", description='HA resources, which are relocated to the same requested target node as the given HA resource, because these are in positive affinity with the HA resource.')
    requested_node: StrictStr = Field(..., alias="requested-node", description='Node, which was requested to be relocated to.')
    sid: StrictStr = Field(..., description='HA resource, which is requested to be relocated.')

class GetClusterHaRulesResponseItem(ProxmoxBaseModel):
    """Model for index. Get HA rules. response."""
    rule: StrictStr | None = Field(None)

class GetClusterHaRulesResponse(RootModel[list[GetClusterHaRulesResponseItem]]):
    """List of items. index. Get HA rules. response."""
    root: list[GetClusterHaRulesResponseItem] = Field(...)

class PostClusterHaRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create HA rule. request."""
    affinity: StrictStr | None = Field(None, description="Describes whether the HA resources are supposed to be kept on the same node ('positive'), or are supposed to be kept on separate nodes ('negative').")
    comment: StrictStr | None = Field(None, description='HA rule description.')
    disable: bool | None = Field(None, description='Whether the HA rule is disabled.')
    nodes: StrictStr | None = Field(None, description='List of cluster node names with optional priority.')
    resources: StrictStr = Field(..., description='List of HA resource IDs. This consists of a list of resource types followed by a resource specific name separated with a colon (example: vm:100,ct:101).')
    rule: StrictStr = Field(..., description='HA rule identifier.')
    strict: bool | None = Field(None, description='Describes whether the node affinity rule is strict or non-strict.')
    type: StrictStr = Field(..., description='HA rule type.')

class PostClusterHaRulesResponse(RootModel[None]):
    """Model for create_rule. Create HA rule. response."""
    root: None = Field(...)

class DeleteClusterHaRulesRuleRequest(RootModel[dict[str, object]]):
    """Model for delete_rule. Delete HA rule. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterHaRulesRuleResponse(RootModel[None]):
    """Model for delete_rule. Delete HA rule. response."""
    root: None = Field(...)

class GetClusterHaRulesRuleResponse(ProxmoxBaseModel):
    """Model for read_rule. Read HA rule. response."""
    rule: StrictStr = Field(..., description='HA rule identifier.')
    type: StrictStr = Field(..., description='HA rule type.')

class PutClusterHaRulesRuleRequest(ProxmoxBaseModel):
    """Model for update_rule. Update HA rule. request."""
    affinity: StrictStr | None = Field(None, description="Describes whether the HA resources are supposed to be kept on the same node ('positive'), or are supposed to be kept on separate nodes ('negative').")
    comment: StrictStr | None = Field(None, description='HA rule description.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Whether the HA rule is disabled.')
    nodes: StrictStr | None = Field(None, description='List of cluster node names with optional priority.')
    resources: StrictStr | None = Field(None, description='List of HA resource IDs. This consists of a list of resource types followed by a resource specific name separated with a colon (example: vm:100,ct:101).')
    strict: bool | None = Field(None, description='Describes whether the node affinity rule is strict or non-strict.')
    type: StrictStr = Field(..., description='HA rule type.')

class PutClusterHaRulesRuleResponse(RootModel[None]):
    """Model for update_rule. Update HA rule. response."""
    root: None = Field(...)

class GetClusterHaStatusResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class PostClusterHaStatusArmHaResponse(RootModel[None]):
    """Model for arm-ha. Request re-arming the HA stack after it was disarmed. response."""
    root: None = Field(...)

class GetClusterHaStatusCurrentResponseItem(ProxmoxBaseModel):
    """Model for status. Get HA manager status. response."""
    armed_state: StrictStr | None = Field(None, alias="armed-state", description="For type 'fencing'. Whether HA is armed, on standby, disarming or disarmed.")
    crm_state: StrictStr | None = Field(None, description="For type 'service'. Service state as seen by the CRM.")
    failback: bool | None = Field(None, description='The HA resource is automatically migrated to the node with the highest priority according to their node affinity rule, if a node with a higher priority than the current node comes online.')
    id: StrictStr | None = Field(None, description='Status entry ID (quorum, master, lrm:<node>, service:<sid>).')
    max_relocate: int | None = Field(None, description="For type 'service'.")
    max_restart: int | None = Field(None, description="For type 'service'.")
    node: StrictStr | None = Field(None, description='Node associated to status entry.')
    quorate: bool | None = Field(None, description="For type 'quorum'. Whether the cluster is quorate or not.")
    request_state: StrictStr | None = Field(None, description="For type 'service'. Requested service state.")
    resource_mode: StrictStr | None = Field(None, description="For type 'fencing'. How resources are handled while disarmed.")
    sid: StrictStr | None = Field(None, description="For type 'service'. Service ID.")
    state: StrictStr | None = Field(None, description="For type 'service'. Verbose service state.")
    status: StrictStr | None = Field(None, description='Status of the entry (value depends on type).')
    timestamp: int | None = Field(None, description="For type 'lrm','master'. Timestamp of the status information.")
    type: object | None = Field(None, description='Type of status entry.')

class GetClusterHaStatusCurrentResponse(RootModel[list[GetClusterHaStatusCurrentResponseItem]]):
    """List of items. status. Get HA manager status. response."""
    root: list[GetClusterHaStatusCurrentResponseItem] = Field(...)

class PostClusterHaStatusDisarmHaRequest(ProxmoxBaseModel):
    """Model for disarm-ha. Request disarming the HA stack, releasing all watchdogs cluster-wide. request."""
    resource_mode: StrictStr = Field(..., alias="resource-mode", description="Controls how HA managed resources are handled while disarmed. The current state of resources is not affected. 'freeze': new commands and state changes are not applied. 'ignore': resources are removed from HA tracking and can be managed as if they were not HA managed.")

class PostClusterHaStatusDisarmHaResponse(RootModel[None]):
    """Model for disarm-ha. Request disarming the HA stack, releasing all watchdogs cluster-wide. response."""
    root: None = Field(...)

class GetClusterHaStatusManagerStatusResponse(RootModel[dict[str, object]]):
    """Model for manager_status. Get full HA manager status, including LRM status. response."""
    root: dict[str, object] = Field(...)

class GetClusterJobsResponseItem(ProxmoxBaseModel):
    """Model for index. Index for jobs related endpoints. response."""
    subdir: StrictStr | None = Field(None, description='API sub-directory endpoint')

class GetClusterJobsResponse(RootModel[list[GetClusterJobsResponseItem]]):
    """List of items. index. Index for jobs related endpoints. response."""
    root: list[GetClusterJobsResponseItem] = Field(..., description='Directory index.')

class GetClusterJobsRealmSyncResponseItem(ProxmoxBaseModel):
    """Model for syncjob_index. List configured realm-sync-jobs. response."""
    comment: StrictStr | None = Field(None, description='A comment for the job.')
    enabled: bool | None = Field(None, description='If the job is enabled or not.')
    id: StrictStr | None = Field(None, description='The ID of the entry.')
    last_run: int | None = Field(None, alias="last-run", description='Last execution time of the job in seconds since the beginning of the UNIX epoch')
    next_run: int | None = Field(None, alias="next-run", description='Next planned execution time of the job in seconds since the beginning of the UNIX epoch.')
    realm: StrictStr | None = Field(None, description='Authentication domain ID')
    remove_vanished: StrictStr | None = Field(None, alias="remove-vanished", description="A semicolon-separated list of things to remove when they or the user vanishes during a sync. The following values are possible: 'entry' removes the user/group when not returned from the sync. 'properties' removes the set properties on existing user/group that do not appear in the source (even custom ones). 'acl' removes acls when the user/group is not returned from the sync. Instead of a list it also can be 'none' (the default).")
    schedule: StrictStr | None = Field(None, description='The configured sync schedule.')
    scope: StrictStr | None = Field(None, description='Select what to sync.')

class GetClusterJobsRealmSyncResponse(RootModel[list[GetClusterJobsRealmSyncResponseItem]]):
    """List of items. syncjob_index. List configured realm-sync-jobs. response."""
    root: list[GetClusterJobsRealmSyncResponseItem] = Field(...)

class DeleteClusterJobsRealmSyncIdRequest(RootModel[dict[str, object]]):
    """Model for delete_job. Delete realm-sync job definition. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterJobsRealmSyncIdResponse(RootModel[None]):
    """Model for delete_job. Delete realm-sync job definition. response."""
    root: None = Field(...)

class GetClusterJobsRealmSyncIdResponse(RootModel[dict[str, object]]):
    """Model for read_job. Read realm-sync job definition. response."""
    root: dict[str, object] = Field(...)

class PostClusterJobsRealmSyncIdRequest(ProxmoxBaseModel):
    """Model for create_job. Create new realm-sync job. request."""
    comment: StrictStr | None = Field(None, description='Description for the Job.')
    enable_new: bool | None = Field(None, alias="enable-new", description='Enable newly synced users immediately.')
    enabled: bool | None = Field(None, description='Determines if the job is enabled.')
    realm: StrictStr | None = Field(None, description='Authentication domain ID')
    remove_vanished: StrictStr | None = Field(None, alias="remove-vanished", description="A semicolon-separated list of things to remove when they or the user vanishes during a sync. The following values are possible: 'entry' removes the user/group when not returned from the sync. 'properties' removes the set properties on existing user/group that do not appear in the source (even custom ones). 'acl' removes acls when the user/group is not returned from the sync. Instead of a list it also can be 'none' (the default).")
    schedule: StrictStr = Field(..., description='Backup schedule. The format is a subset of `systemd` calendar events.')
    scope: StrictStr | None = Field(None, description='Select what to sync.')

class PostClusterJobsRealmSyncIdResponse(RootModel[None]):
    """Model for create_job. Create new realm-sync job. response."""
    root: None = Field(...)

class PutClusterJobsRealmSyncIdRequest(ProxmoxBaseModel):
    """Model for update_job. Update realm-sync job definition. request."""
    comment: StrictStr | None = Field(None, description='Description for the Job.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    enable_new: bool | None = Field(None, alias="enable-new", description='Enable newly synced users immediately.')
    enabled: bool | None = Field(None, description='Determines if the job is enabled.')
    remove_vanished: StrictStr | None = Field(None, alias="remove-vanished", description="A semicolon-separated list of things to remove when they or the user vanishes during a sync. The following values are possible: 'entry' removes the user/group when not returned from the sync. 'properties' removes the set properties on existing user/group that do not appear in the source (even custom ones). 'acl' removes acls when the user/group is not returned from the sync. Instead of a list it also can be 'none' (the default).")
    schedule: StrictStr = Field(..., description='Backup schedule. The format is a subset of `systemd` calendar events.')
    scope: StrictStr | None = Field(None, description='Select what to sync.')

class PutClusterJobsRealmSyncIdResponse(RootModel[None]):
    """Model for update_job. Update realm-sync job definition. response."""
    root: None = Field(...)

class GetClusterJobsScheduleAnalyzeResponseItem(ProxmoxBaseModel):
    """Model for schedule-analyze. Returns a list of future schedule runtimes. response."""
    timestamp: int | None = Field(None, description='UNIX timestamp for the run.')
    utc: StrictStr | None = Field(None, description='UTC timestamp for the run.')

class GetClusterJobsScheduleAnalyzeResponse(RootModel[list[GetClusterJobsScheduleAnalyzeResponseItem]]):
    """List of items. schedule-analyze. Returns a list of future schedule runtimes. response."""
    root: list[GetClusterJobsScheduleAnalyzeResponseItem] = Field(..., description='An array of the next <iterations> events since <starttime>.')

class GetClusterLogResponse(RootModel[list[dict[str, object]]]):
    """Model for log. Read cluster log response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterMappingResponse(RootModel[list[dict[str, object]]]):
    """Model for index. List resource types. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterMappingDirResponseItem(ProxmoxBaseModel):
    """Model for index. List directory mapping response."""
    checks: list[dict[str, object]] | None = Field(None, description="A list of checks, only present if 'check-node' is set.")
    description: StrictStr | None = Field(None, description='A description of the logical mapping.')
    id: StrictStr | None = Field(None, description='The logical ID of the mapping.')
    map: list[StrictStr] | None = Field(None, description='The entries of the mapping.')

class GetClusterMappingDirResponse(RootModel[list[GetClusterMappingDirResponseItem]]):
    """List of items. index. List directory mapping response."""
    root: list[GetClusterMappingDirResponseItem] = Field(...)

class PostClusterMappingDirRequest(ProxmoxBaseModel):
    """Model for create. Create a new directory mapping. request."""
    description: StrictStr | None = Field(None, description='Description of the directory mapping')
    id: StrictStr = Field(..., description='The ID of the directory mapping')
    map: list[StrictStr] = Field(..., description='A list of maps for the cluster nodes.')

class PostClusterMappingDirResponse(RootModel[None]):
    """Model for create. Create a new directory mapping. response."""
    root: None = Field(...)

class DeleteClusterMappingDirIdRequest(RootModel[dict[str, object]]):
    """Model for delete. Remove directory mapping. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterMappingDirIdResponse(RootModel[None]):
    """Model for delete. Remove directory mapping. response."""
    root: None = Field(...)

class GetClusterMappingDirIdResponse(RootModel[dict[str, object]]):
    """Model for get. Get directory mapping. response."""
    root: dict[str, object] = Field(...)

class PutClusterMappingDirIdRequest(ProxmoxBaseModel):
    """Model for update. Update a directory mapping. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description='Description of the directory mapping')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    map: list[StrictStr] | None = Field(None, description='A list of maps for the cluster nodes.')

class PutClusterMappingDirIdResponse(RootModel[None]):
    """Model for update. Update a directory mapping. response."""
    root: None = Field(...)

class GetClusterMappingPciResponseItem(ProxmoxBaseModel):
    """Model for index. List PCI Hardware Mapping response."""
    checks: list[dict[str, object]] | None = Field(None, description="A list of checks, only present if 'check_node' is set.")
    description: StrictStr | None = Field(None, description='A description of the logical mapping.')
    id: StrictStr | None = Field(None, description='The logical ID of the mapping.')
    map: list[StrictStr] | None = Field(None, description='The entries of the mapping.')

class GetClusterMappingPciResponse(RootModel[list[GetClusterMappingPciResponseItem]]):
    """List of items. index. List PCI Hardware Mapping response."""
    root: list[GetClusterMappingPciResponseItem] = Field(...)

class PostClusterMappingPciRequest(ProxmoxBaseModel):
    """Model for create. Create a new hardware mapping. request."""
    description: StrictStr | None = Field(None, description='Description of the logical PCI device.')
    id: StrictStr = Field(..., description='The ID of the logical PCI mapping.')
    live_migration_capable: bool | None = Field(None, alias="live-migration-capable", description='Marks the device(s) as being able to be live-migrated (Experimental). This needs hardware and driver support to work.')
    map: list[StrictStr] = Field(..., description='A list of maps for the cluster nodes.')
    mdev: bool | None = Field(None, description='Marks the device(s) as being capable of providing mediated devices.')

class PostClusterMappingPciResponse(RootModel[None]):
    """Model for create. Create a new hardware mapping. response."""
    root: None = Field(...)

class DeleteClusterMappingPciIdRequest(RootModel[dict[str, object]]):
    """Model for delete. Remove Hardware Mapping. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterMappingPciIdResponse(RootModel[None]):
    """Model for delete. Remove Hardware Mapping. response."""
    root: None = Field(...)

class GetClusterMappingPciIdResponse(RootModel[dict[str, object]]):
    """Model for get. Get PCI Mapping. response."""
    root: dict[str, object] = Field(...)

class PutClusterMappingPciIdRequest(ProxmoxBaseModel):
    """Model for update. Update a hardware mapping. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description='Description of the logical PCI device.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    live_migration_capable: bool | None = Field(None, alias="live-migration-capable", description='Marks the device(s) as being able to be live-migrated (Experimental). This needs hardware and driver support to work.')
    map: list[StrictStr] | None = Field(None, description='A list of maps for the cluster nodes.')
    mdev: bool | None = Field(None, description='Marks the device(s) as being capable of providing mediated devices.')

class PutClusterMappingPciIdResponse(RootModel[None]):
    """Model for update. Update a hardware mapping. response."""
    root: None = Field(...)

class GetClusterMappingUsbResponseItem(ProxmoxBaseModel):
    """Model for index. List USB Hardware Mappings response."""
    description: StrictStr | None = Field(None, description='A description of the logical mapping.')
    error: object | None = Field(None, description="A list of errors when 'check_node' is given.")
    id: StrictStr | None = Field(None, description='The logical ID of the mapping.')
    map: list[StrictStr] | None = Field(None, description='The entries of the mapping.')

class GetClusterMappingUsbResponse(RootModel[list[GetClusterMappingUsbResponseItem]]):
    """List of items. index. List USB Hardware Mappings response."""
    root: list[GetClusterMappingUsbResponseItem] = Field(...)

class PostClusterMappingUsbRequest(ProxmoxBaseModel):
    """Model for create. Create a new hardware mapping. request."""
    description: StrictStr | None = Field(None, description='Description of the logical USB device.')
    id: StrictStr = Field(..., description='The ID of the logical USB mapping.')
    map: list[StrictStr] = Field(..., description='A list of maps for the cluster nodes.')

class PostClusterMappingUsbResponse(RootModel[None]):
    """Model for create. Create a new hardware mapping. response."""
    root: None = Field(...)

class DeleteClusterMappingUsbIdRequest(RootModel[dict[str, object]]):
    """Model for delete. Remove Hardware Mapping. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterMappingUsbIdResponse(RootModel[None]):
    """Model for delete. Remove Hardware Mapping. response."""
    root: None = Field(...)

class GetClusterMappingUsbIdResponse(RootModel[dict[str, object]]):
    """Model for get. Get USB Mapping. response."""
    root: dict[str, object] = Field(...)

class PutClusterMappingUsbIdRequest(ProxmoxBaseModel):
    """Model for update. Update a hardware mapping. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description='Description of the logical USB device.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    map: list[StrictStr] = Field(..., description='A list of maps for the cluster nodes.')

class PutClusterMappingUsbIdResponse(RootModel[None]):
    """Model for update. Update a hardware mapping. response."""
    root: None = Field(...)

class GetClusterMetricsResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Metrics index. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterMetricsExportResponse(ProxmoxBaseModel):
    """Model for export. Retrieve metrics of the cluster. response."""
    data: list[dict[str, object]] = Field(..., description='Array of system metrics. Metrics are sorted by their timestamp.')

class GetClusterMetricsServerResponseItem(ProxmoxBaseModel):
    """Model for server_index. List configured metric servers. response."""
    disable: bool | None = Field(None, description='Flag to disable the plugin.')
    id: StrictStr | None = Field(None, description='The ID of the entry.')
    port: int | None = Field(None, description='Server network port')
    server: StrictStr | None = Field(None, description='Server dns name or IP address')
    type: StrictStr | None = Field(None, description='Plugin type.')

class GetClusterMetricsServerResponse(RootModel[list[GetClusterMetricsServerResponseItem]]):
    """List of items. server_index. List configured metric servers. response."""
    root: list[GetClusterMetricsServerResponseItem] = Field(...)

class DeleteClusterMetricsServerIdRequest(RootModel[dict[str, object]]):
    """Model for delete. Remove Metric server. request."""
    root: dict[str, object] = Field(...)

class DeleteClusterMetricsServerIdResponse(RootModel[None]):
    """Model for delete. Remove Metric server. response."""
    root: None = Field(...)

class GetClusterMetricsServerIdResponse(RootModel[dict[str, object]]):
    """Model for read. Read metric server configuration. response."""
    root: dict[str, object] = Field(...)

class PostClusterMetricsServerIdRequest(ProxmoxBaseModel):
    """Model for create. Create a new external metric server config request."""
    api_path_prefix: StrictStr | None = Field(None, alias="api-path-prefix", description="An API path prefix inserted between '<host>:<port>/' and '/api2/'. Can be useful if the InfluxDB service runs behind a reverse proxy.")
    bucket: StrictStr | None = Field(None, description='The InfluxDB bucket/db. Only necessary when using the http v2 api.')
    disable: bool | None = Field(None, description='Flag to disable the plugin.')
    influxdbproto: StrictStr | None = Field(None)
    max_body_size: int | None = Field(None, alias="max-body-size", description='InfluxDB max-body-size in bytes. Requests are batched up to this size.')
    mtu: int | None = Field(None, description='MTU for metrics transmission over UDP')
    organization: StrictStr | None = Field(None, description='The InfluxDB organization. Only necessary when using the http v2 api. Has no meaning when using v2 compatibility api.')
    otel_compression: StrictStr | None = Field(None, alias="otel-compression", description='Compression algorithm for requests')
    otel_headers: StrictStr | None = Field(None, alias="otel-headers", description='Custom HTTP headers (JSON format, base64 encoded)')
    otel_max_body_size: int | None = Field(None, alias="otel-max-body-size", description='Maximum request body size in bytes')
    otel_path: StrictStr | None = Field(None, alias="otel-path", description='OTLP endpoint path')
    otel_protocol: StrictStr | None = Field(None, alias="otel-protocol", description='HTTP protocol')
    otel_resource_attributes: StrictStr | None = Field(None, alias="otel-resource-attributes", description='Additional resource attributes as JSON, base64 encoded')
    otel_timeout: int | None = Field(None, alias="otel-timeout", description='HTTP request timeout in seconds')
    otel_verify_ssl: bool | None = Field(None, alias="otel-verify-ssl", description='Verify SSL certificates')
    path: StrictStr | None = Field(None, description='root graphite path (ex: proxmox.mycluster.mykey)')
    port: int = Field(..., description='server network port')
    proto: StrictStr | None = Field(None, description='Protocol to send graphite data. TCP or UDP (default)')
    server: StrictStr = Field(..., description='server dns name or IP address')
    timeout: int | None = Field(None, description='graphite TCP socket timeout (default=1)')
    token: StrictStr | None = Field(None, description="The InfluxDB access token. Only necessary when using the http v2 api. If the v2 compatibility api is used, use 'user:password' instead.")
    type: StrictStr = Field(..., description='Plugin type.')
    verify_certificate: bool | None = Field(None, alias="verify-certificate", description='Set to 0 to disable certificate verification for https endpoints.')

class PostClusterMetricsServerIdResponse(RootModel[None]):
    """Model for create. Create a new external metric server config response."""
    root: None = Field(...)

class PutClusterMetricsServerIdRequest(ProxmoxBaseModel):
    """Model for update. Update metric server configuration. request."""
    api_path_prefix: StrictStr | None = Field(None, alias="api-path-prefix", description="An API path prefix inserted between '<host>:<port>/' and '/api2/'. Can be useful if the InfluxDB service runs behind a reverse proxy.")
    bucket: StrictStr | None = Field(None, description='The InfluxDB bucket/db. Only necessary when using the http v2 api.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the plugin.')
    influxdbproto: StrictStr | None = Field(None)
    max_body_size: int | None = Field(None, alias="max-body-size", description='InfluxDB max-body-size in bytes. Requests are batched up to this size.')
    mtu: int | None = Field(None, description='MTU for metrics transmission over UDP')
    organization: StrictStr | None = Field(None, description='The InfluxDB organization. Only necessary when using the http v2 api. Has no meaning when using v2 compatibility api.')
    otel_compression: StrictStr | None = Field(None, alias="otel-compression", description='Compression algorithm for requests')
    otel_headers: StrictStr | None = Field(None, alias="otel-headers", description='Custom HTTP headers (JSON format, base64 encoded)')
    otel_max_body_size: int | None = Field(None, alias="otel-max-body-size", description='Maximum request body size in bytes')
    otel_path: StrictStr | None = Field(None, alias="otel-path", description='OTLP endpoint path')
    otel_protocol: StrictStr | None = Field(None, alias="otel-protocol", description='HTTP protocol')
    otel_resource_attributes: StrictStr | None = Field(None, alias="otel-resource-attributes", description='Additional resource attributes as JSON, base64 encoded')
    otel_timeout: int | None = Field(None, alias="otel-timeout", description='HTTP request timeout in seconds')
    otel_verify_ssl: bool | None = Field(None, alias="otel-verify-ssl", description='Verify SSL certificates')
    path: StrictStr | None = Field(None, description='root graphite path (ex: proxmox.mycluster.mykey)')
    port: int = Field(..., description='server network port')
    proto: StrictStr | None = Field(None, description='Protocol to send graphite data. TCP or UDP (default)')
    server: StrictStr = Field(..., description='server dns name or IP address')
    timeout: int | None = Field(None, description='graphite TCP socket timeout (default=1)')
    token: StrictStr | None = Field(None, description="The InfluxDB access token. Only necessary when using the http v2 api. If the v2 compatibility api is used, use 'user:password' instead.")
    verify_certificate: bool | None = Field(None, alias="verify-certificate", description='Set to 0 to disable certificate verification for https endpoints.')

class PutClusterMetricsServerIdResponse(RootModel[None]):
    """Model for update. Update metric server configuration. response."""
    root: None = Field(...)

class GetClusterNextidResponse(RootModel[int]):
    """Model for nextid. Get next free VMID. Pass a VMID to assert that its free (at time of check). response."""
    root: int = Field(..., description='The next free VMID.')

class GetClusterNotificationsResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Index for notification-related API endpoints. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterNotificationsEndpointsResponse(RootModel[list[dict[str, object]]]):
    """Model for endpoints_index. Index for all available endpoint types. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterNotificationsEndpointsGotifyResponseItem(ProxmoxBaseModel):
    """Model for get_gotify_endpoints. Returns a list of all gotify endpoints response."""
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    name: StrictStr | None = Field(None, description='The name of the endpoint.')
    origin: StrictStr | None = Field(None, description='Show if this entry was created by a user or was built-in')
    server: StrictStr | None = Field(None, description='Server URL')

class GetClusterNotificationsEndpointsGotifyResponse(RootModel[list[GetClusterNotificationsEndpointsGotifyResponseItem]]):
    """List of items. get_gotify_endpoints. Returns a list of all gotify endpoints response."""
    root: list[GetClusterNotificationsEndpointsGotifyResponseItem] = Field(...)

class PostClusterNotificationsEndpointsGotifyRequest(ProxmoxBaseModel):
    """Model for create_gotify_endpoint. Create a new gotify endpoint request."""
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    name: StrictStr = Field(..., description='The name of the endpoint.')
    server: StrictStr = Field(..., description='Server URL')
    token: StrictStr = Field(..., description='Secret token')

class PostClusterNotificationsEndpointsGotifyResponse(RootModel[None]):
    """Model for create_gotify_endpoint. Create a new gotify endpoint response."""
    root: None = Field(...)

class DeleteClusterNotificationsEndpointsGotifyNameRequest(RootModel[dict[str, object]]):
    """Model for delete_gotify_endpoint. Remove gotify endpoint request."""
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsEndpointsGotifyNameResponse(RootModel[None]):
    """Model for delete_gotify_endpoint. Remove gotify endpoint response."""
    root: None = Field(...)

class GetClusterNotificationsEndpointsGotifyNameResponse(ProxmoxBaseModel):
    """Model for get_gotify_endpoint. Return a specific gotify endpoint response."""
    comment: StrictStr | None = Field(None, description='Comment')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    name: StrictStr = Field(..., description='The name of the endpoint.')
    server: StrictStr = Field(..., description='Server URL')

class PutClusterNotificationsEndpointsGotifyNameRequest(ProxmoxBaseModel):
    """Model for update_gotify_endpoint. Update existing gotify endpoint request."""
    comment: StrictStr | None = Field(None, description='Comment')
    delete: list[StrictStr] | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    server: StrictStr | None = Field(None, description='Server URL')
    token: StrictStr | None = Field(None, description='Secret token')

class PutClusterNotificationsEndpointsGotifyNameResponse(RootModel[None]):
    """Model for update_gotify_endpoint. Update existing gotify endpoint response."""
    root: None = Field(...)

class GetClusterNotificationsEndpointsSendmailResponseItem(ProxmoxBaseModel):
    """Model for get_sendmail_endpoints. Returns a list of all sendmail endpoints response."""
    author: StrictStr | None = Field(None, description='Author of the mail')
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: StrictStr | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[StrictStr] | None = Field(None, description='List of email recipients')
    mailto_user: list[StrictStr] | None = Field(None, alias="mailto-user", description='List of users')
    name: StrictStr | None = Field(None, description='The name of the endpoint.')
    origin: StrictStr | None = Field(None, description='Show if this entry was created by a user or was built-in')

class GetClusterNotificationsEndpointsSendmailResponse(RootModel[list[GetClusterNotificationsEndpointsSendmailResponseItem]]):
    """List of items. get_sendmail_endpoints. Returns a list of all sendmail endpoints response."""
    root: list[GetClusterNotificationsEndpointsSendmailResponseItem] = Field(...)

class PostClusterNotificationsEndpointsSendmailRequest(ProxmoxBaseModel):
    """Model for create_sendmail_endpoint. Create a new sendmail endpoint request."""
    author: StrictStr | None = Field(None, description='Author of the mail')
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: StrictStr | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[StrictStr] | None = Field(None, description='List of email recipients')
    mailto_user: list[StrictStr] | None = Field(None, alias="mailto-user", description='List of users')
    name: StrictStr = Field(..., description='The name of the endpoint.')

class PostClusterNotificationsEndpointsSendmailResponse(RootModel[None]):
    """Model for create_sendmail_endpoint. Create a new sendmail endpoint response."""
    root: None = Field(...)

class DeleteClusterNotificationsEndpointsSendmailNameRequest(RootModel[dict[str, object]]):
    """Model for delete_sendmail_endpoint. Remove sendmail endpoint request."""
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsEndpointsSendmailNameResponse(RootModel[None]):
    """Model for delete_sendmail_endpoint. Remove sendmail endpoint response."""
    root: None = Field(...)

class GetClusterNotificationsEndpointsSendmailNameResponse(ProxmoxBaseModel):
    """Model for get_sendmail_endpoint. Return a specific sendmail endpoint response."""
    author: StrictStr | None = Field(None, description='Author of the mail')
    comment: StrictStr | None = Field(None, description='Comment')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: StrictStr | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[StrictStr] | None = Field(None, description='List of email recipients')
    mailto_user: list[StrictStr] | None = Field(None, alias="mailto-user", description='List of users')
    name: StrictStr = Field(..., description='The name of the endpoint.')

class PutClusterNotificationsEndpointsSendmailNameRequest(ProxmoxBaseModel):
    """Model for update_sendmail_endpoint. Update existing sendmail endpoint request."""
    author: StrictStr | None = Field(None, description='Author of the mail')
    comment: StrictStr | None = Field(None, description='Comment')
    delete: list[StrictStr] | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: StrictStr | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[StrictStr] | None = Field(None, description='List of email recipients')
    mailto_user: list[StrictStr] | None = Field(None, alias="mailto-user", description='List of users')

class PutClusterNotificationsEndpointsSendmailNameResponse(RootModel[None]):
    """Model for update_sendmail_endpoint. Update existing sendmail endpoint response."""
    root: None = Field(...)

class GetClusterNotificationsEndpointsSmtpResponseItem(ProxmoxBaseModel):
    """Model for get_smtp_endpoints. Returns a list of all smtp endpoints response."""
    author: StrictStr | None = Field(None, description="Author of the mail. Defaults to 'Proxmox VE'.")
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: StrictStr | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[StrictStr] | None = Field(None, description='List of email recipients')
    mailto_user: list[StrictStr] | None = Field(None, alias="mailto-user", description='List of users')
    mode: StrictStr | None = Field(None, description='Determine which encryption method shall be used for the connection.')
    name: StrictStr | None = Field(None, description='The name of the endpoint.')
    origin: StrictStr | None = Field(None, description='Show if this entry was created by a user or was built-in')
    port: int | None = Field(None, description='The port to be used. Defaults to 465 for TLS based connections, 587 for STARTTLS based connections and port 25 for insecure plain-text connections.')
    server: StrictStr | None = Field(None, description='The address of the SMTP server.')
    username: StrictStr | None = Field(None, description='Username for SMTP authentication')

class GetClusterNotificationsEndpointsSmtpResponse(RootModel[list[GetClusterNotificationsEndpointsSmtpResponseItem]]):
    """List of items. get_smtp_endpoints. Returns a list of all smtp endpoints response."""
    root: list[GetClusterNotificationsEndpointsSmtpResponseItem] = Field(...)

class PostClusterNotificationsEndpointsSmtpRequest(ProxmoxBaseModel):
    """Model for create_smtp_endpoint. Create a new smtp endpoint request."""
    author: StrictStr | None = Field(None, description="Author of the mail. Defaults to 'Proxmox VE'.")
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: StrictStr = Field(..., alias="from-address", description='`From` address for the mail')
    mailto: list[StrictStr] | None = Field(None, description='List of email recipients')
    mailto_user: list[StrictStr] | None = Field(None, alias="mailto-user", description='List of users')
    mode: StrictStr | None = Field(None, description='Determine which encryption method shall be used for the connection.')
    name: StrictStr = Field(..., description='The name of the endpoint.')
    password: StrictStr | None = Field(None, description='Password for SMTP authentication')
    port: int | None = Field(None, description='The port to be used. Defaults to 465 for TLS based connections, 587 for STARTTLS based connections and port 25 for insecure plain-text connections.')
    server: StrictStr = Field(..., description='The address of the SMTP server.')
    username: StrictStr | None = Field(None, description='Username for SMTP authentication')

class PostClusterNotificationsEndpointsSmtpResponse(RootModel[None]):
    """Model for create_smtp_endpoint. Create a new smtp endpoint response."""
    root: None = Field(...)

class DeleteClusterNotificationsEndpointsSmtpNameRequest(RootModel[dict[str, object]]):
    """Model for delete_smtp_endpoint. Remove smtp endpoint request."""
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsEndpointsSmtpNameResponse(RootModel[None]):
    """Model for delete_smtp_endpoint. Remove smtp endpoint response."""
    root: None = Field(...)

class GetClusterNotificationsEndpointsSmtpNameResponse(ProxmoxBaseModel):
    """Model for get_smtp_endpoint. Return a specific smtp endpoint response."""
    author: StrictStr | None = Field(None, description="Author of the mail. Defaults to 'Proxmox VE'.")
    comment: StrictStr | None = Field(None, description='Comment')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: StrictStr = Field(..., alias="from-address", description='`From` address for the mail')
    mailto: list[StrictStr] | None = Field(None, description='List of email recipients')
    mailto_user: list[StrictStr] | None = Field(None, alias="mailto-user", description='List of users')
    mode: StrictStr | None = Field(None, description='Determine which encryption method shall be used for the connection.')
    name: StrictStr = Field(..., description='The name of the endpoint.')
    port: int | None = Field(None, description='The port to be used. Defaults to 465 for TLS based connections, 587 for STARTTLS based connections and port 25 for insecure plain-text connections.')
    server: StrictStr = Field(..., description='The address of the SMTP server.')
    username: StrictStr | None = Field(None, description='Username for SMTP authentication')

class PutClusterNotificationsEndpointsSmtpNameRequest(ProxmoxBaseModel):
    """Model for update_smtp_endpoint. Update existing smtp endpoint request."""
    author: StrictStr | None = Field(None, description="Author of the mail. Defaults to 'Proxmox VE'.")
    comment: StrictStr | None = Field(None, description='Comment')
    delete: list[StrictStr] | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    from_address: StrictStr | None = Field(None, alias="from-address", description='`From` address for the mail')
    mailto: list[StrictStr] | None = Field(None, description='List of email recipients')
    mailto_user: list[StrictStr] | None = Field(None, alias="mailto-user", description='List of users')
    mode: StrictStr | None = Field(None, description='Determine which encryption method shall be used for the connection.')
    password: StrictStr | None = Field(None, description='Password for SMTP authentication')
    port: int | None = Field(None, description='The port to be used. Defaults to 465 for TLS based connections, 587 for STARTTLS based connections and port 25 for insecure plain-text connections.')
    server: StrictStr | None = Field(None, description='The address of the SMTP server.')
    username: StrictStr | None = Field(None, description='Username for SMTP authentication')

class PutClusterNotificationsEndpointsSmtpNameResponse(RootModel[None]):
    """Model for update_smtp_endpoint. Update existing smtp endpoint response."""
    root: None = Field(...)

class GetClusterNotificationsEndpointsWebhookResponseItem(ProxmoxBaseModel):
    """Model for get_webhook_endpoints. Returns a list of all webhook endpoints response."""
    body: StrictStr | None = Field(None, description='HTTP body, base64 encoded')
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    header: list[StrictStr] | None = Field(None, description='HTTP headers to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    method: StrictStr | None = Field(None, description='HTTP method')
    name: StrictStr | None = Field(None, description='The name of the endpoint.')
    origin: StrictStr | None = Field(None, description='Show if this entry was created by a user or was built-in')
    secret: list[StrictStr] | None = Field(None, description='Secrets to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    url: StrictStr | None = Field(None, description='Server URL')

class GetClusterNotificationsEndpointsWebhookResponse(RootModel[list[GetClusterNotificationsEndpointsWebhookResponseItem]]):
    """List of items. get_webhook_endpoints. Returns a list of all webhook endpoints response."""
    root: list[GetClusterNotificationsEndpointsWebhookResponseItem] = Field(...)

class PostClusterNotificationsEndpointsWebhookRequest(ProxmoxBaseModel):
    """Model for create_webhook_endpoint. Create a new webhook endpoint request."""
    body: StrictStr | None = Field(None, description='HTTP body, base64 encoded')
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this target')
    header: list[StrictStr] | None = Field(None, description='HTTP headers to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    method: StrictStr = Field(..., description='HTTP method')
    name: StrictStr = Field(..., description='The name of the endpoint.')
    secret: list[StrictStr] | None = Field(None, description='Secrets to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    url: StrictStr = Field(..., description='Server URL')

class PostClusterNotificationsEndpointsWebhookResponse(RootModel[None]):
    """Model for create_webhook_endpoint. Create a new webhook endpoint response."""
    root: None = Field(...)

class DeleteClusterNotificationsEndpointsWebhookNameRequest(RootModel[dict[str, object]]):
    """Model for delete_webhook_endpoint. Remove webhook endpoint request."""
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsEndpointsWebhookNameResponse(RootModel[None]):
    """Model for delete_webhook_endpoint. Remove webhook endpoint response."""
    root: None = Field(...)

class GetClusterNotificationsEndpointsWebhookNameResponse(ProxmoxBaseModel):
    """Model for get_webhook_endpoint. Return a specific webhook endpoint response."""
    body: StrictStr | None = Field(None, description='HTTP body, base64 encoded')
    comment: StrictStr | None = Field(None, description='Comment')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    header: list[StrictStr] | None = Field(None, description='HTTP headers to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    method: StrictStr = Field(..., description='HTTP method')
    name: StrictStr = Field(..., description='The name of the endpoint.')
    secret: list[StrictStr] | None = Field(None, description='Secrets to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    url: StrictStr = Field(..., description='Server URL')

class PutClusterNotificationsEndpointsWebhookNameRequest(ProxmoxBaseModel):
    """Model for update_webhook_endpoint. Update existing webhook endpoint request."""
    body: StrictStr | None = Field(None, description='HTTP body, base64 encoded')
    comment: StrictStr | None = Field(None, description='Comment')
    delete: list[StrictStr] | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target')
    header: list[StrictStr] | None = Field(None, description='HTTP headers to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    method: StrictStr | None = Field(None, description='HTTP method')
    secret: list[StrictStr] | None = Field(None, description='Secrets to set. These have to be formatted as a property string in the format name=<name>,value=<base64 of value>')
    url: StrictStr | None = Field(None, description='Server URL')

class PutClusterNotificationsEndpointsWebhookNameResponse(RootModel[None]):
    """Model for update_webhook_endpoint. Update existing webhook endpoint response."""
    root: None = Field(...)

class GetClusterNotificationsMatcherFieldValuesResponseItem(ProxmoxBaseModel):
    """Model for get_matcher_field_values. Returns known notification metadata fields and their known values response."""
    comment: StrictStr | None = Field(None, description='Additional comment for this value.')
    field: StrictStr | None = Field(None, description='Field this value belongs to.')
    value: StrictStr | None = Field(None, description='Notification metadata value known by the system.')

class GetClusterNotificationsMatcherFieldValuesResponse(RootModel[list[GetClusterNotificationsMatcherFieldValuesResponseItem]]):
    """List of items. get_matcher_field_values. Returns known notification metadata fields and their known values response."""
    root: list[GetClusterNotificationsMatcherFieldValuesResponseItem] = Field(...)

class GetClusterNotificationsMatcherFieldsResponseItem(ProxmoxBaseModel):
    """Model for get_matcher_fields. Returns known notification metadata fields response."""
    name: StrictStr | None = Field(None, description='Name of the field.')

class GetClusterNotificationsMatcherFieldsResponse(RootModel[list[GetClusterNotificationsMatcherFieldsResponseItem]]):
    """List of items. get_matcher_fields. Returns known notification metadata fields response."""
    root: list[GetClusterNotificationsMatcherFieldsResponseItem] = Field(...)

class GetClusterNotificationsMatchersResponseItem(ProxmoxBaseModel):
    """Model for get_matchers. Returns a list of all matchers response."""
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this matcher')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole matcher')
    match_calendar: list[StrictStr] | None = Field(None, alias="match-calendar", description='Match notification timestamp')
    match_field: list[StrictStr] | None = Field(None, alias="match-field", description='Metadata fields to match (regex or exact match). Must be in the form (regex|exact):<field>=<value>')
    match_severity: list[StrictStr] | None = Field(None, alias="match-severity", description='Notification severities to match')
    mode: StrictStr | None = Field(None, description="Choose between 'all' and 'any' for when multiple properties are specified")
    name: StrictStr | None = Field(None, description='Name of the matcher.')
    origin: StrictStr | None = Field(None, description='Show if this entry was created by a user or was built-in')
    target: list[StrictStr] | None = Field(None, description='Targets to notify on match')

class GetClusterNotificationsMatchersResponse(RootModel[list[GetClusterNotificationsMatchersResponseItem]]):
    """List of items. get_matchers. Returns a list of all matchers response."""
    root: list[GetClusterNotificationsMatchersResponseItem] = Field(...)

class PostClusterNotificationsMatchersRequest(ProxmoxBaseModel):
    """Model for create_matcher. Create a new matcher request."""
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Disable this matcher')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole matcher')
    match_calendar: list[StrictStr] | None = Field(None, alias="match-calendar", description='Match notification timestamp')
    match_field: list[StrictStr] | None = Field(None, alias="match-field", description='Metadata fields to match (regex or exact match). Must be in the form (regex|exact):<field>=<value>')
    match_severity: list[StrictStr] | None = Field(None, alias="match-severity", description='Notification severities to match')
    mode: StrictStr | None = Field(None, description="Choose between 'all' and 'any' for when multiple properties are specified")
    name: StrictStr = Field(..., description='Name of the matcher.')
    target: list[StrictStr] | None = Field(None, description='Targets to notify on match')

class PostClusterNotificationsMatchersResponse(RootModel[None]):
    """Model for create_matcher. Create a new matcher response."""
    root: None = Field(...)

class DeleteClusterNotificationsMatchersNameRequest(RootModel[dict[str, object]]):
    """Model for delete_matcher. Remove matcher request."""
    root: dict[str, object] = Field(...)

class DeleteClusterNotificationsMatchersNameResponse(RootModel[None]):
    """Model for delete_matcher. Remove matcher response."""
    root: None = Field(...)

class GetClusterNotificationsMatchersNameResponse(ProxmoxBaseModel):
    """Model for get_matcher. Return a specific matcher response."""
    comment: StrictStr | None = Field(None, description='Comment')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this matcher')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole matcher')
    match_calendar: list[StrictStr] | None = Field(None, alias="match-calendar", description='Match notification timestamp')
    match_field: list[StrictStr] | None = Field(None, alias="match-field", description='Metadata fields to match (regex or exact match). Must be in the form (regex|exact):<field>=<value>')
    match_severity: list[StrictStr] | None = Field(None, alias="match-severity", description='Notification severities to match')
    mode: StrictStr | None = Field(None, description="Choose between 'all' and 'any' for when multiple properties are specified")
    name: StrictStr = Field(..., description='Name of the matcher.')
    target: list[StrictStr] | None = Field(None, description='Targets to notify on match')

class PutClusterNotificationsMatchersNameRequest(ProxmoxBaseModel):
    """Model for update_matcher. Update existing matcher request."""
    comment: StrictStr | None = Field(None, description='Comment')
    delete: list[StrictStr] | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this matcher')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole matcher')
    match_calendar: list[StrictStr] | None = Field(None, alias="match-calendar", description='Match notification timestamp')
    match_field: list[StrictStr] | None = Field(None, alias="match-field", description='Metadata fields to match (regex or exact match). Must be in the form (regex|exact):<field>=<value>')
    match_severity: list[StrictStr] | None = Field(None, alias="match-severity", description='Notification severities to match')
    mode: StrictStr | None = Field(None, description="Choose between 'all' and 'any' for when multiple properties are specified")
    target: list[StrictStr] | None = Field(None, description='Targets to notify on match')

class PutClusterNotificationsMatchersNameResponse(RootModel[None]):
    """Model for update_matcher. Update existing matcher response."""
    root: None = Field(...)

class GetClusterNotificationsTargetsResponseItem(ProxmoxBaseModel):
    """Model for get_all_targets. Returns a list of all entities that can be used as notification targets. response."""
    comment: StrictStr | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Show if this target is disabled')
    name: StrictStr | None = Field(None, description='Name of the target.')
    origin: StrictStr | None = Field(None, description='Show if this entry was created by a user or was built-in')
    type: StrictStr | None = Field(None, description='Type of the target.')

class GetClusterNotificationsTargetsResponse(RootModel[list[GetClusterNotificationsTargetsResponseItem]]):
    """List of items. get_all_targets. Returns a list of all entities that can be used as notification targets. response."""
    root: list[GetClusterNotificationsTargetsResponseItem] = Field(...)

class PostClusterNotificationsTargetsNameTestRequest(RootModel[dict[str, object]]):
    """Model for test_target. Send a test notification to a provided target. request."""
    root: dict[str, object] = Field(...)

class PostClusterNotificationsTargetsNameTestResponse(RootModel[None]):
    """Model for test_target. Send a test notification to a provided target. response."""
    root: None = Field(...)

class GetClusterOptionsResponse(RootModel[dict[str, object]]):
    """Model for get_options. Get datacenter options. Without 'Sys.Audit' on '/' not all options are returned. response."""
    root: dict[str, object] = Field(...)

class PutClusterOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set datacenter options. request."""
    bwlimit: StrictStr | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    consent_text: StrictStr | None = Field(None, alias="consent-text", description='Consent text that is displayed before logging in.')
    console: StrictStr | None = Field(None, description='Select the default Console viewer. You can either use the builtin java applet (VNC; deprecated and maps to html5), an external virt-viewer comtatible application (SPICE), an HTML5 based vnc viewer (noVNC), or an HTML5 based console client (xtermjs). If the selected viewer is not available (e.g. SPICE not activated for the VM), the fallback is noVNC.')
    crs: StrictStr | None = Field(None, description='Cluster resource scheduling settings.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description='Datacenter description. Shown in the web-interface datacenter notes panel. This is saved as comment inside the configuration file.')
    email_from: StrictStr | None = Field(None, description='Specify email address to send notification from (default is root@$hostname)')
    fencing: StrictStr | None = Field(None, description="Set the fencing mode of the HA cluster. Hardware mode needs a valid configuration of fence devices in /etc/pve/ha/fence.cfg. With both all two modes are used.\n\nWARNING: 'hardware' and 'both' are EXPERIMENTAL & WIP")
    ha: StrictStr | None = Field(None, description='Cluster wide HA settings.')
    http_proxy: StrictStr | None = Field(None, description="Specify external http proxy which is used for downloads (example: 'http://username:password@host:port/')")
    keyboard: StrictStr | None = Field(None, description='Default keybord layout for vnc server.')
    language: StrictStr | None = Field(None, description='Default GUI language.')
    mac_prefix: StrictStr | None = Field(None, description="Prefix for the auto-generated MAC addresses of virtual guests. The default 'BC:24:11' is the OUI assigned by the IEEE to Proxmox Server Solutions GmbH for a 24-bit large MAC block. You're allowed to use this in local networks, i.e., those not directly reachable by the public (e.g., in a LAN or behind NAT).")
    max_workers: int | None = Field(None, description="Defines how many workers (per node) are maximal started  on actions like 'stopall VMs' or task from the ha-manager.")
    migration: StrictStr | None = Field(None, description='For cluster wide migration settings.')
    migration_unsecure: bool | None = Field(None, description="Migration is secure using SSH tunnel by default. For secure private networks you can disable it to speed up migration. Deprecated, use the 'migration' property instead!")
    next_id: StrictStr | None = Field(None, alias="next-id", description='Control the range for the free VMID auto-selection pool.')
    notify: StrictStr | None = Field(None, description='Cluster-wide notification settings.')
    registered_tags: StrictStr | None = Field(None, alias="registered-tags", description="A list of tags that require a `Sys.Modify` on '/' to set and delete. Tags set here that are also in 'user-tag-access' also require `Sys.Modify`.")
    replication: StrictStr | None = Field(None, description='For cluster wide replication settings.')
    tag_style: StrictStr | None = Field(None, alias="tag-style", description='Tag style options.')
    u2f: StrictStr | None = Field(None, description='u2f')
    user_tag_access: StrictStr | None = Field(None, alias="user-tag-access", description='Privilege options for user-settable tags')
    webauthn: StrictStr | None = Field(None, description='webauthn configuration')

class PutClusterOptionsResponse(RootModel[None]):
    """Model for set_options. Set datacenter options. response."""
    root: None = Field(...)

class GetClusterReplicationResponseItem(ProxmoxBaseModel):
    """Model for index. List replication jobs. response."""
    comment: StrictStr | None = Field(None, description='Description.')
    disable: bool | None = Field(None, description='Flag to disable/deactivate the entry.')
    guest: int | None = Field(None, description='Guest ID.')
    id: StrictStr | None = Field(None, description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. '<GUEST>-<JOBNUM>'.")
    jobnum: int | None = Field(None, description='Unique, sequential ID assigned to each job.')
    rate: float | None = Field(None, description='Rate limit in mbps (megabytes per second) as floating point number.')
    remove_job: StrictStr | None = Field(None, description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to 'full', it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.")
    schedule: StrictStr | None = Field(None, description='Storage replication schedule. The format is a subset of `systemd` calendar events.')
    source: StrictStr | None = Field(None, description='For internal use, to detect if the guest was stolen.')
    target: StrictStr | None = Field(None, description='Target node.')
    type: StrictStr | None = Field(None, description='Section type.')

class GetClusterReplicationResponse(RootModel[list[GetClusterReplicationResponseItem]]):
    """List of items. index. List replication jobs. response."""
    root: list[GetClusterReplicationResponseItem] = Field(...)

class PostClusterReplicationRequest(ProxmoxBaseModel):
    """Model for create. Create a new replication job request."""
    comment: StrictStr | None = Field(None, description='Description.')
    disable: bool | None = Field(None, description='Flag to disable/deactivate the entry.')
    id: StrictStr = Field(..., description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. '<GUEST>-<JOBNUM>'.")
    rate: float | None = Field(None, description='Rate limit in mbps (megabytes per second) as floating point number.')
    remove_job: StrictStr | None = Field(None, description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to 'full', it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.")
    schedule: StrictStr | None = Field(None, description='Storage replication schedule. The format is a subset of `systemd` calendar events.')
    source: StrictStr | None = Field(None, description='For internal use, to detect if the guest was stolen.')
    target: StrictStr = Field(..., description='Target node.')
    type: StrictStr = Field(..., description='Section type.')

class PostClusterReplicationResponse(RootModel[None]):
    """Model for create. Create a new replication job response."""
    root: None = Field(...)

class DeleteClusterReplicationIdRequest(ProxmoxBaseModel):
    """Model for delete. Mark replication job for removal. request."""
    force: bool | None = Field(None, description='Will remove the jobconfig entry, but will not cleanup.')
    keep: bool | None = Field(None, description='Keep replicated data at target (do not remove).')

class DeleteClusterReplicationIdResponse(RootModel[None]):
    """Model for delete. Mark replication job for removal. response."""
    root: None = Field(...)

class GetClusterReplicationIdResponse(ProxmoxBaseModel):
    """Model for read. Read replication job configuration. response."""
    comment: StrictStr | None = Field(None, description='Description.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable/deactivate the entry.')
    guest: int = Field(..., description='Guest ID.')
    id: StrictStr = Field(..., description="Replication Job ID. The ID is composed of a Guest ID and a job number, separated by a hyphen, i.e. '<GUEST>-<JOBNUM>'.")
    jobnum: int = Field(..., description='Unique, sequential ID assigned to each job.')
    rate: float | None = Field(None, description='Rate limit in mbps (megabytes per second) as floating point number.')
    remove_job: StrictStr | None = Field(None, description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to 'full', it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.")
    schedule: StrictStr | None = Field(None, description='Storage replication schedule. The format is a subset of `systemd` calendar events.')
    source: StrictStr | None = Field(None, description='For internal use, to detect if the guest was stolen.')
    target: StrictStr = Field(..., description='Target node.')
    type: StrictStr = Field(..., description='Section type.')

class PutClusterReplicationIdRequest(ProxmoxBaseModel):
    """Model for update. Update replication job configuration. request."""
    comment: StrictStr | None = Field(None, description='Description.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable/deactivate the entry.')
    rate: float | None = Field(None, description='Rate limit in mbps (megabytes per second) as floating point number.')
    remove_job: StrictStr | None = Field(None, description="Mark the replication job for removal. The job will remove all local replication snapshots. When set to 'full', it also tries to remove replicated volumes on the target. The job then removes itself from the configuration file.")
    schedule: StrictStr | None = Field(None, description='Storage replication schedule. The format is a subset of `systemd` calendar events.')
    source: StrictStr | None = Field(None, description='For internal use, to detect if the guest was stolen.')

class PutClusterReplicationIdResponse(RootModel[None]):
    """Model for update. Update replication job configuration. response."""
    root: None = Field(...)

class GetClusterResourcesResponseItem(ProxmoxBaseModel):
    """Model for resources. Resources index (cluster wide). response."""
    cgroup_mode: int | None = Field(None, alias="cgroup-mode", description="The cgroup mode the node operates under (for type 'node').")
    content: StrictStr | None = Field(None, description="Allowed storage content types (for type 'storage').")
    cpu: float | None = Field(None, description="CPU utilization (for types 'node', 'qemu' and 'lxc').")
    disk: int | None = Field(None, description="Used disk space in bytes (for type 'storage'), used root image space for VMs (for types 'qemu' and 'lxc').")
    diskread: int | None = Field(None, description="The number of bytes the guest read from its block devices since the guest was started. This info is not available for all storage types. (for types 'qemu' and 'lxc')")
    diskwrite: int | None = Field(None, description="The number of bytes the guest wrote to its block devices since the guest was started. This info is not available for all storage types. (for types 'qemu' and 'lxc')")
    hastate: StrictStr | None = Field(None, description='HA service status (for HA managed VMs).')
    id: StrictStr | None = Field(None, description='Resource id.')
    level: StrictStr | None = Field(None, description="Support level (for type 'node').")
    lock: StrictStr | None = Field(None, description="The guest's current config lock (for types 'qemu' and 'lxc')")
    maxcpu: float | None = Field(None, description="Number of available CPUs (for types 'node', 'qemu' and 'lxc').")
    maxdisk: int | None = Field(None, description="Storage size in bytes (for type 'storage'), root image size for VMs (for types 'qemu' and 'lxc').")
    maxmem: int | None = Field(None, description="Number of available memory in bytes (for types 'node', 'qemu' and 'lxc').")
    mem: int | None = Field(None, description="Used memory in bytes (for types 'node', 'qemu' and 'lxc').")
    memhost: int | None = Field(None, description="Used memory in bytes from the point of view of the host (for types 'qemu').")
    name: StrictStr | None = Field(None, description='Name of the resource.')
    netin: int | None = Field(None, description="The amount of traffic in bytes that was sent to the guest over the network since it was started. (for types 'qemu' and 'lxc')")
    netout: int | None = Field(None, description="The amount of traffic in bytes that was sent from the guest over the network since it was started. (for types 'qemu' and 'lxc')")
    network: StrictStr | None = Field(None, description="The name of a Network entity (for type 'network').")
    network_type: StrictStr | None = Field(None, alias="network-type", description="The type of network resource (for type 'network').")
    node: StrictStr | None = Field(None, description="The cluster node name (for types 'node', 'storage', 'qemu', and 'lxc').")
    plugintype: StrictStr | None = Field(None, description='More specific type, if available.')
    pool: StrictStr | None = Field(None, description="The pool name (for types 'pool', 'qemu' and 'lxc').")
    protocol: StrictStr | None = Field(None, description="The protocol of a fabric (for type 'network', network-type 'fabric').")
    sdn: StrictStr | None = Field(None, description="The name of an SDN entity (for type 'sdn')")
    shared: bool | None = Field(None, description='Determines whether the storage is shared')
    status: StrictStr | None = Field(None, description='Resource type dependent status.')
    storage: StrictStr | None = Field(None, description="The storage identifier (for type 'storage').")
    tags: StrictStr | None = Field(None, description="The guest's tags (for types 'qemu' and 'lxc')")
    template: bool | None = Field(None, description="Determines if the guest is a template. (for types 'qemu' and 'lxc')")
    type: StrictStr | None = Field(None, description='Resource type.')
    uptime: int | None = Field(None, description="Uptime of node or virtual guest in seconds (for types 'node', 'qemu' and 'lxc').")
    vmid: int | None = Field(None, description="The numerical vmid (for types 'qemu' and 'lxc').")
    zone_type: StrictStr | None = Field(None, alias="zone-type", description="The type of an SDN zone (for type 'sdn').")

class GetClusterResourcesResponse(RootModel[list[GetClusterResourcesResponseItem]]):
    """List of items. resources. Resources index (cluster wide). response."""
    root: list[GetClusterResourcesResponseItem] = Field(...)

class GetClusterSdnResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index. response."""
    id: StrictStr | None = Field(None)

class GetClusterSdnResponse(RootModel[list[GetClusterSdnResponseItem]]):
    """List of items. index. Directory index. response."""
    root: list[GetClusterSdnResponseItem] = Field(...)

class PutClusterSdnRequest(ProxmoxBaseModel):
    """Model for reload. Apply sdn controller changes && reload. request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    release_lock: bool | None = Field(None, alias="release-lock", description='When lock-token has been provided and configuration successfully committed, release the lock automatically afterwards')

class PutClusterSdnResponse(RootModel[StrictStr]):
    """Model for reload. Apply sdn controller changes && reload. response."""
    root: StrictStr = Field(...)

class GetClusterSdnControllersResponseItem(ProxmoxBaseModel):
    """Model for index. SDN controllers index. response."""
    asn: int | None = Field(None, description='The local ASN of the controller. BGP & EVPN only.')
    bgp_multipath_as_relax: bool | None = Field(None, alias="bgp-multipath-as-relax", description='Consider different AS paths of equal length for multipath computation. BGP only.')
    controller: StrictStr | None = Field(None, description='Name of the controller.')
    digest: StrictStr | None = Field(None, description='Digest of the controller section.')
    ebgp: bool | None = Field(None, description='Enable eBGP (remote-as external). BGP only.')
    ebgp_multihop: int | None = Field(None, alias="ebgp-multihop", description='Set maximum amount of hops for eBGP peers. Needs ebgp set to 1. BGP only.')
    isis_domain: StrictStr | None = Field(None, alias="isis-domain", description='Name of the IS-IS domain. IS-IS only.')
    isis_ifaces: StrictStr | None = Field(None, alias="isis-ifaces", description='Comma-separated list of interfaces where IS-IS should be active. IS-IS only.')
    isis_net: StrictStr | None = Field(None, alias="isis-net", description='Network Entity title for this node in the IS-IS network. IS-IS only.')
    loopback: StrictStr | None = Field(None, description='Name of the loopback/dummy interface that provides the Router-IP. BGP only.')
    node: StrictStr | None = Field(None, description='Node(s) where this controller is active.')
    peers: StrictStr | None = Field(None, description='Comma-separated list of the peers IP addresses.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: StrictStr | None = Field(None, description='State of the SDN configuration object.')
    type: StrictStr | None = Field(None, description='Type of the controller')

class GetClusterSdnControllersResponse(RootModel[list[GetClusterSdnControllersResponseItem]]):
    """List of items. index. SDN controllers index. response."""
    root: list[GetClusterSdnControllersResponseItem] = Field(...)

class PostClusterSdnControllersRequest(ProxmoxBaseModel):
    """Model for create. Create a new sdn controller object. request."""
    asn: int | None = Field(None, description='autonomous system number')
    bgp_multipath_as_path_relax: bool | None = Field(None, alias="bgp-multipath-as-path-relax", description='Consider different AS paths of equal length for multipath computation.')
    controller: StrictStr = Field(..., description='The SDN controller object identifier.')
    ebgp: bool | None = Field(None, description='Enable eBGP (remote-as external).')
    ebgp_multihop: int | None = Field(None, alias="ebgp-multihop", description='Set maximum amount of hops for eBGP peers.')
    fabric: StrictStr | None = Field(None, description='SDN fabric to use as underlay for this EVPN controller.')
    isis_domain: StrictStr | None = Field(None, alias="isis-domain", description='Name of the IS-IS domain.')
    isis_ifaces: StrictStr | None = Field(None, alias="isis-ifaces", description='Comma-separated list of interfaces where IS-IS should be active.')
    isis_net: StrictStr | None = Field(None, alias="isis-net", description='Network Entity title for this node in the IS-IS network.')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    loopback: StrictStr | None = Field(None, description='Name of the loopback/dummy interface that provides the Router-IP.')
    node: StrictStr | None = Field(None, description='The cluster node name.')
    peers: StrictStr | None = Field(None, description='peers address list.')
    type: StrictStr = Field(..., description='Plugin type.')

class PostClusterSdnControllersResponse(RootModel[None]):
    """Model for create. Create a new sdn controller object. response."""
    root: None = Field(...)

class DeleteClusterSdnControllersControllerRequest(ProxmoxBaseModel):
    """Model for delete. Delete sdn controller object configuration. request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnControllersControllerResponse(RootModel[None]):
    """Model for delete. Delete sdn controller object configuration. response."""
    root: None = Field(...)

class GetClusterSdnControllersControllerResponse(ProxmoxBaseModel):
    """Model for read. Read sdn controller configuration. response."""
    asn: int | None = Field(None, description='The local ASN of the controller. BGP & EVPN only.')
    bgp_multipath_as_relax: bool | None = Field(None, alias="bgp-multipath-as-relax", description='Consider different AS paths of equal length for multipath computation. BGP only.')
    controller: StrictStr = Field(..., description='Name of the controller.')
    digest: StrictStr | None = Field(None, description='Digest of the controller section.')
    ebgp: bool | None = Field(None, description='Enable eBGP (remote-as external). BGP only.')
    ebgp_multihop: int | None = Field(None, alias="ebgp-multihop", description='Set maximum amount of hops for eBGP peers. Needs ebgp set to 1. BGP only.')
    isis_domain: StrictStr | None = Field(None, alias="isis-domain", description='Name of the IS-IS domain. IS-IS only.')
    isis_ifaces: StrictStr | None = Field(None, alias="isis-ifaces", description='Comma-separated list of interfaces where IS-IS should be active. IS-IS only.')
    isis_net: StrictStr | None = Field(None, alias="isis-net", description='Network Entity title for this node in the IS-IS network. IS-IS only.')
    loopback: StrictStr | None = Field(None, description='Name of the loopback/dummy interface that provides the Router-IP. BGP only.')
    node: StrictStr | None = Field(None, description='Node(s) where this controller is active.')
    peers: StrictStr | None = Field(None, description='Comma-separated list of the peers IP addresses.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: StrictStr | None = Field(None, description='State of the SDN configuration object.')
    type: StrictStr = Field(..., description='Type of the controller')

class PutClusterSdnControllersControllerRequest(ProxmoxBaseModel):
    """Model for update. Update sdn controller object configuration. request."""
    asn: int | None = Field(None, description='autonomous system number')
    bgp_multipath_as_path_relax: bool | None = Field(None, alias="bgp-multipath-as-path-relax", description='Consider different AS paths of equal length for multipath computation.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    ebgp: bool | None = Field(None, description='Enable eBGP (remote-as external).')
    ebgp_multihop: int | None = Field(None, alias="ebgp-multihop", description='Set maximum amount of hops for eBGP peers.')
    fabric: StrictStr | None = Field(None, description='SDN fabric to use as underlay for this EVPN controller.')
    isis_domain: StrictStr | None = Field(None, alias="isis-domain", description='Name of the IS-IS domain.')
    isis_ifaces: StrictStr | None = Field(None, alias="isis-ifaces", description='Comma-separated list of interfaces where IS-IS should be active.')
    isis_net: StrictStr | None = Field(None, alias="isis-net", description='Network Entity title for this node in the IS-IS network.')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    loopback: StrictStr | None = Field(None, description='Name of the loopback/dummy interface that provides the Router-IP.')
    node: StrictStr | None = Field(None, description='The cluster node name.')
    peers: StrictStr | None = Field(None, description='peers address list.')

class PutClusterSdnControllersControllerResponse(RootModel[None]):
    """Model for update. Update sdn controller object configuration. response."""
    root: None = Field(...)

class GetClusterSdnDnsResponseItem(ProxmoxBaseModel):
    """Model for index. SDN dns index. response."""
    dns: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class GetClusterSdnDnsResponse(RootModel[list[GetClusterSdnDnsResponseItem]]):
    """List of items. index. SDN dns index. response."""
    root: list[GetClusterSdnDnsResponseItem] = Field(...)

class PostClusterSdnDnsRequest(ProxmoxBaseModel):
    """Model for create. Create a new sdn dns object. request."""
    dns: StrictStr = Field(..., description='The SDN dns object identifier.')
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    key: StrictStr = Field(...)
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    reversemaskv6: int | None = Field(None)
    reversev6mask: int | None = Field(None)
    ttl: int | None = Field(None)
    type: StrictStr = Field(..., description='Plugin type.')
    url: StrictStr = Field(...)

class PostClusterSdnDnsResponse(RootModel[None]):
    """Model for create. Create a new sdn dns object. response."""
    root: None = Field(...)

class DeleteClusterSdnDnsDnsRequest(ProxmoxBaseModel):
    """Model for delete. Delete sdn dns object configuration. request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnDnsDnsResponse(RootModel[None]):
    """Model for delete. Delete sdn dns object configuration. response."""
    root: None = Field(...)

class GetClusterSdnDnsDnsResponse(RootModel[dict[str, object]]):
    """Model for read. Read sdn dns configuration. response."""
    root: dict[str, object] = Field(...)

class PutClusterSdnDnsDnsRequest(ProxmoxBaseModel):
    """Model for update. Update sdn dns object configuration. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    key: StrictStr | None = Field(None)
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    reversemaskv6: int | None = Field(None)
    ttl: int | None = Field(None)
    url: StrictStr | None = Field(None)

class PutClusterSdnDnsDnsResponse(RootModel[None]):
    """Model for update. Update sdn dns object configuration. response."""
    root: None = Field(...)

class GetClusterSdnDryRunResponse(ProxmoxBaseModel):
    """Model for dry-run. Dry-run the SDN apply action and return the difference between the current configuration and the pending configuration response."""
    frr_diff: StrictStr | None = Field(None, alias="frr-diff", description='The difference between the current and pending FRR configuration.')
    interfaces_diff: StrictStr | None = Field(None, alias="interfaces-diff", description='The difference between the current and pending /etc/network/interfaces.d/sdn configuration.')

class GetClusterSdnFabricsResponseItem(ProxmoxBaseModel):
    """Model for index. SDN Fabrics Index response."""
    subdir: StrictStr | None = Field(None)

class GetClusterSdnFabricsResponse(RootModel[list[GetClusterSdnFabricsResponseItem]]):
    """List of items. index. SDN Fabrics Index response."""
    root: list[GetClusterSdnFabricsResponseItem] = Field(...)

class GetClusterSdnFabricsAllResponse(ProxmoxBaseModel):
    """Model for list_all. SDN Fabrics Index response."""
    fabrics: list[dict[str, object]] = Field(...)
    nodes: list[dict[str, object]] = Field(...)

class GetClusterSdnFabricsFabricResponseItem(ProxmoxBaseModel):
    """Model for index. SDN Fabrics Index response."""
    area: StrictStr | None = Field(None, description='OSPF area. Either a IPv4 address or a 32-bit number. Gets validated in rust.')
    csnp_interval: float | None = Field(None, description='The csnp_interval property for Openfabric')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    hello_interval: float | None = Field(None, description='The hello_interval property for Openfabric')
    id: StrictStr | None = Field(None, description='Identifier for SDN fabrics')
    ip6_prefix: StrictStr | None = Field(None, description='The IP prefix for Node IPs')
    ip_prefix: StrictStr | None = Field(None, description='The IP prefix for Node IPs')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: StrictStr | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')

class GetClusterSdnFabricsFabricResponse(RootModel[list[GetClusterSdnFabricsFabricResponseItem]]):
    """List of items. index. SDN Fabrics Index response."""
    root: list[GetClusterSdnFabricsFabricResponseItem] = Field(...)

class PostClusterSdnFabricsFabricRequest(ProxmoxBaseModel):
    """Model for add_fabric. Add a fabric request."""
    area: StrictStr | None = Field(None, description='OSPF area. Either a IPv4 address or a 32-bit number. Gets validated in rust.')
    csnp_interval: float | None = Field(None, description='The csnp_interval property for Openfabric')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    hello_interval: float | None = Field(None, description='The hello_interval property for Openfabric')
    id: StrictStr = Field(..., description='Identifier for SDN fabrics')
    ip6_prefix: StrictStr | None = Field(None, description='The IP prefix for Node IPs')
    ip_prefix: StrictStr | None = Field(None, description='The IP prefix for Node IPs')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PostClusterSdnFabricsFabricResponse(RootModel[None]):
    """Model for add_fabric. Add a fabric response."""
    root: None = Field(...)

class DeleteClusterSdnFabricsFabricIdRequest(RootModel[dict[str, object]]):
    """Model for delete_fabric. Add a fabric request."""
    root: dict[str, object] = Field(...)

class DeleteClusterSdnFabricsFabricIdResponse(RootModel[None]):
    """Model for delete_fabric. Add a fabric response."""
    root: None = Field(...)

class GetClusterSdnFabricsFabricIdResponse(ProxmoxBaseModel):
    """Model for get_fabric. Update a fabric response."""
    area: StrictStr | None = Field(None, description='OSPF area. Either a IPv4 address or a 32-bit number. Gets validated in rust.')
    csnp_interval: float | None = Field(None, description='The csnp_interval property for Openfabric')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    hello_interval: float | None = Field(None, description='The hello_interval property for Openfabric')
    id: StrictStr = Field(..., description='Identifier for SDN fabrics')
    ip6_prefix: StrictStr | None = Field(None, description='The IP prefix for Node IPs')
    ip_prefix: StrictStr | None = Field(None, description='The IP prefix for Node IPs')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PutClusterSdnFabricsFabricIdRequest(ProxmoxBaseModel):
    """Model for update_fabric. Update a fabric request."""
    area: StrictStr | None = Field(None, description='OSPF area. Either a IPv4 address or a 32-bit number. Gets validated in rust.')
    csnp_interval: float | None = Field(None, description='The csnp_interval property for Openfabric')
    delete: list[StrictStr] = Field(...)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    hello_interval: float | None = Field(None, description='The hello_interval property for Openfabric')
    ip6_prefix: StrictStr | None = Field(None, description='The IP prefix for Node IPs')
    ip_prefix: StrictStr | None = Field(None, description='The IP prefix for Node IPs')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PutClusterSdnFabricsFabricIdResponse(RootModel[None]):
    """Model for update_fabric. Update a fabric response."""
    root: None = Field(...)

class GetClusterSdnFabricsNodeResponseItem(ProxmoxBaseModel):
    """Model for list_nodes. SDN Fabrics Index response."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fabric_id: StrictStr | None = Field(None, description='Identifier for SDN fabrics')
    interfaces: list[StrictStr] | None = Field(None)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: StrictStr | None = Field(None, description='Identifier for nodes in an SDN fabric')
    protocol: StrictStr | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')

class GetClusterSdnFabricsNodeResponse(RootModel[list[GetClusterSdnFabricsNodeResponseItem]]):
    """List of items. list_nodes. SDN Fabrics Index response."""
    root: list[GetClusterSdnFabricsNodeResponseItem] = Field(...)

class GetClusterSdnFabricsNodeFabricIdResponseItem(ProxmoxBaseModel):
    """Model for list_nodes_fabric. SDN Fabrics Index response."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fabric_id: StrictStr | None = Field(None, description='Identifier for SDN fabrics')
    interfaces: list[StrictStr] | None = Field(None)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: StrictStr | None = Field(None, description='Identifier for nodes in an SDN fabric')
    protocol: StrictStr | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')

class GetClusterSdnFabricsNodeFabricIdResponse(RootModel[list[GetClusterSdnFabricsNodeFabricIdResponseItem]]):
    """List of items. list_nodes_fabric. SDN Fabrics Index response."""
    root: list[GetClusterSdnFabricsNodeFabricIdResponseItem] = Field(...)

class PostClusterSdnFabricsNodeFabricIdRequest(ProxmoxBaseModel):
    """Model for add_node. Add a node request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    interfaces: list[StrictStr] = Field(...)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: StrictStr = Field(..., description='Identifier for nodes in an SDN fabric')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PostClusterSdnFabricsNodeFabricIdResponse(RootModel[None]):
    """Model for add_node. Add a node response."""
    root: None = Field(...)

class DeleteClusterSdnFabricsNodeFabricIdNodeIdRequest(RootModel[dict[str, object]]):
    """Model for delete_node. Add a node request."""
    root: dict[str, object] = Field(...)

class DeleteClusterSdnFabricsNodeFabricIdNodeIdResponse(RootModel[None]):
    """Model for delete_node. Add a node response."""
    root: None = Field(...)

class GetClusterSdnFabricsNodeFabricIdNodeIdResponse(ProxmoxBaseModel):
    """Model for get_node. Get a node response."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fabric_id: StrictStr = Field(..., description='Identifier for SDN fabrics')
    interfaces: list[StrictStr] = Field(...)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: StrictStr = Field(..., description='Identifier for nodes in an SDN fabric')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PutClusterSdnFabricsNodeFabricIdNodeIdRequest(ProxmoxBaseModel):
    """Model for update_node. Update a node request."""
    delete: list[StrictStr] | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    interfaces: list[StrictStr] = Field(...)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')

class PutClusterSdnFabricsNodeFabricIdNodeIdResponse(RootModel[None]):
    """Model for update_node. Update a node response."""
    root: None = Field(...)

class GetClusterSdnIpamsResponseItem(ProxmoxBaseModel):
    """Model for index. SDN ipams index. response."""
    ipam: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class GetClusterSdnIpamsResponse(RootModel[list[GetClusterSdnIpamsResponseItem]]):
    """List of items. index. SDN ipams index. response."""
    root: list[GetClusterSdnIpamsResponseItem] = Field(...)

class PostClusterSdnIpamsRequest(ProxmoxBaseModel):
    """Model for create. Create a new sdn ipam object. request."""
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    ipam: StrictStr = Field(..., description='The SDN ipam object identifier.')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    section: int | None = Field(None)
    token: StrictStr | None = Field(None)
    type: StrictStr = Field(..., description='Plugin type.')
    url: StrictStr | None = Field(None)

class PostClusterSdnIpamsResponse(RootModel[None]):
    """Model for create. Create a new sdn ipam object. response."""
    root: None = Field(...)

class DeleteClusterSdnIpamsIpamRequest(ProxmoxBaseModel):
    """Model for delete. Delete sdn ipam object configuration. request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnIpamsIpamResponse(RootModel[None]):
    """Model for delete. Delete sdn ipam object configuration. response."""
    root: None = Field(...)

class GetClusterSdnIpamsIpamResponse(RootModel[dict[str, object]]):
    """Model for read. Read sdn ipam configuration. response."""
    root: dict[str, object] = Field(...)

class PutClusterSdnIpamsIpamRequest(ProxmoxBaseModel):
    """Model for update. Update sdn ipam object configuration. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    section: int | None = Field(None)
    token: StrictStr | None = Field(None)
    url: StrictStr | None = Field(None)

class PutClusterSdnIpamsIpamResponse(RootModel[None]):
    """Model for update. Update sdn ipam object configuration. response."""
    root: None = Field(...)

class GetClusterSdnIpamsIpamStatusResponse(RootModel[list[object]]):
    """Model for ipamindex. List PVE IPAM Entries response."""
    root: list[object] = Field(...)

class DeleteClusterSdnLockRequest(ProxmoxBaseModel):
    """Model for release_lock. Release global lock for SDN configuration request."""
    force: bool | None = Field(None, description='if true, allow releasing lock without providing the token')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnLockResponse(RootModel[None]):
    """Model for release_lock. Release global lock for SDN configuration response."""
    root: None = Field(...)

class PostClusterSdnLockRequest(ProxmoxBaseModel):
    """Model for lock. Acquire global lock for SDN configuration request."""
    allow_pending: bool | None = Field(None, alias="allow-pending", description='if true, allow acquiring lock even though there are pending changes')

class PostClusterSdnLockResponse(RootModel[StrictStr]):
    """Model for lock. Acquire global lock for SDN configuration response."""
    root: StrictStr = Field(...)

class PostClusterSdnRollbackRequest(ProxmoxBaseModel):
    """Model for rollback. Rollback pending changes to SDN configuration request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    release_lock: bool | None = Field(None, alias="release-lock", description='When lock-token has been provided and configuration successfully rollbacked, release the lock automatically afterwards')

class PostClusterSdnRollbackResponse(RootModel[None]):
    """Model for rollback. Rollback pending changes to SDN configuration response."""
    root: None = Field(...)

class GetClusterSdnVnetsResponseItem(ProxmoxBaseModel):
    """Model for index. SDN vnets index. response."""
    alias: StrictStr | None = Field(None, description='Alias name of the VNet.')
    digest: StrictStr | None = Field(None, description='Digest of the VNet section.')
    isolate_ports: bool | None = Field(None, alias="isolate-ports", description='If true, sets the isolated property for all interfaces on the bridge of this VNet.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: StrictStr | None = Field(None, description='State of the SDN configuration object.')
    tag: int | None = Field(None, description='VLAN Tag (for VLAN or QinQ zones) or VXLAN VNI (for VXLAN or EVPN zones).')
    type: StrictStr | None = Field(None, description='Type of the VNet.')
    vlanaware: bool | None = Field(None, description='Allow VLANs to pass through this VNet.')
    vnet: StrictStr | None = Field(None, description='Name of the VNet.')
    zone: StrictStr | None = Field(None, description='Name of the zone this VNet belongs to.')

class GetClusterSdnVnetsResponse(RootModel[list[GetClusterSdnVnetsResponseItem]]):
    """List of items. index. SDN vnets index. response."""
    root: list[GetClusterSdnVnetsResponseItem] = Field(...)

class PostClusterSdnVnetsRequest(ProxmoxBaseModel):
    """Model for create. Create a new sdn vnet object. request."""
    alias: StrictStr | None = Field(None, description='Alias name of the VNet.')
    isolate_ports: bool | None = Field(None, alias="isolate-ports", description='If true, sets the isolated property for all interfaces on the bridge of this VNet.')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    tag: int | None = Field(None, description='VLAN Tag (for VLAN or QinQ zones) or VXLAN VNI (for VXLAN or EVPN zones).')
    type: StrictStr | None = Field(None, description='Type of the VNet.')
    vlanaware: bool | None = Field(None, description='Allow VLANs to pass through this vnet.')
    vnet: StrictStr = Field(..., description='The SDN vnet object identifier.')
    zone: StrictStr = Field(..., description='Name of the zone this VNet belongs to.')

class PostClusterSdnVnetsResponse(RootModel[None]):
    """Model for create. Create a new sdn vnet object. response."""
    root: None = Field(...)

class DeleteClusterSdnVnetsVnetRequest(ProxmoxBaseModel):
    """Model for delete. Delete sdn vnet object configuration. request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnVnetsVnetResponse(RootModel[None]):
    """Model for delete. Delete sdn vnet object configuration. response."""
    root: None = Field(...)

class GetClusterSdnVnetsVnetResponse(ProxmoxBaseModel):
    """Model for read. Read sdn vnet configuration. response."""
    alias: StrictStr | None = Field(None, description='Alias name of the VNet.')
    digest: StrictStr | None = Field(None, description='Digest of the VNet section.')
    isolate_ports: bool | None = Field(None, alias="isolate-ports", description='If true, sets the isolated property for all interfaces on the bridge of this VNet.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: StrictStr | None = Field(None, description='State of the SDN configuration object.')
    tag: int | None = Field(None, description='VLAN Tag (for VLAN or QinQ zones) or VXLAN VNI (for VXLAN or EVPN zones).')
    type: StrictStr = Field(..., description='Type of the VNet.')
    vlanaware: bool | None = Field(None, description='Allow VLANs to pass through this VNet.')
    vnet: StrictStr = Field(..., description='Name of the VNet.')
    zone: StrictStr | None = Field(None, description='Name of the zone this VNet belongs to.')

class PutClusterSdnVnetsVnetRequest(ProxmoxBaseModel):
    """Model for update. Update sdn vnet object configuration. request."""
    alias: StrictStr | None = Field(None, description='Alias name of the VNet.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    isolate_ports: bool | None = Field(None, alias="isolate-ports", description='If true, sets the isolated property for all interfaces on the bridge of this VNet.')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    tag: int | None = Field(None, description='VLAN Tag (for VLAN or QinQ zones) or VXLAN VNI (for VXLAN or EVPN zones).')
    vlanaware: bool | None = Field(None, description='Allow VLANs to pass through this vnet.')
    zone: StrictStr | None = Field(None, description='Name of the zone this VNet belongs to.')

class PutClusterSdnVnetsVnetResponse(RootModel[None]):
    """Model for update. Update sdn vnet object configuration. response."""
    root: None = Field(...)

class GetClusterSdnVnetsVnetFirewallResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterSdnVnetsVnetFirewallOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get vnet firewall options. response."""
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    log_level_forward: StrictStr | None = Field(None, description='Log level for forwarded traffic.')
    policy_forward: StrictStr | None = Field(None, description='Forward policy.')

class PutClusterSdnVnetsVnetFirewallOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set Firewall options. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    log_level_forward: StrictStr | None = Field(None, description='Log level for forwarded traffic.')
    policy_forward: StrictStr | None = Field(None, description='Forward policy.')

class PutClusterSdnVnetsVnetFirewallOptionsResponse(RootModel[None]):
    """Model for set_options. Set Firewall options. response."""
    root: None = Field(...)

class GetClusterSdnVnetsVnetFirewallRulesResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetClusterSdnVnetsVnetFirewallRulesResponse(RootModel[list[GetClusterSdnVnetsVnetFirewallRulesResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetClusterSdnVnetsVnetFirewallRulesResponseItem] = Field(...)

class PostClusterSdnVnetsVnetFirewallRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostClusterSdnVnetsVnetFirewallRulesResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteClusterSdnVnetsVnetFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteClusterSdnVnetsVnetFirewallRulesPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetClusterSdnVnetsVnetFirewallRulesPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutClusterSdnVnetsVnetFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutClusterSdnVnetsVnetFirewallRulesPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class DeleteClusterSdnVnetsVnetIpsRequest(ProxmoxBaseModel):
    """Model for ipdelete. Delete IP Mappings in a VNet request."""
    ip: StrictStr = Field(..., description='The IP address to delete')
    mac: StrictStr | None = Field(None, description='Unicast MAC address.')
    zone: StrictStr = Field(..., description='The SDN zone object identifier.')

class DeleteClusterSdnVnetsVnetIpsResponse(RootModel[None]):
    """Model for ipdelete. Delete IP Mappings in a VNet response."""
    root: None = Field(...)

class PostClusterSdnVnetsVnetIpsRequest(ProxmoxBaseModel):
    """Model for ipcreate. Create IP Mapping in a VNet request."""
    ip: StrictStr = Field(..., description='The IP address to associate with the given MAC address')
    mac: StrictStr | None = Field(None, description='Unicast MAC address.')
    zone: StrictStr = Field(..., description='The SDN zone object identifier.')

class PostClusterSdnVnetsVnetIpsResponse(RootModel[None]):
    """Model for ipcreate. Create IP Mapping in a VNet response."""
    root: None = Field(...)

class PutClusterSdnVnetsVnetIpsRequest(ProxmoxBaseModel):
    """Model for ipupdate. Update IP Mapping in a VNet request."""
    ip: StrictStr = Field(..., description='The IP address to associate with the given MAC address')
    mac: StrictStr | None = Field(None, description='Unicast MAC address.')
    vmid: int | None = Field(None, description='The (unique) ID of the VM.')
    zone: StrictStr = Field(..., description='The SDN zone object identifier.')

class PutClusterSdnVnetsVnetIpsResponse(RootModel[None]):
    """Model for ipupdate. Update IP Mapping in a VNet response."""
    root: None = Field(...)

class GetClusterSdnVnetsVnetSubnetsResponse(RootModel[list[dict[str, object]]]):
    """Model for index. SDN subnets index. response."""
    root: list[dict[str, object]] = Field(...)

class PostClusterSdnVnetsVnetSubnetsRequest(ProxmoxBaseModel):
    """Model for create. Create a new sdn subnet object. request."""
    dhcp_dns_server: StrictStr | None = Field(None, alias="dhcp-dns-server", description='IP address for the DNS server')
    dhcp_range: list[StrictStr] | None = Field(None, alias="dhcp-range", description='A list of DHCP ranges for this subnet')
    dnszoneprefix: StrictStr | None = Field(None, description="dns domain zone prefix  ex: 'adm' -> <hostname>.adm.mydomain.com")
    gateway: StrictStr | None = Field(None, description='Subnet Gateway: Will be assign on vnet for layer3 zones')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    snat: bool | None = Field(None, description='enable masquerade for this subnet if pve-firewall')
    subnet: StrictStr = Field(..., description='The SDN subnet object identifier.')
    type: StrictStr = Field(...)

class PostClusterSdnVnetsVnetSubnetsResponse(RootModel[None]):
    """Model for create. Create a new sdn subnet object. response."""
    root: None = Field(...)

class DeleteClusterSdnVnetsVnetSubnetsSubnetRequest(ProxmoxBaseModel):
    """Model for delete. Delete sdn subnet object configuration. request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnVnetsVnetSubnetsSubnetResponse(RootModel[None]):
    """Model for delete. Delete sdn subnet object configuration. response."""
    root: None = Field(...)

class GetClusterSdnVnetsVnetSubnetsSubnetResponse(RootModel[dict[str, object]]):
    """Model for read. Read sdn subnet configuration. response."""
    root: dict[str, object] = Field(...)

class PutClusterSdnVnetsVnetSubnetsSubnetRequest(ProxmoxBaseModel):
    """Model for update. Update sdn subnet object configuration. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dhcp_dns_server: StrictStr | None = Field(None, alias="dhcp-dns-server", description='IP address for the DNS server')
    dhcp_range: list[StrictStr] | None = Field(None, alias="dhcp-range", description='A list of DHCP ranges for this subnet')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dnszoneprefix: StrictStr | None = Field(None, description="dns domain zone prefix  ex: 'adm' -> <hostname>.adm.mydomain.com")
    gateway: StrictStr | None = Field(None, description='Subnet Gateway: Will be assign on vnet for layer3 zones')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    snat: bool | None = Field(None, description='enable masquerade for this subnet if pve-firewall')

class PutClusterSdnVnetsVnetSubnetsSubnetResponse(RootModel[None]):
    """Model for update. Update sdn subnet object configuration. response."""
    root: None = Field(...)

class GetClusterSdnZonesResponseItem(ProxmoxBaseModel):
    """Model for index. SDN zones index. response."""
    advertise_subnets: bool | None = Field(None, alias="advertise-subnets", description='Advertise IP prefixes (Type-5 routes) instead of MAC/IP pairs (Type-2 routes). EVPN zone only.')
    bridge: StrictStr | None = Field(None, description='the bridge for which VLANs should be managed. VLAN & QinQ zone only.')
    bridge_disable_mac_learning: bool | None = Field(None, alias="bridge-disable-mac-learning", description='Disable auto mac learning. VLAN zone only.')
    controller: StrictStr | None = Field(None, description='ID of the controller for this zone. EVPN zone only.')
    dhcp: StrictStr | None = Field(None, description='Name of DHCP server backend for this zone.')
    digest: StrictStr | None = Field(None, description='Digest of the controller section.')
    disable_arp_nd_suppression: bool | None = Field(None, alias="disable-arp-nd-suppression", description='Suppress IPv4 ARP && IPv6 Neighbour Discovery messages. EVPN zone only.')
    dns: StrictStr | None = Field(None, description='ID of the DNS server for this zone.')
    dnszone: StrictStr | None = Field(None, description='Domain name for this zone.')
    exitnodes: StrictStr | None = Field(None, description='List of PVE Nodes that should act as exit node for this zone. EVPN zone only.')
    exitnodes_local_routing: bool | None = Field(None, alias="exitnodes-local-routing", description='Create routes on the exit nodes, so they can connect to EVPN guests. EVPN zone only.')
    exitnodes_primary: StrictStr | None = Field(None, alias="exitnodes-primary", description='Force traffic through this exitnode first. EVPN zone only.')
    ipam: StrictStr | None = Field(None, description='ID of the IPAM for this zone.')
    mac: StrictStr | None = Field(None, description='MAC address of the anycast router for this zone.')
    mtu: int | None = Field(None, description='MTU of the zone, will be used for the created VNet bridges.')
    nodes: StrictStr | None = Field(None, description='Nodes where this zone should be created.')
    peers: StrictStr | None = Field(None, description='Comma-separated list of peers, that are part of the VXLAN zone. Usually the IPs of the nodes. VXLAN zone only.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    reversedns: StrictStr | None = Field(None, description='ID of the reverse DNS server for this zone.')
    rt_import: StrictStr | None = Field(None, alias="rt-import", description='Route-Targets that should be imported into the VRF of this zone via BGP. EVPN zone only.')
    state: StrictStr | None = Field(None, description='State of the SDN configuration object.')
    tag: int | None = Field(None, description='Service-VLAN Tag (outer VLAN). QinQ zone only')
    type: StrictStr | None = Field(None, description='Type of the zone.')
    vlan_protocol: StrictStr | None = Field(None, alias="vlan-protocol", description='VLAN protocol for the creation of the QinQ zone. QinQ zone only.')
    vrf_vxlan: int | None = Field(None, alias="vrf-vxlan", description='VNI for the zone VRF. EVPN zone only.')
    vxlan_port: int | None = Field(None, alias="vxlan-port", description='UDP port that should be used for the VXLAN tunnel (default 4789). VXLAN zone only.')
    zone: StrictStr | None = Field(None, description='Name of the zone.')

class GetClusterSdnZonesResponse(RootModel[list[GetClusterSdnZonesResponseItem]]):
    """List of items. index. SDN zones index. response."""
    root: list[GetClusterSdnZonesResponseItem] = Field(...)

class PostClusterSdnZonesRequest(ProxmoxBaseModel):
    """Model for create. Create a new sdn zone object. request."""
    advertise_subnets: bool | None = Field(None, alias="advertise-subnets", description='Advertise IP prefixes (Type-5 routes) instead of MAC/IP pairs (Type-2 routes).')
    bridge: StrictStr | None = Field(None, description='The bridge for which VLANs should be managed.')
    bridge_disable_mac_learning: bool | None = Field(None, alias="bridge-disable-mac-learning", description='Disable auto mac learning.')
    controller: StrictStr | None = Field(None, description='Controller for this zone.')
    dhcp: StrictStr | None = Field(None, description='Type of the DHCP backend for this zone')
    disable_arp_nd_suppression: bool | None = Field(None, alias="disable-arp-nd-suppression", description='Suppress IPv4 ARP && IPv6 Neighbour Discovery messages.')
    dns: StrictStr | None = Field(None, description='dns api server')
    dnszone: StrictStr | None = Field(None, description='dns domain zone  ex: mydomain.com')
    dp_id: int | None = Field(None, alias="dp-id", description='Faucet dataplane id')
    exitnodes: StrictStr | None = Field(None, description='List of cluster node names.')
    exitnodes_local_routing: bool | None = Field(None, alias="exitnodes-local-routing", description='Allow exitnodes to connect to EVPN guests.')
    exitnodes_primary: StrictStr | None = Field(None, alias="exitnodes-primary", description='Force traffic through this exitnode first.')
    fabric: StrictStr | None = Field(None, description='SDN fabric to use as underlay for this VXLAN zone.')
    ipam: StrictStr | None = Field(None, description='use a specific ipam')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    mac: StrictStr | None = Field(None, description='Anycast logical router mac address.')
    mtu: int | None = Field(None, description='MTU of the zone, will be used for the created VNet bridges.')
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    peers: StrictStr | None = Field(None, description='Comma-separated list of peers, that are part of the VXLAN zone. Usually the IPs of the nodes.')
    reversedns: StrictStr | None = Field(None, description='reverse dns api server')
    rt_import: StrictStr | None = Field(None, alias="rt-import", description='List of Route Targets that should be imported into the VRF of the zone.')
    tag: int | None = Field(None, description='Service-VLAN Tag (outer VLAN)')
    type: StrictStr = Field(..., description='Plugin type.')
    vlan_protocol: StrictStr | None = Field(None, alias="vlan-protocol", description='Which VLAN protocol should be used for the creation of the QinQ zone.')
    vrf_vxlan: int | None = Field(None, alias="vrf-vxlan", description='VNI for the zone VRF.')
    vxlan_port: int | None = Field(None, alias="vxlan-port", description='UDP port that should be used for the VXLAN tunnel (default 4789).')
    zone: StrictStr = Field(..., description='The SDN zone object identifier.')

class PostClusterSdnZonesResponse(RootModel[None]):
    """Model for create. Create a new sdn zone object. response."""
    root: None = Field(...)

class DeleteClusterSdnZonesZoneRequest(ProxmoxBaseModel):
    """Model for delete. Delete sdn zone object configuration. request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnZonesZoneResponse(RootModel[None]):
    """Model for delete. Delete sdn zone object configuration. response."""
    root: None = Field(...)

class GetClusterSdnZonesZoneResponse(ProxmoxBaseModel):
    """Model for read. Read sdn zone configuration. response."""
    advertise_subnets: bool | None = Field(None, alias="advertise-subnets", description='Advertise IP prefixes (Type-5 routes) instead of MAC/IP pairs (Type-2 routes). EVPN zone only.')
    bridge: StrictStr | None = Field(None, description='the bridge for which VLANs should be managed. VLAN & QinQ zone only.')
    bridge_disable_mac_learning: bool | None = Field(None, alias="bridge-disable-mac-learning", description='Disable auto mac learning. VLAN zone only.')
    controller: StrictStr | None = Field(None, description='ID of the controller for this zone. EVPN zone only.')
    dhcp: StrictStr | None = Field(None, description='Name of DHCP server backend for this zone.')
    digest: StrictStr | None = Field(None, description='Digest of the controller section.')
    disable_arp_nd_suppression: bool | None = Field(None, alias="disable-arp-nd-suppression", description='Suppress IPv4 ARP && IPv6 Neighbour Discovery messages. EVPN zone only.')
    dns: StrictStr | None = Field(None, description='ID of the DNS server for this zone.')
    dnszone: StrictStr | None = Field(None, description='Domain name for this zone.')
    exitnodes: StrictStr | None = Field(None, description='List of PVE Nodes that should act as exit node for this zone. EVPN zone only.')
    exitnodes_local_routing: bool | None = Field(None, alias="exitnodes-local-routing", description='Create routes on the exit nodes, so they can connect to EVPN guests. EVPN zone only.')
    exitnodes_primary: StrictStr | None = Field(None, alias="exitnodes-primary", description='Force traffic through this exitnode first. EVPN zone only.')
    ipam: StrictStr | None = Field(None, description='ID of the IPAM for this zone.')
    mac: StrictStr | None = Field(None, description='MAC address of the anycast router for this zone.')
    mtu: int | None = Field(None, description='MTU of the zone, will be used for the created VNet bridges.')
    nodes: StrictStr | None = Field(None, description='Nodes where this zone should be created.')
    peers: StrictStr | None = Field(None, description='Comma-separated list of peers, that are part of the VXLAN zone. Usually the IPs of the nodes. VXLAN zone only.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    reversedns: StrictStr | None = Field(None, description='ID of the reverse DNS server for this zone.')
    rt_import: StrictStr | None = Field(None, alias="rt-import", description='Route-Targets that should be imported into the VRF of this zone via BGP. EVPN zone only.')
    state: StrictStr | None = Field(None, description='State of the SDN configuration object.')
    tag: int | None = Field(None, description='Service-VLAN Tag (outer VLAN). QinQ zone only')
    type: StrictStr = Field(..., description='Type of the zone.')
    vlan_protocol: StrictStr | None = Field(None, alias="vlan-protocol", description='VLAN protocol for the creation of the QinQ zone. QinQ zone only.')
    vrf_vxlan: int | None = Field(None, alias="vrf-vxlan", description='VNI for the zone VRF. EVPN zone only.')
    vxlan_port: int | None = Field(None, alias="vxlan-port", description='UDP port that should be used for the VXLAN tunnel (default 4789). VXLAN zone only.')
    zone: StrictStr = Field(..., description='Name of the zone.')

class PutClusterSdnZonesZoneRequest(ProxmoxBaseModel):
    """Model for update. Update sdn zone object configuration. request."""
    advertise_subnets: bool | None = Field(None, alias="advertise-subnets", description='Advertise IP prefixes (Type-5 routes) instead of MAC/IP pairs (Type-2 routes).')
    bridge: StrictStr | None = Field(None, description='The bridge for which VLANs should be managed.')
    bridge_disable_mac_learning: bool | None = Field(None, alias="bridge-disable-mac-learning", description='Disable auto mac learning.')
    controller: StrictStr | None = Field(None, description='Controller for this zone.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dhcp: StrictStr | None = Field(None, description='Type of the DHCP backend for this zone')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable_arp_nd_suppression: bool | None = Field(None, alias="disable-arp-nd-suppression", description='Suppress IPv4 ARP && IPv6 Neighbour Discovery messages.')
    dns: StrictStr | None = Field(None, description='dns api server')
    dnszone: StrictStr | None = Field(None, description='dns domain zone  ex: mydomain.com')
    dp_id: int | None = Field(None, alias="dp-id", description='Faucet dataplane id')
    exitnodes: StrictStr | None = Field(None, description='List of cluster node names.')
    exitnodes_local_routing: bool | None = Field(None, alias="exitnodes-local-routing", description='Allow exitnodes to connect to EVPN guests.')
    exitnodes_primary: StrictStr | None = Field(None, alias="exitnodes-primary", description='Force traffic through this exitnode first.')
    fabric: StrictStr | None = Field(None, description='SDN fabric to use as underlay for this VXLAN zone.')
    ipam: StrictStr | None = Field(None, description='use a specific ipam')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    mac: StrictStr | None = Field(None, description='Anycast logical router mac address.')
    mtu: int | None = Field(None, description='MTU of the zone, will be used for the created VNet bridges.')
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    peers: StrictStr | None = Field(None, description='Comma-separated list of peers, that are part of the VXLAN zone. Usually the IPs of the nodes.')
    reversedns: StrictStr | None = Field(None, description='reverse dns api server')
    rt_import: StrictStr | None = Field(None, alias="rt-import", description='List of Route Targets that should be imported into the VRF of the zone.')
    tag: int | None = Field(None, description='Service-VLAN Tag (outer VLAN)')
    vlan_protocol: StrictStr | None = Field(None, alias="vlan-protocol", description='Which VLAN protocol should be used for the creation of the QinQ zone.')
    vrf_vxlan: int | None = Field(None, alias="vrf-vxlan", description='VNI for the zone VRF.')
    vxlan_port: int | None = Field(None, alias="vxlan-port", description='UDP port that should be used for the VXLAN tunnel (default 4789).')

class PutClusterSdnZonesZoneResponse(RootModel[None]):
    """Model for update. Update sdn zone object configuration. response."""
    root: None = Field(...)

class GetClusterStatusResponseItem(ProxmoxBaseModel):
    """Model for get_status. Get cluster status information. response."""
    id: StrictStr | None = Field(None)
    ip: StrictStr | None = Field(None, description='[node] IP of the resolved nodename.')
    level: StrictStr | None = Field(None, description='[node] Proxmox VE Subscription level, indicates if eligible for enterprise support as well as access to the stable Proxmox VE Enterprise Repository.')
    local: bool | None = Field(None, description='[node] Indicates if this is the responding node.')
    name: StrictStr | None = Field(None)
    nodeid: int | None = Field(None, description='[node] ID of the node from the corosync configuration.')
    nodes: int | None = Field(None, description='[cluster] Nodes count, including offline nodes.')
    online: bool | None = Field(None, description='[node] Indicates if the node is online or offline.')
    quorate: bool | None = Field(None, description='[cluster] Indicates if there is a majority of nodes online to make decisions')
    type: StrictStr | None = Field(None, description='Indicates the type, either cluster or node. The type defines the object properties e.g. quorate available for type cluster.')
    version: int | None = Field(None, description='[cluster] Current version of the corosync configuration file.')

class GetClusterStatusResponse(RootModel[list[GetClusterStatusResponseItem]]):
    """List of items. get_status. Get cluster status information. response."""
    root: list[GetClusterStatusResponseItem] = Field(...)

class GetClusterTasksResponseItem(ProxmoxBaseModel):
    """Model for tasks. List recent tasks (cluster wide). response."""
    upid: StrictStr | None = Field(None)

class GetClusterTasksResponse(RootModel[list[GetClusterTasksResponseItem]]):
    """List of items. tasks. List recent tasks (cluster wide). response."""
    root: list[GetClusterTasksResponseItem] = Field(...)

class GetNodesResponseItem(ProxmoxBaseModel):
    """Model for index. Cluster node index. response."""
    cpu: float | None = Field(None, description='CPU utilization.')
    level: StrictStr | None = Field(None, description='Support level.')
    maxcpu: int | None = Field(None, description='Number of available CPUs.')
    maxmem: int | None = Field(None, description='Number of available memory in bytes.')
    mem: int | None = Field(None, description='Used memory in bytes.')
    node: StrictStr | None = Field(None, description='The cluster node name.')
    ssl_fingerprint: StrictStr | None = Field(None, description='The SSL fingerprint for the node certificate.')
    status: StrictStr | None = Field(None, description='Node status.')
    uptime: int | None = Field(None, description='Node uptime in seconds.')

class GetNodesResponse(RootModel[list[GetNodesResponseItem]]):
    """List of items. index. Cluster node index. response."""
    root: list[GetNodesResponseItem] = Field(...)

class GetNodesNodeResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Node index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeAplinfoResponse(RootModel[list[dict[str, object]]]):
    """Model for aplinfo. Get list of appliances. response."""
    root: list[dict[str, object]] = Field(...)

class PostNodesNodeAplinfoRequest(ProxmoxBaseModel):
    """Model for apl_download. Download appliance templates. request."""
    storage: StrictStr = Field(..., description='The storage where the template will be stored')
    template: StrictStr = Field(..., description='The template which will downloaded')

class PostNodesNodeAplinfoResponse(RootModel[StrictStr]):
    """Model for apl_download. Download appliance templates. response."""
    root: StrictStr = Field(...)

class GetNodesNodeAptResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index for apt (Advanced Package Tool). response."""
    id: StrictStr | None = Field(None)

class GetNodesNodeAptResponse(RootModel[list[GetNodesNodeAptResponseItem]]):
    """List of items. index. Directory index for apt (Advanced Package Tool). response."""
    root: list[GetNodesNodeAptResponseItem] = Field(...)

class GetNodesNodeAptChangelogResponse(RootModel[StrictStr]):
    """Model for changelog. Get package changelogs. response."""
    root: StrictStr = Field(...)

class GetNodesNodeAptRepositoriesResponse(ProxmoxBaseModel):
    """Model for repositories. Get APT repository information. response."""
    digest: StrictStr = Field(..., description='Common digest of all files.')
    errors: list[dict[str, object]] = Field(..., description='List of problematic repository files.')
    files: list[dict[str, object]] = Field(..., description='List of parsed repository files.')
    infos: list[dict[str, object]] = Field(..., description='Additional information/warnings for APT repositories.')
    standard_repos: list[dict[str, object]] = Field(..., alias="standard-repos", description='List of standard repositories and their configuration status')

class PostNodesNodeAptRepositoriesRequest(ProxmoxBaseModel):
    """Model for change_repository. Change the properties of a repository. Currently only allows enabling/disabling. request."""
    digest: StrictStr | None = Field(None, description='Digest to detect modifications.')
    enabled: bool | None = Field(None, description='Whether the repository should be enabled or not.')
    index: int = Field(..., description='Index within the file (starting from 0).')
    path: StrictStr = Field(..., description='Path to the containing file.')

class PostNodesNodeAptRepositoriesResponse(RootModel[None]):
    """Model for change_repository. Change the properties of a repository. Currently only allows enabling/disabling. response."""
    root: None = Field(...)

class PutNodesNodeAptRepositoriesRequest(ProxmoxBaseModel):
    """Model for add_repository. Add a standard repository to the configuration request."""
    digest: StrictStr | None = Field(None, description='Digest to detect modifications.')
    handle: StrictStr = Field(..., description='Handle that identifies a repository.')

class PutNodesNodeAptRepositoriesResponse(RootModel[None]):
    """Model for add_repository. Add a standard repository to the configuration response."""
    root: None = Field(...)

class GetNodesNodeAptUpdateResponseItem(ProxmoxBaseModel):
    """Model for list_updates. List available updates. response."""
    arch: StrictStr | None = Field(None, alias="Arch", description='Package Architecture.')
    description: StrictStr | None = Field(None, alias="Description", description='Package description.')
    notify_status: StrictStr | None = Field(None, alias="NotifyStatus", description='Version for which PVE has already sent an update notification for.')
    old_version: StrictStr | None = Field(None, alias="OldVersion", description='Old version currently installed.')
    origin: StrictStr | None = Field(None, alias="Origin", description="Package origin, e.g., 'Proxmox' or 'Debian'.")
    package: StrictStr | None = Field(None, alias="Package", description='Package name.')
    priority: StrictStr | None = Field(None, alias="Priority", description='Package priority.')
    section: StrictStr | None = Field(None, alias="Section", description='Package section.')
    title: StrictStr | None = Field(None, alias="Title", description='Package title.')
    version: StrictStr | None = Field(None, alias="Version", description='New version to be updated to.')

class GetNodesNodeAptUpdateResponse(RootModel[list[GetNodesNodeAptUpdateResponseItem]]):
    """List of items. list_updates. List available updates. response."""
    root: list[GetNodesNodeAptUpdateResponseItem] = Field(...)

class PostNodesNodeAptUpdateRequest(ProxmoxBaseModel):
    """Model for update_database. This is used to resynchronize the package index files from their sources (apt-get update). request."""
    notify: bool | None = Field(None, description='Send notification about new packages.')
    quiet: bool | None = Field(None, description='Only produces output suitable for logging, omitting progress indicators.')

class PostNodesNodeAptUpdateResponse(RootModel[StrictStr]):
    """Model for update_database. This is used to resynchronize the package index files from their sources (apt-get update). response."""
    root: StrictStr = Field(...)

class GetNodesNodeAptVersionsResponseItem(ProxmoxBaseModel):
    """Model for versions. Get package information for important Proxmox packages. response."""
    arch: StrictStr | None = Field(None, alias="Arch", description='Package Architecture.')
    current_state: StrictStr | None = Field(None, alias="CurrentState", description='Current state of the package installed on the system.')
    description: StrictStr | None = Field(None, alias="Description", description='Package description.')
    manager_version: StrictStr | None = Field(None, alias="ManagerVersion", description='Version of the currently running pve-manager API server.')
    notify_status: StrictStr | None = Field(None, alias="NotifyStatus", description='Version for which PVE has already sent an update notification for.')
    old_version: StrictStr | None = Field(None, alias="OldVersion", description='Old version currently installed.')
    origin: StrictStr | None = Field(None, alias="Origin", description="Package origin, e.g., 'Proxmox' or 'Debian'.")
    package: StrictStr | None = Field(None, alias="Package", description='Package name.')
    priority: StrictStr | None = Field(None, alias="Priority", description='Package priority.')
    running_kernel: StrictStr | None = Field(None, alias="RunningKernel", description="Kernel release, only for package 'proxmox-ve'.")
    section: StrictStr | None = Field(None, alias="Section", description='Package section.')
    title: StrictStr | None = Field(None, alias="Title", description='Package title.')
    version: StrictStr | None = Field(None, alias="Version", description='New version to be updated to.')

class GetNodesNodeAptVersionsResponse(RootModel[list[GetNodesNodeAptVersionsResponseItem]]):
    """List of items. versions. Get package information for important Proxmox packages. response."""
    root: list[GetNodesNodeAptVersionsResponseItem] = Field(...)

class GetNodesNodeCapabilitiesResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Node capabilities index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCapabilitiesQemuResponse(RootModel[list[dict[str, object]]]):
    """Model for qemu_caps_index. QEMU capabilities index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCapabilitiesQemuCpuResponseItem(ProxmoxBaseModel):
    """Model for index. List all custom and default CPU models. response."""
    custom: bool | None = Field(None, description='True if this is a custom CPU model.')
    name: StrictStr | None = Field(None, description="Name of the CPU model. Identifies it for subsequent API calls. Prefixed with 'custom-' for custom models.")
    vendor: StrictStr | None = Field(None, description="CPU vendor visible to the guest when this model is selected. Vendor of 'reported-model' in case of custom models.")

class GetNodesNodeCapabilitiesQemuCpuResponse(RootModel[list[GetNodesNodeCapabilitiesQemuCpuResponseItem]]):
    """List of items. index. List all custom and default CPU models. response."""
    root: list[GetNodesNodeCapabilitiesQemuCpuResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem(ProxmoxBaseModel):
    """Model for index. List of available VM-specific CPU flags. response."""
    description: StrictStr | None = Field(None, description='Description of the CPU flag.')
    name: StrictStr | None = Field(None, description='Name of the CPU flag.')

class GetNodesNodeCapabilitiesQemuCpuFlagsResponse(RootModel[list[GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem]]):
    """List of items. index. List of available VM-specific CPU flags. response."""
    root: list[GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuMachinesResponseItem(ProxmoxBaseModel):
    """Model for types. Get available QEMU/KVM machine types. response."""
    changes: StrictStr | None = Field(None, description='Notable changes of a version, currently only set for +pveX versions.')
    id: StrictStr | None = Field(None, description='Full name of machine type and version.')
    type: StrictStr | None = Field(None, description='The machine type.')
    version: StrictStr | None = Field(None, description='The machine version.')

class GetNodesNodeCapabilitiesQemuMachinesResponse(RootModel[list[GetNodesNodeCapabilitiesQemuMachinesResponseItem]]):
    """List of items. types. Get available QEMU/KVM machine types. response."""
    root: list[GetNodesNodeCapabilitiesQemuMachinesResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuMigrationResponse(ProxmoxBaseModel):
    """Model for capabilities. Get node-specific QEMU migration capabilities of the node. Requires the 'Sys.Audit' permission on '/nodes/<node>'. response."""
    has_dbus_vmstate: bool = Field(..., alias="has-dbus-vmstate", description='Whether the host supports live-migrating additional VM state via the dbus-vmstate helper.')

class GetNodesNodeCephResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCephCfgResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCephCfgDbResponseItem(ProxmoxBaseModel):
    """Model for db. Get the Ceph configuration database. response."""
    can_update_at_runtime: bool | None = Field(None)
    level: StrictStr | None = Field(None)
    mask: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None)
    section: StrictStr | None = Field(None)
    value: StrictStr | None = Field(None)

class GetNodesNodeCephCfgDbResponse(RootModel[list[GetNodesNodeCephCfgDbResponseItem]]):
    """List of items. db. Get the Ceph configuration database. response."""
    root: list[GetNodesNodeCephCfgDbResponseItem] = Field(...)

class GetNodesNodeCephCfgRawResponse(RootModel[StrictStr]):
    """Model for raw. Get the Ceph configuration file. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephCfgValueResponse(RootModel[dict[str, object]]):
    """Model for value. Get configured values from either the config file or config DB. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeCephCmdSafetyResponse(ProxmoxBaseModel):
    """Model for cmd_safety. Heuristical check if it is safe to perform an action. response."""
    safe: bool = Field(..., description='If it is safe to run the command.')
    status: StrictStr | None = Field(None, description='Status message given by Ceph.')

class GetNodesNodeCephCrushResponse(RootModel[StrictStr]):
    """Model for crush. Get OSD crush map response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephFsResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index. response."""
    data_pool: StrictStr | None = Field(None, description='The name of the data pool.')
    metadata_pool: StrictStr | None = Field(None, description='The name of the metadata pool.')
    name: StrictStr | None = Field(None, description='The ceph filesystem name.')

class GetNodesNodeCephFsResponse(RootModel[list[GetNodesNodeCephFsResponseItem]]):
    """List of items. index. Directory index. response."""
    root: list[GetNodesNodeCephFsResponseItem] = Field(...)

class PostNodesNodeCephFsNameRequest(ProxmoxBaseModel):
    """Model for createfs. Create a Ceph filesystem request."""
    add_storage: bool | None = Field(None, alias="add-storage", description='Configure the created CephFS as storage for this cluster.')
    pg_num: int | None = Field(None, description='Number of placement groups for the backing data pool. The metadata pool will use a quarter of this.')

class PostNodesNodeCephFsNameResponse(RootModel[StrictStr]):
    """Model for createfs. Create a Ceph filesystem response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephInitRequest(ProxmoxBaseModel):
    """Model for init. Create initial ceph default configuration and setup symlinks. request."""
    cluster_network: StrictStr | None = Field(None, alias="cluster-network", description='Declare a separate cluster network, OSDs will routeheartbeat, object replication and recovery traffic over it')
    disable_cephx: bool | None = Field(None, description='Disable cephx authentication.\n\nWARNING: cephx is a security feature protecting against man-in-the-middle attacks. Only consider disabling cephx if your network is private!')
    min_size: int | None = Field(None, description='Minimum number of available replicas per object to allow I/O')
    network: StrictStr | None = Field(None, description='Use specific network for all ceph related traffic')
    pg_bits: int | None = Field(None, description='Placement group bits, used to specify the default number of placement groups.\n\nDepreacted. This setting was deprecated in recent Ceph versions.')
    size: int | None = Field(None, description='Targeted number of replicas per object')

class PostNodesNodeCephInitResponse(RootModel[None]):
    """Model for init. Create initial ceph default configuration and setup symlinks. response."""
    root: None = Field(...)

class GetNodesNodeCephLogResponseItem(ProxmoxBaseModel):
    """Model for log. Read ceph log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeCephLogResponse(RootModel[list[GetNodesNodeCephLogResponseItem]]):
    """List of items. log. Read ceph log response."""
    root: list[GetNodesNodeCephLogResponseItem] = Field(...)

class GetNodesNodeCephMdsResponseItem(ProxmoxBaseModel):
    """Model for index. MDS directory index. response."""
    addr: StrictStr | None = Field(None)
    host: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None, description='The name (ID) for the MDS')
    rank: int | None = Field(None)
    standby_replay: bool | None = Field(None, description='If true, the standby MDS is polling the active MDS for faster recovery (hot standby).')
    state: StrictStr | None = Field(None, description='State of the MDS')

class GetNodesNodeCephMdsResponse(RootModel[list[GetNodesNodeCephMdsResponseItem]]):
    """List of items. index. MDS directory index. response."""
    root: list[GetNodesNodeCephMdsResponseItem] = Field(...)

class DeleteNodesNodeCephMdsNameRequest(RootModel[dict[str, object]]):
    """Model for destroymds. Destroy Ceph Metadata Server request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeCephMdsNameResponse(RootModel[StrictStr]):
    """Model for destroymds. Destroy Ceph Metadata Server response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephMdsNameRequest(ProxmoxBaseModel):
    """Model for createmds. Create Ceph Metadata Server (MDS) request."""
    hotstandby: bool | None = Field(None, description='Determines whether a ceph-mds daemon should poll and replay the log of an active MDS. Faster switch on MDS failure, but needs more idle resources.')

class PostNodesNodeCephMdsNameResponse(RootModel[StrictStr]):
    """Model for createmds. Create Ceph Metadata Server (MDS) response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephMgrResponseItem(ProxmoxBaseModel):
    """Model for index. MGR directory index. response."""
    addr: StrictStr | None = Field(None)
    host: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None, description='The name (ID) for the MGR')
    state: StrictStr | None = Field(None, description='State of the MGR')

class GetNodesNodeCephMgrResponse(RootModel[list[GetNodesNodeCephMgrResponseItem]]):
    """List of items. index. MGR directory index. response."""
    root: list[GetNodesNodeCephMgrResponseItem] = Field(...)

class DeleteNodesNodeCephMgrIdRequest(RootModel[dict[str, object]]):
    """Model for destroymgr. Destroy Ceph Manager. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeCephMgrIdResponse(RootModel[StrictStr]):
    """Model for destroymgr. Destroy Ceph Manager. response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephMgrIdRequest(RootModel[dict[str, object]]):
    """Model for createmgr. Create Ceph Manager request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeCephMgrIdResponse(RootModel[StrictStr]):
    """Model for createmgr. Create Ceph Manager response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephMonResponseItem(ProxmoxBaseModel):
    """Model for listmon. Get Ceph monitor list. response."""
    addr: StrictStr | None = Field(None)
    ceph_version: StrictStr | None = Field(None)
    ceph_version_short: StrictStr | None = Field(None)
    direxists: StrictStr | None = Field(None)
    host: bool | None = Field(None)
    name: StrictStr | None = Field(None)
    quorum: bool | None = Field(None)
    rank: int | None = Field(None)
    service: int | None = Field(None)
    state: StrictStr | None = Field(None)

class GetNodesNodeCephMonResponse(RootModel[list[GetNodesNodeCephMonResponseItem]]):
    """List of items. listmon. Get Ceph monitor list. response."""
    root: list[GetNodesNodeCephMonResponseItem] = Field(...)

class DeleteNodesNodeCephMonMonidRequest(RootModel[dict[str, object]]):
    """Model for destroymon. Destroy Ceph Monitor and Manager. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeCephMonMonidResponse(RootModel[StrictStr]):
    """Model for destroymon. Destroy Ceph Monitor and Manager. response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephMonMonidRequest(ProxmoxBaseModel):
    """Model for createmon. Create Ceph Monitor and Manager request."""
    mon_address: StrictStr | None = Field(None, alias="mon-address", description='Overwrites autodetected monitor IP address(es). Must be in the public network(s) of Ceph.')

class PostNodesNodeCephMonMonidResponse(RootModel[StrictStr]):
    """Model for createmon. Create Ceph Monitor and Manager response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephOsdResponse(RootModel[dict[str, object]]):
    """Model for index. Get Ceph osd list/tree. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeCephOsdRequest(ProxmoxBaseModel):
    """Model for createosd. Create OSD request."""
    crush_device_class: StrictStr | None = Field(None, alias="crush-device-class", description='Set the device class of the OSD in crush.')
    db_dev: StrictStr | None = Field(None, description='Block device name for block.db.')
    db_dev_size: float | None = Field(None, description='Size in GiB for block.db.')
    dev: StrictStr = Field(..., description='Block device name.')
    encrypted: bool | None = Field(None, description='Enables encryption of the OSD.')
    osds_per_device: int | None = Field(None, alias="osds-per-device", description='OSD services per physical device. Only useful for fast NVMe devices"\n\t\t    ." to utilize their performance better.')
    wal_dev: StrictStr | None = Field(None, description='Block device name for block.wal.')
    wal_dev_size: float | None = Field(None, description='Size in GiB for block.wal.')

class PostNodesNodeCephOsdResponse(RootModel[StrictStr]):
    """Model for createosd. Create OSD response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeCephOsdOsdidRequest(ProxmoxBaseModel):
    """Model for destroyosd. Destroy OSD request."""
    cleanup: bool | None = Field(None, description='If set, we remove partition table entries.')

class DeleteNodesNodeCephOsdOsdidResponse(RootModel[StrictStr]):
    """Model for destroyosd. Destroy OSD response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephOsdOsdidResponse(RootModel[list[dict[str, object]]]):
    """Model for osdindex. OSD index. response."""
    root: list[dict[str, object]] = Field(...)

class PostNodesNodeCephOsdOsdidInRequest(RootModel[dict[str, object]]):
    """Model for in. ceph osd in request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeCephOsdOsdidInResponse(RootModel[None]):
    """Model for in. ceph osd in response."""
    root: None = Field(...)

class GetNodesNodeCephOsdOsdidLvInfoResponse(ProxmoxBaseModel):
    """Model for osdvolume. Get OSD volume details response."""
    creation_time: StrictStr = Field(..., description='Creation time as reported by `lvs`.')
    lv_name: StrictStr = Field(..., description='Name of the logical volume (LV).')
    lv_path: StrictStr = Field(..., description='Path to the logical volume (LV).')
    lv_size: int = Field(..., description='Size of the logical volume (LV).')
    lv_uuid: StrictStr = Field(..., description='UUID of the logical volume (LV).')
    vg_name: StrictStr = Field(..., description='Name of the volume group (VG).')

class GetNodesNodeCephOsdOsdidMetadataResponse(ProxmoxBaseModel):
    """Model for osddetails. Get OSD details response."""
    devices: list[dict[str, object]] = Field(..., description='Array containing data about devices')
    osd: dict[str, object] = Field(..., description='General information about the OSD')

class PostNodesNodeCephOsdOsdidOutRequest(RootModel[dict[str, object]]):
    """Model for out. ceph osd out request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeCephOsdOsdidOutResponse(RootModel[None]):
    """Model for out. ceph osd out response."""
    root: None = Field(...)

class PostNodesNodeCephOsdOsdidScrubRequest(ProxmoxBaseModel):
    """Model for scrub. Instruct the OSD to scrub. request."""
    deep: bool | None = Field(None, description='If set, instructs a deep scrub instead of a normal one.')

class PostNodesNodeCephOsdOsdidScrubResponse(RootModel[None]):
    """Model for scrub. Instruct the OSD to scrub. response."""
    root: None = Field(...)

class GetNodesNodeCephPoolResponseItem(ProxmoxBaseModel):
    """Model for lspools. List all pools and their settings (which are settable by the POST/PUT endpoints). response."""
    application_metadata: dict[str, object] | None = Field(None)
    autoscale_status: dict[str, object] | None = Field(None)
    bytes_used: int | None = Field(None)
    crush_rule: int | None = Field(None)
    crush_rule_name: StrictStr | None = Field(None)
    min_size: int | None = Field(None)
    percent_used: float | None = Field(None)
    pg_autoscale_mode: StrictStr | None = Field(None)
    pg_num: int | None = Field(None)
    pg_num_final: int | None = Field(None)
    pg_num_min: int | None = Field(None)
    pool: int | None = Field(None)
    pool_name: StrictStr | None = Field(None)
    size: int | None = Field(None)
    target_size: int | None = Field(None)
    target_size_ratio: float | None = Field(None)
    type: StrictStr | None = Field(None)

class GetNodesNodeCephPoolResponse(RootModel[list[GetNodesNodeCephPoolResponseItem]]):
    """List of items. lspools. List all pools and their settings (which are settable by the POST/PUT endpoints). response."""
    root: list[GetNodesNodeCephPoolResponseItem] = Field(...)

class PostNodesNodeCephPoolRequest(ProxmoxBaseModel):
    """Model for createpool. Create Ceph pool request."""
    add_storages: bool | None = Field(None, description='Configure VM and CT storage using the new pool.')
    application: StrictStr | None = Field(None, description='The application of the pool.')
    crush_rule: StrictStr | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    erasure_coding: StrictStr | None = Field(None, alias="erasure-coding", description="Create an erasure coded pool for RBD with an accompaning replicated pool for metadata storage. With EC, the common ceph options 'size', 'min_size' and 'crush_rule' parameters will be applied to the metadata pool.")
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    name: StrictStr = Field(..., description='The name of the pool. It must be unique.')
    pg_autoscale_mode: StrictStr | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    size: int | None = Field(None, description='Number of replicas per object')
    target_size: StrictStr | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')

class PostNodesNodeCephPoolResponse(RootModel[StrictStr]):
    """Model for createpool. Create Ceph pool response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeCephPoolNameRequest(ProxmoxBaseModel):
    """Model for destroypool. Destroy pool request."""
    force: bool | None = Field(None, description='If true, destroys pool even if in use')
    remove_ecprofile: bool | None = Field(None, description='Remove the erasure code profile. Defaults to true, if applicable.')
    remove_storages: bool | None = Field(None, description='Remove all pveceph-managed storages configured for this pool')

class DeleteNodesNodeCephPoolNameResponse(RootModel[StrictStr]):
    """Model for destroypool. Destroy pool response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephPoolNameResponse(RootModel[list[dict[str, object]]]):
    """Model for poolindex. Pool index. response."""
    root: list[dict[str, object]] = Field(...)

class PutNodesNodeCephPoolNameRequest(ProxmoxBaseModel):
    """Model for setpool. Change POOL settings request."""
    application: StrictStr | None = Field(None, description='The application of the pool.')
    crush_rule: StrictStr | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    pg_autoscale_mode: StrictStr | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    size: int | None = Field(None, description='Number of replicas per object')
    target_size: StrictStr | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')

class PutNodesNodeCephPoolNameResponse(RootModel[StrictStr]):
    """Model for setpool. Change POOL settings response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephPoolNameStatusResponse(ProxmoxBaseModel):
    """Model for getpool. Show the current pool status. response."""
    application: StrictStr | None = Field(None, description='The application of the pool.')
    application_list: list[object] | None = Field(None)
    autoscale_status: dict[str, object] | None = Field(None)
    crush_rule: StrictStr | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    fast_read: bool = Field(...)
    hashpspool: bool = Field(...)
    id: int = Field(...)
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    name: StrictStr = Field(..., description='The name of the pool. It must be unique.')
    nodeep_scrub: bool = Field(..., alias="nodeep-scrub")
    nodelete: bool = Field(...)
    nopgchange: bool = Field(...)
    noscrub: bool = Field(...)
    nosizechange: bool = Field(...)
    pg_autoscale_mode: StrictStr | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    pgp_num: int = Field(...)
    size: int | None = Field(None, description='Number of replicas per object')
    statistics: dict[str, object] | None = Field(None)
    target_size: StrictStr | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')
    use_gmt_hitset: bool = Field(...)
    write_fadvise_dontneed: bool = Field(...)

class PostNodesNodeCephRestartRequest(ProxmoxBaseModel):
    """Model for restart. Restart ceph services. request."""
    service: StrictStr | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephRestartResponse(RootModel[StrictStr]):
    """Model for restart. Restart ceph services. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephRulesResponseItem(ProxmoxBaseModel):
    """Model for rules. List ceph rules. response."""
    name: StrictStr | None = Field(None, description='Name of the CRUSH rule.')

class GetNodesNodeCephRulesResponse(RootModel[list[GetNodesNodeCephRulesResponseItem]]):
    """List of items. rules. List ceph rules. response."""
    root: list[GetNodesNodeCephRulesResponseItem] = Field(...)

class PostNodesNodeCephStartRequest(ProxmoxBaseModel):
    """Model for start. Start ceph services. request."""
    service: StrictStr | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephStartResponse(RootModel[StrictStr]):
    """Model for start. Start ceph services. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephStatusResponse(RootModel[dict[str, object]]):
    """Model for status. Get ceph status. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeCephStopRequest(ProxmoxBaseModel):
    """Model for stop. Stop ceph services. request."""
    service: StrictStr | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephStopResponse(RootModel[StrictStr]):
    """Model for stop. Stop ceph services. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCertificatesResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Node index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCertificatesAcmeResponse(RootModel[list[dict[str, object]]]):
    """Model for index. ACME index. response."""
    root: list[dict[str, object]] = Field(...)

class DeleteNodesNodeCertificatesAcmeCertificateRequest(RootModel[dict[str, object]]):
    """Model for revoke_certificate. Revoke existing certificate from CA. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeCertificatesAcmeCertificateResponse(RootModel[StrictStr]):
    """Model for revoke_certificate. Revoke existing certificate from CA. response."""
    root: StrictStr = Field(...)

class PostNodesNodeCertificatesAcmeCertificateRequest(ProxmoxBaseModel):
    """Model for new_certificate. Order a new certificate from ACME-compatible CA. request."""
    force: bool | None = Field(None, description='Overwrite existing custom certificate.')

class PostNodesNodeCertificatesAcmeCertificateResponse(RootModel[StrictStr]):
    """Model for new_certificate. Order a new certificate from ACME-compatible CA. response."""
    root: StrictStr = Field(...)

class PutNodesNodeCertificatesAcmeCertificateRequest(ProxmoxBaseModel):
    """Model for renew_certificate. Renew existing certificate from CA. request."""
    force: bool | None = Field(None, description='Force renewal even if expiry is more than 30 days away.')

class PutNodesNodeCertificatesAcmeCertificateResponse(RootModel[StrictStr]):
    """Model for renew_certificate. Renew existing certificate from CA. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeCertificatesCustomRequest(ProxmoxBaseModel):
    """Model for remove_custom_cert. DELETE custom certificate chain and key. request."""
    restart: bool | None = Field(None, description='Restart pveproxy.')

class DeleteNodesNodeCertificatesCustomResponse(RootModel[None]):
    """Model for remove_custom_cert. DELETE custom certificate chain and key. response."""
    root: None = Field(...)

class PostNodesNodeCertificatesCustomRequest(ProxmoxBaseModel):
    """Model for upload_custom_cert. Upload or update custom certificate chain and key. request."""
    certificates: StrictStr = Field(..., description='PEM encoded certificate (chain).')
    force: bool | None = Field(None, description='Overwrite existing custom or ACME certificate files.')
    key: StrictStr | None = Field(None, description='PEM encoded private key.')
    restart: bool | None = Field(None, description='Restart pveproxy.')

class PostNodesNodeCertificatesCustomResponse(ProxmoxBaseModel):
    """Model for upload_custom_cert. Upload or update custom certificate chain and key. response."""
    filename: StrictStr | None = Field(None)
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    issuer: StrictStr | None = Field(None, description='Certificate issuer name.')
    notafter: int | None = Field(None, description="Certificate's notAfter timestamp (UNIX epoch).")
    notbefore: int | None = Field(None, description="Certificate's notBefore timestamp (UNIX epoch).")
    pem: StrictStr | None = Field(None, description='Certificate in PEM format')
    public_key_bits: int | None = Field(None, alias="public-key-bits", description="Certificate's public key size")
    public_key_type: StrictStr | None = Field(None, alias="public-key-type", description="Certificate's public key algorithm")
    san: list[StrictStr] | None = Field(None, description="List of Certificate's SubjectAlternativeName entries.")
    subject: StrictStr | None = Field(None, description='Certificate subject name.')

class GetNodesNodeCertificatesInfoResponseItem(ProxmoxBaseModel):
    """Model for info. Get information about node's certificates. response."""
    filename: StrictStr | None = Field(None)
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    issuer: StrictStr | None = Field(None, description='Certificate issuer name.')
    notafter: int | None = Field(None, description="Certificate's notAfter timestamp (UNIX epoch).")
    notbefore: int | None = Field(None, description="Certificate's notBefore timestamp (UNIX epoch).")
    pem: StrictStr | None = Field(None, description='Certificate in PEM format')
    public_key_bits: int | None = Field(None, alias="public-key-bits", description="Certificate's public key size")
    public_key_type: StrictStr | None = Field(None, alias="public-key-type", description="Certificate's public key algorithm")
    san: list[StrictStr] | None = Field(None, description="List of Certificate's SubjectAlternativeName entries.")
    subject: StrictStr | None = Field(None, description='Certificate subject name.')

class GetNodesNodeCertificatesInfoResponse(RootModel[list[GetNodesNodeCertificatesInfoResponseItem]]):
    """List of items. info. Get information about node's certificates. response."""
    root: list[GetNodesNodeCertificatesInfoResponseItem] = Field(...)

class GetNodesNodeConfigResponse(ProxmoxBaseModel):
    """Model for get_config. Get node configuration options. response."""
    acme: StrictStr | None = Field(None, description='Node specific ACME settings.')
    acmedomain_n: StrictStr | None = Field(None, alias="acmedomain[n]", description='ACME domain and validation plugin')
    ballooning_target: int | None = Field(None, alias="ballooning-target", description='RAM usage target for ballooning (in percent of total memory)')
    description: StrictStr | None = Field(None, description='Description for the Node. Shown in the web-interface node notes panel. This is saved as comment inside the configuration file.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    startall_onboot_delay: int | None = Field(None, alias="startall-onboot-delay", description='Initial delay in seconds, before starting all the Virtual Guests with on-boot enabled.')
    wakeonlan: StrictStr | None = Field(None, description='Node specific wake on LAN settings.')

class PutNodesNodeConfigRequest(ProxmoxBaseModel):
    """Model for set_options. Set node configuration options. request."""
    acme: StrictStr | None = Field(None, description='Node specific ACME settings.')
    acmedomain_n: StrictStr | None = Field(None, alias="acmedomain[n]", description='ACME domain and validation plugin')
    ballooning_target: int | None = Field(None, alias="ballooning-target", description='RAM usage target for ballooning (in percent of total memory)')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description='Description for the Node. Shown in the web-interface node notes panel. This is saved as comment inside the configuration file.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    startall_onboot_delay: int | None = Field(None, alias="startall-onboot-delay", description='Initial delay in seconds, before starting all the Virtual Guests with on-boot enabled.')
    wakeonlan: StrictStr | None = Field(None, description='Node specific wake on LAN settings.')

class PutNodesNodeConfigResponse(RootModel[None]):
    """Model for set_options. Set node configuration options. response."""
    root: None = Field(...)

class GetNodesNodeDisksResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Node index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeDisksDirectoryResponseItem(ProxmoxBaseModel):
    """Model for index. PVE Managed Directory storages. response."""
    device: StrictStr | None = Field(None, description='The mounted device.')
    options: StrictStr | None = Field(None, description='The mount options.')
    path: StrictStr | None = Field(None, description='The mount path.')
    type: StrictStr | None = Field(None, description='The filesystem type.')
    unitfile: StrictStr | None = Field(None, description='The path of the mount unit.')

class GetNodesNodeDisksDirectoryResponse(RootModel[list[GetNodesNodeDisksDirectoryResponseItem]]):
    """List of items. index. PVE Managed Directory storages. response."""
    root: list[GetNodesNodeDisksDirectoryResponseItem] = Field(...)

class PostNodesNodeDisksDirectoryRequest(ProxmoxBaseModel):
    """Model for create. Create a Filesystem on an unused disk. Will be mounted under '/mnt/pve/NAME'. request."""
    add_storage: bool | None = Field(None, description='Configure storage using the directory.')
    device: StrictStr = Field(..., description='The block device you want to create the filesystem on.')
    filesystem: StrictStr | None = Field(None, description='The desired filesystem.')
    name: StrictStr = Field(..., description='The storage identifier.')

class PostNodesNodeDisksDirectoryResponse(RootModel[StrictStr]):
    """Model for create. Create a Filesystem on an unused disk. Will be mounted under '/mnt/pve/NAME'. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeDisksDirectoryNameRequest(ProxmoxBaseModel):
    """Model for delete. Unmounts the storage and removes the mount unit. request."""
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disk so it can be repurposed afterwards.')

class DeleteNodesNodeDisksDirectoryNameResponse(RootModel[StrictStr]):
    """Model for delete. Unmounts the storage and removes the mount unit. response."""
    root: StrictStr = Field(...)

class PostNodesNodeDisksInitgptRequest(ProxmoxBaseModel):
    """Model for initgpt. Initialize Disk with GPT request."""
    disk: StrictStr = Field(..., description='Block device name')
    uuid: StrictStr | None = Field(None, description='UUID for the GPT table')

class PostNodesNodeDisksInitgptResponse(RootModel[StrictStr]):
    """Model for initgpt. Initialize Disk with GPT response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksListResponseItem(ProxmoxBaseModel):
    """Model for list. List local disks. response."""
    devpath: StrictStr | None = Field(None, description='The device path')
    gpt: bool | None = Field(None)
    health: StrictStr | None = Field(None)
    model: StrictStr | None = Field(None)
    mounted: bool | None = Field(None)
    osdid: int | None = Field(None)
    osdid_list: list[int] | None = Field(None, alias="osdid-list")
    parent: StrictStr | None = Field(None, description='For partitions only. The device path of the disk the partition resides on.')
    serial: StrictStr | None = Field(None)
    size: int | None = Field(None)
    used: StrictStr | None = Field(None)
    vendor: StrictStr | None = Field(None)
    wwn: StrictStr | None = Field(None)

class GetNodesNodeDisksListResponse(RootModel[list[GetNodesNodeDisksListResponseItem]]):
    """List of items. list. List local disks. response."""
    root: list[GetNodesNodeDisksListResponseItem] = Field(...)

class GetNodesNodeDisksLvmResponse(ProxmoxBaseModel):
    """Model for index. List LVM Volume Groups response."""
    children: list[dict[str, object]] = Field(...)
    leaf: bool = Field(...)

class PostNodesNodeDisksLvmRequest(ProxmoxBaseModel):
    """Model for create. Create an LVM Volume Group request."""
    add_storage: bool | None = Field(None, description='Configure storage using the Volume Group')
    device: StrictStr = Field(..., description='The block device you want to create the volume group on')
    name: StrictStr = Field(..., description='The storage identifier.')

class PostNodesNodeDisksLvmResponse(RootModel[StrictStr]):
    """Model for create. Create an LVM Volume Group response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeDisksLvmNameRequest(ProxmoxBaseModel):
    """Model for delete. Remove an LVM Volume Group. request."""
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')

class DeleteNodesNodeDisksLvmNameResponse(RootModel[StrictStr]):
    """Model for delete. Remove an LVM Volume Group. response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksLvmthinResponseItem(ProxmoxBaseModel):
    """Model for index. List LVM thinpools response."""
    lv: StrictStr | None = Field(None, description='The name of the thinpool.')
    lv_size: int | None = Field(None, description='The size of the thinpool in bytes.')
    metadata_size: int | None = Field(None, description='The size of the metadata lv in bytes.')
    metadata_used: int | None = Field(None, description='The used bytes of the metadata lv.')
    used: int | None = Field(None, description='The used bytes of the thinpool.')
    vg: StrictStr | None = Field(None, description='The associated volume group.')

class GetNodesNodeDisksLvmthinResponse(RootModel[list[GetNodesNodeDisksLvmthinResponseItem]]):
    """List of items. index. List LVM thinpools response."""
    root: list[GetNodesNodeDisksLvmthinResponseItem] = Field(...)

class PostNodesNodeDisksLvmthinRequest(ProxmoxBaseModel):
    """Model for create. Create an LVM thinpool request."""
    add_storage: bool | None = Field(None, description='Configure storage using the thinpool.')
    device: StrictStr = Field(..., description='The block device you want to create the thinpool on.')
    name: StrictStr = Field(..., description='The storage identifier.')

class PostNodesNodeDisksLvmthinResponse(RootModel[StrictStr]):
    """Model for create. Create an LVM thinpool response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeDisksLvmthinNameRequest(ProxmoxBaseModel):
    """Model for delete. Remove an LVM thin pool. request."""
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')
    volume_group: StrictStr = Field(..., alias="volume-group", description='The storage identifier.')

class DeleteNodesNodeDisksLvmthinNameResponse(RootModel[StrictStr]):
    """Model for delete. Remove an LVM thin pool. response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksSmartResponse(ProxmoxBaseModel):
    """Model for smart. Get SMART Health of a disk. response."""
    attributes: list[object] | None = Field(None)
    health: StrictStr = Field(...)
    text: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class PutNodesNodeDisksWipediskRequest(ProxmoxBaseModel):
    """Model for wipe_disk. Wipe a disk or partition. request."""
    disk: StrictStr = Field(..., description='Block device name')

class PutNodesNodeDisksWipediskResponse(RootModel[StrictStr]):
    """Model for wipe_disk. Wipe a disk or partition. response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksZfsResponseItem(ProxmoxBaseModel):
    """Model for index. List Zpools. response."""
    alloc: int | None = Field(None)
    dedup: float | None = Field(None)
    frag: int | None = Field(None)
    free: int | None = Field(None)
    health: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None)
    size: int | None = Field(None)

class GetNodesNodeDisksZfsResponse(RootModel[list[GetNodesNodeDisksZfsResponseItem]]):
    """List of items. index. List Zpools. response."""
    root: list[GetNodesNodeDisksZfsResponseItem] = Field(...)

class PostNodesNodeDisksZfsRequest(ProxmoxBaseModel):
    """Model for create. Create a ZFS pool. request."""
    add_storage: bool | None = Field(None, description='Configure storage using the zpool.')
    ashift: int | None = Field(None, description='Pool sector size exponent.')
    compression: StrictStr | None = Field(None, description='The compression algorithm to use.')
    devices: StrictStr = Field(..., description='The block devices you want to create the zpool on.')
    draid_config: StrictStr | None = Field(None, alias="draid-config")
    name: StrictStr = Field(..., description='The storage identifier.')
    raidlevel: StrictStr = Field(..., description='The RAID level to use.')

class PostNodesNodeDisksZfsResponse(RootModel[StrictStr]):
    """Model for create. Create a ZFS pool. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeDisksZfsNameRequest(ProxmoxBaseModel):
    """Model for delete. Destroy a ZFS pool. request."""
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')

class DeleteNodesNodeDisksZfsNameResponse(RootModel[StrictStr]):
    """Model for delete. Destroy a ZFS pool. response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksZfsNameResponse(ProxmoxBaseModel):
    """Model for detail. Get details about a zpool. response."""
    action: StrictStr | None = Field(None, description='Information about the recommended action to fix the state.')
    children: list[dict[str, object]] = Field(..., description='The pool configuration information, including the vdevs for each section (e.g. spares, cache), may be nested.')
    errors: StrictStr = Field(..., description='Information about the errors on the zpool.')
    name: StrictStr = Field(..., description='The name of the zpool.')
    scan: StrictStr | None = Field(None, description='Information about the last/current scrub.')
    state: StrictStr = Field(..., description='The state of the zpool.')
    status: StrictStr | None = Field(None, description='Information about the state of the zpool.')

class GetNodesNodeDnsResponse(ProxmoxBaseModel):
    """Model for dns. Read DNS settings. response."""
    dns1: StrictStr | None = Field(None, description='First name server IP address.')
    dns2: StrictStr | None = Field(None, description='Second name server IP address.')
    dns3: StrictStr | None = Field(None, description='Third name server IP address.')
    search: StrictStr | None = Field(None, description='Search domain for host-name lookup.')

class PutNodesNodeDnsRequest(ProxmoxBaseModel):
    """Model for update_dns. Write DNS settings. request."""
    dns1: StrictStr | None = Field(None, description='First name server IP address.')
    dns2: StrictStr | None = Field(None, description='Second name server IP address.')
    dns3: StrictStr | None = Field(None, description='Third name server IP address.')
    search: StrictStr = Field(..., description='Search domain for host-name lookup.')

class PutNodesNodeDnsResponse(RootModel[None]):
    """Model for update_dns. Write DNS settings. response."""
    root: None = Field(...)

class PostNodesNodeExecuteRequest(ProxmoxBaseModel):
    """Model for execute. Execute multiple commands in order, root only. request."""
    commands: StrictStr = Field(..., description='JSON encoded array of commands.')

class PostNodesNodeExecuteResponse(RootModel[list[dict[str, object]]]):
    """Model for execute. Execute multiple commands in order, root only. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeFirewallResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeFirewallLogResponseItem(ProxmoxBaseModel):
    """Model for log. Read firewall log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeFirewallLogResponse(RootModel[list[GetNodesNodeFirewallLogResponseItem]]):
    """List of items. log. Read firewall log response."""
    root: list[GetNodesNodeFirewallLogResponseItem] = Field(...)

class GetNodesNodeFirewallOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get host firewall options. response."""
    enable: bool | None = Field(None, description='Enable host firewall rules.')
    log_level_forward: StrictStr | None = Field(None, description='Log level for forwarded traffic.')
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    log_nf_conntrack: bool | None = Field(None, description='Enable logging of conntrack information.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    nf_conntrack_allow_invalid: bool | None = Field(None, description='Allow invalid packets on connection tracking.')
    nf_conntrack_helpers: StrictStr | None = Field(None, description='Enable conntrack helpers for specific protocols. Supported protocols: amanda, ftp, irc, netbios-ns, pptp, sane, sip, snmp, tftp')
    nf_conntrack_max: int | None = Field(None, description='Maximum number of tracked connections.')
    nf_conntrack_tcp_timeout_established: int | None = Field(None, description='Conntrack established timeout.')
    nf_conntrack_tcp_timeout_syn_recv: int | None = Field(None, description='Conntrack syn recv timeout.')
    nftables: bool | None = Field(None, description='Enable nftables based firewall (tech preview)')
    nosmurfs: bool | None = Field(None, description='Enable SMURFS filter.')
    protection_synflood: bool | None = Field(None, description='Enable synflood protection')
    protection_synflood_burst: int | None = Field(None, description='Synflood protection rate burst by ip src.')
    protection_synflood_rate: int | None = Field(None, description='Synflood protection rate syn/sec by ip src.')
    smurf_log_level: StrictStr | None = Field(None, description='Log level for SMURFS filter.')
    tcp_flags_log_level: StrictStr | None = Field(None, description='Log level for illegal tcp flags filter.')
    tcpflags: bool | None = Field(None, description='Filter illegal combinations of TCP flags.')

class PutNodesNodeFirewallOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set Firewall options. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable host firewall rules.')
    log_level_forward: StrictStr | None = Field(None, description='Log level for forwarded traffic.')
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    log_nf_conntrack: bool | None = Field(None, description='Enable logging of conntrack information.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    nf_conntrack_allow_invalid: bool | None = Field(None, description='Allow invalid packets on connection tracking.')
    nf_conntrack_helpers: StrictStr | None = Field(None, description='Enable conntrack helpers for specific protocols. Supported protocols: amanda, ftp, irc, netbios-ns, pptp, sane, sip, snmp, tftp')
    nf_conntrack_max: int | None = Field(None, description='Maximum number of tracked connections.')
    nf_conntrack_tcp_timeout_established: int | None = Field(None, description='Conntrack established timeout.')
    nf_conntrack_tcp_timeout_syn_recv: int | None = Field(None, description='Conntrack syn recv timeout.')
    nftables: bool | None = Field(None, description='Enable nftables based firewall (tech preview)')
    nosmurfs: bool | None = Field(None, description='Enable SMURFS filter.')
    protection_synflood: bool | None = Field(None, description='Enable synflood protection')
    protection_synflood_burst: int | None = Field(None, description='Synflood protection rate burst by ip src.')
    protection_synflood_rate: int | None = Field(None, description='Synflood protection rate syn/sec by ip src.')
    smurf_log_level: StrictStr | None = Field(None, description='Log level for SMURFS filter.')
    tcp_flags_log_level: StrictStr | None = Field(None, description='Log level for illegal tcp flags filter.')
    tcpflags: bool | None = Field(None, description='Filter illegal combinations of TCP flags.')

class PutNodesNodeFirewallOptionsResponse(RootModel[None]):
    """Model for set_options. Set Firewall options. response."""
    root: None = Field(...)

class GetNodesNodeFirewallRulesResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetNodesNodeFirewallRulesResponse(RootModel[list[GetNodesNodeFirewallRulesResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetNodesNodeFirewallRulesResponseItem] = Field(...)

class PostNodesNodeFirewallRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostNodesNodeFirewallRulesResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteNodesNodeFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeFirewallRulesPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetNodesNodeFirewallRulesPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutNodesNodeFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutNodesNodeFirewallRulesPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class GetNodesNodeHardwareResponseItem(ProxmoxBaseModel):
    """Model for index. Index of hardware types response."""
    type: StrictStr | None = Field(None)

class GetNodesNodeHardwareResponse(RootModel[list[GetNodesNodeHardwareResponseItem]]):
    """List of items. index. Index of hardware types response."""
    root: list[GetNodesNodeHardwareResponseItem] = Field(...)

class GetNodesNodeHardwarePciResponseItem(ProxmoxBaseModel):
    """Model for pci_scan. List local PCI devices. response."""
    class_: StrictStr | None = Field(None, alias="class", description='The PCI Class of the device.')
    device: StrictStr | None = Field(None, description='The Device ID.')
    device_name: StrictStr | None = Field(None)
    id: StrictStr | None = Field(None, description='The PCI ID.')
    iommugroup: int | None = Field(None, description='The IOMMU group in which the device is in. If no IOMMU group is detected, it is set to -1.')
    mdev: bool | None = Field(None, description='If set, marks that the device is capable of creating mediated devices.')
    subsystem_device: StrictStr | None = Field(None, description='The Subsystem Device ID.')
    subsystem_device_name: StrictStr | None = Field(None)
    subsystem_vendor: StrictStr | None = Field(None, description='The Subsystem Vendor ID.')
    subsystem_vendor_name: StrictStr | None = Field(None)
    vendor: StrictStr | None = Field(None, description='The Vendor ID.')
    vendor_name: StrictStr | None = Field(None)

class GetNodesNodeHardwarePciResponse(RootModel[list[GetNodesNodeHardwarePciResponseItem]]):
    """List of items. pci_scan. List local PCI devices. response."""
    root: list[GetNodesNodeHardwarePciResponseItem] = Field(...)

class GetNodesNodeHardwarePciPciIdOrMappingResponseItem(ProxmoxBaseModel):
    """Model for pci_index. Index of available pci methods response."""
    method: StrictStr | None = Field(None)

class GetNodesNodeHardwarePciPciIdOrMappingResponse(RootModel[list[GetNodesNodeHardwarePciPciIdOrMappingResponseItem]]):
    """List of items. pci_index. Index of available pci methods response."""
    root: list[GetNodesNodeHardwarePciPciIdOrMappingResponseItem] = Field(...)

class GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem(ProxmoxBaseModel):
    """Model for mdevscan. List mediated device types for given PCI device. response."""
    available: int | None = Field(None, description='The number of still available instances of this type.')
    description: StrictStr | None = Field(None, description='Additional description of the type.')
    name: StrictStr | None = Field(None, description='A human readable name for the type.')
    type: StrictStr | None = Field(None, description='The name of the mdev type.')

class GetNodesNodeHardwarePciPciIdOrMappingMdevResponse(RootModel[list[GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem]]):
    """List of items. mdevscan. List mediated device types for given PCI device. response."""
    root: list[GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem] = Field(...)

class GetNodesNodeHardwareUsbResponseItem(ProxmoxBaseModel):
    """Model for usbscan. List local USB devices. response."""
    busnum: int | None = Field(None)
    class_: int | None = Field(None, alias="class")
    devnum: int | None = Field(None)
    level: int | None = Field(None)
    manufacturer: StrictStr | None = Field(None)
    port: int | None = Field(None)
    prodid: StrictStr | None = Field(None)
    product: StrictStr | None = Field(None)
    serial: StrictStr | None = Field(None)
    speed: StrictStr | None = Field(None)
    usbpath: StrictStr | None = Field(None)
    vendid: StrictStr | None = Field(None)

class GetNodesNodeHardwareUsbResponse(RootModel[list[GetNodesNodeHardwareUsbResponseItem]]):
    """List of items. usbscan. List local USB devices. response."""
    root: list[GetNodesNodeHardwareUsbResponseItem] = Field(...)

class GetNodesNodeHostsResponse(ProxmoxBaseModel):
    """Model for get_etc_hosts. Get the content of /etc/hosts. response."""
    data: StrictStr = Field(..., description='The content of /etc/hosts.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class PostNodesNodeHostsRequest(ProxmoxBaseModel):
    """Model for write_etc_hosts. Write /etc/hosts. request."""
    data: StrictStr = Field(..., description='The target content of /etc/hosts.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class PostNodesNodeHostsResponse(RootModel[None]):
    """Model for write_etc_hosts. Write /etc/hosts. response."""
    root: None = Field(...)

class GetNodesNodeJournalResponse(RootModel[list[StrictStr]]):
    """Model for journal. Read Journal response."""
    root: list[StrictStr] = Field(...)

class GetNodesNodeLxcResponseItem(ProxmoxBaseModel):
    """Model for vmlist. LXC container index (per node). response."""
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    disk: int | None = Field(None, description='Root disk image space-usage in bytes.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    lock: StrictStr | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk image size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    maxswap: int | None = Field(None, description='Maximum SWAP memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes.')
    name: StrictStr | None = Field(None, description='Container name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    status: StrictStr | None = Field(None, description='LXC Container status.')
    tags: StrictStr | None = Field(None, description='The current configured tags, if any.')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int | None = Field(None, description='The (unique) ID of the VM.')

class GetNodesNodeLxcResponse(RootModel[list[GetNodesNodeLxcResponseItem]]):
    """List of items. vmlist. LXC container index (per node). response."""
    root: list[GetNodesNodeLxcResponseItem] = Field(...)

class PostNodesNodeLxcRequest(ProxmoxBaseModel):
    """Model for create_vm. Create or restore a container. request."""
    arch: StrictStr | None = Field(None, description='OS architecture type.')
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    cmode: StrictStr | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    description: StrictStr | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: StrictStr | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    entrypoint: StrictStr | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: StrictStr | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: StrictStr | None = Field(None, description='Allow containers access to advanced features.')
    force: bool | None = Field(None, description='Allow to overwrite existing container.')
    ha_managed: bool | None = Field(None, alias="ha-managed", description='Add the CT as a HA resource after it was created.')
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: StrictStr | None = Field(None, description='Set a host name for the container.')
    ignore_unpack_errors: bool | None = Field(None, alias="ignore-unpack-errors", description='Ignore errors when extracting the template.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the container.')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: StrictStr | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: StrictStr | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostemplate: StrictStr = Field(..., description='The OS template or backup file.')
    ostype: StrictStr | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    password: StrictStr | None = Field(None, description='Sets root password inside container.')
    pool: StrictStr | None = Field(None, description='Add the VM to the specified pool.')
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    restore: bool | None = Field(None, description='Mark this as restore task.')
    rootfs: StrictStr | None = Field(None, description='Use volume as container root.')
    searchdomain: StrictStr | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    ssh_public_keys: StrictStr | None = Field(None, alias="ssh-public-keys", description='Setup public SSH keys (one key per line, OpenSSH format).')
    start: bool | None = Field(None, description='Start the CT after its creation finished successfully.')
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    storage: StrictStr | None = Field(None, description='Default Storage.')
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: StrictStr | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: StrictStr | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unique: bool | None = Field(None, description='Assign a unique random ethernet address.')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeLxcResponse(RootModel[StrictStr]):
    """Model for create_vm. Create or restore a container. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeLxcVmidRequest(ProxmoxBaseModel):
    """Model for destroy_vm. Destroy the container (also delete all uses files). request."""
    destroy_unreferenced_disks: bool | None = Field(None, alias="destroy-unreferenced-disks", description='If set, destroy additionally all disks with the VMID from all enabled storages which are not referenced in the config.')
    force: bool | None = Field(None, description='Force destroy, even if running.')
    purge: bool | None = Field(None, description='Remove container from all related configurations. For example, backup jobs, replication jobs or HA. Related ACLs and Firewall entries will *always* be removed.')

class DeleteNodesNodeLxcVmidResponse(RootModel[StrictStr]):
    """Model for destroy_vm. Destroy the container (also delete all uses files). response."""
    root: StrictStr = Field(...)

class GetNodesNodeLxcVmidResponseItem(ProxmoxBaseModel):
    """Model for vmdiridx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidResponse(RootModel[list[GetNodesNodeLxcVmidResponseItem]]):
    """List of items. vmdiridx. Directory index response."""
    root: list[GetNodesNodeLxcVmidResponseItem] = Field(...)

class PostNodesNodeLxcVmidCloneRequest(ProxmoxBaseModel):
    """Model for clone_vm. Create a container clone/copy request."""
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    description: StrictStr | None = Field(None, description='Description for the new CT.')
    full: bool | None = Field(None, description='Create a full copy of all disks. This is always done when you clone a normal CT. For CT templates, we try to create a linked clone by default.')
    hostname: StrictStr | None = Field(None, description='Set a hostname for the new CT.')
    newid: int = Field(..., description='VMID for the clone.')
    pool: StrictStr | None = Field(None, description='Add the new CT to the specified pool.')
    snapname: StrictStr | None = Field(None, description='The name of the snapshot.')
    storage: StrictStr | None = Field(None, description='Target storage for full clone.')
    target: StrictStr | None = Field(None, description='Target node. Only allowed if the original VM is on shared storage.')

class PostNodesNodeLxcVmidCloneResponse(RootModel[StrictStr]):
    """Model for clone_vm. Create a container clone/copy response."""
    root: StrictStr = Field(...)

class GetNodesNodeLxcVmidConfigResponse(ProxmoxBaseModel):
    """Model for vm_config. Get container configuration. response."""
    arch: StrictStr | None = Field(None, description='OS architecture type.')
    cmode: StrictStr | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    description: StrictStr | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: StrictStr | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    digest: StrictStr = Field(..., description='SHA1 digest of configuration file. This can be used to prevent concurrent modifications.')
    entrypoint: StrictStr | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: StrictStr | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: StrictStr | None = Field(None, description='Allow containers access to advanced features.')
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: StrictStr | None = Field(None, description='Set a host name for the container.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the container.')
    lxc: list[list[StrictStr]] | None = Field(None, description='Array of lxc low-level configurations ([[key1, value1], [key2, value2] ...]).')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: StrictStr | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: StrictStr | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    rootfs: StrictStr | None = Field(None, description='Use volume as container root.')
    searchdomain: StrictStr | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: StrictStr | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: StrictStr | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')

class PutNodesNodeLxcVmidConfigRequest(ProxmoxBaseModel):
    """Model for update_vm. Set container options. request."""
    arch: StrictStr | None = Field(None, description='OS architecture type.')
    cmode: StrictStr | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: StrictStr | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    entrypoint: StrictStr | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: StrictStr | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: StrictStr | None = Field(None, description='Allow containers access to advanced features.')
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: StrictStr | None = Field(None, description='Set a host name for the container.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the container.')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: StrictStr | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: StrictStr | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    revert: StrictStr | None = Field(None, description='Revert a pending change.')
    rootfs: StrictStr | None = Field(None, description='Use volume as container root.')
    searchdomain: StrictStr | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: StrictStr | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: StrictStr | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')

class PutNodesNodeLxcVmidConfigResponse(RootModel[None]):
    """Model for update_vm. Set container options. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFeatureResponse(ProxmoxBaseModel):
    """Model for vm_feature. Check if feature for virtual machine is available. response."""
    has_feature: bool = Field(..., alias="hasFeature")

class GetNodesNodeLxcVmidFirewallResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidFirewallAliasesResponseItem(ProxmoxBaseModel):
    """Model for get_aliases. List aliases response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidFirewallAliasesResponse(RootModel[list[GetNodesNodeLxcVmidFirewallAliasesResponseItem]]):
    """List of items. get_aliases. List aliases response."""
    root: list[GetNodesNodeLxcVmidFirewallAliasesResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallAliasesRequest(ProxmoxBaseModel):
    """Model for create_alias. Create IP or Network Alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    name: StrictStr = Field(..., description='Alias name.')

class PostNodesNodeLxcVmidFirewallAliasesResponse(RootModel[None]):
    """Model for create_alias. Create IP or Network Alias. response."""
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for remove_alias. Remove IP or Network alias. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[None]):
    """Model for remove_alias. Remove IP or Network alias. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[dict[str, object]]):
    """Model for read_alias. Read alias. response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for update_alias. Update IP or Network alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    rename: StrictStr | None = Field(None, description='Rename an existing alias.')

class PutNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[None]):
    """Model for update_alias. Update IP or Network alias. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetResponseItem(ProxmoxBaseModel):
    """Model for ipset_index. List IPSets response."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None, description='IP set name.')

class GetNodesNodeLxcVmidFirewallIpsetResponse(RootModel[list[GetNodesNodeLxcVmidFirewallIpsetResponseItem]]):
    """List of items. ipset_index. List IPSets response."""
    root: list[GetNodesNodeLxcVmidFirewallIpsetResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallIpsetRequest(ProxmoxBaseModel):
    """Model for create_ipset. Create new IPSet request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr = Field(..., description='IP set name.')
    rename: StrictStr | None = Field(None, description="Rename an existing IPSet. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing IPSet.")

class PostNodesNodeLxcVmidFirewallIpsetResponse(RootModel[None]):
    """Model for create_ipset. Create new IPSet response."""
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for delete_ipset. Delete IPSet request."""
    force: bool | None = Field(None, description='Delete all members of the IPSet, if there are any.')

class DeleteNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[None]):
    """Model for delete_ipset. Delete IPSet response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetNameResponseItem(ProxmoxBaseModel):
    """Model for get_ipset. List IPSet content response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class GetNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[list[GetNodesNodeLxcVmidFirewallIpsetNameResponseItem]]):
    """List of items. get_ipset. List IPSet content response."""
    root: list[GetNodesNodeLxcVmidFirewallIpsetNameResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for create_ip. Add IP or Network to IPSet. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    nomatch: bool | None = Field(None)

class PostNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[None]):
    """Model for create_ip. Add IP or Network to IPSet. response."""
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for remove_ip. Remove IP or Network from IPSet. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for remove_ip. Remove IP or Network from IPSet. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[dict[str, object]]):
    """Model for read_ip. Read IP or Network settings from IPSet. response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for update_ip. Update IP or Network settings request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class PutNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for update_ip. Update IP or Network settings response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallLogResponseItem(ProxmoxBaseModel):
    """Model for log. Read firewall log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeLxcVmidFirewallLogResponse(RootModel[list[GetNodesNodeLxcVmidFirewallLogResponseItem]]):
    """List of items. log. Read firewall log response."""
    root: list[GetNodesNodeLxcVmidFirewallLogResponseItem] = Field(...)

class GetNodesNodeLxcVmidFirewallOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get VM firewall options. response."""
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeLxcVmidFirewallOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set Firewall options. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeLxcVmidFirewallOptionsResponse(RootModel[None]):
    """Model for set_options. Set Firewall options. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallRefsResponseItem(ProxmoxBaseModel):
    """Model for refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    comment: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None)
    ref: StrictStr | None = Field(None)
    scope: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidFirewallRefsResponse(RootModel[list[GetNodesNodeLxcVmidFirewallRefsResponseItem]]):
    """List of items. refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    root: list[GetNodesNodeLxcVmidFirewallRefsResponseItem] = Field(...)

class GetNodesNodeLxcVmidFirewallRulesResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetNodesNodeLxcVmidFirewallRulesResponse(RootModel[list[GetNodesNodeLxcVmidFirewallRulesResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetNodesNodeLxcVmidFirewallRulesResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostNodesNodeLxcVmidFirewallRulesResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallRulesPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallRulesPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutNodesNodeLxcVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutNodesNodeLxcVmidFirewallRulesPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidInterfacesResponseItem(ProxmoxBaseModel):
    """Model for ip. Get IP addresses of the specified container interface. response."""
    hardware_address: StrictStr | None = Field(None, alias="hardware-address", description='The MAC address of the interface')
    hwaddr: StrictStr | None = Field(None, description='The MAC address of the interface')
    inet: StrictStr | None = Field(None, description='The IPv4 address of the interface')
    inet6: StrictStr | None = Field(None, description='The IPv6 address of the interface')
    ip_addresses: list[dict[str, object]] | None = Field(None, alias="ip-addresses", description='The addresses of the interface')
    name: StrictStr | None = Field(None, description='The name of the interface')

class GetNodesNodeLxcVmidInterfacesResponse(RootModel[list[GetNodesNodeLxcVmidInterfacesResponseItem]]):
    """List of items. ip. Get IP addresses of the specified container interface. response."""
    root: list[GetNodesNodeLxcVmidInterfacesResponseItem] = Field(...)

class GetNodesNodeLxcVmidMigrateResponse(ProxmoxBaseModel):
    """Model for migrate_vm_precondition. Get preconditions for migration. response."""
    allowed_nodes: list[StrictStr] | None = Field(None, alias="allowed-nodes", description='List of nodes allowed for migration.')
    dependent_ha_resources: list[StrictStr] | None = Field(None, alias="dependent-ha-resources", description='HA resources, which will be migrated to the same target node as the VM, because these are in positive affinity with the VM.')
    not_allowed_nodes: dict[str, object] | None = Field(None, alias="not-allowed-nodes", description='List of not allowed nodes with additional information.')
    running: bool = Field(..., description='Determines if the container is running.')

class PostNodesNodeLxcVmidMigrateRequest(ProxmoxBaseModel):
    """Model for migrate_vm. Migrate the container to another node. Creates a new migration task. request."""
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    online: bool | None = Field(None, description='Use online/live migration.')
    restart: bool | None = Field(None, description='Use restart migration')
    target: StrictStr = Field(..., description='Target node.')
    target_storage: StrictStr | None = Field(None, alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    timeout: int | None = Field(None, description='Timeout in seconds for shutdown for restart migration')

class PostNodesNodeLxcVmidMigrateResponse(RootModel[StrictStr]):
    """Model for migrate_vm. Migrate the container to another node. Creates a new migration task. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeLxcVmidMoveVolumeRequest(ProxmoxBaseModel):
    """Model for move_volume. Move a rootfs-/mp-volume to a different storage or to a different container. request."""
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original volume after successful copy. By default the original is kept as an unused volume entry.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 " .\n\t\t    "digest. This can be used to prevent concurrent modifications.')
    storage: StrictStr | None = Field(None, description='Target Storage.')
    target_digest: StrictStr | None = Field(None, alias="target-digest", description='Prevent changes if current configuration file of the target " .\n\t\t    "container has a different SHA1 digest. This can be used to prevent " .\n\t\t    "concurrent modifications.')
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')
    target_volume: StrictStr | None = Field(None, alias="target-volume", description='The config key the volume will be moved to. Default is the source volume key.')
    volume: StrictStr = Field(..., description='Volume which will be moved.')

class PostNodesNodeLxcVmidMoveVolumeResponse(RootModel[StrictStr]):
    """Model for move_volume. Move a rootfs-/mp-volume to a different storage or to a different container. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidMtunnelRequest(ProxmoxBaseModel):
    """Model for mtunnel. Migration tunnel endpoint - only for internal use by CT migration. request."""
    bridges: StrictStr | None = Field(None, description='List of network bridges to check availability. Will be checked again for actually used bridges during migration.')
    storages: StrictStr | None = Field(None, description='List of storages to check permission and availability. Will be checked again for all actually used storages during migration.')

class PostNodesNodeLxcVmidMtunnelResponse(ProxmoxBaseModel):
    """Model for mtunnel. Migration tunnel endpoint - only for internal use by CT migration. response."""
    socket: StrictStr = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)

class GetNodesNodeLxcVmidMtunnelwebsocketResponse(ProxmoxBaseModel):
    """Model for mtunnelwebsocket. Migration tunnel endpoint for websocket upgrade - only for internal use by VM migration. response."""
    port: StrictStr | None = Field(None)
    socket: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidPendingResponseItem(ProxmoxBaseModel):
    """Model for vm_pending. Get container configuration, including pending changes. response."""
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0.')
    key: StrictStr | None = Field(None, description='Configuration option name.')
    pending: StrictStr | None = Field(None, description='Pending value.')
    value: StrictStr | None = Field(None, description='Current value.')

class GetNodesNodeLxcVmidPendingResponse(RootModel[list[GetNodesNodeLxcVmidPendingResponseItem]]):
    """List of items. vm_pending. Get container configuration, including pending changes. response."""
    root: list[GetNodesNodeLxcVmidPendingResponseItem] = Field(...)

class PostNodesNodeLxcVmidRemoteMigrateRequest(ProxmoxBaseModel):
    """Model for remote_migrate_vm. Migrate the container to another cluster. Creates a new migration task. EXPERIMENTAL feature! request."""
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original CT and related data after successful migration. By default the original CT is kept on the source cluster in a stopped state.')
    online: bool | None = Field(None, description='Use online/live migration.')
    restart: bool | None = Field(None, description='Use restart migration')
    target_bridge: StrictStr = Field(..., alias="target-bridge", description="Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value '1' will map each source bridge to itself.")
    target_endpoint: StrictStr = Field(..., alias="target-endpoint", description='Remote target endpoint')
    target_storage: StrictStr = Field(..., alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')
    timeout: int | None = Field(None, description='Timeout in seconds for shutdown for restart migration')

class PostNodesNodeLxcVmidRemoteMigrateResponse(RootModel[StrictStr]):
    """Model for remote_migrate_vm. Migrate the container to another cluster. Creates a new migration task. EXPERIMENTAL feature! response."""
    root: StrictStr = Field(..., description='the task ID.')

class PutNodesNodeLxcVmidResizeRequest(ProxmoxBaseModel):
    """Model for resize_vm. Resize a container mount point. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: StrictStr = Field(..., description='The disk you want to resize.')
    size: StrictStr = Field(..., description="The new size. With the '+' sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.")

class PutNodesNodeLxcVmidResizeResponse(RootModel[StrictStr]):
    """Model for resize_vm. Resize a container mount point. response."""
    root: StrictStr = Field(..., description='the task ID.')

class GetNodesNodeLxcVmidRrdResponse(ProxmoxBaseModel):
    """Model for rrd. Read VM RRD statistics (returns PNG) response."""
    filename: StrictStr = Field(...)

class GetNodesNodeLxcVmidRrddataResponse(RootModel[list[dict[str, object]]]):
    """Model for rrddata. Read VM RRD statistics response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidSnapshotResponseItem(ProxmoxBaseModel):
    """Model for list. List all snapshots. response."""
    description: StrictStr | None = Field(None, description='Snapshot description.')
    name: StrictStr | None = Field(None, description="Snapshot identifier. Value 'current' identifies the current VM.")
    parent: StrictStr | None = Field(None, description='Parent snapshot identifier.')
    snaptime: int | None = Field(None, description='Snapshot creation time')

class GetNodesNodeLxcVmidSnapshotResponse(RootModel[list[GetNodesNodeLxcVmidSnapshotResponseItem]]):
    """List of items. list. List all snapshots. response."""
    root: list[GetNodesNodeLxcVmidSnapshotResponseItem] = Field(...)

class PostNodesNodeLxcVmidSnapshotRequest(ProxmoxBaseModel):
    """Model for snapshot. Snapshot a container. request."""
    description: StrictStr | None = Field(None, description='A textual description or comment.')
    snapname: StrictStr = Field(..., description='The name of the snapshot.')

class PostNodesNodeLxcVmidSnapshotResponse(RootModel[StrictStr]):
    """Model for snapshot. Snapshot a container. response."""
    root: StrictStr = Field(..., description='the task ID.')

class DeleteNodesNodeLxcVmidSnapshotSnapnameRequest(ProxmoxBaseModel):
    """Model for delsnapshot. Delete a LXC snapshot. request."""
    force: bool | None = Field(None, description='For removal from config file, even if removing disk snapshots fails.')

class DeleteNodesNodeLxcVmidSnapshotSnapnameResponse(RootModel[StrictStr]):
    """Model for delsnapshot. Delete a LXC snapshot. response."""
    root: StrictStr = Field(..., description='the task ID.')

class GetNodesNodeLxcVmidSnapshotSnapnameResponse(RootModel[list[dict[str, object]]]):
    """Model for snapshot_cmd_idx. None response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidSnapshotSnapnameConfigResponse(RootModel[dict[str, object]]):
    """Model for get_snapshot_config. Get snapshot configuration response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidSnapshotSnapnameConfigRequest(ProxmoxBaseModel):
    """Model for update_snapshot_config. Update snapshot metadata. request."""
    description: StrictStr | None = Field(None, description='A textual description or comment.')

class PutNodesNodeLxcVmidSnapshotSnapnameConfigResponse(RootModel[None]):
    """Model for update_snapshot_config. Update snapshot metadata. response."""
    root: None = Field(...)

class PostNodesNodeLxcVmidSnapshotSnapnameRollbackRequest(ProxmoxBaseModel):
    """Model for rollback. Rollback LXC state to specified snapshot. request."""
    start: bool | None = Field(None, description='Whether the container should get started after rolling back successfully')

class PostNodesNodeLxcVmidSnapshotSnapnameRollbackResponse(RootModel[StrictStr]):
    """Model for rollback. Rollback LXC state to specified snapshot. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeLxcVmidSpiceproxyRequest(ProxmoxBaseModel):
    """Model for spiceproxy. Returns a SPICE configuration to connect to the CT. request."""
    proxy: StrictStr | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeLxcVmidSpiceproxyResponse(ProxmoxBaseModel):
    """Model for spiceproxy. Returns a SPICE configuration to connect to the CT. response."""
    host: StrictStr = Field(...)
    password: StrictStr = Field(...)
    proxy: StrictStr = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: StrictStr = Field(...)

class GetNodesNodeLxcVmidStatusResponseItem(ProxmoxBaseModel):
    """Model for vmcmdidx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidStatusResponse(RootModel[list[GetNodesNodeLxcVmidStatusResponseItem]]):
    """List of items. vmcmdidx. Directory index response."""
    root: list[GetNodesNodeLxcVmidStatusResponseItem] = Field(...)

class GetNodesNodeLxcVmidStatusCurrentResponse(ProxmoxBaseModel):
    """Model for vm_status. Get virtual machine status. response."""
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    disk: int | None = Field(None, description='Root disk image space-usage in bytes.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    ha: dict[str, object] = Field(..., description='HA manager service status.')
    lock: StrictStr | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk image size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    maxswap: int | None = Field(None, description='Maximum SWAP memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes.')
    name: StrictStr | None = Field(None, description='Container name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    status: StrictStr = Field(..., description='LXC Container status.')
    tags: StrictStr | None = Field(None, description='The current configured tags, if any.')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeLxcVmidStatusRebootRequest(ProxmoxBaseModel):
    """Model for vm_reboot. Reboot the container by shutting it down, and starting it again. Applies pending changes. request."""
    timeout: int | None = Field(None, description='Wait maximal timeout seconds for the shutdown.')

class PostNodesNodeLxcVmidStatusRebootResponse(RootModel[StrictStr]):
    """Model for vm_reboot. Reboot the container by shutting it down, and starting it again. Applies pending changes. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusResumeRequest(RootModel[dict[str, object]]):
    """Model for vm_resume. Resume the container. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeLxcVmidStatusResumeResponse(RootModel[StrictStr]):
    """Model for vm_resume. Resume the container. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusShutdownRequest(ProxmoxBaseModel):
    """Model for vm_shutdown. Shutdown the container. This will trigger a clean shutdown of the container, see lxc-stop(1) for details. request."""
    force_stop: bool | None = Field(None, alias="forceStop", description='Make sure the Container stops.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeLxcVmidStatusShutdownResponse(RootModel[StrictStr]):
    """Model for vm_shutdown. Shutdown the container. This will trigger a clean shutdown of the container, see lxc-stop(1) for details. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusStartRequest(ProxmoxBaseModel):
    """Model for vm_start. Start the container. request."""
    debug: bool | None = Field(None, description='If set, enables very verbose debug log-level on start.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeLxcVmidStatusStartResponse(RootModel[StrictStr]):
    """Model for vm_start. Start the container. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusStopRequest(ProxmoxBaseModel):
    """Model for vm_stop. Stop the container. This will abruptly stop all processes running in the container. request."""
    overrule_shutdown: bool | None = Field(None, alias="overrule-shutdown", description="Try to abort active 'vzshutdown' tasks before stopping.")
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeLxcVmidStatusStopResponse(RootModel[StrictStr]):
    """Model for vm_stop. Stop the container. This will abruptly stop all processes running in the container. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusSuspendRequest(RootModel[dict[str, object]]):
    """Model for vm_suspend. Suspend the container. This is experimental. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeLxcVmidStatusSuspendResponse(RootModel[StrictStr]):
    """Model for vm_suspend. Suspend the container. This is experimental. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidTemplateRequest(RootModel[dict[str, object]]):
    """Model for template. Create a Template. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeLxcVmidTemplateResponse(RootModel[None]):
    """Model for template. Create a Template. response."""
    root: None = Field(...)

class PostNodesNodeLxcVmidTermproxyRequest(RootModel[dict[str, object]]):
    """Model for termproxy. Creates a TCP proxy connection. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeLxcVmidTermproxyResponse(ProxmoxBaseModel):
    """Model for termproxy. Creates a TCP proxy connection. response."""
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class PostNodesNodeLxcVmidVncproxyRequest(ProxmoxBaseModel):
    """Model for vncproxy. Creates a TCP VNC proxy connections. request."""
    height: int | None = Field(None, description='sets the height of the console in pixels.')
    websocket: bool | None = Field(None, description='use websocket instead of standard VNC.')
    width: int | None = Field(None, description='sets the width of the console in pixels.')

class PostNodesNodeLxcVmidVncproxyResponse(ProxmoxBaseModel):
    """Model for vncproxy. Creates a TCP VNC proxy connections. response."""
    cert: StrictStr = Field(...)
    password: StrictStr | None = Field(None, description="Password used for authentication within the VNC protocol. Consists of printable ASCII characters ('!' .. '~').")
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class GetNodesNodeLxcVmidVncwebsocketResponse(ProxmoxBaseModel):
    """Model for vncwebsocket. Opens a websocket for VNC traffic. response."""
    port: StrictStr = Field(...)

class PostNodesNodeMigrateallRequest(ProxmoxBaseModel):
    """Model for migrateall. Migrate all VMs and Containers. request."""
    max_workers: int | None = Field(None, alias="max-workers", description="Maximal number of parallel migration job. If not set, uses'max_workers' from datacenter.cfg. One of both must be set!")
    maxworkers: int | None = Field(None, description="Maximal number of parallel migration job. If not set, uses'max_workers' from datacenter.cfg. One of both must be set!Deprecated, use 'max-workers' instead.")
    target: StrictStr = Field(..., description='Target node.')
    vms: StrictStr | None = Field(None, description='Only consider Guests with these IDs.')
    with_local_disks: bool | None = Field(None, alias="with-local-disks", description='Enable live storage migration for local disk')

class PostNodesNodeMigrateallResponse(RootModel[StrictStr]):
    """Model for migrateall. Migrate all VMs and Containers. response."""
    root: StrictStr = Field(...)

class GetNodesNodeNetstatResponse(RootModel[list[dict[str, object]]]):
    """Model for netstat. Read tap/vm network device interface counters response."""
    root: list[dict[str, object]] = Field(...)

class DeleteNodesNodeNetworkRequest(RootModel[dict[str, object]]):
    """Model for revert_network_changes. Revert network configuration changes. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeNetworkResponse(RootModel[None]):
    """Model for revert_network_changes. Revert network configuration changes. response."""
    root: None = Field(...)

class GetNodesNodeNetworkResponseItem(ProxmoxBaseModel):
    """Model for index. List available networks response."""
    active: bool | None = Field(None, description='Set to true if the interface is active.')
    address: StrictStr | None = Field(None, description='IP address.')
    address6: StrictStr | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: StrictStr | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: StrictStr | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: StrictStr | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_access: int | None = Field(None, alias="bridge-access", description='The bridge port access VLAN.')
    bridge_arp_nd_suppress: bool | None = Field(None, alias="bridge-arp-nd-suppress", description='Bridge port ARP/ND suppress flag.')
    bridge_learning: bool | None = Field(None, alias="bridge-learning", description='Bridge port learning flag.')
    bridge_multicast_flood: bool | None = Field(None, alias="bridge-multicast-flood", description='Bridge port multicast flood flag.')
    bridge_unicast_flood: bool | None = Field(None, alias="bridge-unicast-flood", description='Bridge port unicast flood flag.')
    bridge_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: StrictStr | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: StrictStr | None = Field(None, description='IPv4 CIDR.')
    cidr6: StrictStr | None = Field(None, description='IPv6 CIDR.')
    comments: StrictStr | None = Field(None, description='Comments')
    comments6: StrictStr | None = Field(None, description='Comments')
    exists: bool | None = Field(None, description='Set to true if the interface physically exists.')
    families: list[StrictStr] | None = Field(None, description='The network families.')
    gateway: StrictStr | None = Field(None, description='Default gateway address.')
    gateway6: StrictStr | None = Field(None, description='Default ipv6 gateway address.')
    iface: StrictStr | None = Field(None, description='Network interface name.')
    link_type: StrictStr | None = Field(None, alias="link-type", description='The link type.')
    method: StrictStr | None = Field(None, description='The network configuration method for IPv4.')
    method6: StrictStr | None = Field(None, description='The network configuration method for IPv6.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: StrictStr | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    options: list[StrictStr] | None = Field(None, description='A list of additional interface options for IPv4.')
    options6: list[StrictStr] | None = Field(None, description='A list of additional interface options for IPv6.')
    ovs_bonds: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: StrictStr | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: StrictStr | None = Field(None, description='OVS interface options.')
    ovs_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    priority: int | None = Field(None, description='The order of the interface.')
    slaves: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: StrictStr | None = Field(None, description='Network interface type')
    uplink_id: StrictStr | None = Field(None, alias="uplink-id", description='The uplink ID.')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_protocol: StrictStr | None = Field(None, alias="vlan-protocol", description='The VLAN protocol.')
    vlan_raw_device: StrictStr | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')
    vxlan_id: int | None = Field(None, alias="vxlan-id", description='The VXLAN ID.')
    vxlan_local_tunnelip: StrictStr | None = Field(None, alias="vxlan-local-tunnelip", description='The VXLAN local tunnel IP.')
    vxlan_physdev: StrictStr | None = Field(None, alias="vxlan-physdev", description='The physical device for the VXLAN tunnel.')
    vxlan_svcnodeip: StrictStr | None = Field(None, alias="vxlan-svcnodeip", description='The VXLAN SVC node IP.')

class GetNodesNodeNetworkResponse(RootModel[list[GetNodesNodeNetworkResponseItem]]):
    """List of items. index. List available networks response."""
    root: list[GetNodesNodeNetworkResponseItem] = Field(...)

class PostNodesNodeNetworkRequest(ProxmoxBaseModel):
    """Model for create_network. Create network device configuration request."""
    address: StrictStr | None = Field(None, description='IP address.')
    address6: StrictStr | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: StrictStr | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: StrictStr | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: StrictStr | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: StrictStr | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: StrictStr | None = Field(None, description='IPv4 CIDR.')
    cidr6: StrictStr | None = Field(None, description='IPv6 CIDR.')
    comments: StrictStr | None = Field(None, description='Comments')
    comments6: StrictStr | None = Field(None, description='Comments')
    gateway: StrictStr | None = Field(None, description='Default gateway address.')
    gateway6: StrictStr | None = Field(None, description='Default ipv6 gateway address.')
    iface: StrictStr = Field(..., description='Network interface name.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: StrictStr | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    ovs_bonds: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: StrictStr | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: StrictStr | None = Field(None, description='OVS interface options.')
    ovs_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    slaves: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: StrictStr = Field(..., description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_raw_device: StrictStr | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')

class PostNodesNodeNetworkResponse(RootModel[None]):
    """Model for create_network. Create network device configuration response."""
    root: None = Field(...)

class PutNodesNodeNetworkRequest(ProxmoxBaseModel):
    """Model for reload_network_config. Reload network configuration request."""
    regenerate_frr: bool | None = Field(None, alias="regenerate-frr", description='Whether FRR config generation should get skipped or not.')

class PutNodesNodeNetworkResponse(RootModel[StrictStr]):
    """Model for reload_network_config. Reload network configuration response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeNetworkIfaceRequest(RootModel[dict[str, object]]):
    """Model for delete_network. Delete network device configuration request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeNetworkIfaceResponse(RootModel[None]):
    """Model for delete_network. Delete network device configuration response."""
    root: None = Field(...)

class GetNodesNodeNetworkIfaceResponse(ProxmoxBaseModel):
    """Model for network_config. Read network device configuration response."""
    method: StrictStr = Field(...)
    type: StrictStr = Field(...)

class PutNodesNodeNetworkIfaceRequest(ProxmoxBaseModel):
    """Model for update_network. Update network device configuration request."""
    address: StrictStr | None = Field(None, description='IP address.')
    address6: StrictStr | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: StrictStr | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: StrictStr | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: StrictStr | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: StrictStr | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: StrictStr | None = Field(None, description='IPv4 CIDR.')
    cidr6: StrictStr | None = Field(None, description='IPv6 CIDR.')
    comments: StrictStr | None = Field(None, description='Comments')
    comments6: StrictStr | None = Field(None, description='Comments')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    gateway: StrictStr | None = Field(None, description='Default gateway address.')
    gateway6: StrictStr | None = Field(None, description='Default ipv6 gateway address.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: StrictStr | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    ovs_bonds: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: StrictStr | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: StrictStr | None = Field(None, description='OVS interface options.')
    ovs_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    slaves: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: StrictStr = Field(..., description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_raw_device: StrictStr | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')

class PutNodesNodeNetworkIfaceResponse(RootModel[None]):
    """Model for update_network. Update network device configuration response."""
    root: None = Field(...)

class GetNodesNodeQemuResponseItem(ProxmoxBaseModel):
    """Model for vmlist. Virtual machine index (per node). response."""
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    lock: StrictStr | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes. Does not take into account kernel same-page merging (KSM). Uses information from ballooning when available.')
    memhost: int | None = Field(None, description='Current memory usage on the host. Does not take into account kernel same-page merging (KSM).')
    name: StrictStr | None = Field(None, description='VM (host)name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pid: int | None = Field(None, description='PID of the QEMU process, if the VM is running.')
    pressurecpufull: float | None = Field(None, description='CPU Full pressure stall average over the last 10 seconds.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    qmpstatus: StrictStr | None = Field(None, description="VM run state from the 'query-status' QMP monitor command.")
    running_machine: StrictStr | None = Field(None, alias="running-machine", description='The currently running machine type (if running).')
    running_qemu: StrictStr | None = Field(None, alias="running-qemu", description='The QEMU version the VM is currently using (if running).')
    serial: bool | None = Field(None, description='Guest has serial device configured.')
    status: StrictStr | None = Field(None, description='QEMU process status.')
    tags: StrictStr | None = Field(None, description='The current configured tags, if any')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int | None = Field(None, description='The (unique) ID of the VM.')

class GetNodesNodeQemuResponse(RootModel[list[GetNodesNodeQemuResponseItem]]):
    """List of items. vmlist. Virtual machine index (per node). response."""
    root: list[GetNodesNodeQemuResponseItem] = Field(...)

class PostNodesNodeQemuRequest(ProxmoxBaseModel):
    """Model for create_vm. Create or restore a virtual machine. request."""
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: StrictStr | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: StrictStr | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: StrictStr | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: StrictStr | None = Field(None, description='Virtual processor architecture. Defaults to the host architecture.')
    archive: StrictStr | None = Field(None, description="The backup archive. Either the file system path to a .tar or .vma file (use '-' to pipe data from stdin) or a proxmox storage backup volume identifier.")
    args: StrictStr | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: StrictStr | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.')
    bios: StrictStr | None = Field(None, description='Select BIOS implementation.')
    boot: StrictStr | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: StrictStr | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    cdrom: StrictStr | None = Field(None, description='This is an alias for option -ide2')
    cicustom: StrictStr | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: StrictStr | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: StrictStr | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: StrictStr | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: StrictStr | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    description: StrictStr | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    efidisk0: StrictStr | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description='Allow to overwrite existing VM.')
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    ha_managed: bool | None = Field(None, alias="ha-managed", description='Add the VM as a HA resource after it was created.')
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: StrictStr | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: StrictStr | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: StrictStr | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: StrictStr | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    import_working_storage: StrictStr | None = Field(None, alias="import-working-storage", description="A file-based storage with 'images' content-type enabled, which is used as an intermediary extraction storage during import. Defaults to the source storage.")
    intel_tdx: StrictStr | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: StrictStr | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: StrictStr | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: StrictStr | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    live_restore: bool | None = Field(None, alias="live-restore", description='Start the VM immediately while importing or restoring in the background.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the VM.')
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    memory: StrictStr | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: StrictStr | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: StrictStr | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: StrictStr | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description='Specify guest operating system.')
    parallel_n: StrictStr | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    pool: StrictStr | None = Field(None, description='Add the VM to the specified pool.')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    rng0: StrictStr | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: StrictStr | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: StrictStr | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: StrictStr | None = Field(None, description='SCSI controller model')
    searchdomain: StrictStr | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: StrictStr | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    smbios1: StrictStr | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: StrictStr | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: StrictStr | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    start: bool | None = Field(None, description='Start VM after it was created successfully.')
    startdate: StrictStr | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    storage: StrictStr | None = Field(None, description='Default storage.')
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: StrictStr | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: StrictStr | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unique: bool | None = Field(None, description='Assign a unique random ethernet address.')
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: StrictStr | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: StrictStr | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: StrictStr | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: StrictStr | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: StrictStr | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmid: int = Field(..., description='The (unique) ID of the VM.')
    vmstatestorage: StrictStr | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: StrictStr | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuResponse(RootModel[StrictStr]):
    """Model for create_vm. Create or restore a virtual machine. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeQemuVmidRequest(ProxmoxBaseModel):
    """Model for destroy_vm. Destroy the VM and  all used/owned volumes. Removes any VM specific permissions and firewall rules request."""
    destroy_unreferenced_disks: bool | None = Field(None, alias="destroy-unreferenced-disks", description='If set, destroy additionally all disks not referenced in the config but with a matching VMID from all enabled storages.')
    purge: bool | None = Field(None, description='Remove VMID from configurations, like backup & replication jobs and HA.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class DeleteNodesNodeQemuVmidResponse(RootModel[StrictStr]):
    """Model for destroy_vm. Destroy the VM and  all used/owned volumes. Removes any VM specific permissions and firewall rules response."""
    root: StrictStr = Field(...)

class GetNodesNodeQemuVmidResponseItem(ProxmoxBaseModel):
    """Model for vmdiridx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidResponse(RootModel[list[GetNodesNodeQemuVmidResponseItem]]):
    """List of items. vmdiridx. Directory index response."""
    root: list[GetNodesNodeQemuVmidResponseItem] = Field(...)

class GetNodesNodeQemuVmidAgentResponse(RootModel[list[dict[str, object]]]):
    """Model for index. QEMU Guest Agent command index. response."""
    root: list[dict[str, object]] = Field(..., description='Returns the list of QEMU Guest Agent commands')

class PostNodesNodeQemuVmidAgentRequest(ProxmoxBaseModel):
    """Model for agent. Execute QEMU Guest Agent commands. request."""
    command: StrictStr = Field(..., description='The QGA command.')

class PostNodesNodeQemuVmidAgentResponse(RootModel[dict[str, object]]):
    """Model for agent. Execute QEMU Guest Agent commands. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentExecRequest(ProxmoxBaseModel):
    """Model for exec. Executes the given command in the vm via the guest-agent and returns an object with the pid. request."""
    command: list[StrictStr] = Field(..., description='The command as a list of program + arguments.')
    input_data: StrictStr | None = Field(None, alias="input-data", description="Data to pass as 'input-data' to the guest. Usually treated as STDIN to 'command'.")

class PostNodesNodeQemuVmidAgentExecResponse(ProxmoxBaseModel):
    """Model for exec. Executes the given command in the vm via the guest-agent and returns an object with the pid. response."""
    pid: int = Field(..., description='The PID of the process started by the guest-agent.')

class GetNodesNodeQemuVmidAgentExecStatusResponse(ProxmoxBaseModel):
    """Model for exec-status. Gets the status of the given pid started by the guest-agent response."""
    err_data: StrictStr | None = Field(None, alias="err-data", description='stderr of the process')
    err_truncated: bool | None = Field(None, alias="err-truncated", description='true if stderr was not fully captured')
    exitcode: int | None = Field(None, description='process exit code if it was normally terminated.')
    exited: bool = Field(..., description='Tells if the given command has exited yet.')
    out_data: StrictStr | None = Field(None, alias="out-data", description='stdout of the process')
    out_truncated: bool | None = Field(None, alias="out-truncated", description='true if stdout was not fully captured')
    signal: int | None = Field(None, description='signal number or exception code if the process was abnormally terminated.')

class GetNodesNodeQemuVmidAgentFileReadResponse(ProxmoxBaseModel):
    """Model for file-read. Reads the given file via guest agent. Is limited to 16777216 bytes. response."""
    content: StrictStr = Field(..., description='The content of the file, maximum 16777216')
    truncated: bool | None = Field(None, description='If set to 1, the read did not reach the end of the file.')

class PostNodesNodeQemuVmidAgentFileWriteRequest(ProxmoxBaseModel):
    """Model for file-write. Writes the given file via guest agent. request."""
    content: StrictStr = Field(..., description='The content to write into the file.')
    encode: bool | None = Field(None, description='If set, the content will be encoded as base64 (required by QEMU).Otherwise the content needs to be encoded beforehand - defaults to true.')
    file: StrictStr = Field(..., description='The path to the file.')

class PostNodesNodeQemuVmidAgentFileWriteResponse(RootModel[None]):
    """Model for file-write. Writes the given file via guest agent. response."""
    root: None = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeFreezeRequest(RootModel[dict[str, object]]):
    """Model for fsfreeze-freeze. Execute fsfreeze-freeze. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeFreezeResponse(RootModel[dict[str, object]]):
    """Model for fsfreeze-freeze. Execute fsfreeze-freeze. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeStatusRequest(RootModel[dict[str, object]]):
    """Model for fsfreeze-status. Execute fsfreeze-status. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeStatusResponse(RootModel[dict[str, object]]):
    """Model for fsfreeze-status. Execute fsfreeze-status. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeThawRequest(RootModel[dict[str, object]]):
    """Model for fsfreeze-thaw. Execute fsfreeze-thaw. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeThawResponse(RootModel[dict[str, object]]):
    """Model for fsfreeze-thaw. Execute fsfreeze-thaw. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFstrimRequest(RootModel[dict[str, object]]):
    """Model for fstrim. Execute fstrim. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFstrimResponse(RootModel[dict[str, object]]):
    """Model for fstrim. Execute fstrim. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetFsinfoResponse(RootModel[dict[str, object]]):
    """Model for get-fsinfo. Execute get-fsinfo. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetHostNameResponse(RootModel[dict[str, object]]):
    """Model for get-host-name. Execute get-host-name. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetMemoryBlockInfoResponse(RootModel[dict[str, object]]):
    """Model for get-memory-block-info. Execute get-memory-block-info. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetMemoryBlocksResponse(RootModel[dict[str, object]]):
    """Model for get-memory-blocks. Execute get-memory-blocks. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetOsinfoResponse(RootModel[dict[str, object]]):
    """Model for get-osinfo. Execute get-osinfo. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetTimeResponse(RootModel[dict[str, object]]):
    """Model for get-time. Execute get-time. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetTimezoneResponse(RootModel[dict[str, object]]):
    """Model for get-timezone. Execute get-timezone. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetUsersResponse(RootModel[dict[str, object]]):
    """Model for get-users. Execute get-users. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetVcpusResponse(RootModel[dict[str, object]]):
    """Model for get-vcpus. Execute get-vcpus. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentInfoResponse(RootModel[dict[str, object]]):
    """Model for info. Execute info. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentNetworkGetInterfacesResponse(RootModel[dict[str, object]]):
    """Model for network-get-interfaces. Execute network-get-interfaces. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentPingRequest(RootModel[dict[str, object]]):
    """Model for ping. Execute ping. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentPingResponse(RootModel[dict[str, object]]):
    """Model for ping. Execute ping. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSetUserPasswordRequest(ProxmoxBaseModel):
    """Model for set-user-password. Sets the password for the given user to the given password request."""
    crypted: bool | None = Field(None, description='set to 1 if the password has already been passed through crypt()')
    password: StrictStr = Field(..., description='The new password.')
    username: StrictStr = Field(..., description='The user to set the password for.')

class PostNodesNodeQemuVmidAgentSetUserPasswordResponse(RootModel[dict[str, object]]):
    """Model for set-user-password. Sets the password for the given user to the given password response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentShutdownRequest(RootModel[dict[str, object]]):
    """Model for shutdown. Execute shutdown. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentShutdownResponse(RootModel[dict[str, object]]):
    """Model for shutdown. Execute shutdown. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendDiskRequest(RootModel[dict[str, object]]):
    """Model for suspend-disk. Execute suspend-disk. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendDiskResponse(RootModel[dict[str, object]]):
    """Model for suspend-disk. Execute suspend-disk. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendHybridRequest(RootModel[dict[str, object]]):
    """Model for suspend-hybrid. Execute suspend-hybrid. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendHybridResponse(RootModel[dict[str, object]]):
    """Model for suspend-hybrid. Execute suspend-hybrid. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendRamRequest(RootModel[dict[str, object]]):
    """Model for suspend-ram. Execute suspend-ram. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendRamResponse(RootModel[dict[str, object]]):
    """Model for suspend-ram. Execute suspend-ram. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidCloneRequest(ProxmoxBaseModel):
    """Model for clone_vm. Create a copy of virtual machine/template. request."""
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    description: StrictStr | None = Field(None, description='Description for the new VM.')
    format: StrictStr | None = Field(None, description='Target format for file storage. Only valid for full clone.')
    full: bool | None = Field(None, description='Create a full copy of all disks. This is always done when you clone a normal VM. For VM templates, we try to create a linked clone by default.')
    name: StrictStr | None = Field(None, description='Set a name for the new VM.')
    newid: int = Field(..., description='VMID for the clone.')
    pool: StrictStr | None = Field(None, description='Add the new VM to the specified pool.')
    snapname: StrictStr | None = Field(None, description='The name of the snapshot.')
    storage: StrictStr | None = Field(None, description='Target storage for full clone.')
    target: StrictStr | None = Field(None, description='Target node. Only allowed if the original VM is on shared storage.')

class PostNodesNodeQemuVmidCloneResponse(RootModel[StrictStr]):
    """Model for clone_vm. Create a copy of virtual machine/template. response."""
    root: StrictStr = Field(...)

class GetNodesNodeQemuVmidCloudinitResponseItem(ProxmoxBaseModel):
    """Model for cloudinit_pending. Get the cloudinit configuration with both current and pending values. response."""
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0. ')
    key: StrictStr | None = Field(None, description='Configuration option name.')
    pending: StrictStr | None = Field(None, description='The new pending value.')
    value: StrictStr | None = Field(None, description='Value as it was used to generate the current cloudinit image.')

class GetNodesNodeQemuVmidCloudinitResponse(RootModel[list[GetNodesNodeQemuVmidCloudinitResponseItem]]):
    """List of items. cloudinit_pending. Get the cloudinit configuration with both current and pending values. response."""
    root: list[GetNodesNodeQemuVmidCloudinitResponseItem] = Field(...)

class PutNodesNodeQemuVmidCloudinitRequest(RootModel[dict[str, object]]):
    """Model for cloudinit_update. Regenerate and change cloudinit config drive. request."""
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidCloudinitResponse(RootModel[None]):
    """Model for cloudinit_update. Regenerate and change cloudinit config drive. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidCloudinitDumpResponse(RootModel[StrictStr]):
    """Model for cloudinit_generated_config_dump. Get automatically generated cloudinit config. response."""
    root: StrictStr = Field(...)

class GetNodesNodeQemuVmidConfigResponse(ProxmoxBaseModel):
    """Model for vm_config. Get the virtual machine configuration with pending configuration changes applied. Set the 'current' parameter to get the current configuration instead. response."""
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: StrictStr | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: StrictBool | Annotated[StrictInt, Field(ge=0, le=1)] | StrictStr | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: StrictStr | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: StrictStr | None = Field(None, description='Virtual processor architecture. Defaults to the host architecture.')
    args: StrictStr | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: StrictStr | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.')
    bios: StrictStr | None = Field(None, description='Select BIOS implementation.')
    boot: StrictStr | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: StrictStr | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: StrictStr | None = Field(None, description='This is an alias for option -ide2')
    cicustom: StrictStr | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: StrictStr | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: StrictStr | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: StrictStr | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: StrictStr | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    description: StrictStr | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: StrictStr = Field(..., description='SHA1 digest of configuration file. This can be used to prevent concurrent modifications.')
    efidisk0: StrictStr | None = Field(None, description='Configure a disk for storing EFI vars.')
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: StrictStr | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: StrictStr | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: StrictStr | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: StrictStr | None = Field(None, alias="ide[n]", description='Use volume as IDE hard disk or CD-ROM (n is 0 to 3).')
    intel_tdx: StrictStr | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: StrictStr | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: StrictStr | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: StrictStr | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the VM.')
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    memory: Annotated[StrictInt, Field(ge=16)] | StrictStr | None = Field(None, description='Memory properties.')
    meta: StrictStr | None = Field(None, description='Some (read-only) meta-information about this guest.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: StrictStr | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: StrictStr | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: StrictStr | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description='Specify guest operating system.')
    parallel_n: StrictStr | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    parent: StrictStr | None = Field(None, description='Parent snapshot name. This is used internally, and should not be modified.')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    rng0: StrictStr | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    running_nets_host_mtu: StrictStr | None = Field(None, alias="running-nets-host-mtu", description='List of VirtIO network devices and their effective host_mtu setting. A value of 0 means that the host_mtu parameter is to be avoided for the corresponding device. This is used internally for snapshots.')
    runningcpu: StrictStr | None = Field(None, description="Specifies the QEMU '-cpu' parameter of the running vm. This is used internally for snapshots.")
    runningmachine: StrictStr | None = Field(None, description='Specifies the QEMU machine type of the running vm. This is used internally for snapshots.')
    sata_n: StrictStr | None = Field(None, alias="sata[n]", description='Use volume as SATA hard disk or CD-ROM (n is 0 to 5).')
    scsi_n: StrictStr | None = Field(None, alias="scsi[n]", description='Use volume as SCSI hard disk or CD-ROM (n is 0 to 30).')
    scsihw: StrictStr | None = Field(None, description='SCSI controller model')
    searchdomain: StrictStr | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: StrictStr | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    smbios1: StrictStr | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    snaptime: int | None = Field(None, description='Timestamp for snapshots.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: StrictStr | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: StrictStr | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: StrictStr | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: StrictStr | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: StrictStr | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'.")
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: StrictStr | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: StrictStr | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: StrictStr | None = Field(None, alias="virtio[n]", description='Use volume as VIRTIO hard disk (n is 0 to 15).')
    virtiofs_n: StrictStr | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: StrictStr | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstate: StrictStr | None = Field(None, description='Reference to a volume which stores the VM state. This is used internally for snapshots.')
    vmstatestorage: StrictStr | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: StrictStr | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuVmidConfigRequest(ProxmoxBaseModel):
    """Model for update_vm_async. Set virtual machine options (asynchronous API). request."""
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: StrictStr | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: StrictStr | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: StrictStr | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: StrictStr | None = Field(None, description='Virtual processor architecture. Defaults to the host architecture.')
    args: StrictStr | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: StrictStr | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    background_delay: int | None = Field(None, description="Time to wait for the task to finish. We return 'null' if the task finish within that time.")
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.')
    bios: StrictStr | None = Field(None, description='Select BIOS implementation.')
    boot: StrictStr | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: StrictStr | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: StrictStr | None = Field(None, description='This is an alias for option -ide2')
    cicustom: StrictStr | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: StrictStr | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: StrictStr | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: StrictStr | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: StrictStr | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    efidisk0: StrictStr | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: StrictStr | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: StrictStr | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: StrictStr | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: StrictStr | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    import_working_storage: StrictStr | None = Field(None, alias="import-working-storage", description="A file-based storage with 'images' content-type enabled, which is used as an intermediary extraction storage during import. Defaults to the source storage.")
    intel_tdx: StrictStr | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: StrictStr | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: StrictStr | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: StrictStr | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the VM.')
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    memory: StrictStr | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: StrictStr | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: StrictStr | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: StrictStr | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description='Specify guest operating system.')
    parallel_n: StrictStr | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    revert: StrictStr | None = Field(None, description='Revert a pending change.')
    rng0: StrictStr | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: StrictStr | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: StrictStr | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: StrictStr | None = Field(None, description='SCSI controller model')
    searchdomain: StrictStr | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: StrictStr | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    smbios1: StrictStr | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: StrictStr | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: StrictStr | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: StrictStr | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: StrictStr | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: StrictStr | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: StrictStr | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: StrictStr | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: StrictStr | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: StrictStr | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: StrictStr | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstatestorage: StrictStr | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: StrictStr | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuVmidConfigResponse(RootModel[StrictStr]):
    """Model for update_vm_async. Set virtual machine options (asynchronous API). response."""
    root: StrictStr = Field(...)

class PutNodesNodeQemuVmidConfigRequest(ProxmoxBaseModel):
    """Model for update_vm. Set virtual machine options (synchronous API) - You should consider using the POST method instead for any actions involving hotplug or storage allocation. request."""
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: StrictStr | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: StrictStr | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: StrictStr | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: StrictStr | None = Field(None, description='Virtual processor architecture. Defaults to the host architecture.')
    args: StrictStr | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: StrictStr | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.')
    bios: StrictStr | None = Field(None, description='Select BIOS implementation.')
    boot: StrictStr | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: StrictStr | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: StrictStr | None = Field(None, description='This is an alias for option -ide2')
    cicustom: StrictStr | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: StrictStr | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: StrictStr | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: StrictStr | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: StrictStr | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    efidisk0: StrictStr | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: StrictStr | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: StrictStr | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: StrictStr | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: StrictStr | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    intel_tdx: StrictStr | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: StrictStr | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: StrictStr | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: StrictStr | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the VM.')
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    memory: StrictStr | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: StrictStr | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: StrictStr | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: StrictStr | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description='Specify guest operating system.')
    parallel_n: StrictStr | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    revert: StrictStr | None = Field(None, description='Revert a pending change.')
    rng0: StrictStr | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: StrictStr | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: StrictStr | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: StrictStr | None = Field(None, description='SCSI controller model')
    searchdomain: StrictStr | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: StrictStr | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    smbios1: StrictStr | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: StrictStr | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: StrictStr | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: StrictStr | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: StrictStr | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: StrictStr | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: StrictStr | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: StrictStr | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: StrictStr | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: StrictStr | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: StrictStr | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstatestorage: StrictStr | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: StrictStr | None = Field(None, description='Create a virtual hardware watchdog device.')

class PutNodesNodeQemuVmidConfigResponse(RootModel[None]):
    """Model for update_vm. Set virtual machine options (synchronous API) - You should consider using the POST method instead for any actions involving hotplug or storage allocation. response."""
    root: None = Field(...)

class PostNodesNodeQemuVmidDbusVmstateRequest(ProxmoxBaseModel):
    """Model for dbus_vmstate. Control the dbus-vmstate helper for a given running VM. request."""
    action: StrictStr = Field(..., description='Action to perform on the DBus VMState helper.')

class PostNodesNodeQemuVmidDbusVmstateResponse(RootModel[None]):
    """Model for dbus_vmstate. Control the dbus-vmstate helper for a given running VM. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFeatureResponse(ProxmoxBaseModel):
    """Model for vm_feature. Check if feature for virtual machine is available. response."""
    has_feature: bool = Field(..., alias="hasFeature")
    nodes: list[StrictStr] = Field(...)

class GetNodesNodeQemuVmidFirewallResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeQemuVmidFirewallAliasesResponseItem(ProxmoxBaseModel):
    """Model for get_aliases. List aliases response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidFirewallAliasesResponse(RootModel[list[GetNodesNodeQemuVmidFirewallAliasesResponseItem]]):
    """List of items. get_aliases. List aliases response."""
    root: list[GetNodesNodeQemuVmidFirewallAliasesResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallAliasesRequest(ProxmoxBaseModel):
    """Model for create_alias. Create IP or Network Alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    name: StrictStr = Field(..., description='Alias name.')

class PostNodesNodeQemuVmidFirewallAliasesResponse(RootModel[None]):
    """Model for create_alias. Create IP or Network Alias. response."""
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for remove_alias. Remove IP or Network alias. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[None]):
    """Model for remove_alias. Remove IP or Network alias. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[dict[str, object]]):
    """Model for read_alias. Read alias. response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for update_alias. Update IP or Network alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    rename: StrictStr | None = Field(None, description='Rename an existing alias.')

class PutNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[None]):
    """Model for update_alias. Update IP or Network alias. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetResponseItem(ProxmoxBaseModel):
    """Model for ipset_index. List IPSets response."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None, description='IP set name.')

class GetNodesNodeQemuVmidFirewallIpsetResponse(RootModel[list[GetNodesNodeQemuVmidFirewallIpsetResponseItem]]):
    """List of items. ipset_index. List IPSets response."""
    root: list[GetNodesNodeQemuVmidFirewallIpsetResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallIpsetRequest(ProxmoxBaseModel):
    """Model for create_ipset. Create new IPSet request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr = Field(..., description='IP set name.')
    rename: StrictStr | None = Field(None, description="Rename an existing IPSet. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing IPSet.")

class PostNodesNodeQemuVmidFirewallIpsetResponse(RootModel[None]):
    """Model for create_ipset. Create new IPSet response."""
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for delete_ipset. Delete IPSet request."""
    force: bool | None = Field(None, description='Delete all members of the IPSet, if there are any.')

class DeleteNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[None]):
    """Model for delete_ipset. Delete IPSet response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetNameResponseItem(ProxmoxBaseModel):
    """Model for get_ipset. List IPSet content response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class GetNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[list[GetNodesNodeQemuVmidFirewallIpsetNameResponseItem]]):
    """List of items. get_ipset. List IPSet content response."""
    root: list[GetNodesNodeQemuVmidFirewallIpsetNameResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for create_ip. Add IP or Network to IPSet. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    nomatch: bool | None = Field(None)

class PostNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[None]):
    """Model for create_ip. Add IP or Network to IPSet. response."""
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for remove_ip. Remove IP or Network from IPSet. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for remove_ip. Remove IP or Network from IPSet. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[dict[str, object]]):
    """Model for read_ip. Read IP or Network settings from IPSet. response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for update_ip. Update IP or Network settings request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class PutNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for update_ip. Update IP or Network settings response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallLogResponseItem(ProxmoxBaseModel):
    """Model for log. Read firewall log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeQemuVmidFirewallLogResponse(RootModel[list[GetNodesNodeQemuVmidFirewallLogResponseItem]]):
    """List of items. log. Read firewall log response."""
    root: list[GetNodesNodeQemuVmidFirewallLogResponseItem] = Field(...)

class GetNodesNodeQemuVmidFirewallOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get VM firewall options. response."""
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeQemuVmidFirewallOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set Firewall options. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeQemuVmidFirewallOptionsResponse(RootModel[None]):
    """Model for set_options. Set Firewall options. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallRefsResponseItem(ProxmoxBaseModel):
    """Model for refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    comment: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None)
    ref: StrictStr | None = Field(None)
    scope: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidFirewallRefsResponse(RootModel[list[GetNodesNodeQemuVmidFirewallRefsResponseItem]]):
    """List of items. refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    root: list[GetNodesNodeQemuVmidFirewallRefsResponseItem] = Field(...)

class GetNodesNodeQemuVmidFirewallRulesResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetNodesNodeQemuVmidFirewallRulesResponse(RootModel[list[GetNodesNodeQemuVmidFirewallRulesResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetNodesNodeQemuVmidFirewallRulesResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostNodesNodeQemuVmidFirewallRulesResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallRulesPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallRulesPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutNodesNodeQemuVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutNodesNodeQemuVmidFirewallRulesPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidMigrateResponse(ProxmoxBaseModel):
    """Model for migrate_vm_precondition. Get preconditions for migration. response."""
    allowed_nodes: list[StrictStr] | None = Field(None, description='List of nodes allowed for migration.')
    dependent_ha_resources: list[StrictStr] | None = Field(None, alias="dependent-ha-resources", description='HA resources, which will be migrated to the same target node as the VM, because these are in positive affinity with the VM.')
    has_dbus_vmstate: bool = Field(..., alias="has-dbus-vmstate", description='Whether the VM host supports migrating additional VM state, such as conntrack entries.')
    local_disks: list[dict[str, object]] = Field(..., description='List local disks including CD-Rom, unused and not referenced disks')
    local_resources: list[StrictStr] = Field(..., description='List local resources (e.g. pci, usb) that block migration.')
    mapped_resource_info: dict[str, object] = Field(..., alias="mapped-resource-info", description="Object of mapped resources with additional information such if they're live migratable.")
    mapped_resources: list[StrictStr] = Field(..., alias="mapped-resources", description="List of mapped resources e.g. pci, usb. Deprecated, use 'mapped-resource-info' instead.")
    not_allowed_nodes: dict[str, object] | None = Field(None, description='List of not allowed nodes with additional information.')
    running: bool = Field(..., description='Determines if the VM is running.')

class PostNodesNodeQemuVmidMigrateRequest(ProxmoxBaseModel):
    """Model for migrate_vm. Migrate virtual machine. Creates a new migration task. request."""
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    force: bool | None = Field(None, description='Allow to migrate VMs which use local devices. Only root may use this option.')
    migration_network: StrictStr | None = Field(None, description='CIDR of the (sub) network that is used for migration.')
    migration_type: StrictStr | None = Field(None, description='Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.')
    online: bool | None = Field(None, description='Use online/live migration if VM is running. Ignored if VM is stopped.')
    target: StrictStr = Field(..., description='Target node.')
    targetstorage: StrictStr | None = Field(None, description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    with_conntrack_state: bool | None = Field(None, alias="with-conntrack-state", description='Whether to migrate conntrack entries for running VMs.')
    with_local_disks: bool | None = Field(None, alias="with-local-disks", description='Enable live storage migration for local disk')

class PostNodesNodeQemuVmidMigrateResponse(RootModel[StrictStr]):
    """Model for migrate_vm. Migrate virtual machine. Creates a new migration task. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidMonitorRequest(ProxmoxBaseModel):
    """Model for monitor. Execute QEMU monitor commands. request."""
    command: StrictStr = Field(..., description='The monitor command.')

class PostNodesNodeQemuVmidMonitorResponse(RootModel[StrictStr]):
    """Model for monitor. Execute QEMU monitor commands. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidMoveDiskRequest(ProxmoxBaseModel):
    """Model for move_vm_disk. Move volume to different storage or to a different VM. request."""
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original disk after successful copy. By default the original disk is kept as unused disk.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: StrictStr = Field(..., description='The disk you want to move.')
    format: StrictStr | None = Field(None, description='Target Format.')
    storage: StrictStr | None = Field(None, description='Target storage.')
    target_digest: StrictStr | None = Field(None, alias="target-digest", description='Prevent changes if the current config file of the target VM has a different SHA1 digest. This can be used to detect concurrent modifications.')
    target_disk: StrictStr | None = Field(None, alias="target-disk", description='The config key the disk will be moved to on the target VM (for example, ide0 or scsi1). Default is the source disk key.')
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidMoveDiskResponse(RootModel[StrictStr]):
    """Model for move_vm_disk. Move volume to different storage or to a different VM. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidMtunnelRequest(ProxmoxBaseModel):
    """Model for mtunnel. Migration tunnel endpoint - only for internal use by VM migration. request."""
    bridges: StrictStr | None = Field(None, description='List of network bridges to check availability. Will be checked again for actually used bridges during migration.')
    storages: StrictStr | None = Field(None, description='List of storages to check permission and availability. Will be checked again for all actually used storages during migration.')

class PostNodesNodeQemuVmidMtunnelResponse(ProxmoxBaseModel):
    """Model for mtunnel. Migration tunnel endpoint - only for internal use by VM migration. response."""
    socket: StrictStr = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)

class GetNodesNodeQemuVmidMtunnelwebsocketResponse(ProxmoxBaseModel):
    """Model for mtunnelwebsocket. Migration tunnel endpoint for websocket upgrade - only for internal use by VM migration. response."""
    port: StrictStr | None = Field(None)
    socket: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidPendingResponseItem(ProxmoxBaseModel):
    """Model for vm_pending. Get the virtual machine configuration with both current and pending values. response."""
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0. The value 2 indicates a force-delete request.')
    key: StrictStr | None = Field(None, description='Configuration option name.')
    pending: StrictStr | None = Field(None, description='Pending value.')
    value: StrictStr | None = Field(None, description='Current value.')

class GetNodesNodeQemuVmidPendingResponse(RootModel[list[GetNodesNodeQemuVmidPendingResponseItem]]):
    """List of items. vm_pending. Get the virtual machine configuration with both current and pending values. response."""
    root: list[GetNodesNodeQemuVmidPendingResponseItem] = Field(...)

class PostNodesNodeQemuVmidRemoteMigrateRequest(ProxmoxBaseModel):
    """Model for remote_migrate_vm. Migrate virtual machine to a remote cluster. Creates a new migration task. EXPERIMENTAL feature! request."""
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original VM and related data after successful migration. By default the original VM is kept on the source cluster in a stopped state.')
    online: bool | None = Field(None, description='Use online/live migration if VM is running. Ignored if VM is stopped.')
    target_bridge: StrictStr = Field(..., alias="target-bridge", description="Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value '1' will map each source bridge to itself.")
    target_endpoint: StrictStr = Field(..., alias="target-endpoint", description='Remote target endpoint')
    target_storage: StrictStr = Field(..., alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidRemoteMigrateResponse(RootModel[StrictStr]):
    """Model for remote_migrate_vm. Migrate virtual machine to a remote cluster. Creates a new migration task. EXPERIMENTAL feature! response."""
    root: StrictStr = Field(..., description='the task ID.')

class PutNodesNodeQemuVmidResizeRequest(ProxmoxBaseModel):
    """Model for resize_vm. Extend volume size. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: StrictStr = Field(..., description='The disk you want to resize.')
    size: StrictStr = Field(..., description='The new size. With the `+` sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PutNodesNodeQemuVmidResizeResponse(RootModel[StrictStr]):
    """Model for resize_vm. Extend volume size. response."""
    root: StrictStr = Field(..., description='the task ID.')

class GetNodesNodeQemuVmidRrdResponse(ProxmoxBaseModel):
    """Model for rrd. Read VM RRD statistics (returns PNG) response."""
    filename: StrictStr = Field(...)

class GetNodesNodeQemuVmidRrddataResponse(RootModel[list[dict[str, object]]]):
    """Model for rrddata. Read VM RRD statistics response."""
    root: list[dict[str, object]] = Field(...)

class PutNodesNodeQemuVmidSendkeyRequest(ProxmoxBaseModel):
    """Model for vm_sendkey. Send key event to virtual machine. request."""
    key: StrictStr = Field(..., description='The key (qemu monitor encoding).')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PutNodesNodeQemuVmidSendkeyResponse(RootModel[None]):
    """Model for vm_sendkey. Send key event to virtual machine. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidSnapshotResponseItem(ProxmoxBaseModel):
    """Model for snapshot_list. List all snapshots. response."""
    description: StrictStr | None = Field(None, description='Snapshot description.')
    name: StrictStr | None = Field(None, description="Snapshot identifier. Value 'current' identifies the current VM.")
    parent: StrictStr | None = Field(None, description='Parent snapshot identifier.')
    snaptime: int | None = Field(None, description='Snapshot creation time')
    vmstate: bool | None = Field(None, description='Snapshot includes RAM.')

class GetNodesNodeQemuVmidSnapshotResponse(RootModel[list[GetNodesNodeQemuVmidSnapshotResponseItem]]):
    """List of items. snapshot_list. List all snapshots. response."""
    root: list[GetNodesNodeQemuVmidSnapshotResponseItem] = Field(...)

class PostNodesNodeQemuVmidSnapshotRequest(ProxmoxBaseModel):
    """Model for snapshot. Snapshot a VM. request."""
    description: StrictStr | None = Field(None, description='A textual description or comment.')
    snapname: StrictStr = Field(..., description='The name of the snapshot.')
    vmstate: bool | None = Field(None, description='Save the vmstate')

class PostNodesNodeQemuVmidSnapshotResponse(RootModel[StrictStr]):
    """Model for snapshot. Snapshot a VM. response."""
    root: StrictStr = Field(..., description='the task ID.')

class DeleteNodesNodeQemuVmidSnapshotSnapnameRequest(ProxmoxBaseModel):
    """Model for delsnapshot. Delete a VM snapshot. request."""
    force: bool | None = Field(None, description='For removal from config file, even if removing disk snapshots fails.')

class DeleteNodesNodeQemuVmidSnapshotSnapnameResponse(RootModel[StrictStr]):
    """Model for delsnapshot. Delete a VM snapshot. response."""
    root: StrictStr = Field(..., description='the task ID.')

class GetNodesNodeQemuVmidSnapshotSnapnameResponse(RootModel[list[dict[str, object]]]):
    """Model for snapshot_cmd_idx. None response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeQemuVmidSnapshotSnapnameConfigResponse(RootModel[dict[str, object]]):
    """Model for get_snapshot_config. Get snapshot configuration response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidSnapshotSnapnameConfigRequest(ProxmoxBaseModel):
    """Model for update_snapshot_config. Update snapshot metadata. request."""
    description: StrictStr | None = Field(None, description='A textual description or comment.')

class PutNodesNodeQemuVmidSnapshotSnapnameConfigResponse(RootModel[None]):
    """Model for update_snapshot_config. Update snapshot metadata. response."""
    root: None = Field(...)

class PostNodesNodeQemuVmidSnapshotSnapnameRollbackRequest(ProxmoxBaseModel):
    """Model for rollback. Rollback VM state to specified snapshot. request."""
    start: bool | None = Field(None, description='Whether the VM should get started after rolling back successfully. (Note: VMs will be automatically started if the snapshot includes RAM.)')

class PostNodesNodeQemuVmidSnapshotSnapnameRollbackResponse(RootModel[StrictStr]):
    """Model for rollback. Rollback VM state to specified snapshot. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidSpiceproxyRequest(ProxmoxBaseModel):
    """Model for spiceproxy. Returns a SPICE configuration to connect to the VM. request."""
    proxy: StrictStr | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeQemuVmidSpiceproxyResponse(ProxmoxBaseModel):
    """Model for spiceproxy. Returns a SPICE configuration to connect to the VM. response."""
    host: StrictStr = Field(...)
    password: StrictStr = Field(...)
    proxy: StrictStr = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: StrictStr = Field(...)

class GetNodesNodeQemuVmidStatusResponseItem(ProxmoxBaseModel):
    """Model for vmcmdidx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidStatusResponse(RootModel[list[GetNodesNodeQemuVmidStatusResponseItem]]):
    """List of items. vmcmdidx. Directory index response."""
    root: list[GetNodesNodeQemuVmidStatusResponseItem] = Field(...)

class GetNodesNodeQemuVmidStatusCurrentResponse(ProxmoxBaseModel):
    """Model for vm_status. Get virtual machine status. response."""
    agent: bool | None = Field(None, description='QEMU Guest Agent is enabled in config.')
    clipboard: StrictStr | None = Field(None, description='Enable a specific clipboard. If not set, depending on the display type the SPICE one will be added.')
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    ha: dict[str, object] = Field(..., description='HA manager service status.')
    lock: StrictStr | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes. Does not take into account kernel same-page merging (KSM). Uses information from ballooning when available.')
    memhost: int | None = Field(None, description='Current memory usage on the host. Does not take into account kernel same-page merging (KSM).')
    name: StrictStr | None = Field(None, description='VM (host)name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pid: int | None = Field(None, description='PID of the QEMU process, if the VM is running.')
    pressurecpufull: float | None = Field(None, description='CPU Full pressure stall average over the last 10 seconds.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    qmpstatus: StrictStr | None = Field(None, description="VM run state from the 'query-status' QMP monitor command.")
    running_machine: StrictStr | None = Field(None, alias="running-machine", description='The currently running machine type (if running).')
    running_qemu: StrictStr | None = Field(None, alias="running-qemu", description='The QEMU version the VM is currently using (if running).')
    serial: bool | None = Field(None, description='Guest has serial device configured.')
    spice: bool | None = Field(None, description='QEMU VGA configuration supports spice.')
    status: StrictStr = Field(..., description='QEMU process status.')
    tags: StrictStr | None = Field(None, description='The current configured tags, if any')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidStatusRebootRequest(ProxmoxBaseModel):
    """Model for vm_reboot. Reboot the VM by shutting it down, and starting it again. Applies pending changes. request."""
    timeout: int | None = Field(None, description='Wait maximal timeout seconds for the shutdown.')

class PostNodesNodeQemuVmidStatusRebootResponse(RootModel[StrictStr]):
    """Model for vm_reboot. Reboot the VM by shutting it down, and starting it again. Applies pending changes. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusResetRequest(ProxmoxBaseModel):
    """Model for vm_reset. Reset virtual machine. request."""
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeQemuVmidStatusResetResponse(RootModel[StrictStr]):
    """Model for vm_reset. Reset virtual machine. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusResumeRequest(ProxmoxBaseModel):
    """Model for vm_resume. Resume virtual machine. request."""
    nocheck: bool | None = Field(None)
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeQemuVmidStatusResumeResponse(RootModel[StrictStr]):
    """Model for vm_resume. Resume virtual machine. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusShutdownRequest(ProxmoxBaseModel):
    """Model for vm_shutdown. Shutdown virtual machine. This is similar to pressing the power button on a physical machine. This will send an ACPI event for the guest OS, which should then proceed to a clean shutdown. request."""
    force_stop: bool | None = Field(None, alias="forceStop", description='Make sure the VM stops.')
    keep_active: bool | None = Field(None, alias="keepActive", description='Do not deactivate storage volumes.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeQemuVmidStatusShutdownResponse(RootModel[StrictStr]):
    """Model for vm_shutdown. Shutdown virtual machine. This is similar to pressing the power button on a physical machine. This will send an ACPI event for the guest OS, which should then proceed to a clean shutdown. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusStartRequest(ProxmoxBaseModel):
    """Model for vm_start. Start virtual machine. request."""
    force_cpu: StrictStr | None = Field(None, alias="force-cpu", description="Override QEMU's -cpu argument with the given string.")
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    migratedfrom: StrictStr | None = Field(None, description='The cluster node name.')
    migration_network: StrictStr | None = Field(None, description='CIDR of the (sub) network that is used for migration.')
    migration_type: StrictStr | None = Field(None, description='Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.')
    nets_host_mtu: StrictStr | None = Field(None, alias="nets-host-mtu", description='Used for migration compat. List of VirtIO network devices and their effective host_mtu setting according to the QEMU object model on the source side of the migration. A value of 0 means that the host_mtu parameter is to be avoided for the corresponding device.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    stateuri: StrictStr | None = Field(None, description='Some command save/restore state from this location.')
    targetstorage: StrictStr | None = Field(None, description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')
    with_conntrack_state: bool | None = Field(None, alias="with-conntrack-state", description='Whether to migrate conntrack entries for running VMs.')

class PostNodesNodeQemuVmidStatusStartResponse(RootModel[StrictStr]):
    """Model for vm_start. Start virtual machine. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusStopRequest(ProxmoxBaseModel):
    """Model for vm_stop. Stop virtual machine. The qemu process will exit immediately. This is akin to pulling the power plug of a running computer and may damage the VM data. request."""
    keep_active: bool | None = Field(None, alias="keepActive", description='Do not deactivate storage volumes.')
    migratedfrom: StrictStr | None = Field(None, description='The cluster node name.')
    overrule_shutdown: bool | None = Field(None, alias="overrule-shutdown", description="Try to abort active 'qmshutdown' tasks before stopping.")
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeQemuVmidStatusStopResponse(RootModel[StrictStr]):
    """Model for vm_stop. Stop virtual machine. The qemu process will exit immediately. This is akin to pulling the power plug of a running computer and may damage the VM data. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusSuspendRequest(ProxmoxBaseModel):
    """Model for vm_suspend. Suspend virtual machine. request."""
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    statestorage: StrictStr | None = Field(None, description='The storage for the VM state')
    todisk: bool | None = Field(None, description='If set, suspends the VM to disk. Will be resumed on next VM start.')

class PostNodesNodeQemuVmidStatusSuspendResponse(RootModel[StrictStr]):
    """Model for vm_suspend. Suspend virtual machine. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidTemplateRequest(ProxmoxBaseModel):
    """Model for template. Create a Template. request."""
    disk: StrictStr | None = Field(None, description='If you want to convert only 1 disk to base image.')

class PostNodesNodeQemuVmidTemplateResponse(RootModel[StrictStr]):
    """Model for template. Create a Template. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidTermproxyRequest(ProxmoxBaseModel):
    """Model for termproxy. Creates a TCP proxy connections. request."""
    serial: StrictStr | None = Field(None, description='opens a serial terminal (defaults to display)')

class PostNodesNodeQemuVmidTermproxyResponse(ProxmoxBaseModel):
    """Model for termproxy. Creates a TCP proxy connections. response."""
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class PutNodesNodeQemuVmidUnlinkRequest(ProxmoxBaseModel):
    """Model for unlink. Unlink/delete disk images. request."""
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    idlist: StrictStr = Field(..., description='A list of disk IDs you want to delete.')

class PutNodesNodeQemuVmidUnlinkResponse(RootModel[None]):
    """Model for unlink. Unlink/delete disk images. response."""
    root: None = Field(...)

class PostNodesNodeQemuVmidVncproxyRequest(ProxmoxBaseModel):
    """Model for vncproxy. Creates a TCP VNC proxy connections. request."""
    generate_password: bool | None = Field(None, alias="generate-password", description='Deprecated, do not use. Password is generated when required.')
    websocket: bool | None = Field(None, description='Prepare for websocket upgrade (only required when using serial terminal, otherwise upgrade is always possible).')

class PostNodesNodeQemuVmidVncproxyResponse(ProxmoxBaseModel):
    """Model for vncproxy. Creates a TCP VNC proxy connections. response."""
    cert: StrictStr = Field(...)
    password: StrictStr | None = Field(None, description="Password used for authentication within the VNC protocol. Consists of printable ASCII characters ('!' .. '~').")
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class GetNodesNodeQemuVmidVncwebsocketResponse(ProxmoxBaseModel):
    """Model for vncwebsocket. Opens a websocket for VNC traffic. response."""
    port: StrictStr = Field(...)

class GetNodesNodeQueryOciRepoTagsResponse(RootModel[list[StrictStr]]):
    """Model for query_oci_repo_tags. List all tags for an OCI repository reference. response."""
    root: list[StrictStr] = Field(...)

class GetNodesNodeQueryUrlMetadataResponse(ProxmoxBaseModel):
    """Model for query_url_metadata. Query metadata of an URL: file size, file name and mime type. response."""
    filename: StrictStr | None = Field(None)
    mimetype: StrictStr | None = Field(None)
    size: int | None = Field(None)

class GetNodesNodeReplicationResponseItem(ProxmoxBaseModel):
    """Model for status. List status of all replication jobs on this node. response."""
    id: StrictStr | None = Field(None)

class GetNodesNodeReplicationResponse(RootModel[list[GetNodesNodeReplicationResponseItem]]):
    """List of items. status. List status of all replication jobs on this node. response."""
    root: list[GetNodesNodeReplicationResponseItem] = Field(...)

class GetNodesNodeReplicationIdResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeReplicationIdLogResponseItem(ProxmoxBaseModel):
    """Model for read_job_log. Read replication job log. response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeReplicationIdLogResponse(RootModel[list[GetNodesNodeReplicationIdLogResponseItem]]):
    """List of items. read_job_log. Read replication job log. response."""
    root: list[GetNodesNodeReplicationIdLogResponseItem] = Field(...)

class PostNodesNodeReplicationIdScheduleNowRequest(RootModel[dict[str, object]]):
    """Model for schedule_now. Schedule replication job to start as soon as possible. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeReplicationIdScheduleNowResponse(RootModel[StrictStr]):
    """Model for schedule_now. Schedule replication job to start as soon as possible. response."""
    root: StrictStr = Field(...)

class GetNodesNodeReplicationIdStatusResponse(RootModel[dict[str, object]]):
    """Model for job_status. Get replication job status. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeReportResponse(RootModel[StrictStr]):
    """Model for report. Gather various systems information about a node response."""
    root: StrictStr = Field(...)

class GetNodesNodeRrdResponse(ProxmoxBaseModel):
    """Model for rrd. Read node RRD statistics (returns PNG) response."""
    filename: StrictStr = Field(...)

class GetNodesNodeRrddataResponse(RootModel[list[dict[str, object]]]):
    """Model for rrddata. Read node RRD statistics response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeScanResponseItem(ProxmoxBaseModel):
    """Model for index. Index of available scan methods response."""
    method: StrictStr | None = Field(None)

class GetNodesNodeScanResponse(RootModel[list[GetNodesNodeScanResponseItem]]):
    """List of items. index. Index of available scan methods response."""
    root: list[GetNodesNodeScanResponseItem] = Field(...)

class GetNodesNodeScanCifsResponseItem(ProxmoxBaseModel):
    """Model for cifsscan. Scan remote CIFS server. response."""
    description: StrictStr | None = Field(None, description='Descriptive text from server.')
    share: StrictStr | None = Field(None, description='The cifs share name.')

class GetNodesNodeScanCifsResponse(RootModel[list[GetNodesNodeScanCifsResponseItem]]):
    """List of items. cifsscan. Scan remote CIFS server. response."""
    root: list[GetNodesNodeScanCifsResponseItem] = Field(...)

class GetNodesNodeScanIscsiResponseItem(ProxmoxBaseModel):
    """Model for iscsiscan. Scan remote iSCSI server. response."""
    portal: StrictStr | None = Field(None, description='The iSCSI portal name.')
    target: StrictStr | None = Field(None, description='The iSCSI target name.')

class GetNodesNodeScanIscsiResponse(RootModel[list[GetNodesNodeScanIscsiResponseItem]]):
    """List of items. iscsiscan. Scan remote iSCSI server. response."""
    root: list[GetNodesNodeScanIscsiResponseItem] = Field(...)

class GetNodesNodeScanLvmResponseItem(ProxmoxBaseModel):
    """Model for lvmscan. List local LVM volume groups. response."""
    vg: StrictStr | None = Field(None, description='The LVM logical volume group name.')

class GetNodesNodeScanLvmResponse(RootModel[list[GetNodesNodeScanLvmResponseItem]]):
    """List of items. lvmscan. List local LVM volume groups. response."""
    root: list[GetNodesNodeScanLvmResponseItem] = Field(...)

class GetNodesNodeScanLvmthinResponseItem(ProxmoxBaseModel):
    """Model for lvmthinscan. List local LVM Thin Pools. response."""
    lv: StrictStr | None = Field(None, description='The LVM Thin Pool name (LVM logical volume).')

class GetNodesNodeScanLvmthinResponse(RootModel[list[GetNodesNodeScanLvmthinResponseItem]]):
    """List of items. lvmthinscan. List local LVM Thin Pools. response."""
    root: list[GetNodesNodeScanLvmthinResponseItem] = Field(...)

class GetNodesNodeScanNfsResponseItem(ProxmoxBaseModel):
    """Model for nfsscan. Scan remote NFS server. response."""
    options: StrictStr | None = Field(None, description='NFS export options.')
    path: StrictStr | None = Field(None, description='The exported path.')

class GetNodesNodeScanNfsResponse(RootModel[list[GetNodesNodeScanNfsResponseItem]]):
    """List of items. nfsscan. Scan remote NFS server. response."""
    root: list[GetNodesNodeScanNfsResponseItem] = Field(...)

class GetNodesNodeScanPbsResponseItem(ProxmoxBaseModel):
    """Model for pbsscan. Scan remote Proxmox Backup Server. response."""
    comment: StrictStr | None = Field(None, description='Comment from server.')
    store: StrictStr | None = Field(None, description='The datastore name.')

class GetNodesNodeScanPbsResponse(RootModel[list[GetNodesNodeScanPbsResponseItem]]):
    """List of items. pbsscan. Scan remote Proxmox Backup Server. response."""
    root: list[GetNodesNodeScanPbsResponseItem] = Field(...)

class GetNodesNodeScanZfsResponseItem(ProxmoxBaseModel):
    """Model for zfsscan. Scan zfs pool list on local node. response."""
    pool: StrictStr | None = Field(None, description='ZFS pool name.')

class GetNodesNodeScanZfsResponse(RootModel[list[GetNodesNodeScanZfsResponseItem]]):
    """List of items. zfsscan. Scan zfs pool list on local node. response."""
    root: list[GetNodesNodeScanZfsResponseItem] = Field(...)

class GetNodesNodeSdnResponse(RootModel[list[dict[str, object]]]):
    """Model for sdnindex. SDN index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeSdnFabricsFabricResponseItem(ProxmoxBaseModel):
    """Model for diridx. Directory index for SDN fabric status. response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeSdnFabricsFabricResponse(RootModel[list[GetNodesNodeSdnFabricsFabricResponseItem]]):
    """List of items. diridx. Directory index for SDN fabric status. response."""
    root: list[GetNodesNodeSdnFabricsFabricResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricInterfacesResponseItem(ProxmoxBaseModel):
    """Model for interfaces. Get all interfaces for a fabric. response."""
    name: StrictStr | None = Field(None, description='The name of the network interface.')
    state: StrictStr | None = Field(None, description='The current state of the interface.')
    type: StrictStr | None = Field(None, description='The type of this interface in the fabric (e.g. Point-to-Point, Broadcast, ..).')

class GetNodesNodeSdnFabricsFabricInterfacesResponse(RootModel[list[GetNodesNodeSdnFabricsFabricInterfacesResponseItem]]):
    """List of items. interfaces. Get all interfaces for a fabric. response."""
    root: list[GetNodesNodeSdnFabricsFabricInterfacesResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricNeighborsResponseItem(ProxmoxBaseModel):
    """Model for neighbors. Get all neighbors for a fabric. response."""
    neighbor: StrictStr | None = Field(None, description='The IP or hostname of the neighbor.')
    status: StrictStr | None = Field(None, description='The status of the neighbor, as returned by FRR.')
    uptime: StrictStr | None = Field(None, description='The uptime of this neighbor, as returned by FRR (e.g. 8h24m12s).')

class GetNodesNodeSdnFabricsFabricNeighborsResponse(RootModel[list[GetNodesNodeSdnFabricsFabricNeighborsResponseItem]]):
    """List of items. neighbors. Get all neighbors for a fabric. response."""
    root: list[GetNodesNodeSdnFabricsFabricNeighborsResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricRoutesResponseItem(ProxmoxBaseModel):
    """Model for routes. Get all routes for a fabric. response."""
    route: StrictStr | None = Field(None, description='The CIDR block for this routing table entry.')
    via: list[StrictStr] | None = Field(None, description='A list of nexthops for that route.')

class GetNodesNodeSdnFabricsFabricRoutesResponse(RootModel[list[GetNodesNodeSdnFabricsFabricRoutesResponseItem]]):
    """List of items. routes. Get all routes for a fabric. response."""
    root: list[GetNodesNodeSdnFabricsFabricRoutesResponseItem] = Field(...)

class GetNodesNodeSdnVnetsVnetResponseItem(ProxmoxBaseModel):
    """Model for diridx. None response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeSdnVnetsVnetResponse(RootModel[list[GetNodesNodeSdnVnetsVnetResponseItem]]):
    """List of items. diridx. None response."""
    root: list[GetNodesNodeSdnVnetsVnetResponseItem] = Field(...)

class GetNodesNodeSdnVnetsVnetMacVrfResponseItem(ProxmoxBaseModel):
    """Model for mac-vrf. Get the MAC VRF for a VNet in an EVPN zone. response."""
    ip: StrictStr | None = Field(None, description='The IP address of the MAC VRF entry.')
    mac: StrictStr | None = Field(None, description='The MAC address of the MAC VRF entry.')
    nexthop: StrictStr | None = Field(None, description='The IP address of the nexthop.')

class GetNodesNodeSdnVnetsVnetMacVrfResponse(RootModel[list[GetNodesNodeSdnVnetsVnetMacVrfResponseItem]]):
    """List of items. mac-vrf. Get the MAC VRF for a VNet in an EVPN zone. response."""
    root: list[GetNodesNodeSdnVnetsVnetMacVrfResponseItem] = Field(..., description='All routes from the MAC VRF that this node self-originates or has learned via BGP.')

class GetNodesNodeSdnZonesResponseItem(ProxmoxBaseModel):
    """Model for index. Get status for all zones. response."""
    status: StrictStr | None = Field(None, description='Status of zone')
    zone: StrictStr | None = Field(None, description='The SDN zone object identifier.')

class GetNodesNodeSdnZonesResponse(RootModel[list[GetNodesNodeSdnZonesResponseItem]]):
    """List of items. index. Get status for all zones. response."""
    root: list[GetNodesNodeSdnZonesResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneResponseItem(ProxmoxBaseModel):
    """Model for diridx. Directory index for SDN zone status. response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeSdnZonesZoneResponse(RootModel[list[GetNodesNodeSdnZonesZoneResponseItem]]):
    """List of items. diridx. Directory index for SDN zone status. response."""
    root: list[GetNodesNodeSdnZonesZoneResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneBridgesResponseItem(ProxmoxBaseModel):
    """Model for bridges. Get a list of all bridges (vnets) that are part of a zone, as well as the ports that are members of that bridge. response."""
    name: StrictStr | None = Field(None, description='Name of the bridge.')
    ports: list[dict[str, object]] | None = Field(None, description='All ports that are members of the bridge')
    vlan_filtering: StrictStr | None = Field(None, description='Whether VLAN filtering is enabled for this bridge (= VLAN-aware).')

class GetNodesNodeSdnZonesZoneBridgesResponse(RootModel[list[GetNodesNodeSdnZonesZoneBridgesResponseItem]]):
    """List of items. bridges. Get a list of all bridges (vnets) that are part of a zone, as well as the ports that are members of that bridge. response."""
    root: list[GetNodesNodeSdnZonesZoneBridgesResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneContentResponseItem(ProxmoxBaseModel):
    """Model for index. List zone content. response."""
    status: StrictStr | None = Field(None, description='Status.')
    statusmsg: StrictStr | None = Field(None, description='Status details')
    vnet: StrictStr | None = Field(None, description='Vnet identifier.')

class GetNodesNodeSdnZonesZoneContentResponse(RootModel[list[GetNodesNodeSdnZonesZoneContentResponseItem]]):
    """List of items. index. List zone content. response."""
    root: list[GetNodesNodeSdnZonesZoneContentResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneIpVrfResponseItem(ProxmoxBaseModel):
    """Model for ip-vrf. Get the IP VRF of an EVPN zone. response."""
    ip: StrictStr | None = Field(None, description='The CIDR of the route table entry.')
    metric: int | None = Field(None, description="This route's metric.")
    nexthops: list[StrictStr] | None = Field(None, description='A list of nexthops for the route table entry.')
    protocol: StrictStr | None = Field(None, description='The protocol where this route was learned from (e.g. BGP).')

class GetNodesNodeSdnZonesZoneIpVrfResponse(RootModel[list[GetNodesNodeSdnZonesZoneIpVrfResponseItem]]):
    """List of items. ip-vrf. Get the IP VRF of an EVPN zone. response."""
    root: list[GetNodesNodeSdnZonesZoneIpVrfResponseItem] = Field(..., description='All entries in the VRF table of zone {zone} of the node.This does not include /32 routes for guests on this host,since they are handled via the respective vnet bridge directly.')

class GetNodesNodeServicesResponseItem(ProxmoxBaseModel):
    """Model for index. Service list. response."""
    active_state: StrictStr | None = Field(None, alias="active-state", description='Current state of the service process (systemd ActiveState).')
    desc: StrictStr | None = Field(None, description='Description of the service.')
    name: StrictStr | None = Field(None, description='Short identifier for the service (e.g., "pveproxy").')
    service: StrictStr | None = Field(None, description='Systemd unit name (e.g., pveproxy).')
    state: StrictStr | None = Field(None, description='Execution status of the service (systemd SubState).')
    unit_state: StrictStr | None = Field(None, alias="unit-state", description='Whether the service is enabled (systemd UnitFileState).')

class GetNodesNodeServicesResponse(RootModel[list[GetNodesNodeServicesResponseItem]]):
    """List of items. index. Service list. response."""
    root: list[GetNodesNodeServicesResponseItem] = Field(...)

class GetNodesNodeServicesServiceResponseItem(ProxmoxBaseModel):
    """Model for srvcmdidx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeServicesServiceResponse(RootModel[list[GetNodesNodeServicesServiceResponseItem]]):
    """List of items. srvcmdidx. Directory index response."""
    root: list[GetNodesNodeServicesServiceResponseItem] = Field(...)

class PostNodesNodeServicesServiceReloadRequest(RootModel[dict[str, object]]):
    """Model for service_reload. Reload service. Falls back to restart if service cannot be reloaded. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceReloadResponse(RootModel[StrictStr]):
    """Model for service_reload. Reload service. Falls back to restart if service cannot be reloaded. response."""
    root: StrictStr = Field(...)

class PostNodesNodeServicesServiceRestartRequest(RootModel[dict[str, object]]):
    """Model for service_restart. Hard restart service. Use reload if you want to reduce interruptions. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceRestartResponse(RootModel[StrictStr]):
    """Model for service_restart. Hard restart service. Use reload if you want to reduce interruptions. response."""
    root: StrictStr = Field(...)

class PostNodesNodeServicesServiceStartRequest(RootModel[dict[str, object]]):
    """Model for service_start. Start service. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceStartResponse(RootModel[StrictStr]):
    """Model for service_start. Start service. response."""
    root: StrictStr = Field(...)

class GetNodesNodeServicesServiceStateResponse(ProxmoxBaseModel):
    """Model for service_state. Read service properties response."""
    active_state: StrictStr = Field(..., alias="active-state", description='Current state of the service process (systemd ActiveState).')
    desc: StrictStr = Field(..., description='Description of the service.')
    name: StrictStr = Field(..., description='Short identifier for the service (e.g., "pveproxy").')
    service: StrictStr = Field(..., description='Systemd unit name (e.g., pveproxy).')
    state: StrictStr = Field(..., description='Execution status of the service (systemd SubState).')
    unit_state: StrictStr = Field(..., alias="unit-state", description='Whether the service is enabled (systemd UnitFileState).')

class PostNodesNodeServicesServiceStopRequest(RootModel[dict[str, object]]):
    """Model for service_stop. Stop service. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceStopResponse(RootModel[StrictStr]):
    """Model for service_stop. Stop service. response."""
    root: StrictStr = Field(...)

class PostNodesNodeSpiceshellRequest(ProxmoxBaseModel):
    """Model for spiceshell. Creates a SPICE shell. request."""
    cmd: StrictStr | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: StrictStr | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')
    proxy: StrictStr | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeSpiceshellResponse(ProxmoxBaseModel):
    """Model for spiceshell. Creates a SPICE shell. response."""
    host: StrictStr = Field(...)
    password: StrictStr = Field(...)
    proxy: StrictStr = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: StrictStr = Field(...)

class PostNodesNodeStartallRequest(ProxmoxBaseModel):
    """Model for startall. Start all VMs and containers located on this node (by default only those with onboot=1). request."""
    force: bool | None = Field(None, description="Issue start command even if virtual guest have 'onboot' not set or set to off.")
    max_workers: int | None = Field(None, alias="max-workers", description="Defines the maximum number of tasks running concurrently. If not set, uses 'max_workers' from datacenter.cfg, and if that's not set, the available CPU threads, clamped to a maximum of 8, are used.")
    vms: StrictStr | None = Field(None, description='Only consider guests from this comma separated list of VMIDs.')

class PostNodesNodeStartallResponse(RootModel[StrictStr]):
    """Model for startall. Start all VMs and containers located on this node (by default only those with onboot=1). response."""
    root: StrictStr = Field(...)

class GetNodesNodeStatusResponse(ProxmoxBaseModel):
    """Model for status. Read node status response."""
    boot_info: dict[str, object] = Field(..., alias="boot-info", description='Meta-information about the boot mode.')
    cpu: float = Field(..., description='The current cpu usage.')
    cpuinfo: dict[str, object] = Field(...)
    current_kernel: dict[str, object] = Field(..., alias="current-kernel", description='Meta-information about the currently booted kernel of this node.')
    loadavg: list[StrictStr] = Field(..., description='An array of load avg for 1, 5 and 15 minutes respectively.')
    memory: dict[str, object] = Field(...)
    pveversion: StrictStr = Field(..., description='The PVE version string.')
    rootfs: dict[str, object] = Field(...)

class PostNodesNodeStatusRequest(ProxmoxBaseModel):
    """Model for node_cmd. Reboot or shutdown a node. request."""
    command: StrictStr = Field(..., description='Specify the command.')

class PostNodesNodeStatusResponse(RootModel[None]):
    """Model for node_cmd. Reboot or shutdown a node. response."""
    root: None = Field(...)

class PostNodesNodeStopallRequest(ProxmoxBaseModel):
    """Model for stopall. Stop all VMs and Containers. request."""
    force_stop: bool | None = Field(None, alias="force-stop", description='Force a hard-stop after the timeout.')
    max_workers: int | None = Field(None, alias="max-workers", description="Defines the maximum number of tasks running concurrently. If  not set, uses 'max_workers' from datacenter.cfg, and if that's not set, the available CPU threads, clamped to a maximum of 8, are used.")
    timeout: int | None = Field(None, description='Timeout for each guest shutdown task. Depending on `force-stop`, the shutdown gets then simply aborted or a hard-stop is forced.')
    vms: StrictStr | None = Field(None, description='Only consider Guests with these IDs.')

class PostNodesNodeStopallResponse(RootModel[StrictStr]):
    """Model for stopall. Stop all VMs and Containers. response."""
    root: StrictStr = Field(...)

class GetNodesNodeStorageResponseItem(ProxmoxBaseModel):
    """Model for index. Get status for all datastores. response."""
    active: bool | None = Field(None, description='Set when storage is accessible.')
    avail: int | None = Field(None, description='Available storage space in bytes.')
    content: StrictStr | None = Field(None, description='Allowed storage content types.')
    enabled: bool | None = Field(None, description='Set when storage is enabled (not disabled).')
    formats: dict[str, object] | None = Field(None, description="Lists the supported and default format. Use 'formats' instead. Only included if 'format' parameter is set.")
    select_existing: bool | None = Field(None, description="Instead of creating new volumes, one must select one that is already existing. Only included if 'format' parameter is set.")
    shared: bool | None = Field(None, description='Shared flag from storage configuration.')
    storage: StrictStr | None = Field(None, description='The storage identifier.')
    total: int | None = Field(None, description='Total storage space in bytes.')
    type: StrictStr | None = Field(None, description='Storage type.')
    used: int | None = Field(None, description='Used storage space in bytes.')
    used_fraction: float | None = Field(None, description='Used fraction (used/total).')

class GetNodesNodeStorageResponse(RootModel[list[GetNodesNodeStorageResponseItem]]):
    """List of items. index. Get status for all datastores. response."""
    root: list[GetNodesNodeStorageResponseItem] = Field(...)

class GetNodesNodeStorageStorageResponseItem(ProxmoxBaseModel):
    """Model for diridx. None response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeStorageStorageResponse(RootModel[list[GetNodesNodeStorageStorageResponseItem]]):
    """List of items. diridx. None response."""
    root: list[GetNodesNodeStorageStorageResponseItem] = Field(...)

class GetNodesNodeStorageStorageContentResponseItem(ProxmoxBaseModel):
    """Model for index. List storage content. response."""
    ctime: int | None = Field(None, description='Creation time (seconds since the UNIX Epoch).')
    encrypted: StrictStr | None = Field(None, description="If whole backup is encrypted, value is the fingerprint or '1'  if encrypted. Only useful for the Proxmox Backup Server storage type.")
    format: StrictStr | None = Field(None, description="Format identifier ('raw', 'qcow2', 'subvol', 'iso', 'tgz' ...)")
    notes: StrictStr | None = Field(None, description='Optional notes. If they contain multiple lines, only the first one is returned here.')
    parent: StrictStr | None = Field(None, description='Volume identifier of parent (for linked cloned).')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')
    size: int | None = Field(None, description='Volume size in bytes.')
    used: int | None = Field(None, description='Used space. Please note that most storage plugins do not report anything useful here.')
    verification: dict[str, object] | None = Field(None, description='Last backup verification result, only useful for PBS storages.')
    vmid: int | None = Field(None, description='Associated Owner VMID.')
    volid: StrictStr | None = Field(None, description='Volume identifier.')

class GetNodesNodeStorageStorageContentResponse(RootModel[list[GetNodesNodeStorageStorageContentResponseItem]]):
    """List of items. index. List storage content. response."""
    root: list[GetNodesNodeStorageStorageContentResponseItem] = Field(...)

class PostNodesNodeStorageStorageContentRequest(ProxmoxBaseModel):
    """Model for create. Allocate disk images. request."""
    filename: StrictStr = Field(..., description='The name of the file to create.')
    format: StrictStr | None = Field(None, description='Format of the image.')
    size: StrictStr = Field(..., description="Size in kilobyte (1024 bytes). Optional suffixes 'M' (megabyte, 1024K) and 'G' (gigabyte, 1024M)")
    vmid: int = Field(..., description='Specify owner VM')

class PostNodesNodeStorageStorageContentResponse(RootModel[StrictStr]):
    """Model for create. Allocate disk images. response."""
    root: StrictStr = Field(..., description='Volume identifier')

class DeleteNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    """Model for delete. Delete volume request."""
    delay: int | None = Field(None, description="Time to wait for the task to finish. We return 'null' if the task finish within that time.")

class DeleteNodesNodeStorageStorageContentVolumeResponse(RootModel[StrictStr]):
    """Model for delete. Delete volume response."""
    root: StrictStr = Field(...)

class GetNodesNodeStorageStorageContentVolumeResponse(ProxmoxBaseModel):
    """Model for info. Get volume attributes response."""
    format: StrictStr = Field(..., description="Format identifier ('raw', 'qcow2', 'subvol', 'iso', 'tgz' ...)")
    notes: StrictStr | None = Field(None, description='Optional notes.')
    path: StrictStr = Field(..., description='The Path')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')
    size: int = Field(..., description='Volume size in bytes.')
    used: int = Field(..., description='Used space. Please note that most storage plugins do not report anything useful here.')

class PostNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    """Model for copy. Copy a volume. This is experimental code - do not use. request."""
    target: StrictStr = Field(..., description='Target volume identifier')
    target_node: StrictStr | None = Field(None, description='Target node. Default is local node.')

class PostNodesNodeStorageStorageContentVolumeResponse(RootModel[StrictStr]):
    """Model for copy. Copy a volume. This is experimental code - do not use. response."""
    root: StrictStr = Field(...)

class PutNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    """Model for updateattributes. Update volume attributes request."""
    notes: StrictStr | None = Field(None, description='The new notes.')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')

class PutNodesNodeStorageStorageContentVolumeResponse(RootModel[None]):
    """Model for updateattributes. Update volume attributes response."""
    root: None = Field(...)

class PostNodesNodeStorageStorageDownloadUrlRequest(ProxmoxBaseModel):
    """Model for download_url. Download templates, ISO images, OVAs and VM images by using an URL. request."""
    checksum: StrictStr | None = Field(None, description='The expected checksum of the file.')
    checksum_algorithm: StrictStr | None = Field(None, alias="checksum-algorithm", description='The algorithm to calculate the checksum of the file.')
    compression: StrictStr | None = Field(None, description='Decompress the downloaded file using the specified compression algorithm.')
    content: StrictStr = Field(..., description='Content type.')
    filename: StrictStr = Field(..., description='The name of the file to create. Caution: This will be normalized!')
    url: StrictStr = Field(..., description='The URL to download the file from.')
    verify_certificates: bool | None = Field(None, alias="verify-certificates", description='If false, no SSL/TLS certificates will be verified.')

class PostNodesNodeStorageStorageDownloadUrlResponse(RootModel[StrictStr]):
    """Model for download_url. Download templates, ISO images, OVAs and VM images by using an URL. response."""
    root: StrictStr = Field(...)

class GetNodesNodeStorageStorageFileRestoreDownloadResponse(RootModel[object]):
    """Model for download. Extract a file or directory (as zip archive) from a PBS backup. response."""
    root: object = Field(...)

class GetNodesNodeStorageStorageFileRestoreListResponseItem(ProxmoxBaseModel):
    """Model for list. List files and directories for single file restore under the given path. response."""
    filepath: StrictStr | None = Field(None, description='base64 path of the current entry')
    leaf: bool | None = Field(None, description='If this entry is a leaf in the directory graph.')
    mtime: int | None = Field(None, description='Entry last-modified time (unix timestamp).')
    size: int | None = Field(None, description='Entry file size.')
    text: StrictStr | None = Field(None, description='Entry display text.')
    type: StrictStr | None = Field(None, description='Entry type.')

class GetNodesNodeStorageStorageFileRestoreListResponse(RootModel[list[GetNodesNodeStorageStorageFileRestoreListResponseItem]]):
    """List of items. list. List files and directories for single file restore under the given path. response."""
    root: list[GetNodesNodeStorageStorageFileRestoreListResponseItem] = Field(...)

class GetNodesNodeStorageStorageImportMetadataResponse(ProxmoxBaseModel):
    """Model for get_import_metadata. Get the base parameters for creating a guest which imports data from a foreign importable guest, like an ESXi VM response."""
    create_args: dict[str, object] = Field(..., alias="create-args", description='Parameters which can be used in a call to create a VM or container.')
    disks: dict[str, object] | None = Field(None, description='Recognised disk volumes as `$bus$id` => `$storeid:$path` map.')
    net: dict[str, object] | None = Field(None, description='Recognised network interfaces as `net$id` => { ...params } object.')
    source: StrictStr = Field(..., description='The type of the import-source of this guest volume.')
    type: StrictStr = Field(..., description='The type of guest this is going to produce.')
    warnings: list[dict[str, object]] | None = Field(None, description='List of known issues that can affect the import of a guest. Note that lack of warning does not imply that there cannot be any problems.')

class PostNodesNodeStorageStorageOciRegistryPullRequest(ProxmoxBaseModel):
    """Model for oci_registry_pull. Pull an OCI image from a registry. request."""
    filename: StrictStr | None = Field(None, description='Custom destination file name of the OCI image. Caution: This will be normalized!')
    reference: StrictStr = Field(..., description='The reference to the OCI image to download.')

class PostNodesNodeStorageStorageOciRegistryPullResponse(RootModel[StrictStr]):
    """Model for oci_registry_pull. Pull an OCI image from a registry. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeStorageStoragePrunebackupsRequest(ProxmoxBaseModel):
    """Model for delete. Prune backups. Only those using the standard naming scheme are considered. request."""
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    type: StrictStr | None = Field(None, description="Either 'qemu' or 'lxc'. Only consider backups for guests of this type.")
    vmid: int | None = Field(None, description='Only prune backups for this VM.')

class DeleteNodesNodeStorageStoragePrunebackupsResponse(RootModel[StrictStr]):
    """Model for delete. Prune backups. Only those using the standard naming scheme are considered. response."""
    root: StrictStr = Field(...)

class GetNodesNodeStorageStoragePrunebackupsResponseItem(ProxmoxBaseModel):
    """Model for dryrun. Get prune information for backups. NOTE: this is only a preview and might not be what a subsequent prune call does if backups are removed/added in the meantime. response."""
    ctime: int | None = Field(None, description='Creation time of the backup (seconds since the UNIX epoch).')
    mark: StrictStr | None = Field(None, description="Whether the backup would be kept or removed. Backups that are protected or don't use the standard naming scheme are not removed.")
    type: StrictStr | None = Field(None, description="One of 'qemu', 'lxc', 'openvz' or 'unknown'.")
    vmid: int | None = Field(None, description='The VM the backup belongs to.')
    volid: StrictStr | None = Field(None, description='Backup volume ID.')

class GetNodesNodeStorageStoragePrunebackupsResponse(RootModel[list[GetNodesNodeStorageStoragePrunebackupsResponseItem]]):
    """List of items. dryrun. Get prune information for backups. NOTE: this is only a preview and might not be what a subsequent prune call does if backups are removed/added in the meantime. response."""
    root: list[GetNodesNodeStorageStoragePrunebackupsResponseItem] = Field(...)

class GetNodesNodeStorageStorageRrdResponse(ProxmoxBaseModel):
    """Model for rrd. Read storage RRD statistics (returns PNG). response."""
    filename: StrictStr = Field(...)

class GetNodesNodeStorageStorageRrddataResponse(RootModel[list[dict[str, object]]]):
    """Model for rrddata. Read storage RRD statistics. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeStorageStorageStatusResponse(ProxmoxBaseModel):
    """Model for read_status. Read storage status. response."""
    active: bool | None = Field(None, description='Set when storage is accessible.')
    avail: int | None = Field(None, description='Available storage space in bytes.')
    content: StrictStr = Field(..., description='Allowed storage content types.')
    enabled: bool | None = Field(None, description='Set when storage is enabled (not disabled).')
    shared: bool | None = Field(None, description='Shared flag from storage configuration.')
    total: int | None = Field(None, description='Total storage space in bytes.')
    type: StrictStr = Field(..., description='Storage type.')
    used: int | None = Field(None, description='Used storage space in bytes.')

class PostNodesNodeStorageStorageUploadRequest(ProxmoxBaseModel):
    """Model for upload. Upload templates, ISO images, OVAs and VM images. request."""
    checksum: StrictStr | None = Field(None, description='The expected checksum of the file.')
    checksum_algorithm: StrictStr | None = Field(None, alias="checksum-algorithm", description='The algorithm to calculate the checksum of the file.')
    content: StrictStr = Field(..., description='Content type.')
    filename: StrictStr = Field(..., description='The name of the file to create. Caution: This will be normalized!')
    tmpfilename: StrictStr | None = Field(None, description='The source file name. This parameter is usually set by the REST handler. You can only overwrite it when connecting to the trusted port on localhost.')

class PostNodesNodeStorageStorageUploadResponse(RootModel[StrictStr]):
    """Model for upload. Upload templates, ISO images, OVAs and VM images. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeSubscriptionRequest(RootModel[dict[str, object]]):
    """Model for delete. Delete subscription key of this node. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for delete. Delete subscription key of this node. response."""
    root: None = Field(...)

class GetNodesNodeSubscriptionResponse(ProxmoxBaseModel):
    """Model for get. Read subscription info. response."""
    checktime: int | None = Field(None, description='Timestamp of the last check done.')
    key: StrictStr | None = Field(None, description='The subscription key, if set and permitted to access.')
    level: StrictStr | None = Field(None, description='A short code for the subscription level.')
    message: StrictStr | None = Field(None, description='A more human readable status message.')
    nextduedate: StrictStr | None = Field(None, description='Next due date of the set subscription.')
    productname: StrictStr | None = Field(None, description='Human readable productname of the set subscription.')
    regdate: StrictStr | None = Field(None, description='Register date of the set subscription.')
    serverid: StrictStr | None = Field(None, description='The server ID, if permitted to access.')
    signature: StrictStr | None = Field(None, description='Signature for offline keys')
    sockets: int | None = Field(None, description='The number of sockets for this host.')
    status: StrictStr = Field(..., description='The current subscription status.')
    url: StrictStr | None = Field(None, description='URL to the web shop.')

class PostNodesNodeSubscriptionRequest(ProxmoxBaseModel):
    """Model for update. Update subscription info. request."""
    force: bool | None = Field(None, description='Always connect to server, even if local cache is still valid.')

class PostNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for update. Update subscription info. response."""
    root: None = Field(...)

class PutNodesNodeSubscriptionRequest(ProxmoxBaseModel):
    """Model for set. Set subscription key. request."""
    key: StrictStr = Field(..., description='Proxmox VE subscription key')

class PutNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for set. Set subscription key. response."""
    root: None = Field(...)

class PostNodesNodeSuspendallRequest(ProxmoxBaseModel):
    """Model for suspendall. Suspend all VMs. request."""
    max_workers: int | None = Field(None, alias="max-workers", description="Maximal number of parallel migration job. If not set, uses'max_workers' from datacenter.cfg, and if that's not set the available'\n                    .' CPU threads, clamped to a maximum of 8, are used.")
    vms: StrictStr | None = Field(None, description='Only consider Guests with these IDs.')

class PostNodesNodeSuspendallResponse(RootModel[StrictStr]):
    """Model for suspendall. Suspend all VMs. response."""
    root: StrictStr = Field(...)

class GetNodesNodeSyslogResponseItem(ProxmoxBaseModel):
    """Model for syslog. Read system log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeSyslogResponse(RootModel[list[GetNodesNodeSyslogResponseItem]]):
    """List of items. syslog. Read system log response."""
    root: list[GetNodesNodeSyslogResponseItem] = Field(...)

class GetNodesNodeTasksResponseItem(ProxmoxBaseModel):
    """Model for node_tasks. Read task list for one node (finished tasks). response."""
    endtime: int | None = Field(None)
    id: StrictStr | None = Field(None)
    node: StrictStr | None = Field(None)
    pid: int | None = Field(None)
    pstart: int | None = Field(None)
    starttime: int | None = Field(None)
    status: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)
    upid: StrictStr | None = Field(None)
    user: StrictStr | None = Field(None)

class GetNodesNodeTasksResponse(RootModel[list[GetNodesNodeTasksResponseItem]]):
    """List of items. node_tasks. Read task list for one node (finished tasks). response."""
    root: list[GetNodesNodeTasksResponseItem] = Field(...)

class DeleteNodesNodeTasksUpidRequest(RootModel[dict[str, object]]):
    """Model for stop_task. Stop a task. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeTasksUpidResponse(RootModel[None]):
    """Model for stop_task. Stop a task. response."""
    root: None = Field(...)

class GetNodesNodeTasksUpidResponse(RootModel[list[dict[str, object]]]):
    """Model for upid_index. None response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeTasksUpidLogResponseItem(ProxmoxBaseModel):
    """Model for read_task_log. Read task log. response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeTasksUpidLogResponse(RootModel[list[GetNodesNodeTasksUpidLogResponseItem]]):
    """List of items. read_task_log. Read task log. response."""
    root: list[GetNodesNodeTasksUpidLogResponseItem] = Field(...)

class GetNodesNodeTasksUpidStatusResponse(ProxmoxBaseModel):
    """Model for read_task_status. Read task status. response."""
    exitstatus: StrictStr | None = Field(None)
    id: StrictStr = Field(...)
    node: StrictStr = Field(...)
    pid: int = Field(...)
    pstart: int = Field(...)
    starttime: int = Field(...)
    status: StrictStr = Field(...)
    type: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class PostNodesNodeTermproxyRequest(ProxmoxBaseModel):
    """Model for termproxy. Creates a VNC Shell proxy. request."""
    cmd: StrictStr | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: StrictStr | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')

class PostNodesNodeTermproxyResponse(ProxmoxBaseModel):
    """Model for termproxy. Creates a VNC Shell proxy. response."""
    port: int = Field(..., description='port used to bind termproxy to.')
    ticket: StrictStr = Field(..., description='VNC ticket used to verify websocket connection.')
    upid: StrictStr = Field(..., description='UPID for termproxy worker task.')
    user: StrictStr = Field(..., description='user/token that generated the VNC ticket in `ticket`.')

class GetNodesNodeTimeResponse(ProxmoxBaseModel):
    """Model for time. Read server time and time zone settings. response."""
    localtime: int = Field(..., description='Seconds since 1970-01-01 00:00:00 (local time)')
    time: int = Field(..., description='Seconds since 1970-01-01 00:00:00 UTC.')
    timezone: StrictStr = Field(..., description='Time zone')

class PutNodesNodeTimeRequest(ProxmoxBaseModel):
    """Model for set_timezone. Set time zone. request."""
    timezone: StrictStr = Field(..., description="Time zone. The file '/usr/share/zoneinfo/zone.tab' contains the list of valid names.")

class PutNodesNodeTimeResponse(RootModel[None]):
    """Model for set_timezone. Set time zone. response."""
    root: None = Field(...)

class GetNodesNodeVersionResponse(ProxmoxBaseModel):
    """Model for version. API version details response."""
    release: StrictStr = Field(..., description='The current installed Proxmox VE Release')
    repoid: StrictStr = Field(..., description='The short git commit hash ID from which this version was build')
    version: StrictStr = Field(..., description='The current installed pve-manager package version')

class PostNodesNodeVncshellRequest(ProxmoxBaseModel):
    """Model for vncshell. Creates a VNC Shell proxy. request."""
    cmd: StrictStr | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: StrictStr | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')
    height: int | None = Field(None, description='sets the height of the console in pixels.')
    websocket: bool | None = Field(None, description='use websocket instead of standard vnc.')
    width: int | None = Field(None, description='sets the width of the console in pixels.')

class PostNodesNodeVncshellResponse(ProxmoxBaseModel):
    """Model for vncshell. Creates a VNC Shell proxy. response."""
    cert: StrictStr = Field(...)
    password: StrictStr | None = Field(None, description="Password used for authentication within the VNC protocol. Consists of printable ASCII characters ('!' .. '~').")
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class GetNodesNodeVncwebsocketResponse(ProxmoxBaseModel):
    """Model for vncwebsocket. Opens a websocket for VNC traffic. response."""
    port: StrictStr = Field(...)

class PostNodesNodeVzdumpRequest(ProxmoxBaseModel):
    """Model for vzdump. Create backup. request."""
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    compress: StrictStr | None = Field(None, description='Compress dump file.')
    dumpdir: StrictStr | None = Field(None, description='Store resulting files to specified directory.')
    exclude: StrictStr | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[StrictStr] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: StrictStr | None = Field(None, description='Options for backup fleecing (VM only).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    job_id: StrictStr | None = Field(None, alias="job-id", description="The ID of the backup job. If set, the 'backup-job' metadata field of the backup notification will be set to this value. Only root@pam can set this parameter.")
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: StrictStr | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: StrictStr | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: StrictStr | None = Field(None, description='Backup mode.')
    notes_template: StrictStr | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: StrictStr | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: StrictStr | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: StrictStr | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: StrictStr | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    script: StrictStr | None = Field(None, description='Use specified hook script.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stdout: bool | None = Field(None, description='Write tar to stdout, not to a file.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: StrictStr | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: StrictStr | None = Field(None, description='Store temporary files to specified directory.')
    vmid: StrictStr | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class PostNodesNodeVzdumpResponse(RootModel[StrictStr]):
    """Model for vzdump. Create backup. response."""
    root: StrictStr = Field(...)

class GetNodesNodeVzdumpDefaultsResponse(ProxmoxBaseModel):
    """Model for defaults. Get the currently configured vzdump defaults. response."""
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    compress: StrictStr | None = Field(None, description='Compress dump file.')
    dumpdir: StrictStr | None = Field(None, description='Store resulting files to specified directory.')
    exclude: StrictStr | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[StrictStr] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: StrictStr | None = Field(None, description='Options for backup fleecing (VM only).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: StrictStr | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: StrictStr | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    maxfiles: int | None = Field(None, description="Deprecated: use 'prune-backups' instead. Maximal number of backup files per guest system.")
    mode: StrictStr | None = Field(None, description='Backup mode.')
    node: StrictStr | None = Field(None, description='Only run if executed on this node.')
    notes_template: StrictStr | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: StrictStr | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: StrictStr | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: StrictStr | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: StrictStr | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    script: StrictStr | None = Field(None, description='Use specified hook script.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: StrictStr | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: StrictStr | None = Field(None, description='Store temporary files to specified directory.')
    vmid: StrictStr | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class GetNodesNodeVzdumpExtractconfigResponse(RootModel[StrictStr]):
    """Model for extractconfig. Extract configuration from vzdump backup archive. response."""
    root: StrictStr = Field(...)

class PostNodesNodeWakeonlanRequest(RootModel[dict[str, object]]):
    """Model for wakeonlan. Try to wake a node via 'wake on LAN' network packet. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeWakeonlanResponse(RootModel[StrictStr]):
    """Model for wakeonlan. Try to wake a node via 'wake on LAN' network packet. response."""
    root: StrictStr = Field(..., description='MAC address used to assemble the WoL magic packet.')

class DeletePoolsRequest(ProxmoxBaseModel):
    """Model for delete_pool. Delete pool. request."""
    poolid: StrictStr = Field(...)

class DeletePoolsResponse(RootModel[None]):
    """Model for delete_pool. Delete pool. response."""
    root: None = Field(...)

class GetPoolsResponseItem(ProxmoxBaseModel):
    """Model for index. List pools or get pool configuration. response."""
    comment: StrictStr | None = Field(None)
    members: list[dict[str, object]] | None = Field(None)
    poolid: StrictStr | None = Field(None)

class GetPoolsResponse(RootModel[list[GetPoolsResponseItem]]):
    """List of items. index. List pools or get pool configuration. response."""
    root: list[GetPoolsResponseItem] = Field(...)

class PostPoolsRequest(ProxmoxBaseModel):
    """Model for create_pool. Create new pool. request."""
    comment: StrictStr | None = Field(None)
    poolid: StrictStr = Field(...)

class PostPoolsResponse(RootModel[None]):
    """Model for create_pool. Create new pool. response."""
    root: None = Field(...)

class PutPoolsRequest(ProxmoxBaseModel):
    """Model for update_pool. Update pool. request."""
    allow_move: bool | None = Field(None, alias="allow-move", description='Allow adding a guest even if already in another pool. The guest will be removed from its current pool and added to this one.')
    comment: StrictStr | None = Field(None)
    delete: bool | None = Field(None, description='Remove the passed VMIDs and/or storage IDs instead of adding them.')
    poolid: StrictStr = Field(...)
    storage: StrictStr | None = Field(None, description='List of storage IDs to add or remove from this pool.')
    vms: StrictStr | None = Field(None, description='List of guest VMIDs to add or remove from this pool.')

class PutPoolsResponse(RootModel[None]):
    """Model for update_pool. Update pool. response."""
    root: None = Field(...)

class DeletePoolsPoolidRequest(RootModel[dict[str, object]]):
    """Model for delete_pool_deprecated. Delete pool (deprecated, no support for nested pools, use 'DELETE /pools/?poolid={poolid}'). request."""
    root: dict[str, object] = Field(...)

class DeletePoolsPoolidResponse(RootModel[None]):
    """Model for delete_pool_deprecated. Delete pool (deprecated, no support for nested pools, use 'DELETE /pools/?poolid={poolid}'). response."""
    root: None = Field(...)

class GetPoolsPoolidResponse(ProxmoxBaseModel):
    """Model for read_pool. Get pool configuration (deprecated, no support for nested pools, use 'GET /pools/?poolid={poolid}'). response."""
    comment: StrictStr | None = Field(None)
    members: list[dict[str, object]] = Field(...)

class PutPoolsPoolidRequest(ProxmoxBaseModel):
    """Model for update_pool_deprecated. Update pool data (deprecated, no support for nested pools - use 'PUT /pools/?poolid={poolid}' instead). request."""
    allow_move: bool | None = Field(None, alias="allow-move", description='Allow adding a guest even if already in another pool. The guest will be removed from its current pool and added to this one.')
    comment: StrictStr | None = Field(None)
    delete: bool | None = Field(None, description='Remove the passed VMIDs and/or storage IDs instead of adding them.')
    storage: StrictStr | None = Field(None, description='List of storage IDs to add or remove from this pool.')
    vms: StrictStr | None = Field(None, description='List of guest VMIDs to add or remove from this pool.')

class PutPoolsPoolidResponse(RootModel[None]):
    """Model for update_pool_deprecated. Update pool data (deprecated, no support for nested pools - use 'PUT /pools/?poolid={poolid}' instead). response."""
    root: None = Field(...)

class GetStorageResponseItem(ProxmoxBaseModel):
    """Model for index. Storage index. response."""
    storage: StrictStr | None = Field(None)

class GetStorageResponse(RootModel[list[GetStorageResponseItem]]):
    """List of items. index. Storage index. response."""
    root: list[GetStorageResponseItem] = Field(...)

class PostStorageRequest(ProxmoxBaseModel):
    """Model for create. Create a new storage. request."""
    authsupported: StrictStr | None = Field(None, description='Authsupported.')
    base: StrictStr | None = Field(None, description='Base volume. This volume is automatically activated.')
    blocksize: StrictStr | None = Field(None, description='block size')
    bwlimit: StrictStr | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    comstar_hg: StrictStr | None = Field(None, description='host group for comstar views')
    comstar_tg: StrictStr | None = Field(None, description='target group for comstar views')
    content: StrictStr | None = Field(None, description="Allowed content types.\n\nNOTE: the value 'rootdir' is used for Containers, and value 'images' for VMs.\n")
    content_dirs: StrictStr | None = Field(None, alias="content-dirs", description='Overrides for default content type directories.')
    create_base_path: bool | None = Field(None, alias="create-base-path", description="Create the base directory if it doesn't exist.")
    create_subdirs: bool | None = Field(None, alias="create-subdirs", description='Populate the directory with the default structure.')
    data_pool: StrictStr | None = Field(None, alias="data-pool", description='Data Pool (for erasure coding only)')
    datastore: StrictStr | None = Field(None, description='Proxmox Backup Server datastore name.')
    disable: bool | None = Field(None, description='Flag to disable the storage.')
    domain: StrictStr | None = Field(None, description='CIFS domain.')
    encryption_key: StrictStr | None = Field(None, alias="encryption-key", description="Encryption key. Use 'autogen' to generate one automatically without passphrase.")
    export: StrictStr | None = Field(None, description='NFS export path.')
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    format: StrictStr | None = Field(None, description='Default image format.')
    fs_name: StrictStr | None = Field(None, alias="fs-name", description='The Ceph filesystem name.')
    fuse: bool | None = Field(None, description='Mount CephFS through FUSE.')
    is_mountpoint: StrictStr | None = Field(None, description='Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.')
    iscsiprovider: StrictStr | None = Field(None, description='iscsi provider')
    keyring: StrictStr | None = Field(None, description='Client keyring contents (for external clusters).')
    krbd: bool | None = Field(None, description='Always access rbd through krbd kernel module.')
    lio_tpg: StrictStr | None = Field(None, description='target portal group for Linux LIO targets')
    master_pubkey: StrictStr | None = Field(None, alias="master-pubkey", description='Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.')
    max_protected_backups: int | None = Field(None, alias="max-protected-backups", description="Maximal number of protected backups per guest. Use '-1' for unlimited.")
    mkdir: bool | None = Field(None, description="Create the directory if it doesn't exist and populate it with default sub-dirs. NOTE: Deprecated, use the 'create-base-path' and 'create-subdirs' options instead.")
    monhost: StrictStr | None = Field(None, description='IP addresses of monitors (for external clusters).')
    mountpoint: StrictStr | None = Field(None, description='mount point')
    namespace: StrictStr | None = Field(None, description='Namespace.')
    nocow: bool | None = Field(None, description='Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.')
    nodes: StrictStr | None = Field(None, description='List of nodes for which the storage configuration applies.')
    nowritecache: bool | None = Field(None, description='disable write caching on the target')
    options: StrictStr | None = Field(None, description="NFS/CIFS mount options (see 'man nfs' or 'man mount.cifs')")
    password: StrictStr | None = Field(None, description='Password for accessing the share/datastore.')
    path: StrictStr | None = Field(None, description='File system path.')
    pool: StrictStr | None = Field(None, description='Pool.')
    port: int | None = Field(None, description="Use this port to connect to the storage instead of the default one (for example, with PBS or ESXi). For NFS and CIFS, use the 'options' option to configure the port via the mount options.")
    portal: StrictStr | None = Field(None, description='iSCSI portal (IP or DNS name with optional port).')
    preallocation: StrictStr | None = Field(None, description="Preallocation mode for raw and qcow2 images. Using 'metadata' on raw images results in preallocation=off.")
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.')
    saferemove: bool | None = Field(None, description='Zero-out data when removing LVs.')
    saferemove_stepsize: int | None = Field(None, alias="saferemove-stepsize", description='Wipe step size in MiB. It will be capped to the maximum supported by the storage.')
    saferemove_throughput: StrictStr | None = Field(None, description='Wipe throughput (cstream -t parameter value).')
    server: StrictStr | None = Field(None, description='Server IP or DNS name.')
    share: StrictStr | None = Field(None, description='CIFS share.')
    shared: bool | None = Field(None, description="Indicate that this is a single storage with the same contents on all nodes (or all listed in the 'nodes' option). It will not make the contents of a local storage automatically accessible to other nodes, it just marks an already shared storage as such!")
    skip_cert_verification: bool | None = Field(None, alias="skip-cert-verification", description='Disable TLS certificate verification, only enable on fully trusted networks!')
    smbversion: StrictStr | None = Field(None, description="SMB protocol version. 'default' if not set, negotiates the highest SMB2+ version supported by both the client and server.")
    snapshot_as_volume_chain: bool | None = Field(None, alias="snapshot-as-volume-chain", description='Enable support for creating storage-vendor agnostic snapshot through volume backing-chains.')
    sparse: bool | None = Field(None, description='use sparse volumes')
    storage: StrictStr = Field(..., description='The storage identifier.')
    subdir: StrictStr | None = Field(None, description='Subdir to mount.')
    tagged_only: bool | None = Field(None, description="Only use logical volumes tagged with 'pve-vm-ID'.")
    target: StrictStr | None = Field(None, description='iSCSI target.')
    thinpool: StrictStr | None = Field(None, description='LVM thin pool LV name.')
    type: StrictStr = Field(..., description='Storage type.')
    username: StrictStr | None = Field(None, description='RBD Id.')
    vgname: StrictStr | None = Field(None, description='Volume group name.')
    zfs_base_path: StrictStr | None = Field(None, alias="zfs-base-path", description="Base path where to look for the created ZFS block devices. Set automatically during creation if not specified. Usually '/dev/zvol'.")

class PostStorageResponse(ProxmoxBaseModel):
    """Model for create. Create a new storage. response."""
    config: dict[str, object] | None = Field(None, description='Partial, possibly server generated, configuration properties.')
    storage: StrictStr = Field(..., description='The ID of the created storage.')
    type: StrictStr = Field(..., description='The type of the created storage.')

class DeleteStorageStorageRequest(RootModel[dict[str, object]]):
    """Model for delete. Delete storage configuration. request."""
    root: dict[str, object] = Field(...)

class DeleteStorageStorageResponse(RootModel[None]):
    """Model for delete. Delete storage configuration. response."""
    root: None = Field(...)

class GetStorageStorageResponse(RootModel[dict[str, object]]):
    """Model for read. Read storage configuration. response."""
    root: dict[str, object] = Field(...)

class PutStorageStorageRequest(ProxmoxBaseModel):
    """Model for update. Update storage configuration. request."""
    blocksize: StrictStr | None = Field(None, description='block size')
    bwlimit: StrictStr | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    comstar_hg: StrictStr | None = Field(None, description='host group for comstar views')
    comstar_tg: StrictStr | None = Field(None, description='target group for comstar views')
    content: StrictStr | None = Field(None, description="Allowed content types.\n\nNOTE: the value 'rootdir' is used for Containers, and value 'images' for VMs.\n")
    content_dirs: StrictStr | None = Field(None, alias="content-dirs", description='Overrides for default content type directories.')
    create_base_path: bool | None = Field(None, alias="create-base-path", description="Create the base directory if it doesn't exist.")
    create_subdirs: bool | None = Field(None, alias="create-subdirs", description='Populate the directory with the default structure.')
    data_pool: StrictStr | None = Field(None, alias="data-pool", description='Data Pool (for erasure coding only)')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the storage.')
    domain: StrictStr | None = Field(None, description='CIFS domain.')
    encryption_key: StrictStr | None = Field(None, alias="encryption-key", description="Encryption key. Use 'autogen' to generate one automatically without passphrase.")
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    format: StrictStr | None = Field(None, description='Default image format.')
    fs_name: StrictStr | None = Field(None, alias="fs-name", description='The Ceph filesystem name.')
    fuse: bool | None = Field(None, description='Mount CephFS through FUSE.')
    is_mountpoint: StrictStr | None = Field(None, description='Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.')
    keyring: StrictStr | None = Field(None, description='Client keyring contents (for external clusters).')
    krbd: bool | None = Field(None, description='Always access rbd through krbd kernel module.')
    lio_tpg: StrictStr | None = Field(None, description='target portal group for Linux LIO targets')
    master_pubkey: StrictStr | None = Field(None, alias="master-pubkey", description='Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.')
    max_protected_backups: int | None = Field(None, alias="max-protected-backups", description="Maximal number of protected backups per guest. Use '-1' for unlimited.")
    mkdir: bool | None = Field(None, description="Create the directory if it doesn't exist and populate it with default sub-dirs. NOTE: Deprecated, use the 'create-base-path' and 'create-subdirs' options instead.")
    monhost: StrictStr | None = Field(None, description='IP addresses of monitors (for external clusters).')
    mountpoint: StrictStr | None = Field(None, description='mount point')
    namespace: StrictStr | None = Field(None, description='Namespace.')
    nocow: bool | None = Field(None, description='Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.')
    nodes: StrictStr | None = Field(None, description='List of nodes for which the storage configuration applies.')
    nowritecache: bool | None = Field(None, description='disable write caching on the target')
    options: StrictStr | None = Field(None, description="NFS/CIFS mount options (see 'man nfs' or 'man mount.cifs')")
    password: StrictStr | None = Field(None, description='Password for accessing the share/datastore.')
    pool: StrictStr | None = Field(None, description='Pool.')
    port: int | None = Field(None, description="Use this port to connect to the storage instead of the default one (for example, with PBS or ESXi). For NFS and CIFS, use the 'options' option to configure the port via the mount options.")
    preallocation: StrictStr | None = Field(None, description="Preallocation mode for raw and qcow2 images. Using 'metadata' on raw images results in preallocation=off.")
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.')
    saferemove: bool | None = Field(None, description='Zero-out data when removing LVs.')
    saferemove_stepsize: int | None = Field(None, alias="saferemove-stepsize", description='Wipe step size in MiB. It will be capped to the maximum supported by the storage.')
    saferemove_throughput: StrictStr | None = Field(None, description='Wipe throughput (cstream -t parameter value).')
    server: StrictStr | None = Field(None, description='Server IP or DNS name.')
    shared: bool | None = Field(None, description="Indicate that this is a single storage with the same contents on all nodes (or all listed in the 'nodes' option). It will not make the contents of a local storage automatically accessible to other nodes, it just marks an already shared storage as such!")
    skip_cert_verification: bool | None = Field(None, alias="skip-cert-verification", description='Disable TLS certificate verification, only enable on fully trusted networks!')
    smbversion: StrictStr | None = Field(None, description="SMB protocol version. 'default' if not set, negotiates the highest SMB2+ version supported by both the client and server.")
    snapshot_as_volume_chain: bool | None = Field(None, alias="snapshot-as-volume-chain", description='Enable support for creating storage-vendor agnostic snapshot through volume backing-chains.')
    sparse: bool | None = Field(None, description='use sparse volumes')
    subdir: StrictStr | None = Field(None, description='Subdir to mount.')
    tagged_only: bool | None = Field(None, description="Only use logical volumes tagged with 'pve-vm-ID'.")
    username: StrictStr | None = Field(None, description='RBD Id.')
    zfs_base_path: StrictStr | None = Field(None, alias="zfs-base-path", description="Base path where to look for the created ZFS block devices. Set automatically during creation if not specified. Usually '/dev/zvol'.")

class PutStorageStorageResponse(ProxmoxBaseModel):
    """Model for update. Update storage configuration. response."""
    config: dict[str, object] | None = Field(None, description='Partial, possibly server generated, configuration properties.')
    storage: StrictStr = Field(..., description='The ID of the created storage.')
    type: StrictStr = Field(..., description='The type of the created storage.')

class GetVersionResponse(ProxmoxBaseModel):
    """Model for version. API version details, including some parts of the global datacenter config. response."""
    console: StrictStr | None = Field(None, description='The default console viewer to use.')
    release: StrictStr = Field(..., description='The current Proxmox VE point release in `x.y` format.')
    repoid: StrictStr = Field(..., description='The short git revision from which this version was build.')
    version: StrictStr = Field(..., description='The full pve-manager package version of this node.')
