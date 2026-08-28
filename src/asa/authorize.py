"""ASA-004 authorization core — deny-first evaluation order (data-model §5).

Flow:
  Identity → Principal → Request → Capability → Scope → Expiration
  → Revocation → Policy → Decision → Audit

Invariants I1–I8. No cached ALLOW. No GitHub privilege inputs (I8).
AuthorizationEvent never grants authority (I7).

ASA-004.1: G-01 policy binding, G-02 closed-enum DENY, G-03 capability self-id.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from . import reason_codes as rc
from .ports import (
    AuditSink,
    AuthorityRegistry,
    CapabilityStore,
    PolicyStore,
    RevocationStore,
)
from .scope import scope_allows
from .types import (
    ACCEPTED_AUTHENTICATORS,
    AuthorizationEvent,
    AuthorizationRequest,
    Capability,
    Decision,
    DecisionOutcome,
    Operation,
    Policy,
    ResourceKind,
    ResourceSelectorExact,
    ResourceSelectorStructured,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _new_id() -> str:
    return str(uuid.uuid4())


def _deny(
    request: AuthorizationRequest,
    reason_code: str,
    *,
    policy_id: str = "",
    policy_version: str = "",
    capability_id: Optional[str] = None,
    authority_id: Optional[str] = None,
    timestamp: Optional[datetime] = None,
) -> Decision:
    ts = timestamp or _now()
    return Decision(
        decision_id=_new_id(),
        principal_id=request.principal.principal_id if request.principal else "",
        resource_id=request.resource.resource_id if request.resource else "",
        operation=request.operation,
        outcome=DecisionOutcome.DENY,
        reason_code=reason_code,
        policy_id=policy_id,
        policy_version=policy_version,
        timestamp=ts,
        correlation_id=request.correlation_id or "",
        capability_id=capability_id,
        authority_id=authority_id,
    )


def _allow(
    request: AuthorizationRequest,
    *,
    policy_id: str,
    policy_version: str,
    capability_id: str,
    authority_id: str,
    timestamp: datetime,
) -> Decision:
    return Decision(
        decision_id=_new_id(),
        principal_id=request.principal.principal_id,
        resource_id=request.resource.resource_id,
        operation=request.operation,
        outcome=DecisionOutcome.ALLOW,
        reason_code=rc.ALLOW,
        policy_id=policy_id,
        policy_version=policy_version,
        timestamp=timestamp,
        correlation_id=request.correlation_id,
        capability_id=capability_id,
        authority_id=authority_id,
    )


def _append_audit(
    audit: AuditSink,
    decision: Decision,
) -> bool:
    event = AuthorizationEvent(
        event_id=_new_id(),
        principal_id=decision.principal_id,
        operation=decision.operation,
        resource_id=decision.resource_id,
        timestamp=decision.timestamp,
        authority_id=decision.authority_id or "",
        policy_id=decision.policy_id,
        policy_version=decision.policy_version,
        decision=decision.outcome,
        result_or_error_class=decision.reason_code,
        correlation_id=decision.correlation_id,
        capability_id=decision.capability_id,
    )
    return audit.append(event)


def _validate_identity(request: AuthorizationRequest) -> Optional[str]:
    identity = request.identity
    if identity is None:
        return rc.UNKNOWN_IDENTITY
    if not identity.identity_id or not identity.subject_ref:
        return rc.INVALID_IDENTITY
    if identity.authenticator_id not in ACCEPTED_AUTHENTICATORS:
        return rc.UNKNOWN_AUTHENTICATOR
    if identity.verified_at is None:
        return rc.INVALID_IDENTITY
    return None


def _validate_principal(request: AuthorizationRequest) -> Optional[str]:
    principal = request.principal
    identity = request.identity
    if principal is None or not principal.principal_id:
        return rc.PRINCIPAL_UNRESOLVED
    if not principal.identity_id or principal.identity_id != identity.identity_id:
        return rc.PRINCIPAL_UNRESOLVED
    return None


def _validate_request_shape(request: AuthorizationRequest) -> Optional[str]:
    if not request.correlation_id:
        return rc.MALFORMED_REQUEST
    if not request.capability_id:
        return rc.MALFORMED_REQUEST
    if request.resource is None or not request.resource.resource_id:
        return rc.MALFORMED_REQUEST
    if request.operation is None:
        return rc.UNKNOWN_OPERATION
    # G-02: closed Operation enum
    if not isinstance(request.operation, Operation):
        return rc.UNKNOWN_OPERATION
    if request.resource.resource_kind is None:
        return rc.UNKNOWN_RESOURCE_KIND
    # G-02: closed ResourceKind enum
    if not isinstance(request.resource.resource_kind, ResourceKind):
        return rc.UNKNOWN_RESOURCE_KIND
    return None


def _validate_capability_enums(capability: Capability) -> Optional[str]:
    """G-02: every capability.operations member and selector kinds ∈ closed enums."""
    if not capability.operations:
        return rc.INVALID_CAPABILITY
    for op in capability.operations:
        if not isinstance(op, Operation):
            return rc.UNKNOWN_OPERATION
    selector = capability.resource_selector
    if isinstance(selector, ResourceSelectorExact):
        if not selector.resource_ids:
            return rc.INVALID_CAPABILITY
    elif isinstance(selector, ResourceSelectorStructured):
        if not selector.kinds:
            return rc.INVALID_CAPABILITY
        for kind in selector.kinds:
            if not isinstance(kind, ResourceKind):
                return rc.UNKNOWN_RESOURCE_KIND
    else:
        return rc.INVALID_CAPABILITY
    return None


def _validate_expiration(capability: Capability, now: datetime) -> Optional[str]:
    nb = capability.not_before
    na = capability.not_after
    if nb.tzinfo is None:
        nb = nb.replace(tzinfo=timezone.utc)
    if na.tzinfo is None:
        na = na.replace(tzinfo=timezone.utc)
    n = now if now.tzinfo else now.replace(tzinfo=timezone.utc)
    if na <= nb:
        return rc.INVALID_CAPABILITY
    if n < nb:
        return rc.EXPIRED_CAPABILITY
    if n > na:
        return rc.EXPIRED_CAPABILITY
    return None


def _policy_structurally_valid(policy: Policy, now: datetime) -> Optional[str]:
    """ASA-004: structural policy checks only (full use-rules → ASA-006)."""
    if policy.status != "active":
        return rc.POLICY_NOT_ACTIVE
    if not isinstance(policy.body, dict):
        return rc.INVALID_POLICY
    if len(policy.body) == 0:
        return rc.INVALID_POLICY
    if policy.not_after is not None:
        na = policy.not_after
        if na.tzinfo is None:
            na = na.replace(tzinfo=timezone.utc)
        n = now if now.tzinfo else now.replace(tzinfo=timezone.utc)
        if n > na:
            return rc.INVALID_POLICY
    return None


def authorize(
    request: AuthorizationRequest,
    *,
    capability_store: CapabilityStore,
    policy_store: PolicyStore,
    revocation_store: RevocationStore,
    authority_registry: AuthorityRegistry,
    audit_sink: AuditSink,
    now: Optional[datetime] = None,
) -> Decision:
    """Evaluate one authorization request. Always fresh evaluation (no cache).

    Returns Decision. Protected side effects are the caller's responsibility and
    MUST NOT occur unless outcome is ALLOW (I1).
    """
    ts = now or _now()

    # 1. Authenticate → Identity
    err = _validate_identity(request)
    if err:
        decision = _deny(request, err, timestamp=ts)
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # 2. Resolve Principal
    err = _validate_principal(request)
    if err:
        decision = _deny(request, err, timestamp=ts)
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # 3. Validate Request shape (+ G-02 closed enums on request)
    err = _validate_request_shape(request)
    if err:
        decision = _deny(request, err, timestamp=ts)
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # 4. Load Capability
    try:
        capability = capability_store.get(request.capability_id)
    except Exception:
        decision = _deny(
            request,
            rc.INVALID_CAPABILITY,
            capability_id=request.capability_id,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    if capability is None:
        decision = _deny(
            request,
            rc.INVALID_CAPABILITY,
            capability_id=request.capability_id,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # G-03 — Capability self-ID binding
    if capability.capability_id != request.capability_id:
        decision = _deny(
            request,
            rc.INVALID_CAPABILITY,
            capability_id=request.capability_id,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    if capability.principal_id != request.principal.principal_id:
        decision = _deny(
            request,
            rc.CAPABILITY_PRINCIPAL_MISMATCH,
            capability_id=capability.capability_id,
            policy_id=capability.policy_id,
            policy_version=capability.policy_version,
            authority_id=capability.issued_under_authority,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    if not capability.operations or not capability.capability_id:
        decision = _deny(
            request,
            rc.INVALID_CAPABILITY,
            capability_id=capability.capability_id,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # G-02 — capability operations + selector kinds closed enums
    err = _validate_capability_enums(capability)
    if err:
        decision = _deny(
            request,
            err,
            capability_id=capability.capability_id,
            policy_id=capability.policy_id,
            policy_version=capability.policy_version,
            authority_id=capability.issued_under_authority,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # 5. Scope
    if not scope_allows(request.resource, request.operation, capability):
        decision = _deny(
            request,
            rc.SCOPE_DENIED,
            capability_id=capability.capability_id,
            policy_id=capability.policy_id,
            policy_version=capability.policy_version,
            authority_id=capability.issued_under_authority,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # 6. Expiration (every request)
    err = _validate_expiration(capability, ts)
    if err:
        decision = _deny(
            request,
            err,
            capability_id=capability.capability_id,
            policy_id=capability.policy_id,
            policy_version=capability.policy_version,
            authority_id=capability.issued_under_authority,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # 7. Revocation (every request; store down → DENY)
    try:
        if not revocation_store.is_available():
            decision = _deny(
                request,
                rc.REVOCATION_STORE_UNAVAILABLE,
                capability_id=capability.capability_id,
                timestamp=ts,
            )
            if not _append_audit(audit_sink, decision):
                return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
            return decision
        rev = revocation_store.get_revocation(capability.capability_id)
    except Exception:
        decision = _deny(
            request,
            rc.REVOCATION_STORE_UNAVAILABLE,
            capability_id=capability.capability_id,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    if rev is not None and rev.state == "REVOKED":
        decision = _deny(
            request,
            rc.REVOKED_CAPABILITY,
            capability_id=capability.capability_id,
            policy_id=capability.policy_id,
            policy_version=capability.policy_version,
            authority_id=capability.issued_under_authority,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # Authority on capability must be known (not GitHub)
    if not authority_registry.is_known(capability.issued_under_authority):
        decision = _deny(
            request,
            rc.UNKNOWN_AUTHORITY,
            capability_id=capability.capability_id,
            authority_id=capability.issued_under_authority,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # 8. Policy (structural; full engine deferred to ASA-006)
    try:
        policy = policy_store.get(capability.policy_id, capability.policy_version)
    except Exception:
        decision = _deny(
            request,
            rc.POLICY_ENGINE_UNAVAILABLE,
            capability_id=capability.capability_id,
            policy_id=capability.policy_id,
            policy_version=capability.policy_version,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    if policy is None:
        decision = _deny(
            request,
            rc.MISSING_POLICY,
            capability_id=capability.capability_id,
            policy_id=capability.policy_id,
            policy_version=capability.policy_version,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # G-01 — Capability → Policy binding
    if (
        policy.policy_id != capability.policy_id
        or policy.version != capability.policy_version
    ):
        decision = _deny(
            request,
            rc.POLICY_BINDING_MISMATCH,
            capability_id=capability.capability_id,
            policy_id=capability.policy_id,
            policy_version=capability.policy_version,
            authority_id=capability.issued_under_authority,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    if not authority_registry.is_known(policy.authority_id):
        decision = _deny(
            request,
            rc.UNKNOWN_AUTHORITY,
            capability_id=capability.capability_id,
            policy_id=policy.policy_id,
            policy_version=policy.version,
            authority_id=policy.authority_id,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    err = _policy_structurally_valid(policy, ts)
    if err:
        decision = _deny(
            request,
            err,
            capability_id=capability.capability_id,
            policy_id=policy.policy_id,
            policy_version=policy.version,
            authority_id=policy.authority_id,
            timestamp=ts,
        )
        if not _append_audit(audit_sink, decision):
            return _deny(request, rc.AUDIT_UNAVAILABLE, timestamp=ts)
        return decision

    # 9. Decision ALLOW
    decision = _allow(
        request,
        policy_id=policy.policy_id,
        policy_version=policy.version,
        capability_id=capability.capability_id,
        authority_id=capability.issued_under_authority,
        timestamp=ts,
    )

    # 10. Audit — fail-closed if cannot append
    if not _append_audit(audit_sink, decision):
        return _deny(
            request,
            rc.AUDIT_UNAVAILABLE,
            capability_id=capability.capability_id,
            policy_id=policy.policy_id,
            policy_version=policy.version,
            authority_id=capability.issued_under_authority,
            timestamp=ts,
        )

    return decision
