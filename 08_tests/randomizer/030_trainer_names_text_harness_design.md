# 030 - Trainer Names Text Harness Design

## Scope

Read-only harness design for `FVX-FOE-013` Trainer Names / Class Names only.

No ROM, save, emulator state, output ROM, build artifact, tool binary, private path, hash, secret, token or `.env` file is read, copied, changed or documented by this design. No implementation, UPR-FVX code change, Writer-/Reload fix, external download, smoke run, build or P1 promotion is included.

## Relevant Code Paths

Trainer name/class selection:

- `TrainerNameRandomizer.randomizeTrainerNames()` reads `CustomNamesSet.getTrainerNames()` and `getDoublesTrainerNames()`, filters pool entries with `romHandler.internalStringLength(...) <= 10`, applies `trainerNameMode()`, `maxTrainerNameLength()`, `maxSumOfTrainerNameLengths()` and `getTCNameLengthsByTrainer()`, then writes through `setTrainerNames(...)`.
- `TrainerNameRandomizer.randomizeTrainerClassNames()` reads `CustomNamesSet.getTrainerClasses()` and `getDoublesTrainerClasses()`, buckets by `internalStringLength(...)`, applies `fixedTrainerClassNamesLength()` and `maxTrainerClassNameLength()`, then writes through `setTrainerClassNames(...)`.
- The class-name max loop currently uses `changeTo.length() > maxLength`, so encoded/internal byte length is not the final guard in that loop.

Gen3 fixed-length text behavior:

- `Gen3RomHandler.translateString(...)` encodes visible text plus `\xNN` and `\vNN` escape/control forms into bytes.
- `Gen3RomHandler.internalStringLength(...)` returns `translateString(string).length`.
- `writeFixedLengthString(...)` copies up to the fixed field length, writes a terminator if space remains, then pads the rest of the field.
- Gen3 Trainer names use `TrainerNameLength - 1` as payload limit through `maxTrainerNameLength()`.
- Gen3 Trainer class names use `TrainerClassNameLength - 1` as payload limit through `maxTrainerClassNameLength()`.

Existing coverage:

- `TrainerNameRandomizerTest` already covers ROM-free decision behavior, but its fake `internalStringLength(...)` returns Java string length. It does not prove Gen3 encoding, fixed-length writing, terminator/padding or decoded reload equality.

## Recommended Harness Form

Recommended later implementation: UPR-FVX unit tests, not a workspace-only manual plan, local helper or separate diagnosis harness.

Reasoning:

- A workspace document can describe the cases, but it cannot guard future behavior.
- A small local helper would be easy to discard and would not live near the code under test.
- A separate diagnosis harness is useful for ROM-facing evidence, but this scope is explicitly ROM-free.
- A focused UPR-FVX unit test can reuse the existing `TrainerNameRandomizerTest` style, stay synthetic, avoid ROM access and directly exercise the selection logic where the `changeTo.length()` risk exists.

The later unit-test implementation should be split into two synthetic layers:

1. Selection layer in `:random:test`: fake `RomHandler` with configurable `internalStringLength(...)`, explicit custom name pools and captured `setTrainerNames(...)` / `setTrainerClassNames(...)` outputs.
2. Byte-model layer in `:romio:test` or a package-local test helper only if explicitly authorized: pure byte-array model of `translate`, fixed-field write, terminator/padding and decode behavior. This layer must not instantiate or read a ROM.

## Synthetic Length Model

The fake handler should not return Java string length by default. It should expose a deterministic synthetic encoded length map, for example:

- ordinary ASCII token: encoded/internal length equals visible character count;
- synthetic control token such as `\xNN`: Java length differs from encoded/internal length;
- synthetic variable token such as `\vNN`: Java length differs from encoded/internal length and may consume two encoded bytes;
- unknown token: classified as blocked or unsupported for the case, not silently accepted.

The test names do not need to prove that real Gen3 encoding is safe. They need to prove that Trainer-name selection uses encoded/internal length where expected and that class-name selection can expose the current Java-length risk.

## Concrete Cases

| Case | Later target | Harness expectation |
|---|---|---|
| ASCII inside limit | Trainer Names and Class Names | Candidate whose Java and encoded/internal length are below limit is accepted and captured in the write list. |
| Exactly at encoded/internal limit | Trainer Names and Class Names | Candidate with encoded/internal length equal to `maxTrainerNameLength()` or `maxTrainerClassNameLength()` is accepted only because the encoded/internal payload fits. |
| Over encoded/internal limit | Trainer Names | Candidate whose encoded/internal length exceeds `maxTrainerNameLength()` is skipped or replaced by a fitting candidate. |
| Over encoded/internal limit | Class Names | Candidate with Java length within limit but encoded/internal length over limit is selected by current logic only if the Java `changeTo.length()` path permits it; record this as expected risk exposure, not support. |
| Gen3 escaped/control token | Trainer Names and Class Names | Synthetic `\xNN` / `\vNN`-style token demonstrates Java-length versus encoded/internal-length divergence. No safety claim is made for arbitrary custom text. |
| Terminator/padding | Byte-model layer only | Shorter encoded payload writes payload bytes, one terminator when space remains and padding through the fixed field end. |
| Byte truncation | Byte-model layer only | Encoded payload longer than field length increments a truncation/failure metric; it must not be treated as decoded equality. |
| Decoded reload equality | Byte-model layer only | Decoded value after the synthetic fixed-field write equals the expected string for every changed slot; trailing padding must not create false equality. |

## Later Code Changes Needed

No code is changed in this block. A later authorized implementation would likely need:

- new or extended UPR-FVX tests near `TrainerNameRandomizerTest`;
- a fake `RomHandler` length model where `internalStringLength(...)` can differ from Java length;
- explicit assertions on captured `setTrainerNames(...)` and `setTrainerClassNames(...)` values;
- a test that demonstrates the current class-name `changeTo.length()` risk without fixing it;
- if the byte-model layer is authorized, a small test-only helper that models fixed-field write/decode with synthetic bytes, or a package-visible seam around the existing Gen3 encode/write functions;
- no production Writer-/Reload change unless a later fix scope is separately approved.

## Evidence Boundary

The recommended ROM-free harness can strengthen `tested-non-rom` coverage only. It cannot prove ROM write/reload behavior, real Gen3 text safety or P1 support.

P1-relevant evidence would still require a separately authorized ROM-facing or equivalent writer/reload block with encoded byte lengths, truncation detection, terminator/padding validation and decoded reload equality for actual Gen3 Trainer-name and class-name fields.
