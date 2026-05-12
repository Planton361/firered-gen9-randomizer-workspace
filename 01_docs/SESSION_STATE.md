# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- UPR-FVX PR #17 ist gemerged; der CFRU/DPE-Trainer-Movesets-Learnset-Fix `655764816f9fefedb9433f33e4da0bc9d44bcda7` ist im Planton361-Fork verfuegbar.
- Workspace PR #69 ist gemerged; `main` enthaelt die Trainer-Movesets-Kombinationsdiagnosen.
- Trainer Movesets-Kombinationen wurden auf UPR-FVX `655764816f9fefedb9433f33e4da0bc9d44bcda7` diagnostiziert und als P1-stabil eingeordnet.
- Das CFRU/DPE-Gen8/9-Move-Datenmodell wurde read-only modelliert.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-move-data-model`

## Aktueller Arbeitsblock

P1 Move-Datenmodell fuer CFRU/DPE Gen9-BPRE.

## Ziel

Gen8/9-Move-Datenmodell, FVX-Move-Coverage und TM-/Tutor-/Egg-Move-Tabellen fuer CFRU/DPE Gen9-BPRE read-only modellieren. Keine Codeaenderung und keine Learnset-Write-Ausweitung.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #69 als gemerged geprueft.
- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-move-data-model` von `origin/main` erstellt; nicht auf `main` gearbeitet.
- UPR-FVX-Stand `655764816f9fefedb9433f33e4da0bc9d44bcda7` bestaetigt.
- Keine Aenderungen an `02_external/**`; UPR-FVX und CFRU/DPE wurden nur read-only untersucht und UPR-FVX gebaut.
- FVX-Move-Load, CFRU/DPE-Move-Konstanten, `BattleMove`-Layout, TM/HM-, Tutor- und Egg-Move-Tabellen modelliert.
- Neues Protokoll erstellt: `08_tests/randomizer/033_p1_move_data_model.md`.
- `08_tests/randomizer/README.md` auf Latest Nr. 033 aktualisiert.

## Ergebnis

- FVX erzeugt `moves.total=559`, weil der BPRE-Hack-Support `MoveCount` ueber plausible Move-Description-Pointer scannt und nicht aus CFRU/DPE `MOVES_COUNT` ableitet.
- CFRU/DPE definiert `MOVES_COUNT = MOVE_PSYCHICNOISE + 1 = 0x3E0 = 992`; Gen9 beginnt bei `MOVE_AQUACUTTER = 0x39B`.
- CFRU/DPE `struct BattleMove` bleibt 12 Bytes, erweitert aber Byte `+9..+11` um `z_move_power`, `split`, `z_move_effect`.
- FVX liest `effect`, `power`, `type`, `accuracy`, `pp`, `target`, `priority` und ein flags-Byte, ignoriert aber das gespeicherte `split`-Feld und leitet Gen3-Kategorien typbasiert ab.
- TM/HM nutzt im DPE/CFRU-Modell `u16 gTMHMMoves[NUM_TMSHMS]` und ein erweitertes 128-Slot-Kompatibilitaetsbitfeld; FVX erwartet aktuell `50+8` und `8` Bytes pro Species.
- Tutor nutzt `u16 gMoveTutorMoves`, erweiterte Tutor-Bitfelder und Special-Tutor-Sonderlogik; FVX-BPRE-Defaults bleiben bei klassischem Gen3-Scope.
- Egg Moves bleiben ein `u16`-Stream mit `species + 20000`-Markern und `0xFFFF`-Terminator; Move-ID- und interne Species-Grenzen bleiben trotzdem abzusichern.
- Minimaler Folgepfad: gegateter CFRU/DPE-Move-Reader mit `MOVES_COUNT=992` und `split`-Byte; TM/HM-, Tutor-, Egg- und Learnset-Write-Pfade getrennt lassen.

## Noch nicht gestartet

- CFRU/DPE-Move-Data-Reader-Fix gegen `MOVES_COUNT=992`
- TM/HM-128-Slot-Read-/Write-Modellierung
- Tutor-Bitfeld-/Special-Tutor-Modellierung
- Egg-Move-Species-/Move-ID-Diagnose
- Learnset-/TM-/Tutor-/Ability-Datenmodellierung nach der Schreibpfadmatrix
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen. In diesem Arbeitsblock wurden keine ROM-Diagnoselaeufe benoetigt.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

Keine Aenderungen an `02_external/**`; UPR-FVX und CFRU/DPE wurden nur read-only genutzt und UPR-FVX wurde gebaut.

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

`compat/upr-fvx-cfru-dpe-move-data-reader`

Zweck: minimal gegateten CFRU/DPE-Move-Data-Reader fuer `MOVES_COUNT=992` vorbereiten. Kein TM/HM-, Tutor-, Egg- oder Learnset-Write im selben Branch.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-move-data-model

- Workspace PR #69 als gemerged geprueft und Branch `analysis/upr-fvx-cfru-dpe-p1-move-data-model` erstellt.
- UPR-FVX und CFRU/DPE read-only analysiert; keine Aenderungen an `02_external/**`.
- Modellbefund: FVX laedt aktuell `moves.total=559`, weil `MoveCount` aus plausiblen Description-Pointern statt aus CFRU/DPE `MOVES_COUNT` abgeleitet wird.
- CFRU/DPE definiert `MOVES_COUNT=992` bis `MOVE_PSYCHICNOISE=0x3DF`; Gen9-Moves beginnen bei `MOVE_AQUACUTTER=0x39B`.
- CFRU/DPE `BattleMove` ist 12 Bytes und enthaelt `split`; FVX ignoriert dieses Feld aktuell.
- TM/HM-, Tutor- und Egg-Move-Pfade wurden getrennt eingeordnet; nur Egg Moves bleiben formal nah am alten Gen3-Streamformat.
- Neues Protokoll erstellt: `08_tests/randomizer/033_p1_move_data_model.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.
