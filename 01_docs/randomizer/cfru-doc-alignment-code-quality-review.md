# CFRU Doc Alignment and FVX Code Quality Review

Stand: 2026-05-21

Scope: documentation-only review of the current UPR-FVX CFRU/DPE compatibility approach. No ROMs
were read, copied, generated or tested by Codex. No builds were run. No UPR-FVX, CFRU or DPE code was
changed. The local CFRU documentation reference was `02_external/CFRU-expansion/CFRU Documentation.pdf`.

## 1. Executive Summary

The current compatibility approach is broadly aligned with the CFRU documentation: FVX is treating the
built ROM as the source of truth, using `romEntry` pointers and fixed CFRU/DPE pointer locations where
the final build exposes them, while leaving runtime/script-only systems caveated. That matches the key
CFRU model: CFRU/DPE source files and config flags compile into final ROM tables, then the randomizer
must read/write those final tables rather than editing source files.

Confirmed assumptions:

- DPE should be inserted before CFRU; the project model of "DPE/CFRU source -> build -> final ROM table"
  is correct.
- `src/config.h` controls major CFRU behavior relevant to randomizer compatibility, including expanded
  TMs/HMs, move tutors, `EVOS_PER_MON`, time systems, trainer EV support, save expansion and moveset
  expansion behavior.
- CFRU docs and local source both support the key TM/HM constants used by FVX: 120 TMs, 8 HMs, 16
  compatibility bytes, and pointer locations for `gTMHMMoves` / `gTMHMLearnsets`.
- CFRU docs confirm that runtime/special systems such as Time-of-Day wild, swarms, DexNav and raids are
  not the same thing as the standard Gen3 `gWildMonHeaders` table.
- Hidden Abilities are stored in the base-stats structure, so treating ability correctness as tied to
  `gBaseStats` / SpeciesInfo is correct.

Not yet proven:

- The active built-ROM source/pointer chain for every table is not fully verified without a ROM/pointer
  audit. This is especially important for learnsets, TM/Tutor widths, trainer runtime rows and palettes.
- Targeted local smokes do not prove full playthrough behavior, full trainer coverage, shiny palette
  coverage, full type matchup coverage or held-item distribution quality.
- The current main-branch implementation report does not contain a standalone Source-to-ROM-Table-Map
  chapter. The decision matrix repeats the needed map points, so the information exists, but its
  documented location is inconsistent with the earlier follow-up request.

Clean code areas:

- `RestrictedSpeciesService` plus special-form predicates: policy is centralized enough to review.
- `ItemMechanicPredicates` / `CfruDpeItemCategories`: source-backed category checks are a good fit for
  Mega/Z/Dynamax-GMax item filtering.
- `TrainerClassSpriteSyncRandomizer`: opt-in behavior, explicit settings path and clear target mapping.
- Runtime trainer source handling: strict validation and audit-first expansion are appropriate.

Effective but refactor-worthy areas:

- `Gen3RomHandler` has accumulated many CFRU/DPE-specific responsibilities: pointer discovery, runtime
  trainer source sync, learnset repointing, intro visual source writes, palette output writes, misc patch
  detection and diagnostics. It is effective, but a no-behavior-change split into small CFRU/DPE table
  adapters would reduce review risk.
- Logging fallback and audit/report formatting are useful but scattered enough to deserve helper
  extraction later.

## 2. CFRU-Doku-Abgleich

