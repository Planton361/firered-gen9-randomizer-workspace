# Generated CLI Profile Matrix Run

## Scope

This evidence records a sanitized local CLI profile matrix run using generated `.rnqs` profiles from the UPR-FVX Settings Profile Generator.

Codex did not run a ROM smoke. The local run details remain private and only the sanitized aggregate result is recorded here.

## Sanitized Summary

- Profiles processed: 14.
- All profiles produced a CLI log smoke pass or unexpected pass.
- Bad markers: 0 for all profiles.
- Warnings: 0 for all profiles.
- ROM path/hash/full log documented: no.
- Output paths documented: no.
- P1 promotion: no.

## Unexpected Passes

These profiles were previously marked expected-fail/risky but passed the generated profile matrix log smoke:

- `04_foe_held_items_sensible_expected_fail`
- `09_graphics_palettes`
- `10_misc_tweaks`
- `11_special_wild`

## Matrix Impact

- Expected-pass profile features may move to `PASS_LOG` where they were below log-pass status.
- Unexpected-pass profile features remain caveated as `PASS_LOG_WITH_CAVEAT`.
- Ingame status still requires local ingame/manual smoke unless already separately documented.
- Trainer Held Items Sensible no longer has the previous NPE reproduced in this generated matrix run, but still needs a focused isolation pass.
- Graphics/Palettes need visual ingame smoke before removing caveats.
- Misc Tweaks need behavior-specific ingame/manual smoke.
- Special-Wild remains a separate scope even though the generated CLI profile log-smoked cleanly.

No ROMs, output ROMs, full logs, private paths, hashes, screenshots, saves, emulator states, secrets, tokens or `.env` values are documented.
