import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.connector.replay import ReplayBinding, ReplayRegistry, ReplayConflictError


class TestReplay(unittest.TestCase):
    def test_same_payload_same_digest(self):
        a = ReplayBinding.from_payload("r1", {"x": 1})
        b = ReplayBinding.from_payload("r1", {"x": 1})
        self.assertEqual(a.payload_digest, b.payload_digest)

    def test_different_payload_conflict(self):
        reg = ReplayRegistry()
        reg.register(ReplayBinding.from_payload("r1", {"x": 1}))
        with self.assertRaises(ReplayConflictError):
            reg.register(ReplayBinding.from_payload("r1", {"x": 2}))

    def test_request_id_alone_not_sufficient(self):
        a = ReplayBinding.from_payload("r1", {"a": 1})
        b = ReplayBinding.from_payload("r1", {"a": 2})
        self.assertEqual(a.request_id, b.request_id)
        self.assertNotEqual(a.payload_digest, b.payload_digest)


if __name__ == "__main__":
    unittest.main()
