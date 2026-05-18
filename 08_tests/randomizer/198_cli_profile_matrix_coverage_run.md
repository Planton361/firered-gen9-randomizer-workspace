# Coverage CLI Profile Matrix Run

## Scope

This evidence records a sanitized local CLI profile matrix run using generated `.rnqs` profiles from the coverage manifest.

Codex did not run a ROM smoke. The local run details remain private and only the sanitized aggregate result is recorded here.

## Sanitized Summary

- Dry run: no.
- Profiles processed: 14.
- ROM path/hash/full log documented: no.
- Output paths documented: no.
- P1 promotion: no.

## PASS Profiles

These profiles passed with 0 bad markers and 0 warnings:

- `00_baseline`
- `01_traits_full`
- `02_starters_statics_trades_full`
- `03_moves_movesets_full`
- `04_foe_base`
- `04_foe_held_items_basic`
- `05_wild_full`
- `06_tm_tutor_full`
- `07_items_full`
- `08_types_full`

## UNEXPECTED_PASS Profiles

These profiles also had 0 bad markers and 0 warnings, but remain caveated and are not treated as stable/P1 evidence:

- `04_foe_held_items_sensible_expected_fail`
- `09_graphics_palettes`
- `10_misc_tweaks`
- `11_special_wild`

## Matrix Impact

- Feature rows are updated only where the executed coverage profile exactly enabled the Feature ID through the profile/feature overlay set.
- Unexpected-pass rows remain `PASS_LOG_WITH_CAVEAT`.
- `ingame_status` still requires local ingame/manual smoke unless already separately documented.
- Special-Wild remains a separate scope even though the coverage CLI profile log-smoked cleanly.

No ROMs, output ROMs, full logs, private paths, hashes, screenshots, saves, emulator states, secrets, tokens or `.env` values are documented.
