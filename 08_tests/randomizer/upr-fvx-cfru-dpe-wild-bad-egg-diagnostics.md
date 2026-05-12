# UPR-FVX CFRU/DPE Wild Bad Egg Diagnostics

Datum: 2026-05-12

## Ziel

Dieser Arbeitsblock diagnostiziert die `12` `Bad Egg`-Eintraege aus dem bestaetigten CFRU/DPE-Gen9-Standard-/Fallback-Wild-Log.

Keine Codeaenderungen, keine Fixes und keine ROM-/Build-Artefakte wurden committed.

## UPR-FVX Stand

```text
repo: Planton361/universal-pokemon-randomizer-fvx
branch: compat/firered-gen9-cfru-dpe
commit: ee82cb4e Merge pull request #11 from Planton361/compat/upr-fvx-cfru-dpe-skip-unchanged-palette-save
```

Der Submodule-Status war sauber. `origin` zeigt auf den Planton361-Fork.

## Build

```sh
cd 02_external/upr-fvx
./gradlew clean :random:jar
```

Ergebnis: `BUILD SUCCESSFUL`.

## Lokaler Diagnose-Lauf

Derselbe lokale CFRU/DPE-Route-1-Fallback-Teststand wurde mit Wild-Randomization, `limitPokemon=false`, ohne Gen1-3-Einschraenkung und ohne Trainer-/Starter-/Evolution-/Learnset-/TM-/Tutor-/Ability-/Palette-/Sprite-Randomization gestartet.

Der Seed entspricht dem Gen9-Wild-Post-Merge-Smoke:

```text
274269061345319
```

ROM- und Output-Artefakte blieben lokal unter `05_builds/**` und wurden nicht committed.

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar cli \
  -i 05_builds/cfru-dpe-gen9-route1-fallback-smoke/test.gba \
  -o 05_builds/upr-fvx-cfru-dpe-wild-bad-egg-diagnostics.gba \
  -S "<settings-string>" \
  -z 274269061345319 \
  -l
```

CLI-Exit-Code: `0`.

```text
Randomized successfully!
```

## Coverage bleibt stabil

Der Lauf reproduziert die bestaetigte Gen9-Wild-Coverage:

```text
PokemonCount=1439
pokedexCount=1290
speciesList.size=1415
maxInternalSpeciesId=1439
maxSpeciesNumber=1290
maxSpeciesIdentityNumber=1439
generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
```

Die bekannten CFRU/DPE-Unblocker sind aktiv:

```text
[CFRU-DPE-PALETTE] skipped invalid pokemon palettes during load: normal=2 shiny=2
[CFRU-DPE-PALETTE] skipped unchanged pokemon palette save for CFRU/DPE Gen9 BPRE
```

Save und Log-Erzeugung funktionieren:

```text
saveSuccessful=true
```

## Bad-Egg-Auswertung

Ausgewertet wurden `2176` sichtbare Wild-Slots im Log.

```text
Bad Egg=12
<unknown>=0
```

Alle `12` `Bad Egg`-Eintraege liegen in einem einzigen vollstaendigen 12-Slot-Block:

| Area | Encounter-Type | Slot | Level |
|---|---|---:|---:|
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 1 | 22 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 2 | 24 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 3 | 20 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 4 | 26 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 5 | 22 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 6 | 24 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 7 | 28 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 8 | 18 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 9 | 20 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 10 | 26 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 11 | 20 |
| `Area #174 - ALTERING CAVE Grass/Cave (rate=5)` | Grass/Cave | 12 | 26 |

Kontext im Log:

```text
Area #173 - ALTERING CAVE Grass/Cave (rate=5)
Necrozma Lv22
Necrozma Lv24
...

Area #174 - ALTERING CAVE Grass/Cave (rate=5)
Bad Egg Lv22
Bad Egg Lv24
Bad Egg Lv20
Bad Egg Lv26
Bad Egg Lv22
Bad Egg Lv24
Bad Egg Lv28
Bad Egg Lv18
Bad Egg Lv20
Bad Egg Lv26
Bad Egg Lv20
Bad Egg Lv26

Area #175 - ALTERING CAVE Grass/Cave (rate=5)
Mamoswine Lv22
Mamoswine Lv24
...
```

