"""Tests for the host-only exact XNU source fetcher."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "fetch_xnu_source.py"

spec = importlib.util.spec_from_file_location("fetch_xnu_source", SCRIPT)
fetcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetcher)


class XnuSourceFetcherTests(unittest.TestCase):
    def test_repository_manifest_is_valid(self):
        manifest = fetcher.load_manifest()
        self.assertEqual(fetcher.validate_manifest(manifest), [])
        self.assertEqual(manifest["upstream"]["tag"], "xnu-12377.121.6")

    def test_source_must_remain_non_vendored_and_host_only(self):
        manifest = fetcher.load_manifest()
        manifest["handling"]["source_vendored"] = True
        self.assertTrue(
            any("source_vendored must be false" in error for error in fetcher.validate_manifest(manifest))
        )

    def test_destination_must_be_inside_kernel_upstream(self):
        with self.assertRaisesRegex(ValueError, "must be inside"):
            fetcher.validate_destination(ROOT / "docs" / "xnu")

    def test_default_destination_is_inside_kernel_upstream(self):
        destination = fetcher.validate_destination(fetcher.DEFAULT_DESTINATION)
        self.assertTrue(destination.is_relative_to((ROOT / "kernel" / "upstream").resolve()))


if __name__ == "__main__":
    unittest.main()
