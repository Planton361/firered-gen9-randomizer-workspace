# UPR-FVX CFRU/DPE Palette Save Blocker

## Datum

2026-05-12

## Ziel und Sicherheitsrahmen

Read-only Diagnose des neuen Save-Pfad-Blockers nach Gen9-SpeciesCount-Fix, defensivem Palette-Load und lazy Trainer-Moveset-Fix.

Dieser Block nimmt keine Codeaenderungen, keine funktionalen Fixes, keine ROM-Aenderungen und keine Builds vor. P1 Static/Gift bleibt pausiert.

## Kurzfazit

Der neue Blocker liegt nicht mehr im SpeciesCount, nicht im Palette-Load und nicht in `saveTrainers()`/`getMovesLearnt()`. Der lokale Lauf nach dem Lazy-Trainer-Movesets-Unblocker erreicht `AbstractRomHandler.prepareSaveRom()` bis `savePokemonPalettes()` und bricht dort ab:

```text
java.lang.IllegalArgumentException: no compressed data found at offset 0x16b9c08
  at compressors.DSDecmp.Decompress(DSDecmp.java:41)
  at Gen3RomHandler.lengthOfCompressedDataAt(...)
  at AbstractGBRomHandler$DataRewriter.rewriteData(...)
  at Gen3RomHandler.rewriteCompressedPalette(...)
  at Gen3RomHandler.savePokemonPalettes(...)
  at AbstractRomHandler.prepareSaveRom(...)
```

`0x16b9c08` ist hier nicht der Palette-Tabellen-Slot, sondern der alte Palette-Datenoffset, den `DataRewriter` vor dem Repointing dekomprimieren will. Als GBA-Adresse ist das `0x096B9C08`; in DPE `offsets.ini` ist dieser Wert `gFrontSprite252Pal`.

DPE `Palette_Table.c` verwendet `gFrontSprite252Pal` mehrfach fuer die historischen internen Gap-/Dummy-Slots `[252]..[276]` zwischen Celebi und Treecko. FVX speichert Pokemon-Paletten derzeit auch dann neu, wenn Palette-Randomization nicht aktiv war. Dadurch versucht der Save-Pfad, alle geladenen Paletten zu repointen. Das kollidiert mit gemeinsam genutzten Palette-Daten und der Annahme in `rewriteCompressedData()`, dass es nur einen Pointer auf den alten komprimierten Datenblock gibt.

## Relevante Dateien

| Bereich | Datei | Befund |
|---|---|---|
| FVX Save-Lifecycle | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java` | `prepareSaveRom()` ruft `savePokemonPalettes()` immer auf |
| FVX Load-Lifecycle | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractGBRomHandler.java` | `loadGameData()` ruft `loadPokemonPalettes()` immer auf |
| FVX Gen3 Palette-Save | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java` | `savePokemonPalettes()` iteriert alle Species und schreibt normal/shiny Paletten zurueck |
| FVX DataRewriter | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractGBRomHandler.java` | liest alten Pointer, bestimmt alte Datenlaenge, free-space't alte Daten und repointet |
| FVX Species-Palette-Felder | `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Species.java` | `normalPalette`/`shinyPalette` speichern geladene Paletten, aber keinen "modified" oder "saveable" Zustand |
| FVX Palette-Randomizer | `02_external/upr-fvx/random/src/main/java/com/uprfvx/random/GameRandomizer.java`, `randomizers/Gen3to5PaletteRandomizer.java` | Pokemon-Palette-Randomization laeuft nur bei `PokemonPalettesMod.RANDOM` |
| DPE Palettentabelle | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Palette_Table.c` | `[252]..[276]` zeigen alle auf `gFrontSprite252Pal` |
| DPE Shiny-Palettentabelle | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Shiny_Palette_Table.c` | `[252]..[276]` zeigen analog auf `gBackShinySprite252Pal` |
| DPE Offsets | `02_external/Dynamic-Pokemon-Expansion-Gen-9/offsets.ini` | `gFrontSprite252Pal: 096B9C08` |
| DPE Runtime | `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/updated_code.c` | Runtime laedt Sprite-Paletten bedarfsbezogen pro Species |

## Warum laeuft `savePokemonPalettes()`?

`savePokemonPalettes()` ist nicht an die Palette-Randomizer-Option gekoppelt. Der Save-Lifecycle ist allgemein:

```text
AbstractRomHandler.saveRom()
  -> prepareSaveRom()
       -> saveSpeciesStats()
       -> saveMoves()
       -> saveTrainers()
       -> savePokemonPalettes()
```

`GameRandomizer.maybeRandomizePokemonPalettes()` prueft dagegen separat:

```text
if (settings.getPokemonPalettesMod() == PokemonPalettesMod.RANDOM)
    paletteRandomizer.randomizePokemonPalettes()
```

Im lokalen CFRU/DPE-Diagnoselauf ist Palette-/Sprite-Randomization aus. Der Save-Blocker entsteht also nicht, weil Paletten kosmetisch geaendert wurden, sondern weil FVX geladene Paletten bedingungslos wieder speichert.

