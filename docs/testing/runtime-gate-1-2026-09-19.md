# Runtime Gate 1 — targeted post-integration smoke

**Recorded:** 2026-09-19

**Evidence classification:** **CONFIRMED USER-SUPPLIED RUNTIME PASS**.

**Revision status:** **UNKNOWN / not revision-bound**. The user reported that
all rows below passed, but did not provide the exact workspace, component,
configuration, emulator, or run revisions. The repository therefore records
the report without treating it as acceptance of the current pins.

This is a sanitized evidence record. It does not add emulator observations,
ROM/save/state details, screenshots, private paths, hashes or raw logs.

## Revision binding

The documentation branch was based on `origin/main` at
`85a963626791ff8ccbfad63bec04b2733558d41e`, the Workspace #494 merge inspected
before this documentation change. Its integrated Gitlinks were:

| Identity | Integrated revision in the inspected workspace | Exact revision used by the reported run |
|---|---|---|
| Workspace | `85a963626791ff8ccbfad63bec04b2733558d41e` | **UNKNOWN** |
| CFRU Expansion | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` | **UNKNOWN** |
| DPE Gen 9 | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` | **UNKNOWN** |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` | **UNKNOWN** |

The current integration pins are repository facts, not proof that the private
runtime run used those exact revisions. No stronger revision-specific
acceptance statement is made until the tested identities are supplied.

## User-reported results

Every row below is recorded as **PASS — user supplied**. The wording is limited
to the scope reported by the user; no additional cases or observations are
inferred.

| Gate area | Reported PASS scope |
|---|---|
| Premier Ball behavior | Quantities, capacity and cancellation controls passed. |
| Modernized learnsets | Representative learnsets passed, including Pikachu, Rotom, Necrozma, Zacian/Zamazenta and a Gen-9 sample. |
| Learnset/UI persistence | Start moves, level-up, Move Reminder, Summary and save/reload passed. |
| UPR-FVX integration | ROM recognition and randomization passed. |
| Pickup unchanged path | `Pickup = Unchanged` passed. |
| Randomized output | The randomized output started successfully. |
| Randomized gameplay representatives | Starter, wild and trainer paths passed. |
| Data preservation | Tested Stats, Learnsets and Abilities were retained. |
| Unsupported Pickup randomization | The unsupported Pickup-randomization request was rejected cleanly. |

## Gate status and boundary

- **User-reported Gate 1 result:** PASS.
- **Revision-bound Gate 1 acceptance:** UNKNOWN until the tested SHA set is
  recorded.
- **Broad feature-complete/playthrough status:** not established by this gate.
- **ROM feature-complete, ROM frozen, stable support profile and complete
  Gen-1–9 compatibility:** not claimed.
- Missing Gen-9 battle mechanics remain outside the pilot contract.

The exact tested SHA set, test configuration and sanitized run label are the
only missing binding fields for promoting this report beyond a user-supplied,
revision-unbound PASS. The full manual acceptance block remains separate in
[M-014](../milestones/M-014.md).
