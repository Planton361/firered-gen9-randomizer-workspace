# 034 - CFRU/DPE Move-Data-Reader Fix Diagnose

## Kontext

Ziel dieses Fixblocks war, `Gen3RomHandler.loadMoves()` fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks minimal zu erweitern. Der Reader soll `MOVES_COUNT=992` nutzen und das CFRU/DPE-`BattleMove.split`-Byte als Move-Kategorie lesen. TM/HM-, Tutor-, Egg-Move- und Learnset-Write-Pfade wurden nicht erweitert.

Gepruefter Stand:

- Workspace-Branch: `compat/upr-fvx-cfru-dpe-move-data-reader`
- Voraussetzung: Workspace PR #70 gemerged.
- UPR-FVX-Ausgangsstand: `655764816f9fefedb9433f33e4da0bc9d44bcda7`
- UPR-FVX-Fixstand: `c71fd75e67f5a839560bbf5de7c6f17317a64bd1`
- Seed: `274269061345323`
- Lokaler Artefaktordner: `05_builds/randomizer-smoke/034_move_data_reader_fix_diagnostics/` (ignored, nicht committed)

## Implementierter Fix

- Die vorhandene sichere CFRU/DPE-Gen9-BPRE-Erkennung wird wiederverwendet: `useCfruDpeGen9SpeciesCount` bleibt das Gate.
- Nur in diesem Gate wird `MoveCount` auf `CFRU_DPE_MOVES_COUNT - 1` gesetzt. Damit enthaelt die FVX-Move-Liste `992` Eintraege inklusive Slot `0`, und der hoechste geladene Move ist ID `991`.
- `BattleMove` bleibt als 12-Byte-Struktur gelesen.
- Fuer CFRU/DPE wird Byte `+10` als `split` gelesen:
  - `0` -> `PHYSICAL`
  - `1` -> `SPECIAL`
  - `2` -> `STATUS`
- Unbekannte Split-Werte fallen auf die alte Gen3-Kategorieableitung zurueck.
- Move-Type-Indizes werden defensiv gelesen; ungueltige Tabellenindizes fallen auf `NORMAL` zurueck.
- Vanilla-, Jambo- und andere Gen3-Pfade behalten die bisherige Description-Pointer-MoveCount-Erkennung und die alte typbasierte Kategorieableitung.

## Move-Daten Diagnose

Ausgangspunkt aus Diagnose 033:

- `moves.total=559`
- Ursache: FVX leitete den BPRE-Hack-`MoveCount` ueber plausible Move-Description-Pointer ab.

Nach Fix:

- `moves.total=992`
- `moves.highestLoaded=991`
- `moves.highestLoadedName=PsychicNoise`
- `moves.categoryPhysical=420`
- `moves.categorySpecial=301`
- `moves.categoryStatus=270`

Gemeinsame Trainer-Ausgangsdaten:

- `before.trainers=255`
- `before.trainerPokemon=481`
- `before.movesetEntries=53`
- `before.zeroMovePokemon=428`
- `before.resetMoves=0`
- `before.invalidMoves=0`
- `before.unknownNamedMoves=0`
- `before.heldItemEntries=0`

## Lauf 1: Trainer Movesets-only Baseline

Aktivierte Optionen:

- Trainer Movesets: aktiv
- Trainer Species: aus
- Trainer Held Items: aus
- Sensible Held Items: aus

Ergebnis:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `outputRomBytes=33554432`
- `logNonEmpty=true`
- `directLogBytes=38794`
- `logContainsBadEgg=false`
- `logContainsUnknown=false`
- `logContainsUnknownMove=false`
- `logContainsGen8MoveSamples=false`
- `logContainsGen9MoveSamples=false`
- `after.movesetEntries=424`
- `after.zeroMovePokemon=57`
- `after.resetMoves=0`
- `after.invalidMoves=0`
- `after.unknownNamedMoves=0`
- `reload.movesetEntries=424`
- `reload.zeroMovePokemon=57`
- `reload.invalidMoves=0`
- `writeReloadMoveMismatches=0`
- `writeReloadHeldItemMismatches=0`
- `writeReloadSpeciesMismatches=0`

## Lauf 2: Trainer Movesets + Trainer Species

Aktivierte Optionen:

- Trainer Movesets: aktiv
- Trainer Species: `RANDOM`
- Trainer Held Items: aus
- Sensible Held Items: aus

