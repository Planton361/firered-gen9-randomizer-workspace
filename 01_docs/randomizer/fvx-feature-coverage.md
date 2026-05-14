# UPR FVX Feature Coverage Matrix

## Zweck

Diese Datei bildet die sichtbaren Features aus Universal Pokemon Randomizer FVX 1.5.1 auf Projektanforderungen, Roadmap-Pakete und spaetere Tests ab.

Sie ist die detaillierte Requirements-/Coverage-Ebene. Die Roadmap bleibt bewusst grober und verweist auf Feature-Pakete statt auf jede einzelne Checkbox.

## Zaehlregel

- `Unchanged` wird nicht als Feature gezaehlt.
- Sichtbare Checkboxen, Radiobutton-Optionen und klar getrennte Unteroptionen werden als tracebare Feature-Zeilen gezaehlt.
- Unteroptionen werden getrennt gefuehrt, wenn sie eigene Test- oder Risikoaussagen brauchen.
- Ergebnis dieser normalisierten Matrix: **130 Feature-/Suboption-Zeilen**.

## Statusmodell

| Status | Bedeutung |
|---|---|
| Nicht begonnen | Noch kein belastbarer Plan, kein Modell und kein Testnachweis fuer diese Feature-Zeile. |
| Plan erstellt | Feature ist als Arbeitspaket, Suboption oder Regressionstest eingeordnet, aber noch nicht einzeln getestet. |
| Read modelliert | Lesepfad oder Datenmodell ist dokumentiert, aber kein stabiler Writer belegt. |
| Write modelliert | Writer-/Repointing-/Preserve-Risiko ist dokumentiert, aber noch kein stabiler Write-/Reload-Nachweis. |
| Getestet | Dedizierter Diagnose- oder Smoke-Nachweis existiert, aber GUI-Kompatibilitaet ist noch nicht als Paket freigegeben. |
| GUI-kompatibel | Im getesteten CFRU/DPE Gen9-BPRE-Scope liegen Save/Log/Output/Reload-Nachweise oder aequivalente P1-Nachweise fuer die GUI-nahe Option vor. |
| In Arbeit | Aktuell aktiver Arbeitsblock. |

## Coverage Summary

| Status | Anzahl |
|---|---:|
| Nicht begonnen | 39 |
| Plan erstellt | 29 |
| Read modelliert | 0 |
| Write modelliert | 20 |
| Getestet | 10 |
| GUI-kompatibel | 32 |
| In Arbeit | 0 |
| **Gesamt** | **130** |

## Aktueller Hinweis zu 080

Diagnose 080 entblockt `FVX-TRAIT-019` aus Diagnose 070:

- `FVX-TRAIT-019` Evolutions Same Typing ist nach dem Evolution-Same-Typing-Null-Type-Fix im `FVX-TRAIT-016` Evolution-Species-Carrier stabil: Save/Log/Output/Reload true, `writeReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- UPR-FVX `74d88a7ab1d306e1e09ccabb851dffd7f6922b66` bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.
- `Bad Egg=true` bleibt nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil Save/Log/Output/Reload stabil sind und der Reload-Mismatch-Zaehler `0` ist.
- `FVX-TRAIT-018` Evolutions Similar Strength wurde in 080 nur getrennt als Regression beobachtet und nicht mit dem Same-Typing-Fix vermischt.
- `FVX-FOE-009` Force Diverse Types / Trainer Type Diversity ist nach dem Trainer-Type-Diversity-Null-Type-Fix im `FVX-FOE-001` Trainer-Pokemon-Carrier stabil: Save/Log/Output/Reload true, `writeReloadTrainerPokemonMismatches=0`, `filterViolations=0`, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- UPR-FVX `d89fc64e3b0223b03a65466422847dc7df30d03c` bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary sind seit Diagnose 075 im `FVX-WILD-001` Standard/Fallback-Wild-Carrier stabil.
- Trainer Similar Strength ist weiterhin als Suboption unter `FVX-FOE-001` im Trainer-Species-Carrier-Smoke stabil: Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0`.
- Die Statuswerte in der Matrix bleiben konservativ fuer weitere Evolution-Suboptionen und Evolution-Methoden-Writer.

