#!/usr/bin/env python3
"""Host-only DroidiOSXNU boot-flow simulator.

This program models named development stages. It does not load or execute a
kernel, inspect hardware, access a bootloader, read/write device storage, or
produce a boot image.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

STAGES = (
    ("environment", "Host environment checks (simulated)"),
    ("configuration", "Platform configuration review (simulated)"),
    ("kernel_plan", "Kernel integration readiness (simulated)"),
    ("platform_plan", "Platform and driver readiness (simulated)"),
    ("handoff", "Handoff decision (simulated only)"),
)


def run_simulation(fail_at: str | None = None) -> dict[str, Any]:
    """Return a deterministic, explicitly simulated stage report."""
    results: list[dict[str, str]] = []
    blocked = False

    for stage_id, description in STAGES:
        if blocked:
            status = "SKIPPED"
        elif stage_id == fail_at:
            status = "BLOCKED"
            blocked = True
        else:
            status = "SIMULATED"

        results.append(
            {
                "stage": stage_id,
                "description": description,
                "status": status,
            }
        )

    return {
        "project": "DroidiOSXNU",
        "mode": "HOST_ONLY_SIMULATION",
        "result": "SIMULATION_STOPPED" if blocked else "SIMULATION_COMPLETE",
        "bootable": False,
        "hardware_accessed": False,
        "device_storage_modified": False,
        "executable_boot_code_generated": False,
        "stages": results,
        "notice": (
            "Illustrative software simulation only; not a real boot test, "
            "bootloader, kernel loader, or bootable image."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Run a host-only, non-operational simulation of DroidiOSXNU "
            "development stages."
        )
    )
    parser.add_argument(
        "--fail-at",
        choices=[stage_id for stage_id, _ in STAGES],
        help="Inject a simulated block at this stage to exercise reporting.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the report as JSON.",
    )
    parser.add_argument(
        "--list-stages",
        action="store_true",
        help="List the modeled stages without running the simulation.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.list_stages:
        for stage_id, description in STAGES:
            print(f"{stage_id}: {description}")
        return 0

    report = run_simulation(args.fail_at)

    if args.json:
        print(json.dumps(report, indent=2))
        return 0

    print("DroidiOSXNU — HOST-ONLY BOOT-FLOW SIMULATION")
    print("No device or bootloader is accessed. No image is generated.\n")
    for stage in report["stages"]:
        print(f"[{stage['status']}] {stage['stage']}: {stage['description']}")
    print(f"\nResult: {report['result']}")
    print(report["notice"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
