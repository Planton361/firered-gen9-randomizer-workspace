# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE Learnset-Repointing-Modellierung.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model
```

UPR-FVX-Stand:

```text
dd9d80c16936a99bac1d7ef777b43baa7c2f029d
```

## Abschluss dieses Blocks

1. Workspace-Commit erstellen:

```text
docs: document cfru dpe learnset repointing model
```

2. PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model --title "docs: document CFRU DPE learnset repointing model" --body-file /tmp/pr-body-workspace-learnset-repointing-model.md
```

## Analysebefund 045

- `gLevelUpLearnsets` Pointer-Ort bleibt `0x03EA7C`; im getesteten Stand zeigt er auf `0x0825D7B4` / ROM-Offset `0x25D7B4`.
- Die bestehende Pointertable kann fuer `NUM_SPECIES=1440` rechnerisch `0x1680` Bytes umfassen.
- Quellenanalyse: `1408` Pointertable-Zuweisungen, `1104` eindeutige Learnset-Zielarrays, `148` Shared-Zielgruppen.
- Groesster Source-Learnset: `41` Eintraege / `126` Bytes inkl. Sentinel.
- Worst-case fuer Full Write unter `MAX_LEARNABLE_MOVES=50`: `220320` Bytes fuer `1440` Species ohne Sharing.
- DPE `OFFSET_TO_PUT=0x1600000` ist ein Insert-Ort fuer DPE-Code/-Daten, kein freier Randomizer-Append-Bereich.
- Ein spaeterer Full-Write-Fix muss freie ROM-Fläche entweder per FVX-FreeSpace-Mechanik oder per ROM-spezifischem Nachweis reservieren.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
compat/upr-fvx-cfru-dpe-learnset-write-repointing
```

Ziel:

- Full CFRU/DPE Learnset-Write mit Repointing nur dann implementieren, wenn der Fixbranch freie ROM-Fläche diagnostisch nachweist.
- Bestehende Pointertable bei `0x25D7B4` nutzen.
- Neue `u16 move + u8 level` Blobs schreiben und Pointertable-Eintraege pro interner Species-ID aktualisieren.
- Reload per interner SpeciesSet-Identitaet pruefen.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- kein Repointing in diesem Analysebranch
- keine Move-Data-Write-, Tutor-Text-, Special-Tutor- oder Egg-Move-Ausweitung ohne eigenen Branch
