# Next Steps

## Aktueller Arbeitsblock

Repo-Governance fertigstellen und per Pull Request nach `main` führen.

## Nächste Schritte

1. Neue Governance-Dokumente prüfen:
   - `01_docs/setup/git-workflow.md`
   - `01_docs/setup/fork-strategy.md`
   - `01_docs/setup/codex-workflow.md`
   - `01_docs/setup/security-rules.md`
   - `01_docs/setup/workspace-rebuild.md`

2. Bootstrap-/Safety-Scripts prüfen:
   - `07_scripts/bootstrap/bootstrap-workspace.ps1`
   - `07_scripts/bootstrap/check-git-safety.ps1`
   - `07_scripts/bootstrap/check-remotes.ps1`

3. Checks ausführen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-remotes.ps1
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

4. Commit und Push vorbereiten:

```powershell
git add 01_docs/setup 07_scripts/bootstrap 01_docs/SESSION_STATE.md 01_docs/NEXT_STEPS.md 00_project-control/roadmap/roadmap-status.md
git commit -m "docs: add repo governance workflow"
git push -u origin setup/repo-governance
```

5. Pull Request nach `main` erstellen und prüfen.

## Nicht tun

- keine ROMs bewegen
- keine Builds starten
- keine externen Repos klonen
- keine Forks verändern
- keine Tool-Binaries committen
- keine Änderungen direkt auf `main`

## Danach

Nächster sinnvoller Arbeitsblock:

- Codex-Dry-Run mit den neuen Governance-Regeln
- optional: `.codex/config.toml` konservativ dokumentieren
- danach erst externe Quellen read-only analysieren
