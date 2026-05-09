# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | `C:\Users\anton\romhacking\fr-rando-gen9` | main | offen | ja, nur Branches | aktiv |
| Git | Versionierung | n/a | n/a | PATH | n/a | n/a | nein | vorhanden |
| PowerShell | Terminal | n/a | n/a | Windows | n/a | n/a | nein | vorhanden |
| Codex | Agent | OpenAI | n/a | offen | n/a | n/a | n/a | offen |
| JetBrains IDE | IDE | JetBrains | n/a | offen | n/a | n/a | n/a | offen |
| devkitPro/devkitARM | GBA Build Toolchain | devkitPro | n/a | offen | n/a | n/a | nein | offen |
| UPR FVX | Randomizer | https://github.com/upr-fvx/universal-pokemon-randomizer-fvx | offen | `02_external\upr-fvx` | offen | offen | nur nach Freigabe | offen |
| CFRU-expansion | FireRed Gen9/CFRU-Basis | https://github.com/Shiny-Miner/CFRU-expansion | offen | `02_external\CFRU-expansion` | offen | offen | nur nach Freigabe | offen |
| DPE Gen9 | Pokémon Expansion | https://github.com/Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9 | offen | `02_external\Dynamic-Pokemon-Expansion-Gen-9` | offen | offen | nur nach Freigabe | offen |
| Hex Maniac Advance | ROM-Analyse | offen | n/a | `03_tools\releases` | n/a | n/a | nein | offen |
| BizHawk | Emulator | offen | n/a | `03_tools\releases` | n/a | n/a | nein | offen |
| Ironmon Tracker | Tracker | offen | offen | `02_external\Ironmon-Tracker` | offen | offen | nur nach Freigabe | offen |

## Sicherheitsregel

Nicht committen:

- ROMs
- Saves
- Emulator States
- Builds
- Tool-Binaries
- private `.env`-Dateien
- Secrets
