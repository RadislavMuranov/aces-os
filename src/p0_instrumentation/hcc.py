"""HCC component extraction — human events only."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from .events import Actor, EventType, InstrumentationEvent, ProvenanceConfidence


@dataclass(frozen=True)
class HCCComponents:
    """Direct observables that may form the pre-registered HCC composite.

    Coordinator activity is deliberately absent.
    """

    wall_clock_seconds: float | None
    app_switches: int
    searches: int
    refinds: int
    copy_ops: int
    paste_ops: int
    link_inserts: int
    human_corrections: int
    recovery_events: int
    context_errors: int
    decision_errors: int
    cognitive_effort: float | None
    task_quality: float | None
    supervision_inspect: int
    supervision_verify: int
    supervision_reject: int
    supervision_repair: int
    coordinator_events: int  # independent variable, NOT part of HCC
    ineligible_events: int
    primary_eligible_count: int


def compute_hcc_components(events: Sequence[InstrumentationEvent]) -> HCCComponents:
    """Compute HCC components from a unit's events.

    Rules:
    - wall-clock from TASK_START / TASK_END
    - count metrics only from actor=HUMAN with sufficient provenance
    - supervision metrics from human actions that respond to coordinator
    - coordinator_events counted separately and never folded into HCC
    """
    starts = [e for e in events if e.event_type is EventType.TASK_START]
    ends = [e for e in events if e.event_type is EventType.TASK_END]
    wall: float | None = None
    if starts and ends:
        t0: datetime = min(e.timestamp for e in starts)
        t1: datetime = max(e.timestamp for e in ends)
        wall = max(0.0, (t1 - t0).total_seconds())

    def human_count(etype: EventType) -> int:
        return sum(
            1
            for e in events
            if e.event_type is etype
            and e.actor is Actor.HUMAN
            and e.provenance_confidence
            not in (ProvenanceConfidence.LOW, ProvenanceConfidence.INSUFFICIENT)
        )

    effort_vals = [
        float(e.payload["score"])
        for e in events
        if e.event_type is EventType.COGNITIVE_EFFORT
        and "score" in e.payload
        and e.actor is Actor.HUMAN
    ]
    quality_vals = [
        float(e.payload["score"])
        for e in events
        if e.event_type is EventType.TASK_QUALITY and "score" in e.payload
    ]

    coord = sum(
        1
        for e in events
        if e.actor is Actor.COORDINATOR
        or e.event_type
        in (EventType.COORDINATOR_SUGGEST, EventType.COORDINATOR_ACTION)
    )
    ineligible = sum(1 for e in events if not e.primary_analysis_eligible)
    primary = sum(1 for e in events if e.primary_analysis_eligible)

    return HCCComponents(
        wall_clock_seconds=wall,
        app_switches=human_count(EventType.APP_SWITCH),
        searches=human_count(EventType.SEARCH),
        refinds=human_count(EventType.REFIND),
        copy_ops=human_count(EventType.COPY),
        paste_ops=human_count(EventType.PASTE),
        link_inserts=human_count(EventType.LINK_INSERT),
        human_corrections=human_count(EventType.HUMAN_CORRECTION),
        recovery_events=human_count(EventType.RECOVERY),
        context_errors=human_count(EventType.CONTEXT_ERROR),
        decision_errors=human_count(EventType.DECISION_ERROR),
        cognitive_effort=effort_vals[-1] if effort_vals else None,
        task_quality=quality_vals[-1] if quality_vals else None,
        supervision_inspect=human_count(EventType.SUPERVISION_INSPECT),
        supervision_verify=human_count(EventType.SUPERVISION_VERIFY),
        supervision_reject=human_count(EventType.SUPERVISION_REJECT),
        supervision_repair=human_count(EventType.SUPERVISION_REPAIR),
        coordinator_events=coord,
        ineligible_events=ineligible,
        primary_eligible_count=primary,
    )
