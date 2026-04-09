"""Generated Pydantic v2 schemas from Proxmox OpenAPI output."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, RootModel


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')

class GetRootResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetAccessResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetAccessAclResponseItem(ProxmoxBaseModel):
    """Model for None. Read Access Control List (ACLs). response."""
    path: str | None = Field(None, description='Access control path.')
    propagate: bool | None = Field(None, description='Allow to propagate (inherit) permissions.')
    roleid: str | None = Field(None, description='Enum representing roles via their [PRIVILEGES] combination.\n\nSince privileges are implemented as bitflags, each unique combination of privileges maps to a\nsingle, unique `u64` value that is used in this enum definition.')
    ugid: str | None = Field(None, description='User or Group ID.')
    ugid_type: str | None = Field(None, description="Type of 'ugid' property.")

class GetAccessAclResponse(RootModel[list[GetAccessAclResponseItem]]):
    """List of items. None. Read Access Control List (ACLs). response."""
    root: list[GetAccessAclResponseItem] = Field(..., description='ACL entry list.')

class PutAccessAclRequest(ProxmoxBaseModel):
    """Model for None. Update Access Control List (ACLs). request."""
    auth_id: str | None = Field(None, alias="auth-id", description='Authentication ID')
    delete: bool | None = Field(None, description='Remove permissions (instead of adding it).')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    group: str | None = Field(None, description='Group ID')
    path: str = Field(..., description='Access control path.')
    propagate: bool | None = Field(None, description='Allow to propagate (inherit) permissions.')
    role: str = Field(..., description='Enum representing roles via their [PRIVILEGES] combination.\n\nSince privileges are implemented as bitflags, each unique combination of privileges maps to a\nsingle, unique `u64` value that is used in this enum definition.')

class PutAccessAclResponse(RootModel[None]):
    """Model for None. Update Access Control List (ACLs). response."""
    root: None = Field(...)

class GetAccessDomainsResponseItem(ProxmoxBaseModel):
    """Model for None. Authentication domain/realm index. response."""
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if it is the default realm')
    realm: str | None = Field(None, description='Realm name.')
    type: str | None = Field(None, description='type of the realm')

class GetAccessDomainsResponse(RootModel[list[GetAccessDomainsResponseItem]]):
    """List of items. None. Authentication domain/realm index. response."""
    root: list[GetAccessDomainsResponseItem] = Field(..., description='List of realms with basic info.')

class PostAccessDomainsRealmSyncRequest(ProxmoxBaseModel):
    """Model for None. Synchronize users of a given realm request."""
    dry_run: bool | None = Field(None, alias="dry-run", description='If set, do not create/delete anything')
    enable_new: bool | None = Field(None, alias="enable-new", description='Enable newly synced users immediately')
    remove_vanished: str | None = Field(None, alias="remove-vanished", description='A semicolon-separated list of things to remove when they or the user vanishes during user synchronization. The following values are possible: ``entry`` removes the user when not returned from the sync; ``properties`` removes any  properties on existing user that do not appear in the source. ``acl`` removes ACLs when the user is not returned from the sync.')

class PostAccessDomainsRealmSyncResponse(RootModel[str]):
    """Model for None. Synchronize users of a given realm response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetAccessOpenidResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostAccessOpenidAuthUrlRequest(ProxmoxBaseModel):
    """Model for None. Create OpenID Redirect Session request."""
    realm: str = Field(..., description='Realm name.')
    redirect_url: str = Field(..., alias="redirect-url", description='Redirection Url. The client should set this to used server url.')

class PostAccessOpenidAuthUrlResponse(RootModel[str]):
    """Model for None. Create OpenID Redirect Session response."""
    root: str = Field(..., description='Redirection URL.')

class PostAccessOpenidLoginRequest(ProxmoxBaseModel):
    """Model for None. Get a new ticket as an HttpOnly cookie. Supports tickets via cookies. request."""
    code: str = Field(..., description='OpenId authorization code.')
    http_only: bool | None = Field(None, alias="http-only", description='Whether the HttpOnly authentication flow should be used.')
    redirect_url: str = Field(..., alias="redirect-url", description='Redirection Url. The client should set this to used server url.')
    state: str = Field(..., description='OpenId state.')

class PostAccessOpenidLoginResponse(ProxmoxBaseModel):
    """Model for None. Get a new ticket as an HttpOnly cookie. Supports tickets via cookies. response."""
    csrfprevention_token: str = Field(..., alias="CSRFPreventionToken", description='Cross Site Request Forgery Prevention Token.')
    ticket: str | None = Field(None, description='Auth ticket, present if http-only was not provided or is false.')
    ticket_info: str | None = Field(None, alias="ticket-info", description='Informational ticket, can only be used to check if the ticket is expired. Present if http-only was true.')
    username: str = Field(..., description='User name.')

class PutAccessPasswordRequest(ProxmoxBaseModel):
    """Model for None. Change user password

Each user is allowed to change his own password. Superuser
can change all passwords. request."""
    confirmation_password: str | None = Field(None, alias="confirmation-password", description='The current password for confirmation, unless logged in as root@pam')
    password: str = Field(..., description='User Password.')
    userid: str = Field(..., description='User ID')

class PutAccessPasswordResponse(RootModel[None]):
    """Model for None. Change user password

Each user is allowed to change his own password. Superuser
can change all passwords. response."""
    root: None = Field(...)

class GetAccessPermissionsResponse(RootModel[dict[str, object]]):
    """Model for None. List permissions of given or currently authenticated user / API token.

Optionally limited to specific path. response."""
    root: dict[str, object] = Field(...)

class GetAccessRolesResponseItem(ProxmoxBaseModel):
    """Model for None. Role list response."""
    comment: str | None = Field(None, description='Comment.')
    privs: list[str] | None = Field(None, description='List of Privileges')
    roleid: str | None = Field(None, description='Enum representing roles via their [PRIVILEGES] combination.\n\nSince privileges are implemented as bitflags, each unique combination of privileges maps to a\nsingle, unique `u64` value that is used in this enum definition.')

class GetAccessRolesResponse(RootModel[list[GetAccessRolesResponseItem]]):
    """List of items. None. Role list response."""
    root: list[GetAccessRolesResponseItem] = Field(..., description='List of roles.')

class GetAccessTfaResponseItem(ProxmoxBaseModel):
    """Model for None. List user TFA configuration. response."""
    entries: list[dict[str, object]] | None = Field(None, description='TFA entries.')
    tfa_locked_until: int | None = Field(None, alias="tfa-locked-until", description="If a user's second factor is blocked, this contains the block's expiration time.")
    totp_locked: bool | None = Field(None, alias="totp-locked", description='The user is locked out of TOTP authentication.')
    userid: str | None = Field(None, description='The user this entry belongs to.')

class GetAccessTfaResponse(RootModel[list[GetAccessTfaResponseItem]]):
    """List of items. None. List user TFA configuration. response."""
    root: list[GetAccessTfaResponseItem] = Field(..., description='The list tuples of user and TFA entries.')

class GetAccessTfaUseridResponseItem(ProxmoxBaseModel):
    """Model for None. Add a TOTP secret to the user. response."""
    created: int | None = Field(None, description='Creation time of this entry as unix epoch.')
    description: str | None = Field(None, description='User chosen description for this entry.')
    enable: bool | None = Field(None, description='Whether this TFA entry is currently enabled.')
    id: str | None = Field(None, description='The id used to reference this entry.')
    type: str | None = Field(None, description='A TFA entry type.')

class GetAccessTfaUseridResponse(RootModel[list[GetAccessTfaUseridResponseItem]]):
    """List of items. None. Add a TOTP secret to the user. response."""
    root: list[GetAccessTfaUseridResponseItem] = Field(..., description='The list of TFA entries.')

class PostAccessTfaUseridRequest(ProxmoxBaseModel):
    """Model for None. Add a TFA entry to the user. request."""
    challenge: str | None = Field(None, description='When responding to a u2f challenge: the original challenge string')
    description: str | None = Field(None, description='A description to distinguish multiple entries from one another')
    password: str | None = Field(None, description='Password.')
    totp: str | None = Field(None, description='A totp URI.')
    type: str = Field(..., description='A TFA entry type.')
    value: str | None = Field(None, description='The current value for the provided totp URI, or a Webauthn/U2F challenge response')

class PostAccessTfaUseridResponse(ProxmoxBaseModel):
    """Model for None. Add a TFA entry to the user. response."""
    challenge: str | None = Field(None, description='When adding u2f entries, this contains a challenge the user must respond to in order to\nfinish the registration.')
    id: str | None = Field(None, description='The id if a newly added TFA entry.')
    recovery: list[int] = Field(..., description='A list of recovery codes as integers.')

class DeleteAccessTfaUseridIdRequest(ProxmoxBaseModel):
    """Model for None. Delete a single TFA entry. request."""
    password: str | None = Field(None, description='Password.')

class DeleteAccessTfaUseridIdResponse(RootModel[None]):
    """Model for None. Delete a single TFA entry. response."""
    root: None = Field(...)

class GetAccessTfaUseridIdResponse(RootModel[None]):
    """Model for None. Get a single TFA entry. response."""
    root: None = Field(...)

class PutAccessTfaUseridIdRequest(ProxmoxBaseModel):
    """Model for None. Update user's TFA entry description. request."""
    description: str | None = Field(None, description='A description to distinguish multiple entries from one another')
    enable: bool | None = Field(None, description='Whether this entry should currently be enabled or disabled')
    password: str | None = Field(None, description='Password.')

class PutAccessTfaUseridIdResponse(RootModel[None]):
    """Model for None. Update user's TFA entry description. response."""
    root: None = Field(...)

class DeleteAccessTicketResponse(RootModel[None]):
    root: None = Field(...)

class PostAccessTicketRequest(ProxmoxBaseModel):
    """Model for None. Either create a new HttpOnly ticket or a regular ticket. request."""
    http_only: bool | None = Field(None, alias="http-only", description='Whether the HttpOnly authentication flow should be used.')
    password: str | None = Field(None, description='The secret password. This can also be a valid ticket. Only optional if the ticket is\nprovided in a cookie header and only if the endpoint supports this.')
    path: str | None = Field(None, description="Verify ticket, and check if user have access 'privs' on 'path'.")
    port: int | None = Field(None, description='Port for verifying terminal tickets.')
    privs: str | None = Field(None, description="Verify ticket, and check if user have access 'privs' on 'path'.")
    tfa_challenge: str | None = Field(None, alias="tfa-challenge", description='The signed TFA challenge string the user wants to respond to.')
    username: str = Field(..., description='User ID')

class PostAccessTicketResponse(ProxmoxBaseModel):
    """Model for None. Either create a new HttpOnly ticket or a regular ticket. response."""
    csrfprevention_token: str | None = Field(None, alias="CSRFPreventionToken", description='The CSRF prevention token.')
    ticket: str | None = Field(None, description='The ticket as is supposed to be used in the authentication header. Not provided here if the\nendpoint uses HttpOnly cookies to supply the actual ticket.')
    ticket_info: str | None = Field(None, alias="ticket-info", description='Like a full ticket, except the signature is missing. Useful in HttpOnly-contexts\n(browsers).')
    username: str = Field(..., description='User ID')

class GetAccessUsersResponseItem(ProxmoxBaseModel):
    """Model for None. List users response."""
    comment: str | None = Field(None, description='Comment.')
    email: str | None = Field(None, description='E-Mail Address.')
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account.")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: str | None = Field(None, description='First name.')
    lastname: str | None = Field(None, description='Last name.')
    tfa_locked_until: int | None = Field(None, alias="tfa-locked-until", description='Contains a timestamp until when a user is locked out of 2nd factors')
    tokens: list[dict[str, object]] | None = Field(None, description="List of user's API tokens.")
    totp_locked: bool | None = Field(None, alias="totp-locked", description='True if the user is currently locked out of TOTP factors')
    userid: str | None = Field(None, description='User ID')

class GetAccessUsersResponse(RootModel[list[GetAccessUsersResponseItem]]):
    """List of items. None. List users response."""
    root: list[GetAccessUsersResponseItem] = Field(..., description='List users (with config digest).')

class PostAccessUsersRequest(ProxmoxBaseModel):
    """Model for None. Create new user. request."""
    comment: str | None = Field(None, description='Comment.')
    email: str | None = Field(None, description='E-Mail Address.')
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account.")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: str | None = Field(None, description='First name.')
    lastname: str | None = Field(None, description='Last name.')
    password: str | None = Field(None, description='User Password.')
    userid: str = Field(..., description='User ID')

class PostAccessUsersResponse(RootModel[None]):
    """Model for None. Create new user. response."""
    root: None = Field(...)

class DeleteAccessUsersUseridRequest(ProxmoxBaseModel):
    """Model for None. Remove a user from the configuration file. request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteAccessUsersUseridResponse(RootModel[None]):
    """Model for None. Remove a user from the configuration file. response."""
    root: None = Field(...)

class GetAccessUsersUseridResponse(ProxmoxBaseModel):
    """Model for None. Read user configuration data. response."""
    comment: str | None = Field(None, description='Comment.')
    email: str | None = Field(None, description='E-Mail Address.')
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account.")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: str | None = Field(None, description='First name.')
    lastname: str | None = Field(None, description='Last name.')
    userid: str = Field(..., description='User ID')

class PutAccessUsersUseridRequest(ProxmoxBaseModel):
    """Model for None. Update user configuration. To change a user's password use the 'PUT /access/password' endpoint. request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    email: str | None = Field(None, description='E-Mail Address.')
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account.")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    firstname: str | None = Field(None, description='First name.')
    lastname: str | None = Field(None, description='Last name.')
    password: str | None = Field(None, description="This parameter is ignored, please use 'PUT /access/password' to change a user's password")

class PutAccessUsersUseridResponse(RootModel[None]):
    """Model for None. Update user configuration. To change a user's password use the 'PUT /access/password' endpoint. response."""
    root: None = Field(...)

class GetAccessUsersUseridTokenResponseItem(ProxmoxBaseModel):
    """Model for None. List user's API tokens response."""
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account.")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    token_name: str | None = Field(None, alias="token-name", description='The token ID part of an API token authentication id.\n\nThis alone does NOT uniquely identify the API token - use a full `Authid` for such use cases.')
    tokenid: str | None = Field(None, description='API Token ID')

class GetAccessUsersUseridTokenResponse(RootModel[list[GetAccessUsersUseridTokenResponseItem]]):
    """List of items. None. List user's API tokens response."""
    root: list[GetAccessUsersUseridTokenResponseItem] = Field(..., description="List user's API tokens (with config digest).")

class DeleteAccessUsersUseridTokenTokenNameRequest(ProxmoxBaseModel):
    """Model for None. Delete a user's API token request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteAccessUsersUseridTokenTokenNameResponse(RootModel[None]):
    """Model for None. Delete a user's API token response."""
    root: None = Field(...)

class GetAccessUsersUseridTokenTokenNameResponse(ProxmoxBaseModel):
    """Model for None. Read user's API token metadata response."""
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account.")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    tokenid: str = Field(..., description='API Token ID')

