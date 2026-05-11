# Roadmap Status

Dieses Dokument ist die textbasierte Spiegelung der Excel-Roadmap. GitHub und Codex sollen dieses Dokument bevorzugt nutzen, weil Aenderungen hier sauber per Git-Diff nachvollziehbar sind.

## Statuslegende

| Status | Bedeutung |
|---|---|
| Erledigt | abgeschlossen und in GitHub dokumentiert |
| Review/Test | umgesetzt, aber noch zu prüfen oder zu mergen |
| Als Nächstes | nächster aktiver Arbeitsblock |
| In Arbeit | aktuell aktiv bearbeitet |
| Warten/Blockiert | wartet auf Entscheidung, Tool, Quelle oder externen Schritt |
| Noch offen | noch nicht begonnen |

## Aktueller Gesamtstand

| Feld | Wert |
|---|---|
| Projekt | FireRed Gen9 Randomizer Workspace |
| GitHub-Repo | `Planton361/firered-gen9-randomizer-workspace` |
| Source of Truth | GitHub + Markdown-Dokumente |
| Excel-Roadmap | visuelles Dashboard |
| Standardterminal | Linux/CachyOS Shell |
| Stabiler Branch | `main` |
| Branch Protection | eingerichtet |
| Aktueller Branch | `analysis/upr-fvx-cfru-dpe-p0-post-merge-smoke` |
| Nächster Branch | `analysis/upr-fvx-cfru-dpe-p1-encounter-systems` |
| Aktueller Fokus | P0-UPR-FVX/CFRU-DPE-Kompatibilitaetskette post-merge bestaetigen |
| ROM-/Build-Arbeit | Smoke-Test lokal dokumentiert; keine Artefakte committed |
| Externe Repos | als Submodule auf Planton361-Forks eingebunden |
| Forks | Planton361-Forks fuer UPR-FVX, DPE Gen9 und CFRU dokumentiert |
| Installationen | devkitPro/devkitARM lokal dokumentiert; keine Installation in diesem Analyseblock |

## Erledigt

