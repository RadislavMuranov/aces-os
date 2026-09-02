import unittest
import sys
from pathlib import Path
from dataclasses import replace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.adapters.github import GitHubReadOnlyAdapter
from aces_os.adapters.gmail import GmailReadOnlyAdapter
from aces_os.adapters.drive import GoogleDriveReadOnlyAdapter
from aces_os.adapters.slack import SlackReadOnlyAdapter
from aces_os.adapters.kaiten import KaitenReadOnlyAdapter
from aces_os.adapters.obsidian import ObsidianReadOnlyAdapter
from aces_os.connector.resource import ResourceRef, ResourceScope
from aces_os.connector.observation import ObservationState
from aces_os.dwom import DWOMIngestor
from aces_os.evidence import (
    EvidenceAdmissionService,
    AdmissionError,
    AdmissionConflictError,
    CandidateStatus,
    EvidenceStatus,
)


def pipeline(adapter, ref, request_id):
    obs = adapter.read_resource(ref, request_id)
    dwom = DWOMIngestor().ingest(obs)
    svc = EvidenceAdmissionService()
    cand = svc.create_candidate(obs, dwom)
    return obs, dwom, svc, cand


class TestEvidenceAdmission(unittest.TestCase):
    def test_github_admit(self):
        obs, dwom, svc, cand = pipeline(
            GitHubReadOnlyAdapter(),
            ResourceRef("github", "commit", "abc123def4567890abc123def4567890abc123de", ResourceScope("n")),
            "req-ev-1",
        )
        self.assertIn(cand.candidate_status, (CandidateStatus.ELIGIBLE, CandidateStatus.CANDIDATE))
        ev = svc.admit(cand)
        self.assertEqual(ev.status, EvidenceStatus.ADMITTED)
        self.assertEqual(ev.observation_id, obs.observation_id)
        self.assertEqual(ev.payload_digest, obs.payload_digest)
        self.assertFalse(ev.is_verification())
        self.assertFalse(ev.is_accepted_state())
        self.assertFalse(ev.is_knowledge())
        self.assertFalse(ev.is_truth())

    def test_idempotent_admit(self):
        _, _, svc, cand = pipeline(
            GitHubReadOnlyAdapter(),
            ResourceRef("github", "branch", "main", ResourceScope("n")),
            "req-idemp",
        )
        a = svc.admit(cand)
        b = svc.admit(cand)
        self.assertEqual(a.evidence_id, b.evidence_id)
        self.assertEqual(svc.store.evidence_count(), 1)

    def test_digest_conflict(self):
        obs, dwom, svc, cand = pipeline(
            GitHubReadOnlyAdapter(),
            ResourceRef("github", "repo", "12345", ResourceScope("n")),
            "req-c",
        )
        svc.admit(cand)
        bad = replace(cand, payload_digest="ff" * 32)
        with self.assertRaises(AdmissionConflictError):
            svc.admit(bad)

    def test_binding_mismatch(self):
        obs, dwom, svc, _ = pipeline(
            GmailReadOnlyAdapter(),
            ResourceRef("gmail", "message", "msg_001", ResourceScope("n")),
            "req-b",
        )
        bad_dwom = replace(dwom, provider="github")
        with self.assertRaises(AdmissionError):
            svc.create_candidate(obs, bad_dwom)

    def test_not_observable_ineligible(self):
        obs, dwom, svc, cand = pipeline(
            SlackReadOnlyAdapter(),
            ResourceRef("slack", "missing_kind", "x", ResourceScope("n")),
            "req-no",
        )
        self.assertEqual(obs.observed_state, ObservationState.NOT_OBSERVABLE)
        with self.assertRaises(AdmissionError):
            svc.admit(cand)

    def test_pvr_preserved(self):
        cases = [
            (ObsidianReadOnlyAdapter(), ResourceRef("obsidian", "sync_state", "x", ResourceScope("sync")), "OBS-SYNC"),
            (SlackReadOnlyAdapter(), ResourceRef("slack", "history_complete", "x", ResourceScope("n")), "SL-RET"),
            (GoogleDriveReadOnlyAdapter(), ResourceRef("google_drive", "file", "x", ResourceScope("shared_drive")), "GD-SD"),
            (KaitenReadOnlyAdapter(), ResourceRef("kaiten", "webhook_event", "x", ResourceScope("n")), "KT-WH"),
        ]
        for ad, ref, flag in cases:
            obs, dwom, svc, cand = pipeline(ad, ref, "req-pvr")
            self.assertIn(flag, cand.pvr_flags)
            # PARTIAL may still admit structurally with PVR flag retained
            if obs.observed_state == ObservationState.PARTIAL:
                ev = svc.admit(cand)
                self.assertIn(flag, ev.pvr_flags)
                self.assertEqual(ev.authenticity_crypto, "DEFERRED")

    def test_six_providers_candidate(self):
        pairs = [
            (GitHubReadOnlyAdapter(), ResourceRef("github", "commit", "abc123def4567890abc123def4567890abc123de", ResourceScope("n"))),
            (GmailReadOnlyAdapter(), ResourceRef("gmail", "message", "msg_001", ResourceScope("n"))),
            (GoogleDriveReadOnlyAdapter(), ResourceRef("google_drive", "file", "file_abc", ResourceScope("n"))),
            (SlackReadOnlyAdapter(), ResourceRef("slack", "message", "C01:1", ResourceScope("n"))),
            (KaitenReadOnlyAdapter(), ResourceRef("kaiten", "card", "42", ResourceScope("n"))),
            (ObsidianReadOnlyAdapter(), ResourceRef("obsidian", "note", "notes/fixture.md", ResourceScope("n"), path="notes/fixture.md")),
        ]
        for i, (ad, ref) in enumerate(pairs):
            obs, dwom, svc, cand = pipeline(ad, ref, f"req-6-{i}")
            self.assertEqual(cand.provider, ad.identity.provider)
            if obs.observed_state not in (ObservationState.NOT_OBSERVABLE, ObservationState.UNKNOWN):
                ev = svc.admit(cand)
                self.assertEqual(ev.provider, ad.identity.provider)

    def test_authority_denied(self):
        svc = EvidenceAdmissionService()
        for m in (
            "verify",
            "accept",
            "promote_to_knowledge",
            "authorize",
            "execute",
            "resolve_truth",
            "issue_authorization",
            "bypass_asa",
            "mutate_semantic_reality",
            "write_provider",
        ):
            with self.assertRaises(AdmissionError):
                getattr(svc, m)()

    def test_ids_distinct(self):
        obs, dwom, svc, cand = pipeline(
            GitHubReadOnlyAdapter(),
            ResourceRef("github", "commit", "abc123def4567890abc123def4567890abc123de", ResourceScope("n")),
            "req-ids",
        )
        ev = svc.admit(cand)
        ids = {obs.observation_id, cand.candidate_id, ev.evidence_id, obs.request_id}
        self.assertEqual(len(ids), 4)


if __name__ == "__main__":
    unittest.main()
