# UPR-FVX CFRU/DPE Generation Mapping Fix

## Datum

2026-05-11

## Diagnose-Ausgangslage

- ROM-Code/Version aus dem vorherigen lokalen Diagnose-Lauf: `BPRE`, `0`.
- `isRomHack=true`.
- `PokemonCount=823`.
- `pokedexCount=386`.
- `speciesList.size=412`.
- `maxInternalSpeciesId=823`.
- `maxSpeciesNumber=411`.
- `generationCounts={1=328, 2=200, 3=295}`.
- Beispiel-Species ueber 386 wurden geladen, aber als Gen3 klassifiziert.
- Wild-Log-`<unknown>`-Rohwerte waren `rawInternalSpeciesId=0` und bleiben in diesem Fix unveraendert.

## Geaenderte Codepfade

UPR-FVX-Branch:

```text
compat/upr-fvx-gen9-generation-mapping
```

Geaendert:

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `romio/src/main/java/com/uprfvx/romio/gamedata/Species.java`

## Technische Entscheidung

`Species.number` bleibt die Pokedex-/Dex-ID. Das ist wichtig, weil viele Gen3-Schreibpfade weiterhin `pokedexToInternal[species.getNumber()]` verwenden.

Fuer erweiterte CFRU/DPE-aehnliche BPRE-Hacks wird stattdessen eine separate SpeciesSet-Identitaet gesetzt:

```text
isRomHack && romCode == BPRE && PokemonCount > Gen3Constants.unhackedMaxPokedex
```

In diesem Modus:

- `SpeciesSet`/`equals()`/`hashCode()` koennen nach interner Species-ID unterscheiden.
- `speciesList` wird aus `pokesInternal` aufgebaut, nicht aus dem durch `PokedexOrder` kollabierenden Dex-Index `pokes`.
- `pokesInternal[i]` bleibt die direkte ROM-interne Species-Zuordnung.
- Dex-basierte Schreibpfade behalten ihre bisherige `Species.number`-Semantik.
- `generationOf()` nutzt in diesem Modus den normalisierten Species-Namen gegen `SpeciesIDs`; dadurch werden z. B. Skrelp, Dragalge, Sylveon und Hawlucha nicht mehr pauschal als Gen3 eingestuft.

## Erwartete neue Werte

Ohne erneuten ROM-Lauf in diesem Arbeitsschritt sind diese Werte erwartete Diagnosewerte:

- `PokemonCount` bleibt `823`.
- `pokedexCount` kann weiterhin den PokedexOrder-/Dex-Raum spiegeln.
- `speciesList.size` soll deutlich ueber `412` liegen, ideal nahe `PokemonCount + 1`, abhaengig von herausgefilterten `unused`-/`?`-Slots.
- `maxSpeciesNumber` kann weiterhin bei `411` liegen, wenn `Species.number` die Dex-ID bleibt.
- `maxSpeciesIdentityNumber` soll `823` erreichen.
- Gen4+-Species sollen nicht mehr pauschal Gen3 sein; bekannte Namen werden ueber `SpeciesIDs` Gen4-Gen9 zugeordnet.

## Risiken

- `Species.equals()`/`hashCode()` nutzen nun eine separate Identitaetsnummer. Standardmaessig entspricht sie weiter `Species.number`; fuer CFRU/DPE-BPRE wird sie intern gesetzt.
- Code, der `Species.compareTo()` fuer Sortierung nutzt, sortiert weiterhin nach `Species.number`, nicht nach interner Identitaet.
- Species-Namen muessen zu den `SpeciesIDs`-Konstanten normalisierbar sein. Unbekannte Namen fallen auf die bisherige Dex-ID-basierte Generationsermittlung zurueck.
- Legend-/Ultra-Beast-Listen bleiben Dex-ID-basiert und wurden in diesem Branch nicht erweitert.
- Wild-Encounter-`rawInternalSpeciesId=0` bleibt ein separates Nullslot-Thema.

## Offene Folgepunkte

1. Denselben lokalen CFRU/DPE-Teststand erneut mit Diagnoseausgabe laden.
2. Pruefen, ob `speciesList.size` nahe `PokemonCount + 1` liegt und `maxSpeciesIdentityNumber=823` erscheint.
3. Pruefen, ob Beispiel-Species ueber 386 generationstreu klassifiziert werden.
4. Danach separat bewerten, ob `rawInternalSpeciesId=0` legitime leere/sonderfallartige Wildslots oder ein Lesefehler sind.
