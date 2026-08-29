"""Event schema and provenance types for P0.3.2-I."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class Actor(str, Enum):
    HUMAN = "human"
    COORDINATOR = "coordinator"
    SYSTEM = "system"


class ProvenanceConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INSUFFICIENT = "insufficient"


class EventType(str, Enum):
    TASK_START = "task_start"
    TASK_END = "task_end"
    APP_SWITCH = "app_switch"
    SEARCH = "search"
    REFIND = "refind"
    COPY = "copy"
    PASTE = "paste"
    LINK_INSERT = "link_insert"
    NAVIGATION = "navigation"
    HUMAN_CORRECTION = "human_correction"
    RECOVERY = "recovery"
    CONTEXT_ERROR = "context_error"
    DECISION_ERROR = "decision_error"
    INTERRUPTION = "interruption"
    COGNITIVE_EFFORT = "cognitive_effort"
    TASK_QUALITY = "task_quality"
    COORDINATOR_SUGGEST = "coordinator_suggest"
    COORDINATOR_ACTION = "coordinator_action"
    SUPERVISION_INSPECT = "supervision_inspect"
    SUPERVISION_VERIFY = "supervision_verify"
    SUPERVISION_REJECT = "supervision_reject"
    SUPERVISION_REPAIR = "supervision_repair"
    SYSTEM_NOISE = "system_noise"


# Event types that may contribute to HCC only when actor=HUMAN and confidence sufficient
HCC_ELIGIBLE_TYPES = frozenset({
    EventType.APP_SWITCH,
    EventType.SEARCH,
    EventType.REFIND,
    EventType.COPY,
    EventType.PASTE,
    EventType.LINK_INSERT,
    EventType.HUMAN_CORRECTION,
    EventType.RECOVERY,
    EventType.CONTEXT_ERROR,
    EventType.DECISION_ERROR,
})


@dataclass(frozen=True)
class InstrumentationEvent:
    """Immutable experimental event with mandatory provenance."""

    event_id: str
    session_id: str
    participant_id: str
    unit_id: str
    timestamp: datetime
    actor: Actor
    system_surface: str
    event_type: EventType
    provenance_confidence: ProvenanceConfidence
    condition: str | None = None
    variant: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "explicit"

    @property
    def primary_analysis_eligible(self) -> bool:
        """True only when the event may enter the HCC composite."""
        if self.provenance_confidence in (
            ProvenanceConfidence.LOW,
            ProvenanceConfidence.INSUFFICIENT,
        ):
            return False
        if self.actor is not Actor.HUMAN:
            return False
        if self.event_type not in HCC_ELIGIBLE_TYPES and self.event_type not in (
            EventType.TASK_START,
            EventType.TASK_END,
            EventType.COGNITIVE_EFFORT,
            EventType.TASK_QUALITY,
            EventType.INTERRUPTION,
        ):
            return False
        return True

    @staticmethod
    def create(
        *,
        session_id: str,
        participant_id: str,
        unit_id: str,
        actor: Actor,
        system_surface: str,
        event_type: EventType,
        provenance_confidence: ProvenanceConfidence = ProvenanceConfidence.HIGH,
        condition: str | None = None,
        variant: str | None = None,
        payload: dict[str, Any] | None = None,
        source: str = "explicit",
        timestamp: datetime | None = None,
    ) -> "InstrumentationEvent":
        return InstrumentationEvent(
            event_id=str(uuid4()),
            session_id=session_id,
            participant_id=participant_id,
            unit_id=unit_id,
            timestamp=timestamp or datetime.now(timezone.utc),
            actor=actor,
            system_surface=system_surface,
            event_type=event_type,
            provenance_confidence=provenance_confidence,
            condition=condition,
            variant=variant,
            payload=payload or {},
            source=source,
        )
