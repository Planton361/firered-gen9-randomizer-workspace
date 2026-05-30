# CFRU QoL coverage handoff

Status: `PASS_READ_ONLY_COVERAGE_WITH_CAVEATS`.

This is a documentation-only handoff for `01_docs/analysis/cfru-qol-coverage.md`. It records source-backed coverage findings from the current local Planton361 CFRU checkout without changing CFRU, DPE or UPR-FVX code.

## Read-only source coverage

Reviewed local source areas:

- CFRU config flags in `02_external/CFRU-expansion/src/config.h`.
- Overworld behavior in `src/overworld.c` and `assembly/overworld_scripts/system_scripts.s`.
- Runtime options in `src/option_menu.c`, `src/start_menu.c`, `src/read_keys.c`, and related strings.
- Item/TM/HM behavior in `src/item.c`, `src/party_menu.c`, `src/scripting.c`, and item table headers.
- Existing Workspace QoL inventory and manual smoke matrix.
- Existing UPR-FVX Field Items docs/smokes for randomizer-output ownership.

## Result summary

| Area | Result | Follow-up smoke |
|---|---|---|
| Repel-Reuse / BW Repel System | Present and active in CFRU as compile-time plus script behavior. No runtime option found. | Repel expiration Yes/No branch and matching Repel/Super/Max step reset. |
| New Game / intro / Oak tutorial | Controls-guide skip and Oak tutorial battle absence are already provided; broader faster intro/lab/parcel flow is not. | Keep existing New Game smoke as regression gate. |
| Runtime Options | Current runtime pages already cover several settings rows; no duplicate UI should be built casually. | Page navigation, dirty-row preservation, Nuzlocke/Wild Prebattle ownership. |
| Field items / itemballs | Generic itemball and item acquire presentation exist; per-TM/HM/important visual balls are absent. | Generic itemball pickup smoke; UPR-FVX Field Items reload smokes after any visual work. |
| Hidden Items | Hidden pickup presentation exists; visible hidden-item/sparkle cue is not implemented. | Hidden item pickup once, flag set, optional cue only after design. |
| DPE | No direct QoL ownership. | None. |

## Caveats

- No local build, emulator run, full playthrough, BizHawk validation, Ironmon Tracker validation or support promotion is claimed here.
- Manual New Game coverage remains the existing `PASS_FULL_WITH_CAVEATS` result from `cfru-qol-new-game-smoke.md`.
- Field Items output remains UPR-FVX-owned; this analysis does not change or broaden any randomizer writer.
- Missing QoL features need separate design branches before implementation.

## First implementation-block handoff

Recommended first real block: preserve-smoke the already-provided CFRU QoL instead of writing new features.

Suggested smoke list:

1. Repel-Reuse: Repel/Super/Max prompt, Yes/No, item consumption and step reset.
2. Auto-run / running indoors: L toggle after running is available, indoor/outdoor run behavior.
3. TM/HM handling: reusable TM remains owned; HM field-use convenience still respects badge/location checks.
4. Item acquire presentation: normal item and hidden item icon/description clear correctly.
5. Runtime Options: Page 2/3 navigation and dirty-row save behavior.

Explicit exclusions for that first block:

- No hidden-sparkle implementation.
- No Field Item writer change.
- No itemball graphics change.
- No New Game script shortening.
- No DPE work.
- No binary patch ports.
