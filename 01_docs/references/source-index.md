# Source Index

## Zweck

Dieses Dokument sammelt externe Quellen für den FireRed Gen9 Randomizer Workspace.

Dieser Arbeitsblock ist read-only:

- keine externen Repos klonen
- keine Forks anlegen
- keine ROMs, Saves, Builds oder Tool-Binaries anfassen
- keine Downloads von Releases oder Assets durchführen

## Hauptquellen

| Bereich | Quelle | URL | Zweck | Read-only-Bewertung | Status |
|---|---|---|---|---|---|
| Randomizer | Universal Pokémon Randomizer FVX | https://github.com/upr-fvx/universal-pokemon-randomizer-fvx | Haupt-Randomizer-Kandidat | Unterstützt offiziell Vanilla-Core-Games Gen 1-7; ROM-Hacks sind nicht offiziell unterstützt und daher Kompatibilitätsrisiko | read-only geprüft |
| Randomizer Docs | UPR FVX Website/Wiki | https://upr-fvx.github.io/universal-pokemon-randomizer-fvx/ | Nutzung, Java, Build, CLI und Optionen dokumentieren | wichtig für spätere Smoke-Tests; keine Downloads in diesem Block | read-only geprüft |
| FireRed Gen9 | Shiny-Miner/CFRU-expansion | https://github.com/Shiny-Miner/CFRU-expansion | CFRU-/Gen9-Basis prüfen | Fork von Skeli789/Complete-Fire-Red-Upgrade; Kandidat, aber vor Nutzung Commit/Branch pinnen | read-only geprüft |
| FireRed Gen9 | Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | DPE-/Gen9-Basis prüfen | Fork von Skeli789/Dynamic-Pokemon-Expansion; Kandidat, aber vor Nutzung Commit/Branch pinnen | read-only geprüft |
| Upstream | Skeli789/Complete-Fire-Red-Upgrade | https://github.com/Skeli789/Complete-Fire-Red-Upgrade | CFRU-Referenz | enthält FireRed-Upgrade/Battle-Engine-Referenz; Build erfordert später lokale ROM und Toolchain, daher aktuell nur Doku/Code-Referenz | read-only geprüft |
| Upstream | Skeli789/Dynamic-Pokemon-Expansion | https://github.com/Skeli789/Dynamic-Pokemon-Expansion | DPE-Referenz | dynamische FireRed-Pokémon-Erweiterung; soll mit CFRU genutzt werden | read-only geprüft |
| NatDex/IronMON | CyanSMP64/NatDexExtension | https://github.com/CyanSMP64/NatDexExtension | NatDex-/Randomizer-/Tracker-nahe Referenz | aktuelle Referenz für IronMON NatDex-Erweiterung; relevant wegen FireRed, 1209 Pokémon und Tracker-/BizHawk-Anforderungen | read-only geprüft |
| NatDex Referenz | CyanSMP64/pokefirered | https://github.com/CyanSMP64/pokefirered | FireRed/NatDex-Referenz | Fork von pret/pokefirered; erst nach genauer Branch-/Commit-Prüfung nutzen | offen |
| Randomizer Referenz | CyanSMP64/universal-pokemon-randomizer-zx | https://github.com/CyanSMP64/universal-pokemon-randomizer-zx | Randomizer-Referenz | nur relevant, falls NatDexExtension auf eigene Randomizer-Änderungen verweist | offen |
| Decomp Referenz | pret/pokefirered | https://github.com/pret/pokefirered | FireRed-Architektur/Symbole | englische FireRed/LeafGreen-Decompilation; gute Referenz für Strukturen, Builds erst später | read-only geprüft |
| Editor | Hex Maniac Advance | offen | ROM-Analyse und Tabellenprüfung | Quelle/Release muss noch eindeutig festgelegt werden; keine Tool-Binaries committen | offen |
| Emulator | BizHawk | https://github.com/TASEmulators/BizHawk | Emulatorziel | multi-system Emulator; relevant für IronMON Tracker und spätere Smoke-Tests | read-only geprüft |
| Tracker | Ironmon Tracker | https://github.com/besteon/Ironmon-Tracker | Trackerziel | Lua-Tracker für BizHawk/mGBA; unterstützt FireRed/LeafGreen/RSE; Contributions gehen laut Repo-Prozess gegen Dev | read-only geprüft |
| Toolchain | devkitPro/devkitARM | https://devkitpro.org/ | GBA-Build-Toolchain | erst später lokal prüfen; keine Installation in diesem Block | offen |
| Agent Workflow | OpenAI Codex AGENTS.md | https://github.com/openai/codex | Agent-Regeln | nur für Workflow-Regeln relevant | offen |
| Git Workflow | GitHub Docs | https://docs.github.com/ | Branches, PRs, Forks, Schutzregeln | nur Doku-Referenz | offen |

## Read-only-Ergebnis 2026-05-10

- UPR FVX bleibt Haupt-Randomizer-Kandidat, aber ROM-Hack-Kompatibilität ist ein Risiko und muss später separat getestet werden.
- Shiny-Miner CFRU/DPE-Gen9 bleiben Hauptbasis-Kandidaten, müssen aber vor lokaler Nutzung auf Branch/Commit gepinnt werden.
- Skeli789 CFRU/DPE bleiben Upstream-Referenzen für Architektur und Build-Prozess.
- CyanSMP64 NatDexExtension ist eine wichtige IronMON-/NatDex-Referenz, aber nicht automatisch identisch mit dem geplanten Custom-Hack-Ziel.
- pret/pokefirered ist die saubere Decomp-Referenz für FireRed/LeafGreen-Strukturen.
- BizHawk und Ironmon Tracker bleiben spätere Kompatibilitätsziele.

## Regel

Vor produktiver Nutzung müssen Branch, Commit-Hash, lokaler Pfad und Zweck im Tool-Manifest festgehalten werden.

Externe Quellen werden erst nach separater Freigabe geklont oder geforkt.
