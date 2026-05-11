# UPR FVX Source Integration

## Datum

2026-05-11

## Zweck

Universal Pokemon Randomizer FVX wird als eigener Source-Code-Bestand fuer FireRed-Gen9-/CFRU-/DPE-Kompatibilitaetsarbeiten in den Workspace eingebunden.

## Architektur

- Workspace-Repo: Planton361/firered-gen9-randomizer-workspace
- UPR-FVX Fork: Planton361/universal-pokemon-randomizer-fvx
- Upstream: upr-fvx/universal-pokemon-randomizer-fvx
- Lokaler Pfad: `02_external/upr-fvx`
- Einbindung: Git-Submodule
- Randomizer-Arbeitsbranch: `compat/firered-gen9-cfru-dpe`

## Gepinnter Stand

```text
origin	https://github.com/Planton361/universal-pokemon-randomizer-fvx.git (fetch)
origin	https://github.com/Planton361/universal-pokemon-randomizer-fvx.git (push)
upstream	https://github.com/upr-fvx/universal-pokemon-randomizer-fvx.git (fetch)
upstream	DISABLED (push)
Branch: compat/firered-gen9-cfru-dpe
Commit: e0788edc6529c2605f201996e4807ff30165354c
```

## Sicherheitsgrenzen

- Keine ROMs im Randomizer-Repo.
- Keine ROMs im Workspace-Repo.
- Keine Tool-Binaries im Workspace-Repo.
- Gebaute JARs bleiben lokal in `03_tools/releases/` oder in ignored Build-Ausgaben.
- Randomizer-Code-Aenderungen erfolgen im UPR-FVX-Fork, nicht direkt im Upstream.
