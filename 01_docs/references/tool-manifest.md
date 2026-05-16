# Tool Manifest Update - 2026-05-16 - Trainer special rules follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-special-rules-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #49: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/49>.
- Original UPR-FVX test commit: `6489dd1e61d1bcb35345ae006032b884527e0a97`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `bc46fdc49741643d8f09dd302b67b5b2d35d24c5`.
- Previous workspace pin was `32ab7d969e5439d38e5781670c9a68e0ea418d0a`.
- Scope: Non-ROM `TrainerSpecialRulesTest`; synthetic Trainer, Party, Species and Evolution data cover `FVX-FOE-010`, `FVX-FOE-012` and `FVX-FOE-014`.
- Checks recorded from UPR-FVX PR #49: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.TrainerSpecialRulesTest`, `./gradlew --offline :random:test --tests '*Trainer*'` and `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Battle Style scope, no Trainer Names/Class Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer additional pokemon follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-additional-pokemon-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #48: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/48>.
- Original UPR-FVX test commit: `cdc09eaee12c44a7f3ba5ca24a091ce4da2ef8ac`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `32ab7d969e5439d38e5781670c9a68e0ea418d0a`.
- Previous workspace pin was `ea5269706eb7d04eb0b305f88e8fa20bfb21f92a`.
- Scope: Non-ROM `TrainerAdditionalPokemonTest`; synthetic Trainer, Party and Species data cover `FVX-FOE-005`, `FVX-FOE-006` and `FVX-FOE-007`.
- Guard/Fix: `TrainerPokemonRandomizer` clones additional Pokemon only from original slots with non-null Species; trainers without a safe template are skipped, and max party size 6 plus multi-battle limit 3 are covered.
- Checks recorded from UPR-FVX PR #48: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.TrainerAdditionalPokemonTest`, `./gradlew --offline :random:test --tests '*Trainer*'` and `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Trainer Names/Class Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Trainer type diversity follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-trainer-type-diversity-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #47: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/47>.
- Original UPR-FVX test commit: `60f6664e556cc750801ad1d47ba970ded8d6af85`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `ea5269706eb7d04eb0b305f88e8fa20bfb21f92a`.
- Previous workspace pin was `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.
- Scope: Non-ROM `TrainerTypeDiversityGuardTest`; synthetic `Species`, `Trainer` and `TrainerPokemon` data cover `FVX-FOE-009` Force Diverse Types / Type Themes null Primary/Secondary Type guard behavior.
- Checks recorded from UPR-FVX PR #47: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.TrainerTypeDiversityGuardTest`, `./gradlew --offline :random:test --tests '*Trainer*'` and `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Trainer Names/Class Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-16 - Wild catch level follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-wild-catch-level-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #46: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/46>.
- Original UPR-FVX test commit: `8665eb4f070567fd908327b272c7f1da5abdef68`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `c86221d758bece06b216b1f4fb23dd8e4a6c8ec0`.
- Previous workspace pin was `1be6f51779906af017f6177f264e41f8c7902d8e`.
- Scope: Non-ROM `WildCatchLevelDecisionTest`; synthetic `Species`, `Encounter` and `EncounterArea` data cover `FVX-WILD-007`, `FVX-WILD-010` and `FVX-WILD-012`.
- Checks recorded from UPR-FVX PR #46: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.WildCatchLevelDecisionTest`, `./gradlew --offline :random:test --tests '*Wild*'` and `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - MoveData write follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-movedata-write-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #45: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/45>.
- Original UPR-FVX test commit: `60996b166113d40f4ff848d8063e98661415a599`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `1be6f51779906af017f6177f264e41f8c7902d8e`.
- Previous workspace pin was `85b282112322f8991dd11b14cc98d6dd68fd3fd4`.
- Scope: Non-ROM `Gen3MoveDataWriterTest` and `MoveUpdateDecisionTest`; synthetic MoveData bytes and synthetic `Move` data cover `FVX-MOVE-001`, `FVX-MOVE-002`, `FVX-MOVE-003`, `FVX-MOVE-004` and `FVX-MOVE-006`.
- Checks recorded from UPR-FVX PR #45: focused `./gradlew --offline :romio:test --tests '*Move*'`, focused `./gradlew --offline :random:test --tests '*Move*'`, full `./gradlew --offline :romio:test` and full `./gradlew --offline :random:test`, all `BUILD SUCCESSFUL`; known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts committed, no Move Names/Text scope, no ROM-Smoke, no Writer-/Reload-ROM test, no P1-promotion and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - Evolution make easier follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-make-evolutions-easier-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #44: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/44>.
- Original UPR-FVX test commit: `a0fc6515b60ad3032a8d94c554bbc3021e10a33f`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `85b282112322f8991dd11b14cc98d6dd68fd3fd4`.
- Previous workspace pin was `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- Scope: Non-ROM `EvolutionMakeEasierDecisionTest` only; synthetic `Species` / `Evolution` chains and a small package-private helper in `AbstractRomHandler` cover `FVX-TRAIT-025A`.
- Checks recorded from UPR-FVX PR #44: `./gradlew --offline :romio:test --tests '*Evolution*'` and `./gradlew --offline :romio:test`, both `BUILD SUCCESSFUL`; known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no Gen3 Happiness-byte patch, no writer/reload, no ROM-Smoke, no Randomizer run, no `FVX-TRAIT-025B` scope, no `FVX-TRAIT-026` standalone support claim, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - Evolution method decision harness follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-evolution-method-decisions-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #43: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/43>.
- Original UPR-FVX test commit: `4b049ee82cf8716cb2fc17d0b6244020cddd22e4`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `3b33412e80d1cb2d97725ad7a7dd01529aa56919`.
- Previous workspace pin was `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Scope: Non-ROM `EvolutionMethodDecisionTest` only; synthetic `Species` / `Evolution` data and small package-private decision seams in `Gen3RomHandler` and `AbstractRomHandler` cover `FVX-TRAIT-024` and `FVX-TRAIT-027`.
- Checks recorded from UPR-FVX PR #43: `./gradlew --offline :romio:test --tests '*Evolution*'` and `./gradlew --offline :romio:test`, both `BUILD SUCCESSFUL`; known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no Gen3 writer, no reload, no ROM-Smoke, no Randomizer run, no `FVX-TRAIT-025/026` scope except `useEstimatedLevels` as `024` decision input, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - Evolution filter non-ROM harness follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-evolution-filter-non-rom-harness-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #42: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/42>.
- Original UPR-FVX test commit: `e71a126c test: cover evolution filter options`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `587e857088cac4fba41c6559d3a6f6e2a7aad71f`.
- Previous workspace pin was `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Scope: Non-ROM `EvolutionFilterOptionsTest` only; synthetic `Species` / `Evolution` data and a minimal `RomHandler` proxy/fake cover `FVX-TRAIT-017` and `FVX-TRAIT-020` through `FVX-TRAIT-023`.
- Checks recorded from UPR-FVX PR #42: `./gradlew --offline :random:test --tests com.uprfvx.random.randomizers.EvolutionFilterOptionsTest` and `./gradlew --offline :random:test`, both `BUILD SUCCESSFUL`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no ROM-Smoke, no Gen3 writer, no reload, no `FVX-TRAIT-024..027` scope, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - In-Game Trades writer preserve follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-writer-preserve-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #41: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/41>.
- Original UPR-FVX test commit: `b71bd2ec test: cover ingame trade writer preserve guard`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `dc6ad3cb01282db5ff85935959bbdac6c2d3fa0c`.
- Previous workspace pin was `1eaee2873cd69682335223f817b124bf36d004f2`.
- Scope: ROM-free `Gen3InGameTradeWriterTest` only; synthetic `InGameTrade` rows and synthetic bytes cover unsafe/null-request writer preserve decisions through a narrow package-private `Gen3RomHandler` seam.
- Checks recorded from UPR-FVX PR #41: `./gradlew --offline :romio:test` and focused `./gradlew --offline :romio:test --tests com.uprfvx.romio.romhandlers.Gen3InGameTradeWriterTest`, both `BUILD SUCCESSFUL`; known existing `PlayerCharacterGraphicsTest.fromSheetGiveSameImagesAndPalsAsFromSeparate_RSE()` report failure line remains a risk/assumption.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no ROM-Smoke, no Species-Write-Smoke, no valid-active-row promotion, no text, Nickname/OT, IV or Trade Held Item randomization, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - In-Game Trades non-ROM harness follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-non-rom-harness-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #40: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/40>.
- Original UPR-FVX test commit: `8b7d0846 test: cover ingame trade skip guard`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `1eaee2873cd69682335223f817b124bf36d004f2`.
- Previous workspace pin was `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Scope: non-ROM `TradeRandomizerTest` harness only; synthetic `InGameTrade` rows and a minimal `RomHandler` proxy/fake cover null-request and placeholder/unsafe Species skips, all-skipped no `setInGameTrades(...)`, `isChangesMade=false`, skip counters and `hasSkippedTrades()`.
- Safety: no Workspace code changes, no UPR-FVX code changes in this block, no ROM/save/output/log/build artifacts, no Gen3 writer test, no ROM-Smoke, no Species-Write-Smoke, no text, Nickname/OT, IV or Trade Held Item randomization, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - In-Game Trades null-request guard follow-up

- Workspace branch: `test/upr-fvx-cfru-dpe-ingame-trades-null-request-guard-followup`.
- UPR-FVX fork base branch: `compat/firered-gen9-cfru-dpe`.
- UPR-FVX PR #39: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/39>.
- Original UPR-FVX fix commit: `1d3062d1 fix: skip unsafe ingame trade rows`.
- Workspace submodule `02_external/upr-fvx` now pins merged UPR-FVX commit `a86315e8d82e0854e0fd59549f50e2c49f523c40`.
- Previous workspace pin was `a2373888ad17145f270ebf6ff17303af41aa86eb`.
- Scope: In-Game Trades defensive null/invalid Species guard only; `TradeRandomizer.java` skips unsafe rows before mutation and `Gen3RomHandler.java` preserves/skips unsafe rows before byte writes.
- Safety: no Workspace code changes, no ROM/save/output/log/build artifacts, no text randomization, no Nickname/OT, IV or Trade Held Item randomization, and no Original-Upstream PR.

# Tool Manifest Update - 2026-05-15 - Pickup reload locator fix

- Workspace branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- UPR-FVX fork branch: `compat/upr-fvx-cfru-dpe-pickup-items-reload-locator-fix`.
- UPR-FVX PR #38: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/38>.
- Workspace submodule `02_external/upr-fvx` now pins `a2373888ad17145f270ebf6ff17303af41aa86eb` for the Pickup table reload locator fix.
- Previous pin was `328e4441c2981d37aba9e2707a6f27f779b026e2`.

# Tool Manifest Update - 2026-05-15 - UPR-FVX Field Items API TM-slot fix

- `02_external/upr-fvx` pinned to Planton361/universal-pokemon-randomizer-fvx commit `328e4441c2981d37aba9e2707a6f27f779b026e2` on branch `compat/upr-fvx-cfru-dpe-field-items-api-tm-slot-scope-fix`.
- UPR-FVX PR #37 opened against `compat/firered-gen9-cfru-dpe`: <https://github.com/Planton361/universal-pokemon-randomizer-fvx/pull/37>.
- Scope: CFRU/DPE Field-Items API TM-slot exposure only; no original-upstream PR.

# Tool Manifest Update - 2026-05-15 - Field Items Random TM-pool fix pin

Dieser Stand dokumentiert den Arbeitsblock `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix`. UPR-FVX wurde im Planton361-Fork-Submodule eng im Field-Items-Random-TM-Pool geaendert; kein ROM-/Randomizer-Reload-Smoke wurde in diesem Block ausgefuehrt. Tool-Binaries, Release-Assets, Secrets und private Pfade wurden nicht dokumentiert.

| Komponente | Rolle | Remote | Lokaler Pfad | Branch | Commit/Pin | Aenderung | Notiz |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-field-items-random-tm-pool-fix` | `7b4fb8ed8bcf00c6e0ac2871459adfeec1503fcd` | ja, nur in diesem Branch | Field-Items-Random-TM-Pool-Fix fuer `FVX-ITEM-002`; Required TMs bleiben Pflicht, Filler-Pool dedupliziert; Reload-Smoke noch offen |

# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

## Sicherheitsstatus

Dieser Stand dokumentiert den Arbeitsblock `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`. UPR-FVX wurde im Planton361-Fork-Submodule gezielt geaendert und gebaut; kein ROM-/Randomizer-Reload-Smoke wurde ausgefuehrt. Tool-Binaries, Release-Assets, Secrets und private Pfade wurden nicht dokumentiert.

Linux/CachyOS ist die primaere lokale Umgebung. Windows-Toolchain-Befunde bleiben historischer Referenzstand und duerfen nicht als Linux-Ist-Stand verwendet werden.

Der aktuelle Arbeitsblock pinnt den Workspace auf den UPR-FVX-Normal-Palette-Single-owner-Write-Guard-Fix-Commit fuer CFRU/DPE.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | Workspace-Root | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` | offen | ja, nur Branches | aktiv |
| Git | Versionierung | n/a | n/a | `/usr/bin/git` | n/a | n/a | nein | gefunden: 2.54.0 |
| GitHub CLI (`gh`) | PRs und GitHub-Checks automatisieren | https://cli.github.com/ | n/a | `/usr/bin/gh` | n/a | n/a | nein | gefunden: 2.92.0; Auth via Keyring aktiv |
| POSIX Shell | Terminal-Standard | n/a | n/a | `/bin/fish` laut `$SHELL` | n/a | n/a | nein | primär |
| PowerShell 7 (`pwsh`) | optionale Script-Ausführung für bestehende Checks | https://github.com/PowerShell/PowerShell | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt/optional |
| Java | Laufzeit fuer UPR FVX | https://adoptium.net/ oder Distribution-Paket | n/a | `/usr/bin/java` | n/a | n/a | nein | gefunden: OpenJDK 26.0.1; UPR-FVX-Anforderung spaeter verifizieren |
| `make` | Build-Orchestrierung fuer spaetere Toolchain-Schritte | n/a | n/a | `/usr/bin/make` | n/a | n/a | nein | gefunden: GNU Make 4.4.1 |
| devkitPro/devkitARM | GBA Build Toolchain | devkitPro | n/a | Linux-Pfad offen | n/a | n/a | nein | nicht nachgewiesen; Installation nur in separatem Block |
| `arm-none-eabi-gcc` | GBA Cross-Compiler | ARM GNU Toolchain/devkitARM | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt; ueber devkitPro/devkitARM priorisiert klaeren |
| `agbcc` | optionale GBA/pret-kompatible Compiler-Komponente | pret/devkitARM-Kontext | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt/optional; nur bei Buildpfad-Bedarf klaeren |
| Codex CLI | primärer Coding Agent | OpenAI | n/a | offen | n/a | n/a | nur nach Branch-Freigabe | primärer Worker fuer erlaubte Arbeitsbranches |
| ChatGPT QA | Analyse, Review und Handoff | OpenAI | n/a | n/a | n/a | n/a | nein | Steuerungs-/QA-Ebene |
| JetBrains Toolbox | JetBrains IDE-Verwaltung | JetBrains | n/a | User-Installation; privater Pfad nicht dokumentiert | n/a | n/a | nein | gefunden: Toolbox 3.4.3.81140 |
| IntelliJ IDEA | optionale lokale IDE-Navigation | JetBrains | n/a | Toolbox-verwaltete User-Installation; privater Pfad nicht dokumentiert | n/a | Build `IU-262.4852.50` | nein | gefunden: IntelliJ IDEA 2026.2 EAP; Mindestversion 2025.2 erfuellt |
| JetBrains MCP Server | optionale IDE-MCP-Integration fuer read-only Codebase-Analyse | JetBrains, gebuendelt in IntelliJ-basierten IDEs | n/a | gebuendeltes IntelliJ-Plugin `com.intellij.mcpServer`; Installationspfad nicht dokumentiert | n/a | Plugin-Version `262.4852.50` | nein | verfuegbar; fuer Codex nur read-only und optional freigegeben |
| `.aiignore` | Agent-Kontextschutz | n/a | n/a | `.aiignore` | n/a | n/a | ja | ergänzt fuer ROM-/Build-/Tool-Binary-/Secret-Pfade |
| GitHub PR Template | PR-Checkliste | GitHub | n/a | `.github/pull_request_template.md` | n/a | n/a | ja | ergänzt |
| MCP allgemein | optionale Tool-Integration | abhängig vom Server | n/a | keine aktive Config committed | n/a | n/a | nur nach Manifest-Eintrag | optional, nicht Default |
| UPR FVX | Randomizer | https://github.com/upr-fvx/universal-pokemon-randomizer-fvx | offen | `02_external/upr-fvx` oder lokales JAR unter `03_tools/releases/upr-fvx/` | offen | offen | nur nach Freigabe | read-only geprüft; spaeter Release/JAR oder Source-Clone entscheiden |
| CFRU-expansion | FireRed Gen9/CFRU-Basis | https://github.com/Shiny-Miner/CFRU-expansion | offen | `02_external/CFRU-expansion` | offen | offen | nur nach Freigabe | Hauptbasis-Kandidat; nicht geklont |
| DPE Gen9 | Pokémon Expansion | https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | offen | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | offen | offen | nur nach Freigabe | Hauptbasis-Kandidat; nicht geklont |
| Skeli789 CFRU | Upstream CFRU-Referenz | https://github.com/Skeli789/Complete-Fire-Red-Upgrade | n/a | `02_external/Complete-Fire-Red-Upgrade` | offen | offen | nein, Referenz zuerst | read-only geprüft; nicht geklont |
| Skeli789 DPE | Upstream DPE-Referenz | https://github.com/Skeli789/Dynamic-Pokemon-Expansion | n/a | `02_external/Dynamic-Pokemon-Expansion` | offen | offen | nein, Referenz zuerst | read-only geprüft; nicht geklont |
| CyanSMP64 NatDexExtension | IronMON/NatDex-Referenz | https://github.com/CyanSMP64/NatDexExtension | offen | `02_external/NatDexExtension` | offen | offen | nur nach Freigabe | read-only geprüft; nicht geklont |
| pret/pokefirered | FireRed Decomp-Referenz | https://github.com/pret/pokefirered | n/a | `02_external/pokefirered` | offen | offen | nein, Referenz zuerst | read-only geprüft; nicht geklont |
| Hex Maniac Advance | ROM-Analyse | offen | n/a | `03_tools/releases` | n/a | n/a | nein | Quelle offen; Tool-Binary nicht committen |
| BizHawk | Emulator | https://github.com/TASEmulators/BizHawk | n/a | `03_tools/releases` | n/a | n/a | nein | read-only geprüft; Tool-Binary nicht committen |
| Ironmon Tracker | Tracker | https://github.com/besteon/Ironmon-Tracker | offen | `02_external/Ironmon-Tracker` | offen | offen | nur nach Freigabe | read-only geprüft; nicht geklont |

## Lokale Submodule-Pins 2026-05-14

Arbeitsblock: `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` | `2697511da9a97df4c29c00dfda8b40e556020489` | ja, nur in diesem Branch | Normal-Palette-Single-owner-Write-Guard fuer CFRU/DPE; Shiny/shared/invalid/missing/decode-failed/cross-kind Faelle werden nicht an den Palette-Rewriter uebergeben; Reload-Smoke noch offen |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only, unveraendert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only, unveraendert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

Arbeitsblock: `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-move-data-type-fairy-byte` | `fad56f60d6fae9b006290a4d5fd1f0715f3d9dc3` | ja, nur in diesem Branch | MoveData-Fairy-Type-Byte-Fix fuer CFRU/DPE; `Type.FAIRY` wird im sicheren MoveData-Gate als raw `0x17` gelesen/geschrieben; `FVX-MOVE-004` reloadet mit `writeReloadMoveDataMismatches=0`; kein TypeChart/TypeEffectiveness/Species-Type-Write |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only, unveraendert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only, unveraendert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

Arbeitsblock: `compat/upr-fvx-cfru-dpe-move-data-write-preserve`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-move-data-write-preserve` | `bb5ee11978e38839979e654ff1c14ba60a0cde93` | ja, nur in diesem Branch | MoveData-Write-Preserve-Fix fuer CFRU/DPE; klassische MoveData-Bytes `+0..+4` bleiben geschrieben, `BattleMove.split` wird im CFRU/DPE-Gate bei `+10` geschrieben, Preserve-Bytes bleiben unangetastet; Reload-Smoke noch offen |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only, unveraendert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only, unveraendert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