| CFRU-Doku-Thema | Doku-Aussage | Unser Verstaendnis / Mapping | FVX-Codepfad | Bewertung | Risiko / offene Frage |
| --- | --- | --- | --- | --- | --- |
| DPE-before-CFRU / Insert-Reihenfolge | CFRU setup recommends adding DPE first, then CFRU at the planned offset and treating the resulting ROM as the base for test builds. | Correct: FVX should not edit CFRU/DPE source; it must read/write the final built ROM tables. | `Gen3RomHandler` reads ROM pointers into `romEntry` in `addGen3ExpandedRomEntryPointers()` and related setup. | CONFIRMED_BY_CFRU_DOC | No code issue. Pointer verification still needs built ROM evidence. |
| `src/config.h` as central config | CFRU docs and local `src/config.h` define expanded TM/HM, tutors, `EVOS_PER_MON`, `TIME_ENABLED`, `TRAINERS_WITH_EVS`, `SAVE_BLOCK_EXPANSION`, `EXPAND_MOVESETS`, `REUSABLE_TMS`. | Correct: config flags explain table widths and runtime systems that FVX must not assume from vanilla Gen3. | `Gen3RomHandler` constants for CFRU/DPE counts; `GameRandomizer` settings gates; misc tweak caveats. | CONFIRMED_BY_CFRU_DOC | FVX cannot infer every compile flag perfectly without ROM/source-specific verification. |
| `EXPAND_MOVESETS` vs DPE learnsets | CFRU says `EXPAND_MOVESETS` uses CFRU learnsets, and should be commented when using DPE-created learnsets. Local `src/config.h` currently defines it. | Existing docs correctly caveat active learnset source as source/pointer verification required. | `getMovesLearnt()`, `setMovesLearnt()`, `getCfruDpeLevelUpLearnsetsOffset()`, `getRuntimeLevelUpLearnsetsOffset()`. | PARTIALLY_CONFIRMED | Possible mismatch: local CFRU config has `EXPAND_MOVESETS` defined while DPE learnsets are also present. Needs source/pointer review, not data correction. |
| `gLevelUpLearnsets` / learnset table | CFRU docs list `gLevelUpLearnsets`; CFRU source can read runtime pointer `0x8043E20`; DPE repointall lists `gLevelUpLearnsets 0803EA7C`. | Correct to treat final pointer as decisive; source file can be CFRU or DPE depending build. | `Gen3RomHandler.getMovesLearnt()`, `setMovesLearnt()`, learnset diagnostics and repoint allocation. | CONFIRMED_BY_CFRU_DOC | Active final table must be verified locally before stronger support claim. |
| `gBaseStats` / SpeciesInfo / Hidden Abilities | CFRU docs say Hidden Abilities live in byte `0x1A` of the base-stats structure. Local CFRU linker aliases `gSpeciesInfo` to the `gBaseStats` address. | Correct: BaseStats / SpeciesInfo / Abilities are one compatibility surface, while value correctness is data quality. | `loadSpeciesStats()`, `saveSpeciesStats()`, `SpeciesAbilityRandomizer`, `RestrictedSpeciesService`. | CONFIRMED_BY_CFRU_DOC | Ability values/names may still need later data-quality audit. |
| `gBattleMoves` / Move Data | CFRU Table Compendium lists `gBattleMoves` in `src/tables/battle_moves.c`; local CFRU code consumes extra fields such as split and Z/Max effect data. | Correct to map FVX `MoveData` to final `gBattleMoves`, but extra CFRU fields remain caveated. | `getMoves()`, `setMoves()`, `writeGen3BattleMoveData()`, move updaters/randomizers. | PARTIALLY_CONFIRMED | FVX writes known fields; full CFRU extra-field behavior is not proven by log-smoke alone. |
| TM/HM Expansion | CFRU docs define `EXPANDED_TMSHMS`, `NUM_TMS`, `NUM_HMS`, `gTMHMMoves`, and 16-byte compatibility width. Local config: `NUM_TMS 120`, `NUM_HMS 8`. | Correct: FVX constants match the local CFRU/DPE setup and the decision matrix caveat. | `getTMMoves()`, `setTMMoves()`, `getTMHMCompatibility()`, `setTMHMCompatibility()`. | CONFIRMED_BY_CFRU_DOC | Needs final ROM pointer and duplicate-write verification for stronger claim. |
| Move Tutor Expansion | CFRU docs define `EXPANDED_MOVE_TUTORS`, `NUM_MOVE_TUTORS`, `LAST_TOTAL_TUTOR_NUM`; special tutors extend beyond normal tutor count. Local config uses 152 and 161. | Mostly correct: FVX models 152 normal tutor entries and 19 bytes compatibility. Special tutor/text/menu behavior remains out of scope. | `getMoveTutorMoves()`, `setMoveTutorMoves()`, `getMoveTutorCompatibility()`, `setMoveTutorCompatibility()`. | PARTIALLY_CONFIRMED | CFRU doc says DPE examples may use different tutor counts; verify local final pointer/count before support wording. |
| Item Defines / Item Tables / Pickup / Fling / item sorting | CFRU docs list `sPickupCommonItems`, `sPickupRareItems`, `gFlingTable`, `gItemsByType`; reusable TMs affect item behavior. | Correct to keep item randomization caveated by source class and not assume all static/gift/NPC items flow through one pool. | `ItemRandomizer`, `ItemMechanicPredicates`, `CfruDpeItemCategories`, pickup/item handlers. | CONFIRMED_BY_CFRU_DOC | Static/gift/NPC item sources still need mapping if leaks appear. |
| Trainer data / Trainer parties / Trainers with EVs | CFRU config supports `TRAINERS_WITH_EVS`; local trainer runtime source work uses final TrainerData rows plus script references. | Correct: normal loaded trainer list and FRLG runtime script rows are separate compatibility surfaces. | `loadTrainers()`, `saveTrainers()`, `findFrlgTrainerBattleRuntimeSources()`, `loadFrlgRuntimeTrainerSourceRows()`, `TrainerPokemonRandomizer`. | PARTIALLY_CONFIRMED | EV trainer structure interaction is not globally reviewed; loaded-mismatch/invalid rows remain open. |
| Trainer Class Poke Balls | CFRU Table Compendium lists class-based Poke Ball tables; local source has class-based trainer encounter/music and ball tables. | Not currently treated as a randomizer-controlled feature; relevant only as a potential trainer-class side effect. | Trainer class/name/sprite paths do not intentionally edit Poke Ball class tables. | NOT_COVERED_BY_CURRENT_SCOPE | If trainer class IDs change, CFRU class-based auxiliary behavior may change too. This should be caveated, not guessed. |
| Time-of-Day Wild / Swarms / DexNav / Raids | CFRU docs describe separate Time-of-Day wild headers, swarm table, DexNav and raid encounter sources. | Correct: standard FVX wild table support must not be promoted to special/runtime wild support. | `getEncounters(false)`, `setEncounters(...)`, Wild Base-vs-Output audit; no modeled special-wild writer. | CONFIRMED_BY_CFRU_DOC | Ingame divergence requires separate source-specific audit. |
| Mega / Primal / Ultra Burst / Gigantamax evolution setup | CFRU docs place these mechanics in evolution methods/items and DPE evolution table setup. | Correct to keep special-form filtering and mechanic item filtering separate from generic species/item metadata. | `RestrictedSpeciesService`, `SpecialFormPredicates`, `CfruDpeItemCategories`, `ItemMechanicPredicates`, evolution handling. | CONFIRMED_BY_CFRU_DOC | Custom/future encodings can bypass current classifiers. |
| Z-Move setup and `sSpecialZMoveTable` | CFRU docs list signature Z moves in `src/set_z_effect.c`; Table Compendium includes `sSpecialZMoveTable`. | Correct: Z crystals are mechanic items; signature Z move behavior is engine-specific and not a generic FVX item/move claim. | `ItemMechanicPredicates`, `CfruDpeItemCategories`, trainer held item guards. | CONFIRMED_BY_CFRU_DOC | No full special-Z table compatibility audit. |
| Hidden Abilities storage | CFRU docs state hidden abilities are in base-stats byte `0x1A`. | Correct: ability randomization affects base stats; bad ability values are data-quality scope. | `loadSpeciesStats()`, `saveSpeciesStats()`, `SpeciesAbilityRandomizer`. | CONFIRMED_BY_CFRU_DOC | Hidden ability runtime display/use still needs ingame proof for stronger claim. |
| Save Block Expansion / flags / vars | CFRU docs say Save Expansion adds flags, vars, PC boxes, roamers and bag capacity; local config keeps it defined. | Correctly out of current randomizer-write scope except where scripts/runtime systems depend on it. | No direct FVX table writer reviewed. | OUT_OF_SCOPE | Do not let FVX docs imply save-system support beyond not touching it. |
| Reusable TMs / Forgettable HMs / HM-use behavior | CFRU docs provide reusable TM behavior through config and item Mystery byte; workspace docs say stable profile should not duplicate CFRU behavior in FVX. | Correct: treat CFRU-provided behavior as profile caveat, not UPR-FVX compatibility proof. | `MiscTweakRandomizer`, `ItemRandomizer`, dashboard/TSV caveats. | CONFIRMED_BY_CFRU_DOC | If FVX reusable TM tweak is enabled, it needs a separate CFRU-specific smoke. |
| Dynamic palettes / DNS / palette tables | CFRU docs discuss dynamic overworld/battle fading; DPE/CFRU source exposes Pokemon palette pointer tables separately. | Correct to limit current Graphics/Palettes claim to Pokemon normal/shiny palette tables, not DNS/OW dynamic palettes. | `loadPokemonPalettes()`, `savePokemonPalettes()`, palette audit tests. | PARTIALLY_CONFIRMED | Shiny coverage and DNS/overworld palettes remain separate. |
| Table Compendium entries relevant to map | CFRU docs list `gBattleMoves`, `gTypeEffectiveness`, pickup/Fling/item tables, `gLevelUpLearnsets`, `sSpecialZMoveTable`; DPE source confirms `gBaseStats`, `gEvolutionTable`, TM/Tutor and sprite/palette tables. | Source-to-ROM map is directionally correct. | Decision matrix map plus `Gen3RomHandler` table paths. | PARTIALLY_CONFIRMED | Report file lacks standalone map chapter; final pointer proof still local-only. |

