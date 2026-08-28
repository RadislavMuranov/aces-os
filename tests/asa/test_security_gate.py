"""ASA-008 Security Test Gate for accepted ASA-004 authorization core.

Deterministic in-memory port fakes only. No production stores, authenticators,
policy language (ASA-006), issuance (ASA-005), or DSH.

Run from repository root:
  PYTHONPATH=src:. python -m unittest discover -s tests/asa -p 'test_*.py' -v

I1: Decision contract is asserted (side effects only when outcome==ALLOW).
Harness cannot enforce arbitrary external callers.
"""

from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from asa import reason_codes as rc
from asa.authorize import authorize
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

try:
    from tests.asa.fakes import (
        InMemoryAuditSink,
        InMemoryAuthorityRegistry,
        InMemoryCapabilityStore,
        InMemoryPolicyStore,
        InMemoryRevocationStore,
    )
except ImportError:  # pragma: no cover
    from fakes import (  # type: ignore
        InMemoryAuditSink,
        InMemoryAuthorityRegistry,
        InMemoryCapabilityStore,
        InMemoryPolicyStore,
        InMemoryRevocationStore,
    )

NOW = datetime(2026, 8, 28, 12, 0, 0, tzinfo=timezone.utc)
AUTH_ID = "aces-authority-1"


