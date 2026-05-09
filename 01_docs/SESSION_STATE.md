# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance und Codex-Dry-Run wurden gemerged.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`analysis/external-sources-readonly`

## Aktueller Arbeitsblock

Externe Quellen read-only bewerten und Dokumentation präzisieren.

## Ziel

Quellenlage für Randomizer, FireRed-Gen9-Basis, Upstream-Referenzen, Emulator und Tracker dokumentieren, ohne externe Repos zu klonen oder Forks anzulegen.

## In diesem Arbeitsblock vorbereitet

- `01_docs/references/source-index.md` aktualisieren
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

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine externen Repos geklont.

Keine Forks angelegt.

## Nächste Prüfung

- `pwsh -File .\07_scripts\bootstrap\check-remotes.ps1`
- `pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1`
- `git status --short`
- `git diff --stat`
- Branch committen und als PR nach `main` führen