Ergebnis:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `outputRomBytes=33554432`
- `logNonEmpty=true`
- `directLogBytes=34845`
- `logContainsBadEgg=false`
- `logContainsUnknown=false`
- `logContainsUnknownMove=false`
- `logContainsGen8MoveSamples=false`
- `logContainsGen9MoveSamples=false`
- `after.gen8plusSpecies=81`
- `after.gen9Species=37`
- `after.movesetEntries=276`
- `after.zeroMovePokemon=205`
- `after.resetMoves=0`
- `after.invalidMoves=0`
- `after.unknownNamedMoves=0`
- `reload.gen8plusSpecies=81`
- `reload.gen9Species=37`
- `reload.movesetEntries=276`
- `reload.zeroMovePokemon=205`
- `reload.invalidMoves=0`
- `writeReloadMoveMismatches=0`
- `writeReloadHeldItemMismatches=0`
- `writeReloadSpeciesMismatches=0`

## Lauf 3: Trainer Movesets + Trainer Held Items normal

Aktivierte Optionen:

- Trainer Movesets: aktiv
- Trainer Species: aus
- Trainer Held Items: normal
- Sensible Held Items: aus

Ergebnis:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `outputRomBytes=33554432`
- `logNonEmpty=true`
- `directLogBytes=44404`
- `logContainsBadEgg=false`
- `logContainsUnknown=false`
- `logContainsUnknownMove=false`
- `logContainsGen8MoveSamples=false`
- `logContainsGen9MoveSamples=false`
- `after.movesetEntries=424`
- `after.zeroMovePokemon=57`
- `after.resetMoves=0`
- `after.invalidMoves=0`
- `after.unknownNamedMoves=0`
- `after.heldItemEntries=481`
- `reload.movesetEntries=424`
- `reload.heldItemEntries=481`
- `reload.invalidMoves=0`
- `writeReloadMoveMismatches=0`
- `writeReloadHeldItemMismatches=0`
- `writeReloadSpeciesMismatches=0`

## Lauf 4: Trainer Movesets + sensible movebasierte Trainer Held Items

Aktivierte Optionen:

- Trainer Movesets: aktiv
- Trainer Species: aus
- Trainer Held Items: sensible
- Sensible Held Items: an

Ergebnis:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `outputRomBytes=33554432`
- `logNonEmpty=true`
- `directLogBytes=44528`
- `logContainsBadEgg=false`
- `logContainsUnknown=false`
- `logContainsUnknownMove=false`
- `logContainsGen8MoveSamples=false`
- `logContainsGen9MoveSamples=false`
- `after.movesetEntries=424`
- `after.zeroMovePokemon=57`
- `after.resetMoves=0`
- `after.invalidMoves=0`
- `after.unknownNamedMoves=0`
- `after.heldItemEntries=481`
- `reload.movesetEntries=424`
- `reload.heldItemEntries=481`
- `reload.invalidMoves=0`
- `writeReloadMoveMismatches=0`
- `writeReloadHeldItemMismatches=0`
- `writeReloadSpeciesMismatches=0`

## Bewertung

- Der Move-Data-Reader erreicht fuer den getesteten CFRU/DPE Gen9-BPRE-Stand `moves.total=992` und laedt `PsychicNoise` als hoechsten dokumentierten Move.
- Trainer Movesets-only bleibt stabil und nutzt nach dem Fix einen vollstaendigeren Move-Pool.
- Trainer Movesets + Species bleibt stabil; Gen8/9-Trainer-Species werden geschrieben und reloaden ohne Species-Mismatches.
- Normale und sensible Trainer-Held-Item-Kombinationen bleiben stabil und reloaden ohne Held-Item-Mismatches.
- In allen vier Laeufen gilt: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM vorhanden, Log nicht leer, `writeReloadMoveMismatches=0`, keine invaliden Moves, kein Bad Egg und kein `<unknown>` im Log.

## Restrisiken

- Die Diagnose bestaetigt den Move-Data-Read-Pfad und Trainer-Kombinationen, aber keine TM/HM-, Tutor-, Egg-Move- oder Learnset-Write-Ausweitung.
- Die Trainer-Logs enthalten in diesen Seeds keine Gen8/9-Move-Samples; das ist kein Fehlernachweis, aber auch kein vollstaendiger Nutzungsnachweis aller neuen Moves in Trainer-Movesets.
- `saveMoves()` wurde nicht erweitert. Move-Data-Randomization fuer CFRU/DPE bleibt daher ein separater Folgepfad, falls spaeter Move-Daten geschrieben werden sollen.
