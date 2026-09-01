"""World Model invariant tests (post G2-R1)."""

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
from aces_knowledge.services import KnowledgeUpdateService, SemanticRealityService
from aces_worldmodel.models import BeliefState
from aces_worldmodel.services import WorldModelService

NOW = datetime(2026, 9, 1, 21, 0, 0, tzinfo=timezone.utc)
TASK, OP, RES, SCOPE = "wm-task", "SYNTHETIC_ECHO", "synthetic://wm", "wm-test"


def _ko():
    adapter = ExecutionAdapter()
    adapter.register_runtime(LocalSyntheticRuntime())
    wall = datetime.now(timezone.utc)
    auth = AuthorizationRecord(
        principal="Architectural Authority / Human",
        operation=OP, resource=RES, scope=SCOPE, task_id=TASK,
        valid_from=wall - timedelta(hours=1), valid_until=wall + timedelta(hours=2),
        approval_id="a-wm",
    )
    r = adapter.dispatch(ExecutionRequest(
        request_id="req-wm", intent_reference="i", operation=OP, resource=RES, scope=SCOPE,
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
        d.result, content="claim", task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )


def test_belief_state_requires_positive_params():
    with pytest.raises(EpistemicError, match="belief_alpha_beta"):
        BeliefState(alpha=0, beta=1)
    with pytest.raises(EpistemicError, match="belief_alpha_beta"):
        BeliefState(alpha=1, beta=-1)
    assert BeliefState(alpha=3, beta=1).mean == 0.75


def test_update_from_knowledge():
    ko = _ko()
    wm = WorldModelService().update_from_knowledge(knowledge=ko, alpha=4, beta=2)
    assert wm.belief.mean == pytest.approx(4 / 6)
    assert wm.knowledge_ref == ko.knowledge_id
    assert wm.provenance.accepted_state_ref == "ESTABLISHED"


def test_world_model_forbidden_roles():
    ko = _ko()
    wsvc = WorldModelService()
    wm = wsvc.update_from_knowledge(knowledge=ko)
    with pytest.raises(EpistemicError, match="world_model_is_not_evidence"):
        wsvc.reject_as_evidence(wm)
    with pytest.raises(EpistemicError, match="world_model_is_not_accepted_state"):
        wsvc.reject_as_accepted_state(wm)
    with pytest.raises(EpistemicError, match="world_model_is_not_authority"):
        wsvc.reject_as_authority(wm)
    with pytest.raises(EpistemicError, match="world_model_cannot_create_knowledge"):
        wsvc.reject_auto_knowledge(wm)
    with pytest.raises(EpistemicError, match="world_model_cannot_mutate_semantic_reality"):
        wsvc.reject_semantic_reality_mutation(wm)


def test_world_model_cannot_call_semantic_reality_path():
    with pytest.raises(EpistemicError, match="world_model_cannot_mutate_semantic_reality"):
        SemanticRealityService().reject_from_world_model()
