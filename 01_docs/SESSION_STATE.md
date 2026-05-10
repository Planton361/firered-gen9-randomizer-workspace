# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance, Codex-Dry-Run, externe Quellenprüfung, Workflow-Automation und Post-Merge-Doku-Sync wurden gemerged.
- PR #10 `docs: sync post-merge workflow state` ist gemerged.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`setup/toolchain-local-inventory`

## Aktueller Arbeitsblock

Lokale Toolchain-/Workspace-Inventur dokumentieren, ohne ROM-, Build-, Clone- oder Fork-Arbeit.

## Ziel

Vorhandene und noch lokal zu prüfende Tools im Tool-Manifest nachvollziehbar erfassen:

- PowerShell
- Git
- GitHub CLI
- Java
- make
- arm-none-eabi-gcc
- agbcc, falls vorhanden
- pwsh

## In diesem Arbeitsblock vorbereitet

- `main` wurde gegen den Merge-Commit von PR #10 geprüft und ist remote aktuell.
- Branch `setup/toolchain-local-inventory` wurde von `main` erstellt.
- `01_docs/references/tool-manifest.md` wurde um eine lokale Toolchain-Inventur erweitert.
- Bekannte Vorinformationen wurden nicht als frisch verifizierte lokale Checks ausgegeben, sondern getrennt dokumentiert.
- Für offene lokale Toolprüfungen wurden PowerShell-Prüfbefehle dokumentiert.
- Lokale Windows-Checks und Inventurbefehle wurden anschließend auf dem Branch ausgeführt.
- Lokal bestätigte Versionen und Pfade wurden im Tool-Manifest nachgetragen.

## Inventurstatus

| Tool | Status |
|---|---|
| PowerShell | lokal bestätigt: 5.1.26100.8328 |
| Git | lokal bestätigt: 2.54.0 unter `c:\devkitPro\msys2\usr\bin\git.exe` |
| GitHub CLI (`gh`) | lokal bestätigt: 2.92.0 und authentifiziert, aber nicht im aktuellen PATH |
| Java | lokal bestätigt: Temurin OpenJDK 25.0.3+9 LTS |
| make | lokal bestätigt: GNU Make 4.4.1 |
| arm-none-eabi-gcc | nicht im aktuellen PATH gefunden |
| agbcc | optional; nicht im aktuellen PATH gefunden |
| pwsh | lokal bestätigt: 7.6.1 |

## Noch nicht gestartet

- externe Repos klonen
- Forks anlegen
- devkitPro-Build testen
- UPR FVX testen
- Hex Maniac Advance prüfen
- BizHawk/Ironmon testen
- ROMs oder Builds bearbeiten
- PR mergen

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine externen Repos geklont.

Keine Forks angelegt.

Keine Änderungen direkt auf `main`.

## Nächste Prüfung

Vor PR-Abschluss erneut prüfen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

Danach PR `setup/toolchain-local-inventory` prüfen, nicht durch Codex mergen.
