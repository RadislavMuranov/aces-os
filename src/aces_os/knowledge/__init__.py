"""Phase VI — Knowledge promotion from AcceptedState via KnowledgeUpdateRequest."""

from .model import (
    KnowledgeObjectType,
    TruthLevel,
    KnowledgeStatus,
    KnowledgeObject,
    KnowledgeUpdateRequest,
    KnowledgeProvenance,
    knowledge_identity_key,
)
from .store import InMemoryKnowledgeStore
from .service import KnowledgePromotionService, KnowledgeError, KnowledgeConflictError

__all__ = [
    "KnowledgeObjectType",
    "TruthLevel",
    "KnowledgeStatus",
    "KnowledgeObject",
    "KnowledgeUpdateRequest",
    "KnowledgeProvenance",
    "knowledge_identity_key",
    "InMemoryKnowledgeStore",
    "KnowledgePromotionService",
    "KnowledgeError",
    "KnowledgeConflictError",
]
