# FVX Feature Test Status Matrix

## Purpose

`fvx_feature_test_status_matrix.tsv` is the existing feature execution ledger: the 130 historical dashboard IDs plus two current public-source overlay IDs, for **132 rows**. It is supporting evidence under Workspace Issue #727, not an operational queue.

The dashboard remains the human overview. The TSV is the per-feature execution ledger that can later be joined to the CLI profile matrix and updated one feature at a time.

## Status Model

`test_mode` values:

- `single`: tested as a focused single feature.
- `tab_full`: tested as part of a full GUI tab/profile block.
- `cumulative`: tested only as part of a broader cumulative profile.
- `risk_interaction`: passed or failed with an important interaction caveat.
- `manual_only`: not suitable for automated CLI-only evidence.

`log_status` values:

- `NOT_STARTED`: no current log evidence.
- `PLAN_READY`: scope is planned but not log-smoked.
- `TESTED_NON_ROM`: ROM-free test or harness evidence only.
- `PASS_LOG`: local log smoke passed in sanitized evidence.
- `PASS_LOG_WITH_CAVEAT`: local log smoke passed, but the row has a known caveat.
- `FAIL`: unexpected current failure.
- `EXPECTED_FAIL`: known blocked/risky profile until fixed.
- `OUT_OF_SCOPE`: deliberately excluded from the current matrix.

`ingame_status` values:

- `NOT_STARTED`: no ingame evidence.
- `NEEDS_INGAME_SMOKE`: log-level evidence exists, but a local play/visual check is still needed.
- `PASS_INGAME_SMOKE`: a sanitized local ingame smoke exists for this feature path.
- `MANUAL_ONLY`: evidence requires manual local inspection.
- `OUT_OF_SCOPE`: excluded from current smoke scope.

## CLI Profile Link

The `test_profile_id` column maps each feature to the profile IDs in `cli_profile_matrix.example.tsv`.

Current profile IDs:

- `00_baseline`
- `01_traits_full`
- `02_starters_statics_trades_full`
- `03_moves_movesets_full`
- `04_foe_base`
- `04_foe_held_items_basic`
- `05_wild_full`
- `06_tm_tutor_full`
- `07_items_full`
- `08_types_full`
- `09_graphics_palettes`
- `10_misc_tweaks`

`11_special_wild` now maps to `FVX-SPECIAL-WILD-001` (Use Time-Based Encounters). The source overlay and existing runner case establish a test intent, not support for CFRU Day/Night/Swarms. Target-normalized-away flags do not count as tested. `04_foe_held_items_sensible_expected_fail` maps to the new `FVX-FOE-SENSIBLE-HELD-ITEMS` row; it remains an unresolved diagnostic, not a positive PASS or an accepted unsupported product choice.

## Historical Caveats Captured — Legacy Revisions Only

The following statements and the original 130 TSV rows retain their historical
revision-scoped evidence: 99 `PASS_LOG`, 26 `PASS_LOG_WITH_CAVEAT`, four
`OUT_OF_SCOPE`, one `NOT_STARTED`. None is promoted to acceptance of CFRU #77
`e27e2113e4d59dc76cf5da8d4c43b067addae348`, DPE
`d887185de1f6ae6a78e85c4311bbadde17041d00` or UPR-FVX #217
`f979c3c6ec4d32a92ecf632a3d9d38151d5cb19c`. The two new rows have
`NOT_STARTED` for log and gameplay; source inventory is not execution evidence.

- Generated `.rnqs` CLI profile matrix passed log smoke for all 14 profiles with 0 bad markers and 0 warnings.
- Pokemon Traits tab is marked log-passed, including Evolutions and subsettings.
- Hard Evolution combinations are marked with constraint/fallback caveats.
- Starters, Statics and Trades are marked log-passed; Oak-Lab Rival sync has ingame smoke for `FVX-SST-002`.
- Static null placeholder entries remain null.
- Starter Held Items are marked log-passed.
- In-Game Trades Species/Nickname-visible path is marked log-passed; no `NEW GIVEN = ?` is recorded in the sanitized evidence.
- Moves and Movesets are marked log-passed.
- `Update Moves to Generation` is `OUT_OF_SCOPE` by design for the CFRU/DPE Gen9 basis.
- Foe base is marked log-passed.
- Trainer Class Names remains textlabel-only.
- Trainer Held Items basic is log-passed. The generated Sensible Items profile also log-passed; the prior `getSensibleHeldItemsFor` NPE was not reproduced there, but the interaction remains caveated until a focused isolation run.
- Trainer `Don't Use Legendaries` carries an expanded-pool caveat on the Trainer Pokemon base row.
- Special-Wild generated profile log-passed, but Special-Wild/Day-Night/Swarms remain a separate scope.
- Palettes/Graphics generated profile log-passed, but ingame visual smoke remains required; Custom Player Graphics remains P2/out-of-scope.
- Misc Tweaks generated profile log-passed, but behavior-specific ingame/manual smoke remains required.
- No P1 promotion is made by this matrix.

