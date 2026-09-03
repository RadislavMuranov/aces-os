"""Knowledge models — epistemically downstream from AcceptedState."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class KnowledgeObjectType(str, Enum):
    FACT = "Fact"
    DECISION = "Decision"
    ARTIFACT = "Artifact"
    HYPOTHESIS = "Hypothesis"
    POLICY = "Policy"


class TruthLevel(str, Enum):
    WORKING = "Working"
    OPERATIONAL = "Operational"
    CANONICAL = "Canonical"


class KnowledgeStatus(str, Enum):
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    CONFLICT = "CONFLICT"


@dataclass(frozen=True)
class KnowledgeProvenance:
    """Explicit chain; not free-form text. Crypto remains DEFERRED."""

    accepted_state_id: str
    verification_result_id: str
    verifier_id: str
    verifier_version: str
    policy_id: str
    policy_version: str
    evidence_id: str
    evidence_digest: str
    observation_id: str
    candidate_id: str
    dwom_object_id: str
    provider: str
    resource_kind: str
    connector_id: str
    authenticity_crypto: str = "DEFERRED"


@dataclass(frozen=True)
class KnowledgeUpdateRequest:
    request_id: str
    accepted_state_id: str
    evidence_id: str
    evidence_digest: str
    knowledge_object_id: str
    object_type: KnowledgeObjectType
    truth_level: TruthLevel
    semantic_payload: Dict[str, Any]
    semantic_identity: str  # stable identity within object_type for idempotency


@dataclass(frozen=True)
class KnowledgeObject:
    knowledge_object_id: str
    object_type: KnowledgeObjectType
    truth_level: TruthLevel
    semantic_payload: Dict[str, Any]
    semantic_identity: str
    source_evidence_id: str
    evidence_digest: str
    accepted_state_id: str
    verification_result_id: str
    provenance: KnowledgeProvenance
    status: KnowledgeStatus
    created_at: str

    def is_truth(self) -> bool:
        return False

    def is_authority(self) -> bool:
        return False

    def is_authorization(self) -> bool:
        return False

    def is_accepted_state(self) -> bool:
        return False

    def is_memory(self) -> bool:
        return False

    def is_world_model(self) -> bool:
        return False

    def is_semantic_reality(self) -> bool:
        return False

    def is_canonical_truth(self) -> bool:
        # Explicit field may be Canonical level; does not imply Canon promotion authority
        return False


def knowledge_identity_key(
    accepted_state_id: str,
    evidence_digest: str,
    object_type: str,
    semantic_identity: str,
) -> str:
    """Deterministic Knowledge identity — not evidence_id alone."""
    return "|".join([accepted_state_id, evidence_digest, object_type, semantic_identity])
