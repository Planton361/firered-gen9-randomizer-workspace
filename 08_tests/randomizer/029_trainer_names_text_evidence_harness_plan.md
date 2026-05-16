# 029 - Trainer Names Text Evidence Harness Plan

## Scope

Read-only Evidence-/Harness-Plan for `FVX-FOE-013` Trainer Names / Class Names only.

No ROM, save, emulator state, output ROM, build artifact, tool binary, private path, hash, secret, token or `.env` file is read, copied, changed or documented by this plan. No UPR-FVX code change, Writer-/Reload fix, Text-Encoding implementation, smoke run, build or P1 promotion is included.

## Current Evidence Boundary

`027_trainer_rom_reload_text_evidence_plan.md` keeps Trainer Names / Class Names at `tested-non-rom`, not P1-supported. `028_trainer_writer_reload_text_field_review.md` identifies the later evidence surface:

- `TrainerNameRandomizer.randomizeTrainerNames()` uses `internalStringLength(...)` for Trainer-name pool filtering, replacement length and total-length accounting.
- `TrainerNameRandomizer.randomizeTrainerClassNames()` builds class-name buckets with `internalStringLength(...)`, but the max-length rejection loop uses Java `changeTo.length()`.
- Gen3 Trainer names are written through `writeFixedLengthString(tr.getName(), ..., TrainerNameLength)`.
- Gen3 Trainer class names are written through `setTrainerClassNames(...)` and `writeFixedLengthString(..., TrainerClassNameLength)`.
- Gen3 `internalStringLength(...)` maps to `translateString(...).length`.
- `writeFixedLengthString(...)` copies at most the fixed field length, writes a terminator if room remains, then pads the remaining bytes.

This plan does not claim that any encoding case is safe.

## Minimal Harness Shape

A later authorized harness should isolate Trainer Names / Class Names from all Trainer Pokemon, Battle Style, Special Rules, Wild, Starter, Static/Gift, Evolution, MoveData, Move Names, Items, Shops and Text/Menu scopes.

Preferred evidence levels, in order:

1. ROM-free unit harness around selection logic using a fake `RomHandler` whose `internalStringLength(...)` deliberately differs from Java length for at least one token. This can prove selection logic and expose the `changeTo.length()` risk without touching ROM bytes.
2. Separate fixed-field writer/reload evidence only if explicitly authorized later. That evidence must inspect encoded byte length, truncation, terminator, padding and decoded reload equality for Gen3 Trainer-name and class-name fields.

The first harness can remain `tested-non-rom` only. The second level is required before any P1 discussion.

## Minimal Test Cases

| Case | Field | Input shape | Required observation |
|---|---|---|---|
| ASCII inside limit | Trainer name and class name | visible ASCII shorter than max payload | accepted by selection, encoded/internal length below payload, later writer evidence would show terminator plus padding |
| ASCII exactly at limit | Trainer name and class name | visible ASCII with encoded/internal length equal to `maxTrainerNameLength()` or `maxTrainerClassNameLength()` | accepted only when encoded/internal payload length fits; later writer evidence would show terminator still fits in the full fixed field |
| Over limit | Trainer name and class name | encoded/internal length greater than max payload | rejected or skipped before write; if selected by class-name Java-length logic, record as blocked risk |
| Encoding token case | Trainer name and class name | a codepath-relevant escaped/control token such as `\xNN` or `\vNN`, or another Gen3 dictionary token if the harness exposes it | compare Java length with `internalStringLength(...)`; do not mark safe unless encoded/internal length and decoded reload are measured |
| Terminator/padding | fixed-field writer evidence only | shortened replacement after a longer original slot | verify one terminator after encoded bytes when space remains, then padding until fixed field end |
| Decoded reload equality | fixed-field writer/reload evidence only | every changed name/class slot | decoded reload text equals expected text, not merely non-empty or save-successful |

For the encoding-token case, the harness must use only code-visible synthetic strings and must not infer that arbitrary custom text is supported. Unsupported or untranslatable text should be documented as blocked, not supported.

## Required Metrics For Later Evidence

Later Trainer Names / Class Names evidence should report at minimum:

- selected field: `trainerNames` or `trainerClassNames`;
- slot count before/after/reload;
- changed slot indexes only, not private source paths or ROM-derived hashes;
- expected decoded text and reloaded decoded text for each changed slot;
- Java length, encoded/internal byte length and fixed payload limit for each candidate;
- rejected/blocked over-limit candidates;
- truncation count, expected `0`;
- missing-terminator count, expected `0`;
- padding mismatch count, expected `0`;
- decoded reload mismatch count, expected `0`;
- repeated-name translation stability for Trainer names;
- singles/doubles pool classification when the selected case uses `&` or doubles trainer classes;
- explicit statement that `changeTo.length()` was not used as the proof metric.

Save/Log/Output/Reload success is necessary for a ROM-facing evidence level, but it is not sufficient without the byte-length, terminator/padding and decoded-reload checks above.

## Open Risks

- Class-name max filtering still contains `changeTo.length()`, so Java length can accept a candidate whose encoded/internal byte length does not fit.
- `writeFixedLengthString(...)` truncates translated bytes to the fixed field length; successful save/reload alone can hide truncation.
- `readVariableLengthString(...)` reads fixed slots until terminator, so stale trailing bytes can be hidden unless terminator and padding are checked.
- Escape/control text such as `\xNN` / `\vNN` is code-visible in the encoder, but support for any specific custom-name use needs evidence.

## P1-Relevant Evidence Gate

Trainer Names / Class Names can be evaluated more tightly only after a separately authorized evidence block proves:

- encoded/internal length is the enforced limit for both names and class names;
- over-limit encoded text is rejected before write or recorded as blocked;
- byte truncation is detected and absent;
- terminator and padding are valid after write;
- decoded reload equality is exact for all changed slots;
- repeated-name and doubles-pool behavior remains stable;
- no Writer-/Reload fix is mixed into the evidence run.

Until then, `FVX-FOE-013` remains `tested-non-rom`, not P1-supported.
