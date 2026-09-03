> **LEGACY / SUPPORTING GUIDANCE:** The canonical work-package lifecycle and
> Definition of Done are in [docs/ENGINEERING_RULES.md](../../docs/ENGINEERING_RULES.md)
> and [docs/milestones/M-000R.md](../../docs/milestones/M-000R.md). Historical
> guidance below is retained for evidence and does not override them.

# Work Package Lifecycle

## Ziel

Ein Arbeitspaket soll klein genug sein, um in einem Branch geprüft, committed und als PR nach `main` geführt zu werden.

## Ablauf

1. Kontext lesen:
   - `README.md`
   - `AGENTS.md`
   - `01_docs/PROJECT_BRIEF.md`
   - `01_docs/SESSION_STATE.md`
   - `01_docs/NEXT_STEPS.md`
2. Branch prüfen:
   - nicht auf `main` arbeiten
   - bei unerwarteten Änderungen stoppen
3. Aufgabe ausführen:
   - nur freigegebene Dateien ändern
   - keine ROMs, Saves, Builds, Tool-Binaries oder Secrets anfassen
   - zusammengehörige Änderungen bündeln
4. Abschlussdokumentation aktualisieren:
   - `01_docs/SESSION_STATE.md`
   - `01_docs/NEXT_STEPS.md`
   - `00_project-control/roadmap/roadmap-status.md`, wenn sich Status ändert
   - `01_docs/references/tool-manifest.md`, wenn Tools, Repos, Branches oder Commits betroffen sind
5. Prüfen:
   - `git status --short`
   - `git diff --stat`
   - `pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1`
6. Commit und PR:
   - sprechende Commit Message
   - Branch pushen
   - PR nach `main` erstellen
   - nicht selbst mergen
7. Handoff-Prompt liefern:
   - aktueller Branch/PR
   - Checks
   - Risiken
   - nächster minimaler Schritt

## Stop-Regeln

Sofort stoppen, wenn:

- der aktuelle Branch `main` ist
- unerwartete geänderte Dateien auftauchen
- verbotene Dateien im Status erscheinen
- ein Check private Artefakte, Builds, ROMs, Saves oder Tool-Binaries meldet
- die Aufgabe externe Repos oder Forks braucht, aber keine dokumentierte Entscheidung existiert

## Definition of Done

- Änderung ist klein und reviewbar.
- Alle betroffenen Statusdokumente sind aktuell.
- Checks wurden frisch ausgeführt.
- Commit existiert auf dem Arbeitsbranch.
- PR nach `main` existiert oder der exakte PR-Befehl ist dokumentiert.
- Ein Handoff-Prompt für den nächsten Chat liegt vor.
