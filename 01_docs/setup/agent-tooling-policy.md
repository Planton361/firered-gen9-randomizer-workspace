# Agent Tooling Policy

## Ziel

Dieses Dokument legt fest, welche Agent- und IDE-Werkzeuge im Projekt welche Rolle haben. Es soll Tool-Wildwuchs vermeiden und die bestehende Branch-/PR-Arbeitsweise stützen.

## Rollen

| Werkzeug | Rolle | Standardstatus |
|---|---|---|
| ChatGPT QA | Analyse, Review, Planung, Handoff-Prompts, PR-/Diff-Erklärung | aktiv |
| Codex CLI | primärer Worker für erlaubte Repo-Änderungen auf Arbeitsbranches | aktiv, wenn Branch freigegeben |
| GitHub CLI (`gh`) | Branch-/PR-Unterstützung, wenn lokal verfügbar | optional |
| JetBrains IDE | lokale Navigation und manuelle Bearbeitung | optional |
| JetBrains MCP | optionale read-only IDE-Kontextanalyse für Codex | optional, geprüft |
| JetBrains AI / Junie | optionaler IDE-Agent nach separater Freigabe | optional |
| Continue | optionaler lokaler Assistenz-Client | optional |
| Cursor | optionaler Editor-Agent | optional |
| Windsurf | optionaler Editor-Agent | optional |

## ChatGPT QA

ChatGPT wird als Steuerungs- und Qualitätsebene genutzt:

- Arbeitsblöcke zuschneiden
- Risiken und Stop-Regeln klären
- Codex-Prompts vorbereiten
- Diffs und PRs reviewen
- Handoff-Prompts schreiben
- Projektstatus in `SESSION_STATE.md`, `NEXT_STEPS.md` und Roadmap spiegeln

ChatGPT soll keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, Secrets oder `.env`-Inhalte erhalten.

## Codex CLI

Codex CLI ist der primäre Worker für Repo-Änderungen.

Codex darf nur arbeiten, wenn der Prompt enthält:

- Arbeitsbranch
- Ziel
- erlaubte Dateien
- Stop-Regeln
- Checks
- gewünschtes Abgabeformat

Codex darf auf freigegebenen Arbeitsbranches:

- erlaubte Dateien ändern
- lokale Checks ausführen
- committen
- pushen
- PR nach `main` erstellen, wenn `gh` verfügbar ist

Codex darf nicht:

- direkt auf `main` arbeiten
- direkt auf `main` pushen
- PRs mergen
- ROMs, Saves, Emulator States, Builds oder Tool-Binaries anfassen
- externe Repos klonen oder Forks anlegen, außer ausdrücklich freigegeben
- große Refactors ohne Freigabe durchführen

## Suggest, Auto Edit, Full Auto

### Suggest

Nutzen für:

- Analyse
- Review
- Erklärung
- kleine Textvorschläge
- riskante oder unklare Änderungen

Regel: Suggest darf keine Dateien ohne explizite Bestätigung ändern.

### Auto Edit

Nutzen für:

- kleine Dokumentationsänderungen
- klar begrenzte Script-/Config-Anpassungen
- erlaubte Dateiliste mit Review vor Commit

Regel: Auto Edit ist geeignet, wenn die Änderung klein ist und alle betroffenen Dateien im Prompt genannt sind.

### Full Auto

Nur nutzen, wenn alle Bedingungen erfüllt sind:

- Arbeitsbranch ist nicht `main`
- erlaubte Dateien sind vollständig genannt
- Stop-Regeln sind eindeutig
- keine ROM-/Build-/Tool-Binary-/Secret-Pfade betroffen
- keine externen Clones, Forks oder Installationen nötig
- Checks sind lokal verfügbar oder Fallback ist definiert

Nicht nutzen für:

- erste Toolchain-Installation
- externe Repo-Änderungen
- Build- oder ROM-Arbeit
- große Refactors
- mehrere Agenten parallel

## Optionale IDE-/Editor-Agenten

JetBrains/Junie/Continue/Cursor/Windsurf sind optional. Sie dürfen den Codex-Workflow nicht ersetzen, solange Codex CLI als primärer Worker dokumentiert ist.

Regeln:

- Nicht parallel mit Codex auf demselben Branch arbeiten.
- Nicht ohne Handoff denselben Arbeitsbaum ändern.
- Keine eigenen Tool-/MCP-Konfigurationen mit Secrets committen.
- Keine privaten IDE-Dateien committen.
- Änderungen weiterhin über Branch, Checks, Commit und PR führen.

## JetBrains MCP

Arbeitsblock `setup/intellij-mcp-readonly-check` hat lokal IntelliJ IDEA 2026.2 EAP mit gebündeltem JetBrains-MCP-Server gefunden. Die Mindestanforderung 2025.2 ist erfüllt; Codex-Auto-Configuration ist in der lokalen MCP-Server-Distribution als unterstützter Client erkennbar.

Projektregel:

- JetBrains MCP ist optional und nicht blockierend.
- Git, `rg`, Submodule-Pins und Markdown-Dokumente bleiben der Default für Codex.
- MCP darf nur read-only für Code-Navigation, Symbolsuche und IDE-Kontextanalyse genutzt werden.
- Schreibende MCP-Tools, Terminalausführung, Run Configurations, Builds, Formatierung, Patch-Anwendung und Refactorings bleiben für dieses Projekt gesperrt.
- ROM-, Save-, Emulator-State-, Build-, Tool-Binary- und Secret-Pfade dürfen nicht über MCP zugänglich gemacht werden.
- MCP-Auto-Configuration für Codex darf keine Secrets oder privaten absoluten Pfade in Git bringen.
- Auf einem Branch darf nicht gleichzeitig ein MCP-gestützter Agent und ein anderer schreibender Agent arbeiten.

## Parallelitätsregel

Pro Branch arbeitet zu einem Zeitpunkt genau ein schreibender Agent.

Wenn ein anderer Agent übernehmen soll:

1. aktuellen Status committen oder Änderungen verwerfen
2. `git status --short` prüfen
3. Handoff schreiben
4. erst dann den nächsten Agent starten

## Definition of Done

- Genutztes Tool war für die Aufgabe passend.
- Keine parallele schreibende Agent-Arbeit auf demselben Branch.
- Keine verbotenen Artefakte wurden berührt.
- Checks und Handoff sind dokumentiert.
