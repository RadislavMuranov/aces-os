"""Phase VI Knowledge promotion + Request boundary adversarial suite."""

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
)
from aces_os.knowledge import (
    KnowledgePromotionService,
    KnowledgeObjectType,
    TruthLevel,
    KnowledgeError,
    KnowledgeConflictError,
    KnowledgeUpdateRequest,
)


def bootstrap():
    reg = TrustedVerifierRegistry()
    reg.register_policy(VerificationPolicy("structural_v1", "1.0.0", True))
    reg.register_verifier(
        VerifierDescriptor(
            StructuralEvidenceVerifier.VERIFIER_ID,
            StructuralEvidenceVerifier.VERIFIER_VERSION,
            StructuralEvidenceVerifier.METHOD,
            "TRUSTED",
            ("structural_v1",),
        )
    )
    reg.lock()
    return reg


def pipeline():
    gh = GitHubReadOnlyAdapter()
    obs = gh.read_resource(
        ResourceRef(
            "github", "commit", "abc123def4567890abc123def4567890abc123de", ResourceScope("n")
        ),
        "req-k",
    )
    dwom = DWOMIngestor().ingest(obs)
    adm = EvidenceAdmissionService()
    evidence = adm.admit(adm.create_candidate(obs, dwom))
    vs = VerificationService(bootstrap())
    vreq = vs.build_request(evidence, "structural_v1", "1.0.0", "k-pipe")
    result, accepted = vs.verify(
        evidence,
        vreq,
        StructuralEvidenceVerifier.VERIFIER_ID,
        StructuralEvidenceVerifier.VERIFIER_VERSION,
    )
    return evidence, result, accepted


