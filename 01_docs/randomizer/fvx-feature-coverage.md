# FVX Feature Coverage Update - 2026-05-15 - Field Items Random Ban Bad reload smoke

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains `GUI-kompatibel` in the narrow Field-Items Random scope; Diagnose 112 additionally confirms `banBadRandomFieldItems=true` for `FieldItemsMod.RANDOM`.
- `FVX-ITEM-003` remains `GUI-kompatibel` only for `banBadRandomFieldItems=false`; Random Even + Ban Bad remains separate.
- `FVX-ITEM-004` is tested for `FieldItemsMod.RANDOM`, but not fully GUI-compatible until Random Even + Ban Bad is smoked.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu and Scriptparser work remain outside Diagnose 112.

# FVX Feature Coverage Update - 2026-05-15 - Field Items Ban Bad scope plan

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains `GUI-kompatibel` in the narrow Field-Items Random scope with `banBadRandomFieldItems=false`.
- `FVX-ITEM-003` remains `GUI-kompatibel` in the narrow Field-Items Random-Even scope with `banBadRandomFieldItems=false`.
- `FVX-ITEM-004` remains `Write modelliert`; Diagnose 111 plans the first Ban-Bad smoke as `FieldItemsMod.RANDOM` with `banBadRandomFieldItems=true`.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu and Scriptparser work remain outside Diagnose 111.

# FVX Feature Coverage Update - 2026-05-15 - Field Items Random Even reload smoke

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains `GUI-kompatibel` in the narrow Field-Items Random scope with `banBadRandomFieldItems=false`.
- `FVX-ITEM-003` is `GUI-kompatibel` in the narrow Field-Items Random-Even scope with `banBadRandomFieldItems=false` after Diagnose 110.
- `FVX-ITEM-004` remains `Write modelliert`; Ban Bad Items stays separate.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu and Scriptparser work remain outside Diagnose 110.

# FVX Feature Coverage Update - 2026-05-15 - Field Items API TM-slot reload smoke

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested Shuffle allowed-slot scope.
- `FVX-ITEM-002` is `GUI-kompatibel` in the narrow Field-Items Random scope with `banBadRandomFieldItems=false` after Diagnose 109.
- `FVX-ITEM-003` remains `Write modelliert`; Random Even needs its own smoke.
- `FVX-ITEM-004` remains `Write modelliert`; Ban Bad Items stays separate.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames, TypeChart, Trainer/Wild/Evolution, Text/Menu and Scriptparser work remain outside Diagnose 109.

# FVX Feature Coverage Update - 2026-05-15 - Field Items API TM-slot fix prepared

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested CFRU/DPE Gen9-BPRE Field Items Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains `Write modelliert`: UPR-FVX PR #37 prepares the API TM-slot scope fix, but no fachlicher reload smoke has passed yet.
- `FVX-ITEM-003` remains `Write modelliert`.
- `FVX-ITEM-004` remains `Write modelliert`.
- The fix does not make TMs globally allowed and does not expand Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even or Ban Bad Items.

# FVX Feature Coverage Update - 2026-05-15 - Field Items API TM-slot scope planned

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested CFRU/DPE Gen9-BPRE Field Items Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains `Write modelliert`: Diagnose 107 identifies the remaining blocker as the Field-Items API TM-slot scope (`getFieldItems()` exposes `0` TM slots while raw diagnostics found `28`).
- `FVX-ITEM-003` remains `Write modelliert`.
- `FVX-ITEM-004` remains `Write modelliert`.
- A later fix must not make TMs globally allowed and must not expand Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Random Even or Ban Bad Items.

# FVX Feature Coverage Update - 2026-05-15 - Field Items Random API TM-slot blocker

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested CFRU/DPE Gen9-BPRE Field Items Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains `Write modelliert`: Diagnose 106 confirms `randomTmPoolDeficit=0`, but blocks because the Randomizer Field-Items API sees `0` TM slots while raw diagnostics found `28`.
- `FVX-ITEM-003` remains `Write modelliert`.
- `FVX-ITEM-004` remains `Write modelliert`.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames and TypeChart remain outside this scope.

# FVX Feature Coverage Update - 2026-05-15 - Field Items Random TM-pool fix prepared

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested CFRU/DPE Gen9-BPRE Field Items Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains pending: UPR-FVX PR #36 prepares the TM-pool fix, but no fachlicher Field-Items-Random reload smoke was executed in this block.
- `FVX-ITEM-003` remains `Write modelliert`.
- `FVX-ITEM-004` remains `Write modelliert`.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames and TypeChart remain outside this scope.

# FVX Feature Coverage Update - 2026-05-15 - Field Items Random TM-pool blocker planned

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested CFRU/DPE Gen9-BPRE Field Items Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains `Write modelliert`: Diagnose 104 narrows the blocker to the Field-Items-Random TM-pool path.
- `FVX-ITEM-003` remains `Write modelliert`.
- `FVX-ITEM-004` remains `Write modelliert`.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames and TypeChart remain outside this scope.

# FVX Feature Coverage Update - 2026-05-15 - Field Items Random blocked

- `FVX-ITEM-001` remains `GUI-kompatibel` for the tested CFRU/DPE Gen9-BPRE Field Items Shuffle allowed-slot scope.
- `FVX-ITEM-002` remains `Write modelliert`: Diagnose 103 blocks with `RandomizationException` before output/reload.
- `FVX-ITEM-003` remains `Write modelliert`.
- `FVX-ITEM-004` remains `Write modelliert`.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames and TypeChart remain outside Diagnose 103.

# FVX Feature Coverage Update - 2026-05-15 - Field Items Shuffle GUI-compatible

- `FVX-ITEM-001` is `GUI-kompatibel` for the tested CFRU/DPE Gen9-BPRE Field Items Shuffle allowed-slot scope after Diagnose 102.
- `FVX-ITEM-002` remains `Write modelliert` pending a separate Random smoke.
- `FVX-ITEM-003` remains `Write modelliert` pending a separate Random Even smoke.
- `FVX-ITEM-004` remains `Write modelliert` pending a separate Ban Bad Items smoke.
- Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames and TypeChart remain outside Diagnose 102.

# FVX Feature Coverage Update - 2026-05-14 - Field Items allowed-slot guard