Arbeitsblock: `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-p1-evolution-same-typing-nulltype-fix` | `74d88a7ab1d306e1e09ccabb851dffd7f6922b66` | ja, nur in diesem Branch | Evolution-Same-Typing-Null-Type-Fix fuer CFRU/DPE; `FVX-TRAIT-019` im `FVX-TRAIT-016` Carrier mit Save/Log/Output/Reload und `writeReloadEvolutionMismatches=0` bestaetigt |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only analysiert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only analysiert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

## Lokale Submodule-Pins 2026-05-13

Arbeitsblock: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write` | `5c7170b654b09e1fc27ced6857dd50a8e4711f08` | ja, nur in diesem Branch | Encounter-Held-Items-Scope-and-Write-Fix fuer CFRU/DPE; basiert auf Abilities-Hidden-Ability-Scope-and-Write-Fix `639c7e61` |
| CFRU-expansion Fork | CFRU/Gen9-Basis | `https://github.com/Planton361/CFRU-expansion.git` | `02_external/CFRU-expansion` | `compat/firered-gen9-randomizer` | `b885d7a974375c6c722e5698914963b82e8cdad6` | nein in diesem Block | read-only analysiert |
| DPE Gen9 Fork | DPE/Gen9-Basis | `https://github.com/Planton361/Dynamic-Pokemon-Expansion-Gen-9.git` | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `compat/firered-gen9-randomizer` | `5906aa4d4904e41393fd9184a16951c961e96263` | nein in diesem Block | read-only analysiert |
| CyanSMP64 UPR-ZX NatDex | NatDex-Randomizer-Referenz | `https://github.com/CyanSMP64/universal-pokemon-randomizer-zx.git` | `02_external/references/cyansmp64-upr-zx-natdex` | `natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` | nein | read-only Referenz |
| CyanSMP64 FireRed NatDex | NatDex-FireRed-Referenz | `https://github.com/CyanSMP64/pokefirered.git` | `02_external/references/cyansmp64-pokefirered-natdex` | `natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` | nein | read-only Referenz |
| UPR-FVX upstream | FVX-Upstream-Vergleich | `https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git` | `02_external/references/upr-fvx-upstream` | `master` | `e0788edc6529c2605f201996e4807ff30165354c` | nein | read-only Referenz |
| Ajarmar UPR-ZX | UPR-ZX-Basisvergleich | `https://github.com/Ajarmar/universal-pokemon-randomizer-zx.git` | `02_external/references/upr-zx-ajarmar` | `master` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` | nein | read-only Referenz |
| pret FireRed | Vanilla-BPRE-Decomp | `https://github.com/pret/pokefirered.git` | `02_external/references/pret-pokefirered` | `master` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` | nein | read-only Referenz |

