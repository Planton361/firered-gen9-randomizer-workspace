# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Initialer Projektkontext wurde committed und gemerged.
- Roadmap-Status wurde ergänzt und gemerged.
- Repo-Governance-Dokumentation wurde vorbereitet und gemerged.
- Bootstrap-/Safety-Scripts wurden vorbereitet und gemerged.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`setup/codex-dry-run`

## Aktueller Arbeitsblock

Codex-Dry-Run vorbereiten.

## Ziel

Prüfen, ob die dokumentierten Governance-Regeln für Codex praktisch nutzbar sind, ohne externe Repos, ROMs, Saves, Builds oder Tool-Binaries anzufassen.

## In diesem Arbeitsblock vorbereitet

- `01_docs/setup/codex-dry-run.md`
- Aktualisierung von `SESSION_STATE.md`
- Aktualisierung von `NEXT_STEPS.md`
- Aktualisierung von `roadmap-status.md`

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

- `pwsh -File .\07_scripts\bootstrap\check-remotes.ps1`
- `pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1`
- `git status --short`
- `git diff --stat`
- Branch committen und als PR nach `main` führen
