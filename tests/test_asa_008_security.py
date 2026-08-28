"""ASA-008 Security Test Gate for ASA-004.

READ-ONLY test harness: deterministic in-memory fakes implement existing ports.
No production stores, authenticators, policy language, or host integration.
Run with: PYTHONPATH=src python -m unittest discover -s tests -p 'test_asa_008_security.py' -v
"""

import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from asa.authorize import authorize
from asa import reason_codes as rc
from asa.types import (
    AuthorizationEvent,
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
    ResourceSelectorStructured,
    RevocationRecord,
)

NOW = datetime(2026, 8, 28, 12, 0, tzinfo=timezone.utc)


class CapabilityFake:
    def __init__(self, capability):
        self.capability = capability
        self.calls = 0
        self.raise_error = False

    def get(self, capability_id):
        self.calls += 1
        if self.raise_error:
            raise RuntimeError("capability store unavailable")
        return self.capability


class PolicyFake:
    def __init__(self, policy):
        self.policy = policy
        self.calls = 0
        self.raise_error = False

    def get(self, policy_id, version):
        self.calls += 1
        if self.raise_error:
            raise RuntimeError("policy store unavailable")
        return self.policy


class RevocationFake:
    def __init__(self, revocation=None, available=True):
        self.revocation = revocation
        self.available = available
        self.calls = 0
        self.raise_error = False

    def is_available(self):
        if self.raise_error:
            raise RuntimeError("revocation availability failure")
        return self.available

    def get_revocation(self, capability_id):
        self.calls += 1
        if self.raise_error:
            raise RuntimeError("revocation lookup failure")
        return self.revocation


class AuthorityFake:
    def __init__(self, known=True):
        self.known = known
        self.calls = []
        self.raise_error = False

    def is_known(self, authority_id):
        self.calls.append(authority_id)
        if self.raise_error:
            raise RuntimeError("authority registry unavailable")
        return self.known


class AuditFake:
    def __init__(self, result=True):
        self.result = result
        self.events = []
        self.raise_error = False

    def append(self, event: AuthorizationEvent):
        self.events.append(event)
        if self.raise_error:
            raise RuntimeError("audit unavailable")
        return self.result