Das Muster ist nicht gestreut. Es sieht aus wie eine area-/game-1:1-Ersetzung fuer eine komplette Altering-Cave-Variante.

## Source- und Code-Befunde

DPE/CFRU fuehren `SPECIES_EGG` als internen Species-Slot innerhalb des geladenen Count-Bereichs:

```text
Dynamic-Pokemon-Expansion-Gen-9/include/species.h:
#define SPECIES_EGG 0x19C

CFRU-expansion/include/constants/species.h:
#define SPECIES_EGG 0x19C
```

`0x19C` ist dezimal `412` und liegt damit klar innerhalb `1..1439`.

Die DPE-Name-Quelle mappt diesen Slot auf den sichtbaren Log-Namen:

```text
Dynamic-Pokemon-Expansion-Gen-9/strings/Pokemon_Name_Table.string:
#org @NAME_BAD_EGG
Bad Egg
```

DPE gibt `SPECIES_EGG` zwar Tabellenwerte, aber keine spielbare Kampf-Statistik:

```text
Dynamic-Pokemon-Expansion-Gen-9/src/Base_Stats.c:
[SPECIES_EGG] =
{
    .baseHP = 0,
    .baseAttack = 0,
    .baseDefense = 0,
    .baseSpAttack = 0,
    .baseSpDefense = 0,
    .baseSpeed = 0,
    .type1 = TYPE_NORMAL,
    .type2 = TYPE_NORMAL,
    ...
}
```

CFRU selbst behandelt `SPECIES_EGG` an mehreren Stellen als nicht kampffaehige Sonder-Species, etwa ueber:

```text
CFRU-expansion/include/battle_util.h:
SPECIES_CANT_BATTLE(species) (species == SPECIES_NONE || species == SPECIES_EGG)
```

FVX baut den Wild-Pool dagegen allgemein aus dem unrestricted Species-Set:

```text
WildEncounterRandomizer:
SpeciesSet allowed = new SpeciesSet(rSpecService.getSpecies(noLegendaries, allowAltFormes, false));
allowed.removeAll(banned);
```

Bei `limitPokemon=false` setzt `RestrictedSpeciesService` ohne Generation-Restriktionen `allInclAltFormes` auf `romHandler.getSpeciesSetInclFormes()`. Danach filtert es Alt-Formes, aber keine Egg-/Dummy-/None-Species speziell heraus.

Der Gen3-Wild-Ban in `Gen3RomHandler.getBannedForWildEncounters()` bannt fuer FRLG nur Unown:

```text
// Ban Unown in FRLG because the game crashes if it is encountered outside of Tanoby Ruins.
banned.add(pokes[SpeciesIDs.unown]);
```

In `SpeciesIDs.java` gibt es keine eigene `egg`-/`badEgg`-Konstante. Damit kann der bestehende Gen3-Ban den DPE-Slot `SPECIES_EGG=0x19C` nicht erfassen.

## Interpretation

Wahrscheinlichste Ursache: `SPECIES_EGG` gelangt als regulaere, nicht gebannte Species in den Allowed Pool und wird im area-/game-1:1-Wild-Randomizer als Ersatz fuer eine komplette Altering-Cave-Variante ausgewaehlt.

Das spricht gegen ein reines Log-Mapping-Problem:

- Der Logger zeigt fuer nicht aufgeloeste Species explizit `<unknown>`.
- `<unknown>` bleibt im Lauf `0`.
- `Bad Egg` ist ein normal geladener Species-Name aus DPE.

Das spricht auch gegen einen Write-/Reload-Fehler:

- Der CLI-Lauf speichert erfolgreich.
- Die `Bad Egg`-Eintraege sind nicht zufaellig verteilt, sondern alle 12 Slots einer Area.
- Die Levelstruktur der Altering-Cave-Area bleibt erhalten.

