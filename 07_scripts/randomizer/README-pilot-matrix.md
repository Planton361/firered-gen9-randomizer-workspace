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

## #748 single options

`--single --select ID[,ID]` (or `all`) runs the single options S01-S05 listed by
`--plan`, with the same prerequisites and `--confirm USER_LOCAL_RUN`. `--matrix`
is unchanged and never runs them.

```fish
python3 07_scripts/randomizer/firered_pilot_matrix.py --single --confirm USER_LOCAL_RUN \
    --select FVX-TRAIT-001,FVX-TM-001,FVX-ITEM-002,FVX-TYPE-001 \
    --rom 04_private_roms/SOURCE.gba --baseline 04_private_roms/NEUTRAL.rnqs \
    --out 05_builds/single-(date +%Y%m%d-%H%M%S)
```

Before any ROM is generated, every case's settings must equal the baseline plus
its declared change, and must still do so after UPR's `tweakForRom` for the
source ROM. A case `tweakForRom` changes is `NEEDS_REVIEW` and is not generated.
Each remaining case is generated, reopened, exported and replayed byte for
byte. The best result is `GENERATION/REOPEN PASS`. The feature itself is not
verified.

To add an option, add a `SINGLE_OPTIONS` entry whose `source` is the exact
overlay lambda; the source-backing test checks it.

## #750 comprehensive matrix

`--plan` lists every current `settings-profile` ID and every ID in the
historical 132-feature ledger as `RUNNABLE`, `GUARDED`, `UNSUPPORTED`,
`NEEDS_REVIEW` or `NOT_RUN`, each with its reason. Historical ledger results are
not current acceptance. The expected Settings change of each overlay is read
from the UPR-FVX source at the pinned revision; if that source changes,
everything becomes `NEEDS_REVIEW` and `--suite` stops. Sub-options run together
with their parent toggles. High-risk options whose own CFRU/DPE repair contract
is still open (`PREREQUISITES`) are `NEEDS_REVIEW`, citing the issue, even when
their source would run. This covers TRAIT-024/027, ITEM-010 and GFX-001 to
GFX-004. Overlays whose value does not survive the `.rnqs` round trip at this
revision (`SERIALIZATION_DEFECTS`) are `NEEDS_REVIEW` too. FVX-WILD-007 sets
catch-rate level 45, which reads back as 5; see #752. Overlays that set a
value `tweakForRom` resets for every CFRU/DPE pilot ROM (`TARGET_NORMALIZED`)
are `NEEDS_REVIEW` as ineffective on the pilot target. That covers Limit
Pokemon (FVX-GEN-001, `setGenLimit` modes, and Allow Regional Forms through its
parent), because the CFRU/DPE ROM fails the vanilla CRC32 `isRomValid` check.
It also covers time-based encounters (FVX-SPECIAL-WILD-001), because the Gen 3
handler has no time-based encounters. A reset that applies to one value only is
listed in `TARGET_NORMALIZED_VALUES`, together with its exact source condition.
`MODE-FOE-MAIN-PLAYTHROUGH` is reset to RANDOM outside Gen 5, so it is
`NEEDS_REVIEW`. The other trainer modes stay runnable. None of these kinds is ever part of a
runnable single or composite. GEN_SAFE and SPECIAL_WILD combinations are
therefore `NEEDS_REVIEW` until a component release makes them effective.

It then plans single, pair (66 family pairs), triple (the 12 #681 triples) and
profile cases from `upr_generation_matrix.py`'s definitions. Cases that are
guarded, unsupported, unclear or contradictory are excluded with a reason.
A member that contradicts earlier ones is left out visibly. A pair, triple or
profile that keeps no effective change for one of its named families is
`NEEDS_REVIEW`. Cases with identical effective settings run once (`DUPLICATE`).

`--suite` runs one bounded batch (at most 25 cases), chosen with `--kind`
(`SINGLE,PAIR,TRIPLE,PROFILE`), `--family` (e.g. `TRAIT,TM`), `--risk`
(`high`/`normal`) and/or `--case`. A larger selection needs `--chunk N`.
There is no implicit full run.

```fish
python3 07_scripts/randomizer/firered_pilot_matrix.py --suite --confirm USER_LOCAL_RUN \
    --kind SINGLE --risk normal --chunk 1 \
    --rom 04_private_roms/SOURCE.gba --baseline 04_private_roms/NEUTRAL.rnqs \
    --out 05_builds/suite-(date +%Y%m%d-%H%M%S)
```

Before any ROM is generated, each case's settings must equal baseline + its
source-derived change. The case's own change must not already be in the
baseline. In a pair or triple, each family's change must still differ from
the baseline. Both conditions must still hold after `tweakForRom`; otherwise the
case is `NEEDS_REVIEW` and is not generated.
Results are `PASS_GENERATION_REOPEN_REPLAY`, `EXPECTED_REJECTION`,
 `FAIL` (stops the batch), `NEEDS_REVIEW` or `NOT_RUN`.
`EXPECTED_REJECTION` requires that the CLI's only failure output is the
expected guard line plus its closing `ERROR: Randomization failed`, with no
other error, exception or stack trace and no output file. No result claims
that a feature works in the game.