- `FVX-ITEM-001` remains `Write modelliert`: existing allowed-slot writer guard is documented in Diagnose 101, but no Write-/Reload-Smoke ran in this block.
- `FVX-ITEM-002` remains `Write modelliert`.
- `FVX-ITEM-003` remains `Write modelliert`.
- `FVX-ITEM-004` remains `Write modelliert`.
- Field Items are separate from Shops, Pickup, Held Items, TM/HM/Tutor/Learnset, Palette/Graphics, MoveData/MoveNames and TypeChart.

# UPR FVX Feature Coverage Matrix

## Zweck

Diese Datei bildet die sichtbaren Features aus Universal Pokemon Randomizer FVX 1.5.1 auf Projektanforderungen, Roadmap-Pakete und spaetere Tests ab.

Sie ist die detaillierte Requirements-/Coverage-Ebene. Die Roadmap bleibt bewusst grober und verweist auf Feature-Pakete statt auf jede einzelne Checkbox.

## Zaehlregel

- `Unchanged` wird nicht als Feature gezaehlt.
- Sichtbare Checkboxen, Radiobutton-Optionen und klar getrennte Unteroptionen werden als tracebare Feature-Zeilen gezaehlt.
- Unteroptionen werden getrennt gefuehrt, wenn sie eigene Test- oder Risikoaussagen brauchen.
- Ergebnis dieser normalisierten Matrix: **130 Feature-/Suboption-Zeilen**.

## Statusmodell

| Status | Bedeutung |
|---|---|
| Nicht begonnen | Noch kein belastbarer Plan, kein Modell und kein Testnachweis fuer diese Feature-Zeile. |
| Plan erstellt | Feature ist als Arbeitspaket, Suboption oder Regressionstest eingeordnet, aber noch nicht einzeln getestet. |
| Read modelliert | Lesepfad oder Datenmodell ist dokumentiert, aber kein stabiler Writer belegt. |
| Write modelliert | Writer-/Repointing-/Preserve-Risiko ist dokumentiert, aber noch kein stabiler Write-/Reload-Nachweis. |
| Getestet | Dedizierter Diagnose- oder Smoke-Nachweis existiert, aber GUI-Kompatibilitaet ist noch nicht als Paket freigegeben. |
| GUI-kompatibel | Im getesteten CFRU/DPE Gen9-BPRE-Scope liegen Save/Log/Output/Reload-Nachweise oder aequivalente P1-Nachweise fuer die GUI-nahe Option vor. |
| In Arbeit | Aktuell aktiver Arbeitsblock. |

## Coverage Summary

| Status | Anzahl |
|---|---:|
| Nicht begonnen | 39 |
| Plan erstellt | 28 |
| Read modelliert | 0 |
| Write modelliert | 15 |
| Getestet | 10 |
| GUI-kompatibel | 38 |
| In Arbeit | 0 |
| **Gesamt** | **130** |

## Aktueller Hinweis zu 095

Diagnose 095 dokumentiert den UPR-FVX-Guard-Fix fuer den spaeteren Normal-Palette-only-Smoke:

