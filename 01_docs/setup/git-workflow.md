# Git Workflow

## Ziel

Dieses Dokument beschreibt den Standard-Git-Workflow für das Workspace-Repo.

## Grundregeln

- `main` ist stabil und geschützt.
- Änderungen erfolgen nicht direkt auf `main`.
- Jeder Arbeitsblock nutzt einen sprechenden Branch.
- Änderungen werden per Pull Request nach `main` geführt.
- Force-Push auf `main` ist verboten.
- ROMs, Saves, Builds, Tool-Binaries, Secrets und `.env`-Dateien werden nicht committed.

## Branch-Namen

Empfohlene Präfixe:

- `setup/...`
- `docs/...`
- `analysis/...`
- `compat/...`
- `randomizer/...`
- `build/...`
- `experiment/...`

## Standardablauf

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
git status --short
git switch -c setup/<thema>
```

Vor jedem Commit:

```powershell
git status --short
git diff --stat
git diff
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
```

Commit und Push:

```powershell
git add <dateien>
git status --short
git commit -m "docs: add repo governance workflow"
git push -u origin setup/<thema>
```

## Pull Request

Mit GitHub CLI:

```powershell
gh pr create --base main --head setup/<thema> --title "<kurzer Titel>" --body "<Summary, Dateien, Checks, Risiken, nächster Schritt>"
```

Der PR soll enthalten:

- Ziel des Branches
- geänderte Dateien
- Checks/Tests
- Risiken
- offene Folgeaufgaben

## Nach Merge

```powershell
git switch main
git pull --ff-only origin main
git branch -d setup/<thema>
git push origin --delete setup/<thema>
git status --short
```

Remote-Branch nur löschen, wenn der PR gemerged ist und keine Folgearbeit auf diesem Branch offen ist.

Wenn mehrere Arbeitsbranches offen sind, nur den gerade gemergten Branch bereinigen.
