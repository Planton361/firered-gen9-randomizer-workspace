# Roadmap Status

Dieses Dokument ist die textbasierte Spiegelung der Excel-Roadmap.  
GitHub und Codex sollen dieses Dokument bevorzugt nutzen, weil Änderungen hier sauber per Git-Diff nachvollziehbar sind.

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
| Aktueller Branch | `planning/workspace-build-randomizer-integration` |
| Nächster Branch | `setup/devkitpro-toolchain-install-check` |
| Aktueller Fokus | Workspace-Build- und Randomizer-Integration planen |
| ROM-/Build-Arbeit | noch nicht gestartet |
| Externe Repos | noch nicht geklont |
| Forks | noch nicht angelegt |
| Installationen | noch nicht gestartet |

## Erledigt

| Paket | Aufgabe | Ergebnis |
|---|---|---|
| 01 Initial Setup | lokalen Workspace erstellt | historisch auf Windows; Linux-Pfad neu zu prüfen |
| 01 Initial Setup | GitHub-Repo erstellt | `Planton361/firered-gen9-randomizer-workspace` existiert |
| 01 Initial Setup | `main` eingerichtet | `main` ist Default Branch |
| 01 Initial Setup | Branch Protection eingerichtet | `main` ist geschützt |
| 01 Initial Setup | Grundstruktur angelegt | `00_project-control`, `01_docs`, `02_external`, `03_tools`, `04_private_roms`, `05_builds`, `06_patches`, `07_scripts`, `08_tests` |
| 01 Initial Setup | `.gitignore` angelegt | ROMs, Saves, Builds, Tool-Binaries und private Dateien werden ausgeschlossen |
| 02 Projektkontext | Projektkontext angelegt | README, AGENTS, PROJECT_BRIEF, SESSION_STATE, NEXT_STEPS, DECISIONS_INDEX |
| 03 Repo Governance | Governance-Dokumente erstellt | Git-, Fork-, Codex-, Security- und Rebuild-Regeln dokumentiert |
| 04 Codex Start | Workflow-Automation abgeschlossen | PR #9 gemerged |
| 04 Codex Start | Post-Merge-Doku-Sync abgeschlossen | PR #10 gemerged |
| 04 Codex Start | Agent-Best-Practices-Refresh abgeschlossen | PR #17 gemerged; kompakte Prompts, Usage-Optimierung, Agent-/MCP-Regeln, `.aiignore` und PR-Template dokumentiert |
| 04 Codex Start | Post-Merge-Agent-Best-Practices-Sync abgeschlossen | PR #18 gemerged; main/post-merge-Stand synchronisiert |
| 05 Externe Quellen | read-only Analyseblock dokumentiert | Quellen und Tool-Manifest ohne Clone/Fork präzisiert |
| 06 Toolchain | lokale Windows-Toolchain-/Workspace-Inventur abgeschlossen | PR #11 gemerged; historischer Stand |
| 06 Toolchain | Windows-PATH-Folgeklärung vorbereitet | PR #12 gemerged; durch OS-Wechsel historisch |
| 06 Toolchain | Linux/CachyOS-Migration dokumentiert | Linux/CachyOS ist primaere lokale Umgebung; Windows-Befunde sind historisch |
| 06 Toolchain | Linux/CachyOS-Toolchain-Inventur dokumentiert | Git, gh, Shell, Java und make gefunden; GBA-Toolchain-Komponenten bleiben offen |
| 06 Toolchain | GitHub-CLI-/Git-Auth-Refresh dokumentiert | `gh auth status` und `git fetch origin` erfolgreich; Push und PR-Erstellung nutzbar |
| 06 Toolchain | Linux-GBA-Toolchain-Plan dokumentiert | PR #19 gemerged; devkitPro/devkitARM-Vorgehen geplant, keine Installation/Builds |

## In Review/Test

