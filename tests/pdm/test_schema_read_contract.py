"""Schema-backed contract coverage for every public PDM read operation."""

from __future__ import annotations

import traceback
from collections.abc import Awaitable, Callable
from typing import Any, NamedTuple, cast

import pytest

from proxmox_sdk.pdm import PDMClient, PDMResponseContractError
from proxmox_sdk.pdm import models as m
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.backends.mock import MockBackend
from proxmox_sdk.sdk.resource import ProxmoxResource
from proxmox_sdk.sdk.services import SERVICES

from .conftest import make_pdm_sdk


class ReadCase(NamedTuple):
    """One public read call and its captured-schema contract."""

    name: str
    attributes: tuple[str, ...]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    path: str
    result_type: type[Any]
    item_type: type[Any] | None = None
    params: dict[str, Any] | None = None


READ_CASES = [
    ReadCase("version", ("version",), (), {}, "/api2/json/version", m.PDMVersion),
    ReadCase("ping", ("ping",), (), {}, "/api2/json/ping", str),
    ReadCase(
        "remotes-list",
        ("remotes", "list"),
        (),
        {},
        "/api2/json/remotes/remote",
        list,
        m.PDMRemote,
    ),
    ReadCase(
        "remotes-get",
        ("remotes", "get"),
        ("pve-a",),
        {},
        "/api2/json/remotes/remote/pve-a/config",
        m.PDMRemote,
    ),
    ReadCase(
        "remotes-version",
        ("remotes", "version"),
        ("pve-a",),
        {},
        "/api2/json/remotes/remote/pve-a/version",
        m.PDMRemoteVersion,
    ),
    ReadCase(
        "qemu-list",
        ("pve", "qemu", "list"),
        ("pve-a",),
        {},
        "/api2/json/pve/remotes/pve-a/qemu",
        list,
        m.PDMGuest,
    ),
    ReadCase(
        "qemu-config",
        ("pve", "qemu", "config"),
        ("pve-a", 100),
        {},
        "/api2/json/pve/remotes/pve-a/qemu/100/config",
        m.PDMGuestConfig,
        params={"state": "pending"},
    ),
    ReadCase(
        "qemu-rrddata",
        ("pve", "qemu", "rrddata"),
        ("pve-a", 100),
        {},
        "/api2/json/pve/remotes/pve-a/qemu/100/rrddata",
        list,
        m.PDMRRDData,
        {"timeframe": "hour", "cf": "AVERAGE"},
    ),
    ReadCase(
        "lxc-list",
        ("pve", "lxc", "list"),
        ("pve-a",),
        {},
        "/api2/json/pve/remotes/pve-a/lxc",
        list,
        m.PDMGuest,
    ),
    ReadCase(
        "lxc-config",
        ("pve", "lxc", "config"),
        ("pve-a", 200),
        {},
        "/api2/json/pve/remotes/pve-a/lxc/200/config",
        m.PDMGuestConfig,
        params={"state": "pending"},
    ),
    ReadCase(
        "lxc-rrddata",
        ("pve", "lxc", "rrddata"),
        ("pve-a", 200),
        {},
        "/api2/json/pve/remotes/pve-a/lxc/200/rrddata",
        list,
        m.PDMRRDData,
        {"timeframe": "hour", "cf": "AVERAGE"},
    ),
    ReadCase(
        "pve-nodes",
        ("pve", "nodes"),
        ("pve-a",),
        {},
        "/api2/json/pve/remotes/pve-a/nodes",
        list,
        m.PDMNode,
    ),
    ReadCase(
        "pve-node-rrddata",
        ("pve", "node_rrddata"),
        ("pve-a", "node-a"),
        {},
        "/api2/json/pve/remotes/pve-a/nodes/node-a/rrddata",
        list,
        m.PDMRRDData,
        {"timeframe": "hour", "cf": "AVERAGE"},
    ),
    ReadCase(
        "pve-resources",
        ("pve", "resources"),
        ("pve-a",),
        {"type": "vm"},
        "/api2/json/pve/remotes/pve-a/resources",
        list,
        m.PDMResource,
        {"kind": "vm"},
    ),
    ReadCase(
        "pve-tasks",
        ("pve", "tasks"),
        ("pve-a",),
        {},
        "/api2/json/pve/remotes/pve-a/tasks",
        list,
        m.PDMTask,
    ),
    ReadCase(
        "pbs-datastores",
        ("pbs", "datastores"),
        ("pbs-a",),
        {},
        "/api2/json/pbs/remotes/pbs-a/datastore",
        list,
        m.PDMPBSDatastore,
    ),
    ReadCase(
        "pbs-datastore-rrddata",
        ("pbs", "datastore_rrddata"),
        ("pbs-a", "tank"),
        {},
        "/api2/json/pbs/remotes/pbs-a/datastore/tank/rrddata",
        list,
        m.PDMRRDData,
        {"timeframe": "hour", "cf": "AVERAGE"},
    ),
    ReadCase(
        "pbs-snapshots",
        ("pbs", "snapshots"),
        ("pbs-a", "tank"),
        {"namespace": "prod"},
        "/api2/json/pbs/remotes/pbs-a/datastore/tank/snapshots",
        list,
        m.PDMPBSSnapshot,
        {"ns": "prod"},
    ),
    ReadCase(
        "pbs-node-rrddata",
        ("pbs", "node_rrddata"),
        ("pbs-a",),
        {},
        "/api2/json/pbs/remotes/pbs-a/rrddata",
        list,
        m.PDMRRDData,
        {"timeframe": "hour", "cf": "AVERAGE"},
    ),
    ReadCase(
        "pbs-tasks",
        ("pbs", "tasks"),
        ("pbs-a",),
        {},
        "/api2/json/pbs/remotes/pbs-a/tasks",
        list,
        m.PDMTask,
    ),
    ReadCase(
        "pbs-task-status",
        ("pbs", "task_status"),
        ("pbs-a", "UPID:pbs:1"),
        {},
        "/api2/json/pbs/remotes/pbs-a/tasks/UPID%3Apbs%3A1/status",
        m.PDMTaskStatus,
    ),
    ReadCase(
        "resources-list",
        ("resources", "list"),
        (),
        {"type": "vm"},
        "/api2/json/resources/list",
        list,
        m.PDMResource,
        {"resource-type": "qemu"},
    ),
    ReadCase(
        "resources-status",
        ("resources", "status"),
        (),
        {},
        "/api2/json/resources/status",
        m.PDMResourceStatus,
    ),
    ReadCase(
        "subscriptions-list",
        ("subscriptions", "list"),
        (),
        {},
        "/api2/json/resources/subscription",
        list,
        m.PDMSubscription,
    ),
    ReadCase(
        "metrics-status",
        ("metrics", "status"),
        (),
        {},
        "/api2/json/remotes/metric-collection/status",
        list,
        m.PDMMetricCollectionStatus,
    ),
    ReadCase(
        "users-list",
        ("access", "users", "list"),
        (),
        {},
        "/api2/json/access/users",
        list,
        m.PDMUser,
    ),
    ReadCase(
        "users-get",
        ("access", "users", "get"),
        ("alice@pdm",),
        {},
        "/api2/json/access/users/alice%40pdm",
        m.PDMUser,
    ),
    ReadCase(
        "acl-list",
        ("access", "acl", "list"),
        (),
        {},
        "/api2/json/access/acl",
        list,
        m.PDMACLEntry,
    ),
    ReadCase(
        "tfa-list",
        ("access", "tfa", "list"),
        ("alice@pdm",),
        {},
        "/api2/json/access/tfa/alice%40pdm",
        list,
        m.PDMTFAEntry,
    ),
    ReadCase(
        "tokens-list",
        ("access", "tokens", "list"),
        ("alice@pdm",),
        {},
        "/api2/json/access/users/alice%40pdm/token",
        list,
        m.PDMAPIToken,
    ),
    ReadCase(
        "views-list",
        ("views", "list"),
        (),
        {},
        "/api2/json/config/views",
        list,
        m.PDMView,
    ),
    ReadCase(
        "views-get",
        ("views", "get"),
        ("ops",),
        {},
        "/api2/json/config/views/ops",
        m.PDMView,
    ),
]