## Codepfad im Palette-Save

`Gen3RomHandler.savePokemonPalettes()`:

```text
for pk in getSpeciesSet():
    pokeNumber = pokedexToInternal[pk.getNumber()]
    normalPalPointerOffset = PokemonNormalPalettes + pokeNumber * 8
    shinyPalPointerOffset = PokemonShinyPalettes + pokeNumber * 8

    if CFRU/DPE and missing loaded palette:
        skip
    else:
        rewriteCompressedPalette(normalPalPointerOffset, pk.getNormalPalette())
        rewriteCompressedPalette(shinyPalPointerOffset, pk.getShinyPalette())
```

Der defensive PR #9-Schutz greift nur fuer `null`/fehlende geladene Paletten. Er verhindert nicht, dass gueltig geladene, aber unveraenderte oder gemeinsam genutzte Palette-Daten spaeter neu geschrieben werden.

`rewriteCompressedPalette()` nutzt `rewriteCompressedData()`. Der Kommentar dort ist fuer diesen Befund zentral:

```text
Assumes there is only one pointer to the compressed data.
```

Der DPE-Gap-Bereich `[252]..[276]` verletzt genau diese Annahme, weil viele Tabellen-Slots denselben Datenpointer `gFrontSprite252Pal` teilen.

## Betroffene Adresse und wahrscheinlicher Index

Die Fehleradresse:

```text
0x16b9c08 + 0x08000000 = 0x096B9C08
```

In DPE `offsets.ini`:

```text
gFrontSprite251CelebiPal 096B9A5C
gFrontSprite252Pal       096B9C08
gFrontSprite277TreeckoPal 096B9EE4
```

In DPE `Palette_Table.c`:

```text
[SPECIES_CELEBI] = {gFrontSprite251CelebiPal, SPECIES_CELEBI, 0x0},
[252] = {gFrontSprite252Pal, 0xfc, 0x0},
...
[276] = {gFrontSprite252Pal, 0x114, 0x0},
[SPECIES_TREECKO] = {gFrontSprite277TreeckoPal, SPECIES_TREECKO, 0x0},
```

Damit ist der alte Datenblock eindeutig `gFrontSprite252Pal`. Der erste konkrete `Species`-Eintrag, der im FVX-Save diese Adresse erreicht, ist ohne zusaetzliche ROM-Instrumentierung nicht final belegt. Wahrscheinlich ist der Ausloeser ein SpeciesSet-Eintrag mit Dex-/Mapping-basiertem `pokeNumber` im Bereich `252..276`, also der bekannte Palette-Pfad-Mismatch `pokedexToInternal[Species.number]` statt stabiler interner Species-Identitaet.

## Problemklassifikation

Der Befund spricht nicht fuer einen Nullslot wie beim Loader-Blocker `SPECIES_CUBONE_A`.

Wahrscheinlicher ist eine Kombination aus:

- gemeinsam genutztem DPE-Palette-Datenpointer (`gFrontSprite252Pal` fuer `[252]..[276]`);
- FVX-Save schreibt alle geladenen Pokemon-Paletten neu, auch unveraenderte;
- `DataRewriter` free-space't den alten Datenblock nach dem ersten Repoint;
- ein spaeterer Slot zeigt noch auf denselben alten Datenblock und `lengthOfCompressedDataAt()` kann dort keine komprimierten Daten mehr finden;
- der Palette-Pfad nutzt weiterhin `pokedexToInternal[Species.number]`, was fuer CFRU/DPE bereits beim Palette-Load als Mapping-Risiko belegt ist.

Ob `gFrontSprite252Pal` selbst unkomprimiert oder anders komprimiert ist, ist aus Source allein nicht abschliessend zu beweisen. Der vorherige defensive Load loggte nur zwei fehlende normal/shiny Paletten und erreichte den Save-Pfad; daher wurde dieser Datenpointer beim Load offenbar nicht als invalid/fehlend behandelt. Das spricht staerker fuer "mehrfach geteilter und beim Save bereits freigegebener Datenblock" als fuer "von Anfang an unlesbarer Palette-Block".

## Zusammenhang mit defensivem Palette-Load

Der defensive Palette-Load/-Save aus PR #9 schuetzt zwei Faelle:

- ungueltige oder nullinitialisierte Palette-Pointer beim Load werden nicht fatal;
- Species mit fehlender geladener Normal- oder Shiny-Palette werden beim Save uebersprungen.

Der neue Blocker liegt ausserhalb dieses Schutzes. Die betroffene Palette ist nicht `null`, sondern gilt als geladen und speicherbar. Der Save-Pfad hat aber keine Information darueber, ob die Palette jemals veraendert wurde oder ob ihr alter Datenblock von mehreren Tabelleintraegen geteilt wird.

## Ist Palette-Save fuer P0/CFRU-DPE noetig?

Fuer die aktuelle CFRU/DPE-Kompatibilitaetsstufe ist Palette-Save fachlich nicht noetig, solange keine Palette-/Sprite-Randomization aktiv ist:

