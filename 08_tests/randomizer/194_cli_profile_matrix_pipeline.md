# CLI Profile Matrix Pipeline

## Scope

This document extends the CLI log smoke into a profile matrix runner.

Codex may only test this pipeline with `--dry-run` or artificial fixtures. Real ROM-smokes remain local-only user work. Private ROMs, output ROMs, raw logs and reports with private paths stay under ignored local paths.

## Technical Decision

FVX settings are not plain text. `Settings.writeToFileFormat(...)` writes:

- a four-byte settings version,
- a four-byte payload length,
- a Base64 settings payload,
- CRC/checksum state inside the payload.

`CliRandomizer` reads settings via `-s <settings file>` or `-S <settings string>`, then reconstructs `Settings` through FVX's Java code.

Because of that, this workspace PR does not byte-patch `.rnqs` files from shell/Python. The safe implementation is Option C for now:

- Profile settings are saved locally, usually from the GUI.
- A manifest lists the profile IDs and local settings files.
- The matrix runner executes each profile through the existing CLI log smoke helper.
- A sanitized aggregate report is produced.

Target state remains Option A or B later:

- Option A: add an FVX CLI/helper subcommand in a separate UPR-FVX PR to derive profile settings using `Settings` APIs.
- Option B: add a Java workspace helper that links against UPR-FVX classes and writes settings with `Settings.writeToFileFormat(...)`.

## Files

- `07_scripts/randomizer/cli_log_smoke_pipeline.sh`
- `07_scripts/randomizer/generate_cli_smoke_profiles.sh`
- `07_scripts/randomizer/run_cli_profile_matrix.sh`
- `08_tests/randomizer/cli_profile_matrix.example.tsv`

## Manifest Format

Tab-separated columns:

```text
profile_id  enabled  expected_result  settings_file  seed  notes
```

Expected results:

- `PASS_LOG`: profile should pass with zero fatal/bad markers.
- `PASS_WITH_WARNINGS`: profile should pass; warning markers are acceptable.
- `EXPECTED_FAIL`: profile is intentionally blocked or risky until separately fixed.

The example manifest covers:

- `00_baseline`
- `01_traits_full`
- `02_starters_statics_trades_full`
- `03_moves_movesets_full`
- `04_foe_base`
- `04_foe_held_items_basic`
- `04_foe_held_items_sensible_expected_fail`
- `05_wild_full`
- `06_tm_tutor_full`
- `07_items_full`
- `08_types_full`
- `09_graphics_palettes`
- `10_misc_tweaks`
- `11_special_wild`

## Scaffold a Local Manifest

```sh
07_scripts/randomizer/generate_cli_smoke_profiles.sh \
  --output 05_builds/randomizer-smoke/cli-profile-matrix/profiles.tsv
```

This only writes a manifest scaffold. It does not create or modify `.rnqs` settings files.

## Dry Run

```sh
07_scripts/randomizer/run_cli_profile_matrix.sh \
  --profile-manifest 08_tests/randomizer/cli_profile_matrix.example.tsv \
  --output-dir /tmp/upr-fvx-cli-profile-matrix \
  --summary-report /tmp/upr-fvx-cli-profile-matrix/summary.md \
  --dry-run
```

Dry-run validates the matrix wiring and delegates each profile to `cli_log_smoke_pipeline.sh --dry-run`. It does not check that ROM or settings files exist.

## Local Real Run

After creating real local settings files:

```sh
07_scripts/randomizer/run_cli_profile_matrix.sh \
  --profile-manifest 05_builds/randomizer-smoke/cli-profile-matrix/profiles.tsv \
  --rom <private-input.gba> \
  --output-dir 05_builds/randomizer-smoke/cli-profile-matrix/run-001 \
  --summary-report 05_builds/randomizer-smoke/cli-profile-matrix/run-001/summary.md
```

The aggregate report table is:

```text
profile_id | result | bad markers | warnings | next action
```

## Current Roadmap Mapping

Stable or expected-pass profiles:

- `00_baseline`
- `01_traits_full`
- `02_starters_statics_trades_full`
- `03_moves_movesets_full`
- `04_foe_base`
- `04_foe_held_items_basic`
- `05_wild_full`
- `06_tm_tutor_full`
- `07_items_full`

Caveated profile:

- `08_types_full`, because type-effectiveness chaos can be intentionally disruptive.

Expected-fail or not-stable profiles until separately fixed:

- `04_foe_held_items_sensible_expected_fail`
- `09_graphics_palettes`
- `10_misc_tweaks`
- `11_special_wild`

## Evidence Boundary

The GUI is still needed only to create a base settings profile unless a future FVX settings helper exists. The target state is manifest-driven profile generation where feature blocks can be activated automatically by a helper that uses FVX `Settings` APIs.

This pipeline does not promote P1. It is orchestration and reporting infrastructure for local smoke evidence.