class ASA008SecurityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.identity = Identity(
            identity_id="id-1",
            authenticator_id="architectural_authority_human",
            subject_ref="subject-1",
            verified_at=NOW,
        )
        self.principal = Principal(principal_id="principal-1", identity_id="id-1")
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
            issued_under_authority=AUTH_ID,
            policy_id="policy-1",
            policy_version="v1",
        )
        self.policy = Policy(
            policy_id="policy-1",
            version="v1",
            authority_id=AUTH_ID,
            body={"use": {"note": "structural-only"}},
            status="active",
        )
        self.cap_store = InMemoryCapabilityStore({"cap-1": self.capability})
        self.policy_store = InMemoryPolicyStore({("policy-1", "v1"): self.policy})
        self.rev_store = InMemoryRevocationStore()
        self.authority = InMemoryAuthorityRegistry({AUTH_ID})
        self.audit = InMemoryAuditSink(succeed=True)

    def _request(self, **kwargs) -> AuthorizationRequest:
        base = AuthorizationRequest(
            correlation_id="corr-1",
            identity=self.identity,
            principal=self.principal,
            capability_id="cap-1",
            resource=self.resource,
            operation=Operation.READ,
        )
        return replace(base, **kwargs)

    def _auth(self, request: AuthorizationRequest | None = None, **ports):
        return authorize(
            request or self._request(),
            capability_store=ports.get("capability_store", self.cap_store),
            policy_store=ports.get("policy_store", self.policy_store),
            revocation_store=ports.get("revocation_store", self.rev_store),
            authority_registry=ports.get("authority_registry", self.authority),
            audit_sink=ports.get("audit_sink", self.audit),
            now=NOW,
        )

    def _deny(self, decision, reason: str | None = None) -> None:
        self.assertEqual(decision.outcome, DecisionOutcome.DENY)
        if reason is not None:
            self.assertEqual(decision.reason_code, reason)

    def test_i2_valid_identity_allows(self):
        self.assertEqual(self._auth().outcome, DecisionOutcome.ALLOW)

    def test_i2_unknown_authenticator_denies(self):
        ident = replace(self.identity, authenticator_id="not-accepted")
        self._deny(self._auth(self._request(identity=ident)), rc.UNKNOWN_AUTHENTICATOR)

    def test_i2_missing_identity_denies(self):
        self._deny(self._auth(self._request(identity=None)), rc.UNKNOWN_IDENTITY)

    def test_i2_invalid_identity_denies(self):
        ident = replace(self.identity, identity_id="", subject_ref="")
        self._deny(self._auth(self._request(identity=ident)), rc.INVALID_IDENTITY)

    def test_i2_principal_identity_mismatch_denies(self):
        prin = replace(self.principal, identity_id="other")
        self._deny(self._auth(self._request(principal=prin)), rc.PRINCIPAL_UNRESOLVED)

    def test_i3_exact_resource_match_allows(self):
        self.assertEqual(self._auth().outcome, DecisionOutcome.ALLOW)

    def test_i3_exact_resource_mismatch_denies(self):
        res = replace(self.resource, resource_id="res-other")
        self._deny(self._auth(self._request(resource=res)), rc.SCOPE_DENIED)

    def test_i3_kinds_namespace_match_allows(self):
        cap = replace(
            self.capability,
            resource_selector=ResourceSelectorStructured(
                kinds=(ResourceKind.KnowledgeObject,), namespace="ns-a"
            ),
        )
        self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
        self.assertEqual(self._auth().outcome, DecisionOutcome.ALLOW)

    def test_i3_namespace_mismatch_denies(self):
        cap = replace(
            self.capability,
            resource_selector=ResourceSelectorStructured(
                kinds=(ResourceKind.KnowledgeObject,), namespace="ns-b"
            ),
        )
        self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
        self._deny(self._auth(), rc.SCOPE_DENIED)

    def test_i3_unsupported_pattern_selector_denies(self):
        for selector in (
            SimpleNamespace(pattern="res-*"),
            SimpleNamespace(glob="res-*"),
            SimpleNamespace(regex=r"^res"),
            SimpleNamespace(cel="true"),
        ):
            with self.subTest(selector=type(selector).__name__ + str(vars(selector))):
                cap = replace(self.capability, resource_selector=selector)
                self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
                self._deny(self._auth(), rc.INVALID_CAPABILITY)

    def test_enum_invalid_operation_string_denies(self):
        self._deny(self._auth(self._request(operation="READ")), rc.UNKNOWN_OPERATION)

    def test_enum_invalid_resource_kind_string_denies(self):
        res = replace(self.resource, resource_kind="KnowledgeObject")
        self._deny(self._auth(self._request(resource=res)), rc.UNKNOWN_RESOURCE_KIND)

    def test_enum_invalid_capability_operations_element_denies(self):
        cap = replace(self.capability, operations=("READ",))
        self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
        self._deny(self._auth(), rc.UNKNOWN_OPERATION)

    def test_enum_invalid_selector_kind_denies(self):
        sel = ResourceSelectorStructured(kinds=("KnowledgeObject",), namespace="ns-a")
        cap = replace(self.capability, resource_selector=sel)
        self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
        self._deny(self._auth(), rc.UNKNOWN_RESOURCE_KIND)

    def test_capability_missing_denies(self):
        self.cap_store = InMemoryCapabilityStore({})
        self._deny(self._auth(), rc.INVALID_CAPABILITY)

    def test_capability_store_raise_denies(self):
        self.cap_store = InMemoryCapabilityStore({"cap-1": self.capability}, raise_on_get=True)
        self._deny(self._auth(), rc.INVALID_CAPABILITY)

    def test_capability_principal_mismatch_denies(self):
        cap = replace(self.capability, principal_id="other-principal")
        self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
        self._deny(self._auth(), rc.CAPABILITY_PRINCIPAL_MISMATCH)

    def test_capability_self_id_mismatch_denies(self):
        bad = replace(self.capability, capability_id="cap-OTHER")
        self.cap_store = InMemoryCapabilityStore({"cap-1": bad})
        self._deny(self._auth(), rc.INVALID_CAPABILITY)

    def test_capability_inverted_window_denies(self):
        cap = replace(
            self.capability,
            not_before=NOW + timedelta(hours=1),
            not_after=NOW - timedelta(hours=1),
        )
        self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
        self._deny(self._auth(), rc.INVALID_CAPABILITY)

    def test_expiration_before_not_before_denies(self):
        cap = replace(self.capability, not_before=NOW + timedelta(minutes=5))
        self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
        self._deny(self._auth(), rc.EXPIRED_CAPABILITY)

    def test_expiration_inside_window_allows(self):
        self.assertEqual(self._auth().outcome, DecisionOutcome.ALLOW)

    def test_expiration_after_not_after_denies(self):
        cap = replace(self.capability, not_after=NOW - timedelta(minutes=5))
        self.cap_store = InMemoryCapabilityStore({"cap-1": cap})
        self._deny(self._auth(), rc.EXPIRED_CAPABILITY)

    def test_revocation_revoked_denies(self):
        rev = RevocationRecord(
            capability_id="cap-1",
            revoked_at=NOW,
            revoked_under_authority=AUTH_ID,
            state="REVOKED",
        )
        self.rev_store = InMemoryRevocationStore({"cap-1": rev})
        self._deny(self._auth(), rc.REVOKED_CAPABILITY)

    def test_revocation_store_unavailable_denies(self):
        self.rev_store = InMemoryRevocationStore(available=False)
        self._deny(self._auth(), rc.REVOCATION_STORE_UNAVAILABLE)

    def test_revocation_lookup_failure_denies(self):
        self.rev_store = InMemoryRevocationStore(raise_on_get=True)
        self._deny(self._auth(), rc.REVOCATION_STORE_UNAVAILABLE)

    def test_fresh_evaluation_no_cached_allow(self):
        first = self._auth()
        self.assertEqual(first.outcome, DecisionOutcome.ALLOW)
        rev = RevocationRecord(
            capability_id="cap-1",
            revoked_at=NOW,
            revoked_under_authority=AUTH_ID,
            state="REVOKED",
        )
        self.rev_store = InMemoryRevocationStore({"cap-1": rev})
        second = self._auth()
        self.assertEqual(second.outcome, DecisionOutcome.DENY)
        self.assertEqual(second.reason_code, rc.REVOKED_CAPABILITY)
        self.assertGreaterEqual(self.rev_store.get_calls, 1)

    def test_policy_missing_denies(self):
        self.policy_store = InMemoryPolicyStore({})
        self._deny(self._auth(), rc.MISSING_POLICY)

    def test_policy_store_raise_denies(self):
        self.policy_store = InMemoryPolicyStore(
            {("policy-1", "v1"): self.policy}, raise_on_get=True
        )
        self._deny(self._auth(), rc.POLICY_ENGINE_UNAVAILABLE)

    def test_policy_inactive_denies(self):
        pol = replace(self.policy, status="retired")
        self.policy_store = InMemoryPolicyStore({("policy-1", "v1"): pol})
        self._deny(self._auth(), rc.POLICY_NOT_ACTIVE)

    def test_policy_empty_body_denies(self):
        pol = replace(self.policy, body={})
        self.policy_store = InMemoryPolicyStore({("policy-1", "v1"): pol})
        self._deny(self._auth(), rc.INVALID_POLICY)

    def test_policy_invalid_body_type_denies(self):
        pol = replace(self.policy, body="not-a-dict")  # type: ignore[arg-type]
        self.policy_store = InMemoryPolicyStore({("policy-1", "v1"): pol})
        self._deny(self._auth(), rc.INVALID_POLICY)

    def test_policy_authority_unknown_denies(self):
        pol = replace(self.policy, authority_id="unknown-pol-auth")
        self.policy_store = InMemoryPolicyStore({("policy-1", "v1"): pol})
        self._deny(self._auth(), rc.UNKNOWN_AUTHORITY)

    def test_policy_id_mismatch_denies(self):
        pol = replace(self.policy, policy_id="policy-OTHER")
        self.policy_store = InMemoryPolicyStore({("policy-1", "v1"): pol})
        self._deny(self._auth(), rc.POLICY_BINDING_MISMATCH)

    def test_policy_version_mismatch_denies(self):
        pol = replace(self.policy, version="v9")
        self.policy_store = InMemoryPolicyStore({("policy-1", "v1"): pol})
        self._deny(self._auth(), rc.POLICY_BINDING_MISMATCH)

    def test_policy_binding_match_allows(self):
        self.assertEqual(self._auth().outcome, DecisionOutcome.ALLOW)

    def test_authority_known_allows(self):
        self.assertEqual(self._auth().outcome, DecisionOutcome.ALLOW)

    def test_authority_unknown_denies(self):
        self.authority = InMemoryAuthorityRegistry(set())
        self._deny(self._auth(), rc.UNKNOWN_AUTHORITY)

    def test_github_privilege_fields_do_not_affect_decision(self):
        class CapShim:
            pass

        shim = CapShim()
        for name in (
            "capability_id",
            "principal_id",
            "resource_selector",
            "operations",
            "not_before",
            "not_after",
            "issued_under_authority",
            "policy_id",
            "policy_version",
            "purpose",
        ):
            setattr(shim, name, getattr(self.capability, name))
        for flag in ("github_admin", "github_maintain", "github_push", "github_triage"):
            setattr(shim, flag, False)
        self.cap_store = InMemoryCapabilityStore({"cap-1": shim})  # type: ignore[arg-type]
        first = self._auth()
        for flag in ("github_admin", "github_maintain", "github_push", "github_triage"):
            setattr(shim, flag, True)
        second = self._auth()
        self.assertEqual(first.outcome, DecisionOutcome.ALLOW)
        self.assertEqual(second.outcome, DecisionOutcome.ALLOW)

    def test_audit_success_preserves_allow(self):
        d = self._auth()
        self.assertEqual(d.outcome, DecisionOutcome.ALLOW)
        self.assertEqual(len(self.audit.events), 1)
        self.assertEqual(self.audit.events[0].decision, DecisionOutcome.ALLOW)

    def test_audit_failure_returns_deny(self):
        self.audit = InMemoryAuditSink(succeed=False)
        self._deny(self._auth(), rc.AUDIT_UNAVAILABLE)

    def test_authorization_event_is_not_allow_source(self):
        rev = RevocationRecord(
            capability_id="cap-1",
            revoked_at=NOW,
            revoked_under_authority=AUTH_ID,
            state="REVOKED",
        )
        self.rev_store = InMemoryRevocationStore({"cap-1": rev})
        d = self._auth()
        self.assertEqual(d.outcome, DecisionOutcome.DENY)
        self.assertIsInstance(self.audit.events[0], AuthorizationEvent)
        self.assertEqual(self.audit.events[0].decision, DecisionOutcome.DENY)

    def test_i1_side_effect_contract_on_decision(self):
        allow = self._auth()
        self.assertEqual(allow.outcome, DecisionOutcome.ALLOW)
        self.assertTrue(allow.outcome == DecisionOutcome.ALLOW)
        rev = RevocationRecord(
            capability_id="cap-1",
            revoked_at=NOW,
            revoked_under_authority=AUTH_ID,
            state="REVOKED",
        )
        self.rev_store = InMemoryRevocationStore({"cap-1": rev})
        deny = self._auth()
        self.assertEqual(deny.outcome, DecisionOutcome.DENY)
        self.assertFalse(deny.outcome == DecisionOutcome.ALLOW)


if __name__ == "__main__":
    unittest.main()
