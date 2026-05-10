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
| Nächster Branch | `setup/linux-gh-auth-refresh` |
| Aktueller Fokus | Linux/CachyOS-Toolchain-Inventur dokumentieren |
| ROM-/Build-Arbeit | noch nicht gestartet |
| Externe Repos | noch nicht geklont |
| Forks | noch nicht angelegt |

## Erledigt

| Paket | Aufgabe | Ergebnis |
|---|---|---|
| 01 Initial Setup | lokalen Workspace erstellt | historisch auf Windows; Linux-Pfad neu zu prüfen |
| 01 Initial Setup | Git initialisiert | lokales Git-Repo erstellt |
| 01 Initial Setup | GitHub-Repo erstellt | `Planton361/firered-gen9-randomizer-workspace` existiert |
| 01 Initial Setup | `main` eingerichtet | `main` ist Default Branch |
| 01 Initial Setup | Branch Protection eingerichtet | `main` ist geschützt |
| 01 Initial Setup | Grundstruktur angelegt | `00_project-control`, `01_docs`, `02_external`, `03_tools`, `04_private_roms`, `05_builds`, `06_patches`, `07_scripts`, `08_tests` |
| 01 Initial Setup | `.gitignore` angelegt | ROMs, Saves, Builds, Tool-Binaries und private Dateien werden ausgeschlossen |
| 01 Initial Setup | Projektkontext angelegt | README, AGENTS, PROJECT_BRIEF, SESSION_STATE, NEXT_STEPS, DECISIONS_INDEX |
| 01 Initial Setup | Quellenindex angelegt | `01_docs/references/source-index.md` |
| 01 Initial Setup | Tool-Manifest angelegt | `01_docs/references/tool-manifest.md` |
| 01 Initial Setup | alte Arbeitsbranches bereinigt | nicht mehr benötigte Setup-Branches lokal und remote gelöscht |
| 01 Initial Setup | ChatGPT-Projekt vorbereitet | Projektdateien und Roadmap als Kontext vorgesehen |
| 03 Repo Governance | Governance-Dokumente erstellt | Git-, Fork-, Codex-, Security- und Rebuild-Regeln dokumentiert |
| 03 Repo Governance | Bootstrap-/Safety-Scripts erstellt | Workspace-Bootstrap, Remote-Check und Git-Safety-Check dokumentiert |
| 05 Externe Quellen | read-only Analyseblock dokumentiert | Quellen und Tool-Manifest ohne Clone/Fork präzisiert |
| 04 Codex Start | Workflow-Automation abgeschlossen | PR #9 `docs: improve codex workflow automation` gemerged |
| 04 Codex Start | Post-Merge-Doku-Sync abgeschlossen | PR #10 `docs: sync post-merge workflow state` gemerged |
| 06 Toolchain | lokale Windows-Toolchain-/Workspace-Inventur abgeschlossen | PR #11 `docs: record local toolchain inventory` gemerged; historischer Stand |
| 06 Toolchain | Windows-PATH-Folgeklärung vorbereitet | PR #12 `docs: prepare path toolchain followup` gemerged; durch OS-Wechsel historisch |
| 06 Toolchain | Linux/CachyOS-Migration dokumentiert | Linux/CachyOS ist primaere lokale Umgebung; Windows-Befunde sind historisch |

## In Review/Test

| Paket | Aufgabe | Prüfpunkte |
|---|---|---|
| 02 Projektkontext | README, AGENTS und Handoff-Dateien prüfen | Sind Ziel, Grenzen, Arbeitsmodell und Codex-Regeln vollständig? |
| 02 Projektkontext | Tool-Manifest prüfen | Sind Pfade, Fork-/Upstream-Regeln und Codex-Freigaben ausreichend klar? |
| 04 Codex Start | Codex Dry Run auswerten | Prüfen, ob Governance-Regeln konsistent und praktisch nutzbar sind |
| 06 Toolchain | Linux/CachyOS-Migration reviewen | Sind Windows-Annahmen aus neuen Arbeitsblöcken entfernt? |
| 06 Toolchain | Linux/CachyOS-Toolchain-Inventur reviewen | Git, gh, Shell, Java und make gefunden; gh Auth, devkitPro/devkitARM und Cross-Compiler bleiben offen |

## Als Nächstes

