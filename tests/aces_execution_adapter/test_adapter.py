"""Contract and fail-closed tests for ExecutionAdapter (post evidence hardening)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from aces_execution_adapter import (
    AuthorizationRecord,
    ExecutionAdapter,
    ExecutionRequest,
    ExecutionStatus,
    LocalSyntheticRuntime,
    VerificationStatus,
    AcceptedStateStatus,
)
from aces_execution_adapter.runtimes import NullRuntime


NOW = datetime(2026, 9, 1, 18, 30, 0, tzinfo=timezone.utc)


def _auth(**kwargs) -> AuthorizationRecord:
    wall = datetime.now(timezone.utc)
    base = dict(
        principal="Architectural Authority / Human",
        operation="SYNTHETIC_ECHO",
        resource="synthetic://boundary-test",
        scope="local-test only",
        task_id="ea-boundary-001",
        valid_from=wall - timedelta(hours=1),
        valid_until=wall + timedelta(hours=2),
        approval_id="approval-ea-001",
    )
    base.update(kwargs)
    return AuthorizationRecord(**base)


def _req(auth=None, **kwargs) -> ExecutionRequest:
    base = dict(
        request_id="req-1",
        intent_reference="intent:boundary-demo",
        operation="SYNTHETIC_ECHO",
        resource="synthetic://boundary-test",
        scope="local-test only",
        task_id="ea-boundary-001",
        runtime_id=LocalSyntheticRuntime.runtime_id,
        authorization=auth,
        payload={"note": "synthetic"},
        requested_at=NOW,
    )
    base.update(kwargs)
    return ExecutionRequest(**base)


def _adapter() -> ExecutionAdapter:
    a = ExecutionAdapter()
    a.register_runtime(LocalSyntheticRuntime())
    a.register_runtime(NullRuntime())
    return a


def test_happy_path_succeeds_but_accepted_state_not_established():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth()))
    assert r.status == ExecutionStatus.SUCCEEDED
    assert r.verification_status == VerificationStatus.PENDING
    assert r.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED


def test_missing_authorization_fail_closed():
    a = _adapter()
    r = a.dispatch(_req(auth=None))
    assert r.status == ExecutionStatus.REJECTED
    assert r.reject_reason == "missing_authorization"


def test_operation_mismatch_fail_closed():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth(operation="OTHER_OP")))
    assert r.status == ExecutionStatus.REJECTED


def test_resource_mismatch_fail_closed():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth(resource="synthetic://other")))
    assert r.status == ExecutionStatus.REJECTED


def test_scope_mismatch_fail_closed():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth(scope="production")))
    assert r.status == ExecutionStatus.REJECTED


def test_expired_authorization_fail_closed():
    a = _adapter()
    r = a.dispatch(
        _req(
            auth=_auth(
                valid_from=NOW - timedelta(days=2),
                valid_until=NOW - timedelta(days=1),
            )
        )
    )
    assert r.status == ExecutionStatus.REJECTED


def test_unknown_runtime_fail_closed():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth(), runtime_id="no-such-runtime"))
    assert r.status == ExecutionStatus.REJECTED


def test_runtime_failure_does_not_accept():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth(), payload={"force_runtime_failure": True}))
    assert r.status == ExecutionStatus.FAILED
    assert r.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED


def test_null_runtime_replaceable_failure():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth(), runtime_id=NullRuntime.runtime_id))
    assert r.status == ExecutionStatus.FAILED


def test_legacy_apply_verification_true_does_not_establish():
    """HARDENING: caller boolean alone cannot establish AcceptedState."""
    a = _adapter()
    r = a.dispatch(_req(auth=_auth()))
    v = a.apply_verification(r, passed=True, verifier_id="test-verifier")
    assert v.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED
    assert v.verification_status == VerificationStatus.FAILED


def test_verification_fail_keeps_not_established():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth()))
    v = a.apply_verification(r, passed=False, verifier_id="test-verifier")
    assert v.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED


def test_execution_success_alone_never_equals_accepted_state():
    a = _adapter()
    r = a.dispatch(_req(auth=_auth()))
    assert r.status == ExecutionStatus.SUCCEEDED
    assert r.accepted_state != AcceptedStateStatus.ESTABLISHED


def test_dsh_is_not_registered_as_authority():
    a = _adapter()
    assert "dsh" not in a._runtimes
