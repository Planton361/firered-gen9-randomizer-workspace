# Codex Workflow

## Ziel

Dieses Dokument beschreibt, wie Codex im Projekt eingesetzt wird.

## Grundsatz

Codex arbeitet nur auf freigegebenen Arbeitsbranches und nur an klar abgegrenzten Aufgaben.

Auf freigegebenen Branches darf Codex die Arbeit vollständig durchführen: Branches erstellen, erlaubte Dateien ändern, Checks ausführen, committen, pushen und Pull Requests erstellen.

Codex darf niemals direkt auf `main` arbeiten, direkt auf `main` pushen oder PRs mergen.

Bei unerwarteten Änderungen im Arbeitsbaum muss Codex stoppen und den Fund melden, bevor weitere Änderungen erfolgen.

## Vor Codex-Aufgaben

Vor jeder Codex-Änderung müssen gelesen werden:

1. `README.md`
2. `AGENTS.md`
3. `01_docs/PROJECT_BRIEF.md`
4. `01_docs/SESSION_STATE.md`
5. `01_docs/NEXT_STEPS.md`

## Erlaubt

Codex darf:

- Dokumentation verbessern
- kleine PowerShell-Scripts schreiben
- freigegebene Arbeitsbranches erstellen
- erlaubte Dateien auf freigegebenen Branches ändern
- lokale Checks ausführen
- Änderungen committen und pushen
- Pull Requests nach `main` erstellen
- Diffs erklären
- PR-Beschreibungen vorbereiten
- Tool-Manifest und Quellenindex pflegen
- Build- oder Fehlerlogs analysieren, wenn der Nutzer sie bereitstellt

## Verboten

Codex darf nicht:

- direkt auf `main` arbeiten
- direkt auf `main` pushen
- ROMs lesen, kopieren, ändern oder committen
- Saves, Emulator States oder Builds committen
- `04_private_roms/`, `05_builds/` oder `03_tools/releases/` bearbeiten
- Secrets, Tokens, `.env` oder private Keys veröffentlichen
- große Refactors ohne ausdrückliche Freigabe durchführen
- externe Repos ohne Freigabe klonen oder ändern
- PRs mergen

## Standardprompt

```text
Lies README.md, AGENTS.md, 01_docs/PROJECT_BRIEF.md, 01_docs/SESSION_STATE.md und 01_docs/NEXT_STEPS.md.

Aufgabe: <klar abgegrenzte Aufgabe>

Erlaubte Dateien:
<konkrete Liste>

Verboten:
ROMs, Saves, Builds, Tool-Binaries, externe Downloads, private Pfade, Secrets, Änderungen direkt auf main.

Abgabeformat:
Summary, geänderte Dateien, Checks/Tests, Risiken/Annahmen, PR-Link oder PR-Befehl, Handoff-Prompt.
```

## Erwartete Codex-Abgabe

Codex soll immer liefern:

- Summary
- geänderte Dateien
- ausgeführte Checks
- Risiken/Annahmen
- PR-Link oder PR-Befehl, wenn ein PR erwartet wird
- Handoff-Prompt für den nächsten Chat

## Nach Codex-Änderungen

Lokal prüfen:

```powershell
git status --short
git diff --stat
git diff
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
```

Erst danach committen, pushen und PR erstellen. Nicht selbst mergen.

## Arbeitspaket-Lifecycle

Siehe `01_docs/setup/work-package-lifecycle.md`.
