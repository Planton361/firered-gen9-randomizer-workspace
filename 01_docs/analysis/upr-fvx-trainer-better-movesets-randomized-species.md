# UPR-FVX Trainer Better Movesets With Randomized Species

Datum: 2026-05-25

## Ziel

Diese Analyse klaert source-backed, warum Trainer-Pokemon nach Foe-Pokemon-Randomization plus Better Movesets offenbar Moves vom alten/originalen Trainer-Pokemon behalten koennen.

Sanitized lokaler Smoke-Befund:

- CFRUDPEExtension `gBattleMons` Reader liest live aus dem finalen Battle-State.
- Player: `Unfezant F Lv30` mit `Growl` / `Leer` / `Roost` / `Aircutter`.
- Enemy: `Incineroar Lv6` mit `Tackle` / `String Shot` / `Stun Spore`.
- Better Movesets war aktiviert.
- Erwartung: Trainer-Moves sollten zur randomisierten Species passen.

## Executive Summary

Die globale Randomizer-Reihenfolge ist nicht die wahrscheinlichste Ursache. In `GameRandomizer.applyRandomizers()` laeuft Trainer-Pokemon-Randomization vor Trainer-Better-Movesets:

| Datei/Funktion | Source-backed Befund | Wirkung |
| --- | --- | --- |
| `random/src/main/java/com/uprfvx/random/GameRandomizer.java:307-308` | `maybeRandomizeTrainerPokemon()` laeuft vor `maybeRandomizeTrainerMovesets()`. | Better Movesets sieht grundsaetzlich bereits randomisierte Trainer-Species. |
| `TrainerPokemonRandomizer.randomizeTrainerPokes()`, `:285-289` | Nach Species-Ersatz setzt der Code `tp.setResetMoves(true)`. | Der Writer soll bei fehlenden Custom-Moves Moves fuer die neue Species berechnen koennen. |
| `TrainerMovesetRandomizer.randomizeTrainerMovesets()`, `:44-52` | Better Movesets setzt `tp.setResetMoves(false)`, bevor geprueft wird, ob ein Move-Pool existiert. Wenn `movesAtLevel` leer ist, wird nur `continue` ausgefuehrt. | Alte `tp.getMoves()` koennen erhalten bleiben und der Writer-Fallback wird deaktiviert. |
| `Gen3RomHandler.trainerPokemonToBytes()`, `:4396-4408` | Bei `resetMoves=true` werden Moves via `getMovesAtLevel()` berechnet; sonst werden `tp.getMoves()[0..3]` direkt geschrieben. | Wenn Better Movesets `resetMoves=false` setzt, werden alte Moves exakt persistiert. |

Wahrscheinlichste Ursache: Better Movesets nutzt zwar die randomisierte Species als Basis, aber der leere/fehlende Pool-Pfad deaktiviert `resetMoves` zu frueh. Dadurch kann ein randomisiertes Pokemon mit alten Custom-Moves in den finalen Battle-State gelangen.

## Relevante Codepfade

### Reihenfolge Trainer Species -> Trainer Better Movesets

`GameRandomizer.applyRandomizers()` ruft erst Trainer-Pokemon- und danach Trainer-Moveset-Randomization auf:

- `GameRandomizer.java:307`: `maybeRandomizeTrainerPokemon()`
- `GameRandomizer.java:308`: `maybeRandomizeTrainerMovesets()`

Innerhalb von `maybeRandomizeTrainerPokemon()`:

- `GameRandomizer.java:579-582`: Rival carry kann vor Trainer-Randomization angewendet werden.
- `GameRandomizer.java:584-588`: `randomizeTrainerPokes()` laeuft bei Trainer-Pokemon-Randomization.
- `GameRandomizer.java:592-599`: Rival carry / Opening Rival Counter-Starter wird nach Trainer-Randomization erneut korrigiert.
- `GameRandomizer.java:603-608`: Better Movesets laeuft danach, wenn eine der Better-Movesets-Optionen aktiv ist.

Bewertung: Der Ablauf ist grundsaetzlich richtig. Better Movesets ist nicht vor der Species-Randomization platziert.

### Species-Randomization setzt Reset-Move-Fallback

