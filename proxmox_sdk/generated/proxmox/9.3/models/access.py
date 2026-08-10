"""Generated Pydantic v2 schemas for Proxmox route group 'access'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr

GENERATED_FOR_PROXMOX_VERSION = "9.3"
GENERATED_SOURCE_SHA256 = "8231806a7dda8120eea2b23e03fc180ec4cfe253011c4c6e15b294f8afd2913e"
GENERATED_AT = "2026-08-10T04:42:06.419608+00:00"


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
    audiences: StrictStr | None = Field(None, description="A list of audiences that the OpenID Issuer may include that are accepted in addition to 'client-id'.")
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

class DeleteAccessDomainsRealmResponse(RootModel[None]):
    """Model for delete. Delete an authentication server. response."""
    root: None = Field(...)

class GetAccessDomainsRealmResponse(RootModel[dict[str, object]]):
    """Model for read. Get auth server configuration. response."""
    root: dict[str, object] = Field(...)

class PutAccessDomainsRealmRequest(ProxmoxBaseModel):
    """Model for update. Update authentication server settings. request."""
    acr_values: StrictStr | None = Field(None, alias="acr-values", description='Specifies the Authentication Context Class Reference values that theAuthorization Server is being requested to use for the Auth Request.')
    audiences: StrictStr | None = Field(None, description="A list of audiences that the OpenID Issuer may include that are accepted in addition to 'client-id'.")
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
    """Model for update_token_info. Update API token for a specific user. NOTE: when 'regenerate' is set, the returned token value needs to be stored as it cannot be retrieved afterwards! request."""
    comment: StrictStr | None = Field(None)
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')
    regenerate: bool | None = Field(None, description="Regenerate the token's secret value. All users of the previous secret will lose access after this operation.")

class PutAccessUsersUseridTokenTokenidResponse(ProxmoxBaseModel):
    """Model for update_token_info. Update API token for a specific user. NOTE: when 'regenerate' is set, the returned token value needs to be stored as it cannot be retrieved afterwards! response."""
    comment: StrictStr | None = Field(None)
    expire: int | None = Field(None, description="API token expiration date (seconds since epoch). '0' means no expiration date.")
    full_tokenid: StrictStr | None = Field(None, alias="full-tokenid", description="The full token id. Only set when 'regenerate' was set.")
    privsep: bool | None = Field(None, description='Restrict API token privileges with separate ACLs (default), or give full privileges of corresponding user.')
    value: StrictStr | None = Field(None, description="API token value used for authentication. Only set when 'regenerate' was set.")

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
