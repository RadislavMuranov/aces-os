"""Memory layer invariant tests."""

from __future__ import annotations

import pytest

from aces_knowledge.services import KnowledgeUpdateService
from aces_memory.services import MemoryService
from aces_knowledge.models import EpistemicError


def test_consolidate_from_knowledge():
    ksvc = KnowledgeUpdateService()
    msvc = MemoryService()
    ko = ksvc.promote_from_accepted_state(
        accepted_state="ESTABLISHED",
        evidence_id="ev-1",
        verification_ref="ver-1",
        content="remembered claim",
        task_id="t1",
    )
    mem = msvc.consolidate_from_knowledge(knowledge=ko)
    assert mem.content == "remembered claim"
    assert mem.knowledge_ref == ko.knowledge_id
    assert mem.provenance.knowledge_ref == ko.knowledge_id
    assert mem.accepted_state_ref == "ESTABLISHED"


def test_memory_not_evidence_truth_authority_verification():
    ksvc = KnowledgeUpdateService()
    msvc = MemoryService()
    ko = ksvc.promote_from_accepted_state(
        accepted_state="ESTABLISHED",
        evidence_id="ev-1",
        verification_ref="ver-1",
        content="x",
    )
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
    ksvc = KnowledgeUpdateService()
    msvc = MemoryService()
    ko = ksvc.promote_from_accepted_state(
        accepted_state="ESTABLISHED",
        evidence_id="ev-1",
        verification_ref="ver-1",
        content="v1",
    )
    m1 = msvc.consolidate_from_knowledge(knowledge=ko)
    m2 = msvc.consolidate_from_knowledge(knowledge=ko)
    hist = msvc.store.history()
    assert len(hist) == 2
    assert hist[0].memory_id == m1.memory_id
    assert hist[1].memory_id == m2.memory_id