## 3. Source-to-ROM-Map Review

Status vocabulary: `CONFIRMED_BY_CFRU_DOC`, `PARTIALLY_CONFIRMED`,
`NEEDS_LOCAL_POINTER_VERIFICATION`, `DOC_MISMATCH`, `NOT_COVERED_BY_CFRU_DOC`.

| Mapping | Report / Matrix state | CFRU-doc review | Code path | Status | Note |
| --- | --- | --- | --- | --- | --- |
| BaseStats / Abilities | Matrix maps DPE `Base_Stats.c` and CFRU `gBaseStats` / `gSpeciesInfo`. | Hidden Ability storage in base stats is confirmed. | `loadSpeciesStats()`, `saveSpeciesStats()`. | CONFIRMED_BY_CFRU_DOC | Values are later data-quality scope. |
| Level-Up Learnsets | Matrix maps DPE `Learnsets.c`, CFRU `level_up_learnsets.c`, final `gLevelUpLearnsets`. | CFRU doc confirms both CFRU and DPE learnset decision point. | `getMovesLearnt()`, `setMovesLearnt()`. | NEEDS_LOCAL_POINTER_VERIFICATION | Local config has `EXPAND_MOVESETS` defined; verify active final table before support wording. |
| Evolutions | Matrix maps DPE `Evolution Table.c`, final `gEvolutionTable`. | CFRU doc confirms Mega/Primal/Ultra/GMax use evolution methods. | `getEvolutions()`, `setEvolutions()`, `getEvolutionRowOffset()`. | PARTIALLY_CONFIRMED | Method encodings and custom methods stay caveated. |
| Move Data | Matrix maps final `gBattleMoves`. | CFRU Table Compendium confirms `gBattleMoves`; extra CFRU fields exist. | `getMoves()`, `setMoves()`, `writeGen3BattleMoveData()`. | PARTIALLY_CONFIRMED | Field coverage is not full battle-behavior coverage. |
| TM/HM | Matrix maps `gTMHMMoves` / `gTMHMLearnsets` and FVX TM/HM methods. | CFRU docs confirm pointer locations and 16-byte compatibility width. | `getTMMoves()`, `setTMMoves()`, `getTMHMCompatibility()`, `setTMHMCompatibility()`. | CONFIRMED_BY_CFRU_DOC | Still needs local duplicate pointer/write verification. |
| Tutors | Matrix maps `gMoveTutorMoves` / `gTutorLearnsets`. | CFRU docs confirm expanded tutor constants and special tutors. | Move tutor methods in `Gen3RomHandler`. | PARTIALLY_CONFIRMED | Verify `NUM_MOVE_TUTORS` / compatibility width in final build. |
| Items | Matrix maps `gItemData`, pickup/shop/field caveats, mechanic item filters. | CFRU doc confirms pickup/Fling/item type tables and reusable TM behavior. | `ItemRandomizer`, item handlers, mechanic predicates. | PARTIALLY_CONFIRMED | Static script/gift/NPC item sources are not fully source-mapped. |
| Wild | Matrix correctly separates standard/fallback and special wild. | CFRU doc confirms Time-of-Day, swarms, DexNav and raids as special/runtime sources. | `getEncounters(false)`, `setEncounters(...)`, Wild audit. | CONFIRMED_BY_CFRU_DOC | Standard Wild support must remain caveated until ingame smoke. |
| Trainer | Matrix maps `TrainerData`, trainer parties, runtime source sync. | CFRU doc/source confirm trainer data and runtime/script systems but not all row variants. | `loadTrainers()`, `saveTrainers()`, runtime trainer source methods. | PARTIALLY_CONFIRMED | EV trainers and loaded-mismatch/invalid rows remain open. |
| Palettes/Sprites | Matrix maps DPE front/back/normal/shiny palette pointer tables. | CFRU/DPE source confirms Pokemon sprite/palette table pointers; CFRU DNS dynamic palettes are separate. | `loadPokemonPalettes()`, `savePokemonPalettes()`, intro visual writes. | PARTIALLY_CONFIRMED | Normal palette writes targeted-smoked; shiny and DNS/OW palettes not proven. |
| Source-to-ROM chapter location | User-requested source-map chapter was expected in implementation report; current main report has no standalone chapter. Matrix repeats map data. | CFRU docs do not decide document placement. | Documentation only. | DOC_MISMATCH | Fix later by adding/relocating map chapter; no code implication. |

