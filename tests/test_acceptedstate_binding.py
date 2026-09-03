"""Adversarial AcceptedState binding / anti-aliasing tests."""

import unittest
import sys
from pathlib import Path
from dataclasses import replace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.adapters.github import GitHubReadOnlyAdapter
from aces_os.connector.resource import ResourceRef, ResourceScope
from aces_os.dwom import DWOMIngestor
from aces_os.evidence import EvidenceAdmissionService
from aces_os.verification import (
    TrustedVerifierRegistry,
    VerificationPolicy,
    VerifierDescriptor,
    VerificationService,
    VerificationStatus,
    StructuralEvidenceVerifier,
    accepted_identity_key,
)


def make_evidence():
    gh = GitHubReadOnlyAdapter()
    obs = gh.read_resource(
        ResourceRef(
            "github",
            "commit",
            "abc123def4567890abc123def4567890abc123de",
            ResourceScope("n"),
        ),
        "req-bind",
    )
    dwom = DWOMIngestor().ingest(obs)
    adm = EvidenceAdmissionService()
    return adm.admit(adm.create_candidate(obs, dwom))


def reg_with_two_policies():
    reg = TrustedVerifierRegistry()
    reg.register_policy(VerificationPolicy("structural_v1", "1.0.0", True))
    reg.register_policy(VerificationPolicy("structural_v1b", "1.0.0", True))
    reg.register_verifier(
        VerifierDescriptor(
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
            StructuralEvidenceVerifier.METHOD,
            "TRUSTED",
            ("structural_v1", "structural_v1b"),
        )
    )
    reg.lock()
    return reg


class TestAcceptedStateBinding(unittest.TestCase):
    def test_A_same_identity_idempotent(self):
        ev = make_evidence()
        vs = VerificationService(reg_with_two_policies())
        req = vs.build_request(ev, "structural_v1", "1.0.0", "a1")
        r1, a1 = vs.verify(
            ev, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        r2, a2 = vs.verify(
            ev, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        self.assertEqual(r1.status, VerificationStatus.PASSED)
        self.assertEqual(r1.verification_result_id, r2.verification_result_id)
        self.assertIsNotNone(a1)
        self.assertEqual(a1.accepted_state_id, a2.accepted_state_id)
        self.assertEqual(a1.verification_result_id, r1.verification_result_id)

    def test_B_different_policy_no_alias(self):
        ev = make_evidence()
        vs = VerificationService(reg_with_two_policies())
        req_a = vs.build_request(ev, "structural_v1", "1.0.0", "b1")
        req_b = vs.build_request(ev, "structural_v1b", "1.0.0", "b2")
        r1, a1 = vs.verify(
            ev, req_a,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        r2, a2 = vs.verify(
            ev, req_b,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        self.assertEqual(r1.status, VerificationStatus.PASSED)
        self.assertEqual(r2.status, VerificationStatus.PASSED)
        self.assertIsNotNone(a1)
        self.assertIsNotNone(a2)
        self.assertNotEqual(a1.accepted_state_id, a2.accepted_state_id)
        self.assertEqual(a1.policy_id, "structural_v1")
        self.assertEqual(a2.policy_id, "structural_v1b")
        self.assertNotEqual(a1.verification_result_id, a2.verification_result_id)

    def test_C_different_verifier_no_alias(self):
        # Second verifier trusted for policy but no bound implementation → REJECTED
        # (no AcceptedState); proves no alias from first PASSED state
        reg = TrustedVerifierRegistry()
        reg.register_policy(VerificationPolicy("structural_v1", "1.0.0", True))
        reg.register_verifier(
            VerifierDescriptor(
                StructuralEvidenceVerifier.VERIFIER_ID,
                StructuralEvidenceVerifier.VERIFIER_VERSION,
                "m", "TRUSTED", ("structural_v1",),
            )
        )
        reg.register_verifier(
            VerifierDescriptor("aces.verifier.other", "1.0.0", "m2", "TRUSTED", ("structural_v1",))
        )
        reg.lock()
        ev = make_evidence()
        vs = VerificationService(reg)
        req = vs.build_request(ev, "structural_v1", "1.0.0", "c1")
        r1, a1 = vs.verify(
            ev, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        r2, a2 = vs.verify(ev, req, "aces.verifier.other", "1.0.0")
        self.assertEqual(r1.status, VerificationStatus.PASSED)
        self.assertIsNotNone(a1)
        self.assertEqual(r2.status, VerificationStatus.REJECTED)
        self.assertIsNone(a2)

    def test_D_different_verifier_version_identity(self):
        key1 = accepted_identity_key("e", "d", "p", "1", "v", "1.0.0")
        key2 = accepted_identity_key("e", "d", "p", "1", "v", "2.0.0")
        self.assertNotEqual(key1, key2)

    def test_E_result_state_binding(self):
        ev = make_evidence()
        vs = VerificationService(reg_with_two_policies())
        req = vs.build_request(ev, "structural_v1", "1.0.0", "e1")
        r, a = vs.verify(
            ev, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        self.assertEqual(a.verification_result_id, r.verification_result_id)
        self.assertEqual(a.verifier_id, r.verifier_id)
        self.assertEqual(a.verifier_version, r.verifier_version)
        self.assertEqual(a.policy_id, r.policy_id)
        self.assertEqual(a.evidence_digest, r.evidence_digest)

    def test_F_digest_change_no_reuse(self):
        ev = make_evidence()
        vs = VerificationService(reg_with_two_policies())
        req = vs.build_request(ev, "structural_v1", "1.0.0", "f1")
        r1, a1 = vs.verify(
            ev, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        bad_req = replace(req, payload_digest="00" * 32)
        with self.assertRaises(Exception):
            vs.verify(
                ev, bad_req,
                StructuralEvidenceVerifier.VERIFIER_ID,
                StructuralEvidenceVerifier.VERIFIER_VERSION,
            )
        # Original state still only under original identity
        lookup = vs.store.get_accepted_by_identity(
            ev.evidence_id,
            "00" * 32,
            "structural_v1",
            "1.0.0",
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        self.assertIsNone(lookup)
        self.assertIsNotNone(a1)

    def test_G_no_downgrade_from_rejected(self):
        reg = TrustedVerifierRegistry()
        reg.register_policy(VerificationPolicy("structural_v1", "1.0.0", True))
        reg.register_verifier(
            VerifierDescriptor("fake", "1.0.0", "m", "TRUSTED", ("structural_v1",))
        )
        reg.lock()
        ev = make_evidence()
        vs = VerificationService(reg)
        req = vs.build_request(ev, "structural_v1", "1.0.0", "g1")
        r, a = vs.verify(ev, req, "fake", "1.0.0")
        self.assertEqual(r.status, VerificationStatus.REJECTED)
        self.assertIsNone(a)


if __name__ == "__main__":
    unittest.main()
