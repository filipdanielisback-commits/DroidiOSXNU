"""Tests for the host-only XNU source pin verifier."""

import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "verify_xnu_pin.py"
MANIFEST_PATH = ROOT / "kernel" / "xnu-source-pin.json"

spec = importlib.util.spec_from_file_location("verify_xnu_pin", SCRIPT)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return self.payload


class XnuPinVerifierTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = verifier.load_manifest(MANIFEST_PATH)

    def test_repository_manifest_is_valid(self):
        self.assertEqual(verifier.validate_manifest(self.manifest), [])

    def test_scope_flags_must_remain_false(self):
        manifest = json.loads(json.dumps(self.manifest))
        manifest["handling"]["device_access"] = True
        self.assertTrue(any("device_access must be false" in e for e in verifier.validate_manifest(manifest)))

    def test_offline_mode_does_not_fetch_network(self):
        with patch.object(verifier.urllib.request, "urlopen", side_effect=AssertionError("network used")):
            report = verifier.main(["--offline", "--json"])
        self.assertEqual(report, 0)

    def test_upstream_tag_and_commit_are_verified(self):
        ref = {"object": {"type": "tag", "sha": self.manifest["upstream"]["tag_object_sha"]}}
        tag = {"object": {"type": "commit", "sha": self.manifest["upstream"]["commit_sha"]}}
        with patch.object(verifier, "fetch_json", side_effect=[ref, tag]):
            report = verifier.verify_upstream(self.manifest)
        self.assertTrue(report["valid"])
        self.assertFalse(report["source_downloaded"])

    def test_moved_tag_object_is_rejected(self):
        ref = {"object": {"type": "tag", "sha": "0" * 40}}
        with patch.object(verifier, "fetch_json", return_value=ref):
            with self.assertRaisesRegex(ValueError, "tag object mismatch"):
                verifier.verify_upstream(self.manifest)

    def test_changed_peeled_commit_is_rejected(self):
        ref = {"object": {"type": "tag", "sha": self.manifest["upstream"]["tag_object_sha"]}}
        tag = {"object": {"type": "commit", "sha": "0" * 40}}
        with patch.object(verifier, "fetch_json", side_effect=[ref, tag]):
            with self.assertRaisesRegex(ValueError, "peeled commit mismatch"):
                verifier.verify_upstream(self.manifest)


if __name__ == "__main__":
    unittest.main()
