"""Memory consolidation. Append/version semantics. Non-authoritative."""

from __future__ import annotations

from typing import Dict, Optional

from aces_knowledge.models import EpistemicError, KnowledgeObject, Provenance
from aces_memory.models import MemoryObject, new_memory_id


class MemoryStore:
    def __init__(self) -> None:
        self._objects: Dict[str, MemoryObject] = {}
        self._history: list[MemoryObject] = []

    def put(self, obj: MemoryObject) -> None:
        self._objects[obj.memory_id] = obj
        self._history.append(obj)

    def get(self, memory_id: str) -> Optional[MemoryObject]:
        return self._objects.get(memory_id)

    def history(self) -> list[MemoryObject]:
        return list(self._history)


class MemoryService:
    """Durable recall/consolidation. Never Evidence, Truth, or Authority."""

    def __init__(self, store: Optional[MemoryStore] = None) -> None:
        self.store = store or MemoryStore()

    def consolidate_from_knowledge(
        self,
        *,
        knowledge: KnowledgeObject,
        actor: str = "memory_service",
    ) -> MemoryObject:
        provenance = Provenance(
            source_ref=knowledge.knowledge_id,
            task_id=knowledge.provenance.task_id,
            execution_id=knowledge.provenance.execution_id,
            evidence_ref=knowledge.provenance.evidence_ref,
            verification_ref=knowledge.provenance.verification_ref,
            accepted_state_ref=knowledge.provenance.accepted_state_ref,
            knowledge_ref=knowledge.knowledge_id,
            transformation="knowledge_to_memory",
            actor=actor,
        )
        provenance.validate()
        mem = MemoryObject(
            memory_id=new_memory_id(),
            content=knowledge.content,
            provenance=provenance,
            knowledge_ref=knowledge.knowledge_id,
            accepted_state_ref=knowledge.provenance.accepted_state_ref,
        )
        self.store.put(mem)
        return mem

    def consolidate_from_accepted_state(
        self,
        *,
        accepted_state: str,
        content: str,
        evidence_ref: Optional[str] = None,
        task_id: Optional[str] = None,
        actor: str = "memory_service",
    ) -> MemoryObject:
        if accepted_state != "ESTABLISHED":
            raise EpistemicError("accepted_state_required_for_memory_from_acceptance")
        provenance = Provenance(
            source_ref=f"accepted:{accepted_state}",
            task_id=task_id,
            evidence_ref=evidence_ref,
            accepted_state_ref=accepted_state,
            transformation="accepted_state_to_memory",
            actor=actor,
        )
        provenance.validate()
        mem = MemoryObject(
            memory_id=new_memory_id(),
            content=content,
            provenance=provenance,
            accepted_state_ref=accepted_state,
        )
        self.store.put(mem)
        return mem

    def recall(self, memory_id: str) -> MemoryObject:
        mem = self.store.get(memory_id)
        if mem is None:
            raise EpistemicError("memory_not_found")
        return mem

    def reject_as_evidence(self, memory: MemoryObject) -> None:
        raise EpistemicError("memory_is_not_evidence")

    def reject_as_truth(self, memory: MemoryObject) -> None:
        raise EpistemicError("memory_is_not_truth")

    def reject_as_authority(self, memory: MemoryObject) -> None:
        raise EpistemicError("memory_is_not_authority")

    def reject_as_verification(self, memory: MemoryObject) -> None:
        raise EpistemicError("memory_is_not_verification")