- Wild-Randomization braucht Species-IDs, Namen, Stats und Encounter-Schreibpfade.
- Trainer-/Static-/Starter-Schreibpfade brauchen keine Pokemon-Palette-Daten.
- Palette-Randomization ist eine explizite kosmetische Option und im aktuellen Diagnoseprofil ausgeschaltet.

Technisch ist Palette-Save aktuell trotzdem Teil von `prepareSaveRom()`. Ein minimaler Fix sollte den Save-Pfad fuer unveraenderte Paletten optional oder defensiv machen, statt den SpeciesCount wieder zu reduzieren.

## Vergleich zu CyanSMP64 NatDex

CyanSMP64 FireRed NatDex haelt die Gap-Semantik ebenfalls sichtbar: `SPECIES_TREECKO` liegt bei `277`, und der Bereich zwischen Celebi und Treecko ist kein normaler Gen3-National-Dex-Speciesbereich. Die Runtime laedt Sprite-Paletten bedarfsbezogen ueber Species und Formlogik.

Der fuer FVX relevante Unterschied bleibt: Cyan repointet nicht pauschal beim Randomizer-Save alle Pokemon-Paletten. Die NatDex-Referenz stuetzt daher die Fixrichtung, Palette-Daten nur dann zu schreiben, wenn ein Palette-Feature sie wirklich veraendert hat oder ein dediziertes Graphics-Profil die geteilten Pointer kennt.

## Fixoptionen

| Option | Beschreibung | Vorteile | Risiken |
|---|---|---|---|
| A | `savePokemonPalettes()` nur ausfuehren, wenn Pokemon-Palette-Randomization aktiv war | kleinster P0-Unblocker; keine unnoetigen Palette-Repoints; Vanilla kann unveraendert bleiben | Handler kennt Settings aktuell nicht direkt; braucht saubere Zustandsuebergabe |
| B | Fuer CFRU/DPE Species ohne gueltige speicherbare Palette oder mit geteilter/unsicherer Palette ueberspringen | bleibt im Handler gekapselt; schuetzt weitere DPE-Sonderfaelle | braucht Tracking von Pointer-Zieladressen oder Saveability; Palette-Randomizer bleibt partial |
| C | Paletten als immutable/unmodified markieren und nur modified Paletten speichern | technisch sauberer; verhindert unnoetige Writes auch ausserhalb CFRU/DPE | braucht Modell-/State-Erweiterung in `Species` oder Handler |
| D | DPE/CFRU Graphics-Profil | langfristig korrekt fuer Forms, Gap-Slots, geteilte Pointer und echte Grafikfeatures | groesserer Folgeblock; nicht minimal fuer P0/Wild |

Count weiter begrenzen ist keine empfohlene Option, weil dadurch die bereits erreichte Gen9-Coverage wieder verloren ginge.

## Empfehlung

Minimaler naechster Fix: fuer konservativ erkannte CFRU/DPE-Gen9-BPRE-Hacks Pokemon-Palette-Save ueberspringen, solange Pokemon-Palette-Randomization nicht aktiv war.

Begruendung:

- Der aktuelle Diagnose-Lauf hat keine Palette-Randomization aktiv.
- Der Save-Pfad schreibt aktuell unveraenderte Paletten und erzeugt dadurch den Blocker.
- Ein Skip fuer unveraenderte CFRU/DPE-Paletten ist enger und risikoaermer als ein DPE-Graphics-Profil oder ein Learnset-/Trainer-Fix.
- Palette-Randomization fuer CFRU/DPE sollte bis zum Graphics-Profil als partial/unsupported gelten.

Falls Settings-Zugriff im Handler zu gross waere, ist die naechstbeste kleine Variante Option C/B: geladene Paletten nicht automatisch als speicherpflichtig behandeln und unsichere/geteilte Pointer-Ziele nicht repointen.

## Risiken und offene Fragen

- Der erste konkrete Species-Eintrag, der `gFrontSprite252Pal` im Save erreicht, ist ohne zusaetzliche Instrumentierung nicht final belegt.
- Weitere gemeinsam genutzte Palette-Daten oder Form-/Gap-Slots koennen nach `0x16b9c08` folgen.
- Der `pokedexToInternal[Species.number]`-Grafikpfad bleibt semantisch falsch fuer CFRU/DPE-Forms und muss spaeter durch ein Graphics-Profil oder interne-ID-Nutzung ersetzt werden.
- Ein Skip von Palette-Save darf nicht versehentlich echte Palette-Randomization verschlucken; der Fix muss klar an "Palette-Randomization nicht aktiv / keine Palette geaendert" gebunden sein.
- Nach dem Palette-Save-Unblocker koennen weitere Save-Pfade sichtbar werden, bevor ein nutzbarer Wild-Log entsteht.

## Naechster minimaler Schritt

Separater UPR-FVX-Fixbranch: `savePokemonPalettes()` fuer CFRU/DPE nur dann ausfuehren, wenn Pokemon-Palette-Randomization wirklich aktiv war oder Paletten explizit geaendert wurden. Kein Count-, Learnset-, Trainer-, Static/Gift-, Wild- oder Day/Night-Fix im selben Branch.
