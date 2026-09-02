import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.adapters.github import GitHubReadOnlyAdapter
from aces_os.adapters.gmail import GmailReadOnlyAdapter
from aces_os.adapters.drive import GoogleDriveReadOnlyAdapter
from aces_os.adapters.slack import SlackReadOnlyAdapter
from aces_os.adapters.kaiten import KaitenReadOnlyAdapter
from aces_os.adapters.obsidian import ObsidianReadOnlyAdapter
from aces_os.connector.resource import ResourceRef, ResourceScope
from aces_os.connector.observation import ObservationState, PartialState
from aces_os.connector.replay import ReplayBinding
from aces_os.dwom import DWOMIngestor, IngestConflictError, IngestError
from aces_os.dwom.model import ExistenceState, DeletionState, DWOMStatus


class TestDWOMIngest(unittest.TestCase):
    def setUp(self):
        self.ing = DWOMIngestor()

    def test_github_commit_ingest(self):
        gh = GitHubReadOnlyAdapter()
        obs = gh.read_resource(
            ResourceRef("github", "commit", "abc123def4567890abc123def4567890abc123de", ResourceScope("ns")),
            "req-gh-1",
        )
        obj = self.ing.ingest(obs)
        self.assertEqual(obj.provider, "github")
        self.assertEqual(obj.observation_id, obs.observation_id)
        self.assertEqual(obj.payload_digest, obs.payload_digest)
        self.assertEqual(obj.version_or_revision, obs.observed_payload.get("sha"))
        self.assertEqual(obj.existence_state, ExistenceState.PRESENT)
        self.assertFalse(obj.is_evidence())

    def test_idempotent(self):
        gh = GitHubReadOnlyAdapter()
        obs = gh.read_resource(
            ResourceRef("github", "branch", "main", ResourceScope("ns")), "req-idemp"
        )
        a = self.ing.ingest(obs)
        b = self.ing.ingest(obs)
        self.assertEqual(a.dwom_object_id, b.dwom_object_id)
        self.assertEqual(len(self.ing.store), 1)

    def test_digest_conflict(self):
        gh = GitHubReadOnlyAdapter()
        obs = gh.read_resource(
            ResourceRef("github", "repo", "12345", ResourceScope("ns")), "req-c"
        )
        self.ing.ingest(obs)
        # Force same observation_id different digest
        from dataclasses import replace

        bad = replace(obs, payload_digest="deadbeef" * 8)
        with self.assertRaises(IngestConflictError):
            self.ing.ingest(bad)

    def test_gmail_ids_preserved(self):
        gm = GmailReadOnlyAdapter()
        obs = gm.read_resource(ResourceRef("gmail", "message", "msg_001", ResourceScope("ns")), "r")
        obj = self.ing.ingest(obs)
        self.assertNotEqual(obj.payload["id"], obj.payload["threadId"])

    def test_drive_fileid_not_path(self):
        dr = GoogleDriveReadOnlyAdapter()
        obs = dr.read_resource(
            ResourceRef("google_drive", "file", "file_abc", ResourceScope("ns")), "r"
        )
        obj = self.ing.ingest(obs)
        self.assertNotEqual(obj.payload["fileId"], obj.payload["path"])

    def test_slack_not_observable(self):
        sl = SlackReadOnlyAdapter()
        obs = sl.read_resource(
            ResourceRef("slack", "missing_kind", "x", ResourceScope("ns")), "r"
        )
        obj = self.ing.ingest(obs)
        self.assertEqual(obj.observed_state, ObservationState.NOT_OBSERVABLE)
        self.assertEqual(obj.existence_state, ExistenceState.NOT_OBSERVABLE)
        self.assertNotEqual(obj.deletion_state, DeletionState.DELETED)

    def test_pvr_flags(self):
        for adapter, kind, scope_ns, flag in [
            (ObsidianReadOnlyAdapter(), "sync_state", "sync", "OBS-SYNC"),
            (SlackReadOnlyAdapter(), "history_complete", "ns", "SL-RET"),
            (GoogleDriveReadOnlyAdapter(), "file", "shared_drive", "GD-SD"),
            (KaitenReadOnlyAdapter(), "webhook_event", "ns", "KT-WH"),
        ]:
            ing = DWOMIngestor()
            provider = adapter.identity.provider
            obs = adapter.read_resource(
                ResourceRef(provider, kind, "x", ResourceScope(scope_ns)), "r-pvr"
            )
            obj = ing.ingest(obs)
            self.assertIn(flag, obj.pvr_flags)
            self.assertEqual(obj.status, DWOMStatus.PARTIAL)

    def test_all_six_providers(self):
        pairs = [
            (GitHubReadOnlyAdapter(), ResourceRef("github", "commit", "abc123def4567890abc123def4567890abc123de", ResourceScope("n"))),
            (GmailReadOnlyAdapter(), ResourceRef("gmail", "message", "msg_001", ResourceScope("n"))),
            (GoogleDriveReadOnlyAdapter(), ResourceRef("google_drive", "file", "file_abc", ResourceScope("n"))),
            (SlackReadOnlyAdapter(), ResourceRef("slack", "message", "C01:1", ResourceScope("n"))),
            (KaitenReadOnlyAdapter(), ResourceRef("kaiten", "card", "42", ResourceScope("n"))),
            (ObsidianReadOnlyAdapter(), ResourceRef("obsidian", "note", "notes/fixture.md", ResourceScope("n"), path="notes/fixture.md")),
        ]
        for i, (ad, ref) in enumerate(pairs):
            obs = ad.read_resource(ref, f"req-{i}")
            obj = self.ing.ingest(obs)
            self.assertEqual(obj.provider, ad.identity.provider)

    def test_validate_missing(self):
        from aces_os.connector.observation import Observation, Provenance
        from aces_os.connector.resource import ResourceRef, ResourceScope

        ref = ResourceRef("github", "commit", "x", ResourceScope("n"))
        with self.assertRaises(IngestError):
            self.ing.ingest(
                Observation(
                    observation_id="",
                    provider="github",
                    resource_ref=ref,
                    observed_at="t",
                    observed_state=ObservationState.KNOWN,
                    partial_state=PartialState.COMPLETE,
                    provenance=Provenance("github", "c", "x", "t", "r", "s"),
                    request_id="r",
                    payload_digest="d",
                )
            )

    def test_authority_denied(self):
        for m in (
            "create_evidence",
            "create_accepted_state",
            "mutate_knowledge",
            "mutate_memory",
            "mutate_world_model",
            "mutate_semantic_reality",
            "issue_authorization",
            "bypass_asa",
            "resolve_conflict",
        ):
            with self.assertRaises(IngestError):
                getattr(self.ing, m)()

    def test_absence_not_deleted(self):
        gh = GitHubReadOnlyAdapter()
        obs = gh.read_resource(
            ResourceRef("github", "unknown_kind", "z", ResourceScope("n")), "r-abs"
        )
        obj = self.ing.ingest(obs)
        self.assertEqual(obj.observed_state, ObservationState.ABSENT)
        self.assertEqual(obj.deletion_state, DeletionState.UNKNOWN)


if __name__ == "__main__":
    unittest.main()
