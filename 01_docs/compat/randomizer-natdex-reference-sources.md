# Randomizer NatDex Reference Sources

## Datum

2026-05-11

## Arbeitsbranch

`analysis/randomizer-natdex-reference-sources`

## Ziel und Sicherheitsrahmen

Read-only Inventar der neu eingebundenen Referenz-Submodules fuer spaetere UPR-FVX/CFRU/DPE-Implementierung. Dieser Block nimmt keine Codeaenderungen, keine Builds, keine ROM-Zugriffe, keine Release-Asset-Zugriffe und keine funktionalen Fixes vor.

`02_external/**` wurde nur gelesen. Alle Befunde in diesem Dokument sind aus lokalen Submodule-Staenden abgeleitet.

## Submodule-Inventar

| Pfad | Rolle | Remote | Branch | Commit | Kurzbefund |
|---|---|---|---|---|---|
| `02_external/upr-fvx` | Planton361 UPR-FVX-Fork mit PR #3 | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `compat/upr-fvx-gen9-generation-mapping` | `223ee9efaf1a29435674cbe6a03f25011364b2a1` | enthaelt SpeciesSet-Identity-Fix fuer erweiterte BPRE-Hacks |
| `02_external/CFRU-expansion` | lokale CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | Route-1-Custom-Wild fuer Randomizer-Kompatibilitaet standardmaessig deaktiviert |
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | lokale DPE-Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | DPE-Gen9-Datenbasis mit dynamischer Insertion |
| `02_external/references/cyansmp64-upr-zx-natdex` | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | erweitert ZX-Konzept auf Gen8/Gen9, Megas, Regional Forms, Eternamax |
| `02_external/references/cyansmp64-pokefirered-natdex` | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | FireRed-Decomp mit grossem NatDex-Speciesraum und ROM-Header-Metadaten |
| `02_external/references/upr-fvx-upstream` | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | upstream FVX 1.5.1-nahe Basis vor Planton361-Kompatibilitaetsfixes |
| `02_external/references/upr-zx-ajarmar` | ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | klassische UPR-ZX-Architektur bis Gen7 |
| `02_external/references/pret-pokefirered` | Vanilla-FireRed-Decomp-Baseline | `https://github.com/pret/pokefirered.git` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | Source-of-Truth fuer Vanilla-BPRE-Strukturen |

## Quelleninventar

### Randomizer

| Bereich | Primaere Pfade | Relevanz |
|---|---|---|
| FVX Struktur | `02_external/upr-fvx/README.md`, `docs/src/_wikipages/structure.md` | FVX trennt `romio` und `random`, anders als ZX-Monolithen |
| FVX Gen3-ROM-Modell | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | BPRE-Hack-Erkennung, Species-Loading, Wild/Trainer/Starter/Evo/Learnset-Schreibpfade |
| FVX Species-Modell | `Species.java`, `SpeciesSet.java`, `SpeciesIDs.java`, `Gen3Constants.java` | `Species.number`, `speciesSetIdentityNumber`, Generation-Mapping |
| FVX Restrictions | `GenRestrictions.java`, `RestrictedSpeciesService.java`, `Settings.java`, `GameRandomizer.java` | finaler Species-Pool und P0-Problem |
| FVX Randomizer | `WildEncounterRandomizer.java`, `TrainerPokemonRandomizer.java`, `StarterRandomizer.java`, `EvolutionRandomizer.java`, `SpeciesMovesetRandomizer.java` | Pool-Nutzung nach `RestrictedSpeciesService` |
| ZX Basis | `02_external/references/upr-zx-ajarmar/src/com/dabomstew/pkrandom/**` | Vergleich fuer altes `Pokemon`-Modell und monolithischen `Randomizer` |
| CyanSMP64 ZX NatDex | `02_external/references/cyansmp64-upr-zx-natdex/src/com/dabomstew/pkrandom/**` | Referenz fuer Gen8/Gen9-Restrictions und NatDex-Pools |

### FireRed, NatDex, CFRU und DPE

