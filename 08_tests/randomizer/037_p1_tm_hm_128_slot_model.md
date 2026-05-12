# 037 - P1 TM/HM 128-Slot-Modell fuer CFRU/DPE Gen9-BPRE

## Kontext

Ziel dieses Analyseblocks war, den aktiven CFRU/DPE-128-Slot-TM/HM-Ort read-only zu modellieren und das Table-/Pointermodell, HM-Schutz, Compatibility-Flagmodell sowie Write/Reload-Risiken fuer einen spaeteren Fix einzugrenzen.

Gepruefter Stand:

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model`
- Voraussetzung: UPR-FVX PR #19 gemerged.
- Voraussetzung: Workspace PR #73 gemerged.
- UPR-FVX-Stand: `32e43ac03a5762542773213a13be4e0389f1deae`
- Ausgangsbefund Diagnose 036: TM/HM-only ist im FVX-`50+8`-Scope P1-supported.
- Keine Codeaenderung.
- Keine Aenderung an `02_external/**`.
- Kein ROM-Zugriff in diesem Branch; ROM-Offsets stammen aus bestehenden Diagnoseprotokollen.

## Relevante Pfade

UPR-FVX:

- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `02_external/upr-fvx/romio/src/main/java/com/uprfvx/romio/constants/Gen3Constants.java`
- `02_external/upr-fvx/romio/src/main/resources/com/uprfvx/romio/romentries/gen3_offsets.ini`

CFRU/DPE:

- `02_external/CFRU-expansion/src/config.h`
- `02_external/CFRU-expansion/include/new/item.h`
- `02_external/CFRU-expansion/src/item.c`
- `02_external/CFRU-expansion/src/learn_move.c`
- `02_external/CFRU-expansion/include/constants/items.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/defines.h`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/src/TM_Tutor_Tables.c`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/assembly/generated/tm_compatibility.s`
- `02_external/Dynamic-Pokemon-Expansion-Gen-9/repointall`

## CFRU/DPE-Konstanten und Symbole

Der getestete CFRU/DPE-Stand ist fuer ein erweitertes TM/HM-Modell konfiguriert:

- `EXPANDED_TMSHMS` ist in `CFRU-expansion/src/config.h` definiert.
- `NUM_TMS = 120`.
- `NUM_HMS = 8`.
- `NUM_TMSHMS = NUM_TMS + NUM_HMS`.
- DPE `src/defines.h` definiert passend `NUM_TMSHMS 128`.
- DPE `src/TM_Tutor_Tables.c` definiert `const u16 gTMHMMoves[NUM_TMSHMS]`.

Die aktive Move-Tabelle ist also keine Folge einzelner Item-Records, sondern eine `u16`-Move-ID-Tabelle mit 128 Slots.

## Aktiver Tabellenort und Pointermodell

`Dynamic-Pokemon-Expansion-Gen-9/repointall` dokumentiert:

- `gTMHMLearnsets 08043C68`
- `gTMHMMoves 08125A8C`

CFRU bindet diese Tabellen als Pointer-Pointer an:

- `gTMHMLearnsets ((TM_HM_T*) *((u32*) 0x8043C68))`
- `gTMHMMoves ((const u16*) *((u32*) 0x8125A8C))`

Folgerung:

- Der ROM-Code nutzt nicht direkt eine fest eingebettete Tabelle an der Pointer-Location.
- Die Pointer-Location enthaelt den Zielpointer auf die aktive Tabelle.
- Ein Randomizer-Fix muss den Pointer bei `0x8125A8C` lesen, um `gTMHMMoves` zu finden.
- Ein Randomizer-Fix muss den Pointer bei `0x8043C68` lesen, um `gTMHMLearnsets` zu finden.

Das passt zu bestehenden UPR-FVX-Hack-Pointer-Updates fuer Compatibility:

- `Gen3RomHandler` setzt bei BPRE-Hacks bereits `PokemonTMHMCompat = readPointer(0x43C68)`.
- Fuer `TmMoves` wird aktuell kein CFRU/DPE-Pointer gelesen; FVX bleibt beim RomEntry-Offset.

## Slotanzahl und Slotbelegung

DPE `gTMHMMoves[NUM_TMSHMS]` enthaelt 128 `u16`-Move-IDs:

- Slots `1..120` sind TMs.
- Slots `121..128` sind HMs.
- Intern verwendet CFRU nullbasierte TM/HM-Indizes `0..127`.
- `CanMonLearnTMHM(mon, i)` und `BuildTMMoveset()` iterieren `i < NUM_TMSHMS`.
- `BuildTMMoveset()` schreibt fuer Anzeige/Runtime `moves[numTotalMoves].num = i + 1` und `moves[numTotalMoves].move = gTMHMMoves[i]`.

Belegte Beispiele:

- Slot 1: `MOVE_FOCUSPUNCH`
- Slot 50: `MOVE_OVERHEAT`
- Slot 51: `MOVE_ROOST`
- Slot 58: `MOVE_ENDURE`
- Slot 59: `MOVE_DRAGONPULSE`
- Slot 70: `MOVE_FLASH`
- Slot 120: `MOVE_NATUREPOWER`
- Slot 121: `MOVE_CUT`
- Slot 122: `MOVE_FLY`
- Slot 123: `MOVE_SURF`
- Slot 124: `MOVE_STRENGTH`
- Slot 125: `MOVE_DIVE`
- Slot 126: `MOVE_ROCKSMASH`
- Slot 127: `MOVE_WATERFALL`
- Slot 128: `MOVE_ROCKCLIMB`

Move-ID-Grenzen aus DPE/CFRU:

- `MOVE_ROOST = 0x18B`
- `MOVE_DRAGONPULSE = 0x172`
- `MOVE_ROCKCLIMB = 0x188`
- `MOVE_PSYCHICNOISE = 0x3DF`
- `MOVES_COUNT = MOVE_PSYCHICNOISE + 1 = 992`

Damit koennen aktive TM/HM-Slots Move-IDs oberhalb klassischer Gen3-Werte enthalten, liegen aber weiterhin als `u16` innerhalb `moves.total=992`.

## Verhaeltnis zu klassischem 50+8-Modell

UPR-FVX Gen3 ist aktuell fest auf klassisches FRLG ausgerichtet:

- `Gen3Constants.tmCount = 50`
- `Gen3Constants.hmCount = 8`
- `Gen3Constants.hmMoves` ist eine statische Liste.
- `getTMMoves()` liest 50 `u16` ab `romEntry.TmMoves`.
- `getHMMoves()` gibt die statische HM-Liste zurueck, nicht ROM-Daten.
- `setTMMoves()` schreibt nur 50 `u16` ab `romEntry.TmMoves`.
- `setTMMoves()` kopiert optional `50 * 2` Bytes nach `TmMovesDuplicate`.
- `getTMHMCompatibility()` erzeugt `boolean[59]` und liest 8 Bytes pro Species.
- `setTMHMCompatibility()` schreibt 8 Bytes pro Species.

Diagnose 035/036 bestaetigten fuer den getesteten ROM-Stand:

- `romEntry.TmMoves=0x45a5a4`
- `romEntry.PokemonTMHMCompat=0x16002d0`
- `tmCount=50`
- `hmCount=8`
- `compat.flagLength=59`
- Die ersten 50 rohen Slots ab `romEntry.TmMoves` entsprechen den oeffentlichen FVX-TMs.
- Slots `51..58` ab diesem Offset entsprechen den klassischen acht FVX-HMs.
- Slots `59..128` ab diesem Offset sind unplausibel/invalid.

Einordnung:

- `0x45a5a4` ist der klassische FRLG/FVX-Ort aus `gen3_offsets.ini`, nicht der DPE-`gTMHMMoves`-Pointer-Ort.
- Dass dort nach 50+8 unplausible Werte stehen, ist erwartbar: FVX liest ueber das klassische Tabellenende hinaus in benachbarte Daten.
- Dieser Befund widerlegt das 128-Slot-Modell nicht; er zeigt nur, dass der klassische FVX-Ort nicht die aktive DPE-128-Slot-Tabelle ist.

## HM-Schutzlogik

CFRU/DPE leitet HM fachlich ueber den TM/HM-Index ab, nicht ueber eine statische FVX-HM-Move-Liste:

- `NUM_TMS = 120`
- `NUM_HMS = 8`
- HM-Slots sind nullbasiert `120..127`, sichtbar `121..128`.
- `LoadTMNameWithNo()` berechnet `hmNum = tmNum - NUM_TMS`, wenn `tmNum > NUM_TMS`.
- `CheckIsHmMove()` iteriert ohne `DELETABLE_HMS` ueber `i = NUM_TMS; i < NUM_TMSHMS; ++i` und vergleicht `move == gTMHMMoves[i]`.
- Im getesteten CFRU-Config ist `DELETABLE_HMS` definiert; diese Gameplay-Option macht HMs loeschbar, aendert aber nicht die Slotklassifikation.

Minimaler HM-Schutz fuer einen Randomizer-Fix:

- Slots `0..119` duerfen als TMs behandelt werden.
- Slots `120..127` sind HMs und muessen standardmaessig geschuetzt bleiben.
- HM-Schutz darf nicht aus `Gen3Constants.hmMoves` abgeleitet werden, wenn CFRU/DPE-128-Slot-Scope aktiv ist.
- Falls HM-Moves selbst randomisiert werden sollen, braucht das einen eigenen, explizit freigegebenen Scope.

## Compatibility-Flagmodell

CFRU verwendet bei `EXPANDED_TMSHMS`:

- `typedef u32 TM_HM_T[4]`
- 4 * 32 Bits = 128 Compatibility-Flags pro Species.
- `CanMonLearnTMHM()` liest Bits in vier Bereichen:
  - `0..31`
  - `32..63`
  - `64..95`
  - `96..127`

DPE `assembly/generated/tm_compatibility.s` bestaetigt das praktisch:

- `gTMHMLearnsets` ist eine generierte Tabelle.
- Jede sichtbare Zeile hat 16 Bytes.
- 16 Bytes entsprechen exakt 128 Bits.

FVX-Kompatibilitaet ist dagegen nicht kompatibel:

- `boolean[59]`
- 8 Bytes pro Species
- `tmCount + hmCount = 58`

Folgerung:

- Ein 128-Slot-Fix braucht `boolean[129]` oder ein aequivalentes Modell mit Nullslot plus 128 Slots.
- Read/Write muss 16 Bytes pro Species verwenden.
- Die bestehende 8-Byte-FVX-Compatibility-Routine darf nicht fuer CFRU/DPE-128-Slot-Daten wiederverwendet werden.

## Write/Reload-Risiken

TM/HM-Move-Tabelle:

- `gTMHMMoves` ist `u16[128]`; reines Lesen ist klar.
- Write muss ueber den Pointer bei `0x8125A8C` erfolgen, nicht ueber `romEntry.TmMoves`.
- Ein Write darf nur die 120 TM-Slots veraendern, wenn HMs geschuetzt bleiben.
- Es ist offen, ob es weitere Duplikate oder abgeleitete Item-Text-/Disc-/Bag-Daten gibt, die nach TM-Write konsistent gehalten werden muessen.
- FVX `writeTMItemText()` und `writeTMItemPalettes()` sind aktuell auf 50 klassische TM-Items ausgerichtet und koennen nicht einfach auf 120 erweitert werden.

Compatibility:

- Write muss 16 Bytes pro Species schreiben.
- Species-Indexierung muss zur CFRU/DPE-internen Species-ID passen, nicht zu Dex-ID/PokedexOrder.
- Placeholder-/Null-Type-Species aus Diagnose 036 muessen weiterhin defensiv behandelt werden.
- Ein gemischter Zustand aus 128-Slot-Move-Tabelle und 59-Flag-Compatibility wuerde Randomizer- und Reload-Vergleiche verfälschen.

HM-Schutz:

- FVX `getHMMoves()` liefert aktuell statische klassische HMs.
- Im 128-Slot-Modell sollte HM-Schutz ueber Slots `120..127` erfolgen.
- Ein Move-ID-basierter Schutz kann falsch sein, wenn HM-Slots spaeter andere Moves enthalten oder wenn ein TM denselben Move wie ein HM enthaelt.

## Risiken fuer Randomizer-Optionen

TM/HM-Randomization:

- Ohne 128-Slot-Reader randomisiert FVX nur 50 TMs und behandelt HMs separat statisch.
- Mit 128-Slot-Reader duerfen hohe Move-IDs nicht wieder in alte FVX-Sicherheitslisten oder Item-Textpfade laufen.
- Der Fix aus Diagnose 036 schliesst hohe Move-IDs fuer TM-Auswahl defensiv aus; ein 128-Slot-Fix muss diese Entscheidung bewusst beibehalten oder ein neues Sicherheitsmodell definieren.

Compatibility-Randomization:

- 128 Slots erfordern 16-Byte-Bitfelder.
- Probability-Logik muss mit 128 Move-IDs und `moves.total=992` umgehen.
- Placeholder-Species ohne Primaertyp bleiben ein Scope-Risiko.

Log/Reload:

- Reload-Vergleiche muessen 128 TM/HM-Eintraege und 128 Compatibility-Flags pruefen.
- Der bisher bestaetigte `50+8`-Reload-Erfolg ist nicht automatisch Nachweis fuer das 128-Slot-Modell.

## Empfohlener minimaler Folge-Fixpfad

1. Enges CFRU/DPE-Gate verwenden.

   Nur fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks aktivieren, z. B. ueber denselben erweiterten BPRE-/Species-Gate wie bisher. Vanilla, Jambo und andere Gen3-Hacks bleiben auf dem bestehenden Pfad.

2. `gTMHMMoves` ueber Pointer bei `0x8125A8C` lesen.

   Fuer CFRU/DPE `u16[128]` laden. `getTMCount()` sollte in diesem Scope `120` und `getHMCount()` `8` liefern oder intern ein aequivalentes Scope-Modell bereitstellen.

3. HM-Schutz slotbasiert modellieren.

   Slots `0..119` sind TMs, Slots `120..127` sind HMs. TM-Randomization schreibt nur die ersten 120 Slots, solange HM-Randomization nicht explizit freigegeben ist.

4. Compatibility ueber Pointer bei `0x8043C68` als 16 Bytes pro Species lesen.

   Flags als Nullslot plus 128 Slots abbilden. Write erst implementieren, wenn Read/Reload auf interner Species-ID stabil nachgewiesen ist.

5. Item-Text-/Palette-/Duplicate-Write zunaechst nicht breit ausweiten.

   Wenn TM-Move-Write fuer 120 Slots folgt, zuerst pruefen, welche CFRU/DPE-Itemdaten fuer TM51..TM120 aktiv sind. Der klassische FVX-Text-/Palette-Code fuer 50 TMs ist nicht ausreichend.

6. Diagnose zuerst read-only, dann Fix getrennt.

   Ein Folge-Fix sollte Diagnosewerte fuer `tmCount=120`, `hmCount=8`, `compat.flagLength=129`, `before/after/reload` fuer 128 Slots und HM-Slot-Schutz liefern.

## Offene Fragen

- Gibt es im konkreten Build weitere Pointerkopien oder Duplikate von `gTMHMMoves`, die beim Write synchronisiert werden muessen?
- Welche Item-Text-/Item-Palette-/Disc-Daten sind fuer TM51..TM120 aktiv und muessen bei Move-Randomization angepasst werden?
- Soll TM-Randomization in einem ersten 128-Slot-Fix hohe Gen8/9-Moves weiterhin ausschliessen oder ein neues Sicherheitsmodell fuer Move-Bans/Descriptions erhalten?
- Welche Species-Indexierung ist fuer `gTMHMLearnsets` im getesteten Build exakt stabil: interne Species-ID direkt oder eine weitere CFRU/DPE-Forme-Abbildung?
- Wie sollen Placeholder-Species in 128-Slot-Compatibility-Write/Reload-Vergleichen behandelt werden?

## Ergebnis

Das aktive CFRU/DPE-128-Slot-Modell ist durch Source- und Pointermodell hinreichend belegt:

- `gTMHMMoves` ist `u16[128]` und wird ueber Pointer `0x8125A8C` angebunden.
- Slots `1..120` sind TMs, Slots `121..128` sind HMs.
- `gTMHMLearnsets` ist ein 128-Bit-/16-Byte-Compatibility-Modell pro Species und wird ueber Pointer `0x8043C68` angebunden.
- FVX nutzt aktuell den klassischen `50+8`-Ort `romEntry.TmMoves=0x45a5a4` und 8-Byte-Compatibility, weshalb der Bereich nach 50+8 dort unplausible Daten zeigt.

Ein minimaler Fix ist plausibel, sollte aber separat erfolgen und nur das 128-Slot-Read-/Write-Modell fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks betreffen. Tutor-, Egg-Move-, Learnset-Write- und Move-Data-Write-Pfade bleiben getrennt.
