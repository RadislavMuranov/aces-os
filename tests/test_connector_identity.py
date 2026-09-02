import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from aces_os.connector.identity import ConnectorIdentity
from aces_os.connector.capability import Capability, FORBIDDEN_CAPABILITIES, READ_ONLY_CAPABILITIES
from aces_os.connector.resource import ResourceRef, ResourceScope


class TestConnectorIdentity(unittest.TestCase):
    def test_identity_required_fields(self):
        ident = ConnectorIdentity(
            connector_id="c1", provider="github", connector_version="0.1.0", configuration_scope="s"
        )
        self.assertEqual(ident.provider, "github")

    def test_identity_rejects_empty(self):
        with self.assertRaises(ValueError):
            ConnectorIdentity("", "github", "0.1.0", "s")

    def test_read_only_capabilities(self):
        self.assertIn(Capability.READ_RESOURCE.value, READ_ONLY_CAPABILITIES)
        self.assertIn("CREATE", FORBIDDEN_CAPABILITIES)
        self.assertIn("DELETE", FORBIDDEN_CAPABILITIES)

    def test_resource_ref_distinct_fields(self):
        ref = ResourceRef(
            provider="google_drive",
            resource_kind="file",
            resource_id="file_abc",
            scope=ResourceScope("ns"),
            path="/My Drive/doc.txt",
            display_name="doc.txt",
        )
        self.assertNotEqual(ref.resource_id, ref.path)


if __name__ == "__main__":
    unittest.main()
