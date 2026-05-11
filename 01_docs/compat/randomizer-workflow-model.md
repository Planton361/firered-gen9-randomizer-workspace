# Randomizer Workflow Model

## Datum

2026-05-11

## Arbeitsbranch

`analysis/randomizer-natdex-reference-sources`

## Scope

Read-only Vergleich von UPR-FVX, UPR-FVX upstream, Ajarmar UPR-ZX und CyanSMP64 UPR-ZX NatDex. Ziel ist ein kompaktes Workflowmodell fuer spaetere CFRU/DPE-Kompatibilitaetsfixes. Kein Code wurde geaendert.

## Kurzvergleich

| Thema | UPR-ZX Ajarmar | CyanSMP64 UPR-ZX NatDex | UPR-FVX upstream | Planton361 UPR-FVX |
|---|---|---|---|---|
| Architektur | monolithischer `Randomizer`, Handler in `src/com/dabomstew/pkrandom` | gleiche Grundarchitektur, NatDex-Erweiterungen | getrennte Module `romio` und `random` | FVX mit CFRU/DPE-Kompatibilitaetsdiagnosen und PR #3 |
| Pokemon/Species-Modell | `Pokemon` mit `number` als ID | `Pokemon` mit erweitertem Gen9-Konstantenraum | `Species`, `SpeciesSet`, Services | `Species.number` bleibt Dex-ID, `speciesSetIdentityNumber` kann interne ID sein |
| Generationen | Gen1-7 | Gen1-9 plus Mega/Eternamax/Regional Forms | Gen1-7 | Gen1-7 Settings-Modell, aber Gen3-DPE-Species koennen bis Gen9 klassifiziert werden |
| Restrictions | `limitToGen()` kappt hoehere Generationen | `limitToGen()` ist auskommentiert | `GenRestrictions.MAX_GENERATION = 7`; `limitToGen()` aktiv | P0 offen: Settings kappen CFRU/DPE-BPRE noch auf Gen3 |
| Wild-Workflow | `Randomizer` nutzt `getEncounters()`/`setEncounters()` | wie ZX, aber NatDex-Pool breiter | `WildEncounterRandomizer` nutzt `RestrictedSpeciesService` | Wild-Pool bleibt aktuell wegen Restrictions Gen1-3 |
| ROM-Hack-Erkennung | Gen3-Heuristiken in Handlern | Gen3-Heuristiken plus NatDex-Datenbasis | FVX Gen3-Heuristiken | erweiterte BPRE-Heuristik plus SpeciesSet-Identity-Fix |

## UPR-FVX Lifecycle

1. CLI oder GUI laedt Settings und ROM.
2. `RomOpener` waehlt den RomHandler anhand ROM-Code, Version und Offset-Profil.
3. `Gen3RomHandler.midLoadingSetUp()` aktiviert fuer veraenderte BPRE-ROMs `basicBPRE10HackSupport()`.
4. `basicBPRE10HackSupport()` ermittelt `PokemonCount` heuristisch ueber Namen, Moveset-Pointer, `PokedexOrder` und bekannte Pointer.
5. `loadSpeciesStats()` laedt Namen, `PokedexOrder`, Stats und baut `pokesInternal`, `pokes` und `speciesList`.
6. PR #3 setzt fuer erweiterte BPRE-Hacks `speciesSetIdentityNumber = interne ID`; `Species.number` bleibt Dex-/Pokedex-ID.
7. `Settings.tweakForRom()` passt Settings an den RomHandler an.
8. `GameRandomizer.randomize()` ruft zuerst `setupSpeciesRestrictions()`.
9. `setupSpeciesRestrictions()` setzt immer `romHandler.getRestrictedSpeciesService().setRestrictions(settings.getCurrentRestrictions())`.
10. Die Randomizer-Kategorien verwenden danach entweder RomHandler-Daten direkt oder den gefilterten `RestrictedSpeciesService`.
11. `WildEncounterRandomizer` ruft `romHandler.getEncounters()`, baut `allowed` aus `rSpecService.getSpecies(...)`, randomisiert und schreibt via `romHandler.setEncounters()`.

