# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE TM/HM-128-Slot-Modell read-only.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model
```

UPR-FVX-Stand:

```text
32e43ac03a5762542773213a13be4e0389f1deae
```

## Abschluss dieses Blocks

1. Workspace-Commit erstellen:

```text
docs: document tm hm 128 slot model
```

2. Workspace-PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model --title "docs: document tm hm 128 slot model" --body-file /tmp/pr-body-workspace-tm-hm-128-slot.md
```

## Analysebefund 037

- CFRU/DPE nutzt `EXPANDED_TMSHMS` mit `NUM_TMS=120`, `NUM_HMS=8`, `NUM_TMSHMS=128`.
- `gTMHMMoves` ist `u16[128]` und wird ueber Pointer `0x8125A8C` angebunden.
- Slots `1..120` sind TMs; Slots `121..128` sind HMs.
- `gTMHMLearnsets` wird ueber Pointer `0x8043C68` angebunden und nutzt 128 Bits beziehungsweise 16 Bytes pro Species.
- FVX nutzt aktuell weiterhin den klassischen `50+8`-Pfad mit `romEntry.TmMoves=0x45a5a4` und `compat.flagLength=59`.
- Der Bereich nach 50+8 am klassischen FVX-Ort ist unplausibel, weil er nicht die aktive DPE-128-Slot-Tabelle ist.
- Ein minimaler 128-Slot-Fix ist plausibel, sollte aber separat und eng gegatet erfolgen.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
compat/upr-fvx-cfru-dpe-tm-hm-128-slot
```

Ziel:

- CFRU/DPE-128-Slot-TM/HM-Reader/Writer eng gaten.
- `gTMHMMoves` ueber Pointer `0x8125A8C` als `u16[128]` lesen.
- HM-Schutz slotbasiert fuer Slots `120..127` erhalten.
- Compatibility separat als 16 Bytes pro Species ueber Pointer `0x8043C68` lesen/schreiben oder in einem eigenen Folgebranch behandeln.
- Keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung ohne eigenen Branch
