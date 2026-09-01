"""VerificationService — sole path to AcceptedState ESTABLISHED.

Requires: SUCCEEDED execution + store-backed Evidence + trusted Verifier
+ exact binding + non-replay. Does not authorize. Does not create capability.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from aces_execution_adapter.models import (
    AcceptedStateStatus,
    ExecutionResult,
    ExecutionStatus,
    VerificationStatus,
)

from .models import Evidence, VerificationOutcome, fingerprint_result
from .stores import InMemoryEvidenceStore, InMemoryVerificationLedger, InMemoryVerifierRegistry


@dataclass(frozen=True)
class VerificationDecision:
    outcome: VerificationOutcome
    reason: str
    result: ExecutionResult


class VerificationService:
    def __init__(
        self,
        *,
        evidence_store: InMemoryEvidenceStore,
        verifier_registry: InMemoryVerifierRegistry,
        ledger: Optional[InMemoryVerificationLedger] = None,
    ) -> None:
        self._evidence_store = evidence_store
        self._verifier_registry = verifier_registry
        self._ledger = ledger or InMemoryVerificationLedger()

    def register_evidence_from_result(
        self,
        result: ExecutionResult,
        *,
        evidence_id: str,
        task_id: str,
        operation: str,
        resource: str,
        scope: str,
        extra_provenance: Optional[Dict[str, Any]] = None,
    ) -> Evidence:
        fp = fingerprint_result(
            request_id=result.request_id,
            status=result.status.value,
            runtime_id=result.runtime_id,
            observed=result.observed,
            task_id=task_id,
            operation=operation,
            resource=resource,
            scope=scope,
        )
        prov = dict(result.provenance)
        if extra_provenance:
            prov.update(extra_provenance)
        evidence = Evidence(
            evidence_id=evidence_id,
            task_id=task_id,
            request_id=result.request_id,
            operation=operation,
            resource=resource,
            scope=scope,
            result_fingerprint=fp,
            observed=dict(result.observed),
            provenance=prov,
        )
        if not self._evidence_store.put(evidence):
            raise RuntimeError("evidence_store_unavailable")
        return evidence

    def verify(
        self,
        result: ExecutionResult,
        *,
        evidence_id: str,
        verifier_id: str,
        task_id: str,
        operation: str,
        resource: str,
        scope: str,
        notes: str = "",
    ) -> VerificationDecision:
        now = datetime.now(timezone.utc)

        def _reject(reason: str, status: VerificationStatus = VerificationStatus.FAILED) -> VerificationDecision:
            return VerificationDecision(
                outcome=VerificationOutcome.REJECTED,
                reason=reason,
                result=ExecutionResult(
                    request_id=result.request_id,
                    status=result.status,
                    runtime_id=result.runtime_id,
                    observed=result.observed,
                    provenance={
                        **result.provenance,
                        "verifier_id": verifier_id,
                        "evidence_id": evidence_id,
                        "verify_notes": notes,
                        "verify_reason": reason,
                        "verified_at": now.isoformat(),
                    },
                    verification_status=status,
                    accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
                    reject_reason=result.reject_reason,
                    error=result.error,
                    completed_at=result.completed_at,
                ),
            )

        if result.status != ExecutionStatus.SUCCEEDED:
            return _reject("execution_not_succeeded", VerificationStatus.NOT_APPLICABLE)

        if not self._evidence_store.is_available():
            return _reject("evidence_store_unavailable")

        try:
            evidence = self._evidence_store.get(evidence_id)
        except RuntimeError:
            return _reject("evidence_store_unavailable")

        if evidence is None:
            return _reject("missing_evidence")

        if not self._verifier_registry.is_available():
            return _reject("verifier_registry_unavailable")

        try:
            verifier = self._verifier_registry.get(verifier_id)
        except RuntimeError:
            return _reject("verifier_registry_unavailable")

        if verifier is None:
            return _reject("unknown_verifier")
        if not verifier.trusted:
            return _reject("untrusted_verifier")

        fp = fingerprint_result(
            request_id=result.request_id,
            status=result.status.value,
            runtime_id=result.runtime_id,
            observed=result.observed,
            task_id=task_id,
            operation=operation,
            resource=resource,
            scope=scope,
        )
        ok, reason = evidence.matches_result_fields(
            task_id=task_id,
            request_id=result.request_id,
            operation=operation,
            resource=resource,
            scope=scope,
            result_fingerprint=fp,
        )
        if not ok:
            return _reject(reason)

        if self._ledger.already_accepted(evidence_id, verifier_id, fp):
            return _reject("replayed_verification")

        self._ledger.mark_accepted(evidence_id, verifier_id, fp)
        accepted = ExecutionResult(
            request_id=result.request_id,
            status=result.status,
            runtime_id=result.runtime_id,
            observed=result.observed,
            provenance={
                **result.provenance,
                "verifier_id": verifier_id,
                "evidence_id": evidence_id,
                "verify_notes": notes,
                "verify_reason": "ok",
                "verified_at": now.isoformat(),
                "result_fingerprint": fp,
            },
            verification_status=VerificationStatus.PASSED,
            accepted_state=AcceptedStateStatus.ESTABLISHED,
            completed_at=result.completed_at,
        )
        return VerificationDecision(
            outcome=VerificationOutcome.ACCEPTED,
            reason="ok",
            result=accepted,
        )