## Coverage nach GUI-Tab

| GUI-Tab | Features | Nicht begonnen | Plan erstellt | Read modelliert | Write modelliert | Getestet | GUI-kompatibel | In Arbeit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| General Options | 4 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| Pokemon Traits | 28 | 7 | 16 | 0 | 0 | 0 | 5 | 0 |
| Starters, Statics & Trades | 15 | 5 | 0 | 0 | 0 | 5 | 5 | 0 |
| Moves & Movesets | 11 | 0 | 3 | 0 | 6 | 0 | 2 | 0 |
| Foe Pokemon | 14 | 8 | 0 | 0 | 0 | 0 | 6 | 0 |
| Wild Pokemon | 12 | 3 | 1 | 0 | 0 | 0 | 8 | 0 |
| TM/HMs & Tutors | 15 | 0 | 9 | 0 | 0 | 0 | 6 | 0 |
| Items | 10 | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| Types | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 0 |
| Graphics | 6 | 2 | 0 | 0 | 4 | 0 | 0 | 0 |
| Misc Tweaks | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |

## Feature Matrix

### General Options

- FVX-GEN-001 | Limit Pokemon | Getestet
- FVX-GEN-002 | No Premature Evolutions | Getestet
- FVX-GEN-003 | No Random Intro Mon | Nicht begonnen
- FVX-GEN-004 | Race Mode | Nicht begonnen

### Pokemon Traits

- FVX-TRAIT-001 | Base Stats: Shuffle / Random | GUI-kompatibel
- FVX-TRAIT-002 | Base Stats: Follow Evolutions | Plan erstellt
- FVX-TRAIT-003 | Randomize Added Stats on Evolution | Plan erstellt
- FVX-TRAIT-004 | Update Base Stats to Generation | Nicht begonnen
- FVX-TRAIT-005 | Standardize EXP Curves | Nicht begonnen
- FVX-TRAIT-006 | Pokemon Types randomisieren | GUI-kompatibel
- FVX-TRAIT-007 | Force Dual Types | Plan erstellt
- FVX-TRAIT-008 | Pokemon Abilities randomisieren | GUI-kompatibel
- FVX-TRAIT-009 | Abilities: Follow Evolutions | Plan erstellt
- FVX-TRAIT-010 | Abilities: Allow Wonder Guard | Plan erstellt
- FVX-TRAIT-011 | Abilities: Combine Duplicate Abilities | Plan erstellt
- FVX-TRAIT-012 | Abilities: Ensure Two Abilities | Plan erstellt
- FVX-TRAIT-013 | Abilities: Ban Trapping Abilities | Plan erstellt
- FVX-TRAIT-014 | Abilities: Ban Negative Abilities | Plan erstellt
- FVX-TRAIT-015 | Abilities: Ban Bad Abilities | Plan erstellt
- FVX-TRAIT-016 | Pokemon Evolutions randomisieren | GUI-kompatibel
- FVX-TRAIT-017 | Evolutions: Random Every Level | Plan erstellt
- FVX-TRAIT-018 | Evolutions: Similar Strength | Plan erstellt
- FVX-TRAIT-019 | Evolutions: Same Typing | GUI-kompatibel
- FVX-TRAIT-020 | Evolutions: Limit to Three Stages | Plan erstellt
- FVX-TRAIT-021 | Evolutions: No Convergence | Plan erstellt
- FVX-TRAIT-022 | Evolutions: Force Change | Plan erstellt
- FVX-TRAIT-023 | Evolutions: Force Growth | Plan erstellt
- FVX-TRAIT-024 | Change Impossible Evolutions | Nicht begonnen
- FVX-TRAIT-025 | Make Evolutions Easier | Nicht begonnen
- FVX-TRAIT-026 | Use Estimated Evolution Levels | Nicht begonnen
- FVX-TRAIT-027 | Remove Time-Based Evolutions | Nicht begonnen
- FVX-TRAIT-028 | EXP-/Legendary-Kurven-Sonderfaelle | Nicht begonnen

