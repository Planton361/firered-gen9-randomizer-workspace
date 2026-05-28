# MacBook rebuild success

## Scope

This document records a sanitized local status sync for the MacBook rebuild.

It intentionally does not include ROMs, saves, emulator states, builds, tool binaries, screenshots, raw logs, ROM hashes, private paths, tokens, secrets or `.env` data.

## Confirmed local status

- Workspace branch for this documentation sync: `docs/macbook-rebuild-success`.
- UPR-FVX submodule: `02_external/upr-fvx` is confirmed at `1a597a667129b50284dd88afb231372b5bd01d7f`.
- UPR-FVX build: `./gradlew clean :random:jar` completed locally.
- UPR-FVX GUI: starts locally with Java 25.
- GBA toolchain: devkitPro/devkitARM is present.
- Compiler: `arm-none-eabi-gcc` 15.2.0 is present.
- Build tools: `gbafix`, `grit` and GNU Make 4.4.1 are present.
- Audio conversion tooling: local Wine wrappers for `wav2agb.exe` and `mid2agb.exe` are present.
- DPE build: local rebuild completed successfully.
- CFRU build: local rebuild completed successfully.
- Final local CFRU+DPE Gen9 ROM candidate: loads in UPR-FVX and boots in mGBA.

## Open status

- BizHawk compatibility remains open.
- Ironmon Tracker compatibility remains open.
- No P1 or full-playthrough promotion is implied by this rebuild sync.

## Safety boundary

- No ROM, save, emulator state, build artifact, tool binary, screenshot, raw log, ROM hash, private path, token, secret or `.env` content is documented here.
- No external repo, fork or submodule was changed for this status sync.
- The status is a local environment rebuild confirmation, not a reproducible public binary release.
