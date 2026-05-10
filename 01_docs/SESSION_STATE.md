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

## Inventurstatus

| Tool | Status |
|---|---|
| PowerShell | dokumentiert vorhanden |
| Git | dokumentiert vorhanden; lokal frisch zu prüfen |
| GitHub CLI (`gh`) | dokumentiert installiert/authentifiziert; bei PATH-Problemen neues Terminal nutzen |
| Java | offen: lokal prüfen |
| make | offen: lokal prüfen |
| arm-none-eabi-gcc | offen: lokal prüfen |
| agbcc | optional/offen: lokal prüfen, falls vorhanden |
| pwsh | offen: lokal prüfen |

## Einschränkung dieser Session

Diese ChatGPT-/GitHub-Connector-Session konnte keine Befehle auf dem lokalen Windows-Workspace ausführen. Daher wurden keine lokalen Versionen erfunden und keine lokalen Toolpfade geraten. Die ausführbaren Prüfkommandos sind im Tool-Manifest dokumentiert.

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

Lokal im Windows-Workspace ausführen:

```powershell
pwsh -File .\07_scripts\bootstrap\check-git-safety.ps1
git status --short
git diff --stat
```

Danach PR `setup/toolchain-local-inventory` prüfen, nicht durch Codex mergen.
