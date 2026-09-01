"""Handoff from ASA Decision to ExecutionAdapter AuthorizationRecord.

Critical rule:
  - Only ALLOW decisions may produce an adapter authorization.
  - Structural AuthorizationRecord alone is NOT authority; ASA Decision is required.
  - Verification remains outside ASA (Evidence/Verification gate residual).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from .types import Decision, DecisionOutcome

if TYPE_CHECKING:
    from aces_execution_adapter.models import AuthorizationRecord


@dataclass(frozen=True)
class AdapterHandoff:
    """Sealed handoff: adapter may be invoked only when authorized=True."""

    authorized: bool
    decision_id: str
    reason_code: str
    authorization_record: Optional["AuthorizationRecord"]
    principal_id: str
    resource_id: str
    operation: str
    authority_id: Optional[str]
    capability_id: Optional[str]
    policy_id: str
    policy_version: str


def build_adapter_authorization(
    decision: Decision,
    *,
    scope: str,
    task_id: str,
    valid_from: datetime,
    valid_until: datetime,
    approval_id: Optional[str] = None,
) -> AdapterHandoff:
    """Build adapter AuthorizationRecord only when decision is ALLOW.

    DENY → authorized=False, no AuthorizationRecord, adapter MUST NOT dispatch.
    """
    if decision.outcome != DecisionOutcome.ALLOW:
        return AdapterHandoff(
            authorized=False,
            decision_id=decision.decision_id,
            reason_code=decision.reason_code,
            authorization_record=None,
            principal_id=decision.principal_id,
            resource_id=decision.resource_id,
            operation=decision.operation.value if hasattr(decision.operation, "value") else str(decision.operation),
            authority_id=decision.authority_id,
            capability_id=decision.capability_id,
            policy_id=decision.policy_id,
            policy_version=decision.policy_version,
        )

    from aces_execution_adapter.models import AuthorizationRecord

    record = AuthorizationRecord(
        principal=decision.principal_id,
        operation=decision.operation.value,
        resource=decision.resource_id,
        scope=scope,
        task_id=task_id,
        valid_from=valid_from,
        valid_until=valid_until,
        approval_id=approval_id or f"asa-decision:{decision.decision_id}",
    )
    return AdapterHandoff(
        authorized=True,
        decision_id=decision.decision_id,
        reason_code=decision.reason_code,
        authorization_record=record,
        principal_id=decision.principal_id,
        resource_id=decision.resource_id,
        operation=decision.operation.value,
        authority_id=decision.authority_id,
        capability_id=decision.capability_id,
        policy_id=decision.policy_id,
        policy_version=decision.policy_version,
    )


def dispatch_if_allowed(adapter, request, handoff: AdapterHandoff):
    """Adapter integration primitive: BLOCK ⇒ adapter not called."""
    if not handoff.authorized or handoff.authorization_record is None:
        return None
    return adapter.dispatch(request)