### Starters, Statics & Trades

- FVX-SST-001 | Starter Pokemon: Custom | GUI-kompatibel
- FVX-SST-002 | Starter Pokemon: Random completely | GUI-kompatibel
- FVX-SST-003 | Starter Pokemon: Random basic with 2 evolutions | Getestet
- FVX-SST-004 | Starter Pokemon: Random any basic | Getestet
- FVX-SST-005 | Starter Type Restrictions | Getestet
- FVX-SST-006 | Starter: Don't Use Legendaries | Getestet
- FVX-SST-007 | Starter Held Items randomisieren | Nicht begonnen
- FVX-SST-008 | Starter Held Items: Ban Bad Items | Nicht begonnen
- FVX-SST-009 | Starter BST-Min/Max | Getestet
- FVX-SST-010 | Static Pokemon: Swap Legendaries & Standards | GUI-kompatibel
- FVX-SST-011 | Static Pokemon: Random completely | GUI-kompatibel
- FVX-SST-012 | Static Pokemon: Random similar strength | GUI-kompatibel
- FVX-SST-013 | Static Pokemon: Level Modifier / Fix Music | Nicht begonnen
- FVX-SST-014 | In-Game Trades: Given/Requested species | Nicht begonnen
- FVX-SST-015 | In-Game Trades: Nickname/OT/IV/Item | Nicht begonnen

### Moves & Movesets

- FVX-MOVE-001 | Randomize Move Power | Write modelliert
- FVX-MOVE-002 | Randomize Move Accuracy | Write modelliert
- FVX-MOVE-003 | Randomize Move PP | Write modelliert
- FVX-MOVE-004 | Randomize Move Types | Write modelliert
- FVX-MOVE-005 | Randomize Move Names | Write modelliert
- FVX-MOVE-006 | Update Moves to Generation | Write modelliert
- FVX-MOVE-007 | Pokemon Movesets randomisieren | GUI-kompatibel
- FVX-MOVE-008 | Guaranteed Level 1 Moves | Plan erstellt
- FVX-MOVE-009 | Reorder Damaging Moves | GUI-kompatibel
- FVX-MOVE-010 | No Game-Breaking Moves | Plan erstellt
- FVX-MOVE-011 | Force % Good Damaging Moves | Plan erstellt

### Foe Pokemon

- FVX-FOE-001 | Trainer Pokemon randomisieren | GUI-kompatibel
- FVX-FOE-002 | Better Movesets: Boss Trainers | GUI-kompatibel
- FVX-FOE-003 | Better Movesets: Important Trainers | GUI-kompatibel
- FVX-FOE-004 | Better Movesets: Regular Trainers | GUI-kompatibel
- FVX-FOE-005 | Additional Pokemon: Boss Trainers | Nicht begonnen
- FVX-FOE-006 | Additional Pokemon: Important Trainers | Nicht begonnen
- FVX-FOE-007 | Additional Pokemon: Regular Trainers | Nicht begonnen
- FVX-FOE-008 | Trainer Held Items | GUI-kompatibel
- FVX-FOE-009 | Force Diverse Types | GUI-kompatibel
- FVX-FOE-010 | Pokemon League Has Unique Pokemon | Nicht begonnen
- FVX-FOE-011 | Battle Style randomisieren | Nicht begonnen
- FVX-FOE-012 | Rival Carries Starter Through Game | Nicht begonnen
- FVX-FOE-013 | Randomize Trainer Names / Class Names | Nicht begonnen
- FVX-FOE-014 | Trainers Evolve Their Pokemon + Level Modifier | Nicht begonnen

### Wild Pokemon

