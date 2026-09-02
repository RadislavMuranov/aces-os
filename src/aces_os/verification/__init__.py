"""Phase V — Verification → AcceptedState.

Evidence ≠ Verification ≠ Authorization.
AcceptedState ≠ Knowledge ≠ Semantic Reality ≠ Authority.
Only trusted PASSED verification establishes AcceptedState.
"""

from .model import (
    VerificationRequest,
    VerificationResult,
    VerificationStatus,
    AcceptedState,
    AcceptedStateStatus,
    VerificationPolicy,
    VerifierDescriptor,
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
    "TrustedVerifierRegistry",
    "RegistryError",
    "VerificationService",
    "VerificationError",
    "VerificationConflictError",
    "StructuralEvidenceVerifier",
    "InMemoryVerificationStore",
]
