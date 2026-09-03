"""Phase VI — Knowledge promotion from AcceptedState.

Knowledge ≠ Truth ≠ Authority ≠ Memory ≠ World Model ≠ Semantic Reality.
Only ESTABLISHED AcceptedState may promote Knowledge.
Canonical truth is NOT implicit.
"""

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
