# Randomizer Testprotokolle

Dieses Verzeichnis enthaelt die dauerhaften Markdown-Protokolle fuer UPR-FVX/CFRU-DPE-Randomizer-Analysen und Smokes. Lokale ROM-, Build-, Log- und Tool-Artefakte bleiben unter `05_builds/**` oder `03_tools/releases/**` und werden nicht committed.

## Nummerierung und Latest

Neue Randomizer-Smoke-Protokolle sollen ab jetzt eine laufende Nummer bekommen:

```text
001_<kurzer-zweck>.md
002_<kurzer-zweck>.md
003_<kurzer-zweck>.md
```

Bestehende unnummerierte Protokolle bleiben vorerst unveraendert, damit alte Verweise stabil bleiben. Fuer sie gilt die Nummer in der Tabelle unten als Ordnungsindex.

Lokale Smoke-Artefakte sollen passend dazu unter nummerierten Ordnern abgelegt werden:

```text
05_builds/randomizer-smoke/001_<kurzer-zweck>/
05_builds/randomizer-smoke/002_<kurzer-zweck>/
05_builds/randomizer-smoke/003_<kurzer-zweck>/
```

Der neueste bestaetigte Stand wird in Markdown ueber die Spalte `Latest` markiert. Ein `latest`-Symlink ist nicht erforderlich.

## Wichtige Protokolle

