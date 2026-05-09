# Workspace Rebuild

## Ziel

Dieses Dokument beschreibt, wie der Workspace auf einem neuen Rechner sicher wiederhergestellt wird.

## Voraussetzungen

- Git installiert
- Windows PowerShell verfügbar
- Zugriff auf das private GitHub-Repo
- keine ROMs, Saves, Builds oder Tool-Binaries im Repo erwartet

## Clone

```powershell
Set-Location "$HOME\romhacking"
git clone git@github.com:Planton361/firered-gen9-randomizer-workspace.git fr-rando-gen9
Set-Location ".\fr-rando-gen9"
```

## Lokale Ordner wiederherstellen

```powershell
pwsh -File .\07_scripts\bootstrap\bootstrap-workspace.ps1
```

Der Bootstrap legt nur lokale Arbeitsordner an. Er klont keine externen Repos und lädt keine Tools herunter.

## Sicherheitscheck

```powershell
pwsh -File .\07_scripts\bootstrap\check-remotes.ps1
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1 -AllowMain
```

`-AllowMain` ist für reine Checks nach einem frischen Clone erlaubt. Für Arbeitsänderungen soll danach ein Branch erstellt werden.

## Private Dateien

Private Dateien werden manuell ergänzt und nie committed:

```text
04_private_roms/
05_builds/
03_tools/releases/
```

## Externe Repos

Externe Repos werden erst nach dokumentierter Entscheidung geklont oder geforkt.

Vor produktiver Nutzung dokumentieren:

- Repo-URL
- Branch
- Commit-Hash
- lokaler Pfad
- Zweck
- ob Codex Änderungen durchführen darf

Ablage: `01_docs/references/tool-manifest.md`.
