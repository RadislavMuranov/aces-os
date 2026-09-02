import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.connector.observation import (
    Observation,
    ObservationState,
    PartialState,
    Provenance,
)
from aces_os.connector.resource import ResourceRef, ResourceScope


class TestObservation(unittest.TestCase):
    def _obs(self, **kw):
        ref = ResourceRef("github", "commit", "abc", ResourceScope("ns"))
        prov = Provenance(
            provider="github",
            connector_id="c",
            resource_ref_id="abc",
            observed_at="t",
            request_id="r1",
            configuration_scope="s",
        )
        defaults = dict(
            observation_id="o1",
            provider="github",
            resource_ref=ref,
            observed_at="t",
            observed_state=ObservationState.KNOWN,
            partial_state=PartialState.COMPLETE,
            provenance=prov,
            request_id="r1",
            payload_digest="d",
        )
        defaults.update(kw)
        return Observation(**defaults)

    def test_observation_not_evidence(self):
        self.assertFalse(self._obs().is_evidence())

    def test_observation_not_accepted_state(self):
        self.assertFalse(self._obs().is_accepted_state())

    def test_crypto_deferred(self):
        self.assertEqual(self._obs().provenance.authenticity_crypto, "DEFERRED")

    def test_partial_states_distinct(self):
        self.assertNotEqual(ObservationState.UNKNOWN, ObservationState.ABSENT)
        self.assertNotEqual(ObservationState.NOT_OBSERVABLE, ObservationState.ABSENT)


if __name__ == "__main__":
    unittest.main()