class RecordingSchemaBackend(MockBackend):
    """Use captured-schema happy-path samples and record the exact request."""

    def __init__(self) -> None:
        super().__init__(schema_version="latest", api_path_prefix="/api2/json", service="PDM")
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        self.calls.append((method, path, params))
        return await super().request(method, path, params=params, data=data)


def make_schema_client() -> tuple[PDMClient, RecordingSchemaBackend]:
    """Build a PDM client backed by the committed captured OpenAPI artifact."""

    service = SERVICES["PDM"]
    backend = RecordingSchemaBackend()
    sdk = object.__new__(ProxmoxSDK)
    sdk._service_name = "PDM"
    sdk._service_config = service
    sdk._backend_name = "recording-schema"
    sdk._backend = backend
    sdk._root = ProxmoxResource(path=service.api_path_prefix, backend=backend)
    return PDMClient.from_sdk(sdk), backend


async def invoke(client: PDMClient, case: ReadCase) -> Any:
    """Resolve and invoke a dotted public PDM read method."""

    target: Any = client
    for attribute in case.attributes:
        target = getattr(target, attribute)
    method = cast(Callable[..., Awaitable[Any]], target)
    return await method(*case.args, **case.kwargs)


@pytest.mark.parametrize("case", READ_CASES, ids=lambda case: case.name)
async def test_every_public_read_accepts_captured_schema_samples(case: ReadCase) -> None:
    client, backend = make_schema_client()
    try:
        result = await invoke(client, case)
    finally:
        await client.close()

    assert backend.calls == [("GET", case.path, case.params)]
    assert isinstance(result, case.result_type)
    if case.item_type is not None:
        assert result
        assert all(isinstance(item, case.item_type) for item in result)


