"""World Model and BeliefState. World Model ≠ Semantic Reality."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import uuid

from aces_knowledge.models import EpistemicError, Provenance


@dataclass(frozen=True)
class BeliefState:
    """Minimal Beta(α, β). alpha > 0, beta > 0. Confidence ≠ Truth."""

    alpha: float
    beta: float

    def __post_init__(self) -> None:
        if self.alpha <= 0 or self.beta <= 0:
            raise EpistemicError("belief_alpha_beta_must_be_positive")

    @property
    def mean(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    def to_dict(self) -> dict[str, Any]:
        return {"alpha": self.alpha, "beta": self.beta, "mean": self.mean}


@dataclass(frozen=True)
class WorldModelState:
    world_model_id: str
    belief: BeliefState
    projection: str
    provenance: Provenance
    knowledge_ref: Optional[str] = None
    accepted_state_ref: Optional[str] = None
    version: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict[str, Any]:
        return {
            "world_model_id": self.world_model_id,
            "belief": self.belief.to_dict(),
            "projection": self.projection,
            "provenance": self.provenance.to_dict(),
            "knowledge_ref": self.knowledge_ref,
            "accepted_state_ref": self.accepted_state_ref,
            "version": self.version,
            "created_at": self.created_at.isoformat(),
        }


def new_wm_id() -> str:
    return f"wm-{uuid.uuid4().hex[:12]}"
