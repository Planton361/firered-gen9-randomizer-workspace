# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

## Sicherheitsstatus

Dieser Stand ist read-only. Es wurden keine externen Repos geklont, keine Forks angelegt, keine Installationen durchgeführt und keine Tool-Binaries heruntergeladen.

Die bisherige lokale Toolchain-Inventur wurde auf Windows durchgeführt und ist ab dem OS-Wechsel nur noch historischer Referenzstand. Linux/CachyOS ist die neue primäre lokale Umgebung. Der folgende Linux-Stand wurde auf Branch `setup/linux-toolchain-inventory` read-only geprüft.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | `/home/anton/IdeaProjects/firered-gen9-randomizer-workspace` | `setup/linux-toolchain-inventory` | offen | ja, nur Branches | aktiv |
| Git | Versionierung | n/a | n/a | `/usr/bin/git` | n/a | n/a | nein | gefunden: 2.54.0 |
| GitHub CLI (`gh`) | PRs und GitHub-Checks automatisieren | https://cli.github.com/ | n/a | `/usr/bin/gh` | n/a | n/a | nein | gefunden: 2.92.0; Auth-Token ungueltig |
| POSIX Shell | Terminal-Standard | n/a | n/a | `/bin/fish` laut `$SHELL` | n/a | n/a | nein | primär |
| PowerShell 7 (`pwsh`) | optionale Script-Ausführung für bestehende Checks | https://github.com/PowerShell/PowerShell | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt/optional |
| Java | Laufzeit für UPR FVX | https://adoptium.net/ oder Distribution-Paket | n/a | `/usr/bin/java` | n/a | n/a | nein | gefunden: OpenJDK 26.0.1 |
| `make` | Build-Orchestrierung für spätere Toolchain-Schritte | n/a | n/a | `/usr/bin/make` | n/a | n/a | nein | gefunden: GNU Make 4.4.1 |
| devkitPro/devkitARM | GBA Build Toolchain | devkitPro | n/a | Linux-Pfad offen | n/a | n/a | nein | nicht nachgewiesen |
| `arm-none-eabi-gcc` | GBA Cross-Compiler | ARM GNU Toolchain/devkitARM | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt |
| `agbcc` | optionale GBA/pret-kompatible Compiler-Komponente | pret/devkitARM-Kontext | n/a | nicht im PATH gefunden | n/a | n/a | nein | fehlt/optional |
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

Arbeitsblock: `setup/linux-toolchain-inventory`.

Zweck: Nur lokale Tool-Verfügbarkeit, Versionen und PATH-Erreichbarkeit auf Linux dokumentieren. Keine ROMs, Saves, Builds, Tool-Binaries, externen Clones oder Forks anfassen.

| Prüfpunkt | Status | Nachweisstand | Nächster Schritt |
|---|---|---|---|
| Git | gefunden | `/usr/bin/git`; Git 2.54.0 | keine Aktion |
| GitHub CLI (`gh`) | gefunden, Auth offen | `/usr/bin/gh`; gh 2.92.0; `gh auth status` meldet ungueltigen gespeicherten Token fuer `Planton361` | auf Folgebranch neu authentifizieren |
| Shell | gefunden | `$SHELL` ist `/bin/fish` | POSIX-kompatible Projektbefehle weiter bevorzugen |
| Java | gefunden | `/usr/bin/java`; OpenJDK 26.0.1 | spaeter UPR-FVX-Anforderung gegen konkrete Version pruefen |
| `make` | gefunden | `/usr/bin/make`; GNU Make 4.4.1 | keine Aktion |
| devkitPro/devkitARM | offen | nicht installiert oder nicht nachgewiesen; keine Installation durchgefuehrt | separaten Toolchain-Setup-Block planen |
| `arm-none-eabi-gcc` | fehlt | nicht im PATH gefunden | spaeter devkitPro/devkitARM oder ARM-Toolchain klaeren |
| `agbcc` | fehlt/optional | nicht im PATH gefunden | nur bei konkretem pret-/Build-Bedarf klaeren |
| `pwsh` | fehlt/optional | nicht im PATH gefunden | PowerShell-Checks unter Linux nur nutzen, wenn `pwsh` separat bereitgestellt wird |

### Ergebnis 2026-05-10

- Gefunden: Git 2.54.0, GitHub CLI 2.92.0, fish als Login-/Standardshell, OpenJDK 26.0.1, GNU Make 4.4.1.
- Fehlend im PATH: `arm-none-eabi-gcc`, `agbcc`, `pwsh`.
- Offen: GitHub CLI ist installiert, aber der gespeicherte GitHub-Token ist ungueltig; devkitPro/devkitARM wurde nicht als installierte Toolchain nachgewiesen.
- Historisch: Windows-Toolchain-Befunde bleiben dokumentiert, gelten aber nicht als Linux/CachyOS-Ist-Stand.

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

Naechster empfohlener Branch: `setup/linux-gh-auth-refresh`.

Ziel: GitHub CLI auf Linux neu authentifizieren bzw. den ungueltigen gespeicherten Token bereinigen, ohne Tokens oder Secrets zu dokumentieren.

Vor dem ersten Clone pro externer Quelle weiterhin festlegen:

- ob nur gelesen, geklont oder geforkt wird
- welcher Branch relevant ist
- welcher Commit-Hash gepinnt wird
- ob Codex Änderungen durchführen darf