| Paket | Aufgabe | Prüfpunkte |
|---|---|---|
| 02 Projektkontext | README, AGENTS und Handoff-Dateien prüfen | Sind Ziel, Grenzen, Arbeitsmodell und Codex-Regeln vollständig? |
| 02 Projektkontext | Tool-Manifest prüfen | Sind Pfade, Fork-/Upstream-Regeln und Codex-Freigaben ausreichend klar? |
| 04 Codex Start | Codex Dry Run auswerten | Prüfen, ob Governance-Regeln konsistent und praktisch nutzbar sind |
| 06 Toolchain | Linux/CachyOS-Migration reviewen | Sind Windows-Annahmen aus neuen Arbeitsblöcken entfernt? |
| 07 Build-Basis | Workspace-Build-/Randomizer-Integrationsplan reviewen | Sind Zielstruktur, ROM-Grenzen, Toolchain-Plan, externe Quellen, UPR-FVX-Pfad und Folgepakete ausreichend konkret? |

## In Arbeit

| Paket | Aufgabe | Ziel |
|---|---|---|
| 07 Build-Basis | Workspace-Build- und Randomizer-Integration planen | praktischen Integrationsplan erstellen, ohne Installation, Clone, Fork, Build oder ROM-Zugriff |

## Als Nächstes

| Paket | Aufgabe | Ziel |
|---|---|---|
| 06 Toolchain | devkitPro/devkitARM installieren/pruefen | Toolchain nur nach Freigabe installieren oder pruefen; keine Builds und keine ROM-Zugriffe |

## Noch offen

| Paket | Aufgabe | Hinweise |
|---|---|---|
| 05 Externe Quellen | Entscheidung: klonen oder forken | Nur forken, wenn Änderungen nötig sind; vorher Branch/Commit pinnen |
| 06 Toolchain | Java-Anforderung für UPR FVX prüfen | OpenJDK 26.0.1 ist lokal vorhanden; spaeter gegen UPR-FVX-Anforderung testen |
| 06 Toolchain | devkitPro/devkitARM auf Linux installieren/pruefen | erst nach separater Freigabe; Tool-Manifest aktualisieren |
| 06 Toolchain | Hex Maniac Advance prüfen | Tool lokal dokumentieren, nicht committen |
| 06 Toolchain | BizHawk prüfen | Tool lokal dokumentieren, nicht committen |
| 06 Toolchain | Ironmon Tracker prüfen | Repo/Release dokumentieren |
| 07 Build-Basis | FireRed-Basis vorbereiten | keine ROMs ins Repo; nur lokale Hash-Pruefung dokumentieren |
| 07 Build-Basis | CFRU/DPE-Gen9 Quellen pinnen | Shiny-Miner-Forks und Skeli789-Referenzen auf Branch/Commit festlegen |
| 07 Build-Basis | erster Build-Smoke-Test | erst nach Toolchain-Setup, Quellen-Pinning und ROM-Freigabe |
| 08 Randomizer-Kompatibilität | UPR FVX lokal startbar machen | JAR beschaffen oder reproduzierbar bauen; keine Tool-Binaries committen |
| 08 Randomizer-Kompatibilität | UPR FVX Smoke-Test | Vanilla/Custom-Kompatibilität getrennt testen |
| 08 Randomizer-Kompatibilität | Wild Encounters testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Trainer testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Learnsets testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Evolutions testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Items/Moves/Abilities testen | späterer Einzeltest |
| 09 Ironmon | BizHawk-Start prüfen | erst nach lauffähigem ROM/Build |
| 09 Ironmon | Ironmon Tracker anbinden | erst nach Randomizer-/Emulator-Smoke-Test |

## Geplante Folge-Arbeitspakete aus dem Integrationsplan

