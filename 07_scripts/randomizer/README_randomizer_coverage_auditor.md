# Randomizer Coverage Auditor

`randomizer_coverage_auditor.py` is a local-only helper for checking whether source-expected CFRU/DPE Pokemon, Items, and TM/HM item constants are visible in UPR-FVX Randomizer logs across many local runs.

The tool is designed for Anton's machine. Codex may build and test the parser, but must not run ROM batch mode.

## Purpose

The auditor answers review questions like:

- Which Pokemon constants exist in local CFRU/DPE source files?
- Which item and TM/HM constants exist in local CFRU/DPE source files?
- Which Pokemon and items appear in sanitized Randomizer logs across batch runs?
- Which observed labels do not match the source-derived expected index?

It does not prove full gameplay reachability. Random batch observations are useful evidence, but absence from logs is not the same as absence from the loaded ROM or from the game.

## Limits

`EXPECTED_NOT_OBSERVED` is not a hard error. It only means the label was not seen in the parsed logs.

Only a future sanitized loaded-manifest generated after ROM load can distinguish:

- `EXPECTED_NOT_LOADED`: expected source constant was not loaded by UPR-FVX.
- `LOADED_NOT_OBSERVED`: loaded by UPR-FVX but not seen in batch logs.

Without a loaded manifest, batch runs cannot prove complete Pokemon or item coverage.

## CLI Examples

Build source-derived expected TSVs without a ROM:

```sh
python 07_scripts/randomizer/randomizer_coverage_auditor.py build-expected \
  --output-dir .local/randomizer-coverage
```

Parse existing local logs:

```sh
python 07_scripts/randomizer/randomizer_coverage_auditor.py parse-logs \
  --logs-dir .local/randomizer-coverage/raw-logs \
  --output-dir .local/randomizer-coverage \
  --delete-raw
```

Run local batches, parse logs, and delete raw logs/output ROMs after summaries:

```sh
python 07_scripts/randomizer/randomizer_coverage_auditor.py batch-run \
  --jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar \
  --input-rom /PRIVATE/PATH/input.gba \
  --settings-file /PRIVATE/PATH/profile.rnqs \
  --runs 1000 \
  --output-dir .local/randomizer-coverage \
  --seed-strategy sequential \
  --seed-base 12000
```

Full local flow:

```sh
python 07_scripts/randomizer/randomizer_coverage_auditor.py all \
  --jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar \
  --input-rom /PRIVATE/PATH/input.gba \
  --settings-file /PRIVATE/PATH/profile.rnqs \
  --runs 1000 \
  --output-dir .local/randomizer-coverage \
  --seed-strategy sequential \
  --seed-base 12000
```

## Output Files

Expected indexes:

- `.local/randomizer-coverage/species_expected.tsv`
- `.local/randomizer-coverage/items_expected.tsv`
- `.local/randomizer-coverage/tms_hms_expected.tsv`

Observed summaries:

- `.local/randomizer-coverage/species_observed.tsv`
- `.local/randomizer-coverage/items_observed.tsv`
- `.local/randomizer-coverage/tms_hms_observed.tsv`

Coverage comparisons:

- `.local/randomizer-coverage/species_coverage.tsv`
- `.local/randomizer-coverage/items_coverage.tsv`
- `.local/randomizer-coverage/tm_hm_coverage.tsv`
- `.local/randomizer-coverage/coverage_summary.md`
- `.local/randomizer-coverage/suspicious_or_missing.tsv`

Raw local-only paths used by `batch-run`:

- `.local/randomizer-coverage/raw-logs/`
- `.local/randomizer-coverage/output-roms/`

By default, raw logs and output ROMs are deleted after successful batch analysis. Use `--keep-raw` only for local debugging.

## Safe To Share Or Commit

Only sanitized summaries may be shared or committed after review:

- `*_expected.tsv`
- `*_observed.tsv`
- `*_coverage.tsv`
- `coverage_summary.md`
- `suspicious_or_missing.tsv`

Do not share or commit:

- ROMs
- output ROMs
- raw logs or full logs
- saves
- screenshots
- private paths
- hashes
- secrets, tokens, or `.env` content

`.local/` is ignored by the workspace `.gitignore`.

## Coverage Status

| Status | Meaning |
| --- | --- |
| `EXPECTED_AND_OBSERVED` | A source-derived expected row appeared in parsed Randomizer logs. |
| `EXPECTED_NOT_OBSERVED` | A source-derived expected row did not appear in parsed logs. This is not a hard failure. |
| `OBSERVED_NOT_EXPECTED` | A parsed log label did not match the source-derived expected index. Review mapping, spelling, parser logic, or source constants. |
| `EXPECTED_NOT_LOADED` | Reserved for a future loaded-manifest flow; only valid when a sanitized loaded manifest is supplied. |
| `LOADED_NOT_OBSERVED` | Reserved for a future loaded-manifest flow; loaded by UPR-FVX but not observed in logs. |
| `FILTERED_BY_POLICY` | Reserved for later policy-aware reports. |
| `MECHANIC_GATED` | Reserved for later policy-aware reports, especially Mega/Z/Dynamax/GMax. |
| `BANNED_EXPECTED` | Reserved for later policy-aware reports. |
| `UNKNOWN_REVIEW` | Source-derived expectation exists, but no observation/loaded status has been assigned yet. |

## Parser Coverage

The log parser currently handles:

- Starter Pokemon sections.
- Static Pokemon sections.
- Wild Pokemon sections.
- Trainer Pokemon sections.
- Shop Items and Pickup Items through the existing `item_pool_batch_analyzer.py` parser.
- Field Items when the log contains simple `old => new` or `- item` lines.
- TM/HM labels such as `TM01`, `TM51`, and `HM01` when they appear in item or TM/HM sections.

The parser is intentionally tolerant and review-oriented. If a future UPR-FVX log format changes, `OBSERVED_NOT_EXPECTED` rows should be reviewed before treating them as data bugs.

## Loaded Manifest Future Work

The current UPR-FVX CLI can run randomization and write detailed logs, but this workspace tool does not add a ROM-load diagnostic export. A future UPR-FVX local-only diagnostic could emit sanitized loaded manifests:

- `species_loaded.tsv`
- `items_loaded.tsv`
- `tms_hms_loaded.tsv`

Those manifests should contain aggregate names/keys only, with no ROM paths, hashes, seeds, raw offsets, full logs, or private filesystem information.
