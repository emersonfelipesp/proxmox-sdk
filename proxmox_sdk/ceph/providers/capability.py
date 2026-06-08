"""Provider capability descriptor shared by direct Ceph provider clients.

Higher layers (``proxbox-api``) ask a provider *whether* it supports a desired
operation before planning it.  Each client exposes an async ``capabilities()``
returning a :class:`ProviderCapability`, which the orchestration layer maps onto
its own capability map.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ProviderCapability(BaseModel):
    """What a direct Ceph provider can do for a given cluster.

    ``operations`` is a flat map of ``"{kind}:{action}"`` (and bare ``"{kind}"``
    / ``"{action}"``) keys to booleans, matching the lookup order used by the
    ``proxbox-api`` plan engine.  Unknown keys default to ``False`` so a missing
    entry reads as "unsupported", never as an unsafe fallback.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    provider: str
    available: bool = False
    version: str | None = None
    read: bool = False
    write: bool = False
    metrics: bool = False
    operations: dict[str, bool] = Field(default_factory=dict)
    notes: list[str] = Field(default_factory=list)

    def supports(self, kind: str, action: str | None = None) -> bool:
        """Return whether ``{kind}/{action}`` is supported by this provider."""

        if not self.available:
            return False
        candidates = []
        if action:
            candidates.append(f"{kind}:{action}")
            candidates.append(f"{kind}:*")
            candidates.append(action)
        candidates.append(kind)
        for key in candidates:
            if key in self.operations:
                return self.operations[key]
        # No explicit ``operations`` entry. Reads are non-destructive, so a
        # provider that advertises ``read`` may answer read queries True. Writes
        # must be enumerated explicitly: an unknown write-like action is reported
        # as unsupported so the gate never fails open on a destructive op.
        if action and action not in {"get", "list", "read"}:
            return False
        return self.read
