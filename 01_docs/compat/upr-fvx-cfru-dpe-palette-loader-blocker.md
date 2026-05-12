# UPR-FVX CFRU/DPE Palette Loader Blocker

## Datum

2026-05-12

## Ziel und Sicherheitsrahmen

Read-only Diagnose des neuen Loader-Blockers nach dem CFRU/DPE-Gen9-SpeciesCount-Fix. Mit `PokemonCount=1439` erreicht UPR-FVX Gen7/8/9 im Species-Load, bricht danach aber in `Gen3RomHandler.loadPokemonPalettes()` mit einem ungueltigen Pointer ab.

Dieser Block nimmt keine Codeaenderungen, keine funktionalen Fixes, keine ROM-Aenderungen und keine Builds vor. P1 Static/Gift bleibt pausiert.

## Kurzfazit

Der neue Blocker liegt nicht mehr in der Count-Erkennung. `AbstractGBRomHandler.loadGameData()` ruft `loadPokemonPalettes()` fest im allgemeinen ROM-Load auf:

```text
loadItems()
loadSpeciesStats()
loadEvolutions()
loadMoves()
loadPokemonPalettes()
loadTrainers()
```

Der lokale Lauf nach UPR-FVX PR #8 belegt:

```text
PokemonCount=1439
speciesList.size=1415
generationCounts={1=271, 2=118, 3=188, 4=174, 5=191, 6=127, 7=123, 8=127, 9=120}
java.lang.IllegalArgumentException: No valid pointer at 0x1a495d8.
  at Gen3RomHandler.loadPokemonPalettes(...)
```

Die Adresse `0x1a495d8` passt exakt zu DPE `gMonPaletteTable + 1038 * 8`, wenn man den generierten DPE-Offset `gMonPaletteTable: 09A47568` als GBA-Adresse nimmt:

```text
0x09A47568 - 0x08000000 = 0x1A47568
0x1A495D8 - 0x1A47568 = 0x2070
0x2070 / 8 = 1038 = 0x40E
```

`0x40E` ist `SPECIES_CUBONE_A`. In `Dynamic-Pokemon-Expansion-Gen-9/src/Palette_Table.c` und `src/Shiny_Palette_Table.c` gibt es Eintraege fuer die Nachbarn `SPECIES_EXEGGUTOR_A` und `SPECIES_MAROWAK_A`, aber keinen Eintrag fuer `SPECIES_CUBONE_A`. Bei einem C-Array mit Designated Initializers bleibt dieser Slot dadurch nullinitialisiert. FVX liest den Null-Pointer als GBA-Pointer und wirft deshalb `No valid pointer`.

## Relevante Dateien

| Bereich | Datei | Befund |
|---|---|---|
| FVX Lifecycle | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractGBRomHandler.java` | `loadPokemonPalettes()` ist Teil des generischen `loadGameData()` |
| FVX Gen3 Palette Load | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | iteriert `getSpeciesSet()` und liest normal/shiny Palette-Pointer ohne defensive Pointer-Pruefung |
| FVX Species-Palette-Felder | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java` | `Species` haelt `normalPalette` und `shinyPalette` fuer Palette-Randomization/Grafikzugriff |
| FVX Palette Randomizer | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/randomizers/Gen3to5PaletteRandomizer.java` | nutzt `pk.getNormalPalette()` nur, wenn Palette-Randomization aktiv ist |
| DPE Palettentabellen | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Palette_Table.c`, `src/Shiny_Palette_Table.c` | `gMonPaletteTable[NUM_SPECIES]`, `gMonShinyPaletteTable[NUM_SPECIES]`; `SPECIES_CUBONE_A` fehlt |
| DPE generierte Offsets | `02_external/Dynamic-Pokemon-Expansion-Gen-9/offsets.ini` | `gMonPaletteTable: 09A47568`, `gMonShinyPaletteTable: 09A55EAC` |
| DPE Runtime | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/updated_code.c` | Runtime greift per Species auf `gMonPaletteTable[species]`/`gMonShinyPaletteTable[species]` zu |
| CFRU Runtime | `02_external/CFRU-expansion/src/scripting.c`, `src/follower_mon.c`, `BPRE.ld` | CFRU nutzt ebenfalls `gMonPaletteTable[species]`/`gMonShinyPaletteTable[species]` |
| Cyan NatDex FireRed | `02_external/references/cyansmp64-pokefirered-natdex/src/rom_header_gf.c`, `src/pokemon.c`, `tools/inigen/inigen.c` | exportiert Mon-Palette-Tabellen im ROM-Header; Runtime laedt Paletten bedarfsbezogen |

## FVX-Lifecycle

UPR-FVX laedt Paletten fuer GBA-ROMs immer beim ROM-Load, bevor Randomizer-Settings entscheiden, ob Pokemon-Paletten ueberhaupt veraendert werden:

```text
AbstractGBRomHandler.loadGameData()
  -> loadItems()
  -> loadSpeciesStats()
  -> loadEvolutions()
  -> loadMoves()
  -> loadPokemonPalettes()
  -> loadTrainers()
