# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- UPR-FVX PR #16 ist gemerged; der Trainer-Held-Items-lazy-Moveset-Fix `3864ad0e7efda4ed8a329fb22edb3a28db1040e8` ist im Planton361-Fork verfuegbar.
- Workspace PR #65 ist gemerged; `main` enthaelt den Trainer-Held-Items-Fixdiagnosestand.
- Trainer Movesets-only wurde auf UPR-FVX `3864ad0e7efda4ed8a329fb22edb3a28db1040e8` diagnostiziert.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets`

## Aktueller Arbeitsblock

P1 Trainer Movesets Learnsets-Fix fuer CFRU/DPE Gen9-BPRE.

## Ziel

Trainer Movesets-only entblocken: minimal gegateter CFRU/DPE-Learnset-Reader in UPR-FVX und Diagnose 031 dokumentieren.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #67 als gemerged geprueft.
- Workspace-Branch `compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets` verwendet; nicht auf `main` gearbeitet.
- UPR-FVX-Fix erstellt: `655764816f9fefedb9433f33e4da0bc9d44bcda7`.
- UPR-FVX per `./gradlew clean :random:jar` erfolgreich gebaut.
- CFRU/DPE-Learnset-Reader und defensiver Ability-Log-Fallback in `Gen3RomHandler` umgesetzt.
- Neues Protokoll erstellt: `08_tests/randomizer/031_trainer_movesets_learnsets_fix_diagnostics.md`.
- `08_tests/randomizer/README.md` auf Latest Nr. 031 aktualisiert.

## Ergebnis

- Move-Daten laden: `moves.total=559`.
- Trainer-Load funktioniert: `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Vor Randomization: `before.movesetEntries=53`, `before.zeroMovePokemon=428`, `before.resetMoves=0`, `before.invalidMoves=0`, `before.unknownNamedMoves=0`.
- Der fruehere Fehlerpfad `Gen3RomHandler.getMovesLearnt()` -> `No valid pointer at 0x25e49c` ist entblockt.
- Direct Results: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `directLogBytes=38171`.
- Output-ROM und nichtleerer Trainer-Log entstehen; `Bad Egg=false`, `<unknown>=false`, Unknown-Move-Marker `false`.
- Trainer-Movesets werden sichtbar geaendert: `beforeAfterMoveSignatureChanges=418`.
- Write/Reload ist stabil: `writeReloadCompared=481`, `writeReloadMismatches=0`.
- Trainer Movesets-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand P1-supported auf dem Fixstand.

## Noch nicht gestartet

- CFRU/DPE-Level-Up-Learnset-Modell fuer `gLevelUpLearnsets`
- Trainer-Movesets-Fix
- Sensible movebasierte Trainer-Held-Item-Auswahl gegen CFRU/DPE-Learnsets
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

Keine Aenderungen an `02_external/**`; UPR-FVX wurde nur read-only analysiert und gebaut.

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

`analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations`

Zweck: Trainer Movesets-only als P1-supported Baseline in Kombinationslaeufen pruefen und die offenen Gen8/9-Move-, TM/Tutor/Egg- und Held-Item-Folgerisiken separat diagnostizieren.

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
