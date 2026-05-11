# DPE and CFRU Source Integration

## Datum

2026-05-11

## Zweck

DPE Gen9 und CFRU-expansion werden als änderbare Source-Repos fuer den spaeteren FireRed-Gen9-Build in den Workspace eingebunden.

## DPE Gen9

- Fork: Planton361/Dynamic-Pokemon-Expansion-Gen-9
- Upstream: Shiny-Miner/Dynamic-Pokemon-Expansion-Gen-9
- Lokaler Pfad: `02_external/Dynamic-Pokemon-Expansion-Gen-9`
- Branch: compat/firered-gen9-randomizer
- Commit: 5906aa4d4904e41393fd9184a16951c961e96263

## CFRU-expansion

- Fork: Planton361/CFRU-expansion
- Upstream: Shiny-Miner/CFRU-expansion
- Lokaler Pfad: `02_external/CFRU-expansion`
- Branch: compat/firered-gen9-randomizer
- Commit: 64e8adb13b00b0b675a1fbc0a08f02359682a7dc

## Build-Hinweise aus den Repos

- DPE Gen9 erwartet eine lokale `BPRE0.gba` im Projektordner und baut ueber `python scripts/make.py`.
- DPE erzeugt typischerweise `test.gba` und `offsets.ini`.
- DPE soll vor CFRU angewendet werden.
- CFRU-expansion wird danach separat geprueft und gebaut.

## Sicherheitsgrenzen

- devkitPro/devkitARM wird nur als Toolchain unter `/opt/devkitpro` genutzt.
- Kein devkitPro-Source-Code wird geändert.
- DPE/CFRU-Codeänderungen erfolgen nur in den Forks.
- ROMs bleiben lokal unter `04_private_roms/` oder als lokale Build-Kopie in externen Arbeitsordnern.
- Build-Ergebnisse bleiben lokal unter `05_builds/`.
- Keine ROMs, Builds oder Tool-Binaries werden committed.
