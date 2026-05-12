# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- UPR-FVX PR #17 ist gemerged; der CFRU/DPE-Trainer-Movesets-Learnset-Fix `655764816f9fefedb9433f33e4da0bc9d44bcda7` ist im Planton361-Fork verfuegbar.
- Workspace PR #68 ist gemerged; `main` enthaelt den Trainer-Movesets-Learnset-Fixdiagnosestand.
- Trainer Movesets-Kombinationen wurden auf UPR-FVX `655764816f9fefedb9433f33e4da0bc9d44bcda7` diagnostiziert.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations`

## Aktueller Arbeitsblock

P1 Trainer Movesets Kombinationsdiagnosen fuer CFRU/DPE Gen9-BPRE.

## Ziel

Trainer Movesets-only als P1-supported Baseline in Kombinationslaeufen pruefen. Fokus: Gen8/9-Move-Datenmodell, TM/Tutor/Egg-Move-Folgerisiken und sensible movebasierte Trainer-Held-Item-Auswahl.

## In diesem Arbeitsblock geprueft / geaendert

- UPR-FVX PR #17 und Workspace PR #68 als gemerged geprueft.
- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations` erstellt; nicht auf `main` gearbeitet.
- Keine Aenderungen an `02_external/**`; UPR-FVX wurde nur read-only genutzt und gebaut.
- Vier Kombinationslaeufe ausgefuehrt: Movesets-only, Movesets+Species, Movesets+Held Items normal, Movesets+sensible Held Items.
- Neues Protokoll erstellt: `08_tests/randomizer/032_p1_trainer_movesets_combinations.md`.
- `08_tests/randomizer/README.md` auf Latest Nr. 032 aktualisiert.

## Ergebnis

- Gemeinsame Ausgangsdaten: `moves.total=559`, `trainers=255`, `trainerPokemon=481`, `before.movesetEntries=53`, `before.invalidMoves=0`.
- Movesets-only: `saveSuccessful=true`, `logSuccessful=true`, `after/reload.movesetEntries=417`, `writeReloadMoveMismatches=0`.
- Movesets+Species: `saveSuccessful=true`, `logSuccessful=true`, `after/reload.gen8plusSpecies=77`, `after/reload.gen9Species=38`, `writeReloadSpeciesMismatches=0`, `writeReloadMoveMismatches=0`.
- Movesets+Held Items normal: `saveSuccessful=true`, `logSuccessful=true`, `after/reload.heldItemEntries=481`, `writeReloadHeldItemMismatches=0`, `writeReloadMoveMismatches=0`.
- Movesets+sensible Held Items: `saveSuccessful=true`, `logSuccessful=true`, `after/reload.heldItemEntries=481`, `writeReloadHeldItemMismatches=0`, `writeReloadMoveMismatches=0`.
- Alle Laeufe: Output-ROM entsteht, Log ist nicht leer, kein `Bad Egg`, kein `<unknown>`, keine Unknown-Move-Marker, keine invaliden Move-IDs.
- Trainer Movesets ist in den geprueften Kombinationen P1-supported; Gen8/9-Move-Datenmodell und TM/Tutor/Egg-Move-Pfade bleiben separate Risiken.

## Noch nicht gestartet

- Gen8/9-Move-Datenmodell gegen CFRU/DPE `MOVES_COUNT=992`
- TM-/Tutor-/Egg-Move-Tabellenpfade
- Learnset-/TM-/Tutor-/Ability-Datenmodellierung nach der Schreibpfadmatrix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen. ROMs wurden nur lokal fuer den Diagnose-Lauf gelesen; Artefakte blieben unter `05_builds/**` und wurden nicht committed.

Lokale ignored Smoke-Outputs wurden nur summarisch ausgewertet. Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

Keine Aenderungen an `02_external/**`; UPR-FVX wurde nur read-only genutzt und gebaut.

Keine MCP-Configs mit Secrets angelegt.

## Naechste Pruefung

Lokal im Workspace nach den Dokumentationsaenderungen pruefen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Naechster empfohlener Branch

`analysis/upr-fvx-cfru-dpe-p1-move-data-model`

