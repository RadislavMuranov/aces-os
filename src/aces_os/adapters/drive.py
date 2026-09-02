"""Google Drive read-only — fileId ≠ path; shared-drive PVR guarded."""

from __future__ import annotations

from typing import Iterable, Sequence

from aces_os.connector.base import ReadOnlyConnector, ConnectorError
from aces_os.connector.capability import Capability
from aces_os.connector.identity import ConnectorIdentity
from aces_os.connector.observation import Observation, ObservationState, PartialState
from aces_os.connector.resource import ResourceRef

from . import fixtures
from ._common import default_scope, make_observation


class GoogleDriveReadOnlyAdapter(ReadOnlyConnector):
    def __init__(self) -> None:
        super().__init__(
            ConnectorIdentity(
                connector_id="aces.connector.google_drive.readonly.v1",
                provider="google_drive",
                connector_version="0.1.0",
                configuration_scope="fixture-my-drive",
            )
        )
        self._data = fixtures.DRIVE_FIXTURES

    def supported_capabilities(self) -> Sequence[Capability]:
        return (
            Capability.READ_RESOURCE,
            Capability.OBSERVE_RESOURCE,
            Capability.LIST_RESOURCE,
            Capability.READ_METADATA,
        )

    def read_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        if ref.provider != "google_drive":
            raise ConnectorError("provider mismatch")
        # Shared-drive PVR: block or mark partial
        if ref.scope.namespace == "shared_drive":
            return make_observation(
                identity=self.identity,
                ref=ref,
                request_id=request_id,
                payload={"pvr": "GD-SD", "note": "shared-drive semantics not verified live"},
                observed_state=ObservationState.PARTIAL,
                partial_state=PartialState.PARTIAL,
                pvr_flags=("GD-SD",),
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
        assert payload["fileId"] != payload.get("path")
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
            provider="google_drive",
            resource_kind=kind,
            resource_id=raw["fileId"],
            scope=default_scope("google_drive"),
            path=raw.get("path"),
            revision=raw.get("revisionId"),
        )
        return [self.read_resource(ref, request_id)]

    def observe_resource(self, ref: ResourceRef, request_id: str) -> Observation:
        return self.read_resource(ref, request_id)
