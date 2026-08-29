"""Provenance and integrity tests for P0.3.2-I instrumentation."""

from datetime import datetime, timedelta, timezone

from src.p0_instrumentation.events import (
    Actor,
    EventType,
    InstrumentationEvent,
    ProvenanceConfidence,
)
from src.p0_instrumentation.recorder import EventRecorder
from src.p0_instrumentation.hcc import compute_hcc_components


def _rec() -> EventRecorder:
    return EventRecorder(session_id="s1", participant_id="p1")


def test_human_event_classified_as_human():
    r = _rec()
    e = r.record_explicit(
        unit_id="u1",
        actor=Actor.HUMAN,
        system_surface="gmail",
        event_type=EventType.SEARCH,
    )
    assert e.actor is Actor.HUMAN
    assert e.primary_analysis_eligible is True


def test_coordinator_event_classified_as_coordinator():
    r = _rec()
    e = r.record_explicit(
        unit_id="u1",
        actor=Actor.COORDINATOR,
        system_surface="coordinator",
        event_type=EventType.COORDINATOR_SUGGEST,
    )
    assert e.actor is Actor.COORDINATOR
    assert e.primary_analysis_eligible is False


def test_system_event_classified_as_system():
    r = _rec()
    e = r.record_explicit(
        unit_id="u1",
        actor=Actor.SYSTEM,
        system_surface="os",
        event_type=EventType.SYSTEM_NOISE,
    )
    assert e.actor is Actor.SYSTEM
    assert e.primary_analysis_eligible is False


def test_ambiguous_event_ineligible():
    r = _rec()
    e = r.record_explicit(
        unit_id="u1",
        actor=Actor.HUMAN,
        system_surface="docs",
        event_type=EventType.SEARCH,
        provenance_confidence=ProvenanceConfidence.INSUFFICIENT,
    )
    assert e.primary_analysis_eligible is False


def test_coordinator_cannot_become_human_in_hcc():
    r = _rec()
    r.record_explicit(
        unit_id="u1",
        actor=Actor.COORDINATOR,
        system_surface="coordinator",
        event_type=EventType.COORDINATOR_SUGGEST,
    )
    r.record_explicit(
        unit_id="u1",
        actor=Actor.HUMAN,
        system_surface="github",
        event_type=EventType.APP_SWITCH,
    )
    comps = compute_hcc_components(r.events_for_unit("u1"))
    assert comps.coordinator_events == 1
    assert comps.app_switches == 1
    assert comps.searches == 0


def test_task_duration():
    r = _rec()
    t0 = datetime(2026, 8, 29, 12, 0, 0, tzinfo=timezone.utc)
    t1 = t0 + timedelta(seconds=125)
    start = InstrumentationEvent.create(
        session_id="s1",
        participant_id="p1",
        unit_id="u1",
        actor=Actor.HUMAN,
        system_surface="experiment",
        event_type=EventType.TASK_START,
        timestamp=t0,
    )
    end = InstrumentationEvent.create(
        session_id="s1",
        participant_id="p1",
        unit_id="u1",
        actor=Actor.HUMAN,
        system_surface="experiment",
        event_type=EventType.TASK_END,
        timestamp=t1,
    )
    r.record(start)
    r.record(end)
    comps = compute_hcc_components(r.events_for_unit("u1"))
    assert comps.wall_clock_seconds == 125.0


def test_copy_paste_link_recorded():
    r = _rec()
    for et in (EventType.COPY, EventType.PASTE, EventType.LINK_INSERT):
        r.record_explicit(
            unit_id="u1",
            actor=Actor.HUMAN,
            system_surface="docs",
            event_type=et,
        )
    comps = compute_hcc_components(r.events_for_unit("u1"))
    assert comps.copy_ops == 1
    assert comps.paste_ops == 1
    assert comps.link_inserts == 1


def test_correction_and_recovery():
    r = _rec()
    r.record_explicit(
        unit_id="u1",
        actor=Actor.HUMAN,
        system_surface="github",
        event_type=EventType.HUMAN_CORRECTION,
    )
    r.record_explicit(
        unit_id="u1",
        actor=Actor.HUMAN,
        system_surface="github",
        event_type=EventType.RECOVERY,
    )
    comps = compute_hcc_components(r.events_for_unit("u1"))
    assert comps.human_corrections == 1
    assert comps.recovery_events == 1


def test_supervision_cost_separated():
    r = _rec()
    for et in (
        EventType.SUPERVISION_INSPECT,
        EventType.SUPERVISION_VERIFY,
        EventType.SUPERVISION_REJECT,
        EventType.SUPERVISION_REPAIR,
    ):
        r.record_explicit(
            unit_id="u1",
            actor=Actor.HUMAN,
            system_surface="coordinator",
            event_type=et,
        )
    comps = compute_hcc_components(r.events_for_unit("u1"))
    assert comps.supervision_inspect == 1
    assert comps.supervision_verify == 1
    assert comps.supervision_reject == 1
    assert comps.supervision_repair == 1
    assert comps.app_switches == 0


def test_synthetic_step_count_cannot_enter_hcc():
    r = _rec()
    r.record_explicit(
        unit_id="u1",
        actor=Actor.SYSTEM,
        system_surface="harness",
        event_type=EventType.SYSTEM_NOISE,
        payload={"synthetic_step": 5},
    )
    comps = compute_hcc_components(r.events_for_unit("u1"))
    assert comps.app_switches == 0
    assert comps.searches == 0
    assert comps.coordinator_events == 0


def test_automation_intervention_count_not_in_hcc():
    r = _rec()
    for _ in range(8):
        r.record_explicit(
            unit_id="u1",
            actor=Actor.COORDINATOR,
            system_surface="coordinator",
            event_type=EventType.COORDINATOR_SUGGEST,
        )
    comps = compute_hcc_components(r.events_for_unit("u1"))
    assert comps.coordinator_events == 8
    assert comps.primary_eligible_count == 0
    assert comps.app_switches == 0
    assert comps.searches == 0


def test_low_confidence_excluded():
    r = _rec()
    r.record_explicit(
        unit_id="u1",
        actor=Actor.HUMAN,
        system_surface="gmail",
        event_type=EventType.SEARCH,
        provenance_confidence=ProvenanceConfidence.LOW,
    )
    comps = compute_hcc_components(r.events_for_unit("u1"))
    assert comps.searches == 0
    assert comps.ineligible_events >= 1
