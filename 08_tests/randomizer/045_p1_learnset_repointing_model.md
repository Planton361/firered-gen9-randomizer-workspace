# 045 - CFRU/DPE Learnset Repointing Model

## Ziel

Full Learnset-Write-Repointing-Modell fuer CFRU/DPE Gen9-BPRE read-only klaeren. Kein Fix, kein Repointing und keine Randomizer-Codeaenderung in diesem Branch.

## Kontext

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model`
- Voraussetzung: UPR-FVX PR #23 und Workspace PR #81 sind gemerged.
- Ausgangsstand: Diagnose 044 bestaetigt bounded in-place `setMovesLearnt()` fuer strikt validierte same-size Writes.
- Offener Kernblocker: Full Learnset randomization braucht ein belastbares Repointing-/Tabellenmodell.

## Relevante Dateien und Symbole

### UPR-FVX

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
  - `CFRU_DPE_LEVEL_UP_LEARNSETS_POINTER_LOCATION = 0x3EA7C`
  - `getCfruDpeMovesLearnt()`
  - `setCfruDpeMovesLearnt(...)`
  - `lengthOfCfruDpeMovesLearntAt(...)`
  - `isCfruDpeMovesLearntSafeForInPlaceWrite(...)`
  - `getCfruDpeLevelUpLearnsetsOffset()`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractGBRomHandler.java`
  - `DataRewriter`
  - `freeSpace(...)`
  - `findAndUnfreeSpace(...)`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`
  - `[Fire Red (U) 1.0]`
  - `FreeSpace=0x800000`
  - `PokemonMovesets=0x25D7B4`

### CFRU/DPE

- `02_external/Dynamic-Pokemon-Expansion-Gen-9/repointall`
  - `gLevelUpLearnsets 0803EA7C` unter `EXPAND_LEARNSETS`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/scripts/make.py`
  - `OFFSET_TO_PUT = 0x1600000`
  - `SEARCH_FREE_SPACE = False`
  - `FindOffsetToPut(...)` nur optional
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/scripts/insert.py`
  - ROM wird auf `32MB` erweitert
  - `repointall` repointet Symbol-Pointer auf neu gebaute Symboladressen
- `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c`
  - `LEVEL_UP_MOVE(lvl, move) {move, lvl}`
  - `LEVEL_UP_END {0x0, 0xFF}`
  - `gLevelUpLearnsets[]`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Learnsets.c`
  - `struct __attribute__((packed)) LevelUpMove { u16 move; u8 level; }`
- `02_external/CFRU-expansion/include/new/learn_move.h`
  - `MAX_LEARNABLE_MOVES 50`
- `02_external/CFRU-expansion/include/constants/species.h`
  - `SPECIES_NONE = 0x0`
  - `SPECIES_EGG = 0x19C`
  - `SPECIES_PECHARUNT = 0x59F`
  - `NUM_SPECIES = 0x5A0` / `1440`
- `02_external/CFRU-expansion/include/constants/moves.h`
  - `MOVE_PSYCHICNOISE = 0x3DF`
  - `MOVES_COUNT = 0x3E0` / `992`

## Pointertable-Ort und Zielpointer-Region

`repointall` belegt nur den Pointer-Ort:

```text
gLevelUpLearnsets 0803EA7C
```

Als ROM-Offset:

```text
0x03EA7C
```

Diagnose 044 sah im getesteten ROM:

```text
0x03EA7C -> 0x0825D7B4
ROM offset: 0x25D7B4
```

Damit liegt die aktive Pointertable in der klassischen FireRed-Region, die FVX bereits als `PokemonMovesets=0x25D7B4` kennt. Wichtig: `0x03EA7C` ist der Pointer-Ort, `0x25D7B4` ist die aktive Tabelle. Repointing von Learnsets betrifft die Eintraege innerhalb dieser Tabelle, nicht den Pointer-Ort selbst, solange die Tabelle in-place erhalten bleibt.

Bei `NUM_SPECIES=0x5A0` braucht die Pointertable:

```text
1440 species * 4 bytes = 5760 bytes = 0x1680
```

Wenn die Tabelle bei `0x25D7B4` beginnt, reicht der volle interne Species-Bereich rechnerisch bis exklusiv:

```text
0x25D7B4 + 0x1680 = 0x25EE34
```

## Warum Diagnose 044 `skippedInvalidPointer=1412` meldet

Der bounded Writer aus Diagnose 044 verwendet eine strikte Safety-Pruefung:

