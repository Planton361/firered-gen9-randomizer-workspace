# 174 - Evolution Make Evolutions Easier Follow-up

## Scope

- Protokoll: `174_evolution_make_easier_followup.md`
- Branch: `test/upr-fvx-cfru-dpe-make-evolutions-easier-followup`
- Voraussetzung: UPR-FVX PR #44 ist in `Planton361/universal-pokemon-randomizer-fvx` auf `compat/firered-gen9-cfru-dpe` gemerged.
- Modus: Workspace-Follow-up und Submodule-Pin.
- Ergebnis: `follow-up-recorded`

Nicht ausgefuehrt: ROM-Smoke, Randomizer-Lauf, Workspace-Codeaenderung, weitere UPR-FVX-Codeaenderung, Writer-/Reload-Test, Gen3 Happiness-byte patch, Output-ROM, Save, Emulator oder Log-Artefakt.

## UPR-FVX Referenz

- PR: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/44>
- Originaler Commit: `a0fc6515b60ad3032a8d94c554bbc3021e10a33f`
- Gemergter UPR-FVX-Commit / Workspace-Pin: `85b282112322f8991dd11b14cc98d6dd68fd3fd4`
- Base-Branch: `compat/firered-gen9-cfru-dpe`

Betroffene UPR-FVX-Dateien:

- `romio/src/main/java/com/uprfvx/romio/romhandlers/AbstractRomHandler.java`
- `romio/src/test/java/com/uprfvx/romio/romhandlers/EvolutionMakeEasierDecisionTest.java`

## Test-/Seam-Entscheidung

- Kleiner package-private Helper in `AbstractRomHandler`.
- ROM-freier `EvolutionMakeEasierDecisionTest` mit synthetischen `Species`-/`Evolution`-Ketten.
- Getestet fuer `FVX-TRAIT-025A`:
  - intermediate-level cap / Condense-Verhalten
  - final-level cap / Condense-Verhalten
  - non-level `estimatedEvoLvl` capping
  - `highestEvoLvl` Verhalten
- `FVX-TRAIT-026` ist nur als `estimatedEvoLvl`-/Helper-Input beruehrt; kein standalone Support-Claim.

## Checks aus 174A

- `./gradlew --offline :romio:test --tests '*Evolution*'`: `BUILD SUCCESSFUL`
- `./gradlew --offline :romio:test`: `BUILD SUCCESSFUL`
- Bekannte bestehende Report-Failure-Zeile zu `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` bleibt als Risiko/Annahme dokumentiert.

## Statuswirkung

- `FVX-TRAIT-025` bleibt gesplittet:
  - `025A` = `tested-non-rom`
  - `025B` = separater Gen3 Happiness-byte patch / Writer-like Scope offen
- `FVX-TRAIT-026` bleibt Helper-Flag fuer `024/025`; kein standalone Support-Claim.
- Keine P1-Promotion fuer `025`.
- Keine Writer-/Reload-Evidenz, kein ROM-Smoke und keine Output-ROM-Evidenz durch diesen Follow-up.

## Grenzen

- Kein Gen3 Happiness-byte patch.
- Kein Writer-/Reload-Test.
- Kein ROM-Smoke.
- Kein `FVX-TRAIT-025B` Scope.
- Keine P1-Freigabe.
- Keine Promotion fuer `FVX-TRAIT-026` als eigenstaendiges Feature.

## Naechster sinnvoller Schritt

Wenn der Evolution-Methoden-Scope fortgesetzt wird, ist der naechste kleine Block ein read-only Plan fuer `FVX-TRAIT-025B` Gen3 Happiness-byte patch / Writer-like Scope oder ein bewusstes Parken von `025B` bis Writer-/Reload-Evidenz explizit freigegeben wird.

## Sicherheitsnotizen

- Der Workspace pinnt nur den gemergten UPR-FVX-Commit.
- Keine ROMs, Saves, Emulator States, Output-ROMs, Logs, Randomizer-JARs, Tool-Binaries, privaten Pfade, Hashes, Secrets, Tokens oder `.env`-Dateien wurden beruehrt oder dokumentiert.
- Keine weiteren UPR-FVX-Codeaenderungen wurden in diesem Workspace-Block vorgenommen.
- Keine Original-Upstreams wurden kontaktiert.
