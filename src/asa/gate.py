"""AuthorityGate — explicit ASA decision boundary before ExecutionAdapter.

Separates:
  authenticity (store-backed capability + known authority)
  from authorization semantics (scope/op/resource/time/revoke/policy)
  from execution (adapter dispatch)
  from verification (deferred — caller-trusted verification is NOT independent evidence)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .authorize import authorize
from .ports import (
    AuditSink,
    AuthorityRegistry,
    CapabilityStore,
    PolicyStore,
    RevocationStore,
)
from .types import AuthorizationRequest, Decision, DecisionOutcome


@dataclass(frozen=True)
class GateDecision:
    """Normalized gate result for handoff consumers."""

    decision: Decision
    may_dispatch: bool
    reason_code: str
    outcome: DecisionOutcome


class AuthorityGate:
    """Fail-closed ASA gate. DENY ⇒ ExecutionAdapter MUST NOT be called."""

    def __init__(
        self,
        *,
        capability_store: CapabilityStore,
        policy_store: PolicyStore,
        revocation_store: RevocationStore,
        authority_registry: AuthorityRegistry,
        audit_sink: AuditSink,
    ) -> None:
        self._capability_store = capability_store
        self._policy_store = policy_store
        self._revocation_store = revocation_store
        self._authority_registry = authority_registry
        self._audit_sink = audit_sink

    def evaluate(
        self,
        request: AuthorizationRequest,
        *,
        now: Optional[datetime] = None,
    ) -> GateDecision:
        decision = authorize(
            request,
            capability_store=self._capability_store,
            policy_store=self._policy_store,
            revocation_store=self._revocation_store,
            authority_registry=self._authority_registry,
            audit_sink=self._audit_sink,
            now=now,
        )
        allow = decision.outcome == DecisionOutcome.ALLOW
        return GateDecision(
            decision=decision,
            may_dispatch=allow,
            reason_code=decision.reason_code,
            outcome=decision.outcome,
        )
