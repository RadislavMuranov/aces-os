import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.adapters import (
    GitHubReadOnlyAdapter,
    GmailReadOnlyAdapter,
    GoogleDriveReadOnlyAdapter,
    SlackReadOnlyAdapter,
    KaitenReadOnlyAdapter,
    ObsidianReadOnlyAdapter,
)
from aces_os.connector.resource import ResourceRef, ResourceScope
from aces_os.connector.observation import ObservationState


class TestAdapters(unittest.TestCase):
    def test_github_branch_not_commit(self):
        gh = GitHubReadOnlyAdapter()
        branch = gh.read_resource(
            ResourceRef("github", "branch", "main", ResourceScope("ns")), "req-b"
        )
        commit = gh.read_resource(
            ResourceRef("github", "commit", "abc123def4567890abc123def4567890abc123de", ResourceScope("ns")),
            "req-c",
        )
        self.assertEqual(branch.observed_payload.get("kind"), "branch")
        self.assertEqual(commit.observed_payload.get("kind"), "commit")
        self.assertNotEqual(branch.resource_ref.resource_kind, commit.resource_ref.resource_kind)

    def test_gmail_ids_distinct(self):
        gm = GmailReadOnlyAdapter()
        obs = gm.read_resource(ResourceRef("gmail", "message", "msg_001", ResourceScope("ns")), "r")
        p = obs.observed_payload
        self.assertNotEqual(p["id"], p["threadId"])
        self.assertNotEqual(p["id"], p["rfcMessageId"])

    def test_drive_fileid_not_path(self):
        dr = GoogleDriveReadOnlyAdapter()
        obs = dr.read_resource(ResourceRef("google_drive", "file", "file_abc", ResourceScope("ns")), "r")
        self.assertNotEqual(obs.observed_payload["fileId"], obs.observed_payload["path"])

    def test_slack_message_identity(self):
        sl = SlackReadOnlyAdapter()
        obs = sl.read_resource(
            ResourceRef("slack", "message", "C01:1690000000.000100", ResourceScope("ns")), "r"
        )
        self.assertIn(":", obs.observed_payload["identity"])

    def test_kaiten_card(self):
        kt = KaitenReadOnlyAdapter()
        obs = kt.read_resource(ResourceRef("kaiten", "card", "42", ResourceScope("ns")), "r")
        self.assertEqual(obs.observed_payload["id"], 42)

    def test_obsidian_local(self):
        ob = ObsidianReadOnlyAdapter()
        obs = ob.read_resource(
            ResourceRef("obsidian", "note", "notes/fixture.md", ResourceScope("ns"), path="notes/fixture.md"),
            "r",
        )
        self.assertEqual(obs.observed_state, ObservationState.KNOWN)

    def test_all_providers_list(self):
        adapters = [
            GitHubReadOnlyAdapter(),
            GmailReadOnlyAdapter(),
            GoogleDriveReadOnlyAdapter(),
            SlackReadOnlyAdapter(),
            KaitenReadOnlyAdapter(),
            ObsidianReadOnlyAdapter(),
        ]
        self.assertEqual(len(adapters), 6)
        for a in adapters:
            self.assertTrue(a.identity.connector_id)


if __name__ == "__main__":
    unittest.main()
