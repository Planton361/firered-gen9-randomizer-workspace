# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

## Sicherheitsstatus

Dieser Stand ist read-only. Es wurden keine externen Repos geklont, keine Forks angelegt und keine Tool-Binaries heruntergeladen.

Die lokale Toolchain-Inventur wurde im Arbeitsblock `setup/toolchain-local-inventory` dokumentiert. Diese ChatGPT-/GitHub-Connector-Session konnte keine Befehle auf dem lokalen Windows-Workspace ausführen; daher sind frisch zu prüfende lokale Versionen und Pfade ausdrücklich als offen markiert.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | `C:\Users\anton\romhacking\fr-rando-gen9` | main | offen | ja, nur Branches | aktiv |
| Git | Versionierung | n/a | n/a | PATH | n/a | n/a | nein | dokumentiert vorhanden; lokal frisch zu prüfen |
| GitHub CLI (`gh`) | PRs und GitHub-Checks automatisieren | https://cli.github.com/ | n/a | PATH | n/a | n/a | nein | dokumentiert installiert und authentifiziert; PATH-Hinweis beachten |
| PowerShell | Terminal | n/a | n/a | Windows | n/a | n/a | nein | dokumentiert vorhanden |
| PowerShell 7 (`pwsh`) | Script-Ausführung und Checks | https://github.com/PowerShell/PowerShell | n/a | PATH | n/a | n/a | nein | offen: lokal prüfen |
| Java | Laufzeit für UPR FVX | https://adoptium.net/ oder lokale Distribution | n/a | PATH | n/a | n/a | nein | offen: lokal prüfen |
| `make` | Build-Orchestrierung für spätere Toolchain-Schritte | n/a | n/a | PATH | n/a | n/a | nein | offen: lokal prüfen |
| `arm-none-eabi-gcc` | GBA Cross-Compiler | ARM GNU Toolchain/devkitARM | n/a | PATH | n/a | n/a | nein | offen: lokal prüfen |
| `agbcc` | optionale GBA/pret-kompatible Compiler-Komponente | pret/devkitARM-Kontext | n/a | PATH oder lokaler Toolchain-Pfad | n/a | n/a | nein | optional; lokal prüfen, falls vorhanden |
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
| PowerShell | dokumentiert vorhanden | Standardterminal im Projekt | bei lokaler Prüfung `$PSVersionTable.PSVersion` notieren |
| Git | dokumentiert vorhanden | Projekt nutzt Git/GitHub-Workflow | `git --version` lokal ausführen |
| GitHub CLI (`gh`) | dokumentiert installiert/authentifiziert | PR #10 Handoff und Manifest-Hinweis | `gh --version` und `gh auth status` lokal ausführen; bei PATH-Problem neues Terminal nutzen |
| Java | offen | keine lokale Version dokumentiert | `java -version` lokal ausführen |
| `make` | offen | keine lokale Version dokumentiert | `make --version` lokal ausführen |
| `arm-none-eabi-gcc` | offen | keine lokale Version dokumentiert | `arm-none-eabi-gcc --version` lokal ausführen |
| `agbcc` | optional/offen | keine lokale Verfügbarkeit dokumentiert | `Get-Command agbcc -ErrorAction SilentlyContinue` lokal ausführen |
| `pwsh` | offen | Check-Script nutzt `pwsh`, lokale Verfügbarkeit nicht frisch dokumentiert | `pwsh -NoProfile -Command '$PSVersionTable.PSVersion'` lokal ausführen |

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