Zweck: Gen8/9-Move-Datenmodell, TM-/Tutor-/Egg-Move-Tabellen und Move-Listen-Coverage fuer CFRU/DPE read-only modellieren. Kein Learnset-Write und kein breiter Randomizer-Fix im selben Branch.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-p1-learnsets-model

- Workspace PR #66 als gemerged geprueft und Branch `compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets` erstellt.
- UPR-FVX und CFRU/DPE read-only analysiert; keine Aenderungen an `02_external/**`.
- Modellbefund: CFRU/DPE `gLevelUpLearnsets[]` ist eine interne Species-ID-Pointertabelle bis `SPECIES_PECHARUNT`/`NUM_SPECIES=1440`.
- Learnset-Eintraege sind im DPE-Modell `u16 move` + `u8 level`; Sentinel ist `move == 0 && level == 0xFF`.
- UPR-FVX nimmt fuer `getMovesLearnt()` aktuell Vanilla-Gen3-2-Byte- oder Jambo-3-Byte-Formate ueber `PokemonMovesets` und `pokedexToInternal` an.
- `0x25e49c` wurde als `0x25D7B4 + SPECIES_ZYGARDE(0x33A) * 4` eingeordnet; der Fehler ist ein Learnset-Modellblocker, kein Trainer-Write-Problem.
- Neues Protokoll erstellt: `08_tests/randomizer/030_p1_learnsets_model.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.

### 2026-05-13 – compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets

- Workspace PR #67 als gemerged geprueft und Branch `compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets` verwendet.
- UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets` erstellt.
- Minimaler Fix in `Gen3RomHandler`: CFRU/DPE-`getMovesLearnt()`-Read-Pool fuer `useCfruDpeGen9SpeciesCount && !jamboMovesetHack`.
- CFRU/DPE-Level-Up-Eintraege werden als `u16 move` + `u8 level` bis `{0, 0xFF}` gelesen; Move-IDs ausserhalb der geladenen FVX-Move-Liste werden gefiltert.
- Learnset-Write / `setMovesLearnt()` wurde nicht erweitert.
- Defensiver `abilityName()`-Fallback verhindert Trainer-Log-Abbruch bei erweiterten CFRU/DPE-Ability-IDs.
- UPR-FVX-Commit erstellt: `655764816f9fefedb9433f33e4da0bc9d44bcda7`.
- Diagnose 031: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM und nichtleerer Trainer-Log entstehen.
- Trainer-Movesets werden geschrieben und nach Reload erhalten: `after/reload.movesetEntries=417`, `writeReloadMismatches=0`.
- Kein `Bad Egg`, kein `<unknown>`, keine Unknown-Move-Marker und keine invaliden Move-IDs im Trainerbestand.

### 2026-05-13 – analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations

- UPR-FVX PR #17 und Workspace PR #68 als gemerged geprueft.
- Analysebranch `analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations` erstellt; keine Aenderungen an `02_external/**`.
- Vier Kombinationsdiagnosen mit Seed `274269061345323` ausgefuehrt.
- Movesets-only, Movesets+Species, Movesets+Held Items normal und Movesets+sensible Held Items melden jeweils `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleeren Trainer-Log und `writeReloadMoveMismatches=0`.
- Normale und sensible Held-Item-Kombinationen schreiben `heldItemEntries=481` und reloaden ohne Held-Item-Mismatches.
- Movesets+Species erreicht Gen8/9-Trainer-Pokemon im geschriebenen Bestand: `after/reload.gen8plusSpecies=77`, `after/reload.gen9Species=38`.
- Keine `Bad Egg`-/`<unknown>`-/Unknown-Move-Marker und keine invaliden Move-IDs im Trainerbestand.
- Neues Protokoll erstellt: `08_tests/randomizer/032_p1_trainer_movesets_combinations.md`.
- Trainer Movesets ist fuer die geprueften Kombinationen P1-supported; Gen8/9-Move-Datenmodell und TM/Tutor/Egg-Move-Pfade bleiben separate Folgerisiken.
