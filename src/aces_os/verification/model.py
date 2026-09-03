"""Verification and AcceptedState models — not truth, not authority."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from aces_os.connector.resource import ResourceRef


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"
    INCONCLUSIVE = "INCONCLUSIVE"


class AcceptedStateStatus(str, Enum):
    ESTABLISHED = "ESTABLISHED"


@dataclass(frozen=True)
class VerificationPolicy:
    policy_id: str
    policy_version: str
    active: bool = True
    description: str = ""


@dataclass(frozen=True)
class VerifierDescriptor:
    verifier_id: str
    verifier_version: str
    verification_method: str
    trust_status: str  # TRUSTED | UNTRUSTED
    policy_scope: Tuple[str, ...]  # policy_id values allowed


@dataclass(frozen=True)
class VerificationRequest:
    verification_request_id: str
    evidence_id: str
    candidate_id: str
    observation_id: str
    dwom_object_id: str
    provider: str
    resource_ref: ResourceRef
    resource_kind: str
    scope_namespace: str
    payload_digest: str
    request_id: str
    verification_policy_id: str
    verification_policy_version: str
    requested_at: str
    connector_id: str


@dataclass(frozen=True)
class VerificationResult:
    verification_result_id: str
    verification_request_id: str
    evidence_id: str
    verifier_id: str
    verifier_version: str
    policy_id: str
    policy_version: str
    status: VerificationStatus
    reason: str
    verified_at: str
    evidence_digest: str
    authenticity_crypto: str = "DEFERRED"

    def establishes_accepted_state(self) -> bool:
        return self.status == VerificationStatus.PASSED


@dataclass(frozen=True)
class AcceptedState:
    """Evidence passed authorized verification under exact verification identity.

    Bound to evidence_id + evidence_digest + policy + verifier — not evidence_id alone.
    Not universal truth.
    """

    accepted_state_id: str
    evidence_id: str
    verification_result_id: str
    verifier_id: str
    verifier_version: str
    policy_id: str
    policy_version: str
    status: AcceptedStateStatus
    accepted_at: str
    evidence_digest: str
    observation_id: str
    provider: str
    resource_kind: str
    authenticity_crypto: str = "DEFERRED"

    def is_knowledge(self) -> bool:
        return False

    def is_semantic_reality(self) -> bool:
        return False

    def is_authorization(self) -> bool:
        return False

    def is_truth(self) -> bool:
        return False


def accepted_identity_key(
    evidence_id: str,
    evidence_digest: str,
    policy_id: str,
    policy_version: str,
    verifier_id: str,
    verifier_version: str,
) -> str:
    """Canonical verification identity for AcceptedState lookup (deterministic)."""
    return "|".join(
        [
            evidence_id,
            evidence_digest,
            policy_id,
            policy_version,
            verifier_id,
            verifier_version,
        ]
    )
