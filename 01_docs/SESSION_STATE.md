# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #72 ist gemerged.
- UPR-FVX-Fix `32e43ac03a5762542773213a13be4e0389f1deae` entblockt TM/HM-only im klassischen `50+8`-Scope fuer CFRU/DPE Gen9-BPRE.
- TM/HM-only ist im getesteten FVX-`50+8`-Scope P1-supported; das CFRU/DPE-128-Slot-TM/HM-Modell bleibt separat offen.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety`

## Aktueller Arbeitsblock

TM/HM Scope-and-Safety-Fix fuer CFRU/DPE Gen9-BPRE.

## Ziel

TM/HM-only entblocken, ohne Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Ausweitung.

## In diesem Arbeitsblock geprueft / geaendert

- Workspace PR #72 als gemerged geprueft.
- Workspace-Branch `compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety` von `origin/main` erstellt; nicht auf `main` gearbeitet.
- UPR-FVX-Branch `compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety` erstellt.
- UPR-FVX-Fix implementiert: TM-Move-Auswahl gegen hohe Move-IDs abgesichert und TM/HM-Compatibility gegen Placeholder-Species/null-Typen abgesichert.
- Diagnose-Laeufe fuer TM moves + Compatibility, Compatibility-only und TM moves-only ausgefuehrt.
- Neues Protokoll erstellt: `08_tests/randomizer/036_tm_hm_scope_and_safety_fix_diagnostics.md`.
- `08_tests/randomizer/README.md`, `SESSION_STATE.md`, `NEXT_STEPS.md`, Roadmap und Tool-Manifest aktualisiert.

## Ergebnis

- `moves.total=992`, hoechster Move `PsychicNoise`, ID `991`.
- FVX erkennt im TM/HM-Pfad weiterhin `tmCount=50`, `hmCount=8`, `compat.flagLength=59`.
- TM moves + Compatibility: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleerer Log, `writeReloadTmHmMismatches=0`, `writeReloadCompatibilityMismatches=0`.
- Compatibility-only: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleerer Log, `writeReloadTmHmMismatches=0`, `writeReloadCompatibilityMismatches=0`.
- TM moves-only: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM, nichtleerer Log, `writeReloadTmHmMismatches=0`, `writeReloadCompatibilityMismatches=0`.
- Keine invaliden TM/HM-Move-IDs, kein `Bad Egg`, kein `<unknown>` und kein Unknown-Move-Marker im Log.
- 10 Compatibility-Species haben weiterhin `null`-Primaertyp und werden im erweiterten BPRE-Hack-Scope uebersprungen.

## Noch nicht gestartet

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

Lokale Diagnoseartefakte blieben ignored unter `05_builds/randomizer-smoke/036_tm_hm_scope_and_safety_fix/`.

Private absolute Pfade und private ROM-Dateinamen wurden nicht dokumentiert.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

UPR-FVX wurde nur im erlaubten Planton361-Fork-Submodule geaendert.

Keine Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Ausweitung.

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

Nach Merge dieses Fixblocks: separater Analysebranch fuer das echte CFRU/DPE-128-Slot-TM/HM-Modell oder Tutor-/Egg-Move-Pfade. Nicht mit dem bestaetigten `50+8`-Scope vermischen.

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