- FVX-WILD-001 | Randomize Wild Pokemon | GUI-kompatibel
- FVX-WILD-002 | Replacements Per Species | GUI-kompatibel
- FVX-WILD-003 | Split by Encounter Types | GUI-kompatibel
- FVX-WILD-004 | Type Restrictions | GUI-kompatibel
- FVX-WILD-005 | Evolution Restrictions | Plan erstellt
- FVX-WILD-006 | Don't Use Legendaries | GUI-kompatibel
- FVX-WILD-007 | Set Minimum Catch Rate | Nicht begonnen
- FVX-WILD-008 | Randomize Wild Held Items | GUI-kompatibel
- FVX-WILD-009 | Ban Bad Held Items | GUI-kompatibel
- FVX-WILD-010 | Catch Em All Mode | Nicht begonnen
- FVX-WILD-011 | Similar Strength | GUI-kompatibel
- FVX-WILD-012 | Balance Low Level Encounters + Level Modifier | Nicht begonnen

### TM/HMs & Tutors

- FVX-TM-001 | TM Moves randomisieren | GUI-kompatibel
- FVX-TM-002 | Keep Field Move TMs | Plan erstellt
- FVX-TM-003 | TM No Game-Breaking Moves | Plan erstellt
- FVX-TM-004 | TM Force % Good Damaging Moves | Plan erstellt
- FVX-TM-005 | TM/HM Compatibility randomisieren | GUI-kompatibel
- FVX-TM-006 | TM/Levelup Move Sanity | GUI-kompatibel
- FVX-TM-007 | TM Compatibility Follow Evolutions | Plan erstellt
- FVX-TM-008 | Full HM Compatibility | Plan erstellt
- FVX-TM-009 | Move Tutor Moves randomisieren | GUI-kompatibel
- FVX-TM-010 | Keep Field Move Tutors | Plan erstellt
- FVX-TM-011 | Tutor No Game-Breaking Moves | Plan erstellt
- FVX-TM-012 | Tutor Force % Good Damaging Moves | Plan erstellt
- FVX-TM-013 | Tutor Compatibility randomisieren | GUI-kompatibel
- FVX-TM-014 | Tutor/Levelup Sanity | GUI-kompatibel
- FVX-TM-015 | Tutor Compatibility Follow Evolutions | Plan erstellt

### Items

- FVX-ITEM-001 | Field Items Shuffle | Write modelliert
- FVX-ITEM-002 | Field Items Random | Write modelliert
- FVX-ITEM-003 | Field Items Random even distribution | Write modelliert
- FVX-ITEM-004 | Field Items Ban Bad Items | Write modelliert
- FVX-ITEM-005 | Shop Items Shuffle | Write modelliert
- FVX-ITEM-006 | Shop Items Random | Write modelliert
- FVX-ITEM-007 | Shop Item Bans | Write modelliert
- FVX-ITEM-008 | Guarantee Evolution/X Items | Write modelliert
- FVX-ITEM-009 | Balance Shop Prices / Cheap Rare Candies | Write modelliert
- FVX-ITEM-010 | Pickup Items Random / Ban Bad Items | Write modelliert

### Types

- FVX-TYPE-001 | Type Effectiveness Random/Balanced/Keep Identities/Inverse | Getestet
- FVX-TYPE-002 | Add Random Immunities | Getestet
- FVX-TYPE-003 | Update Type Effectiveness | Getestet

### Graphics

- FVX-GFX-001 | Pokemon Palettes Random | Write modelliert
- FVX-GFX-002 | Palettes: Follow Types | Write modelliert
- FVX-GFX-003 | Palettes: Follow Evolutions | Write modelliert
- FVX-GFX-004 | Palettes: Shiny From Normal | Write modelliert
- FVX-GFX-005 | Custom Player Graphics | Nicht begonnen
- FVX-GFX-006 | Character to Replace | Nicht begonnen

### Misc Tweaks

- FVX-MISC-001 | Fastest Text | Nicht begonnen
- FVX-MISC-002 | Running Shoes Indoors | Nicht begonnen
- FVX-MISC-003 | Randomize PC Potion | Nicht begonnen
- FVX-MISC-004 | Give National Dex at Start | Nicht begonnen
- FVX-MISC-005 | Fast Egg Hatching | Nicht begonnen
- FVX-MISC-006 | Lower Case Pokemon Names | Nicht begonnen
- FVX-MISC-007 | Randomize Catching Tutorial | Nicht begonnen
- FVX-MISC-008 | Ban Lucky Egg | Nicht begonnen
- FVX-MISC-009 | Balance Static Pokemon Levels | Nicht begonnen
- FVX-MISC-010 | Run Without Running Shoes | Nicht begonnen
- FVX-MISC-011 | Reusable TMs | Nicht begonnen
- FVX-MISC-012 | Forgettable HMs | Nicht begonnen

