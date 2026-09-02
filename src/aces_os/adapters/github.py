"""GitHub read-only adapter — branch ≠ commit; fixture-backed."""

from __future__ import annotations

from typing import Iterable, Sequence

from aces_os.connector.base import ReadOnlyConnector, ConnectorError
from aces_os.connector.capability import Capability
from aces_os.connector.identity import ConnectorIdentity
from aces_os.connector.observation import Observation, ObservationState, PartialState
from aces_os.connector.resource import ResourceRef

from . import fixtures
from ._common import default_scope, make_observation


class GitHubReadOnlyAdapter(ReadOnlyConnector):
    """Native path: REST/git semantics via fixtures. MCP not required."""

    def __init__(self) -> None:
        super().__init__(
            ConnectorIdentity(
                connector_id="aces.connector.github.readonly.v1",
                provider="github",
                connector_version="0.1.0",
                configuration_scope="fixture",
            )
        )
        self._data = fixtures.GITHUB_FIXTURES

    def supported_capabilities(self) -> Sequence[Capability]:
        return (
            Capability.READ_RESOURCE,
            Capability.OBSERVE_RESOURCE,
            Capability.LIST_RESOURCE,
            Capability.READ_METADATA,
        )

    def read_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        if ref.provider != "github":
            raise ConnectorError("provider mismatch")
        raw = self._data.get(ref.resource_kind)
        if raw is None or raw.get("kind") != ref.resource_kind:
            return make_observation(
                identity=self.identity,
                ref=ref,
                request_id=request_id,
                payload={"error": "not_found"},
                observed_state=ObservationState.ABSENT,
                partial_state=PartialState.UNKNOWN,
            )
        # Preserve branch ≠ commit
        payload = dict(raw)
        if ref.resource_kind == "branch":
            payload["identity_note"] = "mutable_ref_not_commit"
        if ref.resource_kind == "commit":
            payload["identity_note"] = "immutable_sha"
        return make_observation(
            identity=self.identity,
            ref=ref,
            request_id=request_id,
            payload=payload,
            source_timestamp=None,
        )

    def list_resources(self, kind: str, request_id: str) -> Iterable[Observation]:
        raw = self._data.get(kind)
        if not raw:
            return []
        ref = ResourceRef(
            provider="github",
            resource_kind=kind,
            resource_id=str(raw.get("sha") or raw.get("name") or raw.get("id")),
            scope=default_scope("github"),
        )
        return [self.read_resource(ref, request_id)]

    def observe_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        return self.read_resource(ref, request_id)
