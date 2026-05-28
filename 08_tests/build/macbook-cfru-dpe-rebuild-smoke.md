# MacBook CFRU/DPE rebuild smoke

## Result

`PASS_TARGETED_LOCAL_REBUILD_SMOKE_WITH_CAVEATS`

## Scope

This smoke records a sanitized local MacBook rebuild confirmation for the current workspace state.

## Confirmed observations

- UPR-FVX submodule is confirmed at `1a597a667129b50284dd88afb231372b5bd01d7f`.
- UPR-FVX build command `./gradlew clean :random:jar` completed.
- UPR-FVX GUI starts with Java 25.
- devkitPro/devkitARM is present.
- `arm-none-eabi-gcc` 15.2.0 is present.
- `gbafix`, `grit`, and GNU Make 4.4.1 are present.
- Local Wine wrappers for `wav2agb.exe` and `mid2agb.exe` are present.
- DPE rebuild completed locally.
- CFRU rebuild completed locally.
- Final local CFRU+DPE Gen9 ROM candidate loads in UPR-FVX.
- Final local CFRU+DPE Gen9 ROM candidate boots in mGBA.

## Caveats

- Targeted local smoke only.
- No BizHawk validation yet.
- No Ironmon Tracker validation yet.
- No full playthrough, broad route matrix, save-state validation or P1 promotion is claimed.

## Safety boundary

No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret or `.env` content is included.
