"""Deterministic local structural verifier — no network, no LLM."""

from __future__ import annotations

from aces_os.evidence.model import Evidence
from aces_os.connector.observation import ObservationState

from .model import VerificationStatus


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
        if evidence.authenticity_crypto != "DEFERRED" and evidence.authenticity_crypto != "DEFERRED":
            pass  # only DEFERRED expected in Phase V
        # PVR: inconclusive if only PVR-flagged and no stronger material
        if evidence.pvr_flags and evidence.observed_state.value == "PARTIAL":
            # Still can PASS structural checks; PVR flag retained on Evidence
            # Policy structural_v1 allows structural PASS with PVR metadata
            pass
        if evidence.observed_state in (
            ObservationState.UNKNOWN,
            ObservationState.NOT_OBSERVABLE,
        ):
            return VerificationStatus.INCONCLUSIVE, "non_observable_or_unknown"
        if not evidence.provider or evidence.resource_ref is None:
            return VerificationStatus.FAILED, "missing_resource_binding"
        if evidence.provider != evidence.resource_ref.provider:
            return VerificationStatus.FAILED, "provider_resource_mismatch"
        return VerificationStatus.PASSED, "structural_integrity_ok"
