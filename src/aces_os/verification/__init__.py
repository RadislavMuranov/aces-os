"""Phase V — Verification → AcceptedState.

Evidence ≠ Verification ≠ Authorization.
AcceptedState ≠ Knowledge ≠ Semantic Reality ≠ Authority.
Only trusted PASSED verification establishes AcceptedState.
AcceptedState identity = full verification identity (not evidence_id alone).
"""

from .model import (
    VerificationRequest,
    VerificationResult,
    VerificationStatus,
    AcceptedState,
    AcceptedStateStatus,
    VerificationPolicy,
    VerifierDescriptor,
    accepted_identity_key,
)
from .registry import TrustedVerifierRegistry, RegistryError
from .service import VerificationService, VerificationError, VerificationConflictError
from .verifiers import StructuralEvidenceVerifier
from .store import InMemoryVerificationStore

__all__ = [
    "VerificationRequest",
    "VerificationResult",
    "VerificationStatus",
    "AcceptedState",
    "AcceptedStateStatus",
    "VerificationPolicy",
    "VerifierDescriptor",
    "accepted_identity_key",
    "TrustedVerifierRegistry",
    "RegistryError",
    "VerificationService",
    "VerificationError",
    "VerificationConflictError",
    "StructuralEvidenceVerifier",
    "InMemoryVerificationStore",
]