## Roadmap-Gruppierung

Diese Matrix soll nicht als 130 Roadmap-Zeilen gepflegt werden. Fuer die Roadmap gelten Feature-Pakete:

1. General Options
2. Pokemon Traits
3. Starters, Statics & Trades
4. Moves & Movesets
5. Foe Pokemon
6. Wild Pokemon
7. TM/HMs & Tutors
8. Items
9. Types
10. Graphics
11. Misc Tweaks
12. GUI-Suboptions-Regressionsmatrix
13. Regression-Smoke-Plan

## Aktueller Bezug zu vorhandenen Diagnosen

- `08_tests/randomizer/047_fvx_gui_options_compatibility_matrix.md` ist die bisherige technische GUI-Kompatibilitaetsmatrix.
- `08_tests/randomizer/055_type_log_placeholder_hygiene.md` trennt Log-/Fallback-Marker von echten Blockern.
- `08_tests/randomizer/056_p1_move_data_write_model.md` modelliert MoveData-Write-Risiken.
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md` modelliert Field Items, Shops und Pickup.
- `08_tests/randomizer/058_p1_palette_randomization_model.md` modelliert echte Palette-Randomization getrennt von Palette-Safety.
- `08_tests/randomizer/059_p1_type_chart_model.md` modelliert Type-Chart-/Effectiveness-Randomization.
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md` konsolidiert GUI-Suboptionen und empfiehlt einen Regression-Smoke-Plan.
- `08_tests/randomizer/064_p1_global_species_pool_regression_smoke_results.md` bestaetigt `FVX-GEN-001` und `FVX-GEN-002` im getesteten `FVX-SST-002`-Starter-Carrier-Smoke; das ist keine globale Vollabdeckung fuer Wild-/Trainer-/Evolution-Kombinationen.
- `08_tests/randomizer/065_p1_starters_suboptions_regression_smoke_results.md` bestaetigt `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` im getesteten Starter-Species-Writer-Smoke; Starter Held Items `FVX-SST-007`/`FVX-SST-008` bleiben separat/offen.
- `08_tests/randomizer/066_type_chart_preserve_effectiveness_fix_diagnostics.md` bestaetigt `FVX-TYPE-001` im TypeEffectiveness-only Random-Smoke mit Fairy-Reload und `writeReloadTypeChartMismatches=0`; Balanced, Keep Identities und Inverse bleiben als einzelne Folgesmokes sinnvoll.
- `08_tests/randomizer/068_type_effectiveness_followup_smoke_results.md` bestaetigt `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse sowie `FVX-TYPE-002` Add Random Immunities und `FVX-TYPE-003` Update Type Effectiveness einzeln mit Save/Log/Output/Reload true und `writeReloadTypeChartMismatches=0`.
- `08_tests/randomizer/078_trainer_type_diversity_nulltype_fix_diagnostics.md` bestaetigt `FVX-FOE-009` Trainer Type Diversity / Type Themes im `FVX-FOE-001` Trainer-Pokemon-Carrier mit Save/Log/Output/Reload true, `writeReloadTrainerPokemonMismatches=0` und `filterViolations=0`.

## Pflege-Regeln

- Statusaenderungen an einzelnen Features werden zuerst in dieser Datei dokumentiert.
- `00_project-control/roadmap/fvx-feature-roadmap.md` bleibt die verdichtete Roadmap-Sicht.
- `00_project-control/roadmap/roadmap-status.md` verweist nur auf grobe Arbeitspakete und grosse Statusaenderungen.
- Neue Tests sollen ihre Feature-IDs nennen, damit Ergebnisse rueckverfolgbar bleiben.
- Keine ROMs, Saves, Builds, Tool-Binaries, privaten Pfade oder Secrets in diese Datei aufnehmen.