async def test_contract_error_rejects_wrong_cardinality_without_leaking_payload() -> None:
    sdk, _ = make_pdm_sdk(
        {"/api2/json/remotes/remote": {"data": {"id": "private-remote", "token": "do-not-leak"}}}
    )

    with pytest.raises(PDMResponseContractError) as exc_info:
        await PDMClient(_sdk=sdk).remotes.list()

    message = str(exc_info.value)
    assert "GET /remotes/remote" in message
    assert "expected a list" in message
    assert "private-remote" not in message
    assert "do-not-leak" not in message


async def test_contract_error_reports_missing_identifier_without_leaking_payload() -> None:
    sdk, _ = make_pdm_sdk(
        {"/api2/json/remotes/remote": {"data": [{"type": "pve", "token": "do-not-leak"}]}}
    )

    with pytest.raises(PDMResponseContractError) as exc_info:
        await PDMClient(_sdk=sdk).remotes.list()

    message = str(exc_info.value)
    assert "invalid fields: id" in message
    assert "do-not-leak" not in message

    formatted_traceback = "".join(traceback.format_exception(exc_info.value))
    assert "do-not-leak" not in formatted_traceback
    assert "ValidationError" not in formatted_traceback
    assert exc_info.value.__cause__ is None
    assert exc_info.value.__context__ is None


async def test_contract_error_redacts_remote_resource_failure() -> None:
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/resources/list": {
                "data": [
                    {
                        "remote": "private-remote",
                        "error": "credential do-not-leak rejected",
                        "resources": [],
                    }
                ]
            }
        }
    )

    with pytest.raises(PDMResponseContractError) as exc_info:
        await PDMClient(_sdk=sdk).resources.list()

    message = str(exc_info.value)
    assert "remote reported an error without usable resources" in message
    assert "private-remote" not in message
    assert "do-not-leak" not in message


