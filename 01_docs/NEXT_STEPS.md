# Next Steps

## Aktueller Arbeitsblock

Read-only-Analyse externer Quellen abschließen und per Pull Request nach `main` führen.

## Nächste Schritte

1. `source-index.md` prüfen.
2. `tool-manifest.md` prüfen.
3. Sicherstellen, dass kein Clone/Fork/Download erfolgt ist.
4. Lokale Checks ausführen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-remotes.ps1
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

5. Branch committen und pushen:

```powershell
git add 01_docs/references/source-index.md 01_docs/references/tool-manifest.md 01_docs/SESSION_STATE.md 01_docs/NEXT_STEPS.md 00_project-control/roadmap/roadmap-status.md
git commit -m "docs: record external source read-only analysis"
git push -u origin analysis/external-sources-readonly
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

- entscheiden, welche externe Quelle zuerst lokal geklont wird
- bevorzugt: nur eine Quelle pro Branch
- vor Clone Branch/Commit/Ort im Tool-Manifest festlegen

## Quality

- Quality-Dokumente prüfen und ersten echten Lesson-Learned-Eintrag erst nach dem nächsten konkreten Projektfehler oder Workflow-Reibungsverlust schreiben.
