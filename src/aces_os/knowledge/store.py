"""In-memory Knowledge store — full identity index."""

from __future__ import annotations

from typing import Dict, Optional

from .model import KnowledgeObject, knowledge_identity_key


class InMemoryKnowledgeStore:
    def __init__(self) -> None:
        self._by_id: Dict[str, KnowledgeObject] = {}
        self._by_identity: Dict[str, str] = {}

    def put(self, obj: KnowledgeObject) -> None:
        key = knowledge_identity_key(
            obj.accepted_state_id,
            obj.evidence_digest,
            obj.object_type.value,
            obj.semantic_identity,
        )
        self._by_id[obj.knowledge_object_id] = obj
        self._by_identity[key] = obj.knowledge_object_id

    def get(self, knowledge_object_id: str) -> Optional[KnowledgeObject]:
        return self._by_id.get(knowledge_object_id)

    def get_by_identity(
        self,
        accepted_state_id: str,
        evidence_digest: str,
        object_type: str,
        semantic_identity: str,
    ) -> Optional[KnowledgeObject]:
        key = knowledge_identity_key(
            accepted_state_id, evidence_digest, object_type, semantic_identity
        )
        kid = self._by_identity.get(key)
        return self._by_id.get(kid) if kid else None
