# 209 Graphics Palettes Visual Smoke

Status: sanitized local Graphics/Palettes visual smoke. No ROM run by Codex. No P1 promotion.

## Scope

- Uses the current workspace UPR-FVX pin with merged PR #123 and PR #124: `0eb815418470fa1ac000695b95d09cb084338dca`.
- Focuses on Pokemon palette randomization and the related Graphics/Palettes smoke path.
- This is targeted visual/audit evidence, not a full playthrough, broad species sweep, shiny-coverage proof or P1 promotion.

## Sanitized Evidence

Available sanitized local evidence:

- `Pokemon Palettes: Randomized/Changed`.
- CFRU-DPE palette copy save completed with `normalPaletteWriteAttempts=841`.
- Base-vs-output Palette Audit sampled 21 species.
- Audit summary: `sampledCount=21`, `normalChangedCount=21`, `shinyChangedCount=0`, `unchangedCount=0`.
- Charmander, Squirtle, Caterpie, Pikachu and Blissey reported `normalChangedFromBase=yes`.
- Changed palettes were visually observed.
- The final run did not report `Error during logging`.

## Status Impact

- Graphics/Palettes visual smoke: local targeted pass with caveats.
- Pokemon Palettes Random: local targeted pass for sampled normal palettes.
- CFRU-DPE normal palette output writes: local audit pass for sampled species.
- Shiny palette coverage remains caveated by the sampled audit: `shinyChangedCount=0`.
- Logging crash from expanded trainer rows was not observed in the final run after the UPR-FVX PR #124 pin.
- No P1 promotion.

## Follow-Up Scope

Future local-only evidence can strengthen confidence by sampling:

- more species and forme ranges.
- shiny palette behavior separately.
- longer visual play or reload paths.
- Graphics/Palettes interactions only after keeping unrelated Wild/Foe/Items/Misc/Type chaos out of the profile.

Keep ROM paths, output paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens and `.env` content out of reports.