async def test_partial_remote_failure_preserves_only_redacted_error_context() -> None:
    sentinel = "credential do-not-leak rejected"
    nested_error = "nested do-not-leak error"
    nested_remote_error = "nested do-not-leak remote error"
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/resources/list": {
                "data": [
                    {
                        "remote": "pve-a",
                        "error": sentinel,
                        "resources": [
                            {
                                "id": "qemu/100",
                                "type": "pve-qemu",
                                "remote": "spoofed-remote",
                                "error": nested_error,
                                "remote_error": nested_remote_error,
                            }
                        ],
                    }
                ]
            }
        }
    )

    resources = await PDMClient(_sdk=sdk).resources.list()

    assert resources[0].id == "qemu/100"
    assert resources[0].remote == "pve-a"
    assert resources[0].remote_error == "remote reported an error"
    serialized = resources[0].model_dump()
    for rendered in (
        repr(resources[0]),
        repr(serialized),
        resources[0].model_dump_json(),
        repr(resources[0].model_extra),
    ):
        assert sentinel not in rendered
        assert nested_error not in rendered
        assert nested_remote_error not in rendered
        assert "spoofed-remote" not in rendered
    assert "error" not in serialized


async def test_successful_resource_envelope_clears_nested_error_context() -> None:
    nested_error = "nested do-not-leak error"
    nested_remote_error = "nested do-not-leak remote error"
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/resources/list": {
                "data": [
                    {
                        "remote": "pve-a",
                        "resources": [
                            {
                                "id": "qemu/100",
                                "type": "pve-qemu",
                                "error": nested_error,
                                "remote_error": nested_remote_error,
                            }
                        ],
                    }
                ]
            }
        }
    )

    resource = (await PDMClient(_sdk=sdk).resources.list())[0]

    assert resource.remote_error is None
    serialized = resource.model_dump()
    assert "error" not in serialized
    for rendered in (
        repr(resource),
        repr(serialized),
        resource.model_dump_json(),
        repr(resource.model_extra),
    ):
        assert nested_error not in rendered
        assert nested_remote_error not in rendered


async def test_pve_resource_read_clears_untrusted_nested_error_context() -> None:
    nested_error = "nested do-not-leak error"
    nested_remote_error = "nested do-not-leak remote error"
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/pve/remotes/pve-a/resources": {
                "data": [
                    {
                        "id": "qemu/100",
                        "type": "qemu",
                        "remote": "spoofed-remote",
                        "error": nested_error,
                        "remote_error": nested_remote_error,
                    }
                ]
            }
        }
    )

    resource = (await PDMClient(_sdk=sdk).pve.resources("pve-a"))[0]

    assert resource.remote == "pve-a"
    assert resource.remote_error is None
    serialized = resource.model_dump()
    assert "error" not in serialized
    for rendered in (
        repr(resource),
        repr(serialized),
        resource.model_dump_json(),
        repr(resource.model_extra),
    ):
        assert nested_error not in rendered
        assert nested_remote_error not in rendered
        assert "spoofed-remote" not in rendered


async def test_successful_error_models_never_retain_upstream_error_text() -> None:
    sentinel = "credential do-not-leak rejected"
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/resources/status": {
                "data": {
                    "remote": "pve-a",
                    "error": sentinel,
                    "resources": [{"id": "qemu/100", "type": "pve-qemu"}],
                }
            },
            "/api2/json/resources/subscription": {
                "data": [{"remote": "pve-a", "state": "unknown", "error": sentinel}]
            },
            "/api2/json/remotes/metric-collection/status": {
                "data": [{"remote": "pve-a", "error": sentinel}]
            },
        }
    )
    client = PDMClient(_sdk=sdk)

    status = await client.resources.status()
    subscription = (await client.subscriptions.list())[0]
    metric = (await client.metrics.status())[0]

    assert status.error == "remote reported an error"
    assert status.resources[0].remote_error == "remote reported an error"
    assert subscription.error == "remote reported an error"
    assert metric.error == "remote reported an error"
    for model in (status, subscription, metric):
        assert sentinel not in repr(model)
        assert sentinel not in model.model_dump_json()
        assert sentinel not in repr(model.model_extra)


