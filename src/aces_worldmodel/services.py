"""World Model update. Belief/projection only — never Semantic Reality."""

from __future__ import annotations

from typing import Dict, Optional

from aces_knowledge.models import EpistemicError, KnowledgeObject, Provenance
from aces_worldmodel.models import BeliefState, WorldModelState, new_wm_id


class WorldModelStore:
    def __init__(self) -> None:
        self._states: Dict[str, WorldModelState] = {}
        self._history: list[WorldModelState] = []

    def put(self, state: WorldModelState) -> None:
        self._states[state.world_model_id] = state
        self._history.append(state)

    def get(self, world_model_id: str) -> Optional[WorldModelState]:
        return self._states.get(world_model_id)

    def history(self) -> list[WorldModelState]:
        return list(self._history)


class WorldModelService:
    """Controlled belief updates. Forbidden: Evidence, AcceptedState, Knowledge auto, Reality mutation."""

    def __init__(self, store: Optional[WorldModelStore] = None) -> None:
        self.store = store or WorldModelStore()

    def update_from_knowledge(
        self,
        *,
        knowledge: KnowledgeObject,
        alpha: float = 2.0,
        beta: float = 2.0,
        projection: Optional[str] = None,
        actor: str = "world_model_service",
    ) -> WorldModelState:
        belief = BeliefState(alpha=alpha, beta=beta)
        provenance = Provenance(
            source_ref=knowledge.knowledge_id,
            task_id=knowledge.provenance.task_id,
            execution_id=knowledge.provenance.execution_id,
            evidence_ref=knowledge.provenance.evidence_ref,
            verification_ref=knowledge.provenance.verification_ref,
            accepted_state_ref=knowledge.provenance.accepted_state_ref,
            knowledge_ref=knowledge.knowledge_id,
            transformation="knowledge_to_world_model",
            actor=actor,
        )
        provenance.validate()
        state = WorldModelState(
            world_model_id=new_wm_id(),
            belief=belief,
            projection=projection or f"belief:{knowledge.content}",
            provenance=provenance,
            knowledge_ref=knowledge.knowledge_id,
            accepted_state_ref=knowledge.provenance.accepted_state_ref,
        )
        self.store.put(state)
        return state

    def update_from_accepted_state(
        self,
        *,
        accepted_state: str,
        projection: str,
        alpha: float = 1.0,
        beta: float = 1.0,
        evidence_ref: Optional[str] = None,
        actor: str = "world_model_service",
    ) -> WorldModelState:
        if accepted_state != "ESTABLISHED":
            raise EpistemicError("accepted_state_required_for_wm_update")
        belief = BeliefState(alpha=alpha, beta=beta)
        provenance = Provenance(
            source_ref=f"accepted:{accepted_state}",
            evidence_ref=evidence_ref,
            accepted_state_ref=accepted_state,
            transformation="accepted_state_to_world_model",
            actor=actor,
        )
        provenance.validate()
        state = WorldModelState(
            world_model_id=new_wm_id(),
            belief=belief,
            projection=projection,
            provenance=provenance,
            accepted_state_ref=accepted_state,
        )
        self.store.put(state)
        return state

    def reject_as_evidence(self, state: WorldModelState) -> None:
        raise EpistemicError("world_model_is_not_evidence")

    def reject_as_accepted_state(self, state: WorldModelState) -> None:
        raise EpistemicError("world_model_is_not_accepted_state")

    def reject_as_authority(self, state: WorldModelState) -> None:
        raise EpistemicError("world_model_is_not_authority")

    def reject_auto_knowledge(self, state: WorldModelState) -> None:
        raise EpistemicError("world_model_cannot_create_knowledge")

    def reject_semantic_reality_mutation(self, state: WorldModelState) -> None:
        raise EpistemicError("world_model_cannot_mutate_semantic_reality")
