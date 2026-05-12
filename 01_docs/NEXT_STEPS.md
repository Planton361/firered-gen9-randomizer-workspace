# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE TM/HM-128-Slot-Fix.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-tm-hm-128-slot
```

UPR-FVX-Stand:

```text
58379ffd3146fcd6bb0eb416647cdf9b752cfc0e
```

## Abschluss dieses Blocks

1. UPR-FVX-Commit ist erstellt:

```text
fix: support cfru dpe tm hm 128 slots
```

2. Workspace-Commit erstellen:

```text
docs: record tm hm 128 slot diagnostics
```

3. PRs erstellen:

```sh
git -C 02_external/upr-fvx push -u origin compat/upr-fvx-cfru-dpe-tm-hm-128-slot
gh pr create --repo Planton361/universal-pokemon-randomizer-fvx --base compat/firered-gen9-cfru-dpe --head compat/upr-fvx-cfru-dpe-tm-hm-128-slot --title "compat: support CFRU DPE TM HM 128 slots" --body-file /tmp/pr-body-upr-tm-hm-128-slot.md

git push -u origin compat/upr-fvx-cfru-dpe-tm-hm-128-slot
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head compat/upr-fvx-cfru-dpe-tm-hm-128-slot --title "docs: record tm hm 128 slot diagnostics" --body-file /tmp/pr-body-workspace-tm-hm-128-slot.md
```

## Diagnosebefund 038

- `moves.total=992`, hoechster Move `PsychicNoise` ID `991`.
- `tmCount=120`, `hmCount=8`, total TM/HM slots `128`.
- `gTMHMMoves` Pointer-Location `0x8125A8C`, Zielpointer `0x09A5981A`, ROM-Offset `0x1A5981A`.
- `gTMHMLearnsets` Pointer-Location `0x8043C68`, Zielpointer `0x096002D0`, ROM-Offset `0x16002D0`.
- Compatibility flag length `129`, also 128 nutzbare TM/HM-Flags plus Dummy-Index 0.
- TM moves-only: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadTmHmMismatches=0`, HM-Slots unveraendert.
- TM/HM compatibility-only: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadCompatibilityMismatches=0`.
- TM moves + compatibility: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadTmHmMismatches=0`, `writeReloadCompatibilityMismatches=0`.
- Keine invaliden TM/HM-Move-IDs, kein `Bad Egg`, kein `<unknown>` und kein Unknown-Move-Marker im Log.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-tutor-model
```

Ziel:

- CFRU/DPE Tutor-/Special-Tutor-Tabellen read-only modellieren.
- Prüfen, ob Tutor-Moves eigene Pointer-, Slot- oder Bitfeldmodelle nutzen.
- Keine Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung.
- Kein Fix im Analysebranch.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung ohne eigenen Branch
