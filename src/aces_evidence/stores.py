"""In-memory evidence/verifier stores for synthetic boundary tests."""

from __future__ import annotations

from typing import Dict, Optional, Set

from .models import Evidence, VerifierRecord


class InMemoryEvidenceStore:
    def __init__(self, available: bool = True) -> None:
        self._items: Dict[str, Evidence] = {}
        self._available = available

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def put(self, evidence: Evidence) -> bool:
        if not self._available:
            return False
        self._items[evidence.evidence_id] = evidence
        return True

    def get(self, evidence_id: str) -> Optional[Evidence]:
        if not self._available:
            raise RuntimeError("evidence_store_unavailable")
        return self._items.get(evidence_id)


class InMemoryVerifierRegistry:
    def __init__(self, available: bool = True) -> None:
        self._verifiers: Dict[str, VerifierRecord] = {}
        self._available = available

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def register(self, record: VerifierRecord) -> None:
        self._verifiers[record.verifier_id] = record

    def get(self, verifier_id: str) -> Optional[VerifierRecord]:
        if not self._available:
            raise RuntimeError("verifier_registry_unavailable")
        return self._verifiers.get(verifier_id)


class InMemoryVerificationLedger:
    """Replay protection: (evidence_id, verifier_id, result_fingerprint) once."""

    def __init__(self) -> None:
        self._seen: Set[str] = set()

    def key(self, evidence_id: str, verifier_id: str, fingerprint: str) -> str:
        return f"{evidence_id}|{verifier_id}|{fingerprint}"

    def already_accepted(self, evidence_id: str, verifier_id: str, fingerprint: str) -> bool:
        return self.key(evidence_id, verifier_id, fingerprint) in self._seen

    def mark_accepted(self, evidence_id: str, verifier_id: str, fingerprint: str) -> None:
        self._seen.add(self.key(evidence_id, verifier_id, fingerprint))
