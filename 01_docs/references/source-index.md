# Source Index

## Zweck

Dieses Dokument sammelt externe Quellen für den FireRed Gen9 Randomizer Workspace.

Dieser Arbeitsblock ist read-only/planend:

- keine externen Repos klonen
- keine Forks anlegen
- keine ROMs, Saves, Builds oder Tool-Binaries anfassen
- keine Downloads von Releases oder Assets durchführen
- keine Installationen oder Builds ausführen

## Hauptquellen

| Bereich | Quelle | URL | Zweck | Read-only-Bewertung | Status |
|---|---|---|---|---|---|
| Randomizer | Universal Pokémon Randomizer FVX | https://github.com/upr-fvx/universal-pokemon-randomizer-fvx | Haupt-Randomizer-Kandidat | Unterstützt offiziell Vanilla-Core-Games Gen 1-7; ROM-Hacks sind nicht offiziell unterstützt und daher Kompatibilitätsrisiko | read-only geprüft; spaeter Release/JAR oder Source-Clone entscheiden |
| Randomizer Docs | UPR FVX Website/Wiki | https://upr-fvx.github.io/universal-pokemon-randomizer-fvx/ | Nutzung, Java, Build, CLI und Optionen dokumentieren | wichtig für spätere Smoke-Tests; keine Downloads in diesem Block | read-only geprüft; Java-/Build-Anforderung spaeter erneut verifizieren |
| FireRed Gen9 | Shiny-Miner/CFRU-expansion | https://github.com/Shiny-Miner/CFRU-expansion | CFRU-/Gen9-Basis prüfen | Fork von Skeli789/Complete-Fire-Red-Upgrade; Kandidat, aber vor Nutzung Commit/Branch pinnen | read-only geprüft; Hauptbasis-Kandidat |
| FireRed Gen9 | Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | DPE-/Gen9-Basis prüfen | Fork von Skeli789/Dynamic-Pokemon-Expansion; Kandidat, aber vor Nutzung Commit/Branch pinnen | read-only geprüft; Hauptbasis-Kandidat |
| Upstream | Skeli789/Complete-Fire-Red-Upgrade | https://github.com/Skeli789/Complete-Fire-Red-Upgrade | CFRU-Referenz | enthält FireRed-Upgrade/Battle-Engine-Referenz; Build erfordert später lokale ROM und Toolchain, daher aktuell nur Doku/Code-Referenz | read-only geprüft; Upstream-Referenz |
| Upstream | Skeli789/Dynamic-Pokemon-Expansion | https://github.com/Skeli789/Dynamic-Pokemon-Expansion | DPE-Referenz | dynamische FireRed-Pokémon-Erweiterung; soll mit CFRU genutzt werden | read-only geprüft; Upstream-Referenz |
| NatDex/IronMON | CyanSMP64/NatDexExtension | https://github.com/CyanSMP64/NatDexExtension | NatDex-/Randomizer-/Tracker-nahe Referenz | aktuelle Referenz für IronMON NatDex-Erweiterung; relevant wegen FireRed, 1209 Pokémon und Tracker-/BizHawk-Anforderungen | read-only geprüft |
| NatDex Referenz | CyanSMP64/pokefirered | https://github.com/CyanSMP64/pokefirered | FireRed/NatDex-Referenz | Fork von pret/pokefirered; erst nach genauer Branch-/Commit-Prüfung nutzen | offen |
| Randomizer Referenz | CyanSMP64/universal-pokemon-randomizer-zx | https://github.com/CyanSMP64/universal-pokemon-randomizer-zx | Randomizer-Referenz | nur relevant, falls NatDexExtension auf eigene Randomizer-Änderungen verweist | offen |
| Decomp Referenz | pret/pokefirered | https://github.com/pret/pokefirered | FireRed-Architektur/Symbole | englische FireRed/LeafGreen-Decompilation; gute Referenz für Strukturen, Builds erst später | read-only geprüft |
| Editor | Hex Maniac Advance | offen | ROM-Analyse und Tabellenprüfung | Quelle/Release muss noch eindeutig festgelegt werden; keine Tool-Binaries committen | offen |
| Emulator | BizHawk | https://github.com/TASEmulators/BizHawk | Emulatorziel | multi-system Emulator; relevant für IronMON Tracker und spätere Smoke-Tests | read-only geprüft |
| Tracker | Ironmon Tracker | https://github.com/besteon/Ironmon-Tracker | Trackerziel | Lua-Tracker für BizHawk/mGBA; unterstützt FireRed/LeafGreen/RSE; Contributions gehen laut Repo-Prozess gegen Dev | read-only geprüft |
| Toolchain | devkitPro/devkitARM | https://devkitpro.org/ | GBA-Build-Toolchain | erst später lokal prüfen; keine Installation in diesem Block | Plan dokumentiert; Installations-/Versionscheck spaeter |
| Agent Workflow | OpenAI Codex AGENTS.md | https://github.com/openai/codex | Agent-Regeln | nur für Workflow-Regeln relevant | offen |
| Git Workflow | GitHub Docs | https://docs.github.com/ | Branches, PRs, Forks, Schutzregeln | nur Doku-Referenz | offen |

