# 212 - Gen Limit / Special Form / Mechanic Item Final Smoke

## Scope

This file records sanitized local evidence for the final UPR-FVX Gen-Limit, Special-Form, Mechanic-Item and Trainer-Held-Item fixes on the CFRU/DPE Gen9 BPRE compatibility branch.

Codex did not run a ROM, read a ROM, create an output ROM, copy a ROM, modify a ROM or inspect saves/emulator states for this evidence file.

## UPR-FVX pin

- Workspace submodule: `02_external/upr-fvx`
- UPR-FVX base branch: `compat/firered-gen9-cfru-dpe`
- Pinned merge commit: `8349daf5ce005f0defc5674cbc3a3468f009218c`
- Included fix chain: merged Gen-Limit 1-9, Gen-Limit pool application, Gen7/8/9 Intro Mon visual candidates, Special-Form predicates/settings/filters/GUI, regional/evolution-relative separation, Trainer Class Sprite Sync GUI exposure, Oak-Lab Rival counter-starter preservation, source-backed CFRU/DPE mechanic item categories and Trainer Held Items / Sensible Items NPE guards through PR #152.

## Local evidence

| Area | Local result | Caveat |
|---|---|---|
| Gen-Limit 1-9 infrastructure | Pass. Gen-Limit 1-9 infrastructure works. | Targeted local smoke only. |
| Gen1-only / Gen1-6 restrictions | Pass. Gen1-only and Gen1-6 log smokes looked correct after the fixes. | Not a full species-matrix audit. |
| Gen7/8/9 Intro Mon | Pass. Random Intro Mon no longer crashes under Gen7/8/9-only and supports valid visual-table candidates. | Broader asset/source coverage remains regression scope. |
| Special-form filtering | Pass. Mega, GMax, Regional, Irregular and Special-form filtering now works in latest local checks. | Custom/future form encodings outside documented CFRU/DPE identity blocks remain audit-required. |
| Evolutionary relatives | Pass. Evolutionary relatives remain an explicit cross-gen-family override. | This does not imply Regional-form override. |
| Regional forms vs evolutionary relatives | Pass. Regional forms are not pulled in by evolutionary relatives unless Regional Forms across Gen Limit is enabled. | Regional-branch edge cases remain audit scope if new metadata appears. |
| Trainer Class Sprite Sync GUI | Pass. Trainer Class Sprite Sync is now GUI-exposed and should be enabled when Trainer Class Names are randomized. | Sync remains opt-in. |
| Oak-Lab Rival counter-starter | Pass. Oak-Lab Rival counter-starter is preserved independently of Rival Carries Starter Through Game. | No all-starter-choice full matrix is claimed here. |
| Mechanic item filtering | Pass. Mechanic item filtering uses source-backed CFRU/DPE categories for Mega, Z and Dynamax/GMax items. | Static Script/Gift/NPC item sources remain caveated if they do not pass through randomizer item replacement pools. |
| Trainer Held Items / Sensible Items | Pass. Latest local GUI smoke reports Trainer Held Items / Sensible Items run without the earlier missing-pool or missing-movepool NPEs. | Targeted smoke only; no full held-item distribution audit is claimed here. |

No current crash was observed in the latest local GUI smoke. No current issue was observed with Pokemon special-form filtering after the latest local checks.

## Status

`Gen Limit / Special Form / Mechanic Item Exclusions = PASS_TARGETED_LOG_VISUAL_SMOKE_WITH_CAVEATS`

No P1 promotion follows from this evidence.

## Remaining caveats

- Targeted local log/visual smoke only, not a full playthrough.
- Plates, Drives, Memories and Nectars are categorized but do not yet have separate user-facing policies.
- Static Script/Gift/NPC item sources remain caveated if they do not run through randomizer item replacement pools.
- Custom or future form encodings outside documented CFRU/DPE identity blocks remain audit-required.
- No ROM paths, hashes, full logs, screenshots, saves, emulator states, secrets, tokens or `.env` data are documented here.
