# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- UPR-FVX PR #20 und Workspace PR #75 sind gemerged.
- UPR-FVX-Stand im Workspace: `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e`.
- TM/HM-only ist im getesteten CFRU/DPE-128-Slot-Scope P1-supported.
- Tutor-/Special-Tutor-Modell ist read-only dokumentiert; Tutor-only ist noch nicht P1-supported.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/upr-fvx-cfru-dpe-p1-tutor-model`

## Aktueller Arbeitsblock

CFRU/DPE Tutor-/Special-Tutor-Modellierung.

## Ziel

Tutor- und Special-Tutor-Tabellen fuer CFRU/DPE Gen9-BPRE read-only modellieren. Kein Fix, keine Codeaenderung.

## In diesem Arbeitsblock geprueft / geaendert

- UPR-FVX PR #20 und Workspace PR #75 als gemerged geprueft.
- Workspace-Branch `analysis/upr-fvx-cfru-dpe-p1-tutor-model` von `origin/main` erstellt; nicht auf `main` gearbeitet.
- UPR-FVX-, CFRU- und DPE-Quellen read-only untersucht.
- Neues Protokoll erstellt: `08_tests/randomizer/039_p1_tutor_model.md`.
- `08_tests/randomizer/README.md`, `SESSION_STATE.md`, `NEXT_STEPS.md` und Roadmap aktualisiert.

## Ergebnis

- DPE definiert normale Tutor-IDs `0..127` plus 9 Special Tutors `128..136`, markiert als nicht in der normalen Tabelle.
- Der aktive DPE-Tabellenstand nutzt `NUM_MOVE_TUTOR_MOVES=152`.
- `gMoveTutorMoves` ist eine `u16`-Tabelle mit `152` Eintraegen; letzter Eintrag `MOVE_TERABLAST` ID `0x3C6` / `966`.
- `gTutorLearnsets` liegt laut `repointall` an Pointer-Location `0x8120C30`.
- `gMoveTutorMoves` liegt laut `repointall` an Pointer-Location `0x8120BE4`.
- Generierte Tutor-Compatibility-Daten zeigen `19` Bytes pro Species, also `152` Bits.
- FVX nutzt fuer FireRed-BPRE aktuell klassisch `MoveTutorMoves=15` und `MoveTutorData=0x459B60`.
- FVX ueberschreibt fuer BPRE-Hacks nur `MoveTutorCompatibility = readPointer(0x120C30)`, nicht `MoveTutorData` oder `MoveTutorMoves`.
- Tutor-only braucht einen separaten, eng gegateten Folge-Fixbranch.

## Noch nicht gestartet

- CFRU/DPE Tutor-Reader-/Writer-Fix
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

Keine neuen lokalen ROM-/Log-/Output-Artefakte erzeugt.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

`02_external/**` wurde nur read-only analysiert.

Keine Egg-Move-, Learnset-Write-, Move-Data-Write-, TM/HM-Item-Text- oder Tutor-Fixes umgesetzt.

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

Nach Merge dieses Analyseblocks: CFRU/DPE Tutor-Move- und Tutor-Compatibility-Fix separat implementieren. Nicht mit Egg-Move-, Learnset-Write- oder Move-Data-Write vermischen.

### 2026-05-13 - analysis/upr-fvx-cfru-dpe-p1-tutor-model

- UPR-FVX PR #20 und Workspace PR #75 als gemerged geprueft.
- CFRU/DPE Tutor-/Special-Tutor-Modell read-only dokumentiert.
- `gMoveTutorMoves` als `u16[152]` ueber Pointer-Location `0x8120BE4` eingeordnet.
- `gTutorLearnsets` als 152-Bit-/19-Byte-Compatibility pro Species ueber Pointer-Location `0x8120C30` eingeordnet.
- Special Tutors als Sonderlogik ausserhalb der normalen Tabelle dokumentiert.
- FVX nutzt aktuell weiterhin klassischen FireRed-Tutor-Scope `15`; Tutor-only bleibt nicht P1-supported.
- Kein Fix, keine Aenderung an `02_external/**`, kein ROM-Zugriff.

### 2026-05-13 - compat/upr-fvx-cfru-dpe-tm-hm-128-slot

- Workspace PR #74 als gemerged geprueft.
- UPR-FVX-Fix `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e` erstellt.
- CFRU/DPE-128-Slot-TM/HM-Pfad eng ueber `useCfruDpeGen9SpeciesCount` gegatet.
- `gTMHMMoves` als `u16[128]` ueber `0x8125A8C` gelesen/geschrieben; TMs `0..119`, HMs `120..127`.
- `gTMHMLearnsets` als 16-Byte-/128-Bit-Compatibility pro Species ueber `0x8043C68` gelesen/geschrieben.
- Diagnose 038 bestaetigt TM moves-only, Compatibility-only und TM moves + Compatibility mit Save/Log/Output/Reload und `writeReloadMismatches=0`.
- Kein Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder TM51..TM120-Item-Text-/Palette-Fix.

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