## Read-only-Ergebnis 2026-05-10

- UPR FVX bleibt Haupt-Randomizer-Kandidat, aber ROM-Hack-Kompatibilität ist ein Risiko und muss später separat getestet werden.
- Shiny-Miner CFRU/DPE-Gen9 bleiben Hauptbasis-Kandidaten, müssen aber vor lokaler Nutzung auf Branch/Commit gepinnt werden.
- Skeli789 CFRU/DPE bleiben Upstream-Referenzen für Architektur und Build-Prozess.
- CyanSMP64 NatDexExtension ist eine wichtige IronMON-/NatDex-Referenz, aber nicht automatisch identisch mit dem geplanten Custom-Hack-Ziel.
- pret/pokefirered ist die saubere Decomp-Referenz für FireRed/LeafGreen-Strukturen.
- BizHawk und Ironmon Tracker bleiben spätere Kompatibilitätsziele.

## Integrationsentscheidung 2026-05-11

Arbeitsblock: `planning/workspace-build-randomizer-integration`.

- `02_external/` bleibt der dokumentierte lokale Ort für spaetere externe Repos.
- Externe Repo-Inhalte werden nicht im Workspace-Repo vendorisiert.
- UPR FVX wird spaeter entweder als lokales Release/JAR in `03_tools/releases/upr-fvx/` oder als gepinnter Source-Clone unter `02_external/upr-fvx` genutzt.
- Shiny-Miner `CFRU-expansion` und `Dynamic-Pokemon-Expansion-Gen-9` bleiben die ersten Gen9-Basis-Kandidaten.
- Skeli789 CFRU/DPE und pret/pokefirered bleiben Referenzen fuer Architektur, Build- und Kompatibilitaetsfragen.
- Vor jedem Clone/Fork muessen Branch, Commit-Hash, lokaler Pfad und Zweck im Tool-Manifest festgehalten werden.
- ROMs bleiben ausschliesslich lokal in `04_private_roms/`; Builds bleiben ausschliesslich lokal in `05_builds/`; Tool-Binaries bleiben ausschliesslich lokal in `03_tools/releases/`.

## Kompatibilitaetsmodell 2026-05-11

Arbeitsblock: `analysis/cfru-dpe-upr-fvx-compatibility-model`.

Neue Workspace-Referenz:

- `01_docs/compat/cfru-dpe-upr-fvx-compatibility-model.md`

Primaere lokale CFRU/DPE-Quellen fuer das Modell:

