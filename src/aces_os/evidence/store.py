"""In-memory Evidence store."""

from __future__ import annotations

from typing import Dict, Optional

from .model import Evidence, EvidenceCandidate


class InMemoryEvidenceStore:
    def __init__(self) -> None:
        self._candidates: Dict[str, EvidenceCandidate] = {}
        self._evidence: Dict[str, Evidence] = {}
        self._by_observation: Dict[str, str] = {}  # observation_id -> evidence_id
        self._digest_by_observation: Dict[str, str] = {}
        self._admitted_candidates: Dict[str, str] = {}  # candidate_id -> evidence_id

    def put_candidate(self, c: EvidenceCandidate) -> None:
        self._candidates[c.candidate_id] = c

    def get_candidate(self, candidate_id: str) -> Optional[EvidenceCandidate]:
        return self._candidates.get(candidate_id)

    def put_evidence(self, e: Evidence) -> None:
        self._evidence[e.evidence_id] = e
        self._by_observation[e.observation_id] = e.evidence_id
        self._digest_by_observation[e.observation_id] = e.payload_digest
        self._admitted_candidates[e.candidate_id] = e.evidence_id

    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        return self._evidence.get(evidence_id)

    def get_by_observation(self, observation_id: str) -> Optional[Evidence]:
        eid = self._by_observation.get(observation_id)
        return self._evidence.get(eid) if eid else None

    def observation_digest(self, observation_id: str) -> Optional[str]:
        return self._digest_by_observation.get(observation_id)

    def get_by_candidate(self, candidate_id: str) -> Optional[Evidence]:
        eid = self._admitted_candidates.get(candidate_id)
        return self._evidence.get(eid) if eid else None

    def evidence_count(self) -> int:
        return len(self._evidence)
