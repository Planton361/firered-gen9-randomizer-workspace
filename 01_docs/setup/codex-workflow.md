# Codex Workflow

## Ziel

Dieses Dokument beschreibt, wie Codex im Projekt eingesetzt wird.

## Grundsatz

Codex arbeitet nur auf freigegebenen Arbeitsbranches und nur an klar abgegrenzten Aufgaben.

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

## Standardprompt

```text
Lies README.md, AGENTS.md, 01_docs/PROJECT_BRIEF.md, 01_docs/SESSION_STATE.md und 01_docs/NEXT_STEPS.md.

Aufgabe: <klar abgegrenzte Aufgabe>

Erlaubte Dateien:
<konkrete Liste>

Verboten:
ROMs, Saves, Builds, Tool-Binaries, externe Downloads, private Pfade, Secrets, Änderungen direkt auf main.

Abgabeformat:
Summary, geänderte Dateien, Checks/Tests, Risiken/Annahmen, nächster minimaler Schritt.
```

## Erwartete Codex-Abgabe

Codex soll immer liefern:

- Summary
- geänderte Dateien
- ausgeführte Checks
- Risiken/Annahmen
- nächsten minimalen Schritt

## Nach Codex-Änderungen

Lokal prüfen:

```powershell
git status --short
git diff --stat
git diff
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
```

Erst danach committen.
