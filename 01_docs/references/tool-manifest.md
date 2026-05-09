# Tool Manifest

Dieses Manifest dokumentiert Tools, Repos, Forks, Versionen, Pfade und Sicherheitsstatus.

## Sicherheitsstatus

Dieser Stand ist read-only. Es wurden keine externen Repos geklont, keine Forks angelegt und keine Tool-Binaries heruntergeladen.

| Tool/Repo | Zweck | Upstream | Fork/Origin | Lokaler Pfad | Branch | Commit | Codex darf ändern | Status |
|---|---|---|---|---|---|---|---|---|
| Workspace Repo | Source of Truth | n/a | git@github.com:Planton361/firered-gen9-randomizer-workspace.git | `C:\Users\anton\romhacking\fr-rando-gen9` | main | offen | ja, nur Branches | aktiv |
| Git | Versionierung | n/a | n/a | PATH | n/a | n/a | nein | vorhanden |
| PowerShell | Terminal | n/a | n/a | Windows | n/a | n/a | nein | vorhanden |
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
