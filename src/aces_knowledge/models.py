"""Knowledge and Semantic Reality domain models (Contract v0.1 + v0.1a).

Knowledge ≠ Authority. Knowledge ≠ Evidence.
Semantic Reality updates require Knowledge path — not World Model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional, Tuple
import uuid


class KnowledgeObjectType(str, Enum):
    FACT = "Fact"
    DECISION = "Decision"
    ARTIFACT = "Artifact"
    HYPOTHESIS = "Hypothesis"
    POLICY = "Policy"


class TruthLevel(str, Enum):
    WORKING = "Working"
    OPERATIONAL = "Operational"
    CANONICAL = "Canonical"


class VerificationState(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class EpistemicError(ValueError):
    """Fail-closed epistemic boundary violation."""


@dataclass(frozen=True)
class Provenance:
    """Logical provenance only — not cryptographic."""

    source_ref: str
    task_id: Optional[str] = None
    execution_id: Optional[str] = None
    evidence_ref: Optional[str] = None
    verification_ref: Optional[str] = None
    accepted_state_ref: Optional[str] = None
    knowledge_ref: Optional[str] = None
    transformation: Optional[str] = None
    actor: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = "1"

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_ref": self.source_ref,
            "task_id": self.task_id,
            "execution_id": self.execution_id,
            "evidence_ref": self.evidence_ref,
            "verification_ref": self.verification_ref,
            "accepted_state_ref": self.accepted_state_ref,
            "knowledge_ref": self.knowledge_ref,
            "transformation": self.transformation,
            "actor": self.actor,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
        }

    def validate(self) -> None:
        if not self.source_ref or not str(self.source_ref).strip():
            raise EpistemicError("provenance_missing_source_ref")


@dataclass(frozen=True)
class KnowledgeObject:
    knowledge_id: str
    object_type: KnowledgeObjectType
    truth_level: TruthLevel
    verification_state: VerificationState
    content: str
    provenance: Provenance
    evidence_refs: Tuple[str, ...] = ()
    version: int = 1
    supersedes: Optional[str] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "knowledge_id": self.knowledge_id,
            "object_type": self.object_type.value,
            "truth_level": self.truth_level.value,
            "verification_state": self.verification_state.value,
            "content": self.content,
            "provenance": self.provenance.to_dict(),
            "evidence_refs": list(self.evidence_refs),
            "version": self.version,
            "supersedes": self.supersedes,
            "created_at": self.created_at.isoformat(),
        }


@dataclass(frozen=True)
class RealityState:
    """Semantic Reality snapshot. Not World Model. Not authority."""

    reality_id: str
    claim: str
    knowledge_ref: str
    provenance: Provenance
    version: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "reality_id": self.reality_id,
            "claim": self.claim,
            "knowledge_ref": self.knowledge_ref,
            "provenance": self.provenance.to_dict(),
            "version": self.version,
            "created_at": self.created_at.isoformat(),
        }


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"
