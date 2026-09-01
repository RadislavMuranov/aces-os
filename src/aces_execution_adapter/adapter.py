"""ExecutionAdapter: ACES control boundary to replaceable runtimes.

Fail-closed on missing/invalid authorization.
Never manufactures authority, approval, evidence, or AcceptedState from caller boolean.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .models import (
    AcceptedStateStatus,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    VerificationStatus,
)
from .runtimes import ExecutionRuntime


class ExecutionAdapter:
    """Minimal runtime-neutral execution adapter."""

    def __init__(self, runtimes: Optional[Dict[str, ExecutionRuntime]] = None):
        self._runtimes: Dict[str, ExecutionRuntime] = dict(runtimes or {})

    def register_runtime(self, runtime: ExecutionRuntime) -> None:
        self._runtimes[runtime.runtime_id] = runtime

    def dispatch(self, request: ExecutionRequest) -> ExecutionResult:
        now = datetime.now(timezone.utc)
        provenance = {
            "adapter": "aces_execution_adapter",
            "adapter_version": "0.1.1",
            "request_id": request.request_id,
            "intent_reference": request.intent_reference,
            "requested_at": request.requested_at.isoformat(),
            "dispatched_at": now.isoformat(),
            "authorization_present": request.authorization is not None,
        }

        if request.authorization is None:
            return self._reject(request, "missing_authorization", provenance)

        ok, reason = request.authorization.matches(
            operation=request.operation,
            resource=request.resource,
            scope=request.scope,
            task_id=request.task_id,
            when=now,
        )
        if not ok:
            return self._reject(request, reason, provenance)

        provenance["approval_id"] = request.authorization.approval_id
        provenance["principal"] = request.authorization.principal

        runtime = self._runtimes.get(request.runtime_id)
        if runtime is None:
            return self._reject(request, "unknown_runtime", provenance)

        try:
            succeeded, observed, error = runtime.execute(request)
        except Exception as exc:  # noqa: BLE001
            return ExecutionResult(
                request_id=request.request_id,
                status=ExecutionStatus.FAILED,
                runtime_id=request.runtime_id,
                observed={},
                provenance=provenance,
                verification_status=VerificationStatus.NOT_STARTED,
                accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
                error=f"runtime_exception:{type(exc).__name__}",
                completed_at=datetime.now(timezone.utc),
            )

        if not succeeded:
            return ExecutionResult(
                request_id=request.request_id,
                status=ExecutionStatus.FAILED,
                runtime_id=request.runtime_id,
                observed=observed,
                provenance=provenance,
                verification_status=VerificationStatus.NOT_STARTED,
                accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
                error=error,
                completed_at=datetime.now(timezone.utc),
            )

        return ExecutionResult(
            request_id=request.request_id,
            status=ExecutionStatus.SUCCEEDED,
            runtime_id=request.runtime_id,
            observed=observed,
            provenance=provenance,
            verification_status=VerificationStatus.PENDING,
            accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
            completed_at=datetime.now(timezone.utc),
        )

    def apply_verification(
        self,
        result: ExecutionResult,
        *,
        passed: bool,
        verifier_id: str,
        notes: str = "",
        evidence_id: Optional[str] = None,
        verification_service: Any = None,
        task_id: Optional[str] = None,
        operation: Optional[str] = None,
        resource: Optional[str] = None,
        scope: Optional[str] = None,
    ) -> ExecutionResult:
        """Verification entrypoint.

        HARDENING: caller boolean `passed=True` alone MUST NOT establish AcceptedState.
        Establishing AcceptedState requires VerificationService + evidence_id + binding fields.
        """
        if evidence_id is None or verification_service is None:
            return ExecutionResult(
                request_id=result.request_id,
                status=result.status,
                runtime_id=result.runtime_id,
                observed=result.observed,
                provenance={
                    **result.provenance,
                    "verifier_id": verifier_id,
                    "verify_notes": notes,
                    "verify_reason": "evidence_required",
                },
                verification_status=VerificationStatus.FAILED,
                accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
                reject_reason=result.reject_reason,
                error=result.error or "caller_boolean_insufficient",
                completed_at=result.completed_at,
            )

        if task_id is None or operation is None or resource is None or scope is None:
            return ExecutionResult(
                request_id=result.request_id,
                status=result.status,
                runtime_id=result.runtime_id,
                observed=result.observed,
                provenance={
                    **result.provenance,
                    "verifier_id": verifier_id,
                    "evidence_id": evidence_id,
                    "verify_reason": "binding_fields_required",
                },
                verification_status=VerificationStatus.FAILED,
                accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
                completed_at=result.completed_at,
            )

        if not passed:
            return ExecutionResult(
                request_id=result.request_id,
                status=result.status,
                runtime_id=result.runtime_id,
                observed=result.observed,
                provenance={
                    **result.provenance,
                    "verifier_id": verifier_id,
                    "evidence_id": evidence_id,
                    "verify_notes": notes,
                    "verify_reason": "verifier_reported_fail",
                },
                verification_status=VerificationStatus.FAILED,
                accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
                completed_at=result.completed_at,
            )

        decision = verification_service.verify(
            result,
            evidence_id=evidence_id,
            verifier_id=verifier_id,
            task_id=task_id,
            operation=operation,
            resource=resource,
            scope=scope,
            notes=notes,
        )
        return decision.result

    def _reject(
        self,
        request: ExecutionRequest,
        reason: str,
        provenance: dict,
    ) -> ExecutionResult:
        return ExecutionResult(
            request_id=request.request_id,
            status=ExecutionStatus.REJECTED,
            runtime_id=request.runtime_id,
            observed={},
            provenance=provenance,
            verification_status=VerificationStatus.NOT_APPLICABLE,
            accepted_state=AcceptedStateStatus.NOT_ESTABLISHED,
            reject_reason=reason,
            completed_at=datetime.now(timezone.utc),
        )
