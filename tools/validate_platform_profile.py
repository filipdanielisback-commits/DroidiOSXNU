#!/usr/bin/env python3
"""Validate a static DroidiOSXNU platform research profile.

This tool reads a JSON file on the host. It does not inspect or contact a
phone, download firmware, modify device storage, or generate boot artifacts.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_DEVICE_FIELDS = (
    "name",
    "model",
    "codename",
    "architecture",
    "ram_gib",
    "storage_gib",
    "software_build",
    "kernel_source_release",
    "soc_platform_family",
)

REQUIRED_UNRESOLVED = (
    "physical_board_revision",
    "physical_board_id",
    "touchscreen_controller_revision",
    "wireless_combo_chip_identity",
)

ALLOWED_CONFIDENCE = {
    "owner_reported",
    "source_correlated",
    "exact_build_source",
    "unverified",
}


def validate_profile(profile: Any) -> list[str]:
    """Return validation errors; an empty list means structurally valid."""
    errors: list[str] = []

    if not isinstance(profile, dict):
        return ["profile root must be a JSON object"]

    if profile.get("profile_schema_version") != 1:
        errors.append("profile_schema_version must be 1")
    if profile.get("project") != "DroidiOSXNU":
        errors.append("project must be 'DroidiOSXNU'")

    device = profile.get("device")
    if not isinstance(device, dict):
        errors.append("device must be a JSON object")
    else:
        for field in REQUIRED_DEVICE_FIELDS:
            value = device.get(field)
            if value is None or value == "":
                errors.append(f"device.{field} is required")

        if device.get("architecture") != "arm64":
            errors.append("device.architecture must be 'arm64'")

        for field in ("ram_gib", "storage_gib"):
            value = device.get(field)
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                errors.append(f"device.{field} must be a positive integer")

    evidence = profile.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        errors.append("evidence must be a non-empty list")
    else:
        for index, item in enumerate(evidence):
            if not isinstance(item, dict):
                errors.append(f"evidence[{index}] must be an object")
                continue
            for field in ("field", "basis"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(f"evidence[{index}].{field} must be non-empty text")
            if item.get("confidence") not in ALLOWED_CONFIDENCE:
                errors.append(
                    f"evidence[{index}].confidence must be one of "
                    f"{', '.join(sorted(ALLOWED_CONFIDENCE))}"
                )

    unresolved = profile.get("unresolved")
    if not isinstance(unresolved, list) or any(
        not isinstance(item, str) or not item.strip() for item in unresolved
    ):
        errors.append("unresolved must be a list of non-empty strings")
    else:
        missing = [item for item in REQUIRED_UNRESOLVED if item not in unresolved]
        if missing:
            errors.append(
                "unresolved must retain these unknowns: " + ", ".join(missing)
            )

    scope = profile.get("scope")
    if not isinstance(scope, dict):
        errors.append("scope must be a JSON object")
    else:
        for flag in (
            "static_research_only",
            "hardware_accessed",
            "device_storage_modified",
            "bootable",
        ):
            if not isinstance(scope.get(flag), bool):
                errors.append(f"scope.{flag} must be a boolean")
        for flag in ("static_research_only",):
            if scope.get(flag) is not True:
                errors.append(f"scope.{flag} must be true")
        for flag in ("hardware_accessed", "device_storage_modified", "bootable"):
            if scope.get(flag) is not False:
                errors.append(f"scope.{flag} must be false")

    return errors


def load_profile(path: Path) -> Any:
    """Load JSON while allowing the caller to report file/parse errors."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a static, host-side DroidiOSXNU platform profile."
    )
    parser.add_argument(
        "profile",
        nargs="?",
        type=Path,
        default=Path("devices/moto-g60/platform-profile.json"),
        help="JSON profile path (default: Moto G60 research profile).",
    )
    parser.add_argument("--json", action="store_true", help="Print a JSON report.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        profile = load_profile(args.profile)
    except (OSError, json.JSONDecodeError) as exc:
        errors = [f"could not read valid JSON from {args.profile}: {exc}"]
    else:
        errors = validate_profile(profile)

    report = {
        "tool": "DroidiOSXNU platform profile validator",
        "mode": "HOST_ONLY_STATIC_VALIDATION",
        "valid": not errors,
        "hardware_accessed": False,
        "device_storage_modified": False,
        "bootable": False,
        "errors": errors,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    elif errors:
        print("PLATFORM PROFILE: INVALID")
        for error in errors:
            print(f"- {error}")
    else:
        print("PLATFORM PROFILE: VALID")
        print("Static metadata and evidence structure passed validation.")
        print("No hardware was accessed; no device storage was modified.")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