- Pointer muss als GBA-ROM-Pointer lesbar sein.
- Die Zieladresse muss innerhalb der ROM liegen.
- Innerhalb von maximal `50` Eintraegen muss Sentinel `{0, 0xFF}` gefunden werden.
- Jeder Nicht-Sentinel-Move muss in `moves.total=992` geladen sein.

Der Diagnose-Harness hatte viele rohe pointertable-artige Werte gesehen, die wie Learnsetdaten geparst werden konnten, aber invalid move-like Werte bis `0xFFFF` enthielten. Deshalb wurden sie als unsafe behandelt. `skippedInvalidPointer=1412` bedeutet in diesem Modell nicht, dass 1412 Species fachlich unbeschreibbar sind; es bedeutet, dass der aktuelle Writer den Pointertable-/Keying-Scope nicht belastbar genug nachweisen kann, um diese Ziele in-place zu mutieren.

Plausible Ursachen aus dem Quellenmodell:

- FVX iteriert `speciesList`/`numRealPokemon`, nicht zwingend exakt `0..NUM_SPECIES-1`.
- `getCfruDpeMovesLearnt()` nutzt weiterhin `romEntry.PokemonMovesets` und `pokedexToInternal[pk.getNumber()]`, waehrend Full Write interne `SpeciesSet`-Identitaet braucht.
- Viele Alt-Forms teilen Learnset-Zielarrays; ein blindes Schreiben pro Species waere fachlich falsch.
- Raw Pointertable-Scans ohne Symbol-/ROM-Map koennen Daten hinter der echten Tabelle als Pointer interpretieren.

## Gueltige Pointerbereiche

Gueltige Learnset-Zielpointer muessen GBA-ROM-Pointer sein:

```text
0x08000000 <= pointer < 0x0A000000
```

Als ROM-Offset:

```text
0 <= offset < rom.length
```

Fuer den getesteten 32MB-CFRU/DPE-Stand ist die absolute Obergrenze rechnerisch:

```text
0x08000000 <= pointer < 0x0A000000
0x0000000 <= offset < 0x2000000
```

Zusaetzlich muss die Zielregion als Learnset validieren:

- 3-Byte-Alignment ist fachlich nicht notwendig, weil `LevelUpMove` gepackt ist.
- 4-Byte-Alignment ist fuer neue Blobs trotzdem empfehlenswert, weil FVX-FreeSpace-Allokation und GBA-Pointerdaten ueblicherweise long-aligned arbeiten.
- Sentinel `{0, 0xFF}` muss innerhalb `MAX_LEARNABLE_MOVES=50` Eintraegen gefunden werden.
- Move IDs muessen `0 < move < moves.total`.

## Shared-Pointer-Situation

Quelltabellenanalyse aus `CFRU-expansion/src/Tables/level_up_learnsets.c`:

| Metric | Value |
|---|---:|
| definierte Learnset-Arrays | `1104` |
| `gLevelUpLearnsets[]`-Zuweisungen | `1408` |
| eindeutige Ziele in der Tabelle | `1104` |
| shared Zielgruppen | `148` |
| maximale Source-Learnset-Laenge | `41` Eintraege |
| maximale Byte-Laenge inkl. Sentinel | `126` Bytes |
| eindeutiger Blob-Bedarf nach Source-Targets | `56829` Bytes |
| per-Species Blob-Bedarf ohne Sharing | `72249` Bytes |

Grosse Shared-Gruppen:

- `sUnownLevelUpLearnset`: `28` Species/Formes
- `sVivillonLevelUpLearnset`: `20`
- `sArceusLevelUpLearnset`: `18`
- `sSilvallyLevelUpLearnset`: `18`
- `sPikachuLevelUpLearnset`: `17`
- `sFurfrouLevelUpLearnset`: `10`
- `sMiniorShieldLevelUpLearnset`: `8`
- `sAlcremieLevelUpLearnset`: `8`

Policy-Folge:

- Full randomization darf Shared-Zielpointer nicht unbewusst gemeinsam mutieren.
- Sicherste Policy fuer Full Write: pro interner Species einen eigenen neuen Learnset-Blob schreiben und den Pointertable-Eintrag auf diesen Blob setzen.
- Alternative Sharing-Erhaltung ist nur sicher, wenn alle Species einer Shared-Gruppe exakt denselben neuen Learnset bekommen sollen.

## Freie ROM-Bereiche und Append-Kandidaten

