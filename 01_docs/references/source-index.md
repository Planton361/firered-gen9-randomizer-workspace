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
| Referenz | CyanSMP64 UPR-ZX NatDex | https://github.com/CyanSMP64/universal-pokemon-randomizer-zx/tree/natdex | Randomizer-Referenz für NatDexExtension; Vergleich für Species-Pool, GenRestrictions, Settings und Wild-Workflow | read-only Submodule | aktiv |
| Referenz | CyanSMP64 FireRed NatDex | https://github.com/CyanSMP64/pokefirered/tree/natdex | FireRed-Decomp-Referenz mit NatDex-Erweiterung; Vergleich gegen pret/pokefirered und CFRU/DPE-Modell | read-only Submodule | aktiv |
| Referenz | UPR-FVX Upstream | https://github.com/upr-fvx/universal-pokemon-randomizer-fvx | Upstream-Vergleich gegen Planton361-Fork; keine Änderungen | read-only Submodule | aktiv |
| Referenz | Ajarmar UPR-ZX | https://github.com/Ajarmar/universal-pokemon-randomizer-zx | historische Randomizer-Basis; Vergleich zu FVX und CyanSMP64-NatDex-Fork | read-only Submodule | aktiv |
| Referenz | pret FireRed | https://github.com/pret/pokefirered | Vanilla-FireRed-Decomp-Baseline für BPRE-Datenstrukturen | read-only Submodule | aktiv |


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

## Randomizer-/NatDex-Referenzen 2026-05-11

Arbeitsblock: `analysis/randomizer-natdex-reference-sources`.

Neue Workspace-Referenzen:

- `01_docs/compat/randomizer-natdex-reference-sources.md`
- `01_docs/compat/randomizer-workflow-model.md`
- `01_docs/compat/natdex-reference-implementation-notes.md`

Read-only analysierte Submodules:

| Bereich | Lokaler Pfad | Branch/Stand | Zweck |
|---|---|---|---|
| UPR-FVX Fork | `02_external/upr-fvx` | `223ee9ef` | Planton361-Kompatibilitaetsstand mit PR #3 |
| UPR-FVX Upstream | `02_external/references/upr-fvx-upstream` | `e0788edc` | Upstream-Vergleich vor Planton361-Fixes |
| UPR-ZX Ajarmar | `02_external/references/upr-zx-ajarmar` | `7f00eb86` | klassische UPR-ZX-Basis bis Gen7 |
| CyanSMP64 UPR-ZX NatDex | `02_external/references/cyansmp64-upr-zx-natdex` | `9b63eb28` | Gen8/Gen9-/Mega-/Regional-Forms-Restriction-Referenz |
| pret FireRed | `02_external/references/pret-pokefirered` | `e060ab95` | Vanilla-BPRE-Decomp-Baseline |
| CyanSMP64 FireRed NatDex | `02_external/references/cyansmp64-pokefirered-natdex` | `16b8b9ff` | NatDex-FireRed-Datenmodell |
| CFRU-expansion | `02_external/CFRU-expansion` | `b885d7a9` | CFRU-Laufzeit- und Tabellenmodell |
| DPE Gen9 | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `5906aa4d` | DPE-Species-/Dex-/Datenmodell |

Ergebnis:

- CyanSMP64 UPR-ZX NatDex zeigt ein NatDex-Randomizer-Modell, in dem `limitToGen()` keine hoeheren Generationen kappt und Gen8/Gen9, Mega, Eternamax sowie Regional Forms eigene Restriction-Bits haben.
- Ajarmar UPR-ZX und FVX begrenzen Settings normal auf `rh.generationOfPokemon()`.
- Fuer den lokalen CFRU/DPE-Teststand bleibt das DPE/CFRU-ID-Modell massgeblich; CyanSMP64 NatDex ist Vergleichs- und Fixplanungsreferenz, aber kein direktes Drop-in-Modell.
- P0 bleibt ein kleiner UPR-FVX-Fix fuer Settings/GenRestrictions, nicht fuer Day/Night-Wild, Nullslots oder Trainer-/Move-Tabellen.

## CFRU Documentation Relevanz 2026-05-11

Arbeitsblock: `analysis/cfru-documentation-randomizer-relevance`.

Neue Workspace-Referenz:

- `01_docs/compat/cfru-documentation-randomizer-relevance.md`

Primaere lokale Quelle:

| Bereich | Lokaler Pfad | Zweck |
|---|---|---|
| CFRU Documentation PDF | `02_external/CFRU-expansion/CFRU Documentation.pdf` | Source-of-Truth fuer CFRU-Setup-Reihenfolge, Runtime-Features, Randomizer-Flags, Day/Night-Wild, Swarms, Roamers, Trainer-EVs, Save Expansion und Table Compendium |

Ergebnis:

- DPE-before-CFRU-Reihenfolge bestaetigt: DPE liefert Datenmodell, CFRU liefert Engine-/Runtime-Modell.
- `SPECIES_NONE=0`, Species-/Pokedex-Defines und `asm_defines.s` sind fuer interne ID vs. Dex-ID und Nullslot-Bewertung relevant.
- CFRU-Runtime-Randomizer-Flags (`FLAG_POKEMON_RANDOMIZER`, Learnset-/Ability-Randomizer, `NUM_SPECIES_RANDOMIZER`, Banlisten) sind getrennt von UPR-FVX-Offline-Randomisierung zu behandeln.
- CFRU-Time-of-Day-Wild-Header, Swarms und Roamers bleiben separate Wild-Systeme nach P0.
- Hidden Ability BaseStats-Byte `0x1A`, `TRAINERS_WITH_EVS`, TM/HM/Tutor-Erweiterung und `EXPAND_MOVESETS` vs. DPE-Learnsets sind P1-Risiken.
- Save Expansion/Roamer-Speicher bestaetigt P4 fuer BizHawk/Ironmon/RAM-Mapping.

## CFRU/DPE Encounter-Systemmodell 2026-05-12

Arbeitsblock: `analysis/upr-fvx-cfru-dpe-p1-encounter-systems`.

Neue Workspace-Referenz:

- `01_docs/compat/cfru-dpe-encounter-systems-model.md`

Zusaetzlich relevant eingeordnete lokale Quellen:

| Bereich | Lokaler Pfad | Zweck |
|---|---|---|
| UPR-FVX Standard-Wild | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | `getEncounters()`/`setEncounters()` fuer Walking, Surfing, Rock Smash und Fishing |
| UPR-FVX Wild-Randomizer | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/WildEncounterRandomizer.java` | finaler Randomizer-Workflow ueber `EncounterArea` |
| UPR-FVX Encounter-Modell | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/EncounterArea.java`, `EncounterType.java` | Gruppierung und Typisierung von Encounter-Areas |
| CFRU Runtime-Wild | `02_external/CFRU-expansion/src/wild_encounter.c` | Time-of-Day-Fallback, Standard-Wild, Swarms, Roamers, Wild Double und Spezialfaelle |
| CFRU Wild-Header | `02_external/CFRU-expansion/include/wild_encounter.h`, `include/new/wild_encounter.h` | WildPokemon-/WildPokemonHeader-Strukturen und Runtime-API |
| CFRU Time/Swarms | `02_external/CFRU-expansion/src/Tables/wild_encounter_tables.c` | Morning/Day/Evening/Night-Header und `gSwarmTable` |
| CFRU Roamers | `02_external/CFRU-expansion/src/roamer.c`, `include/new/roamer.h` | Roamer-State, Script-Initialisierung und Encounter-Abfang |
| CFRU DexNav | `02_external/CFRU-expansion/src/dexnav.c` | DexNav liest lokale Wild-/Swarm-Daten und erzeugt eigene Encounters |
| CFRU Raids | `02_external/CFRU-expansion/src/dynamax.c`, `include/new/dynamax.h`, `src/Tables/raid_encounters.h` | Raid-Species, Items, Abilities, Drops und Battle-Erzeugung |
| Vanilla Referenz | `02_external/references/pret-pokefirered/src/wild_encounter.c`, `include/wild_encounter.h`, `src/wild_pokemon_area.c` | FireRed-Baseline fuer `gWildMonHeaders` |
| NatDex Referenz | `02_external/references/cyansmp64-pokefirered-natdex/include/wild_encounter.h`, `tools/inigen/inigen.c` | NatDex-FireRed-Wildstruktur und Symbol-/INI-Erzeugung |

Ergebnis:

- P0-supported sind nur `gWildMonHeaders`-kompatible Standard-Wildsysteme: Walking/Grass-Cave, Surfing, Fishing und Rock Smash.
- CFRU-Time-of-Day-Wild kann Fallback-Daten uebersteuern und bleibt P2.
- Swarms, Roamers, DexNav, Wild Double Battles, Raids, Altering Cave und Tanoby/Unown sind partial oder unsupported und muessen getrennt behandelt werden.

