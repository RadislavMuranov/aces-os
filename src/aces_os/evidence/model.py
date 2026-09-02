"""EvidenceCandidate and Evidence — structural only, not truth."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional, Tuple

from aces_os.connector.observation import ObservationState, PartialState
from aces_os.connector.resource import ResourceRef


class CandidateStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    ELIGIBLE = "ELIGIBLE"
    INELIGIBLE = "INELIGIBLE"
    REJECTED = "REJECTED"
    ADMITTED = "ADMITTED"
    CONFLICT = "CONFLICT"
    UNKNOWN = "UNKNOWN"


class EvidenceStatus(str, Enum):
    ADMITTED = "ADMITTED"
    CONFLICT = "CONFLICT"
    SUPERSEDED = "SUPERSEDED"


@dataclass(frozen=True)
class EvidenceCandidate:
    candidate_id: str
    observation_id: str
    dwom_object_id: str
    provider: str
    resource_ref: ResourceRef
    resource_kind: str
    scope_namespace: str
    observed_state: ObservationState
    partial_state: PartialState
    observed_at: str
    source_timestamp: Optional[str]
    provider_event_time: Optional[str]
    version_or_revision: Optional[str]
    connector_id: str
    configuration_scope: str
    request_id: str
    payload_digest: str
    candidate_status: CandidateStatus
    eligibility_reason: str
    payload: Dict[str, Any] = field(default_factory=dict)
    pvr_flags: Tuple[str, ...] = ()
    authenticity_crypto: str = "DEFERRED"

    def is_evidence(self) -> bool:
        return False

    def is_admitted(self) -> bool:
        return self.candidate_status == CandidateStatus.ADMITTED


@dataclass(frozen=True)
class Evidence:
    """Admitted structural evidence — NOT verified truth / AcceptedState."""

    evidence_id: str
    candidate_id: str
    observation_id: str
    dwom_object_id: str
    provider: str
    resource_ref: ResourceRef
    resource_kind: str
    scope_namespace: str
    observed_state: ObservationState
    partial_state: PartialState
    connector_id: str
    configuration_scope: str
    observed_at: str
    source_timestamp: Optional[str]
    provider_event_time: Optional[str]
    version_or_revision: Optional[str]
    request_id: str
    payload_digest: str
    admission_id: str
    admitted_at: str
    admission_rule: str
    status: EvidenceStatus
    payload: Dict[str, Any] = field(default_factory=dict)
    pvr_flags: Tuple[str, ...] = ()
    authenticity_crypto: str = "DEFERRED"

    def is_verification(self) -> bool:
        return False

    def is_accepted_state(self) -> bool:
        return False

    def is_knowledge(self) -> bool:
        return False

    def is_truth(self) -> bool:
        return False

    def is_semantic_reality(self) -> bool:
        return False
