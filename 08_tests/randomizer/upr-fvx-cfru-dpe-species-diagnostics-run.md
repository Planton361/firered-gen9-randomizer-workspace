# UPR-FVX CFRU/DPE Species Diagnostics Run

## Datum

2026-05-11

## UPR-FVX-Stand

- Fork: `Planton361/universal-pokemon-randomizer-fvx`
- Branch: `analysis/log-cfru-dpe-species-diagnostics`
- Commit: `6a8ea276 chore: add CFRU DPE species diagnostics`
- PR: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/2`
- PR-Status fuer diesen Lauf: nicht gemerged; lokaler Branch/Commit direkt genutzt.

## Lokaler Teststand

- Verwendet wurde der vorhandene lokale CFRU/DPE-Route-1-Fallback-Teststand aus `05_builds/`.
- Input-ROM, Output-ROM, Konsolenlog und Randomizer-Log blieben lokal/ignored unter `05_builds/`.
- Keine ROMs, Builds, Randomizer-JARs, Saves oder Emulator States wurden committed.
- Keine privaten absoluten Pfade werden in diesem Protokoll dokumentiert.

## Build und Start

Build:

```sh
cd 02_external/upr-fvx
./gradlew :random:jar
./gradlew clean :random:jar
```

Hinweis: Der erste inkrementelle Build war erfolgreich, das erzeugte JAR war beim CLI-Start aber wegen doppelter GUI-Designer-Instrumentierung unbrauchbar. Der Clean-Build war erfolgreich und wurde fuer den Diagnose-Lauf verwendet.

CLI-Lauf, relativ zum Workspace:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-species-diagnostics.gba \
  -S "<bestehende Smoke-Test-Settings>" \
  -z 274269061345319 \
  -l
```

## Artefakte

Lokale Artefakte, nicht committed:

