# UPR-FVX CFRU/DPE Generation Mapping Diagnostics Run

## Datum

2026-05-11

## UPR-FVX-Stand

- Fork: `Planton361/universal-pokemon-randomizer-fvx`
- PR: `https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/3`
- Branch: `compat/upr-fvx-gen9-generation-mapping`
- Commit: `223ee9efaf1a29435674cbe6a03f25011364b2a1`
- Commit-Titel: `compat: preserve CFRU DPE species identity`
- PR-Status fuer diesen Lauf: nicht gemerged; lokaler Branch/Commit direkt genutzt.

## Lokaler Teststand

- Verwendet wurde derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand aus `05_builds/` wie im vorherigen Diagnose-Lauf.
- Input-ROM, Output-ROM, Konsolenlog und Randomizer-Log blieben lokal/ignored unter `05_builds/`.
- Keine ROMs, Builds, Randomizer-JARs, Saves oder Emulator States wurden committed.
- Keine privaten absoluten Pfade werden in diesem Protokoll dokumentiert.

## Build und Start

Build:

```sh
cd 02_external/upr-fvx
./gradlew clean :random:jar
```

CLI-Lauf, relativ zum Workspace:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/randomizer-smoke/upr-fvx-cfru-dpe-generation-mapping-diagnostics.gba \
  -S "<bestehende Smoke-Test-Settings>" \
  -z 274269061345319 \
  -l
