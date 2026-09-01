"""G2-R1: live VerificationService → AcceptedState → Knowledge integration."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from aces_evidence import (
    InMemoryEvidenceStore,
    InMemoryVerificationLedger,
    InMemoryVerifierRegistry,
    VerificationOutcome,
    VerificationService,
    VerifierRecord,
)
from aces_execution_adapter import (
    AcceptedStateStatus,
    AuthorizationRecord,
    ExecutionAdapter,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    LocalSyntheticRuntime,
    VerificationStatus,
)
from aces_knowledge.models import EpistemicError
from aces_knowledge.services import KnowledgeUpdateService, SemanticRealityService
from aces_memory.services import MemoryService
from aces_worldmodel.services import WorldModelService

NOW = datetime(2026, 9, 1, 21, 0, 0, tzinfo=timezone.utc)
TASK = "g2r1-task-001"
OP = "SYNTHETIC_ECHO"
RES = "synthetic://g2r1-boundary"
SCOPE = "g2r1-local only"


def _auth():
    wall = datetime.now(timezone.utc)
    return AuthorizationRecord(
        principal="Architectural Authority / Human",
        operation=OP,
        resource=RES,
        scope=SCOPE,
        task_id=TASK,
        valid_from=wall - timedelta(hours=1),
        valid_until=wall + timedelta(hours=2),
        approval_id="approval-g2r1-001",
    )


def _live_verified_path():
    """Execute real Adapter → Evidence → VerificationService → AcceptedState."""
    adapter = ExecutionAdapter()
    adapter.register_runtime(LocalSyntheticRuntime())
    req = ExecutionRequest(
        request_id="req-g2r1-1",
        intent_reference="intent:g2r1",
        operation=OP,
        resource=RES,
        scope=SCOPE,
        task_id=TASK,
        runtime_id=LocalSyntheticRuntime.runtime_id,
        authorization=_auth(),
        payload={"note": "g2r1-live"},
        requested_at=NOW,
    )
    observed = adapter.dispatch(req)
    assert observed.status == ExecutionStatus.SUCCEEDED
    assert observed.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED

    estore = InMemoryEvidenceStore()
    vreg = InMemoryVerifierRegistry()
    vreg.register(
        VerifierRecord(
            verifier_id="verifier.trusted.v1",
            label="Synthetic trusted verifier",
            trusted=True,
        )
    )
    svc = VerificationService(
        evidence_store=estore,
        verifier_registry=vreg,
        ledger=InMemoryVerificationLedger(),
    )
    evidence = svc.register_evidence_from_result(
        observed,
        evidence_id="ev-g2r1-1",
        task_id=TASK,
        operation=OP,
        resource=RES,
        scope=SCOPE,
    )
    decision = svc.verify(
        observed,
        evidence_id=evidence.evidence_id,
        verifier_id="verifier.trusted.v1",
        task_id=TASK,
        operation=OP,
        resource=RES,
        scope=SCOPE,
    )
    assert decision.outcome == VerificationOutcome.ACCEPTED
    verified = decision.result
    assert verified.accepted_state == AcceptedStateStatus.ESTABLISHED
    assert verified.verification_status == VerificationStatus.PASSED
    assert verified.provenance.get("evidence_id") == "ev-g2r1-1"
    assert verified.provenance.get("verifier_id") == "verifier.trusted.v1"
    return verified, evidence, svc


def test_live_verification_to_knowledge_promotion():
    verified, evidence, _svc = _live_verified_path()
    ksvc = KnowledgeUpdateService()
    ko = ksvc.promote_from_verified_result(
        verified,
        content="g2r1 live claim",
        task_id=TASK,
        operation=OP,
        resource=RES,
        scope=SCOPE,
    )
    assert ko.evidence_refs == ("ev-g2r1-1",)
    assert ko.provenance.evidence_ref == "ev-g2r1-1"
    assert ko.provenance.verification_ref == "verifier.trusted.v1"
    assert ko.provenance.accepted_state_ref == "ESTABLISHED"
    assert ko.provenance.execution_id == verified.request_id
    assert ko.provenance.task_id == TASK
    d = ko.to_dict()
    assert "capability" not in d
    assert "authorization" not in d


def test_live_path_to_reality_without_world_model_mutation():
    verified, evidence, _svc = _live_verified_path()
    ksvc = KnowledgeUpdateService()
    msvc = MemoryService()
    wsvc = WorldModelService()
    rsvc = SemanticRealityService()

    ko = ksvc.promote_from_verified_result(
        verified,
        content="g2r1 reality claim",
        task_id=TASK,
        operation=OP,
        resource=RES,
        scope=SCOPE,
    )
    mem = msvc.consolidate_from_knowledge(knowledge=ko)
    wm = wsvc.update_from_knowledge(knowledge=ko)
    reality = rsvc.update_from_knowledge(knowledge=ko)

    assert reality.knowledge_ref == ko.knowledge_id
    assert reality.provenance.actor == "semantic_reality_service"
    assert reality.provenance.transformation == "knowledge_to_semantic_reality"
    assert reality.provenance.evidence_ref == "ev-g2r1-1"
    assert mem.provenance.evidence_ref == "ev-g2r1-1"
    assert wm.provenance.accepted_state_ref == "ESTABLISHED"
    assert reality.provenance.actor != "world_model_service"


def test_status_token_alone_insufficient():
    ksvc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="status_token_insufficient"):
        ksvc.promote_from_accepted_state(
            accepted_state="ESTABLISHED",
            evidence_id="ev-fake",
            verification_ref="ver-fake",
            content="should fail",
        )


def test_fabricated_established_without_provenance_rejected():
    ksvc = KnowledgeUpdateService()
    fabricated = ExecutionResult(
        request_id="req-fabricated",
        status=ExecutionStatus.SUCCEEDED,
        runtime_id="local-synthetic",
        observed={"note": "forged"},
        provenance={},
        verification_status=VerificationStatus.PASSED,
        accepted_state=AcceptedStateStatus.ESTABLISHED,
    )
    with pytest.raises(EpistemicError, match="evidence_binding_required"):
        ksvc.promote_from_verified_result(
            fabricated,
            content="forged claim",
            task_id=TASK,
            operation=OP,
            resource=RES,
            scope=SCOPE,
        )


def test_succeeded_without_accepted_state_rejected():
    ksvc = KnowledgeUpdateService()
    r = ExecutionResult(
        request_id="req-x",
        status=ExecutionStatus.SUCCEEDED,
        runtime_id="local-synthetic",
        observed={},
        provenance={"evidence_id": "ev-1", "verifier_id": "v1"},
        verification_status=VerificationStatus.PENDING,
        accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
    )
    with pytest.raises(EpistemicError, match="accepted_state_required"):
        ksvc.promote_from_verified_result(
            r,
            content="x",
            task_id=TASK,
            operation=OP,
            resource=RES,
            scope=SCOPE,
        )


def test_execution_success_alone_not_knowledge():
    adapter = ExecutionAdapter()
    adapter.register_runtime(LocalSyntheticRuntime())
    req = ExecutionRequest(
        request_id="req-success-only",
        intent_reference="intent:x",
        operation=OP,
        resource=RES,
        scope=SCOPE,
        task_id=TASK,
        runtime_id=LocalSyntheticRuntime.runtime_id,
        authorization=_auth(),
        payload={},
        requested_at=NOW,
    )
    r = adapter.dispatch(req)
    assert r.status == ExecutionStatus.SUCCEEDED
    assert r.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED
    ksvc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="accepted_state_required"):
        ksvc.promote_from_verified_result(
            r,
            content="from success only",
            task_id=TASK,
            operation=OP,
            resource=RES,
            scope=SCOPE,
        )
