# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE Egg-Move-Species-/Move-ID-Modellierung.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-egg-move-model
```

UPR-FVX-Stand:

```text
4ce93754de390e9177efd2541c02edba0afbb0c4
```

## Abschluss dieses Blocks

1. Workspace-Commit erstellen:

```text
docs: document cfru dpe egg move model
```

2. PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-egg-move-model
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-egg-move-model --title "docs: document CFRU DPE egg move model" --body-file /tmp/pr-body-workspace-egg-move-model.md
```

## Analysebefund 041

- `gEggMoves` bleibt ein `u16`-Stream mit Species-Markern `species + 20000` und Terminator `0xFFFF`.
- DPE `repointall` dokumentiert `gEggMoves 08045C50`; FVX nutzt aktuell fuer FireRed-BPRE noch `EggMoves=0x25EF0C`.
- Der DPE-Stream enthaelt `437` Species-Eintraege, darunter Gen8-/PLA-/Paldea-Species.
- Hoechste Species im Stream: `SPECIES_WOOPER_P`, ID `0x584` / `1412`.
- Der Stream enthaelt Move-IDs bis `MOVE_TIDYUP`, ID `0x3C7` / `967`; damit sind Gen9-Moves enthalten und innerhalb `moves.total=992`.
- Egg-Move-only ist noch nicht P1-supported: Tabellenort, interne Species-ID-Abbildung, hohe Move-ID-Arraygrenzen und Kopplung an Learnset-Write brauchen einen separaten Fixbranch.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write
```

Ziel:

- Minimal gegateten CFRU/DPE-Egg-Move-Reader/Writer implementieren.
- `gEggMoves` ueber Pointer-Ort `0x45C50` lesen/schreiben, sofern Zielpointer sicher validiert ist.
- Species-Marker fuer CFRU/DPE ueber interne SpeciesSet-Identitaet erhalten, nicht ueber Pokédex-ID roundtrips.
- Hohe Move-ID-Arrayzugriffe im SpeciesMoveset-/Egg-Move-Pool defensiv absichern.
- Egg-Move-Write/Reload separat diagnostizieren; `setMovesLearnt()` bleibt out of scope.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine Learnset-Write-, Move-Data-Write-, Tutor-Text- oder Special-Tutor-Ausweitung ohne eigenen Branch

## After Egg-Move scope/write fix

- Merge UPR-FVX PR for `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`, then merge the workspace documentation PR.
- Next compatibility scopes remain separate: Learnset-Write, Move-Data-Write, Special Tutors, and Tutor text/menu rewrites.
- Recommended next branch after merge: model or diagnose CFRU/DPE Learnset-Write separately before any write-path implementation.