## 4. Code-Sauberkeit / Effektivitaet

| Area | Bewertung | Review |
| --- | --- | --- |
| Scope control | CLEAN_AND_EFFECTIVE | Most fixes are narrow: runtime trainer source sync validates raw rows, intro visual source writes known entries, class/sprite sync is opt-in, mechanic item filters use category predicates. |
| Diagnose before writes | CLEAN_AND_EFFECTIVE | Runtime trainers, Intro Mon, Wild output audit and Palettes all show diagnostic/audit work before or alongside behavior changes. |
| Static table vs runtime/script separation | EFFECTIVE_WITH_CAVEATS | Wild and trainer docs/code now distinguish standard tables from runtime/script sources. Static/gift/NPC items need the same source map discipline if investigated. |
| Internal CFRU/DPE Species IDs | EFFECTIVE_WITH_CAVEATS | `Gen3RomHandler` uses internal species IDs and guards species `0` / Egg. `RestrictedSpeciesService` centralizes form/gen policy. Future/custom encodings remain open. |
| Guard/fallback paths | CLEAN_AND_EFFECTIVE | Invalid species, missing assets, missing sensible item pools and missing move pools are guarded. This reduced NPE/crash class risks without pretending data is correct. |
| GUI/RNQS/settings-profile semantics | CLEAN_AND_EFFECTIVE | `MODE-INTRO-RANDOM`, `MODE-NO-RANDOM-INTRO`, `MODE-TRAINER-CLASS-SPRITE-SYNC`, Gen Limit and special-form overlays are represented in settings/profile tests. |
| Duplication/logging | EFFECTIVE_BUT_REFACTOR_CANDIDATE | Diagnostic logging and safe table access are useful but spread through `Gen3RomHandler` and logger paths. Helper extraction would be no-behavior-change. |
| `Gen3RomHandler` breadth | EFFECTIVE_BUT_REFACTOR_CANDIDATE | The class now handles many CFRU/DPE table families and patch detections. It works, but CFRU/DPE table adapters would make future audits safer. |
| Source/pointer certainty | UNCLEAR_NEEDS_SOURCE_POINTER_VERIFICATION | Log-smoke and source docs do not replace final ROM pointer verification, especially for learnsets, tutors, trainer runtime rows and palette tables. |
| Out-of-scope runtime features | OUT_OF_SCOPE | DexNav, raids, full special wild, save expansion behavior and DNS/OW palette systems are not current FVX support claims. |

