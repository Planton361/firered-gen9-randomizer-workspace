#!/usr/bin/env python3
"""Check repository branch and protected artifact paths without reading files."""

from __future__ import annotations

import argparse
import posixpath
import subprocess
import sys
from pathlib import PurePosixPath


FORBIDDEN_DIRS = ("04_private_roms", "05_builds", "03_tools/releases")
FORBIDDEN_EXTENSIONS = {
    ".gba", ".gb", ".gbc", ".sav", ".srm", ".state", ".ss0", ".ss1",
    ".zip", ".7z", ".exe", ".dll", ".jar",
}


def git(*args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ("git", *args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )


def normalize_repo_path(value: str) -> str:
    """Normalize a Git-reported path; never dereference or read the path."""
    path = value.strip().strip('"').replace("\\", "/")
    if not path:
        return ""
    normalized = posixpath.normpath(path)
    if normalized == "." or normalized.startswith("../") or normalized.startswith("/"):
        return normalized
    return str(PurePosixPath(normalized))


def forbidden(path: str) -> bool:
    normalized = normalize_repo_path(path)
    if not normalized or normalized.startswith(("../", "/")):
        return True
    lowered = normalized.casefold()
    if any(lowered == directory or lowered.startswith(directory + "/") for directory in FORBIDDEN_DIRS):
        return True
    name = PurePosixPath(lowered).name
    return (
        PurePosixPath(lowered).suffix in FORBIDDEN_EXTENSIONS
        or name == ".env"
        or name.startswith(".env.")
    )


def status_paths(raw: bytes) -> list[str]:
    """Extract both source and destination names from porcelain v1 -z records."""
    records = raw.decode("utf-8", "surrogateescape").split("\0")
    paths: list[str] = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record or len(record) < 4:
            continue
        xy, path = record[:2], record[3:]
        paths.append(path)
        if "R" in xy or "C" in xy:
            if index < len(records) and records[index]:
                paths.append(records[index])
            index += 1
    return paths


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-main",
        action="store_true",
        help="allow main only for read-only/bootstrap checking",
    )
    args = parser.parse_args()

    inside = git("rev-parse", "--is-inside-work-tree")
    if inside.returncode or inside.stdout.strip() != b"true":
        print("This command must run inside a Git worktree.", file=sys.stderr)
        return 2

    branch_result = git("rev-parse", "--abbrev-ref", "HEAD")
    branch = branch_result.stdout.decode("utf-8", "replace").strip()
    failures: list[str] = []
    if branch == "main" and not args.allow_main:
        failures.append("Current branch is main; use a work branch for changes.")

    tracked = git("ls-files", "-z")
    if tracked.returncode:
        print(tracked.stderr.decode("utf-8", "replace"), file=sys.stderr)
        return 2
    for path in tracked.stdout.decode("utf-8", "surrogateescape").split("\0"):
        if path and forbidden(path):
            failures.append(f"Forbidden tracked path: {normalize_repo_path(path)}")

    status = git("status", "--porcelain=v1", "-z", "-uall")
    if status.returncode:
        print(status.stderr.decode("utf-8", "replace"), file=sys.stderr)
        return 2
    for path in status_paths(status.stdout):
        if forbidden(path):
            failures.append(f"Forbidden path in Git status: {normalize_repo_path(path)}")

    print(f"Branch: {branch}")
    print("Git status:")
    sys.stdout.write(git("status", "--short").stdout.decode("utf-8", "replace"))
    if failures:
        print("\nGit safety check failed:")
        for failure in dict.fromkeys(failures):
            print(f"- {failure}")
        return 1
    print("\nGit safety check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
