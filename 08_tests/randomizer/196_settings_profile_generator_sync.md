# Settings Profile Generator Sync

## Scope

UPR-FVX PR #98 adds a no-ROM `settings-profile` helper. The workspace now uses it to derive `.rnqs` profile settings from one local base settings file and the existing CLI profile matrix manifest.

Codex may verify the helper and wrapper without ROM access. Real CLI randomizer runs with a private ROM remain local-only user work.

## Workspace Wrapper

Use:

```sh
07_scripts/randomizer/generate_settings_profiles_from_matrix.sh \
  --upr-dir 02_external/upr-fvx \
  --base-settings <local-base-settings.rnqs> \
  --profile-manifest 08_tests/randomizer/cli_profile_matrix.example.tsv \
  --output-settings-dir <ignored-local-settings-dir>
```

The wrapper reads enabled rows from the manifest and runs:

```sh
java -jar 02_external/upr-fvx/random/build/libs/UPR-FVX.jar settings-profile \
  --base-settings <local-base-settings.rnqs> \
  --output-settings <ignored-local-settings-dir>/<profile_id>.rnqs \
  --profile <profile_id>
```

The wrapper accepts no ROM argument, invokes no randomization command and creates no output ROM.

## Dry Run

```sh
07_scripts/randomizer/generate_settings_profiles_from_matrix.sh \
  --upr-dir 02_external/upr-fvx \
  --base-settings <local-base-settings.rnqs> \
  --profile-manifest 08_tests/randomizer/cli_profile_matrix.example.tsv \
  --output-settings-dir <ignored-local-settings-dir> \
  --dry-run
```

Dry-run validates manifest wiring only. It does not require the base settings file and does not write generated `.rnqs` files.

## Integration Flow

1. Create or export one local base `.rnqs` settings file.
2. Build the pinned UPR-FVX jar.
3. Run `generate_settings_profiles_from_matrix.sh` to create profile `.rnqs` files under an ignored local directory.
4. Run `run_cli_profile_matrix.sh` with a private ROM locally, if and only if a real ROM smoke is intended.
5. Report back only sanitized aggregate evidence.

## Privacy Boundary

Do not document:

- ROM paths.
- Output ROM paths.
- ROM hashes or file hashes.
- Full logs or stack traces.
- Screenshots.
- Save files or emulator states.
- Private local paths.
- Secrets, tokens or `.env` values.

This sync adds no P1 promotion.