- UPR-FVX `2697511da9a97df4c29c00dfda8b40e556020489` schreibt im CFRU/DPE-Gate nur sichere Normal-Paletten.
- Shiny-, Shared-, Invalid-, Missing-, Decode-failed-, Cross-kind-shared- und unsichere Forme-Faelle werden nicht an den komprimierten Rewriter uebergeben.
- Kein ROM-/Reload-Smoke wurde in diesem Block ausgefuehrt.
- `FVX-GFX-001` bleibt bis zum separaten Reload-Smoke `Write modelliert`.
- `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben `Write modelliert`.

## Vorheriger Hinweis zu 094

Diagnose 094 plant den naechsten engen Palette-Fix-/Smoke-Scope auf Basis von Diagnose 093:

- Reviewbar ist nur ein Normal-Palette-only-Scope fuer die `candidateWritableNormalPalettes=385`.
- Spaeterer Writer darf nur Normal-Paletten schreiben, die single-owner, dekomprimierbar, gueltig, nicht shared, nicht missing, nicht invalid, nicht decode-failed und nicht cross-kind shared sind.
- Alle Shiny-, Shared-, Invalid-, Missing-, Decode-failed- und unsicheren Forme-/Expanded-Mapping-Faelle bleiben preserve-only.
- Der bestehende komprimierte Palette-Pfad kann Repointing erfordern; ein spaeterer Smoke muss Pointer-/Free-Space-/Reload-Kriterien explizit nachweisen.
- `FVX-GFX-001` kann spaeter hoechstens als Normal-only-Single-owner-Subset getestet werden.
- `FVX-GFX-002`, `FVX-GFX-003` und `FVX-GFX-004` bleiben getrennt und aktuell `Write modelliert`.

## Vorheriger Hinweis zu 093

Diagnose 093 fuehrt die read-only Palette-Pointer-/Compression-Diagnose sanitisiert aus:

- `candidateLoaded=true`
- `palettePointerScanSuccessful=true`
- `normalPalettePointersTotal=1439`
- `shinyPalettePointersTotal=1439`
- `candidateWritablePalettes=385`
- `candidateWritableNormalPalettes=385`
- `candidateWritableShinyPalettes=0`
- `skipPaletteEntries=2493`
- `crossKindSharedPalettePointers=1809`
- `sharedPointerGroups=775`
- `largestSharedPointerGroupSize=156`
- Ergebnis: ein spaeterer Fix-/Smoke-Scope kann hoechstens normal-palette-only, single-owner/decompressible sein. Shiny, shared, invalid, missing und decode-failed Paletten bleiben preserve-only.
- `FVX-GFX-001..004` bleiben `Write modelliert`; keine GUI-Kompatibilitaets-Hochstufung.

## Vorheriger Hinweis zu 092

Diagnose 092 plant die read-only Palette-Pointer-/Compression-Diagnose als naechsten Schritt vor jedem Palette-Fix:

- Normal- und Shiny-Palette-Pointer sollen getrennt und aggregiert klassifiziert werden.
- Metriken umfassen dekomprimierbare, nicht dekomprimierbare, single-owner, shared, missing/null, invalid/out-of-ROM, duplicate und candidateWritable Paletten.
- Shared, missing, invalid und decode-failed Paletten bleiben preserve-only.
- Ein spaeterer Fix ist nur fuer dekomprimierbare single-owner Kandidaten eng genug, solange keine explizite Secondary-Pointer-/Shared-Pointer-Policy existiert.
- Raw Pointer, Offsets, ROM-Namen, Hashes, lokale Pfade, Logs und Output-ROMs duerfen nicht dokumentiert werden.
- `FVX-GFX-001..004` bleiben `Write modelliert`.

## Vorheriger Hinweis zu 091

Diagnose 091 plant den Preserve-/Repoint-Scope fuer echte CFRU/DPE Pokemon-Palette-Randomization:

- `PokemonPalettesMod.RANDOM` aktiviert `Gen3to5PaletteRandomizer` und fuehrt bei geaenderten Paletten in `Gen3RomHandler.savePokemonPalettes()`.
- Der Save-Pfad schreibt geaenderte Normal-/Shiny-Paletten ueber komprimierte `rewriteCompressedPalette()`-/`DataRewriter`-Repointing-Logik.
- Die bestehenden Safety-Fixes belegen nur defensive missing/invalid Palette Loads und Skip-Unchanged-Saves.
- Direkter Fix ist noch nicht eng genug, weil Compression, FreeSpace, Single-Pointer-Annahme, Shared-Pointer, missing/invalid Slots und Forme-/Mapping-Fragen vorab inventarisiert werden muessen.
- `FVX-GFX-001` Pokemon Palettes Random bleibt `Write modelliert`.
- `FVX-GFX-002` Palettes: Follow Types bleibt `Write modelliert` und ist kein TypeChart-/TypeEffectiveness-Scope.
- `FVX-GFX-003` Palettes: Follow Evolutions bleibt `Write modelliert` und ist kein Evolution-Writer-Scope.
- `FVX-GFX-004` Palettes: Shiny From Normal bleibt `Write modelliert` und braucht sichere Normal-Palette-Inputs.
- Custom Player Graphics bleibt getrennt.

## Vorheriger Hinweis zu 090

Diagnose 090 dokumentiert den erneuten Candidate-Preflight fuer den engen Name-only fixed-length Reload-Smoke fuer `FVX-MOVE-005`:

- Workspace PR #133 ist gemerged; der blockierte Retry ist damit im aktuellen Arbeitsblock abgeschlossen.
- Der lokale Preflight blieb sanitisiert und dokumentierte keine privaten Pfade, ROM-Namen, Hashes, Logauszuege oder Output-ROMs.
- `candidateFilesChecked=94`.
- `candidatePreflightSuccessful=false`.
- `candidateMovesTotal=not available`.
- `candidateHighestMove=not available`.
- Der fachliche Name-only Reload-Smoke wurde nicht ausgefuehrt, weil kein Kandidat gleichzeitig `moves.total=992` und `991:PsychicNoise` meldete.
- `saveSuccessful`, `logSuccessful`, Output-, Reload-, Name-Length-, Terminator-/Padding-, Description-Pointer- und Name-Reload-Zaehler bleiben nicht fachlich ausgewertet.
- `FVX-MOVE-005` wird nicht hochgestuft und bleibt `Write modelliert`.
- Weitere Name-only-Smokes warten auf einen explizit freigegebenen lokalen CFRU/DPE Gen9-BPRE-Kandidaten mit `moves.total=992` und `991:PsychicNoise`.
- Move Descriptions / Text/Menu-Repointing bleibt getrennt und zurueckgestellt.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` bleiben GUI-kompatibel.

## Vorheriger Hinweis zu 089

Diagnose 089 dokumentiert den Versuch eines engen Name-only fixed-length Reload-Smokes fuer `FVX-MOVE-005`:

- Der lokale Harness blieb auf den bestehenden Gen3 fixed-length `MoveNames`-Pfad begrenzt.
- Der fachliche Smoke konnte nicht ausgewertet werden, weil lokal kein freigegebener CFRU/DPE Gen9-BPRE-Kandidat mit `moves.total=992` und `991:PsychicNoise` gefunden wurde.
- `saveSuccessful`, `logSuccessful`, Reload-, Name-Length-, Terminator-/Padding-, Description-Pointer- und Name-Reload-Zaehler bleiben nicht fachlich ausgewertet.
- `FVX-MOVE-005` wird nicht hochgestuft und bleibt `Write modelliert`.
- Move Descriptions / Text/Menu-Repointing bleibt getrennt und zurueckgestellt.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` bleiben GUI-kompatibel.

## Vorheriger Hinweis zu 088

Diagnose 088 plant den getrennten Text/Menu-Scope fuer `FVX-MOVE-005`:

- `FVX-MOVE-005` ist kein sauberer MoveData-Byte-Writer im `BattleMove`-Scope `+0..+11`.
- Der direkte Gen3/CFRU/DPE-Pfad fuer Randomize Move Names ist die fixed-length Move-Namen-Tabelle aus `MoveNames` und `MoveNameLength`.
- `MoveNameRandomizer` veraendert `Move.name`; `Gen3RomHandler.saveMoves()` schreibt Namen ueber `writeFixedLengthString(...)`.
- Ein enger Name-only Reload-Smoke ist realistisch, solange generierte Namen innerhalb der sichtbaren 12-Zeichen-Grenze bleiben und Terminator/Padding stabil reloaden.
- Move Descriptions / Text/Menu-Repointing bleibt getrennt und vorerst zurueckgestellt.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` bleiben GUI-kompatibel.

## Vorheriger Hinweis zu 087

Diagnose 087 bestaetigt den engen MoveData Fairy-Type-Byte-Fix fuer `FVX-MOVE-004`:

- UPR-FVX `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3` liest und schreibt im sicheren CFRU/DPE-Gen9-BPRE-MoveData-Gate Fairy als raw `0x17`.
- `Randomize Move Types` erreicht `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und erfolgreichen Reload.
- `writeReloadMoveDataMismatches=0`.
- `typeReloadMismatches=0`, `fairyReloadMismatches=0`, `cfruDpeTypeByteMismatches=0`.
- `moves.total=992` und `991:PsychicNoise` bleiben nach Reload stabil.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
- `typeByteMismatches=54` ist nur der erwartete Legacy-Mapping-Vergleich gegen `Gen3Constants.typeToByte(...)` und kein CFRU/DPE-Reload-Fehler.
- `FVX-MOVE-004` wird damit als GUI-kompatibel gefuehrt.
- Der Fix beruehrt nicht TypeChart, TypeEffectiveness oder Species-Type-Write.
- `FVX-MOVE-005` Move Names bleibt ausserhalb dieses Writer-Preserve-Smokes.

## Vorheriger Hinweis zu 086

Diagnose 086 dokumentiert den engen MoveData Types Reload-Smoke fuer `FVX-MOVE-004`:

- UPR-FVX `bb5ee11978e38839979e654ff1c14ba60a0cde93` erreicht fuer `Randomize Move Types` `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true` und erfolgreichen Reload.
- `moves.total=992` und `991:PsychicNoise` bleiben nach Reload stabil.
- Der Smoke ist blockiert: `writeReloadMoveDataMismatches=54`, `typeReloadMismatches=54`, `expectedFairyMoves=54`, `fairyReloadMismatches=54`, `cfruDpeTypeByteMismatches=54`.
- `typeByteMismatches=0` beschreibt nur die Uebereinstimmung mit der aktuellen FVX-Writer-Mappingfunktion.
- Die aktuelle Gen3-MoveData-Type-Mappingfunktion schreibt `FAIRY` im MoveData-Pfad faktisch als Fallback `0x00`; fuer den getesteten CFRU/DPE Gen9-BPRE-Stand muss `FAIRY` im sicheren MoveData-Gate als raw `0x17` geschrieben werden.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
- `FVX-MOVE-004` bleibt deshalb `Write modelliert`.
- Der Folgefix darf nicht mit TypeChart, TypeEffectiveness oder Species-Type-Write vermischt werden.
- `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003` und `FVX-MOVE-006` bleiben GUI-kompatibel.
- `FVX-MOVE-005` Move Names bleibt ausserhalb dieses Writer-Preserve-Smokes.

## Vorheriger Hinweis zu 085

Diagnose 085 bestaetigt den engen MoveData Power/Accuracy/PP Reload-Smoke:

- UPR-FVX `bb5ee11978e38839979e654ff1c14ba60a0cde93` reloadet `FVX-MOVE-001`, `FVX-MOVE-002` und `FVX-MOVE-003` mit `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true` und `logNonEmpty=true`.
- `writeReloadMoveDataMismatches=0`.
- `moves.total=992` und `991:PsychicNoise` bleiben nach Reload stabil.
- Power/Accuracy/PP reloaden stabil: `powerReloadMismatches=0`, `accuracyReloadMismatches=0`, `ppReloadMismatches=0`.
- Rohbytes fuer `+1 power`, `+3 accuracy` und `+4 pp` stimmen mit den erwarteten Move-Werten ueberein: `powerByteMismatches=0`, `accuracyByteMismatches=0`, `ppByteMismatches=0`.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben bytegleich: `preserveByteMismatchesAllMoves=0`, `preserveByteMismatchesUnchangedMoves=0`.
- `FVX-MOVE-001`, `FVX-MOVE-002` und `FVX-MOVE-003` werden damit als GUI-kompatibel gefuehrt.
- `FVX-MOVE-004` Randomize Move Types bleibt konservativ auf `Write modelliert`, bis ein eigener Type-Byte-Smoke vorliegt.
- `FVX-MOVE-005` Move Names bleibt ausserhalb dieses Writer-Preserve-Smokes.

## Vorheriger Hinweis zu 084

Diagnose 084 bestaetigt den engen MoveData Write Preserve Reload-Smoke:

- UPR-FVX `bb5ee11978e38839979e654ff1c14ba60a0cde93` reloadet den MoveData-Writer-Preserve-Scope mit `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true` und `logNonEmpty=true`.
- `Update Moves` erreicht `writeReloadMoveDataMismatches=0`.
- `moves.total=992` und `991:PsychicNoise` bleiben nach Reload stabil.
- Der `BattleMove.split`-Write bei Byte `+10` wurde ueber eine gezielt erzwungene einzelne Category-Aenderung geprueft: `categorySplitMismatches=0`, `categoryReloadMismatches=0`.
- Preserve-Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben fuer unveraenderte Moves bytegleich: `preserveByteMismatchesUnchangedMoves=0`.
- `FVX-MOVE-006` wird damit als GUI-kompatibel gefuehrt.
- `FVX-MOVE-001` bis `FVX-MOVE-004` teilen den Writer-Scope, bleiben aber konservativ auf `Write modelliert`, bis ihre konkreten Randomizer-Suboptionen separat GUI-nah geraucht wurden.
- `FVX-MOVE-005` Move Names bleibt ausserhalb dieses Writer-Preserve-Smokes.

## Vorheriger Hinweis zu 083

Diagnose 083 dokumentiert den engen MoveData-Write-Preserve-Fix:

- UPR-FVX `bb5ee11978e38839979e654ff1c14ba60a0cde93` bleibt auf `Gen3RomHandler.saveMoves()` begrenzt.
- Klassische MoveData-Bytes `+0 effect`, `+1 power`, `+2 type`, `+3 accuracy` und `+4 pp` werden weiter geschrieben.
- Im bestehenden CFRU/DPE-Gen9-BPRE-Gate wird `BattleMove.split` bei Byte `+10` geschrieben: `PHYSICAL -> 0`, `SPECIAL -> 1`, `STATUS -> 2`.
- Nicht modellierte Bytes `+5`, `+6`, `+7`, `+8`, `+9` und `+11` bleiben bytegleich erhalten.
- Reload-Sanity wurde separat in Diagnose 084 bestaetigt; einzelne MoveData-Randomizer-Suboptionen ausser `Update Moves` bleiben konservativ bis zu eigenen GUI-nahen Smokes.

## Vorheriger Hinweis zu 082

Diagnose 082 bestaetigt `FVX-TRAIT-018` nach der 081-Normalisierung:

- `FVX-TRAIT-018` Evolutions Similar Strength ist im `FVX-TRAIT-016` Evolution-Species-Carrier stabil: Save/Log/Output/Reload true, `normalizedWriteReloadEvolutionMismatches=0`, `rawWithFormeWriteReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- Der 082-Reload-Vergleich nutzt nur persistierte Gen3-Evolution-Felder: Evolution-Type, ExtraInfo mit Item-ID-Normalisierung und Ziel-Species per interner `SpeciesSet`-Identitaet; `Evolution.forme` ist kein Mismatch-Kriterium.
- `Bad Egg=true` bleibt nach 055 als bestehender Evolution-Log-/Sonder-Species-Marker klassifiziert, weil der normalisierte Reload stabil ist und der Mismatch-Zaehler `0` bleibt.
- `FVX-TRAIT-019` Evolutions Same Typing ist nach dem Evolution-Same-Typing-Null-Type-Fix im `FVX-TRAIT-016` Evolution-Species-Carrier stabil: Save/Log/Output/Reload true, `writeReloadEvolutionMismatches=0`, `<unknown>=false`, `exceptionClass=none` und `stacktrace=none`.
- UPR-FVX `74d88a7ab1d306e1e09ccabb851dffd7f6922b66` bleibt auf `EvolutionRandomizer` und den Same-Typing-/Null-Primary-Type-Scope begrenzt.
- `FVX-FOE-009` Force Diverse Types / Trainer Type Diversity ist nach dem Trainer-Type-Diversity-Null-Type-Fix im `FVX-FOE-001` Trainer-Pokemon-Carrier stabil: Save/Log/Output/Reload true, `writeReloadTrainerPokemonMismatches=0`, `filterViolations=0`, `Bad Egg=false`, `<unknown>=false` und `stacktrace=none`.
- UPR-FVX `d89fc64e3b0223b03a65466422847dc7df30d03c` bleibt auf `TrainerPokemonRandomizer` und den Force-Diverse-Types-/`usedTypes`-Pfad begrenzt.
- `FVX-WILD-011` Wild Similar Strength und `FVX-WILD-004` Wild Type Restrictions / Type Themes / Keep Primary sind seit Diagnose 075 im `FVX-WILD-001` Standard/Fallback-Wild-Carrier stabil.
- Trainer Similar Strength ist weiterhin als Suboption unter `FVX-FOE-001` im Trainer-Species-Carrier-Smoke stabil: Save/Log/Output/Reload true und `writeReloadTrainerPokemonMismatches=0`.
- Die Statuswerte in der Matrix bleiben konservativ fuer weitere Evolution-Suboptionen und Evolution-Methoden-Writer.