## CFRU/DPE Species-Schreibpfade 2026-05-12

Arbeitsblock: `analysis/upr-fvx-cfru-dpe-p1-species-write-paths`.

Neue Workspace-Referenz:

- `01_docs/compat/upr-fvx-cfru-dpe-species-write-paths.md`

Zusaetzlich relevant eingeordnete lokale Quellen:

| Bereich | Lokaler Pfad | Zweck |
|---|---|---|
| UPR-FVX Gen3-Schreibpfade | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | Starters, Static Pokemon, Trainer, Evolutions, Learnsets, TM/HM, Tutor, BaseStats/Abilities und Catching Tutorial |
| UPR-FVX Randomizer-Pfade | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/StarterRandomizer.java`, `StaticPokemonRandomizer.java`, `TrainerPokemonRandomizer.java`, `EvolutionRandomizer.java`, `SpeciesMovesetRandomizer.java`, `TMHMTutorCompatibilityRandomizer.java`, `SpeciesAbilityRandomizer.java`, `ItemRandomizer.java` | Settings- und Randomizer-Nutzung der RomHandler-Daten |
| DPE Species-/BaseStats | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`, `include/base_stats.h`, `src/Base_Stats.c` | interne Species-IDs, BaseStats-Struktur und Hidden Ability bei Byte `0x1A` |
| DPE Evolutions/Learnsets | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/evolution.h`, `src/Evolution Table.c`, `src/Learnsets.c` | interne Species-ID als Tabellenindex fuer Evolutions und Level-up-Learnsets |
| DPE TM/Tutor | `02_external/Dynamic-Pokemon-Expansion-Gen-9/scripts/tm_tutor.py`, `src/tm_compatibility/`, `src/tutor_compatibility/`, `src/TM_Tutor_Tables.c`, `include/tutors.h` | 128 TM/HM, 152 Move Tutors und by-move organisierte Kompatibilitaetsdaten |
| CFRU Trainer | `02_external/CFRU-expansion/src/Tables/trainer_data.c`, `src/Tables/trainer_parties.h`, `src/Tables/trainers_with_evs_table.h`, `src/build_pokemon.c` | Trainerdaten, Parties, EV-/IV-/Ability-Spreads und Runtime-Erzeugung |
| CFRU Pokemon/Abilities | `02_external/CFRU-expansion/src/Tables/pokemon_tables.c`, `src/Tables/level_up_learnsets.c`, `src/ability_util.c`, `include/new/ability_util.h` | CFRU-Tabellen und Runtime-Ability-Kontext |
| CFRU TM/Tutor | `02_external/CFRU-expansion/include/constants/tmshms.h`, `include/constants/tutors.h`, `src/tm_case.c` | erweiterter TM-/Tutor-Kontext |

Ergebnis:

- Starters, Static Pokemon/Gifts und Trainer Pokemon lesen Species aus internen ROM-Werten, schreiben aber weiterhin ueber `pokedexToInternal[Species.number]`.
- Diese drei Pfade sind die kleinsten Kandidaten fuer praktische P1-Diagnosen und spaetere interne-ID-Fixes.
- Evolutions, Learnsets, TM/HM, Tutor und Abilities brauchen zuerst mehr Datenmodellierung, weil Quelle, Tabellenbreite, Hidden Ability und Map-Key-Semantik ueber einen kleinen Wild-Write-aehnlichen Patch hinausgehen.
- Empfohlener naechster Diagnosebranch ist `analysis/upr-fvx-cfru-dpe-p1-starter-write-diagnostics`.

## CFRU/DPE Palette-Loader-Blocker 2026-05-12

Arbeitsblock: `analysis/upr-fvx-cfru-dpe-palette-loader-blocker`.

Neue Workspace-Referenz:

- `01_docs/compat/upr-fvx-cfru-dpe-palette-loader-blocker.md`

Zusaetzlich relevant eingeordnete lokale Quellen:

| Bereich | Lokaler Pfad | Zweck |
|---|---|---|
| FVX Load-Lifecycle | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractGBRomHandler.java` | bedingungsloser `loadPokemonPalettes()`-Aufruf im ROM-Load |
| FVX Gen3 Palette-Load/-Save | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | Palette-Pointer-Lesen ueber `PokemonNormalPalettes`/`PokemonShinyPalettes` und `pokedexToInternal[Species.number]` |
| FVX Species-Palette-Felder | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java` | `normalPalette`/`shinyPalette`-Speicher |
| FVX Palette Randomizer | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/Gen3to5PaletteRandomizer.java`, `random/src/main/java/com/uprfvx/random/GameRandomizer.java` | Palette-Randomization ist settings-abhaengig, Palette-Load aber nicht |
| DPE Palettentabellen | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Palette_Table.c`, `src/Shiny_Palette_Table.c` | `gMonPaletteTable[NUM_SPECIES]`, `gMonShinyPaletteTable[NUM_SPECIES]`; `SPECIES_CUBONE_A` fehlt als erster belegter Nullslot |
| DPE Offsets | `02_external/Dynamic-Pokemon-Expansion-Gen-9/offsets.ini` | `gMonPaletteTable: 09A47568`, `gMonShinyPaletteTable: 09A55EAC`; Fehleradresse `0x1a495d8` entspricht Index `1038` |
| DPE/CFRU Runtime | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/updated_code.c`, `02_external/CFRU-expansion/src/scripting.c`, `src/follower_mon.c` | Runtime nutzt Palette-Tabellen bedarfsbezogen pro Species |
| Cyan NatDex Runtime | `02_external/references/cyansmp64-pokefirered-natdex/src/rom_header_gf.c`, `src/pokemon.c`, `tools/inigen/inigen.c` | NatDex-Referenz fuer Header-/Symbolquellen und bedarfsbezogene Palette-Nutzung |

