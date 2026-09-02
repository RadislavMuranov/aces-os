"""Phase IV — EvidenceCandidate → Evidence Admission → Evidence.

Evidence ≠ Verification ≠ AcceptedState ≠ Knowledge ≠ Truth ≠ Authority.
"""

from .model import (
    EvidenceCandidate,
    CandidateStatus,
    Evidence,
    EvidenceStatus,
)
from .admission import EvidenceAdmissionService, AdmissionError, AdmissionConflictError
from .store import InMemoryEvidenceStore

__all__ = [
    "EvidenceCandidate",
    "CandidateStatus",
    "Evidence",
    "EvidenceStatus",
    "EvidenceAdmissionService",
    "AdmissionError",
    "AdmissionConflictError",
    "InMemoryEvidenceStore",
]