## Coverage nach GUI-Tab

| GUI-Tab | Features | Nicht begonnen | Plan erstellt | Read modelliert | Write modelliert | Getestet | GUI-kompatibel | In Arbeit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| General Options | 4 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| Pokemon Traits | 28 | 7 | 15 | 0 | 0 | 0 | 6 | 0 |
| Starters, Statics & Trades | 15 | 5 | 0 | 0 | 0 | 5 | 5 | 0 |
| Moves & Movesets | 11 | 0 | 3 | 0 | 1 | 0 | 7 | 0 |
| Foe Pokemon | 14 | 8 | 0 | 0 | 0 | 0 | 6 | 0 |
| Wild Pokemon | 12 | 3 | 1 | 0 | 0 | 0 | 8 | 0 |
| TM/HMs & Tutors | 15 | 0 | 9 | 0 | 0 | 0 | 6 | 0 |
| Items | 10 | 0 | 0 | 0 | 10 | 0 | 0 | 0 |
| Types | 3 | 0 | 0 | 0 | 0 | 3 | 0 | 0 |
| Graphics | 6 | 2 | 0 | 0 | 4 | 0 | 0 | 0 |
| Misc Tweaks | 12 | 12 | 0 | 0 | 0 | 0 | 0 | 0 |

## Feature Matrix

### General Options

- FVX-GEN-001 | Limit Pokemon | Getestet
- FVX-GEN-002 | No Premature Evolutions | Getestet
- FVX-GEN-003 | No Random Intro Mon | Nicht begonnen
- FVX-GEN-004 | Race Mode | Nicht begonnen

### Pokemon Traits

- FVX-TRAIT-001 | Base Stats: Shuffle / Random | GUI-kompatibel
- FVX-TRAIT-002 | Base Stats: Follow Evolutions | Plan erstellt
- FVX-TRAIT-003 | Randomize Added Stats on Evolution | Plan erstellt
- FVX-TRAIT-004 | Update Base Stats to Generation | Nicht begonnen
- FVX-TRAIT-005 | Standardize EXP Curves | Nicht begonnen
- FVX-TRAIT-006 | Pokemon Types randomisieren | GUI-kompatibel
- FVX-TRAIT-007 | Force Dual Types | Plan erstellt
- FVX-TRAIT-008 | Pokemon Abilities randomisieren | GUI-kompatibel
- FVX-TRAIT-009 | Abilities: Follow Evolutions | Plan erstellt
- FVX-TRAIT-010 | Abilities: Allow Wonder Guard | Plan erstellt
- FVX-TRAIT-011 | Abilities: Combine Duplicate Abilities | Plan erstellt
- FVX-TRAIT-012 | Abilities: Ensure Two Abilities | Plan erstellt
- FVX-TRAIT-013 | Abilities: Ban Trapping Abilities | Plan erstellt
- FVX-TRAIT-014 | Abilities: Ban Negative Abilities | Plan erstellt
- FVX-TRAIT-015 | Abilities: Ban Bad Abilities | Plan erstellt
- FVX-TRAIT-016 | Pokemon Evolutions randomisieren | GUI-kompatibel
- FVX-TRAIT-017 | Evolutions: Random Every Level | Plan erstellt
- FVX-TRAIT-018 | Evolutions: Similar Strength | GUI-kompatibel
- FVX-TRAIT-019 | Evolutions: Same Typing | GUI-kompatibel
- FVX-TRAIT-020 | Evolutions: Limit to Three Stages | Plan erstellt
- FVX-TRAIT-021 | Evolutions: No Convergence | Plan erstellt
- FVX-TRAIT-022 | Evolutions: Force Change | Plan erstellt
- FVX-TRAIT-023 | Evolutions: Force Growth | Plan erstellt
- FVX-TRAIT-024 | Change Impossible Evolutions | Nicht begonnen
- FVX-TRAIT-025 | Make Evolutions Easier | Nicht begonnen
- FVX-TRAIT-026 | Use Estimated Evolution Levels | Nicht begonnen
- FVX-TRAIT-027 | Remove Time-Based Evolutions | Nicht begonnen
- FVX-TRAIT-028 | EXP-/Legendary-Kurven-Sonderfaelle | Nicht begonnen

