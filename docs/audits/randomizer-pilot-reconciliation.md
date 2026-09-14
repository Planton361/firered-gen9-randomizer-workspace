# Current pilot randomizer reconciliation

Date: 2026-09-15. Evidence: current source/static plus the named synthetic test.
No ROM fixture, output, emulator, save, state or existing build was accessed.

Workspace baseline `7437cd551545ab5e4dcd57a2ff5dbf9672193d74`; CFRU
`827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec`; DPE
`22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`; UPR-FVX
`1a597a667129b50284dd88afb231372b5bd01d7f`. Fetched UPR compatibility head
equals the pin. Separate source and documentation worktrees; no Gitlink changes.

## Result

Draft compatibility fix: [UPR-FVX #185](https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/185),
candidate `0df4ed3d83fba6176f19a3c3146bd3c27561e47e`.

One concrete incompatibility was confirmed: the Pickup reader/writer targets
the vanilla FRLG table, whereas CFRU's active battle command selects from
separate common/rare arrays by level. A bounded UPR guard rejects Pickup
randomization before table access or mutation, with instructions to select
Unchanged. This preserves the engine's existing Pickup behavior. The existing
GUI still displays the choice; selecting Random fails explicitly. It cannot
silently emit a misleading successful Pickup result.

Historical [Working Settings Matrix](../../08_tests/randomizer/190_gui_working_settings_matrix.md)
was at UPR `f3a6d04f`, not the current pin. Its GUI/log observations are supporting
evidence, not runtime verification of current writers. In particular its
Pickup log pass does not prove changes to the active CFRU arrays. The old
starter/rival blocker also predates the current source's dedicated Lab script
reader/writer and GameRandomizer synchronization path; their final pilot
runtime result remains to be obtained.

`PASS_STATIC` means the inspected source contract agrees, not that integration
ran. `PASS_WITH_CAVEAT` means a useful bounded path exists with the stated
limitation. Every enabled row still needs final randomized-output smoke.
`DISABLED_BY_DESIGN` describes the approved pilot profile/guard, not absent
engine behavior. `NOT_APPLICABLE` is for systems outside FireRed's model.

## Feature matrix

All UPR method references below are in
[pinned Gen3RomHandler](https://github.com/Planton361/universal-pokemon-randomizer-fvx/blob/1a597a667129b50284dd88afb231372b5bd01d7f/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java)
unless another file is named. Inspected randomizers are in `random/.../randomizers`.

| Feature | Classification | Current source evidence / practical boundary |
|---|---|---|
| Wild Pokemon | PASS_WITH_CAVEAT | `getEncounters` / `setEncounters` L3959/4289 share 20-byte headers, deduplicate slot pointers and use internal species IDs. Standard/Fallback only; day/night, swarm, DexNav and other special sources are outside this writer. CFRU SWARM_CHANCE is 0. |
| Trainers | PASS_WITH_CAVEAT | `loadTrainers`, `trainerPokemonToBytes`, stride helpers: party flags 0/2 use 8-byte rows, 1 uses 16, 3 uses CFRU 32-byte rows. Ability/nature, six IV/EV bytes, item at 20 and moves at 22 match `include/battle.h`. Writer normalizes IV spread from its scalar IV model and sets teraType to 0; this is not lossless metadata preservation. Trainer class text is independent of sprite selection. |
| Pokemon movesets | PASS_WITH_CAVEAT | Runtime pointer at 0x43E20 takes precedence over DPE fallback. `getCfruDpeMovesLearnt` / `setCfruDpeMovesLearnt`: internal species identity, 3-byte little-endian move+level, 00 00 FF terminator, max 50 entries, aligned deduplicated blobs. Fixed free-space window 0x1219A48..0x1600000 still needs candidate insertion/output validation. Task 3 subsequently found five empty source learnsets; its CFRU restoration is a data prerequisite for those families. |
| Trainer movesets | PASS_WITH_CAVEAT | Reset/custom paths normalize to four moves; level-derived moves use current learnsets. CFRU custom rows carry their own moves. Exercise a rival, ordinary and late custom trainer. |
| Abilities | PASS_WITH_CAVEAT | Three byte slots at BaseStats 0x16/0x17/0x1A; highest ID 0xFE matches CFRU. SpeciesAbilityRandomizer skips invalid/empty species entries. Local IDs/names and shared aliases are engine semantics, not universal modern ability behavior. Global ability ban/duplicate options must remain caveated where generic semantic IDs differ from local engine IDs. |
| TM/HM moves | PASS_STATIC | `getTMMoves`/`getHMMoves`/`writeCfruDpeTMMoves`: 120 TMs + 8 HMs, pointer 0x125A8C, u16 moves. TM writer modifies only the first 120; HM list is preserved. |
| TM/HM compatibility | PASS_STATIC | 16 bytes per internal species, 129 boolean positions with index 0 unused; target pointer 0x43C68. Matches CFRU 128 slots. HM convenience still requires item, compatible party member, badge/location. |
| Tutors | PASS_WITH_CAVEAT | CFRU branch uses 152 moves, 19 compatibility bytes, pointers 0x120BE4 / 0x120C30, internal identity. Exact move count/valid IDs checked. Script dialogue is not generically rewritten on this branch; actual teaching/display needs smoke. |
| Shops | PASS_WITH_CAVEAT | `getShops`/`setShops` follow configured pointer lists, u16 item IDs and zero terminator; DataRewriter handles resizing. Coverage is configured shops, not every runtime vendor. M-013 rewards follow purchased item pocket and need no UPR writer change. |
| Pickup | DISABLED_BY_DESIGN | Candidate rejects get/set before access for recognized CFRU/DPE; keep Pickup Unchanged. Existing source has a concrete wrong-runtime-table gap, described below. |
| In-game trades | PASS_WITH_CAVEAT | 60-byte rows; given/requested species at 12/56 use SpeciesSet identity for extended BPRE; null/placeholder checks prevent invalid writes. Held items/names/IVs retained through the existing model. Trade completion and offered/requested display need smoke. |
| Static Pokemon | PASS_WITH_CAVEAT | `StaticPokemon.setPokemon` preserves null species, internal identity path present; writer keeps configured linked/roamer/ghost branches. This does not prove all configured script offsets remain active after overlays. |
| Type Effectiveness | PASS_WITH_CAVEAT | Fairy 0x17 translation; unsupported chart entries preserved; capacity checked before writes. Dense/chaos combinations can exceed fixed capacity and must fail, not overrun. Keep Unchanged for initial playthrough. |
| Base Stats | PASS_STATIC | Six u8 stats at offsets 0..5; target `BaseStats` stride 28, normal/hidden ability offsets agree. No new battle mechanic is inferred from randomized stats. |
| Move Data | PASS_WITH_CAVEAT | 12-byte move rows; core fields 0..4, CFRU category at 10; Fairy 0x17; unmanaged bytes retained. Names use bounded target lengths. Move effects retain CFRU semantics; power/type/name changes do not port modern mechanics. |
| Field items | PASS_WITH_CAVEAT | `preprocessMaps` reads visible scripts and hidden BG events; `getFieldItems`/`setFieldItems` share the same eligible-slot predicate, explicitly including CFRU TMs without adding TMs to normal pools. Key/HM/progression exclusions retained. M-005 Lab Potion is a normal finditem slot; M-004 renewals reuse hidden slots. |
| M-001 visible TM/HM items | PASS_STATIC | Object graphic read uses the low byte at object+1; 0x065C retains 0x5C. It still discovers the same scripts. Item ID/pool semantics, not gold appearance, determine eligibility; HM07 remains excluded from random ordinary items. 29 graphics are not 29 eligible TM slots (28 TMs + one HM). |
| Expanded species/forms | PASS_WITH_CAVEAT | Internal SpeciesSet identities and generation metadata, placeholder/egg/asset guards; 0..1439 table. Real forms are not uniformly equivalent to free-standing encounters. Keep form/asset restrictions; do not turn missing transition mechanics into engine work. |
| Gen1–9 bounds | PASS_STATIC | Species count 1440, last Pecharunt 1439; move count 992 entries; TM/HM 128, tutor 152, ability 0..254. Runtime-pointer and last-entry bounds exist. Detection is structural/heuristic, not an exact revision signature. |
| Output writers | NEEDS_FINAL_RUNTIME_SMOKE | `GameRandomizer` applies settings then saves; internal-ID writers, capacity checks and pointer logic reviewed. Fresh load→randomize→save→reload→gameplay is still required; static agreement cannot establish successful private insertion or all option interactions. |
| Logging | PASS_WITH_CAVEAT | `RandomizationLogger` reports chosen settings/seed and feature sections; Field Items explicitly lack detailed proper logging; ability-name width and semantic aliases remain caveats. Pickup guard fails before ItemRandomizer marks changes/log success. A log is not proof of runtime table usage. |
| Special Wild randomization | DISABLED_BY_DESIGN | Standard/Fallback scope only; do not enable or add new CFRU mechanics. |
| Totem systems / non-Gen3 handlers | NOT_APPLICABLE | Outside the selected BPRE pilot. |
| Starter/rival transition | NEEDS_FINAL_RUNTIME_SMOKE | Current source has Lab script synchronization and corresponding synthetic tests. Historical matrix's unresolved label is not a current-code finding; exercise it with M-006/M-007 flow. |

## Pickup defect and minimal fix

[CFRU battle command table](https://github.com/Planton361/CFRU-expansion/blob/827fa1ef04bd43e5c6bad5c47f7d8690ea6823ec/assembly/data/battle_script_commands_table.s#L246)
binds `atkE5_pickupitemcalculation`. It calls `ChoosePickupItem(level)` in
`src/general_bs_commands.c:5389`, which uses the 18-entry `sPickupCommonItems`
and 11-entry `sPickupRareItems` from `src/Tables/item_tables.c`, sliding by
(level-1)/10 with separate u32 probability ceilings. UPR's FRLG path reads
16 four-byte entries, derives vanilla probabilities and searches a legacy
locator/metadata pattern. Its alternate search does not bind either active
CFRU array. Therefore a changed log/table is insufficient and can be misleading.

Fix is only an early guard on both Pickup entry points, including empty writes.
It makes no guessed pointer or source-pattern rewrite and no CFRU change.
The exception tells GUI/CLI users to set Pickup Unchanged. A future small
UPR milestone can expose the actual arrays through a source-owned revision
profile and test 10 level brackets; that work is not silently included here.

## Checks and gates

- New ROM-free JUnit regression: both entry points reject before any loaded
  ROM metadata exists; exact actionable diagnostic asserted.
- `python3 romio/src/test/host/check_cfru_dpe_pickup_guard.py`: PASS using
  the actual Java get/set/guard bodies with synthetic services. Both read,
  empty write and nonempty write rejected before table access/mutation;
  vanilla 16-entry reads/writes and all ten probability sums preserved.
- `git diff --check`: PASS. Workspace safety: PASS before and after.
- Attempted `gradle :romio:test --tests '*Gen3CfruDpePickupGuardTest' :romio:build`:
  BLOCKED, Gradle command absent. Installed Java reports 23.0.1; source asks
  for Java 25. Wrapper/tool binaries were excluded and not fetched/requested.
  Full module build and JUnit execution are NOT claimed. Existing source tests
  inspected, not counted as new passes. Root Gradle `ignoreFailures=true`
  means a later build exit code alone cannot certify tests; inspect failures,
  errors and skips in its test summary.
- No supported feature receives a full runtime PASS in this report. Repeat
  the final acceptance package with exact candidate/settings and sanitized
  results. Keep Pickup Unchanged; intentionally test rejection once.

This is a bounded source review of every listed feature family, not an
exhaustive combination fuzzing campaign or a general support certification.