`TrainerPokemonRandomizer.randomizeTrainerPokes()` ersetzt die Species und setzt danach Reset-Moves:

- `TrainerPokemonRandomizer.java:270-289`
  - `pickTrainerPokeReplacement(...)`
  - `tp.setSpecies(newSp)`
  - `setFormeForTrainerPokemon(tp, newSp)`
  - `tp.setAbilitySlot(...)`
  - `tp.setResetMoves(true)`

Rival-Starter-Korrektur nutzt denselben Fallback:

- `TrainerPokemonRandomizer.java:741-764`
  - `changeStarterForTrainer(...)`
  - setzt Starter-Species, Forme, `resetMoves=true` und Ability-Slot.

Bewertung: Nach reiner Trainer-Species-Randomization soll der Gen3-Writer Moves fuer die neue Species berechnen koennen.

### Better Movesets deaktiviert Reset-Moves vor Pool-Erfolg

`TrainerMovesetRandomizer.randomizeTrainerMovesets()`:

- `TrainerMovesetRandomizer.java:35-40`: filtert Trainer nach Boss/Important/Regular Better-Movesets-Settings und `!t.shouldNotGetBuffs()`.
- `TrainerMovesetRandomizer.java:44-52`: setzt fuer jedes betroffene Pokemon sofort `tp.setResetMoves(false)`, berechnet dann den Move-Pool, und faehrt bei leerem Pool mit `continue` fort.
- `TrainerMovesetRandomizer.java:108-116`, `:125-133`, `:264-272`: nur bei nichtleerem Pool werden Move-Slots neu geschrieben.
- `TrainerMovesetRandomizer.java:275-276`: fehlende Movesets werden nur als `skippedMissingMovesets` gemeldet.

Der Pool selbst wird aus der aktuellen Species aufgebaut:

- `TrainerMovesetRandomizer.java:608-617`: `trainerSpecies = romHandler.getAltFormeOfSpecies(tp.getSpecies(), tp.getForme())`, danach Level-Up-Moves.
- `TrainerMovesetRandomizer.java:639-656`: TM-Moves anhand `trainerSpecies`.
- `TrainerMovesetRandomizer.java:658-676`: Tutor-Moves anhand `trainerSpecies`.
- `TrainerMovesetRandomizer.java:679-696`: Egg-Moves anhand Evolutionsbasis.
- `TrainerMovesetRandomizer.java:702-717`: Species-Lookup bevorzugt `speciesSetIdentityNumber`, faellt sonst auf `species.getNumber()` zurueck.

Bewertung: Better Movesets schaut nicht offensichtlich auf `originalSpecies`. Das Problem ist der Fehlerpfad: Wenn fuer die randomisierte Species kein nutzbarer Pool entsteht, bleiben alte Moves erhalten, waehrend `resetMoves=false` den Writer-Fallback blockiert.

### Gen3 Writer persistiert entweder Fallback-Moves oder alte Custom-Moves

`Gen3RomHandler.trainerPokemonToBytes()`:

- `Gen3RomHandler.java:4372-4379`: Trainer mit Custom-Moves werden als 16-Byte-Rows geschrieben.
- `Gen3RomHandler.java:4383-4395`: Layout fuer IV, Level, Species, optional Item, danach Move-Slots.
- `Gen3RomHandler.java:4396-4403`: bei `tp.isResetMoves()` werden Moves via `getMovesAtLevel(tp.getSpecies().getNumber(), movesets, tp.getLevel())` berechnet.
- `Gen3RomHandler.java:4404-4408`: sonst werden `tp.getMoves()[0..3]` direkt geschrieben.
- `Trainer.java:350-359`: `pokemonHaveCustomMoves()` ignoriert `resetMoves=true` Pokemon und erkennt Custom-Moves nur an nicht-null Move-Slots von nicht-reset Pokemon.

Bewertung: Das Write-Layout fuer `TrainerMonItemCustomMoves` wirkt in diesem Pfad konsistent mit dem Read-Layout. Das auffaellige Risiko ist nicht primaer ein Slot-Offset-Fehler, sondern dass Better Movesets alte `tp.getMoves()` als neue Custom-Moves stehen laesst.

