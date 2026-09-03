"""In-memory Knowledge store — full identity index + request replay."""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from .model import KnowledgeObject, KnowledgeUpdateRequest, knowledge_identity_key


class InMemoryKnowledgeStore:
    def __init__(self) -> None:
        self._by_id: Dict[str, KnowledgeObject] = {}
        self._by_identity: Dict[str, str] = {}
        # request_id -> (knowledge_object_id, fingerprint of request identity fields)
        self._by_request: Dict[str, Tuple[str, str]] = {}

    @staticmethod
    def request_fingerprint(req: KnowledgeUpdateRequest) -> str:
        return "|".join(
            [
                req.accepted_state_id,
                req.evidence_id,
                req.evidence_digest,
                req.object_type.value,
                req.truth_level.value,
                req.semantic_identity,
                str(sorted(req.semantic_payload.items())),
            ]
        )

    def put(self, obj: KnowledgeObject, req: Optional[KnowledgeUpdateRequest] = None) -> None:
        key = knowledge_identity_key(
            obj.accepted_state_id,
            obj.evidence_digest,
            obj.object_type.value,
            obj.semantic_identity,
        )
        self._by_id[obj.knowledge_object_id] = obj
        self._by_identity[key] = obj.knowledge_object_id
        if req is not None:
            self._by_request[req.request_id] = (
                obj.knowledge_object_id,
                self.request_fingerprint(req),
            )

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

    def get_by_request_id(self, request_id: str) -> Optional[Tuple[KnowledgeObject, str]]:
        entry = self._by_request.get(request_id)
        if entry is None:
            return None
        kid, fp = entry
        obj = self._by_id.get(kid)
        if obj is None:
            return None
        return obj, fp
