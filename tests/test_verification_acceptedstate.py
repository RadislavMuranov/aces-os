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
    AcceptedStateStatus,
    VerificationError,
    StructuralEvidenceVerifier,
    RegistryError,
)


def bootstrap_registry() -> TrustedVerifierRegistry:
    reg = TrustedVerifierRegistry()
    reg.register_policy(
        VerificationPolicy(
            policy_id="structural_v1",
            policy_version="1.0.0",
            active=True,
            description="structural evidence integrity",
        )
    )
    reg.register_verifier(
        VerifierDescriptor(
            verifier_id=StructuralEvidenceVerifier.VERIFIER_ID,
            verifier_version=StructuralEvidenceVerifier.VERIFIER_VERSION,
            verification_method=StructuralEvidenceVerifier.METHOD,
            trust_status="TRUSTED",
            policy_scope=("structural_v1",),
        )
    )
    reg.lock()
    return reg


def admitted_evidence():
    gh = GitHubReadOnlyAdapter()
    obs = gh.read_resource(
        ResourceRef("github", "commit", "abc123def4567890abc123def4567890abc123de", ResourceScope("n")),
        "req-v1",
    )
    dwom = DWOMIngestor().ingest(obs)
    svc = EvidenceAdmissionService()
    cand = svc.create_candidate(obs, dwom)
    return svc.admit(cand)


class TestVerificationAcceptedState(unittest.TestCase):
    def setUp(self):
        self.reg = bootstrap_registry()
        self.vs = VerificationService(self.reg)
        self.evidence = admitted_evidence()

    def test_passed_establishes_accepted(self):
        req = self.vs.build_request(self.evidence, "structural_v1", "1.0.0", "k1")
        result, accepted = self.vs.verify(
            self.evidence,
            req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        self.assertEqual(result.status, VerificationStatus.PASSED)
        self.assertIsNotNone(accepted)
        self.assertEqual(accepted.status, AcceptedStateStatus.ESTABLISHED)
        self.assertEqual(accepted.verifier_version, StructuralEvidenceVerifier.VERIFIER_VERSION)
        self.assertFalse(accepted.is_knowledge())
        self.assertFalse(accepted.is_truth())
        self.assertFalse(accepted.is_authorization())

    def test_idempotent(self):
        req = self.vs.build_request(self.evidence, "structural_v1", "1.0.0", "k2")
        r1, a1 = self.vs.verify(
            self.evidence, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        r2, a2 = self.vs.verify(
            self.evidence, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        self.assertEqual(r1.verification_result_id, r2.verification_result_id)
        self.assertEqual(a1.accepted_state_id, a2.accepted_state_id)

    def test_unknown_verifier_rejected(self):
        req = self.vs.build_request(self.evidence, "structural_v1", "1.0.0", "k3")
        result, accepted = self.vs.verify(self.evidence, req, "fake.verifier", "9.9.9")
        self.assertEqual(result.status, VerificationStatus.REJECTED)
        self.assertIsNone(accepted)

    def test_untrusted_verifier(self):
        reg = TrustedVerifierRegistry()
        reg.register_policy(VerificationPolicy("structural_v1", "1.0.0", True))
        reg.register_verifier(
            VerifierDescriptor("evil", "1", "x", "UNTRUSTED", ("structural_v1",))
        )
        reg.lock()
        vs = VerificationService(reg)
        req = vs.build_request(self.evidence, "structural_v1", "1.0.0", "k4")
        result, accepted = vs.verify(self.evidence, req, "evil", "1")
        self.assertEqual(result.status, VerificationStatus.REJECTED)
        self.assertIsNone(accepted)

    def test_inactive_policy(self):
        reg = TrustedVerifierRegistry()
        reg.register_policy(VerificationPolicy("structural_v1", "1.0.0", active=False))
        reg.register_verifier(
            VerifierDescriptor(
                StructuralEvidenceVerifier.VERIFIER_ID,
                StructuralEvidenceVerifier.VERIFIER_VERSION,
                "m", "TRUSTED", ("structural_v1",),
            )
        )
        reg.lock()
        vs = VerificationService(reg)
        req = vs.build_request(self.evidence, "structural_v1", "1.0.0", "k5")
        result, accepted = vs.verify(
            self.evidence, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        self.assertEqual(result.status, VerificationStatus.REJECTED)
        self.assertIsNone(accepted)

    def test_digest_mismatch(self):
        req = self.vs.build_request(self.evidence, "structural_v1", "1.0.0", "k6")
        bad_req = replace(req, payload_digest="00" * 32)
        with self.assertRaises(VerificationError):
            self.vs.verify(
                self.evidence, bad_req,
                StructuralEvidenceVerifier.VERIFIER_ID,
                StructuralEvidenceVerifier.VERIFIER_VERSION,
            )

    def test_registry_locked(self):
        with self.assertRaises(RegistryError):
            self.reg.register_verifier(
                VerifierDescriptor("x", "1", "m", "TRUSTED", ("structural_v1",))
            )

    def test_authority_denied(self):
        for m in (
            "establish_passed",
            "create_accepted_state_direct",
            "issue_authorization",
            "issue_capability",
            "bypass_asa",
            "promote_knowledge",
            "mutate_memory",
            "mutate_world_model",
            "mutate_semantic_reality",
            "write_provider",
            "resolve_reconciliation",
        ):
            with self.assertRaises(VerificationError):
                getattr(self.vs, m)()

    def test_digest_binding_on_result(self):
        req = self.vs.build_request(self.evidence, "structural_v1", "1.0.0", "k7")
        result, accepted = self.vs.verify(
            self.evidence, req,
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
        )
        self.assertEqual(result.evidence_digest, self.evidence.payload_digest)
        self.assertEqual(accepted.evidence_digest, self.evidence.payload_digest)


if __name__ == "__main__":
    unittest.main()
