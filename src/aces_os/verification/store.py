"""In-memory verification / AcceptedState store."""

from __future__ import annotations

from typing import Dict, Optional

from .model import AcceptedState, VerificationRequest, VerificationResult, accepted_identity_key


class InMemoryVerificationStore:
    def __init__(self) -> None:
        self._requests: Dict[str, VerificationRequest] = {}
        self._results: Dict[str, VerificationResult] = {}
        self._accepted: Dict[str, AcceptedState] = {}
        # key: full verification identity -> result_id
        self._replay: Dict[str, str] = {}
        # key: full verification identity -> accepted_state_id (NOT evidence_id alone)
        self._accepted_by_identity: Dict[str, str] = {}

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
        key = accepted_identity_key(
            state.evidence_id,
            state.evidence_digest,
            state.policy_id,
            state.policy_version,
            state.verifier_id,
            state.verifier_version,
        )
        self._accepted_by_identity[key] = state.accepted_state_id

    def get_accepted(self, accepted_state_id: str) -> Optional[AcceptedState]:
        return self._accepted.get(accepted_state_id)

    def get_accepted_by_identity(
        self,
        evidence_id: str,
        evidence_digest: str,
        policy_id: str,
        policy_version: str,
        verifier_id: str,
        verifier_version: str,
    ) -> Optional[AcceptedState]:
        key = accepted_identity_key(
            evidence_id,
            evidence_digest,
            policy_id,
            policy_version,
            verifier_id,
            verifier_version,
        )
        aid = self._accepted_by_identity.get(key)
        return self._accepted.get(aid) if aid else None