class TestKnowledgePromotion(unittest.TestCase):
    def setUp(self):
        self.evidence, self.result, self.accepted = pipeline()
        self.ks = KnowledgePromotionService()

    def _req(self, rid="r1", **kw):
        defaults = dict(
            request_id=rid,
            accepted_state_id=self.accepted.accepted_state_id,
            evidence_id=self.evidence.evidence_id,
            evidence_digest=self.evidence.payload_digest,
            knowledge_object_id="",
            object_type=KnowledgeObjectType.FACT,
            truth_level=TruthLevel.WORKING,
            semantic_payload={"claim": "commit observed"},
            semantic_identity="commit-fact-1",
        )
        defaults.update(kw)
        return KnowledgeUpdateRequest(**defaults)

    def test_A_valid_request(self):
        ko = self.ks.promote(self._req("A"), self.accepted, self.result, self.evidence)
        self.assertEqual(ko.status.value, "ACTIVE")
        self.assertEqual(ko.originating_request_id, "A")
        self.assertFalse(ko.is_memory())

    def test_B_missing_request(self):
        with self.assertRaises(KnowledgeError):
            self.ks.promote(None, self.accepted, self.result, self.evidence)

    def test_C_request_accepted_state_mismatch(self):
        with self.assertRaises(KnowledgeError):
            self.ks.promote(
                self._req("C", accepted_state_id="wrong-as"),
                self.accepted,
                self.result,
                self.evidence,
            )

    def test_D_request_evidence_id_mismatch(self):
        with self.assertRaises(KnowledgeError):
            self.ks.promote(
                self._req("D", evidence_id="wrong-ev"),
                self.accepted,
                self.result,
                self.evidence,
            )

    def test_E_request_digest_mismatch(self):
        with self.assertRaises(KnowledgeError):
            self.ks.promote(
                self._req("E", evidence_digest="00" * 32),
                self.accepted,
                self.result,
                self.evidence,
            )

    def test_G_same_request_id_idempotent(self):
        a = self.ks.promote(self._req("G"), self.accepted, self.result, self.evidence)
        b = self.ks.promote(self._req("G"), self.accepted, self.result, self.evidence)
        self.assertEqual(a.knowledge_object_id, b.knowledge_object_id)

    def test_H_different_request_same_identity(self):
        a = self.ks.promote(self._req("H1"), self.accepted, self.result, self.evidence)
        b = self.ks.promote(self._req("H2"), self.accepted, self.result, self.evidence)
        self.assertEqual(a.knowledge_object_id, b.knowledge_object_id)

    def test_I_payload_conflict(self):
        self.ks.promote(self._req("I1"), self.accepted, self.result, self.evidence)
        with self.assertRaises(KnowledgeConflictError):
            self.ks.promote(
                self._req("I2", semantic_payload={"claim": "other"}),
                self.accepted,
                self.result,
                self.evidence,
            )

    def test_J_truth_level_conflict(self):
        self.ks.promote(self._req("J1"), self.accepted, self.result, self.evidence)
        with self.assertRaises(KnowledgeConflictError):
            self.ks.promote(
                self._req("J2", truth_level=TruthLevel.OPERATIONAL),
                self.accepted,
                self.result,
                self.evidence,
            )

    def test_K_different_identity(self):
        a = self.ks.promote(
            self._req("K1", semantic_identity="id-a"),
            self.accepted,
            self.result,
            self.evidence,
        )
        b = self.ks.promote(
            self._req("K2", semantic_identity="id-b"),
            self.accepted,
            self.result,
            self.evidence,
        )
        self.assertNotEqual(a.knowledge_object_id, b.knowledge_object_id)

    def test_M_failed_cannot(self):
        failed = replace(self.result, status=VerificationStatus.FAILED)
        with self.assertRaises(KnowledgeError):
            self.ks.promote(self._req("M"), self.accepted, failed, self.evidence)

    def test_N_rejected_cannot(self):
        rej = replace(self.result, status=VerificationStatus.REJECTED)
        with self.assertRaises(KnowledgeError):
            self.ks.promote(self._req("N"), self.accepted, rej, self.evidence)

    def test_O_inconclusive_cannot(self):
        inc = replace(self.result, status=VerificationStatus.INCONCLUSIVE)
        with self.assertRaises(KnowledgeError):
            self.ks.promote(self._req("O"), self.accepted, inc, self.evidence)

    def test_P_bare_boolean(self):
        with self.assertRaises(KnowledgeError):
            self.ks.promote_from_boolean(verified=True)

    def test_Q_fabricated_accepted(self):
        with self.assertRaises(KnowledgeError):
            self.ks.promote(
                self._req("Q"),
                replace(self.accepted, evidence_id="fake"),
                self.result,
                self.evidence,
            )

    def test_S_result_mismatch(self):
        with self.assertRaises(KnowledgeError):
            self.ks.promote(
                self._req("S"),
                replace(self.accepted, verification_result_id="other"),
                self.result,
                self.evidence,
            )

    def test_T_to_AD_non_capabilities(self):
        for m in (
            "promote_without_request",
            "create_accepted_state",
            "perform_verification",
            "mutate_memory",
            "mutate_world_model",
            "mutate_semantic_reality",
            "authorize_execution",
            "issue_capability",
            "bypass_asa",
            "write_provider",
            "invoke_mcp",
            "promote_canonical",
        ):
            with self.assertRaises(KnowledgeError):
                getattr(self.ks, m)()

    def test_AC_canonical_rejected(self):
        with self.assertRaises(KnowledgeError):
            self.ks.promote(
                self._req("AC", truth_level=TruthLevel.CANONICAL),
                self.accepted,
                self.result,
                self.evidence,
            )

    def test_request_id_conflict_reuse(self):
        self.ks.promote(self._req("dup"), self.accepted, self.result, self.evidence)
        with self.assertRaises(KnowledgeConflictError):
            self.ks.promote(
                self._req("dup", semantic_identity="other-sem"),
                self.accepted,
                self.result,
                self.evidence,
            )

    def test_provenance(self):
        ko = self.ks.promote(self._req("prov"), self.accepted, self.result, self.evidence)
        p = ko.provenance
        self.assertEqual(p.accepted_state_id, self.accepted.accepted_state_id)
        self.assertEqual(p.verification_result_id, self.result.verification_result_id)
        self.assertEqual(p.evidence_digest, self.evidence.payload_digest)
        self.assertEqual(p.authenticity_crypto, "DEFERRED")


if __name__ == "__main__":
    unittest.main()