| Paket | Aufgabe | Ergebnis |
|---|---|---|
| 01 Initial Setup | GitHub-Repo erstellt | `Planton361/firered-gen9-randomizer-workspace` existiert |
| 01 Initial Setup | `main` eingerichtet | `main` ist Default Branch und stabil |
| 01 Initial Setup | Branch Protection eingerichtet | `main` ist geschützt |
| 01 Initial Setup | Grundstruktur angelegt | `00_project-control`, `01_docs`, `02_external`, `03_tools`, `04_private_roms`, `05_builds`, `06_patches`, `07_scripts`, `08_tests` |
| 01 Initial Setup | `.gitignore` angelegt | ROMs, Saves, Builds, Tool-Binaries und private Dateien werden ausgeschlossen |
| 02 Projektkontext | Projektkontext angelegt | README, AGENTS, PROJECT_BRIEF, SESSION_STATE, NEXT_STEPS, DECISIONS_INDEX |
| 03 Repo Governance | Governance-Dokumente erstellt | Git-, Fork-, Codex-, Security- und Rebuild-Regeln dokumentiert |
| 04 Codex Start | Workflow-/Agent-Regeln dokumentiert | PRs #9, #10, #17, #18 gemerged |
| 05 Externe Quellen | read-only Analyseblock dokumentiert | Quellen und Tool-Manifest ohne Clone/Fork präzisiert |
| 06 Toolchain | Linux/CachyOS-Migration dokumentiert | Linux/CachyOS ist primaere lokale Umgebung; Windows-Befunde sind historisch |
| 06 Toolchain | Linux-GitHub-Auth dokumentiert | `gh` und `git fetch origin` nutzbar dokumentiert |
| 06 Toolchain | devkitPro/devkitARM lokal dokumentiert | `/opt/devkitpro`, `DEVKITARM`, `arm-none-eabi-gcc` und `grit` im Smoke-Test dokumentiert |
| 07 Build-Basis | DPE Gen9 Smoke-Build dokumentiert | Build erfolgreich; Output blieb lokal unter `05_builds/` |
| 07 Build-Basis | CFRU auf DPE Smoke-Build dokumentiert | Build erfolgreich; Output blieb lokal unter `05_builds/` |
| 08 Randomizer-Kompatibilität | UPR-FVX Source-Build dokumentiert | `compat/firered-gen9-cfru-dpe` baut/startet lokal |
| 08 Randomizer-Kompatibilität | erster Randomizer-/BizHawk-Smoke-Test dokumentiert | CFRU/DPE-ROM konnte geladen, minimal randomisiert, gespeichert und in BizHawk gebootet werden |
| 08 Randomizer-Kompatibilität | Route-1-Fallback-Wilddaten dokumentiert | CFRU Route-1-Custom-Day/Night-Wilddaten per Macro deaktiviert; Route 1 wieder als FVX-Fallback-Area sichtbar |
| 08 Randomizer-Kompatibilität | CFRU/DPE-Species-Diagnose dokumentiert | UPR-FVX PR #2 lokal gebaut/ausgefuehrt; Count-, Generation- und `<unknown>`-Rohwerte protokolliert |
| 08 Randomizer-Kompatibilität | CFRU/DPE-Species-Identity-Fix vorbereitet | UPR-FVX-Fixbranch trennt Dex-ID von SpeciesSet-Identitaet fuer erweiterte BPRE-Hacks |
| 08 Randomizer-Kompatibilität | CFRU/DPE-Species-Identity-Fix diagnostiziert | PR #3 hebt `speciesList.size` von 412 auf 799 und `maxSpeciesIdentityNumber` auf 823 |
| 08 Randomizer-Kompatibilität | Gen4+-Wild-Pool-Diagnose dokumentiert | All-Gens-Settings werden fuer Gen3-ROMs auf Gen1-3 gekappt; finaler Wild-Log enthaelt Gen4+ `0` |
| 08 Randomizer-Kompatibilität | CFRU/DPE-UPR-FVX-Kompatibilitaetsmodell dokumentiert | RAM-Mapping zurueckgestellt; P0 bis P4 Fix-Reihenfolge dokumentiert |
| 08 Randomizer-Kompatibilität | Randomizer-/NatDex-Referenzen dokumentiert | Quelleninventar, Workflowmodell und Implementierungsnotizen fuer P0/P1 festgehalten |
| 08 Randomizer-Kompatibilität | CFRU-Documentation-Randomizer-Relevanz dokumentiert | PDF-Befunde zu Defines, Randomizer-Flags, Day/Night-Wild, Trainer-EVs, Save/RAM und Roadmap-Folgen festgehalten |
| 08 Randomizer-Kompatibilität | UPR-FVX Gen-Restrictions-Folgefix | PR #4 gemerged; finaler `RestrictedSpeciesService`-Pool enthaelt Gen4+-Species bei `limitPokemon=false` |
| 08 Randomizer-Kompatibilität | UPR-FVX Wild-Write-Folgefix | PR #5 gemerged; Vanilla/Fallback-Wild-Species werden fuer erweiterte BPRE-Hacks per interner Identitaet geschrieben |
| 08 Randomizer-Kompatibilität | P0-Post-Merge-Smoke | PR #3/#4/#5-Fixkette auf UPR-FVX Merge-Commit `843b75a8` bestaetigt; sichtbarer Wild-Log enthaelt Gen4+ `1030`, `<unknown>` `0` |

## In Arbeit

| Paket | Aufgabe | Ziel |
|---|---|---|
| 08 Randomizer-Kompatibilität | P0-Post-Merge-Smoke dokumentieren | Bestätigungslauf und naechste P1-Schreibpfad-Diagnose festhalten |

## Als Nächstes

