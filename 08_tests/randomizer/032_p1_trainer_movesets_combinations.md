# 032 - P1 Trainer Movesets Kombinationsdiagnosen

## Kontext

Ziel dieses Diagnoseblocks war, Trainer Movesets-only nach dem CFRU/DPE-Learnset-Reader-Fix als P1-supported Baseline in Kombinationen zu pruefen. Es wurden keine UPR-FVX-Codeaenderungen vorgenommen.

Gepruefter Stand:

- Workspace-Branch: `analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations`
- Voraussetzung: UPR-FVX PR #17 gemerged.
- Voraussetzung: Workspace PR #68 gemerged.
- UPR-FVX-Stand: `655764816f9fefedb9433f33e4da0bc9d44bcda7`
- Seed: `274269061345323`
- Lokaler Artefaktordner: `05_builds/randomizer-smoke/032_p1_trainer_movesets_combinations/` (ignored, nicht committed)

## Harness

Der lokale Diagnose-Harness vergleicht Trainerdaten vor Randomization, nach Randomization und nach Reload der geschriebenen Output-ROM. Gezaehlt wurden Trainer, Trainer-Pokemon, Moveset-Slots, Held-Item-Slots, invalide Moves, Unknown-Move-Marker, `Bad Egg`/`<unknown>` im Log und Write/Reload-Mismatches.

Gemeinsame Ausgangsdaten:

- `moves.total=559`
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
- Trainer Species: unveraendert
- Trainer Held Items: aus
- Sensible Held Items: aus

Ergebnis:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `outputRomBytes=33554432`
- `logNonEmpty=true`
- `directLogBytes=38171`
- `logContainsTrainerPokemon=true`
- `logContainsBadEgg=false`
- `logContainsUnknownSpecies=false`
- `logContainsUnknownMove=false`
- `logContainsAbilityFallback=true`
- `logContainsGen8MoveSamples=false`
- `logContainsGen9MoveSamples=false`
- `after.movesetEntries=417`
- `after.zeroMovePokemon=64`
- `after.invalidMoves=0`
- `after.unknownNamedMoves=0`
- `after.heldItemEntries=0`
- `beforeAfterMoveSignatureChanges=418`
- `reload.movesetEntries=417`
- `reload.zeroMovePokemon=64`
- `reload.invalidMoves=0`
- `writeReloadCompared=481`
- `writeReloadMoveMismatches=0`
- `writeReloadHeldItemMismatches=0`
- `writeReloadSpeciesMismatches=0`

Bewertung: Trainer Movesets-only bleibt nach Write/Reload stabil.

## Lauf 2: Trainer Movesets + Trainer Species-only

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
- `directLogBytes=34951`
- `logContainsTrainerPokemon=true`
- `logContainsBadEgg=false`
- `logContainsUnknownSpecies=false`
- `logContainsUnknownMove=false`
- `logContainsAbilityFallback=true`
- `logContainsGen8MoveSamples=false`
- `logContainsGen9MoveSamples=false`
- `after.gen8plusSpecies=77`
- `after.gen9Species=38`
- `after.movesetEntries=289`
- `after.zeroMovePokemon=192`
- `after.invalidMoves=0`
- `after.unknownNamedMoves=0`
- `after.heldItemEntries=0`
- `beforeAfterMoveSignatureChanges=308`
- `beforeAfterSpeciesChanges=479`
- `reload.gen8plusSpecies=77`
- `reload.gen9Species=38`
- `reload.movesetEntries=289`
- `reload.zeroMovePokemon=192`
- `reload.invalidMoves=0`
- `writeReloadCompared=481`
- `writeReloadMoveMismatches=0`
- `writeReloadHeldItemMismatches=0`
- `writeReloadSpeciesMismatches=0`

Bewertung: Kombination mit Trainer Species-only bleibt stabil. Gen8/9-Trainer-Species werden geschrieben und nach Reload erhalten; Movesets bleiben konsistent, soweit FVX-Move-Daten geladen sind.

## Lauf 3: Trainer Movesets + Trainer Held Items normal

Aktivierte Optionen:

- Trainer Movesets: aktiv
- Trainer Species: unveraendert
- Trainer Held Items: normal
- Sensible Held Items: aus

Ergebnis:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `outputRomBytes=33554432`
- `logNonEmpty=true`
- `directLogBytes=43795`
- `logContainsTrainerPokemon=true`
- `logContainsBadEgg=false`
- `logContainsUnknownSpecies=false`
- `logContainsUnknownMove=false`
- `logContainsAbilityFallback=true`
- `logContainsGen8MoveSamples=false`
- `logContainsGen9MoveSamples=false`
- `after.movesetEntries=417`
- `after.zeroMovePokemon=64`
- `after.invalidMoves=0`
- `after.unknownNamedMoves=0`
- `after.heldItemEntries=481`
- `after.zeroNoItemEntries=0`
- `beforeAfterMoveSignatureChanges=418`
- `beforeAfterHeldItemChanges=481`
- `reload.movesetEntries=417`
- `reload.heldItemEntries=481`
- `reload.zeroNoItemEntries=0`
- `reload.invalidMoves=0`
- `writeReloadCompared=481`
- `writeReloadMoveMismatches=0`
- `writeReloadHeldItemMismatches=0`
- `writeReloadSpeciesMismatches=0`