Aus den Quellen ist kein belastbarer, statisch reservierter freier Learnset-Append-Bereich fuer Randomizer-Repointing belegt.

Befunde:

- DPE `make.py` insertet seine Erweiterung standardmaessig ab `0x1600000`.
- `SEARCH_FREE_SPACE = False` bedeutet: DPE sucht beim Build nicht automatisch nach einem freien Bereich, sondern nutzt den festen Insert-Ort.
- `insert.py` erweitert die ROM auf `32MB`.
- FVX FireRed-RomEntry nutzt fuer Vanilla `FreeSpace=0x800000` und markiert freie Bereiche ueber `0xFF`-Scans als nutzbar.

Bewertung:

- `0x1600000` ist kein freier Randomizer-Bereich; dort liegt sehr wahrscheinlich CFRU/DPE-Code/-Daten.
- `0x800000` ist nur der historische Startpunkt fuer FVX-FF-FreeSpace-Scans, kein Beleg fuer sichere Learnset-Repointing-Fläche im konkreten CFRU/DPE-ROM.
- Ein spaeterer Fix darf freien Speicher nicht hart codieren. Er muss entweder FVX `findAndUnfreeSpace(...)` nutzen oder einen ROM-spezifisch nachgewiesenen freien Bereich verwenden.

## Zentrales neues Learnset-Blob-Modell

Ein zentraler neuer Learnset-Blob ist plausibel:

1. Alle neu geschriebenen Learnset-Arrays werden in einem zusammenhaengenden oder per-FVX-FreeSpace allokierten Bereich geschrieben.
2. Die bestehende Pointertable bei `0x25D7B4` bleibt in-place.
3. Jeder Pointertable-Eintrag fuer eine echte interne Species wird auf den passenden neuen Array-Anfang gesetzt.
4. Placeholder-/Null-Species werden auf `sEmptyMoveset`-Aequivalent oder unveraendert belassen.
5. Shared-Gruppen werden explizit entschieden: entweder dedupliziert, wenn Daten identisch sind, oder pro Species getrennt.

Vorteil:

- Keine Erweiterung des Pointertable-Orts noetig, solange `NUM_SPECIES=1440` und die bestehende Tabelle `0x1680` Bytes umfasst.
- Reload nutzt automatisch dieselbe Tabelle, wenn `getMovesLearnt()` die Pointertable liest.

Risiko:

- Die aktuelle Reader-/Writer-Keying-Logik muss vollstaendig auf interne Species-ID ausgerichtet werden, sonst werden falsche Table-Slots repointed.

## Pointertable-Updates

Pointertable-Update-Regeln fuer einen spaeteren Fix:

- Pointertable-Basis via `readRequiredCfruDpePointer(0x03EA7C, 4, "gLevelUpLearnsets")` lesen.
- Fuer jede interne Species-ID `0..1439` Pointer bei `base + species * 4` schreiben.
- Pointer little-endian als GBA-ROM-Pointer speichern: `romOffset + 0x08000000`.
- `SPECIES_NONE` und `SPECIES_EGG` nicht randomisiert schreiben.
- Alt-Forms nur mit bewusster Policy repointen.

Die Pointertable selbst muss nicht repointed werden, solange `NUM_SPECIES` nicht ueber die vorhandene Tabelle hinaus erweitert wird.

## Alignment, Endian und Sentinel

- Pointertable-Eintraege: `u32` little-endian GBA-ROM-Pointer.
- Learnset-Eintraege: gepackte `3` Bytes.
- Move: `u16` little-endian.
- Level: `u8`.
- Sentinel: `00 00 FF`.
- Level `0` ist erlaubt, solange Move nicht `0` ist.
- Maximaler Runtime-Loop: `MAX_LEARNABLE_MOVES=50`.
- Empfohlenes Blob-Alignment: `4` Bytes, obwohl Entry-Format nur `3` Bytes braucht.

## Reload-Verhalten

Reload ist konzeptionell stabil, wenn:

- die Pointertable-Eintraege auf valide GBA-ROM-Pointer zeigen,
- alle Blobs im saved ROM liegen,
- jeder Blob Sentinel `{0, 0xFF}` innerhalb `50` Eintraegen enthaelt,
- Move IDs im geladenen FVX-Move-Modell vorhanden sind.

Diagnose 044 bestaetigte bereits `writeReloadLearnsetMismatches=0` fuer bounded in-place Write. Fuer Repointing muss derselbe Vergleich nach Pointertable-Update erfolgen, bevorzugt nach interner SpeciesSet-Identitaet statt Pokedex-ID.

