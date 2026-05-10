# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance, Codex-Dry-Run, externe Quellenprüfung, Workflow-Automation, Post-Merge-Doku-Sync, lokale Windows-Toolchain-Inventur, PATH-Follow-up, Linux/CachyOS-Workspace-Migration, Linux-Toolchain-Inventur, Linux-GitHub-Auth-Refresh und Agent-Best-Practices-Refresh wurden gemerged bzw. lokal übernommen.
- PR #10 `docs: sync post-merge workflow state` ist gemerged.
- PR #11 `docs: record local toolchain inventory` ist gemerged.
- PR #12 `docs: prepare path toolchain followup` ist gemerged.
- PR #17 Agent-Best-Practices-Refresh ist gemerged.
- Nutzer hat die lokale Arbeitsumgebung von Windows auf Linux/CachyOS gewechselt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`docs/post-merge-agent-best-practices-sync`

## Aktueller Arbeitsblock

Post-Merge-Dokumentationsstatus nach gemergtem PR #17 synchronisieren. Keine neuen Workflow-Regeln einführen.

## Ziel

Den aktuellen Stand auf main/post-merge-synchronisiert setzen:

- Agent-Best-Practices-Refresh als gemerged/erledigt markieren
- aktuellen Arbeitsblock auf Post-Merge-Sync setzen
- nächsten Arbeitsbranch `setup/linux-gba-toolchain-plan` bestätigen
- keine neuen Workflow-Regeln ergänzen

## In diesem Arbeitsblock geprüft / geändert

- Branch `docs/post-merge-agent-best-practices-sync` ist der Arbeitsbranch.
- Stand nach gemergtem PR #17 wurde auf main/post-merge-synchronisiert gesetzt.
- Agent-Best-Practices-Refresh wurde als erledigt dokumentiert.
- Nächster empfohlener Arbeitsbranch bleibt `setup/linux-gba-toolchain-plan`.
- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries oder Secrets wurden angefasst.
- Keine externen Repos wurden geklont.
- Keine Forks wurden angelegt.
- Keine Installationen oder Build-Schritte wurden durchgeführt.

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
- JetBrains MCP evaluieren

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine externen Repos geklont.

Keine Forks angelegt.

Keine Änderungen direkt auf `main`.

Keine MCP-Configs mit Secrets angelegt.

## Nächste Prüfung

Für diesen Dokumentationsblock nach den Änderungen prüfen:

```sh
git status --short
git diff --stat
# falls im aktuellen Linux-Setup verfügbar:
07_scripts/bootstrap/check-git-safety.ps1 oder vorhandenes Safety-Check-Fallback
```

Danach Branch `docs/post-merge-agent-best-practices-sync` reviewbar committen, pushen und als PR nach `main` führen. Nicht durch Codex mergen.

## Nächster empfohlener Branch

`setup/linux-gba-toolchain-plan`

Zweck: devkitPro/devkitARM- und `arm-none-eabi-gcc`-Vorgehen für Linux/CachyOS planen, bevor Installationen oder Build-Schritte freigegeben werden.
