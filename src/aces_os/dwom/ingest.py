"""Observation → DWOM ingestion (deterministic, fail-closed)."""

from __future__ import annotations

import hashlib
from typing import Optional

from aces_os.connector.observation import Observation, ObservationState, PartialState

from .model import (
    DWOMObject,
    DeletionState,
    DWOMStatus,
    ExistenceState,
)
from .store import InMemoryDWOMStore


class IngestError(ValueError):
    pass


class IngestConflictError(IngestError):
    """same observation_id + different payload_digest."""


def _correlation_key(obs: Observation) -> str:
    ref = obs.resource_ref
    return f"{ref.provider}|{ref.resource_kind}|{ref.resource_id}|{ref.scope.namespace}"


def _dwom_object_id(obs: Observation) -> str:
    """Deterministic id from provider-native identity + observation digest."""
    key = f"{_correlation_key(obs)}|{obs.payload_digest}"
    return "dwom:" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]


def _map_existence(state: ObservationState) -> ExistenceState:
    if state == ObservationState.KNOWN:
        return ExistenceState.PRESENT
    if state == ObservationState.ABSENT:
        return ExistenceState.ABSENT
    if state == ObservationState.NOT_OBSERVABLE:
        return ExistenceState.NOT_OBSERVABLE
    if state == ObservationState.PARTIAL:
        return ExistenceState.PRESENT  # exists but incomplete
    return ExistenceState.UNKNOWN


def _map_deletion(payload: dict, state: ObservationState) -> DeletionState:
    # Never infer deletion from mere absence without explicit tombstone
    if state == ObservationState.ABSENT:
        return DeletionState.UNKNOWN
    flag = str(payload.get("deletion_state") or payload.get("condition") or "").lower()
    if flag in ("deleted", "delete"):
        return DeletionState.DELETED
    if flag in ("trashed", "trash"):
        return DeletionState.TRASHED
    if state == ObservationState.KNOWN:
        return DeletionState.NOT_DELETED
    return DeletionState.UNKNOWN


def _map_status(obs: Observation) -> DWOMStatus:
    if obs.pvr_flags:
        return DWOMStatus.PARTIAL
    mapping = {
        ObservationState.KNOWN: DWOMStatus.KNOWN,
        ObservationState.UNKNOWN: DWOMStatus.UNKNOWN,
        ObservationState.PARTIAL: DWOMStatus.PARTIAL,
        ObservationState.NOT_OBSERVABLE: DWOMStatus.NOT_OBSERVABLE,
        ObservationState.ABSENT: DWOMStatus.ABSENT,
    }
    return mapping.get(obs.observed_state, DWOMStatus.UNKNOWN)


def _version(obs: Observation) -> Optional[str]:
    ref = obs.resource_ref
    if ref.revision:
        return ref.revision
    p = obs.observed_payload
    for k in ("sha", "revisionId", "revision", "version", "content_hash"):
        if p.get(k):
            return str(p[k])
    return None


class DWOMIngestor:
    """ingest(observation) -> DWOMObject. No Evidence / AcceptedState / authority."""

    def __init__(self, store: Optional[InMemoryDWOMStore] = None) -> None:
        self.store = store or InMemoryDWOMStore()

    def ingest(self, observation: Observation) -> DWOMObject:
        self._validate(observation)

        existing_digest = self.store.observation_digest(observation.observation_id)
        if existing_digest is not None:
            if existing_digest != observation.payload_digest:
                raise IngestConflictError(
                    f"observation_id={observation.observation_id} payload_digest mismatch"
                )
            # Idempotent: return existing
            existing = self.store.get_by_observation(observation.observation_id)
            if existing is not None:
                return existing

        obj = DWOMObject(
            dwom_object_id=_dwom_object_id(observation),
            provider=observation.provider,
            resource_ref=observation.resource_ref,
            resource_kind=observation.resource_ref.resource_kind,
            scope_namespace=observation.resource_ref.scope.namespace,
            observed_state=observation.observed_state,
            existence_state=_map_existence(observation.observed_state),
            deletion_state=_map_deletion(observation.observed_payload, observation.observed_state),
            partial_state=observation.partial_state,
            version_or_revision=_version(observation),
            observed_at=observation.observed_at,
            source_timestamp=observation.source_timestamp,
            provider_event_time=observation.provider_event_time,
            observation_id=observation.observation_id,
            request_id=observation.request_id,
            payload_digest=observation.payload_digest,
            connector_id=observation.provenance.connector_id,
            configuration_scope=observation.provenance.configuration_scope,
            status=_map_status(observation),
            payload=dict(observation.observed_payload),
            pvr_flags=tuple(observation.pvr_flags),
            correlation_key=_correlation_key(observation),
            authenticity_crypto="DEFERRED",
        )
        self.store.put(obj)
        return obj

    def _validate(self, obs: Observation) -> None:
        if not obs.observation_id:
            raise IngestError("missing observation_id")
        if not obs.request_id:
            raise IngestError("missing request_id")
        if not obs.payload_digest:
            raise IngestError("missing payload_digest")
        if not obs.provider:
            raise IngestError("missing provider")
        if obs.resource_ref is None:
            raise IngestError("missing resource_ref")
        if not obs.provenance or not obs.provenance.connector_id:
            raise IngestError("missing provenance.connector_id")
        if obs.provider != obs.resource_ref.provider:
            raise IngestError("provider / resource_ref.provider mismatch")

    # Explicit non-capabilities
    def create_evidence(self, *a, **k):
        raise IngestError("DWOM cannot create Evidence")

    def create_accepted_state(self, *a, **k):
        raise IngestError("DWOM cannot create AcceptedState")

    def mutate_knowledge(self, *a, **k):
        raise IngestError("DWOM cannot mutate Knowledge")

    def mutate_memory(self, *a, **k):
        raise IngestError("DWOM cannot mutate Memory")

    def mutate_world_model(self, *a, **k):
        raise IngestError("DWOM cannot mutate World Model")

    def mutate_semantic_reality(self, *a, **k):
        raise IngestError("DWOM cannot mutate Semantic Reality")

    def issue_authorization(self, *a, **k):
        raise IngestError("DWOM cannot issue authorization")

    def bypass_asa(self, *a, **k):
        raise IngestError("DWOM cannot bypass ASA")

    def resolve_conflict(self, *a, **k):
        raise IngestError("DWOM does not select reconciliation winners")