## Updating Rows

When a new local run is reported:

1. Identify the profile ID and affected feature IDs.
2. Update only the affected TSV rows.
3. Use `PASS_LOG` only when the sanitized CLI/log report passed with no blocking markers.
4. Use `PASS_LOG_WITH_CAVEAT` when the log passed but the feature has a known scoped limitation.
5. Move `ingame_status` to `PASS_INGAME_SMOKE` only when the user reports sanitized local ingame evidence for that specific path.
6. Keep `known_caveat`, `blocker`, `evidence` and `next_step` concise and free of private data.

Do not put these into the TSV:

- ROM paths.
- Output ROM paths.
- ROM hashes or file hashes.
- Full logs or stack traces.
- Screenshots.
- Save files or emulator states.
- Private local paths.
- Secrets, tokens or `.env` values.

## Validation

Expected invariants:

- 132 feature rows after the header; all 130 historical rows preserved byte-for-byte.
- No duplicate `feature_id` values.
- Every `Feature-ID` in `fvx-progress-dashboard.md` appears in the TSV.
- The dashboard's full feature list must not be shortened or replaced by this TSV.

## #727 Candidate Runner Handoff — Source Only

The runner pins Workspace basis `9411c39f472d1d08555be988d2f7ab9482902580`
separately from the three candidate sources above. Workspace Gitlinks stay
unchanged. It inspects root Git objects/index only, ignores existing component
worktrees and untracked local diagnostics, and never fetches/checks out/cleans
them. Overlay text is loaded from the exact public GitHub commit and checked
against its public Git blob ID. An optional `--public-source-file` must be
identical public `SettingsProfileGenerator.java`, outside component/protected
paths; dirty checkout source is never the fallback.

The source plan has 159 catalogue IDs, four generator-unsupported IDs, nine
target exclusions and 146 single-overlay intents subject to effective-option
preflight. A requested option is not positive coverage unless it survives
Settings round-trip and target normalization. Six new positive
intents comprise the four separate `FVX-TRAIT-027`, `FVX-ITEM-010`,
`FVX-GFX-002`, `FVX-GFX-004` singles and the two named compositions:

- `CANDIDATE_EVOLUTION_TARGET_LINKED`: Limit all Gen1–9 with evolutionary
  relatives **ON**, RANDOM evolutions, Change Impossible + Estimated Levels +
  Remove Time-Based, Make Easier **OFF** (`016+024+026+027`).
- `CANDIDATE_PICKUP_SHOP`: `FVX-ITEM-010 + FVX-ITEM-006`.

These leaves are not added to safe FULL/family/MAX bundles. Existing selected
Control/Casual/IronMON identities, no-relatives routes, 66 family pairs, 12
triples, canonical Settings deduplication and fixed-seed/JVM replay remain.
The resulting plan contains 303 intents before actual Settings deduplication.
All six risk intents use the established fixed seed set and same-seed replay.

`GFX-002+GFX-004` is rejected before overrides, serialization or runtime;
`TRAIT-025` remains excluded pending independent `OWNERSHIP_WITNESS_V1`.
This runner does not accept or synthesize that witness. RANDOM_EVERY_LEVEL,
disallowed Mega/GMax/mechanic-item modes and duplicate UPR Reusable TMs remain
outside mandatory positive cases.

Public/mock checks (no Java, Gradle, JAR or ROM execution):

```sh
python3 -B -m unittest discover -s 07_scripts/randomizer/tests -p test_upr_generation_matrix.py
```

