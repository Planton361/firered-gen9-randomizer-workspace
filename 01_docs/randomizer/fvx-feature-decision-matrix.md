# UPR-FVX CFRU/DPE Feature Decision Matrix

Stand: 2026-05-21

Scope: documentation-only decision matrix for evaluating UPR-FVX feature readiness in the FireRed
Gen9 CFRU/DPE workspace. No ROM execution, no build, no UPR-FVX/CFRU/DPE code change and no P1
promotion are documented here.

## Zweck

Diese Matrix ist ein review tool. Sie soll pro Feature-Gruppe sichtbar machen, ob der bisherige
Stand stabil genug ist, nur caveated weiterverwendet werden sollte, zuerst Ingame-Smoke braucht,
eine Source-/Pointer-Verifikation braucht oder bewusst ausserhalb des aktuellen Scopes bleibt.

Primaere technische Grundlage ist `01_docs/randomizer/fvx-compat-implementation-report.md` plus die
lokal vorliegende Source-to-ROM-Table-Map aus dem Folgearbeitsstand. Die fuer diese Matrix benoetigten
Source-to-ROM-Punkte sind hier wiederholt, damit dieser Bericht eigenstaendig reviewbar bleibt.
Evidence und Status kommen aus `01_docs/randomizer/fvx-progress-dashboard.md`,
`08_tests/randomizer/fvx_feature_test_status_matrix.tsv` und `08_tests/randomizer/README.md`.

## Kompatibilitaet vs Datenqualitaet

Randomizer-Kompatibilitaet bedeutet: UPR-FVX liest die fuer das Spiel relevante finale ROM-Tabelle
oder Runtime-Quelle, schreibt die richtige Datenform zurueck, nutzt CFRU/DPE-interne Species-IDs wo
noetig und laeuft ohne bekannte Crash-/NPE-/Logging-Blocker.

Datenqualitaet ist eine getrennte Problemklasse. Falsche BaseStats, veraltete Learnsets, falsche
Abilities oder unvollstaendige Move-/Evolution-Daten koennen echte Hack-Datenfehler sein, auch wenn
UPR-FVX technisch korrekt liest und schreibt. Solche Befunde werden hier nicht als automatische
Randomizer-Kompatibilitaetsfehler gewertet, sondern als `NEEDS_DATA_QUALITY_AUDIT_LATER`.

## Bewertungslogik

Eine Feature-Zeile bewertet jeweils:

- `Source Table`: lokale CFRU/DPE-Datei oder `unclear / verify locally`, wenn die Quelle nicht
  eindeutig aus `rg` belegbar ist.
- `Final ROM Table / Pointer`: die Tabelle oder der Pointer, den der gebaute ROM-Stand bereitstellt.
- `FVX Code Path`: der Randomizer-/RomHandler-Pfad, der diese Tabelle tatsaechlich liest/schreibt.
- `Existing Evidence`: Log-Smoke, targeted visual/behavior smoke, audit-only Evidence oder PR-ID.
- `Current Status`: kein Supportclaim, sondern der konservative Ist-Stand.
- `Ingame Test Needed`: `Anton required`, wenn der naechste starke Beleg nur lokal mit privater ROM
  und sanitized Ergebnis entstehen kann.
- `Decision`: eine der Kategorien unten.

Log-only Evidence reicht nicht fuer `KEEP_STABLE_ENOUGH`. Targeted visual/behavior smoke bleibt
caveated. Audit-only belegt Diagnosefaehigkeit, nicht Ingame-Korrektheit.

## Entscheidungskategorien