### Starters, Statics & Trades

- FVX-SST-001 | Starter Pokemon: Custom | GUI-kompatibel
- FVX-SST-002 | Starter Pokemon: Random completely | GUI-kompatibel
- FVX-SST-003 | Starter Pokemon: Random basic with 2 evolutions | Getestet
- FVX-SST-004 | Starter Pokemon: Random any basic | Getestet
- FVX-SST-005 | Starter Type Restrictions | Getestet
- FVX-SST-006 | Starter: Don't Use Legendaries | Getestet
- FVX-SST-007 | Starter Held Items randomisieren | Nicht begonnen
- FVX-SST-008 | Starter Held Items: Ban Bad Items | Nicht begonnen
- FVX-SST-009 | Starter BST-Min/Max | Getestet
- FVX-SST-010 | Static Pokemon: Swap Legendaries & Standards | GUI-kompatibel
- FVX-SST-011 | Static Pokemon: Random completely | GUI-kompatibel
- FVX-SST-012 | Static Pokemon: Random similar strength | GUI-kompatibel
- FVX-SST-013 | Static Pokemon: Level Modifier / Fix Music | Nicht begonnen
- FVX-SST-014 | In-Game Trades: Given/Requested species | Nicht begonnen
- FVX-SST-015 | In-Game Trades: Nickname/OT/IV/Item | Nicht begonnen

### Moves & Movesets

- FVX-MOVE-001 | Randomize Move Power | GUI-kompatibel
- FVX-MOVE-002 | Randomize Move Accuracy | GUI-kompatibel
- FVX-MOVE-003 | Randomize Move PP | GUI-kompatibel
- FVX-MOVE-004 | Randomize Move Types | GUI-kompatibel
- FVX-MOVE-005 | Randomize Move Names | Write modelliert
- FVX-MOVE-006 | Update Moves to Generation | GUI-kompatibel
- FVX-MOVE-007 | Pokemon Movesets randomisieren | GUI-kompatibel
- FVX-MOVE-008 | Guaranteed Level 1 Moves | Plan erstellt
- FVX-MOVE-009 | Reorder Damaging Moves | GUI-kompatibel
- FVX-MOVE-010 | No Game-Breaking Moves | Plan erstellt
- FVX-MOVE-011 | Force % Good Damaging Moves | Plan erstellt

### Foe Pokemon

- FVX-FOE-001 | Trainer Pokemon randomisieren | GUI-kompatibel
- FVX-FOE-002 | Better Movesets: Boss Trainers | GUI-kompatibel
- FVX-FOE-003 | Better Movesets: Important Trainers | GUI-kompatibel
- FVX-FOE-004 | Better Movesets: Regular Trainers | GUI-kompatibel
- FVX-FOE-005 | Additional Pokemon: Boss Trainers | Nicht begonnen
- FVX-FOE-006 | Additional Pokemon: Important Trainers | Nicht begonnen
- FVX-FOE-007 | Additional Pokemon: Regular Trainers | Nicht begonnen
- FVX-FOE-008 | Trainer Held Items | GUI-kompatibel
- FVX-FOE-009 | Force Diverse Types | GUI-kompatibel
- FVX-FOE-010 | Pokemon League Has Unique Pokemon | Nicht begonnen
- FVX-FOE-011 | Battle Style randomisieren | Nicht begonnen
- FVX-FOE-012 | Rival Carries Starter Through Game | Nicht begonnen
- FVX-FOE-013 | Randomize Trainer Names / Class Names | Nicht begonnen
- FVX-FOE-014 | Trainers Evolve Their Pokemon + Level Modifier | Nicht begonnen

### Wild Pokemon

- FVX-WILD-001 | Randomize Wild Pokemon | GUI-kompatibel
- FVX-WILD-002 | Replacements Per Species | GUI-kompatibel
- FVX-WILD-003 | Split by Encounter Types | GUI-kompatibel
- FVX-WILD-004 | Type Restrictions | GUI-kompatibel
- FVX-WILD-005 | Evolution Restrictions | Plan erstellt
- FVX-WILD-006 | Don't Use Legendaries | GUI-kompatibel
- FVX-WILD-007 | Set Minimum Catch Rate | Nicht begonnen
- FVX-WILD-008 | Randomize Wild Held Items | GUI-kompatibel
- FVX-WILD-009 | Ban Bad Held Items | GUI-kompatibel
- FVX-WILD-010 | Catch Em All Mode | Nicht begonnen
- FVX-WILD-011 | Similar Strength | GUI-kompatibel
- FVX-WILD-012 | Balance Low Level Encounters + Level Modifier | Nicht begonnen

### TM/HMs & Tutors

- FVX-TM-001 | TM Moves randomisieren | GUI-kompatibel
- FVX-TM-002 | Keep Field Move TMs | Plan erstellt
- FVX-TM-003 | TM No Game-Breaking Moves | Plan erstellt
- FVX-TM-004 | TM Force % Good Damaging Moves | Plan erstellt
- FVX-TM-005 | TM/HM Compatibility randomisieren | GUI-kompatibel
- FVX-TM-006 | TM/Levelup Move Sanity | GUI-kompatibel
- FVX-TM-007 | TM Compatibility Follow Evolutions | Plan erstellt
- FVX-TM-008 | Full HM Compatibility | Plan erstellt
- FVX-TM-009 | Move Tutor Moves randomisieren | GUI-kompatibel
- FVX-TM-010 | Keep Field Move Tutors | Plan erstellt
- FVX-TM-011 | Tutor No Game-Breaking Moves | Plan erstellt
- FVX-TM-012 | Tutor Force % Good Damaging Moves | Plan erstellt
- FVX-TM-013 | Tutor Compatibility randomisieren | GUI-kompatibel
- FVX-TM-014 | Tutor/Levelup Sanity | GUI-kompatibel
- FVX-TM-015 | Tutor Compatibility Follow Evolutions | Plan erstellt

### Items

