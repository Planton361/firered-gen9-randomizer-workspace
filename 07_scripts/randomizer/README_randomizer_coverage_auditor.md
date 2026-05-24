# Randomizer Coverage Auditor

`randomizer_coverage_auditor.py` is a local-only helper for checking whether source-expected CFRU/DPE Pokemon, Items, and TM/HM item constants are visible in UPR-FVX Randomizer logs across many local runs.

The tool is designed for Anton's machine. Codex may build and test the parser, but must not run ROM batch mode.

## Purpose

The auditor answers review questions like:

- Which Pokemon constants exist in local CFRU/DPE source files?
- Which item and TM/HM constants exist in local CFRU/DPE source files?
- Which Pokemon and items appear in sanitized Randomizer logs across batch runs?
- Which observed labels do not match the source-derived expected index?
- Which observed labels are only shortened or normalized in logs and can be mapped back to expected source constants?
- Which loaded Pokemon are eligible for broad Wild, Trainer, Starter, or Static randomizer pools under a supplied settings/profile file?

It does not prove full gameplay reachability. Random batch observations are useful evidence, but absence from logs is not the same as absence from the loaded ROM or from the game.

## Limits

`EXPECTED_NOT_OBSERVED` is not a hard error. It only means the label was not seen in the parsed logs.

Sanitized loaded manifests generated after ROM load can distinguish:

- `EXPECTED_NOT_LOADED`: expected source constant was not loaded by UPR-FVX.
- `LOADED_NOT_OBSERVED`: loaded by UPR-FVX but not seen in batch logs.

Sanitized eligibility manifests generated after ROM load plus settings/profile evaluation can further distinguish:

- `LOADED_NOT_ELIGIBLE`: loaded by UPR-FVX but excluded by broad settings/profile eligibility filters.
- `ELIGIBLE_NOT_OBSERVED`: loaded and eligible, but not seen in parsed batch logs.
- `ELIGIBLE_AND_OBSERVED`: loaded, eligible, and observed.

Without a loaded manifest, batch runs cannot prove complete Pokemon or item coverage.
Without an eligibility manifest, `LOADED_NOT_OBSERVED` does not explain whether a loaded Pokemon was actually eligible for the active settings/profile.

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

Export a sanitized loaded manifest after ROM load:

```sh
python 07_scripts/randomizer/randomizer_coverage_auditor.py export-loaded \
  --jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar \
  --input-rom /PRIVATE/PATH/input.gba \
  --output-dir .local/randomizer-coverage
```

Equivalent direct UPR-FVX command:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar loaded-manifest \
  --input-rom /PRIVATE/PATH/input.gba \
  --output-dir .local/randomizer-coverage
```

Export a sanitized Species eligibility manifest after ROM load and settings/profile evaluation:

```sh
python 07_scripts/randomizer/randomizer_coverage_auditor.py export-eligible \
  --jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar \
  --input-rom /PRIVATE/PATH/input.gba \
  --settings-file /PRIVATE/PATH/profile.rnqs \
  --output-dir .local/randomizer-coverage
```

Equivalent direct UPR-FVX command:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar eligible-manifest \
  --input-rom /PRIVATE/PATH/input.gba \
  --settings-file /PRIVATE/PATH/profile.rnqs \
  --output-dir .local/randomizer-coverage
```

Compare with loaded-manifest files:

```sh
python 07_scripts/randomizer/randomizer_coverage_auditor.py compare \
  --output-dir .local/randomizer-coverage
```

`compare` auto-detects `species_loaded.tsv`, `items_loaded.tsv`, `tms_hms_loaded.tsv`, and `species_eligible.tsv` in the output directory. You can also pass `--loaded-manifest-dir` and `--eligibility-manifest-dir` explicitly.

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
- `.local/randomizer-coverage/species_loaded.tsv`
- `.local/randomizer-coverage/items_loaded.tsv`
- `.local/randomizer-coverage/tms_hms_loaded.tsv`
- `.local/randomizer-coverage/species_eligible.tsv`

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
- `*_loaded.tsv`
- `*_eligible.tsv`
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
| `EXPECTED_NOT_LOADED` | A source-derived expected row is absent from the sanitized loaded manifest. This is a hard failure candidate. |
| `LOADED_NOT_OBSERVED` | Loaded by UPR-FVX but not observed in parsed logs. This is not a hard failure. |
| `LOADED_NOT_ELIGIBLE` | Loaded by UPR-FVX but excluded by the supplied settings/profile eligibility manifest. This is not a hard failure. |
| `ELIGIBLE_NOT_OBSERVED` | Loaded and eligible under the supplied settings/profile manifest, but not observed in parsed logs. This is not a hard failure. |
| `ELIGIBLE_AND_OBSERVED` | Loaded, eligible under the supplied settings/profile manifest, and observed in parsed logs. |
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