| Kategorie | Bedeutung |
| --- | --- |
| `KEEP_STABLE_ENOUGH` | Im dokumentierten Scope hinreichend stabil fuer die naechste Runde, ohne neuen Review-Block. Keine P1-Promotion. |
| `KEEP_WITH_CAVEATS` | Nutzbar oder sinnvoll beizubehalten, aber nur mit dokumentierten Grenzen wie targeted smoke, no full playthrough oder no broad matrix. |
| `NEEDS_INGAME_SMOKE` | Code-/Log-Stand reicht nicht; Anton muss lokal mit privater ROM testen und nur sanitized Ergebnis dokumentieren. |
| `NEEDS_SOURCE_POINTER_VERIFICATION` | Source-Datei, Repointing, finale ROM-Tabelle oder Runtime-Pointer sind noch nicht eindeutig genug belegt. |
| `NEEDS_REFACTOR_NO_BEHAVIOR_CHANGE` | Verhalten beibehalten, aber Code-/Dokumentationsstruktur spaeter vereinfachen, um Folgefehler zu senken. |
| `NEEDS_DATA_QUALITY_AUDIT_LATER` | Wahrscheinlicher Dateninhalt-Scope statt Randomizer-Kompatibilitaet; spaeter separat auditieren. |
| `DEFER_OUT_OF_SCOPE` | Bewusst nicht aktueller Bewertungs-/P1-Scope. |
| `UNSUPPORTED_OR_DISABLED` | Feature/Variante bleibt deaktiviert, manuell oder nicht supported. |

## Matrix

