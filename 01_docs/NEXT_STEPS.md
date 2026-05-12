# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE Move-Data-Reader-Fix fuer UPR-FVX.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-move-data-reader
```

UPR-FVX-Stand:

```text
c71fd75e67f5a839560bbf5de7c6f17317a64bd1
```

## Abschluss dieses Blocks

1. UPR-FVX-Commit pushen und PR erstellen:

```sh
git -C 02_external/upr-fvx push -u origin compat/upr-fvx-cfru-dpe-move-data-reader
gh pr create --repo Planton361/universal-pokemon-randomizer-fvx --base compat/firered-gen9-cfru-dpe --head compat/upr-fvx-cfru-dpe-move-data-reader --title "fix: read cfru dpe move data" --body-file /tmp/pr-body-upr-move-data-reader.md
```

2. Workspace-Commit erstellen:

```text
docs: record move data reader diagnostics
```

3. Workspace-PR erstellen:

```sh
git push -u origin compat/upr-fvx-cfru-dpe-move-data-reader
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head compat/upr-fvx-cfru-dpe-move-data-reader --title "docs: record move data reader diagnostics" --body-file /tmp/pr-body-workspace-move-data-reader.md
```

## Diagnosebefund 034

- UPR-FVX-Ausgangsstand: `655764816f9fefedb9433f33e4da0bc9d44bcda7`.
- UPR-FVX-Fixstand: `c71fd75e67f5a839560bbf5de7c6f17317a64bd1`.
- Vor Fix aus Diagnose 033: `moves.total=559`.
- Nach Fix: `moves.total=992`.
- Hoechster geladener Move: `moves.highestLoaded=991`, `moves.highestLoadedName=PsychicNoise`.
- Kategoriezaehlung aus `BattleMove.split`: `physical=420`, `special=301`, `status=270`.
- Trainer Movesets-only, Movesets+Species, Movesets+Held Items normal und Movesets+sensible Held Items speichern/loggen/reloaden erfolgreich.
- Alle vier Laeufe: `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadMoveMismatches=0`.
- Keine invaliden Moves, kein Bad Egg und kein `<unknown>` im Log.

## Naechster empfohlener Arbeitsblock nach Merge

Separater Analyse- oder Fixbranch fuer einen der verbleibenden Move-Pfade:

1. TM/HM-128-Slot-Read-/Write-Modell fuer CFRU/DPE.
2. Tutor-Bitfeld- und Special-Tutor-Modell fuer CFRU/DPE.
3. Egg-Move-Species-/Move-ID-Diagnose fuer CFRU/DPE.
4. Move-Data-Write/`saveMoves()` nur, falls Move-Data-Randomization explizit scoped wird.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine TM/HM-, Tutor-, Egg-Move- oder Learnset-Write-Ausweitung ohne eigenen Branch
