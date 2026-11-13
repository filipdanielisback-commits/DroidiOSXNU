"""Tests for the host-only boot-flow simulator."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIMULATOR = ROOT / "tools" / "boot_flow_simulator.py"


class BootFlowSimulatorTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SIMULATOR), *args],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_default_run_is_explicitly_non_bootable(self):
        report = json.loads(self.run_cli("--json").stdout)
        self.assertEqual(report["mode"], "HOST_ONLY_SIMULATION")
        self.assertEqual(report["result"], "SIMULATION_COMPLETE")
        self.assertFalse(report["bootable"])
        self.assertFalse(report["hardware_accessed"])
        self.assertFalse(report["device_storage_modified"])
        self.assertFalse(report["executable_boot_code_generated"])
        self.assertTrue(report["stages"])
        self.assertTrue(all(s["status"] == "SIMULATED" for s in report["stages"]))

    def test_injected_block_skips_later_stages(self):
        report = json.loads(
            self.run_cli("--json", "--fail-at", "kernel_plan").stdout
        )
        statuses = {stage["stage"]: stage["status"] for stage in report["stages"]}
        self.assertEqual(report["result"], "SIMULATION_STOPPED")
        self.assertEqual(statuses["environment"], "SIMULATED")
        self.assertEqual(statuses["kernel_plan"], "BLOCKED")
        self.assertEqual(statuses["platform_plan"], "SKIPPED")
        self.assertEqual(statuses["handoff"], "SKIPPED")

    def test_stage_listing_does_not_run_a_boot(self):
        output = self.run_cli("--list-stages").stdout
        self.assertIn("environment:", output)
        self.assertIn("handoff:", output)
        self.assertNotIn("SIMULATION_COMPLETE", output)


if __name__ == "__main__":
    unittest.main()