| Paket | Aufgabe | Ziel |
|---|---|---|
| 06 Toolchain | GitHub-CLI-Auth auf Linux klaeren | Ungueltigen gespeicherten `gh`-Token bereinigen oder neu authentifizieren, ohne Secrets zu dokumentieren |

## Noch offen

| Paket | Aufgabe | Hinweise |
|---|---|---|
| 04 Codex Start | Codex Dry Run abschließen | Codex soll nur Docs prüfen, keine ROM-/Build-Arbeit |
| 04 Codex Start | Codex Standardprompt anwenden | Vorlage für kleine Arbeitsbranches testen |
| 05 Externe Quellen | Repos analysieren, aber noch nicht ändern | UPR FVX, Shiny-Miner, CyanSMP64, Skeli789, pret |
| 05 Externe Quellen | Entscheidung: klonen oder forken | Nur forken, wenn Änderungen nötig sind |
| 06 Toolchain | Linux-Toolchain-Inventur durchführen | auf `setup/linux-toolchain-inventory` dokumentiert; Review/PR offen |
| 06 Toolchain | devkitPro/devkitARM auf Linux prüfen | Installation und Version dokumentieren, kein Build |
| 06 Toolchain | Java-Anforderung für UPR FVX prüfen | OpenJDK 26.0.1 ist lokal vorhanden; spaeter gegen UPR-FVX-Anforderung testen |
| 06 Toolchain | Hex Maniac Advance prüfen | Tool lokal dokumentieren, nicht committen |
| 06 Toolchain | BizHawk prüfen | Tool lokal dokumentieren, nicht committen |
| 06 Toolchain | Ironmon Tracker prüfen | Repo/Release dokumentieren |
| 07 Build-Basis | FireRed-Basis vorbereiten | keine ROMs ins Repo; Hashes lokal dokumentieren |
| 07 Build-Basis | erster Build-Smoke-Test | erst nach Toolchain-Setup |
| 08 Randomizer-Kompatibilität | UPR FVX Smoke-Test | Vanilla/Custom-Kompatibilität getrennt testen |
| 08 Randomizer-Kompatibilität | Wild Encounters testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Trainer testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Learnsets testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Evolutions testen | späterer Einzeltest |
| 08 Randomizer-Kompatibilität | Items/Moves/Abilities testen | späterer Einzeltest |
| 09 Ironmon | BizHawk-Start prüfen | erst nach lauffähigem ROM/Build |
| 09 Ironmon | Ironmon Tracker anbinden | erst nach Randomizer-/Emulator-Smoke-Test |

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

## Update-Regeln

Nach jeder Session aktualisieren:

1. `01_docs/SESSION_STATE.md`
2. `01_docs/NEXT_STEPS.md`
3. dieses Dokument, falls sich Roadmap-Status geändert hat
4. `01_docs/DECISIONS_INDEX.md`, falls Entscheidungen getroffen wurden
5. `01_docs/references/tool-manifest.md`, falls Tools, Repos, Branches oder Commits geändert wurden

Excel-Roadmap:

- Die Excel-Datei dient als visuelles Dashboard.
- Statusänderungen sollen zuerst in Markdown nachvollziehbar sein.
- Excel wird regelmäßig aus dem dokumentierten Status aktualisiert.
- Bei größeren Roadmap-Änderungen wird eine neue Excel-Version committed.

## Nächster empfohlener Branch

```text
setup/linux-gh-auth-refresh
```
## Arbeitsblock-Log

### 2026-05-10 – setup/repo-governance

- Kontextdateien auf GitHub und im ChatGPT-Projektkontext geprüft.
- `SESSION_STATE.md` wurde für `setup/repo-governance` aktualisiert.
- Repo-Governance-Dokumente und Bootstrap-/Safety-Scripts wurden im Arbeitsbranch vorbereitet.
- Keine externen Repos geklont.
- Keine Forks angelegt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.

### 2026-05-10 – setup/codex-dry-run

- Codex-Dry-Run-Dokument vorbereitet.
- Session- und Next-Steps-Dokumente auf den Dry-Run-Arbeitsblock umgestellt.
- Roadmap-Status auf Codex-Dry-Run fortgeschrieben.
- Keine externen Repos geklont.
- Keine Forks angelegt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.

