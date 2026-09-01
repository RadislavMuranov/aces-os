"""Execution Adapter domain models. No authority is manufactured here."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional, Tuple
import hashlib
import json


class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    DISPATCHED = "DISPATCHED"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    REJECTED = "REJECTED"  # fail-closed at adapter (auth/scope)
    CANCELLED = "CANCELLED"


class VerificationStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    PENDING = "PENDING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class AcceptedStateStatus(str, Enum):
    """AcceptedState is never set by the adapter from execution success alone."""
    NOT_ESTABLISHED = "NOT_ESTABLISHED"
    ESTABLISHED = "ESTABLISHED"  # only via explicit external verifier path


@dataclass(frozen=True)
class AuthorizationRecord:
    """Explicit authorization. Missing/invalid => fail-closed."""

    principal: str
    operation: str
    resource: str
    scope: str
    task_id: str
    valid_from: datetime
    valid_until: datetime
    approval_id: str

    def is_valid_at(self, when: datetime) -> bool:
        return self.valid_from <= when <= self.valid_until

    def matches(
        self,
        *,
        operation: str,
        resource: str,
        scope: str,
        task_id: str,
        when: datetime,
    ) -> Tuple[bool, str]:
        if not self.principal.strip():
            return False, "missing_principal"
        if operation != self.operation:
            return False, "operation_mismatch"
        if resource != self.resource:
            return False, "resource_mismatch"
        if scope != self.scope:
            return False, "scope_mismatch"
        if task_id != self.task_id:
            return False, "task_mismatch"
        if not self.is_valid_at(when):
            return False, "expired_or_not_yet_valid"
        return True, "ok"


@dataclass
class ExecutionRequest:
    """Intent + authorization reference. Adapter does not invent approval."""

    request_id: str
    intent_reference: str  # semantic intent id / description handle
    operation: str
    resource: str
    scope: str
    task_id: str
    runtime_id: str
    authorization: Optional[AuthorizationRecord]
    payload: Dict[str, Any] = field(default_factory=dict)
    requested_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ExecutionResult:
    request_id: str
    status: ExecutionStatus
    runtime_id: str
    observed: Dict[str, Any]
    provenance: Dict[str, Any]
    verification_status: VerificationStatus
    accepted_state: AcceptedStateStatus
    reject_reason: Optional[str] = None
    error: Optional[str] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "status": self.status.value,
            "runtime_id": self.runtime_id,
            "observed": self.observed,
            "provenance": self.provenance,
            "verification_status": self.verification_status.value,
            "accepted_state": self.accepted_state.value,
            "reject_reason": self.reject_reason,
            "error": self.error,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    def material_fingerprint(self) -> str:
        body = json.dumps(self.to_dict(), sort_keys=True, default=str)
        return hashlib.sha256(body.encode()).hexdigest()