## Rival-Starter-Befund

Source-backed ist die Rival-Starter-Korrektur vorhanden und nach Trainer-Pokemon-Randomization platziert:

- `GameRandomizer.java:592-599`: `makeRivalCarryStarter()` und `makeFirstRivalCarryStarter()` laufen nach `randomizeTrainerPokes()`.
- `TrainerPokemonRandomizer.java:853-858`: FRLG Opening Rival IDs werden per Spieler-Starter-Slot auf die Counter-Starter-Slots projiziert.
- `TrainerPokemonRandomizer.java:870-879`: passende Trainer-ID wird auf den Starter gesetzt.
- `TrainerPokemonRandomizer.java:887-960`: spaetere Rival/Friend-Tags werden je Starter-Variante aktualisiert, wenn Rival carry aktiv ist.

Vorhandene Tests decken diese Logik ab:

- `GameRandomizerStarterRivalSyncTest.java:17-46`: Reihenfolge und Reapply-Guard fuer Opening Rival / Rival carry.
- `TrainerSpecialRulesTest.java:156-213`: Foe-Randomization korrigiert Oak-Lab und, bei Carry-On, spaetere Rival-Starter wieder.
- `TrainerSpecialRulesTest.java:215-262`: FRLG Opening Rival Trainer-IDs werden auf randomisierte Counter-Starter-Slots gemappt.
- `TrainerSpecialRulesTest.java:265-288`: Foe-Randomization ueberschreibt den korrigierten Rival-Starter nicht erneut.
- `TrainerSpecialRulesTest.java:291-307`: bekannte Runtime-Source-Rival-Rows koennen Counter-Starter tragen.

Interpretation fuer den aktuellen Smoke:

- Ein einzelner `Incineroar Lv6` beweist noch nicht, dass der Rival-Starter-Slot falsch ist. Es muss geklaert werden, ob es der forcierte Starter-Slot oder ein randomisierter Rival-/Trainer-Nichtstarter war.
- Wenn es ein normaler Trainer oder ein Rival-Nichtstarter war, passt der Befund gut zum Better-Movesets-Fallback-Risiko.
- Wenn es sicher der forcierte Oak-Lab- oder Carry-Starter-Slot war, waere das ein separater Bug in Runtime-Source-Auswahl, Trainer-ID/Slot-Erkennung oder Settings-Kontext und sollte mit Trainer-ID/Slot-orientierter Smoke-Doku isoliert werden.

## Bestehende Diagnose-Luecke

Fruehere Diagnosen zeigen Stabilitaet, aber nicht die semantische Korrektheit "Moves passen zur randomisierten Species":

- `08_tests/randomizer/031_trainer_movesets_learnsets_fix_diagnostics.md`: Trainer Movesets-only wurde fuer CFRU/DPE entblockt; leere/ungueltige Learnset-Pointer werden defensiv behandelt.
- `08_tests/randomizer/034_move_data_reader_fix_diagnostics.md:90-126`: Trainer Movesets + Trainer Species speichert und reloadet ohne Move-/Species-Mismatches.

Diese Checks beweisen Write/Reload-Konsistenz. Sie beweisen nicht, dass ein randomisiertes Trainer-Pokemon bei leerem Better-Movesets-Pool keine alten Custom-Moves behaelt.

## Wahrscheinlichste Ursache

Der lokale Befund ist am besten erklaerbar durch diesen Ablauf:

1. Trainer-Pokemon wird von Original-Species auf neue Species randomisiert.
2. `TrainerPokemonRandomizer` setzt `resetMoves=true`.
3. Better Movesets wird auf den Trainer angewendet.
4. `TrainerMovesetRandomizer` setzt `resetMoves=false`.
5. Fuer die neue Species entsteht kein nutzbarer Move-Pool, z. B. wegen fehlender/leer gelesener CFRU/DPE-Learnsets, nicht geladener TM-/Tutor-/Egg-Kompatibilitaet, niedrigem Level oder Filterung.
6. Der Code `continue`t, ohne Move-Slots zu ueberschreiben.
7. Der Gen3-Writer schreibt alte `tp.getMoves()` als Custom-Moves.
8. CFRU baut im Kampf das neue Pokemon mit alten Moves; der `gBattleMons` Reader sieht den finalen Zustand.