| Paket | Aufgabe | Ziel |
|---|---|---|
| 08 Randomizer-Kompatibilität | P1-Schreibpfade diagnostizieren | Trainer, Starters, Static Pokemon, Evolutions und Learnsets getrennt pruefen |

## Noch offen

| Paket | Aufgabe | Hinweise |
|---|---|---|
| 08 Randomizer-Kompatibilität | P1-Schreibpfad-Fixes vorbereiten | Weitere Gen3-Pfade mit `pokedexToInternal[Species.number]` duerfen nicht nebenbei refactored werden |
| 08 Randomizer-Kompatibilität | DPE-Gesamtumfang/PokemonCount bewerten | lokaler Teststand meldet `PokemonCount=823`, waehrend CFRU/DPE-Quellen bis Gen9 reichen |
| 08 Randomizer-Kompatibilität | Wild-Log-`<unknown>` aufloesen | eindeutige Rohwerte sind `rawInternalSpeciesId=0`; Nullslots separat klassifizieren |
| 08 Randomizer-Kompatibilität | CFRU-Day/Night-Custom-Wild-Tabellen analysieren | getrennt vom Vanilla/Fallback-Wild-Pool behandeln |
| 08 Randomizer-Kompatibilität | Trainer-Pokémon testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Starters testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Learnsets testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Evolutions testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Items/Moves/Abilities testen | späterer Einzeltest |
| 09 Ironmon | BizHawk-/Ironmon-Tracker-Anbindung prüfen | erst nach stabiler Randomizer-Kompatibilität |

## Geplante Folge-Arbeitspakete

| Reihenfolge | Branch | Ziel | Grenzen |
|---|---|---|---|
| P0 | `compat/upr-fvx-cfru-dpe-gen-restrictions` | finalen Gen4+-Allowed-Pool fuer erweiterte CFRU/DPE-BPRE-Hacks freigeben | PR #4 gemerged und post-merge bestaetigt |
| P0b | `compat/upr-fvx-cfru-dpe-wild-internal-species-write` | Wild-Encounter-Schreibpfade auf interne Species-Identitaet fuer erweiterte BPRE-Hacks pruefen | PR #5 gemerged und post-merge bestaetigt |
| P1 | noch festlegen | Trainer, Starters, Evolutions, Learnsets und TM/Tutor-Kompatibilitaet diagnostizieren | besonders `pokedexToInternal[species.getNumber()]`-Schreibpfade pruefen |
| P2 | `randomizer/cfru-day-night-wild-table-analysis` | CFRU-Custom-Day/Night-Wild-Tabellen separat untersuchen | Route-1-Fallback bleibt stabil |
| P3 | noch festlegen | Nullslot-`<unknown>` mit `rawInternalSpeciesId=0` klassifizieren | nicht mit GenRestrictions vermischen |
| P4 | noch festlegen | BizHawk-/Ironmon-Tracker-/RAM-Mapping pruefen | erst nach stabiler ROM-Randomizer-Kompatibilitaet |

## Aktuelle Sicherheitsregeln

