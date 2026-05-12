# Next Steps

## Aktueller Arbeitsblock

P1 TM/HM-only Diagnose fuer CFRU/DPE Gen9-BPRE.

Aktueller Workspace-Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-tm-hm-only
```

UPR-FVX-Stand:

```text
c71fd75e67f5a839560bbf5de7c6f17317a64bd1
```

## Abschluss dieses Blocks

1. Workspace-Commit erstellen:

```text
test: document tm hm only diagnosis
```

2. Workspace-PR erstellen:

```sh
git push -u origin analysis/upr-fvx-cfru-dpe-p1-tm-hm-only
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head analysis/upr-fvx-cfru-dpe-p1-tm-hm-only --title "test: document tm hm only diagnosis" --body-file /tmp/pr-body-workspace-tm-hm-only.md
```

## Diagnosebefund 035

- `moves.total=992`, `moves.highestLoaded=991`, `moves.highestLoadedName=PsychicNoise`.
- FVX erkennt im TM/HM-Pfad `tmCount=50`, `hmCount=8`.
- `getTMHMCompatibility()` liefert `flagLength=59`, nicht 128 Slots.
- Oeffentliche 50 TMs und 8 HMs sind gueltige Move-IDs.
- Rohe 128-Slot-Lesung ab FVX-`TmMoves` zeigt nach den klassischen 50 TMs und 8 HMs unplausible/invalid Daten.
- TM-Move-Randomization scheitert vor Save an `ArrayIndexOutOfBoundsException: Index 827 out of bounds for length 827`.
- TM/HM-Compatibility-only scheitert separat vor Save an `NullPointerException` wegen Species mit `null`-Primaertyp.
- Kein Output-ROM, kein nichtleeres Log, kein Reload-Vergleich.
- TM/HM-only ist nicht P1-supported.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
compat/upr-fvx-cfru-dpe-tm-hm-scope-and-safety
```

Ziel:

- TM-Move-Randomizer defensiv gegen hohe CFRU/DPE-Move-IDs absichern.
- TM/HM-Compatibility-Randomizer gegen Null-/Placeholder-Species absichern.
- CFRU/DPE-TM/HM-Scope eng gaten und klaeren, ob/wo das aktive 128-Slot-Modell im getesteten ROM liegt.
- Keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung im selben Branch.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung ohne eigenen Branch
