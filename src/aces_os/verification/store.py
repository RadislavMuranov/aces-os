"""In-memory verification / AcceptedState store."""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from .model import AcceptedState, VerificationRequest, VerificationResult


class InMemoryVerificationStore:
    def __init__(self) -> None:
        self._requests: Dict[str, VerificationRequest] = {}
        self._results: Dict[str, VerificationResult] = {}
        self._accepted: Dict[str, AcceptedState] = {}
        # key: evidence_id|policy|verifier|digest -> result_id
        self._replay: Dict[str, str] = {}
        self._accepted_by_evidence: Dict[str, str] = {}

    def put_request(self, req: VerificationRequest) -> None:
        self._requests[req.verification_request_id] = req

    def put_result(self, result: VerificationResult, replay_key: str) -> None:
        self._results[result.verification_result_id] = result
        self._replay[replay_key] = result.verification_result_id

    def get_result(self, result_id: str) -> Optional[VerificationResult]:
        return self._results.get(result_id)

    def get_by_replay(self, replay_key: str) -> Optional[VerificationResult]:
        rid = self._replay.get(replay_key)
        return self._results.get(rid) if rid else None

    def put_accepted(self, state: AcceptedState) -> None:
        self._accepted[state.accepted_state_id] = state
        self._accepted_by_evidence[state.evidence_id] = state.accepted_state_id

    def get_accepted(self, accepted_state_id: str) -> Optional[AcceptedState]:
        return self._accepted.get(accepted_state_id)

    def get_accepted_by_evidence(self, evidence_id: str) -> Optional[AcceptedState]:
        aid = self._accepted_by_evidence.get(evidence_id)
        return self._accepted.get(aid) if aid else None