class ASA008TestCase(unittest.TestCase):
    def setUp(self):
        self.identity = Identity(
            identity_id="id-1",
            authenticator_id="architectural_authority_human",
            subject_ref="subject-1",
            verified_at=NOW,
        )
        self.principal = Principal(
            principal_id="principal-1",
            identity_id="id-1",
        )
        self.resource = ResourceRef(
            resource_id="res-1",
            resource_kind=ResourceKind.KnowledgeObject,
            namespace="ns-a",
        )
        self.capability = Capability(
            capability_id="cap-1",
            principal_id="principal-1",
            resource_selector=ResourceSelectorExact(("res-1",)),
            operations=(Operation.READ,),
            not_before=NOW - timedelta(hours=1),
            not_after=NOW + timedelta(hours=1),
            issued_under_authority="authority-1",
            policy_id="policy-1",
            policy_version="v1",
        )
        self.policy = Policy(
            policy_id="policy-1",
            version="v1",
            authority_id="authority-1",
            body={"use": {"operation": "READ"}},
            status="active",
        )
        self.cap_store = CapabilityFake(self.capability)
        self.policy_store = PolicyFake(self.policy)
        self.rev_store = RevocationFake()
        self.authority = AuthorityFake(True)
        self.audit = AuditFake(True)

    def request(self, **changes):
        base = AuthorizationRequest(
            correlation_id="corr-1",
            identity=self.identity,
            principal=self.principal,
            capability_id="cap-1",
            resource=self.resource,
            operation=Operation.READ,
        )
        return replace(base, **changes)

    def auth(self, request=None, **kwargs):
        return authorize(
            request or self.request(),
            capability_store=kwargs.get("capability_store", self.cap_store),
            policy_store=kwargs.get("policy_store", self.policy_store),
            revocation_store=kwargs.get("revocation_store", self.rev_store),
            authority_registry=kwargs.get("authority_registry", self.authority),
            audit_sink=kwargs.get("audit_sink", self.audit),
            now=NOW,
        )

    def assert_deny(self, decision, reason=None):
        self.assertEqual(decision.outcome, DecisionOutcome.DENY)
        if reason:
            self.assertEqual(decision.reason_code, reason)

    # I2 — Identity / Principal
    def test_i2_valid_identity_continues_to_allow(self):
        self.assertEqual(self.auth().outcome, DecisionOutcome.ALLOW)

    def test_i2_unknown_authenticator_denies(self):
        identity = replace(self.identity, authenticator_id="unknown-auth")
        self.assert_deny(self.auth(self.request(identity=identity)), rc.UNKNOWN_AUTHENTICATOR)

    def test_i2_missing_identity_denies(self):
        self.assert_deny(self.auth(self.request(identity=None)), rc.UNKNOWN_IDENTITY)

    def test_i2_invalid_identity_denies(self):
        identity = replace(self.identity, identity_id="", subject_ref="")
        self.assert_deny(self.auth(self.request(identity=identity)), rc.INVALID_IDENTITY)

    def test_i2_principal_mismatch_denies(self):
        principal = replace(self.principal, identity_id="other-id")
        self.assert_deny(self.auth(self.request(principal=principal)), rc.PRINCIPAL_UNRESOLVED)

    # I3 — Scope
    def test_i3_exact_resource_match_allows(self):
        self.assertEqual(self.auth().outcome, DecisionOutcome.ALLOW)

    def test_i3_exact_resource_mismatch_denies(self):
        resource = replace(self.resource, resource_id="res-other")
        self.assert_deny(self.auth(self.request(resource=resource)), rc.SCOPE_DENIED)

    def test_i3_kinds_namespace_match_allows(self):
        cap = replace(
            self.capability,
            resource_selector=ResourceSelectorStructured(
                kinds=(ResourceKind.KnowledgeObject,), namespace="ns-a"
            ),
        )
        self.cap_store.capability = cap
        self.assertEqual(self.auth().outcome, DecisionOutcome.ALLOW)

    def test_i3_namespace_mismatch_denies(self):
        cap = replace(
            self.capability,
            resource_selector=ResourceSelectorStructured(
                kinds=(ResourceKind.KnowledgeObject,), namespace="ns-b"
            ),
        )
        self.cap_store.capability = cap
        self.assert_deny(self.auth(), rc.SCOPE_DENIED)

    def test_i3_glob_pattern_denies(self):
        cap = replace(self.capability, resource_selector=SimpleNamespace(pattern="res-*"))
        self.cap_store.capability = cap
        self.assert_deny(self.auth(), rc.INVALID_CAPABILITY)

    def test_i3_regex_pattern_denies(self):
        cap = replace(self.capability, resource_selector=SimpleNamespace(regex=r"^res-.*$"))
        self.cap_store.capability = cap
        self.assert_deny(self.auth(), rc.INVALID_CAPABILITY)

    def test_i3_cel_pattern_denies(self):
        cap = replace(self.capability, resource_selector=SimpleNamespace(cel="resource.id == 'res-1'"))
        self.cap_store.capability = cap
        self.assert_deny(self.auth(), rc.INVALID_CAPABILITY)

    # Closed enums
    def test_enum_invalid_operation_denies(self):
        self.assert_deny(self.auth(self.request(operation="READ")), rc.UNKNOWN_OPERATION)

    def test_enum_invalid_resource_kind_denies(self):
        resource = replace(self.resource, resource_kind="KnowledgeObject")
        self.assert_deny(self.auth(self.request(resource=resource)), rc.UNKNOWN_RESOURCE_KIND)

    def test_enum_invalid_capability_operation_denies(self):
        cap = replace(self.capability, operations=("READ",))
        self.cap_store.capability = cap
        self.assert_deny(self.auth(), rc.UNKNOWN_OPERATION)

    def test_enum_invalid_selector_kind_denies(self):
        selector = ResourceSelectorStructured(kinds=("KnowledgeObject",), namespace="ns-a")
        self.cap_store.capability = replace(self.capability, resource_selector=selector)
        self.assert_deny(self.auth(), rc.UNKNOWN_RESOURCE_KIND)

    # Capability
    def test_capability_missing_denies(self):
        self.cap_store.capability = None
        self.assert_deny(self.auth(), rc.INVALID_CAPABILITY)

    def test_capability_store_error_denies(self):
        self.cap_store.raise_error = True
        self.assert_deny(self.auth(), rc.INVALID_CAPABILITY)

    def test_capability_principal_mismatch_denies(self):
        self.cap_store.capability = replace(self.capability, principal_id="other-principal")
        self.assert_deny(self.auth(), rc.CAPABILITY_PRINCIPAL_MISMATCH)

    def test_capability_self_id_mismatch_denies(self):
        self.cap_store.capability = replace(self.capability, capability_id="other-cap")
        self.assert_deny(self.auth(), rc.INVALID_CAPABILITY)

    def test_capability_invalid_window_denies(self):
        self.cap_store.capability = replace(
            self.capability,
            not_before=NOW + timedelta(hours=1),
            not_after=NOW - timedelta(hours=1),
        )
        self.assert_deny(self.auth(), rc.INVALID_CAPABILITY)

    # Expiration
    def test_expiration_before_not_before_denies(self):
        cap = replace(self.capability, not_before=NOW + timedelta(minutes=1))
        self.cap_store.capability = cap
        self.assert_deny(self.auth(), rc.EXPIRED_CAPABILITY)

    def test_expiration_inside_window_continues(self):
        self.assertEqual(self.auth().outcome, DecisionOutcome.ALLOW)

    def test_expiration_after_not_after_denies(self):
        cap = replace(self.capability, not_after=NOW - timedelta(minutes=1))
        self.cap_store.capability = cap
        self.assert_deny(self.auth(), rc.EXPIRED_CAPABILITY)

    # Revocation
    def test_revocation_revoked_denies(self):
        self.rev_store.revocation = RevocationRecord(
            capability_id="cap-1",
            revoked_at=NOW,
            revoked_under_authority="authority-1",
            state="REVOKED",
        )
        self.assert_deny(self.auth(), rc.REVOKED_CAPABILITY)

    def test_revocation_store_unavailable_denies(self):
        self.rev_store.available = False
        self.assert_deny(self.auth(), rc.REVOCATION_STORE_UNAVAILABLE)

    def test_revocation_lookup_failure_denies(self):
        self.rev_store.raise_error = True
        self.assert_deny(self.auth(), rc.REVOCATION_STORE_UNAVAILABLE)

    def test_revocation_fresh_evaluation_no_cached_allow(self):
        first = self.auth()
        self.assertEqual(first.outcome, DecisionOutcome.ALLOW)
        self.rev_store.revocation = RevocationRecord(
            capability_id="cap-1",
            revoked_at=NOW,
            revoked_under_authority="authority-1",
            state="REVOKED",
        )
        second = self.auth()
        self.assertEqual(second.outcome, DecisionOutcome.DENY)
        self.assertEqual(second.reason_code, rc.REVOKED_CAPABILITY)
        self.assertEqual(self.rev_store.calls, 2)

    # Policy
    def test_policy_missing_denies(self):
        self.policy_store.policy = None
        self.assert_deny(self.auth(), rc.MISSING_POLICY)

    def test_policy_store_failure_denies(self):
        self.policy_store.raise_error = True
        self.assert_deny(self.auth(), rc.POLICY_ENGINE_UNAVAILABLE)

    def test_policy_inactive_denies(self):
        self.policy_store.policy = replace(self.policy, status="inactive")
        self.assert_deny(self.auth(), rc.POLICY_NOT_ACTIVE)

    def test_policy_empty_body_denies(self):
        self.policy_store.policy = replace(self.policy, body={})
        self.assert_deny(self.auth(), rc.INVALID_POLICY)

    def test_policy_invalid_body_denies(self):
        self.policy_store.policy = replace(self.policy, body=None)
        self.assert_deny(self.auth(), rc.INVALID_POLICY)

    def test_policy_authority_unknown_denies(self):
        self.authority.known = False
        self.assert_deny(self.auth(), rc.UNKNOWN_AUTHORITY)

    def test_policy_id_mismatch_denies(self):
        self.policy_store.policy = replace(self.policy, policy_id="policy-other")
        self.assert_deny(self.auth(), rc.POLICY_BINDING_MISMATCH)

    def test_policy_version_mismatch_denies(self):
        self.policy_store.policy = replace(self.policy, version="v2")
        self.assert_deny(self.auth(), rc.POLICY_BINDING_MISMATCH)

    def test_policy_binding_match_continues_to_allow(self):
        self.assertEqual(self.auth().outcome, DecisionOutcome.ALLOW)

    # Authority / GitHub separation
    def test_authority_known_allows(self):
        self.assertEqual(self.auth().outcome, DecisionOutcome.ALLOW)

    def test_authority_unknown_denies(self):
        self.authority.known = False
        self.assert_deny(self.auth(), rc.UNKNOWN_AUTHORITY)

    def test_github_role_fields_do_not_participate(self):
        class CapabilityWithGithubFields:
            pass
        cap = CapabilityWithGithubFields()
        for name in (
            "capability_id", "principal_id", "resource_selector", "operations",
            "not_before", "not_after", "issued_under_authority", "policy_id",
            "policy_version", "purpose",
        ):
            setattr(cap, name, getattr(self.capability, name))
        cap.github_admin = False
        cap.github_maintain = False
        cap.github_push = False
        cap.github_triage = False
        self.cap_store.capability = cap
        first = self.auth()
        cap.github_admin = True
        cap.github_maintain = True
        cap.github_push = True
        cap.github_triage = True
        second = self.auth()
        self.assertEqual(first.outcome, DecisionOutcome.ALLOW)
        self.assertEqual(second.outcome, DecisionOutcome.ALLOW)

    # Audit / I7
    def test_audit_success_preserves_allow(self):
        decision = self.auth()
        self.assertEqual(decision.outcome, DecisionOutcome.ALLOW)
        self.assertEqual(len(self.audit.events), 1)
        self.assertEqual(self.audit.events[0].decision, DecisionOutcome.ALLOW)

    def test_audit_failure_denies(self):
        self.audit.result = False
        self.assert_deny(self.auth(), rc.AUDIT_UNAVAILABLE)

    def test_authorization_event_cannot_itself_produce_allow(self):
        self.rev_store.revocation = RevocationRecord(
            capability_id="cap-1", revoked_at=NOW,
            revoked_under_authority="authority-1", state="REVOKED"
        )
        denied = self.auth()
        self.assertEqual(denied.outcome, DecisionOutcome.DENY)
        self.assertEqual(self.audit.events[0].decision, DecisionOutcome.DENY)
        self.assertIsInstance(self.audit.events[0], AuthorizationEvent)

    # Fail-closed error conditions
    def test_authority_registry_error_denies(self):
        self.authority.raise_error = True
        self.assert_deny(self.auth(), rc.UNKNOWN_AUTHORITY)

    def test_audit_exception_denies(self):
        self.audit.raise_error = True
        self.assert_deny(self.auth(), rc.AUDIT_UNAVAILABLE)

    def test_i1_decision_contract_allows_side_effect_only_on_allow(self):
        allow = self.auth()
        self.assertEqual(allow.outcome, DecisionOutcome.ALLOW)
        self.assertTrue(allow.outcome == DecisionOutcome.ALLOW)
        self.rev_store.revocation = RevocationRecord(
            capability_id="cap-1", revoked_at=NOW,
            revoked_under_authority="authority-1", state="REVOKED"
        )
        deny = self.auth()
        self.assertEqual(deny.outcome, DecisionOutcome.DENY)
        self.assertFalse(deny.outcome == DecisionOutcome.ALLOW)


if __name__ == "__main__":
    unittest.main()
