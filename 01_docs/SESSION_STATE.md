# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance und Codex-Dry-Run wurden gemerged.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`docs/codex-workflow-automation`

## Aktueller Arbeitsblock

Codex-/ChatGPT-/GitHub-Workflow effizienter und stärker automatisierbar dokumentieren.

## Ziel

Kurze Prompt-Vorlagen, Work-Package-Lifecycle, PR-Automation und Abschlussdokumentation als Definition of Done festhalten.

## In diesem Arbeitsblock vorbereitet

- `01_docs/quality/prompt-templates.md` neu anlegen
- `01_docs/setup/work-package-lifecycle.md` neu anlegen
- `01_docs/quality/prompt-guidelines.md` aktualisieren
- `01_docs/setup/codex-workflow.md` aktualisieren
- `01_docs/setup/git-workflow.md` aktualisieren
- `01_docs/setup/fork-strategy.md` aktualisieren
- `01_docs/quality/workflow-improvements.md` aktualisieren
- `01_docs/quality/lessons-learned.md` aktualisieren
- `01_docs/references/tool-manifest.md` aktualisieren
- `01_docs/SESSION_STATE.md` aktualisieren
- `01_docs/NEXT_STEPS.md` aktualisieren
- `00_project-control/roadmap/roadmap-status.md` aktualisieren

## Noch nicht gestartet

- externe Repos klonen
- Forks anlegen
- devkitPro-Build testen
- UPR FVX testen
- Hex Maniac Advance prüfen
- BizHawk/Ironmon testen
- ROMs oder Builds bearbeiten
- PR mergen

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine externen Repos geklont.

Keine Forks angelegt.

Keine Änderungen direkt auf `main`.

## Nächste Prüfung

- `pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1`
- `git status --short`
- `git diff --stat`
- Branch committen, pushen und als PR nach `main` führen
