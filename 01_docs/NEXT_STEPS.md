# Next Steps

## Aktueller Arbeitsblock

Codex-Dry-Run vorbereiten und per Pull Request nach `main` führen.

## Nächste Schritte

1. `01_docs/setup/codex-dry-run.md` prüfen.
2. Dry-Run-Prompt lokal für Codex verwenden.
3. Prüfen, ob Codex die erlaubten und verbotenen Bereiche korrekt einhält.
4. Lokale Checks ausführen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-remotes.ps1
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

5. Branch committen und pushen:

```powershell
git add 01_docs/setup/codex-dry-run.md 01_docs/SESSION_STATE.md 01_docs/NEXT_STEPS.md 00_project-control/roadmap/roadmap-status.md
git commit -m "docs: add codex dry run"
git push -u origin setup/codex-dry-run
```

6. Pull Request nach `main` erstellen.

## Nicht tun

- keine ROMs bewegen
- keine Builds starten
- keine externen Repos klonen
- keine Forks verändern
- keine Tool-Binaries committen
- keine Änderungen direkt auf `main`

## Danach

Nächster sinnvoller Arbeitsblock:

- externe Quellen read-only analysieren
- Source Index und Tool Manifest schrittweise präzisieren
- erst danach entscheiden, ob Repos geklont oder geforkt werden
