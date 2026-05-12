# Next Steps

## Aktueller Arbeitsblock

TM/HM Scope-and-Safety-Fix fuer CFRU/DPE Gen9-BPRE.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety
```

UPR-FVX-Stand:

```text
32e43ac03a5762542773213a13be4e0389f1deae
```

## Abschluss dieses Blocks

1. UPR-FVX-PR erstellen:

```text
fix: guard cfru dpe tm hm randomization
```

2. Workspace-Commit erstellen:

```text
docs: record tm hm safety fix diagnostics
```

3. Workspace-PR erstellen:

```sh
git push -u origin compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety --title "docs: record tm hm safety fix diagnostics" --body-file /tmp/pr-body-workspace-tm-hm-safety.md
```

## Diagnosebefund 036

- `moves.total=992`, hoechster Move `PsychicNoise`, ID `991`.
- FVX erkennt im TM/HM-Pfad weiterhin `tmCount=50`, `hmCount=8`, `compat.flagLength=59`.
- TM moves + Compatibility, Compatibility-only und TM moves-only erzeugen jeweils Save, Log, Output-ROM und nichtleeren Log.
- Alle drei Laeufe reloaden mit `writeReloadTmHmMismatches=0` und `writeReloadCompatibilityMismatches=0`.
- `after.invalidTmHmMoves=0`, `reload.invalidTmHmMoves=0`.
- Kein `Bad Egg`, kein `<unknown>` und kein Unknown-Move-Marker im Log.
- TM/HM-only ist im klassischen FVX-`50+8`-Scope P1-supported.
- Das echte CFRU/DPE-128-Slot-TM/HM-Modell bleibt separat offen.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-tm-hm-128-slot-model
```

Ziel:

- Aktiven CFRU/DPE-128-Slot-TM/HM-Ort read-only nachweisen.
- Table-/Pointermodell, Slotanzahl, HM-Schutz und Write/Reload-Risiken dokumentieren.
- Kein Fix, keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine Tutor-, Egg-Move-, Learnset-Write-, Move-Data-Write- oder 128-Slot-TM/HM-Ausweitung ohne eigenen Branch
