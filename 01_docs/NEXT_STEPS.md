# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE Learnset-Write bounded in-place Fix.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-learnset-write-bounded
```

UPR-FVX-Stand:

```text
dd9d80c16936a99bac1d7ef777b43baa7c2f029d
```

## Abschluss dieses Blocks

1. UPR-FVX-Commit ist erstellt:

```text
fix: support bounded cfru dpe learnset writes
```

2. Workspace-Commit erstellen:

```text
docs: record bounded learnset write diagnostics
```

3. PRs erstellen:

```sh
git -C 02_external/upr-fvx push -u origin compat/upr-fvx-cfru-dpe-learnset-write-bounded
gh pr create --repo Planton361/universal-pokemon-randomizer-fvx --base compat/firered-gen9-cfru-dpe --head compat/upr-fvx-cfru-dpe-learnset-write-bounded --title "compat: support bounded CFRU DPE learnset writes" --body-file /tmp/pr-body-upr-learnset-write-bounded.md

git push -u origin compat/upr-fvx-cfru-dpe-learnset-write-bounded
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head compat/upr-fvx-cfru-dpe-learnset-write-bounded --title "docs: record bounded learnset write diagnostics" --body-file /tmp/pr-body-workspace-learnset-write-bounded.md
```

## Diagnosebefund 044

- `moves.total=992`; hoechster geladener Move ist `991:PsychicNoise`.
- `gLevelUpLearnsets` wird ueber Pointer-Ort `0x03EA7C` validiert; Zielpointer im Test: `0x0825D7B4`, ROM-Offset `0x25D7B4`.
- Der CFRU/DPE-Writer schreibt `u16 move + u8 level` bis Sentinel `{0, 0xFF}`.
- Bounded in-place Write wird nur ausgefuehrt, wenn `newEntryCount <= originalEntryCount`.
- Kein Repointing: Growth wird als `needsRepoint` / `skippedGrowth` gezaehlt und nicht geschrieben.
- Writer-Diagnose im Test: `boundedWrites=1`, `skippedGrowth=0`, `needsRepoint=0`, `skippedSharedPointer=0`, `skippedPlaceholderSpecies=1`, `skippedInvalidPointer=1412`, `skippedInvalidMoves=0`.
- Diagnose-Harness bestaetigt `saveSuccessful=true`, `logSuccessful=true`, `outputRomExists=true`, `logNonEmpty=true`, `writeReloadLearnsetMismatches=0`.
- Gesamtbewertung: bounded Writer ist sicher und stabil, aber voller Learnset-Write ist noch nicht P1-supported. Ein Repointing-/Tabellenmodell bleibt separat.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-learnset-repointing-model
```

Ziel:

- Repointing- und Speicherbereichsmodell fuer full CFRU/DPE Learnset-Write read-only klaeren.
- Shared-Pointer-Policy, freie ROM-Bereiche, Pointertable-Update und Reload-Verhalten dokumentieren.
- Keine Umsetzung, solange das Repointing-Modell nicht sicher nachgewiesen ist.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- kein Repointing in diesem Branch
- keine Move-Data-Write-, Tutor-Text-, Special-Tutor- oder Egg-Move-Ausweitung ohne eigenen Branch
