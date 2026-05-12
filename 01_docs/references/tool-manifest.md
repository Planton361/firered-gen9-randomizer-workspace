# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

## Sicherheitsstatus

Dieser Stand dokumentiert den read-only Setupblock `setup/intellij-mcp-readonly-check`. Es wurden keine Codeaenderungen vorgenommen, keine Builds gestartet, keine ROMs gelesen oder kopiert und keine Tool-Binaries oder Release-Assets angefasst.

Linux/CachyOS ist die primaere lokale Umgebung. Windows-Toolchain-Befunde bleiben historischer Referenzstand und duerfen nicht als Linux-Ist-Stand verwendet werden.

Der aktuelle Arbeitsblock dokumentiert, ob JetBrains MCP lokal optional fuer read-only Codex-Codebase-Analyse nutzbar waere.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | Workspace-Root | `docs/pin-upr-fvx-wild-special-species-fix` | offen | ja, nur Branches | aktiv |
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

## Lokale Submodule-Pins 2026-05-12

Arbeitsblock: `docs/pin-upr-fvx-wild-special-species-fix`.

| Repo | Zweck | Origin | Lokaler Pfad | Branch | Commit | Codex darf aendern | Status |
|---|---|---|---|---|---|---|---|
| UPR-FVX Fork | Haupt-Randomizer-Fork | `https://github.com/Planton361/universal-pokemon-randomizer-fvx.git` | `02_external/upr-fvx` | `compat/upr-fvx-cfru-dpe-wild-banned-special-species` | `0f127e9bb9a5c47306fe1f2af11e8e9fe1802717` | nein in diesem Block | gepinnter Planton361-Fork-Stand fuer CFRU/DPE-Wild-Sonder-Species-Fix |
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
| Arbeitsbranch | `compat/firered-gen9-cfru-dpe` |
| Gepinnter Workspace-Stand | `0f127e9bb9a5c47306fe1f2af11e8e9fe1802717` auf `compat/upr-fvx-cfru-dpe-wild-banned-special-species`; enthaelt den CFRU/DPE-Wild-Sonder-Species-Fix |
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