## Workspace-Zielstruktur fuer Integration

| Pfad | Zweck | Git-Regel |
|---|---|---|
| `02_external/` | spaetere lokale Clone-Ziele fuer UPR FVX, CFRU/DPE und Referenzen | Clone-Inhalte nicht vendorisieren; Branch/Commit im Manifest pinnen |
| `03_tools/` | Tool-Dokumentation | committen |
| `03_tools/releases/` | UPR-FVX-JARs, BizHawk, Hex Maniac, Tool-Releases | lokal/ignored, nicht committen |
| `04_private_roms/` | private FireRed-ROM-Basis und lokale ROM-Arbeitskopien | lokal/ignored, nicht in ChatGPT hochladen |
| `05_builds/` | CFRU/DPE-Build-Ausgaben, gepatchte GBA, lokale Logs | lokal/ignored, nicht committen |
| `08_tests/` | Smoke-Test-Protokolle ohne ROM-Inhalte | committen |

## Randomizer-Smoke-Artefaktkonvention

Arbeitsblock: `maintenance/randomizer-smoke-artifact-cleanup`.

| Pfad | Zweck | Git-Regel |
|---|---|---|
| `08_tests/randomizer/README.md` | Index, Nummerierung und Latest-Markierung fuer Randomizer-Smoke-Protokolle | committen |
| `08_tests/randomizer/NNN_<kurzer-zweck>.md` | neue dauerhafte Randomizer-Smoke-Protokolle | committen |
| `05_builds/randomizer-smoke/NNN_<kurzer-zweck>/` | lokale ROM-/Log-/Output-Artefakte passend zum Protokoll | lokal/ignored, nicht committen |

