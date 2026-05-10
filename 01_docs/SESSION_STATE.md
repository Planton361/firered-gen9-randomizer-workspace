# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance, Codex-Dry-Run, externe Quellenprüfung, Workflow-Automation, Post-Merge-Doku-Sync, lokale Windows-Toolchain-Inventur, PATH-Follow-up, Linux/CachyOS-Workspace-Migration und Linux-Toolchain-Inventur wurden gemerged bzw. lokal übernommen.
- PR #10 `docs: sync post-merge workflow state` ist gemerged.
- PR #11 `docs: record local toolchain inventory` ist gemerged.
- PR #12 `docs: prepare path toolchain followup` ist gemerged.
- Nutzer hat die lokale Arbeitsumgebung von Windows auf Linux/CachyOS gewechselt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`setup/linux-gh-auth-refresh`

## Aktueller Arbeitsblock

Linux/CachyOS-GitHub-CLI- und Git-Auth-Refresh dokumentieren, ohne Installation, ROM-, Build-, Clone- oder Fork-Arbeit.

## Ziel

Den aktuellen Linux/CachyOS-Ist-Stand von GitHub CLI und Git-Remote-Zugriff dokumentieren:

- `gh auth status` prüfen
- `git fetch origin` prüfen
- festhalten, dass GitHub CLI und Git für Push und PR-Erstellung nutzbar sind
- keine Tokens oder Secrets dokumentieren
- Windows-Toolchain-Befunde weiterhin als historischen Referenzstand kennzeichnen
- nächsten Arbeitsblock aus den verbleibenden Linux-Toolchain-Befunden ableiten

## In diesem Arbeitsblock geprüft

- Branch `setup/linux-gh-auth-refresh` ist aktiv.
- `gh auth status` ist erfolgreich.
- GitHub CLI ist für `github.com` mit Account `Planton361` über den lokalen Keyring angemeldet.
- Git-Operationen über GitHub CLI sind auf HTTPS konfiguriert.
- `git fetch origin` ist erfolgreich.
- GitHub CLI und Git sind auf Linux/CachyOS für Push und PR-Erstellung nutzbar.
- Token-Wert und Secrets wurden nicht dokumentiert.
- Windows-Toolchain-Befunde bleiben historisch und gelten nicht als Linux-Ist-Stand.

## Noch nicht gestartet

- Linux-Toolchain installieren
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

Für diesen Dokumentationsblock nach den Änderungen prüfen:

```sh
git status --short
git diff --stat
git diff
```

Danach Branch `setup/linux-gh-auth-refresh` reviewbar committen, pushen und als PR nach `main` führen. Nicht durch Codex mergen.

## Nächster empfohlener Branch

`setup/linux-gba-toolchain-plan`

Zweck: devkitPro/devkitARM- und `arm-none-eabi-gcc`-Vorgehen für Linux/CachyOS planen, bevor Installationen oder Build-Schritte freigegeben werden.
