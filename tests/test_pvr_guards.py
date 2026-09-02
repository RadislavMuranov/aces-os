import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.adapters.drive import GoogleDriveReadOnlyAdapter
from aces_os.adapters.slack import SlackReadOnlyAdapter
from aces_os.adapters.kaiten import KaitenReadOnlyAdapter
from aces_os.adapters.obsidian import ObsidianReadOnlyAdapter
from aces_os.connector.resource import ResourceRef, ResourceScope
from aces_os.connector.observation import ObservationState, PartialState


class TestPVRGuards(unittest.TestCase):
    def test_obs_sync_pvr(self):
        ob = ObsidianReadOnlyAdapter()
        obs = ob.read_resource(
            ResourceRef("obsidian", "sync_state", "x", ResourceScope("sync")), "r"
        )
        self.assertIn("OBS-SYNC", obs.pvr_flags)
        self.assertEqual(obs.observed_state, ObservationState.PARTIAL)

    def test_sl_ret_pvr(self):
        sl = SlackReadOnlyAdapter()
        obs = sl.read_resource(
            ResourceRef("slack", "history_complete", "all", ResourceScope("ns")), "r"
        )
        self.assertIn("SL-RET", obs.pvr_flags)

    def test_gd_sd_pvr(self):
        dr = GoogleDriveReadOnlyAdapter()
        obs = dr.read_resource(
            ResourceRef("google_drive", "file", "x", ResourceScope("shared_drive")), "r"
        )
        self.assertIn("GD-SD", obs.pvr_flags)

    def test_kt_wh_pvr(self):
        kt = KaitenReadOnlyAdapter()
        obs = kt.read_resource(
            ResourceRef("kaiten", "webhook_event", "e1", ResourceScope("ns")), "r"
        )
        self.assertIn("KT-WH", obs.pvr_flags)
        self.assertEqual(obs.partial_state, PartialState.PARTIAL)


if __name__ == "__main__":
    unittest.main()
