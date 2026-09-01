"""Knowledge promotion and Semantic Reality update services.

AcceptedState → Knowledge is explicit and must originate from a verified
ExecutionResult (VerificationService path). A bare status token is insufficient.
World Model has no path into Semantic Reality here.
"""

from __future__ import annotations

from typing import Dict, Optional

from aces_execution_adapter.models import (
    AcceptedStateStatus,
    ExecutionResult,
    ExecutionStatus,
    VerificationStatus,
)

from aces_knowledge.models import (
    EpistemicError,
    KnowledgeObject,
    KnowledgeObjectType,
    Provenance,
    RealityState,
    TruthLevel,
    VerificationState,
    new_id,
)


class KnowledgeStore:
    """In-memory append/version store. Not production persistence."""

    def __init__(self) -> None:
        self._objects: Dict[str, KnowledgeObject] = {}
        self._history: list[KnowledgeObject] = []

    def put(self, obj: KnowledgeObject) -> None:
        self._objects[obj.knowledge_id] = obj
        self._history.append(obj)

    def get(self, knowledge_id: str) -> Optional[KnowledgeObject]:
        return self._objects.get(knowledge_id)

    def history(self) -> list[KnowledgeObject]:
        return list(self._history)


class RealityStore:
    def __init__(self) -> None:
        self._states: Dict[str, RealityState] = {}
        self._history: list[RealityState] = []

    def put(self, state: RealityState) -> None:
        self._states[state.reality_id] = state
        self._history.append(state)

    def get(self, reality_id: str) -> Optional[RealityState]:
        return self._states.get(reality_id)

    def history(self) -> list[RealityState]:
        return list(self._history)


class KnowledgeUpdateService:
    """Explicit verified-result → Knowledge promotion. No silent Fact creation."""

    def __init__(self, store: Optional[KnowledgeStore] = None) -> None:
        self.store = store or KnowledgeStore()

    def promote_from_verified_result(
        self,
        verified_result: ExecutionResult,
        *,
        content: str,
        task_id: str,
        operation: str,
        resource: str,
        scope: str,
        object_type: KnowledgeObjectType = KnowledgeObjectType.FACT,
        truth_level: TruthLevel = TruthLevel.WORKING,
        actor: str = "knowledge_update_service",
    ) -> KnowledgeObject:
        if verified_result is None:
            raise EpistemicError("verified_result_required")

        if verified_result.status != ExecutionStatus.SUCCEEDED:
            raise EpistemicError("execution_not_succeeded")

        if verified_result.accepted_state != AcceptedStateStatus.ESTABLISHED:
            raise EpistemicError("accepted_state_required")

        if verified_result.verification_status != VerificationStatus.PASSED:
            raise EpistemicError("verification_not_passed")

        evidence_id = verified_result.provenance.get("evidence_id")
        verifier_id = verified_result.provenance.get("verifier_id")
        if not evidence_id or not str(evidence_id).strip():
            raise EpistemicError("evidence_binding_required")
        if not verifier_id or not str(verifier_id).strip():
            raise EpistemicError("verification_ref_required")
        if not content or not str(content).strip():
            raise EpistemicError("content_required")
        if not task_id or not operation or not resource or not scope:
            raise EpistemicError("binding_fields_required")
        if truth_level not in TruthLevel:
            raise EpistemicError("invalid_truth_level")

        provenance = Provenance(
            source_ref=f"accepted:{verified_result.accepted_state.value}",
            task_id=task_id,
            execution_id=verified_result.request_id,
            evidence_ref=str(evidence_id),
            verification_ref=str(verifier_id),
            accepted_state_ref=verified_result.accepted_state.value,
            transformation="verified_result_to_knowledge",
            actor=actor,
        )
        provenance.validate()

        obj = KnowledgeObject(
            knowledge_id=new_id("ko"),
            object_type=object_type,
            truth_level=truth_level,
            verification_state=VerificationState.VERIFIED,
            content=content,
            provenance=provenance,
            evidence_refs=(str(evidence_id),),
        )
        self.store.put(obj)
        return obj

    def promote_from_accepted_state(self, *args, **kwargs):
        """Deprecated token path — status string alone is insufficient."""
        raise EpistemicError("status_token_insufficient_use_promote_from_verified_result")

    def reject_execution_success_alone(self, *, execution_status: str) -> None:
        if execution_status == "SUCCEEDED":
            raise EpistemicError("execution_success_is_not_knowledge")
        raise EpistemicError("execution_status_not_promotable")

    def reject_evidence_without_accepted_state(self, *, evidence_id: str) -> None:
        raise EpistemicError("evidence_without_accepted_state_not_knowledge")

    def reject_agent_assertion(self, *, assertion: str) -> None:
        raise EpistemicError("agent_assertion_is_not_knowledge")

    def reject_world_model_auto_knowledge(self) -> None:
        raise EpistemicError("world_model_cannot_create_knowledge")

    def reject_knowledge_as_authorization(self) -> None:
        raise EpistemicError("knowledge_is_not_authority")


class SemanticRealityService:
    """Knowledge → Semantic Reality only. World Model / Memory cannot call this successfully."""

    def __init__(self, store: Optional[RealityStore] = None) -> None:
        self.store = store or RealityStore()

    def update_from_knowledge(
        self,
        *,
        knowledge: KnowledgeObject,
        actor: str = "semantic_reality_service",
    ) -> RealityState:
        if knowledge.verification_state != VerificationState.VERIFIED:
            raise EpistemicError("knowledge_not_verified")
        if not knowledge.provenance.accepted_state_ref:
            raise EpistemicError("knowledge_missing_accepted_state_provenance")
        if not knowledge.evidence_refs:
            raise EpistemicError("knowledge_missing_evidence_refs")

        provenance = Provenance(
            source_ref=knowledge.knowledge_id,
            task_id=knowledge.provenance.task_id,
            execution_id=knowledge.provenance.execution_id,
            evidence_ref=knowledge.provenance.evidence_ref,
            verification_ref=knowledge.provenance.verification_ref,
            accepted_state_ref=knowledge.provenance.accepted_state_ref,
            knowledge_ref=knowledge.knowledge_id,
            transformation="knowledge_to_semantic_reality",
            actor=actor,
        )
        provenance.validate()

        state = RealityState(
            reality_id=new_id("reality"),
            claim=knowledge.content,
            knowledge_ref=knowledge.knowledge_id,
            provenance=provenance,
        )
        self.store.put(state)
        return state

    def reject_from_memory(self) -> None:
        raise EpistemicError("memory_cannot_mutate_semantic_reality")

    def reject_from_world_model(self) -> None:
        raise EpistemicError("world_model_cannot_mutate_semantic_reality")

    def reject_from_execution_success(self) -> None:
        raise EpistemicError("execution_success_cannot_mutate_semantic_reality")

    def reject_from_unverified_evidence(self) -> None:
        raise EpistemicError("unverified_evidence_cannot_mutate_semantic_reality")

    def reject_from_agent_assertion(self) -> None:
        raise EpistemicError("agent_assertion_cannot_mutate_semantic_reality")