async def test_shared_model_boundary_redacts_forward_compatible_error_fields() -> None:
    sentinel = "unexpected upstream credential do-not-leak"
    sdk, _ = make_pdm_sdk(
        {"/api2/json/remotes/remote": {"data": [{"id": "pve-a", "type": "pve", "error": sentinel}]}}
    )

    remote = (await PDMClient(_sdk=sdk).remotes.list())[0]

    assert remote.model_extra == {"error": "remote reported an error"}
    for rendered in (
        repr(remote),
        repr(remote.model_dump()),
        remote.model_dump_json(),
        repr(remote.model_extra),
    ):
        assert sentinel not in rendered


@pytest.mark.parametrize("resource_type", [None, "unknown", "qemu"])
async def test_global_resource_discriminator_is_required_and_closed(
    resource_type: str | None,
) -> None:
    resource: dict[str, Any] = {"id": "qemu/100"}
    if resource_type is not None:
        resource["type"] = resource_type
    sdk, _ = make_pdm_sdk(
        {"/api2/json/resources/list": {"data": [{"remote": "pve-a", "resources": [resource]}]}}
    )

    with pytest.raises(PDMResponseContractError) as exc_info:
        await PDMClient(_sdk=sdk).resources.list()

    assert "invalid fields: type" in str(exc_info.value)


@pytest.mark.parametrize(
    ("path", "call"),
    [
        ("/api2/json/version", lambda client: client.version()),
        (
            "/api2/json/remotes/remote/pve-a/version",
            lambda client: client.remotes.version("pve-a"),
        ),
    ],
)
async def test_version_reads_require_release_and_repoid(
    path: str,
    call: Callable[[PDMClient], Awaitable[Any]],
) -> None:
    sdk, _ = make_pdm_sdk({path: {"data": {"version": "1.0"}}})

    with pytest.raises(PDMResponseContractError) as exc_info:
        await call(PDMClient(_sdk=sdk))

    assert "release" in str(exc_info.value)
    assert "repoid" in str(exc_info.value)


async def test_pbs_task_status_requires_coherent_schema_fields() -> None:
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/pbs/remotes/pbs-a/tasks/UPID%3Apbs%3A1/status": {
                "data": {"upid": "UPID:pbs:1", "node": "pbs-a", "status": "stopped"}
            }
        }
    )

    with pytest.raises(PDMResponseContractError) as exc_info:
        await PDMClient(_sdk=sdk).pbs.task_status("pbs-a", "UPID:pbs:1")

    message = str(exc_info.value)
    assert "pid" in message
    assert "pstart" in message
    assert "starttime" in message
    assert "type" in message
    assert "user" in message


async def test_schema_samples_preserve_nontrivial_wire_values() -> None:
    """Guard aliases/coercions that previously failed or silently lost data."""

    client, _ = make_schema_client()
    try:
        qemu = (await client.pve.qemu.list("pve-a"))[0]
        lxc = (await client.pve.lxc.list("pve-a"))[0]
        qemu_config = await client.pve.qemu.config("pve-a", 100)
        pbs_datastore = (await client.pbs.datastores("pbs-a"))[0]
        resources = await client.resources.list()
        resource_status = await client.resources.status()
        subscription = (await client.subscriptions.list())[0]
        metric_status = (await client.metrics.status())[0]
        acl = (await client.access.acl.list())[0]
        token = (await client.access.tokens.list("alice@pdm"))[0]
        view = (await client.views.list())[0]
        rrd = (await client.pve.node_rrddata("pve-a", "node-a"))[0]
        datastore_rrd = (await client.pbs.datastore_rrddata("pbs-a", "tank"))[0]
    finally:
        await client.close()

    assert isinstance(qemu.cpus, float) and not qemu.cpus.is_integer()
    assert isinstance(lxc.cpus, float) and not lxc.cpus.is_integer()
    assert isinstance(qemu_config.memory, str)
    assert pbs_datastore.store
    assert resources and all(resource.remote for resource in resources)
    assert resource_status.remote and resource_status.resources
    assert subscription.state in {"none", "unknown", "mixed", "active"}
    assert metric_status.remote
    assert acl.type in {"user", "group"}
    assert token.token_name
    assert isinstance(view.include_all, bool)
    assert rrd.cpu is not None
    assert datastore_rrd.disk_used is not None
    assert datastore_rrd.disk_available is not None
