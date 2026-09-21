#!/usr/bin/env python3
"""POSIX-friendly CLI for the synthetic host contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ai_policy.metrics import summarize
from ai_policy.runner import replay_matches, run_all, run_fixture, twin_mismatches
from ai_policy.schema import FixtureError, load_fixtures


FIXTURE_DIRECTORY = Path(__file__).resolve().parent / "fixtures"
DEFAULT_FIXTURES = FIXTURE_DIRECTORY / "synthetic_fixtures.json"
STANDARD_FIXTURES = FIXTURE_DIRECTORY / "standard_fixtures.json"
IRONMON_FIXTURES = FIXTURE_DIRECTORY / "ironmon_fixtures.json"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Synthetic Trainer AI host contract")
    result.add_argument("--fixtures", type=Path)
    subparsers = result.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate")
    run = subparsers.add_parser("run")
    run.add_argument("--policy", default="uniform_legal")
    run.add_argument("--replicate", type=int, default=0)
    replay = subparsers.add_parser("replay")
    replay.add_argument("--fixture-id", required=True)
    replay.add_argument("--policy", default="uniform_legal")
    replay.add_argument("--replicate", type=int, default=0)
    summary = subparsers.add_parser("summarize")
    summary.add_argument("--policy", default="uniform_legal")
    summary.add_argument("--replicate", type=int, default=0)
    return result


def emit(value: object) -> None:
    sys.stdout.write(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n")


def _fixture_paths(args: argparse.Namespace) -> tuple[Path, ...]:
    if args.fixtures is not None:
        return (args.fixtures,)
    if args.command == "validate":
        return (DEFAULT_FIXTURES, STANDARD_FIXTURES, IRONMON_FIXTURES)
    if getattr(args, "policy", None) == "standard":
        return (STANDARD_FIXTURES,)
    if getattr(args, "policy", None) == "ironmon_smart":
        return (IRONMON_FIXTURES,)
    return (DEFAULT_FIXTURES,)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        fixtures = [
            fixture
            for path in _fixture_paths(args)
            for fixture in load_fixtures(path)
        ]
        if args.command == "validate":
            schemas = sorted({fixture["schema_version"] for fixture in fixtures})
            emit({
                "fixture_count": len(fixtures),
                "schema_versions": schemas,
                "status": "PASS",
            })
        elif args.command == "run":
            for result in run_all(fixtures, args.policy, args.replicate):
                sys.stdout.buffer.write(result.line)
        elif args.command == "replay":
            by_id = {fixture["fixture_id"]: fixture for fixture in fixtures}
            if args.fixture_id not in by_id:
                raise FixtureError(f"unknown fixture ID: {args.fixture_id}")
            fixture = by_id[args.fixture_id]
            result = run_fixture(fixture, args.policy, args.replicate)
            emit({"byte_identical": replay_matches(fixture, args.policy, args.replicate),
                  "draw_count": result.trace["policy_rng"]["draw_count"],
                  "fixture_id": args.fixture_id, "status": "PASS"})
        else:
            results = run_all(fixtures, args.policy, args.replicate)
            summary = summarize(results)
            summary["twin_mismatches"] = twin_mismatches(results)
            emit(summary)
    except (FixtureError, ValueError) as error:
        sys.stderr.write(f"ERROR: {error}\n")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
