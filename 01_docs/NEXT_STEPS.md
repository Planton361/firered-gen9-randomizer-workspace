# Next Steps

## Aktueller Arbeitsblock

P1 Move-Datenmodell fuer CFRU/DPE Gen9-BPRE.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-move-data-model
```

UPR-FVX-Stand:

```text
655764816f9fefedb9433f33e4da0bc9d44bcda7
```

## Abschluss dieses Blocks

1. Workspace-Commit erstellen:

```text
docs: document cfru dpe move data model
```

2. Workspace-PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-move-data-model
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-move-data-model --title "docs: document cfru dpe move data model" --body-file /tmp/pr-body-workspace-move-data-model.md
```

## Analysebefund 033

- UPR-FVX-Commit: `655764816f9fefedb9433f33e4da0bc9d44bcda7`.
- Ausgangspunkt aus Diagnose 032: `moves.total=559`.
- FVX-Gen3-BPRE-Hack-Support ermittelt `MoveCount` ueber Move-Description-Pointer, nicht ueber CFRU/DPE `MOVES_COUNT`.
- CFRU/DPE definiert `MOVES_COUNT = MOVE_PSYCHICNOISE + 1 = 0x3E0 = 992`.
- CFRU/DPE `BattleMove` bleibt 12 Bytes, enthaelt aber `z_move_power`, `split` und `z_move_effect`.
- FVX liest das `split`-Byte aktuell nicht und leitet Kategorie typbasiert wie Gen3 ab.
- TM/HM: DPE/CFRU nutzt 128 Slots und breitere Bitfelder; FVX erwartet aktuell `50+8`.
- Tutor: DPE/CFRU nutzt erweiterte Tutor-IDs/Bitfelder und Special-Tutor-Sonderlogik.
- Egg Moves: `u16`-Stream mit Species-Markern `species + 20000` und `0xFFFF`-Terminator bleibt formal kompatibel, braucht aber Move-ID-/Species-Grenzschutz.
- Learnset-Write / `setMovesLearnt()` bleibt unveraendert und ausserhalb des naechsten minimalen Move-Data-Fixpfads.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
compat/upr-fvx-cfru-dpe-move-data-reader
```

Ziel:

- Minimal gegateten CFRU/DPE-Move-Data-Reader fuer `Gen3RomHandler.loadMoves()` vorbereiten.
- `MOVES_COUNT=992` nur fuer sicher erkannte CFRU/DPE Gen9-BPRE-Hacks verwenden.
- CFRU/DPE-`split`-Byte als Move-Kategorie lesen.
- TM/HM-, Tutor-, Egg- und Learnset-Write-Pfade nicht im selben Fix ausweiten.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine Learnset-Write-Ausweitung im Move-Data-Fixbranch