Bestehende unnummerierte Protokolle unter `08_tests/randomizer/` bleiben vorerst unveraendert und werden ueber die README-Tabelle eingeordnet. Der neueste bestaetigte Stand wird in Markdown als `Latest` markiert; ein lokaler `latest`-Symlink ist nicht erforderlich.

## UPR-FVX Source Build

| Thema | Stand |
|---|---|
| Lokaler Pfad | `02_external/upr-fvx` |
| Einbindung | Git-Submodule auf `Planton361/universal-pokemon-randomizer-fvx` |
| Upstream | `upr-fvx/universal-pokemon-randomizer-fvx` |
| Arbeitsbranch | `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write` |
| Gepinnter Workspace-Stand | `2697511da9a97df4c29c00dfda8b40e556020489` auf `compat/upr-fvx-cfru-dpe-palette-normal-single-owner-write`; enthaelt den CFRU/DPE-Normal-Palette-Single-owner-Write-Guard-Fix auf Basis der bisherigen MoveData-Fairy-Type-Byte-Fixkette |
| Buildsystem | Gradle Wrapper |
| Java | JDK 25 |
| JAR-Build | `./gradlew :random:jar` |
| GUI-Start | `./gradlew :random:launch` oder `java -jar random/build/libs/UPR-FVX.jar` |
| ROM-freie Tests | `./gradlew test` |
| ROM-Tests | `./gradlew :romio:testROMs`, `./gradlew :random:testROMs`; nur separat freigegeben |


