# AGENTS.md

## Projektkontext

Dieses Repository steuert einen dokumentierten Workspace für einen Pokémon FireRed Gen9 Randomizer-Hack.

Ziel:
- FireRed-basierter Custom Hack
- Gen9-Pokémon über CFRU/DPE-nahe Basis prüfen
- Universal Pokémon Randomizer FVX als Haupt-Randomizer-Kandidat
- spätere Kompatibilität mit BizHawk und Ironmon Tracker
- reproduzierbarer GitHub-/Linux-/Codex-Workflow

## Grundregeln

Codex darf:

- Dokumentation lesen und verbessern
- kleine, reviewbare Änderungen auf Arbeitsbranches machen
- kleine Shell-Scripts für Setup und Checks schreiben
- Tool- und Quellenmanifest pflegen
- Diffs erklären
- PR-Beschreibungen vorbereiten
- Build- oder Fehlerlogs analysieren, wenn der Nutzer sie bereitstellt

Codex darf nicht:

- direkt auf `main` arbeiten
- direkt auf `main` pushen
- ROMs lesen, kopieren, ändern oder committen
- Saves, Emulator States oder Builds committen
- Dateien in `04_private_roms/`, `05_builds/` oder `03_tools/releases/` bearbeiten
- private Zugangsdaten oder lokale Geheimnisse veröffentlichen
- große Refactors ohne ausdrückliche Freigabe durchführen
- mehrere externe Repos gleichzeitig ändern

## Vor jeder Änderung

1. README.md lesen
2. PROJECT_BRIEF.md lesen
3. SESSION_STATE.md lesen
4. NEXT_STEPS.md lesen
5. geplante Änderung kurz zusammenfassen
6. betroffene Dateien nennen
7. Risiken nennen

## Nach jeder Änderung

1. `git status --short`
2. `git diff --stat`
3. Änderung kurz zusammenfassen
4. Checks oder Tests nennen
5. nächsten sinnvollen Schritt nennen

## Terminal

Primäre Shell: Linux/CachyOS Standard-Shell.

POSIX-Shell-kompatible Kommandos bevorzugen:

- `mkdir -p`
- `cat`
- `test`
- `find`
- `sha256sum`

PowerShell-Kommandos bleiben nur für historische Windows-Arbeitsblöcke oder wenn ein Script ausdrücklich PowerShell verlangt. In neuen Arbeitsblöcken keine Windows-Pfade als bestätigten Ist-Stand übernehmen.

## Git-Regeln

- `main` ist stabil.
- Arbeit erfolgt auf Branches.
- Branch-Namen sollen sprechend sein:
  - `setup/...`
  - `docs/...`
  - `analysis/...`
  - `compat/...`
  - `randomizer/...`
  - `build/...`
  - `experiment/...`
- Änderungen sollen per Pull Request nach `main`.
- Keine Force Pushes auf `main`.

## Multi-Repo-Regel

Für Forks gilt:

- `origin` zeigt auf den eigenen Fork.
- `upstream` zeigt auf das Originalrepo.
- Änderungen an Forks nur auf Arbeitsbranches.
- Das Workspace-Repo dokumentiert Forks, Branches und Commit-Hashes im Tool-Manifest.
