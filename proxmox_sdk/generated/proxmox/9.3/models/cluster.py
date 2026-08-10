"""Generated Pydantic v2 schemas for Proxmox route group 'cluster'.

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
    """Model for set_flags. Set/Unset multiple Ceph flags at once. Each flag is a top-level optional boolean: passing true sets the flag, false unsets it, omitting it leaves the current state untouched. Runs as a worker task; returns a UPID to follow. request."""
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
    """Model for set_flags. Set/Unset multiple Ceph flags at once. Each flag is a top-level optional boolean: passing true sets the flag, false unsets it, omitting it leaves the current state untouched. Runs as a worker task; returns a UPID to follow. response."""
    root: StrictStr = Field(...)

class GetClusterCephFlagsFlagResponse(RootModel[bool]):
    """Model for get_flag. Get the status of a specific ceph flag. response."""
    root: bool = Field(...)

class PutClusterCephFlagsFlagRequest(ProxmoxBaseModel):
    """Model for update_flag. Set or clear (unset) a specific Ceph flag. Runs synchronously (unlike the bulk PUT /cluster/ceph/flags endpoint, which forks a worker task). request."""
    value: bool = Field(..., description='The new value of the flag')

class PutClusterCephFlagsFlagResponse(RootModel[None]):
    """Model for update_flag. Set or clear (unset) a specific Ceph flag. Runs synchronously (unlike the bulk PUT /cluster/ceph/flags endpoint, which forks a worker task). response."""
    root: None = Field(...)

class GetClusterCephMetadataResponse(ProxmoxBaseModel):
    """Model for metadata. Get ceph metadata. response."""
    mds: dict[str, object] = Field(..., description="Metadata servers configured in the cluster and their properties, keyed by '<name>@<host>'.")
    mgr: dict[str, object] = Field(..., description="Managers configured in the cluster and their properties, keyed by '<name>@<host>'.")
    mon: dict[str, object] = Field(..., description="Monitors configured in the cluster and their properties, keyed by '<name>@<host>'.")
    node: dict[str, object] = Field(..., description='Ceph version installed on the nodes, keyed by node name.')
    osd: list[dict[str, object]] = Field(..., description='OSDs configured in the cluster and their properties.')

class PostClusterCephRestartBulkRequest(ProxmoxBaseModel):
    """Model for restart_bulk. Cluster-wide rolling restart of all Ceph daemons of the given type. For MON/MGR/MDS each daemon is restarted only after Ceph reports the previous one is back up and the next one is safe to stop. For OSDs the cluster path orchestrates the per-node endpoint at /nodes/{node}/ceph/restart-bulk on each node in turn, inheriting that endpoint's per-OSD 'noout' handling and resume support. The 'noout' flag itself is not exposed by this endpoint as it is OSD-specific (and for OSDs handled by the per-node sub-tasks). request."""
    dry_run: bool | None = Field(None, alias="dry-run", description='Log the plan (which daemons would be restarted, in what order) without actually doing anything.')
    force: bool | None = Field(None, description='Proceed past a HEALTH_WARN with non-benign checks like PG_DEGRADED, SLOW_OPS, or MON_DOWN. HEALTH_ERR is always fatal regardless. The operator is responsible for confirming the cluster is stable enough to absorb a rolling restart.')
    only_outdated: bool | None = Field(None, alias="only-outdated", description='OSDs only: restart only OSDs whose running version differs from the locally-installed ceph-osd binary on their host. Forwarded to each per-node sub-task so the per-host installed version is used (a partial upgrade where one host is on a newer build is handled correctly).')
    service_type: StrictStr = Field(..., alias="service-type", description='Ceph daemon type to restart cluster-wide.')
    timeout: int | None = Field(None, description='Per-daemon timeout (in seconds) for the up-wait phase. Note: for daemons on remote nodes the same timeout also bounds the remote restart task, so the per-daemon budget can be up to 2x this value. Default sized for slow MDS journal replay or MON paxos settle on busy clusters; bump higher if the cluster routinely takes longer to stabilize after a daemon restart.')

class PostClusterCephRestartBulkResponse(RootModel[StrictStr]):
    """Model for restart_bulk. Cluster-wide rolling restart of all Ceph daemons of the given type. For MON/MGR/MDS each daemon is restarted only after Ceph reports the previous one is back up and the next one is safe to stop. For OSDs the cluster path orchestrates the per-node endpoint at /nodes/{node}/ceph/restart-bulk on each node in turn, inheriting that endpoint's per-OSD 'noout' handling and resume support. The 'noout' flag itself is not exposed by this endpoint as it is OSD-specific (and for OSDs handled by the per-node sub-tasks). response."""
    root: StrictStr = Field(...)

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
    comment: StrictStr | None = Field(None, description='Optional comment or description.')
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
    comment: StrictStr | None = Field(None, description='Optional comment or description.')
    name: StrictStr | None = Field(None, description='The name of the alias or ipset.')
    ref: StrictStr | None = Field(None, description='The reference string used in firewall rules.')
    scope: StrictStr | None = Field(None, description='The scope of the reference (e.g., SDN).')
    type: StrictStr | None = Field(None, description='The type of reference (alias or ipset).')

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
    auto_rebalance: bool | None = Field(None, alias="auto-rebalance", description='HA resource may be migrated during automatic rebalancing')
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
    auto_rebalance: bool | None = Field(None, alias="auto-rebalance", description='HA resource may be migrated during automatic rebalancing.')
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
    auto_rebalance: bool | None = Field(None, alias="auto-rebalance", description='HA resource may be migrated during automatic rebalancing')
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