## Settings und GenRestrictions

Aktueller FVX-/Planton361-Codepfad:

- `Settings.tweakForRom()` setzt bei validen Gen3-ROMs `currentRestrictions.limitToGen(rh.generationOfPokemon())`.
- `Gen3RomHandler.generationOfPokemon()` gibt weiterhin `3` zurueck.
- `GenRestrictions.MAX_GENERATION` ist `7`.
- `RestrictedSpeciesService.allInclAltFormesFromRestrictions()` nimmt fuer erlaubte Generationen Species aus `romHandler.getSpeciesSetInclFormes()`.
- Die Filterung laeuft ueber `sp.getBaseForme().getGeneration() == gen`.
- Bei `restrictions == null` nutzt `RestrictedSpeciesService` den unbeschraenkten `romHandler.getSpeciesSetInclFormes()`.

Konsequenz:

- Nach PR #3 ist der RomHandler-Pool erweitert (`speciesList.size=799`, `maxSpeciesIdentityNumber=823`).
- Danach kappt `Settings.tweakForRom()` fuer CFRU/DPE-BPRE den finalen Pool trotzdem auf Gen1-3.
- `limitPokemon=false` hilft nicht, weil `GameRandomizer.setupSpeciesRestrictions()` die Restrictions trotzdem setzt und `limitPokemon` nur noch `removeEvosForPokemonPool()` steuert.

## SpeciesSet und Identitaet

FVX `Species.equals()` und `hashCode()` nutzen `speciesSetIdentityNumber`. Der Default ist `number`. PR #3 nutzt fuer erweiterte BPRE-Hacks:

```text
isRomHack && romCode == BPRE && PokemonCount > Gen3Constants.unhackedMaxPokedex
```

In diesem Modus:

- `Species.number` bleibt die Dex-/Pokedex-ID, damit bestehende Gen3-Schreibpfade weiter mit `pokedexToInternal[species.getNumber()]` arbeiten.
- `speciesSetIdentityNumber` wird auf die interne ID gesetzt, damit `SpeciesSet` nicht auf kompakte Dex-Nummern kollabiert.
- `speciesList` wird aus `pokesInternal` aufgebaut, nicht aus dem Dex-indexierten `pokes`.

Das ist fuer CFRU/DPE minimal sicherer als `Species.number` direkt auf interne ID umzudeuten, weil Wild-, Trainer-, Starter-, Evolution-, Learnset-, TM/HM- und Tutor-Schreibpfade noch viele Dex-ID-basierte Zugriffe enthalten.

## Wild-Randomizer-Lifecycle

Aktueller FVX-Pfad:

1. `WildEncounterRandomizer.randomizeEncounters()` liest Settings wie Zone-Modus, Type-Themes, Evolution-Filter, Legendaries, Alt-Formes und Levelmodifier.
2. `romHandler.getEncounters(useTimeOfDay)` liefert Encounter-Areas.
3. `prepEncounterAreas()` bereitet die Areas vor.
4. `getBannedForWildEncounters()` entfernt verbotene Formes und Sonderfaelle.
5. `allowed = new SpeciesSet(rSpecService.getSpecies(noLegendaries, allowAltFormes, false))`.
6. `allowed.removeAll(banned)`.
7. InnerRandomizer waehlt Ersetzungen.
8. `romHandler.setEncounters(useTimeOfDay, encounterAreas)` schreibt zurueck.

Fuer CFRU/DPE ist Schritt 5 der P0-Engpass: Der erlaubte Pool kommt nicht direkt aus dem erweiterten RomHandler-Pool, sondern aus dem bereits nach Settings gefilterten `RestrictedSpeciesService`.

## UPR-ZX und CyanSMP64 NatDex als Referenz

Ajarmar UPR-ZX:

