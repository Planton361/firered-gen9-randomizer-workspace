# 176 - Wild Catch / Level Non-ROM Follow-up

## Ergebnis

- Follow-up: `176_wild_catch_level_followup`
- Ergebnisstatus: `tested-non-rom`
- Workspace-Branch: `test/upr-fvx-cfru-dpe-wild-catch-level-followup`
- UPR-FVX PR: [#46](https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/46)
- UPR-FVX Base: `compat/firered-gen9-cfru-dpe`
- Urspruenglicher UPR-FVX Commit: `8665eb4f070567fd908327b272c7f1da5abdef68`
- Gemergter UPR-FVX Commit / Workspace-Pin: `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`

UPR-FVX PR #46 ist gemerged und der Workspace pinnt `02_external/upr-fvx` auf den gemergten Commit
`c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.

## Testdatei

- `random/src/test/java/com/uprfvx/random/randomizers/WildCatchLevelDecisionTest.java`

Der Test ist ROM-frei und nutzt synthetische `Species`-, `Encounter`- und `EncounterArea`-Daten mit einem minimalen
`RomHandler`-Proxy.

## Getestete Feature-IDs

| Feature-ID | Feature | Evidenz | Statuswirkung |
|---|---|---|---|
| `FVX-WILD-007` | Set Minimum Catch Rate | niedrige normale und legendaere Catch Rates werden auf den Mindestwert angehoben; hoehere Catch Rates bleiben unveraendert | `tested-non-rom` |
| `FVX-WILD-010` | Catch Em All Mode | synthetische Remaining-Species werden ueber Encounter-Slots verteilt und per `setEncounters(...)` zurueckgegeben | `tested-non-rom` |
| `FVX-WILD-012` | Balance Low Level Encounters + Level Modifier | Level-Modifier veraendert synthetische Encounter-Level; Balance-Low-Level cappt Similar-Strength-Auswahl anhand niedriger Encounter-Level | `tested-non-rom` |

## Checks aus UPR-FVX PR #46

- `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.WildCatchLevelDecisionTest`: `BUILD SUCCESSFUL`
- `./gradlew --offline :random:test --tests '*Wild*'`: `BUILD SUCCESSFUL`
- `./gradlew --offline :random:test`: `BUILD SUCCESSFUL`

## Grenzen

- Non-ROM-only; keine ROM-Datei, kein Save, kein Emulator, kein Output-ROM.
- Keine Writer-/Reload-ROM-Evidenz.
- Kein ROM-Smoke und keine P1-Promotion.
- Kein weiterer UPR-FVX-Code in diesem Workspace-Block.

## Statuswirkung

`FVX-WILD-007`, `FVX-WILD-010` und `FVX-WILD-012` werden auf `tested-non-rom` hochgestuft.
Das ist keine GUI-kompatible oder P1-supported Freigabe, weil weiterhin ROM-/Reload-Evidenz und ROM-Smoke fehlen.

## Naechster sinnvoller Schritt

Wild Catch-/Level-Slices koennen vorerst als ROM-frei getestet gefuehrt werden. Eine P1-Promotion braucht einen
separat freigegebenen ROM-/Reload-Smoke oder eine explizit definierte aequivalente Writer-/Reload-Evidenz.