- Keine ROMs in GitHub.
- Keine ROMs in ChatGPT hochladen.
- Keine Saves oder Emulator States committen.
- Keine Builds committen.
- Keine Tool-Binaries committen.
- Keine `.env`, Tokens, privaten Keys oder lokalen Secrets committen.
- Keine Änderungen direkt auf `main`.
- Externe Original-Upstreams nicht kontaktieren.
- Submodules sollen nur `origin` auf Planton361-Forks nutzen.
- PRs nur mit explizitem `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltem Planton361-Repository erstellen.
- Tool-Binaries bleiben in `03_tools/releases/` und damit lokal/ignored.
- ROMs bleiben in `04_private_roms/` und damit lokal/ignored.
- Build-Ergebnisse bleiben in `05_builds/` und damit lokal/ignored.
- Nicht parallel mehrere schreibende Agenten auf demselben Branch nutzen.

## Update-Regeln

Nach jeder Session aktualisieren:

1. `01_docs/SESSION_STATE.md`
2. `01_docs/NEXT_STEPS.md`
3. dieses Dokument, falls sich Roadmap-Status geändert hat
4. `01_docs/DECISIONS_INDEX.md`, falls Entscheidungen getroffen wurden
5. `01_docs/references/tool-manifest.md`, falls Tools, Repos, Branches oder Commits geändert wurden
6. `01_docs/references/source-index.md`, falls Quellen oder Quellenentscheidungen geändert wurden

Excel-Roadmap:

- Die Excel-Datei dient als visuelles Dashboard.
- Statusänderungen sollen zuerst in Markdown nachvollziehbar sein.
- Excel wird regelmäßig aus dem dokumentierten Status aktualisiert.
- Bei größeren Roadmap-Änderungen wird eine neue Excel-Version committed.

## Nächster empfohlener Branch

```text
analysis/upr-fvx-cfru-dpe-p1-encounter-systems
```

## Arbeitsblock-Log

### 2026-05-11 – setup/workspace-build-randomizer-smoke

- UPR-FVX, DPE Gen9 und CFRU-expansion als Submodule auf Planton361-Forks dokumentiert.
- DPE Gen9 und CFRU auf DPE bauten lokal erfolgreich.
- UPR-FVX konnte die CFRU/DPE-ROM laden, minimal randomisieren und speichern.
- BizHawk bootete die randomisierte ROM.
- Vanilla-/Fallback-Wild-Encounter-Randomization funktionierte; Route 22 und Viridian Forest zeigten randomisierte Encounters.
- Der Wild-Log zeigte weiterhin nur Gen1-3 bzw. `<unknown>`; Species-Pool-Analyse wurde als naechster Fokus identifiziert.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien wurden committed.

### 2026-05-11 – randomizer/route-1-fallback-wild-randomizer-check

- CFRU Route-1-Custom-Day/Night-Wild-Tabelle fuer den Randomizer-Kompatibilitaetsbuild per `FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0` deaktiviert.
- FVX-Log erkannte Route 1 wieder als `Area #3 - ROUTE 1 Grass/Cave`.
- Route 1 zeigte im Log randomisierte Encounters wie Geodude und Abra.
- Gen4-Gen9-Species-Pool und `<unknown>` blieben separat offen.

### 2026-05-11 – analysis/upr-fvx-cfru-dpe-species-pool

