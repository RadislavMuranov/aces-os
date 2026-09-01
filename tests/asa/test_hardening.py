"""ASA Hardening contract tests — authenticity + semantics + adapter handoff."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from asa.gate import AuthorityGate
from asa.handoff import build_adapter_authorization, dispatch_if_allowed
from asa.memory_stores import (
    InMemoryAuditSink,
    InMemoryAuthorityRegistry,
    InMemoryCapabilityStore,
    InMemoryPolicyStore,
    InMemoryRevocationStore,
)
from asa.types import (
    AuthorizationRequest,
    Capability,
    DecisionOutcome,
    Identity,
    Operation,
    Policy,
    Principal,
    ResourceKind,
    ResourceRef,
    ResourceSelectorExact,
    RevocationRecord,
)
from aces_execution_adapter import (
    ExecutionAdapter,
    ExecutionRequest,
    ExecutionStatus,
    LocalSyntheticRuntime,
)


NOW = datetime(2026, 9, 1, 19, 0, 0, tzinfo=timezone.utc)
AUTH_ID = "authority.architectural.v1"
POLICY_ID = "policy.protected-artifact.v1"
POLICY_VER = "1"
CAP_ID = "cap-test-001"
PRINCIPAL_ID = "principal-human-1"
IDENTITY_ID = "identity-human-1"
RESOURCE_ID = "synthetic://asa-boundary-test"


def _fixture():
    caps = InMemoryCapabilityStore()
    policies = InMemoryPolicyStore()
    revs = InMemoryRevocationStore(available=True)
    authorities = InMemoryAuthorityRegistry({AUTH_ID})
    audit = InMemoryAuditSink(available=True)

    policies.put(
        Policy(
            policy_id=POLICY_ID,
            version=POLICY_VER,
            authority_id=AUTH_ID,
            body={"rule": "exact-resource-execute"},
            status="active",
        )
    )
    caps.put(
        Capability(
            capability_id=CAP_ID,
            principal_id=PRINCIPAL_ID,
            resource_selector=ResourceSelectorExact(resource_ids=(RESOURCE_ID,)),
            operations=(Operation.EXECUTE, Operation.CREATE),
            not_before=NOW - timedelta(hours=1),
            not_after=NOW + timedelta(hours=2),
            issued_under_authority=AUTH_ID,
            policy_id=POLICY_ID,
            policy_version=POLICY_VER,
            purpose="asa-hardening-test",
        )
    )
    gate = AuthorityGate(
        capability_store=caps,
        policy_store=policies,
        revocation_store=revs,
        authority_registry=authorities,
        audit_sink=audit,
    )
    return gate, caps, policies, revs, authorities, audit


def _req(**kwargs) -> AuthorizationRequest:
    base = dict(
        correlation_id="corr-1",
        identity=Identity(
            identity_id=IDENTITY_ID,
            authenticator_id="architectural_authority_human",
            subject_ref="human:test",
            verified_at=NOW - timedelta(minutes=5),
        ),
        principal=Principal(principal_id=PRINCIPAL_ID, identity_id=IDENTITY_ID),
        capability_id=CAP_ID,
        resource=ResourceRef(
            resource_id=RESOURCE_ID,
            resource_kind=ResourceKind.ProtectedArtifact,
            namespace="test",
        ),
        operation=Operation.EXECUTE,
    )
    base.update(kwargs)
    return AuthorizationRequest(**base)


def test_valid_authorization_allow():
    gate, *_ = _fixture()
    gd = gate.evaluate(_req(), now=NOW)
    assert gd.outcome == DecisionOutcome.ALLOW
    assert gd.may_dispatch is True
    assert gd.reason_code == "ALLOW"


def test_forged_unknown_capability_reject():
    gate, *_ = _fixture()
    gd = gate.evaluate(_req(capability_id="cap-forged-unknown"), now=NOW)
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.may_dispatch is False
    assert gd.reason_code == "INVALID_CAPABILITY"


def test_unknown_authority_reject():
    gate, caps, policies, revs, authorities, audit = _fixture()
    caps.put(
        Capability(
            capability_id="cap-bad-auth",
            principal_id=PRINCIPAL_ID,
            resource_selector=ResourceSelectorExact(resource_ids=(RESOURCE_ID,)),
            operations=(Operation.EXECUTE,),
            not_before=NOW - timedelta(hours=1),
            not_after=NOW + timedelta(hours=2),
            issued_under_authority="authority.unknown",
            policy_id=POLICY_ID,
            policy_version=POLICY_VER,
        )
    )
    gd = gate.evaluate(_req(capability_id="cap-bad-auth"), now=NOW)
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "UNKNOWN_AUTHORITY"
    assert gd.may_dispatch is False


def test_expired_capability_reject():
    gate, caps, *_ = _fixture()
    caps.put(
        Capability(
            capability_id="cap-expired",
            principal_id=PRINCIPAL_ID,
            resource_selector=ResourceSelectorExact(resource_ids=(RESOURCE_ID,)),
            operations=(Operation.EXECUTE,),
            not_before=NOW - timedelta(days=3),
            not_after=NOW - timedelta(days=1),
            issued_under_authority=AUTH_ID,
            policy_id=POLICY_ID,
            policy_version=POLICY_VER,
        )
    )
    gd = gate.evaluate(_req(capability_id="cap-expired"), now=NOW)
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "EXPIRED_CAPABILITY"


def test_revoked_capability_reject():
    gate, caps, policies, revs, *_ = _fixture()
    revs.revoke(
        RevocationRecord(
            capability_id=CAP_ID,
            revoked_at=NOW - timedelta(minutes=1),
            revoked_under_authority=AUTH_ID,
            state="REVOKED",
        )
    )
    gd = gate.evaluate(_req(), now=NOW)
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "REVOKED_CAPABILITY"
    assert gd.may_dispatch is False


def test_operation_mismatch_scope_denied():
    gate, *_ = _fixture()
    gd = gate.evaluate(_req(operation=Operation.DELETE), now=NOW)
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "SCOPE_DENIED"


def test_resource_mismatch_scope_denied():
    gate, *_ = _fixture()
    gd = gate.evaluate(
        _req(
            resource=ResourceRef(
                resource_id="synthetic://other-resource",
                resource_kind=ResourceKind.ProtectedArtifact,
            )
        ),
        now=NOW,
    )
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "SCOPE_DENIED"


def test_principal_substitution_reject():
    gate, *_ = _fixture()
    gd = gate.evaluate(
        _req(principal=Principal(principal_id="principal-attacker", identity_id=IDENTITY_ID)),
        now=NOW,
    )
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "CAPABILITY_PRINCIPAL_MISMATCH"


def test_missing_policy_fail_closed():
    gate, caps, policies, revs, authorities, audit = _fixture()
    caps.put(
        Capability(
            capability_id="cap-no-policy",
            principal_id=PRINCIPAL_ID,
            resource_selector=ResourceSelectorExact(resource_ids=(RESOURCE_ID,)),
            operations=(Operation.EXECUTE,),
            not_before=NOW - timedelta(hours=1),
            not_after=NOW + timedelta(hours=2),
            issued_under_authority=AUTH_ID,
            policy_id="policy.missing",
            policy_version="9",
        )
    )
    gd = gate.evaluate(_req(capability_id="cap-no-policy"), now=NOW)
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "MISSING_POLICY"


def test_revocation_store_unavailable_fail_closed():
    gate, caps, policies, revs, authorities, audit = _fixture()
    revs.set_available(False)
    gd = gate.evaluate(_req(), now=NOW)
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "REVOCATION_STORE_UNAVAILABLE"


def test_audit_unavailable_fail_closed():
    gate, caps, policies, revs, authorities, audit = _fixture()
    audit.set_available(False)
    gd = gate.evaluate(_req(), now=NOW)
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "AUDIT_UNAVAILABLE"
    assert gd.may_dispatch is False


def test_unknown_identity_reject():
    gate, *_ = _fixture()
    gd = gate.evaluate(
        _req(
            identity=Identity(
                identity_id="x",
                authenticator_id="not-an-accepted-authenticator",
                subject_ref="x",
                verified_at=NOW,
            )
        ),
        now=NOW,
    )
    assert gd.outcome == DecisionOutcome.DENY
    assert gd.reason_code == "UNKNOWN_AUTHENTICATOR"


def test_deny_handoff_no_authorization_record():
    gate, *_ = _fixture()
    gd = gate.evaluate(_req(capability_id="missing"), now=NOW)
    handoff = build_adapter_authorization(
        gd.decision,
        scope="local-test only",
        task_id="asa-h-001",
        valid_from=NOW,
        valid_until=NOW + timedelta(hours=1),
    )
    assert handoff.authorized is False
    assert handoff.authorization_record is None


def test_allow_handoff_builds_record():
    gate, *_ = _fixture()
    gd = gate.evaluate(_req(), now=NOW)
    handoff = build_adapter_authorization(
        gd.decision,
        scope="local-test only",
        task_id="asa-h-001",
        valid_from=NOW,
        valid_until=NOW + timedelta(hours=1),
    )
    assert handoff.authorized is True
    assert handoff.authorization_record is not None
    assert handoff.authorization_record.resource == RESOURCE_ID


def test_asa_block_adapter_not_called():
    gate, *_ = _fixture()
    gd = gate.evaluate(_req(capability_id="forged"), now=NOW)
    handoff = build_adapter_authorization(
        gd.decision,
        scope="local-test only",
        task_id="asa-h-001",
        valid_from=NOW,
        valid_until=NOW + timedelta(hours=1),
    )
    adapter = ExecutionAdapter()
    adapter.register_runtime(LocalSyntheticRuntime())
    called = {"n": 0}
    original = adapter.dispatch

    def tracking_dispatch(req):
        called["n"] += 1
        return original(req)

    adapter.dispatch = tracking_dispatch  # type: ignore
    result = dispatch_if_allowed(adapter, None, handoff)
    assert result is None
    assert called["n"] == 0


def test_asa_allow_adapter_may_be_called():
    gate, *_ = _fixture()
    gd = gate.evaluate(_req(), now=NOW)
    wall = datetime.now(timezone.utc)
    handoff = build_adapter_authorization(
        gd.decision,
        scope="local-test only",
        task_id="asa-h-001",
        valid_from=wall - timedelta(hours=1),
        valid_until=wall + timedelta(hours=2),
    )
    assert handoff.authorized and handoff.authorization_record
    adapter = ExecutionAdapter()
    adapter.register_runtime(LocalSyntheticRuntime())
    req = ExecutionRequest(
        request_id="req-asa-1",
        intent_reference="intent:asa-hardening",
        operation=Operation.EXECUTE.value,
        resource=RESOURCE_ID,
        scope="local-test only",
        task_id="asa-h-001",
        runtime_id=LocalSyntheticRuntime.runtime_id,
        authorization=handoff.authorization_record,
        payload={"note": "synthetic"},
        requested_at=NOW,
    )
    result = dispatch_if_allowed(adapter, req, handoff)
    assert result is not None
    assert result.status == ExecutionStatus.SUCCEEDED
    from aces_execution_adapter import AcceptedStateStatus
    assert result.accepted_state == AcceptedStateStatus.NOT_ESTABLISHED


def test_context_cannot_authorize():
    gate, *_ = _fixture()
    gd = gate.evaluate(
        _req(capability_id="none", context={"claimed_admin": True, "github_role": "admin"}),
        now=NOW,
    )
    assert gd.may_dispatch is False


def test_execution_success_cannot_authorize():
    gate, *_ = _fixture()
    assert gate.evaluate(_req(), now=NOW).may_dispatch
    gate2, caps2, policies2, revs2, _, _ = _fixture()
    revs2.revoke(
        RevocationRecord(
            capability_id=CAP_ID,
            revoked_at=NOW,
            revoked_under_authority=AUTH_ID,
            state="REVOKED",
        )
    )
    gd = gate2.evaluate(_req(), now=NOW)
    assert gd.may_dispatch is False
    assert gd.reason_code == "REVOKED_CAPABILITY"
