# UPR-FVX National Dex Guard Workspace integration — 2026-09-29

**Evidence classification:** CONFIRMED CURRENT STATE, limited to the exact revisions and ROM-free checks below.

## Revision basis

- Workspace base: `8260d03162ce8843a477a466f240e7de00afe839`
- Workspace branch: `integration/upr-national-dex-guard-pin`
- Final Workspace branch head: the commit containing this report; GitHub PR metadata records its full SHA.
- UPR-FVX Gitlink: `0e3be63e94e34215cc35308d64e8db15e9a3c48c` → `7bf79ee1e7c46c972f7a9c84942970a950be0723`
- Accepted #550 source head: `3fbe7afc0a6ececf63aa446b04ba7e5e3577faa0`
- UPR-FVX PR #186 squash merge: `7bf79ee1e7c46c972f7a9c84942970a950be0723`
- Live UPR-FVX `compat/firered-cfru-dpe` branch: `7bf79ee1e7c46c972f7a9c84942970a950be0723`

PR #186 was squash-merged. The accepted head is not a parent of the squash commit. The squash commit's parent is the previous UPR-FVX pin `0e3be63e94e34215cc35308d64e8db15e9a3c48c`. GitHub reports tree `c7a9a6fdfb849022f73b17f185a50ee946e250e6` for both the accepted head and merged revision, proving exact tree equality. The base-to-merge diff contains the two accepted #550 paths.

## Workspace scope and Gitlinks

The Workspace change contains exactly:

1. `02_external/upr-fvx`
2. `docs/testing/upr-national-dex-guard-workspace-integration-2026-09-29.md`

The recursive Gitlink diff has exactly one mode-`160000` change: UPR-FVX from `0e3be63e94e34215cc35308d64e8db15e9a3c48c` to `7bf79ee1e7c46c972f7a9c84942970a950be0723`. All other Gitlinks match the Workspace base:

| Path | Unchanged pin |
|---|---|
| `02_external/CFRU-expansion` | `818f65090b1af2b60287f9dbc60302c2b27ac404` |
| `02_external/Dynamic-Pokemon-Expansion-Gen-9` | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| `02_external/Ironmon-Tracker` | `c450ecaee2d8131a2789bb656e3be792a93712fb` |
| `02_external/NatDexExtension` | `a94b8844800308248bb5090b6c36c8b2d7e5d7b9` |
| `02_external/references/cyansmp64-pokefirered-natdex` | `16b8b9ffd77607debe7ce332cd50d3615f47e125` |
| `02_external/references/cyansmp64-upr-zx-natdex` | `9b63eb2876d901dc2e5af49855ae41ac255e1a72` |
| `02_external/references/pret-pokefirered` | `e060ab955b5dc9ac1c4904c2cd141683615cf477` |
| `02_external/references/upr-fvx-upstream` | `e0788edc6529c2605f201996e4807ff30165354c` |
| `02_external/references/upr-zx-ajarmar` | `7f00eb866ed35c8fe3963f078b6a2e0979dc2b8c` |

No protected Workspace path changed. CFRU, DPE, Tracker, NatDexExtension, and all reference Gitlinks are unchanged.

## Exact-pin ROM-free gates

All tests ran from UPR-FVX at `7bf79ee1e7c46c972f7a9c84942970a950be0723` using the existing Gradle wrapper in offline mode. The nine selected classes passed: **30 tests, 0 failures, 0 errors, 0 skipped**.

| Test class | Tests | Result |
|---|---:|---|
| `Gen3NationalDexTweakGuardTest` | 4 | PASS |
| `Gen3RunningShoesTweakPatchTest` | 7 | PASS |
| `Gen3CatchingTutorialSpeciesMappingTest` | 4 | PASS |
| `Gen3FastEggHatchingTweakTest` | 1 | PASS |
| `Gen3CfruDpePickupGuardTest` | 1 | PASS |
| `Gen3CfruDpeSpeciesGenerationTest` | 3 | PASS |
| `Gen3CfruDpeLearnsetPointerTest` | 4 | PASS |
| `Gen3EvolutionLoadDecisionTest` | 4 | PASS |
| `Gen3EvolutionTableScopeTest` | 2 | PASS |

- `git diff --check 0e3be63e94e34215cc35308d64e8db15e9a3c48c 7bf79ee1e7c46c972f7a9c84942970a950be0723`: PASS.
- Workspace `python3 07_scripts/bootstrap/check_git_safety.py`: PASS before the pin change and after it.
- Gradle reported a non-blocking deprecated-feature warning; the selected test task completed successfully.

## Preserved behavior

- Detected CFRU/DPE Gen9 BPRE does not advertise `NATIONAL_DEX_AT_START`; the focused test verifies all other Misc availability bits are unchanged.
- A stale/direct National-Dex request for that profile returns before the generic patch. The synthetic stale-request fixture remains byte-identical, including its FRLG script and check signatures.
- Vanilla FireRed BPRE 1.0 still advertises the tweak and applies the existing generic `patchForNationalDex()` path.
- The existing CFRU/DPE profile detection, Running Shoes, Catching Tutorial, Fast Egg Hatching, Pickup, species-generation, learnset-pointer, and evolution-profile regressions pass.
- This Workspace change only pins the accepted UPR-FVX revision; it implements no CFRU/DPE behavior and does not implement #546 or #547.

## Protected boundary and evidence limit

Tests used synthetic/in-memory fixtures. No ROM, save, emulator state, generated ROM, file under protected `03_tools/releases/`, private runtime path, screenshot, secret, or `.env` was accessed or requested. No runtime or ROM acceptance was performed or is claimed.
