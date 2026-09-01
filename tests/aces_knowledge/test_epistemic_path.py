"""Positive end-to-end epistemic path and provenance reconstruction."""

from __future__ import annotations

from aces_knowledge.services import KnowledgeUpdateService, SemanticRealityService
from aces_memory.services import MemoryService
from aces_worldmodel.services import WorldModelService


def test_full_positive_path_with_provenance():
    ksvc = KnowledgeUpdateService()
    msvc = MemoryService()
    wsvc = WorldModelService()
    rsvc = SemanticRealityService()

    accepted = "ESTABLISHED"
    evidence_id = "ev-e2e-001"
    verification_ref = "ver-e2e-001"
    task_id = "task-e2e"
    execution_id = "exec-e2e"

    ko = ksvc.promote_from_accepted_state(
        accepted_state=accepted,
        evidence_id=evidence_id,
        verification_ref=verification_ref,
        content="E3.4 marker exists on branch",
        task_id=task_id,
        execution_id=execution_id,
    )

    mem = msvc.consolidate_from_knowledge(knowledge=ko)
    wm = wsvc.update_from_knowledge(knowledge=ko, alpha=5, beta=1, projection="likely true")
    reality = rsvc.update_from_knowledge(knowledge=ko)

    assert reality.knowledge_ref == ko.knowledge_id
    assert reality.provenance.transformation == "knowledge_to_semantic_reality"
    assert reality.provenance.actor == "semantic_reality_service"

    assert reality.provenance.knowledge_ref == ko.knowledge_id
    assert reality.provenance.accepted_state_ref == accepted
    assert reality.provenance.evidence_ref == evidence_id
    assert reality.provenance.verification_ref == verification_ref
    assert ko.provenance.evidence_ref == evidence_id
    assert ko.provenance.verification_ref == verification_ref
    assert ko.provenance.accepted_state_ref == accepted
    assert mem.provenance.knowledge_ref == ko.knowledge_id
    assert mem.provenance.evidence_ref == evidence_id
    assert wm.provenance.knowledge_ref == ko.knowledge_id
    assert wm.provenance.accepted_state_ref == accepted

    assert reality.knowledge_ref == ko.knowledge_id
    assert ko.provenance.accepted_state_ref == "ESTABLISHED"
    assert ko.provenance.verification_ref == verification_ref
    assert evidence_id in ko.evidence_refs