Ergebnis:

- Der erste belegte Paletten-Loader-Abbruch bei `0x1a495d8` ist `gMonPaletteTable[1038]`, also `SPECIES_CUBONE_A`.
- DPE/CFRU-Palettentabellen sind strukturell Gen3-kompatibel, enthalten aber mindestens diesen nicht initialisierten Form-Slot.
- Palette-Load ist fuer P0/Wild fachlich nicht noetig, aber in FVX aktuell technischer Bestandteil von ROM-Load und Save.
- Naechste empfohlene Richtung ist ein defensiver CFRU/DPE-spezifischer Palette-Load/-Save-Fix, nicht eine erneute Count-Begrenzung.

## CFRU/DPE Palette-Save-Blocker 2026-05-12

Arbeitsblock: `analysis/upr-fvx-cfru-dpe-palette-save-blocker`.

Neue Workspace-Referenz:

- `01_docs/compat/upr-fvx-cfru-dpe-palette-save-blocker.md`

Zusaetzlich relevant eingeordnete lokale Quellen:

| Bereich | Lokaler Pfad | Zweck |
|---|---|---|
| FVX Save-Lifecycle | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java` | `prepareSaveRom()` ruft `savePokemonPalettes()` bedingungslos auf |
| FVX DataRewriter | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractGBRomHandler.java` | `rewriteData()` nimmt fuer einfache Writes einen einzelnen Pointer auf alte komprimierte Daten an |
| FVX Gen3 Palette-Save | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | `savePokemonPalettes()` schreibt alle geladenen normal/shiny Paletten neu, auch ohne Palette-Randomization |
| DPE Palette-Gap | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Palette_Table.c`, `src/Shiny_Palette_Table.c` | `[252]..[276]` teilen `gFrontSprite252Pal` beziehungsweise `gBackShinySprite252Pal` |
| DPE Offsets | `02_external/Dynamic-Pokemon-Expansion-Gen-9/offsets.ini` | `gFrontSprite252Pal: 096B9C08`; Save-Blocker `0x16b9c08` entspricht diesem ROM-Offset |
| FVX Palette-Randomizer | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java` | `maybeRandomizePokemonPalettes()` laeuft nur bei `PokemonPalettesMod.RANDOM` |

Ergebnis:

- Der neue Save-Blocker ist kein Null-Palette-Slot wie `SPECIES_CUBONE_A`, sondern ein Save-/Repointing-Problem bei geladenen Paletten.
- `0x16b9c08` ist das alte Datenziel `gFrontSprite252Pal`, das DPE fuer mehrere Gap-/Dummy-Tabelleneintraege teilt.
- Der defensive Palette-Load schuetzt fehlende Paletten, aber nicht unveraenderte, gemeinsam genutzte oder nicht speicherbare Palette-Daten.
- Naechste empfohlene Richtung ist, CFRU/DPE-Pokemon-Palette-Save zu ueberspringen, solange Palette-Randomization nicht aktiv war beziehungsweise keine Palette geaendert wurde.

