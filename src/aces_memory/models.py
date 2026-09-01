"""Memory domain models. Memory ≠ Truth ≠ Evidence ≠ Authority."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import uuid

from aces_knowledge.models import EpistemicError, Provenance


@dataclass(frozen=True)
class MemoryObject:
    memory_id: str
    content: str
    provenance: Provenance
    knowledge_ref: Optional[str] = None
    accepted_state_ref: Optional[str] = None
    version: int = 1
    supersedes: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "memory_id": self.memory_id,
            "content": self.content,
            "provenance": self.provenance.to_dict(),
            "knowledge_ref": self.knowledge_ref,
            "accepted_state_ref": self.accepted_state_ref,
            "version": self.version,
            "supersedes": self.supersedes,
            "created_at": self.created_at.isoformat(),
        }


def new_memory_id() -> str:
    return f"mem-{uuid.uuid4().hex[:12]}"
