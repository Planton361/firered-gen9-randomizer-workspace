# Next Steps

## Aktueller Arbeitsblock

P1 Trainer Movesets Learnsets-Fix fuer CFRU/DPE Gen9-BPRE.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets
```

UPR-FVX-Stand:

```text
655764816f9fefedb9433f33e4da0bc9d44bcda7
```

## Abschluss dieses Blocks

1. UPR-FVX-PR erstellen:

```sh
git -C 02_external/upr-fvx push -u origin compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets
gh pr create --repo Planton361/universal-pokemon-randomizer-fvx --base compat/firered-gen9-cfru-dpe --head compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets --title "fix: read cfru dpe level up learnsets" --body-file /tmp/pr-body-upr-learnsets.md
```

2. Workspace-Commit erstellen:

```text
docs: record trainer movesets learnsets fix diagnostics
```

3. Workspace-PR erstellen:

```sh
git push -u origin compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head compat/upr-fvx-cfru-dpe-trainer-movesets-learnsets --title "docs: record trainer movesets learnsets fix diagnostics" --body-file /tmp/pr-body-workspace-learnsets.md
```

## Diagnosebefund 031

- UPR-FVX-Commit: `655764816f9fefedb9433f33e4da0bc9d44bcda7`.
- Seed: `274269061345323`.
- `moves.total=559`.
- Vor Randomization: `before.trainers=255`, `before.trainerPokemon=481`, `before.movesetEntries=53`, `before.invalidMoves=0`.
- Ergebnis: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`.
- Log: `Bad Egg=false`, `<unknown>=false`, Unknown-Move-Marker `false`.
- Nach Randomization: `after.movesetEntries=417`, `after.invalidMoves=0`, `beforeAfterMoveSignatureChanges=418`.
- Reload: `reload.movesetEntries=417`, `reload.invalidMoves=0`, `writeReloadMismatches=0`.
- Learnset-Write / `setMovesLearnt()` bleibt unveraendert.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-trainer-movesets-combinations
```

Ziel:

- Trainer Movesets-only als P1-supported Baseline in Kombinationslaeufen nutzen.
- Offene Risiken separat pruefen: Gen8/9-Move-Datenmodell, TM/Tutor/Egg-Move-Tabellen, sensible movebasierte Trainer-Held-Item-Auswahl.
- Keine Learnset-Write-Ausweitung ohne eigenes Modell.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
