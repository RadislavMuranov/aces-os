import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.adapters.github import GitHubReadOnlyAdapter
from aces_os.connector.base import WriteNotAuthorizedError


class TestSecurityBoundaries(unittest.TestCase):
    def setUp(self):
        self.c = GitHubReadOnlyAdapter()

    def test_write_blocked(self):
        with self.assertRaises(WriteNotAuthorizedError):
            self.c.write()

    def test_create_blocked(self):
        with self.assertRaises(WriteNotAuthorizedError):
            self.c.create()

    def test_update_blocked(self):
        with self.assertRaises(WriteNotAuthorizedError):
            self.c.update()

    def test_delete_blocked(self):
        with self.assertRaises(WriteNotAuthorizedError):
            self.c.delete()

    def test_execute_blocked(self):
        with self.assertRaises(WriteNotAuthorizedError):
            self.c.execute()

    def test_authorize_blocked(self):
        with self.assertRaises(WriteNotAuthorizedError):
            self.c.authorize()

    def test_mint_evidence_blocked(self):
        with self.assertRaises(WriteNotAuthorizedError):
            self.c.mint_evidence()

    def test_mint_accepted_state_blocked(self):
        with self.assertRaises(WriteNotAuthorizedError):
            self.c.mint_accepted_state()


if __name__ == "__main__":
    unittest.main()
