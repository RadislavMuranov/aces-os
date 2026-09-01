"""World Model invariant tests (v0.1a: no Semantic Reality mutation)."""

from __future__ import annotations

import pytest

from aces_knowledge.models import EpistemicError
from aces_knowledge.services import KnowledgeUpdateService, SemanticRealityService
from aces_worldmodel.models import BeliefState
from aces_worldmodel.services import WorldModelService


def test_belief_state_requires_positive_params():
    with pytest.raises(EpistemicError, match="belief_alpha_beta"):
        BeliefState(alpha=0, beta=1)
    with pytest.raises(EpistemicError, match="belief_alpha_beta"):
        BeliefState(alpha=1, beta=-1)
    b = BeliefState(alpha=3, beta=1)
    assert b.mean == 0.75


def test_update_from_knowledge():
    ksvc = KnowledgeUpdateService()
    wsvc = WorldModelService()
    ko = ksvc.promote_from_accepted_state(
        accepted_state="ESTABLISHED",
        evidence_id="ev-1",
        verification_ref="ver-1",
        content="claim",
    )
    wm = wsvc.update_from_knowledge(knowledge=ko, alpha=4, beta=2)
    assert wm.belief.mean == pytest.approx(4 / 6)
    assert wm.knowledge_ref == ko.knowledge_id
    assert wm.provenance.accepted_state_ref == "ESTABLISHED"


def test_world_model_forbidden_roles():
    ksvc = KnowledgeUpdateService()
    wsvc = WorldModelService()
    ko = ksvc.promote_from_accepted_state(
        accepted_state="ESTABLISHED",
        evidence_id="ev-1",
        verification_ref="ver-1",
        content="claim",
    )
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
    rsvc = SemanticRealityService()
    with pytest.raises(EpistemicError, match="world_model_cannot_mutate_semantic_reality"):
        rsvc.reject_from_world_model()
