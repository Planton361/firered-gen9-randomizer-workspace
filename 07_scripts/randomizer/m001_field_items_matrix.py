#!/usr/bin/env python3
"""Run the six sanitized M-001 UPR-FVX Field Items save/reload rows."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Final


WORKSPACE: Final = Path(__file__).resolve().parents[2]
RUNNER_SOURCE: Final = Path(__file__).with_name("M001FieldItemsMatrixRunner.java")
ROWS: Final = (
    ("unchanged", "off"),
    ("shuffle", "off"),
    ("random", "off"),
    ("random", "on"),
    ("random-even", "off"),
    ("random-even", "on"),
)
RESULT_KEYS: Final = (
    "mode",
    "banBad",
    "candidateLoaded",
    "saveSuccessful",
    "reloadSuccessful",
    "rawApiTmSlotAlignmentMismatches",
    "tmFieldItemSlotMismatches",
    "nonTmFieldItemSlotMismatches",
    "requiredFieldTMMissingAfter",
    "fieldItemReloadMismatches",
    "lowByte92Discovery",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run six fresh, sanitized UPR-FVX Field Items rows against a private ROM."
    )
    parser.add_argument("--rom", required=True, help="Local private input ROM; never printed or overwritten.")
    parser.add_argument("--upr-jar", required=True, help="Explicit UPR-FVX runtime JAR.")
    parser.add_argument("--output-dir", required=True, help="Ignored destination directory for runtime artifacts.")
    parser.add_argument("--dry-run", action="store_true", help="Validate locations and show rows without opening the ROM.")
    return parser.parse_args()


def safe_error(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def output_dir_is_safe(output_dir: Path) -> bool:
    resolved = output_dir.resolve(strict=False)
    build_root = (WORKSPACE / "05_builds").resolve(strict=False)
    try:
        resolved.relative_to(build_root)
        return True
    except ValueError:
        pass
    # A caller-selected external directory must already exist; never create an unverified target.
    try:
        resolved.relative_to(WORKSPACE.resolve())
        return False
    except ValueError:
        return resolved.is_dir()


def validate_environment(args: argparse.Namespace) -> tuple[Path, Path, Path] | None:
    rom = Path(args.rom)
    jar = Path(args.upr_jar)
    output_dir = Path(args.output_dir)
    if shutil.which("java") is None or shutil.which("javac") is None:
        safe_error("Java and javac are both required.")
        return None
    if not RUNNER_SOURCE.is_file():
        safe_error("Committed Java runner is unavailable.")
        return None
    if not jar.is_file():
        safe_error("UPR-FVX runtime JAR is unavailable.")
        return None
    if not output_dir_is_safe(output_dir):
        safe_error("Output directory must be under ignored 05_builds or be an existing external directory.")
        return None
    if not args.dry_run and not rom.is_file():
        safe_error("Private input ROM is unavailable.")
        return None
    return rom, jar, output_dir


def print_rows(prefix: str = "") -> None:
    for mode, ban_bad in ROWS:
        print(f"{prefix}mode={mode}")
        print(f"{prefix}banBad={ban_bad}")


def compile_runner(jar: Path, classes_dir: Path) -> bool:
    classes_dir.mkdir(parents=True, exist_ok=False)
    completed = subprocess.run(
        ["javac", "-cp", str(jar), "-d", str(classes_dir), str(RUNNER_SOURCE)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if completed.returncode:
        safe_error("Could not compile the workspace-side Java runner.")
        return False
    return True


def sanitized_result(stdout: str, mode: str, ban_bad: str) -> list[str]:
    values: dict[str, str] = {}
    for line in stdout.splitlines():
        key, separator, value = line.partition("=")
        if separator and key in RESULT_KEYS:
            values[key] = value
    fallback = {
        "mode": mode,
        "banBad": ban_bad,
        "candidateLoaded": "false",
        "saveSuccessful": "false",
        "reloadSuccessful": "false",
        "rawApiTmSlotAlignmentMismatches": "-1",
        "tmFieldItemSlotMismatches": "-1",
        "nonTmFieldItemSlotMismatches": "-1",
        "requiredFieldTMMissingAfter": "-1",
        "fieldItemReloadMismatches": "-1",
        "lowByte92Discovery": "false",
    }
    fallback.update(values)
    return [f"{key}={fallback[key]}" for key in RESULT_KEYS]


def run_matrix(rom: Path, jar: Path, output_dir: Path) -> int:
    run_dir = output_dir / f"m001-field-items-{dt.datetime.now(dt.UTC).strftime('%Y%m%dT%H%M%SZ')}-{os.getpid()}"
    run_dir.mkdir(parents=True, exist_ok=False)
    classes_dir = run_dir / "runner-classes"
    if not compile_runner(jar, classes_dir):
        return 1

    failure = False
    for row_number, (mode, ban_bad) in enumerate(ROWS, start=1):
        row_dir = run_dir / f"row-{row_number:02d}"
        row_dir.mkdir()
        output_rom = row_dir / "randomized-output.gba"
        completed = subprocess.run(
            [
                "java", "-cp", f"{classes_dir}{os.pathsep}{jar}", "M001FieldItemsMatrixRunner",
                "--input", str(rom), "--output", str(output_rom), "--mode", mode, "--ban-bad", ban_bad,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            check=False,
        )
        lines = sanitized_result(completed.stdout, mode, ban_bad)
        print("\n".join(lines))
        values = dict(line.split("=", 1) for line in lines)
        row_passed = (
            values["candidateLoaded"] == "true"
            and values["saveSuccessful"] == "true"
            and values["reloadSuccessful"] == "true"
            and all(values[key] == "0" for key in RESULT_KEYS[5:10])
            and values["lowByte92Discovery"] == "true"
        )
        failure = failure or completed.returncode != 0 or not row_passed
    return 1 if failure else 0


def main() -> int:
    args = parse_args()
    validated = validate_environment(args)
    if validated is None:
        return 2
    _, _, _ = validated
    if args.dry_run:
        print("dryRun=true")
        print("romOpened=false")
        print("randomizedOutputsCreated=false")
        print_rows()
        return 0
    return run_matrix(*validated)


if __name__ == "__main__":
    raise SystemExit(main())