- `GenRestrictions` kennt Gen1-7.
- `Settings.tweakForRom()` kappt auf `rh.generationOfPokemon()`.
- `AbstractRomHandler` baut Main-Pokemon-Listen ueber statische Species-ID-Ranges.

CyanSMP64 UPR-ZX NatDex:

- `GenRestrictions` kennt Gen1-9, Mega, Eternamax und Regional Forms.
- `limitToGen()` ist auskommentiert und kappt keine hoehere Generation.
- `AbstractRomHandler` erweitert die Range-Logik bis Gen9: `grookey` bis `enamorus`, `sprigatito` bis `pecharunt`, plus Form- und Mega-Ranges.
- Die Referenz zeigt, dass ein NatDex-Randomizer die ROM-Generation nicht als harte Obergrenze fuer den Species-Pool behandeln darf.

Nicht direkt uebertragbar:

- CyanSMP64 UPR-ZX NatDex und CyanSMP64 FireRed NatDex sind aufeinander abgestimmt.
- UPR-FVX muss externe CFRU/DPE-ROM-Hacks heuristisch lesen und kann nicht voraussetzen, dass ROM-Metadaten im CyanSMP64-Format vorhanden sind.

## P0-Fixempfehlung

Minimaler Zielbranch:

```text
compat/upr-fvx-cfru-dpe-gen-restrictions
```

Minimal aendern:

- Eine zentrale Erkennung fuer erweiterte CFRU/DPE-aehnliche BPRE-Hacks nutzen: mindestens `Gen3RomHandler`, `isRomHack`, ROM-Code `BPRE`, `PokemonCount > Gen3Constants.unhackedMaxPokedex`.
- In diesem Modus darf `Settings.tweakForRom()` `currentRestrictions` nicht blind auf `generationOfPokemon() == 3` kappen.
- Alternativ oder zusaetzlich muss `GameRandomizer.setupSpeciesRestrictions()` bei `limitPokemon=false` den unbeschraenkten Pool setzen, also `setRestrictions(null)`.
- Fuer den aktuellen Teststand reicht als Erfolgskriterium zunaechst, dass Gen4-Gen6-Species aus dem bereits korrekt klassifizierten RomHandler-Pool in den finalen Wild-Pool gelangen.

Nicht aendern:

- Keine Aenderung an Species-Identity/PR #3 im selben Branch.
- Keine Day/Night-CFRU-Wildtabellen modellieren.
- Keine Nullslot-`<unknown>`-Behandlung.
- Keine Trainer-, Starter-, Evolution-, Learnset-, TM/HM- oder Tutor-Schreibpfade refactoren.
- Keine RAM-/Tracker-Arbeit.

Erfolgsnachweis:

- ROM-freie Unit-Tests fuer `GenRestrictions`/Settings-Restriction-Verhalten, falls ohne ROM moeglich.
- Clean `:random:jar` nur nach separater Build-Freigabe im Fixblock.
- Wiederholung des bestehenden Gen4+-Wild-Pool-Diagnoselaufs mit denselben Settings.
- Erwartung: `speciesList.size` bleibt erweitert, `maxSpeciesIdentityNumber` bleibt `823`, finaler Wild-Log enthaelt sichtbare Gen4+-Species.
- `<unknown>` bleibt getrennt zu bewerten und darf im P0-Fix nicht als Erfolgskriterium vermischt werden.

## Offene Punkte nach P0

- Gen8/Gen9 im FVX-Settings-Modell: `MAX_GENERATION=7` ist fuer echte Gen9-Ziele zu klein, aber der aktuelle lokale Diagnosepool reicht nur bis Gen6.
- P1 muss alle Gen3-Schreibpfade pruefen, die `pokedexToInternal[species.getNumber()]` nutzen.
- P2 muss CFRU-Day/Night-Custom-Wildtabellen separat lesen/schreiben oder bewusst als nicht unterstuetzt markieren.