### 2026-05-10 – analysis/external-sources-readonly

- Externe Quellen read-only geprüft und dokumentiert.
- `source-index.md` und `tool-manifest.md` präzisiert.
- Keine externen Repos geklont.
- Keine Forks angelegt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.

### 2026-05-10 – docs/codex-workflow-automation

- Prompt-Templates und Work-Package-Lifecycle vorbereitet.
- Codex-, Git- und Fork-Workflow um PR-Automation, Stop-Regeln und Handoff ergänzt.
- Abschlussdokumentation als Definition of Done dokumentiert.
- GitHub CLI als optionales Tool im Manifest ergänzt.
- Keine externen Repos geklont.
- Keine Forks angelegt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.

### 2026-05-10 – docs/sync-post-merge-workflow-state

- Dokumentationsstand nach gemergtem PR #9 synchronisiert.
- Workflow-Automation in den erledigten Status verschoben.
- Nächsten Branch `setup/toolchain-local-inventory` vorbereitet.
- Nächster Fokus ist lokale Toolchain-/Workspace-Inventur ohne ROM-/Build-Arbeit.
- Keine externen Repos geklont.
- Keine Forks angelegt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.

### 2026-05-10 – setup/toolchain-local-inventory

- Branch `setup/toolchain-local-inventory` von aktuellem `main` erstellt.
- Lokale Toolchain-/Workspace-Inventur im Tool-Manifest dokumentiert.
- PowerShell-Prüfbefehle für PowerShell, Git, GitHub CLI, Java, make, arm-none-eabi-gcc, optional agbcc und pwsh ergänzt.
- Lokale Windows-Checks ausgeführt und bestätigte Versionen/Pfade für PowerShell, Git, GitHub CLI, Java, make und pwsh nachgetragen.
- `gh` ist installiert/authentifiziert, aber im damaligen PATH nicht als `gh` erreichbar.
- `arm-none-eabi-gcc` und optional `agbcc` wurden im damaligen PATH nicht gefunden.
- Keine externen Repos geklont.
- Keine Forks angelegt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.

### 2026-05-10 – setup/path-toolchain-followup

- `main` nach gemergtem PR #11 auf Merge-Commit `e83b1325b71c1e10799ed036a9a7d98718c9a0aa` geprüft.
- Lokale Inventur als erledigt dokumentiert.
- PATH-Folgeklärung für `gh`, `arm-none-eabi-gcc` und optional `agbcc` vorbereitet.
- Keine PATH-Änderungen, Installationen oder Build-Schritte durchgeführt.
- Keine externen Repos geklont.
- Keine Forks angelegt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.

### 2026-05-10 – setup/linux-workspace-migration

- OS-Wechsel von Windows auf Linux/CachyOS als Governance-Änderung dokumentiert.
- README, AGENTS, Tool-Manifest, Session State, Next Steps und Roadmap auf Linux-first umgestellt.
- Windows-Toolchain- und PATH-Befunde als historischer Stand gekennzeichnet.
- Nächster Branch `setup/linux-toolchain-inventory` vorbereitet.
- Keine Installationen, Build-Schritte, externen Clones oder Forks durchgeführt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.

### 2026-05-10 – setup/linux-toolchain-inventory

- Branch `setup/linux-toolchain-inventory` von lokalem `main` erstellt.
- Linux/CachyOS-Toolchain-Inventur read-only durchgeführt.
- Gefunden: Git 2.54.0 unter `/usr/bin/git`, GitHub CLI 2.92.0 unter `/usr/bin/gh`, Shell `/bin/fish`, OpenJDK 26.0.1 unter `/usr/bin/java`, GNU Make 4.4.1 unter `/usr/bin/make`.
- Offen: `gh auth status` meldet einen ungueltigen gespeicherten Token fuer `Planton361`; `arm-none-eabi-gcc`, `agbcc` und `pwsh` sind nicht im PATH; devkitPro/devkitARM ist nicht nachgewiesen.
- Windows-Toolchain-Befunde bleiben historisch und duerfen nicht als Linux-Ist-Stand verwendet werden.
- Keine Installationen, Build-Schritte, externen Clones oder Forks durchgeführt.
- Keine ROMs, Saves, Builds, Tool-Binaries oder privaten Dateien angefasst.
