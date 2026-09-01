"""Memory layer invariant tests (post G2-R1)."""

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
from aces_knowledge.models import EpistemicError
from aces_knowledge.services import KnowledgeUpdateService
from aces_memory.services import MemoryService

NOW = datetime(2026, 9, 1, 21, 0, 0, tzinfo=timezone.utc)
TASK, OP, RES, SCOPE = "mem-task", "SYNTHETIC_ECHO", "synthetic://mem", "mem-test"


def _ko():
    adapter = ExecutionAdapter()
    adapter.register_runtime(LocalSyntheticRuntime())
    wall = datetime.now(timezone.utc)
    auth = AuthorizationRecord(
        principal="Architectural Authority / Human",
        operation=OP, resource=RES, scope=SCOPE, task_id=TASK,
        valid_from=wall - timedelta(hours=1), valid_until=wall + timedelta(hours=2),
        approval_id="a-mem",
    )
    r = adapter.dispatch(ExecutionRequest(
        request_id="req-mem", intent_reference="i", operation=OP, resource=RES, scope=SCOPE,
        task_id=TASK, runtime_id=LocalSyntheticRuntime.runtime_id, authorization=auth,
        payload={}, requested_at=NOW,
    ))
    estore, vreg = InMemoryEvidenceStore(), InMemoryVerifierRegistry()
    vreg.register(VerifierRecord(verifier_id="verifier.trusted.v1", label="t", trusted=True))
    svc = VerificationService(evidence_store=estore, verifier_registry=vreg, ledger=InMemoryVerificationLedger())
    svc.register_evidence_from_result(r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE)
    d = svc.verify(r, evidence_id="ev-1", verifier_id="verifier.trusted.v1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE)
    assert d.result.accepted_state == AcceptedStateStatus.ESTABLISHED
    return KnowledgeUpdateService().promote_from_verified_result(
        d.result, content="remembered claim", task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )


def test_consolidate_from_knowledge():
    ko = _ko()
    mem = MemoryService().consolidate_from_knowledge(knowledge=ko)
    assert mem.content == "remembered claim"
    assert mem.knowledge_ref == ko.knowledge_id
    assert mem.accepted_state_ref == "ESTABLISHED"


def test_memory_not_evidence_truth_authority_verification():
    ko = _ko()
    msvc = MemoryService()
    mem = msvc.consolidate_from_knowledge(knowledge=ko)
    with pytest.raises(EpistemicError, match="memory_is_not_evidence"):
        msvc.reject_as_evidence(mem)
    with pytest.raises(EpistemicError, match="memory_is_not_truth"):
        msvc.reject_as_truth(mem)
    with pytest.raises(EpistemicError, match="memory_is_not_authority"):
        msvc.reject_as_authority(mem)
    with pytest.raises(EpistemicError, match="memory_is_not_verification"):
        msvc.reject_as_verification(mem)


def test_memory_append_history_preserved():
    ko = _ko()
    msvc = MemoryService()
    m1 = msvc.consolidate_from_knowledge(knowledge=ko)
    m2 = msvc.consolidate_from_knowledge(knowledge=ko)
    hist = msvc.store.history()
    assert len(hist) == 2
    assert hist[0].memory_id == m1.memory_id
    assert hist[1].memory_id == m2.memory_id
