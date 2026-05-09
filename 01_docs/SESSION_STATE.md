# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Initialer Projektkontext wurde committed und gemerged.
- `roadmap-status.md` wurde ergänzt und gemerged.
- Alte Setup-/Roadmap-Branches wurden bereinigt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.
- Aktueller Arbeitsblock: Repo-Governance, Codex-Workflow und Bootstrap-/Safety-Scripts.

## Aktueller Branch

`setup/repo-governance`

## In diesem Arbeitsblock vorbereitet

- `01_docs/setup/git-workflow.md`
- `01_docs/setup/fork-strategy.md`
- `01_docs/setup/codex-workflow.md`
- `01_docs/setup/security-rules.md`
- `01_docs/setup/workspace-rebuild.md`
- `07_scripts/bootstrap/bootstrap-workspace.ps1`
- `07_scripts/bootstrap/check-git-safety.ps1`
- `07_scripts/bootstrap/check-remotes.ps1`

## Noch nicht gestartet

- externe Repos klonen
- Forks anlegen
- devkitPro-Build testen
- UPR FVX testen
- Hex Maniac Advance prüfen
- BizHawk/Ironmon testen
- ROMs oder Builds bearbeiten

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

## Nächste Prüfung

- `git status --short`
- `git diff --stat`
- `pwsh -File .\07_scripts\bootstrap\check-remotes.ps1`
- `pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1`
- Branch committen und als PR nach `main` führen
