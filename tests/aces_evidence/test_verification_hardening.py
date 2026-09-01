"""Evidence/Verification hardening — close caller-boolean AcceptedState shortcut."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from aces_evidence import (
    InMemoryEvidenceStore,
    InMemoryVerifierRegistry,
    InMemoryVerificationLedger,
    VerificationService,
    VerifierRecord,
    VerificationOutcome,
)
from aces_execution_adapter import (
    AuthorizationRecord,
    ExecutionAdapter,
    ExecutionRequest,
    ExecutionStatus,
    LocalSyntheticRuntime,
    AcceptedStateStatus,
    VerificationStatus,
)

NOW = datetime(2026, 9, 1, 20, 0, 0, tzinfo=timezone.utc)
TASK = "ev-task-001"
OP = "SYNTHETIC_ECHO"
RES = "synthetic://ev-boundary"
SCOPE = "local-test only"


def _auth():
    wall = datetime.now(timezone.utc)
    return AuthorizationRecord(
        principal="Architectural Authority / Human",
        operation=OP,
        resource=RES,
        scope=SCOPE,
        task_id=TASK,
        valid_from=wall - timedelta(hours=1),
        valid_until=wall + timedelta(hours=2),
        approval_id="approval-ev-001",
    )


def _dispatch(adapter=None, force_fail=False):
    a = adapter or ExecutionAdapter()
    a.register_runtime(LocalSyntheticRuntime())
    req = ExecutionRequest(
        request_id="req-ev-1",
        intent_reference="intent:ev",
        operation=OP,
        resource=RES,
        scope=SCOPE,
        task_id=TASK,
        runtime_id=LocalSyntheticRuntime.runtime_id,
        authorization=_auth(),
        payload={"force_runtime_failure": True} if force_fail else {"note": "synthetic"},
        requested_at=NOW,
    )
    return a, a.dispatch(req)


def _service(trusted=True, evidence_ok=True, verifier_ok=True):
    estore = InMemoryEvidenceStore(available=evidence_ok)
    vreg = InMemoryVerifierRegistry(available=verifier_ok)
    if verifier_ok:
        vreg.register(
            VerifierRecord(
                verifier_id="verifier.trusted.v1",
                label="Synthetic trusted verifier",
                trusted=trusted,
            )
        )
        vreg.register(
            VerifierRecord(
                verifier_id="verifier.untrusted.v1",
                label="Untrusted",
                trusted=False,
            )
        )
    return VerificationService(
        evidence_store=estore,
        verifier_registry=vreg,
        ledger=InMemoryVerificationLedger(),
    ), estore, vreg


def test_success_without_evidence_no_accepted_state():
    a, r = _dispatch()
    assert r.status == ExecutionStatus.SUCCEEDED
    assert r.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED


def test_caller_passed_true_without_service_rejected():
    a, r = _dispatch()
    v = a.apply_verification(r, passed=True, verifier_id="anyone")
    assert v.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED
    assert v.verification_status == VerificationStatus.FAILED
    assert "evidence_required" in v.provenance.get("verify_reason", "")


def test_unknown_verifier_rejected():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.unknown",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.outcome == VerificationOutcome.REJECTED
    assert d.reason == "unknown_verifier"
    assert d.result.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED


def test_untrusted_verifier_rejected():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.untrusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.reason == "untrusted_verifier"
    assert d.result.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED


def test_missing_evidence_rejected():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    d = svc.verify(
        r, evidence_id="missing", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.reason == "missing_evidence"


def test_mismatched_task_rejected():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id="OTHER-TASK", operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.reason == "task_mismatch"


def test_mismatched_resource_rejected():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource="synthetic://other", scope=SCOPE,
    )
    assert d.reason in ("resource_mismatch", "fingerprint_mismatch")


def test_failed_execution_cannot_accept():
    svc, estore, vreg = _service()
    a, r = _dispatch(force_fail=True)
    assert r.status == ExecutionStatus.FAILED
    d = svc.verify(
        r, evidence_id="ev-fail", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.result.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED
    assert d.reason == "execution_not_succeeded"


def test_replayed_verification_rejected():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    d1 = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d1.outcome == VerificationOutcome.ACCEPTED
    d2 = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d2.reason == "replayed_verification"
    assert d2.result.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED


def test_evidence_store_unavailable_fail_closed():
    svc, estore, vreg = _service(evidence_ok=False)
    a, r = _dispatch()
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.reason == "evidence_store_unavailable"


def test_verifier_registry_unavailable_fail_closed():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    vreg.set_available(False)
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.reason == "verifier_registry_unavailable"


def test_valid_path_establishes_accepted_state():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert d.outcome == VerificationOutcome.ACCEPTED
    assert d.result.accepted_state == AcceptedStateStatus.ESTABLISHED
    assert d.result.verification_status == VerificationStatus.PASSED


def test_adapter_path_with_service_accepts():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    v = a.apply_verification(
        r,
        passed=True,
        verifier_id="verifier.trusted.v1",
        evidence_id="ev-1",
        verification_service=svc,
        task_id=TASK,
        operation=OP,
        resource=RES,
        scope=SCOPE,
    )
    assert v.accepted_state == AcceptedStateStatus.ESTABLISHED


def test_legacy_shortcut_broken_explicitly():
    a, r = _dispatch()
    assert r.status == ExecutionStatus.SUCCEEDED
    v = a.apply_verification(r, passed=True, verifier_id="forged-verifier")
    assert v.accepted_state != AcceptedStateStatus.ESTABLISHED


def test_verification_does_not_create_authorization():
    svc, estore, vreg = _service()
    a, r = _dispatch()
    svc.register_evidence_from_result(
        r, evidence_id="ev-1", task_id=TASK, operation=OP, resource=RES, scope=SCOPE
    )
    d = svc.verify(
        r, evidence_id="ev-1", verifier_id="verifier.trusted.v1",
        task_id=TASK, operation=OP, resource=RES, scope=SCOPE,
    )
    assert not hasattr(d, "authorization")
