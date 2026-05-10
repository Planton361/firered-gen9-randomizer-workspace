# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance, Codex-Dry-Run, externe Quellenprüfung, Workflow-Automation, Post-Merge-Doku-Sync, lokale Windows-Toolchain-Inventur, PATH-Follow-up, Linux/CachyOS-Workspace-Migration, Linux-Toolchain-Inventur, Linux-GitHub-Auth-Refresh, Agent-Best-Practices-Refresh und Post-Merge-Agent-Best-Practices-Sync wurden gemerged bzw. lokal übernommen.
- PR #10 `docs: sync post-merge workflow state` ist gemerged.
- PR #11 `docs: record local toolchain inventory` ist gemerged.
- PR #12 `docs: prepare path toolchain followup` ist gemerged.
- PR #17 Agent-Best-Practices-Refresh ist gemerged.
- PR #18 Post-Merge-Agent-Best-Practices-Sync ist gemerged.
- Nutzer hat die lokale Arbeitsumgebung von Windows auf Linux/CachyOS gewechselt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`setup/linux-gba-toolchain-plan`

## Aktueller Arbeitsblock

GBA-Toolchain-Vorgehen fuer Linux/CachyOS planen, ohne Installationen oder Build-Schritte durchzufuehren.

## Ziel

Optionen und Entscheidungspunkte fuer devkitPro/devkitARM und `arm-none-eabi-gcc` dokumentieren:

- vorhandene Projektquellen und dokumentierte Toolchain-Befunde auswerten
- Plan fuer Linux/CachyOS-GBA-Toolchain erstellen
- keine Installation und keinen Build ausfuehren
- naechsten konkreten Setup-/Pruefschritt ableiten

## In diesem Arbeitsblock geprüft / geändert

- Branch `setup/linux-gba-toolchain-plan` ist der Arbeitsbranch.
- `01_docs/setup/linux-gba-toolchain-plan.md` wurde als Planungsdokument erstellt.
- Dokumentierte Optionen: devkitPro/devkitARM primaer vorbereiten, System-`arm-none-eabi-gcc` als Fallback bewerten, Build-Details bis nach Repo-Pinning verschieben.
- Naechster empfohlener Arbeitsbranch: `setup/linux-gba-toolchain-source-review`.
- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries oder Secrets wurden angefasst.
- Keine externen Repos wurden geklont.
- Keine Forks wurden angelegt.
- Keine Installationen oder Build-Schritte wurden durchgeführt.

## Noch nicht gestartet

- Linux-Toolchain installieren
- offizielle devkitPro/devkitARM-Installationsquelle fuer Linux/CachyOS festlegen
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

Danach Branch `setup/linux-gba-toolchain-plan` reviewbar committen, pushen und als PR nach `main` führen. Nicht durch Codex mergen.

## Nächster empfohlener Branch

`setup/linux-gba-toolchain-source-review`

Zweck: offizielle devkitPro/devkitARM-Dokumentation und dokumentierte Ziel-Repos read-only auf Toolchain-Anforderungen pruefen, bevor Installationen oder Build-Schritte freigegeben werden.