No-behavior refactors worth considering later:

- Extract CFRU/DPE table pointer access into a small `Gen3CfruDpeTables` helper.
- Extract runtime trainer source classification/audit formatting from `Gen3RomHandler`.
- Extract palette and intro visual source helpers into a graphics-focused helper.
- Consolidate safe logging fallback helpers so `RandomizationLogger` and RomHandler diagnostics do not duplicate bounds/null handling.
- Keep existing method behavior and tests unchanged during those refactors.

## 5. Feature-spezifische Review-Tabelle

| Feature | CFRU-Doku-Abgleich | Code-Sauberkeit | Effektivitaet | Evidence | Caveat | Empfehlung |
| --- | --- | --- | --- | --- | --- | --- |
| BaseStats / SpeciesInfo / Abilities | CONFIRMED_BY_CFRU_DOC | CLEAN_AND_EFFECTIVE | Effective for table read/write | TSV `FVX-TRAIT-001..015`, dashboard | Data values are separate quality scope | Keep with source/pointer caveat |
| Level-Up Learnsets | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | Effective but pointer-sensitive | TSV `FVX-MOVE-007..011`, `Gen3CfruDpeLearnsetPointerTest` | `EXPAND_MOVESETS` vs DPE source unresolved | Needs source/pointer verification |
| Evolutions | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | Effective for known row model | TSV `FVX-TRAIT-016..027`, evolution tests | Mega/GMax/custom methods caveated | Needs source/pointer verification |
| Move Data | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | Effective for supported fields | TSV `FVX-MOVE-001..005`, move writer tests | Extra CFRU fields not fully covered | Keep with caveats |
| TM/HM | CONFIRMED_BY_CFRU_DOC | CLEAN_AND_EFFECTIVE | Effective for local constants | TSV `FVX-TM-001..008` | Duplicate write/final pointer needs proof | Needs source/pointer verification |
| Tutors | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | Effective for modeled normal tutors | TSV `FVX-TM-009..015` | Special tutors/text/menu out of scope | Needs source/pointer verification |
| Wild Standard/Fallback | CONFIRMED_BY_CFRU_DOC | CLEAN_AND_EFFECTIVE | Auditable standard path | TSV `FVX-WILD-001`, PR #118 | Ingame standard-wild smoke still needed | Needs ingame smoke by Anton |
| Special Wild / Day-Night / Swarms | CONFIRMED_BY_CFRU_DOC | OUT_OF_SCOPE | Not supported by standard writer | Dashboard caveat | Runtime sources can bypass `WildPokemon` | Out of scope |
| Trainer Core | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | Targeted core path works | Evidence 202-204, 208, 212 | Full route/playthrough absent | Keep with caveats |
| Trainer Runtime Source Sync | PARTIALLY_CONFIRMED | CLEAN_AND_EFFECTIVE | Strong targeted fix pattern | PR #100-#106, Evidence 202-204 | Loaded-mismatch/invalid/out-of-range rows open | Keep with caveats |
| Rival Counter-Starter / Oak-Lab Rival | PARTIALLY_CONFIRMED | CLEAN_AND_EFFECTIVE | Effective in sampled path | Evidence 207, 208, 212 | Not all-starter matrix | Keep with caveats |
| Trainer Class Sprite Sync | PARTIALLY_CONFIRMED | CLEAN_AND_EFFECTIVE | Effective opt-in visual sync | Evidence 206, 208, 212; GUI/settings tests | Class-based auxiliary CFRU tables not audited | Keep with caveats |
| Trainer Held Items / Sensible Items | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | NPE class fixed | `Gen3SensibleHeldItemsTest`, `ItemDecisionTest`, Evidence 212 | Distribution audit absent | Keep with caveats |
| Items / Mechanic Filtering | CONFIRMED_BY_CFRU_DOC | CLEAN_AND_EFFECTIVE | Effective for Mega/Z/Dynamax-GMax exclusion | `ItemMechanicPredicatesTest`, Evidence 212 | Static/gift/NPC sources open | Keep with caveats |
| Gen Limit 1-9 | NOT_COVERED_BY_CFRU_DOC | CLEAN_AND_EFFECTIVE | Effective in targeted smoke | Evidence 212, settings profile tests | Custom/future forms open | Keep with caveats |
| Special Form Filtering | CONFIRMED_BY_CFRU_DOC | CLEAN_AND_EFFECTIVE | Effective for known categories | `SpecialFormPredicatesTest`, Evidence 212 | Source-backed categories only | Keep with caveats |
| Mechanic Item Filtering | CONFIRMED_BY_CFRU_DOC | CLEAN_AND_EFFECTIVE | Effective for known mechanic items | `ItemMechanicPredicatesTest`, Evidence 212 | Plates/Drives/Memories/Nectars policy separate | Keep with caveats |
| Intro Mon Visual Source | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | Targeted visual mismatch fixed | Evidence 205, 207, 208, 212; intro tests | Other hacks may use other visual sources | Keep with caveats |
| Catching Tutorial | NOT_COVERED_BY_CFRU_DOC | EFFECTIVE_WITH_CAVEATS | Targeted behavior fixed | Evidence 210; `Gen3CatchingTutorialSpeciesMappingTest` | Source location not globally mapped | Keep with caveats |
| Misc Tweaks | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | Targeted behavior smoke passed | Evidence 210; running shoes/fast egg tests | Fast Egg full hatch and Ban Lucky Egg not strong proof | Keep with caveats |
| Type Effectiveness | CONFIRMED_BY_CFRU_DOC | EFFECTIVE_WITH_CAVEATS | Battle smoke passed | Evidence 211; type tests | No full matchup matrix | Keep with caveats |
| Graphics / Palettes | PARTIALLY_CONFIRMED | EFFECTIVE_WITH_CAVEATS | Normal palette output writes targeted-smoked | Evidence 209; palette tests | Shiny/DNS/OW palettes not proven | Keep with caveats |

