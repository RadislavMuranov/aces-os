"""Privacy-safe capture adapter with allow-list and provenance enforcement.

This adapter does NOT perform OS-level focus or clipboard monitoring.
It accepts explicit observations (from a test driver or a future OS adapter)
and enforces:

- experiment-surface allow-list
- automatic treatment of non-allow-listed surfaces as insufficient provenance
- never inferring human from generic software events
- dedicated coordinator emission channel
- explicit missing-event recording
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable

from .allowlist import SurfaceAllowList
from .schema import (
    Actor,
    CaptureEvent,
    EventType,
    MissingEvent,
    ProvenanceConfidence,
    HCC_COUNT_TYPES,
)


def _hash_meta(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


@dataclass
class CaptureAdapter:
    session_id: str
    allowlist: SurfaceAllowList
    events: list[CaptureEvent] = field(default_factory=list)
    missing: list[MissingEvent] = field(default_factory=list)
    unit_id: str = "default"
    _paused_outside: bool = False

    def start_unit(self, unit_id: str) -> CaptureEvent:
        self.unit_id = unit_id
        return self._emit_human_structural(EventType.TASK_START)

    def end_unit(self) -> CaptureEvent:
        return self._emit_human_structural(EventType.TASK_END)

    def pause_outside_allowlist(self) -> None:
        self._paused_outside = True
        self.allowlist.pause()

    def resume_on_allowlist(self) -> None:
        self._paused_outside = False
        self.allowlist.resume()

    def observe_human(
        self,
        event_type: EventType,
        surface: str,
        *,
        artifact_id: str | None = None,
        content_for_hash: str | None = None,
        payload: dict | None = None,
        timestamp: datetime | None = None,
    ) -> CaptureEvent:
        if not self.allowlist.is_allowed(surface):
            return self._record_insufficient(
                event_type=event_type,
                surface=surface,
                intended_actor=Actor.HUMAN,
                artifact_id=artifact_id,
                content_for_hash=content_for_hash,
                payload=payload,
                timestamp=timestamp,
            )
        primary = event_type in HCC_COUNT_TYPES
        ev = CaptureEvent.make(
            session_id=self.session_id,
            event_type=event_type,
            actor=Actor.HUMAN,
            experiment_surface=surface,
            provenance_confidence=ProvenanceConfidence.HIGH,
            primary_analysis_eligible=primary,
            artifact_id=artifact_id,
            content_hash=_hash_meta(content_for_hash) if content_for_hash else None,
            source="human_observation",
            payload=payload,
            timestamp=timestamp,
        )
        self.events.append(ev)
        return ev

    def emit_coordinator(
        self,
        event_type: EventType,
        *,
        surface: str = "coordinator",
        artifact_id: str | None = None,
        payload: dict | None = None,
        timestamp: datetime | None = None,
    ) -> CaptureEvent:
        if event_type not in (
            EventType.COORDINATOR_SUGGEST,
            EventType.COORDINATOR_ACTION,
        ):
            event_type = EventType.COORDINATOR_ACTION
        ev = CaptureEvent.make(
            session_id=self.session_id,
            event_type=event_type,
            actor=Actor.COORDINATOR,
            experiment_surface=surface,
            provenance_confidence=ProvenanceConfidence.HIGH,
            primary_analysis_eligible=False,
            artifact_id=artifact_id,
            source="coordinator_channel",
            payload=payload,
            timestamp=timestamp,
        )
        self.events.append(ev)
        return ev

    def observe_system(
        self,
        surface: str = "os",
        *,
        payload: dict | None = None,
        timestamp: datetime | None = None,
    ) -> CaptureEvent:
        ev = CaptureEvent.make(
            session_id=self.session_id,
            event_type=EventType.SYSTEM_EVENT,
            actor=Actor.SYSTEM,
            experiment_surface=surface,
            provenance_confidence=ProvenanceConfidence.HIGH,
            primary_analysis_eligible=False,
            source="system",
            payload=payload,
            timestamp=timestamp,
        )
        self.events.append(ev)
        return ev

    def observe_unknown_surface(
        self,
        event_type: EventType,
        surface: str,
        *,
        payload: dict | None = None,
        timestamp: datetime | None = None,
    ) -> CaptureEvent:
        return self._record_insufficient(
            event_type=event_type,
            surface=surface,
            intended_actor=Actor.HUMAN,
            payload=payload,
            timestamp=timestamp,
        )

    def record_missing(self, expected_type: EventType, reason: str) -> MissingEvent:
        m = MissingEvent(
            session_id=self.session_id,
            unit_id=self.unit_id,
            expected_type=expected_type,
            reason=reason,
        )
        self.missing.append(m)
        return m

    def unit_incomplete(self) -> bool:
        return len(self.missing) > 0

    def human_eligible(self) -> list[CaptureEvent]:
        return [e for e in self.events if e.primary_analysis_eligible and e.actor is Actor.HUMAN]

    def by_actor(self, actor: Actor) -> list[CaptureEvent]:
        return [e for e in self.events if e.actor is actor]

    def _emit_human_structural(self, et: EventType) -> CaptureEvent:
        ev = CaptureEvent.make(
            session_id=self.session_id,
            event_type=et,
            actor=Actor.HUMAN,
            experiment_surface="experiment",
            provenance_confidence=ProvenanceConfidence.HIGH,
            primary_analysis_eligible=False,
            source="structural",
        )
        self.events.append(ev)
        return ev

    def _record_insufficient(
        self,
        *,
        event_type: EventType,
        surface: str,
        intended_actor: Actor,
        artifact_id: str | None = None,
        content_for_hash: str | None = None,
        payload: dict | None = None,
        timestamp: datetime | None = None,
    ) -> CaptureEvent:
        ev = CaptureEvent.make(
            session_id=self.session_id,
            event_type=event_type,
            actor=intended_actor,
            experiment_surface=surface,
            provenance_confidence=ProvenanceConfidence.INSUFFICIENT,
            primary_analysis_eligible=False,
            artifact_id=artifact_id,
            content_hash=_hash_meta(content_for_hash) if content_for_hash else None,
            source="insufficient_surface",
            payload=payload,
            ambiguous=True,
            timestamp=timestamp,
        )
        self.events.append(ev)
        return ev
