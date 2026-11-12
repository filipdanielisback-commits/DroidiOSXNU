#!/usr/bin/env python3
"""Best-effort, read-only inventory of selected properties in DTS/DTSI text.

This is intentionally not a complete Device Tree compiler. It does not resolve
includes, labels, overlays, phandles, macros, or inherited bus address cells.
Use dtc for syntax validation and a full DT parser for semantic analysis.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Iterable

TRACKED = ("compatible", "reg", "status")
TOKEN_RE = re.compile(r'"(?:\\.|[^"\\])*"|[{};=]|[^\s{};=]+')
NODE_RE = re.compile(r"^(?:[A-Za-z_][\w,.-]*@?[\w,.-]*|/|&[A-Za-z_][\w]*)$")


def strip_comments(source: str) -> str:
    """Remove C and C++ comments while preserving strings and line numbers."""
    out = []
    i = 0
    in_string = False
    escaped = False
    while i < len(source):
        ch = source[i]
        nxt = source[i + 1] if i + 1 < len(source) else ""
        if in_string:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            i += 1
        elif ch == '"':
            in_string = True
            out.append(ch)
            i += 1
        elif ch == "/" and nxt == "/":
            while i < len(source) and source[i] != "\n":
                out.append(" ")
                i += 1
        elif ch == "/" and nxt == "*":
            out.extend("  ")
            i += 2
            while i < len(source) and not (source[i] == "*" and i + 1 < len(source) and source[i + 1] == "/"):
                out.append("\n" if source[i] == "\n" else " ")
                i += 1
            if i < len(source):
                out.extend("  ")
                i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _clean_value(tokens: list[str]) -> str:
    return " ".join(tokens).strip()


def parse_dts(source: str, source_name: str = "<memory>") -> list[dict[str, object]]:
    """Extract node paths and compatible/reg/status properties."""
    text = strip_comments(source)
    tokens = [(m.group(0), text.count("\n", 0, m.start()) + 1) for m in TOKEN_RE.finditer(text)]
    stack: list[str] = []
    pending: list[tuple[str, int]] = []
    records: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for token, line in tokens:
        if token == "{":
            header = [t for t, _ in pending]
            pending.clear()
            # The final header token is the node name; preceding tokens may
            # contain a label (label:) or directives.
            name = header[-1] if header else "<unknown>"
            if name == ":" and len(header) > 1:
                name = header[-2]
            if name == "/":
                path = "/"
            elif name.startswith("&"):
                path = "/" + name
            else:
                parent = stack[-1] if stack else ""
                path = (parent.rstrip("/") + "/" + name) if parent else "/" + name
            stack.append(path)
            current = {
                "source": source_name,
                "line": line,
                "path": path,
                "compatible": None,
                "reg": None,
                "status": None,
            }
            records.append(current)
        elif token == ";":
            if current is not None and pending:
                parts = [t for t, _ in pending]
                if "=" in parts:
                    eq = parts.index("=")
                    key = parts[eq - 1] if eq else ""
                    if key in TRACKED:
                        current[key] = _clean_value(parts[eq + 1 :])
            pending.clear()
        elif token == "}":
            pending.clear()
            if stack:
                stack.pop()
            current = None
        else:
            pending.append((token, line))

    # Keep only nodes that contribute useful hardware inventory evidence.
    return [r for r in records if any(r[k] is not None for k in TRACKED)]


def discover(paths: Iterable[Path]) -> list[Path]:
    found: set[Path] = set()
    for item in paths:
        if item.is_dir():
            found.update(p for p in item.rglob("*") if p.is_file() and p.suffix in {".dts", ".dtsi"})
        elif item.is_file() and item.suffix in {".dts", ".dtsi"}:
            found.add(item)
    return sorted(found)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="DTS/DTSI files or directories")
    parser.add_argument("--format", choices=("json", "csv"), default="json")
    parser.add_argument("-o", "--output", type=Path, help="write report to this path (default: stdout)")
    args = parser.parse_args(argv)

    files = discover(args.paths)
    if not files:
        parser.error("no .dts or .dtsi files found")

    rows: list[dict[str, object]] = []
    for path in files:
        try:
            rows.extend(parse_dts(path.read_text(encoding="utf-8", errors="replace"), str(path)))
        except OSError as exc:
            print(f"warning: cannot read {path}: {exc}", file=sys.stderr)

    if args.format == "json":
        rendered = json.dumps(rows, indent=2) + "\n"
    else:
        from io import StringIO
        buffer = StringIO()
        fields = ("source", "line", "path", "compatible", "reg", "status")
        writer = csv.DictWriter(buffer, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
        rendered = buffer.getvalue()

    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
