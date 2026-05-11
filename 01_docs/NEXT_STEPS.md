# Next Steps

## Aktueller Arbeitsblock

Read-only Inventur der lokalen IntelliJ-/JetBrains-MCP-Verfuegbarkeit dokumentieren.

Aktueller Branch:

```text
setup/intellij-mcp-readonly-check
```

Zieldokumente:

```text
01_docs/setup/mcp-policy.md
01_docs/setup/agent-tooling-policy.md
01_docs/references/tool-manifest.md
01_docs/SESSION_STATE.md
01_docs/NEXT_STEPS.md
00_project-control/roadmap/roadmap-status.md
```

## Naechste Schritte in diesem Block

1. Dokumentation reviewen:
   - `01_docs/setup/mcp-policy.md`
   - `01_docs/setup/agent-tooling-policy.md`
   - `01_docs/references/tool-manifest.md`
   - `01_docs/SESSION_STATE.md`
   - `01_docs/NEXT_STEPS.md`
   - `00_project-control/roadmap/roadmap-status.md`
2. Workspace-Checks ausfuehren:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

3. Commit erstellen:

```text
docs: document IntelliJ MCP readiness
```

4. Branch pushen und Workspace-PR nach `main` vorbereiten.

## Ergebnis dieses Blocks

- IntelliJ IDEA ist lokal ueber JetBrains Toolbox auffindbar.
- Gefundene Version: IntelliJ IDEA 2026.2 EAP, Build `IU-262.4852.50`.
- Die Mindestanforderung 2025.2 ist erfuellt.
- JetBrains MCP Server ist als gebuendeltes IDE-Plugin vorhanden.
- `Settings | Tools | MCP Server` ist in der lokalen IDE-Distribution als Settings-Pfad erkennbar.
- Codex-Auto-Configuration ist in der lokalen MCP-Server-Distribution erkennbar.
- Es wurde keine MCP-Konfiguration aktiviert, geaendert oder committed.
- Kuenftige Nutzung bleibt optional, read-only und nicht blockierend; Codex bleibt Git/`rg`-first.

## Danach

Naechster minimaler UPR-FVX-Fixbranch:

```text
compat/upr-fvx-cfru-dpe-gen-restrictions
```

Ziel:

- Fuer erweiterte CFRU/DPE-aehnliche BPRE-Hacks die Gen3-Kappung im finalen Randomizer-Pool verhindern.
- Der RomHandler-Pool aus PR #3 soll im finalen Wild-Randomizer-Pool Gen4+-Species zulassen.
- Der Fix soll nur Settings/Restrictions betreffen.
- Danach denselben Gen4+-Wild-Pool-Diagnoselauf wiederholen.

## Fix-Reihenfolge

P0: GenRestrictions / finaler Gen4+ Wild-Pool.

P1: Trainer, Starters, Evolutions, Learnsets und TM/Tutor-Kompatibilitaet.

P2: CFRU Day/Night Custom Wild Tables.

P3: Nullslot-`<unknown>` mit `rawInternalSpeciesId=0`.

P4: BizHawk/Ironmon Tracker/RAM-Mapping.

## Nicht tun

- keine ROMs bewegen
- keine ROMs lesen, kopieren oder aendern
- keine Saves oder Emulator States anfassen
- keine Builds starten oder committen
- keine Randomizer-JARs oder Tool-Binaries anfassen oder committen
- keine Codeaenderungen in `02_external/**` in diesem Analysebranch
- keinen GenRestrictions-Fix in diesem Branch
- keine Day/Night-Wild-Fixes
- keine Nullslot-Fixes
- keine Trainer-/Starter-/Evolution-/Learnset-/TM-/Tutor-Fixes
- keine externen Original-Upstreams kontaktieren
- keine PRs ohne explizites `--repo Planton361/<repo>` beziehungsweise eindeutig ausgewaehltes Planton361-Repository
- keine Aenderungen direkt auf `main`
- keine Installationen erzwingen
- keine GitHub-Tokens oder lokale Secrets dokumentieren
- keine MCP-Configs mit Secrets committen
- keine MCP-Config ohne separaten Freigabe-Block aktivieren oder committen
- JetBrains MCP nicht fuer Schreibaktionen, Terminalbefehle, Builds, Run Configurations, Patch-Anwendung oder Refactorings nutzen
- keine parallelen Agenten auf demselben Branch einsetzen

## Quality

- Abschlussdokumentation ist Teil der Definition of Done.
- Prompts sollen kurz bleiben und auf Dateipfade statt kopierte Inhalte verweisen.
- ROMs, Builds, Tool-Binaries und private Pfade bleiben ausserhalb von Git und ChatGPT.
