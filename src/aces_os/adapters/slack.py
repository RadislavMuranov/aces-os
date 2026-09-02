"""Slack read-only — channel+ts identity; SL-RET PVR guarded."""

from __future__ import annotations

from typing import Iterable, Sequence

from aces_os.connector.base import ReadOnlyConnector, ConnectorError
from aces_os.connector.capability import Capability
from aces_os.connector.identity import ConnectorIdentity
from aces_os.connector.observation import Observation, ObservationState, PartialState
from aces_os.connector.resource import ResourceRef

from . import fixtures
from ._common import default_scope, make_observation


class SlackReadOnlyAdapter(ReadOnlyConnector):
    def __init__(self) -> None:
        super().__init__(
            ConnectorIdentity(
                connector_id="aces.connector.slack.readonly.v1",
                provider="slack",
                connector_version="0.1.0",
                configuration_scope="fixture",
            )
        )
        self._data = fixtures.SLACK_FIXTURES

    def supported_capabilities(self) -> Sequence[Capability]:
        return (
            Capability.READ_RESOURCE,
            Capability.OBSERVE_RESOURCE,
            Capability.LIST_RESOURCE,
            Capability.READ_METADATA,
        )

    def read_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        if ref.provider != "slack":
            raise ConnectorError("provider mismatch")
        if ref.resource_kind == "history_complete":
            # SL-RET: do not claim complete retention history
            return make_observation(
                identity=self.identity,
                ref=ref,
                request_id=request_id,
                payload={"pvr": "SL-RET", "note": "retention completeness not verified"},
                observed_state=ObservationState.PARTIAL,
                partial_state=PartialState.PARTIAL,
                pvr_flags=("SL-RET",),
            )
        raw = self._data.get(ref.resource_kind)
        if raw is None:
            # Absence ≠ deletion without tombstone
            return make_observation(
                identity=self.identity,
                ref=ref,
                request_id=request_id,
                payload={"visibility": "NOT_OBSERVABLE"},
                observed_state=ObservationState.NOT_OBSERVABLE,
                partial_state=PartialState.UNKNOWN,
            )
        payload = dict(raw)
        if ref.resource_kind == "message":
            payload["identity"] = f"{payload['channel_id']}:{payload['ts']}"
        return make_observation(
            identity=self.identity,
            ref=ref,
            request_id=request_id,
            payload=payload,
            source_timestamp=payload.get("ts"),
        )

    def list_resources(self, kind: str, request_id: str) -> Iterable[Observation]:
        raw = self._data.get(kind)
        if not raw:
            return []
        rid = f"{raw.get('channel_id')}:{raw.get('ts') or raw.get('thread_ts')}"
        ref = ResourceRef(
            provider="slack",
            resource_kind=kind,
            resource_id=rid,
            scope=default_scope("slack"),
        )
        return [self.read_resource(ref, request_id)]

    def observe_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        return self.read_resource(ref, request_id)
