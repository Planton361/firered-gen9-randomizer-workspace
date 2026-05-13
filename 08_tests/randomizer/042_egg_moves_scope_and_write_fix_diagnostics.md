# 042 - CFRU/DPE Egg Moves Scope and Write Fix Diagnostics

Branch: `compat/upr-fvx-cfru-dpe-egg-moves-scope-and-write`
Date: 2026-05-13
UPR-FVX commit: `18168b78b973a4c39f34053ac58f21279a26d8d2`

## Scope

This protocol validates the minimal CFRU/DPE Egg-Move reader/writer for Gen9 BPRE.

No Learnset-Write, Move-Data-Write, Tutor-Text, Special-Tutor, or `setMovesLearnt()` expansion is included.

## Fix summary

- CFRU/DPE Egg-Move handling is gated behind the existing CFRU/DPE Gen9 species-count path.
- `gEggMoves` is read through pointer location `0x45C50`.
- The pointer resolves to `0x09A0E94C`, ROM offset `0x1A0E94C`, on the tested ROM.
- The classic `u16` stream format is preserved.
- Species markers remain `species + 20000`.
- End sentinel remains `0xFFFF`.
- Egg-Move species keys use internal `SpeciesSet` identity rather than Pokédex ID round-tripping.
- High move-ID flag-array access in `SpeciesMovesetRandomizer` is bounds-checked.
- Vanilla, Jambo, and other Gen3 paths keep their existing Egg-Move offsets and logic.

## Harness

Egg moves are only coupled to broader moveset randomization in the normal settings flow. To keep `setMovesLearnt()` out of scope, this diagnosis used a direct local harness that invokes `SpeciesMovesetRandomizer.randomizeEggMoves()` and then saves/reloads the ROM.

Local output artifacts were written under ignored `05_builds/randomizer-smoke/042_egg_moves_scope_and_write_fix/` and were not staged.

## Results

| Metric | Result |
| --- | --- |
| `moves.total` | `992` |
| highest loaded move | `991:PsychicNoise` |
| `gEggMoves` pointer location | `0x45C50` |
| `gEggMoves` target pointer | `0x09A0E94C` |
| `gEggMoves` ROM offset | `0x1A0E94C` |
| stream format | `u16` confirmed |
| species marker | `species + 20000` confirmed |
| end sentinel | `0xFFFF` confirmed |
| species entries before | `436` |
| species entries after | `436` |
| species entries reload | `436` |
| highest species before | `0x584` / `1412` |
| highest species after | `0x584` / `1412` |
| highest species reload | `1412` |
| highest move before | `967` |
| highest move after | `991` |
| highest move reload | `991` |
| Gen8+ species entries before | `93` |
| Gen8+ species entries after | `93` |
| Gen9 move entries before | `4` |
| Gen9 move entries after | `272` |
| invalid Egg moves before | `0` |
| invalid Egg moves after | `0` |
| skipped Placeholder-/Null-Species before | `0` |
| skipped Placeholder-/Null-Species after | `0` |
| `writeReloadEggMoveMismatches` | `0` |
| Bad Egg / `<unknown>` in log | `false` |
| unknown move marker | `false` |
| `saveSuccessful` | `true` |
| `logSuccessful` | `true` |
| `outputRomExists` | `true` |
| `logNonEmpty` | `true` |

## P1 support assessment

Egg-Move-only is P1-supported for the tested CFRU/DPE Gen9 BPRE scope when executed through the direct Egg-Move path. The normal full settings flow still couples Egg-Move randomization to broader moveset handling, so this protocol intentionally avoids claiming expanded Learnset-Write support.

## Remaining risks

- The diagnosis validates the known CFRU/DPE Gen9 BPRE pointer location only; other hacks remain on their existing paths.
- Egg-Move stream growth is not expanded in this branch. The tested randomized stream rewrites in place and reloads without mismatch.
- Future work should keep Learnset-Write, Move-Data-Write, Special Tutors, and Tutor text separate.
