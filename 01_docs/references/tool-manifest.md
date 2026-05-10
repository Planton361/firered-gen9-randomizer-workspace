# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

## Sicherheitsstatus

Dieser Stand ist read-only. Es wurden keine externen Repos geklont, keine Forks angelegt und keine Tool-Binaries heruntergeladen.

Die bisherige lokale Toolchain-Inventur wurde auf Windows durchgeführt und ist ab dem OS-Wechsel nur noch historischer Referenzstand. Linux/CachyOS ist die neue primäre lokale Umgebung. Linux-Pfade, Versionen und PATH-Erreichbarkeit müssen in einem eigenen Folgeblock neu geprüft werden.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | Linux-Pfad offen, neu zu prüfen | main | offen | ja, nur Branches | aktiv |
| Git | Versionierung | n/a | n/a | Linux PATH, neu zu prüfen | n/a | n/a | nein | offen für Linux-Inventur |
| GitHub CLI (`gh`) | PRs und GitHub-Checks automatisieren | https://cli.github.com/ | n/a | Linux PATH, neu zu prüfen | n/a | n/a | nein | offen für Linux-Inventur |
| POSIX Shell | Terminal-Standard | n/a | n/a | Linux/CachyOS | n/a | n/a | nein | primär |
| PowerShell 7 (`pwsh`) | optionale Script-Ausführung für bestehende Checks | https://github.com/PowerShell/PowerShell | n/a | Linux PATH, optional neu zu prüfen | n/a | n/a | nein | optional |
| Java | Laufzeit für UPR FVX | https://adoptium.net/ oder Distribution-Paket | n/a | Linux PATH, neu zu prüfen | n/a | n/a | nein | offen für Linux-Inventur |
| `make` | Build-Orchestrierung für spätere Toolchain-Schritte | n/a | n/a | Linux PATH, neu zu prüfen | n/a | n/a | nein | offen für Linux-Inventur |
| devkitPro/devkitARM | GBA Build Toolchain | devkitPro | n/a | Linux-Pfad offen | n/a | n/a | nein | offen für Linux-Inventur |
| `arm-none-eabi-gcc` | GBA Cross-Compiler | ARM GNU Toolchain/devkitARM | n/a | Linux PATH, neu zu prüfen | n/a | n/a | nein | offen für Linux-Inventur |
| `agbcc` | optionale GBA/pret-kompatible Compiler-Komponente | pret/devkitARM-Kontext | n/a | Linux PATH oder lokaler Toolchain-Pfad, neu zu prüfen | n/a | n/a | nein | optional |
| Codex | Agent | OpenAI | n/a | offen | n/a | n/a | nur nach Branch-Freigabe | geprüft für Docs-Dry-Run |
| JetBrains IDE | IDE | JetBrains | n/a | lokal | n/a | n/a | nein | auf Linux neu zu prüfen |
| UPR FVX | Randomizer | https://github.com/upr-fvx/universal-pokemon-randomizer-fvx | offen | `02_external/upr-fvx` | offen | offen | nur nach Freigabe | read-only geprüft, nicht geklont |
| CFRU-expansion | FireRed Gen9/CFRU-Basis | https://github.com/Shiny-Miner/CFRU-expansion | offen | `02_external/CFRU-expansion` | offen | offen | nur nach Freigabe | read-only geprüft, nicht geklont |
| DPE Gen9 | Pokémon Expansion | https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | offen | `02_external/Dynamic-Pokemon-Expansion-Gen-9` | offen | offen | nur nach Freigabe | read-only geprüft, nicht geklont |
| Skeli789 CFRU | Upstream CFRU-Referenz | https://github.com/Skeli789/Complete-Fire-Red-Upgrade | n/a | `02_external/Complete-Fire-Red-Upgrade` | offen | offen | nein, Referenz zuerst | read-only geprüft, nicht geklont |
| Skeli789 DPE | Upstream DPE-Referenz | https://github.com/Skeli789/Dynamic-Pokemon-Expansion | n/a | `02_external/Dynamic-Pokemon-Expansion` | offen | offen | nein, Referenz zuerst | read-only geprüft, nicht geklont |
| CyanSMP64 NatDexExtension | IronMON/NatDex-Referenz | https://github.com/CyanSMP64/NatDexExtension | offen | `02_external/NatDexExtension` | offen | offen | nur nach Freigabe | read-only geprüft, nicht geklont |
| pret/pokefirered | FireRed Decomp-Referenz | https://github.com/pret/pokefirered | n/a | `02_external/pokefirered` | offen | offen | nein, Referenz zuerst | read-only geprüft, nicht geklont |
| Hex Maniac Advance | ROM-Analyse | offen | n/a | `03_tools/releases` | n/a | n/a | nein | Quelle offen; Tool-Binary nicht committen |
| BizHawk | Emulator | https://github.com/TASEmulators/BizHawk | n/a | `03_tools/releases` | n/a | n/a | nein | read-only geprüft; Tool-Binary nicht committen |
| Ironmon Tracker | Tracker | https://github.com/besteon/Ironmon-Tracker | offen | `02_external/Ironmon-Tracker` | offen | offen | nur nach Freigabe | read-only geprüft, nicht geklont |

## Linux/CachyOS-Inventur

Arbeitsblock: nächster Branch nach `setup/linux-workspace-migration`.

Zweck: Nur lokale Tool-Verfügbarkeit, Versionen und PATH-Erreichbarkeit auf Linux dokumentieren. Keine ROMs, Saves, Builds, Tool-Binaries, externen Clones oder Forks anfassen.

| Prüfpunkt | Status | Nachweisstand | Nächster Schritt |
|---|---|---|---|
| Git | offen | noch nicht auf Linux geprüft | `git --version` dokumentieren |
| GitHub CLI (`gh`) | offen | noch nicht auf Linux geprüft | `gh --version` und `gh auth status` dokumentieren |
| Shell | offen | Linux/CachyOS als primäre Umgebung gesetzt | verwendete Shell dokumentieren |
| Java | offen | noch nicht auf Linux geprüft | `java -version` dokumentieren |
| `make` | offen | noch nicht auf Linux geprüft | `make --version` dokumentieren |
| devkitPro/devkitARM | offen | noch nicht auf Linux geprüft | Installations-/PATH-Status nur dokumentieren |
| `arm-none-eabi-gcc` | offen | noch nicht auf Linux geprüft | `command -v arm-none-eabi-gcc` und Version prüfen |
| `agbcc` | optional | noch nicht auf Linux geprüft | nur bei konkretem Bedarf prüfen |
| `pwsh` | optional | noch nicht auf Linux geprüft | nur prüfen, falls bestehende PowerShell-Checks weiter genutzt werden sollen |

### Nicht-mutierende Linux-Prüfbefehle

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

## Nächste Manifest-Aufgabe

Vor dem ersten Clone pro externer Quelle festlegen:

- ob nur gelesen, geklont oder geforkt wird
- welcher Branch relevant ist
- welcher Commit-Hash gepinnt wird
- ob Codex Änderungen durchführen darf