| Reihenfolge | Branch | Ziel | Grenzen |
|---|---|---|---|
| 1 | `setup/devkitpro-toolchain-install-check` | devkitPro/devkitARM installieren oder freigegebenen Installationsweg ausführen und read-only pruefen | keine Builds, keine ROMs |
| 2 | `analysis/external-source-pinning` | externe Quellen read-only klonen oder ueber GitHub pruefen; Branches/Commits pinnen | keine Forks ohne Entscheidung, keine Repo-Aenderungen |
| 3 | `randomizer/upr-fvx-start-smoke-test` | UPR-FVX-JAR lokal beschaffen oder aus gepinntem Source-Stand bauen und starten | keine Tool-Binaries committen, keine ROM laden ohne Freigabe |
| 4 | `build/cfru-dpe-source-readiness` | CFRU/DPE-Gen9 Build-Anforderungen und Configs dokumentieren | keine ROM, kein Build |
| 5 | `rom/fire-red-private-hash-check` | private FeuerRot-ROM lokal in `04_private_roms/` hashen | keine ROM hochladen oder committen |
| 6 | `build/cfru-dpe-first-smoke-build` | erster lokaler Build aus CFRU/DPE-Gen9 | erst nach Toolchain-, Quellen- und ROM-Freigabe; Builds in `05_builds/` |
| 7 | `randomizer/custom-build-compatibility-smoke-test` | UPR-FVX-Kompatibilität gegen lokalen Custom-Build testen | keine randomized Builds committen |

## Aktuelle Sicherheitsregeln

- Keine ROMs in GitHub.
- Keine ROMs in ChatGPT hochladen.
- Keine Saves oder Emulator States committen.
- Keine Builds committen.
- Keine Tool-Binaries committen.
- Keine `.env`, Tokens, privaten Keys oder lokalen Secrets committen.
- Codex arbeitet nur auf freigegebenen Arbeitsbranches.
- Codex darf nicht direkt auf `main` pushen.
- Externe Repos werden erst im Manifest dokumentiert, dann gezielt geklont oder geforkt.
- Tool-Binaries bleiben in `03_tools/releases/` und damit lokal/ignored.
- ROMs bleiben in `04_private_roms/` und damit lokal/ignored.
- Build-Ergebnisse bleiben in `05_builds/` und damit lokal/ignored.
- MCP-Server sind optional und erst nach Manifest-Eintrag freigegeben.
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
setup/devkitpro-toolchain-install-check
```

## Arbeitsblock-Log

### 2026-05-10 bis 2026-05-11 – bisherige Setup-/Governance-/Toolchain-Blöcke

- Repo-Governance, Codex-Workflow, Post-Merge-Doku-Sync, lokale Toolchain-Inventuren, Linux/CachyOS-Migration, GitHub-Auth-Refresh, Agent-Best-Practices und Linux-GBA-Toolchain-Plan wurden dokumentiert.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien wurden angefasst.
- Keine externen Repos wurden geklont.
- Keine Forks wurden angelegt.

### 2026-05-11 – planning/workspace-build-randomizer-integration

- Branch `planning/workspace-build-randomizer-integration` fuer den Integrationsplan erstellt.
- `01_docs/setup/workspace-build-randomizer-integration-plan.md` erstellt.
- Zielstruktur dokumentiert: `02_external/`, `03_tools/releases/`, `04_private_roms/`, `05_builds/`, `08_tests/`.
- ROM-Umgang geplant: private FireRed-ROM nur lokal, Hash-Pruefung nur als Metadaten/Testprotokoll, keine ROM-Inhalte in Git/ChatGPT.
- devkitPro/devkitARM-Plan konkretisiert: spaetere Installation/Checks, `DEVKITPRO`, `DEVKITARM`, PATH und `arm-none-eabi-gcc` dokumentieren.
- CFRU/DPE-Gen9-Plan konkretisiert: Shiny-Miner-Forks als Hauptkandidaten, Skeli789/pret als Referenzen, Branch/Commit-Pinning vor Clone/Fork/Build.
- UPR-FVX-Plan konkretisiert: Release/JAR oder Source-Clone, Java-Anforderung klaeren, Start-Smoke-Test ohne ROM laden.
- Folge-Arbeitspakete bis Toolchain, Source-Pinning, UPR-FVX-Smoke-Test, CFRU/DPE-Readiness, privatem ROM-Hash, erstem Build-Smoke-Test und Randomizer-Kompatibilitaet definiert.
- Keine Installationen, Build-Schritte, externen Clones oder Forks durchgeführt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.
