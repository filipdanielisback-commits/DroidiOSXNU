"""Tests for the host-only platform profile validator."""

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "tools" / "validate_platform_profile.py"
PROFILE_PATH = ROOT / "devices" / "moto-g60" / "platform-profile.json"


class PlatformProfileValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *map(str, args)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_repository_profile_is_valid(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PLATFORM PROFILE: VALID", result.stdout)

    def test_json_report_declares_host_only_scope(self):
        result = self.run_cli("--json")
        report = json.loads(result.stdout)
        self.assertTrue(report["valid"])
        self.assertEqual(report["mode"], "HOST_ONLY_STATIC_VALIDATION")
        self.assertFalse(report["hardware_accessed"])
        self.assertFalse(report["device_storage_modified"])
        self.assertFalse(report["bootable"])

    def test_missing_device_field_is_rejected(self):
        profile = copy.deepcopy(self.profile)
        del profile["device"]["model"]
        self.assertTrue(
            any("device.model is required" in error
                for error in validate_for_test(profile))
        )

    def test_unknown_hardware_details_must_remain_unresolved(self):
        profile = copy.deepcopy(self.profile)
        profile["unresolved"].remove("physical_board_id")
        errors = validate_for_test(profile)
        self.assertTrue(any("physical_board_id" in error for error in errors))

    def test_bootable_scope_is_rejected(self):
        profile = copy.deepcopy(self.profile)
        profile["scope"]["bootable"] = True
        errors = validate_for_test(profile)
        self.assertTrue(any("scope.bootable must be false" in error for error in errors))

    def test_invalid_json_file_returns_nonzero(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{not json", encoding="utf-8")
            result = self.run_cli(path)
        self.assertEqual(result.returncode, 1)
        self.assertIn("could not read valid JSON", result.stdout)


def validate_for_test(profile):
    # Import by file path so the tests do not depend on tools/ being a package.
    import importlib.util

    spec = importlib.util.spec_from_file_location("platform_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_profile(profile)


if __name__ == "__main__":
    unittest.main()
