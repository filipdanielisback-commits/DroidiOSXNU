"""Synthetic tests for the host-only platform dependency validator."""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_platform_dependencies import validate  # noqa: E402


class PlatformDependenciesValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads(
            (ROOT / "devices/moto-g60/platform-dependencies.json").read_text(encoding="utf-8")
        )

    def test_repository_inventory_is_valid(self):
        self.assertEqual(validate(self.profile), [])

    def test_inventory_contains_unique_dependency_ids(self):
        ids = [item["id"] for item in self.profile["dependencies"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(ids), 10)

    def test_evidence_and_unknowns_are_explicit(self):
        for item in self.profile["dependencies"]:
            self.assertTrue(item["evidence"])
            self.assertIn("unknowns", item)

    def test_duplicate_ids_are_rejected(self):
        data = copy.deepcopy(self.profile)
        data["dependencies"].append(copy.deepcopy(data["dependencies"][0]))
        self.assertTrue(any("duplicates" in error for error in validate(data)))

    def test_bootable_scope_is_rejected(self):
        data = copy.deepcopy(self.profile)
        data["scope"]["bootable"] = True
        self.assertTrue(any("scope.bootable" in error for error in validate(data)))

    def test_hardware_access_scope_is_rejected(self):
        data = copy.deepcopy(self.profile)
        data["scope"]["hardware_accessed"] = True
        self.assertTrue(any("scope.hardware_accessed" in error for error in validate(data)))

    def test_invalid_status_is_rejected(self):
        data = copy.deepcopy(self.profile)
        data["dependencies"][0]["status"] = "working"
        self.assertTrue(any("status is invalid" in error for error in validate(data)))

    def test_cli_json_report(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools/validate_platform_dependencies.py"), "--json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(json.loads(result.stdout)["valid"])


if __name__ == "__main__":
    unittest.main()