## Linux/CachyOS-Inventur

Arbeitsblock: `setup/linux-toolchain-inventory`.

| Prüfpunkt | Status | Nachweisstand | Nächster Schritt |
|---|---|---|---|
| Git | gefunden | `/usr/bin/git`; Git 2.54.0 | keine Aktion |
| GitHub CLI (`gh`) | gefunden, Auth aktiv | `/usr/bin/gh`; gh 2.92.0; Auth-Refresh auf `setup/linux-gh-auth-refresh` erfolgreich | keine Aktion |
| Shell | gefunden | `$SHELL` ist `/bin/fish` | POSIX-kompatible Projektbefehle weiter bevorzugen |
| Java | gefunden | `/usr/bin/java`; OpenJDK 26.0.1 | UPR-FVX-Anforderung spaeter gegen konkrete Version pruefen |
| `make` | gefunden | `/usr/bin/make`; GNU Make 4.4.1 | keine Aktion |
| devkitPro/devkitARM | offen | nicht installiert oder nicht nachgewiesen; keine Installation durchgefuehrt | separaten Toolchain-Setup-Block planen |
| `arm-none-eabi-gcc` | fehlt | nicht im PATH gefunden | spaeter devkitPro/devkitARM oder ARM-Toolchain klaeren |
| `agbcc` | fehlt/optional | nicht im PATH gefunden | nur bei konkretem pret-/Build-Bedarf klaeren |
| `pwsh` | fehlt/optional | nicht im PATH gefunden | PowerShell-Checks unter Linux nur nutzen, wenn `pwsh` separat bereitgestellt wird |

