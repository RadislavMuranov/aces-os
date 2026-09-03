"""VerificationService — only trusted PASSED path establishes AcceptedState."""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Optional

from aces_os.evidence.model import Evidence

from .model import (
    AcceptedState,
    AcceptedStateStatus,
    VerificationRequest,
    VerificationResult,
    VerificationStatus,
    accepted_identity_key,
)
from .registry import TrustedVerifierRegistry, RegistryError
from .store import InMemoryVerificationStore
from .verifiers import StructuralEvidenceVerifier


class VerificationError(ValueError):
    pass


class VerificationConflictError(VerificationError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _id(prefix: str, *parts: str) -> str:
    raw = "|".join(parts)
    return f"{prefix}:" + hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]


class VerificationService:
    """Caller submits Evidence; cannot force PASSED or AcceptedState."""

    def __init__(
        self,
        registry: TrustedVerifierRegistry,
        store: Optional[InMemoryVerificationStore] = None,
        structural_verifier: Optional[StructuralEvidenceVerifier] = None,
    ) -> None:
        self.registry = registry
        self.store = store or InMemoryVerificationStore()
        self._structural = structural_verifier or StructuralEvidenceVerifier()

    def build_request(
        self,
        evidence: Evidence,
        policy_id: str,
        policy_version: str,
        request_key: str,
    ) -> VerificationRequest:
        if not evidence or not evidence.evidence_id:
            raise VerificationError("missing evidence")
        return VerificationRequest(
            verification_request_id=_id("vreq", request_key, evidence.evidence_id, policy_id),
            evidence_id=evidence.evidence_id,
            candidate_id=evidence.candidate_id,
            observation_id=evidence.observation_id,
            dwom_object_id=evidence.dwom_object_id,
            provider=evidence.provider,
            resource_ref=evidence.resource_ref,
            resource_kind=evidence.resource_kind,
            scope_namespace=evidence.scope_namespace,
            payload_digest=evidence.payload_digest,
            request_id=evidence.request_id,
            verification_policy_id=policy_id,
            verification_policy_version=policy_version,
            requested_at=_utc_now(),
            connector_id=evidence.connector_id,
        )

    def verify(
        self,
        evidence: Evidence,
        request: VerificationRequest,
        verifier_id: str,
        verifier_version: str,
    ) -> tuple[VerificationResult, Optional[AcceptedState]]:
        self._validate_binding(evidence, request)

        try:
            policy = self.registry.get_policy(
                request.verification_policy_id, request.verification_policy_version
            )
            verifier_desc = self.registry.get_trusted_verifier(
                verifier_id, verifier_version, policy.policy_id
            )
        except RegistryError as e:
            result = self._make_result(
                request,
                evidence,
                verifier_id,
                verifier_version,
                VerificationStatus.REJECTED,
                str(e),
            )
            self.store.put_request(request)
            self.store.put_result(
                result, self._replay_key(request, evidence, verifier_id, verifier_version)
            )
            return result, None

        replay_key = self._replay_key(request, evidence, verifier_id, verifier_version)
        prior = self.store.get_by_replay(replay_key)
        if prior is not None:
            if prior.evidence_digest != evidence.payload_digest:
                raise VerificationConflictError("replay digest conflict")
            accepted = self.store.get_accepted_by_identity(
                evidence.evidence_id,
                evidence.payload_digest,
                request.verification_policy_id,
                request.verification_policy_version,
                verifier_id,
                verifier_version,
            )
            # Only return AcceptedState if prior was PASSED and binding matches result
            if accepted is not None and prior.status != VerificationStatus.PASSED:
                accepted = None
            if accepted is not None and accepted.verification_result_id != prior.verification_result_id:
                raise VerificationConflictError("AcceptedState/Result binding mismatch")
            return prior, accepted

        if (
            verifier_id != StructuralEvidenceVerifier.VERIFIER_ID
            or verifier_version != StructuralEvidenceVerifier.VERIFIER_VERSION
        ):
            # Alternate trusted verifiers without bound implementation: REJECTED
            # (structural is the only executable method in Phase V)
            if verifier_id == StructuralEvidenceVerifier.VERIFIER_ID:
                status, reason = VerificationStatus.REJECTED, "verifier_version_not_bound"
            else:
                status, reason = VerificationStatus.REJECTED, "verifier_implementation_not_bound"
        else:
            status, reason = self._structural.verify(evidence)

        result = self._make_result(
            request,
            evidence,
            verifier_desc.verifier_id,
            verifier_desc.verifier_version,
            status,
            reason,
        )
        self.store.put_request(request)
        self.store.put_result(result, replay_key)

        accepted: Optional[AcceptedState] = None
        if result.status == VerificationStatus.PASSED:
            existing = self.store.get_accepted_by_identity(
                evidence.evidence_id,
                evidence.payload_digest,
                result.policy_id,
                result.policy_version,
                result.verifier_id,
                result.verifier_version,
            )
            if existing is not None:
                if existing.verification_result_id != result.verification_result_id:
                    # Same identity should have been caught by replay; treat as conflict
                    if existing.evidence_digest != evidence.payload_digest:
                        raise VerificationConflictError("identity digest conflict")
                    accepted = existing
                else:
                    accepted = existing
            else:
                accepted = AcceptedState(
                    accepted_state_id=_id(
                        "as",
                        evidence.evidence_id,
                        evidence.payload_digest,
                        result.policy_id,
                        result.policy_version,
                        result.verifier_id,
                        result.verifier_version,
                        result.verification_result_id,
                    ),
                    evidence_id=evidence.evidence_id,
                    verification_result_id=result.verification_result_id,
                    verifier_id=result.verifier_id,
                    verifier_version=result.verifier_version,
                    policy_id=result.policy_id,
                    policy_version=result.policy_version,
                    status=AcceptedStateStatus.ESTABLISHED,
                    accepted_at=result.verified_at,
                    evidence_digest=evidence.payload_digest,
                    observation_id=evidence.observation_id,
                    provider=evidence.provider,
                    resource_kind=evidence.resource_kind,
                    authenticity_crypto="DEFERRED",
                )
                self.store.put_accepted(accepted)
        return result, accepted

    def _replay_key(
        self,
        request: VerificationRequest,
        evidence: Evidence,
        verifier_id: str,
        verifier_version: str,
    ) -> str:
        return accepted_identity_key(
            evidence.evidence_id,
            evidence.payload_digest,
            request.verification_policy_id,
            request.verification_policy_version,
            verifier_id,
            verifier_version,
        )

    def _validate_binding(self, evidence: Evidence, request: VerificationRequest) -> None:
        if evidence.evidence_id != request.evidence_id:
            raise VerificationError("evidence_id mismatch")
        if evidence.candidate_id != request.candidate_id:
            raise VerificationError("candidate_id mismatch")
        if evidence.observation_id != request.observation_id:
            raise VerificationError("observation_id mismatch")
        if evidence.dwom_object_id != request.dwom_object_id:
            raise VerificationError("dwom_object_id mismatch")
        if evidence.provider != request.provider:
            raise VerificationError("provider mismatch")
        if evidence.resource_ref.resource_id != request.resource_ref.resource_id:
            raise VerificationError("resource mismatch")
        if evidence.scope_namespace != request.scope_namespace:
            raise VerificationError("scope mismatch")
        if evidence.payload_digest != request.payload_digest:
            raise VerificationError("digest mismatch")

    def _make_result(
        self,
        request: VerificationRequest,
        evidence: Evidence,
        verifier_id: str,
        verifier_version: str,
        status: VerificationStatus,
        reason: str,
    ) -> VerificationResult:
        return VerificationResult(
            verification_result_id=_id(
                "vres", request.verification_request_id, status.value, reason
            ),
            verification_request_id=request.verification_request_id,
            evidence_id=evidence.evidence_id,
            verifier_id=verifier_id,
            verifier_version=verifier_version,
            policy_id=request.verification_policy_id,
            policy_version=request.verification_policy_version,
            status=status,
            reason=reason,
            verified_at=_utc_now(),
            evidence_digest=evidence.payload_digest,
            authenticity_crypto="DEFERRED",
        )

    def establish_passed(self, *a, **k):
        raise VerificationError("caller cannot set PASSED")

    def create_accepted_state_direct(self, *a, **k):
        raise VerificationError("caller cannot create AcceptedState")

    def issue_authorization(self, *a, **k):
        raise VerificationError("Verification ≠ Authorization")

    def issue_capability(self, *a, **k):
        raise VerificationError("Verification cannot issue capability")

    def bypass_asa(self, *a, **k):
        raise VerificationError("cannot bypass ASA")

    def promote_knowledge(self, *a, **k):
        raise VerificationError("AcceptedState ≠ Knowledge")

    def mutate_memory(self, *a, **k):
        raise VerificationError("cannot mutate Memory")

    def mutate_world_model(self, *a, **k):
        raise VerificationError("cannot mutate World Model")

    def mutate_semantic_reality(self, *a, **k):
        raise VerificationError("cannot mutate Semantic Reality")

    def write_provider(self, *a, **k):
        raise VerificationError("cannot write providers")

    def resolve_reconciliation(self, *a, **k):
        raise VerificationError("Verification does not select reconciliation winners")
