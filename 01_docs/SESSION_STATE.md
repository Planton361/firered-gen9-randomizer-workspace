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

`analysis/upr-fvx-cfru-dpe-p1-learnsets-model`

## Aktueller Arbeitsblock

P1 CFRU/DPE-Learnset-Modell fuer Trainer Movesets-only fuer CFRU/DPE Gen9-BPRE.

## Ziel

Trainer Movesets-only isoliert pruefen und dokumentieren. Keine Codeaenderung, kein Fix, keine Aenderungen an `02_external/**`.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #66 als gemerged geprueft.
- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-learnsets-model` erstellt; nicht auf `main` gearbeitet.
- UPR-FVX read-only geprueft: Submodule steht auf `3864ad0e7efda4ed8a329fb22edb3a28db1040e8`.
- UPR-FVX per `./gradlew clean :random:jar` erfolgreich gebaut.
- UPR-FVX- und CFRU/DPE-Quellen read-only fuer `gLevelUpLearnsets` modelliert.
- Neues Protokoll erstellt: `08_tests/randomizer/030_p1_learnsets_model.md`.
- `08_tests/randomizer/README.md` auf Latest Nr. 030 aktualisiert.

## Ergebnis

- Move-Daten laden: `moves.total=559`.
- Trainer-Load funktioniert: `trainers=255`, `trainerPokemon=481`, `nullSpecies=0`.
- Vor Randomization: `before.movesetEntries=53`, `before.zeroMovePokemon=428`, `before.resetMoves=0`, `before.invalidMoves=0`, `before.unknownNamedMoves=0`.
- Der Lauf scheitert vor Save/Log in `TrainerMovesetRandomizer.getMoveSelectionPoolAtLevel()`.
- Fehlerpfad: `Gen3RomHandler.getMovesLearnt()` liest ueber `readPointer()` einen ungueltigen Pointer bei `0x25e49c`.
- Direct Results: `saveSuccessful=false`, `logSuccessful=true`, `outputRomExists=false`, `logNonEmpty=false`, `directLogBytes=0`.
- Kein Output-ROM und kein nichtleerer Trainer-Log entstehen; `Bad Egg`, `<unknown>` und Unknown-Move-Befunde werden im Log nicht erreicht.
- Nach dem Fehlversuch bleibt der Trainer-Moveset-Stand unveraendert: `beforeAfterMoveSignatureChanges=0`.
- Write/Reload ist nicht pruefbar: `writeReloadCompared=0`, `writeReloadMismatches=not run`.
- Trainer Movesets-only ist fuer den getesteten CFRU/DPE-Gen9-BPRE-Stand noch nicht P1-supported.

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

`analysis/upr-fvx-cfru-dpe-p1-learnsets-model`

Zweck: CFRU/DPE-Level-Up-Learnset- und Moveset-Datenmodell fuer `gLevelUpLearnsets` read-only modellieren, bevor ein Trainer-Movesets-Fix versucht wird. Kein Trainer-Movesets-, Held-Items-, TM-/Tutor-, Ability-, Wild-, Starter-, Static/Gift-, Evolution- oder Palette-Fix im selben Branch.

### 2026-05-12 – analysis/upr-fvx-cfru-dpe-p1-learnsets-model

- Workspace PR #66 als gemerged geprueft und Branch `analysis/upr-fvx-cfru-dpe-p1-learnsets-model` erstellt.
- UPR-FVX und CFRU/DPE read-only analysiert; keine Aenderungen an `02_external/**`.
- Modellbefund: CFRU/DPE `gLevelUpLearnsets[]` ist eine interne Species-ID-Pointertabelle bis `SPECIES_PECHARUNT`/`NUM_SPECIES=1440`.
- Learnset-Eintraege sind im DPE-Modell `u16 move` + `u8 level`; Sentinel ist `move == 0 && level == 0xFF`.
- UPR-FVX nimmt fuer `getMovesLearnt()` aktuell Vanilla-Gen3-2-Byte- oder Jambo-3-Byte-Formate ueber `PokemonMovesets` und `pokedexToInternal` an.
- `0x25e49c` wurde als `0x25D7B4 + SPECIES_ZYGARDE(0x33A) * 4` eingeordnet; der Fehler ist ein Learnset-Modellblocker, kein Trainer-Write-Problem.
- Neues Protokoll erstellt: `08_tests/randomizer/030_p1_learnsets_model.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.