## Linux/CachyOS GitHub-Auth-Refresh

Arbeitsblock: `setup/linux-gh-auth-refresh`.

- GitHub CLI und Git-Auth sind auf Linux/CachyOS wieder funktionsfähig.
- `gh` ist fuer Account `Planton361` authentifiziert; der Token-Wert wurde nicht übernommen.
- `git fetch origin` ist erfolgreich und bestätigt Remote-Zugriff auf `origin`.
- GitHub CLI und Git können fuer Push und PR-Erstellung genutzt werden.

## Linux/CachyOS GBA-Toolchain-Plan

Arbeitsblock: `setup/linux-gba-toolchain-plan`.

Planungsdokument: `01_docs/setup/linux-gba-toolchain-plan.md`.

| Thema | Stand | Naechster Schritt |
|---|---|---|
| devkitPro/devkitARM | primaere Richtung vorbereiten, aber nicht installieren | Installation/Check nur in separatem Arbeitsblock |
| `arm-none-eabi-gcc` | fehlt im PATH; soll im Kontext der Ziel-Toolchain geloest werden | pruefen, ob devkitARM oder Fallback-Paket genutzt werden soll |
| `agbcc` | fehlt/optional | erst bei konkretem pret-/Build-Bedarf bewerten |
| Build-Schritte | weiterhin gesperrt | erst nach Repo-Pinning, Toolchain-Freigabe und ROM-/Build-Freigabe |
| Externe Repos | weiterhin nicht geklont | erst nach separater Clone-/Fork-Entscheidung |

## Workspace Build and Randomizer Integration

Arbeitsblock: `planning/workspace-build-randomizer-integration`.

Planungsdokument: `01_docs/setup/workspace-build-randomizer-integration-plan.md`.

| Thema | Stand | Naechster Schritt |
|---|---|---|
| Private FireRed-ROM | bleibt nur lokal in `04_private_roms/`; keine ROM in Git/ChatGPT | separater `rom/fire-red-private-hash-check`-Block |
| devkitPro/devkitARM | Ziel-Toolchain fuer spaeteres Bauen | `setup/devkitpro-toolchain-install-check` nach Freigabe |
| CFRU/DPE Gen9 | Shiny-Miner-Forks bleiben Hauptkandidaten | Branch/Commit pinnen, bevor Clone/Fork/Build erfolgt |
| UPR FVX | Haupt-Randomizer-Kandidat | Release/JAR oder Source-Clone entscheiden; Java-Anforderung pruefen |
| `03_tools/releases/` | lokaler Ort fuer JARs/Tool-Binaries | ignored, nicht committen |
| `05_builds/` | lokaler Ort fuer Build-Ergebnisse | ignored, nicht committen |
| `08_tests/` | Testprotokolle ohne ROM-Inhalte | spaetere Smoke-Tests dokumentieren |

## Nicht-mutierende Linux-Prüfbefehle