## 6. Red Flags / Mismatches

- `EXPAND_MOVESETS` is defined in local `02_external/CFRU-expansion/src/config.h`, while the project also
  has DPE learnset sources. This is not automatically wrong, but it makes active `gLevelUpLearnsets`
  source/pointer verification mandatory before stronger learnset claims.
- `NUM_MOVE_TUTORS` / `LAST_TOTAL_TUTOR_NUM` are local config values and may differ from generic DPE
  examples. FVX constants currently match local `152` / compatibility-byte assumptions, but final
  pointer/count verification remains needed.
- TM/HM compatibility width is doc-confirmed at 16 bytes for the local 120+8 setup, but duplicate
  `gTMHMMoves` write behavior still needs final build verification if we want stronger wording.
- Special Wild can still be misunderstood as standard Wild. CFRU docs explicitly describe separate
  Time-of-Day, swarm, DexNav and raid sources, so no standard-wild support claim should cover them.
- CFRU runtime randomizer flags/features must not be mixed with UPR-FVX randomization. FVX writes final
  tables/settings; CFRU runtime features may choose different sources at runtime.
- Hidden Ability storage is correctly understood as base-stats storage, but ability correctness is not a
  randomizer-compatibility finding unless FVX reads/writes the wrong table/byte.
- Mega/GMax/Primal/Z behavior is not safely inferable from generic FVX metadata alone. The current
  source-backed species/form and item category filters are the right direction, but custom/future
  encodings remain audit-required.