class PostClusterHaRulesResponse(RootModel[None]):
    """Model for create_rule. Create HA rule. response."""
    root: None = Field(...)

class DeleteClusterHaRulesRuleResponse(RootModel[None]):
    """Model for delete_rule. Delete HA rule. response."""
    root: None = Field(...)

class GetClusterHaRulesRuleResponse(ProxmoxBaseModel):
    """Model for read_rule. Read HA rule. response."""
    rule: StrictStr = Field(..., description='HA rule identifier.')
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
    auto_rebalance: bool | None = Field(None, alias="auto-rebalance", description='HA resource may be migrated during automatic rebalancing.')
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

class PostClusterNotificationsTargetsNameTestResponse(RootModel[None]):
    """Model for test_target. Send a test notification to a provided target. response."""
    root: None = Field(...)

class GetClusterOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get datacenter options. Without 'Sys.Audit' on '/' not all options are returned. response."""
    allowed_tags: list[StrictStr] = Field(..., alias="allowed-tags", description='The tags the current user is allowed to set and see.')
    bwlimit: StrictStr | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    consent_text: StrictStr | None = Field(None, alias="consent-text", description='Consent text that is displayed before logging in.')
    console: StrictStr | None = Field(None, description='Select the default Console viewer. You can either use the builtin java applet (VNC; deprecated and maps to html5), an external virt-viewer comtatible application (SPICE), an HTML5 based vnc viewer (noVNC), or an HTML5 based console client (xtermjs). If the selected viewer is not available (e.g. SPICE not activated for the VM), the fallback is noVNC.')
    crs: StrictStr | None = Field(None, description='Cluster resource scheduling settings.')
    description: StrictStr | None = Field(None, description='Datacenter description. Shown in the web-interface datacenter notes panel. This is saved as comment inside the configuration file.')
    email_from: StrictStr | None = Field(None, description='Specify email address to send notification from (default is root@$hostname)')
    fencing: StrictStr | None = Field(None, description="Set the fencing mode of the HA cluster. Hardware mode needs a valid configuration of fence devices in /etc/pve/ha/fence.cfg. With both all two modes are used.\n\nWARNING: 'hardware' and 'both' are EXPERIMENTAL & WIP")
    ha: StrictStr | None = Field(None, description='Cluster wide HA settings.')
    http_proxy: StrictStr | None = Field(None, description="Specify external http proxy which is used for downloads (example: 'http://username:password@host:port/')")
    keyboard: StrictStr | None = Field(None, description='Default keybord layout for vnc server.')
    language: StrictStr | None = Field(None, description='Default GUI language.')
    location: StrictStr | None = Field(None, description='The location of the cluster.')
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
    location: StrictStr | None = Field(None, description='The location of the cluster.')
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

class GetClusterQemuResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Cluster-wide QEMU index response."""
    root: list[dict[str, object]] = Field(...)

class GetClusterQemuCpuFlagsResponseItem(ProxmoxBaseModel):
    """Model for index. List of available CPU flags. Currently only implemented for x86_64, returns an empty list for aarch64. response."""
    description: StrictStr | None = Field(None, description='Description of the CPU flag.')
    name: StrictStr | None = Field(None, description='Name of the CPU flag.')
    supported_on: list[StrictStr] | None = Field(None, alias="supported-on", description='List of nodes supporting the flag with the selected acceleration type ("accel").')

class GetClusterQemuCpuFlagsResponse(RootModel[list[GetClusterQemuCpuFlagsResponseItem]]):
    """List of items. index. List of available CPU flags. Currently only implemented for x86_64, returns an empty list for aarch64. response."""
    root: list[GetClusterQemuCpuFlagsResponseItem] = Field(...)