| Nr. | Datei | Zweck | Status | Lokaler Artefaktordner | Latest |
|---:|---|---|---|---|---|
| 001 | `upr-fvx-source-integration.md` | UPR-FVX-Source-Integration und Sicherheitsgrenzen | dokumentiert | keiner | nein |
| 002 | `upr-fvx-source-build-smoke-test.md` | lokaler UPR-FVX-Source-Build-Smoke | bestaetigt | keiner | nein |
| 003 | `upr-fvx-cfru-dpe-load-smoke-test.md` | CFRU/DPE-ROM in UPR-FVX laden | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 004 | `upr-fvx-cfru-dpe-randomize-smoke-test.md` | minimal randomisieren und speichern | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 005 | `route-1-fallback-wild-randomizer-check.md` | Route-1-Fallback-Wilddaten fuer FVX pruefen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 006 | `upr-fvx-cfru-dpe-species-pool-analysis.md` | Species-Pool read-only analysieren | dokumentiert | keiner | nein |
| 007 | `upr-fvx-cfru-dpe-species-diagnostics-run.md` | CFRU/DPE-Species-Diagnose mit `PokemonCount=823` | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 008 | `upr-fvx-gen4plus-wild-pool-diagnostics.md` | Gen4+-Wild-Pool-Engpass diagnostizieren | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 009 | `upr-fvx-cfru-dpe-wild-internal-species-write-diagnostics.md` | Wild-Write ueber interne Species-Identitaet diagnostizieren | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 010 | `upr-fvx-cfru-dpe-p0-post-merge-smoke.md` | PR #3/#4/#5 Post-Merge-Smoke | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 011 | `upr-fvx-cfru-dpe-p1-starter-write-diagnostics.md` | Starter-Schreibpfad diagnostizieren | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 012 | `upr-fvx-cfru-dpe-starter-internal-species-write-diagnostics.md` | Starter-Fix diagnostisch bestaetigen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 013 | `upr-fvx-cfru-dpe-p1-static-gift-write-diagnostics.md` | Static/Gift-Read-/Write-Scope vor Gen9-Coverage | teilweise, wieder aufnehmen | `05_builds/randomizer-smoke/` historisch | nein |
| 014 | `upr-fvx-cfru-dpe-pokemon-count-cutoff-diagnostics.md` | `PokemonCount`-Kappung bei DPE/CFRU einordnen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 015 | `upr-fvx-cfru-dpe-gen9-species-count-diagnostics.md` | Gen9-SpeciesCount-Unblocker diagnostizieren | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 016 | `upr-fvx-cfru-dpe-defensive-palette-loading-diagnostics.md` | defensives Palette-Load/-Save-Verhalten pruefen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 017 | `upr-fvx-cfru-dpe-lazy-trainer-movesets-diagnostics.md` | Lazy-Trainer-Movesets-Unblocker pruefen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 018 | `upr-fvx-cfru-dpe-skip-unchanged-palette-save-diagnostics.md` | unveraenderte CFRU/DPE-Paletten beim Save ueberspringen | bestaetigt | `05_builds/randomizer-smoke/` historisch | nein |
| 019 | `upr-fvx-cfru-dpe-gen9-wild-post-merge-smoke.md` | Gen9 Standard-/Fallback-Wild post-merge smoke | bestaetigt: `saveSuccessful=true`, Gen7/8/9 im Wild-Log | `05_builds/randomizer-smoke/` historisch, lokal bereinigt | nein |
| 020 | `upr-fvx-cfru-dpe-wild-banned-special-species-diagnostics.md` | CFRU/DPE-Special-Species-Wild-Ban diagnostisch bestaetigen | bestaetigt: `Bad Egg=0`, `<unknown>=0`, Gen7/8/9 im Wild-Log | `05_builds/randomizer-smoke/` historisch, lokal bereinigt | nein |
| 021 | `021_p1_static_gift_species_only.md` | Static/Gift Species-only Diagnose auf Gen9-Wild-sauberem Stand | blockiert: Gen1-Gen9-Pool vorhanden, Pick erreicht Gen7/8/9, Save bricht an Null-Static-Scope ab | `05_builds/randomizer-smoke/021_p1_static_gift_species_only/` lokal/ignored | nein |
| 022 | `022_static_gift_scope_write_diagnostics.md` | Static/Gift-Scope und interner Species-Write fuer CFRU/DPE | bestaetigt: `saveSuccessful=true`, nichtleerer Static/Gift-Log, Gen7/8/9-Picks, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/022_static_gift_scope_write/` lokal/ignored | nein |
| 023 | `023_p1_trainer_species_only.md` | Trainer-Species-only Diagnose mit Gen1-Gen9-Pool | blockiert: Trainer-Pool Gen1-Gen9 vorhanden, aber `randomizeTrainerPokes()` haengt in `getRandomAbilitySlot()` auf Zero-Ability-Sonder-Species | `05_builds/randomizer-smoke/023_p1_trainer_species_only/` lokal/ignored | nein |
| 024 | `024_trainer_scope_write_diagnostics.md` | Trainer-Scope und interner Species-Write fuer CFRU/DPE | bestaetigt: `saveSuccessful=true`, nichtleerer Trainer-Log, Gen7/8/9-Picks, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/024_trainer_scope_write/` lokal/ignored | nein |
| 025 | `025_p1_evolutions_species_only.md` | Evolution-Species-only Diagnose mit Gen1-Gen9-Pool | blockiert: Evolution-Pool Gen1-Gen9 vorhanden, Save erzeugt Output-ROM, aber Log-Fehler und `writeReloadMismatches=146` | `05_builds/randomizer-smoke/025_p1_evolutions_species_only/` lokal/ignored | nein |
| 026 | `026_evolutions_scope_write_diagnostics.md` | Evolution-Scope und interner Species-Write fuer CFRU/DPE | bestaetigt: `saveSuccessful=true`, `logSuccessful=true`, Gen7/8/9-Picks, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/026_evolutions_scope_write/` lokal/ignored | nein |
| 027 | `027_p1_trainer_held_items_only.md` | Trainer Held Items-only Diagnose | blockiert: Trainer-Held-Item-Pool vorhanden, aber `randomizeTrainerHeldItems()` scheitert in `getMovesLearnt()` bei `0x25e49c`; kein Save/Log/Reload | `05_builds/randomizer-smoke/027_p1_trainer_held_items_only/` lokal/ignored | nein |
| 028 | `028_trainer_held_items_lazy_movesets_diagnostics.md` | Trainer Held Items lazy Moveset-/Learnset-Load | bestaetigt: `saveSuccessful=true`, nichtleerer Trainer-Log, `after/reload.heldItemEntries=481`, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/028_trainer_held_items_lazy_movesets/` lokal/ignored | nein |
| 029 | `029_p1_trainer_movesets_only.md` | Trainer Movesets-only Diagnose | blockiert: Trainer-Load stabil, aber `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()` scheitert in `getMovesLearnt()` bei `0x25e49c`; kein Save/Log/Reload | `05_builds/randomizer-smoke/029_p1_trainer_movesets_only/` lokal/ignored | nein |
| 030 | `030_p1_learnsets_model.md` | CFRU/DPE-Level-Up-Learnset-Modell fuer `gLevelUpLearnsets` | dokumentiert: FVX liest CFRU/DPE-Learnsets mit alten Gen3-/Jambo-Annahmen; `0x25e49c` ist `PokemonMovesets + SPECIES_ZYGARDE*4`; minimaler Folgepfad ist ein gegateter CFRU/DPE-Learnset-Reader | keiner | nein |
| 031 | `031_trainer_movesets_learnsets_fix_diagnostics.md` | Trainer Movesets Learnsets-Fix Diagnose | bestaetigt: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleerer Trainer-Log, `after/reload.movesetEntries=417`, `writeReloadMismatches=0` | `05_builds/randomizer-smoke/031_trainer_movesets_learnsets_fix/` lokal/ignored | nein |
| 032 | `032_p1_trainer_movesets_combinations.md` | Trainer Movesets Kombinationsdiagnosen | bestaetigt: Movesets-only, Movesets+Species, Movesets+Held Items normal und Movesets+sensible Held Items jeweils mit `saveSuccessful=true`, `logSuccessful=true`, `writeReloadMoveMismatches=0` | `05_builds/randomizer-smoke/032_p1_trainer_movesets_combinations/` lokal/ignored | nein |
| 033 | `033_p1_move_data_model.md` | CFRU/DPE Gen8/9-Move-Datenmodell | dokumentiert: FVX laedt aktuell `moves.total=559`, CFRU/DPE definiert `MOVES_COUNT=992`; TM/HM-, Tutor- und Egg-Move-Pfade brauchen getrennte gegatete Modelle | keiner | nein |
| 034 | `034_move_data_reader_fix_diagnostics.md` | CFRU/DPE Move-Data-Reader-Fix Diagnose | bestaetigt: `moves.total=992`, hoechster Move `PsychicNoise`, Trainer-Moveset-Kombinationen mit `saveSuccessful=true`, `logSuccessful=true`, `writeReloadMoveMismatches=0` | `05_builds/randomizer-smoke/034_move_data_reader_fix_diagnostics/` lokal/ignored | nein |
| 035 | `035_p1_tm_hm_only.md` | TM/HM-only Diagnose | blockiert: FVX erkennt nur `50+8`, TM-Move-Randomization scheitert an altem Move-Ban-Array-Limit `827`, Compatibility-only scheitert an Null-Type-Species; kein Save/Output/Reload | `05_builds/randomizer-smoke/035_p1_tm_hm_only/` lokal/ignored | nein |
| 036 | `036_tm_hm_scope_and_safety_fix_diagnostics.md` | TM/HM Scope-and-Safety-Fix Diagnose | bestaetigt im klassischen `50+8`-Scope: TM moves + Compatibility, Compatibility-only und TM moves-only jeweils mit `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleerem Log und `writeReloadMismatches=0` | `05_builds/randomizer-smoke/036_tm_hm_scope_and_safety_fix/` lokal/ignored | ja |

## Aktuell bestaetigter Stand

Latest ist Nr. 036: TM/HM Scope-and-Safety-Fix Diagnose.

Kernaussagen:

- Move-Data-Coverage bleibt stabil mit `moves.total=992` und hoechstem Move `PsychicNoise`.
- FVX erkennt im TM/HM-Pfad weiterhin nur das klassische Modell `50 TMs + 8 HMs`; `getTMHMCompatibility()` liefert `flagLength=59`.
- TM moves + TM/HM Compatibility, Compatibility-only und TM moves-only speichern, loggen und reloaden im klassischen `50+8`-Scope ohne Mismatches.
- Gen8/9-Moves oberhalb der FVX-Sicherheitslisten werden fuer TM-Move-Randomization defensiv ausgeschlossen, nicht voll als TM-Kandidaten modelliert.
- Das CFRU/DPE-128-Slot-TM/HM-Modell bleibt separat offen.

## Lokale Artefaktpflege

Der Ordner `05_builds/randomizer-smoke/` ist nur fuer lokale, ignored Smoke-Outputs gedacht. Alte lokale `.gba`- und `.log`-Artefakte duerfen entfernt werden, wenn sie eindeutig zu dokumentierten Smoke-Laeufen gehoeren und keine Markdown-Protokolle betroffen sind.

Wenn ein Artefakt nicht eindeutig Smoke-Output ist, bleibt es lokal liegen und wird im jeweiligen Protokoll oder in der Session-Dokumentation als `manuell pruefen` markiert.

## Offene Themen

- Gen8/9-Move-Datenmodell-Fix
- Learnsets/Movesets
- TM/Tutor/Egg-Move-Pfade
- TM/Tutor/Abilities
- CFRU Day/Night
