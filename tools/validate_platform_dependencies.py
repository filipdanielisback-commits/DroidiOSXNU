#!/usr/bin/env python3
"""Validate the static Moto G60 platform dependency inventory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

DEFAULT_PATH = Path("devices/moto-g60/platform-dependencies.json")
STATUSES = {"documented_overlap", "partially_documented", "unknown", "not_implemented"}
CONFIDENCE = {"high", "medium", "low", "unknown"}
PRIORITIES = {"critical", "high", "medium", "low"}
REQUIRED_SCOPE = {
    "static_research_only": True,
    "host_side_only": True,
    "hardware_accessed": False,
    "device_storage_modified": False,
    "bootable": False,
}


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top-level JSON value must be an object"]
    if data.get("inventory_schema_version") != 1:
        errors.append("inventory_schema_version must be 1")
    if data.get("project") != "DroidiOSXNU":
        errors.append("project must be DroidiOSXNU")
    if data.get("assessment") != "static_source_research_only":
        errors.append("assessment must be static_source_research_only")

    dependencies = data.get("dependencies")
    if not isinstance(dependencies, list) or not dependencies:
        errors.append("dependencies must be a non-empty array")
        dependencies = []

    seen: set[str] = set()
    for index, item in enumerate(dependencies):
        prefix = f"dependencies[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        for field in ("id", "area", "finding"):
            if not isinstance(item.get(field), str) or not item[field].strip():
                errors.append(f"{prefix}.{field} must be a non-empty string")
        identifier = item.get("id")
        if isinstance(identifier, str):
            if identifier in seen:
                errors.append(f"{prefix}.id duplicates {identifier}")
            seen.add(identifier)
        if item.get("status") not in STATUSES:
            errors.append(f"{prefix}.status is invalid")
        if item.get("confidence") not in CONFIDENCE:
            errors.append(f"{prefix}.confidence is invalid")
        if item.get("priority") not in PRIORITIES:
            errors.append(f"{prefix}.priority is invalid")
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence or any(
            not isinstance(ref, str) or not ref.strip() for ref in evidence
        ):
            errors.append(f"{prefix}.evidence must be a non-empty array of path strings")
        unknowns = item.get("unknowns")
        if not isinstance(unknowns, list) or any(
            not isinstance(value, str) or not value.strip() for value in unknowns
        ):
            errors.append(f"{prefix}.unknowns must be an array of non-empty strings")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        errors.append("scope must be an object")
    else:
        for key, expected in REQUIRED_SCOPE.items():
            if scope.get(key) is not expected:
                errors.append(f"scope.{key} must be {str(expected).lower()}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", type=Path, default=DEFAULT_PATH)
    parser.add_argument("--json", action="store_true", help="emit a JSON validation report")
    args = parser.parse_args()

    try:
        data = json.loads(args.profile.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    else:
        errors = validate(data)

    report = {"valid": not errors, "errors": errors, "path": str(args.profile)}
    if args.json:
        print(json.dumps(report, indent=2))
    elif errors:
        print(f"Invalid platform dependency inventory: {len(errors)} error(s)")
        for error in errors:
            print(f"- {error}")
    else:
        print(f"Platform dependency inventory is structurally valid: {args.profile}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