class GetClusterQemuCustomCpuModelsResponseItem(ProxmoxBaseModel):
    """Model for config. List all custom CPU model definitions visible to the user. response."""
    cputype: StrictStr | None = Field(None, description="Emulated CPU type. Can be default or custom name (custom model names must be prefixed with 'custom-').")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    flags: StrictStr | None = Field(None, description="List of additional CPU flags separated by ';'. Use '+FLAG' to enable, '-FLAG' to disable a flag. There is a special 'nested-virt' shorthand which controls nested virtualization for the current CPU ('svm' for AMD and 'vmx' for Intel). Custom CPU models can specify any flag supported by QEMU/KVM, VM-specific flags must be from the following set for security reasons: aes, amd-no-ssb, amd-ssbd, hv-evmcs, hv-tlbflush, ibpb, md-clear, nested-virt, pcid, pdpe1gb, spec-ctrl, ssbd, virt-ssbd")
    guest_phys_bits: int | None = Field(None, alias="guest-phys-bits", description='Number of physical address bits available to the guest.')
    hidden: bool | None = Field(None, description='Do not identify as a KVM virtual machine. Only affects vCPUs with x86-64 architecture.')
    hv_vendor_id: StrictStr | None = Field(None, alias="hv-vendor-id", description='The Hyper-V vendor ID. Some drivers or programs inside Windows guests need a specific ID.')
    level: int | None = Field(None, description="Maximum input value for the basic CPUID leaves the guest can query - that is the vendor (leaf 0), family/model/stepping and feature bits (leaf 1), cache and topology info (leaves 4 and B), and so on. Higher-numbered leaves are hidden. Setting '30' is a common workaround for Hyper-V boot failures on Windows guests running on recent Intel hosts. Only applies when the vCPU architecture is x86_64.")
    phys_bits: StrictStr | None = Field(None, alias="phys-bits", description="The physical memory address bits that are reported to the guest OS. Should be smaller or equal to the host's. Set to 'host' to use value from host CPU, but note that doing so will break live migration to CPUs with other values.")
    reported_model: StrictStr | None = Field(None, alias="reported-model", description='CPU model and vendor to report to the guest. Must be a QEMU/KVM supported model. Only valid for custom CPU model definitions, default models will always report themselves to the guest OS.')

class GetClusterQemuCustomCpuModelsResponse(RootModel[list[GetClusterQemuCustomCpuModelsResponseItem]]):
    """List of items. config. List all custom CPU model definitions visible to the user. response."""
    root: list[GetClusterQemuCustomCpuModelsResponseItem] = Field(...)

class PostClusterQemuCustomCpuModelsRequest(ProxmoxBaseModel):
    """Model for create. Add a custom CPU model definition. request."""
    cputype: StrictStr = Field(..., description="Name for the custom CPU model. The 'custom-' prefix is optional.")
    flags: StrictStr | None = Field(None, description="List of additional CPU flags separated by ';'. Use '+FLAG' to enable, '-FLAG' to disable a flag. There is a special 'nested-virt' shorthand which controls nested virtualization for the current CPU ('svm' for AMD and 'vmx' for Intel). Custom CPU models can specify any flag supported by QEMU/KVM, VM-specific flags must be from the following set for security reasons: aes, amd-no-ssb, amd-ssbd, hv-evmcs, hv-tlbflush, ibpb, md-clear, nested-virt, pcid, pdpe1gb, spec-ctrl, ssbd, virt-ssbd")
    guest_phys_bits: int | None = Field(None, alias="guest-phys-bits", description='Number of physical address bits available to the guest.')
    hidden: bool | None = Field(None, description='Do not identify as a KVM virtual machine. Only affects vCPUs with x86-64 architecture.')
    hv_vendor_id: StrictStr | None = Field(None, alias="hv-vendor-id", description='The Hyper-V vendor ID. Some drivers or programs inside Windows guests need a specific ID.')
    level: int | None = Field(None, description="Maximum input value for the basic CPUID leaves the guest can query - that is the vendor (leaf 0), family/model/stepping and feature bits (leaf 1), cache and topology info (leaves 4 and B), and so on. Higher-numbered leaves are hidden. Setting '30' is a common workaround for Hyper-V boot failures on Windows guests running on recent Intel hosts. Only applies when the vCPU architecture is x86_64.")
    phys_bits: StrictStr | None = Field(None, alias="phys-bits", description="The physical memory address bits that are reported to the guest OS. Should be smaller or equal to the host's. Set to 'host' to use value from host CPU, but note that doing so will break live migration to CPUs with other values.")
    reported_model: StrictStr = Field(..., alias="reported-model", description='CPU model and vendor to report to the guest. Must be a QEMU/KVM supported model. Only valid for custom CPU model definitions, default models will always report themselves to the guest OS.')

class PostClusterQemuCustomCpuModelsResponse(RootModel[None]):
    """Model for create. Add a custom CPU model definition. response."""
    root: None = Field(...)

class DeleteClusterQemuCustomCpuModelsCputypeResponse(RootModel[None]):
    """Model for delete. Delete a custom CPU model definition. response."""
    root: None = Field(...)

