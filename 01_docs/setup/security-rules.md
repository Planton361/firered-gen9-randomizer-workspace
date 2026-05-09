# Security Rules

## Ziel

Dieses Dokument bündelt die Sicherheits- und Ausschlussregeln für das Workspace-Repo.

## Nie committen

Nicht in Git:

- ROMs: `*.gba`, `*.gb`, `*.gbc`
- Saves: `*.sav`, `*.srm`
- Emulator States: `*.state`, `*.ss0`, `*.ss1`
- Builds und generierte ROMs
- Tool-Binaries und Release-Archive: `*.zip`, `*.7z`, `*.exe`, `*.dll`, `*.jar`
- private `.env`-Dateien
- Tokens, private Keys, Secrets
- private absolute Pfade, wenn sie Rückschlüsse auf sensible Daten erlauben

## Tabu-Pfade

Codex und normale Projekt-Commits dürfen diese Pfade nicht bearbeiten:

```text
04_private_roms/
05_builds/
03_tools/releases/
```

## Erlaubte Artefakte

Erlaubt sind:

- Markdown-Dokumentation
- PowerShell-Scripts
- Testprotokolle ohne ROM-Daten
- Quellenindex
- Tool-Manifest mit Versionen, Pfaden, Branches und Commit-Hashes
- Hashes privater Dateien, wenn keine Datei selbst veröffentlicht wird

## Vor Commit prüfen

```powershell
git status --short
git diff --stat
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
```

## Bei Fund verbotener Dateien

Sofort stoppen.

Nicht committen.

Wenn Datei nur untracked ist:

```powershell
git status --short
```

Dann `.gitignore` prüfen und Datei lokal belassen oder entfernen.

Wenn Datei bereits staged ist:

```powershell
git restore --staged <datei>
```

Wenn Datei versehentlich committed wurde, nicht pushen und erst bereinigen.