- FVX-ITEM-001 | Field Items Shuffle | GUI-kompatibel im engen allowed-slot Scope
- FVX-ITEM-002 | Field Items Random | GUI-kompatibel im engen Field-Items-Random-Scope; Ban Bad fuer RANDOM getestet
- FVX-ITEM-003 | Field Items Random even distribution | GUI-kompatibel im engen Random-Even-Scope ohne Ban Bad
- FVX-ITEM-004 | Field Items Ban Bad Items | Getestet fuer FieldItemsMod.RANDOM; Random Even + Ban Bad ausstehend
- FVX-ITEM-005 | Shop Items Shuffle | Write modelliert
- FVX-ITEM-006 | Shop Items Random | Write modelliert
- FVX-ITEM-007 | Shop Item Bans | Write modelliert
- FVX-ITEM-008 | Guarantee Evolution/X Items | Write modelliert
- FVX-ITEM-009 | Balance Shop Prices / Cheap Rare Candies | Write modelliert
- FVX-ITEM-010 | Pickup Items Random / Ban Bad Items | Write modelliert

### Types

- FVX-TYPE-001 | Type Effectiveness Random/Balanced/Keep Identities/Inverse | Getestet
- FVX-TYPE-002 | Add Random Immunities | Getestet
- FVX-TYPE-003 | Update Type Effectiveness | Getestet

### Graphics

- FVX-GFX-001 | Pokemon Palettes Random | Write modelliert
- FVX-GFX-002 | Palettes: Follow Types | Write modelliert
- FVX-GFX-003 | Palettes: Follow Evolutions | Write modelliert
- FVX-GFX-004 | Palettes: Shiny From Normal | Write modelliert
- FVX-GFX-005 | Custom Player Graphics | Nicht begonnen
- FVX-GFX-006 | Character to Replace | Nicht begonnen

### Misc Tweaks

- FVX-MISC-001 | Fastest Text | Nicht begonnen
- FVX-MISC-002 | Running Shoes Indoors | Nicht begonnen
- FVX-MISC-003 | Randomize PC Potion | Nicht begonnen
- FVX-MISC-004 | Give National Dex at Start | Nicht begonnen
- FVX-MISC-005 | Fast Egg Hatching | Nicht begonnen
- FVX-MISC-006 | Lower Case Pokemon Names | Nicht begonnen
- FVX-MISC-007 | Randomize Catching Tutorial | Nicht begonnen
- FVX-MISC-008 | Ban Lucky Egg | Nicht begonnen
- FVX-MISC-009 | Balance Static Pokemon Levels | Nicht begonnen
- FVX-MISC-010 | Run Without Running Shoes | Nicht begonnen
- FVX-MISC-011 | Reusable TMs | Nicht begonnen
- FVX-MISC-012 | Forgettable HMs | Nicht begonnen

## Roadmap-Gruppierung

Diese Matrix soll nicht als 130 Roadmap-Zeilen gepflegt werden. Fuer die Roadmap gelten Feature-Pakete:

1. General Options
2. Pokemon Traits
3. Starters, Statics & Trades
4. Moves & Movesets
5. Foe Pokemon
6. Wild Pokemon
7. TM/HMs & Tutors
8. Items
9. Types
10. Graphics
11. Misc Tweaks
12. GUI-Suboptions-Regressionsmatrix
13. Regression-Smoke-Plan

## Aktueller Bezug zu vorhandenen Diagnosen

- `08_tests/randomizer/047_fvx_gui_options_compatibility_matrix.md` ist die bisherige technische GUI-Kompatibilitaetsmatrix.
- `08_tests/randomizer/055_type_log_placeholder_hygiene.md` trennt Log-/Fallback-Marker von echten Blockern.
- `08_tests/randomizer/056_p1_move_data_write_model.md` modelliert MoveData-Write-Risiken.
- `08_tests/randomizer/083_move_data_write_preserve_diagnostics.md` dokumentiert den UPR-FVX-Fix fuer klassischen MoveData-Write plus CFRU/DPE `BattleMove.split`-Write; Reload-Smoke bleibt offen.
- `08_tests/randomizer/088_move_names_text_menu_scope_plan.md` dokumentiert `FVX-MOVE-005` als getrennten Text/Menu-Scope; ein Name-only fixed-length Smoke ist realistisch, Move Descriptions / Repointing bleibt zurueckgestellt.
- `08_tests/randomizer/089_move_names_fixed_length_reload_smoke.md` dokumentiert den blockierten Name-only-Smoke-Versuch; ohne lokalen 992-Move-Kandidaten bleibt `FVX-MOVE-005` `Write modelliert`.
- `08_tests/randomizer/057_p1_field_items_shops_pickup_model.md` modelliert Field Items, Shops und Pickup.
- `08_tests/randomizer/058_p1_palette_randomization_model.md` modelliert echte Palette-Randomization getrennt von Palette-Safety.
- `08_tests/randomizer/059_p1_type_chart_model.md` modelliert Type-Chart-/Effectiveness-Randomization.
- `08_tests/randomizer/060_p1_gui_suboptions_regression_matrix.md` konsolidiert GUI-Suboptionen und empfiehlt einen Regression-Smoke-Plan.
- `08_tests/randomizer/064_p1_global_species_pool_regression_smoke_results.md` bestaetigt `FVX-GEN-001` und `FVX-GEN-002` im getesteten `FVX-SST-002`-Starter-Carrier-Smoke; das ist keine globale Vollabdeckung fuer Wild-/Trainer-/Evolution-Kombinationen.
- `08_tests/randomizer/065_p1_starters_suboptions_regression_smoke_results.md` bestaetigt `FVX-SST-003`, `FVX-SST-004`, `FVX-SST-005`, `FVX-SST-006` und `FVX-SST-009` im getesteten Starter-Species-Writer-Smoke; Starter Held Items `FVX-SST-007`/`FVX-SST-008` bleiben separat/offen.
- `08_tests/randomizer/066_type_chart_preserve_effectiveness_fix_diagnostics.md` bestaetigt `FVX-TYPE-001` im TypeEffectiveness-only Random-Smoke mit Fairy-Reload und `writeReloadTypeChartMismatches=0`; Balanced, Keep Identities und Inverse bleiben als einzelne Folgesmokes sinnvoll.
- `08_tests/randomizer/068_type_effectiveness_followup_smoke_results.md` bestaetigt `FVX-TYPE-001` Balanced, Keep Type Identities und Inverse sowie `FVX-TYPE-002` Add Random Immunities und `FVX-TYPE-003` Update Type Effectiveness einzeln mit Save/Log/Output/Reload true und `writeReloadTypeChartMismatches=0`.
- `08_tests/randomizer/078_trainer_type_diversity_nulltype_fix_diagnostics.md` bestaetigt `FVX-FOE-009` Trainer Type Diversity / Type Themes im `FVX-FOE-001` Trainer-Pokemon-Carrier mit Save/Log/Output/Reload true, `writeReloadTrainerPokemonMismatches=0` und `filterViolations=0`.

