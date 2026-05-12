# 033 - P1 Move-Datenmodell fuer CFRU/DPE Gen9-BPRE

## Kontext

Ziel dieses Analyseblocks war, das Gen8/9-Move-Datenmodell, die aktuelle FVX-Move-Coverage und die TM-/Tutor-/Egg-Move-Pfade fuer den getesteten CFRU/DPE Gen9-BPRE-Stand read-only zu modellieren.

Gepruefter Stand:

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-move-data-model`
- Voraussetzung: Workspace PR #69 gemerged.
- UPR-FVX-Stand: `655764816f9fefedb9433f33e4da0bc9d44bcda7`
- Ausgangsbefund aus Diagnose 032: `moves.total=559`
- CFRU/DPE-Quellbefund: `MOVES_COUNT = MOVE_PSYCHICNOISE + 1 = 0x3E0 = 992`
- Keine Codeaenderung.
- Keine Aenderung an `02_external/**`.
- Keine Learnset-Write-Ausweitung.

## Relevante Pfade

UPR-FVX:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/constants/Gen3Constants.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/gamedata/Move.java`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`

CFRU/DPE:

- `02_external/CFRU-expansion/include/constants/moves.h`
- `02_external/CFRU-expansion/include/pokemon.h`
- `02_external/CFRU-expansion/include/battle.h`
- `02_external/CFRU-expansion/src/Tables/battle_moves.c`
- `02_external/CFRU-expansion/src/Tables/level_up_learnsets.c`
- `02_external/CFRU-expansion/src/item.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/moves.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/include/tutors.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/TM_Tutor_Tables.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/Egg_Moves.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/assembly/generated/tm_compatibility.s`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/assembly/generated/tutor_compatibility.s`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/repointall`

## FVX-Move-Load und Herkunft von `moves.total=559`

FVX-Gen3 laedt Moves in `Gen3RomHandler.loadMoves()` aus `romEntry`:

- `MoveCount`
- `MoveData`
- `MoveNames`
- `MoveNameLength`

Fuer BPRE-ROM-Hacks wird `MoveData` aus Pointer Block 2 gelesen:

- `MoveData = readPointer(Gen3Constants.moveDataPointer)`
- `Gen3Constants.moveDataPointer = 0x1CC`

Der BPRE-Hack-Support ueberschreibt `MoveCount` nicht aus einer CFRU/DPE-Konstante, sondern scannt die Move-Description-Pointer-Tabelle:

- `descsTable = readPointer(0xE5440)`
- fuer jeden nicht-invaliden Pointer mit plausibler Stringlaenge wird `moveCount++`
- beim ersten invaliden oder unplausiblen Eintrag stoppt die Erkennung

Diagnose 032 meldete `moves.total=559`. Da `getMoves()` eine Java-Liste ueber das Array `moves` liefert und `moves[0]` als Null-/No-Move-Slot enthalten ist, entspricht das praktisch einer geladenen FVX-Coverage bis etwa Move-ID `558`. Alle Move-IDs ab `559` sind fuer FVX in diesem Stand nicht als vollstaendige `Move`-Objekte geladen.

FVX dekodiert Gen3-Move-Records mit fester 12-Byte-Struktur:

- Offset `i * 0xC`
- `+0`: effect
- `+1`: power
- `+2`: type
- `+3`: accuracy
- `+4`: pp
- `+6`: target
- `+7`: priority
- `+8`: flags, aktuell nur Contact-Bit direkt ausgewertet

FVX setzt die Move-Kategorie fuer Gen3 aktuell nicht aus einem gespeicherten Split-Feld, sondern aus dem Typ:

- physische Typen werden `PHYSICAL`
- andere nicht-Status-Damaging-Moves werden `SPECIAL`
- `power == 0` wird meistens `STATUS`

Das ist fuer Vanilla Gen3 plausibel, aber fuer CFRU/DPE mit physisch/speziellem Split pro Move unvollstaendig.

## CFRU/DPE-Move-ID-Grenzen und Coverage-Luecke

CFRU/DPE definiert Move-IDs in `include/constants/moves.h` beziehungsweise DPE `include/moves.h`.

Wichtige Grenzen:

- `MOVE_NONE = 0x0`
- `MOVE_POUND = 0x1`
- `MOVE_STRUGGLE = 0xA5`
- spaete Gen5-Beispiele: `MOVE_HEATCRASH = 0x220`, `MOVE_DRAGONASCENT = 0x22F`
- spaete Gen8-/PLA-Beispiele: `MOVE_THUNDEROUSKICK = 0x2E0`, `MOVE_GLACIALLANCE = 0x2E6`, `MOVE_DIRECLAW = 0x2E7`
- Max-Move-Bereich: `MOVE_MAX_GUARD = 0x334`
- Gen9-Beginn: `MOVE_AQUACUTTER = 0x39B`
- Gen9-Ende: `MOVE_PSYCHICNOISE = 0x3DF`
- `MOVES_COUNT = MOVE_PSYCHICNOISE + 1 = 0x3E0 = 992`
- `NON_Z_MOVE_COUNT = MOVE_GLACIALLANCE + 1`

Folgerung:

- FVX `moves.total=559` deckt nur einen Teil der CFRU/DPE-Move-ID-Skala ab.
- Move-IDs `559..991` sind nicht als vollstaendige FVX-Move-Daten geladen.
- Gen9-Moves `0x39B..0x3DF` sind vollstaendig ausserhalb der aktuellen FVX-Coverage.
- Ein Teil spaeter Gen5- und die Gen6/7/8-/PLA-/Max-/G-Max-Move-Bereiche liegen ebenfalls ausserhalb oder nur teilweise innerhalb der aktuellen Coverage.

## CFRU/DPE-`BattleMove`-Layout

CFRU definiert `struct BattleMove` in `include/pokemon.h`:

- `u8 effect`
- `u8 power`
- `u8 type`
- `u8 accuracy`
- `u8 pp`
- `u8 secondaryEffectChance`
- `u8 target`
- `s8 priority`
- `u8 flags`
- `u8 z_move_power`
- `u8 split`
- `u8 z_move_effect`

Das Layout bleibt 12 Bytes gross und passt daher formal zur FVX-Gen3-Stride-Annahme `0xC`. Inhaltlich ist es aber erweitert:

- Byte `+9` ist `z_move_power`.
- Byte `+10` ist `split`.
- Byte `+11` ist `z_move_effect`.
- FVX liest Byte `+10` aktuell nicht und leitet Kategorie stattdessen aus dem Typ ab.

CFRU `src/Tables/battle_moves.c` benutzt designierte Initializer nach Move-ID, zum Beispiel `[MOVE_NONE]`, `[MOVE_POUND]`, `[MOVE_AQUACUTTER]`, `[MOVE_TERABLAST]`, `[MOVE_TRAILBLAZE]` und `[MOVE_PSYCHICNOISE]`.

Relevante Kodierung:

- `effect` nutzt `EFFECT_*` aus `include/constants/battle_move_effects.h`.
- `type` nutzt `TYPE_*`.
- `accuracy == 0` bedeutet bei vielen Moves "trifft immer" oder Status-Sonderfall.
- `flags` nutzt Bits wie `FLAG_MAKES_CONTACT`, `FLAG_PROTECT_AFFECTED`, `FLAG_MAGIC_COAT_AFFECTED`, `FLAG_SNATCH_AFFECTED`, `FLAG_MIRROR_MOVE_AFFECTED`, `FLAG_KINGS_ROCK_AFFECTED`, `FLAG_TRIAGE_AFFECTED`.
- `split` nutzt `SPLIT_PHYSICAL = 0`, `SPLIT_SPECIAL = 1`, `SPLIT_STATUS = 2`.

## Move-Namen und Move-Descriptions

FVX liest Move-Namen ueber:

- `MoveNames = readPointer(Gen3Constants.moveNamesPointer)`
- `moveNamesPointer = 0x148`
- `MoveNameLength = 13` aus BPRE-RomEntry fuer FireRed

CFRU/DPE definiert `MOVE_NAME_LENGTH = 12`. Der Unterschied ist nicht zwingend ein Widerspruch, weil FVX fuer die ROM-Stringtabelle inklusive Terminator/Padding arbeitet, waehrend CFRU die sichtbare Maximalnamenlaenge als Konstante fuehrt.

Der aktuelle Move-Count-Scan haengt an der Description-Pointer-Tabelle, nicht direkt an `MOVES_COUNT`. Wenn die Description-Tabelle im getesteten Build nicht bis `MOVE_PSYCHICNOISE` als durchgehend gueltige Pointerliste erkennbar ist, stoppt FVX frueh und erzeugt `moves.total=559`.

## Level-Up-Learnsets und Trainer-Movesets

Der Stand aus Diagnose 031/032:

- Trainer-Movesets sind fuer die getesteten P1-Kombinationen stabil.
- CFRU/DPE-Level-Up-Learnsets werden fuer Trainer-Movesets read-only ueber den schmalen Reader gelesen.
- Der Reader filtert Move-IDs defensiv gegen `isLoadedMoveId(move)`.

Konsequenz:

- Der Write/Reload-Pfad bleibt stabil, weil nicht geladene Move-IDs nicht in den FVX-Auswahlpool gelangen.
- Das bestaetigt Stabilitaet, aber nicht Gen8/9-Move-Coverage.
- Gen8/9-Moves in CFRU/DPE-Learnsets koennen aktuell aus dem FVX-Pool herausfallen, solange `moves.total` nicht erweitert wird.

## TM-/HM-Move-Tabellen

DPE definiert `gTMHMMoves[NUM_TMSHMS]` in `src/TM_Tutor_Tables.c`.

Beobachtungen:

- Die Tabelle ist `u16`.
- Sie enthaelt Move-IDs, nicht Pointer auf Move-Daten.
- Die gezeigte Tabelle umfasst `128` TM/HM-Slots.
- Slots `1..120` sind TMs.
- Slots `121..128` sind HMs.
- Spaetere Tabellenwerte koennen Move-IDs deutlich oberhalb der alten Gen3-Grenze enthalten.

CFRU nutzt in `src/item.c`:

- `gTMHMMoves` als Pointer ueber `0x8125A8C`
- `gTMHMLearnsets` als Pointer ueber `0x8043C68`
- bei `EXPANDED_TMSHMS`: `typedef u32 TM_HM_T[4]`
- ohne `EXPANDED_TMSHMS`: `typedef u32 TM_HM_T[2]`
- `CanMonLearnTMHM()` prueft Bitfelder pro Species und TM-Index

DPE `assembly/generated/tm_compatibility.s` bestaetigt:

- `gTMHMLearnsets` ist generierte Byte-/Bitfelddaten pro Species.
- Ein sichtbarer Datensatz umfasst beim erweiterten 128-Slot-Modell 16 Bytes pro Species.

UPR-FVX Gen3 erwartet aktuell:

- `Gen3Constants.tmCount = 50`
- `Gen3Constants.hmCount = 8`
- `getTMHMCompatibility()` liest `8` Bytes pro Species.

Folgerung:

- FVX kann das erweiterte 128-Slot-CFRU/DPE-TM/HM-Modell nicht vollstaendig abbilden.
- Die aktuelle FVX-Grenze 50+8 ist ein Vanilla-Gen3-Modell.
- Ein Fix darf nicht nur Move-Daten erweitern; TM/HM-Kompatibilitaet braucht ein eigenes, gegatetes 128-Slot-Modell.

## Move-Tutor-Tabellen

DPE definiert Tutor-IDs in `include/tutors.h`:

- normale Tutor-IDs `0..127`
- Special Tutors `128..136`
- `LAST_TOTAL_TUTOR_NUM = 136`

DPE definiert `gMoveTutorMoves[NUM_MOVE_TUTOR_MOVES]` in `src/TM_Tutor_Tables.c`:

- Tabelle ist `u16`.
- Sie enthaelt Move-IDs.
- Beobachteter Tabellenbereich reicht bis `MOVE_TERABLAST` bei Slot `151`.

CFRU nutzt in `src/item.c`:

- `gTutorLearnsets` als Pointer ueber `0x8120C30`
- bei `EXPANDED_MOVE_TUTORS`: `ExpandedTutor_T[...]` mit `u32`-Bitfeldern
- Bitfeldbreite wird aus `NUM_MOVE_TUTORS` abgeleitet
- Special Tutors sind teilweise nicht in der generischen Tabelle gespeichert, sondern ueber Sonderlogik behandelt

DPE `assembly/generated/tutor_compatibility.s` bestaetigt:

- `gTutorLearnsets` ist generierte Byte-/Bitfelddaten pro Species.
- Sichtbare Datensaetze sind breiter als Vanilla-FRLG-Tutor-Kompatibilitaet.

UPR-FVX Gen3 erwartet aktuell:

- `MoveTutorMoves` aus RomEntry, fuer BPRE vanilla `15`
- `getMoveTutorMoves()` liest `moveCount * 2` ab `MoveTutorData`
- die Kompatibilitaetsmodellierung bleibt am klassischen Gen3-Tutor-Scope orientiert

Folgerung:

- Das CFRU/DPE-Tutor-Modell nutzt eigene Counts und breitere Bitfelder.
- Move-IDs sind `u16`, also grundsaetzlich gross genug fuer 992 Moves.
- FVX muss fuer Tutor-Randomization separat gegatet werden; ein reiner Move-Data-Reader reicht nicht.

## Egg-Move-Tabelle

DPE definiert `gEggMoves[]` in `src/Egg_Moves.c`.

Format:

- `u16`-Stream.
- `EGG_MOVES_SPECIES_OFFSET = 20000`.
- Makro: `egg_moves(species, moves...) (SPECIES_##species + EGG_MOVES_SPECIES_OFFSET), moves`.
- Terminator: `EGG_MOVES_TERMINATOR = 0xFFFF`.
- Die Move-Eintraege sind `u16`-Move-IDs.

UPR-FVX `Gen3RomHandler.getEggMoves()` nutzt exakt das alte Gen3-Decomp-Prinzip:

- liest `u16`-Werte aus `EggMoves`
- `val > 20000` startet eine neue Species
- sonst ist `val` eine Move-ID
- `0xFFFF` beendet die Tabelle

Folgerung:

- Das Egg-Move-Streamformat ist fuer CFRU/DPE weiterhin grundsaetzlich kompatibel.
- Die Species-Abbildung muss aber auf interne Species-IDs und Gen9-Counts achten.
- Die Move-ID-Grenze bleibt kritisch: Egg-Moves koennen Move-IDs oberhalb der geladenen FVX-Move-Liste enthalten.

## Pointer-/Offset-Befunde

DPE `repointall` dokumentiert relevante Pointer-Locations:

- `gEggMoves 08045C50`
- `gTMHMLearnsets 08043C68`
- `gTutorLearnsets 08120C30`
- `gTMHMMoves 08125A8C`
- `gMoveTutorMoves 08120BE4`
- `gLevelUpLearnsets 0803EA7C` unter `EXPAND_LEARNSETS`

FVX-BPRE-RomEntry fuer FireRed enthaelt klassisch:

- `PokemonMovesets=0x25D7B4`
- `EggMoves=0x25EF0C`
- `PokemonTMHMCompat=0x252BC8`
- `MoveCount=354`
- `MoveNameLength=13`
- `MoveTutorData=0x459B60`
- `MoveTutorMoves=15`

Der BPRE-Hack-Support ueberschreibt Teile davon dynamisch:

- `PokemonTMHMCompat = readPointer(0x43C68)`
- `PokemonEvolutions = readPointer(0x42F6C)`
- `MoveTutorCompatibility = readPointer(0x120C30)`
- `MoveDescriptions = readPointer(0xE5440)`
- `TrainerData = readPointer(0xFC00)`
- `MoveCount` via Description-Scan

## Risiken fuer Randomizer-Optionen

Trainer Movesets:

- P1-stabil in Diagnose 032.
- Gen8/9-Moves werden durch die aktuell zu niedrige FVX-Move-Liste weiterhin nicht belastbar genutzt.
- Nicht geladene Learnset-Moves werden defensiv aus dem Auswahlpool gefiltert.

Sensible Trainer Held Items:

- P1-stabil in Kombination mit Trainer Movesets.
- Movebasierte Auswertung sieht nur Moves, die FVX als `Move`-Objekte kennt.
- Dadurch bleiben Gen8/9-spezifische Synergien/Flags unvollstaendig.

Move Data Randomization:

- Nicht P1-bestaetigt fuer CFRU/DPE Gen9.
- FVX schreibt aktuell nur die ersten 5 Bytes des 12-Byte-Records zurueck und ignoriert `split`, `z_move_power`, `z_move_effect`.
- Ohne gating koennte Move Data Randomization nur einen Teilbestand erfassen und erweitertes CFRU/DPE-Verhalten verlieren.

TM/HM Randomization:

- Nicht P1-bestaetigt.
- FVX-Counts `50+8` passen nicht zum beobachteten 128-Slot-TM/HM-Modell.
- FVX liest aktuell `8` Kompatibilitaetsbytes pro Species; CFRU/DPE expanded nutzt bis zu `16`.

Tutor Randomization:

- Nicht P1-bestaetigt.
- FVX-BPRE-Defaults `15` Tutor-Moves passen nicht zum DPE-Tutorbestand.
- Tutor-Kompatibilitaet nutzt erweiterte Bitfelder und Special-Tutor-Sonderlogik.

Egg Moves:

- Tabellenformat ist naheliegend kompatibel.
- Species-ID- und Move-ID-Grenzen bleiben separat zu sichern.

## Empfohlener minimaler Folge-Fixpfad

1. CFRU/DPE-Move-Data-Reader schmal gaten.

   Bedingung sollte an dieselbe CFRU/DPE-Gen9-Erkennung gebunden sein, die fuer Species/Learnsets bereits genutzt wird. Vanilla und normale Gen3-Hacks duerfen ihren bestehenden Pfad behalten.

2. `MoveCount` nicht aus Description-Pointern ableiten, wenn CFRU/DPE Gen9 sicher erkannt ist.

   Plausibler minimaler Wert: `MOVES_COUNT = 992`, entweder ueber bekannte CFRU/DPE-Konstante/Signatur oder defensiv ueber `LAST_MOVE_INDEX + 1` aus Tabellenmodell. Kein globaler Gen3-Default.

3. Gen3-12-Byte-Stride weiterverwenden, aber CFRU/DPE-Byte `+10` als `split` lesen.

   Mapping: `0 -> PHYSICAL`, `1 -> SPECIAL`, `2 -> STATUS`.

4. Move-IDs defensiv behandeln.

   Wenn Name, Description oder Move-Record fuer hohe IDs unplausibel ist, Move als nicht randomisierbar markieren oder aus Pools filtern, statt globale Randomizer-Pfade abbrechen zu lassen.

5. TM/HM und Tutor nicht im selben Fix breit umbauen.

   Nach Move-Data-Coverage sollten eigene Modell-/Fixbranches folgen: CFRU/DPE-TM/HM 128-Slot, CFRU/DPE-Tutor-Bitfeldmodell und Egg-Move Species-/Move-ID-Diagnose.

6. `setMovesLearnt()` weiterhin nicht ausweiten.

   Learnset-Write bleibt ausserhalb des Trainer-Movesets-P1-Scope.

## Offene Fragen

- Ist die Move-Description-Tabelle im konkreten Build absichtlich nur bis `558` gueltig oder bricht der FVX-Scan an einem Format-/Pointermodell-Wechsel ab?
- Gibt es eine stabile ROM-Signatur fuer `MOVES_COUNT=992`, ohne Source-Konstanten zu parsen?
- Sind Move-Namen fuer alle `0..991` im getesteten ROM lueckenlos vorhanden und mit `MOVE_NAME_LENGTH`/FVX `MoveNameLength=13` korrekt lesbar?
- Soll FVX hohe Max-/G-Max-/Z-Move-IDs fuer Randomizer-Pools ueberhaupt zulassen oder zunaechst ausschliessen?
- Wie sollen Special Tutors `128..136` gegen die beobachtete `gMoveTutorMoves`-Tabelle bis Slot `151` abgegrenzt werden?
- Muss Egg-Move-Randomization zuerst an interner Species-Identitaet oder zuerst an Move-Data-Coverage scheitern?

## Ergebnis

Trainer Movesets bleiben nach Diagnose 032 P1-stabil, aber das Move-Datenmodell ist noch nicht vollstaendig CFRU/DPE-Gen9-kompatibel. Die zentrale Coverage-Luecke ist `moves.total=559` gegen `MOVES_COUNT=992`. Ein minimaler naechster Fix sollte zuerst den CFRU/DPE-Move-Reader und die Move-Count-Ermittlung gegatet erweitern, inklusive `split`-Byte, aber TM/HM-, Tutor-, Egg- und Learnset-Write-Pfade getrennt lassen.
