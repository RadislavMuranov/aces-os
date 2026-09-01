"""Knowledge promotion and Semantic Reality boundary tests (post G2-R1)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from aces_evidence import (
    InMemoryEvidenceStore,
    InMemoryVerificationLedger,
    InMemoryVerifierRegistry,
    VerificationService,
    VerifierRecord,
)
from aces_execution_adapter import (
    AcceptedStateStatus,
    AuthorizationRecord,
    ExecutionAdapter,
    ExecutionRequest,
    LocalSyntheticRuntime,
)
from aces_knowledge.models import (
    EpistemicError,
    KnowledgeObjectType,
    TruthLevel,
    VerificationState,
)
from aces_knowledge.services import KnowledgeUpdateService, SemanticRealityService

NOW = datetime(2026, 9, 1, 21, 0, 0, tzinfo=timezone.utc)
TASK = "ko-task"
OP = "SYNTHETIC_ECHO"
RES = "synthetic://ko"
SCOPE = "ko-test"


def _verified_result():
    adapter = ExecutionAdapter()
    adapter.register_runtime(LocalSyntheticRuntime())
    wall = datetime.now(timezone.utc)
    auth = AuthorizationRecord(
        principal="Architectural Authority / Human",
        operation=OP,
        resource=RES,
        scope=SCOPE,
        task_id=TASK,
        valid_from=wall - timedelta(hours=1),
        valid_until=wall + timedelta(hours=2),
        approval_id="approval-ko",
    )
    req = ExecutionRequest(
        request_id="req-ko-1",
        intent_reference="intent:ko",
        operation=OP,
        resource=RES,
        scope=SCOPE,
        task_id=TASK,
        runtime_id=LocalSyntheticRuntime.runtime_id,
        authorization=auth,
        payload={"note": "ko"},
        requested_at=NOW,
    )
    r = adapter.dispatch(req)
    estore = InMemoryEvidenceStore()
    vreg = InMemoryVerifierRegistry()
    vreg.register(VerifierRecord(verifier_id="verifier.trusted.v1", label="t", trusted=True))
    svc = VerificationService(evidence_store=estore, verifier_registry=vreg, ledger=InMemoryVerificationLedger())
    svc.register_evidence_from_result(r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE)
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.result.accepted_state == AcceptedStateStatus.ESTABLISHED
    return d.result


def test_promote_from_verified_result_creates_knowledge():
    verified = _verified_result()
    svc = KnowledgeUpdateService()
    ko = svc.promote_from_verified_result(
        verified,
        content="marker created",
        task_id=TASK,
        operation=OP,
        resource=RES,
        scope=SCOPE,
    )
    assert ko.object_type == KnowledgeObjectType.FACT
    assert ko.truth_level == TruthLevel.WORKING
    assert ko.verification_state == VerificationState.VERIFIED
    assert ko.evidence_refs == ("ev-1",)
    assert ko.provenance.accepted_state_ref == "ESTABLISHED"
    assert ko.provenance.evidence_ref == "ev-1"


def test_execution_success_alone_not_knowledge():
    svc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="execution_success_is_not_knowledge"):
        svc.reject_execution_success_alone(execution_status="SUCCEEDED")


def test_evidence_without_accepted_state_not_knowledge():
    svc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="evidence_without_accepted_state"):
        svc.reject_evidence_without_accepted_state(evidence_id="ev-1")


def test_status_token_path_rejected():
    svc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="status_token_insufficient"):
        svc.promote_from_accepted_state(
            accepted_state="ESTABLISHED",
            evidence_id="ev-1",
            verification_ref="ver-1",
            content="x",
        )


def test_agent_assertion_not_knowledge():
    svc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="agent_assertion"):
        svc.reject_agent_assertion(assertion="I claim this is true")


def test_world_model_cannot_create_knowledge():
    svc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="world_model_cannot_create_knowledge"):
        svc.reject_world_model_auto_knowledge()


def test_knowledge_is_not_authority():
    svc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="knowledge_is_not_authority"):
        svc.reject_knowledge_as_authorization()


def test_semantic_reality_from_knowledge():
    verified = _verified_result()
    ksvc = KnowledgeUpdateService()
    rsvc = SemanticRealityService()
    ko = ksvc.promote_from_verified_result(
        verified, content="reality claim", task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    reality = rsvc.update_from_knowledge(knowledge=ko)
    assert reality.knowledge_ref == ko.knowledge_id
    assert reality.claim == "reality claim"
    assert reality.provenance.accepted_state_ref == "ESTABLISHED"
    assert reality.provenance.evidence_ref == "ev-1"


def test_semantic_reality_rejects_memory_world_model_execution_agent():
    rsvc = SemanticRealityService()
    with pytest.raises(EpistemicError, match="memory_cannot_mutate"):
        rsvc.reject_from_memory()
    with pytest.raises(EpistemicError, match="world_model_cannot_mutate"):
        rsvc.reject_from_world_model()
    with pytest.raises(EpistemicError, match="execution_success_cannot_mutate"):
        rsvc.reject_from_execution_success()
    with pytest.raises(EpistemicError, match="unverified_evidence"):
        rsvc.reject_from_unverified_evidence()
    with pytest.raises(EpistemicError, match="agent_assertion_cannot_mutate"):
        rsvc.reject_from_agent_assertion()


def test_accepted_state_does_not_issue_capabilities():
    verified = _verified_result()
    svc = KnowledgeUpdateService()
    ko = svc.promote_from_verified_result(
        verified, content="x", task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert not hasattr(ko, "capability_id")
    d = ko.to_dict()
    assert "capability" not in d
    assert "authorization" not in d