- Branch `analysis/upr-fvx-cfru-dpe-species-pool` von `main`-Merge-Commit `5c2cc1eda7e600db461e56eac2eba2c31a575fcc` erstellt.
- UPR-FVX-Codepfade read-only analysiert: `Gen3RomHandler`, `RestrictedSpeciesService`, `SpeciesSet`, `Species`, `SpeciesIDs`, `Gen3Constants`, `WildEncounterRandomizer`, `Randomizer`.
- Ergebnis: `Gen3RomHandler` erkennt DPE-Species nicht ueber DPE-Metadaten, sondern ueber BPRE-Hack-Heuristiken; `generationOf()` ist auf Gen1-3 hardcoded; der Wild-Pool kommt ueber `RestrictedSpeciesService` und `romHandler.getSpeciesSetInclFormes()`.
- `<unknown>` im Wild-Log ist wahrscheinlich ein Null-/Fallback fuer nicht aufgeloeste Encounter-Species, verursacht durch Count-/ID-/Mapping-Probleme.
- Analyseprotokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-species-pool-analysis.md`.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien wurden angefasst.

### 2026-05-11 – analysis/log-cfru-dpe-species-diagnostics

- UPR-FVX PR #2 auf Branch `analysis/log-cfru-dpe-species-diagnostics` lokal reviewt.
- PR #2 enthaelt nur temporaere Diagnoseausgaben in `Gen3RomHandler.java` und `RandomizationLogger.java`.
- UPR-FVX per Clean-Build neu gebaut und lokalen CFRU/DPE-Route-1-Fallback-Teststand per CLI geladen/randomisiert.
- Diagnosebefund dokumentiert: `PokemonCount=823`, `pokedexCount=386`, `speciesList.size=412`, `maxInternalSpeciesId=823`, `maxSpeciesNumber=411`, `generationCounts={1=328, 2=200, 3=295}`.
- Beispiel-Species ueber 386 werden als Gen3 klassifiziert; eindeutige Wild-Log-`<unknown>`-Rohwerte sind `rawInternalSpeciesId=0`.
- Neues Protokoll erstellt: `08_tests/randomizer/upr-fvx-cfru-dpe-species-diagnostics-run.md`.
- Keine ROMs, Builds, Randomizer-JARs, Saves oder Tool-Binaries wurden committed.

### 2026-05-11 – analysis/cfru-dpe-upr-fvx-compatibility-model

- Workspace PR #28 und UPR-FVX PR #3 als gemerged geprueft.
- CFRU/DPE- und UPR-FVX-Codepfade read-only als Kompatibilitaetsmodell zusammengefuehrt.
- Neues Modell erstellt: `01_docs/compat/cfru-dpe-upr-fvx-compatibility-model.md`.
- Ergebnis: RAM-Mapping ist noch nicht noetig; zuerst P0 GenRestrictions/finaler Gen4+-Wild-Pool, danach P1 Trainer/Starters/Evolutions/Learnsets, P2 CFRU Day/Night Wild, P3 Nullslot-`<unknown>`, P4 Ironmon/BizHawk/RAM-Mapping.
- Keine Codeaenderungen, keine Builds und keine ROM-Zugriffe.

### 2026-05-11 – analysis/randomizer-natdex-reference-sources

- Workspace `main` aktualisiert und Branch `analysis/randomizer-natdex-reference-sources` erstellt.
- Neue Referenz-Submodules read-only inventarisiert: UPR-FVX, UPR-FVX upstream, Ajarmar UPR-ZX, CyanSMP64 UPR-ZX NatDex, CyanSMP64 FireRed NatDex, pret FireRed, CFRU-expansion und DPE Gen9.
- Neues Quelleninventar erstellt: `01_docs/compat/randomizer-natdex-reference-sources.md`.
- Neues Workflowmodell erstellt: `01_docs/compat/randomizer-workflow-model.md`.
- Neue Implementierungsnotizen erstellt: `01_docs/compat/natdex-reference-implementation-notes.md`.
- Ergebnis: CyanSMP64 UPR-ZX NatDex ist eine wichtige Gen8/Gen9-Restriction-Referenz; fuer den lokalen CFRU/DPE-Teststand bleibt DPE/CFRU Source-of-Truth fuer interne Species-IDs.
- Keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keine Aenderungen in `02_external/**`.

### 2026-05-11 – analysis/cfru-documentation-randomizer-relevance

- Workspace `main` aktualisiert und Branch `analysis/cfru-documentation-randomizer-relevance` erstellt.
- `02_external/CFRU-expansion/CFRU Documentation.pdf` read-only ausgewertet.
- Neues Referenzdokument erstellt: `01_docs/compat/cfru-documentation-randomizer-relevance.md`.
- Bestehendes Kompatibilitaetsmodell um den CFRU-Doku-Querverweis ergaenzt.
- Ergebnis: CFRU-Runtime-Randomizer-Flags, Day/Night-Wild, Swarms, Roamers, Hidden Ability, Trainer-EV-Spreads, TM/Tutor/Learnsets und Save/RAM bleiben getrennte P1/P2/P4-Themen; P0 bleibt nur GenRestrictions/finaler Gen4+-Wild-Pool.
- Keine Codeaenderungen, keine Builds, keine ROM-Zugriffe und keine Aenderungen in `02_external/**`.

### 2026-05-11 – analysis/upr-fvx-cfru-dpe-gen-restrictions

- UPR-FVX Branch `compat/upr-fvx-cfru-dpe-gen-restrictions` von `compat/firered-gen9-cfru-dpe` erstellt.
- P0-Fix umgesetzt: erweiterte CFRU/DPE-BPRE-Hacks werden in `Settings.tweakForRom()` nicht mehr blind auf Gen3 gekappt; `GameRandomizer.setupSpeciesRestrictions()` nutzt bei `limitPokemon=false` `setRestrictions(null)`.
- UPR-FVX Commit `61a15e521811c5181025e216b3acc27340a495de` erstellt und PR #4 geoeffnet.
- Diagnose: finaler `RestrictedSpeciesService`-Pool enthaelt bei `limitPokemon=false` Gen4+-Species (`gen4plus=381`).
- Sichtbarer Wild-Log bleibt Gen1-3: Gen1 `841`, Gen2 `527`, Gen3 `791`, Gen4+ `0`, `<unknown>` `17`.
- Interpretation: P0-GenRestrictions ist geloest; naechster Engpass ist wahrscheinlich der Gen3/CFRU-DPE-Wild-Write-/Reload-Pfad ueber `pokedexToInternal[Species.number]`.
- Keine Day/Night-Wildtable-, Nullslot-, SpeciesSet-Identity-, Trainer-, Starter-, Evolution-, Learnset-, TM- oder Tutor-Fixes umgesetzt.

### 2026-05-11 – analysis/upr-fvx-cfru-dpe-wild-internal-species-write

- UPR-FVX Branch `compat/upr-fvx-cfru-dpe-wild-internal-species-write` von `compat/firered-gen9-cfru-dpe` erstellt.
- Basis enthaelt PR #4 als Merge-Commit `03b42a1216f5a087d42a3e94a7e81a15db2e977b`.
- Minimaler Wild-Write-Fix umgesetzt: erweiterte CFRU/DPE-BPRE-Hacks schreiben Vanilla/Fallback-Wild-Species ueber `speciesSetIdentityNumber`; Vanilla und normale Gen3-Hacks bleiben auf `pokedexToInternal[Species.number]`.
- UPR-FVX Commit `5f68ec0fc8e1592079486f6d22cf5a122eb08d01` erstellt und PR #5 geoeffnet.
- Diagnose: sichtbarer Wild-Log enthaelt jetzt Gen4+-Species: Gen1 `354`, Gen2 `388`, Gen3 `404`, Gen4 `398`, Gen5 `528`, Gen6 `104`, `<unknown>` `0`.
- Route 1, Route 22 und Viridian Forest wirken weiterhin sichtbar randomisiert.
- Keine Settings-/GenRestrictions-, Day/Night-Wildtable-, Nullslot-, SpeciesSet-Identity-, Trainer-, Starter-, Evolution-, Learnset-, TM- oder Tutor-Fixes umgesetzt.

### 2026-05-11 – analysis/upr-fvx-cfru-dpe-p0-post-merge-smoke

- UPR-FVX PR #5 ist gemerged; Submodule steht auf `compat/firered-gen9-cfru-dpe` bei Merge-Commit `843b75a8f1016fa41a1879408fbeca45de7e030a`.
- UPR-FVX per `./gradlew clean :random:jar` erfolgreich gebaut.
- Derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wurde mit Wild-Randomization, `limitPokemon=false` und ohne Gen1-3-Einschraenkung randomisiert.
- Diagnose bleibt stabil: `PokemonCount=823`, `speciesList.size=799`, `maxSpeciesIdentityNumber=823`.
- Sichtbarer Wild-Log bestaetigt die P0-Kette: Gen1 `354`, Gen2 `388`, Gen3 `404`, Gen4 `398`, Gen5 `528`, Gen6 `104`, `<unknown>` `0`.
- Keine Codeaenderungen, keine neuen Fixes, keine ROMs/Builds/Tool-Binaries committed.
