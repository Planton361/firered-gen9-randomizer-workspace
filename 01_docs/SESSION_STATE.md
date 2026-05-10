# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance, Codex-Dry-Run, externe Quellenprüfung, Workflow-Automation, Post-Merge-Doku-Sync, lokale Windows-Toolchain-Inventur, PATH-Follow-up, Linux/CachyOS-Workspace-Migration, Linux-Toolchain-Inventur, Linux-GitHub-Auth-Refresh, Agent-Best-Practices-Refresh, Post-Merge-Agent-Best-Practices-Sync und Linux-GBA-Toolchain-Plan wurden gemerged bzw. lokal übernommen.
- PR #10 `docs: sync post-merge workflow state` ist gemerged.
- PR #11 `docs: record local toolchain inventory` ist gemerged.
- PR #12 `docs: prepare path toolchain followup` ist gemerged.
- PR #17 Agent-Best-Practices-Refresh ist gemerged.
- PR #18 Post-Merge-Agent-Best-Practices-Sync ist gemerged.
- PR #19 Linux-GBA-Toolchain-Plan ist gemerged.
- Nutzer hat die lokale Arbeitsumgebung von Windows auf Linux/CachyOS gewechselt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`planning/workspace-build-randomizer-integration`

## Aktueller Arbeitsblock

Workspace-Build- und Randomizer-Integration planen, ohne Installationen, Builds, ROM-Zugriffe, externe Clones oder Forks auszuführen.

## Ziel

Konkreten Integrationsplan erstellen für:

- lokale private FireRed-ROM-Basis
- devkitPro/devkitARM als spätere GBA-Build-Toolchain
- Complete FireRed Upgrade und Dynamic Pokemon Expansion Gen9 als spaetere Build-Basis
- Universal Pokemon Randomizer FVX als Randomizer-Kandidat
- Zielstruktur fuer `02_external/`, `03_tools/`, `04_private_roms/`, `05_builds/` und `08_tests/`
- Folge-Arbeitspakete bis zum ersten Build-/Randomizer-Smoke-Test

## In diesem Arbeitsblock geprüft / geändert

- Branch `planning/workspace-build-randomizer-integration` wurde von aktuellem `main` erstellt.
- `01_docs/setup/workspace-build-randomizer-integration-plan.md` wurde erstellt.
- Workspace-Zielstruktur, Git-/Lokalgrenzen, ROM-Hash-Vorgehen, devkitPro/devkitARM-Pruefpunkte, CFRU/DPE-Gen9-Strategie und UPR-FVX-Strategie wurden geplant.
- `01_docs/references/tool-manifest.md` wurde auf den Integrationsplan synchronisiert.
- `01_docs/references/source-index.md` wurde um die Integrationsentscheidung und Nutzung der bestehenden Quellen ergänzt.
- `00_project-control/roadmap/roadmap-status.md` wurde auf den aktuellen Planungsblock fortgeschrieben.
- `01_docs/NEXT_STEPS.md` wurde auf die Folge-Arbeitspakete aktualisiert.
- Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries oder Secrets wurden angefasst.
- Keine externen Repos wurden geklont.
- Keine Forks wurden angelegt.
- Keine Installationen oder Build-Schritte wurden durchgeführt.

## Noch nicht gestartet

- devkitPro/devkitARM installieren
- externe Repos klonen
- Forks anlegen
- UPR-FVX-JAR beschaffen oder bauen
- UPR FVX testen
- CFRU/DPE lokal bauen
- private FireRed-ROM hashen
- erste Patch-/Build-Smoke-Tests ausführen
- Randomizer-Kompatibilität testen
- Hex Maniac Advance prüfen
- BizHawk/Ironmon testen
- PR mergen

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen oder gelesen.

Keine externen Repos geklont.

Keine Forks angelegt.

Keine Änderungen direkt auf `main`.

Keine Installationen oder Builds durchgeführt.

Keine MCP-Configs mit Secrets angelegt.

## Nächste Prüfung

Für diesen Dokumentationsblock nach den Änderungen prüfen:

```sh
git status --short
git diff --stat
# falls im aktuellen Linux-Setup verfügbar:
07_scripts/bootstrap/check-git-safety.ps1 oder vorhandenes Safety-Check-Fallback
```

Hinweis: `pwsh` war im dokumentierten Linux/CachyOS-Stand nicht im PATH. Falls `pwsh` weiterhin fehlt, Safety-Check-Einschraenkung dokumentieren und lokale Fallback-Pruefung der verbotenen Pfade nutzen.

Danach Branch `planning/workspace-build-randomizer-integration` reviewbar committen, pushen und als PR nach `main` führen. Nicht durch Codex mergen.

## Nächster empfohlener Branch

`setup/devkitpro-toolchain-install-check`

Zweck: devkitPro/devkitARM installieren oder den freigegebenen Installationsweg ausführen und rein read-only pruefen. Keine Builds und keine ROM-Zugriffe.
