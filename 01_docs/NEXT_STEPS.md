# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE Tutor-/Special-Tutor-Modellierung.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-tutor-model
```

UPR-FVX-Stand:

```text
58379ffd3146fcd6bb0eb416647cdf9b752cfc0e
```

## Abschluss dieses Blocks

1. Workspace-Commit erstellen:

```text
docs: document cfru dpe tutor model
```

2. PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-tutor-model
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-tutor-model --title "docs: document CFRU DPE tutor model" --body-file /tmp/pr-body-workspace-tutor-model.md
```

## Analysebefund 039

- `gMoveTutorMoves` ist eine CFRU/DPE-`u16`-Tabelle mit `152` Eintraegen.
- Pointer-Location fuer `gMoveTutorMoves`: `0x8120BE4`.
- Letzter sichtbarer Tutor-Move: `MOVE_TERABLAST`, ID `0x3C6` / `966`.
- `gTutorLearnsets` liegt laut `repointall` an Pointer-Location `0x8120C30`.
- Generierte DPE-Tutor-Compatibility zeigt `19` Bytes pro Species, passend zu `152` Bits.
- DPE Special Tutors sind als `Not in Table` markiert und duerfen nicht als normale Tutor-Slots behandelt werden.
- FVX nutzt aktuell fuer FireRed-BPRE im Tutor-Move-Pfad klassisch `MoveTutorMoves=15` und `MoveTutorData=0x459B60`.
- FVX ueberschreibt aktuell nur den Compatibility-Pointer auf `readPointer(0x120C30)`; Count und Move-Tabelle bleiben klassisch.
- Tutor-only ist daher noch nicht P1-supported.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility
```

Ziel:

- Minimal gegateten CFRU/DPE-Tutor-Reader/Writer implementieren.
- `gMoveTutorMoves` ueber `0x8120BE4` lesen/schreiben.
- `gTutorLearnsets` ueber `0x8120C30` mit nachgewiesenem 19- oder 20-Byte-Stride lesen/schreiben.
- Special Tutors nicht randomisieren, solange deren Sonderlogik nicht separat modelliert ist.
- Keine Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine Egg-Move-, Learnset-Write-, Move-Data-Write- oder Special-Tutor-Fixes ohne eigenen Branch