| Feature Group | Feature / Scope | CFRU/DPE Source Table | Final ROM Table / Pointer | FVX Code Path | Existing Evidence | Current Status | Ingame Test Needed | Main Risk | Caveat | Decision | Next Minimal Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BaseStats / SpeciesInfo / Abilities | Stats, typing, ability IDs and ability randomization | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c`; ability names/descriptions source `unclear / verify locally` | FVX `PokemonStats`; CFRU/DPE `gBaseStats`; CFRU alias `gSpeciesInfo` | `Gen3RomHandler.loadSpeciesStats()`, `saveSpeciesStats()`, `SpeciesBaseStatRandomizer`, `SpeciesBaseStatUpdater`, `SpeciesAbilityRandomizer`, `RestrictedSpeciesService` | TSV `FVX-TRAIT-001` through `FVX-TRAIT-015` PASS_LOG; dashboard working-matrix passed | Compatibility log-clean, but no dedicated ingame trait proof | Anton required for stronger claim | Final build may alias/repoint `gBaseStats`; ability data correctness is separate | Do not treat wrong stats/abilities as UPR-FVX bug before data audit | `NEEDS_SOURCE_POINTER_VERIFICATION` | Verify final `PokemonStats` -> `gBaseStats`/`gSpeciesInfo` mapping; open data audit only later |
| Level-Up Learnsets | Pokemon level-up movesets | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c`; CFRU `src/Tables/level_up_learnsets.c` also exists | FVX `PokemonMovesets`; CFRU/DPE `gLevelUpLearnsets` | `Gen3RomHandler.getMovesLearnt()`, `setMovesLearnt()`, runtime learnset pointer helpers, `SpeciesMovesetRandomizer` | TSV `FVX-MOVE-007` through `FVX-MOVE-011` PASS_LOG | Log-smoked; source-vs-final active table still needs proof | Anton required for ingame moveset behavior | Active final table may be DPE, CFRU or repointed runtime source | Old/bad learnset values are data-quality scope | `NEEDS_SOURCE_POINTER_VERIFICATION` | Verify active final `gLevelUpLearnsets`; defer value correctness to data audit |
| Evolutions | Evolution randomization and method handling | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Evolution Table.c`; CFRU engine consumers in `src/evolution.c`, `src/mega.c` | FVX `PokemonEvolutions`; CFRU/DPE `gEvolutionTable` | `Gen3RomHandler.getEvolutions()`, `setEvolutions()`, `getEvolutionRowOffset()`, `EvolutionRandomizer` | TSV `FVX-TRAIT-016` through `FVX-TRAIT-027` PASS_LOG or PASS_LOG_WITH_CAVEAT | Log-smoked only; expanded/custom method behavior not broadly proven | Anton required for method-specific smoke | Mega/GMax/custom methods can be misinterpreted | Hard evolution combos and method changes stay caveated | `NEEDS_SOURCE_POINTER_VERIFICATION` | Verify final row layout and method encodings before stronger support |
| Move Data | Power, accuracy, PP, type, names and battle move fields | CFRU `02_external/CFRU-expansion/src/Tables/battle_moves.c`; DPE move data source `unclear / verify locally` | FVX `MoveData`; CFRU `gBattleMoves` | `Gen3RomHandler.getMoves()`, `setMoves()`, `writeGen3BattleMoveData()`, `MoveDataRandomizer`, move updaters | TSV `FVX-MOVE-001` through `FVX-MOVE-005` PASS_LOG; `FVX-MOVE-006` OUT_OF_SCOPE | Log-smoked for randomization; update-to-generation disabled/out of scope | Anton required for move-specific gameplay | CFRU/DPE extra fields such as split, flags, Z/Max fields | Text/name and full battle behavior not globally proven | `NEEDS_SOURCE_POINTER_VERIFICATION` | Verify final `MoveData`/`gBattleMoves` layout; keep Update Moves out of scope |
| TM/HM Moves + Compatibility | TM move list and TM/HM learn compatibility | DPE `src/TM_Tutor_Tables.c`, `src/tm_compatibility/`, `scripts/tm_tutor.py`; CFRU consumers in `src/item.c` | FVX `TmMoves`, `TmMovesDuplicate`, `TMHMCompatibility`; DPE/CFRU `gTMHMMoves`, `gTMHMLearnsets` | `Gen3RomHandler.getTMMoves()`, `setTMMoves()`, `getTMHMCompatibility()`, `setTMHMCompatibility()`, `TMTutorMoveRandomizer`, `TMHMTutorCompatibilityRandomizer` | TSV `FVX-TM-001` through `FVX-TM-008` PASS_LOG; dashboard working-matrix passed | Log-smoked, no dedicated ingame TM compatibility proof | Anton required | Expanded TM count/bit width and duplicate TM list writes | Required-TM item forcing remains separate caveat | `NEEDS_SOURCE_POINTER_VERIFICATION` | Verify active TM count, bit width and duplicate-write semantics |
| Tutor Moves + Compatibility | Move Tutor list and tutor compatibility | DPE `src/TM_Tutor_Tables.c`, `src/tutor_compatibility/`, `scripts/tm_tutor.py`; CFRU consumers in `src/item.c` | FVX `MoveTutorMoves`, `MoveTutorCompatibility`; DPE/CFRU `gMoveTutorMoves`, `gTutorLearnsets` | `Gen3RomHandler.getMoveTutorMoves()`, `setMoveTutorMoves()`, `getMoveTutorCompatibility()`, `setMoveTutorCompatibility()`, CFRU/DPE tutor offset helpers | TSV `FVX-TM-009` through `FVX-TM-015` PASS_LOG; dashboard working-matrix passed | Log-smoked, no dedicated ingame tutor proof | Anton required | Active tutor count/width and menu/text sources | Special tutors/text/menu remain out of current scope | `NEEDS_SOURCE_POINTER_VERIFICATION` | Verify active tutor count and compatibility width |
| Wild Pokemon Standard/Fallback | Modeled Gen3 wild encounter table | CFRU `src/Tables/wild_encounter_tables.c`, `include/wild_encounter.h`, `src/wild_encounter.c` | FVX `WildPokemon`; CFRU `gWildMonHeaders` | `Gen3RomHandler.getEncounters(false)`, `setEncounters(...)`, `getWildEncounterInternalSpeciesId()`, `WildEncounterRandomizer`, output audit | TSV `FVX-WILD-001` PASS_LOG_WITH_CAVEAT; PR #118 output audit available | Standard/fallback modeled path is auditable; ingame smoke still needed | Anton required | Logs can differ from runtime wild systems | Audit-only is not gameplay proof | `NEEDS_INGAME_SMOKE` | Local standard-wild smoke; if divergent, run private Base-vs-Output audit and sanitize summary |
| Special Wild / Day-Night / Swarms | CFRU runtime/special wild systems | CFRU `src/wild_encounter.c`, `src/Tables/wild_encounter_tables.c`, swarm/roamer/raid/dexnav sources | CFRU runtime wild headers, Day/Night, Swarms, DexNav, Raids; not normal FVX `WildPokemon` only | Not modeled by current FVX standard wild writer | Dashboard and report mark separate scope | Out of current P1/standard support | Anton required only if separate scope opens | Ingame source can bypass modeled standard table | No support claim; no P1 promotion | `DEFER_OUT_OF_SCOPE` | Keep separate; open focused scope only after a sanitized divergence report |
| Trainer Pokemon Core | Normal trainer rows and parties | CFRU `src/Tables/trainer_data.c`, `src/Tables/trainer_parties.h` | FVX `TrainerData`, `TrainerCount`, `TrainerEntrySize`; CFRU `gTrainers` | `Gen3RomHandler.loadTrainers()`, `saveTrainers()`, `TrainerPokemonRandomizer` | TSV `FVX-FOE-001` PASS_INGAME_SMOKE with caveats; Evidence 202-204 | Core path works in targeted scope with runtime caveats | Anton required for broader trainer route sweep | Script/runtime rows can differ from normal list | Full playthrough and invalid/loaded-mismatch rows open | `KEEP_WITH_CAVEATS` | Keep; triage only new suspected vanilla-looking battles with sanitized evidence |
| Trainer Runtime Source Sync | FRLG `trainerbattle` runtime rows | Script-referenced CFRU/FRLG TrainerData rows; source table `trainer_data.c` plus script references | Raw `TrainerData` rows outside normal loaded count | `findFrlgTrainerBattleRuntimeSources()`, `loadFrlgRuntimeTrainerSourceRows()`, `saveFrlgRuntimeTrainerSourceRows()`, audits | Evidence 202, 203, 204; PR #100-#106; Viridian Forest 531/532 smoke | Targeted smoke/audit confirmed; not global | Anton required for additional rows | `LOADED_AND_RUNTIME_MISMATCH`, invalid, empty, out-of-range | Strict sync intentionally skips unsafe rows | `KEEP_WITH_CAVEATS` | Keep strict sync; review loaded-mismatch/invalid only with new sanitized audit |
| Rival Counter-Starter / Oak-Lab Rival | Oak-Lab and Rival starter correction after Foe randomization | TrainerData plus FRLG script starter-slot mapping | Runtime TrainerData and Rival starter slots | `findFrlgOakLabRivalTrainerIdsByPlayerStarterSlot()`, `GameRandomizer.maybeRandomizeTrainerPokemon()`, `makeFirstRivalCarryStarter()` | Evidence 207, 208, 212; PR #97, #117, #144/#152 | Targeted counter path passed | Anton required for all-starter matrix | Sampled path is not full starter-choice matrix | Non-starter Rival Pokemon remain eligible by design | `KEEP_WITH_CAVEATS` | Keep; broaden only if later Rival/all-starter sampling is requested |
| Trainer Class Names | Text labels vs IDs/pics semantics | CFRU trainer class name table source `unclear / verify locally`; TrainerData source in `trainer_data.c` | Trainer class names table; `trainerClass` in `TrainerData` | `TrainerNameRandomizer`, `Gen3RomHandler.setTrainerClassNames()`, display-name refresh | Evidence 206, 208, 212; TSV `FVX-FOE-013` | Textlabel-only without Sprite Sync; Sync changes IDs/pics | Anton required for broader visual sweep | User may confuse labels with class IDs/sprites | Needs explicit UI/setting caveat | `KEEP_WITH_CAVEATS` | Keep wording: Class Names textlabel-only unless Sprite Sync is enabled |
| Trainer Class Sprite Sync | Opt-in class label / classId / trainerPic alignment | CFRU `trainer_data.c`; target class/pic mapping inferred from loaded trainers | `TrainerData.trainerClass`, `trainerPic`, class names | `TrainerClassSpriteSyncRandomizer`, `writeTrainerClassSpriteFields()`, runtime row save path, GUI/settings | Evidence 206, 208, 212; PR #111-#116, #143 | Targeted visual smoke passed; GUI-exposed | Anton required for broader categories | Missing valid target pics or untested trainer classes | Regular per-trainer, Rival/Friend grouped semantics only targeted-smoked | `KEEP_WITH_CAVEATS` | Keep enabled when class names are randomized; broader sampling only on demand |
| Trainer Held Items / Sensible Items | Trainer item pools and sensible held items | Trainer parties in `trainer_parties.h`; item data/categories in `item_tables.c` and FVX predicates | Trainer party item fields; FVX item pools | `TrainerPokemonRandomizer.randomizeHeldItems()`, `ItemMechanicPredicates`, `CfruDpeItemCategories` | TSV `FVX-FOE-008`; Evidence 212; PR #151/#152 | NPE-free targeted GUI smoke; distribution unproven | Anton required for distribution audit | Missing movepools/pools, mechanic item leakage, runtime rows | No full held-item distribution proof | `KEEP_WITH_CAVEATS` | Keep guards/filters; full distribution audit only later |
| Items / Mechanic Item Filtering | Field/shop/pickup items and mechanic item bans | CFRU `src/Tables/item_tables.c`; DPE item source `unclear / verify locally` | FVX `ItemData`; CFRU `gItemData`; script/shop/pickup item tables vary | `ItemRandomizer`, `getAllowedItems()`, `CfruDpeItemCategories`, `ItemMechanicPredicates` | TSV `FVX-ITEM-001` through `FVX-ITEM-010`; Evidence 200, 212 | Log-smoked; mechanic filters targeted-smoked with caveats | Anton required for item-specific ingame smoke | Static/gift/NPC sources can bypass item pools | Plates/Drives/Memories/Nectars lack separate policy | `KEEP_WITH_CAVEATS` | Keep source-backed filters; audit only if new leak evidence appears |
| Static Script/Gift/NPC Item Sources | Scripted/gift/NPC item sources outside normal pools | `unclear / verify locally` | Static script constants, gift/NPC item writes, maybe not `ItemData` | Not fully modeled by current item randomizer | Dashboard/report list as open risk | Open risk, no support claim | Anton required if investigated | Source may bypass FVX replacement pools | Separate source audit needed; no data writes now | `NEEDS_SOURCE_POINTER_VERIFICATION` | Map sources first; do not claim randomizer coverage |
| Gen Limit 1-9 | Settings, pools and Gen 1-9 filtering | Species constants and DPE identity blocks; source map partially documented | FVX settings/restriction model, internal species identity | `GenerationLimitDialog`, `Settings`, `SettingsProfileGenerator`, `RestrictedSpeciesService` | Evidence 212; TSV `FVX-GEN-001` PASS_TARGETED_LOG_VISUAL_SMOKE_WITH_CAVEATS | Targeted log/visual smoke passed | Anton required only for broader species matrix | Future/custom forms outside known blocks | No full species matrix or P1 promotion | `KEEP_WITH_CAVEATS` | Keep; revisit only for regression or full species-matrix question |
| Special Form Filtering | Mega/GMax/Regional/Irregular/Special form exclusions | DPE/CFRU species constants and FVX source-backed form classifiers | Species pools, restrictions and item/mechanic filters | `RestrictedSpeciesService`, form filtering helpers, settings/GUI paths | Evidence 212; PR #150-#152 | Latest local checks pass with caveats | Anton required for broad form sampling | Custom/future encodings may escape filters | Regional override semantics must stay explicit | `KEEP_WITH_CAVEATS` | Keep classifiers source-backed; audit future encodings separately |
| Evolutionary Relatives vs Regional Override | Cross-gen family inclusion vs regional-form policy | DPE/CFRU species/form metadata; exact source table varies | Species pool restrictions | `RestrictedSpeciesService` and evolution-relative filtering | Evidence 212 | Behavior documented: relatives can cross gen; regionals need override | Anton required only if disputed | Users may expect regional forms to follow relatives automatically | Policy decision, not data bug | `KEEP_WITH_CAVEATS` | Keep explicit documentation; no behavior change |
| Intro Mon Visual Source | Oak intro visible sprite/palette source | DPE front/palette tables; CFRU script/intro consumers | `PokemonFrontImages`, `PokemonNormalPalettes`; known FRLG intro source entries | `setIntroPokemon()`, `writeCfruDpeIntroVisualTables()`, `syncCfruDpeIntroVisualSourcePointerTableEntries()` | Evidence 205, 207, 208, 212; PR #107/#109/#117/#131 | Targeted visual smoke passed | Anton required for broader intro visual coverage | Other hacks may use different visual source | Species-0 guard fixed, but global visual-source proof absent | `KEEP_WITH_CAVEATS` | Keep; retest only for regression or new intro source |
| Catching Tutorial | Tutorial species mapping and visible tutorial assets | Script/tutorial sources `unclear / verify locally`; species tables via DPE | Tutorial species literals/pointers plus normal species tables | `Gen3RomHandler.setCatchingTutorial()`, Misc tweak path | Evidence 210; PR #126 | Targeted behavior smoke passed | Anton required only for broader behavior proof | Tutorial source may differ in custom hacks | No global tutorial-source proof | `KEEP_WITH_CAVEATS` | Keep targeted caveat; regression-only follow-up |
| Misc Tweaks | Fast Text, PC Potion, Running Shoes, Fast Egg, etc. | Mixed script/constants; exact per-tweak sources vary | Patch literals, flags, text/items, breeding info | `MiscTweakRandomizer`, `applyMiscTweak()`, Fast Egg guard paths | Evidence 210; PR #125-#127; TSV `FVX-MISC-*` | Targeted behavior smoke passed with caveats | Anton required for full behavior proof | Tweak-specific source variance | Fast Egg lacks full hatch-cycle proof; Ban Lucky Egg only likely pass | `KEEP_WITH_CAVEATS` | Keep; only retest detail paths on regression/request |
| Type Effectiveness | Type chart random/update/immunity behavior | Type chart source `unclear / verify locally` | FVX type effectiveness table / battle type chart | Type effectiveness randomizer/updater paths; battle engine consumes final chart | Evidence 211; TSV `FVX-TYPE-001` through `FVX-TYPE-003` | Targeted battle smoke passed | Anton required for full matchup matrix | Partial smoke can miss matchups | No full type-chart matrix or P1 | `KEEP_WITH_CAVEATS` | Keep; full matrix only if explicitly requested |
| Graphics / Palettes | Normal palette randomization output writes | DPE `Front_Pic_Table.c`, `Back_Pic_Table.c`, `Palette_Table.c`, `Shiny_Palette_Table.c` | `PokemonFrontImages`, `PokemonBackImages`, `PokemonNormalPalettes`, `PokemonShinyPalettes` | `loadPokemonPalettes()`, `savePokemonPalettes()`, palette output audit, `Gen3to5PaletteRandomizer` | Evidence 209; PR #123/#124; TSV `FVX-GFX-001` through `FVX-GFX-004` | Targeted visual/audit smoke passed | Anton required for broader species/form visual samples | Pointer copies and form slots can be incomplete | Normal sample changed; not broad or shiny proof | `KEEP_WITH_CAVEATS` | Keep output-write fix; sample broader only if needed |
| Shiny Palette Coverage | Shiny palette behavior and shiny-from-normal | DPE `Shiny_Palette_Table.c`; sprite/form sources as above | `PokemonShinyPalettes`, `gMonShinyPaletteTable` | `savePokemonPalettes()`, shiny palette audit path, `Gen3to5PaletteRandomizer` | Evidence 209 reports `shinyChangedCount=0`; TSV `FVX-GFX-004` caveat | Not proven; only caveated by current audit | Anton required | Shiny pointers may not change or may not be sampled | No shiny-focused visual/audit smoke | `NEEDS_INGAME_SMOKE` | Run separate local shiny-focused audit/visual smoke if desired |
| Custom/future Forms | Unknown future/custom form encodings | `unclear / verify locally` | Species/form identity blocks outside documented current model | `RestrictedSpeciesService`, form classifiers | Report and dashboard list as open risk | Unsupported unless explicitly mapped | Anton required only if a custom encoding appears | Form may bypass filters or ID assumptions | No support claim | `UNSUPPORTED_OR_DISABLED` | Keep disabled/unsupported until source-backed mapping exists |
| Full Playthrough Scope | End-to-end practical compatibility | All above | All above | Full game workflow, not one FVX method | Explicitly absent in report/dashboard | Missing by design | Anton required | Targeted smokes can miss late-game/runtime paths | No P1 promotion without broader playthrough evidence | `NEEDS_INGAME_SMOKE` | Treat as separate manual milestone with sanitized notes only |

## Pflege der Matrix

- Update this file only when a new evidence file, report, PR pin or explicit decision changes a row.
- Keep `fvx_feature_test_status_matrix.tsv` as the per-Feature-ID worklist; this matrix is the
  higher-level decision view.
- Never promote from log-only evidence to stable wording. Add `KEEP_WITH_CAVEATS` or
  `NEEDS_INGAME_SMOKE` instead.
- When a local ROM smoke is performed by Anton, record only sanitized observations: feature label,
  pass/fail, high-level species/item/trainer labels if safe, and caveats. Do not record ROM paths,
  hashes, screenshots, saves, emulator states, output ROMs, full logs, private paths, secrets,
  tokens or `.env`.
- Source-to-ROM claims require a source file, final ROM pointer/table, and FVX code path. If any part
  is unclear, write `unclear / verify locally`.

## Prioritaetenliste

### First review now

- BaseStats / SpeciesInfo / Abilities
- Level-Up Learnsets
- Evolutions
- TM/HM Moves + Compatibility
- Tutor Moves + Compatibility
- Wild Pokemon Standard/Fallback
- Trainer Pokemon Core
- Trainer Runtime Source Sync
- Items / Mechanic Item Filtering
- Graphics / Palettes

### Keep but caveated

- Trainer Held Items / Sensible Items
- Rival Counter-Starter / Oak-Lab Rival
- Trainer Class Names and Trainer Class Sprite Sync
- Gen Limit 1-9
- Special Form Filtering
- Evolutionary Relatives vs Regional Override
- Intro Mon Visual Source
- Catching Tutorial
- Misc Tweaks
- Type Effectiveness

### Later data audit

- BaseStats values, abilities and ability names/descriptions
- Level-up learnset correctness
- Evolution method data and species relationships
- Move data values and text naming quality

### Later refactor

- Shared CFRU/DPE internal species identity helpers
- Source/pointer verification helpers for CFRU/DPE dynamic tables
- Logging fallback/safe access helpers
- Runtime-source audit/report formatting, without changing sync behavior

### Explicitly out of scope

- Special Wild / Day-Night / Swarms until separately scoped
- Static Script/Gift/NPC Item Sources until source-mapped
- Custom/future form encodings until source-backed
- Shiny Palette Coverage until a shiny-focused local smoke exists
- Full Playthrough Scope until a separate manual milestone is requested
