"""Deterministic local structural verifier — no network, no LLM."""

from __future__ import annotations

from aces_os.evidence.model import Evidence
from aces_os.connector.observation import ObservationState

from .model import VerificationStatus

# Phase V allows only explicit deferred crypto marker
_ALLOWED_CRYPTO = frozenset({"DEFERRED"})


class StructuralEvidenceVerifier:
    """Verifies structural integrity of admitted Evidence under policy structural_v1."""

    VERIFIER_ID = "aces.verifier.structural"
    VERIFIER_VERSION = "1.0.0"
    METHOD = "structural_evidence_integrity"

    def verify(self, evidence: Evidence) -> tuple[VerificationStatus, str]:
        if not evidence.evidence_id or not evidence.payload_digest:
            return VerificationStatus.REJECTED, "incomplete_evidence"
        if not evidence.observation_id or not evidence.candidate_id:
            return VerificationStatus.REJECTED, "incomplete_lineage"
        # Crypto authenticity not implemented in Phase V — only DEFERRED is admissible
        crypto = getattr(evidence, "authenticity_crypto", "DEFERRED") or "DEFERRED"
        if crypto not in _ALLOWED_CRYPTO:
            return VerificationStatus.REJECTED, "unsupported_authenticity_crypto_claim"
        if evidence.observed_state in (
            ObservationState.UNKNOWN,
            ObservationState.NOT_OBSERVABLE,
        ):
            return VerificationStatus.INCONCLUSIVE, "non_observable_or_unknown"
        if not evidence.provider or evidence.resource_ref is None:
            return VerificationStatus.FAILED, "missing_resource_binding"
        if evidence.provider != evidence.resource_ref.provider:
            return VerificationStatus.FAILED, "provider_resource_mismatch"
        # PVR flags may remain on Evidence; structural PASS does not upgrade PVR to VERIFIED
        return VerificationStatus.PASSED, "structural_integrity_ok"