```

## Artefakte

Lokale Artefakte, nicht committed:

- Console/stderr: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-generation-mapping-diagnostics-console.log`
- Randomizer-Log: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-generation-mapping-diagnostics.gba.log`
- Output-ROM: `05_builds/randomizer-smoke/upr-fvx-cfru-dpe-generation-mapping-diagnostics.gba`

Hashes der lokalen Diagnose-Artefakte:

```text
9deaf9277d37506101a9ec55b2bba74ebcd322af36227fc088575b557630c200  upr-fvx-cfru-dpe-generation-mapping-diagnostics.gba
00b178e4534719cc9cc32ef74bcbcad8f47ed62ac9ee8ce24c8fe8d0de7e069a  upr-fvx-cfru-dpe-generation-mapping-diagnostics.gba.log
70ca71e03c2ad8af81e0e87409b5549d11ac95efc821a6efb48d21b3130d1315  upr-fvx-cfru-dpe-generation-mapping-diagnostics-console.log
```

## Vorher/Nachher

| Wert | Vor PR #3 | Nach PR #3 |
|---|---:|---:|
| `PokemonCount` | 823 | 823 |
| `pokedexCount` | 386 | 386 |
| `speciesList.size` | 412 | 799 |
| `maxInternalSpeciesId` | 823 | 823 |
| `maxSpeciesNumber` | 411 | 411 |
| `maxSpeciesIdentityNumber` | nicht geloggt | 823 |

Generation-Counts:

```text
Vorher: {1=328, 2=200, 3=295}
Nachher: {1=177, 2=104, 3=161, 4=139, 5=178, 6=64}
```

## Beispiel-Species ueber 386

| Internal ID | Interne Identitaet | Dex-/Species-Nummer | Name | Generation vorher | Generation nachher |
|---:|---:|---:|---|---:|---:|
| 798 | 798 | 387 | Skrelp | 3 | 6 |
| 799 | 799 | 388 | Dragalge | 3 | 6 |
| 800 | 800 | 389 | Clauncher | 3 | 6 |
| 801 | 801 | 390 | Clawitzer | 3 | 6 |
| 802 | 802 | 391 | Helioptile | 3 | 6 |
| 803 | 803 | 392 | Heliolisk | 3 | 6 |
| 804 | 804 | 393 | Tyrunt | 3 | 6 |
| 805 | 805 | 394 | Tyrantrum | 3 | 6 |
| 806 | 806 | 395 | Amaura | 3 | 6 |
| 807 | 807 | 396 | Aurorus | 3 | 6 |
| 808 | 808 | 397 | Sylveon | 3 | 6 |
| 809 | 809 | 398 | Hawlucha | 3 | 6 |

## Wild-Randomizer-Pool

Der RomHandler-Species-Pool kollabiert nach PR #3 nicht mehr auf den kompakten Dex-Index:

- `speciesList.size` steigt von `412` auf `799`.
- `maxSpeciesIdentityNumber=823` zeigt, dass die interne Species-Identitaet bis zur erkannten `PokemonCount` reicht.
- Die geloggten Beispiel-Species ueber 386 werden generationstreu als Gen6 statt pauschal als Gen3 klassifiziert.

Im konkreten Wild-Pokemon-Log dieses Smoke-Settings-Laufs wurden keine sichtbaren Gen4+-Encounter-Namen gefunden. Die Ausgabe enthaelt weiterhin sichtbare Gen1-3-Namen und `<unknown>`-Eintraege. Damit ist der RomHandler-Pool erweitert, aber die konkrete Randomizer-Ausgabe mit diesem Settings-String beweist noch nicht, dass Gen4+-Species in der finalen Wild-Auswahl landen. Das kann an Generation-Restrictions oder weiteren Wild-Pool-Filtern liegen und sollte separat mit gezielt passenden Settings diagnostiziert werden.

## `<unknown>`-Eintraege

Alle eindeutigen neuen stderr-Befunde fuer `<unknown>` hatten weiterhin `rawInternalSpeciesId=0`.

| Area | Encounter-Type | Slot | rawInternalSpeciesId | Datenoffset |
|---|---|---:|---:|---|
| VIRIDIAN FOREST Grass/Cave | WALKING | 7 | 0 | `0x3C7528` |
| VIRIDIAN FOREST Grass/Cave | WALKING | 8 | 0 | `0x3C7528` |
| VIRIDIAN FOREST Grass/Cave | WALKING | 10 | 0 | `0x3C7528` |
| POKeMON TOWER Grass/Cave | WALKING | 7 | 0 | `0x3C7DF4` |
| POKeMON TOWER Grass/Cave | WALKING | 9 | 0 | `0x3C7DF4` |
| POKeMON TOWER Grass/Cave | WALKING | 7 | 0 | `0x3C7E2C` |
| POKeMON TOWER Grass/Cave | WALKING | 9 | 0 | `0x3C7E2C` |
| POKeMON TOWER Grass/Cave | WALKING | 7 | 0 | `0x3C7E64` |
| POKeMON TOWER Grass/Cave | WALKING | 9 | 0 | `0x3C7E64` |
| POKeMON TOWER Grass/Cave | WALKING | 7 | 0 | `0x3C7E9C` |
| POKeMON TOWER Grass/Cave | WALKING | 9 | 0 | `0x3C7E9C` |
| POKeMON TOWER Grass/Cave | WALKING | 6 | 0 | `0x3C7ED4` |
| POKeMON TOWER Grass/Cave | WALKING | 7 | 0 | `0x3C7ED4` |
| PATTERN BUSH Grass/Cave | WALKING | 1 | 0 | `0x3C8450` |
| SEVAULT CANYON Grass/Cave | WALKING | 2 | 0 | `0x3C8DC0` |
| ROUTE 24 Grass/Cave | WALKING | 8 | 0 | `0x3C96C0` |
| ROUTE 25 Grass/Cave | WALKING | 8 | 0 | `0x3C9744` |

Der Randomizer-Wild-Log zeigt die korrespondierenden `<unknown>`-Zeilen mit Area-/Encounter-Kontext. Der Logger selbst hat keinen Rohwertzugriff; der Rohwert kommt aus stderr.

## Technische Interpretation

PR #3 behebt den dokumentierten SpeciesSet-Kollaps fuer den lokalen CFRU/DPE-BPRE-Teststand:

- `PokemonCount` bleibt stabil bei `823`.
- `pokedexCount` und `maxSpeciesNumber` bleiben Dex-/Pokedex-basiert.
- Die neue interne SpeciesSet-Identitaet erreicht `823`.
- `speciesList.size=799` zeigt, dass der RomHandler jetzt fast alle gueltigen internen Species statt nur den Dex-Index-Bereich nutzt.
- Gen4-Gen6-Species im geladenen Bereich werden nicht mehr pauschal als Gen3 klassifiziert.

Nicht geloest und nicht Ziel dieses Schritts:

- `<unknown>` bleibt ein separates Nullslot-Thema mit `rawInternalSpeciesId=0`.
- Der konkrete Smoke-Settings-Wild-Log zeigt noch keine sichtbaren Gen4+-Encounter-Namen; dafuer braucht es einen separaten Settings-/Pool-Diagnosebranch oder einen gezielten Testlauf mit passenden Generation-Restrictions.
- Gen7-Gen9 erscheinen in diesem Lauf nicht in `generationCounts`; das kann am erkannten `PokemonCount=823`, der konkreten DPE-Namen-/Order-Tabelle oder weiteren Loader-Grenzen liegen.

## Entscheidungsempfehlung

PR #3 mergen.

Begruendung:

- Der Kernbefund `speciesList.size=412` ist mit PR #3 behoben.
- Die interne Identitaet erreicht `823`.
- Die Generation-Klassifizierung der Beispiel-Species ueber 386 ist korrigiert.
- Es wurden keine Nullslot- oder Day/Night-Wild-Tabellen-Fixes vermischt.

Nach dem Merge sollte ein weiterer Analysebranch den finalen Wild-Randomizer-Pool unter gezielten Gen4+-Settings pruefen.
