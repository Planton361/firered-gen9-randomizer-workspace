# Draft PR reconciliation — 2026-09-19

**Evidence classification:** **CONFIRMED CURRENT STATE** for GitHub metadata,
Gitlinks and merged history inspected on 2026-09-19. Runtime rows are
**CONFIRMED USER-SUPPLIED REVISION-BOUND RUNTIME PASS** only as recorded in
[Runtime Gate 1](../testing/runtime-gate-1-2026-09-19.md); that report records
their exact tested revisions.

## Current comparison base

`origin/main` is `85a963626791ff8ccbfad63bec04b2733558d41e` (Workspace PR #494
merge), following Workspace PR #493 merge
`6665a4816e5f5d252d5fc5d6af85487f44086e7a`.
The authoritative current Gitlinks in that tree are:

| Component | Current Gitlink |
|---|---|
| CFRU | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` |
| DPE | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |

CFRU #45 (M-013) and CFRU #48 (coherent learnsets) are contained in the
current CFRU pin. UPR-FVX #185 is contained in the current UPR pin. No Gitlink
is changed by this documentation closure.

## Open Workspace Draft PRs

All six PRs remain open and draft as inspected. Their heads and stale/current
dispositions are recorded without changing or closing those PRs.

| PR | Draft head | Superseded or still-valid statement | Current disposition |
|---|---|---|---|
| [#487](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/487) | `559013955f6b25848748579a75523a40c1539fca` | Its `7437cd5`/CFRU `827fa1e` baseline and CFRU #46 five-table restoration candidate predate merged Workspace #493 and CFRU #48. | **SUPERSEDED for current data status.** Its source inventories remain historical evidence; they do not establish complete Gen-1–9 support. |
| [#488](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/488) | `44ea58b376d976edf22d13833d0a2f214f6ee01a` | Its UPR `1a597a6`/candidate `0df4ed3` context predates UPR-FVX #185 merge `0e3be63`. Its Pickup guard is now integrated. | **SUPERSEDED for current pin/status.** The user-reported Gate 1 covers targeted Pickup/output rows; the full feature matrix remains open. |
| [#489](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/489) | `391a200a20bd217feee9ca9b973b200c089e6de1` | “All cases NOT_RUN” is no longer true for the user-reported Gate 1 subset. The full A–H package was not thereby passed. | **RETAIN as historical test-package source;** M-014 is the current refreshed bounded block. |
| [#490](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/490) | `fd4835905a48c0135562e66327208ee2c22288b4` | Its “pins unchanged”, old M-013 pending status and pre-#494 baseline are stale. Its no-freeze/no-feature-complete boundary remains valid. | **SUPERSEDED for pin/readiness facts;** freeze and broad acceptance remain open. |
| [#491](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/491) | `d6034ae39cbc2e5a551289db685f4687388ce59d` | Its tracker discovery is design-only and uses the pre-#494 identity. Gate 1 did not activate Tracker or establish a freeze. | **STILL FUTURE / not activated.** Keep outside this closure and M-014. |
| [#492](https://github.com/Planton361/firered-gen9-randomizer-workspace/pull/492) | `0d071dba7d788be7be1f937ef360878e2f1f3671` | Its M-013 candidate `d8468e1` and old CFRU `827fa1e` baseline are now in the integrated CFRU #45 → #48 ancestry. Its runtime-pending wording predates the user report. | **SUPERSEDED for implementation status;** the reported Premier rows are now revision-bound by Gate 1's supplied integrated revision set. |

## Historical handling

The old Draft PR branches and reports are not rewritten or promoted. Their
source/static findings remain useful when explicitly read as historical or
superseded evidence. Current integration facts are in
[M-013](../milestones/M-013.md) and current runtime evidence is in
[Runtime Gate 1](../testing/runtime-gate-1-2026-09-19.md).
