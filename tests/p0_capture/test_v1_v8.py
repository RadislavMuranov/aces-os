"""Controlled validation V1–V8 for P0.3.2-III capture adapter."""

from datetime import datetime, timedelta, timezone

from src.p0_capture import (
    Actor,
    CaptureAdapter,
    EventType,
    ProvenanceConfidence,
    SurfaceAllowList,
    compute_hcc_from_capture,
)
from src.p0_capture.schema import CaptureEvent


def _adapter() -> CaptureAdapter:
    al = SurfaceAllowList()
    for s in ("gmail", "docs", "github", "calendar", "chat", "experiment"):
        al.add(s)
    return CaptureAdapter(session_id="val-s1", allowlist=al)


def test_v1_human_search_copy_paste_navigation():
    a = _adapter()
    a.start_unit("u1")
    e_search = a.observe_human(EventType.SEARCH, "gmail", artifact_id="msg-1")
    e_copy = a.observe_human(EventType.COPY, "docs", content_for_hash="spec text")
    e_paste = a.observe_human(EventType.PASTE, "github", content_for_hash="spec text")
    e_nav = a.observe_human(EventType.NAVIGATION, "github", artifact_id="pr-1")
    e_switch = a.observe_human(EventType.APP_SWITCH, "calendar")
    a.end_unit()
    for e in (e_search, e_copy, e_paste, e_nav, e_switch):
        assert e.actor is Actor.HUMAN
        assert e.provenance_confidence is ProvenanceConfidence.HIGH
        assert e.primary_analysis_eligible is True
        assert e.content_hash is None or len(e.content_hash) == 16
    snap = compute_hcc_from_capture(a.events, a.missing)
    assert snap.searches == 1
    assert snap.copy_ops == 1
    assert snap.paste_ops == 1
    assert snap.navigations == 1
    assert snap.app_switches == 1
    assert snap.coordinator_events == 0


def test_v2_coordinator_tagged_channel():
    a = _adapter()
    a.start_unit("u1")
    e = a.emit_coordinator(EventType.COORDINATOR_SUGGEST, payload={"text": "open related PR"})
    a.end_unit()
    assert e.actor is Actor.COORDINATOR
    assert e.primary_analysis_eligible is False
    assert e.source == "coordinator_channel"
    snap = compute_hcc_from_capture(a.events, a.missing)
    assert snap.coordinator_events == 1
    assert snap.searches == 0
    assert snap.app_switches == 0


def test_v3_system_event():
    a = _adapter()
    e = a.observe_system(payload={"kind": "notification"})
    assert e.actor is Actor.SYSTEM
    assert e.primary_analysis_eligible is False
    snap = compute_hcc_from_capture(a.events, a.missing)
    assert snap.system_events == 1
    assert snap.app_switches == 0


def test_v4_unknown_surface_insufficient():
    a = _adapter()
    e = a.observe_unknown_surface(EventType.SEARCH, "personal-browser")
    assert e.provenance_confidence is ProvenanceConfidence.INSUFFICIENT
    assert e.primary_analysis_eligible is False
    assert e.ambiguous is True
    snap = compute_hcc_from_capture(a.events, a.missing)
    assert snap.searches == 0
    assert snap.ineligible_events >= 1


def test_v4_human_on_disallowed_surface():
    a = _adapter()
    e = a.observe_human(EventType.COPY, "slack-personal", content_for_hash="secret")
    assert e.provenance_confidence is ProvenanceConfidence.INSUFFICIENT
    assert e.primary_analysis_eligible is False
    assert e.content_hash is not None
    assert "secret" not in (e.content_hash or "")
    assert e.payload.get("content") is None


def test_v5_coordinator_does_not_inflate_hcc():
    a = _adapter()
    a.start_unit("u1")
    for _ in range(8):
        a.emit_coordinator(EventType.COORDINATOR_SUGGEST)
    a.end_unit()
    snap = compute_hcc_from_capture(a.events, a.missing)
    assert snap.coordinator_events == 8
    assert snap.app_switches == 0
    assert snap.searches == 0
    assert snap.copy_ops == 0
    assert snap.paste_ops == 0
    assert snap.navigations == 0
    assert snap.human_corrections == 0


def test_v6_no_unrelated_content_captured():
    a = _adapter()
    e = a.observe_unknown_surface(
        EventType.NAVIGATION,
        "/home/user/private/taxes.pdf",
        payload={"note": "should not store path body"},
    )
    assert e.primary_analysis_eligible is False
    assert e.content_hash is None
    snap = compute_hcc_from_capture(a.events, a.missing)
    assert snap.navigations == 0


def test_v6_clipboard_stores_hash_not_raw():
    a = _adapter()
    raw = "CONFIDENTIAL contract text 999"
    e = a.observe_human(EventType.COPY, "docs", content_for_hash=raw)
    assert e.content_hash is not None
    assert raw not in e.content_hash
    assert e.payload.get("text") is None


def test_v7_monotonic_timestamps_and_duration():
    a2 = _adapter()
    t0 = datetime(2026, 8, 29, 18, 0, 0, tzinfo=timezone.utc)
    start = CaptureEvent.make(
        session_id=a2.session_id,
        event_type=EventType.TASK_START,
        actor=Actor.HUMAN,
        experiment_surface="experiment",
        provenance_confidence=ProvenanceConfidence.HIGH,
        primary_analysis_eligible=False,
        timestamp=t0,
    )
    mid = CaptureEvent.make(
        session_id=a2.session_id,
        event_type=EventType.SEARCH,
        actor=Actor.HUMAN,
        experiment_surface="gmail",
        provenance_confidence=ProvenanceConfidence.HIGH,
        primary_analysis_eligible=True,
        timestamp=t0 + timedelta(seconds=10),
    )
    end = CaptureEvent.make(
        session_id=a2.session_id,
        event_type=EventType.TASK_END,
        actor=Actor.HUMAN,
        experiment_surface="experiment",
        provenance_confidence=ProvenanceConfidence.HIGH,
        primary_analysis_eligible=False,
        timestamp=t0 + timedelta(seconds=45),
    )
    a2.events.extend([start, mid, end])
    ts = [e.timestamp for e in a2.events]
    assert ts == sorted(ts)
    snap = compute_hcc_from_capture(a2.events, a2.missing)
    assert snap.wall_clock_seconds == 45.0
    assert snap.searches == 1


def test_v8_missing_event_explicit_not_zero():
    a = _adapter()
    a.start_unit("u1")
    a.observe_human(EventType.SEARCH, "gmail")
    a.record_missing(EventType.APP_SWITCH, reason="capture gap: focus observer unavailable")
    a.end_unit()
    assert a.unit_incomplete() is True
    assert len(a.missing) == 1
    assert a.missing[0].expected_type is EventType.APP_SWITCH
    snap = compute_hcc_from_capture(a.events, a.missing)
    assert snap.unit_incomplete is True
    assert snap.missing_count == 1
    assert snap.searches == 1
    assert snap.app_switches == 0


def test_pause_outside_allowlist():
    a = _adapter()
    a.pause_outside_allowlist()
    e = a.observe_human(EventType.SEARCH, "gmail")
    assert e.primary_analysis_eligible is False
    a.resume_on_allowlist()
    e2 = a.observe_human(EventType.SEARCH, "gmail")
    assert e2.primary_analysis_eligible is True
