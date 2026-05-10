# Next Steps

## Aktueller Arbeitsblock

Codex-/ChatGPT-/GitHub-Workflow-Automation abschließen und per Pull Request nach `main` führen.

## Nächste Schritte

1. Neue Prompt-Templates und Work-Package-Lifecycle prüfen.
2. Sicherstellen, dass Workflow-Regeln kurz, nutzbar und konsistent sind.
3. Sicherstellen, dass kein Clone/Fork/Download erfolgt ist.
4. Lokale Checks ausführen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

5. Branch committen und pushen:

```powershell
git add AGENTS.md 01_docs/setup/codex-workflow.md 01_docs/setup/git-workflow.md 01_docs/setup/fork-strategy.md 01_docs/setup/work-package-lifecycle.md 01_docs/quality/prompt-guidelines.md 01_docs/quality/prompt-templates.md 01_docs/quality/workflow-improvements.md 01_docs/quality/lessons-learned.md 01_docs/references/tool-manifest.md 01_docs/SESSION_STATE.md 01_docs/NEXT_STEPS.md 00_project-control/roadmap/roadmap-status.md
git commit -m "docs: improve codex workflow automation"
git push -u origin docs/codex-workflow-automation
```

6. Pull Request nach `main` erstellen:

```powershell
gh pr create --base main --head docs/codex-workflow-automation --title "docs: improve codex workflow automation" --body "<Summary, Dateien, Checks, Risiken, nächster Schritt>"
```

## Nicht tun

- keine ROMs bewegen
- keine Builds starten
- keine externen Repos klonen
- keine Forks verändern
- keine Tool-Binaries committen
- keine Änderungen direkt auf `main`

## Danach

Nächster sinnvoller Arbeitsblock:

- gemergten PR nachbereiten
- `main` aktualisieren
- gemergten Branch lokal und remote bereinigen
- nächsten kleinen Arbeitsblock aus `prompt-templates.md` starten

## Quality

- Handoff-Prompt am Ende jedes Arbeitspakets mitgeben.
- Abschlussdokumentation ist Teil der Definition of Done.
