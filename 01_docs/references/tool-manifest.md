# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

## Sicherheitsstatus

Dieser Stand ist read-only. Es wurden keine externen Repos geklont, keine Forks angelegt und keine Tool-Binaries heruntergeladen.

Die lokale Toolchain-Inventur wurde im Arbeitsblock `setup/toolchain-local-inventory` dokumentiert und mit PR #11 gemerged. Lokale Windows-Checks wurden auf dem Branch ausgeführt; bestätigte Versionen und Pfade sind unten dokumentiert. Fehlende PATH-Einträge bleiben ausdrücklich offen.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | `C:\Users\anton\romhacking\fr-rando-gen9` | main | offen | ja, nur Branches | aktiv |
| Git | Versionierung | n/a | n/a | `c:\devkitPro\msys2\usr\bin\git.exe` | n/a | n/a | nein | lokal bestätigt: Git 2.54.0 |
| GitHub CLI (`gh`) | PRs und GitHub-Checks automatisieren | https://cli.github.com/ | n/a | `C:\Program Files\GitHub CLI\gh.exe`; nicht im aktuellen PATH | n/a | n/a | nein | lokal bestätigt: gh 2.92.0, authentifiziert |
| PowerShell | Terminal | n/a | n/a | `C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe` | n/a | n/a | nein | lokal bestätigt: Windows PowerShell 5.1.26100.8328 |
| PowerShell 7 (`pwsh`) | Script-Ausführung und Checks | https://github.com/PowerShell/PowerShell | n/a | `C:\Program Files\WindowsApps\Microsoft.PowerShell_7.6.1.0_x64__8wekyb3d8bbwe\pwsh.exe` | n/a | n/a | nein | lokal bestätigt: pwsh 7.6.1 |
| Java | Laufzeit für UPR FVX | https://adoptium.net/ oder lokale Distribution | n/a | `C:\Program Files\Eclipse Adoptium\jdk-25.0.3.9-hotspot\bin\java.exe` | n/a | n/a | nein | lokal bestätigt: Temurin OpenJDK 25.0.3+9 LTS |
| `make` | Build-Orchestrierung für spätere Toolchain-Schritte | n/a | n/a | `c:\devkitPro\msys2\usr\bin\make.exe` | n/a | n/a | nein | lokal bestätigt: GNU Make 4.4.1 |
| `arm-none-eabi-gcc` | GBA Cross-Compiler | ARM GNU Toolchain/devkitARM | n/a | PATH | n/a | n/a | nein | nicht im aktuellen PATH gefunden |
| `agbcc` | optionale GBA/pret-kompatible Compiler-Komponente | pret/devkitARM-Kontext | n/a | PATH oder lokaler Toolchain-Pfad | n/a | n/a | nein | optional; nicht im aktuellen PATH gefunden |
| Codex | Agent | OpenAI | n/a | offen | n/a | n/a | nur nach Branch-Freigabe | geprüft für Docs-Dry-Run |
| JetBrains IDE | IDE | JetBrains | n/a | lokal | n/a | n/a | nein | vorhanden |
| devkitPro/devkitARM | GBA Build Toolchain | devkitPro | n/a | offen | n/a | n/a | nein | offen |
| UPR FVX | Randomizer | https://github.com/upr-fvx/universal-pokemon-randomizer-fvx | offen | `02_external\upr-fvx` | offen | offen | nur nach Freigabe | read-only geprüft |
| CFRU-expansion | FireRed Gen9/CFRU-Basis | https://github.com/Shiny-Miner/CFRU-expansion | offen | `02_external\CFRU-expansion` | offen | offen | nur nach Freigabe | read-only geprüft |
| DPE Gen9 | Pokémon Expansion | https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | offen | `02_external\Dynamic-Pokemon-Expansion-Gen-9` | offen | offen | nur nach Freigabe | read-only geprüft |
| Skeli789 CFRU | Upstream CFRU-Referenz | https://github.com/Skeli789/Complete-Fire-Red-Upgrade | n/a | `02_external\Complete-Fire-Red-Upgrade` | offen | offen | nein, Referenz zuerst | read-only geprüft |
| Skeli789 DPE | Upstream DPE-Referenz | https://github.com/Skeli789/Dynamic-Pokemon-Expansion | n/a | `02_external\Dynamic-Pokemon-Expansion` | offen | offen | nein, Referenz zuerst | read-only geprüft |
| CyanSMP64 NatDexExtension | IronMON/NatDex-Referenz | https://github.com/CyanSMP64/NatDexExtension | offen | `02_external\NatDexExtension` | offen | offen | nur nach Freigabe | read-only geprüft |
| pret/pokefirered | FireRed Decomp-Referenz | https://github.com/pret/pokefirered | n/a | `02_external\pokefirered` | offen | offen | nein, Referenz zuerst | read-only geprüft |
| Hex Maniac Advance | ROM-Analyse | offen | n/a | `03_tools\releases` | n/a | n/a | nein | Quelle offen |
| BizHawk | Emulator | https://github.com/TASEmulators/BizHawk | n/a | `03_tools\releases` | n/a | n/a | nein | read-only geprüft |
| Ironmon Tracker | Tracker | https://github.com/besteon/Ironmon-Tracker | offen | `02_external\Ironmon-Tracker` | offen | offen | nur nach Freigabe | read-only geprüft |

## Lokale Toolchain-Inventur

Arbeitsblock: `setup/toolchain-local-inventory`

