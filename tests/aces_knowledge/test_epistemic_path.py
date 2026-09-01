"""Positive end-to-end path via live VerificationService (G2-R1)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

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
from aces_knowledge.services import KnowledgeUpdateService, SemanticRealityService
from aces_memory.services import MemoryService
from aces_worldmodel.services import WorldModelService

NOW = datetime(2026, 9, 1, 21, 0, 0, tzinfo=timezone.utc)
TASK, OP, RES, SCOPE = "e2e-task", "SYNTHETIC_ECHO", "synthetic://e2e", "e2e"


def test_full_positive_path_with_provenance():
    adapter = ExecutionAdapter()
    adapter.register_runtime(LocalSyntheticRuntime())
    wall = datetime.now(timezone.utc)
    auth = AuthorizationRecord(
        principal="Architectural Authority / Human",
        operation=OP, resource=RES, scope=SCOPE, task_id=TASK,
        valid_from=wall - timedelta(hours=1), valid_until=wall + timedelta(hours=2),
        approval_id="a-e2e",
    )
    r = adapter.dispatch(ExecutionRequest(
        request_id="req-e2e", intent_reference="i", operation=OP, resource=RES, scope=SCOPE,
        task_id=TASK, runtime_id=LocalSyntheticRuntime.runtime_id, authorization=auth,
        payload={}, requested_at=NOW,
    ))
    estore, vreg = InMemoryEvidenceStore(), InMemoryVerifierRegistry()
    vreg.register(VerifierRecord(verifier_id="verifier.trusted.v1", label="t", trusted=True))
    vsvc = VerificationService(evidence_store=estore, verifier_registry=vreg, ledger=InMemoryVerificationLedger())
    vsvc.register_evidence_from_result(r, evidence_id="ev-e2e-001", task_id=TASK, operation=OP, resource=RES, scope=SCOPE)
    d = vsvc.verify(r, evidence_id="ev-e2e-001", verifier_id="verifier.trusted.v1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE)
    assert d.result.accepted_state == AcceptedStateStatus.ESTABLISHED
    verified = d.result

    ksvc, msvc, wsvc, rsvc = KnowledgeUpdateService(), MemoryService(), WorldModelService(), SemanticRealityService()
    ko = ksvc.promote_from_verified_result(
        verified, content="E3.4 marker exists on branch",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    mem = msvc.consolidate_from_knowledge(knowledge=ko)
    wm = wsvc.update_from_knowledge(knowledge=ko, alpha=5, beta=1, projection="likely true")
    reality = rsvc.update_from_knowledge(knowledge=ko)

    assert reality.provenance.transformation == "knowledge_to_semantic_reality"
    assert reality.provenance.actor == "semantic_reality_service"
    assert reality.provenance.evidence_ref == "ev-e2e-001"
    assert ko.provenance.verification_ref == "verifier.trusted.v1"
    assert mem.provenance.knowledge_ref == ko.knowledge_id
    assert wm.provenance.accepted_state_ref == "ESTABLISHED"
