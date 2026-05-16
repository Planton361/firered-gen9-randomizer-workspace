# 027 - Trainer ROM/Reload/Text-Encoding Evidence Plan

## Scope

This is a read-only planning note for later Trainer ROM-/Reload-/Text-Encoding evidence.

No ROM file, save, emulator state, build artifact, output ROM, Randomizer JAR, tool binary, private path, secret, token or `.env` file was read, copied, changed or documented in this block. No UPR-FVX code, writer fix, reload implementation, text-encoding implementation or P1 promotion is included.

## Already Tested Non-ROM

The recent Trainer follow-ups provide synthetic Non-ROM evidence only:

| Feature-ID | Area | Current evidence | Current status |
|---|---|---|---|
| `FVX-FOE-005` | Additional Pokemon: Boss Trainers | synthetic Trainer/Party/Species harness | `tested-non-rom`, not P1-supported |
| `FVX-FOE-006` | Additional Pokemon: Important Trainers | synthetic Trainer/Party/Species harness | `tested-non-rom`, not P1-supported |
| `FVX-FOE-007` | Additional Pokemon: Regular Trainers | synthetic Trainer/Party/Species harness | `tested-non-rom`, not P1-supported |
| `FVX-FOE-009` | Force Diverse Types / Type Themes | synthetic null-Type guard harness | `tested-non-rom`, not P1-supported |
| `FVX-FOE-010` | Pokemon League Has Unique Pokemon | synthetic Trainer/Party/Species/Evolution harness | `tested-non-rom`, not P1-supported |
| `FVX-FOE-011` | Battle Style | synthetic Trainer harness | `tested-non-rom`, not P1-supported |
| `FVX-FOE-012` | Rival Carries Starter Through Game | synthetic Trainer/Party/Species/Evolution harness | `tested-non-rom`, not P1-supported |
| `FVX-FOE-013` | Trainer Names / Class Names | synthetic name/class decision harness | `tested-non-rom`, not P1-supported |
| `FVX-FOE-014` | Trainers Evolve Their Pokemon + Level Modifier | synthetic Trainer/Party/Species/Evolution harness | `tested-non-rom`, not P1-supported |

Older Trainer Species, Trainer Held Items and Trainer Movesets documents contain ROM-/Reload-style evidence for their own previously scoped paths. They do not prove the newer synthetic-only Trainer suboptions above, and they do not prove Trainer Names/Class Names text encoding.

## Missing ROM-/Reload Evidence

Before any later P1 promotion, each promoted Trainer suboption needs separately authorized ROM-facing or equivalent writer/reload evidence:

- Save, log, output and reload must all complete successfully in the scoped run.
- The changed Trainer data must compare cleanly after fresh reload with a path-specific mismatch counter of `0`.
- Unchanged Trainer fields outside the selected option must remain preserved.
- The scope must stay isolated from Wild, Starter, Static/Gift, Evolution, Learnset, TM/Tutor, Ability, Palette, MoveData, Move Names, Items, Shops and Text/Menu paths unless explicitly authorized.
- The evidence must name the exact Trainer option mix being tested instead of promoting the whole Trainer group.

This plan does not authorize running that evidence.

## Text-Encoding Risk

Trainer Names and Trainer Class Names are text fields, so ordinary string-level checks are not enough for P1 promotion.

Required later evidence:

- prove which text encoder/decoder path is used for Gen3 Trainer names and class names;
- prove fixed-length fields stay fixed after encoding, padding and reload;
- prove repeated-name handling still maps to reload-stable encoded text;
- prove class-name length constraints are measured against the encoded/internal representation, not only visible characters;
- report any unsupported character, terminator, padding or control-token case as blocked rather than supported.

No text-encoding claim is made by the current Non-ROM `TrainerNameRandomizerTest` evidence.

## `changeTo.length()` Risk

`changeTo.length()` is a risk marker because Java string length may not match the encoded/internal text length used by the ROM writer.

A later implementation or evidence block must not treat `changeTo.length()` alone as proof of safety for Trainer text. Promotion requires either:

- a demonstrated encoded/internal-length check for the affected field, or
- a documented reason why the selected character pool makes Java length and encoded/internal length equivalent for that exact field.

Without that proof, Trainer Names/Class Names remain `tested-non-rom` only.

## Criteria For Later P1 Promotion

A later Trainer P1 promotion can be considered only when all applicable criteria are met:

- the scope is explicitly authorized and remains narrower than the whole Trainer feature group;
- no new writer/reload code change is mixed with unrelated Trainer suboptions;
- Save/Log/Output/Reload evidence passes for the selected option set;
- path-specific Trainer mismatch counters are `0` after reload;
- unsafe Species, null Species, invalid moves, invalid held items, `Bad Egg`, `<unknown>` and fallback markers are absent or explicitly classified as preserved non-target data;
- Trainer text promotion additionally has encoded/internal-length proof and no unresolved `changeTo.length()` risk;
- the result is documented as P1 only for the exact tested settings, not for untested combinations.

## Next Minimal Step

If this scope is reopened, start with a read-only design/review block that identifies the exact Trainer writer/reload fields and the exact Trainer text encoder/decoder length checks to measure. Do not run ROM evidence, implement writer/reload fixes or promote P1 from this plan.
