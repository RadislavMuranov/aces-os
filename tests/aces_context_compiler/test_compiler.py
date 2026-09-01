"""E3.1 Context Compiler tests T1–T10."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from aces_context_compiler import (
    COMPILER_VERSION,
    CompilationError,
    ContextCompiler,
    EpistemicStatus,
    SourceContribution,
    Unknown,
)


TS = datetime(2026, 9, 1, 17, 0, 0, tzinfo=timezone.utc)
TS2 = datetime(2026, 9, 1, 16, 0, 0, tzinfo=timezone.utc)


def _src(
    *,
    owner: str = "Gmail",
    oid: str = "msg-1",
    state: str = "meeting Wed 10:00",
    claim: str | None = "meeting_time",
    status: EpistemicStatus = EpistemicStatus.OBSERVED,
    authority: str = "read-only",
    prov: str = "gmail:msg-1",
    perms: tuple[str, ...] = ("READ",),
    source_ts: datetime | None = TS,
) -> SourceContribution:
    return SourceContribution(
        owner_system=owner,
        source_object_id=oid,
        retrieval_timestamp=TS,
        source_type="message",
        observed_state=state,
        access_authority=authority,
        provenance_reference=prov,
        epistemic_status=status,
        source_timestamp=source_ts,
        claim_key=claim,
        permissions=perms,
    )


def test_t1_basic_compilation():
    c = ContextCompiler()
    result = c.compile(
        task="Reconstruct Aurora continuity",
        sources=[_src()],
        task_id="aurora-001",
        package_id="pkg-fixed",
        compiled_at=TS,
        run_id="run-fixed",
    )
    pkg = result.package
    assert pkg.task == "Reconstruct Aurora continuity"
    assert len(pkg.context_items) == 1
    item = pkg.context_items[0]
    assert item.owner_system == "Gmail"
    assert item.source_ref == "msg-1"
    assert item.observed_state == "meeting Wed 10:00"
    assert item.epistemic_status is EpistemicStatus.OBSERVED
    assert pkg.compiler_version == COMPILER_VERSION
    assert pkg.package_id == "pkg-fixed"


def test_t2_provenance_preservation():
    c = ContextCompiler()
    result = c.compile("t", [_src(prov="gmail:1a05dd3d5f1fcc21")])
    item = result.package.context_items[0]
    assert item.provenance.provenance_reference == "gmail:1a05dd3d5f1fcc21"
    assert item.provenance.owner_system == "Gmail"
    assert item.provenance.source_ref == "msg-1"
    assert item.provenance.access_authority == "read-only"
    assert len(result.package.provenance) == 1


def test_t3_unknown_not_converted_to_observed():
    c = ContextCompiler()
    src = _src(
        oid="gap-1",
        state="briefing status not found in scope",
        status=EpistemicStatus.UNKNOWN,
        claim="briefing_status",
        prov="gmail:search-empty",
    )
    result = c.compile("t", [src])
    item = result.package.context_items[0]
    assert item.epistemic_status is EpistemicStatus.UNKNOWN
    assert item.epistemic_status is not EpistemicStatus.OBSERVED
    assert any(u.reason == "briefing status not found in scope" for u in result.package.unknowns)


def test_t3_explicit_unknown_object():
    c = ContextCompiler()
    unk = Unknown(
        unknown_id="unk-manual",
        reason="no residual Friday authority known",
        source_scope="Calendar",
        checked_at=TS.isoformat(),
        claim_key="friday_authority",
    )
    result = c.compile("t", [_src()], unknowns=[unk])
    assert any(u.reason == "no residual Friday authority known" for u in result.package.unknowns)


def test_t4_inferred_not_promoted_to_observed():
    c = ContextCompiler()
    src = _src(
        oid="inf-1",
        state="likely Wednesday preferred",
        status=EpistemicStatus.INFERRED,
        claim="meeting_preference",
        prov="agent:inference-1",
    )
    result = c.compile("t", [src])
    item = result.package.context_items[0]
    assert item.epistemic_status is EpistemicStatus.INFERRED
    assert item.epistemic_status is not EpistemicStatus.OBSERVED


def test_t5_conflict_preserves_both_observations():
    c = ContextCompiler()
    a = _src(oid="msg-wed", state="Wednesday 10:00", claim="meeting_time", prov="gmail:wed")
    b = _src(oid="msg-fri", state="Friday 15:00", claim="meeting_time", prov="gmail:fri", source_ts=TS2)
    result = c.compile("t", [a, b])
    pkg = result.package
    assert len(pkg.context_items) == 2
    states = {i.observed_state for i in pkg.context_items}
    assert states == {"Wednesday 10:00", "Friday 15:00"}
    assert len(pkg.conflicts) == 1
    conf = pkg.conflicts[0]
    assert conf.claim_key == "meeting_time"
    assert conf.resolved is False
    assert conf.resolution is None
    assert set(conf.observations) == {"Wednesday 10:00", "Friday 15:00"}


def test_t6_owner_preservation():
    c = ContextCompiler()
    a = _src(owner="Gmail", oid="m1", state="s1", claim="k1", prov="g:1")
    b = _src(owner="Google Calendar", oid="e1", state="s2", claim="k2", prov="c:1")
    result = c.compile("t", [a, b])
    owners = {i.owner_system for i in result.package.context_items}
    assert owners == {"Gmail", "Google Calendar"}
    for item in result.package.context_items:
        assert item.owner_system == item.provenance.owner_system


def test_t7_compilation_does_not_create_authorization():
    c = ContextCompiler()
    src = _src(perms=("READ",))
    result = c.compile("t", [src], suggested_next_action="update calendar event")
    pkg = result.package
    assert "WRITE" not in pkg.permissions
    assert "AUTHORIZE" not in pkg.permissions
    assert pkg.permissions == ("READ",)
    assert result.evidence.verification_result is None
    assert result.evidence.accepted_state_reference is None
    assert result.evidence.execution_reference is None


def test_t8_deterministic_material_equivalence():
    c = ContextCompiler()
    sources = [
        _src(oid="msg-wed", state="Wednesday 10:00", claim="meeting_time", prov="g:wed"),
        _src(oid="msg-fri", state="Friday 15:00", claim="meeting_time", prov="g:fri"),
    ]
    r1 = c.compile("Reconstruct Aurora", sources, task_id="aurora-001", package_id="pkg-1", compiled_at=TS, run_id="run-1")
    r2 = c.compile("Reconstruct Aurora", sources, task_id="aurora-001", package_id="pkg-2", compiled_at=TS2, run_id="run-2")
    assert r1.package.material_fingerprint() == r2.package.material_fingerprint()
    assert [i.id for i in r1.package.context_items] == [i.id for i in r2.package.context_items]


def test_t9_audit_record_complete():
    c = ContextCompiler()
    result = c.compile(
        "t",
        [_src()],
        task_id="task-9",
        human_interventions=["operator confirmed read-only"],
        agent_actions=["retrieve gmail", "compile"],
        decision_point="pre-decision context only",
        run_id="run-9",
    )
    ev = result.evidence
    assert ev.run_id == "run-9"
    assert ev.task_id == "task-9"
    assert ev.compiler_version == COMPILER_VERSION
    assert "Gmail" in ev.source_systems
    assert "msg-1" in ev.source_objects
    assert len(ev.context_item_ids) == 1
    assert ev.started_at is not None
    assert ev.completed_at is not None
    assert ev.elapsed_ms is not None and ev.elapsed_ms >= 0
    assert ev.material_fingerprint is not None
    assert ev.error is None


def test_t10_missing_provenance_fails_closed():
    c = ContextCompiler()
    with pytest.raises(CompilationError):
        SourceContribution(
            owner_system="Gmail",
            source_object_id="msg-x",
            retrieval_timestamp=TS,
            source_type="message",
            observed_state="x",
            access_authority="read",
            provenance_reference="",
        ).validate()
    bad = SourceContribution(
        owner_system="Gmail",
        source_object_id="msg-x",
        retrieval_timestamp=TS,
        source_type="message",
        observed_state="x",
        access_authority="read",
        provenance_reference="",
    )
    with pytest.raises(CompilationError):
        c.compile("t", [bad])


def test_t10_empty_task_fails_closed():
    c = ContextCompiler()
    with pytest.raises(CompilationError):
        c.compile("  ", [_src()])


def test_t10_missing_owner_fails_closed():
    c = ContextCompiler()
    bad = SourceContribution(
        owner_system="",
        source_object_id="msg-x",
        retrieval_timestamp=TS,
        source_type="message",
        observed_state="x",
        access_authority="read",
        provenance_reference="ref",
    )
    with pytest.raises(CompilationError):
        c.compile("t", [bad])
