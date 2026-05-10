# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Projektkontext, Roadmap-Status, Repo-Governance, Codex-Dry-Run, externe Quellenprüfung, Workflow-Automation, Post-Merge-Doku-Sync, lokale Windows-Toolchain-Inventur, PATH-Follow-up, Linux/CachyOS-Workspace-Migration, Linux-Toolchain-Inventur und Linux-GitHub-Auth-Refresh wurden gemerged bzw. lokal übernommen.
- PR #10 `docs: sync post-merge workflow state` ist gemerged.
- PR #11 `docs: record local toolchain inventory` ist gemerged.
- PR #12 `docs: prepare path toolchain followup` ist gemerged.
- Nutzer hat die lokale Arbeitsumgebung von Windows auf Linux/CachyOS gewechselt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`docs/agent-best-practices-refresh`

## Aktueller Arbeitsblock

Agent-Best-Practices, Usage-Optimierung, Agent-Tooling, MCP-Regeln, `.aiignore` und PR-Template repo-tauglich dokumentieren, ohne neue Bürokratie einzuführen.

## Ziel

Den aktuellen Dokumentationsstand für ChatGPT/Codex-/Agent-Workflow aktualisieren:

- kompaktere Codex-Prompts ohne Overprompting dokumentieren
- Usage-Optimierung über Dateipfade, Handoff und stabile `AGENTS.md`-Regeln dokumentieren
- ChatGPT QA, Codex CLI und optionale IDE-Agenten sauber abgrenzen
- MCP als optional und sicherheitsbegrenzt dokumentieren
- `.aiignore` für ROM-/Build-/Tool-Binary-/Secret-Pfade ergänzen
- PR-Template mit Sicherheits- und Checkliste ergänzen
- Tool-Manifest und Roadmap auf diesen Arbeitsblock synchronisieren

## In diesem Arbeitsblock geprüft / geändert

- Branch `docs/agent-best-practices-refresh` ist der Arbeitsbranch.
- `01_docs/quality/prompt-templates.md` wurde auf einen kompakteren Codex-Arbeitspaket-Prompt aktualisiert.
- `01_docs/quality/usage-optimization.md` wurde erstellt.
- `01_docs/setup/agent-tooling-policy.md` wurde erstellt.
- `01_docs/setup/mcp-policy.md` wurde erstellt.
- `.aiignore` wurde erstellt.
- `.github/pull_request_template.md` wurde erstellt.
- `01_docs/references/tool-manifest.md` wurde um Agent-/MCP-/PR-Template-/`.aiignore`-Status ergänzt.
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

Danach Branch `docs/agent-best-practices-refresh` reviewbar committen, pushen und als PR nach `main` führen. Nicht durch Codex mergen.

## Nächster empfohlener Branch

`setup/linux-gba-toolchain-plan`

Zweck: devkitPro/devkitARM- und `arm-none-eabi-gcc`-Vorgehen für Linux/CachyOS planen, bevor Installationen oder Build-Schritte freigegeben werden.
