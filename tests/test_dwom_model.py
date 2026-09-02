import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.connector.resource import ResourceRef, ResourceScope
from aces_os.connector.observation import ObservationState, PartialState
from aces_os.dwom.model import (
    DWOMObject,
    ExistenceState,
    DeletionState,
    DWOMStatus,
    DigitalWorldState,
)


def _obj(**kw):
    ref = ResourceRef("github", "commit", "abc", ResourceScope("ns"))
    base = dict(
        dwom_object_id="dwom:1",
        provider="github",
        resource_ref=ref,
        resource_kind="commit",
        scope_namespace="ns",
        observed_state=ObservationState.KNOWN,
        existence_state=ExistenceState.PRESENT,
        deletion_state=DeletionState.NOT_DELETED,
        partial_state=PartialState.COMPLETE,
        version_or_revision="abc",
        observed_at="t",
        source_timestamp=None,
        provider_event_time=None,
        observation_id="o1",
        request_id="r1",
        payload_digest="d",
        connector_id="c",
        configuration_scope="s",
        status=DWOMStatus.KNOWN,
    )
    base.update(kw)
    return DWOMObject(**base)


class TestDWOMModel(unittest.TestCase):
    def test_not_epistemic(self):
        o = _obj()
        self.assertFalse(o.is_evidence())
        self.assertFalse(o.is_accepted_state())
        self.assertFalse(o.is_knowledge())
        self.assertFalse(o.is_semantic_reality())

    def test_crypto_deferred(self):
        self.assertEqual(_obj().authenticity_crypto, "DEFERRED")

    def test_state_snapshot(self):
        s = DigitalWorldState()
        o = _obj()
        s.objects[o.dwom_object_id] = o
        self.assertIs(s.get(o.dwom_object_id), o)


if __name__ == "__main__":
    unittest.main()
