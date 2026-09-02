"""Gmail read-only — message_id ≠ thread_id ≠ RFC Message-ID."""

from __future__ import annotations

from typing import Iterable, Sequence

from aces_os.connector.base import ReadOnlyConnector, ConnectorError
from aces_os.connector.capability import Capability
from aces_os.connector.identity import ConnectorIdentity
from aces_os.connector.observation import Observation, ObservationState, PartialState
from aces_os.connector.resource import ResourceRef

from . import fixtures
from ._common import default_scope, make_observation


class GmailReadOnlyAdapter(ReadOnlyConnector):
    def __init__(self) -> None:
        super().__init__(
            ConnectorIdentity(
                connector_id="aces.connector.gmail.readonly.v1",
                provider="gmail",
                connector_version="0.1.0",
                configuration_scope="fixture",
            )
        )
        self._data = fixtures.GMAIL_FIXTURES

    def supported_capabilities(self) -> Sequence[Capability]:
        return (
            Capability.READ_RESOURCE,
            Capability.OBSERVE_RESOURCE,
            Capability.LIST_RESOURCE,
            Capability.READ_METADATA,
        )

    def read_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        if ref.provider != "gmail":
            raise ConnectorError("provider mismatch")
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
        # Explicit identity separation
        if ref.resource_kind == "message":
            assert payload["id"] != payload["threadId"]
            assert payload["id"] != payload["rfcMessageId"]
        src_ts = payload.get("internalDate")
        return make_observation(
            identity=self.identity,
            ref=ref,
            request_id=request_id,
            payload=payload,
            source_timestamp=str(src_ts) if src_ts else None,
        )

    def list_resources(self, kind: str, request_id: str) -> Iterable[Observation]:
        raw = self._data.get(kind)
        if not raw:
            return []
        ref = ResourceRef(
            provider="gmail",
            resource_kind=kind,
            resource_id=str(raw["id"]),
            scope=default_scope("gmail"),
        )
        return [self.read_resource(ref, request_id)]

    def observe_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        return self.read_resource(ref, request_id)
