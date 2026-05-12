# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #74 ist gemerged.
- UPR-FVX-Fix `58379ffd3146fcd6bb0eb416647cdf9b752cfc0e` implementiert den eng gegateten CFRU/DPE-128-Slot-TM/HM-Reader/Writer.
- TM/HM-only ist im getesteten CFRU/DPE-128-Slot-Scope P1-supported.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`compat/upr-fvx-cfru-dpe-tm-hm-128-slot`

## Aktueller Arbeitsblock

CFRU/DPE TM/HM-128-Slot-Fix.

## Ziel

Minimal gegateten CFRU/DPE-128-Slot-TM/HM-Reader/Writer implementieren und diagnostisch bestaetigen.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #74 als gemerged geprueft.
- Workspace-Branch `compat/upr-fvx-cfru-dpe-tm-hm-128-slot` und UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-tm-hm-128-slot` verwendet; nicht auf `main` gearbeitet.
- UPR-FVX `Gen3RomHandler` fuer CFRU/DPE-Gen9-BPRE um 128-Slot-TM/HM-Read/Write und 16-Byte-Compatibility erweitert.
- Neues Protokoll erstellt: `08_tests/randomizer/038_tm_hm_128_slot_fix_diagnostics.md`.
- `08_tests/randomizer/README.md`, `SESSION_STATE.md`, `NEXT_STEPS.md`, Roadmap und Tool-Manifest aktualisiert.

## Ergebnis

- `getTMCount()` liefert im CFRU/DPE-Gate `120`, `getHMCount()` liefert `8`.
- `gTMHMMoves` wird ueber Pointer-Location `0x8125A8C` gelesen; Zielpointer im Teststand `0x09A5981A`, ROM-Offset `0x1A5981A`.
- TM-Slots `0..119` werden gelesen/geschrieben; HM-Slots `120..127` bleiben bei TM-Randomization unveraendert.
- `gTMHMLearnsets` wird ueber Pointer-Location `0x8043C68` gelesen; Zielpointer im Teststand `0x096002D0`, ROM-Offset `0x16002D0`.
- Compatibility nutzt `129` Flags inklusive Dummy-Index 0 und ist reload-stabil.
- TM moves-only, TM/HM compatibility-only und TM moves + compatibility erzeugen Save, Log, Output-ROM und `writeReloadMismatches=0`.

## Noch nicht gestartet

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

Neue lokale ROM-/Log-Artefakte wurden nur unter `05_builds/randomizer-smoke/038_tm_hm_128_slot_fix/` erzeugt und bleiben ignored.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX wurde nur im erlaubten Submodule-Pfad `02_external/upr-fvx/romio/src/main/java/**` geaendert.

Keine Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder TM51..TM120-Item-Text-/Palette-Codeausweitung.

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

Nach Merge dieses Fixblocks: Tutor-Bitfeld-/Special-Tutor-Modellierung separat read-only untersuchen. Nicht mit Egg-Move-, Learnset-Write- oder Move-Data-Write vermischen.

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
