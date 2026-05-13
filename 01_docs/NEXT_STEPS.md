# Next Steps

## Aktueller Arbeitsblock

CFRU/DPE Tutor-Scope-and-Compatibility-Fix.

Aktueller Workspace-Branch:

```text
compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility
```

UPR-FVX-Stand:

```text
4ce93754de390e9177efd2541c02edba0afbb0c4
```

## Abschluss dieses Blocks

1. UPR-FVX-Commit ist erstellt:

```text
fix: support cfru dpe tutor compatibility
```

2. Workspace-Commit erstellen:

```text
docs: record tutor compatibility diagnostics
```

3. PRs erstellen:

```sh
git -C 02_external/upr-fvx push -u origin compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility
gh pr create --repo Planton361/universal-pokemon-randomizer-fvx --base compat/firered-gen9-cfru-dpe --head compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility --title "compat: support CFRU DPE tutor compatibility" --body-file /tmp/pr-body-upr-tutor-compatibility.md

git push -u origin compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility
gh pr create --repo Planton361/firered-gen9-randomizer-workspace --base main --head compat/upr-fvx-cfru-dpe-tutor-scope-and-compatibility --title "docs: record tutor compatibility diagnostics" --body-file /tmp/pr-body-workspace-tutor-compatibility.md
```

## Diagnosebefund 040

- `moves.total=992`, hoechster Move `PsychicNoise` ID `991`.
- `tutorMoveCount=152`, letzter Tutor-Move `MOVE_TERABLAST` ID `966`, hoechste Tutor-Move-ID `969`.
- `gMoveTutorMoves` Pointer-Location `0x8120BE4`, Zielpointer `0x09A596EA`, ROM-Offset `0x1A596EA`.
- `gTutorLearnsets` Pointer-Location `0x8120C30`, Zielpointer `0x09605CD0`, ROM-Offset `0x1605CD0`.
- Nachgewiesener Compatibility-Stride: `19` Bytes pro Species.
- Compatibility flag length `153`, also 152 nutzbare Tutor-Flags plus Dummy-Index 0.
- Tutor moves-only: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadTutorMoveMismatches=0`.
- Tutor compatibility-only: `saveSuccessful=true`, `logSuccessful=true`, `writeReloadTutorCompatibilityMismatches=0`.
- Tutor moves + compatibility: `saveSuccessful=true`, `logSuccessful=true`, beide Write/Reload-Mismatch-Werte `0`.
- Keine invaliden Tutor-Move-IDs, kein `Bad Egg`, kein `<unknown>` und kein Unknown-Move-Marker im Log.

## Naechster empfohlener Arbeitsblock nach Merge

Branch:

```text
analysis/upr-fvx-cfru-dpe-p1-egg-move-model
```

Ziel:

- CFRU/DPE Egg-Move-Species-/Move-ID-Modell read-only untersuchen.
- Pruefen, ob FVX-Egg-Move-Streamformat fuer interne CFRU/DPE-Species und Move-IDs bis 991 stabil ist.
- Kein Fix im Analysebranch.
- Keine Learnset-Write- oder Move-Data-Write-Ausweitung.

## Nicht tun

- keine ROMs bewegen oder committen
- keine Saves oder Emulator States anfassen
- keine Builds, Randomizer-JARs oder Tool-Binaries committen
- keine privaten Pfade, Secrets, Tokens oder `.env` dokumentieren
- keine Original-Upstreams kontaktieren
- keine Aenderungen direkt auf `main`
- keine Special-Tutor-, Egg-Move-, Learnset-Write- oder Move-Data-Write-Ausweitung ohne eigenen Branch
