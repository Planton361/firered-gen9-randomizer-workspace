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
| Standardterminal | Windows PowerShell |
| Stabiler Branch | `main` |
| Branch Protection | eingerichtet |
| Nächster Branch | `setup/repo-governance` |
| Aktueller Fokus | Codex-Dry-Run der Governance-Regeln |
| ROM-/Build-Arbeit | noch nicht gestartet |
| Externe Repos | noch nicht geklont |
| Forks | noch nicht angelegt |

## Erledigt

| Paket | Aufgabe | Ergebnis |
|---|---|---|
| 01 Initial Setup | lokalen Workspace erstellt | `C:\Users\anton\romhacking\fr-rando-gen9` existiert |
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

## In Review/Test

| Paket | Aufgabe | Prüfpunkte |
|---|---|---|
| 02 Projektkontext | README, AGENTS und Handoff-Dateien prüfen | Sind Ziel, Grenzen, Arbeitsmodell und Codex-Regeln vollständig? |
| 02 Projektkontext | Tool-Manifest prüfen | Sind Pfade, Fork-/Upstream-Regeln und Codex-Freigaben ausreichend klar? |

## Als Nächstes

| Paket | Aufgabe | Ziel |
|---|---|---|
| 03 Repo Governance | `setup/repo-governance` erstellen | Git-, Branch-, Fork-, PR- und Codex-Workflow dokumentieren |

## Noch offen

| Paket | Aufgabe | Hinweise |
|---|---|---|
| 03 Repo Governance | `01_docs/setup/git-workflow.md` erstellen | Branches, Pull Requests, Merge-Regeln, Branch Protection |
| 03 Repo Governance | `01_docs/setup/fork-strategy.md` erstellen | `origin` vs. `upstream`, Forks, Sync-Regeln, Commit-Pinning |
| 03 Repo Governance | `01_docs/setup/codex-workflow.md` erstellen | Was Codex darf, was nicht, Standardprompt, Reviewprozess |
| 03 Repo Governance | `01_docs/setup/security-rules.md` erstellen | ROMs, Builds, Saves, Tools, Secrets, private Pfade |
| 03 Repo Governance | `01_docs/setup/workspace-rebuild.md` erstellen | Zweitrechner-/Neuaufbau-Anleitung |
| 03 Repo Governance | `07_scripts/bootstrap/bootstrap-workspace.ps1` erstellen | lokale Ordner nach Clone neu anlegen |
| 03 Repo Governance | `07_scripts/bootstrap/check-git-safety.ps1` erstellen | Branch, Status, verbotene Dateien prüfen |
| 03 Repo Governance | `07_scripts/bootstrap/check-remotes.ps1` erstellen | `origin`, `upstream`, Branches und Remotes prüfen |
| 04 Codex Start | Codex Dry Run vorbereiten | In Arbeit auf setup/codex-dry-run; Codex soll nur Docs prüfen, keine ROM-/Build-Arbeit |
| 04 Codex Start | Codex Standardprompt dokumentieren | wiederverwendbarer Prompt für kleine Arbeitsbranches |
| 05 Externe Quellen | Repos analysieren, aber noch nicht ändern | UPR FVX, Shiny-Miner, CyanSMP64, Skeli789, pret |
| 05 Externe Quellen | Entscheidung: klonen oder forken | Nur forken, wenn Änderungen nötig sind |
| 06 Toolchain | devkitPro/devkitARM prüfen | Installation und Version dokumentieren |
| 06 Toolchain | Java prüfen | notwendig für UPR FVX |
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
setup/repo-governance
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