- Current main `fvx-compat-implementation-report.md` does not contain the requested standalone
  Source-to-ROM-Table-Map chapter. The decision matrix repeats that map data, so review content exists
  but documentation placement is inconsistent.

## 7. Empfehlungen

Keep as-is:

- Strict runtime trainer source validation for `VALID_RUNTIME_NOT_LOADED` rows.
- Trainer Class Sprite Sync as opt-in, with class names remaining textlabel-only without sync.
- Species-0 / Egg guards and missing asset/missing pool fallbacks.
- Mechanic item filtering backed by CFRU/DPE categories.

Keep with caveats:

- Trainer Core, Rival counter-starter, Intro Mon, Catching Tutorial, Misc Tweaks, Type Effectiveness,
  Graphics/Palettes and Trainer Held Items.
- Standard Wild, only as modeled `WildPokemon`/`gWildMonHeaders` path plus audit support.
- Gen Limit 1-9 and special-form filtering for known CFRU/DPE identity blocks.

Needs source/pointer verification:

- Active `gLevelUpLearnsets` source and runtime pointer.
- TM/HM `gTMHMMoves` / `gTMHMLearnsets` final pointer and duplicate-write behavior.
- Move Tutor `gMoveTutorMoves` / `gTutorLearnsets` final pointer, count and width.
- Evolution row/method encodings for Mega/GMax/custom methods.
- Static Script/Gift/NPC item sources before any coverage claim.

