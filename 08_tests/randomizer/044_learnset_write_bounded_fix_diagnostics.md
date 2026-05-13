# 044 - CFRU/DPE Learnset-Write bounded in-place Fix Diagnostics

## Scope

- Branch: `compat/upr-fvx-cfru-dpe-learnset-write-bounded`
- UPR-FVX commit: `dd9d80c16936a99bac1d7ef777b43baa7c2f029d`
- Workspace follow-up for: `08_tests/randomizer/043_p1_learnset_write_model.md`
- Goal: validate the minimal gated CFRU/DPE `setMovesLearnt()` path for bounded in-place writes.

Out of scope:

- no repointing
- no Move-Data-Write
- no Tutor text/menu rewrite
- no Special-Tutor support
- no Egg-Move expansion
- no broad Gen3 refactor

Local ROM, output ROM and log artifacts stayed ignored under `05_builds/randomizer-smoke/044_learnset_write_bounded_fix/`.

## Implemented Fix

`Gen3RomHandler.setMovesLearnt()` now has a narrow CFRU/DPE Gen9-BPRE branch gated by the existing CFRU/DPE species-count detection.

The new path:

- resolves `gLevelUpLearnsets` through pointer location `0x03EA7C`
- keeps internal `SpeciesSet` identity as the primary key
- writes entries as `u16 move + u8 level`
- writes the `{0, 0xFF}` sentinel
- writes only when `newEntryCount <= originalEntryCount`
- skips growth instead of repointing
- skips unsafe or non-learnset pointer targets
- skips placeholder/null species
- detects shared pointer conflicts before writing
- validates move IDs against the loaded `moves.total`
- leaves vanilla, Jambo and other Gen3 paths unchanged

## Pointer and Model Findings

| Metric | Value |
|---|---:|
| `moves.total` | `992` |
| Highest loaded move | `991:PsychicNoise` |
| `gLevelUpLearnsets` pointer location | `0x03EA7C` |
| `gLevelUpLearnsets` target pointer | `0x0825D7B4` |
| `gLevelUpLearnsets` ROM offset | `0x25D7B4` |
| Entry format | `u16 move + u8 level` |
| Sentinel | `00 00 FF` / `{0, 0xFF}` |
| Runtime cap used for safety | `50` learnable moves |

## Diagnostic Run

Harness scope:

- direct bounded Learnset write harness
- normal Settings flow was not used because broader moveset/learnset randomization can request growth and is outside this no-repoint branch
- the harness changed only same-length learnsets where the writer accepted the target as safe

Writer diagnostic line:

```text
[CFRU-DPE-LEARNSET-WRITE] boundedWrites=1 skippedGrowth=0 needsRepoint=0 skippedSharedPointer=0 skippedPlaceholderSpecies=1 skippedInvalidPointer=1412 skippedInvalidMoves=0
```

Result metrics:

| Metric | Value |
|---|---:|
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |
| `writeReloadLearnsetMismatches` | `0` |
| Bounded writes accepted by writer | `1` |
| `skippedGrowth` / `needsRepoint` | `0` / `0` |
| `skippedSharedPointer` | `0` |
| skipped placeholder/null species | `1` |
| skipped invalid/unsafe pointers | `1412` |
| invalid input learnset moves | `0` |
| Bad Egg / `<unknown>` in log | `false` |
| Unknown move marker in log | `false` |
| Stacktrace | none |

Raw pointer-table scan notes:

- The raw pointer-table scan sees many formal entries that are not safe CFRU/DPE level-up learnset arrays.
- Raw scan values included invalid move-like words and `0xFFFF`, which confirms the writer must not blindly write every pointer-table entry.
- The writer therefore treats the strict safe-pointer check as authoritative for write eligibility.

Raw scan metrics from the harness:

| Metric | Value |
|---|---:|
| raw species with parseable pointer entries before/after/reload | `447 / 447 / 447` |
| raw highest species before/after/reload | `930 / 930 / 930` |
| raw learnset entries before/after/reload | `21858 / 21856 / 2818` |
| raw invalid move-like values before/after | `18878 / 18878` |
| raw highest move-like value before/after/reload | `65535 / 65535 / 864` |

These raw metrics are not evidence of safe writable scope. They are retained to document why bounded in-place write requires pointer-target validation and why full Learnset-Write support still needs a repoint/table model.

## P1 Support Assessment

Bounded in-place `setMovesLearnt()` is implemented and stable for strictly validated same-size CFRU/DPE learnsets:

- save succeeds
- log succeeds
- output ROM is produced
- reload comparison has `0` mismatches
- no repointing is attempted

Full Learnset-Write randomization is not yet broadly P1-supported. The current tested ROM exposes only a very small safe bounded-write subset through the strict guard, while most pointer-table entries are skipped as unsafe or out of scope. Learnset growth still requires a separate repointing design.

## Risks and Follow-Up

- Most table entries are skipped by the safe-pointer guard; this is intentional for this branch but limits practical Learnset randomization coverage.
- Growth cases remain out of scope and should be counted as `needsRepoint`, not written in-place.
- A future full Learnset-Write branch needs a proven allocation/repointing model and shared-pointer policy.
- Move IDs up to `991` are supported only where loaded by the current CFRU/DPE move-data reader.

## Checks

UPR-FVX:

```sh
git status --short
git diff --stat
git diff --check
./gradlew clean :random:jar
```

Workspace:

```sh
git status --short
git submodule status --recursive
git diff --stat
git diff --submodule
git diff --check
```