class GetClusterQemuCustomCpuModelsCputypeResponse(ProxmoxBaseModel):
    """Model for info. Retrieve details about a specific custom CPU model. response."""
    cputype: StrictStr | None = Field(None, description="Emulated CPU type. Can be default or custom name (custom model names must be prefixed with 'custom-').")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    flags: StrictStr | None = Field(None, description="List of additional CPU flags separated by ';'. Use '+FLAG' to enable, '-FLAG' to disable a flag. There is a special 'nested-virt' shorthand which controls nested virtualization for the current CPU ('svm' for AMD and 'vmx' for Intel). Custom CPU models can specify any flag supported by QEMU/KVM, VM-specific flags must be from the following set for security reasons: aes, amd-no-ssb, amd-ssbd, hv-evmcs, hv-tlbflush, ibpb, md-clear, nested-virt, pcid, pdpe1gb, spec-ctrl, ssbd, virt-ssbd")
    guest_phys_bits: int | None = Field(None, alias="guest-phys-bits", description='Number of physical address bits available to the guest.')
    hidden: bool | None = Field(None, description='Do not identify as a KVM virtual machine. Only affects vCPUs with x86-64 architecture.')
    hv_vendor_id: StrictStr | None = Field(None, alias="hv-vendor-id", description='The Hyper-V vendor ID. Some drivers or programs inside Windows guests need a specific ID.')
    level: int | None = Field(None, description="Maximum input value for the basic CPUID leaves the guest can query - that is the vendor (leaf 0), family/model/stepping and feature bits (leaf 1), cache and topology info (leaves 4 and B), and so on. Higher-numbered leaves are hidden. Setting '30' is a common workaround for Hyper-V boot failures on Windows guests running on recent Intel hosts. Only applies when the vCPU architecture is x86_64.")
    phys_bits: StrictStr | None = Field(None, alias="phys-bits", description="The physical memory address bits that are reported to the guest OS. Should be smaller or equal to the host's. Set to 'host' to use value from host CPU, but note that doing so will break live migration to CPUs with other values.")
    reported_model: StrictStr | None = Field(None, alias="reported-model", description='CPU model and vendor to report to the guest. Must be a QEMU/KVM supported model. Only valid for custom CPU model definitions, default models will always report themselves to the guest OS.')