```

`GameRandomizer.maybeRandomizePokemonPalettes()` ruft den Palette-Randomizer dagegen nur auf, wenn `settings.getPokemonPalettesMod() == RANDOM`. Der lokale Smoke nutzt keine Palette-Randomization. Der Blocker entsteht also nicht durch eine aktivierte Palette-Randomizer-Option, sondern durch das generische Vorausladen aller Pokemon-Paletten.

Zusaetzlich ruft `AbstractRomHandler.prepareSaveRom()` immer `savePokemonPalettes()` auf. Das ist fuer einen spaeteren Fix wichtig: Palette-Load einfach zu deaktivieren reicht nur dann, wenn der Save-Pfad bei unveraenderten Paletten nicht versucht, null Palettes zurueckzuschreiben.

## Gen3-Palette-Load in FVX

Der Gen3-Code ist streng und vanilla-nah:

```text
normalPaletteTableOffset = PokemonNormalPalettes
shinyPaletteTableOffset = PokemonShinyPalettes
for pk in getSpeciesSet():
    pokeNumber = pokedexToInternal[pk.getNumber()]
    normalPalOffset = readPointer(normalPaletteTableOffset + pokeNumber * 8)
    pk.setNormalPalette(readPalette(normalPalOffset))
    shinyPalOffset = readPointer(shinyPaletteTableOffset + pokeNumber * 8)
    pk.setShinyPalette(readPalette(shinyPalOffset))
