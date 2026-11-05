# Environment

## Canonical baseline

**CONFIRMED USER DECISION:** macOS (Apple Silicon) and Linux are both regular
development environments for the local DPE/CFRU build, UPR-FVX build and
randomizer workflow; POSIX-compatible commands are the default. Neither host is
the sole canonical one. PowerShell material is **LEGACY / OPTIONAL
COMPATIBILITY GUIDANCE**, retained for historical Windows workflows only.

On macOS, the CFRU/DPE build scripts take their non-Windows path: devkitARM
(`arm-none-eabi-*`), `grit` from `$DEVKITPRO/tools/bin`, and native
`wav2agb`/`mid2agb` must be on `PATH`; the Windows `deps/*.exe` are unused.
The system `python3` (3.9+) and Apple `make` suffice. mGBA is installed as the
Homebrew cask `mgba-app`.

| Requirement | Role | Classification |
|---|---|---|
| Git with submodules | Pinned source checkout | **CONFIRMED CURRENT STATE** |
| Python 3 | Bootstrap and safety helpers | **CONFIRMED CURRENT STATE** |
| Java / Gradle | UPR-FVX source work | **CONFIRMED CURRENT STATE** |
| devkitPro / devkitARM and GNU Make | DPE/CFRU build tooling | **CONFIRMED CURRENT STATE** |
| mGBA | Current targeted smoke emulator | **CONFIRMED CURRENT STATE** |
| BizHawk / Ironmon Tracker | Later validation targets | **INTENDED FUTURE STATE** |

## Version policy

Use an exact version only when repository evidence records it for the relevant
revision. Submodule Gitlinks are the authoritative source revision for a
checkout; historical source/version evidence is retained in
[01_docs/references/tool-manifest.md](../01_docs/references/tool-manifest.md).

**UNKNOWN:** No canonical host-package version inventory is established by
M-000R. Do not invent Python, Java, Gradle, devkitPro, GNU Make, or emulator
versions in task reports.

## Daily FAST workflow

See [development modes](ENGINEERING_RULES.md#development-modes). All outputs
stay in the git-ignored `05_builds/`; ROMs, saves and logs never enter Git.

```sh
# Run from the Workspace root.
# 1. ROM build: DPE, then CFRU on the fresh DPE output (base ROM is only read)
07_scripts/build/dev_build.sh <clean-BPRE-rev0.gba>
#    -> 05_builds/dev-<timestamp>/cfru-<sha>-dpe-<sha>.gba + BUILD_INFO.txt

# 2. Randomizer JAR (only after UPR-FVX changes; no test suite)
(cd 02_external/upr-fvx && ./gradlew :random:jar)

# 3. Randomize + log scan with the existing smoke runner
07_scripts/randomizer/cli_log_smoke_pipeline.sh \
  --rom 05_builds/dev-<timestamp>/cfru-<sha>-dpe-<sha>.gba \
  --settings-file <settings.rnqs> \
  --output-rom 05_builds/dev-<timestamp>/randomized.gba \
  --report 05_builds/dev-<timestamp>/smoke-report.md

# 4. Play-test
open -a mGBA 05_builds/dev-<timestamp>/randomized.gba   # Linux: mgba-qt <rom>
```

`dev_build.sh` moves previous in-place DPE/CFRU artifacts into
`05_builds/<build>/pre-build-archive/` instead of deleting them. It records the
actual component commits, Gitlink deviations and local changes in
`BUILD_INFO.txt`; `--release` enforces Workspace-pinned, clean sources instead.

**Known limitation:** CFRU's own `scripts/make.py` runs
`scripts/check_native_source_identity.py` and refuses any uncommitted tracked
change or unignored untracked file. Commit work in progress on a CFRU feature
branch before building; `dev_build.sh` reports this before touching any file
and does not bypass it. DPE may be built with local changes (recorded as
`-dirty`).

## Safety command

Run from the workspace root before changes and before handoff:

```sh
python3 07_scripts/bootstrap/check_git_safety.py
```

For read-only/bootstrap inspection on `main`, use the explicit exception:

```sh
python3 07_scripts/bootstrap/check_git_safety.py --allow-main
```