Zweck: Nur lokale Tool-Verfügbarkeit, Versionen und PATH-Erreichbarkeit dokumentieren. Keine ROMs, Saves, Builds, Tool-Binaries, externen Clones oder Forks anfassen.

| Prüfpukt | Status | Nachweisstand | Nächster Schritt |
|---|---|---|---|
| PowerShell | lokal bestätigt | `C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe`; 5.1.26100.8328 | keine |
| Git | lokal bestätigt | `c:\devkitPro\msys2\usr\bin\git.exe`; Git 2.54.0 | keine |
| GitHub CLI (`gh`) | lokal bestätigt, aber nicht im aktuellen PATH | `gh` im PATH fehlt; `C:\Program Files\GitHub CLI\gh.exe` meldet 2.92.0 und ist authentifiziert | Windows Terminal neu öffnen oder PATH in PowerShell neu laden |
| Java | lokal bestätigt | `C:\Program Files\Eclipse Adoptium\jdk-25.0.3.9-hotspot\bin\java.exe`; Temurin OpenJDK 25.0.3+9 LTS | keine |
| `make` | lokal bestätigt | `c:\devkitPro\msys2\usr\bin\make.exe`; GNU Make 4.4.1 | keine |
| `arm-none-eabi-gcc` | nicht im aktuellen PATH gefunden | `Get-Command arm-none-eabi-gcc` und Inventurscript ohne Treffer | devkitARM PATH später gezielt klären, ohne Build zu starten |
| `agbcc` | optional; nicht im aktuellen PATH gefunden | Inventurscript ohne Treffer | nur bei Bedarf später klären |
| `pwsh` | lokal bestätigt | `C:\Program Files\WindowsApps\Microsoft.PowerShell_7.6.1.0_x64__8wekyb3d8bbwe\pwsh.exe`; 7.6.1 | keine |

### PowerShell-Prüfbefehle für lokale Inventur

```powershell
$ToolChecks = @(
  @{ Name = 'PowerShell'; Command = 'powershell.exe'; Args = @('-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()') },
  @{ Name = 'Git'; Command = 'git'; Args = @('--version') },
  @{ Name = 'GitHub CLI'; Command = 'gh'; Args = @('--version') },
  @{ Name = 'Java'; Command = 'java'; Args = @('-version') },
  @{ Name = 'make'; Command = 'make'; Args = @('--version') },
  @{ Name = 'arm-none-eabi-gcc'; Command = 'arm-none-eabi-gcc'; Args = @('--version') },
  @{ Name = 'agbcc'; Command = 'agbcc'; Args = @('--version') },
  @{ Name = 'pwsh'; Command = 'pwsh'; Args = @('-NoProfile', '-Command', '$PSVersionTable.PSVersion.ToString()') }
)

foreach ($Tool in $ToolChecks) {
  $Resolved = Get-Command $Tool.Command -ErrorAction SilentlyContinue
  if ($Resolved) {
    Write-Host "FOUND: $($Tool.Name) -> $($Resolved.Source)"
    & $Tool.Command @($Tool.Args) 2>&1 | Select-Object -First 3
  }
  else {
    Write-Host "MISSING: $($Tool.Name)"
  }
  Write-Host ''
}
```

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

## Windows-Hinweis

Nach Installation von GitHub CLI muss Windows Terminal neu geöffnet werden. Alternativ muss der PATH in der laufenden PowerShell neu geladen werden, bevor `gh` verfügbar ist.

## PATH-Folgeklärung

Arbeitsblock: `setup/path-toolchain-followup`

Zweck: Nur dokumentieren, welche PATH- oder Umgebungsvariablen-Fragen nach der lokalen Inventur offen sind. Keine PATH-Änderungen, Installationen, Builds, ROM-Zugriffe, Tool-Binary-Downloads, externen Clones oder Forks durchführen.

| Punkt | Aktueller Nachweis | Folgeklärung |
|---|---|---|
| GitHub CLI (`gh`) | `C:\Program Files\GitHub CLI\gh.exe` ist vorhanden, Version 2.92.0, authentifiziert; `gh` war im aktuellen PATH nicht auflösbar | Windows Terminal neu öffnen oder PATH in PowerShell neu laden; danach `gh --version` und `gh auth status` erneut dokumentieren |
| `arm-none-eabi-gcc` | `Get-Command arm-none-eabi-gcc` und Inventurscript ohne Treffer | Prüfen, ob devkitARM installiert ist und ob `C:\devkitPro\devkitARM\bin` oder ein äquivalenter Toolchain-Pfad im PATH fehlt |
| `agbcc` | optional; Inventurscript ohne Treffer | Erst klären, falls eine konkrete Build-Basis agbcc verlangt; vorher keine Installation oder Tool-Binary-Arbeit |

### Nicht-mutierende Prüfbefehle

Diese Befehle dürfen in einem späteren lokalen Prüfblock verwendet werden, weil sie nur lesen:

```powershell
Get-Command gh -ErrorAction SilentlyContinue
& 'C:\Program Files\GitHub CLI\gh.exe' --version
& 'C:\Program Files\GitHub CLI\gh.exe' auth status
Get-ChildItem Env:DEVKITARM,Env:DEVKITPRO -ErrorAction SilentlyContinue
Get-Command arm-none-eabi-gcc -ErrorAction SilentlyContinue
Test-Path 'C:\devkitPro\devkitARM\bin\arm-none-eabi-gcc.exe'
Get-Command agbcc -ErrorAction SilentlyContinue
$env:Path -split ';' | Where-Object { $_ -match 'GitHub CLI|devkitPro|devkitARM|msys2' }
```
