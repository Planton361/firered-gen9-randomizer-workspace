# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance, Codex-Dry-Run, externe Quellenprüfung, Workflow-Automation, Post-Merge-Doku-Sync, lokale Windows-Toolchain-Inventur, PATH-Follow-up und Linux/CachyOS-Workspace-Migration wurden gemerged bzw. lokal übernommen.
- PR #10 `docs: sync post-merge workflow state` ist gemerged.
- PR #11 `docs: record local toolchain inventory` ist gemerged.
- PR #12 `docs: prepare path toolchain followup` ist gemerged.
- Nutzer hat die lokale Arbeitsumgebung von Windows auf Linux/CachyOS gewechselt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`setup/linux-toolchain-inventory`

## Aktueller Arbeitsblock

Read-only Linux/CachyOS-Toolchain-Inventur dokumentieren, ohne Installation, ROM-, Build-, Clone- oder Fork-Arbeit.

## Ziel

Den aktuellen Linux/CachyOS-Ist-Stand der lokal erreichbaren Basis-Tools dokumentieren:

- Git, GitHub CLI, Shell, Java und `make` mit Versionen bzw. Pfad erfassen
- fehlende oder nicht erreichbare Tools dokumentieren
- GitHub-CLI-Auth-Status ohne Secrets dokumentieren
- Windows-Toolchain-Befunde weiterhin als historischen Referenzstand kennzeichnen
- nächsten Arbeitsblock aus den Linux-Befunden ableiten

## In diesem Arbeitsblock geprüft

- Branch `setup/linux-toolchain-inventory` wurde von lokalem `main` erstellt.
- Git ist unter `/usr/bin/git` erreichbar: Git 2.54.0.
- GitHub CLI ist unter `/usr/bin/gh` erreichbar: gh 2.92.0.
- `gh auth status` meldet für `github.com` den Account `Planton361` als aktiv, aber den gespeicherten Token als ungültig.
- Aktuelle Shell laut `$SHELL`: `/bin/fish`.
- Java ist unter `/usr/bin/java` erreichbar: OpenJDK 26.0.1.
- `make` ist unter `/usr/bin/make` erreichbar: GNU Make 4.4.1.
- `arm-none-eabi-gcc` wurde im PATH nicht gefunden.
- `agbcc` wurde im PATH nicht gefunden.
- `pwsh` wurde im PATH nicht gefunden.
- Windows-Toolchain-Befunde bleiben historisch und gelten nicht als Linux-Ist-Stand.

## Noch nicht gestartet

- Linux-Toolchain installieren
- GitHub CLI neu authentifizieren
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
```

Danach Branch `setup/linux-toolchain-inventory` reviewbar committen und als PR nach `main` führen. Nicht durch Codex mergen.

## Nächster empfohlener Branch

`setup/linux-gh-auth-refresh`

Zweck: GitHub CLI auf Linux neu authentifizieren bzw. Auth-Status reparieren, damit spätere PR- und CI-Workflows wieder reproduzierbar über `gh` laufen. Keine Tokens dokumentieren.