- Console/stderr: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-species-diagnostics-console.log`
- Randomizer-Log: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-species-diagnostics.gba.log`
- Output-ROM: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-species-diagnostics.gba`

Hashes der lokalen Diagnose-Artefakte:

```text
98d0ec702dff7a8be500c362cca556a1d4e50b97921a65f6448bd0887ea97bb9  upr-fvx-cfru-dpe-species-diagnostics.gba
d014280d199ac5d8283c39ab3c3c056946c8d037300ad0dd03c19475c6b096ad  upr-fvx-cfru-dpe-species-diagnostics.gba.log
8c8b1a14116b17da2f23700dc6752272a454714278db03e17b9aab8501347ab0  upr-fvx-cfru-dpe-species-diagnostics-console.log
```

## Diagnosewerte aus stderr

```text
ROM code=BPRE
version=0
isRomHack=true
PokemonCount=823
pokedexCount=386
speciesList.size=412
maxInternalSpeciesId=823
maxSpeciesNumber=411
generationCounts={1=328, 2=200, 3=295}
```

Beispiel-Species `> 386`:

| Internal ID | Species-/Dex-Nummer | Name | Generation laut FVX |
|---:|---:|---|---:|
| 798 | 387 | Skrelp | 3 |
| 799 | 388 | Dragalge | 3 |
| 800 | 389 | Clauncher | 3 |
| 801 | 390 | Clawitzer | 3 |
| 802 | 391 | Helioptile | 3 |
| 803 | 392 | Heliolisk | 3 |
| 804 | 393 | Tyrunt | 3 |
| 805 | 394 | Tyrantrum | 3 |
| 806 | 395 | Amaura | 3 |
| 807 | 396 | Aurorus | 3 |
| 808 | 397 | Sylveon | 3 |
| 809 | 398 | Hawlucha | 3 |

## `<unknown>`-Eintraege

Der Gen3RomHandler gab dieselben Rohbefunde im CLI-Lauf zweimal aus, weil der Lauf Encounter beim Randomisieren/Loggen erneut liest. Die Tabelle listet die eindeutigen Rohbefunde.

| Area | Encounter-Type | Slots | rawInternalSpeciesId | Datenoffset |
|---|---|---:|---:|---|
| VIRIDIAN FOREST Grass/Cave | WALKING | 9, 11 | 0 | `0x3C7528` |
| POWER PLANT Grass/Cave | WALKING | 4, 5, 8, 10 | 0 | `0x3C7F0C` |
| BERRY FOREST Grass/Cave | WALKING | 1 | 0 | `0x3C8254` |
| PATTERN BUSH Grass/Cave | WALKING | 0, 2, 8, 10 | 0 | `0x3C8450` |
| CAPE BRINK Grass/Cave | WALKING | 3, 6 | 0 | `0x3C88BC` |
| BOND BRIDGE Grass/Cave | WALKING | 3 | 0 | `0x3C8940` |
| RESORT GORGEOUS Surfing | SURFING | 1 | 0 | `0x3C89FC` |
| WATER LABYRINTH Surfing | SURFING | 1 | 0 | `0x3C8A48` |
| FIVE ISLE MEADOW Grass/Cave | WALKING | 3, 6 | 0 | `0x3C8A94` |
| FIVE ISLE MEADOW Surfing | SURFING | 1 | 0 | `0x3C8ACC` |
| MEMORIAL PILLAR Grass/Cave | WALKING | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 | 0 | `0x3C8B18` |
| MEMORIAL PILLAR Surfing | SURFING | 1 | 0 | `0x3C8B50` |
| WATER PATH Grass/Cave | WALKING | 6 | 0 | `0x3C8C34` |
| ROUTE 12 Grass/Cave | WALKING | 9, 11 | 0 | `0x3C91F8` |
| ROUTE 13 Grass/Cave | WALKING | 9, 11 | 0 | `0x3C927C` |
| ROUTE 14 Grass/Cave | WALKING | 7 | 0 | `0x3C9300` |
| ROUTE 15 Grass/Cave | WALKING | 9, 11 | 0 | `0x3C9338` |
| FIVE ISLAND Surfing | SURFING | 1 | 0 | `0x3C9A74` |
| ALTERING CAVE Grass/Cave | WALKING | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 | 0 | `0x3C9C80` |

Der Randomizer-Wild-Log zeigt die korrespondierenden `<unknown>`-Zeilen mit Area-/Encounter-Kontext. Der Logger selbst hat keinen Rohwertzugriff; der Rohwert kommt aus stderr und ist in allen eindeutigen Faellen `0`.

## Technische Interpretation

### Count-Problem?

Teilweise ja. `PokemonCount=823` und `maxInternalSpeciesId=823` zeigen, dass FVX mehr als Vanilla-386 interne Slots laedt. Gleichzeitig ist `pokedexCount=386`, `speciesList.size=412` und `maxSpeciesNumber=411`. Damit ist der geladene Randomizer-Species-Pool effektiv auf den klassischen FireRed/National-Dex-Umfang plus die bekannten Zusatzslots begrenzt, obwohl interne DPE-Slots bis 823 vorhanden sind.

### Generation-Mapping-Problem?

Ja. Die Beispiel-Species oberhalb 386 werden geladen, aber alle als Generation 3 markiert. Das bestaetigt, dass `Gen3RomHandler.generationOf()` fuer diesen Build keine Gen4-Gen9-Zuordnung liefern kann.

### Interne ID vs. Dex-ID-Mapping-Problem?

Ja, sehr wahrscheinlich. Die Beispiele zeigen interne IDs 798-809, aber Species-/Dex-Nummern 387-398. FVX mappt also DPE-interne IDs ueber `PokedexOrder` auf einen kompakten Dex-/Species-Nummernbereich. Die `<unknown>`-Wild-Slots sind dagegen Rohwert `0`; das ist kein Gen4+-Rohslot, sondern ein leerer/ungemappt wirkender Encounter-Wert, der beim Logging zu `null` wird.

## Minimaler naechster Fixvorschlag

Naechster Branch:

```text
compat/upr-fvx-gen9-generation-mapping
```

Minimaler Umfang:

1. Nur die Species-Generation-Zuordnung fuer Gen3-Hacks mit erweiterten National-Dex-Nummern korrigieren, idealerweise zentral ueber SpeciesID-Ranges Gen1-9.
2. Keine `PokemonCount`-Heuristik im selben Schritt aendern.
3. Danach denselben Diagnose-Lauf wiederholen und pruefen, ob Gen4+-Species im erlaubten Wild-Pool generationstreu erscheinen.
4. `<unknown>` mit `rawInternalSpeciesId=0` separat behandeln; zuerst klaeren, ob diese Nullslots aus Vanilla/Fallback-Wilddaten legitime leere Slots, Altering-Cave-/Sevii-Sonderdaten oder ein Lesefehler sind.

## Sicherheitsstatus

- Keine ROMs committed.
- Keine Builds committed.
- Keine Randomizer-JARs committed.
- Keine Saves oder Emulator States angefasst.
- Keine Original-Upstreams kontaktiert.
- Keine funktionalen Fixes vorgenommen.
