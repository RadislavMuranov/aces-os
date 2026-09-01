"""Knowledge promotion and Semantic Reality boundary tests."""

from __future__ import annotations

import pytest

from aces_knowledge.models import (
    EpistemicError,
    KnowledgeObjectType,
    TruthLevel,
    VerificationState,
)
from aces_knowledge.services import KnowledgeUpdateService, SemanticRealityService


def test_promote_from_accepted_state_creates_knowledge():
    svc = KnowledgeUpdateService()
    ko = svc.promote_from_accepted_state(
        accepted_state="ESTABLISHED",
        evidence_id="ev-1",
        verification_ref="ver-1",
        content="marker created",
        task_id="task-1",
        execution_id="exec-1",
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
    with pytest.raises(EpistemicError, match="accepted_state_required"):
        svc.promote_from_accepted_state(
            accepted_state="NOT_ESTABLISHED",
            evidence_id="ev-1",
            verification_ref="ver-1",
            content="x",
        )


def test_missing_evidence_binding_rejected():
    svc = KnowledgeUpdateService()
    with pytest.raises(EpistemicError, match="evidence_binding_required"):
        svc.promote_from_accepted_state(
            accepted_state="ESTABLISHED",
            evidence_id="",
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
    ksvc = KnowledgeUpdateService()
    rsvc = SemanticRealityService()
    ko = ksvc.promote_from_accepted_state(
        accepted_state="ESTABLISHED",
        evidence_id="ev-1",
        verification_ref="ver-1",
        content="reality claim",
        task_id="t1",
    )
    reality = rsvc.update_from_knowledge(knowledge=ko)
    assert reality.knowledge_ref == ko.knowledge_id
    assert reality.claim == "reality claim"
    assert reality.provenance.knowledge_ref == ko.knowledge_id
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
    """AcceptedState ≠ Authorization: promotion never returns capabilities."""
    svc = KnowledgeUpdateService()
    ko = svc.promote_from_accepted_state(
        accepted_state="ESTABLISHED",
        evidence_id="ev-1",
        verification_ref="ver-1",
        content="x",
    )
    assert not hasattr(ko, "capability_id")
    d = ko.to_dict()
    assert "capability" not in d
    assert "authorization" not in d