```

Risiken dieses Modells fuer CFRU/DPE:

- Es nutzt `Species.number` und `pokedexToInternal`, nicht die interne SpeciesSet-Identitaet.
- Es erwartet fuer jeden geladenen SpeciesSet-Eintrag einen gueltigen `CompressedSpritePalette`-Pointer.
- `readPointer(offset)` wirft sofort, wenn der gelesene Pointer `0`, ausserhalb der ROM oder anderweitig ungueltig ist.
- Es gibt keinen Modus "Palette nicht geladen, weil Palette-Randomization nicht aktiv ist".

## Konkreter Pointer-Befund

Der lokale Fehler:

```text
No valid pointer at 0x1a495d8
```

ist der Pointer-Slot, aus dem FVX lesen wollte, nicht zwingend der Zielpointer. `readPointer()` wirft mit der Slot-Adresse, wenn `readLong(slot) - 0x8000000` nicht in den ROM-Bereich faellt.

Die DPE-Offsets ordnen ihn ein:

| Wert | Bedeutung |
|---|---:|
| `gMonPaletteTable` aus `offsets.ini` | `09A47568` |
| als ROM-Offset | `0x1A47568` |
| Fehler-Slot | `0x1A495D8` |
| Abstand | `0x2070` |
| Strukturbreite | `8` Bytes |
| Tabellenindex | `1038` / `0x40E` |
| DPE/CFRU Species | `SPECIES_CUBONE_A` |

In DPE `include/species.h`:

```text
SPECIES_CUBONE_A 0x40E
SPECIES_MAROWAK_A 0x40F
```

In DPE `Palette_Table.c` und `Shiny_Palette_Table.c`:

```text
[SPECIES_EXEGGUTOR_A] = ...
[SPECIES_MAROWAK_A] = ...
```

Ein `SPECIES_CUBONE_A`-Eintrag fehlt in beiden Tabellen. Das ist fuer DPE/CFRU nicht zwingend ein Engine-Absturz, solange diese Species/Form nie oder nur ueber fallback-/form-spezifische Logik benutzt wird. Fuer FVX ist es aber ein Load-Blocker, weil FVX alle SpeciesSet-Eintraege pauschal vorlaedt.

## Standard-Gen3-Kompatibilitaet der DPE/CFRU-Paletten

DPE/CFRU verwenden weiterhin die klassische `struct CompressedSpritePalette`-Form:

```text
data pointer
tag
filler
```

Die Tabellen sind also strukturell Gen3-kompatibel. Der Unterschied ist semantisch:

- DPE hat `NUM_SPECIES=1440` interne Slots inklusive Forms/Sonderformen.
- Nicht jeder interne Slot muss fuer UPR-FVX pauschal als voll randomisierbare Species mit eigener, gueltiger Palette behandelt werden.
- Omitted Designated Initializers sind in C valide, erzeugen aber Nullslots.
- FVX kann mit Nullslots in Palette-Tabellen aktuell nicht umgehen.

Der konkrete Blocker ist daher kein Beleg, dass die gesamte DPE-Palette-Struktur falsch ist. Er belegt, dass der FVX-Palette-Loader fuer CFRU/DPE defensive Behandlung von fehlenden/ungueltigen Palette-Slots oder ein eigenes Graphics-Profil braucht.

## Ist Palette-Loading fuer P0/Wild noetig?

Fuer den aktuellen P0-/Coverage-Zweck ist Palette-Loading nicht fachlich notwendig:

- Wild-Randomization schreibt Species-IDs in Encounter-Tabellen.
- Starter/Static/Trainer-Schreibpfade brauchen Species-IDs, Stats, Namen und ggf. Trainerdaten, aber keine vorgeladenen Palette-Objekte.
- Pokemon-Palette-Randomization ist eine eigene kosmetische Option und in den aktuellen Smoke-Settings nicht aktiv.

Technisch ist Palette-Loading in FVX derzeit trotzdem notwendig, weil `loadGameData()` und `prepareSaveRom()` es bedingungslos verwenden. Ein Fix muss deshalb entweder defensiv laden und speichern oder den Palette-Pfad fuer nicht genutzte Paletten sauber optional machen.

## Vergleich zu CyanSMP64 NatDex

CyanSMP64 FireRed NatDex exportiert `monNormalPalettes = gMonPaletteTable` und `monShinyPalettes = gMonShinyPaletteTable` im ROM-Header. Die Runtime-Funktionen `GetMonSpritePalFromSpeciesAndPersonality()` und `GetMonSpritePalStructFromOtIdPersonality()` greifen bedarfsbezogen auf `gMonPaletteTable[formSpecies]` zu und fallbacken nur fuer ungueltige Species oberhalb `NUM_SPECIES`.

Der CyanSMP64 UPR-ZX-NatDex-Referenzhandler zeigt keinen FVX-aehnlichen globalen `loadPokemonPalettes()`-Pfad fuer Gen3. Die NatDex-INI wird aus Symbolen generiert (`PokemonCount=NUM_SPECIES - 1`), aber die Randomizer-Referenz laedt Paletten nicht pauschal fuer alle NatDex-Species beim ROM-Open.

Schlussfolgerung: Cyan bestaetigt die Architekturidee, bekannte Expansion-Builds ueber explizite Profil-/Symbolquellen zu behandeln. Es liefert keinen direkten "skip invalid palette" Drop-in-Fix fuer FVX, zeigt aber, dass Palette-Tabellen nicht zwingend vor jeder nicht-kosmetischen Randomization global dekomprimiert werden muessen.

## Fixoptionen

| Option | Beschreibung | Vorteile | Risiken |
|---|---|---|---|
| A | Paletten defensiv laden; ungueltige Pointer ueberspringen oder auf null/fallback setzen | kleiner Loader-Fix; Wild/Species-Load kann weiterlaufen; Palette-Randomizer kann invalide Species gezielt auslassen | Save-Pfad muss null/fallback kennen; kosmetische Features koennen fuer einzelne Forms fehlen |
| B | Palette-Load fuer CFRU/DPE deaktivieren, solange keine Palette-Randomization genutzt wird | passend fuer P0/Wild/Count; minimiert nicht noetige Grafikannahmen | `prepareSaveRom()` darf dann nicht blind `savePokemonPalettes()` schreiben; GUI/Bildvorschau kann Paletten erwarten |
| C | DPE/CFRU-spezifisches Graphics-/Palette-Profil | langfristig sauber; kann Forms, fallback-Paletten und echte DPE-Offsets modellieren | groesserer Aufwand; braucht systematische Symbol-/Offset-Quelle und Regression-Tests |
| D | Count weiter begrenzen | vermeidet Paletten-Nullslot kurzfristig | nicht bevorzugt; wuerde Gen9-Coverage wieder verlieren und die Ursache verdecken |

## Empfehlung

Der naechste minimale Fix sollte nicht den Count zurueckdrehen. Empfohlen ist Option A, eng auf CFRU/DPE-BPRE gekapselt:

1. `loadPokemonPalettes()` prueft Palette-Pointer defensiv, wenn `hasExtendedBpreHackSpeciesPool()` aktiv ist.
2. Ungueltige normal/shiny Palette-Slots werden nicht zum ROM-Load-Abbruch.
3. Palette-Randomization bleibt fuer Species ohne gueltige Paletten deaktiviert oder ueberspringt diese Species.
4. `savePokemonPalettes()` schreibt nur Paletten zurueck, die gueltig geladen oder absichtlich randomisiert wurden.

Option B ist ein moeglicher noch kleinerer P0-Unblocker, muss aber zusammen mit dem Save-Pfad betrachtet werden. Option C bleibt die langfristig richtige Richtung fuer vollstaendige CFRU/DPE-Grafikkompatibilitaet.

## Risiken und offene Fragen

- Ohne erneute ROM-Instrumentierung ist nur der erste Abbruchslot belegt. Weitere ausgelassene oder ungueltige Palette-Slots koennen nach `SPECIES_CUBONE_A` folgen.
- `pokedexToInternal[Species.number]` bleibt im Palette-Pfad ein Dex-/Mapping-Risiko; ein defensiver Pointer-Fix loest nicht automatisch korrektes Form-/Dex-Mapping.
- DPE-Runtime kann mit bestimmten fehlenden Form-Paletten anders umgehen als FVX, weil sie Paletten bedarfsbezogen und mit Formlogik laedt.
- Palette-Randomization sollte fuer CFRU/DPE erst freigegeben werden, wenn ein Graphics-/Palette-Profil die Nullslots und Form-Semantik explizit modelliert.

## Naechster minimaler Schritt

In einem separaten UPR-FVX-Fixbranch `loadPokemonPalettes()` und `savePokemonPalettes()` fuer konservativ erkannte erweiterte CFRU/DPE-BPRE-Hacks defensiv machen. Ziel ist nur, den ROM-Load bis zur bestehenden Wild-Randomization wieder zu erreichen; kein Static/Gift-, Trainer-, Moveset-, Learnset- oder Count-Fix im selben Branch.
