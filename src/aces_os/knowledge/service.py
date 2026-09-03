"""KnowledgePromotionService — only ESTABLISHED AcceptedState promotes Knowledge."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from aces_os.evidence.model import Evidence
from aces_os.verification.model import (
    AcceptedState,
    AcceptedStateStatus,
    VerificationResult,
    VerificationStatus,
)

from .model import (
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgeProvenance,
    KnowledgeStatus,
    KnowledgeUpdateRequest,
    TruthLevel,
    knowledge_identity_key,
)
from .store import InMemoryKnowledgeStore


class KnowledgeError(ValueError):
    pass


class KnowledgeConflictError(KnowledgeError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id(prefix: str, *parts: str) -> str:
    raw = "|".join(parts)
    return f"{prefix}:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


class KnowledgePromotionService:
    """Promote Knowledge only from validated ESTABLISHED AcceptedState."""

    def __init__(self, store: Optional[InMemoryKnowledgeStore] = None) -> None:
        self.store = store or InMemoryKnowledgeStore()

    def promote(
        self,
        accepted_state: AcceptedState,
        verification_result: VerificationResult,
        evidence: Evidence,
        object_type: KnowledgeObjectType,
        truth_level: TruthLevel,
        semantic_payload: Dict[str, Any],
        semantic_identity: str,
        request_id: str,
    ) -> KnowledgeObject:
        self._validate_authority(accepted_state, verification_result, evidence)

        if truth_level == TruthLevel.CANONICAL:
            raise KnowledgeError(
                "Canonical truth cannot be established implicitly; requires separate authority"
            )

        if not semantic_identity:
            raise KnowledgeError("missing semantic_identity")

        kid = _id(
            "ko",
            accepted_state.accepted_state_id,
            evidence.payload_digest,
            object_type.value,
            semantic_identity,
        )

        existing = self.store.get_by_identity(
            accepted_state.accepted_state_id,
            evidence.payload_digest,
            object_type.value,
            semantic_identity,
        )
        if existing is not None:
            if existing.semantic_payload != semantic_payload:
                raise KnowledgeConflictError("semantic_payload conflict for same identity")
            if existing.truth_level != truth_level:
                raise KnowledgeConflictError("truth_level conflict for same identity")
            return existing

        prov = KnowledgeProvenance(
            accepted_state_id=accepted_state.accepted_state_id,
            verification_result_id=verification_result.verification_result_id,
            verifier_id=accepted_state.verifier_id,
            verifier_version=accepted_state.verifier_version,
            policy_id=accepted_state.policy_id,
            policy_version=accepted_state.policy_version,
            evidence_id=evidence.evidence_id,
            evidence_digest=evidence.payload_digest,
            observation_id=evidence.observation_id,
            candidate_id=evidence.candidate_id,
            dwom_object_id=evidence.dwom_object_id,
            provider=evidence.provider,
            resource_kind=evidence.resource_kind,
            connector_id=evidence.connector_id,
            authenticity_crypto="DEFERRED",
        )

        obj = KnowledgeObject(
            knowledge_object_id=kid,
            object_type=object_type,
            truth_level=truth_level,
            semantic_payload=dict(semantic_payload),
            semantic_identity=semantic_identity,
            source_evidence_id=evidence.evidence_id,
            evidence_digest=evidence.payload_digest,
            accepted_state_id=accepted_state.accepted_state_id,
            verification_result_id=verification_result.verification_result_id,
            provenance=prov,
            status=KnowledgeStatus.ACTIVE,
            created_at=_utc_now(),
        )
        self.store.put(obj)
        return obj

    def _validate_authority(
        self,
        accepted_state: AcceptedState,
        verification_result: VerificationResult,
        evidence: Evidence,
    ) -> None:
        if accepted_state is None:
            raise KnowledgeError("missing AcceptedState")
        if accepted_state.status != AcceptedStateStatus.ESTABLISHED:
            raise KnowledgeError("AcceptedState not ESTABLISHED")
        if verification_result is None:
            raise KnowledgeError("missing VerificationResult")
        if verification_result.status != VerificationStatus.PASSED:
            raise KnowledgeError("VerificationResult not PASSED")
        if evidence is None:
            raise KnowledgeError("missing Evidence")

        # Exact AcceptedState ↔ VerificationResult binding
        if accepted_state.verification_result_id != verification_result.verification_result_id:
            raise KnowledgeError("verification_result_id mismatch")
        if accepted_state.evidence_id != verification_result.evidence_id:
            raise KnowledgeError("evidence_id mismatch on result")
        if accepted_state.evidence_digest != verification_result.evidence_digest:
            raise KnowledgeError("evidence_digest mismatch on result")
        if accepted_state.policy_id != verification_result.policy_id:
            raise KnowledgeError("policy_id mismatch")
        if accepted_state.policy_version != verification_result.policy_version:
            raise KnowledgeError("policy_version mismatch")
        if accepted_state.verifier_id != verification_result.verifier_id:
            raise KnowledgeError("verifier_id mismatch")
        if accepted_state.verifier_version != verification_result.verifier_version:
            raise KnowledgeError("verifier_version mismatch")

        # Exact AcceptedState ↔ Evidence binding
        if accepted_state.evidence_id != evidence.evidence_id:
            raise KnowledgeError("evidence_id mismatch")
        if accepted_state.evidence_digest != evidence.payload_digest:
            raise KnowledgeError("evidence_digest mismatch")

        # No bare-token path: require concrete IDs
        for label, val in (
            ("accepted_state_id", accepted_state.accepted_state_id),
            ("verification_result_id", accepted_state.verification_result_id),
            ("evidence_id", evidence.evidence_id),
            ("evidence_digest", evidence.payload_digest),
        ):
            if not val:
                raise KnowledgeError(f"missing {label}")

    # Explicit non-capabilities
    def promote_from_boolean(self, *a, **k):
        raise KnowledgeError("bare verified/passed boolean cannot promote Knowledge")

    def create_accepted_state(self, *a, **k):
        raise KnowledgeError("Knowledge cannot establish AcceptedState")

    def perform_verification(self, *a, **k):
        raise KnowledgeError("Knowledge cannot perform verification")

    def mutate_memory(self, *a, **k):
        raise KnowledgeError("Knowledge cannot mutate Memory")

    def mutate_world_model(self, *a, **k):
        raise KnowledgeError("Knowledge cannot mutate World Model")

    def mutate_semantic_reality(self, *a, **k):
        raise KnowledgeError("Knowledge cannot mutate Semantic Reality")

    def authorize_execution(self, *a, **k):
        raise KnowledgeError("Knowledge cannot authorize execution")

    def issue_capability(self, *a, **k):
        raise KnowledgeError("Knowledge cannot issue capabilities")

    def bypass_asa(self, *a, **k):
        raise KnowledgeError("Knowledge cannot bypass ASA")

    def write_provider(self, *a, **k):
        raise KnowledgeError("Knowledge cannot write providers")

    def invoke_mcp(self, *a, **k):
        raise KnowledgeError("Knowledge cannot invoke MCP side effects")

    def promote_canonical(self, *a, **k):
        raise KnowledgeError("Canonical truth requires separate authority; not Phase VI")
