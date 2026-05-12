# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- UPR-FVX PR #19 und Workspace PR #73 sind gemerged.
- UPR-FVX-Fix `32e43ac03a5762542773213a13be4e0389f1deae` entblockt TM/HM-only im klassischen `50+8`-Scope fuer CFRU/DPE Gen9-BPRE.
- TM/HM-only ist im getesteten FVX-`50+8`-Scope P1-supported; das CFRU/DPE-128-Slot-TM/HM-Modell ist read-only modelliert.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model`

## Aktueller Arbeitsblock

CFRU/DPE TM/HM-128-Slot-Modell read-only.

## Ziel

Aktiven CFRU/DPE-128-Slot-TM/HM-Ort, Table-/Pointermodell, HM-Schutz und Write/Reload-Risiken dokumentieren. Kein Fix.

## In diesem Arbeitsblock geprueft / geaendert

- UPR-FVX PR #19 und Workspace PR #73 als gemerged geprueft.
- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model` von `origin/main` erstellt; nicht auf `main` gearbeitet.
- UPR-FVX, CFRU und DPE read-only auf TM/HM-128-Slot-Symbole, Pointer und Compatibility-Modell untersucht.
- Neues Protokoll erstellt: `08_tests/randomizer/037_p1_tm_hm_128_slot_model.md`.
- `08_tests/randomizer/README.md`, `SESSION_STATE.md`, `NEXT_STEPS.md` und Roadmap aktualisiert.
- Keine Aenderungen an `02_external/**`.

## Ergebnis

- CFRU/DPE definiert `EXPANDED_TMSHMS`, `NUM_TMS=120`, `NUM_HMS=8`, `NUM_TMSHMS=128`.
- DPE `gTMHMMoves` ist `u16[128]` und wird ueber Pointer `0x8125A8C` angebunden.
- Slots `1..120` sind TMs; Slots `121..128` sind HMs.
- CFRU/DPE `gTMHMLearnsets` wird ueber Pointer `0x8043C68` angebunden und nutzt 128 Bits beziehungsweise 16 Bytes pro Species.
- FVX nutzt aktuell den klassischen `50+8`-Ort `romEntry.TmMoves=0x45a5a4` und 8-Byte-Compatibility; nach 50+8 erscheinen dort unplausible Daten, weil ueber das klassische Tabellenende hinaus gelesen wird.
- Ein minimaler 128-Slot-Fix ist plausibel, muss aber separat und eng gegatet erfolgen.

## Noch nicht gestartet

- CFRU/DPE-128-Slot-TM/HM-Fix
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

Keine neuen ROM-/Build-Artefakte erzeugt.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

Keine Aenderungen an `02_external/**`; externe Repos wurden nur read-only analysiert.

Keine Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Codeausweitung.

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

Nach Merge dieses Analyseblocks: separater Fixbranch fuer CFRU/DPE-128-Slot-TM/HM-Read/Write-Scope. Nicht mit Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write vermischen.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model

- UPR-FVX PR #19 und Workspace PR #73 als gemerged geprueft.
- CFRU/DPE-128-Slot-TM/HM-Modell read-only dokumentiert.
- `gTMHMMoves` ist `u16[128]` ueber Pointer `0x8125A8C`; TMs `1..120`, HMs `121..128`.
- `gTMHMLearnsets` ist 128-Bit-/16-Byte-Compatibility pro Species ueber Pointer `0x8043C68`.
- FVX-`50+8`-Pfad bleibt P1-supported, bildet aber das 128-Slot-Modell nicht ab.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety

- Workspace PR #72 als gemerged geprueft.
- UPR-FVX-Fix `32e43ac03a5762542773213a13be4e0389f1deae` erstellt.
- TM-Move-Randomization fuer CFRU/DPE gegen Move-IDs oberhalb der alten FVX-Sicherheitslisten abgesichert.
- TM/HM-Compatibility fuer CFRU/DPE gegen Placeholder-Species und `null`-Typen abgesichert.
- Diagnose 036 bestaetigt TM moves + Compatibility, Compatibility-only und TM moves-only mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Fix.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tm-hm-only

- UPR-FVX PR #18 und Workspace PR #71 als gemerged geprueft.
- TM/HM-only Diagnose auf UPR-FVX `c71fd75e67f5a839560bbf5de7c6f17317a64bd1` ausgefuehrt.
- FVX erkennt nur klassisches `50+8`-TM/HM-Modell.
- TM-Move-Randomization blockiert an altem Move-Ban-Array-Limit.
- TM/HM-Compatibility-only blockiert separat an Null-Type-Species.
- Neues Protokoll erstellt: `08_tests/randomizer/035_p1_tm_hm_only.md`.
- Kein Fix, keine Randomizer-Codeaenderung, keine committed ROM-/Build-Artefakte.
