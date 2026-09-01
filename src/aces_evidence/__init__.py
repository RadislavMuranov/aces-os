"""ACES Evidence / Verification boundary.

AcceptedState is established only after:
  successful execution + bound Evidence + trusted Verifier + matching verification.

Inference ≠ Evidence. Execution success ≠ AcceptedState. Verification ≠ Authorization.
"""

from .models import Evidence, VerifierRecord, VerificationOutcome
from .stores import InMemoryEvidenceStore, InMemoryVerifierRegistry, InMemoryVerificationLedger
from .service import VerificationService

__all__ = [
    "Evidence",
    "VerifierRecord",
    "VerificationOutcome",
    "InMemoryEvidenceStore",
    "InMemoryVerifierRegistry",
    "InMemoryVerificationLedger",
    "VerificationService",
]

__version__ = "0.1.0"
