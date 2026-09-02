import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.connector.observation import ObservationState
from aces_os.adapters.slack import SlackReadOnlyAdapter
from aces_os.connector.resource import ResourceRef, ResourceScope


class TestNegativeSemantics(unittest.TestCase):
    def test_unknown_not_absent(self):
        self.assertNotEqual(ObservationState.UNKNOWN, ObservationState.ABSENT)

    def test_not_observable_not_absent(self):
        self.assertNotEqual(ObservationState.NOT_OBSERVABLE, ObservationState.ABSENT)

    def test_slack_missing_is_not_observable_not_deleted(self):
        sl = SlackReadOnlyAdapter()
        obs = sl.read_resource(
            ResourceRef("slack", "missing_kind", "x", ResourceScope("ns")), "r"
        )
        self.assertEqual(obs.observed_state, ObservationState.NOT_OBSERVABLE)
        self.assertNotEqual(obs.observed_state, ObservationState.ABSENT)


if __name__ == "__main__":
    unittest.main()