| Bereich | Quelle | Zweck |
|---|---|---|
| DPE Zielumfang | `02_external/Dynamic-Pokemon-Expansion-Gen-9/README.md` | dynamisches FireRed-Pokemon-Insertionsmodell, Pokedex-/Forme-Zielumfang |
| DPE Species-ID | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h` | interne `SPECIES_*`-IDs und `NUM_SPECIES` |
| DPE Dex-ID | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/pokedex.h` | National-Dex-Konstanten und Dex-Datenstrukturen |
| DPE Mapping | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Species_To_Pokdex_Table.c` | interne Species-ID zu National-Dex-ID |
| DPE Reihenfolge | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Pokedex_Orders.c` | regionale und sortierte Dex-Ordnungen |
| DPE Daten | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c`, `src/Evolution Table.c`, `src/Learnsets.c` | BaseStats, Evolutions und Learnsets indiziert nach interner Species-ID |
| DPE Offsets | `02_external/Dynamic-Pokemon-Expansion-Gen-9/offsets.ini`, `scripts/make.py` | generierte Adressen und Insertionslogik fuer konkret gebaute Teststaende |
| CFRU Zielumfang | `02_external/CFRU-expansion/README.md` | Engine-/Gen9-Zielumfang und DPE-Bezug |
| CFRU Species-ID | `02_external/CFRU-expansion/include/constants/species.h` | CFRU-interner Species-ID-Raum |
| CFRU Wild | `02_external/CFRU-expansion/include/wild_encounter.h`, `include/new/wild_encounter.h`, `src/wild_encounter.c`, `src/Tables/wild_encounter_tables.c` | Vanilla/Fallback-Wild, CFRU-Day/Night-Header und Laufzeit-Fallback |
| CFRU Trainer/Daten | `02_external/CFRU-expansion/src/Tables/trainer_data.c`, `src/Tables/trainer_parties.h`, `src/Tables/pokemon_tables.c`, `src/Tables/level_up_learnsets.c` | spaetere Trainer-/Pokemon-/Learnset-Kompatibilitaetsanalyse |

Primaere lokale UPR-FVX-Quellen fuer das Modell:

| Bereich | Quelle | Zweck |
|---|---|---|
| Struktur | `02_external/upr-fvx/README.md`, `02_external/upr-fvx/docs/src/_wikipages/structure.md` | Modulgrenzen `romio`/`random` |
| ROM-Erkennung | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romio/RomOpener.java`, `romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini` | Handler-Auswahl und Gen3-Offsets |
| Gen3-ROM-Modell | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | BPRE-Hack-Heuristik, Species-Loading, Wild/Trainer/Starter/Evolution/Learnset-Lese- und Schreibpfade |
| Species-Modell | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`, `SpeciesSet.java`, `SpeciesIDs.java`, `Gen3Constants.java` | Dex-ID, SpeciesSet-Identitaet, Generation-Mapping und Gen3-Konstanten |
| Restrictions | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/Settings.java`, `GameRandomizer.java`, `romio/src/main/java/com/uprfvx/romio/gamedata/GenRestrictions.java`, `romio/src/main/java/com/uprfvx/romio/services/RestrictedSpeciesService.java` | finaler Allowed-Pool und Gen-Filter |
| Randomizer | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java`, `TrainerPokemonRandomizer.java`, `StarterRandomizer.java`, `EvolutionRandomizer.java`, `SpeciesMovesetRandomizer.java`, `ItemRandomizer.java` | Randomizer-Pool-Nutzung und spaetere Kompatibilitaetsrisiken |
| Logging/CLI | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/cli/CliRandomizer.java`, `random/src/main/java/com/uprfvx/random/log/RandomizationLogger.java` | CLI-/Settings-Flow und Log-Auswertung |

Ergebnis:

- RAM-Mapping ist kein aktueller Blocker; zuerst muessen ROM-Datenmodell und finaler Randomizer-Pool stabil sein.
- P0 ist ein separater UPR-FVX-Fix fuer GenRestrictions/finalen Gen4+-Wild-Pool.
- P1 bis P4 bleiben Trainer/Starters/Evolutions/Learnsets, CFRU Day/Night Wild, Nullslot-`<unknown>` und Ironmon/BizHawk/RAM-Mapping.

## Regel

Vor produktiver Nutzung müssen Branch, Commit-Hash, lokaler Pfad und Zweck im Tool-Manifest festgehalten werden.

Externe Quellen werden erst nach separater Freigabe geklont oder geforkt.

Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Keys, Tokens, Secrets oder `.env`-Dateien in Git oder ChatGPT bringen.
