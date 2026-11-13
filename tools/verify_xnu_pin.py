#!/usr/bin/env python3
"""Verify the pinned public XNU Git tag without downloading or building source."""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "kernel" / "xnu-source-pin.json"
API_ROOT = "https://api.github.com/repos"


def load_manifest(path):
    with Path(path).open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return manifest


def validate_manifest(manifest):
    errors = []
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        return ["schema_version must be 1"]
    upstream = manifest.get("upstream")
    if not isinstance(upstream, dict):
        return ["upstream must be an object"]
    for key in ("repository", "tag", "tag_object_sha", "commit_sha"):
        value = upstream.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"upstream.{key} is required")
    for key in ("tag_object_sha", "commit_sha"):
        value = upstream.get(key, "")
        if value and (len(value) != 40 or any(c not in "0123456789abcdef" for c in value)):
            errors.append(f"upstream.{key} must be a lowercase 40-character Git SHA")
    handling = manifest.get("handling")
    if not isinstance(handling, dict):
        errors.append("handling must be an object")
    else:
        for key in ("source_vendored", "device_access", "bootable_artifact"):
            if handling.get(key) is not False:
                errors.append(f"handling.{key} must be false")
    license_info = manifest.get("license")
    if not isinstance(license_info, dict) or not license_info.get("file") or not license_info.get("name"):
        errors.append("license.file and license.name are required")
    return errors


def fetch_json(url, timeout=15):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "DroidiOSXNU-source-pin-verifier",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def verify_upstream(manifest):
    upstream = manifest["upstream"]
    repository = upstream["repository"]
    tag = upstream["tag"]
    ref_url = f"{API_ROOT}/{repository}/git/ref/tags/{tag}"
    ref_data = fetch_json(ref_url)
    ref_object = ref_data.get("object", {})
    actual_tag_sha = ref_object.get("sha")
    if ref_object.get("type") != "tag":
        raise ValueError("upstream tag reference is not an annotated tag")
    if actual_tag_sha != upstream["tag_object_sha"]:
        raise ValueError(
            f"tag object mismatch: expected {upstream['tag_object_sha']}, got {actual_tag_sha}"
        )

    tag_data = fetch_json(f"{API_ROOT}/{repository}/git/tags/{actual_tag_sha}")
    target = tag_data.get("object", {})
    if target.get("type") != "commit":
        raise ValueError("annotated tag does not point directly to a commit")
    actual_commit_sha = target.get("sha")
    if actual_commit_sha != upstream["commit_sha"]:
        raise ValueError(
            f"peeled commit mismatch: expected {upstream['commit_sha']}, got {actual_commit_sha}"
        )
    return {
        "valid": True,
        "mode": "UPSTREAM_TAG_AND_COMMIT_VERIFICATION",
        "repository": repository,
        "tag": tag,
        "tag_object_sha": actual_tag_sha,
        "commit_sha": actual_commit_sha,
        "source_downloaded": False,
        "source_vendored": False,
        "device_access": False,
        "bootable_artifact": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check the pinned XNU tag and commit using GitHub's public API."
    )
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="path to the pin manifest")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="validate only the local manifest; do not make a network request",
    )
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    args = parser.parse_args(argv)

    try:
        manifest = load_manifest(args.manifest)
        if args.offline:
            report = {
                "valid": True,
                "mode": "OFFLINE_MANIFEST_VALIDATION",
                "source_downloaded": False,
                "source_vendored": False,
                "device_access": False,
                "bootable_artifact": False,
            }
        else:
            report = verify_upstream(manifest)
    except (OSError, json.JSONDecodeError, urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
        report = {"valid": False, "error": str(exc)}
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"XNU SOURCE PIN: FAILED - {exc}")
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    elif args.offline:
        print("XNU SOURCE PIN: LOCAL MANIFEST VALID")
        print("No network request, source download, device access, or boot artifact.")
    else:
        print("XNU SOURCE PIN: UPSTREAM TAG AND COMMIT VERIFIED")
        print(f"Tag: {report['tag']}")
        print(f"Commit: {report['commit_sha']}")
        print("No source download, device access, or boot artifact.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
