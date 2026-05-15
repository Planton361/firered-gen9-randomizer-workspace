# 175 - MoveData Write Follow-up

## Scope

- Branch: `test/upr-fvx-cfru-dpe-movedata-write-followup`
- Voraussetzung: UPR-FVX PR #45 ist in `Planton361/universal-pokemon-randomizer-fvx` auf `compat/firered-gen9-cfru-dpe` gemerged.
- Modus: Workspace-Follow-up, Submodule-Pin und Dokumentation.
- Ergebnis: `tested-non-rom` fuer `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006`.

Nicht ausgefuehrt: ROM-Smoke, Writer-/Reload-ROM-Test, Randomizer-Lauf, Build, UPR-FVX-Codeaenderung, Move-Names/Text-Scope, Output-ROM, Save, Emulator oder Log-Artefakt.

## UPR-FVX PR

- PR: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/45>
- Base: `compat/firered-gen9-cfru-dpe`
- Urspruenglicher Commit: `60996b166113d40f4ff848d8063e98661415a599`
- Gemergter UPR-FVX-Commit / Workspace-Pin: `1be6f51779906af017f6177f264e41f8c7902d8e`

## Geaenderte UPR-FVX-Dateien

- `romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java`
- `romio/src/test/java/com/uprfvx/romio/romhandlers/Gen3MoveDataWriterTest.java`
- `random/src/test/java/com/uprfvx/random/updaters/MoveUpdateDecisionTest.java`

## Test-/Seam-Entscheidung

UPR-FVX PR #45 fuegt einen kleinen package-private Gen3-MoveData-Writer-Seam hinzu. Der Seam isoliert die Core-Battle-MoveData-Bytes fuer ROM-freie Tests:

- `effectIndex` bei `+0`
- `power` bei `+1`
- `type` bei `+2`
- `hitratio` / Accuracy bei `+3`
- `pp` bei `+4`
- CFRU/DPE `BattleMove.split` bei `+10`

Der bestehende `saveMoves()`-Pfad delegiert diese Core-Bytes an den Seam. Move Names/Text bleiben davon getrennt; es wurde keine Text-, Repointing- oder Name-Randomization erweitert.

`Gen3MoveDataWriterTest` nutzt synthetische 12-Byte-MoveData-Rows und prueft:

- Power-/Accuracy-/PP-/Type-Bytes werden geschrieben.
- CFRU/DPE Fairy nutzt das erwartete MoveData-Type-Byte.
- Split-Byte wird im CFRU/DPE-Gate geschrieben.
- Nicht verwaltete Bytes bleiben bytegleich preserved.

`MoveUpdateDecisionTest` nutzt synthetische `Move`-Daten und einen minimalen `RomHandler`-Proxy. Der Test prueft ROM-frei, dass `Update Moves to Generation` Power-, Accuracy-, PP- und Type-Entscheidungen anwendet, ohne ROM-Datei, Save, Reload oder Output-ROM.

## Getestete Feature-IDs

| Feature-ID | Feature | Statuswirkung |
|---|---|---|
| `FVX-MOVE-001` | Randomize Move Power | `tested-non-rom` |
| `FVX-MOVE-002` | Randomize Move Accuracy | `tested-non-rom` |
| `FVX-MOVE-003` | Randomize Move PP | `tested-non-rom` |
| `FVX-MOVE-004` | Randomize Move Types | `tested-non-rom` |
| `FVX-MOVE-006` | Update Moves to Generation | `tested-non-rom` |

`FVX-MOVE-005` Randomize Move Names bleibt out of scope / Text. Keine P1-Promotion erfolgt durch diesen Follow-up, weil keine neue ROM-/Reload-Evidenz und kein ROM-Smoke Teil des Blocks ist.

## Checks aus UPR-FVX PR #45

- `git status --short`
- `git diff --stat`
- `git diff --check`
- `rg -n "MoveData|move data|Move Power|Move Accuracy|Move PP|Move Types|Update Moves|writeGen3BattleMoveData|setMoves|moves\\[|type|power|accuracy|pp" romio/src/test romio/src/main random/src/test random/src/main`
- `./gradlew --offline :romio:test --tests '*Move*'`: `BUILD SUCCESSFUL`
- `./gradlew --offline :random:test --tests '*Move*'`: `BUILD SUCCESSFUL`
- `./gradlew --offline :romio:test`: `BUILD SUCCESSFUL`; bekannte bestehende Report-Failure-Zeile zu `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` blieb sichtbar.
- `./gradlew --offline :random:test`: `BUILD SUCCESSFUL`

## Grenzen

- Keine ROM-/Reload-Evidenz.
- Kein ROM-Smoke, kein Randomizer-Lauf und kein Output-ROM.
- Keine Move Names/Text-Arbeit und kein Text/Menu-Repointing.
- Keine P1-Freigabe durch diesen Follow-up.
- Die bekannte bestehende `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` Report-Failure-Zeile bleibt als Risiko/Annahme dokumentiert, obwohl `:romio:test` laut Gradle mit `BUILD SUCCESSFUL` abgeschlossen hat.

## Statuswirkung

`FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` und `FVX-MOVE-006` werden im Workspace als `tested-non-rom` gefuehrt. Das ist ein Fortschritt fuer Writer-/Updater-Entscheidungen, ersetzt aber keine ROM-backed Reload-Evidenz und hebt die Features nicht auf `P1-supported`.

`FVX-MOVE-005` bleibt der getrennte Move Names/Text-Scope und wird durch diesen Follow-up nicht geaendert.

## Empfohlener naechster Schritt

Naechster minimaler Workspace-Schritt ist Statuspflege oder ein separat freigegebener Plan fuer Move Names/Text, falls `FVX-MOVE-005` wieder geoeffnet werden soll. Ein ROM-Smoke oder Writer-/Reload-ROM-Test fuer MoveData braucht einen eigenen expliziten Scope.

## Sicherheitsnotizen

- Es wurden keine ROMs, Saves, Emulator States, Builds, Randomizer-JARs, Tool-Binaries, Logs, Output-ROMs, privaten Pfade, Hashes, Secrets, Tokens oder `.env`-Dateien committed.
- Das UPR-FVX-Submodule wurde nur auf den gemergten PR-#45-Commit gepinnt.
- Keine weiteren UPR-FVX-Codeaenderungen wurden in diesem Workspace-Block vorgenommen.
- Keine Original-Upstreams wurden kontaktiert.
