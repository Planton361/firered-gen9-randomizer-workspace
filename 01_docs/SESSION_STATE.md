# Session State

## Stand

- Lokales Git-Repo ist eingerichtet.
- GitHub-Repo `Planton361/firered-gen9-randomizer-workspace` existiert und bleibt Source of Truth.
- `main` ist Default Branch und bleibt stabil.
- Branch Protection und PR-Pflicht sind laut dokumentiertem Projektstand eingerichtet.
- Workspace PR #28 ist gemerged; der Gen4+-Wild-Pool-Diagnosebefund ist in `main` verfuegbar.
- Workspace PR #29 ist gemerged; das CFRU/DPE-UPR-FVX-Kompatibilitaetsmodell ist in `main` verfuegbar.
- IntelliJ IDEA 2026.2 EAP ist lokal ueber JetBrains Toolbox auffindbar; JetBrains MCP ist als gebuendeltes IDE-Plugin vorhanden und bleibt nur optional fuer read-only Analyse.
- UPR-FVX PR #3 ist gemerged; der lokale Submodule-Stand bleibt in diesem Workspace auf `223ee9ef compat: preserve CFRU DPE species identity`.
- Die neu eingebundenen NatDex-/Randomizer-/FireRed-Referenz-Submodules sind in `main` verfuegbar und wurden read-only inventarisiert.
- devkitPro/devkitARM wurde lokal installiert und geprueft.
- DPE Gen9 baut lokal erfolgreich.
- CFRU auf DPE baut lokal erfolgreich.
- UPR-FVX wurde aus Source gebaut und startet.
- UPR-FVX kann die CFRU/DPE-ROM laden, minimal randomisieren und speichern.
- BizHawk bootet die randomisierte ROM; neues Spiel, Starterwahl und Rivalenkampf funktionieren.
- Wild-Encounter-Randomization funktioniert fuer Vanilla-/Fallback-Encounter-Tabellen.
- Route 1 wurde fuer den Randomizer-Kompatibilitaetsbuild per `FIRERED_GEN9_ENABLE_ROUTE1_CUSTOM_WILD 0` auf Vanilla/Fallback-Wilddaten zurueckgefuehrt.
- PR #3 behebt den SpeciesSet-Kollaps: `speciesList.size` steigt im Diagnosebefund von `412` auf `799`, `maxSpeciesIdentityNumber=823`, Skrelp bis Hawlucha werden Gen6 statt Gen3.
- Der finale Wild-Randomizer-Pool bleibt im dokumentierten Gen4+-Diagnoselauf auf Gen1-3 begrenzt, weil `Settings.tweakForRom()` Gen3-ROMs auf `generationOfPokemon() == 3` kappt und `GameRandomizer.setupSpeciesRestrictions()` diese Restrictions auch bei `limitPokemon=false` setzt.
- ROMs, Saves, Builds, Tool-Binaries und private Dateien sind ausgeschlossen.

## Aktueller Branch

`setup/intellij-mcp-readonly-check`

## Aktueller Arbeitsblock

Read-only Inventur der lokalen JetBrains-/IntelliJ-MCP-Verfuegbarkeit fuer kuenftige optionale Codex-Codebase-Analyse.

## Ziel

Konkret klaeren:

- ob IntelliJ IDEA lokal auffindbar ist
- ob die IDE-Version mindestens 2025.2 ist
- ob JetBrains MCP Server in der IDE-Distribution vorhanden ist
- ob Codex-Auto-Configuration erkennbar ist
- welche Projektregeln fuer eine spaetere read-only Nutzung gelten

## In diesem Arbeitsblock geprueft / geaendert

- Workspace `main` per `git pull --ff-only origin main` aktualisiert.
- Branch `setup/intellij-mcp-readonly-check` von aktuellem `main` erstellt.
- Pflichtdokumente sowie MCP-/Agent-/Tooling-Policies gelesen.
- IntelliJ IDEA read-only ueber PATH/Toolbox geprueft.
- Gefundene IDE-Version: IntelliJ IDEA 2026.2 EAP, Build `IU-262.4852.50`.
- JetBrains MCP Server als gebuendeltes Plugin `com.intellij.mcpServer` gefunden.
- Lokale Distribution enthaelt MCP-Settings-Hinweise fuer `Settings | Tools | MCP Server`.
- Lokale Distribution enthaelt Codex-Client-/Auto-Configuration-Hinweise.
- Keine Codeaenderungen vorgenommen.
- Keine Builds gestartet.
- Keine ROMs, Saves, Emulator States, Tool-Binaries oder privaten Pfade gelesen, kopiert, geaendert oder committed.

## Ergebnis

- IntelliJ MCP ist lokal verfuegbar und erfuellt die Mindestversion.
- Codex-Auto-Configuration ist in der lokalen IDE-Distribution erkennbar, wurde aber nicht aktiviert oder getestet.
- JetBrains MCP bleibt fuer dieses Projekt optional, nicht blockierend und nur read-only fuer Code-Navigation/Symbolsuche.
- Codex nutzt weiter Git/`rg`-first.
- Schreibende MCP-Tools, Terminalausfuehrung, Builds, Run Configurations, Patch-Anwendung und Refactorings bleiben gesperrt.
- ROM-/Build-/Tool-Binary-/Secret-Pfade duerfen nicht ueber MCP exponiert werden.

## Noch nicht gestartet

- Aktivierung oder echter Verbindungstest von JetBrains MCP mit Codex
- UPR-FVX-Fix fuer CFRU/DPE-Generation-Restrictions
- Trainer-/Starter-/Evolution-/Learnset-Diagnosen nach PR #3
- CFRU-Day/Night-Custom-Wild-Tabellen-Support
- Nullslot-`<unknown>`-Analyse
- Ironmon-Tracker-Tests

## Sicherheitsstatus

Keine ROMs, Saves, Builds oder Tool-Binaries committed.

Keine ROMs in ChatGPT hochgeladen oder gelesen.

Keine externen Original-Upstreams kontaktiert.

Keine Aenderungen direkt auf `main`.

Keine Codeaenderungen in `02_external/**`.

Keine MCP-Configs mit Secrets angelegt.

Keine MCP-Configs geaendert oder committed.

## Naechste Pruefung

Lokal im Workspace nach den Dokumentationsaenderungen pruefen:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```

## Naechster empfohlener Branch

`compat/upr-fvx-cfru-dpe-gen-restrictions`

Zweck: Im UPR-FVX-Fork verhindern, dass erweiterte CFRU/DPE-BPRE-Hacks trotz erweitertem Species-Pool durch `Settings.tweakForRom()` und `RestrictedSpeciesService` auf Gen1-3 begrenzt werden.
