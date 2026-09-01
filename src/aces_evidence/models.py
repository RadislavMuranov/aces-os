"""Evidence and verifier domain models. No authority is manufactured here."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
import hashlib
import json


class VerificationOutcome(str, Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


@dataclass(frozen=True)
class Evidence:
    """Observed-result binding. Not authorization. Not AcceptedState."""

    evidence_id: str
    task_id: str
    request_id: str
    operation: str
    resource: str
    scope: str
    result_fingerprint: str
    observed: Dict[str, Any]
    provenance: Dict[str, Any]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def matches_result_fields(
        self,
        *,
        task_id: str,
        request_id: str,
        operation: str,
        resource: str,
        scope: str,
        result_fingerprint: str,
    ) -> tuple[bool, str]:
        if self.task_id != task_id:
            return False, "task_mismatch"
        if self.request_id != request_id:
            return False, "result_mismatch"
        if self.operation != operation:
            return False, "operation_mismatch"
        if self.resource != resource:
            return False, "resource_mismatch"
        if self.scope != scope:
            return False, "scope_mismatch"
        if self.result_fingerprint != result_fingerprint:
            return False, "fingerprint_mismatch"
        if not self.provenance:
            return False, "provenance_missing"
        return True, "ok"


@dataclass(frozen=True)
class VerifierRecord:
    """Trusted verifier registry entry. Arbitrary verifier_id is not trust."""

    verifier_id: str
    label: str
    trusted: bool
    registered_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


def fingerprint_result(
    *,
    request_id: str,
    status: str,
    runtime_id: str,
    observed: Dict[str, Any],
    task_id: str,
    operation: str,
    resource: str,
    scope: str,
) -> str:
    body = {
        "request_id": request_id,
        "status": status,
        "runtime_id": runtime_id,
        "observed": observed,
        "task_id": task_id,
        "operation": operation,
        "resource": resource,
        "scope": scope,
    }
    return hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()