class PostAccessUsersUseridTokenTokenNameRequest(ProxmoxBaseModel):
    """Model for None. Generate a new API token with given metadata request."""
    comment: str | None = Field(None, description='Comment.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account.")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")

class PostAccessUsersUseridTokenTokenNameResponse(ProxmoxBaseModel):
    """Model for None. Generate a new API token with given metadata response."""
    tokenid: str = Field(..., description='The API token identifier')
    value: str = Field(..., description='The API token secret')

class PutAccessUsersUseridTokenTokenNameRequest(ProxmoxBaseModel):
    """Model for None. Update user's API token metadata request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description="Enable the account (default). You can set this to '0' to disable the account.")
    expire: int | None = Field(None, description="Account expiration date (seconds since epoch). '0' means no expiration date.")
    regenerate: bool | None = Field(None, description='Regenerate token secret while keeping permissions.')

class PutAccessUsersUseridTokenTokenNameResponse(ProxmoxBaseModel):
    """Model for None. Update user's API token metadata response."""
    secret: str | None = Field(None, description='The new API token secret')

class PutAccessUsersUseridUnlockTfaRequest(RootModel[dict[str, object]]):
    """Model for None. Unlock a user's TFA authentication. request."""
    root: dict[str, object] = Field(...)

class PutAccessUsersUseridUnlockTfaResponse(RootModel[bool]):
    """Model for None. Unlock a user's TFA authentication. response."""
    root: bool = Field(..., description='Whether the user was previously locked out of any 2nd factor.')

class PostAccessVncticketRequest(ProxmoxBaseModel):
    """Model for None. Verify that a VNC ticket is valid for a given Authid, path and privilege(s). request."""
    authid: str = Field(..., description='Authentication ID')
    path: str = Field(..., description="Verify ticket, and check if user have access 'privs' on 'path'.")
    port: int | None = Field(None, description='Port for verifying terminal tickets.')
    privs: str = Field(..., description="Verify ticket, and check if user have access 'privs' on 'path'.")
    vncticket: str = Field(..., description='The VNC ticket')

class PostAccessVncticketResponse(RootModel[None]):
    """Model for None. Verify that a VNC ticket is valid for a given Authid, path and privilege(s). response."""
    root: None = Field(...)

class GetAdminResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetAdminDatastoreResponseItem(ProxmoxBaseModel):
    """Model for None. Datastore list response."""
    comment: str | None = Field(None, description='Comment.')
    maintenance: str | None = Field(None, description='If the datastore is in maintenance mode, information about it')
    mount_status: str | None = Field(None, alias="mount-status", description='Current mounting status of a datastore, useful for removable datastores.')
    store: str | None = Field(None, description='Datastore name.')

class GetAdminDatastoreResponse(RootModel[list[GetAdminDatastoreResponseItem]]):
    """List of items. None. Datastore list response."""
    root: list[GetAdminDatastoreResponseItem] = Field(..., description='List the accessible datastores.')

class GetAdminDatastoreStoreResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetAdminDatastoreStoreActiveOperationsResponse(RootModel[None]):
    """Model for None. Read datastore stats response."""
    root: None = Field(...)

class GetAdminDatastoreStoreCatalogResponse(RootModel[None]):
    """Model for None. Get the entries of the given path of the catalog response."""
    root: None = Field(...)

class PostAdminDatastoreStoreChangeOwnerRequest(ProxmoxBaseModel):
    """Model for None. Change owner of a backup group request."""
    backup_id: str = Field(..., alias="backup-id", description='Backup ID.')
    backup_type: str = Field(..., alias="backup-type", description='Backup types.')
    new_owner: str = Field(..., alias="new-owner", description='Authentication ID')
    ns: str | None = Field(None, description='Namespace.')

class PostAdminDatastoreStoreChangeOwnerResponse(RootModel[None]):
    """Model for None. Change owner of a backup group response."""
    root: None = Field(...)

class GetAdminDatastoreStoreDownloadResponse(RootModel[None]):
    """Model for None. Download single raw file from backup snapshot. response."""
    root: None = Field(...)

class GetAdminDatastoreStoreDownloadDecodedResponse(RootModel[None]):
    """Model for None. Download single decoded file from backup snapshot. Only works if it's not encrypted. response."""
    root: None = Field(...)

class GetAdminDatastoreStoreFilesResponseItem(ProxmoxBaseModel):
    """Model for None. List snapshot files. response."""
    crypt_mode: str | None = Field(None, alias="crypt-mode", description='Defines whether data is encrypted (using an AEAD cipher), only signed, or neither.')
    filename: str | None = Field(None, description='Backup archive name.')
    size: int | None = Field(None, description='Archive size (from backup manifest).')

class GetAdminDatastoreStoreFilesResponse(RootModel[list[GetAdminDatastoreStoreFilesResponseItem]]):
    """List of items. None. List snapshot files. response."""
    root: list[GetAdminDatastoreStoreFilesResponseItem] = Field(..., description='Returns the list of archive files inside a backup snapshots.')

class GetAdminDatastoreStoreGcResponse(ProxmoxBaseModel):
    """Model for None. Garbage collection status. response."""
    cache_stats: dict[str, object] | None = Field(None, alias="cache-stats", description='Garbage collection cache statistics')
    disk_bytes: int = Field(..., alias="disk-bytes", description='Bytes used on disk.')
    disk_chunks: int = Field(..., alias="disk-chunks", description='Chunks used on disk.')
    duration: int | None = Field(None, description='Duration of last gc run')
    index_data_bytes: int = Field(..., alias="index-data-bytes", description='Sum of bytes referred by index files.')
    index_file_count: int = Field(..., alias="index-file-count", description='Number of processed index files.')
    last_run_endtime: int | None = Field(None, alias="last-run-endtime", description='Endtime of the last gc run')
    last_run_state: str | None = Field(None, alias="last-run-state", description='State of the last gc run')
    next_run: int | None = Field(None, alias="next-run", description='Time of the next gc run')
    pending_bytes: int = Field(..., alias="pending-bytes", description='Sum of pending bytes (pending removal - kept for safety).')
    pending_chunks: int = Field(..., alias="pending-chunks", description='Number of pending chunks (pending removal - kept for safety).')
    removed_bad: int = Field(..., alias="removed-bad", description='Number of chunks marked as .bad by verify that have been removed by GC.')
    removed_bytes: int = Field(..., alias="removed-bytes", description='Sum of removed bytes.')
    removed_chunks: int = Field(..., alias="removed-chunks", description='Number of removed chunks.')
    schedule: str | None = Field(None, description='Schedule of the gc job')
    still_bad: int = Field(..., alias="still-bad", description='Number of chunks still marked as .bad after garbage collection.')
    store: str = Field(..., description='Datastore')
    upid: str | None = Field(None, description='Unique Process/Task Identifier')

class PostAdminDatastoreStoreGcRequest(RootModel[dict[str, object]]):
    """Model for None. Start garbage collection. request."""
    root: dict[str, object] = Field(...)

class PostAdminDatastoreStoreGcResponse(RootModel[str]):
    """Model for None. Start garbage collection. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetAdminDatastoreStoreGroupNotesResponse(RootModel[None]):
    """Model for None. Get "notes" for a backup group response."""
    root: None = Field(...)

class PutAdminDatastoreStoreGroupNotesRequest(ProxmoxBaseModel):
    """Model for None. Set "notes" for a backup group request."""
    backup_id: str = Field(..., alias="backup-id", description='Backup ID.')
    backup_type: str = Field(..., alias="backup-type", description='Backup types.')
    notes: str = Field(..., description='A multiline text.')
    ns: str | None = Field(None, description='Namespace.')

class PutAdminDatastoreStoreGroupNotesResponse(RootModel[None]):
    """Model for None. Set "notes" for a backup group response."""
    root: None = Field(...)

class DeleteAdminDatastoreStoreGroupsRequest(ProxmoxBaseModel):
    """Model for None. Delete backup group including all snapshots. request."""
    backup_id: str = Field(..., alias="backup-id", description='Backup ID.')
    backup_type: str = Field(..., alias="backup-type", description='Backup types.')
    error_on_protected: bool | None = Field(None, alias="error-on-protected", description='Return error when group cannot be deleted because of protected snapshots')
    ns: str | None = Field(None, description='Namespace.')

class DeleteAdminDatastoreStoreGroupsResponse(ProxmoxBaseModel):
    """Model for None. Delete backup group including all snapshots. response."""
    protected_snapshots: int = Field(..., alias="protected-snapshots", description='Number of entities')
    removed_groups: int = Field(..., alias="removed-groups", description='Number of entities')
    removed_snapshots: int = Field(..., alias="removed-snapshots", description='Number of entities')

class GetAdminDatastoreStoreGroupsResponseItem(ProxmoxBaseModel):
    """Model for None. List backup groups. response."""
    backup_count: int | None = Field(None, alias="backup-count", description='Number of contained snapshots')
    backup_id: str | None = Field(None, alias="backup-id", description='Backup ID.')
    backup_type: str | None = Field(None, alias="backup-type", description='Backup types.')
    comment: str | None = Field(None, description='The first line from group "notes"')
    files: list[str] | None = Field(None, description='List of contained archive files.')
    last_backup: int | None = Field(None, alias="last-backup", description='Backup time (Unix epoch.)')
    owner: str | None = Field(None, description='Authentication ID')

class GetAdminDatastoreStoreGroupsResponse(RootModel[list[GetAdminDatastoreStoreGroupsResponseItem]]):
    """List of items. None. List backup groups. response."""
    root: list[GetAdminDatastoreStoreGroupsResponseItem] = Field(..., description='Returns the list of backup groups.')

class PostAdminDatastoreStoreMountRequest(RootModel[dict[str, object]]):
    """Model for None. Mount removable datastore. request."""
    root: dict[str, object] = Field(...)

class PostAdminDatastoreStoreMountResponse(RootModel[str]):
    """Model for None. Mount removable datastore. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class DeleteAdminDatastoreStoreNamespaceRequest(ProxmoxBaseModel):
    """Model for None. Delete a backup namespace including all snapshots. request."""
    delete_groups: bool | None = Field(None, alias="delete-groups", description='If set, all groups will be destroyed in the whole hierarchy below andincluding `ns`. If not set, only empty namespaces will be pruned.')
    error_on_protected: bool | None = Field(None, alias="error-on-protected", description='Return error when namespace cannot be deleted because of protected snapshots')
    ns: str = Field(..., description='Namespace.')

class DeleteAdminDatastoreStoreNamespaceResponse(RootModel[None]):
    """Model for None. Delete a backup namespace including all snapshots. response."""
    root: None = Field(...)

class GetAdminDatastoreStoreNamespaceResponseItem(ProxmoxBaseModel):
    """Model for None. List the namespaces of a datastore. response."""
    comment: str | None = Field(None, description='The first line from the namespace\'s "notes"')
    ns: str | None = Field(None, description='Namespace.')

class GetAdminDatastoreStoreNamespaceResponse(RootModel[list[GetAdminDatastoreStoreNamespaceResponseItem]]):
    """List of items. None. List the namespaces of a datastore. response."""
    root: list[GetAdminDatastoreStoreNamespaceResponseItem] = Field(..., description='Returns the list of backup namespaces.')

class PostAdminDatastoreStoreNamespaceRequest(ProxmoxBaseModel):
    """Model for None. Create a new datastore namespace. request."""
    name: str = Field(..., description='The name of the new namespace to add at the parent.')
    parent: str | None = Field(None, description='Namespace.')

class PostAdminDatastoreStoreNamespaceResponse(RootModel[str]):
    """Model for None. Create a new datastore namespace. response."""
    root: str = Field(..., description='Namespace.')

class GetAdminDatastoreStoreNotesResponse(RootModel[None]):
    """Model for None. Get "notes" for a specific backup response."""
    root: None = Field(...)

class PutAdminDatastoreStoreNotesRequest(ProxmoxBaseModel):
    """Model for None. Set "notes" for a specific backup request."""
    backup_id: str = Field(..., alias="backup-id", description='Backup ID.')
    backup_time: int = Field(..., alias="backup-time", description='Backup time (Unix epoch.)')
    backup_type: str = Field(..., alias="backup-type", description='Backup types.')
    notes: str = Field(..., description='A multiline text.')
    ns: str | None = Field(None, description='Namespace.')

class PutAdminDatastoreStoreNotesResponse(RootModel[None]):
    """Model for None. Set "notes" for a specific backup response."""
    root: None = Field(...)

class GetAdminDatastoreStoreProtectedResponse(RootModel[None]):
    """Model for None. Query protection for a specific backup response."""
    root: None = Field(...)

class PutAdminDatastoreStoreProtectedRequest(ProxmoxBaseModel):
    """Model for None. En- or disable protection for a specific backup request."""
    backup_id: str = Field(..., alias="backup-id", description='Backup ID.')
    backup_time: int = Field(..., alias="backup-time", description='Backup time (Unix epoch.)')
    backup_type: str = Field(..., alias="backup-type", description='Backup types.')
    ns: str | None = Field(None, description='Namespace.')
    protected: bool = Field(..., description='Enable/disable protection.')

class PutAdminDatastoreStoreProtectedResponse(RootModel[None]):
    """Model for None. En- or disable protection for a specific backup response."""
    root: None = Field(...)

class PostAdminDatastoreStorePruneRequest(ProxmoxBaseModel):
    """Model for None. Prune a group on the datastore request."""
    backup_id: str = Field(..., alias="backup-id", description='Backup ID.')
    backup_type: str = Field(..., alias="backup-type", description='Backup types.')
    dry_run: bool | None = Field(None, alias="dry-run", description='Just show what prune would do, but do not delete anything.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    ns: str | None = Field(None, description='Namespace.')
    use_task: bool | None = Field(None, alias="use-task", description='Spins up an asynchronous task that does the work.')

class PostAdminDatastoreStorePruneResponseItem(ProxmoxBaseModel):
    """Model for None. Prune a group on the datastore response."""
    backup_id: str | None = Field(None, alias="backup-id", description='Backup ID.')
    backup_time: int | None = Field(None, alias="backup-time", description='Backup time (Unix epoch.)')
    backup_type: str | None = Field(None, alias="backup-type", description='Backup types.')
    keep: bool | None = Field(None, description='Keep snapshot')

class PostAdminDatastoreStorePruneResponse(RootModel[list[PostAdminDatastoreStorePruneResponseItem]]):
    """List of items. None. Prune a group on the datastore response."""
    root: list[PostAdminDatastoreStorePruneResponseItem] = Field(..., description='Returns the list of snapshots and a flag indicating if there are kept or removed.')

class PostAdminDatastoreStorePruneDatastoreRequest(ProxmoxBaseModel):
    """Model for None. Prune the datastore request."""
    dry_run: bool | None = Field(None, alias="dry-run", description='Just show what prune would do, but do not delete anything.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')

class PostAdminDatastoreStorePruneDatastoreResponse(RootModel[str]):
    """Model for None. Prune the datastore response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetAdminDatastoreStorePxarFileDownloadResponse(RootModel[None]):
    """Model for None. Download single file from pxar file of a backup snapshot. Only works if it's not encrypted. response."""
    root: None = Field(...)

class GetAdminDatastoreStoreRrdResponse(RootModel[None]):
    """Model for None. Read datastore stats response."""
    root: None = Field(...)

class PutAdminDatastoreStoreS3RefreshRequest(RootModel[dict[str, object]]):
    """Model for None. Refresh datastore contents from S3 to local cache store. request."""
    root: dict[str, object] = Field(...)

class PutAdminDatastoreStoreS3RefreshResponse(RootModel[str]):
    """Model for None. Refresh datastore contents from S3 to local cache store. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class DeleteAdminDatastoreStoreSnapshotsRequest(ProxmoxBaseModel):
    """Model for None. Delete backup snapshot. request."""
    backup_id: str = Field(..., alias="backup-id", description='Backup ID.')
    backup_time: int = Field(..., alias="backup-time", description='Backup time (Unix epoch.)')
    backup_type: str = Field(..., alias="backup-type", description='Backup types.')
    ns: str | None = Field(None, description='Namespace.')

class DeleteAdminDatastoreStoreSnapshotsResponse(RootModel[None]):
    """Model for None. Delete backup snapshot. response."""
    root: None = Field(...)

class GetAdminDatastoreStoreSnapshotsResponseItem(ProxmoxBaseModel):
    """Model for None. List backup snapshots. response."""
    backup_id: str | None = Field(None, alias="backup-id", description='Backup ID.')
    backup_time: int | None = Field(None, alias="backup-time", description='Backup time (Unix epoch.)')
    backup_type: str | None = Field(None, alias="backup-type", description='Backup types.')
    comment: str | None = Field(None, description='Comment.')
    files: list[str] | None = Field(None, description='List of contained archive files.')
    fingerprint: str | None = Field(None, description='Fingerprint of encryption key')
    owner: str | None = Field(None, description='Authentication ID')
    protected: bool | None = Field(None, description='Protection from prunes')
    size: int | None = Field(None, description='Overall snapshot size (sum of all archive sizes).')
    verification: dict[str, object] | None = Field(None, description='Task properties.')

class GetAdminDatastoreStoreSnapshotsResponse(RootModel[list[GetAdminDatastoreStoreSnapshotsResponseItem]]):
    """List of items. None. List backup snapshots. response."""
    root: list[GetAdminDatastoreStoreSnapshotsResponseItem] = Field(..., description='Returns the list of snapshots.')

class GetAdminDatastoreStoreStatusResponse(ProxmoxBaseModel):
    """Model for None. Get datastore status. response."""
    avail: int = Field(..., description='Available space (bytes).')
    backend_type: str = Field(..., alias="backend-type", description='Datastore backend type')
    counts: dict[str, object] | None = Field(None, description='Counts of groups/snapshots per BackupType.')
    gc_status: dict[str, object] | None = Field(None, alias="gc-status", description='Garbage collection status.')
    total: int = Field(..., description='Total space (bytes).')
    used: int = Field(..., description='Used space (bytes).')

class PostAdminDatastoreStoreUnmountRequest(RootModel[dict[str, object]]):
    """Model for None. Unmount a removable device that is associated with the datastore request."""
    root: dict[str, object] = Field(...)

class PostAdminDatastoreStoreUnmountResponse(RootModel[str]):
    """Model for None. Unmount a removable device that is associated with the datastore response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class PostAdminDatastoreStoreUploadBackupLogRequest(ProxmoxBaseModel):
    """Model for None. Upload the client backup log file into a backup snapshot ('client.log.blob'). request."""
    backup_id: str = Field(..., alias="backup-id", description='Backup ID.')
    backup_time: int = Field(..., alias="backup-time", description='Backup time (Unix epoch.)')
    backup_type: str = Field(..., alias="backup-type", description='Backup type.')
    ns: str | None = Field(None, description='Namespace.')

class PostAdminDatastoreStoreUploadBackupLogResponse(RootModel[None]):
    """Model for None. Upload the client backup log file into a backup snapshot ('client.log.blob'). response."""
    root: None = Field(...)

class PostAdminDatastoreStoreVerifyRequest(ProxmoxBaseModel):
    """Model for None. Verify backups.

This function can verify a single backup snapshot, all backups from a backup group,
or all backups in the datastore. request."""
    backup_id: str | None = Field(None, alias="backup-id", description='Backup ID.')
    backup_time: int | None = Field(None, alias="backup-time", description='Backup time (Unix epoch.)')
    backup_type: str | None = Field(None, alias="backup-type", description='Backup types.')
    ignore_verified: bool | None = Field(None, alias="ignore-verified", description='Do not verify backups that are already verified if their verification is not outdated.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    ns: str | None = Field(None, description='Namespace.')
    outdated_after: int | None = Field(None, alias="outdated-after", description="Days after that a verification becomes outdated. (0 is deprecated)'")
    read_threads: int | None = Field(None, alias="read-threads", description='The number of threads to use for reading chunks in verify job.')
    verify_threads: int | None = Field(None, alias="verify-threads", description='The number of threads to use for verifying chunks in verify job.')

class PostAdminDatastoreStoreVerifyResponse(RootModel[str]):
    """Model for None. Verify backups.

This function can verify a single backup snapshot, all backups from a backup group,
or all backups in the datastore. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetAdminGcResponseItem(ProxmoxBaseModel):
    """Model for None. List all GC jobs (max one per datastore) response."""
    cache_stats: dict[str, object] | None = Field(None, alias="cache-stats", description='Garbage collection cache statistics')
    disk_bytes: int | None = Field(None, alias="disk-bytes", description='Bytes used on disk.')
    disk_chunks: int | None = Field(None, alias="disk-chunks", description='Chunks used on disk.')
    duration: int | None = Field(None, description='Duration of last gc run')
    index_data_bytes: int | None = Field(None, alias="index-data-bytes", description='Sum of bytes referred by index files.')
    index_file_count: int | None = Field(None, alias="index-file-count", description='Number of processed index files.')
    last_run_endtime: int | None = Field(None, alias="last-run-endtime", description='Endtime of the last gc run')
    last_run_state: str | None = Field(None, alias="last-run-state", description='State of the last gc run')
    next_run: int | None = Field(None, alias="next-run", description='Time of the next gc run')
    pending_bytes: int | None = Field(None, alias="pending-bytes", description='Sum of pending bytes (pending removal - kept for safety).')
    pending_chunks: int | None = Field(None, alias="pending-chunks", description='Number of pending chunks (pending removal - kept for safety).')
    removed_bad: int | None = Field(None, alias="removed-bad", description='Number of chunks marked as .bad by verify that have been removed by GC.')
    removed_bytes: int | None = Field(None, alias="removed-bytes", description='Sum of removed bytes.')
    removed_chunks: int | None = Field(None, alias="removed-chunks", description='Number of removed chunks.')
    schedule: str | None = Field(None, description='Schedule of the gc job')
    still_bad: int | None = Field(None, alias="still-bad", description='Number of chunks still marked as .bad after garbage collection.')
    store: str | None = Field(None, description='Datastore')
    upid: str | None = Field(None, description='Unique Process/Task Identifier')

class GetAdminGcResponse(RootModel[list[GetAdminGcResponseItem]]):
    """List of items. None. List all GC jobs (max one per datastore) response."""
    root: list[GetAdminGcResponseItem] = Field(..., description='List configured gc jobs and their status')

class GetAdminGcStoreResponseItem(ProxmoxBaseModel):
    """Model for None. List all GC jobs (max one per datastore) response."""
    cache_stats: dict[str, object] | None = Field(None, alias="cache-stats", description='Garbage collection cache statistics')
    disk_bytes: int | None = Field(None, alias="disk-bytes", description='Bytes used on disk.')
    disk_chunks: int | None = Field(None, alias="disk-chunks", description='Chunks used on disk.')
    duration: int | None = Field(None, description='Duration of last gc run')
    index_data_bytes: int | None = Field(None, alias="index-data-bytes", description='Sum of bytes referred by index files.')
    index_file_count: int | None = Field(None, alias="index-file-count", description='Number of processed index files.')
    last_run_endtime: int | None = Field(None, alias="last-run-endtime", description='Endtime of the last gc run')
    last_run_state: str | None = Field(None, alias="last-run-state", description='State of the last gc run')
    next_run: int | None = Field(None, alias="next-run", description='Time of the next gc run')
    pending_bytes: int | None = Field(None, alias="pending-bytes", description='Sum of pending bytes (pending removal - kept for safety).')
    pending_chunks: int | None = Field(None, alias="pending-chunks", description='Number of pending chunks (pending removal - kept for safety).')
    removed_bad: int | None = Field(None, alias="removed-bad", description='Number of chunks marked as .bad by verify that have been removed by GC.')
    removed_bytes: int | None = Field(None, alias="removed-bytes", description='Sum of removed bytes.')
    removed_chunks: int | None = Field(None, alias="removed-chunks", description='Number of removed chunks.')
    schedule: str | None = Field(None, description='Schedule of the gc job')
    still_bad: int | None = Field(None, alias="still-bad", description='Number of chunks still marked as .bad after garbage collection.')
    store: str | None = Field(None, description='Datastore')
    upid: str | None = Field(None, description='Unique Process/Task Identifier')

class GetAdminGcStoreResponse(RootModel[list[GetAdminGcStoreResponseItem]]):
    """List of items. None. List all GC jobs (max one per datastore) response."""
    root: list[GetAdminGcStoreResponseItem] = Field(..., description='List configured gc jobs and their status')

class GetAdminMetricsResponseItem(ProxmoxBaseModel):
    """Model for None. List configured metric servers. response."""
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    name: str | None = Field(None, description='Metrics Server ID.')
    server: str | None = Field(None, description='The target server')
    type: str | None = Field(None, description='Type of the metric server')

class GetAdminMetricsResponse(RootModel[list[GetAdminMetricsResponseItem]]):
    """List of items. None. List configured metric servers. response."""
    root: list[GetAdminMetricsResponseItem] = Field(..., description='List of configured metric servers.')

class GetAdminPruneResponseItem(ProxmoxBaseModel):
    """Model for None. List all prune jobs response."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this job.')
    id: str | None = Field(None, description='Job ID.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    last_run_endtime: int | None = Field(None, alias="last-run-endtime", description='Endtime of the last run.')
    last_run_state: str | None = Field(None, alias="last-run-state", description='Result of the last run.')
    last_run_upid: str | None = Field(None, alias="last-run-upid", description='Task UPID of the last run.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    next_run: int | None = Field(None, alias="next-run", description='Estimated time of the next run (UNIX epoch).')
    ns: str | None = Field(None, description='Namespace.')
    schedule: str | None = Field(None, description='Run prune job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')

class GetAdminPruneResponse(RootModel[list[GetAdminPruneResponseItem]]):
    """List of items. None. List all prune jobs response."""
    root: list[GetAdminPruneResponseItem] = Field(..., description='List configured jobs and their status (filtered by access)')

class GetAdminPruneIdResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostAdminPruneIdRunRequest(RootModel[dict[str, object]]):
    """Model for None. Runs a prune job manually. request."""
    root: dict[str, object] = Field(...)

class PostAdminPruneIdRunResponse(RootModel[None]):
    """Model for None. Runs a prune job manually. response."""
    root: None = Field(...)

class GetAdminS3S3ClientIdResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PutAdminS3S3ClientIdCheckRequest(ProxmoxBaseModel):
    """Model for None. Perform basic sanity check for given s3 client configuration request."""
    bucket: str = Field(..., description='Bucket name for S3 object store.')
    store_prefix: str | None = Field(None, alias="store-prefix", description='Store prefix within bucket for S3 object keys (commonly datastore name)')

class PutAdminS3S3ClientIdCheckResponse(RootModel[None]):
    """Model for None. Perform basic sanity check for given s3 client configuration response."""
    root: None = Field(...)

class GetAdminSyncResponseItem(ProxmoxBaseModel):
    """Model for None. List all configured sync jobs response."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    encrypted_only: bool | None = Field(None, alias="encrypted-only", description='Only synchronize encrypted backup snapshots, exclude others.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    id: str | None = Field(None, description='Job ID.')
    last_run_endtime: int | None = Field(None, alias="last-run-endtime", description='Endtime of the last run.')
    last_run_state: str | None = Field(None, alias="last-run-state", description='Result of the last run.')
    last_run_upid: str | None = Field(None, alias="last-run-upid", description='Task UPID of the last run.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    next_run: int | None = Field(None, alias="next-run", description='Estimated time of the next run (UNIX epoch).')
    ns: str | None = Field(None, description='Namespace.')
    owner: str | None = Field(None, description='Authentication ID')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    remote: str | None = Field(None, description='Remote ID.')
    remote_ns: str | None = Field(None, alias="remote-ns", description='Namespace.')
    remote_store: str | None = Field(None, alias="remote-store", description='Datastore name.')
    remove_vanished: bool | None = Field(None, alias="remove-vanished", description='Delete vanished backups. This remove the local copy if the remote backup was deleted.')
    resync_corrupt: bool | None = Field(None, alias="resync-corrupt", description='If the verification failed for a local snapshot, try to pull it again.')
    run_on_mount: bool | None = Field(None, alias="run-on-mount", description='Run this job when a relevant datastore is mounted.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    sync_direction: str | None = Field(None, alias="sync-direction", description='Direction of the sync job, push or pull')
    transfer_last: int | None = Field(None, alias="transfer-last", description='Limit transfer to last N snapshots (per group), skipping others')
    unmount_on_done: bool | None = Field(None, alias="unmount-on-done", description="Unmount involved removable datastore after the sync job finishes. Requires 'run-on-mount' to be enabled.")
    verified_only: bool | None = Field(None, alias="verified-only", description='Only synchronize verified backup snapshots, exclude others.')

class GetAdminSyncResponse(RootModel[list[GetAdminSyncResponseItem]]):
    """List of items. None. List all configured sync jobs response."""
    root: list[GetAdminSyncResponseItem] = Field(..., description='List configured jobs and their status.')

class GetAdminSyncIdResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostAdminSyncIdRunRequest(RootModel[dict[str, object]]):
    """Model for None. Runs the sync jobs manually. request."""
    root: dict[str, object] = Field(...)

class PostAdminSyncIdRunResponse(RootModel[None]):
    """Model for None. Runs the sync jobs manually. response."""
    root: None = Field(...)

class GetAdminTrafficControlResponseItem(ProxmoxBaseModel):
    """Model for None. Show current traffic for all traffic control rules. response."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    cur_rate_in: int | None = Field(None, alias="cur-rate-in", description='Current ingress rate in bytes/second')
    cur_rate_out: int | None = Field(None, alias="cur-rate-out", description='Current egress rate in bytes/second')
    name: str | None = Field(None, description='Rule ID.')
    network: list[str] | None = Field(None, description='Rule applies to Source IPs within this networks')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    timeframe: list[str] | None = Field(None, description='Enable the rule at specific times')
    users: list[str] | None = Field(None, description='Rule applies to authenticated API requests of any of these users (overrides IP-only rules)')

class GetAdminTrafficControlResponse(RootModel[list[GetAdminTrafficControlResponseItem]]):
    """List of items. None. Show current traffic for all traffic control rules. response."""
    root: list[GetAdminTrafficControlResponseItem] = Field(..., description='Show current traffic control rates.')

class GetAdminVerifyResponseItem(ProxmoxBaseModel):
    """Model for None. List all verification jobs response."""
    comment: str | None = Field(None, description='Comment.')
    id: str | None = Field(None, description='Job ID.')
    ignore_verified: bool | None = Field(None, alias="ignore-verified", description='Do not verify backups that are already verified if their verification is not outdated.')
    last_run_endtime: int | None = Field(None, alias="last-run-endtime", description='Endtime of the last run.')
    last_run_state: str | None = Field(None, alias="last-run-state", description='Result of the last run.')
    last_run_upid: str | None = Field(None, alias="last-run-upid", description='Task UPID of the last run.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    next_run: int | None = Field(None, alias="next-run", description='Estimated time of the next run (UNIX epoch).')
    ns: str | None = Field(None, description='Namespace.')
    outdated_after: int | None = Field(None, alias="outdated-after", description="Days after that a verification becomes outdated. (0 is deprecated)'")
    read_threads: int | None = Field(None, alias="read-threads", description='The number of threads to use for reading chunks in verify job.')
    schedule: str | None = Field(None, description='Run verify job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    verify_threads: int | None = Field(None, alias="verify-threads", description='The number of threads to use for verifying chunks in verify job.')

class GetAdminVerifyResponse(RootModel[list[GetAdminVerifyResponseItem]]):
    """List of items. None. List all verification jobs response."""
    root: list[GetAdminVerifyResponseItem] = Field(..., description='List configured jobs and their status (filtered by access)')

class GetAdminVerifyIdResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostAdminVerifyIdRunRequest(RootModel[dict[str, object]]):
    """Model for None. Runs a verification job manually. request."""
    root: dict[str, object] = Field(...)

class PostAdminVerifyIdRunResponse(RootModel[None]):
    """Model for None. Runs a verification job manually. response."""
    root: None = Field(...)

class GetBackupResponse(RootModel[None]):
    """Model for None. Upgraded to backup protocol ('proxmox-backup-protocol-v1'). response."""
    root: None = Field(...)

class GetBackupUpgradeResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostBackupUpgradeBlobRequest(ProxmoxBaseModel):
    """Model for None. Upload binary blob file. request."""
    encoded_size: int = Field(..., alias="encoded-size", description='Encoded blob size.')
    file_name: str = Field(..., alias="file-name", description='Backup archive name.')

class PostBackupUpgradeBlobResponse(RootModel[None]):
    """Model for None. Upload binary blob file. response."""
    root: None = Field(...)

class PostBackupUpgradeDynamicChunkRequest(ProxmoxBaseModel):
    """Model for None. Upload a new chunk. request."""
    digest: str = Field(..., description='Chunk digest (SHA256).')
    encoded_size: int = Field(..., alias="encoded-size", description='Encoded chunk size.')
    size: int = Field(..., description='Chunk size.')
    wid: int = Field(..., description='Dynamic writer ID.')

class PostBackupUpgradeDynamicChunkResponse(RootModel[None]):
    """Model for None. Upload a new chunk. response."""
    root: None = Field(...)

class PostBackupUpgradeDynamicCloseRequest(ProxmoxBaseModel):
    """Model for None. Close dynamic index writer. request."""
    chunk_count: int = Field(..., alias="chunk-count", description='Chunk count. This is used to verify that the server got all chunks.')
    csum: str = Field(..., description='Digest list checksum.')
    size: int = Field(..., description='File size. This is used to verify that the server got all data.')
    wid: int = Field(..., description='Dynamic writer ID.')

class PostBackupUpgradeDynamicCloseResponse(RootModel[None]):
    """Model for None. Close dynamic index writer. response."""
    root: None = Field(...)

class PostBackupUpgradeDynamicIndexRequest(ProxmoxBaseModel):
    """Model for None. Create dynamic chunk index file. request."""
    archive_name: str = Field(..., alias="archive-name", description='Backup archive name.')

class PostBackupUpgradeDynamicIndexResponse(RootModel[None]):
    """Model for None. Create dynamic chunk index file. response."""
    root: None = Field(...)

class PutBackupUpgradeDynamicIndexRequest(ProxmoxBaseModel):
    """Model for None. Append chunk to dynamic index writer. request."""
    digest_list: list[str] = Field(..., alias="digest-list", description='Chunk digest list.')
    offset_list: list[int] = Field(..., alias="offset-list", description='Chunk offset list.')
    wid: int = Field(..., description='Dynamic writer ID.')

class PutBackupUpgradeDynamicIndexResponse(RootModel[None]):
    """Model for None. Append chunk to dynamic index writer. response."""
    root: None = Field(...)

class PostBackupUpgradeFinishResponse(RootModel[None]):
    """Model for None. Mark backup as finished. response."""
    root: None = Field(...)

class PostBackupUpgradeFixedChunkRequest(ProxmoxBaseModel):
    """Model for None. Upload a new chunk. request."""
    digest: str = Field(..., description='Chunk digest (SHA256).')
    encoded_size: int = Field(..., alias="encoded-size", description='Encoded chunk size.')
    size: int = Field(..., description='Chunk size.')
    wid: int = Field(..., description='Fixed writer ID.')

class PostBackupUpgradeFixedChunkResponse(RootModel[None]):
    """Model for None. Upload a new chunk. response."""
    root: None = Field(...)

class PostBackupUpgradeFixedCloseRequest(ProxmoxBaseModel):
    """Model for None. Close fixed index writer. request."""
    chunk_count: int = Field(..., alias="chunk-count", description='Number of new and re-indexed chunks. Used to verify that the server got all chunk digests.')
    csum: str = Field(..., description='Digest list checksum.')
    size: int = Field(..., description='File size. This is used to verify that the server got all data. Ignored for incremental backups.')
    wid: int = Field(..., description='Fixed writer ID.')

class PostBackupUpgradeFixedCloseResponse(RootModel[None]):
    """Model for None. Close fixed index writer. response."""
    root: None = Field(...)

class PostBackupUpgradeFixedIndexRequest(ProxmoxBaseModel):
    """Model for None. Create fixed chunk index file. request."""
    archive_name: str = Field(..., alias="archive-name", description='Backup archive name.')
    reuse_csum: str | None = Field(None, alias="reuse-csum", description="If set, compare last backup's csum and reuse index for incremental backup if it matches.")
    size: int | None = Field(None, description='File size.')

class PostBackupUpgradeFixedIndexResponse(RootModel[None]):
    """Model for None. Create fixed chunk index file. response."""
    root: None = Field(...)

class PutBackupUpgradeFixedIndexRequest(ProxmoxBaseModel):
    """Model for None. Append chunk to fixed index writer. request."""
    digest_list: list[str] = Field(..., alias="digest-list", description='Chunk digest list.')
    offset_list: list[int] = Field(..., alias="offset-list", description='Chunk offset list.')
    wid: int = Field(..., description='Fixed writer ID.')

class PutBackupUpgradeFixedIndexResponse(RootModel[None]):
    """Model for None. Append chunk to fixed index writer. response."""
    root: None = Field(...)

class GetBackupUpgradePreviousResponse(RootModel[None]):
    """Model for None. Download archive from previous backup. response."""
    root: None = Field(...)

class GetBackupUpgradePreviousBackupTimeResponse(RootModel[None]):
    """Model for None. Get previous backup time. response."""
    root: None = Field(...)

class PostBackupUpgradeSpeedtestResponse(RootModel[None]):
    """Model for None. Test upload speed. response."""
    root: None = Field(...)

class GetConfigResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetConfigAccessResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetConfigAccessAdResponseItem(ProxmoxBaseModel):
    """Model for None. List configured AD realms response."""
    base_dn: str | None = Field(None, alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    port: int | None = Field(None, description='AD server Port')
    realm: str | None = Field(None, description='Realm name.')
    server1: str | None = Field(None, description='AD server address')
    server2: str | None = Field(None, description='Fallback AD server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class GetConfigAccessAdResponse(RootModel[list[GetConfigAccessAdResponseItem]]):
    """List of items. None. List configured AD realms response."""
    root: list[GetConfigAccessAdResponseItem] = Field(..., description='List of configured AD realms.')

class PostConfigAccessAdRequest(ProxmoxBaseModel):
    """Model for None. Create a new AD realm request."""
    base_dn: str | None = Field(None, alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    password: str | None = Field(None, description='AD bind password')
    port: int | None = Field(None, description='AD server Port')
    realm: str = Field(..., description='Realm name.')
    server1: str = Field(..., description='AD server address')
    server2: str | None = Field(None, description='Fallback AD server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class PostConfigAccessAdResponse(RootModel[None]):
    """Model for None. Create a new AD realm response."""
    root: None = Field(...)

class DeleteConfigAccessAdRealmRequest(ProxmoxBaseModel):
    """Model for None. Remove an LDAP realm configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigAccessAdRealmResponse(RootModel[None]):
    """Model for None. Remove an LDAP realm configuration response."""
    root: None = Field(...)

class GetConfigAccessAdRealmResponse(ProxmoxBaseModel):
    """Model for None. Read the AD realm configuration response."""
    base_dn: str | None = Field(None, alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    port: int | None = Field(None, description='AD server Port')
    realm: str = Field(..., description='Realm name.')
    server1: str = Field(..., description='AD server address')
    server2: str | None = Field(None, description='Fallback AD server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class PutConfigAccessAdRealmRequest(ProxmoxBaseModel):
    """Model for None. Update an AD realm configuration request."""
    base_dn: str | None = Field(None, alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    password: str | None = Field(None, description='AD bind password')
    port: int | None = Field(None, description='AD server Port')
    server1: str | None = Field(None, description='AD server address')
    server2: str | None = Field(None, description='Fallback AD server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class PutConfigAccessAdRealmResponse(ProxmoxBaseModel):
    """Model for None. Update an AD realm configuration response."""
    base_dn: str | None = Field(None, alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    port: int | None = Field(None, description='AD server Port')
    realm: str = Field(..., description='Realm name.')
    server1: str = Field(..., description='AD server address')
    server2: str | None = Field(None, description='Fallback AD server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class GetConfigAccessLdapResponseItem(ProxmoxBaseModel):
    """Model for None. List configured LDAP realms response."""
    base_dn: str | None = Field(None, alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    port: int | None = Field(None, description='Port')
    realm: str | None = Field(None, description='Realm name.')
    server1: str | None = Field(None, description='LDAP server address')
    server2: str | None = Field(None, description='Fallback LDAP server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_attr: str | None = Field(None, alias="user-attr", description='Username attribute. Used to map a ``userid`` to LDAP to an LDAP ``dn``.')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class GetConfigAccessLdapResponse(RootModel[list[GetConfigAccessLdapResponseItem]]):
    """List of items. None. List configured LDAP realms response."""
    root: list[GetConfigAccessLdapResponseItem] = Field(..., description='List of configured LDAP realms.')

class PostConfigAccessLdapRequest(ProxmoxBaseModel):
    """Model for None. Create a new LDAP realm request."""
    base_dn: str = Field(..., alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    password: str | None = Field(None, description='LDAP bind password')
    port: int | None = Field(None, description='Port')
    realm: str = Field(..., description='Realm name.')
    server1: str = Field(..., description='LDAP server address')
    server2: str | None = Field(None, description='Fallback LDAP server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_attr: str = Field(..., alias="user-attr", description='Username attribute. Used to map a ``userid`` to LDAP to an LDAP ``dn``.')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class PostConfigAccessLdapResponse(RootModel[None]):
    """Model for None. Create a new LDAP realm response."""
    root: None = Field(...)

class DeleteConfigAccessLdapRealmRequest(ProxmoxBaseModel):
    """Model for None. Remove an LDAP realm configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigAccessLdapRealmResponse(RootModel[None]):
    """Model for None. Remove an LDAP realm configuration response."""
    root: None = Field(...)

class GetConfigAccessLdapRealmResponse(ProxmoxBaseModel):
    """Model for None. Read the LDAP realm configuration response."""
    base_dn: str = Field(..., alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    port: int | None = Field(None, description='Port')
    realm: str = Field(..., description='Realm name.')
    server1: str = Field(..., description='LDAP server address')
    server2: str | None = Field(None, description='Fallback LDAP server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_attr: str = Field(..., alias="user-attr", description='Username attribute. Used to map a ``userid`` to LDAP to an LDAP ``dn``.')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class PutConfigAccessLdapRealmRequest(ProxmoxBaseModel):
    """Model for None. Update an LDAP realm configuration request."""
    base_dn: str | None = Field(None, alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    password: str | None = Field(None, description='LDAP bind password')
    port: int | None = Field(None, description='Port')
    server1: str | None = Field(None, description='LDAP server address')
    server2: str | None = Field(None, description='Fallback LDAP server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_attr: str | None = Field(None, alias="user-attr", description='Username attribute. Used to map a ``userid`` to LDAP to an LDAP ``dn``.')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class PutConfigAccessLdapRealmResponse(ProxmoxBaseModel):
    """Model for None. Update an LDAP realm configuration response."""
    base_dn: str = Field(..., alias="base-dn", description='LDAP Domain')
    bind_dn: str | None = Field(None, alias="bind-dn", description='LDAP Domain')
    capath: str | None = Field(None, description="CA certificate to use for the server. The path can point to\neither a file, or a directory. If it points to a file,\nthe PEM-formatted X.509 certificate stored at the path\nwill be added as a trusted certificate.\nIf the path points to a directory,\nthe directory replaces the system's default certificate\nstore at `/etc/ssl/certs` - Every file in the directory\nwill be loaded as a trusted certificate.")
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    filter: str | None = Field(None, description='Custom LDAP search filter for user sync')
    mode: str | None = Field(None, description='LDAP connection type')
    port: int | None = Field(None, description='Port')
    realm: str = Field(..., description='Realm name.')
    server1: str = Field(..., description='LDAP server address')
    server2: str | None = Field(None, description='Fallback LDAP server address')
    sync_attributes: str | None = Field(None, alias="sync-attributes", description="Comma-separated list of key=value pairs for specifying which LDAP attributes map to which PBS user field. For example, to map the LDAP attribute ``mail`` to PBS's ``email``, write ``email=mail``.")
    sync_defaults_options: str | None = Field(None, alias="sync-defaults-options", description='sync defaults options')
    user_attr: str = Field(..., alias="user-attr", description='Username attribute. Used to map a ``userid`` to LDAP to an LDAP ``dn``.')
    user_classes: str | None = Field(None, alias="user-classes", description='Comma-separated list of allowed objectClass values for user synchronization. For instance, if ``user-classes`` is set to ``person,user``, then user synchronization will consider all LDAP entities where ``objectClass: person`` `or` ``objectClass: user``.')
    verify: bool | None = Field(None, description='Verify server certificate')

class GetConfigAccessOpenidResponseItem(ProxmoxBaseModel):
    """Model for None. List configured OpenId realms response."""
    acr_values: str | None = Field(None, alias="acr-values", description='OpenID ACR List')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    client_id: str | None = Field(None, alias="client-id", description='OpenID Client ID')
    client_key: str | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    issuer_url: str | None = Field(None, alias="issuer-url", description='OpenID Issuer Url')
    prompt: str | None = Field(None, description='OpenID Prompt')
    realm: str | None = Field(None, description='Realm name.')
    scopes: str | None = Field(None, description='OpenID Scope List')
    username_claim: str | None = Field(None, alias="username-claim", description="Use the value of this attribute/claim as unique user name. It is up to the identity provider to guarantee the uniqueness. The OpenID specification only guarantees that Subject ('sub') is unique. Also make sure that the user is not allowed to change that attribute by himself!")

class GetConfigAccessOpenidResponse(RootModel[list[GetConfigAccessOpenidResponseItem]]):
    """List of items. None. List configured OpenId realms response."""
    root: list[GetConfigAccessOpenidResponseItem] = Field(..., description='List of configured OpenId realms.')

class PostConfigAccessOpenidRequest(ProxmoxBaseModel):
    """Model for None. Create a new OpenId realm request."""
    acr_values: str | None = Field(None, alias="acr-values", description='OpenID ACR List')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    client_id: str = Field(..., alias="client-id", description='OpenID Client ID')
    client_key: str | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    issuer_url: str = Field(..., alias="issuer-url", description='OpenID Issuer Url')
    prompt: str | None = Field(None, description='OpenID Prompt')
    realm: str = Field(..., description='Realm name.')
    scopes: str | None = Field(None, description='OpenID Scope List')
    username_claim: str | None = Field(None, alias="username-claim", description="Use the value of this attribute/claim as unique user name. It is up to the identity provider to guarantee the uniqueness. The OpenID specification only guarantees that Subject ('sub') is unique. Also make sure that the user is not allowed to change that attribute by himself!")

class PostConfigAccessOpenidResponse(RootModel[None]):
    """Model for None. Create a new OpenId realm response."""
    root: None = Field(...)

class DeleteConfigAccessOpenidRealmRequest(ProxmoxBaseModel):
    """Model for None. Remove a OpenID realm configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigAccessOpenidRealmResponse(RootModel[None]):
    """Model for None. Remove a OpenID realm configuration response."""
    root: None = Field(...)

class GetConfigAccessOpenidRealmResponse(ProxmoxBaseModel):
    """Model for None. Read the OpenID realm configuration response."""
    acr_values: str | None = Field(None, alias="acr-values", description='OpenID ACR List')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    client_id: str = Field(..., alias="client-id", description='OpenID Client ID')
    client_key: str | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    issuer_url: str = Field(..., alias="issuer-url", description='OpenID Issuer Url')
    prompt: str | None = Field(None, description='OpenID Prompt')
    realm: str = Field(..., description='Realm name.')
    scopes: str | None = Field(None, description='OpenID Scope List')
    username_claim: str | None = Field(None, alias="username-claim", description="Use the value of this attribute/claim as unique user name. It is up to the identity provider to guarantee the uniqueness. The OpenID specification only guarantees that Subject ('sub') is unique. Also make sure that the user is not allowed to change that attribute by himself!")

class PutConfigAccessOpenidRealmRequest(ProxmoxBaseModel):
    """Model for None. Update an OpenID realm configuration request."""
    acr_values: str | None = Field(None, alias="acr-values", description='OpenID ACR List')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    client_id: str | None = Field(None, alias="client-id", description='OpenID Client ID')
    client_key: str | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    issuer_url: str | None = Field(None, alias="issuer-url", description='OpenID Issuer Url')
    prompt: str | None = Field(None, description='OpenID Prompt')
    scopes: str | None = Field(None, description='OpenID Scope List')

class PutConfigAccessOpenidRealmResponse(ProxmoxBaseModel):
    """Model for None. Update an OpenID realm configuration response."""
    acr_values: str | None = Field(None, alias="acr-values", description='OpenID ACR List')
    autocreate: bool | None = Field(None, description='Automatically create users if they do not exist.')
    client_id: str = Field(..., alias="client-id", description='OpenID Client ID')
    client_key: str | None = Field(None, alias="client-key", description='OpenID Client Key')
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    issuer_url: str = Field(..., alias="issuer-url", description='OpenID Issuer Url')
    prompt: str | None = Field(None, description='OpenID Prompt')
    realm: str = Field(..., description='Realm name.')
    scopes: str | None = Field(None, description='OpenID Scope List')
    username_claim: str | None = Field(None, alias="username-claim", description="Use the value of this attribute/claim as unique user name. It is up to the identity provider to guarantee the uniqueness. The OpenID specification only guarantees that Subject ('sub') is unique. Also make sure that the user is not allowed to change that attribute by himself!")

class GetConfigAccessPamResponse(ProxmoxBaseModel):
    """Model for None. Read the PAM realm configuration response."""
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    realm: str = Field(..., description='Realm name.')
    type: str = Field(..., description='type of the realm')

class PutConfigAccessPamRequest(ProxmoxBaseModel):
    """Model for None. Update the PAM realm configuration request."""
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class PutConfigAccessPamResponse(ProxmoxBaseModel):
    """Model for None. Update the PAM realm configuration response."""
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    realm: str = Field(..., description='Realm name.')
    type: str = Field(..., description='type of the realm')

class GetConfigAccessPbsResponse(ProxmoxBaseModel):
    """Model for None. Read the Proxmox Backup authentication server realm configuration response."""
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    realm: str = Field(..., description='Realm name.')
    type: str = Field(..., description='type of the realm')

class PutConfigAccessPbsRequest(ProxmoxBaseModel):
    """Model for None. Update the Proxmox Backup authentication server realm configuration request."""
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class PutConfigAccessPbsResponse(ProxmoxBaseModel):
    """Model for None. Update the Proxmox Backup authentication server realm configuration response."""
    comment: str | None = Field(None, description='Comment.')
    default: bool | None = Field(None, description='True if you want this to be the default realm selected on login.')
    realm: str = Field(..., description='Realm name.')
    type: str = Field(..., description='type of the realm')

class GetConfigAccessTfaResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetConfigAccessTfaWebauthnResponse(ProxmoxBaseModel):
    """Model for None. Get the TFA configuration. response."""
    allow_subdomains: bool | None = Field(None, alias="allow-subdomains", description='If an `origin` is specified, this specifies whether subdomains should be considered valid\nas well.\n\nMay be changed at any time.\n\nDefaults to `true`.')
    id: str = Field(..., description='Relying party ID. Must be the domain name without protocol, port or location.\n\nChanging this *will* break existing credentials.')
    origin: str | None = Field(None, description='Site origin. Must be a `https://` URL (or `http://localhost`). Should contain the address\nusers type in their browsers to access the web interface.\n\nChanging this *may* break existing credentials.')
    rp: str = Field(..., description='Relying party name. Any text identifier.\n\nChanging this *may* break existing credentials.')

class PutConfigAccessTfaWebauthnRequest(ProxmoxBaseModel):
    """Model for None. Update the TFA configuration. request."""
    allow_subdomains: bool | None = Field(None, alias="allow-subdomains", description='If an `origin` is specified, this specifies whether subdomains should be considered valid\nas well.\n\nMay be changed at any time.\n\nDefaults to `true`.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    id: str | None = Field(None, description='Relying party ID. Must be the domain name without protocol, port or location.\n\nChanging this *will* break existing credentials.')
    origin: str | None = Field(None, description='Site origin. Must be a `https://` URL (or `http://localhost`). Should contain the address\nusers type in their browsers to access the web interface.\n\nChanging this *may* break existing credentials.')
    rp: str | None = Field(None, description='Relying party name. Any text identifier.\n\nChanging this *may* break existing credentials.')

class PutConfigAccessTfaWebauthnResponse(RootModel[None]):
    """Model for None. Update the TFA configuration. response."""
    root: None = Field(...)

class GetConfigAcmeResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetConfigAcmeAccountResponseItem(ProxmoxBaseModel):
    """Model for None. List ACME accounts. response."""
    name: str | None = Field(None, description='ACME account name.')

class GetConfigAcmeAccountResponse(RootModel[list[GetConfigAcmeAccountResponseItem]]):
    """List of items. None. List ACME accounts. response."""
    root: list[GetConfigAcmeAccountResponseItem] = Field(..., description='List of ACME accounts.')

class PostConfigAcmeAccountRequest(ProxmoxBaseModel):
    """Model for None. Register an ACME account. request."""
    contact: str = Field(..., description='List of email addresses.')
    directory: str | None = Field(None, description='The ACME Directory.')
    eab_hmac_key: str | None = Field(None, description='HMAC Key for External Account Binding.')
    eab_kid: str | None = Field(None, description='Key Identifier for External Account Binding.')
    name: str | None = Field(None, description='ACME account name.')
    tos_url: str | None = Field(None, description='URL of CA TermsOfService - setting this indicates agreement.')

class PostConfigAcmeAccountResponse(RootModel[None]):
    """Model for None. Register an ACME account. response."""
    root: None = Field(...)

class DeleteConfigAcmeAccountNameRequest(ProxmoxBaseModel):
    """Model for None. Deactivate an ACME account. request."""
    force: bool | None = Field(None, description='Delete account data even if the server refuses to deactivate the account.')

class DeleteConfigAcmeAccountNameResponse(RootModel[None]):
    """Model for None. Deactivate an ACME account. response."""
    root: None = Field(...)

class GetConfigAcmeAccountNameResponse(ProxmoxBaseModel):
    """Model for None. Return existing ACME account information. response."""
    account: dict[str, object] = Field(..., description='ACME Account data. This is the part of the account returned from and possibly sent to the ACME\nprovider. Some fields may be uptdated by the user via a request to the account location, others\nmay not be changed.')
    directory: str = Field(..., description='The ACME directory URL the account was created at.')
    location: str = Field(..., description="The account's own URL within the ACME directory.")
    tos: str | None = Field(None, description='The ToS URL, if the user agreed to one.')

class PutConfigAcmeAccountNameRequest(ProxmoxBaseModel):
    """Model for None. Update an ACME account. request."""
    contact: str | None = Field(None, description='List of email addresses.')

class PutConfigAcmeAccountNameResponse(RootModel[None]):
    """Model for None. Update an ACME account. response."""
    root: None = Field(...)

class GetConfigAcmeChallengeSchemaResponseItem(ProxmoxBaseModel):
    """Model for None. Get named known ACME directory endpoints. response."""
    id: str | None = Field(None, description='Plugin ID.')
    name: str | None = Field(None, description='Human readable name, falls back to id.')
    schema: dict[str, object] | None = Field(None, description="The plugin's parameter schema.")
    type: str | None = Field(None, description='Plugin Type.')

class GetConfigAcmeChallengeSchemaResponse(RootModel[list[GetConfigAcmeChallengeSchemaResponseItem]]):
    """List of items. None. Get named known ACME directory endpoints. response."""
    root: list[GetConfigAcmeChallengeSchemaResponseItem] = Field(..., description='ACME Challenge Plugin Shema.')

class GetConfigAcmeDirectoriesResponseItem(ProxmoxBaseModel):
    """Model for None. Get named known ACME directory endpoints. response."""
    name: str | None = Field(None, description="The ACME directory's name.")
    url: str | None = Field(None, description="The ACME directory's endpoint URL.")

class GetConfigAcmeDirectoriesResponse(RootModel[list[GetConfigAcmeDirectoriesResponseItem]]):
    """List of items. None. Get named known ACME directory endpoints. response."""
    root: list[GetConfigAcmeDirectoriesResponseItem] = Field(..., description='List of known ACME directories.')

class GetConfigAcmePluginsResponseItem(ProxmoxBaseModel):
    """Model for None. List ACME challenge plugins. response."""
    api: str | None = Field(None, description='DNS Api name.')
    data: str | None = Field(None, description='Plugin configuration data.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    plugin: str | None = Field(None, description='Plugin ID.')
    type: str | None = Field(None, description='Plugin type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation.\n\nAllows to cope with long TTL of DNS records.')

class GetConfigAcmePluginsResponse(RootModel[list[GetConfigAcmePluginsResponseItem]]):
    """List of items. None. List ACME challenge plugins. response."""
    root: list[GetConfigAcmePluginsResponseItem] = Field(..., description='List of ACME plugin configurations.')

class PostConfigAcmePluginsRequest(ProxmoxBaseModel):
    """Model for None. Add ACME plugin configuration. request."""
    api: str = Field(..., description='DNS API Plugin Id.')
    data: str = Field(..., description='DNS plugin data (base64 encoded with padding).')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    id: str = Field(..., description='ACME Challenge Plugin ID.')
    type: str = Field(..., description='The ACME challenge plugin type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation.\n\nAllows to cope with long TTL of DNS records.')

class PostConfigAcmePluginsResponse(RootModel[None]):
    """Model for None. Add ACME plugin configuration. response."""
    root: None = Field(...)

class DeleteConfigAcmePluginsIdRequest(RootModel[dict[str, object]]):
    """Model for None. Delete an ACME plugin configuration. request."""
    root: dict[str, object] = Field(...)

class DeleteConfigAcmePluginsIdResponse(RootModel[None]):
    """Model for None. Delete an ACME plugin configuration. response."""
    root: None = Field(...)

class GetConfigAcmePluginsIdResponse(ProxmoxBaseModel):
    """Model for None. List ACME challenge plugins. response."""
    api: str | None = Field(None, description='DNS Api name.')
    data: str | None = Field(None, description='Plugin configuration data.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    plugin: str = Field(..., description='Plugin ID.')
    type: str = Field(..., description='Plugin type.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation.\n\nAllows to cope with long TTL of DNS records.')

class PutConfigAcmePluginsIdRequest(ProxmoxBaseModel):
    """Model for None. Update an ACME plugin configuration. request."""
    api: str | None = Field(None, description='DNS API Plugin Id.')
    data: str | None = Field(None, description='DNS plugin data (base64 encoded with padding).')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the config.')
    validation_delay: int | None = Field(None, alias="validation-delay", description='Extra delay in seconds to wait before requesting validation.\n\nAllows to cope with long TTL of DNS records.')

class PutConfigAcmePluginsIdResponse(RootModel[None]):
    """Model for None. Update an ACME plugin configuration. response."""
    root: None = Field(...)

class GetConfigAcmeTosResponse(RootModel[str]):
    """Model for None. Get the Terms of Service URL for an ACME directory. response."""
    root: str = Field(..., description="The ACME Directory's ToS URL, if any.")

class GetConfigChangerResponseItem(ProxmoxBaseModel):
    """Model for None. List changers response."""
    eject_before_unload: bool | None = Field(None, alias="eject-before-unload", description='if set to true, tapes are ejected manually before unloading')
    export_slots: str | None = Field(None, alias="export-slots", description="A list of slot numbers, comma separated. Those slots are reserved for\nImport/Export, i.e. any media in those slots are considered to be\n'offline'.\n")
    name: str | None = Field(None, description='Tape Changer Identifier.')
    path: str | None = Field(None, description="Path to Linux generic SCSI device (e.g. '/dev/sg4')")

class GetConfigChangerResponse(RootModel[list[GetConfigChangerResponseItem]]):
    """List of items. None. List changers response."""
    root: list[GetConfigChangerResponseItem] = Field(..., description='The list of configured changers (with config digest).')

class PostConfigChangerRequest(ProxmoxBaseModel):
    """Model for None. Create a new changer device request."""
    eject_before_unload: bool | None = Field(None, alias="eject-before-unload", description='if set to true, tapes are ejected manually before unloading')
    export_slots: str | None = Field(None, alias="export-slots", description="A list of slot numbers, comma separated. Those slots are reserved for\nImport/Export, i.e. any media in those slots are considered to be\n'offline'.\n")
    name: str = Field(..., description='Tape Changer Identifier.')
    path: str = Field(..., description="Path to Linux generic SCSI device (e.g. '/dev/sg4')")

class PostConfigChangerResponse(RootModel[None]):
    """Model for None. Create a new changer device response."""
    root: None = Field(...)

class DeleteConfigChangerNameRequest(RootModel[dict[str, object]]):
    """Model for None. Delete a tape changer configuration request."""
    root: dict[str, object] = Field(...)

class DeleteConfigChangerNameResponse(RootModel[None]):
    """Model for None. Delete a tape changer configuration response."""
    root: None = Field(...)

class GetConfigChangerNameResponse(ProxmoxBaseModel):
    """Model for None. Get tape changer configuration response."""
    eject_before_unload: bool | None = Field(None, alias="eject-before-unload", description='if set to true, tapes are ejected manually before unloading')
    export_slots: str | None = Field(None, alias="export-slots", description="A list of slot numbers, comma separated. Those slots are reserved for\nImport/Export, i.e. any media in those slots are considered to be\n'offline'.\n")
    name: str = Field(..., description='Tape Changer Identifier.')
    path: str = Field(..., description="Path to Linux generic SCSI device (e.g. '/dev/sg4')")

class PutConfigChangerNameRequest(ProxmoxBaseModel):
    """Model for None. Update a tape changer configuration request."""
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    eject_before_unload: bool | None = Field(None, alias="eject-before-unload", description='if set to true, tapes are ejected manually before unloading')
    export_slots: str | None = Field(None, alias="export-slots", description="A list of slot numbers, comma separated. Those slots are reserved for\nImport/Export, i.e. any media in those slots are considered to be\n'offline'.\n")
    path: str | None = Field(None, description="Path to Linux generic SCSI device (e.g. '/dev/sg4')")

class PutConfigChangerNameResponse(RootModel[None]):
    """Model for None. Update a tape changer configuration response."""
    root: None = Field(...)

class GetConfigDatastoreResponseItem(ProxmoxBaseModel):
    """Model for None. List all datastores response."""
    backend: str | None = Field(None, description='Datastore backend config')
    backing_device: str | None = Field(None, alias="backing-device", description='The UUID of the filesystem partition for removable datastores.')
    comment: str | None = Field(None, description='Comment.')
    gc_schedule: str | None = Field(None, alias="gc-schedule", description='Run garbage collection job at specified schedule.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    maintenance_mode: str | None = Field(None, alias="maintenance-mode", description='Maintenance mode, type is either \'offline\' or \'read-only\', message should be enclosed in "')
    name: str | None = Field(None, description='Datastore name.')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify: str | None = Field(None, description="Datastore notification setting, enum can be one of 'always', 'never', or 'error'.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    path: str | None = Field(None, description='Either the absolute path to the datastore directory, or a relative on-device path for removable datastores.')
    prune_schedule: str | None = Field(None, alias="prune-schedule", description='Run prune job at specified schedule.')
    tuning: str | None = Field(None, description='Datastore tuning options')
    verify_new: bool | None = Field(None, alias="verify-new", description='If enabled, all new backups will be verified right after completion.')

class GetConfigDatastoreResponse(RootModel[list[GetConfigDatastoreResponseItem]]):
    """List of items. None. List all datastores response."""
    root: list[GetConfigDatastoreResponseItem] = Field(..., description='List the configured datastores (with config digest).')

class PostConfigDatastoreRequest(ProxmoxBaseModel):
    """Model for None. Create new datastore config. request."""
    backend: str | None = Field(None, description='Datastore backend config')
    backing_device: str | None = Field(None, alias="backing-device", description='The UUID of the filesystem partition for removable datastores.')
    comment: str | None = Field(None, description='Comment.')
    gc_schedule: str | None = Field(None, alias="gc-schedule", description='Run garbage collection job at specified schedule.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    maintenance_mode: str | None = Field(None, alias="maintenance-mode", description='Maintenance mode, type is either \'offline\' or \'read-only\', message should be enclosed in "')
    name: str = Field(..., description='Datastore name.')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify: str | None = Field(None, description="Datastore notification setting, enum can be one of 'always', 'never', or 'error'.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    overwrite_in_use: bool | None = Field(None, alias="overwrite-in-use", description='Overwrite in use marker (S3 backed datastores only).')
    path: str = Field(..., description='Either the absolute path to the datastore directory, or a relative on-device path for removable datastores.')
    prune_schedule: str | None = Field(None, alias="prune-schedule", description='Run prune job at specified schedule.')
    reuse_datastore: bool | None = Field(None, alias="reuse-datastore", description='Re-use existing datastore directory.')
    tuning: str | None = Field(None, description='Datastore tuning options')
    verify_new: bool | None = Field(None, alias="verify-new", description='If enabled, all new backups will be verified right after completion.')

class PostConfigDatastoreResponse(RootModel[None]):
    """Model for None. Create new datastore config. response."""
    root: None = Field(...)

class DeleteConfigDatastoreNameRequest(ProxmoxBaseModel):
    """Model for None. Remove a datastore configuration and optionally delete all its contents. request."""
    destroy_data: bool | None = Field(None, alias="destroy-data", description="Delete the datastore's underlying contents")
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    keep_job_configs: bool | None = Field(None, alias="keep-job-configs", description='If enabled, the job configurations related to this datastore will be kept.')

class DeleteConfigDatastoreNameResponse(RootModel[str]):
    """Model for None. Remove a datastore configuration and optionally delete all its contents. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetConfigDatastoreNameResponse(ProxmoxBaseModel):
    """Model for None. Read a datastore configuration. response."""
    backend: str | None = Field(None, description='Datastore backend config')
    backing_device: str | None = Field(None, alias="backing-device", description='The UUID of the filesystem partition for removable datastores.')
    comment: str | None = Field(None, description='Comment.')
    gc_schedule: str | None = Field(None, alias="gc-schedule", description='Run garbage collection job at specified schedule.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    maintenance_mode: str | None = Field(None, alias="maintenance-mode", description='Maintenance mode, type is either \'offline\' or \'read-only\', message should be enclosed in "')
    name: str = Field(..., description='Datastore name.')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify: str | None = Field(None, description="Datastore notification setting, enum can be one of 'always', 'never', or 'error'.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    path: str = Field(..., description='Either the absolute path to the datastore directory, or a relative on-device path for removable datastores.')
    prune_schedule: str | None = Field(None, alias="prune-schedule", description='Run prune job at specified schedule.')
    tuning: str | None = Field(None, description='Datastore tuning options')
    verify_new: bool | None = Field(None, alias="verify-new", description='If enabled, all new backups will be verified right after completion.')

class PutConfigDatastoreNameRequest(ProxmoxBaseModel):
    """Model for None. Update datastore config. request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    gc_schedule: str | None = Field(None, alias="gc-schedule", description='Run garbage collection job at specified schedule.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    maintenance_mode: str | None = Field(None, alias="maintenance-mode", description='Maintenance mode, type is either \'offline\' or \'read-only\', message should be enclosed in "')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify: str | None = Field(None, description="Datastore notification setting, enum can be one of 'always', 'never', or 'error'.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    prune_schedule: str | None = Field(None, alias="prune-schedule", description='Run prune job at specified schedule.')
    tuning: str | None = Field(None, description='Datastore tuning options')
    verify_new: bool | None = Field(None, alias="verify-new", description='If enabled, all new backups will be verified right after completion.')

class PutConfigDatastoreNameResponse(RootModel[None]):
    """Model for None. Update datastore config. response."""
    root: None = Field(...)

class GetConfigDriveResponseItem(ProxmoxBaseModel):
    """Model for None. List drives response."""
    changer: str | None = Field(None, description='Tape Changer Identifier.')
    changer_drivenum: int | None = Field(None, alias="changer-drivenum", description='Associated changer drive number (requires option changer)')
    name: str | None = Field(None, description='Drive Identifier.')
    path: str | None = Field(None, description="The path to a LTO SCSI-generic tape device (i.e. '/dev/sg0')")

class GetConfigDriveResponse(RootModel[list[GetConfigDriveResponseItem]]):
    """List of items. None. List drives response."""
    root: list[GetConfigDriveResponseItem] = Field(..., description='The list of configured drives (with config digest).')

class PostConfigDriveRequest(ProxmoxBaseModel):
    """Model for None. Create a new drive request."""
    changer: str | None = Field(None, description='Tape Changer Identifier.')
    changer_drivenum: int | None = Field(None, alias="changer-drivenum", description='Associated changer drive number (requires option changer)')
    name: str = Field(..., description='Drive Identifier.')
    path: str = Field(..., description="The path to a LTO SCSI-generic tape device (i.e. '/dev/sg0')")

class PostConfigDriveResponse(RootModel[None]):
    """Model for None. Create a new drive response."""
    root: None = Field(...)

class DeleteConfigDriveNameRequest(RootModel[dict[str, object]]):
    """Model for None. Delete a drive configuration request."""
    root: dict[str, object] = Field(...)

class DeleteConfigDriveNameResponse(RootModel[None]):
    """Model for None. Delete a drive configuration response."""
    root: None = Field(...)

class GetConfigDriveNameResponse(ProxmoxBaseModel):
    """Model for None. Get drive configuration response."""
    changer: str | None = Field(None, description='Tape Changer Identifier.')
    changer_drivenum: int | None = Field(None, alias="changer-drivenum", description='Associated changer drive number (requires option changer)')
    name: str = Field(..., description='Drive Identifier.')
    path: str = Field(..., description="The path to a LTO SCSI-generic tape device (i.e. '/dev/sg0')")

class PutConfigDriveNameRequest(ProxmoxBaseModel):
    """Model for None. Update a drive configuration request."""
    changer: str | None = Field(None, description='Tape Changer Identifier.')
    changer_drivenum: int | None = Field(None, alias="changer-drivenum", description='Associated changer drive number (requires option changer)')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    path: str | None = Field(None, description="The path to a LTO SCSI-generic tape device (i.e. '/dev/sg0')")

class PutConfigDriveNameResponse(RootModel[None]):
    """Model for None. Update a drive configuration response."""
    root: None = Field(...)

class GetConfigMediaPoolResponseItem(ProxmoxBaseModel):
    """Model for None. List media pools response."""
    allocation: str | None = Field(None, description="Media set allocation policy ('continue', 'always', or a calendar event).")
    comment: str | None = Field(None, description='Comment.')
    encrypt: str | None = Field(None, description='Tape encryption key fingerprint (sha256).')
    name: str | None = Field(None, description='Media pool name.')
    retention: str | None = Field(None, description="Media retention policy ('overwrite', 'keep', or time span).")
    template: str | None = Field(None, description='Media set naming template (may contain strftime() time format specifications).')

class GetConfigMediaPoolResponse(RootModel[list[GetConfigMediaPoolResponseItem]]):
    """List of items. None. List media pools response."""
    root: list[GetConfigMediaPoolResponseItem] = Field(..., description='The list of configured media pools (with config digest).')

class PostConfigMediaPoolRequest(ProxmoxBaseModel):
    """Model for None. Create a new media pool request."""
    allocation: str | None = Field(None, description="Media set allocation policy ('continue', 'always', or a calendar event).")
    comment: str | None = Field(None, description='Comment.')
    encrypt: str | None = Field(None, description='Tape encryption key fingerprint (sha256).')
    name: str = Field(..., description='Media pool name.')
    retention: str | None = Field(None, description="Media retention policy ('overwrite', 'keep', or time span).")
    template: str | None = Field(None, description='Media set naming template (may contain strftime() time format specifications).')

class PostConfigMediaPoolResponse(RootModel[None]):
    """Model for None. Create a new media pool response."""
    root: None = Field(...)

class DeleteConfigMediaPoolNameRequest(RootModel[dict[str, object]]):
    """Model for None. Delete a media pool configuration request."""
    root: dict[str, object] = Field(...)

class DeleteConfigMediaPoolNameResponse(RootModel[None]):
    """Model for None. Delete a media pool configuration response."""
    root: None = Field(...)

class GetConfigMediaPoolNameResponse(ProxmoxBaseModel):
    """Model for None. Get media pool configuration response."""
    allocation: str | None = Field(None, description="Media set allocation policy ('continue', 'always', or a calendar event).")
    comment: str | None = Field(None, description='Comment.')
    encrypt: str | None = Field(None, description='Tape encryption key fingerprint (sha256).')
    name: str = Field(..., description='Media pool name.')
    retention: str | None = Field(None, description="Media retention policy ('overwrite', 'keep', or time span).")
    template: str | None = Field(None, description='Media set naming template (may contain strftime() time format specifications).')

class PutConfigMediaPoolNameRequest(ProxmoxBaseModel):
    """Model for None. Update media pool settings request."""
    allocation: str | None = Field(None, description="Media set allocation policy ('continue', 'always', or a calendar event).")
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    encrypt: str | None = Field(None, description='Tape encryption key fingerprint (sha256).')
    retention: str | None = Field(None, description="Media retention policy ('overwrite', 'keep', or time span).")
    template: str | None = Field(None, description='Media set naming template (may contain strftime() time format specifications).')

class PutConfigMediaPoolNameResponse(RootModel[None]):
    """Model for None. Update media pool settings response."""
    root: None = Field(...)

class GetConfigMetricsResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetConfigMetricsInfluxdbHttpResponseItem(ProxmoxBaseModel):
    """Model for None. List configured InfluxDB http metric servers. response."""
    bucket: str | None = Field(None, description='InfluxDB Bucket.')
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    max_body_size: int | None = Field(None, alias="max-body-size", description='The (optional) maximum body size')
    name: str | None = Field(None, description='Metrics Server ID.')
    organization: str | None = Field(None, description='InfluxDB Organization.')
    token: str | None = Field(None, description='The (optional) API token')
    url: str | None = Field(None, description='HTTP(s) url with optional port.')
    verify_tls: bool | None = Field(None, alias="verify-tls", description='If true, the certificate will be validated.')

class GetConfigMetricsInfluxdbHttpResponse(RootModel[list[GetConfigMetricsInfluxdbHttpResponseItem]]):
    """List of items. None. List configured InfluxDB http metric servers. response."""
    root: list[GetConfigMetricsInfluxdbHttpResponseItem] = Field(..., description='List of configured InfluxDB http metric servers.')

class PostConfigMetricsInfluxdbHttpRequest(ProxmoxBaseModel):
    """Model for None. Create a new InfluxDB http server configuration request."""
    bucket: str | None = Field(None, description='InfluxDB Bucket.')
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    max_body_size: int | None = Field(None, alias="max-body-size", description='The (optional) maximum body size')
    name: str = Field(..., description='Metrics Server ID.')
    organization: str | None = Field(None, description='InfluxDB Organization.')
    token: str | None = Field(None, description='The (optional) API token')
    url: str = Field(..., description='HTTP(s) url with optional port.')
    verify_tls: bool | None = Field(None, alias="verify-tls", description='If true, the certificate will be validated.')

class PostConfigMetricsInfluxdbHttpResponse(RootModel[None]):
    """Model for None. Create a new InfluxDB http server configuration response."""
    root: None = Field(...)

class DeleteConfigMetricsInfluxdbHttpNameRequest(ProxmoxBaseModel):
    """Model for None. Remove a InfluxDB http server configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigMetricsInfluxdbHttpNameResponse(RootModel[None]):
    """Model for None. Remove a InfluxDB http server configuration response."""
    root: None = Field(...)

class GetConfigMetricsInfluxdbHttpNameResponse(ProxmoxBaseModel):
    """Model for None. Read the InfluxDB http server configuration response."""
    bucket: str | None = Field(None, description='InfluxDB Bucket.')
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    max_body_size: int | None = Field(None, alias="max-body-size", description='The (optional) maximum body size')
    name: str = Field(..., description='Metrics Server ID.')
    organization: str | None = Field(None, description='InfluxDB Organization.')
    token: str | None = Field(None, description='The (optional) API token')
    url: str = Field(..., description='HTTP(s) url with optional port.')
    verify_tls: bool | None = Field(None, alias="verify-tls", description='If true, the certificate will be validated.')

class PutConfigMetricsInfluxdbHttpNameRequest(ProxmoxBaseModel):
    """Model for None. Update an InfluxDB http server configuration request."""
    bucket: str | None = Field(None, description='InfluxDB Bucket.')
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    max_body_size: int | None = Field(None, alias="max-body-size", description='The (optional) maximum body size')
    organization: str | None = Field(None, description='InfluxDB Organization.')
    token: str | None = Field(None, description='The (optional) API token')
    url: str | None = Field(None, description='HTTP(s) url with optional port.')
    verify_tls: bool | None = Field(None, alias="verify-tls", description='If true, the certificate will be validated.')

class PutConfigMetricsInfluxdbHttpNameResponse(RootModel[None]):
    """Model for None. Update an InfluxDB http server configuration response."""
    root: None = Field(...)

class GetConfigMetricsInfluxdbUdpResponseItem(ProxmoxBaseModel):
    """Model for None. List configured InfluxDB udp metric servers. response."""
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    host: str | None = Field(None, description='host:port combination (Host can be DNS name or IP address).')
    mtu: int | None = Field(None, description='The MTU')
    name: str | None = Field(None, description='Metrics Server ID.')

class GetConfigMetricsInfluxdbUdpResponse(RootModel[list[GetConfigMetricsInfluxdbUdpResponseItem]]):
    """List of items. None. List configured InfluxDB udp metric servers. response."""
    root: list[GetConfigMetricsInfluxdbUdpResponseItem] = Field(..., description='List of configured InfluxDB udp metric servers.')

class PostConfigMetricsInfluxdbUdpRequest(ProxmoxBaseModel):
    """Model for None. Create a new InfluxDB udp server configuration request."""
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    host: str = Field(..., description='host:port combination (Host can be DNS name or IP address).')
    mtu: int | None = Field(None, description='The MTU')
    name: str = Field(..., description='Metrics Server ID.')

class PostConfigMetricsInfluxdbUdpResponse(RootModel[None]):
    """Model for None. Create a new InfluxDB udp server configuration response."""
    root: None = Field(...)

class DeleteConfigMetricsInfluxdbUdpNameRequest(ProxmoxBaseModel):
    """Model for None. Remove a InfluxDB udp server configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigMetricsInfluxdbUdpNameResponse(RootModel[None]):
    """Model for None. Remove a InfluxDB udp server configuration response."""
    root: None = Field(...)

class GetConfigMetricsInfluxdbUdpNameResponse(ProxmoxBaseModel):
    """Model for None. Read the InfluxDB udp server configuration response."""
    comment: str | None = Field(None, description='Comment.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    host: str = Field(..., description='host:port combination (Host can be DNS name or IP address).')
    mtu: int | None = Field(None, description='The MTU')
    name: str = Field(..., description='Metrics Server ID.')

class PutConfigMetricsInfluxdbUdpNameRequest(ProxmoxBaseModel):
    """Model for None. Update an InfluxDB udp server configuration request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enables or disables the metrics server')
    host: str | None = Field(None, description='host:port combination (Host can be DNS name or IP address).')
    mtu: int | None = Field(None, description='The MTU')

class PutConfigMetricsInfluxdbUdpNameResponse(RootModel[None]):
    """Model for None. Update an InfluxDB udp server configuration response."""
    root: None = Field(...)

class GetConfigNotificationsResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsGotifyResponseItem(ProxmoxBaseModel):
    """Model for None. List all gotify endpoints. response."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    filter: str | None = Field(None, description='Deprecated.')
    name: str | None = Field(None, description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    server: str | None = Field(None, description='Gotify Server URL.')

class GetConfigNotificationsEndpointsGotifyResponse(RootModel[list[GetConfigNotificationsEndpointsGotifyResponseItem]]):
    """List of items. None. List all gotify endpoints. response."""
    root: list[GetConfigNotificationsEndpointsGotifyResponseItem] = Field(..., description='List of gotify endpoints.')

class PostConfigNotificationsEndpointsGotifyRequest(ProxmoxBaseModel):
    """Model for None. Add a new gotify endpoint. request."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    filter: str | None = Field(None, description='Deprecated.')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    server: str = Field(..., description='Gotify Server URL.')
    token: str = Field(..., description='Authentication token')

class PostConfigNotificationsEndpointsGotifyResponse(RootModel[None]):
    """Model for None. Add a new gotify endpoint. response."""
    root: None = Field(...)

class DeleteConfigNotificationsEndpointsGotifyNameRequest(RootModel[dict[str, object]]):
    """Model for None. Delete gotify endpoint. request."""
    root: dict[str, object] = Field(...)

class DeleteConfigNotificationsEndpointsGotifyNameResponse(RootModel[None]):
    """Model for None. Delete gotify endpoint. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsGotifyNameResponse(ProxmoxBaseModel):
    """Model for None. Get a gotify endpoint. response."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    filter: str | None = Field(None, description='Deprecated.')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    server: str = Field(..., description='Gotify Server URL.')

class PutConfigNotificationsEndpointsGotifyNameRequest(ProxmoxBaseModel):
    """Model for None. Update gotify endpoint. request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target.')
    server: str | None = Field(None, description='Gotify Server URL.')
    token: str | None = Field(None, description='Authentication token')

class PutConfigNotificationsEndpointsGotifyNameResponse(RootModel[None]):
    """Model for None. Update gotify endpoint. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsSendmailResponseItem(ProxmoxBaseModel):
    """Model for None. List all sendmail endpoints. response."""
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox Backup Server ($hostname)'")
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    filter: str | None = Field(None, description='Deprecated.')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for sent E-Mails.\nIf the parameter is not set, the plugin will fall back to the\nemail-from setting from node.cfg (PBS).\nIf that is also not set, the plugin will default to root@$hostname,\nwhere $hostname is the hostname of the node.')
    mailto: list[str] | None = Field(None, description='Mail address to send a mail to.')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='Users to send a mail to. The email address of the user\nwill be looked up in users.cfg.')
    name: str | None = Field(None, description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')

class GetConfigNotificationsEndpointsSendmailResponse(RootModel[list[GetConfigNotificationsEndpointsSendmailResponseItem]]):
    """List of items. None. List all sendmail endpoints. response."""
    root: list[GetConfigNotificationsEndpointsSendmailResponseItem] = Field(..., description='List of sendmail endpoints.')

class PostConfigNotificationsEndpointsSendmailRequest(ProxmoxBaseModel):
    """Model for None. Add a new sendmail endpoint. request."""
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox Backup Server ($hostname)'")
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    filter: str | None = Field(None, description='Deprecated.')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for sent E-Mails.\nIf the parameter is not set, the plugin will fall back to the\nemail-from setting from node.cfg (PBS).\nIf that is also not set, the plugin will default to root@$hostname,\nwhere $hostname is the hostname of the node.')
    mailto: list[str] | None = Field(None, description='Mail address to send a mail to.')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='Users to send a mail to. The email address of the user\nwill be looked up in users.cfg.')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')

class PostConfigNotificationsEndpointsSendmailResponse(RootModel[None]):
    """Model for None. Add a new sendmail endpoint. response."""
    root: None = Field(...)

class DeleteConfigNotificationsEndpointsSendmailNameRequest(RootModel[dict[str, object]]):
    """Model for None. Delete sendmail endpoint. request."""
    root: dict[str, object] = Field(...)

class DeleteConfigNotificationsEndpointsSendmailNameResponse(RootModel[None]):
    """Model for None. Delete sendmail endpoint. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsSendmailNameResponse(ProxmoxBaseModel):
    """Model for None. Get a sendmail endpoint. response."""
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox Backup Server ($hostname)'")
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    filter: str | None = Field(None, description='Deprecated.')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for sent E-Mails.\nIf the parameter is not set, the plugin will fall back to the\nemail-from setting from node.cfg (PBS).\nIf that is also not set, the plugin will default to root@$hostname,\nwhere $hostname is the hostname of the node.')
    mailto: list[str] | None = Field(None, description='Mail address to send a mail to.')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='Users to send a mail to. The email address of the user\nwill be looked up in users.cfg.')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')

class PutConfigNotificationsEndpointsSendmailNameRequest(ProxmoxBaseModel):
    """Model for None. Update sendmail endpoint. request."""
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox Backup Server ($hostname)'")
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target.')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for sent E-Mails.\nIf the parameter is not set, the plugin will fall back to the\nemail-from setting from node.cfg (PBS).\nIf that is also not set, the plugin will default to root@$hostname,\nwhere $hostname is the hostname of the node.')
    mailto: list[str] | None = Field(None, description='Mail address to send a mail to.')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='Users to send a mail to. The email address of the user\nwill be looked up in users.cfg.')

class PutConfigNotificationsEndpointsSendmailNameResponse(RootModel[None]):
    """Model for None. Update sendmail endpoint. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsSmtpResponseItem(ProxmoxBaseModel):
    """Model for None. List all smtp endpoints. response."""
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox Backup Server ($hostname)'")
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for the mail.\nSMTP relays might require that this address is owned by the user\nin order to avoid spoofing. The `From` header in the email will be\nset to `$author <$from-address>`.')
    mailto: list[str] | None = Field(None, description='Mail address to send a mail to.')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='Users to send a mail to. The email address of the user\nwill be looked up in users.cfg.')
    mode: str | None = Field(None, description='Connection security')
    name: str | None = Field(None, description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    port: int | None = Field(None, description='The port to connect to.\nIf not set, the used port defaults to 25 (insecure), 465 (tls)\nor 587 (starttls), depending on the value of mode')
    server: str | None = Field(None, description='Host name or IP of the SMTP relay.')
    username: str | None = Field(None, description='Username to use during authentication.\nIf no username is set, no authentication will be performed.\nThe PLAIN and LOGIN authentication methods are supported')

class GetConfigNotificationsEndpointsSmtpResponse(RootModel[list[GetConfigNotificationsEndpointsSmtpResponseItem]]):
    """List of items. None. List all smtp endpoints. response."""
    root: list[GetConfigNotificationsEndpointsSmtpResponseItem] = Field(..., description='List of smtp endpoints.')

class PostConfigNotificationsEndpointsSmtpRequest(ProxmoxBaseModel):
    """Model for None. Add a new smtp endpoint. request."""
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox Backup Server ($hostname)'")
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    from_address: str = Field(..., alias="from-address", description='`From` address for the mail.\nSMTP relays might require that this address is owned by the user\nin order to avoid spoofing. The `From` header in the email will be\nset to `$author <$from-address>`.')
    mailto: list[str] | None = Field(None, description='Mail address to send a mail to.')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='Users to send a mail to. The email address of the user\nwill be looked up in users.cfg.')
    mode: str | None = Field(None, description='Connection security')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    password: str | None = Field(None, description='SMTP authentication password')
    port: int | None = Field(None, description='The port to connect to.\nIf not set, the used port defaults to 25 (insecure), 465 (tls)\nor 587 (starttls), depending on the value of mode')
    server: str = Field(..., description='Host name or IP of the SMTP relay.')
    username: str | None = Field(None, description='Username to use during authentication.\nIf no username is set, no authentication will be performed.\nThe PLAIN and LOGIN authentication methods are supported')

class PostConfigNotificationsEndpointsSmtpResponse(RootModel[None]):
    """Model for None. Add a new smtp endpoint. response."""
    root: None = Field(...)

class DeleteConfigNotificationsEndpointsSmtpNameRequest(RootModel[dict[str, object]]):
    """Model for None. Delete smtp endpoint. request."""
    root: dict[str, object] = Field(...)

class DeleteConfigNotificationsEndpointsSmtpNameResponse(RootModel[None]):
    """Model for None. Delete smtp endpoint. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsSmtpNameResponse(ProxmoxBaseModel):
    """Model for None. Get a smtp endpoint. response."""
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox Backup Server ($hostname)'")
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    from_address: str = Field(..., alias="from-address", description='`From` address for the mail.\nSMTP relays might require that this address is owned by the user\nin order to avoid spoofing. The `From` header in the email will be\nset to `$author <$from-address>`.')
    mailto: list[str] | None = Field(None, description='Mail address to send a mail to.')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='Users to send a mail to. The email address of the user\nwill be looked up in users.cfg.')
    mode: str | None = Field(None, description='Connection security')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    port: int | None = Field(None, description='The port to connect to.\nIf not set, the used port defaults to 25 (insecure), 465 (tls)\nor 587 (starttls), depending on the value of mode')
    server: str = Field(..., description='Host name or IP of the SMTP relay.')
    username: str | None = Field(None, description='Username to use during authentication.\nIf no username is set, no authentication will be performed.\nThe PLAIN and LOGIN authentication methods are supported')

class PutConfigNotificationsEndpointsSmtpNameRequest(ProxmoxBaseModel):
    """Model for None. Update smtp endpoint. request."""
    author: str | None = Field(None, description="Author of the mail. Defaults to 'Proxmox Backup Server ($hostname)'")
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target.')
    from_address: str | None = Field(None, alias="from-address", description='`From` address for the mail.\nSMTP relays might require that this address is owned by the user\nin order to avoid spoofing. The `From` header in the email will be\nset to `$author <$from-address>`.')
    mailto: list[str] | None = Field(None, description='Mail address to send a mail to.')
    mailto_user: list[str] | None = Field(None, alias="mailto-user", description='Users to send a mail to. The email address of the user\nwill be looked up in users.cfg.')
    mode: str | None = Field(None, description='Connection security')
    password: str | None = Field(None, description='SMTP authentication password')
    port: int | None = Field(None, description='The port to connect to.\nIf not set, the used port defaults to 25 (insecure), 465 (tls)\nor 587 (starttls), depending on the value of mode')
    server: str | None = Field(None, description='Host name or IP of the SMTP relay.')
    username: str | None = Field(None, description='Username to use during authentication.\nIf no username is set, no authentication will be performed.\nThe PLAIN and LOGIN authentication methods are supported')

class PutConfigNotificationsEndpointsSmtpNameResponse(RootModel[None]):
    """Model for None. Update smtp endpoint. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsWebhookResponseItem(ProxmoxBaseModel):
    """Model for None. List all webhook endpoints. response."""
    body: str | None = Field(None, description='The HTTP body to send. Supports templating.')
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    header: list[str] | None = Field(None, description='Array of HTTP headers. Each entry is a property string with a name and a value.\nThe value property contains the header in base64 encoding. Supports templating.')
    method: str | None = Field(None, description='HTTP Method to use.')
    name: str | None = Field(None, description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    secret: list[str] | None = Field(None, description='Array of secrets. Each entry is a property string with a name and an optional value.\nThe value property contains the secret in base64 encoding.\nFor any API endpoints returning the endpoint config,\nonly the secret name but not the value will be returned.\nWhen updating the config, also send all secrets that you want\nto keep, setting only the name but not the value. Can be accessed from templates.')
    url: str | None = Field(None, description='HTTP(s) url with optional port.')

class GetConfigNotificationsEndpointsWebhookResponse(RootModel[list[GetConfigNotificationsEndpointsWebhookResponseItem]]):
    """List of items. None. List all webhook endpoints. response."""
    root: list[GetConfigNotificationsEndpointsWebhookResponseItem] = Field(..., description='List of webhook endpoints.')

class PostConfigNotificationsEndpointsWebhookRequest(ProxmoxBaseModel):
    """Model for None. Add a new webhook endpoint. request."""
    body: str | None = Field(None, description='The HTTP body to send. Supports templating.')
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    header: list[str] | None = Field(None, description='Array of HTTP headers. Each entry is a property string with a name and a value.\nThe value property contains the header in base64 encoding. Supports templating.')
    method: str = Field(..., description='HTTP Method to use.')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    secret: list[str] | None = Field(None, description='Array of secrets. Each entry is a property string with a name and an optional value.\nThe value property contains the secret in base64 encoding.\nFor any API endpoints returning the endpoint config,\nonly the secret name but not the value will be returned.\nWhen updating the config, also send all secrets that you want\nto keep, setting only the name but not the value. Can be accessed from templates.')
    url: str = Field(..., description='HTTP(s) url with optional port.')

class PostConfigNotificationsEndpointsWebhookResponse(RootModel[None]):
    """Model for None. Add a new webhook endpoint. response."""
    root: None = Field(...)

class DeleteConfigNotificationsEndpointsWebhookNameRequest(RootModel[dict[str, object]]):
    """Model for None. Delete webhook endpoint. request."""
    root: dict[str, object] = Field(...)

class DeleteConfigNotificationsEndpointsWebhookNameResponse(RootModel[None]):
    """Model for None. Delete webhook endpoint. response."""
    root: None = Field(...)

class GetConfigNotificationsEndpointsWebhookNameResponse(ProxmoxBaseModel):
    """Model for None. Get a webhook endpoint. response."""
    body: str | None = Field(None, description='The HTTP body to send. Supports templating.')
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this target.')
    header: list[str] | None = Field(None, description='Array of HTTP headers. Each entry is a property string with a name and a value.\nThe value property contains the header in base64 encoding. Supports templating.')
    method: str = Field(..., description='HTTP Method to use.')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    secret: list[str] | None = Field(None, description='Array of secrets. Each entry is a property string with a name and an optional value.\nThe value property contains the secret in base64 encoding.\nFor any API endpoints returning the endpoint config,\nonly the secret name but not the value will be returned.\nWhen updating the config, also send all secrets that you want\nto keep, setting only the name but not the value. Can be accessed from templates.')
    url: str = Field(..., description='HTTP(s) url with optional port.')

class PutConfigNotificationsEndpointsWebhookNameRequest(ProxmoxBaseModel):
    """Model for None. Update webhook endpoint. request."""
    body: str | None = Field(None, description='The HTTP body to send. Supports templating.')
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this target.')
    header: list[str] | None = Field(None, description='Array of HTTP headers. Each entry is a property string with a name and a value.\nThe value property contains the header in base64 encoding. Supports templating.')
    method: str | None = Field(None, description='HTTP Method to use.')
    secret: list[str] | None = Field(None, description='Array of secrets. Each entry is a property string with a name and an optional value.\nThe value property contains the secret in base64 encoding.\nFor any API endpoints returning the endpoint config,\nonly the secret name but not the value will be returned.\nWhen updating the config, also send all secrets that you want\nto keep, setting only the name but not the value. Can be accessed from templates.')
    url: str | None = Field(None, description='HTTP(s) url with optional port.')

class PutConfigNotificationsEndpointsWebhookNameResponse(RootModel[None]):
    """Model for None. Update webhook endpoint. response."""
    root: None = Field(...)

class GetConfigNotificationsMatcherFieldValuesResponseItem(ProxmoxBaseModel):
    """Model for None. List all known, matchable metadata field values. response."""
    comment: str | None = Field(None, description='Additional comment for this value.')
    field: str | None = Field(None, description='Field this value belongs to.')
    value: str | None = Field(None, description='Notification metadata value known by the system.')

class GetConfigNotificationsMatcherFieldValuesResponse(RootModel[list[GetConfigNotificationsMatcherFieldValuesResponseItem]]):
    """List of items. None. List all known, matchable metadata field values. response."""
    root: list[GetConfigNotificationsMatcherFieldValuesResponseItem] = Field(..., description='List of known metadata field values.')

class GetConfigNotificationsMatcherFieldsResponseItem(ProxmoxBaseModel):
    """Model for None. Get all known metadata fields. response."""
    name: str | None = Field(None, description='Name of the field')

class GetConfigNotificationsMatcherFieldsResponse(RootModel[list[GetConfigNotificationsMatcherFieldsResponseItem]]):
    """List of items. None. Get all known metadata fields. response."""
    root: list[GetConfigNotificationsMatcherFieldsResponseItem] = Field(..., description='List of known metadata fields.')

class GetConfigNotificationsMatchersResponseItem(ProxmoxBaseModel):
    """Model for None. List all notification matchers. response."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this matcher.')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole filter.')
    match_calendar: list[str] | None = Field(None, alias="match-calendar", description='List of matched severity levels.')
    match_field: list[str] | None = Field(None, alias="match-field", description='List of matched metadata fields.')
    match_severity: list[str] | None = Field(None, alias="match-severity", description='List of matched severity levels.')
    mode: str | None = Field(None, description='The mode in which the results of matches are combined.')
    name: str | None = Field(None, description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    target: list[str] | None = Field(None, description='Targets to notify.')

class GetConfigNotificationsMatchersResponse(RootModel[list[GetConfigNotificationsMatchersResponseItem]]):
    """List of items. None. List all notification matchers. response."""
    root: list[GetConfigNotificationsMatchersResponseItem] = Field(..., description='List of matchers.')

class PostConfigNotificationsMatchersRequest(ProxmoxBaseModel):
    """Model for None. Add a new notification matcher. request."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this matcher.')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole filter.')
    match_calendar: list[str] | None = Field(None, alias="match-calendar", description='List of matched severity levels.')
    match_field: list[str] | None = Field(None, alias="match-field", description='List of matched metadata fields.')
    match_severity: list[str] | None = Field(None, alias="match-severity", description='List of matched severity levels.')
    mode: str | None = Field(None, description='The mode in which the results of matches are combined.')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    target: list[str] | None = Field(None, description='Targets to notify.')

class PostConfigNotificationsMatchersResponse(RootModel[None]):
    """Model for None. Add a new notification matcher. response."""
    root: None = Field(...)

class DeleteConfigNotificationsMatchersNameRequest(RootModel[dict[str, object]]):
    """Model for None. Delete notification matcher. request."""
    root: dict[str, object] = Field(...)

class DeleteConfigNotificationsMatchersNameResponse(RootModel[None]):
    """Model for None. Delete notification matcher. response."""
    root: None = Field(...)

class GetConfigNotificationsMatchersNameResponse(ProxmoxBaseModel):
    """Model for None. Get a notification matcher. response."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this matcher.')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole filter.')
    match_calendar: list[str] | None = Field(None, alias="match-calendar", description='List of matched severity levels.')
    match_field: list[str] | None = Field(None, alias="match-field", description='List of matched metadata fields.')
    match_severity: list[str] | None = Field(None, alias="match-severity", description='List of matched severity levels.')
    mode: str | None = Field(None, description='The mode in which the results of matches are combined.')
    name: str = Field(..., description='Name schema for targets and matchers')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    target: list[str] | None = Field(None, description='Targets to notify.')

class PutConfigNotificationsMatchersNameRequest(ProxmoxBaseModel):
    """Model for None. Update notification matcher. request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this matcher.')
    invert_match: bool | None = Field(None, alias="invert-match", description='Invert match of the whole filter.')
    match_calendar: list[str] | None = Field(None, alias="match-calendar", description='List of matched severity levels.')
    match_field: list[str] | None = Field(None, alias="match-field", description='List of matched metadata fields.')
    match_severity: list[str] | None = Field(None, alias="match-severity", description='List of matched severity levels.')
    mode: str | None = Field(None, description='The mode in which the results of matches are combined.')
    target: list[str] | None = Field(None, description='Targets to notify.')

class PutConfigNotificationsMatchersNameResponse(RootModel[None]):
    """Model for None. Update notification matcher. response."""
    root: None = Field(...)

class GetConfigNotificationsTargetsResponseItem(ProxmoxBaseModel):
    """Model for None. List all notification targets. response."""
    comment: str | None = Field(None, description='Comment')
    disable: bool | None = Field(None, description='Target is disabled')
    name: str | None = Field(None, description='Name of the endpoint')
    origin: str | None = Field(None, description='The origin of a notification configuration entry.')
    type: str | None = Field(None, description='Type of the endpoint.')

class GetConfigNotificationsTargetsResponse(RootModel[list[GetConfigNotificationsTargetsResponseItem]]):
    """List of items. None. List all notification targets. response."""
    root: list[GetConfigNotificationsTargetsResponseItem] = Field(..., description='List of all entities which can be used as notification targets.')

class GetConfigNotificationsTargetsNameResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostConfigNotificationsTargetsNameTestRequest(RootModel[dict[str, object]]):
    """Model for None. Test a given notification target. request."""
    root: dict[str, object] = Field(...)

class PostConfigNotificationsTargetsNameTestResponse(RootModel[None]):
    """Model for None. Test a given notification target. response."""
    root: None = Field(...)

class GetConfigPruneResponseItem(ProxmoxBaseModel):
    """Model for None. List all scheduled prune jobs. response."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this job.')
    id: str | None = Field(None, description='Job ID.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    schedule: str | None = Field(None, description='Run prune job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')

class GetConfigPruneResponse(RootModel[list[GetConfigPruneResponseItem]]):
    """List of items. None. List all scheduled prune jobs. response."""
    root: list[GetConfigPruneResponseItem] = Field(..., description='List configured prune schedules.')

class PostConfigPruneRequest(ProxmoxBaseModel):
    """Model for None. Create a new prune job. request."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this job.')
    id: str = Field(..., description='Job ID.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    schedule: str = Field(..., description='Run prune job at specified schedule.')
    store: str = Field(..., description='Datastore name.')

class PostConfigPruneResponse(RootModel[None]):
    """Model for None. Create a new prune job. response."""
    root: None = Field(...)

class DeleteConfigPruneIdRequest(ProxmoxBaseModel):
    """Model for None. Remove a prune job configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigPruneIdResponse(RootModel[None]):
    """Model for None. Remove a prune job configuration response."""
    root: None = Field(...)

class GetConfigPruneIdResponse(ProxmoxBaseModel):
    """Model for None. Read a prune job configuration. response."""
    comment: str | None = Field(None, description='Comment.')
    disable: bool | None = Field(None, description='Disable this job.')
    id: str = Field(..., description='Job ID.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    schedule: str = Field(..., description='Run prune job at specified schedule.')
    store: str = Field(..., description='Datastore name.')

class PutConfigPruneIdRequest(ProxmoxBaseModel):
    """Model for None. Update prune job config. request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Disable this job.')
    keep_daily: int | None = Field(None, alias="keep-daily", description='Number of daily backups to keep.')
    keep_hourly: int | None = Field(None, alias="keep-hourly", description='Number of hourly backups to keep.')
    keep_last: int | None = Field(None, alias="keep-last", description='Number of backups to keep.')
    keep_monthly: int | None = Field(None, alias="keep-monthly", description='Number of monthly backups to keep.')
    keep_weekly: int | None = Field(None, alias="keep-weekly", description='Number of weekly backups to keep.')
    keep_yearly: int | None = Field(None, alias="keep-yearly", description='Number of yearly backups to keep.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    schedule: str | None = Field(None, description='Run prune job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')

class PutConfigPruneIdResponse(RootModel[None]):
    """Model for None. Update prune job config. response."""
    root: None = Field(...)

class GetConfigRemoteResponseItem(ProxmoxBaseModel):
    """Model for None. List all remotes response."""
    auth_id: str | None = Field(None, alias="auth-id", description='Authentication ID')
    comment: str | None = Field(None, description='Comment.')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    host: str | None = Field(None, description='DNS name or IP address.')
    name: str | None = Field(None, description='Remote ID.')
    port: int | None = Field(None, description='The (optional) port')
    use_node_proxy: bool | None = Field(None, alias="use-node-proxy", description='Use the http proxy configuration of the node for remote connections.')

class GetConfigRemoteResponse(RootModel[list[GetConfigRemoteResponseItem]]):
    """List of items. None. List all remotes response."""
    root: list[GetConfigRemoteResponseItem] = Field(..., description='The list of configured remotes (with config digest).')

class PostConfigRemoteRequest(ProxmoxBaseModel):
    """Model for None. Create new remote. request."""
    auth_id: str = Field(..., alias="auth-id", description='Authentication ID')
    comment: str | None = Field(None, description='Comment.')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    host: str = Field(..., description='DNS name or IP address.')
    name: str = Field(..., description='Remote ID.')
    password: str = Field(..., description='Password or auth token for remote host.')
    port: int | None = Field(None, description='The (optional) port')
    use_node_proxy: bool | None = Field(None, alias="use-node-proxy", description='Use the http proxy configuration of the node for remote connections.')

class PostConfigRemoteResponse(RootModel[None]):
    """Model for None. Create new remote. response."""
    root: None = Field(...)

class DeleteConfigRemoteNameRequest(ProxmoxBaseModel):
    """Model for None. Remove a remote from the configuration file. request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigRemoteNameResponse(RootModel[None]):
    """Model for None. Remove a remote from the configuration file. response."""
    root: None = Field(...)

class GetConfigRemoteNameResponse(ProxmoxBaseModel):
    """Model for None. Read remote configuration data. response."""
    auth_id: str = Field(..., alias="auth-id", description='Authentication ID')
    comment: str | None = Field(None, description='Comment.')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    host: str = Field(..., description='DNS name or IP address.')
    name: str = Field(..., description='Remote ID.')
    port: int | None = Field(None, description='The (optional) port')
    use_node_proxy: bool | None = Field(None, alias="use-node-proxy", description='Use the http proxy configuration of the node for remote connections.')

class PutConfigRemoteNameRequest(ProxmoxBaseModel):
    """Model for None. Update remote configuration. request."""
    auth_id: str | None = Field(None, alias="auth-id", description='Authentication ID')
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    host: str | None = Field(None, description='DNS name or IP address.')
    password: str | None = Field(None, description='Password or auth token for remote host.')
    port: int | None = Field(None, description='The (optional) port')
    use_node_proxy: bool | None = Field(None, alias="use-node-proxy", description='Use the http proxy configuration of the node for remote connections.')

class PutConfigRemoteNameResponse(RootModel[None]):
    """Model for None. Update remote configuration. response."""
    root: None = Field(...)

class GetConfigRemoteNameScanResponseItem(ProxmoxBaseModel):
    """Model for None. List datastores of a remote.cfg entry response."""
    comment: str | None = Field(None, description='Comment.')
    maintenance: str | None = Field(None, description='If the datastore is in maintenance mode, information about it')
    mount_status: str | None = Field(None, alias="mount-status", description='Current mounting status of a datastore, useful for removable datastores.')
    store: str | None = Field(None, description='Datastore name.')

class GetConfigRemoteNameScanResponse(RootModel[list[GetConfigRemoteNameScanResponseItem]]):
    """List of items. None. List datastores of a remote.cfg entry response."""
    root: list[GetConfigRemoteNameScanResponseItem] = Field(..., description='List the accessible datastores.')

class GetConfigRemoteNameScanStoreResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetConfigRemoteNameScanStoreGroupsResponseItem(ProxmoxBaseModel):
    """Model for None. List groups of a remote.cfg entry's datastore response."""
    backup_count: int | None = Field(None, alias="backup-count", description='Number of contained snapshots')
    backup_id: str | None = Field(None, alias="backup-id", description='Backup ID.')
    backup_type: str | None = Field(None, alias="backup-type", description='Backup types.')
    comment: str | None = Field(None, description='The first line from group "notes"')
    files: list[str] | None = Field(None, description='List of contained archive files.')
    last_backup: int | None = Field(None, alias="last-backup", description='Backup time (Unix epoch.)')
    owner: str | None = Field(None, description='Authentication ID')

class GetConfigRemoteNameScanStoreGroupsResponse(RootModel[list[GetConfigRemoteNameScanStoreGroupsResponseItem]]):
    """List of items. None. List groups of a remote.cfg entry's datastore response."""
    root: list[GetConfigRemoteNameScanStoreGroupsResponseItem] = Field(..., description='Lists the accessible backup groups in a remote datastore.')

class GetConfigRemoteNameScanStoreNamespacesResponseItem(ProxmoxBaseModel):
    """Model for None. List namespaces of a datastore of a remote.cfg entry response."""
    comment: str | None = Field(None, description='The first line from the namespace\'s "notes"')
    ns: str | None = Field(None, description='Namespace.')

class GetConfigRemoteNameScanStoreNamespacesResponse(RootModel[list[GetConfigRemoteNameScanStoreNamespacesResponseItem]]):
    """List of items. None. List namespaces of a datastore of a remote.cfg entry response."""
    root: list[GetConfigRemoteNameScanStoreNamespacesResponseItem] = Field(..., description='List the accessible namespaces of a remote datastore.')

class GetConfigS3ResponseItem(ProxmoxBaseModel):
    """Model for None. List all s3 client configurations. response."""
    access_key: str | None = Field(None, alias="access-key", description='Access key for S3 object store.')
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    endpoint: str | None = Field(None, description='Endpoint to access S3 object store.')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    id: str | None = Field(None, description='ID to uniquely identify s3 client config.')
    path_style: bool | None = Field(None, alias="path-style", description='Use path style bucket addressing over vhost style.')
    port: int | None = Field(None, description='Port to access S3 object store.')
    provider_quirks: list[str] | None = Field(None, alias="provider-quirks", description='List of provider specific feature implementation quirks.')
    put_rate_limit: int | None = Field(None, alias="put-rate-limit", description='Rate limit for put requests given as #request/s.')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    region: str | None = Field(None, description='Region to access S3 object store.')

class GetConfigS3Response(RootModel[list[GetConfigS3ResponseItem]]):
    """List of items. None. List all s3 client configurations. response."""
    root: list[GetConfigS3ResponseItem] = Field(..., description='List configured s3 clients.')

class PostConfigS3Request(ProxmoxBaseModel):
    """Model for None. Create a new s3 client configuration. request."""
    access_key: str = Field(..., alias="access-key", description='Access key for S3 object store.')
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    endpoint: str = Field(..., description='Endpoint to access S3 object store.')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    id: str = Field(..., description='ID to uniquely identify s3 client config.')
    path_style: bool | None = Field(None, alias="path-style", description='Use path style bucket addressing over vhost style.')
    port: int | None = Field(None, description='Port to access S3 object store.')
    provider_quirks: list[str] | None = Field(None, alias="provider-quirks", description='List of provider specific feature implementation quirks.')
    put_rate_limit: int | None = Field(None, alias="put-rate-limit", description='Rate limit for put requests given as #request/s.')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    region: str | None = Field(None, description='Region to access S3 object store.')
    secret_key: str = Field(..., alias="secret-key", description='S3 secret key')

class PostConfigS3Response(RootModel[None]):
    """Model for None. Create a new s3 client configuration. response."""
    root: None = Field(...)

class DeleteConfigS3IdRequest(ProxmoxBaseModel):
    """Model for None. Remove an s3 client configuration. request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigS3IdResponse(RootModel[None]):
    """Model for None. Remove an s3 client configuration. response."""
    root: None = Field(...)

class GetConfigS3IdResponse(ProxmoxBaseModel):
    """Model for None. Read an s3 client configuration. response."""
    access_key: str = Field(..., alias="access-key", description='Access key for S3 object store.')
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    endpoint: str = Field(..., description='Endpoint to access S3 object store.')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    id: str = Field(..., description='ID to uniquely identify s3 client config.')
    path_style: bool | None = Field(None, alias="path-style", description='Use path style bucket addressing over vhost style.')
    port: int | None = Field(None, description='Port to access S3 object store.')
    provider_quirks: list[str] | None = Field(None, alias="provider-quirks", description='List of provider specific feature implementation quirks.')
    put_rate_limit: int | None = Field(None, alias="put-rate-limit", description='Rate limit for put requests given as #request/s.')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    region: str | None = Field(None, description='Region to access S3 object store.')

class PutConfigS3IdRequest(ProxmoxBaseModel):
    """Model for None. Update an s3 client configuration. request."""
    access_key: str | None = Field(None, alias="access-key", description='Access key for S3 object store.')
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    endpoint: str | None = Field(None, description='Endpoint to access S3 object store.')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    path_style: bool | None = Field(None, alias="path-style", description='Use path style bucket addressing over vhost style.')
    port: int | None = Field(None, description='Port to access S3 object store.')
    provider_quirks: list[str] | None = Field(None, alias="provider-quirks", description='List of provider specific feature implementation quirks.')
    put_rate_limit: int | None = Field(None, alias="put-rate-limit", description='Rate limit for put requests given as #request/s.')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    region: str | None = Field(None, description='Region to access S3 object store.')
    secret_key: str | None = Field(None, alias="secret-key", description='S3 client secret key.')

class PutConfigS3IdResponse(RootModel[None]):
    """Model for None. Update an s3 client configuration. response."""
    root: None = Field(...)

class GetConfigS3IdListBucketsResponse(RootModel[None]):
    """Model for None. List buckets accessible by given s3 client configuration response."""
    root: None = Field(...)

class GetConfigSyncResponseItem(ProxmoxBaseModel):
    """Model for None. List all sync jobs response."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    encrypted_only: bool | None = Field(None, alias="encrypted-only", description='Only synchronize encrypted backup snapshots, exclude others.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    id: str | None = Field(None, description='Job ID.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    owner: str | None = Field(None, description='Authentication ID')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    remote: str | None = Field(None, description='Remote ID.')
    remote_ns: str | None = Field(None, alias="remote-ns", description='Namespace.')
    remote_store: str | None = Field(None, alias="remote-store", description='Datastore name.')
    remove_vanished: bool | None = Field(None, alias="remove-vanished", description='Delete vanished backups. This remove the local copy if the remote backup was deleted.')
    resync_corrupt: bool | None = Field(None, alias="resync-corrupt", description='If the verification failed for a local snapshot, try to pull it again.')
    run_on_mount: bool | None = Field(None, alias="run-on-mount", description='Run this job when a relevant datastore is mounted.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    sync_direction: str | None = Field(None, alias="sync-direction", description='Direction of the sync job, push or pull')
    transfer_last: int | None = Field(None, alias="transfer-last", description='Limit transfer to last N snapshots (per group), skipping others')
    unmount_on_done: bool | None = Field(None, alias="unmount-on-done", description="Unmount involved removable datastore after the sync job finishes. Requires 'run-on-mount' to be enabled.")
    verified_only: bool | None = Field(None, alias="verified-only", description='Only synchronize verified backup snapshots, exclude others.')

class GetConfigSyncResponse(RootModel[list[GetConfigSyncResponseItem]]):
    """List of items. None. List all sync jobs response."""
    root: list[GetConfigSyncResponseItem] = Field(..., description='List configured jobs.')

class PostConfigSyncRequest(ProxmoxBaseModel):
    """Model for None. Create a new sync job. request."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    encrypted_only: bool | None = Field(None, alias="encrypted-only", description='Only synchronize encrypted backup snapshots, exclude others.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    id: str = Field(..., description='Job ID.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    owner: str | None = Field(None, description='Authentication ID')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    remote: str | None = Field(None, description='Remote ID.')
    remote_ns: str | None = Field(None, alias="remote-ns", description='Namespace.')
    remote_store: str = Field(..., alias="remote-store", description='Datastore name.')
    remove_vanished: bool | None = Field(None, alias="remove-vanished", description='Delete vanished backups. This remove the local copy if the remote backup was deleted.')
    resync_corrupt: bool | None = Field(None, alias="resync-corrupt", description='If the verification failed for a local snapshot, try to pull it again.')
    run_on_mount: bool | None = Field(None, alias="run-on-mount", description='Run this job when a relevant datastore is mounted.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str = Field(..., description='Datastore name.')
    sync_direction: str | None = Field(None, alias="sync-direction", description='Direction of the sync job, push or pull')
    transfer_last: int | None = Field(None, alias="transfer-last", description='Limit transfer to last N snapshots (per group), skipping others')
    unmount_on_done: bool | None = Field(None, alias="unmount-on-done", description="Unmount involved removable datastore after the sync job finishes. Requires 'run-on-mount' to be enabled.")
    verified_only: bool | None = Field(None, alias="verified-only", description='Only synchronize verified backup snapshots, exclude others.')

class PostConfigSyncResponse(RootModel[None]):
    """Model for None. Create a new sync job. response."""
    root: None = Field(...)

class DeleteConfigSyncIdRequest(ProxmoxBaseModel):
    """Model for None. Remove a sync job configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigSyncIdResponse(RootModel[None]):
    """Model for None. Remove a sync job configuration response."""
    root: None = Field(...)

class GetConfigSyncIdResponse(ProxmoxBaseModel):
    """Model for None. Read a sync job configuration. response."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    encrypted_only: bool | None = Field(None, alias="encrypted-only", description='Only synchronize encrypted backup snapshots, exclude others.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    id: str = Field(..., description='Job ID.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    owner: str | None = Field(None, description='Authentication ID')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    remote: str | None = Field(None, description='Remote ID.')
    remote_ns: str | None = Field(None, alias="remote-ns", description='Namespace.')
    remote_store: str = Field(..., alias="remote-store", description='Datastore name.')
    remove_vanished: bool | None = Field(None, alias="remove-vanished", description='Delete vanished backups. This remove the local copy if the remote backup was deleted.')
    resync_corrupt: bool | None = Field(None, alias="resync-corrupt", description='If the verification failed for a local snapshot, try to pull it again.')
    run_on_mount: bool | None = Field(None, alias="run-on-mount", description='Run this job when a relevant datastore is mounted.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str = Field(..., description='Datastore name.')
    sync_direction: str | None = Field(None, alias="sync-direction", description='Direction of the sync job, push or pull')
    transfer_last: int | None = Field(None, alias="transfer-last", description='Limit transfer to last N snapshots (per group), skipping others')
    unmount_on_done: bool | None = Field(None, alias="unmount-on-done", description="Unmount involved removable datastore after the sync job finishes. Requires 'run-on-mount' to be enabled.")
    verified_only: bool | None = Field(None, alias="verified-only", description='Only synchronize verified backup snapshots, exclude others.')

class PutConfigSyncIdRequest(ProxmoxBaseModel):
    """Model for None. Update sync job config. request."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    encrypted_only: bool | None = Field(None, alias="encrypted-only", description='Only synchronize encrypted backup snapshots, exclude others.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    owner: str | None = Field(None, description='Authentication ID')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    remote: str | None = Field(None, description='Remote ID.')
    remote_ns: str | None = Field(None, alias="remote-ns", description='Namespace.')
    remote_store: str | None = Field(None, alias="remote-store", description='Datastore name.')
    remove_vanished: bool | None = Field(None, alias="remove-vanished", description='Delete vanished backups. This remove the local copy if the remote backup was deleted.')
    resync_corrupt: bool | None = Field(None, alias="resync-corrupt", description='If the verification failed for a local snapshot, try to pull it again.')
    run_on_mount: bool | None = Field(None, alias="run-on-mount", description='Run this job when a relevant datastore is mounted.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    sync_direction: str | None = Field(None, alias="sync-direction", description='Direction of the sync job, push or pull')
    transfer_last: int | None = Field(None, alias="transfer-last", description='Limit transfer to last N snapshots (per group), skipping others')
    unmount_on_done: bool | None = Field(None, alias="unmount-on-done", description="Unmount involved removable datastore after the sync job finishes. Requires 'run-on-mount' to be enabled.")
    verified_only: bool | None = Field(None, alias="verified-only", description='Only synchronize verified backup snapshots, exclude others.')

class PutConfigSyncIdResponse(RootModel[None]):
    """Model for None. Update sync job config. response."""
    root: None = Field(...)

class GetConfigTapeBackupJobResponseItem(ProxmoxBaseModel):
    """Model for None. List all tape backup jobs response."""
    comment: str | None = Field(None, description='Comment.')
    drive: str | None = Field(None, description='Drive Identifier.')
    eject_media: bool | None = Field(None, alias="eject-media", description='Eject media upon job completion.')
    export_media_set: bool | None = Field(None, alias="export-media-set", description='Export media set upon job completion.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    id: str | None = Field(None, description='Job ID.')
    latest_only: bool | None = Field(None, alias="latest-only", description='Backup latest snapshots only.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    ns: str | None = Field(None, description='Namespace.')
    pool: str | None = Field(None, description='Media pool name.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    worker_threads: int | None = Field(None, alias="worker-threads", description='The number of threads to use for the tape backup job.')

class GetConfigTapeBackupJobResponse(RootModel[list[GetConfigTapeBackupJobResponseItem]]):
    """List of items. None. List all tape backup jobs response."""
    root: list[GetConfigTapeBackupJobResponseItem] = Field(..., description='List configured jobs.')

class PostConfigTapeBackupJobRequest(ProxmoxBaseModel):
    """Model for None. Create a new tape backup job. request."""
    comment: str | None = Field(None, description='Comment.')
    drive: str = Field(..., description='Drive Identifier.')
    eject_media: bool | None = Field(None, alias="eject-media", description='Eject media upon job completion.')
    export_media_set: bool | None = Field(None, alias="export-media-set", description='Export media set upon job completion.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    id: str = Field(..., description='Job ID.')
    latest_only: bool | None = Field(None, alias="latest-only", description='Backup latest snapshots only.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    ns: str | None = Field(None, description='Namespace.')
    pool: str = Field(..., description='Media pool name.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str = Field(..., description='Datastore name.')
    worker_threads: int | None = Field(None, alias="worker-threads", description='The number of threads to use for the tape backup job.')

class PostConfigTapeBackupJobResponse(RootModel[None]):
    """Model for None. Create a new tape backup job. response."""
    root: None = Field(...)

class DeleteConfigTapeBackupJobIdRequest(ProxmoxBaseModel):
    """Model for None. Remove a tape backup job configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigTapeBackupJobIdResponse(RootModel[None]):
    """Model for None. Remove a tape backup job configuration response."""
    root: None = Field(...)

class GetConfigTapeBackupJobIdResponse(ProxmoxBaseModel):
    """Model for None. Read a tape backup job configuration. response."""
    comment: str | None = Field(None, description='Comment.')
    drive: str = Field(..., description='Drive Identifier.')
    eject_media: bool | None = Field(None, alias="eject-media", description='Eject media upon job completion.')
    export_media_set: bool | None = Field(None, alias="export-media-set", description='Export media set upon job completion.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    id: str = Field(..., description='Job ID.')
    latest_only: bool | None = Field(None, alias="latest-only", description='Backup latest snapshots only.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    ns: str | None = Field(None, description='Namespace.')
    pool: str = Field(..., description='Media pool name.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str = Field(..., description='Datastore name.')
    worker_threads: int | None = Field(None, alias="worker-threads", description='The number of threads to use for the tape backup job.')

class PutConfigTapeBackupJobIdRequest(ProxmoxBaseModel):
    """Model for None. Update the tape backup job request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    drive: str | None = Field(None, description='Drive Identifier.')
    eject_media: bool | None = Field(None, alias="eject-media", description='Eject media upon job completion.')
    export_media_set: bool | None = Field(None, alias="export-media-set", description='Export media set upon job completion.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    latest_only: bool | None = Field(None, alias="latest-only", description='Backup latest snapshots only.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    ns: str | None = Field(None, description='Namespace.')
    pool: str | None = Field(None, description='Media pool name.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    worker_threads: int | None = Field(None, alias="worker-threads", description='The number of threads to use for the tape backup job.')

class PutConfigTapeBackupJobIdResponse(RootModel[None]):
    """Model for None. Update the tape backup job response."""
    root: None = Field(...)

class GetConfigTapeEncryptionKeysResponseItem(ProxmoxBaseModel):
    """Model for None. List existing keys response."""
    created: int | None = Field(None, description='Key creation time')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    hint: str | None = Field(None, description='Password hint')
    kdf: str | None = Field(None, description='Key derivation function for password protected encryption keys.')
    modified: int | None = Field(None, description='Key modification time')
    path: str | None = Field(None, description='Path to key (if stored in a file)')

class GetConfigTapeEncryptionKeysResponse(RootModel[list[GetConfigTapeEncryptionKeysResponseItem]]):
    """List of items. None. List existing keys response."""
    root: list[GetConfigTapeEncryptionKeysResponseItem] = Field(..., description='The list of tape encryption keys (with config digest).')

class PostConfigTapeEncryptionKeysRequest(ProxmoxBaseModel):
    """Model for None. Create a new encryption key request."""
    hint: str | None = Field(None, description='Password hint.')
    kdf: str | None = Field(None, description='Key derivation function for password protected encryption keys.')
    key: str | None = Field(None, description='Restore/Re-create a key from this JSON string.')
    password: str = Field(..., description='A secret password.')

class PostConfigTapeEncryptionKeysResponse(RootModel[str]):
    """Model for None. Create a new encryption key response."""
    root: str = Field(..., description='Tape encryption key fingerprint (sha256).')

class DeleteConfigTapeEncryptionKeysFingerprintRequest(ProxmoxBaseModel):
    """Model for None. Remove a encryption key from the database

Please note that you can no longer access tapes using this key. request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigTapeEncryptionKeysFingerprintResponse(RootModel[None]):
    """Model for None. Remove a encryption key from the database

Please note that you can no longer access tapes using this key. response."""
    root: None = Field(...)

class GetConfigTapeEncryptionKeysFingerprintResponse(ProxmoxBaseModel):
    """Model for None. Get key config (public key part) response."""
    created: int = Field(..., description='Key creation time')
    fingerprint: str | None = Field(None, description='X509 certificate fingerprint (sha256).')
    hint: str | None = Field(None, description='Password hint')
    kdf: str = Field(..., description='Key derivation function for password protected encryption keys.')
    modified: int = Field(..., description='Key modification time')
    path: str | None = Field(None, description='Path to key (if stored in a file)')

class PutConfigTapeEncryptionKeysFingerprintRequest(ProxmoxBaseModel):
    """Model for None. Change the encryption key's password (and password hint). request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    force: bool | None = Field(None, description='Reset the passphrase for a tape key, using the root-only accessible copy.')
    hint: str = Field(..., description='Password hint.')
    kdf: str | None = Field(None, description='Key derivation function for password protected encryption keys.')
    new_password: str = Field(..., alias="new-password", description='The new password.')
    password: str | None = Field(None, description='The current password.')

class PutConfigTapeEncryptionKeysFingerprintResponse(RootModel[None]):
    """Model for None. Change the encryption key's password (and password hint). response."""
    root: None = Field(...)

class GetConfigTrafficControlResponseItem(ProxmoxBaseModel):
    """Model for None. List traffic control rules response."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    name: str | None = Field(None, description='Rule ID.')
    network: list[str] | None = Field(None, description='Rule applies to Source IPs within this networks')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    timeframe: list[str] | None = Field(None, description='Enable the rule at specific times')
    users: list[str] | None = Field(None, description='Rule applies to authenticated API requests of any of these users (overrides IP-only rules)')

class GetConfigTrafficControlResponse(RootModel[list[GetConfigTrafficControlResponseItem]]):
    """List of items. None. List traffic control rules response."""
    root: list[GetConfigTrafficControlResponseItem] = Field(..., description='The list of configured traffic control rules (with config digest).')

class PostConfigTrafficControlRequest(ProxmoxBaseModel):
    """Model for None. Create new traffic control rule. request."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    name: str = Field(..., description='Rule ID.')
    network: list[str] = Field(..., description='Rule applies to Source IPs within this networks')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    timeframe: list[str] | None = Field(None, description='Enable the rule at specific times')
    users: list[str] | None = Field(None, description='Rule applies to authenticated API requests of any of these users (overrides IP-only rules)')

class PostConfigTrafficControlResponse(RootModel[None]):
    """Model for None. Create new traffic control rule. response."""
    root: None = Field(...)

class DeleteConfigTrafficControlNameRequest(ProxmoxBaseModel):
    """Model for None. Remove a traffic control rule from the configuration file. request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigTrafficControlNameResponse(RootModel[None]):
    """Model for None. Remove a traffic control rule from the configuration file. response."""
    root: None = Field(...)

class GetConfigTrafficControlNameResponse(ProxmoxBaseModel):
    """Model for None. Read traffic control configuration data. response."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    name: str = Field(..., description='Rule ID.')
    network: list[str] = Field(..., description='Rule applies to Source IPs within this networks')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    timeframe: list[str] | None = Field(None, description='Enable the rule at specific times')
    users: list[str] | None = Field(None, description='Rule applies to authenticated API requests of any of these users (overrides IP-only rules)')

class PutConfigTrafficControlNameRequest(ProxmoxBaseModel):
    """Model for None. Update traffic control configuration. request."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    network: list[str] | None = Field(None, description='Rule applies to Source IPs within this networks')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    timeframe: list[str] | None = Field(None, description='Enable the rule at specific times')
    users: list[str] | None = Field(None, description='Rule applies to authenticated API requests of any of these users (overrides IP-only rules)')

class PutConfigTrafficControlNameResponse(RootModel[None]):
    """Model for None. Update traffic control configuration. response."""
    root: None = Field(...)

class GetConfigVerifyResponseItem(ProxmoxBaseModel):
    """Model for None. List all verification jobs response."""
    comment: str | None = Field(None, description='Comment.')
    id: str | None = Field(None, description='Job ID.')
    ignore_verified: bool | None = Field(None, alias="ignore-verified", description='Do not verify backups that are already verified if their verification is not outdated.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    ns: str | None = Field(None, description='Namespace.')
    outdated_after: int | None = Field(None, alias="outdated-after", description="Days after that a verification becomes outdated. (0 is deprecated)'")
    read_threads: int | None = Field(None, alias="read-threads", description='The number of threads to use for reading chunks in verify job.')
    schedule: str | None = Field(None, description='Run verify job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    verify_threads: int | None = Field(None, alias="verify-threads", description='The number of threads to use for verifying chunks in verify job.')

class GetConfigVerifyResponse(RootModel[list[GetConfigVerifyResponseItem]]):
    """List of items. None. List all verification jobs response."""
    root: list[GetConfigVerifyResponseItem] = Field(..., description='List configured jobs.')

class PostConfigVerifyRequest(ProxmoxBaseModel):
    """Model for None. Create a new verification job. request."""
    comment: str | None = Field(None, description='Comment.')
    id: str = Field(..., description='Job ID.')
    ignore_verified: bool | None = Field(None, alias="ignore-verified", description='Do not verify backups that are already verified if their verification is not outdated.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    ns: str | None = Field(None, description='Namespace.')
    outdated_after: int | None = Field(None, alias="outdated-after", description="Days after that a verification becomes outdated. (0 is deprecated)'")
    read_threads: int | None = Field(None, alias="read-threads", description='The number of threads to use for reading chunks in verify job.')
    schedule: str | None = Field(None, description='Run verify job at specified schedule.')
    store: str = Field(..., description='Datastore name.')
    verify_threads: int | None = Field(None, alias="verify-threads", description='The number of threads to use for verifying chunks in verify job.')

class PostConfigVerifyResponse(RootModel[None]):
    """Model for None. Create a new verification job. response."""
    root: None = Field(...)

class DeleteConfigVerifyIdRequest(ProxmoxBaseModel):
    """Model for None. Remove a verification job configuration request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteConfigVerifyIdResponse(RootModel[None]):
    """Model for None. Remove a verification job configuration response."""
    root: None = Field(...)

class GetConfigVerifyIdResponse(ProxmoxBaseModel):
    """Model for None. Read a verification job configuration. response."""
    comment: str | None = Field(None, description='Comment.')
    id: str = Field(..., description='Job ID.')
    ignore_verified: bool | None = Field(None, alias="ignore-verified", description='Do not verify backups that are already verified if their verification is not outdated.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    ns: str | None = Field(None, description='Namespace.')
    outdated_after: int | None = Field(None, alias="outdated-after", description="Days after that a verification becomes outdated. (0 is deprecated)'")
    read_threads: int | None = Field(None, alias="read-threads", description='The number of threads to use for reading chunks in verify job.')
    schedule: str | None = Field(None, description='Run verify job at specified schedule.')
    store: str = Field(..., description='Datastore name.')
    verify_threads: int | None = Field(None, alias="verify-threads", description='The number of threads to use for verifying chunks in verify job.')

class PutConfigVerifyIdRequest(ProxmoxBaseModel):
    """Model for None. Update verification job config. request."""
    comment: str | None = Field(None, description='Comment.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    ignore_verified: bool | None = Field(None, alias="ignore-verified", description='Do not verify backups that are already verified if their verification is not outdated.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    ns: str | None = Field(None, description='Namespace.')
    outdated_after: int | None = Field(None, alias="outdated-after", description="Days after that a verification becomes outdated. (0 is deprecated)'")
    read_threads: int | None = Field(None, alias="read-threads", description='The number of threads to use for reading chunks in verify job.')
    schedule: str | None = Field(None, description='Run verify job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    verify_threads: int | None = Field(None, alias="verify-threads", description='The number of threads to use for verifying chunks in verify job.')

class PutConfigVerifyIdResponse(RootModel[None]):
    """Model for None. Update verification job config. response."""
    root: None = Field(...)

class GetNodesResponse(RootModel[None]):
    """Model for None. List Nodes (only for compatibility) response."""
    root: None = Field(...)

class GetNodesNodeResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetNodesNodeAptResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetNodesNodeAptChangelogResponse(RootModel[str]):
    """Model for None. Retrieve the changelog of the specified package. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetNodesNodeAptRepositoriesResponse(ProxmoxBaseModel):
    """Model for None. Get APT repository information. response."""
    digest: str = Field(..., description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    errors: list[dict[str, object]] = Field(..., description='List of problematic files.')
    files: list[dict[str, object]] = Field(..., description='List of parsed repository files.')
    infos: list[dict[str, object]] = Field(..., description='List of additional information/warnings about the repositories')
    standard_repos: list[dict[str, object]] = Field(..., alias="standard-repos", description='List of standard repositories and their configuration status.')

class PostNodesNodeAptRepositoriesRequest(ProxmoxBaseModel):
    """Model for None. Change the properties of the specified repository.

The `digest` parameter asserts that the configuration has not been modified. request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    enabled: bool | None = Field(None, description='Whether the repository should be enabled or not.')
    index: int = Field(..., description='Index within the file (starting from 0).')
    path: str = Field(..., description='Path to the containing file.')

class PostNodesNodeAptRepositoriesResponse(RootModel[None]):
    """Model for None. Change the properties of the specified repository.

The `digest` parameter asserts that the configuration has not been modified. response."""
    root: None = Field(...)

class PutNodesNodeAptRepositoriesRequest(ProxmoxBaseModel):
    """Model for None. Add the repository identified by the `handle`.
If the repository is already configured, it will be set to enabled.

The `digest` parameter asserts that the configuration has not been modified. request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    handle: str = Field(..., description='Handles for Proxmox repositories.')

class PutNodesNodeAptRepositoriesResponse(RootModel[None]):
    """Model for None. Add the repository identified by the `handle`.
If the repository is already configured, it will be set to enabled.

The `digest` parameter asserts that the configuration has not been modified. response."""
    root: None = Field(...)

class GetNodesNodeAptUpdateResponseItem(ProxmoxBaseModel):
    """Model for None. List available APT updates response."""
    arch: str | None = Field(None, alias="Arch", description='Package architecture')
    description: str | None = Field(None, alias="Description", description='Human readable package description')
    extra_info: str | None = Field(None, alias="ExtraInfo", description='Custom extra field for additional package information')
    old_version: str | None = Field(None, alias="OldVersion", description='Old version currently installed')
    origin: str | None = Field(None, alias="Origin", description='Package origin')
    package: str | None = Field(None, alias="Package", description='Package name')
    priority: str | None = Field(None, alias="Priority", description='Package priority in human-readable form')
    section: str | None = Field(None, alias="Section", description='Package section')
    title: str | None = Field(None, alias="Title", description='Package title')
    version: str | None = Field(None, alias="Version", description='New version to be updated to')

class GetNodesNodeAptUpdateResponse(RootModel[list[GetNodesNodeAptUpdateResponseItem]]):
    """List of items. None. List available APT updates response."""
    root: list[GetNodesNodeAptUpdateResponseItem] = Field(..., description='A list of packages with available updates.')

class PostNodesNodeAptUpdateRequest(ProxmoxBaseModel):
    """Model for None. Update the APT database request."""
    notify: bool | None = Field(None, description="Send notification mail about new package updates available to the email\naddress configured for 'root@pam').")
    quiet: bool | None = Field(None, description='Only produces output suitable for logging, omitting progress indicators.')

class PostNodesNodeAptUpdateResponse(RootModel[str]):
    """Model for None. Update the APT database response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetNodesNodeAptVersionsResponseItem(ProxmoxBaseModel):
    """Model for None. Get package information for important Proxmox Backup Server packages. response."""
    arch: str | None = Field(None, alias="Arch", description='Package architecture')
    description: str | None = Field(None, alias="Description", description='Human readable package description')
    extra_info: str | None = Field(None, alias="ExtraInfo", description='Custom extra field for additional package information')
    old_version: str | None = Field(None, alias="OldVersion", description='Old version currently installed')
    origin: str | None = Field(None, alias="Origin", description='Package origin')
    package: str | None = Field(None, alias="Package", description='Package name')
    priority: str | None = Field(None, alias="Priority", description='Package priority in human-readable form')
    section: str | None = Field(None, alias="Section", description='Package section')
    title: str | None = Field(None, alias="Title", description='Package title')
    version: str | None = Field(None, alias="Version", description='New version to be updated to')

class GetNodesNodeAptVersionsResponse(RootModel[list[GetNodesNodeAptVersionsResponseItem]]):
    """List of items. None. Get package information for important Proxmox Backup Server packages. response."""
    root: list[GetNodesNodeAptVersionsResponseItem] = Field(..., description='List of more relevant packages.')

class GetNodesNodeCertificatesResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetNodesNodeCertificatesAcmeResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostNodesNodeCertificatesAcmeCertificateRequest(ProxmoxBaseModel):
    """Model for None. Order a new ACME certificate. request."""
    force: bool | None = Field(None, description='Force replacement of existing files.')

class PostNodesNodeCertificatesAcmeCertificateResponse(RootModel[None]):
    """Model for None. Order a new ACME certificate. response."""
    root: None = Field(...)

class PutNodesNodeCertificatesAcmeCertificateRequest(ProxmoxBaseModel):
    """Model for None. Renew the current ACME certificate if it expires within 30 days (or always if the `force`
parameter is set). request."""
    force: bool | None = Field(None, description='Force replacement of existing files.')

class PutNodesNodeCertificatesAcmeCertificateResponse(RootModel[None]):
    """Model for None. Renew the current ACME certificate if it expires within 30 days (or always if the `force`
parameter is set). response."""
    root: None = Field(...)

class DeleteNodesNodeCertificatesCustomRequest(ProxmoxBaseModel):
    """Model for None. Delete the current certificate and regenerate a self signed one. request."""
    restart: bool | None = Field(None, description='UI compatibility parameter, ignored')

class DeleteNodesNodeCertificatesCustomResponse(RootModel[None]):
    """Model for None. Delete the current certificate and regenerate a self signed one. response."""
    root: None = Field(...)

class PostNodesNodeCertificatesCustomRequest(ProxmoxBaseModel):
    """Model for None. Upload a custom certificate. request."""
    certificates: str = Field(..., description='PEM encoded certificate (chain).')
    force: bool | None = Field(None, description='Force replacement of existing files.')
    key: str | None = Field(None, description='PEM encoded private key.')
    restart: bool | None = Field(None, description='UI compatibility parameter, ignored')

class PostNodesNodeCertificatesCustomResponseItem(ProxmoxBaseModel):
    """Model for None. Upload a custom certificate. response."""
    filename: str | None = Field(None, description='Certificate file name.')
    fingerprint: str | None = Field(None, description='The SSL Fingerprint.')
    issuer: str | None = Field(None, description='Certificate issuer name.')
    notafter: int | None = Field(None, description="Certificate's notAfter timestamp (UNIX epoch).")
    notbefore: int | None = Field(None, description="Certificate's notBefore timestamp (UNIX epoch).")
    pem: str | None = Field(None, description='Certificate in PEM format.')
    public_key_bits: int | None = Field(None, alias="public-key-bits", description="Certificate's public key size if available.")
    public_key_type: str | None = Field(None, alias="public-key-type", description="Certificate's public key algorithm.")
    san: list[str] | None = Field(None, description="List of certificate's SubjectAlternativeName entries.")
    subject: str | None = Field(None, description='Certificate subject name.')

class PostNodesNodeCertificatesCustomResponse(RootModel[list[PostNodesNodeCertificatesCustomResponseItem]]):
    """List of items. None. Upload a custom certificate. response."""
    root: list[PostNodesNodeCertificatesCustomResponseItem] = Field(..., description='List of certificate infos.')

class GetNodesNodeCertificatesInfoResponseItem(ProxmoxBaseModel):
    """Model for None. Get certificate info. response."""
    filename: str | None = Field(None, description='Certificate file name.')
    fingerprint: str | None = Field(None, description='The SSL Fingerprint.')
    issuer: str | None = Field(None, description='Certificate issuer name.')
    notafter: int | None = Field(None, description="Certificate's notAfter timestamp (UNIX epoch).")
    notbefore: int | None = Field(None, description="Certificate's notBefore timestamp (UNIX epoch).")
    pem: str | None = Field(None, description='Certificate in PEM format.')
    public_key_bits: int | None = Field(None, alias="public-key-bits", description="Certificate's public key size if available.")
    public_key_type: str | None = Field(None, alias="public-key-type", description="Certificate's public key algorithm.")
    san: list[str] | None = Field(None, description="List of certificate's SubjectAlternativeName entries.")
    subject: str | None = Field(None, description='Certificate subject name.')

class GetNodesNodeCertificatesInfoResponse(RootModel[list[GetNodesNodeCertificatesInfoResponseItem]]):
    """List of items. None. Get certificate info. response."""
    root: list[GetNodesNodeCertificatesInfoResponseItem] = Field(..., description='List of certificate infos.')

class GetNodesNodeConfigResponse(ProxmoxBaseModel):
    """Model for None. Get the node configuration response."""
    acme: str | None = Field(None, description='The acme account to use on this node.')
    acmedomain0: str | None = Field(None, description='ACME domain configuration string')
    acmedomain1: str | None = Field(None, description='ACME domain configuration string')
    acmedomain2: str | None = Field(None, description='ACME domain configuration string')
    acmedomain3: str | None = Field(None, description='ACME domain configuration string')
    acmedomain4: str | None = Field(None, description='ACME domain configuration string')
    ciphers_tls_1_2: str | None = Field(None, alias="ciphers-tls-1.2", description='OpenSSL cipher list used by the proxy for TLS <= 1.2')
    ciphers_tls_1_3: str | None = Field(None, alias="ciphers-tls-1.3", description='OpenSSL ciphersuites list used by the proxy for TLS 1.3')
    consent_text: str | None = Field(None, alias="consent-text", description='Consent banner text')
    default_lang: str | None = Field(None, alias="default-lang", description='All available languages in Proxmox. Taken from proxmox-i18n repository.\npt_BR, zh_CN, and zh_TW use the same case in the translation files.')
    description: str | None = Field(None, description='Comment (multiple lines).')
    email_from: str | None = Field(None, alias="email-from", description='E-Mail Address.')
    http_proxy: str | None = Field(None, alias="http-proxy", description='HTTP proxy configuration [http://]<host>[:port]')
    task_log_max_days: int | None = Field(None, alias="task-log-max-days", description='Maximum days to keep Task logs')

class PutNodesNodeConfigRequest(ProxmoxBaseModel):
    """Model for None. Update the node configuration request."""
    acme: str | None = Field(None, description='The acme account to use on this node.')
    acmedomain0: str | None = Field(None, description='ACME domain configuration string')
    acmedomain1: str | None = Field(None, description='ACME domain configuration string')
    acmedomain2: str | None = Field(None, description='ACME domain configuration string')
    acmedomain3: str | None = Field(None, description='ACME domain configuration string')
    acmedomain4: str | None = Field(None, description='ACME domain configuration string')
    ciphers_tls_1_2: str | None = Field(None, alias="ciphers-tls-1.2", description='OpenSSL cipher list used by the proxy for TLS <= 1.2')
    ciphers_tls_1_3: str | None = Field(None, alias="ciphers-tls-1.3", description='OpenSSL ciphersuites list used by the proxy for TLS 1.3')
    consent_text: str | None = Field(None, alias="consent-text", description='Consent banner text')
    default_lang: str | None = Field(None, alias="default-lang", description='All available languages in Proxmox. Taken from proxmox-i18n repository.\npt_BR, zh_CN, and zh_TW use the same case in the translation files.')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    description: str | None = Field(None, description='Comment (multiple lines).')
    digest: str | None = Field(None, description='Digest to protect against concurrent updates')
    email_from: str | None = Field(None, alias="email-from", description='E-Mail Address.')
    http_proxy: str | None = Field(None, alias="http-proxy", description='HTTP proxy configuration [http://]<host>[:port]')
    task_log_max_days: int | None = Field(None, alias="task-log-max-days", description='Maximum days to keep Task logs')

class PutNodesNodeConfigResponse(RootModel[None]):
    """Model for None. Update the node configuration response."""
    root: None = Field(...)

class GetNodesNodeDisksResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetNodesNodeDisksDirectoryResponseItem(ProxmoxBaseModel):
    """Model for None. List systemd datastore mount units. response."""
    device: str | None = Field(None, description='The mounted device.')
    filesystem: str | None = Field(None, description='A file system type supported by our tooling.')
    name: str | None = Field(None, description='The name of the mount')
    options: str | None = Field(None, description='Mount options')
    path: str | None = Field(None, description='The mount path.')
    removable: bool | None = Field(None, description='This is removable')
    unitfile: str | None = Field(None, description='The path of the mount unit.')

class GetNodesNodeDisksDirectoryResponse(RootModel[list[GetNodesNodeDisksDirectoryResponseItem]]):
    """List of items. None. List systemd datastore mount units. response."""
    root: list[GetNodesNodeDisksDirectoryResponseItem] = Field(..., description='List of removable-datastore devices and systemd datastore mount units.')

class PostNodesNodeDisksDirectoryRequest(ProxmoxBaseModel):
    """Model for None. Create a Filesystem on an unused disk. Will be mounted under `/mnt/datastore/<name>`. request."""
    add_datastore: bool | None = Field(None, alias="add-datastore", description='Configure a datastore using the directory.')
    disk: str = Field(..., description='Block device name (/sys/block/<name>).')
    filesystem: str | None = Field(None, description='A file system type supported by our tooling.')
    name: str = Field(..., description='Datastore name.')
    removable_datastore: bool | None = Field(None, alias="removable-datastore", description='The added datastore is removable.')

class PostNodesNodeDisksDirectoryResponse(RootModel[str]):
    """Model for None. Create a Filesystem on an unused disk. Will be mounted under `/mnt/datastore/<name>`. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class DeleteNodesNodeDisksDirectoryNameRequest(RootModel[dict[str, object]]):
    """Model for None. Remove a Filesystem mounted under `/mnt/datastore/<name>`. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeDisksDirectoryNameResponse(RootModel[None]):
    """Model for None. Remove a Filesystem mounted under `/mnt/datastore/<name>`. response."""
    root: None = Field(...)

class PostNodesNodeDisksInitgptRequest(ProxmoxBaseModel):
    """Model for None. Initialize empty Disk with GPT request."""
    disk: str = Field(..., description='Block device name (/sys/block/<name>).')
    uuid: str | None = Field(None, description='UUID for the GPT table.')

class PostNodesNodeDisksInitgptResponse(RootModel[str]):
    """Model for None. Initialize empty Disk with GPT response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetNodesNodeDisksListResponseItem(ProxmoxBaseModel):
    """Model for None. List local disks response."""
    devpath: str | None = Field(None, description='Linux device path (/dev/xxx)')
    disk_type: str | None = Field(None, alias="disk-type", description='This is just a rough estimate for a "type" of disk.')
    gpt: bool | None = Field(None, description='Set if disk contains a GPT partition table')
    model: str | None = Field(None, description='Model')
    name: str | None = Field(None, description='Disk name (`/sys/block/<name>`)')
    partitions: list[dict[str, object]] | None = Field(None, description='Partitions on the device')
    rpm: int | None = Field(None, description='RPM')
    serial: str | None = Field(None, description='Serisal number')
    size: int | None = Field(None, description='Disk size')
    status: str | None = Field(None, description='SMART status')
    used: str | None = Field(None, description='What a block device (disk) is used for.')
    vendor: str | None = Field(None, description='Vendor')
    wearout: float | None = Field(None, description='Disk wearout')
    wwn: str | None = Field(None, description='WWN')

class GetNodesNodeDisksListResponse(RootModel[list[GetNodesNodeDisksListResponseItem]]):
    """List of items. None. List local disks response."""
    root: list[GetNodesNodeDisksListResponseItem] = Field(..., description='Local disk list.')

class GetNodesNodeDisksSmartResponse(ProxmoxBaseModel):
    """Model for None. Get SMART attributes and health of a disk. response."""
    attributes: list[dict[str, object]] = Field(..., description='SMART attributes.')
    status: str = Field(..., description='SMART status')
    wearout: float | None = Field(None, description='Wearout level.')

class PutNodesNodeDisksWipediskRequest(ProxmoxBaseModel):
    """Model for None. wipe disk request."""
    disk: str = Field(..., description='(Partition) block device name (/sys/class/block/<name>).')

class PutNodesNodeDisksWipediskResponse(RootModel[str]):
    """Model for None. wipe disk response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetNodesNodeDisksZfsResponseItem(ProxmoxBaseModel):
    """Model for None. List zfs pools. response."""
    alloc: int | None = Field(None, description='Used size')
    dedup: float | None = Field(None, description='ZFS deduplication ratio')
    frag: int | None = Field(None, description='ZFS fragnentation level')
    free: int | None = Field(None, description='Free space')
    health: str | None = Field(None, description='Health')
    name: str | None = Field(None, description='zpool name')
    size: int | None = Field(None, description='Total size')

class GetNodesNodeDisksZfsResponse(RootModel[list[GetNodesNodeDisksZfsResponseItem]]):
    """List of items. None. List zfs pools. response."""
    root: list[GetNodesNodeDisksZfsResponseItem] = Field(..., description='List of zpools.')

class PostNodesNodeDisksZfsRequest(ProxmoxBaseModel):
    """Model for None. Create a new ZFS pool. Will be mounted under `/mnt/datastore/<name>`. request."""
    add_datastore: bool | None = Field(None, alias="add-datastore", description='Configure a datastore using the zpool.')
    ashift: int | None = Field(None, description='Pool sector size exponent.')
    compression: str | None = Field(None, description='The ZFS compression algorithm to use.')
    devices: str = Field(..., description='A list of disk names, comma separated.')
    name: str = Field(..., description='Datastore name.')
    raidlevel: str = Field(..., description='The ZFS RAID level to use.')

class PostNodesNodeDisksZfsResponse(RootModel[str]):
    """Model for None. Create a new ZFS pool. Will be mounted under `/mnt/datastore/<name>`. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetNodesNodeDisksZfsNameResponse(RootModel[dict[str, object]]):
    """Model for None. Get zpool status details. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeDnsResponse(ProxmoxBaseModel):
    """Model for None. Read DNS settings. response."""
    digest: str = Field(..., description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    dns1: str | None = Field(None, description='First name server IP address.')
    dns2: str | None = Field(None, description='Second name server IP address.')
    dns3: str | None = Field(None, description='Third name server IP address.')
    search: str | None = Field(None, description='Search domain for host-name lookup.')

class PutNodesNodeDnsRequest(ProxmoxBaseModel):
    """Model for None. Update DNS settings. request."""
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    dns1: str | None = Field(None, description='First name server IP address.')
    dns2: str | None = Field(None, description='Second name server IP address.')
    dns3: str | None = Field(None, description='Third name server IP address.')
    search: str | None = Field(None, description='Search domain for host-name lookup.')

class PutNodesNodeDnsResponse(RootModel[None]):
    """Model for None. Update DNS settings. response."""
    root: None = Field(...)

class GetNodesNodeJournalResponse(RootModel[list[str]]):
    """Model for None. Read syslog entries. response."""
    root: list[str] = Field(..., description='Returns a list of journal entries.')

class DeleteNodesNodeNetworkRequest(RootModel[dict[str, object]]):
    """Model for None. Revert network configuration (rm /etc/network/interfaces.new). request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeNetworkResponse(RootModel[None]):
    """Model for None. Revert network configuration (rm /etc/network/interfaces.new). response."""
    root: None = Field(...)

class GetNodesNodeNetworkResponseItem(ProxmoxBaseModel):
    """Model for None. List all datastores response."""
    active: bool | None = Field(None, description='Interface is active (UP)')
    altnames: list[str] | None = Field(None, description='List of altnames for this interface')
    autostart: bool | None = Field(None, description='Autostart interface')
    bond_primary: str | None = Field(None, alias="bond-primary", description='Network interface name.')
    bond_mode: str | None = Field(None, description='Linux Bond Mode')
    bond_xmit_hash_policy: str | None = Field(None, description='Bond Transmit Hash Policy for LACP (802.3ad)')
    bridge_ports: list[str] | None = Field(None, description='Network interface list.')
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: str | None = Field(None, description='IPv4 address with netmask (CIDR notation).')
    cidr6: str | None = Field(None, description='IPv6 address with netmask (CIDR notation).')
    comments: str | None = Field(None, description='Comments (inet, may span multiple lines)')
    comments6: str | None = Field(None, description='Comments (inet6, may span multiple lines)')
    gateway: str | None = Field(None, description='IPv4 address.')
    gateway6: str | None = Field(None, description='IPv6 address.')
    method: str | None = Field(None, description='Interface configuration method')
    method6: str | None = Field(None, description='Interface configuration method')
    mtu: int | None = Field(None, description='Maximum Transmission Unit')
    name: str | None = Field(None, description='Network interface name.')
    options: list[str] | None = Field(None, description='Option list (inet)')
    options6: list[str] | None = Field(None, description='Option list (inet6)')
    slaves: list[str] | None = Field(None, description='Network interface list.')
    type: str | None = Field(None, description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='VLAN ID.')
    vlan_raw_device: str | None = Field(None, alias="vlan-raw-device", description='Network interface name.')

class GetNodesNodeNetworkResponse(RootModel[list[GetNodesNodeNetworkResponseItem]]):
    """List of items. None. List all datastores response."""
    root: list[GetNodesNodeNetworkResponseItem] = Field(..., description='List network devices (with config digest).')

class PostNodesNodeNetworkRequest(ProxmoxBaseModel):
    """Model for None. Create network interface configuration. request."""
    autostart: bool | None = Field(None, description='Autostart interface.')
    bond_primary: str | None = Field(None, alias="bond-primary", description='Network interface name.')
    bond_mode: str | None = Field(None, description='Linux Bond Mode')
    bond_xmit_hash_policy: str | None = Field(None, description='Bond Transmit Hash Policy for LACP (802.3ad)')
    bridge_ports: str | None = Field(None, description='A list of network devices, comma separated.')
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: str | None = Field(None, description='IPv4 address with netmask (CIDR notation).')
    cidr6: str | None = Field(None, description='IPv6 address with netmask (CIDR notation).')
    comments: str | None = Field(None, description='Comments (inet, may span multiple lines)')
    comments6: str | None = Field(None, description='Comments (inet5, may span multiple lines)')
    gateway: str | None = Field(None, description='IPv4 address.')
    gateway6: str | None = Field(None, description='IPv6 address.')
    iface: str = Field(..., description='Network interface name.')
    method: str | None = Field(None, description='Interface configuration method')
    method6: str | None = Field(None, description='Interface configuration method')
    mtu: int | None = Field(None, description='Maximum Transmission Unit.')
    slaves: str | None = Field(None, description='A list of network devices, comma separated.')
    type: str | None = Field(None, description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='VLAN ID.')
    vlan_raw_device: str | None = Field(None, alias="vlan-raw-device", description='Network interface name.')

class PostNodesNodeNetworkResponse(RootModel[None]):
    """Model for None. Create network interface configuration. response."""
    root: None = Field(...)

class PutNodesNodeNetworkRequest(RootModel[dict[str, object]]):
    """Model for None. Reload network configuration (requires ifupdown2). request."""
    root: dict[str, object] = Field(...)

class PutNodesNodeNetworkResponse(RootModel[None]):
    """Model for None. Reload network configuration (requires ifupdown2). response."""
    root: None = Field(...)

class DeleteNodesNodeNetworkIfaceRequest(ProxmoxBaseModel):
    """Model for None. Remove network interface configuration. request."""
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeNetworkIfaceResponse(RootModel[None]):
    """Model for None. Remove network interface configuration. response."""
    root: None = Field(...)

class GetNodesNodeNetworkIfaceResponse(ProxmoxBaseModel):
    """Model for None. Read a network interface configuration. response."""
    active: bool = Field(..., description='Interface is active (UP)')
    altnames: list[str] = Field(..., description='List of altnames for this interface')
    autostart: bool = Field(..., description='Autostart interface')
    bond_primary: str | None = Field(None, alias="bond-primary", description='Network interface name.')
    bond_mode: str | None = Field(None, description='Linux Bond Mode')
    bond_xmit_hash_policy: str | None = Field(None, description='Bond Transmit Hash Policy for LACP (802.3ad)')
    bridge_ports: list[str] | None = Field(None, description='Network interface list.')
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: str | None = Field(None, description='IPv4 address with netmask (CIDR notation).')
    cidr6: str | None = Field(None, description='IPv6 address with netmask (CIDR notation).')
    comments: str | None = Field(None, description='Comments (inet, may span multiple lines)')
    comments6: str | None = Field(None, description='Comments (inet6, may span multiple lines)')
    gateway: str | None = Field(None, description='IPv4 address.')
    gateway6: str | None = Field(None, description='IPv6 address.')
    method: str | None = Field(None, description='Interface configuration method')
    method6: str | None = Field(None, description='Interface configuration method')
    mtu: int | None = Field(None, description='Maximum Transmission Unit')
    name: str = Field(..., description='Network interface name.')
    options: list[str] = Field(..., description='Option list (inet)')
    options6: list[str] = Field(..., description='Option list (inet6)')
    slaves: list[str] | None = Field(None, description='Network interface list.')
    type: str = Field(..., description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='VLAN ID.')
    vlan_raw_device: str | None = Field(None, alias="vlan-raw-device", description='Network interface name.')

class PutNodesNodeNetworkIfaceRequest(ProxmoxBaseModel):
    """Model for None. Update network interface config. request."""
    autostart: bool | None = Field(None, description='Autostart interface.')
    bond_primary: str | None = Field(None, alias="bond-primary", description='Network interface name.')
    bond_mode: str | None = Field(None, description='Linux Bond Mode')
    bond_xmit_hash_policy: str | None = Field(None, description='Bond Transmit Hash Policy for LACP (802.3ad)')
    bridge_ports: str | None = Field(None, description='A list of network devices, comma separated.')
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: str | None = Field(None, description='IPv4 address with netmask (CIDR notation).')
    cidr6: str | None = Field(None, description='IPv6 address with netmask (CIDR notation).')
    comments: str | None = Field(None, description='Comments (inet, may span multiple lines)')
    comments6: str | None = Field(None, description='Comments (inet5, may span multiple lines)')
    delete: list[str] | None = Field(None, description='List of properties to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has different SHA256 digest. This can be used to prevent concurrent modifications.')
    gateway: str | None = Field(None, description='IPv4 address.')
    gateway6: str | None = Field(None, description='IPv6 address.')
    method: str | None = Field(None, description='Interface configuration method')
    method6: str | None = Field(None, description='Interface configuration method')
    mtu: int | None = Field(None, description='Maximum Transmission Unit.')
    slaves: str | None = Field(None, description='A list of network devices, comma separated.')
    type: str | None = Field(None, description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='VLAN ID.')
    vlan_raw_device: str | None = Field(None, alias="vlan-raw-device", description='Network interface name.')

class PutNodesNodeNetworkIfaceResponse(RootModel[None]):
    """Model for None. Update network interface config. response."""
    root: None = Field(...)

class GetNodesNodeReportResponse(RootModel[str]):
    """Model for None. Generate a report response."""
    root: str = Field(..., description='Returns report of the node')

class GetNodesNodeRrdResponse(RootModel[None]):
    """Model for None. Read node stats response."""
    root: None = Field(...)

class GetNodesNodeServicesResponseItem(ProxmoxBaseModel):
    """Model for None. Service list. response."""
    desc: str | None = Field(None, description='systemd service description.')
    name: str | None = Field(None, description='systemd service name.')
    service: str | None = Field(None, description='Service ID.')
    state: str | None = Field(None, description="systemd service 'SubState'.")
    unit_state: str | None = Field(None, alias="unit-state", description='systemd service unit state.')

class GetNodesNodeServicesResponse(RootModel[list[GetNodesNodeServicesResponseItem]]):
    """List of items. None. Service list. response."""
    root: list[GetNodesNodeServicesResponseItem] = Field(..., description='Returns a list of systemd services.')

class GetNodesNodeServicesServiceResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostNodesNodeServicesServiceReloadRequest(RootModel[dict[str, object]]):
    """Model for None. Reload service. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceReloadResponse(RootModel[None]):
    """Model for None. Reload service. response."""
    root: None = Field(...)

class PostNodesNodeServicesServiceRestartRequest(RootModel[dict[str, object]]):
    """Model for None. Restart service. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceRestartResponse(RootModel[None]):
    """Model for None. Restart service. response."""
    root: None = Field(...)

class PostNodesNodeServicesServiceStartRequest(RootModel[dict[str, object]]):
    """Model for None. Start service. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceStartResponse(RootModel[None]):
    """Model for None. Start service. response."""
    root: None = Field(...)

class GetNodesNodeServicesServiceStateResponse(RootModel[None]):
    """Model for None. Read service properties. response."""
    root: None = Field(...)

class PostNodesNodeServicesServiceStopRequest(RootModel[dict[str, object]]):
    """Model for None. Stop service. request."""
    root: dict[str, object] = Field(...)

class PostNodesNodeServicesServiceStopResponse(RootModel[None]):
    """Model for None. Stop service. response."""
    root: None = Field(...)

class GetNodesNodeStatusResponse(ProxmoxBaseModel):
    """Model for None. Read node memory, CPU and (root) disk usage response."""
    boot_info: dict[str, object] = Field(..., alias="boot-info", description='Holds the Bootmodes')
    cpu: float = Field(..., description='Total CPU usage since last query.')
    cpuinfo: dict[str, object] = Field(..., description='Information about the CPU')
    current_kernel: dict[str, object] = Field(..., alias="current-kernel", description='The current kernel version (output of `uname`)')
    info: dict[str, object] = Field(..., description='Contains general node information such as the fingerprint`')
    kversion: str = Field(..., description='The current kernel version (LEGACY string type).')
    loadavg: list[float] = Field(..., description='Load for 1, 5 and 15 minutes.')
    memory: dict[str, object] = Field(..., description='Node memory usage counters')
    root: dict[str, object] = Field(..., description='Storage space usage information.')
    swap: dict[str, object] = Field(..., description='Node swap usage counters')
    uptime: int = Field(..., description='The current uptime of the server.')
    wait: float = Field(..., description='Total IO wait since last query.')

class PostNodesNodeStatusRequest(ProxmoxBaseModel):
    """Model for None. Reboot or shutdown the node. request."""
    command: str = Field(..., description='Node Power command type.')

class PostNodesNodeStatusResponse(RootModel[None]):
    """Model for None. Reboot or shutdown the node. response."""
    root: None = Field(...)

class DeleteNodesNodeSubscriptionRequest(RootModel[dict[str, object]]):
    """Model for None. Delete subscription info. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for None. Delete subscription info. response."""
    root: None = Field(...)

class GetNodesNodeSubscriptionResponse(ProxmoxBaseModel):
    """Model for None. Read subscription info. response."""
    checktime: int | None = Field(None, description='timestamp of the last check done')
    key: str | None = Field(None, description='the subscription key, if set and permitted to access')
    message: str | None = Field(None, description='a more human readable status message')
    nextduedate: str | None = Field(None, description='next due date of the set subscription')
    productname: str | None = Field(None, description='human readable productname of the set subscription')
    regdate: str | None = Field(None, description='register date of the set subscription')
    serverid: str | None = Field(None, description='the server ID, if permitted to access')
    signature: str | None = Field(None, description='Signature for offline keys')
    status: str = Field(..., description='Subscription status')
    url: str | None = Field(None, description='URL to the web shop')

class PostNodesNodeSubscriptionRequest(ProxmoxBaseModel):
    """Model for None. Check and update subscription status. request."""
    force: bool | None = Field(None, description='Always connect to server, even if information in cache is up to date.')

class PostNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for None. Check and update subscription status. response."""
    root: None = Field(...)

class PutNodesNodeSubscriptionRequest(ProxmoxBaseModel):
    """Model for None. Set a subscription key and check it. request."""
    key: str = Field(..., description='Proxmox Backup Server subscription key.')

class PutNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for None. Set a subscription key and check it. response."""
    root: None = Field(...)

class GetNodesNodeSyslogResponseItem(ProxmoxBaseModel):
    """Model for None. Read syslog entries. response."""
    n: int | None = Field(None, description='Line number.')
    t: str | None = Field(None, description='Line text.')

class GetNodesNodeSyslogResponse(RootModel[list[GetNodesNodeSyslogResponseItem]]):
    """List of items. None. Read syslog entries. response."""
    root: list[GetNodesNodeSyslogResponseItem] = Field(..., description='Returns a list of syslog entries.')

class GetNodesNodeTasksResponseItem(ProxmoxBaseModel):
    """Model for None. List tasks. response."""
    endtime: int | None = Field(None, description='The task end time (Epoch)')
    node: str | None = Field(None, description='The node name where the task is running on.')
    pid: int | None = Field(None, description='The Unix PID')
    pstart: int | None = Field(None, description='The task start time (Epoch)')
    starttime: int | None = Field(None, description='The task start time (Epoch)')
    status: str | None = Field(None, description='Task end status')
    upid: str | None = Field(None, description='Unique Process/Task Identifier')
    user: str | None = Field(None, description='The authenticated entity who started the task')
    worker_id: str | None = Field(None, description='Worker ID (arbitrary ASCII string)')
    worker_type: str | None = Field(None, description='Worker type (arbitrary ASCII string)')

class GetNodesNodeTasksResponse(RootModel[list[GetNodesNodeTasksResponseItem]]):
    """List of items. None. List tasks. response."""
    root: list[GetNodesNodeTasksResponseItem] = Field(..., description='A list of tasks.')

class DeleteNodesNodeTasksUpidRequest(RootModel[dict[str, object]]):
    """Model for None. Try to stop a task. request."""
    root: dict[str, object] = Field(...)

class DeleteNodesNodeTasksUpidResponse(RootModel[None]):
    """Model for None. Try to stop a task. response."""
    root: None = Field(...)

class GetNodesNodeTasksUpidResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetNodesNodeTasksUpidLogResponse(RootModel[None]):
    """Model for None. Read the task log response."""
    root: None = Field(...)

class GetNodesNodeTasksUpidStatusResponse(ProxmoxBaseModel):
    """Model for None. Get task status. response."""
    exitstatus: str | None = Field(None, description="'OK', 'Error: <msg>', or 'unknown'.")
    id: str | None = Field(None, description='Worker ID (arbitrary ASCII string)')
    node: str = Field(..., description="Node name (or 'localhost')")
    pid: int = Field(..., description='The Unix PID.')
    pstart: int = Field(..., description='The Unix process start time from `/proc/pid/stat`')
    starttime: int = Field(..., description='The task start time (Epoch)')
    status: str = Field(..., description="'running' or 'stopped'")
    tokenid: str | None = Field(None, description='The token ID part of an API token authentication id.\n\nThis alone does NOT uniquely identify the API token - use a full `Authid` for such use cases.')
    type: str = Field(..., description='Worker type (arbitrary ASCII string)')
    upid: str = Field(..., description='Unique Process/Task Identifier')
    user: str = Field(..., description='User ID')

class PostNodesNodeTermproxyRequest(ProxmoxBaseModel):
    """Model for None. Call termproxy and return shell ticket request."""
    cmd: str | None = Field(None, description='The command to run.')

class PostNodesNodeTermproxyResponse(ProxmoxBaseModel):
    """Model for None. Call termproxy and return shell ticket response."""
    port: int = Field(..., description='port used to bind termproxy to')
    ticket: str = Field(..., description='ticket used to verifiy websocket connection')
    upid: str = Field(..., description='UPID for termproxy worker task')
    user: str = Field(..., description='user or authid encoded in the ticket')

class GetNodesNodeTimeResponse(ProxmoxBaseModel):
    """Model for None. Read server time and time zone settings. response."""
    localtime: int = Field(..., description='Seconds since 1970-01-01 00:00:00 UTC. (local time)')
    time: int = Field(..., description='Seconds since 1970-01-01 00:00:00 UTC.')
    timezone: str = Field(..., description="Time zone. The file '/usr/share/zoneinfo/zone.tab' contains the list of valid names.")

class PutNodesNodeTimeRequest(ProxmoxBaseModel):
    """Model for None. Set time zone request."""
    timezone: str = Field(..., description="Time zone. The file '/usr/share/zoneinfo/zone.tab' contains the list of valid names.")

class PutNodesNodeTimeResponse(RootModel[None]):
    """Model for None. Set time zone response."""
    root: None = Field(...)

class GetNodesNodeVncwebsocketResponse(RootModel[None]):
    """Model for None. Upgraded to websocket response."""
    root: None = Field(...)

class GetPingResponse(ProxmoxBaseModel):
    """Model for None. Dummy method which replies with `{ "pong": True }` response."""
    pong: bool = Field(..., description='Always true')

class PostPullRequest(ProxmoxBaseModel):
    """Model for None. Sync store from other repository request."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    encrypted_only: bool | None = Field(None, alias="encrypted-only", description='Only synchronize encrypted backup snapshots, exclude others.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    remote: str | None = Field(None, description='Remote ID.')
    remote_ns: str | None = Field(None, alias="remote-ns", description='Namespace.')
    remote_store: str = Field(..., alias="remote-store", description='Datastore name.')
    remove_vanished: bool | None = Field(None, alias="remove-vanished", description='Delete vanished backups. This remove the local copy if the remote backup was deleted.')
    resync_corrupt: bool | None = Field(None, alias="resync-corrupt", description='If the verification failed for a local snapshot, try to pull it again.')
    store: str = Field(..., description='Datastore name.')
    transfer_last: int | None = Field(None, alias="transfer-last", description='Limit transfer to last N snapshots (per group), skipping others')
    verified_only: bool | None = Field(None, alias="verified-only", description='Only synchronize verified backup snapshots, exclude others.')

class PostPullResponse(RootModel[None]):
    """Model for None. Sync store from other repository response."""
    root: None = Field(...)

class PostPushRequest(ProxmoxBaseModel):
    """Model for None. Push store to other repository request."""
    burst_in: str | None = Field(None, alias="burst-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    burst_out: str | None = Field(None, alias="burst-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    encrypted_only: bool | None = Field(None, alias="encrypted-only", description='Only synchronize encrypted backup snapshots, exclude others.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion, empty == automatic full recursion, namespace depths reduce maximum allowed value)')
    ns: str | None = Field(None, description='Namespace.')
    rate_in: str | None = Field(None, alias="rate-in", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    rate_out: str | None = Field(None, alias="rate-out", description='Byte size with optional unit (B, KB (base 10), MB, GB, ..., KiB (base 2), MiB, Gib, ...).')
    remote: str = Field(..., description='Remote ID.')
    remote_ns: str | None = Field(None, alias="remote-ns", description='Namespace.')
    remote_store: str = Field(..., alias="remote-store", description='Datastore name.')
    remove_vanished: bool | None = Field(None, alias="remove-vanished", description='Delete vanished backups. This remove the local copy if the remote backup was deleted.')
    store: str = Field(..., description='Datastore name.')
    transfer_last: int | None = Field(None, alias="transfer-last", description='Limit transfer to last N snapshots (per group), skipping others')
    verified_only: bool | None = Field(None, alias="verified-only", description='Only synchronize verified backup snapshots, exclude others.')

class PostPushResponse(RootModel[None]):
    """Model for None. Push store to other repository response."""
    root: None = Field(...)

class GetReaderResponse(RootModel[None]):
    """Model for None. Upgraded to backup protocol ('proxmox-backup-reader-protocol-v1'). response."""
    root: None = Field(...)

class GetReaderUpgradeResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetReaderUpgradeChunkResponse(RootModel[None]):
    """Model for None. Download specified chunk. response."""
    root: None = Field(...)

class GetReaderUpgradeDownloadResponse(RootModel[None]):
    """Model for None. Download specified file. response."""
    root: None = Field(...)

class GetReaderUpgradeSpeedtestResponse(RootModel[None]):
    """Model for None. Test 1M block download speed. response."""
    root: None = Field(...)

class GetStatusResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetStatusDatastoreUsageResponseItem(ProxmoxBaseModel):
    """Model for None. List Datastore usages and estimates response."""
    avail: int | None = Field(None, description='The available bytes of the underlying storage. (-1 on error)')
    backend_type: str | None = Field(None, alias="backend-type", description='Datastore backend type')
    error: str | None = Field(None, description='An error description, for example, when the datastore could not be looked up')
    estimated_full_date: int | None = Field(None, alias="estimated-full-date", description="Estimation of the UNIX epoch when the storage will be full.\nIt's calculated via a simple Linear Regression (Least Squares) over the RRD data of the\nlast Month. Missing if not enough data points are available yet. An estimate in the past\nmeans that usage is declining or not changing.")
    gc_status: dict[str, object] | None = Field(None, alias="gc-status", description='Garbage collection status.')
    history: list[float] | None = Field(None, description='A list of usages of the past (last Month).')
    history_delta: int | None = Field(None, alias="history-delta", description='History resolution (seconds)')
    history_start: int | None = Field(None, alias="history-start", description='History start time (epoch)')
    mount_status: str | None = Field(None, alias="mount-status", description='Current mounting status of a datastore, useful for removable datastores.')
    store: str | None = Field(None, description='Datastore name.')
    total: int | None = Field(None, description='The Size of the underlying storage in bytes.')
    used: int | None = Field(None, description='The used bytes of the underlying storage.')

class GetStatusDatastoreUsageResponse(RootModel[list[GetStatusDatastoreUsageResponseItem]]):
    """List of items. None. List Datastore usages and estimates response."""
    root: list[GetStatusDatastoreUsageResponseItem] = Field(..., description='Lists the Status of the Datastores.')

class GetStatusMetricsResponse(RootModel[None]):
    """Model for None. Return backup server metrics. response."""
    root: None = Field(...)

class GetTapeResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetTapeBackupResponseItem(ProxmoxBaseModel):
    """Model for None. List all tape backup jobs response."""
    comment: str | None = Field(None, description='Comment.')
    drive: str | None = Field(None, description='Drive Identifier.')
    eject_media: bool | None = Field(None, alias="eject-media", description='Eject media upon job completion.')
    export_media_set: bool | None = Field(None, alias="export-media-set", description='Export media set upon job completion.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    id: str | None = Field(None, description='Job ID.')
    last_run_endtime: int | None = Field(None, alias="last-run-endtime", description='Endtime of the last run.')
    last_run_state: str | None = Field(None, alias="last-run-state", description='Result of the last run.')
    last_run_upid: str | None = Field(None, alias="last-run-upid", description='Task UPID of the last run.')
    latest_only: bool | None = Field(None, alias="latest-only", description='Backup latest snapshots only.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    next_media_label: str | None = Field(None, alias="next-media-label", description='Next tape used (best guess)')
    next_run: int | None = Field(None, alias="next-run", description='Estimated time of the next run (UNIX epoch).')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    ns: str | None = Field(None, description='Namespace.')
    pool: str | None = Field(None, description='Media pool name.')
    schedule: str | None = Field(None, description='Run sync job at specified schedule.')
    store: str | None = Field(None, description='Datastore name.')
    worker_threads: int | None = Field(None, alias="worker-threads", description='The number of threads to use for the tape backup job.')

class GetTapeBackupResponse(RootModel[list[GetTapeBackupResponseItem]]):
    """List of items. None. List all tape backup jobs response."""
    root: list[GetTapeBackupResponseItem] = Field(..., description='List configured thape backup jobs and their status')

class PostTapeBackupRequest(ProxmoxBaseModel):
    """Model for None. Backup datastore to tape media pool request."""
    drive: str = Field(..., description='Drive Identifier.')
    eject_media: bool | None = Field(None, alias="eject-media", description='Eject media upon job completion.')
    export_media_set: bool | None = Field(None, alias="export-media-set", description='Export media set upon job completion.')
    force_media_set: bool | None = Field(None, alias="force-media-set", description='Ignore the allocation policy and start a new media-set.')
    group_filter: list[str] | None = Field(None, alias="group-filter", description='List of group filters.')
    latest_only: bool | None = Field(None, alias="latest-only", description='Backup latest snapshots only.')
    max_depth: int | None = Field(None, alias="max-depth", description='How many levels of namespaces should be operated on (0 == no recursion)')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    ns: str | None = Field(None, description='Namespace.')
    pool: str = Field(..., description='Media pool name.')
    store: str = Field(..., description='Datastore name.')
    worker_threads: int | None = Field(None, alias="worker-threads", description='The number of threads to use for the tape backup job.')

class PostTapeBackupResponse(RootModel[str]):
    """Model for None. Backup datastore to tape media pool response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class PostTapeBackupIdRequest(RootModel[dict[str, object]]):
    """Model for None. Runs a tape backup job manually. request."""
    root: dict[str, object] = Field(...)

class PostTapeBackupIdResponse(RootModel[None]):
    """Model for None. Runs a tape backup job manually. response."""
    root: None = Field(...)

class GetTapeChangerResponseItem(ProxmoxBaseModel):
    """Model for None. List changers response."""
    eject_before_unload: bool | None = Field(None, alias="eject-before-unload", description='if set to true, tapes are ejected manually before unloading')
    export_slots: str | None = Field(None, alias="export-slots", description="A list of slot numbers, comma separated. Those slots are reserved for\nImport/Export, i.e. any media in those slots are considered to be\n'offline'.\n")
    model: str | None = Field(None, description='Model (autodetected)')
    name: str | None = Field(None, description='Tape Changer Identifier.')
    path: str | None = Field(None, description="Path to Linux generic SCSI device (e.g. '/dev/sg4')")
    serial: str | None = Field(None, description='Serial number (autodetected)')
    vendor: str | None = Field(None, description='Vendor (autodetected)')

class GetTapeChangerResponse(RootModel[list[GetTapeChangerResponseItem]]):
    """List of items. None. List changers response."""
    root: list[GetTapeChangerResponseItem] = Field(..., description='The list of configured changers with model information.')

class GetTapeChangerNameResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetTapeChangerNameStatusResponseItem(ProxmoxBaseModel):
    """Model for None. Get tape changer status response."""
    entry_id: int | None = Field(None, alias="entry-id", description='The ID of the slot or drive')
    entry_kind: str | None = Field(None, alias="entry-kind", description='Mtx Entry Kind')
    label_text: str | None = Field(None, alias="label-text", description='Media Label/Barcode.')
    loaded_slot: int | None = Field(None, alias="loaded-slot", description='The slot the drive was loaded from')
    state: str | None = Field(None, description='The current state of the drive')

class GetTapeChangerNameStatusResponse(RootModel[list[GetTapeChangerNameStatusResponseItem]]):
    """List of items. None. Get tape changer status response."""
    root: list[GetTapeChangerNameStatusResponseItem] = Field(..., description='A status entry for each drive and slot.')

class PostTapeChangerNameTransferRequest(ProxmoxBaseModel):
    """Model for None. Transfers media from one slot to another request."""
    from_: int = Field(..., alias="from", description='Source slot number')
    to: int = Field(..., description='Destination slot number')

class PostTapeChangerNameTransferResponse(RootModel[None]):
    """Model for None. Transfers media from one slot to another response."""
    root: None = Field(...)

class GetTapeDriveResponseItem(ProxmoxBaseModel):
    """Model for None. List drives response."""
    activity: str | None = Field(None, description='The DT Device Activity from DT Device Status LP page')
    changer: str | None = Field(None, description='Tape Changer Identifier.')
    changer_drivenum: int | None = Field(None, alias="changer-drivenum", description='Associated changer drive number (requires option changer)')
    model: str | None = Field(None, description='Model (autodetected)')
    name: str | None = Field(None, description='Drive Identifier.')
    path: str | None = Field(None, description="The path to a LTO SCSI-generic tape device (i.e. '/dev/sg0')")
    serial: str | None = Field(None, description='Serial number (autodetected)')
    state: str | None = Field(None, description='the state of the drive if locked')
    vendor: str | None = Field(None, description='Vendor (autodetected)')

class GetTapeDriveResponse(RootModel[list[GetTapeDriveResponseItem]]):
    """List of items. None. List drives response."""
    root: list[GetTapeDriveResponseItem] = Field(..., description='The list of configured drives with model information.')

class GetTapeDriveDriveResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class PostTapeDriveDriveBarcodeLabelMediaRequest(ProxmoxBaseModel):
    """Model for None. Label media with barcodes from changer device request."""
    pool: str | None = Field(None, description='Media pool name.')

class PostTapeDriveDriveBarcodeLabelMediaResponse(RootModel[str]):
    """Model for None. Label media with barcodes from changer device response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetTapeDriveDriveCartridgeMemoryResponseItem(ProxmoxBaseModel):
    """Model for None. Read Cartridge Memory (Medium auxiliary memory attributes) response."""
    id: int | None = Field(None, description='Attribute id')
    name: str | None = Field(None, description='Attribute name')
    value: str | None = Field(None, description='Attribute value')

class GetTapeDriveDriveCartridgeMemoryResponse(RootModel[list[GetTapeDriveDriveCartridgeMemoryResponseItem]]):
    """List of items. None. Read Cartridge Memory (Medium auxiliary memory attributes) response."""
    root: list[GetTapeDriveDriveCartridgeMemoryResponseItem] = Field(..., description='A List of medium auxiliary memory attributes.')

class PostTapeDriveDriveCatalogRequest(ProxmoxBaseModel):
    """Model for None. Scan media and record content request."""
    force: bool | None = Field(None, description='Force overriding existing index.')
    scan: bool | None = Field(None, description='Re-read the whole tape to reconstruct the catalog instead of restoring saved versions.')
    verbose: bool | None = Field(None, description='Verbose mode - log all found chunks.')

class PostTapeDriveDriveCatalogResponse(RootModel[str]):
    """Model for None. Scan media and record content response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class PutTapeDriveDriveCleanRequest(RootModel[dict[str, object]]):
    """Model for None. Clean drive request."""
    root: dict[str, object] = Field(...)

class PutTapeDriveDriveCleanResponse(RootModel[str]):
    """Model for None. Clean drive response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class PostTapeDriveDriveEjectMediaRequest(RootModel[dict[str, object]]):
    """Model for None. Eject/Unload drive media request."""
    root: dict[str, object] = Field(...)

class PostTapeDriveDriveEjectMediaResponse(RootModel[str]):
    """Model for None. Eject/Unload drive media response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class PutTapeDriveDriveExportMediaRequest(ProxmoxBaseModel):
    """Model for None. Export media with specified label request."""
    label_text: str = Field(..., alias="label-text", description='Media Label/Barcode.')

class PutTapeDriveDriveExportMediaResponse(RootModel[int]):
    """Model for None. Export media with specified label response."""
    root: int = Field(..., description='The import-export slot number the media was transferred to.')

class PostTapeDriveDriveFormatMediaRequest(ProxmoxBaseModel):
    """Model for None. Format media. Check for label-text if given (cancels if wrong media). request."""
    fast: bool | None = Field(None, description='Use fast erase.')
    label_text: str | None = Field(None, alias="label-text", description='Media Label/Barcode.')

class PostTapeDriveDriveFormatMediaResponse(RootModel[str]):
    """Model for None. Format media. Check for label-text if given (cancels if wrong media). response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetTapeDriveDriveInventoryResponseItem(ProxmoxBaseModel):
    """Model for None. List known media labels (Changer Inventory)

Note: Only useful for drives with associated changer device.

This method queries the changer to get a list of media labels.

Note: This updates the media online status. response."""
    label_text: str | None = Field(None, alias="label-text", description='Changer label text (or Barcode)')
    uuid: str | None = Field(None, description='Media Uuid.')

class GetTapeDriveDriveInventoryResponse(RootModel[list[GetTapeDriveDriveInventoryResponseItem]]):
    """List of items. None. List known media labels (Changer Inventory)

Note: Only useful for drives with associated changer device.

This method queries the changer to get a list of media labels.

Note: This updates the media online status. response."""
    root: list[GetTapeDriveDriveInventoryResponseItem] = Field(..., description='The list of media labels with associated media Uuid (if any).')

class PutTapeDriveDriveInventoryRequest(ProxmoxBaseModel):
    """Model for None. Update inventory

Note: Only useful for drives with associated changer device.

This method queries the changer to get a list of media labels. It
then loads any unknown media into the drive, reads the label, and
store the result to the media database.

If `catalog` is true, also tries to restore the catalog from tape.

Note: This updates the media online status. request."""
    catalog: bool | None = Field(None, description='Restore the catalog from tape.')
    read_all_labels: bool | None = Field(None, alias="read-all-labels", description='Load all tapes and try read labels (even if already inventoried)')

class PutTapeDriveDriveInventoryResponse(RootModel[str]):
    """Model for None. Update inventory

Note: Only useful for drives with associated changer device.

This method queries the changer to get a list of media labels. It
then loads any unknown media into the drive, reads the label, and
store the result to the media database.

If `catalog` is true, also tries to restore the catalog from tape.

Note: This updates the media online status. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class PostTapeDriveDriveLabelMediaRequest(ProxmoxBaseModel):
    """Model for None. Label media

Write a new media label to the media in 'drive'. The media is
assigned to the specified 'pool', or else to the free media pool.

Note: The media need to be empty (you may want to format it first). request."""
    label_text: str = Field(..., alias="label-text", description='Media Label/Barcode.')
    pool: str | None = Field(None, description='Media pool name.')

class PostTapeDriveDriveLabelMediaResponse(RootModel[str]):
    """Model for None. Label media

Write a new media label to the media in 'drive'. The media is
assigned to the specified 'pool', or else to the free media pool.

Note: The media need to be empty (you may want to format it first). response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class PostTapeDriveDriveLoadMediaRequest(ProxmoxBaseModel):
    """Model for None. Load media with specified label

Issue a media load request to the associated changer device. request."""
    label_text: str = Field(..., alias="label-text", description='Media Label/Barcode.')

class PostTapeDriveDriveLoadMediaResponse(RootModel[str]):
    """Model for None. Load media with specified label

Issue a media load request to the associated changer device. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class PostTapeDriveDriveLoadSlotRequest(ProxmoxBaseModel):
    """Model for None. Load media from the specified slot

Issue a media load request to the associated changer device. request."""
    source_slot: int = Field(..., alias="source-slot", description='Source slot number.')

class PostTapeDriveDriveLoadSlotResponse(RootModel[None]):
    """Model for None. Load media from the specified slot

Issue a media load request to the associated changer device. response."""
    root: None = Field(...)

class GetTapeDriveDriveReadLabelResponse(ProxmoxBaseModel):
    """Model for None. Read media label (optionally inventorize media) response."""
    ctime: int = Field(..., description='Creation time stamp')
    encryption_key_fingerprint: str | None = Field(None, alias="encryption-key-fingerprint", description='Encryption key fingerprint')
    label_text: str = Field(..., alias="label-text", description='Media label text (or Barcode)')
    media_set_ctime: int | None = Field(None, alias="media-set-ctime", description='MediaSet Creation time stamp')
    media_set_uuid: str | None = Field(None, alias="media-set-uuid", description='MediaSet Uuid (We use the all-zero Uuid to reserve an empty media for a specific pool).')
    pool: str | None = Field(None, description='MediaSet Pool')
    seq_nr: int | None = Field(None, alias="seq-nr", description='MediaSet media sequence number')
    uuid: str = Field(..., description='Media Uuid.')

class PostTapeDriveDriveRestoreKeyRequest(ProxmoxBaseModel):
    """Model for None. Try to restore a tape encryption key request."""
    password: str = Field(..., description='The password the key was encrypted with.')

class PostTapeDriveDriveRestoreKeyResponse(RootModel[None]):
    """Model for None. Try to restore a tape encryption key response."""
    root: None = Field(...)

class PostTapeDriveDriveRewindRequest(RootModel[dict[str, object]]):
    """Model for None. Rewind tape request."""
    root: dict[str, object] = Field(...)

class PostTapeDriveDriveRewindResponse(RootModel[str]):
    """Model for None. Rewind tape response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetTapeDriveDriveStatusResponse(ProxmoxBaseModel):
    """Model for None. Get drive/media status response."""
    alert_flags: str | None = Field(None, alias="alert-flags", description='Tape Alert Flags')
    block_number: int | None = Field(None, alias="block-number", description='Current block number')
    blocksize: int = Field(..., description='Block size (0 is variable size)')
    buffer_mode: int = Field(..., alias="buffer-mode", description='Drive buffer mode')
    bytes_read: int | None = Field(None, alias="bytes-read", description='Total Bytes Read in Medium Life')
    bytes_written: int | None = Field(None, alias="bytes-written", description='Total Bytes Written in Medium Life')
    compression: bool = Field(..., description='Compression enabled')
    density: str | None = Field(None, description='The density of a tape medium, derived from the LTO version.')
    drive_activity: str | None = Field(None, alias="drive-activity", description='The DT Device Activity from DT Device Status LP page')
    file_number: int | None = Field(None, alias="file-number", description='Current file number')
    manufactured: int | None = Field(None, description='Medium Manufacture Date (epoch)')
    medium_passes: int | None = Field(None, alias="medium-passes", description='Count of the total number of times the medium has passed over\nthe head.')
    medium_wearout: float | None = Field(None, alias="medium-wearout", description='Estimated tape wearout factor (assuming max. 16000 end-to-end passes)')
    product: str = Field(..., description='Product')
    revision: str = Field(..., description='Revision')
    vendor: str = Field(..., description='Vendor')
    volume_mounts: int | None = Field(None, alias="volume-mounts", description='Number of mounts for the current volume (i.e., Thread Count)')
    write_protect: bool | None = Field(None, alias="write-protect", description='Media is write protected')

class PostTapeDriveDriveUnloadRequest(ProxmoxBaseModel):
    """Model for None. Unload media via changer request."""
    target_slot: int | None = Field(None, alias="target-slot", description='Target slot number. If omitted, defaults to the slot that the drive was loaded from.')

class PostTapeDriveDriveUnloadResponse(RootModel[str]):
    """Model for None. Unload media via changer response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetTapeDriveDriveVolumeStatisticsResponse(ProxmoxBaseModel):
    """Model for None. Read Volume Statistics (SCSI log page 17h) response."""
    beginning_of_medium_passes: int = Field(..., alias="beginning-of-medium-passes", description='Beginning of medium passes')
    last_load_read_compression_ratio: int = Field(..., alias="last-load-read-compression-ratio", description='Last load read compression ratio')
    last_load_write_compression_ratio: int = Field(..., alias="last-load-write-compression-ratio", description='Last load write compression ratio')
    last_mount_bytes_read: int = Field(..., alias="last-mount-bytes-read", description='Last mount bytes read')
    last_mount_bytes_written: int = Field(..., alias="last-mount-bytes-written", description='Last mount bytes written')
    last_mount_unrecovered_read_errors: int = Field(..., alias="last-mount-unrecovered-read-errors", description='Last mount unrecovered read errors')
    last_mount_unrecovered_write_errors: int = Field(..., alias="last-mount-unrecovered-write-errors", description='Last mount unrecovered write errors')
    lifetime_bytes_read: int = Field(..., alias="lifetime-bytes-read", description='Lifetime bytes read')
    lifetime_bytes_written: int = Field(..., alias="lifetime-bytes-written", description='Lifetime bytes written')
    medium_mount_time: int = Field(..., alias="medium-mount-time", description='Medium mount time')
    medium_ready_time: int = Field(..., alias="medium-ready-time", description='Medium ready time')
    middle_of_tape_passes: int = Field(..., alias="middle-of-tape-passes", description='Middle of medium passes')
    serial: str = Field(..., description='Volume serial number')
    total_native_capacity: int = Field(..., alias="total-native-capacity", description='Total native capacity')
    total_used_native_capacity: int = Field(..., alias="total-used-native-capacity", description='Total used native capacity')
    volume_datasets_read: int = Field(..., alias="volume-datasets-read", description='Total datasets read')
    volume_datasets_written: int = Field(..., alias="volume-datasets-written", description='Total data sets written')
    volume_mounts: int = Field(..., alias="volume-mounts", description='Volume mounts (thread count)')
    volume_recovered_read_errors: int = Field(..., alias="volume-recovered-read-errors", description='Total read retries')
    volume_recovered_write_data_errors: int = Field(..., alias="volume-recovered-write-data-errors", description='Write retries')
    volume_unrecovered_read_errors: int = Field(..., alias="volume-unrecovered-read-errors", description='Total unrecovered read errors')
    volume_unrecovered_write_data_errors: int = Field(..., alias="volume-unrecovered-write-data-errors", description='Total unrecovered write errors')
    volume_unrecovered_write_servo_errors: int = Field(..., alias="volume-unrecovered-write-servo-errors", description='Total fatal suspended writes')
    volume_write_servo_errors: int = Field(..., alias="volume-write-servo-errors", description='Total suspended writes')
    worm: bool = Field(..., description='Volume is WORM')
    write_protect: bool = Field(..., alias="write-protect", description='Write protect')

class GetTapeMediaResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetTapeMediaContentResponseItem(ProxmoxBaseModel):
    """Model for None. List media content response."""
    backup_time: int | None = Field(None, alias="backup-time", description='Snapshot creation time (epoch)')
    label_text: str | None = Field(None, alias="label-text", description='Media label text (or Barcode)')
    media_set_ctime: int | None = Field(None, alias="media-set-ctime", description='MediaSet Creation time stamp')
    media_set_name: str | None = Field(None, alias="media-set-name", description='Media set name')
    media_set_uuid: str | None = Field(None, alias="media-set-uuid", description='MediaSet Uuid (We use the all-zero Uuid to reserve an empty media for a specific pool).')
    pool: str | None = Field(None, description='Media Pool')
    seq_nr: int | None = Field(None, alias="seq-nr", description='Media set seq_nr')
    snapshot: str | None = Field(None, description='Backup snapshot')
    store: str | None = Field(None, description='Datastore Name')
    uuid: str | None = Field(None, description='Media Uuid.')

class GetTapeMediaContentResponse(RootModel[list[GetTapeMediaContentResponseItem]]):
    """List of items. None. List media content response."""
    root: list[GetTapeMediaContentResponseItem] = Field(..., description='Media content list.')

class GetTapeMediaDestroyResponse(RootModel[None]):
    """Model for None. Destroy media (completely remove from database) response."""
    root: None = Field(...)

class GetTapeMediaListResponseItem(ProxmoxBaseModel):
    """Model for None. List pool media response."""
    bytes_used: int | None = Field(None, alias="bytes-used", description='Bytes currently used')
    catalog: bool | None = Field(None, description='Catalog status OK')
    ctime: int | None = Field(None, description='Creation time stamp')
    expired: bool | None = Field(None, description='Expired flag')
    label_text: str | None = Field(None, alias="label-text", description='Media label text (or Barcode)')
    location: str | None = Field(None, description="Media location (e.g. 'offline', 'online-<changer_name>', 'vault-<vault_name>')")
    media_set_ctime: int | None = Field(None, alias="media-set-ctime", description='MediaSet creation time stamp')
    media_set_name: str | None = Field(None, alias="media-set-name", description='Media set name')
    media_set_uuid: str | None = Field(None, alias="media-set-uuid", description='MediaSet Uuid (We use the all-zero Uuid to reserve an empty media for a specific pool).')
    pool: str | None = Field(None, description='Media Pool')
    seq_nr: int | None = Field(None, alias="seq-nr", description='Media set seq_nr')
    status: str | None = Field(None, description='Media status\nMedia Status')
    uuid: str | None = Field(None, description='Media Uuid.')

class GetTapeMediaListResponse(RootModel[list[GetTapeMediaListResponseItem]]):
    """List of items. None. List pool media response."""
    root: list[GetTapeMediaListResponseItem] = Field(..., description='List of registered backup media.')

class GetTapeMediaListUuidResponse(RootModel[None]):
    """Model for None. Directory index. response."""
    root: None = Field(...)

class GetTapeMediaListUuidStatusResponse(RootModel[None]):
    """Model for None. Get current media status response."""
    root: None = Field(...)

class PostTapeMediaListUuidStatusRequest(ProxmoxBaseModel):
    """Model for None. Update media status (None, 'full', 'damaged' or 'retired')

It is not allowed to set status to 'writable' or 'unknown' (those
are internally managed states). request."""
    status: str | None = Field(None, description='Media status\nMedia Status')

class PostTapeMediaListUuidStatusResponse(RootModel[None]):
    """Model for None. Update media status (None, 'full', 'damaged' or 'retired')

It is not allowed to set status to 'writable' or 'unknown' (those
are internally managed states). response."""
    root: None = Field(...)

class GetTapeMediaMediaSetsResponseItem(ProxmoxBaseModel):
    """Model for None. List Media sets response."""
    media_set_ctime: int | None = Field(None, alias="media-set-ctime", description='MediaSet creation time stamp')
    media_set_name: str | None = Field(None, alias="media-set-name", description='Media set name')
    media_set_uuid: str | None = Field(None, alias="media-set-uuid", description='MediaSet Uuid (We use the all-zero Uuid to reserve an empty media for a specific pool).')
    pool: str | None = Field(None, description='Media Pool')

class GetTapeMediaMediaSetsResponse(RootModel[list[GetTapeMediaMediaSetsResponseItem]]):
    """List of items. None. List Media sets response."""
    root: list[GetTapeMediaMediaSetsResponseItem] = Field(..., description='List of media sets.')

class PostTapeMediaMoveRequest(ProxmoxBaseModel):
    """Model for None. Change Tape location to vault (if given), or offline. request."""
    label_text: str | None = Field(None, alias="label-text", description='Media Label/Barcode.')
    uuid: str | None = Field(None, description='Media Uuid.')
    vault_name: str | None = Field(None, alias="vault-name", description='Vault name.')

class PostTapeMediaMoveResponse(RootModel[None]):
    """Model for None. Change Tape location to vault (if given), or offline. response."""
    root: None = Field(...)

class PostTapeRestoreRequest(ProxmoxBaseModel):
    """Model for None. Restore data from media-set. Namespaces will be automatically created if necessary. request."""
    drive: str = Field(..., description='Drive Identifier.')
    media_set: str = Field(..., alias="media-set", description='Media set UUID.')
    namespaces: list[str] | None = Field(None, description='List of namespace to restore.')
    notification_mode: str | None = Field(None, alias="notification-mode", description="Configure how notifications for this datastore should be sent.\n`legacy-sendmail` sends email notifications to the user configured\nin `notify-user` via the system's `sendmail` executable.\n`notification-system` emits matchable notification events to the\nnotification system.")
    notify_user: str | None = Field(None, alias="notify-user", description='User ID')
    owner: str | None = Field(None, description='Authentication ID')
    snapshots: list[str] | None = Field(None, description='List of snapshots.')
    store: str = Field(..., description="A list of Datastore mappings (or single datastore), comma separated. For example 'a=b,e' maps the source datastore 'a' to target 'b and all other sources to the default 'e'. If no default is given, only the specified sources are mapped.")

class PostTapeRestoreResponse(RootModel[str]):
    """Model for None. Restore data from media-set. Namespaces will be automatically created if necessary. response."""
    root: str = Field(..., description='Unique Process/Task Identifier')

class GetTapeScanChangersResponseItem(ProxmoxBaseModel):
    """Model for None. Scan for SCSI tape changers response."""
    kind: str | None = Field(None, description='Kind of device')
    major: int | None = Field(None, description='Device major number')
    minor: int | None = Field(None, description='Device minor number')
    model: str | None = Field(None, description='Model (autodetected)')
    path: str | None = Field(None, description='Path to the linux device node')
    serial: str | None = Field(None, description='Serial number (autodetected)')
    vendor: str | None = Field(None, description='Vendor (autodetected)')

class GetTapeScanChangersResponse(RootModel[list[GetTapeScanChangersResponseItem]]):
    """List of items. None. Scan for SCSI tape changers response."""
    root: list[GetTapeScanChangersResponseItem] = Field(..., description='The list of autodetected tape changers.')

class GetTapeScanDrivesResponseItem(ProxmoxBaseModel):
    """Model for None. Scan tape drives response."""
    kind: str | None = Field(None, description='Kind of device')
    major: int | None = Field(None, description='Device major number')
    minor: int | None = Field(None, description='Device minor number')
    model: str | None = Field(None, description='Model (autodetected)')
    path: str | None = Field(None, description='Path to the linux device node')
    serial: str | None = Field(None, description='Serial number (autodetected)')
    vendor: str | None = Field(None, description='Vendor (autodetected)')

class GetTapeScanDrivesResponse(RootModel[list[GetTapeScanDrivesResponseItem]]):
    """List of items. None. Scan tape drives response."""
    root: list[GetTapeScanDrivesResponseItem] = Field(..., description='The list of autodetected tape drives.')

class GetVersionResponse(ProxmoxBaseModel):
    """Model for None. Proxmox Backup Server API version. response."""
    release: str = Field(..., description='Version release')
    repoid: str = Field(..., description='Version repository id')
    version: str = Field(..., description="Version 'major.minor'")