```sh
command -v git && git --version
command -v gh && gh --version
gh auth status
printf '%s\n' "$SHELL"
command -v java && java -version
command -v make && make --version
command -v arm-none-eabi-gcc && arm-none-eabi-gcc --version
command -v agbcc || true
command -v pwsh && pwsh -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'
```

## Historischer Windows-Stand

Die folgenden Befunde stammen aus der Windows-Inventur vor dem OS-Wechsel und dürfen nicht als Linux-Ist-Stand verwendet werden:

| Tool | Historischer Windows-Befund |
|---|---|
| Git | Git 2.54.0 unter `c:\\devkitPro\\msys2\\usr\\bin\\git.exe` |
| GitHub CLI (`gh`) | 2.92.0, authentifiziert, aber nicht im damaligen PowerShell-PATH |
| PowerShell | Windows PowerShell 5.1.26100.8328 |
| PowerShell 7 (`pwsh`) | 7.6.1 |
| Java | Temurin OpenJDK 25.0.3+9 LTS |
| `make` | GNU Make 4.4.1 unter devkitPro/MSYS2 |
| `arm-none-eabi-gcc` | nicht im damaligen PATH gefunden |
| `agbcc` | optional; nicht im damaligen PATH gefunden |

## Nicht committen

- ROMs
- Saves
- Emulator States
- Builds
- Tool-Binaries
- private `.env`-Dateien
- Secrets
- lokale absolute private Pfade

## Naechste Manifest-Aufgabe

Naechster empfohlener Branch nach Review/Merge von `planning/workspace-build-randomizer-integration`: `setup/devkitpro-toolchain-install-check`.

Ziel: devkitPro/devkitARM installieren oder den freigegebenen Installationsweg ausführen und rein read-only pruefen. Keine Builds und keine ROM-Zugriffe.

Vor dem ersten Clone pro externer Quelle weiterhin festlegen:

- ob nur gelesen, geklont oder geforkt wird
- welcher Branch relevant ist
- welcher Commit-Hash gepinnt wird
- ob Codex Änderungen durchführen darf

## 2026-05-13 - UPR-FVX Egg-Move scope/write pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`.
- UPR-FVX commit: `18168b78b973a4c39f34053ac58f21279a26d8d2`.
- Scope: gated CFRU/DPE Gen9 BPRE `gEggMoves` reader/writer plus high move-ID safety in Egg-Move randomization.

## 2026-05-13 - UPR-FVX Learnset-Write bounded pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`.
- UPR-FVX commit: `77de517da880bebb6ed690ca6e170e5bd10b9cad`.
- Scope: gated CFRU/DPE Gen9 BPRE `setMovesLearnt()` full repointing writer for `gLevelUpLearnsets`; no Move-Data-Write, no Tutor text/menu rewrite, no Special Tutors, no Egg-Move expansion.

## 2026-05-13 - UPR-FVX Encounter Held Items scope/write pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-encounter-held-items-scope-and-write`.
- UPR-FVX commit: `5c7170b654b09e1fc27ced6857dd50a8e4711f08`.
- Scope: gated CFRU/DPE Gen9 BPRE Item-Scope, modern Bad-/Banned-Item filters, and `gBaseStats` Encounter Held Item read/write/reload for `item1`/`item2`.

## 2026-05-13 - UPR-FVX Learnset GUI flow safety pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-learnset-gui-flow-safety`.
- UPR-FVX commit: `086d2a9177df7624a0e7ca1876b210a200d7aa98`.
- Scope: gated CFRU/DPE Gen9 BPRE Learnset GUI flow safety: Logger null-safety, repeated `setMovesLearnt()` FreeSpace allocation, Trainer-Movesets missing-map fallback and TM/HM-/Tutor-Level-Up-Sanity fallback; no Move-Data-Write, Tutor text/menu rewrite, Special Tutors, Egg-Move expansion, Palette/Graphics or Text/Menu paths.


## 2026-05-13 - UPR-FVX Learnset-Write repointing pin

- Workspace branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`.
- UPR-FVX branch: `compat/upr-fvx-cfru-dpe-learnset-write-repointing`.
- UPR-FVX commit: `77de517da880bebb6ed690ca6e170e5bd10b9cad`.
- Scope: gated CFRU/DPE Gen9 BPRE `setMovesLearnt()` full repointing writer for `gLevelUpLearnsets`; writes new blobs into validated FreeSpace, updates the existing pointertable by internal SpeciesSet ID, and leaves Move-Data-Write, Tutor text/menu rewrites, Special Tutors and Egg Moves out of scope.
