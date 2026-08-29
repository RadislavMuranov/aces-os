"""HCC snapshot from capture events — human eligible only."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from .schema import Actor, CaptureEvent, EventType, MissingEvent, ProvenanceConfidence


@dataclass(frozen=True)
class HCCSnapshot:
    wall_clock_seconds: float | None
    app_switches: int
    navigations: int
    searches: int
    refinds: int
    copy_ops: int
    paste_ops: int
    link_inserts: int
    human_corrections: int
    recovery_events: int
    coordinator_events: int
    system_events: int
    ineligible_events: int
    missing_count: int
    unit_incomplete: bool
    supervision_total: int


def compute_hcc_from_capture(
    events: Sequence[CaptureEvent],
    missing: Sequence[MissingEvent] | None = None,
) -> HCCSnapshot:
    missing = missing or []

    def hcount(et: EventType) -> int:
        return sum(
            1
            for e in events
            if e.event_type is et
            and e.actor is Actor.HUMAN
            and e.primary_analysis_eligible
            and e.provenance_confidence
            not in (ProvenanceConfidence.LOW, ProvenanceConfidence.INSUFFICIENT)
        )

    starts = [e for e in events if e.event_type is EventType.TASK_START]
    ends = [e for e in events if e.event_type is EventType.TASK_END]
    wall = None
    if starts and ends:
        t0 = min(e.timestamp for e in starts)
        t1 = max(e.timestamp for e in ends)
        wall = max(0.0, (t1 - t0).total_seconds())

    coord = sum(1 for e in events if e.actor is Actor.COORDINATOR)
    system = sum(1 for e in events if e.actor is Actor.SYSTEM)
    ineligible = sum(1 for e in events if not e.primary_analysis_eligible)
    supervision = sum(
        1
        for e in events
        if e.actor is Actor.HUMAN and e.event_type.value.startswith("supervision_")
    )

    return HCCSnapshot(
        wall_clock_seconds=wall,
        app_switches=hcount(EventType.APP_SWITCH),
        navigations=hcount(EventType.NAVIGATION),
        searches=hcount(EventType.SEARCH),
        refinds=hcount(EventType.REFIND),
        copy_ops=hcount(EventType.COPY),
        paste_ops=hcount(EventType.PASTE),
        link_inserts=hcount(EventType.LINK_INSERT),
        human_corrections=hcount(EventType.HUMAN_CORRECTION),
        recovery_events=hcount(EventType.RECOVERY),
        coordinator_events=coord,
        system_events=system,
        ineligible_events=ineligible,
        missing_count=len(missing),
        unit_incomplete=len(missing) > 0,
        supervision_total=supervision,
    )
