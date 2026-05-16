# 178 - Trainer Additional Pokemon Non-ROM Follow-up

## Ergebnis

- Follow-up: `178_trainer_additional_pokemon_followup`
- UPR-FVX PR: #48, <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/48>
- UPR-FVX Base-Branch: `compat/firered-gen9-cfru-dpe`
- Urspruenglicher UPR-FVX Commit: `cdc09eaee12c44a7f3ba5ca24a091ce4da2ef8ac`
- Gemergter UPR-FVX Commit: `32ab7d969e5439d38e5781670c9a68e0ea418d0a`
- Workspace-Branch: `test/upr-fvx-cfru-dpe-trainer-additional-pokemon-followup`

UPR-FVX PR #48 ist gemerged und der Workspace pinnt `02_external/upr-fvx` auf den gemergten Commit
`32ab7d969e5439d38e5781670c9a68e0ea418d0a`.

## Betroffene UPR-FVX-Dateien

- `random/src/main/java/com/uprfvx/random/randomizers/TrainerPokemonRandomizer.java`
- `random/src/test/java/com/uprfvx/random/randomizers/TrainerAdditionalPokemonTest.java`

## Test- und Guard-Scope

`TrainerAdditionalPokemonTest` ist ein Non-ROM `:random:test` mit synthetischen `Trainer`, `TrainerPokemon`
und `Species`-Daten. Er deckt die Additional-Pokemon-Mutation fuer Boss-, Important- und Regular-Trainer ab.

Der Guard in `TrainerPokemonRandomizer.addTrainerPokemon()` verhindert, dass zusaetzliche Pokemon aus
Originalslots mit `null` `TrainerPokemon` oder `null` Species geklont werden. Trainer ohne sichere Vorlage werden
uebersprungen. Max-Party-Size `6` und Multi-Battle-Limit `3` bleiben abgedeckt.

## Getestete Feature-IDs

| Feature-ID | Feature | Evidenz | Statuswirkung |
|---|---|---|---|
| `FVX-FOE-005` | Additional Pokemon: Boss Trainers | Boss-Trainer erhaelt zusaetzliche Pokemon, bleibt bei maximal 6 Party-Slots und klont keine null Species | `tested-non-rom` |
| `FVX-FOE-006` | Additional Pokemon: Important Trainers | Important-Trainer erhaelt zusaetzliche Pokemon, bleibt bei maximal 6 Party-Slots und klont keine null Species | `tested-non-rom` |
| `FVX-FOE-007` | Additional Pokemon: Regular Trainers | Regular-Trainer erhaelt zusaetzliche Pokemon; Multi-Battle-Scope bleibt bei maximal 3 Party-Slots | `tested-non-rom` |

## Checks aus UPR-FVX PR #48

- `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.TrainerAdditionalPokemonTest`: `BUILD SUCCESSFUL`
- `./gradlew --offline :random:test --tests '*Trainer*'`: `BUILD SUCCESSFUL`
- `./gradlew --offline :random:test`: `BUILD SUCCESSFUL`

## Grenzen

- Non-ROM-only; kein ROM-Smoke.
- Keine Trainer Writer-/Reload-ROM-Evidenz.
- Keine Trainer Names/Class Names/Text-Arbeit.
- Keine P1-Promotion und keine Output-ROM-Evidenz.
- Keine weiteren UPR-FVX-Codeaenderungen in diesem Workspace-Follow-up.

## Statuswirkung

`FVX-FOE-005`, `FVX-FOE-006` und `FVX-FOE-007` werden auf `tested-non-rom` hochgestuft.
Das ist keine GUI-kompatible oder P1-supported Freigabe, weil weiterhin ROM-/Reload-Evidenz und
ROM-Smoke fehlen.

## Naechster Schritt

Trainer Additional Pokemon kann vorerst als ROM-frei getestet gefuehrt werden. Eine P1-Promotion braucht
einen separat freigegebenen ROM-/Reload-Scope oder aequivalente Writer-/Reload-Evidenz. Trainer Names/Class Names/Text
bleiben getrennt.