Tests load immutable public source fixtures in memory, then mock subprocesses
and use synthetic temporary bytes. The source plan alone is available with
`python3 07_scripts/randomizer/upr_generation_matrix.py --dry-run`.

**Later USER-only execution, only after explicit CONTROL re-review authorization**,
with independently attested existing PR-#217
JAR; no automatic JAR build, binary inspection or copy:

```sh
python3 07_scripts/randomizer/upr_generation_matrix.py \
  --jar "$PR217_JAR" \
  --jar-source-commit f979c3c6ec4d32a92ecf632a3d9d38151d5cb19c \
  --stop-on-fail
```

The path stays user-local. A filename/version cannot prove provenance:
attestation is required, and the supplied JAR's feature/profile CLI catalogue
must match exact public source before input is requested. Source check,
Settings round-trip, actual normalized risk-option state, generation,
supported-profile reopen, deterministic replay and input-unchanged checks
remain distinct. Lost Gen1–9/relative flags stop the requested high-risk case
with `STOP/NOT_RUN`; they are never substituted by no-relatives semantics.

### CONTROL repair: effective coverage and partial execution

The temporary adapter observes actual Settings getters after serialization
and after `tweakForRom`. The bounded preflight checks all six risk intents,
every requested Gen-limit case and every `UseTimeBasedEncounters=ON` intent,
including the Special-Wild single, FULL, family pairs and MAX composition.
Source/round-trip, malformed observation/witness, selected-profile identity
and safety failures still STOP the run.

Exact #217 `AbstractRomHandler.hasTimeBasedEncounters()` defaults to false;
Gen3 does not override it, so `Settings.tweakForRom` disables time encounters.
An observed ON→OFF transition is
`TIME_BASED_ENCOUNTERS_NORMALIZED_OFF / NOT_RUN`. All affected compositions
remain visible in the plan and report but cannot receive FULL/MAX PASS.
This is no activation or support claim for CFRU Day/Night/Swarms. The ledger
row stays `NOT_STARTED`.

Gen3's original-ROM validity check can remove generation restrictions on the
patched target. After validated normalization accounting, unavailable requested
Gen-limit/relative coverage is isolated as
`GEN_LIMIT_OR_RELATIVES_NOT_EFFECTIVE / NOT_RUN`; the named evolution risk
additionally reports `STOP/NOT_RUN`. Other observed risk-option losses also
block that risk before execution. No flag is forced back ON, no CRC rule is
bypassed and no source-owned normalization behavior is changed. The established
exact C/I disposition for the witnessed no-relatives Gen-limit delta remains;
that limited disposition does not accept any other normalized Gen-limit case.

Blocked intents are removed **before** canonical Settings deduplication.
They cannot inherit PASS from an identical effective core payload. Original
temporary settings-file indices are preserved. Independent eligible groups
run first, followed by eligible risks; both retain existing primary/replay and
fixed-seed rules. Blocked risks do not suppress independent generation,
technical reopen or replay evidence, including with `--stop-on-fail`.

A full result requires every mandatory intent and its planned seeds/replays.
Any blocked, unexecuted or incomplete mandatory intent yields
`R2_RANDOMIZER_GENERATION_MATRIX_PARTIAL_NOT_RUN` and exit code 1, even when
all executed cases pass. An executed mandatory failure yields MATRIX_FAIL.
Only complete positive coverage can yield MATRIX_PASS. Reports distinguish
executed effective-case counts from requested-intent PASS/FAIL/NOT_RUN and list
each blocked intent with reason and generation/reopen/replay NOT_RUN.
Partial evidence never establishes a full matrix or runtime PASS.

Only USER execution opens input/output or invokes the JAR. Temporary outputs,
adapters and manifests are deleted after success, failure or interruption;
private input comparison values remain transient and unreported. Reports
suppress paths, settings strings, raw stack traces, seeds and binary hashes.

Reopen currently proves supported loader identity and successful manifest
export. **Log-content quality, manifest semantic consistency and manual
gameplay remain NOT_RUN**; this patch adds no logger/source-owner repairs or
runtime feature PASS. Existing user-supplied broad generation/log evidence
under #727 remains separately scoped. Codex does not execute the private ROM
matrix, access the candidate JAR, merge PRs or update component Gitlinks.