## Alias Normalization

Observed labels are normalized before comparison with expected source constants. This reduces review noise from:

- Accents and typographic punctuation, such as `Flabébé` and `Farfetch’d`.
- Shortened Species labels, such as `Squawkbily`, `Baculegion`, `Dudunsprce`, and selected Paradox names logged without spaces or underscores.
- CamelCase or shortened item labels, such as `RageCandyBar`, `Lumiose Gal.`, `Max Candy`, `BalmMushroom`, `Whip Dream`, `Straw. Sweet`, `Rusty Sword`, `Necrozium Z`, `TinyMushroom`, `BrightPowder`, `DeepSeaScale`, `Nevermeltice`, `Paralyz Heal`, `Marang Berry`, `HeavyDBoots`, `Auspicious-A`, `CharzarditeX`, `Bird Fossil`, `Wish Piece`, `A-Potion`, `Gimmi Coin`, `Well. Mask`, `EV-IV Viewer`, `Masp. Teacup`, `Unr. Teacup`, `Protec Pads`, `Ut. Umbrella`, Memory abbreviations, Mask abbreviations, Nectar abbreviations, and Apricorn abbreviations.

Loaded-manifest comparison uses the same normalization layer. For Species, stable source/internal IDs are also accepted as loaded matches, so form keys such as `rotom_heat` do not become hard `EXPECTED_NOT_LOADED` rows when the manifest uses a base display label with the same internal ID. For Items, matching intentionally prefers canonical/name aliases over raw IDs because source item IDs and loaded manifest IDs may not always be comparable across local tables.

Loaded-item aliases may also include manifest-only local display names such as `Safe Guard` for source-expected `Safety Goggles`. Those aliases are not applied to Pokemon, moves, or TM/HM move-name parsing.

Non-reward bookkeeping constants such as `ITEM_USE_*`, key-item/system constants, free-space placeholders, local Mega accessory placeholders, and reviewed legacy/source-collision constants are excluded from the expected reward item index. If an older expected TSV still contains such a row, compare mode does not promote it to a hard loaded-manifest failure.

Trainer held items are parsed only from explicit Trainer Pokemon party entries with `Species@Item Lv...` format. Trainer-class labels such as `Black Belt` are not treated as held items unless they appear in that explicit item position.

## TM/HM Coverage Caveat

TM/HM labels are counted when they appear in Shop, Pickup, Field, or explicit TM/HM log sections. A batch profile that does not randomize or log TM/HM slots will naturally leave most TM/HM rows as `EXPECTED_NOT_OBSERVED`.

Expected labels such as `ITEM_HM06_ROCK_SMASH`, `hm06_rock_smash`, `ITEM_HM08_ROCK_CLIMB`, and loaded labels such as `HM06` or `HM08` are matched by TM/HM number during loaded-manifest comparison. Item-scope loaded hard-fail checks delegate TM/HM constants to `tm_hm_coverage.tsv`, so HM rows are not double-counted as missing reward items.

Do not treat TM/HM `EXPECTED_NOT_OBSERVED` as proof of missing TM/HM loading. It only means the current logs did not contain matching TM/HM observations.

## Loaded Manifest Export

The UPR-FVX local-only `loaded-manifest` command loads a private ROM and writes sanitized loaded manifests:

- `species_loaded.tsv`
- `items_loaded.tsv`
- `tms_hms_loaded.tsv`

Those manifests contain aggregate names/keys, internal IDs, family labels, loaded flags, and item policy flags where the ROM model exposes them. They do not contain ROM paths, output-ROM paths, hashes, seeds, raw offsets, full logs, or private filesystem information.

Codex must not run this mode with a ROM. Anton runs it locally and shares or commits only reviewed sanitized TSV summaries when needed.

## Eligibility Manifest Export

The UPR-FVX local-only `eligible-manifest` command loads a private ROM, reads a private `.rnqs` settings/profile file, sets the same global Species restrictions used before randomization, and writes:

- `species_eligible.tsv`

The current exporter is intentionally conservative. It reports broad Species eligibility for Wild, Trainer, Starter, and Static pools after core settings and randomizer filters such as Gen Limit, Mega/GMax/Regional form options, alternate-form flags, legendary restrictions, ability-dependent/irregular-form bans, known Wild/Trainer/Static bans, starter basic/BST/type constraints, and CFRU/DPE random-pool asset guards where available.

It does not claim exact slot-level eligibility for every route, trainer, type theme, local Pokemon setting, similar-strength window, static restricted list, or per-encounter context. Treat `LOADED_NOT_ELIGIBLE` as an explanation for broad settings/profile exclusion, and treat `ELIGIBLE_NOT_OBSERVED` as non-hard sampling evidence.

Codex must not run this mode with a ROM. Anton runs it locally and shares or commits only reviewed sanitized TSV summaries when needed.