## Growth-Faelle und Speicherabschaetzung

Jeder Learnset braucht:

```text
entryCount * 3 + 3 bytes
```

Maximal unter CFRU-Runtime-Cap:

```text
50 * 3 + 3 = 153 bytes pro Species
```

Worst-case fuer `NUM_SPECIES=1440`, ohne Sharing:

```text
1440 * 153 = 220320 bytes
```

Quellenbasierter Ist-Stand:

- eindeutige Source-Ziele: `56829` Bytes
- per-Species ohne Sharing: `72249` Bytes
- maximaler Source-Learnset: `41` Eintraege / `126` Bytes inkl. Sentinel

Folge:

- Full randomization kann deutlich mehr Speicher brauchen als der heutige Blob-Bestand.
- Worst-case bleibt unter `256 KiB`, aber nur ein ROM-/FreeSpace-Scan kann belegen, ob ein zusammenhaengender Bereich existiert.
- FVX kann alternativ mehrere kleinere Blobs per `findAndUnfreeSpace(...)` allokieren; ein zentraler zusammenhaengender Blob ist einfacher zu diagnostizieren, aber nicht zwingend.

## Risiken durch SpeciesSet, Placeholder und Alt-Forms

- `Species.getNumber()` ist fuer Full Write nicht ausreichend.
- Interne `SpeciesSet`-Identitaet muss der Pointertable-Index sein.
- `SPECIES_NONE` und `SPECIES_EGG` duerfen nicht randomisiert werden.
- Formes koennen fachlich getrennte oder gemeinsame Learnsets haben; das muss eine bewusste Policy sein.
- Deduplizierung nach identischem neuen Learnset ist moeglich, darf aber nicht aus alter Shared-Pointer-Struktur blind abgeleitet werden.

## Minimaler spaeterer Fixpfad

1. Nur CFRU/DPE Gen9-BPRE eng gaten.
2. `gLevelUpLearnsets` Pointertable-Basis ueber `0x03EA7C` lesen und validieren.
3. Vollstaendige interne Species-ID-Schluesselung fuer Read und Write verwenden.
4. Vor dem Schreiben geplante neue Learnset-Blobs erzeugen und validieren.
5. Speicherbedarf berechnen und freie ROM-Fläche mit FVX-FreeSpace-Mechanik oder belegtem Append-Bereich reservieren.
6. Neue Blobs schreiben.
7. Pointertable-Eintraege little-endian auf die neuen Blobs setzen.
8. Placeholder-/Null-Species skippen oder auf einen bewusst gewaehlten Empty-Learnset-Pointer setzen.
9. Shared-Pointer-Policy explizit implementieren: per Species getrennt oder nur bei identischen neuen Daten deduplizieren.
10. Reload-Diagnose nach interner SpeciesSet-Identitaet mit `writeReloadLearnsetMismatches`, invalid moves, highest move/species und Growth-/Repoint-Zaehlung.

## Offene Fragen

- Ob der konkrete CFRU/DPE-Test-ROM einen ausreichend grossen zusammenhaengenden `0xFF`-Bereich fuer einen zentralen Learnset-Blob hat, ist ohne ROM-Scan nicht belastbar belegt.
- Ob FVX `getMovesLearnt()` fuer CFRU/DPE komplett auf interne Species-ID-Keying umgestellt werden soll oder parallel Pokedex-Keys fuer Legacy-Aufrufer liefern muss, ist eine Implementierungsentscheidung.
- Ob Full Write Shared-Gruppen erhalten, aufbrechen oder nach identischen neuen Daten deduplizieren soll, muss fachlich entschieden werden.
- Ob `SPECIES_NONE`/`SPECIES_EGG` unveraendert bleiben oder auf einen neuen Empty-Learnset-Pointer zeigen sollen, sollte im Fixbranch explizit diagnostiziert werden.

## Ergebnis

Full Learnset-Write-Repointing ist modellseitig machbar, aber nicht durch eine harte Append-Adresse oder einen impliziten `DataRewriter`-Einsatz abgesichert. Der belastbare Pfad ist: bestehende Pointertable bei `0x25D7B4` behalten, neue `u16 move + u8 level` Learnset-Blobs in nachgewiesen freie ROM-Fläche schreiben, Pointertable-Eintraege pro interner Species-ID aktualisieren und Reload ueber interne SpeciesSet-Identitaet validieren.