Bewertung: Kombination mit normaler Trainer-Held-Item-Auswahl bleibt stabil. Die lazy Moveset-Load-Grenze aus PR #16 wird durch Trainer Movesets selbst erwartungsgemaess ueberschritten, aber der CFRU/DPE-Learnset-Reader aus PR #17 entblockt den Pfad.

## Lauf 4: Trainer Movesets + sensible movebasierte Trainer Held Items

Aktivierte Optionen:

- Trainer Movesets: aktiv
- Trainer Species: unveraendert
- Trainer Held Items: sensible
- Sensible Held Items: an

Ergebnis:

- `saveSuccessful=true`
- `logSuccessful=true`
- `outputRomExists=true`
- `outputRomBytes=33554432`
- `logNonEmpty=true`
- `directLogBytes=43935`
- `logContainsTrainerPokemon=true`
- `logContainsBadEgg=false`
- `logContainsUnknownSpecies=false`
- `logContainsUnknownMove=false`
- `logContainsAbilityFallback=true`
- `logContainsGen8MoveSamples=false`
- `logContainsGen9MoveSamples=false`
- `after.movesetEntries=417`
- `after.zeroMovePokemon=64`
- `after.invalidMoves=0`
- `after.unknownNamedMoves=0`
- `after.heldItemEntries=481`
- `after.zeroNoItemEntries=0`
- `beforeAfterMoveSignatureChanges=418`
- `beforeAfterHeldItemChanges=481`
- `reload.movesetEntries=417`
- `reload.heldItemEntries=481`
- `reload.zeroNoItemEntries=0`
- `reload.invalidMoves=0`
- `writeReloadCompared=481`
- `writeReloadMoveMismatches=0`
- `writeReloadHeldItemMismatches=0`
- `writeReloadSpeciesMismatches=0`

Bewertung: Sensible movebasierte Trainer-Held-Item-Auswahl ist fuer diesen Kombinationslauf nicht separat blockiert. Der Pfad kann auf Moveset-/Learnset-Kontext zugreifen und bleibt nach Write/Reload stabil.

## Gesamtbewertung

- Trainer Movesets-only ist auf dem getesteten UPR-FVX-Stand P1-supported.
- Trainer Movesets + Trainer Species-only ist P1-stabil: Gen8/9-Trainer-Species bleiben nach Reload erhalten und erzeugen keine Move-Mismatches.
- Trainer Movesets + normale Trainer Held Items ist P1-stabil.
- Trainer Movesets + sensible movebasierte Trainer Held Items ist im getesteten Harness verfuegbar und P1-stabil.
- In allen vier Laeufen gilt: `saveSuccessful=true`, `logSuccessful=true`, Output-ROM entsteht, Log ist nicht leer, `writeReloadMoveMismatches=0`, `writeReloadHeldItemMismatches=0`, kein `Bad Egg`, kein `<unknown>`, keine Unknown-Move-Marker und keine invaliden Move-IDs.

## Folgerisiken

- `moves.total=559` bleibt deutlich unter dem dokumentierten CFRU/DPE-`MOVES_COUNT=992`. Gen8/9-Moves werden dadurch weiterhin nicht als belastbarer FVX-Move-Datenbestand bestaetigt.
- Die Logs enthalten keine Gen8/9-Move-Samples. Das spricht dafuer, dass die Kombinationen stabil sind, aber nicht, dass Gen8/9-Move-Daten vollstaendig modelliert sind.
- TM-/Tutor-/Egg-Move-Tabellen wurden in diesem Branch nicht aktiviert. Es gibt keine neue Regression, aber diese Pfade bleiben eigene Diagnose-/Modellierungsarbeit.
- Learnset-Write / `setMovesLearnt()` wurde nicht erweitert und bleibt bewusst ausserhalb dieses P1-Kombinationsblocks.
- `logContainsAbilityFallback=true` zeigt weiterhin, dass erweiterte CFRU/DPE-Ability-IDs im Trainer-Log defensiv behandelt werden. Das blockiert den Lauf nicht, sollte aber nicht als vollstaendiges Ability-Datenmodell missverstanden werden.

## Ergebnis

Trainer Movesets ist fuer den getesteten CFRU/DPE Gen9-BPRE-Stand als P1-supported Baseline in den geprueften Kombinationen bestaetigt. Die naechsten Risiken liegen nicht mehr im Trainer-Moveset-Write/Reload-Pfad, sondern im erweiterten Move-Datenmodell und in separaten TM-/Tutor-/Egg-Move-Pfaden.
