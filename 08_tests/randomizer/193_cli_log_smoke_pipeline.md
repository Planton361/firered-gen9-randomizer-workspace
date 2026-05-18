# CLI Log Smoke Pipeline

## Scope

This document defines a repo-safe, local-only CLI log smoke for the pinned UPR-FVX jar.

Codex does not run this smoke with a ROM. The private input ROM, generated output ROM, raw CLI stdout and detailed UPR-FVX log stay local under ignored paths.

The goal is a fast CLI counterpart to the GUI smoke:

1. Run `UPR-FVX.jar cli` with a local private ROM and a known settings file/string.
2. Ask UPR-FVX to generate its detailed log with `-l`.
3. Produce a sanitized summary report.
4. Check the report for CLI success and known bad markers.

## Helper Script

Use:

```sh
07_scripts/randomizer/cli_log_smoke_pipeline.sh \
  --rom <private-input.gba> \
  --settings-file <local-settings-file> \
  --output-rom 05_builds/randomizer-smoke/cli-log-smoke/output.gba \
  --report 05_builds/randomizer-smoke/cli-log-smoke/sanitized-report.md
```

Optional:

```sh
07_scripts/randomizer/cli_log_smoke_pipeline.sh \
  --rom <private-input.gba> \
  --settings-string '<settings-string>' \
  --output-rom 05_builds/randomizer-smoke/cli-log-smoke/output.gba \
  --report 05_builds/randomizer-smoke/cli-log-smoke/sanitized-report.md \
  --seed 123456789
```

Settings files are preferred for local runs because they avoid putting a settings string into shell history.

The script defaults to:

```text
02_external/upr-fvx/random/build/libs/UPR-FVX.jar
```

Build the jar locally first if needed:

```sh
git -C 02_external/upr-fvx rev-parse HEAD
cd 02_external/upr-fvx
./gradlew :random:jar
```

## Dry Run

The helper supports a dry run that does not read a ROM or create output:

```sh
07_scripts/randomizer/cli_log_smoke_pipeline.sh \
  --rom <private-input.gba> \
  --settings-file <local-settings-file> \
  --output-rom 05_builds/randomizer-smoke/cli-log-smoke/output.gba \
  --report 05_builds/randomizer-smoke/cli-log-smoke/sanitized-report.md \
  --dry-run
```

## Pass Criteria

The sanitized report should show:

```text
UPR-FVX CLI exit code: 0
CLI success marker observed: yes
Output ROM created: yes
Detailed UPR-FVX log created: yes
Fatal marker count: 0
Known bad marker count: 0
ROM path/hash/full log documented: no
Output path documented: no
P1 promotion: no
```

The helper treats these as blocked markers:

- `Exception`
- `ERROR:`
- `Randomization failed`
- `IndexOutOfBoundsException`
- `NullPointerException`
- `NoSuchElementException`
- `NEW GIVEN = ?`
- `move-less`
- `missing sprite`
- `unknown/undecoded`
- `SpeciesMovesetRandomizer` `IndexOutOfBoundsException`

## Recommended Stable CLI Profile

Use a settings file matching the current Stable Visual Profile plus the now-passed Starter Pokemon option only when that profile is intentionally being sampled.

Keep disabled unless explicitly testing them:

- Trainer Class Names, because it is textlabel-only and can visually mismatch trainer sprites.
- Evolution Randomization.
- Special-Wild, Day/Night and Swarms.
- `Rival Carries Starter Through Game`, because the full-rival path remains separate from the Oak-Lab first Rival sync.

## Sanitized Handoff Format

Use this exact structure when reporting local CLI smoke evidence:

```text
CLI randomization completed: yes/no
Output ROM created: yes/no
Detailed log created: yes/no
Fatal markers: none / sanitized category
Known bad markers: none / sanitized category
Settings profile: Stable Visual / Stable Visual + Starter Pokemon / other narrow block
Local boot/play check: not in scope / yes / no
Error summary: sanitized, no paths/logs/hashes
```

Do not include:

- ROM paths.
- Output ROM paths.
- ROM hashes or file hashes.
- Full logs or stack traces.
- Screenshots.
- Save files, emulator states or build artifacts.
- Tokens, secrets or `.env` data.

## Evidence Boundary

This is pipeline/tooling evidence only until a local run is reported back with sanitized results. It does not read or write ROMs by itself in the repo, does not commit output artifacts and does not promote any feature to P1-supported.
