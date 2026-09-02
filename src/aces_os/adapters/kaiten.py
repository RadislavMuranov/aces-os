"""Kaiten read-only — poll/API fixtures; KT-WH webhook PVR guarded."""

from __future__ import annotations

from typing import Iterable, Sequence

from aces_os.connector.base import ReadOnlyConnector, ConnectorError
from aces_os.connector.capability import Capability
from aces_os.connector.identity import ConnectorIdentity
from aces_os.connector.observation import Observation, ObservationState, PartialState
from aces_os.connector.resource import ResourceRef

from . import fixtures
from ._common import default_scope, make_observation


class KaitenReadOnlyAdapter(ReadOnlyConnector):
    def __init__(self) -> None:
        super().__init__(
            ConnectorIdentity(
                connector_id="aces.connector.kaiten.readonly.v1",
                provider="kaiten",
                connector_version="0.1.0",
                configuration_scope="fixture",
            )
        )
        self._data = fixtures.KAITEN_FIXTURES

    def supported_capabilities(self) -> Sequence[Capability]:
        return (
            Capability.READ_RESOURCE,
            Capability.OBSERVE_RESOURCE,
            Capability.LIST_RESOURCE,
            Capability.READ_METADATA,
        )

    def read_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        if ref.provider != "kaiten":
            raise ConnectorError("provider mismatch")
        if ref.resource_kind == "webhook_event":
            return make_observation(
                identity=self.identity,
                ref=ref,
                request_id=request_id,
                payload={
                    "pvr": "KT-WH",
                    "note": "webhook delivery semantics not verified; poll preferred",
                },
                observed_state=ObservationState.PARTIAL,
                partial_state=PartialState.PARTIAL,
                pvr_flags=("KT-WH",),
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
        return make_observation(
            identity=self.identity,
            ref=ref,
            request_id=request_id,
            payload=dict(raw),
        )

    def list_resources(self, kind: str, request_id: str) -> Iterable[Observation]:
        raw = self._data.get(kind)
        if not raw:
            return []
        ref = ResourceRef(
            provider="kaiten",
            resource_kind=kind,
            resource_id=str(raw["id"]),
            scope=default_scope("kaiten"),
        )
        return [self.read_resource(ref, request_id)]

    def observe_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        return self.read_resource(ref, request_id)
