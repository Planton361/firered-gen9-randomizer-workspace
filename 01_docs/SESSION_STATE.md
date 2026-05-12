# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #70 ist gemerged; `main` enthaelt das CFRU/DPE-Move-Datenmodell aus Diagnose 033.
- UPR-FVX-Fix `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` liest fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks `MOVES_COUNT=992` und `BattleMove.split`.
- Trainer Movesets-Kombinationen wurden nach dem Move-Data-Reader-Fix erneut diagnostiziert und bleiben P1-stabil.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`compat/upr-fvx-cfru-dpe-move-data-reader`

## Aktueller Arbeitsblock

CFRU/DPE Move-Data-Reader-Fix fuer UPR-FVX.

## Ziel

Minimal gegateten CFRU/DPE-Move-Data-Reader in `Gen3RomHandler.loadMoves()` implementieren. Fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks sollen `MOVES_COUNT=992` und `BattleMove.split` verwendet werden. Keine TM/HM-, Tutor-, Egg-Move- oder Learnset-Write-Ausweitung.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #70 als gemerged geprueft.
- Workspace-Branch `compat/upr-fvx-cfru-dpe-move-data-reader` von `origin/main` erstellt; nicht auf `main` gearbeitet.
- UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-move-data-reader` erstellt.
- UPR-FVX `Gen3RomHandler.loadMoves()` minimal erweitert.
- Gate: vorhandene sichere CFRU/DPE-Gen9-BPRE-Erkennung `useCfruDpeGen9SpeciesCount`.
- Fuer diesen Gate-Pfad wird `MoveCount` auf `CFRU_DPE_MOVES_COUNT - 1` gesetzt.
- CFRU/DPE-`BattleMove.split` wird als Kategorie gelesen; unbekannte Split-Werte fallen auf die alte Gen3-Ableitung zurueck.
- Neues Protokoll erstellt: `08_tests/randomizer/034_move_data_reader_fix_diagnostics.md`.
- `08_tests/randomizer/README.md`, `NEXT_STEPS.md`, Roadmap und Tool-Manifest auf den Fixstand aktualisiert.

## Ergebnis

- Vor Fix aus Diagnose 033: `moves.total=559`.
- Nach Fix: `moves.total=992`.
- Hoechster geladener Move: `moves.highestLoaded=991`, `moves.highestLoadedName=PsychicNoise`.
- Split/Kategoriezaehlung: `physical=420`, `special=301`, `status=270`.
- Trainer Movesets-only: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadMoveMismatches=0`.
- Trainer Movesets + Species: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadMoveMismatches=0`, `writeReloadSpeciesMismatches=0`, `after.gen8plusSpecies=81`, `after.gen9Species=37`.
- Trainer Movesets + Held Items normal: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadMoveMismatches=0`, `writeReloadHeldItemMismatches=0`.
- Trainer Movesets + sensible Held Items: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadMoveMismatches=0`, `writeReloadHeldItemMismatches=0`.
- In allen Diagnose-Laeufen: Output-ROM vorhanden, Log nicht leer, keine invaliden Moves, kein Bad Egg und kein `<unknown>` im Log.

## Noch nicht gestartet

- TM/HM-128-Slot-Read-/Write-Modellierung
- Tutor-Bitfeld-/Special-Tutor-Modellierung
- Egg-Move-Species-/Move-ID-Diagnose
- Move-Data-Write/`saveMoves()` fuer CFRU/DPE
- Learnset-Write / `setMovesLearnt()` fuer CFRU/DPE
- Ability-Datenmodellierung
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen.

Lokale Diagnoseartefakte blieben ignored unter `05_builds/randomizer-smoke/034_move_data_reader_fix_diagnostics/`.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX wurde nur im Planton361-Fork-Submodule auf dem Arbeitsbranch geaendert.

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

Nach Merge der UPR-FVX- und Workspace-PRs: separaten Analyseblock fuer TM/HM-, Tutor- oder Egg-Move-Pfade waehlen. Keine Learnset-Write- oder Move-Data-Write-Ausweitung ohne eigenen Scope.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-move-data-reader

- Workspace PR #70 als gemerged geprueft und Branch `compat/upr-fvx-cfru-dpe-move-data-reader` erstellt.
- UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-move-data-reader` erstellt.
- UPR-FVX-Fix `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` committed.
- Diagnose 034 bestaetigt `moves.total=992`, `PsychicNoise` als hoechsten geladenen Move und stabile Trainer-Moveset-Kombinationen.
- Keine TM/HM-, Tutor-, Egg-Move- oder Learnset-Write-Ausweitung vorgenommen.
