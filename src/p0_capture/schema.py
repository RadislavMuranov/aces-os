"""Event schema with mandatory provenance for capture adapter."""

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
    NAVIGATION = "navigation"
    SEARCH = "search"
    REFIND = "refind"
    COPY = "copy"
    PASTE = "paste"
    LINK_INSERT = "link_insert"
    HUMAN_CORRECTION = "human_correction"
    RECOVERY = "recovery"
    INTERRUPTION = "interruption"
    COGNITIVE_EFFORT = "cognitive_effort"
    TASK_QUALITY = "task_quality"
    COORDINATOR_SUGGEST = "coordinator_suggest"
    COORDINATOR_ACTION = "coordinator_action"
    SYSTEM_EVENT = "system_event"
    SUPERVISION_INSPECT = "supervision_inspect"
    SUPERVISION_VERIFY = "supervision_verify"
    SUPERVISION_REJECT = "supervision_reject"
    SUPERVISION_REPAIR = "supervision_repair"


HCC_COUNT_TYPES = frozenset({
    EventType.APP_SWITCH,
    EventType.NAVIGATION,
    EventType.SEARCH,
    EventType.REFIND,
    EventType.COPY,
    EventType.PASTE,
    EventType.LINK_INSERT,
    EventType.HUMAN_CORRECTION,
    EventType.RECOVERY,
})


@dataclass(frozen=True)
class CaptureEvent:
    event_id: str
    session_id: str
    timestamp: datetime
    event_type: EventType
    actor: Actor
    provenance_confidence: ProvenanceConfidence
    experiment_surface: str
    primary_analysis_eligible: bool
    artifact_id: str | None = None
    content_hash: str | None = None
    source: str = "capture"
    payload: dict[str, Any] = field(default_factory=dict)
    ambiguous: bool = False

    @staticmethod
    def make(
        *,
        session_id: str,
        event_type: EventType,
        actor: Actor,
        experiment_surface: str,
        provenance_confidence: ProvenanceConfidence,
        primary_analysis_eligible: bool,
        artifact_id: str | None = None,
        content_hash: str | None = None,
        source: str = "capture",
        payload: dict[str, Any] | None = None,
        ambiguous: bool = False,
        timestamp: datetime | None = None,
    ) -> "CaptureEvent":
        return CaptureEvent(
            event_id=str(uuid4()),
            session_id=session_id,
            timestamp=timestamp or datetime.now(timezone.utc),
            event_type=event_type,
            actor=actor,
            provenance_confidence=provenance_confidence,
            experiment_surface=experiment_surface,
            primary_analysis_eligible=primary_analysis_eligible,
            artifact_id=artifact_id,
            content_hash=content_hash,
            source=source,
            payload=payload or {},
            ambiguous=ambiguous,
        )


@dataclass(frozen=True)
class MissingEvent:
    session_id: str
    unit_id: str
    expected_type: EventType
    reason: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
