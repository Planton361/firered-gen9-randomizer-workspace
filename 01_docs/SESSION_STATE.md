# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- UPR-FVX PR #18 und Workspace PR #71 sind gemerged.
- UPR-FVX-Fix `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` liest fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks `MOVES_COUNT=992` und `BattleMove.split`.
- TM/HM-only wurde auf dem Move-Data-Reader-Fixstand diagnostiziert und ist blockiert.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-tm-hm-only`

## Aktueller Arbeitsblock

P1 TM/HM-only Diagnose fuer CFRU/DPE Gen9-BPRE.

## Ziel

TM/HM-only Randomizer-Diagnose durchfuehren und dokumentieren. Keine Codeaenderung, kein Fix, keine Aenderungen an `02_external/**`.

## In diesem Arbeitsblock geprueft / geaendert

- UPR-FVX PR #18 und Workspace PR #71 als gemerged geprueft.
- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-tm-hm-only` von `origin/main` erstellt; nicht auf `main` gearbeitet.
- UPR-FVX-Stand `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` bestaetigt.
- Keine Aenderungen an `02_external/**`; UPR-FVX wurde nur gebaut und read-only diagnostiziert.
- TM/HM-only und TM/HM-Compatibility-only diagnostisch ausgefuehrt.
- Neues Protokoll erstellt: `08_tests/randomizer/035_p1_tm_hm_only.md`.
- `08_tests/randomizer/README.md`, `NEXT_STEPS.md` und Roadmap aktualisiert.

## Ergebnis

- `moves.total=992`, `moves.highestLoaded=991`, `moves.highestLoadedName=PsychicNoise`.
- FVX erkennt im TM/HM-Pfad nur `tmCount=50` und `hmCount=8`.
- `getTMHMCompatibility()` liefert `flagLength=59`, also 58 Slots plus Nullslot, nicht 128 Slots.
- Oeffentliche 50 TMs und 8 HMs enthalten keine invaliden Move-IDs.
- Rohe 128-Slot-Lesung ab FVX-`TmMoves` zeigt nach den klassischen 50 TMs und 8 HMs keine plausible 128-Slot-Tabelle; Slots `59..128` sind unplausibel/invalid.
- TM-Move-Randomization scheitert vor Save an `ArrayIndexOutOfBoundsException: Index 827 out of bounds for length 827` in `TMTutorMoveRandomizer.randomizeTMMoves()`.
- TM/HM-Compatibility-only scheitert separat vor Save an einer `NullPointerException` in `TMHMTutorCompatibilityRandomizer.getMoveCompatibilityProbability()` wegen Species mit `null`-Primaertyp.
- Kein Output-ROM, kein nichtleeres Log und kein Reload-Vergleich fuer die TM/HM-only-Pfade.
- TM/HM-only ist nicht P1-supported.

## Noch nicht gestartet

- TM/HM-Fixbranch fuer hohes Move-ID-Limit und Null-Type-Species im Compatibility-Pfad
- CFRU/DPE-128-Slot-TM/HM-Modellierung/Fix
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

Lokale Diagnoseartefakte blieben ignored unter `05_builds/randomizer-smoke/035_p1_tm_hm_only/`.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

Keine Aenderungen an `02_external/**`; UPR-FVX wurde nur read-only genutzt und gebaut.

Keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung.

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

Nach Merge dieses Diagnoseblocks: separater Fixbranch fuer TM/HM-only. Minimaler Scope: hohe Move-IDs defensiv behandeln, Null-Type-Species im Compatibility-Pfad ueberspringen oder absichern, dann CFRU/DPE-128-Slot-TM/HM-Modell eng gaten.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-only

- UPR-FVX PR #18 und Workspace PR #71 als gemerged geprueft.
- TM/HM-only Diagnose auf UPR-FVX `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` ausgefuehrt.
- FVX erkennt nur klassisches `50+8`-TM/HM-Modell.
- TM-Move-Randomization blockiert an altem Move-Ban-Array-Limit.
- TM/HM-Compatibility-only blockiert separat an Null-Type-Species.
- Neues Protokoll erstellt: `08_tests/randomizer/035_p1_tm_hm_only.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.
