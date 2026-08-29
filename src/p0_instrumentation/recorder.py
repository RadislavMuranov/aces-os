"""Provenance-aware event recorder."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from .events import (
    Actor,
    EventType,
    InstrumentationEvent,
    ProvenanceConfidence,
)


@dataclass
class EventRecorder:
    """In-memory recorder that enforces provenance rules.

    Callers must supply actor explicitly. The recorder never infers human
    activity from the mere presence of an event on a human-facing surface.
    """

    session_id: str
    participant_id: str
    events: list[InstrumentationEvent] = field(default_factory=list)

    def record(self, event: InstrumentationEvent) -> InstrumentationEvent:
        if event.session_id != self.session_id:
            raise ValueError("session_id mismatch")
        if event.participant_id != self.participant_id:
            raise ValueError("participant_id mismatch")
        self.events.append(event)
        return event

    def record_explicit(
        self,
        *,
        unit_id: str,
        actor: Actor,
        system_surface: str,
        event_type: EventType,
        provenance_confidence: ProvenanceConfidence = ProvenanceConfidence.HIGH,
        condition: str | None = None,
        variant: str | None = None,
        payload: dict | None = None,
        source: str = "explicit",
    ) -> InstrumentationEvent:
        event = InstrumentationEvent.create(
            session_id=self.session_id,
            participant_id=self.participant_id,
            unit_id=unit_id,
            actor=actor,
            system_surface=system_surface,
            event_type=event_type,
            provenance_confidence=provenance_confidence,
            condition=condition,
            variant=variant,
            payload=payload,
            source=source,
        )
        return self.record(event)

    def events_for_unit(self, unit_id: str) -> list[InstrumentationEvent]:
        return [e for e in self.events if e.unit_id == unit_id]

    def primary_eligible(self, unit_id: str | None = None) -> list[InstrumentationEvent]:
        pool: Iterable[InstrumentationEvent] = (
            self.events_for_unit(unit_id) if unit_id else self.events
        )
        return [e for e in pool if e.primary_analysis_eligible]

    def by_actor(self, actor: Actor, unit_id: str | None = None) -> list[InstrumentationEvent]:
        pool: Iterable[InstrumentationEvent] = (
            self.events_for_unit(unit_id) if unit_id else self.events
        )
        return [e for e in pool if e.actor is actor]
