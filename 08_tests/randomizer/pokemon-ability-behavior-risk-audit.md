# Pokemon ability behavior risk audit smoke

Date: 2026-05-29
Branch: `analysis/pokemon-ability-behavior-risk-audit`
Status: `PASS_SOURCE_BACKED_READ_ONLY_AUDIT_WITH_CAVEATS`

## Scope

Read-only source audit of local CFRU/DPE Ability constants, alias defines, names/descriptions, DPE assignments and CFRU battle behavior hooks for Gen9/newer Ability names.

No CFRU code, DPE data, UPR-FVX code, submodule pin, Showdown data, raw report, ROM, save, emulator state, build artifact, tool binary, screenshot, hash, private path, token, secret or `.env` data was changed or documented.

## Commands run

- `git branch --show-current`
- `git status --short`
- `rg --files 02_external/CFRU-expansion 02_external/Dynamic-Pokemon-Expansion-Gen-9`
- `rg` searches for focused Ability constants, `SpeciesHas*` helpers, Ability strings, DPE `Base_Stats.c` assignments and CFRU behavior hooks.
- Targeted `sed` reads of CFRU/DPE source snippets for alias blocks, display overrides, battle behavior and DPE species ability assignments.

## Result summary

- Branch guard passed: working branch was `analysis/pokemon-ability-behavior-risk-audit`.
- Initial tree guard passed: `git status --short` was clean before documentation edits.
- CFRU/DPE Ability headers show Gen9 Ability names mainly as aliases to older Ability IDs.
- CFRU behavior hooks exist for several alias-backed abilities, including Hadron Engine, Orichalcum Pulse, Toxic Debris, Poison Puppeteer, Ruin abilities, Sharpness, Rocky Payload, Seed Sower, Wind Power, Wind Rider, Earth Eater and others.
- Missing or high-risk focus areas remain visible: Commander, Hospitality and Embody Aspect are not locally represented; Terapagos Tera Shift / Tera Shell paths are inconsistent; Zero to Hero behavior was not fully confirmed as true form-change behavior by this source pass.

## Caveats

This is a source-backed documentation smoke only. It is not a local ROM build, emulator smoke, battle validation, full-playthrough, BizHawk validation, Ironmon Tracker validation or P1 promotion.