## CFRU/DPE Gen9-Species-Coverage 2026-05-12

Arbeitsblock: `analysis/upr-fvx-cfru-dpe-gen9-species-coverage`.

Neue Workspace-Referenz:

- `01_docs/compat/upr-fvx-cfru-dpe-gen9-species-coverage.md`

Zusaetzlich relevant eingeordnete lokale Quellen:

| Bereich | Lokaler Pfad | Zweck |
|---|---|---|
| DPE Species-Grenzen | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h` | Gen7-/Gen8-/Gen9-Startpunkte und `NUM_SPECIES = SPECIES_PECHARUNT + 1` |
| CFRU Species-Grenzen | `02_external/CFRU-expansion/include/constants/species.h` | gespiegelter DPE-ID-Raum, `NUM_SPECIES_GEN_7`, `NUM_SPECIES_GEN_8`, `NUM_SPECIES` |
| DPE Pokedex-Grenzen | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/pokedex.h` | National-Dex bis `NATIONAL_DEX_PECHARUNT = 1025` und `NATIONAL_DEX_COUNT` |
| CFRU Runtime-Dex-Count | `02_external/CFRU-expansion/src/config.h` | `NATIONAL_DEX_COUNT 1025` und `NUM_SPECIES_RANDOMIZER NUM_SPECIES` |
| DPE Dex-Mapping | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Species_To_Pokdex_Table.c` | Gen7-Gen9 Species-to-National-Dex-Mapping bis Pecharunt |
| DPE Pokedex-Orders | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Pokedex_Orders.c` | Species-ID-orientierte Dex-Ordnungen bis Terapagos/Pecharunt |
| DPE Gen9-Daten | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c`, `src/Learnsets.c`, `src/Evolution Table.c` | Gen7-Gen9-Tabelleneintraege bis Pecharunt |
| CFRU Gen9-Learnsets | `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c` | Gen7-Gen9-Learnset-Eintraege im CFRU-Kontext |
| FVX Count-Heuristik | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | `basicBPRE10HackSupport()`, `loadPokemonNames()`, `loadPokedexOrder()`, `loadSpeciesStats()` |
| FVX Species-/Generation-Modell | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/constants/SpeciesIDs.java`, `romio/src/main/java/com/uprfvx/romio/gamedata/GenRestrictions.java` | Gen8/Gen9-Konstanten, `generationOf()`-Schwellen und `MAX_GENERATION=7` |
| CyanSMP64 NatDex-Randomizer | `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/pokemon/GenRestrictions.java`, `src/com/dabomstew/pkrandom/romhandlers/AbstractRomHandler.java` | Gen8/Gen9-Restriction-Bits und NatDex-Range-Strategie |
| CyanSMP64 FireRed NatDex | `02_external/references/cyansmp64-pokefirered-natdex/src/rom_header_gf.c`, `include/constants/species.h`, `include/constants/pokedex.h` | explizite NatDex-Metadaten und Species-/Dex-Grenzen |

Ergebnis:

- DPE/CFRU-Source ist auf vollstaendige Gen9-Species bis Pecharunt ausgelegt.
- Der aktuelle FVX-Diagnose-Load endet bei `PokemonCount=823` und erreicht damit weder Gen7 noch Gen8/Gen9.
- Wahrscheinlichster Engpass ist die BPRE-Hack-Heuristik aus `PokemonNames`, `PokemonMovesets` und `PokedexOrder`, nicht fehlende DPE/CFRU-Source-Coverage.

## PokedexOrder-/Count-Modell 2026-05-12

Arbeitsblock: `analysis/upr-fvx-cfru-dpe-pokedex-order-model`.

Neue Workspace-Referenz:

- `01_docs/compat/upr-fvx-cfru-dpe-pokedex-order-model.md`

Zusaetzlich relevant eingeordnete lokale Quellen:

| Bereich | Lokaler Pfad | Zweck |
|---|---|---|
| DPE Pokedex Runtime | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/updated_code.c` | belegt, dass DPE `gPokedexOrder_*` als Species-ID-Listen nutzt und fuer Dex-Flags ueber `SpeciesToNationalPokedexNum()` wandelt |
| DPE Species-to-Dex Mapping | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Species_To_Pokdex_Table.c` | beste Dex-ID-Quelle fuer FVX: internes Species-Mapping auf National-Dex-ID |
| DPE Pokedex Orders | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Pokedex_Orders.c` | Species-ID-Sortierlisten fuer Regional/Alphabetical/Weight/Height/Type; keine FVX-kompatible Count-Quelle |
| CFRU Dex Runtime | `02_external/CFRU-expansion/src/util.c` | National-Dex-Count und Species-to-Dex-Nutzung im CFRU-Kontext |
| FVX Legacy Gen3 Offsets | `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini` | Vanilla-BPRE `PokedexOrder=0x251FEE`; im CFRU/DPE-Teststand nicht als Count-Grenze belastbar |
| CyanSMP64 NatDex INI-Generator | `02_external/references/cyansmp64-pokefirered-natdex/tools/inigen/inigen.c` | Referenz fuer expliziten `PokemonCount = NUM_SPECIES - 1` und symbolbasierte Tabellenadressen |

Ergebnis:

- FVX `PokedexOrder` und DPE `PokedexOrder` haben unterschiedliche Semantik.
- DPE `PokedexOrder`-Eintraege `>1023` koennen valide interne Species-IDs sein.
- Fuer CFRU/DPE sollte `PokemonCount` nicht aus `PokedexOrder`-Sanity abgeleitet werden.
- Naechster Schritt ist ein separater UPR-FVX-Fixbranch fuer CFRU/DPE-spezifische Count-Erkennung; keine Static-/Gift- oder Learnset-Fixes im selben Branch.

## CFRU/DPE Save-Trainers-/Moveset-Blocker 2026-05-12

Arbeitsblock: `analysis/upr-fvx-cfru-dpe-save-trainers-moveset-blocker`.

Neue Workspace-Referenz:

- `01_docs/compat/upr-fvx-cfru-dpe-save-trainers-moveset-blocker.md`

Zusaetzlich relevant eingeordnete lokale Quellen:

| Bereich | Lokaler Pfad | Zweck |
|---|---|---|
| FVX Save-Lifecycle | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java` | `prepareSaveRom()` ruft `saveTrainers()` bedingungslos vor `savePokemonPalettes()` auf |
| FVX Trainer-Save | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | `saveTrainers()`, `trainerPokemonToBytes()`, `getMovesLearnt()`, `readMovesLearnt()` und `jamboMovesetHack` |
| FVX Legacy Offsets | `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini` | Vanilla-BPRE-`PokemonMovesets`-Fallback, der im CFRU/DPE-Teststand nicht belastbar ist |
| DPE Learnsets | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c` | `gLevelUpLearnsets[NUM_SPECIES]`, 3-Byte-`LevelUpMove`, Gen7-Gen9-Learnsets bis Pecharunt |
| CFRU Learnsets | `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c`, `src/learn_move.c` | CFRU-seitige `gLevelUpLearnsets`-Nutzung und 3-Byte-LevelUpMove-Terminator |
| Cyan NatDex Learnsets | `02_external/references/cyansmp64-pokefirered-natdex/tools/inigen/inigen.c`, `src/rom_header_gf.c`, `src/pokemon.c`, `include/constants/pokemon.h` | Referenz fuer symbol-/headerbasierte Learnset-Tabellenquellen und explizite Format-Metadaten |

Ergebnis:

- `saveTrainers()` ist nur der ausloesende Pfad; die Ursache ist ein allgemeiner Learnset-/Moveset-Zugriff auf eine fuer CFRU/DPE ungeeignete Tabelle.
- `0x25e49c` entspricht `PokemonMovesets + 826 * 4`; ID `826` ist im DPE/CFRU-Modell `SPECIES_ZYGARDE`.
- DPE/CFRU enthalten Source-Learnsets fuer Gen7-Gen9 bis Pecharunt; der aktuelle FVX-Zugriff liest diese Daten wahrscheinlich nicht korrekt.
- Naechste empfohlene Richtung ist ein kleiner Save-Trainers-Unblocker durch Lazy-Learnset-Load, gefolgt von einem separaten DPE/CFRU-Learnset-Profil.

## Regel

Vor produktiver Nutzung müssen Branch, Commit-Hash, lokaler Pfad und Zweck im Tool-Manifest festgehalten werden.

Externe Quellen werden erst nach separater Freigabe geklont oder geforkt.

Keine ROMs, Saves, Emulator States, Builds, Tool-Binaries, privaten Keys, Tokens, Secrets oder `.env`-Dateien in Git oder ChatGPT bringen.