class PutClusterQemuCustomCpuModelsCputypeRequest(ProxmoxBaseModel):
    """Model for update. Update a custom CPU model definition. request."""
    delete: StrictStr | None = Field(None, description='A list of properties to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    flags: StrictStr | None = Field(None, description="List of additional CPU flags separated by ';'. Use '+FLAG' to enable, '-FLAG' to disable a flag. There is a special 'nested-virt' shorthand which controls nested virtualization for the current CPU ('svm' for AMD and 'vmx' for Intel). Custom CPU models can specify any flag supported by QEMU/KVM, VM-specific flags must be from the following set for security reasons: aes, amd-no-ssb, amd-ssbd, hv-evmcs, hv-tlbflush, ibpb, md-clear, nested-virt, pcid, pdpe1gb, spec-ctrl, ssbd, virt-ssbd")
    guest_phys_bits: int | None = Field(None, alias="guest-phys-bits", description='Number of physical address bits available to the guest.')
    hidden: bool | None = Field(None, description='Do not identify as a KVM virtual machine. Only affects vCPUs with x86-64 architecture.')
    hv_vendor_id: StrictStr | None = Field(None, alias="hv-vendor-id", description='The Hyper-V vendor ID. Some drivers or programs inside Windows guests need a specific ID.')
    level: int | None = Field(None, description="Maximum input value for the basic CPUID leaves the guest can query - that is the vendor (leaf 0), family/model/stepping and feature bits (leaf 1), cache and topology info (leaves 4 and B), and so on. Higher-numbered leaves are hidden. Setting '30' is a common workaround for Hyper-V boot failures on Windows guests running on recent Intel hosts. Only applies when the vCPU architecture is x86_64.")
    phys_bits: StrictStr | None = Field(None, alias="phys-bits", description="The physical memory address bits that are reported to the guest OS. Should be smaller or equal to the host's. Set to 'host' to use value from host CPU, but note that doing so will break live migration to CPUs with other values.")
    reported_model: StrictStr | None = Field(None, alias="reported-model", description='CPU model and vendor to report to the guest. Must be a QEMU/KVM supported model. Only valid for custom CPU model definitions, default models will always report themselves to the guest OS.')

class PutClusterQemuCustomCpuModelsCputypeResponse(RootModel[None]):
    """Model for update. Update a custom CPU model definition. response."""
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
    host_arch: StrictStr | None = Field(None, alias="host-arch", description="The node's CPU architecture. (for type 'node').")
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
    bgp_mode: StrictStr | None = Field(None, alias="bgp-mode", description='Whether to use eBGP or iBGP. Auto mode chooses depending on BGP controller or falls back to iBGP.')
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
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    peer_group_name: StrictStr | None = Field(None, alias="peer-group-name", description='Name of the peer group for this EVPN controller')
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
    bgp_mode: StrictStr | None = Field(None, alias="bgp-mode", description='Whether to use eBGP or iBGP. Auto mode chooses depending on BGP controller or falls back to iBGP.')
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
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    peer_group_name: StrictStr | None = Field(None, alias="peer-group-name", description='Name of the peer group for this EVPN controller')
    peers: StrictStr | None = Field(None, description='peers address list.')
    route_map_in: StrictStr | None = Field(None, alias="route-map-in", description='Route Map that should be applied for incoming routes')
    route_map_out: StrictStr | None = Field(None, alias="route-map-out", description='Route Map that should be applied for outgoing routes')
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
    bgp_mode: StrictStr | None = Field(None, alias="bgp-mode", description='Whether to use eBGP or iBGP. Auto mode chooses depending on BGP controller or falls back to iBGP.')
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
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    peer_group_name: StrictStr | None = Field(None, alias="peer-group-name", description='Name of the peer group for this EVPN controller')
    peers: StrictStr | None = Field(None, description='Comma-separated list of the peers IP addresses.')
    pending: dict[str, object] | None = Field(None, description='Changes that have not yet been applied to the running configuration.')
    state: StrictStr | None = Field(None, description='State of the SDN configuration object.')
    type: StrictStr = Field(..., description='Type of the controller')

class PutClusterSdnControllersControllerRequest(ProxmoxBaseModel):
    """Model for update. Update sdn controller object configuration. request."""
    asn: int | None = Field(None, description='autonomous system number')
    bgp_mode: StrictStr | None = Field(None, alias="bgp-mode", description='Whether to use eBGP or iBGP. Auto mode chooses depending on BGP controller or falls back to iBGP.')
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
    nodes: StrictStr | None = Field(None, description='List of cluster node names.')
    peer_group_name: StrictStr | None = Field(None, alias="peer-group-name", description='Name of the peer group for this EVPN controller')
    peers: StrictStr | None = Field(None, description='peers address list.')
    route_map_in: StrictStr | None = Field(None, alias="route-map-in", description='Route Map that should be applied for incoming routes')
    route_map_out: StrictStr | None = Field(None, alias="route-map-out", description='Route Map that should be applied for outgoing routes')

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
    persistent_keepalive: float | None = Field(None, description='A seconds interval, between 1 and 65535 inclusive, of how often to send an authenticated empty packet to the peer for the purpose of keeping a stateful firewall or NAT mapping valid persistently. For example, if the interface very rarely sends traffic, but it might at anytime receive traffic from another node, and it is behind NAT, the interface might benefit from having a persistent keepalive interval of 25 seconds. If unset or set to 0, it is turned off')
    protocol: StrictStr | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')
    redistribute: list[StrictStr] | None = Field(None)
    route_filter: StrictStr | None = Field(None, description='A prefix list that should be used for filtering routes that are to be installed into the kernel routing table')

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
    persistent_keepalive: float | None = Field(None, description='A seconds interval, between 1 and 65535 inclusive, of how often to send an authenticated empty packet to the peer for the purpose of keeping a stateful firewall or NAT mapping valid persistently. For example, if the interface very rarely sends traffic, but it might at anytime receive traffic from another node, and it is behind NAT, the interface might benefit from having a persistent keepalive interval of 25 seconds. If unset or set to 0, it is turned off')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')
    redistribute: list[StrictStr] = Field(...)
    route_filter: StrictStr | None = Field(None, description='A prefix list that should be used for filtering routes that are to be installed into the kernel routing table')

class PostClusterSdnFabricsFabricResponse(RootModel[None]):
    """Model for add_fabric. Add a fabric response."""
    root: None = Field(...)

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
    persistent_keepalive: float | None = Field(None, description='A seconds interval, between 1 and 65535 inclusive, of how often to send an authenticated empty packet to the peer for the purpose of keeping a stateful firewall or NAT mapping valid persistently. For example, if the interface very rarely sends traffic, but it might at anytime receive traffic from another node, and it is behind NAT, the interface might benefit from having a persistent keepalive interval of 25 seconds. If unset or set to 0, it is turned off')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')
    redistribute: list[StrictStr] = Field(...)
    route_filter: StrictStr | None = Field(None, description='A prefix list that should be used for filtering routes that are to be installed into the kernel routing table')

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
    persistent_keepalive: float | None = Field(None, description='A seconds interval, between 1 and 65535 inclusive, of how often to send an authenticated empty packet to the peer for the purpose of keeping a stateful firewall or NAT mapping valid persistently. For example, if the interface very rarely sends traffic, but it might at anytime receive traffic from another node, and it is behind NAT, the interface might benefit from having a persistent keepalive interval of 25 seconds. If unset or set to 0, it is turned off')
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')
    redistribute: list[StrictStr] = Field(...)
    route_filter: StrictStr | None = Field(None, description='A prefix list that should be used for filtering routes that are to be installed into the kernel routing table')

class PutClusterSdnFabricsFabricIdResponse(RootModel[None]):
    """Model for update_fabric. Update a fabric response."""
    root: None = Field(...)

class GetClusterSdnFabricsNodeResponseItem(ProxmoxBaseModel):
    """Model for list_nodes. SDN Fabrics Index response."""
    allowed_ips: list[StrictStr] | None = Field(None, description='A list of IPs that are routable via this node in the WireGuard fabric.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    endpoint: StrictStr | None = Field(None, description='The endpoint used for connecting to this node.')
    fabric_id: StrictStr | None = Field(None, description='Identifier for SDN fabrics')
    interfaces: list[StrictStr] | None = Field(None)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: StrictStr | None = Field(None, description='Identifier for nodes in an SDN fabric')
    peers: list[StrictStr] | None = Field(None)
    protocol: StrictStr | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')
    public_key: StrictStr | None = Field(None, description='The public key for the external node.')
    role: StrictStr | None = Field(None, description='The role of this node in the WireGuard fabric.')

class GetClusterSdnFabricsNodeResponse(RootModel[list[GetClusterSdnFabricsNodeResponseItem]]):
    """List of items. list_nodes. SDN Fabrics Index response."""
    root: list[GetClusterSdnFabricsNodeResponseItem] = Field(...)

class GetClusterSdnFabricsNodeFabricIdResponseItem(ProxmoxBaseModel):
    """Model for list_nodes_fabric. SDN Fabrics Index response."""
    allowed_ips: list[StrictStr] | None = Field(None, description='A list of IPs that are routable via this node in the WireGuard fabric.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    endpoint: StrictStr | None = Field(None, description='The endpoint used for connecting to this node.')
    fabric_id: StrictStr | None = Field(None, description='Identifier for SDN fabrics')
    interfaces: list[StrictStr] | None = Field(None)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: StrictStr | None = Field(None, description='Identifier for nodes in an SDN fabric')
    peers: list[StrictStr] | None = Field(None)
    protocol: StrictStr | None = Field(None, description='Type of configuration entry in an SDN Fabric section config')
    public_key: StrictStr | None = Field(None, description='The public key for the external node.')
    role: StrictStr | None = Field(None, description='The role of this node in the WireGuard fabric.')

class GetClusterSdnFabricsNodeFabricIdResponse(RootModel[list[GetClusterSdnFabricsNodeFabricIdResponseItem]]):
    """List of items. list_nodes_fabric. SDN Fabrics Index response."""
    root: list[GetClusterSdnFabricsNodeFabricIdResponseItem] = Field(...)

class PostClusterSdnFabricsNodeFabricIdRequest(ProxmoxBaseModel):
    """Model for add_node. Add a node request."""
    allowed_ips: list[StrictStr] | None = Field(None, description='A list of IPs that are routable via this node in the WireGuard fabric.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    endpoint: StrictStr | None = Field(None, description='The endpoint used for connecting to this node.')
    interfaces: list[StrictStr] = Field(...)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: StrictStr = Field(..., description='Identifier for nodes in an SDN fabric')
    peers: list[StrictStr] | None = Field(None)
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')
    public_key: StrictStr | None = Field(None, description='The public key for the external node.')
    role: StrictStr | None = Field(None, description='The role of this node in the WireGuard fabric.')

class PostClusterSdnFabricsNodeFabricIdResponse(RootModel[None]):
    """Model for add_node. Add a node response."""
    root: None = Field(...)

class DeleteClusterSdnFabricsNodeFabricIdNodeIdResponse(RootModel[None]):
    """Model for delete_node. Add a node response."""
    root: None = Field(...)

class GetClusterSdnFabricsNodeFabricIdNodeIdResponse(ProxmoxBaseModel):
    """Model for get_node. Get a node response."""
    allowed_ips: list[StrictStr] | None = Field(None, description='A list of IPs that are routable via this node in the WireGuard fabric.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    endpoint: StrictStr | None = Field(None, description='The endpoint used for connecting to this node.')
    fabric_id: StrictStr = Field(..., description='Identifier for SDN fabrics')
    interfaces: list[StrictStr] = Field(...)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    node_id: StrictStr = Field(..., description='Identifier for nodes in an SDN fabric')
    peers: list[StrictStr] | None = Field(None)
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')
    public_key: StrictStr | None = Field(None, description='The public key for the external node.')
    role: StrictStr | None = Field(None, description='The role of this node in the WireGuard fabric.')

class PutClusterSdnFabricsNodeFabricIdNodeIdRequest(ProxmoxBaseModel):
    """Model for update_node. Update a node request."""
    allowed_ips: list[StrictStr] | None = Field(None, description='A list of IPs that are routable via this node in the WireGuard fabric.')
    delete: list[StrictStr] = Field(...)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    endpoint: StrictStr | None = Field(None, description='The endpoint used for connecting to this node.')
    interfaces: list[StrictStr] = Field(...)
    ip: StrictStr | None = Field(None, description='IPv4 address for this node')
    ip6: StrictStr | None = Field(None, description='IPv6 address for this node')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    peers: list[StrictStr] | None = Field(None)
    protocol: StrictStr = Field(..., description='Type of configuration entry in an SDN Fabric section config')
    public_key: StrictStr | None = Field(None, description='The public key for the external node.')
    role: StrictStr | None = Field(None, description='The role of this node in the WireGuard fabric.')

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

class GetClusterSdnPrefixListsResponse(RootModel[list[dict[str, object]]]):
    """Model for list_prefix_lists. List Prefix Lists response."""
    root: list[dict[str, object]] = Field(...)

class PostClusterSdnPrefixListsRequest(ProxmoxBaseModel):
    """Model for create_prefix_list_entry. Create Prefix List request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    entries: list[StrictStr] | None = Field(None)
    id: StrictStr = Field(..., description='The SDN prefix list identifier')
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class PostClusterSdnPrefixListsResponse(RootModel[None]):
    """Model for create_prefix_list_entry. Create Prefix List response."""
    root: None = Field(...)

class DeleteClusterSdnPrefixListsIdRequest(ProxmoxBaseModel):
    """Model for delete_prefix_list. Delete Prefix List request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnPrefixListsIdResponse(RootModel[None]):
    """Model for delete_prefix_list. Delete Prefix List response."""
    root: None = Field(...)

class GetClusterSdnPrefixListsIdResponse(RootModel[dict[str, object]]):
    """Model for get_prefix_list. Get Prefix List response."""
    root: dict[str, object] = Field(...)

class PutClusterSdnPrefixListsIdRequest(ProxmoxBaseModel):
    """Model for update_prefix_list. Update Prefix List request."""
    delete: list[StrictStr] | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    entries: list[StrictStr] | None = Field(None)
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class PutClusterSdnPrefixListsIdResponse(RootModel[None]):
    """Model for update_prefix_list. Update Prefix List response."""
    root: None = Field(...)

class GetClusterSdnPrefixListsIdEntriesResponse(RootModel[list[dict[str, object]]]):
    """Model for get_prefix_list_entries. List Prefix List Entries response."""
    root: list[dict[str, object]] = Field(...)

class PostClusterSdnPrefixListsIdEntriesRequest(ProxmoxBaseModel):
    """Model for create_prefix_list_entry. Create Prefix List Entry request."""
    action: StrictStr = Field(...)
    ge: int | None = Field(None)
    le: int | None = Field(None)
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    prefix: StrictStr = Field(...)
    seq: int | None = Field(None)

class PostClusterSdnPrefixListsIdEntriesResponse(RootModel[None]):
    """Model for create_prefix_list_entry. Create Prefix List Entry response."""
    root: None = Field(...)

class DeleteClusterSdnPrefixListsIdEntriesUrlSeqRequest(ProxmoxBaseModel):
    """Model for delete_prefix_list_entry. Delete Prefix List Entry request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnPrefixListsIdEntriesUrlSeqResponse(RootModel[None]):
    """Model for delete_prefix_list_entry. Delete Prefix List Entry response."""
    root: None = Field(...)

class GetClusterSdnPrefixListsIdEntriesUrlSeqResponse(RootModel[dict[str, object]]):
    """Model for get_prefix_list_entry. Get Prefix List Entry response."""
    root: dict[str, object] = Field(...)

class PutClusterSdnPrefixListsIdEntriesUrlSeqRequest(ProxmoxBaseModel):
    """Model for update_prefix_list_entry. Update Prefix List Entry request."""
    action: StrictStr | None = Field(None)
    delete: list[StrictStr] | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    ge: int | None = Field(None)
    le: int | None = Field(None)
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    prefix: StrictStr | None = Field(None)
    seq: int | None = Field(None)

class PutClusterSdnPrefixListsIdEntriesUrlSeqResponse(RootModel[None]):
    """Model for update_prefix_list_entry. Update Prefix List Entry response."""
    root: None = Field(...)

class PostClusterSdnRollbackRequest(ProxmoxBaseModel):
    """Model for rollback. Rollback pending changes to SDN configuration request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    release_lock: bool | None = Field(None, alias="release-lock", description='When lock-token has been provided and configuration successfully rollbacked, release the lock automatically afterwards')

class PostClusterSdnRollbackResponse(RootModel[None]):
    """Model for rollback. Rollback pending changes to SDN configuration response."""
    root: None = Field(...)

class GetClusterSdnRouteMapsResponseItem(ProxmoxBaseModel):
    """Model for list_route_maps. List Route Maps response."""
    id: StrictStr | None = Field(None, description='The SDN route map identifier')

class GetClusterSdnRouteMapsResponse(RootModel[list[GetClusterSdnRouteMapsResponseItem]]):
    """List of items. list_route_maps. List Route Maps response."""
    root: list[GetClusterSdnRouteMapsResponseItem] = Field(...)

class GetClusterSdnRouteMapsEntriesResponseItem(ProxmoxBaseModel):
    """Model for list_route_map_entries. Lists all route map entries. response."""
    action: StrictStr | None = Field(None, description='Matching policy of a route map entry.')
    call: StrictStr | None = Field(None, description='The SDN route map identifier')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    exit_action: StrictStr | None = Field(None, alias="exit-action")
    match: list[StrictStr] | None = Field(None)
    order: int | None = Field(None, description='The index of this route map entry')
    route_map_id: StrictStr | None = Field(None, alias="route-map-id", description='The SDN route map identifier')
    set: list[StrictStr] | None = Field(None)

class GetClusterSdnRouteMapsEntriesResponse(RootModel[list[GetClusterSdnRouteMapsEntriesResponseItem]]):
    """List of items. list_route_map_entries. Lists all route map entries. response."""
    root: list[GetClusterSdnRouteMapsEntriesResponseItem] = Field(...)

class PostClusterSdnRouteMapsEntriesRequest(ProxmoxBaseModel):
    """Model for create_route_map_entry. Create Route Map entry request."""
    action: StrictStr = Field(..., description='Matching policy of a route map entry.')
    call: StrictStr | None = Field(None, description='The SDN route map identifier')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    exit_action: StrictStr | None = Field(None, alias="exit-action")
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    match: list[StrictStr] | None = Field(None)
    order: int = Field(..., description='The index of this route map entry')
    route_map_id: StrictStr = Field(..., alias="route-map-id", description='The SDN route map identifier')
    set: list[StrictStr] | None = Field(None)

class PostClusterSdnRouteMapsEntriesResponse(RootModel[None]):
    """Model for create_route_map_entry. Create Route Map entry response."""
    root: None = Field(...)

class GetClusterSdnRouteMapsEntriesRouteMapIdResponseItem(ProxmoxBaseModel):
    """Model for list_route_map_entries_for_route_map. List all entries for a given Route Map response."""
    action: StrictStr | None = Field(None, description='Matching policy of a route map entry.')
    call: StrictStr | None = Field(None, description='The SDN route map identifier')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    exit_action: StrictStr | None = Field(None, alias="exit-action")
    match: list[StrictStr] | None = Field(None)
    order: int | None = Field(None, description='The index of this route map entry')
    route_map_id: StrictStr | None = Field(None, alias="route-map-id", description='The SDN route map identifier')
    set: list[StrictStr] | None = Field(None)

class GetClusterSdnRouteMapsEntriesRouteMapIdResponse(RootModel[list[GetClusterSdnRouteMapsEntriesRouteMapIdResponseItem]]):
    """List of items. list_route_map_entries_for_route_map. List all entries for a given Route Map response."""
    root: list[GetClusterSdnRouteMapsEntriesRouteMapIdResponseItem] = Field(...)

class DeleteClusterSdnRouteMapsEntriesRouteMapIdEntryOrderRequest(ProxmoxBaseModel):
    """Model for delete_route_map_entry. Delete Route Map Entry request."""
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')

class DeleteClusterSdnRouteMapsEntriesRouteMapIdEntryOrderResponse(RootModel[None]):
    """Model for delete_route_map_entry. Delete Route Map Entry response."""
    root: None = Field(...)

class GetClusterSdnRouteMapsEntriesRouteMapIdEntryOrderResponse(ProxmoxBaseModel):
    """Model for get_route_map_entry. Get Route Map Entry response."""
    action: StrictStr = Field(..., description='Matching policy of a route map entry.')
    call: StrictStr | None = Field(None, description='The SDN route map identifier')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    exit_action: StrictStr | None = Field(None, alias="exit-action")
    match: list[StrictStr] | None = Field(None)
    order: int = Field(..., description='The index of this route map entry')
    route_map_id: StrictStr = Field(..., alias="route-map-id", description='The SDN route map identifier')
    set: list[StrictStr] | None = Field(None)

class PutClusterSdnRouteMapsEntriesRouteMapIdEntryOrderRequest(ProxmoxBaseModel):
    """Model for update_route_map_entry. Update Route Map Entry request."""
    action: StrictStr | None = Field(None, description='Matching policy of a route map entry.')
    call: StrictStr | None = Field(None, description='The SDN route map identifier')
    delete: list[StrictStr] | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    exit_action: StrictStr | None = Field(None, alias="exit-action")
    lock_token: StrictStr | None = Field(None, alias="lock-token", description='the token for unlocking the global SDN configuration')
    match: list[StrictStr] | None = Field(None)
    set: list[StrictStr] | None = Field(None)

class PutClusterSdnRouteMapsEntriesRouteMapIdEntryOrderResponse(RootModel[None]):
    """Model for update_route_map_entry. Update Route Map Entry response."""
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
    secondary_controllers: list[StrictStr] | None = Field(None, alias="secondary-controllers", description='Additional controllers.')
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
    secondary_controllers: list[StrictStr] | None = Field(None, alias="secondary-controllers", description='Additional controllers.')
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
    secondary_controllers: list[StrictStr] | None = Field(None, alias="secondary-controllers", description='Additional controllers.')
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
    secondary_controllers: list[StrictStr] | None = Field(None, alias="secondary-controllers", description='Additional controllers.')
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
