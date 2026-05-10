# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance, Codex-Dry-Run, externe Quellenprüfung, Workflow-Automation, Post-Merge-Doku-Sync, lokale Windows-Toolchain-Inventur und PATH-Follow-up wurden gemerged.
- PR #10 `docs: sync post-merge workflow state` ist gemerged.
- PR #11 `docs: record local toolchain inventory` ist gemerged.
- PR #12 `docs: prepare path toolchain followup` ist gemerged.
- Nutzer hat die lokale Arbeitsumgebung von Windows auf Linux/CachyOS gewechselt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`setup/linux-workspace-migration`

## Aktueller Arbeitsblock

Dokumentation und Projektsteuerung auf Linux/CachyOS-first umstellen, ohne Installation, ROM-, Build-, Clone- oder Fork-Arbeit.

## Ziel

Den OS-Wechsel als Governance-Änderung dokumentieren und Windows-Pfade als historischen Stand kennzeichnen:

- Linux/CachyOS als neue primäre lokale Umgebung
- POSIX-Shell als Standard für neue lokale Arbeitsschritte
- bisherige Windows-/PowerShell-Toolchain-Inventur als historisch markieren
- nächsten Arbeitsblock auf Linux-Toolchain-Inventur ausrichten

## In diesem Arbeitsblock vorbereitet

- Branch `setup/linux-workspace-migration` wurde von aktuellem Stand nach PR #12 erstellt.
- README und AGENTS-Regeln wurden auf Linux/CachyOS-first umgestellt.
- Workflow- und Setup-Dokumente werden für POSIX-Shell-Kommandos angepasst.
- Tool-Manifest, Roadmap und Next Steps werden auf Linux-Inventur statt Windows-PATH-Follow-up umgestellt.

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

Für diesen Dokumentationsblock prüfen:

```sh
git status --short
git diff --stat
# optional, falls pwsh installiert ist:
pwsh -File ./07_scripts/bootstrap/check-git-safety.ps1
```

Danach Branch `setup/linux-workspace-migration` reviewbar committen und als PR nach `main` führen. Nicht durch Codex mergen.