Der Smoke-Beispielbefund `Incineroar Lv6` mit `Tackle` / `String Shot` / `Stun Spore` ist damit plausibel: Die Species ist randomisiert, aber die Move-Slots koennen aus dem alten TrainerMon-Kontext stammen.

## Fix-Optionen

| Option | Aenderung | Vorteil | Risiko |
| --- | --- | --- | --- |
| A: Minimaler Guard | In `TrainerMovesetRandomizer`, `tp.setResetMoves(false)` erst nach erfolgreichem nichtleerem Pool und tatsaechlichem Move-Write setzen. Bei leerem Pool `resetMoves=true` erhalten. | Kleinster Fix; nutzt vorhandenen Writer-Fallback fuer neue Species. | Fallback ist Level-Up-only und nicht "Better"; muss fuer CFRU/DPE species identity weiter validiert werden. |
| B: Expliziter Empty-Pool-Fallback | Bei leerem Better-Movesets-Pool Moves explizit fuer aktuelle Species/Level berechnen oder alte Moves loeschen. | Verhindert alte Custom-Moves auch dann, wenn Writer-Poketype spaeter custom bleibt. | Mehr Codepfade; muss Gen3/CFRU/DPE-sicher sein. |
| C: Species-Identity-Fallback auditieren | Pruefen, ob `Gen3RomHandler.getMovesAtLevel(tp.getSpecies().getNumber(), ...)` fuer CFRU/DPE immer korrekt auf interne Species-ID faellt. | Schuetzt den Reset-Fallback fuer Gen9/expanded Species. | Loest nicht allein das zu-fruehe `resetMoves=false`. |
| D: Kombinations-Test | ROM-freier oder ROM-backed Test: randomisierte Species + Better Movesets + leerer Pool darf keine alten Moves schreiben. | Macht Regression klar sichtbar. | ROM-backed Test darf keine privaten Artefakte committen. |

Empfohlener minimaler Implementierungsschritt: Option A plus ein fokussierter Test, der den leeren Pool simuliert und bestaetigt, dass `resetMoves=true` erhalten bleibt.

## Testfaelle fuer Fix

1. Rival-Starter-Battle
   - Oak-Lab Rival forcierter Starter-Slot.
   - Erwartung: Species ist Counter-Starter zum gewaehlten Player-Starter.
   - Moves werden nicht aus dem alten Vanilla-/Bug-Kontext uebernommen.

2. Regular Trainer mit Better Movesets
   - Trainer-Species randomisiert auf eine Species mit klar unterscheidbarem Learnset.
   - Better Regular Trainer Movesets aktiv.
   - Erwartung: keine alten Custom-Moves des Original-TrainerPokemon.

3. Empty-Pool-Regression
   - Testdaten erzwingen leeren Better-Movesets-Pool fuer eine randomisierte Species.
   - Erwartung: `resetMoves` bleibt aktiv oder Move-Slots werden explizit neu/fallback-sicher gesetzt.

4. CFRUDPEExtension `gBattleMons` Smoke
   - Im lokalen Battle nur sanitized Werte dokumentieren: Trainerrolle, Species, Level, Move-Namen.
   - Erwartung: Battle-State zeigt keine alten Moves, wenn Species randomisiert wurde.

## Offene Fragen

- Welche konkrete Trainer-ID und welcher Slot erzeugten `Incineroar Lv6` im Smoke?
- War es der forcierte Rival-Starter-Slot oder ein Rival-/Trainer-Nichtstarter?
- Welche Better-Movesets-Settings waren aktiv: Boss, Important, Regular oder alle?
- Gab es im Lauf `skippedMissingMovesets`-Ausgabe, und wenn ja, wie hoch?
- Ist der Move-Pool fuer die betroffene Species wegen Learnset, TM/Tutor/Egg-Kompatibilitaet oder Level-Filter leer?
- Muss der Gen3-Writer-Fallback fuer CFRU/DPE konsequent `speciesSetIdentityNumber` statt `species.getNumber()` verwenden?
