"""EvidenceCandidate creation and Evidence Admission — structural only."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Optional

from aces_os.connector.observation import Observation, ObservationState
from aces_os.dwom.model import DWOMObject

from .model import (
    CandidateStatus,
    Evidence,
    EvidenceCandidate,
    EvidenceStatus,
)
from .store import InMemoryEvidenceStore


class AdmissionError(ValueError):
    pass


class AdmissionConflictError(AdmissionError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _candidate_id(obs: Observation, dwom_object_id: str) -> str:
    raw = f"{obs.observation_id}|{dwom_object_id}|{obs.payload_digest}"
    return "cand:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _evidence_id(candidate_id: str, payload_digest: str) -> str:
    raw = f"{candidate_id}|{payload_digest}"
    return "ev:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


def _admission_id(candidate_id: str, admitted_at: str) -> str:
    raw = f"{candidate_id}|{admitted_at}"
    return "adm:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


class EvidenceAdmissionService:
    """create_candidate / admit / get_evidence — stops at Evidence."""

    ADMISSION_RULE = "structural_v1:provenance+binding+digest+no_replay_conflict"

    def __init__(self, store: Optional[InMemoryEvidenceStore] = None) -> None:
        self.store = store or InMemoryEvidenceStore()

    def create_candidate(
        self, observation: Observation, dwom: DWOMObject
    ) -> EvidenceCandidate:
        self._validate_pair(observation, dwom)

        reason = "structural_ok"
        status = CandidateStatus.ELIGIBLE

        if observation.pvr_flags or dwom.pvr_flags:
            reason = "structural_ok_with_pvr_guard"

        if observation.observed_state in (
            ObservationState.UNKNOWN,
            ObservationState.NOT_OBSERVABLE,
        ):
            status = CandidateStatus.CANDIDATE
            reason = f"state={observation.observed_state.value};admit_may_reject"

        cand = EvidenceCandidate(
            candidate_id=_candidate_id(observation, dwom.dwom_object_id),
            observation_id=observation.observation_id,
            dwom_object_id=dwom.dwom_object_id,
            provider=observation.provider,
            resource_ref=observation.resource_ref,
            resource_kind=observation.resource_ref.resource_kind,
            scope_namespace=observation.resource_ref.scope.namespace,
            observed_state=observation.observed_state,
            partial_state=observation.partial_state,
            observed_at=observation.observed_at,
            source_timestamp=observation.source_timestamp,
            provider_event_time=observation.provider_event_time,
            version_or_revision=dwom.version_or_revision,
            connector_id=observation.provenance.connector_id,
            configuration_scope=observation.provenance.configuration_scope,
            request_id=observation.request_id,
            payload_digest=observation.payload_digest,
            candidate_status=status,
            eligibility_reason=reason,
            payload=dict(observation.observed_payload),
            pvr_flags=tuple(observation.pvr_flags or dwom.pvr_flags),
            authenticity_crypto="DEFERRED",
        )
        self.store.put_candidate(cand)
        return cand

    def admit(self, candidate: EvidenceCandidate) -> Evidence:
        self._validate_candidate_for_admission(candidate)

        od = self.store.observation_digest(candidate.observation_id)
        if od is not None and od != candidate.payload_digest:
            raise AdmissionConflictError(
                f"observation_id={candidate.observation_id} digest conflict"
            )

        existing = self.store.get_by_candidate(candidate.candidate_id)
        if existing is not None:
            if existing.payload_digest != candidate.payload_digest:
                raise AdmissionConflictError(
                    f"candidate_id={candidate.candidate_id} payload_digest mismatch"
                )
            return existing

        existing_obs = self.store.get_by_observation(candidate.observation_id)
        if existing_obs is not None:
            if existing_obs.payload_digest != candidate.payload_digest:
                raise AdmissionConflictError(
                    "observation already admitted with different digest"
                )
            return existing_obs

        if candidate.observed_state in (
            ObservationState.UNKNOWN,
            ObservationState.NOT_OBSERVABLE,
        ):
            raise AdmissionError(
                f"INELIGIBLE: observed_state={candidate.observed_state.value}"
            )

        admitted_at = _utc_now()
        evidence = Evidence(
            evidence_id=_evidence_id(candidate.candidate_id, candidate.payload_digest),
            candidate_id=candidate.candidate_id,
            observation_id=candidate.observation_id,
            dwom_object_id=candidate.dwom_object_id,
            provider=candidate.provider,
            resource_ref=candidate.resource_ref,
            resource_kind=candidate.resource_kind,
            scope_namespace=candidate.scope_namespace,
            observed_state=candidate.observed_state,
            partial_state=candidate.partial_state,
            connector_id=candidate.connector_id,
            configuration_scope=candidate.configuration_scope,
            observed_at=candidate.observed_at,
            source_timestamp=candidate.source_timestamp,
            provider_event_time=candidate.provider_event_time,
            version_or_revision=candidate.version_or_revision,
            request_id=candidate.request_id,
            payload_digest=candidate.payload_digest,
            admission_id=_admission_id(candidate.candidate_id, admitted_at),
            admitted_at=admitted_at,
            admission_rule=self.ADMISSION_RULE,
            status=EvidenceStatus.ADMITTED,
            payload=dict(candidate.payload),
            pvr_flags=tuple(candidate.pvr_flags),
            authenticity_crypto="DEFERRED",
        )
        self.store.put_evidence(evidence)
        return evidence

    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        return self.store.get_evidence(evidence_id)

    def _validate_pair(self, obs: Observation, dwom: DWOMObject) -> None:
        if not obs.observation_id:
            raise AdmissionError("missing observation_id")
        if not obs.payload_digest:
            raise AdmissionError("missing payload_digest")
        if not obs.provenance or not obs.provenance.connector_id:
            raise AdmissionError("missing provenance")
        if not dwom.dwom_object_id:
            raise AdmissionError("missing dwom_object_id")
        if obs.observation_id != dwom.observation_id:
            raise AdmissionError("observation_id mismatch with DWOM")
        if obs.provider != dwom.provider:
            raise AdmissionError("provider mismatch")
        if obs.resource_ref.resource_id != dwom.resource_ref.resource_id:
            raise AdmissionError("resource_id mismatch")
        if obs.resource_ref.scope.namespace != dwom.scope_namespace:
            raise AdmissionError("scope mismatch")
        if obs.payload_digest != dwom.payload_digest:
            raise AdmissionError("payload_digest mismatch")

    def _validate_candidate_for_admission(self, c: EvidenceCandidate) -> None:
        if not c.candidate_id or not c.observation_id or not c.dwom_object_id:
            raise AdmissionError("incomplete candidate identity")
        if not c.connector_id or not c.payload_digest or not c.request_id:
            raise AdmissionError("incomplete provenance/binding")
        if not c.provider or c.resource_ref is None:
            raise AdmissionError("incomplete resource binding")
        if c.provider != c.resource_ref.provider:
            raise AdmissionError("provider/resource_ref mismatch")

    def verify(self, *a, **k):
        raise AdmissionError("Phase IV does not implement Verification")

    def accept(self, *a, **k):
        raise AdmissionError("Phase IV does not create AcceptedState")

    def promote_to_knowledge(self, *a, **k):
        raise AdmissionError("Evidence cannot promote Knowledge")

    def authorize(self, *a, **k):
        raise AdmissionError("Evidence ≠ Authority")

    def execute(self, *a, **k):
        raise AdmissionError("Evidence cannot execute")

    def resolve_truth(self, *a, **k):
        raise AdmissionError("Evidence is not Truth")

    def issue_authorization(self, *a, **k):
        raise AdmissionError("Evidence cannot issue AuthorizationRecord")

    def bypass_asa(self, *a, **k):
        raise AdmissionError("Evidence cannot bypass ASA")

    def mutate_semantic_reality(self, *a, **k):
        raise AdmissionError("Evidence cannot mutate Semantic Reality")

    def write_provider(self, *a, **k):
        raise AdmissionError("Evidence cannot write to providers")
