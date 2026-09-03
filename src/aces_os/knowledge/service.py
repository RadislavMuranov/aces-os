"""KnowledgePromotionService — KnowledgeUpdateRequest is mandatory boundary."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Optional

from aces_os.evidence.model import Evidence
from aces_os.verification.model import (
    AcceptedState,
    AcceptedStateStatus,
    VerificationResult,
    VerificationStatus,
)

from .model import (
    KnowledgeObject,
    KnowledgeProvenance,
    KnowledgeStatus,
    KnowledgeUpdateRequest,
    TruthLevel,
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
    """Promote only via KnowledgeUpdateRequest + ESTABLISHED AcceptedState."""

    def __init__(self, store: Optional[InMemoryKnowledgeStore] = None) -> None:
        self.store = store or InMemoryKnowledgeStore()

    def build_request(
        self,
        accepted_state: AcceptedState,
        evidence: Evidence,
        object_type,
        truth_level: TruthLevel,
        semantic_payload: dict,
        semantic_identity: str,
        request_id: str,
        knowledge_object_id: str = "",
    ) -> KnowledgeUpdateRequest:
        """Factory for a consistent KnowledgeUpdateRequest."""
        if not request_id:
            raise KnowledgeError("missing request_id")
        return KnowledgeUpdateRequest(
            request_id=request_id,
            accepted_state_id=accepted_state.accepted_state_id,
            evidence_id=evidence.evidence_id,
            evidence_digest=evidence.payload_digest,
            knowledge_object_id=knowledge_object_id or "",
            object_type=object_type,
            truth_level=truth_level,
            semantic_payload=dict(semantic_payload),
            semantic_identity=semantic_identity,
        )

    def promote(
        self,
        request: KnowledgeUpdateRequest,
        accepted_state: AcceptedState,
        verification_result: VerificationResult,
        evidence: Evidence,
    ) -> KnowledgeObject:
        if request is None:
            raise KnowledgeError("missing KnowledgeUpdateRequest")
        if not request.request_id:
            raise KnowledgeError("missing request_id")

        self._validate_authority(accepted_state, verification_result, evidence)
        self._validate_request(request, accepted_state, evidence)

        if request.truth_level == TruthLevel.CANONICAL:
            raise KnowledgeError(
                "Canonical truth cannot be established implicitly; requires separate authority"
            )
        if not request.semantic_identity:
            raise KnowledgeError("missing semantic_identity")

        # Same request_id replay: deterministic same object if fingerprint matches
        prior_req = self.store.get_by_request_id(request.request_id)
        if prior_req is not None:
            obj, prior_fp = prior_req
            fp = InMemoryKnowledgeStore.request_fingerprint(request)
            if fp != prior_fp:
                raise KnowledgeConflictError("request_id reused with conflicting content")
            return obj

        kid = _id(
            "ko",
            accepted_state.accepted_state_id,
            evidence.payload_digest,
            request.object_type.value,
            request.semantic_identity,
        )

        existing = self.store.get_by_identity(
            accepted_state.accepted_state_id,
            evidence.payload_digest,
            request.object_type.value,
            request.semantic_identity,
        )
        if existing is not None:
            if existing.semantic_payload != request.semantic_payload:
                raise KnowledgeConflictError("semantic_payload conflict for same identity")
            if existing.truth_level != request.truth_level:
                raise KnowledgeConflictError("truth_level conflict for same identity")
            # Different request_id, same Knowledge identity + same payload → same object
            self.store.put(existing, request)
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
            object_type=request.object_type,
            truth_level=request.truth_level,
            semantic_payload=dict(request.semantic_payload),
            semantic_identity=request.semantic_identity,
            source_evidence_id=evidence.evidence_id,
            evidence_digest=evidence.payload_digest,
            accepted_state_id=accepted_state.accepted_state_id,
            verification_result_id=verification_result.verification_result_id,
            provenance=prov,
            status=KnowledgeStatus.ACTIVE,
            created_at=_utc_now(),
            originating_request_id=request.request_id,
        )
        self.store.put(obj, request)
        return obj

    def _validate_request(
        self,
        request: KnowledgeUpdateRequest,
        accepted_state: AcceptedState,
        evidence: Evidence,
    ) -> None:
        if request.accepted_state_id != accepted_state.accepted_state_id:
            raise KnowledgeError("request accepted_state_id mismatch")
        if request.evidence_id != evidence.evidence_id:
            raise KnowledgeError("request evidence_id mismatch")
        if request.evidence_digest != evidence.payload_digest:
            raise KnowledgeError("request evidence_digest mismatch")
        if request.evidence_id != accepted_state.evidence_id:
            raise KnowledgeError("request evidence_id vs AcceptedState mismatch")
        if request.evidence_digest != accepted_state.evidence_digest:
            raise KnowledgeError("request evidence_digest vs AcceptedState mismatch")

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

        if accepted_state.evidence_id != evidence.evidence_id:
            raise KnowledgeError("evidence_id mismatch")
        if accepted_state.evidence_digest != evidence.payload_digest:
            raise KnowledgeError("evidence_digest mismatch")

        for label, val in (
            ("accepted_state_id", accepted_state.accepted_state_id),
            ("verification_result_id", accepted_state.verification_result_id),
            ("evidence_id", evidence.evidence_id),
            ("evidence_digest", evidence.payload_digest),
        ):
            if not val:
                raise KnowledgeError(f"missing {label}")

    def promote_from_boolean(self, *a, **k):
        raise KnowledgeError("bare verified/passed boolean cannot promote Knowledge")

    def promote_without_request(self, *a, **k):
        raise KnowledgeError("KnowledgeUpdateRequest is mandatory")

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