Needs no-behavior refactor later:

- Split CFRU/DPE table access from `Gen3RomHandler`.
- Extract runtime trainer source audit/classification formatting.
- Extract intro/palette helpers from general RomHandler logic.
- Consolidate safe logging fallback helpers.

Needs ingame smoke by Anton:

- Full standard-wild behavior if Wild is promoted beyond audit/log status.
- Broader trainer route sweep only if new suspected runtime rows appear.
- Shiny palette-focused smoke before any stronger shiny claim.
- Full type matchup matrix only if Type Effectiveness is promoted beyond targeted battle smoke.
- Full held-item distribution audit only if item distribution quality becomes the question.

Later data-quality audit:

- BaseStats values, ability values/names and hidden ability assignments.
- Learnset correctness.
- Evolution method data quality and custom method semantics.
- Move data values/text quality.

Out of scope:

- ROM/source table value corrections.
- DexNav/Raid/special wild randomization.
- Save-block behavior support claims.
- DNS/overworld dynamic palette support claims.
- Custom/future form encodings without source-backed mapping.
- Full playthrough certification.

## 8. Minimaler naechster Review-Block

Exactly one recommended next block:

Run a documentation-only TM/HM + Tutor source/pointer mini-review. Scope it to `src/config.h`,
DPE `src/TM_Tutor_Tables.c`, DPE `tm_compatibility/` and `tutor_compatibility/`, CFRU pointer macros,
and FVX `Gen3RomHandler` TM/Tutor methods. The output should answer only whether local source constants,
compatibility widths, pointer symbols and FVX writer assumptions agree. No ROMs, no builds, no data-value
changes and no P1 promotion.
