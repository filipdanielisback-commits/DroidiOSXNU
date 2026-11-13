#!/usr/bin/env python3
"""Fetch the exact pinned Apple XNU source into an ignored local working tree.

This tool does not build a kernel, access a device, or create boot artifacts.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "kernel" / "xnu-source-pin.json"
DEFAULT_DESTINATION = ROOT / "kernel" / "upstream" / "xnu"
UPSTREAM_URL = "https://github.com/apple-oss-distributions/xnu.git"


def load_manifest(path=MANIFEST_PATH):
    with Path(path).open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return manifest


def validate_manifest(manifest):
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        return ["schema_version must be 1"]
    upstream = manifest.get("upstream")
    if not isinstance(upstream, dict):
        return ["upstream must be an object"]
    for key in ("repository", "tag", "tag_object_sha", "commit_sha"):
        value = upstream.get(key)
        if not isinstance(value, str) or not value.strip():
            return [f"upstream.{key} is required"]
    if upstream["repository"] != "apple-oss-distributions/xnu":
        return ["upstream.repository must be apple-oss-distributions/xnu"]
    for key in ("tag_object_sha", "commit_sha"):
        value = upstream[key]
        if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
            return [f"upstream.{key} must be a lowercase 40-character Git SHA"]
    handling = manifest.get("handling")
    if not isinstance(handling, dict):
        return ["handling must be an object"]
    for key in ("source_vendored", "device_access", "bootable_artifact"):
        if handling.get(key) is not False:
            return [f"handling.{key} must be false"]
    return []


def validate_destination(destination):
    destination = Path(destination).resolve()
    allowed_root = (ROOT / "kernel" / "upstream").resolve()
    if allowed_root not in destination.parents:
        raise ValueError(f"destination must be inside {allowed_root}")
    return destination


def run_git(arguments, cwd=None):
    result = subprocess.run(
        ["git", *arguments],
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def fetch_source(destination=DEFAULT_DESTINATION, git_runner=run_git):
    manifest = load_manifest()
    upstream = manifest["upstream"]
    destination = validate_destination(destination)
    tag = upstream["tag"]
    commit_sha = upstream["commit_sha"]
    tag_ref = f"refs/tags/{tag}"

    if destination.exists():
        if not destination.is_dir() or not (destination / ".git").exists():
            raise ValueError("destination exists but is not an XNU Git working tree")
        origin = git_runner(["remote", "get-url", "origin"], cwd=destination)
        if origin.rstrip("/") != UPSTREAM_URL.rstrip("/"):
            raise ValueError("existing working tree origin is not the pinned Apple XNU repository")
        status = git_runner(["status", "--porcelain"], cwd=destination)
        if status:
            raise ValueError("existing XNU working tree has local changes; refusing to overwrite them")
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        git_runner(
            ["clone", "--filter=blob:none", "--no-checkout", UPSTREAM_URL, str(destination)]
        )

    git_runner(
        ["fetch", "--filter=blob:none", "origin", f"{tag_ref}:{tag_ref}"],
        cwd=destination,
    )

    actual_tag_sha = git_runner(["rev-parse", f"{tag_ref}^{{tag}}"], cwd=destination)
    if actual_tag_sha != upstream["tag_object_sha"]:
        raise ValueError(
            f"annotated tag object mismatch: expected {upstream['tag_object_sha']}, "
            f"got {actual_tag_sha}"
        )

    actual_commit_sha = git_runner(["rev-parse", f"{tag_ref}^{{commit}}"], cwd=destination)
    if actual_commit_sha != commit_sha:
        raise ValueError(
            f"peeled commit mismatch: expected {commit_sha}, got {actual_commit_sha}"
        )

    git_runner(["checkout", "--detach", commit_sha], cwd=destination)
    actual_head = git_runner(["rev-parse", "HEAD"], cwd=destination)
    if actual_head != commit_sha:
        raise ValueError(f"checked-out HEAD mismatch: expected {commit_sha}, got {actual_head}")

    return {
        "valid": True,
        "repository": upstream["repository"],
        "tag": tag,
        "tag_object_sha": actual_tag_sha,
        "commit_sha": actual_head,
        "source_path": str(destination),
        "detached_head": True,
        "source_vendored": False,
        "device_access": False,
        "bootable_artifact": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Fetch the exact pinned Apple XNU source into kernel/upstream/xnu."
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=DEFAULT_DESTINATION,
        help="local destination (must remain inside kernel/upstream)",
    )
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    args = parser.parse_args(argv)

    try:
        report = fetch_source(args.destination)
    except (OSError, json.JSONDecodeError, subprocess.CalledProcessError, ValueError) as exc:
        detail = getattr(exc, "stderr", None)
        message = detail.strip() if detail else str(exc)
        report = {"valid": False, "error": message}
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(f"XNU SOURCE FETCH: FAILED - {message}")
        return 1

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("XNU SOURCE FETCH: PINNED APPLE SOURCE CHECKED OUT")
        print(f"Tag: {report['tag']}")
        print(f"Commit: {report['commit_sha']}")
        print(f"Local source: {report['source_path']}")
        print("The source remains local and is not vendored into this repository.")
        print("No build, device access, or boot artifact was produced.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
