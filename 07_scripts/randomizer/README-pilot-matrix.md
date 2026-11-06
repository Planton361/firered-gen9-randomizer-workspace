# #743 pilot settings matrix (USER-ONLY)

`firered_pilot_matrix.py` runs the eleven CFRU/DPE Gen 9 pilot cases (M00-M10)
through UPR-FVX's existing `settings-profile`, `cli` and `loaded-manifest`
commands. Real ROM runs happen only on the user's machine.

## Prerequisites

- An existing UPR-FVX JAR built from the pilot candidate. The runner never
  builds it. It stops if the UPR-FVX checkout is not the candidate or the JAR is
  older than the source. `--allow-revision-drift` is for development runs only.
- The source CFRU/DPE ROM.
- A neutral `.rnqs`, saved once from the UPR GUI: no randomizers, updaters, misc
  tweaks, Intro or evolution options; Movesets Unchanged. The runner reads its
  effective state through the Settings API and stops if it is not neutral or
  cannot be inspected.
- A new `--out` folder. Inside the Workspace only under `05_builds/` or
  `04_private_roms/`. Existing folders are never reused or overwritten.

## Usage (fish)

```fish
python3 07_scripts/randomizer/firered_pilot_matrix.py --plan
python3 07_scripts/randomizer/firered_pilot_matrix.py --self-test
python3 07_scripts/randomizer/firered_pilot_matrix.py --matrix --confirm USER_LOCAL_RUN \
    --rom 04_private_roms/SOURCE.gba --baseline 04_private_roms/NEUTRAL.rnqs \
    --out 05_builds/pilot-matrix-(date +%Y%m%d-%H%M%S)
```

Every case gets its own folder with `output.gba`, `loaded-manifest/` and the
raw UPR logs (`cli.log`, ...). The printed table contains only categories:
`PASS`, `FAIL`, `EXPECTED_REJECTION`, `NOT_RUN`. The run stops at the first
unexpected failure. M08/M09 count as `EXPECTED_REJECTION` only for the exact
CFRU/DPE learnset guard with no output written. M10 must be byte-identical to
M07. Do not paste local logs, paths or manifests into GitHub.

A `MATRIX=PASS` covers generation, reopen and replay only. It says nothing
about boot, gameplay or learnset preservation.
