# Runtime Gate 1 — targeted post-integration smoke

**Recorded:** 2026-09-19

**Evidence classification:** **CONFIRMED USER-SUPPLIED REVISION-BOUND RUNTIME PASS**.

**Revision status:** **REVISION-BOUND** to the supplied Workspace/test basis and
component SHAs below. The successful run predates this documentation commit;
the documentation commit that introduced this report is
`264d30505db4da820a3f1289470d8dedbf7ce0e5` and is not the tested Workspace
revision. This report binds only the targeted Gate 1 scope to the four
recorded revisions.

This is a sanitized evidence record. It does not add emulator observations,
ROM/save/state details, screenshots, private paths, artifact hashes or raw logs.

## Revision binding

The successful Runtime Gate 1 run was executed before this documentation
commit against the then-integrated Workspace/test basis. The exact revisions
used by the reported run were:

| Identity | Exact revision used by the reported run |
|---|---|
| Workspace/test basis | `85a963626791ff8ccbfad63bec04b2733558d41e` |
| CFRU Expansion | `8bc8c38210ddba0b05c933dbda06cb4539254c7a` |
| DPE Gen 9 | `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc` |
| UPR-FVX | `0e3be63e94e34215cc35308d64e8db15e9a3c48c` |

These four revisions are the pre-documentation integrated pins against which
the private runtime run was performed. The later documentation commit is not
itself claimed as a runtime-tested Workspace revision.

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
- **Revision-bound Gate 1 acceptance:** PASS for the targeted scope on the
  four-revision set recorded above.
- **Broad feature-complete/playthrough status:** not established by this gate.
- **ROM feature-complete, ROM frozen, stable support profile and complete
  Gen-1–9 compatibility:** not claimed.
- **Tracker start/activation:** not performed by this gate.
- Missing Gen-9 battle mechanics remain outside the pilot contract.

The full manual acceptance block remains separate in
[M-014](../milestones/M-014.md).