Nicht vollstaendig bewiesen ist die konkrete Roh-ID im Log, weil `RandomizationLogger` fuer aufgeloeste Species keine interne ID oder SpeciesSet-Identity ausgibt. Aus Source- und Namensbefund ist `SPECIES_EGG=0x19C` aber der naheliegende Kandidat.

## Dummy-/Gap-Risiko

`SPECIES_EGG` ist der sichtbare Befund. DPE/CFRU enthalten daneben weitere nicht normale Slots, etwa `SPECIES_NONE=0` und historische Gap-/Dummy-Slots mit Platzhalterdaten. Der aktuelle Lauf zeigt nur `Bad Egg` und kein `<unknown>`, aber ein CFRU/DPE-spezifisches Banned-Set sollte nicht nur diesen einen Namen betrachten.

## Ist ein Code-Diagnosebranch noetig?

Fuer den praktischen Fix ist der Befund stark genug: `Bad Egg` ist als DPE-Species-Slot bekannt, wird nicht gebannt und erscheint exakt als Wild-Ersatz.

Fuer einen wasserdichten Roh-ID-Beleg waere ein kleiner UPR-FVX-Diagnosebranch sinnvoll, der fuer Wild-Replacements den Namen, `speciesSetIdentityNumber`, `number`, Area und Slot protokolliert. Ohne Codeaenderung laesst sich die interne ID der `Bad Egg`-Logzeilen aus dem bestehenden Log nicht direkt ablesen.

## Fixoptionen

| Option | Beschreibung | Bewertung |
|---|---|---|
| A | CFRU/DPE-spezifisch `SPECIES_EGG`, `SPECIES_NONE` und bekannte Dummy-/Gap-Species im Wild-Banned-Set ergaenzen | Minimaler sinnvoller Fix; geringes Risiko fuer Vanilla, wenn strikt auf erweiterten CFRU/DPE-BPRE-Modus begrenzt |
| B | Banned-Species-Liste aus DPE/CFRU-Source ableiten, z. B. `SPECIES_NONE`, `SPECIES_EGG`, zero-stat placeholders und ggf. Gap-/Dummy-Namen | Robuster, aber mehr Modellierungsaufwand |
| C | Log-/Mapping-Problem untersuchen | Nur noetig, falls Roh-ID-Diagnose zeigt, dass nicht `SPECIES_EGG` geschrieben wird |
| D | Wild-Logger temporaer um Roh-ID-/SpeciesSet-Identity-Diagnose erweitern | Gute Absicherung vor dem Fix, aber kein funktionaler Fix |

## Empfehlung

Naechster minimaler Fix: ein kleiner UPR-FVX-Branch, der fuer konservativ erkannte CFRU/DPE-Gen9-BPRE-Hacks `SPECIES_EGG=0x19C` und `SPECIES_NONE=0` sicher aus Wild-Replacement-Pools entfernt. Wenn im selben Patch vertretbar, sollten dokumentierte Dummy-/Gap-Slots ebenfalls CFRU/DPE-spezifisch gebannt werden.

Optional davor: ein sehr kleiner Roh-ID-Diagnosebranch fuer Wild-Replacements, falls die PR den exakten Roh-ID-Nachweis enthalten soll.

## Risiken

- Altering Cave ist im CFRU/DPE-Modell partial/unsupported; die `Bad Egg`-Area ist daher ein Symptom im sichtbaren Standard-/Fallback-Wild-Log, aber nicht automatisch ein vollstaendiger Altering-Cave-Support-Nachweis.
- Ein zu breites Banned-Set koennte echte Formes entfernen. Der Fix sollte daher nicht pauschal nach Namen wie `?` filtern, sondern an belegte CFRU/DPE-Sonder-Species und sichere Strukturmerkmale gebunden werden.
- DPE/CFRU enthalten weitere Sonderformen und Dummy-Slots; `SPECIES_EGG` zu bannen beseitigt wahrscheinlich die 12 sichtbaren `Bad Egg`-Eintraege, beweist aber noch nicht, dass alle nicht spielbaren Slots ausgeschlossen sind.