| Bereich | Primaere Pfade | Relevanz |
|---|---|---|
| Vanilla Species | `02_external/references/pret-pokefirered/include/constants/species.h` | `NUM_SPECIES SPECIES_EGG`, Vanilla-ID-Raum |
| Vanilla Dex | `02_external/references/pret-pokefirered/include/constants/pokedex.h` | `NATIONAL_DEX_COUNT NATIONAL_DEX_DEOXYS` |
| Vanilla Daten | `src/data/pokemon/species_info.h`, `evolution.h`, `level_up_learnset_pointers.h`, `tmhm_learnsets.h`, `tutor_learnsets.h` | Baseline fuer Tabellenindizes nach Species-ID |
| Vanilla Wild/Trainer | `src/data/wild_encounters.json`, `include/wild_encounter.h`, `src/wild_encounter.c`, `src/data/trainers.h`, `src/data/trainer_parties.h` | BPRE-kompatible Wild- und Trainerstrukturen |
| Cyan FireRed NatDex | `include/constants/species.h`, `include/constants/pokedex.h`, `src/pokemon.c`, `src/rom_header_gf.c`, `src/data/pokemon/**` | erweitertes NatDex-Datenmodell und ROM-Header-Metadaten |
| DPE Species/Dex | `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/species.h`, `include/pokedex.h` | DPE-interne Species-ID und National-Dex-ID |
| DPE Tabellen | `src/Base_Stats.c`, `src/Evolution Table.c`, `src/Learnsets.c`, `src/Species_To_Pokdex_Table.c`, `src/Pokedex_Orders.c`, `src/tm_compatibility/**`, `src/tutor_compatibility/**` | tabellarischer Source-of-Truth fuer Speciesdaten |
| CFRU Runtime | `02_external/CFRU-expansion/src/wild_encounter.c`, `include/wild_encounter.h`, `include/new/wild_encounter.h` | Day/Night-Wild-Header und Fallback auf Vanilla-Header |
| CFRU Tabellen | `src/Tables/wild_encounter_tables.c`, `trainer_data.c`, `trainer_parties.h`, `pokemon_tables.c`, `level_up_learnsets.c` | spaetere P1/P2-Diagnosen |

## Wichtigste Referenzbefunde

- CyanSMP64 UPR-ZX NatDex erweitert `GenRestrictions` explizit um Gen8, Gen9, Mega, Eternamax und Regional Forms.
- In CyanSMP64 UPR-ZX NatDex ist `GenRestrictions.limitToGen()` auskommentiert. Damit werden ROM-Generationen nicht automatisch auf die Originalgeneration gekappt.
- Ajarmar UPR-ZX und FVX begrenzen Restrictions normal ueber `limitToGen(rh.generationOfPokemon())`.
- FVX upstream ist gegenueber ZX staerker modularisiert: `romio` liest/schreibt ROM-Daten, `random` orchestriert Settings und Randomizer-Kategorien.
- Planton361 UPR-FVX hat gegenueber FVX upstream den PR-#3-Scope in `Gen3RomHandler`, `Species`, `Gen3Constants`, `RandomizationLogger` und `CheckValueCalculator`: separate SpeciesSet-Identitaet fuer erweiterte BPRE-Hacks.
- CyanSMP64 FireRed NatDex fuehrt einen kompakten, eigenen NatDex-Speciesraum: Beispiele sind `SPECIES_NACLI 957`, `SPECIES_CYCLIZAR 992`, `SPECIES_PECHARUNT 1050`, `NUM_SPECIES SPECIES_EGG`.
- DPE/CFRU verwenden dagegen den erweiterten DPE-ID-Raum: `SPECIES_SKRELP 0x31E`, `SPECIES_SPRIGATITO 0x50E`, `SPECIES_NACLI 0x52D`, `SPECIES_CYCLIZAR 0x551`, `SPECIES_PECHARUNT 0x59F`, `NUM_SPECIES SPECIES_PECHARUNT + 1`.
- DPE README nennt bis zu `1025` Pokedex-Eintraege, bis zu `128` TM/HM und `152` Move Tutors. CFRU README nennt `Pokedex: 1025`, `Species: 1439`, `Items: 798`, `Abilities: 288`.

## Bewertung fuer Workspace-Implementierung

Die Referenzen liefern drei unterschiedliche Modelle:

- Vanilla/pret: kompakte FireRed-Tabellen, `u16 species`, Tabellen nach Species-ID.
- CyanSMP64 NatDex: FireRed-Decomp und UPR-ZX werden zusammen erweitert; GenRestrictions werden fuer NatDex-Fokus praktisch nicht auf ROM-Generation gekappt.
- CFRU/DPE + UPR-FVX: externer Randomizer muss eine ROM-Hack-Datenbasis heuristisch lesen; deshalb muss er interne Species-ID, Dex-ID und SpeciesSet-Identitaet bewusst getrennt halten.

Fuer den naechsten UPR-FVX-Fix ist CyanSMP64 UPR-ZX NatDex vor allem als Restriction-Referenz wertvoll, nicht als direkt uebertragbares Datenmodell. Das DPE/CFRU-ID-Modell bleibt Source-of-Truth fuer den lokalen Teststand.

## Folge fuer Referenzdokumente

Dieses Inventar ergaenzt:

- `01_docs/compat/randomizer-workflow-model.md`
- `01_docs/compat/natdex-reference-implementation-notes.md`

Die bestehenden Referenzdateien bleiben gueltig; `tool-manifest.md` sollte die neu gepinnten Referenz-Submodules explizit dokumentieren.
