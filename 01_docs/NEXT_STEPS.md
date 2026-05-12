# Next Steps

## Aktueller Arbeitsblock

P1 Trainer Movesets Kombinationsdiagnosen fuer CFRU/DPE Gen9-BPRE.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations
```

UPR-FVX-Stand:

```text
655764816f9fefedb9433f33e4da0bc9d44bcda7
```

## Abschluss dieses Blocks

1. Workspace-Commit erstellen:

```text
test: document trainer movesets combination diagnostics
```

2. Workspace-PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations --title "test: document trainer movesets combination diagnostics" --body-file /tmp/pr-body-workspace-trainer-movesets-combinations.md
```

## Diagnosebefund 032

- UPR-FVX-Commit: `655764816f9fefedb9433f33e4da0bc9d44bcda7`.
- Seed: `274269061345323`.
- `moves.total=559`.
- Vor Randomization: `before.trainers=255`, `before.trainerPokemon=481`, `before.movesetEntries=53`, `before.invalidMoves=0`, `before.unknownNamedMoves=0`.
- Movesets-only: `saveSuccessful=true`, `logSuccessful=true`, `after/reload.movesetEntries=417`, `writeReloadMoveMismatches=0`.
- Movesets+Species: `after/reload.gen8plusSpecies=77`, `after/reload.gen9Species=38`, `writeReloadSpeciesMismatches=0`, `writeReloadMoveMismatches=0`.
- Movesets+Held Items normal: `after/reload.heldItemEntries=481`, `writeReloadHeldItemMismatches=0`, `writeReloadMoveMismatches=0`.
- Movesets+sensible Held Items: `after/reload.heldItemEntries=481`, `writeReloadHeldItemMismatches=0`, `writeReloadMoveMismatches=0`.
- Alle Laeufe: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `Bad Egg=false`, `<unknown>=false`, Unknown-Move-Marker `false`.
- Learnset-Write / `setMovesLearnt()` bleibt unveraendert.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-move-data-model
```

Ziel:

- Gen8/9-Move-Datenmodell gegen CFRU/DPE `MOVES_COUNT=992` read-only modellieren.
- TM-/Tutor-/Egg-Move-Tabellenpfade separat einordnen.
- Keine Learnset-Write-Ausweitung ohne eigenes Modell.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
