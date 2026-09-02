"""Obsidian read-only local vault fixture — OBS-SYNC remains PVR."""

from __future__ import annotations

from typing import Iterable, Sequence

from aces_os.connector.base import ReadOnlyConnector, ConnectorError
from aces_os.connector.capability import Capability
from aces_os.connector.identity import ConnectorIdentity
from aces_os.connector.observation import Observation, ObservationState, PartialState
from aces_os.connector.resource import ResourceRef

from . import fixtures
from ._common import default_scope, make_observation


class ObsidianReadOnlyAdapter(ReadOnlyConnector):
    """Local path preferred. Sync multi-device not claimed."""

    def __init__(self) -> None:
        super().__init__(
            ConnectorIdentity(
                connector_id="aces.connector.obsidian.readonly.v1",
                provider="obsidian",
                connector_version="0.1.0",
                configuration_scope="local-fixture-vault",
            )
        )
        self._data = fixtures.OBSIDIAN_FIXTURES

    def supported_capabilities(self) -> Sequence[Capability]:
        return (
            Capability.READ_RESOURCE,
            Capability.OBSERVE_RESOURCE,
            Capability.LIST_RESOURCE,
            Capability.READ_METADATA,
        )

    def read_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        if ref.provider != "obsidian":
            raise ConnectorError("provider mismatch")
        if ref.resource_kind == "sync_state" or (ref.scope.namespace == "sync"):
            return make_observation(
                identity=self.identity,
                ref=ref,
                request_id=request_id,
                payload={"pvr": "OBS-SYNC", "note": "Sync identity not verified live"},
                observed_state=ObservationState.PARTIAL,
                partial_state=PartialState.PARTIAL,
                pvr_flags=("OBS-SYNC",),
            )
        raw = self._data.get(ref.resource_kind)
        if raw is None:
            return make_observation(
                identity=self.identity,
                ref=ref,
                request_id=request_id,
                payload={},
                observed_state=ObservationState.ABSENT,
                partial_state=PartialState.UNKNOWN,
            )
        payload = dict(raw)
        # path is label; content_hash is stronger correlator
        return make_observation(
            identity=self.identity,
            ref=ref,
            request_id=request_id,
            payload=payload,
        )

    def list_resources(self, kind: str, request_id: str) -> Iterable[Observation]:
        raw = self._data.get(kind)
        if not raw:
            return []
        ref = ResourceRef(
            provider="obsidian",
            resource_kind=kind,
            resource_id=raw["path"],
            scope=default_scope("obsidian"),
            path=raw["path"],
        )
        return [self.read_resource(ref, request_id)]

    def observe_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        return self.read_resource(ref, request_id)