## Pflege-Regeln

- Statusaenderungen an einzelnen Features werden zuerst in dieser Datei dokumentiert.
- `00_project-control/roadmap/fvx-feature-roadmap.md` bleibt die verdichtete Roadmap-Sicht.
- `00_project-control/roadmap/roadmap-status.md` verweist nur auf grobe Arbeitspakete und grosse Statusaenderungen.
- Neue Tests sollen ihre Feature-IDs nennen, damit Ergebnisse rueckverfolgbar bleiben.
- Keine ROMs, Saves, Builds, Tool-Binaries, privaten Pfade oder Secrets in diese Datei aufnehmen.

## 2026-05-14 - Palette Normal-only Single-owner Smoke blockiert

- `FVX-GFX-001`: UPR-FVX Write-Guard-Fix vorhanden, aber Diagnose 096 konnte keinen fachlichen Reload-Smoke ausführen, weil kein UPR-FVX-ladbarer CFRU/DPE-Gen9-BPRE-Zielkandidat mit `candidateSpeciesTotal=1439` verfügbar war.
- Status bleibt konservativ: nicht `GUI-kompatibel`; maximal Fix vorbereitet, Smoke blockiert.
- `FVX-GFX-002`, `FVX-GFX-003`, `FVX-GFX-004` bleiben `Write modelliert`.

## 2026-05-14 - Post-Merge Status nach Diagnose 096

- `FVX-GFX-001` bleibt `Write modelliert`: Guard-Fix vorhanden, aber Reload-Smoke blockiert, weil kein UPR-FVX-ladbarer CFRU/DPE Gen9-BPRE-Kandidat mit `candidateSpeciesTotal=1439` verfuegbar war.
- `FVX-GFX-002` bleibt `Write modelliert`.
- `FVX-GFX-003` bleibt `Write modelliert`.
- `FVX-GFX-004` bleibt `Write modelliert`.

## 2026-05-14 - Field Items / Shops / Pickup Scope nach Diagnose 097

- `FVX-ITEM-001` bis `FVX-ITEM-004` bleiben `Write modelliert`; Field Items brauchen einen eigenen Map-/Script-/Hidden-Item-Offset-Smoke.
- `FVX-ITEM-005` bis `FVX-ITEM-009` bleiben `Write modelliert`; Shops brauchen einen eigenen Terminator-/Repointing-/Preis-Scope.
- `FVX-ITEM-010` bleibt `Write modelliert`; Pickup braucht einen eigenen Table-/Locator-/Probability-Scope.
- Encounter Held Items, Trainer Held Items und Starter Held Items bleiben getrennte Datenpfade.

## 2026-05-14 - Field Items diagnostic split

- `FVX-ITEM-001` Field Items Shuffle: remains `Write modelliert`; next step is Field-Items-only diagnostics.
- `FVX-ITEM-002` Field Items Random: remains `Write modelliert`; next step is Field-Items-only diagnostics.
- `FVX-ITEM-003` Field Items Random even distribution: remains `Write modelliert`; next step is Field-Items-only diagnostics.
- `FVX-ITEM-004` Field Items Ban Bad Items: remains `Write modelliert`; next step is Field-Items-only diagnostics.
- Shops, Pickup and held-item paths are intentionally outside this Field-Items-only plan.

## 2026-05-14 - Field Items diagnostics blocked

- `FVX-ITEM-001` Field Items Shuffle: remains `Write modelliert`; diagnostics blocked until an explicitly approved candidate is available.
- `FVX-ITEM-002` Field Items Random: remains `Write modelliert`; diagnostics blocked until an explicitly approved candidate is available.
- `FVX-ITEM-003` Field Items Random even distribution: remains `Write modelliert`; diagnostics blocked until an explicitly approved candidate is available.
- `FVX-ITEM-004` Field Items Ban Bad Items: remains `Write modelliert`; diagnostics blocked until an explicitly approved candidate is available.
- `candidateFilesChecked=0`, `candidateLoaded=false`, `fieldItemScanSuccessful=false`; no fachlicher Field-Item scan was run.

## 2026-05-14 - Field Items candidate diagnostics

- `FVX-ITEM-001` Field Items Shuffle: remains `Write modelliert`; candidate diagnostics support a guarded allowed-slot write/smoke.
- `FVX-ITEM-002` Field Items Random: remains `Write modelliert`; candidate diagnostics support a guarded allowed-slot write/smoke after pool policy is enforced.
- `FVX-ITEM-003` Field Items Random even distribution: remains `Write modelliert`; candidate diagnostics support a guarded allowed-slot write/smoke after pool policy is enforced.
- `FVX-ITEM-004` Field Items Ban Bad Items: remains `Write modelliert`; `badFieldItems=75`, so the ban policy must be asserted in the next smoke.
- Field-Items-only candidate diagnostics: `fieldItemsTotal=339`, allowed `280`, disallowed `59`, TM slots `28`, Non-TM slots `311`, `requiredFieldTMMissing=0`, invalid/unloaded `0`.

## 2026-05-15 - Field Items status after Diagnose 113

- `FVX-ITEM-001 Field Items Shuffle`: `GUI-kompatibel` im getesteten allowed-slot Field-Items-Scope.
- `FVX-ITEM-002 Field Items Random`: `GUI-kompatibel` im getesteten Field-Items-only Scope, inklusive `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM`.
- `FVX-ITEM-003 Field Items Random even distribution`: `GUI-kompatibel` im getesteten Field-Items-only Scope, inklusive `banBadRandomFieldItems=true` fuer `FieldItemsMod.RANDOM_EVEN`.
- `FVX-ITEM-004 Field Items Ban Bad Items`: `GUI-kompatibel` fuer Field Items Random und Random Even.
- Nicht enthalten: Shops, Pickup, Encounter Held Items, Trainer Held Items, Starter Held Items, TM/HM/Tutor/Learnset, Scriptparser, Palette/Graphics, MoveData/MoveNames, TypeChart/TypeEffectiveness, Trainer/Wild/Evolution/Text/Menu.
