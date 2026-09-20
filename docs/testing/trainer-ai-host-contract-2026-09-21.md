# Trainer AI host policy harness — deterministic contract evidence

Date: 2026-09-21. Contract: Workspace Issue #508. Result:
**`AI_HOST_CONTRACT_READY`**, subject to review and user merge.

## Revision and scope

| Item | Value |
|---|---|
| Workspace source basis | `1e58214fd6364a0a76082328c52a4a40d3f41268` |
| Branch | `harness/508-trainer-ai-host-contract` |
| Validated implementation commit | `9a41930cb86ee8bfef9d73b118454bab60a93e91` |
| Final branch commit | The commit containing this evidence file; its exact SHA is recorded in the Workspace PR and sanitized #508 evidence comment after creation. A commit cannot contain its own SHA. |
| Python | `Python 3.14.7`; standard library only |
| Fixture schema | `ai-policy-fixture-v1` |
| Policy configuration | `host-contract-v1` |

Evidence classification: the commands and results in this report are
**CONFIRMED CURRENT STATE** for the branch/revisions above. The harness is an
executable specification/test double. Future CFRU policy behavior remains
**INTENDED FUTURE STATE**.

The implementation is confined to `07_scripts/ai_policy/` plus this report.
Changed files are:

- `.gitignore` and `README.md` for generated-cache exclusion and operator commands;
- package entry points: `__init__.py`, `__main__.py`, and `cli.py`;
- contract modules: `rng.py`, `schema.py`, `observation.py`, `memory.py`,
  `floor.py`, `policies.py`, `runner.py`, `trace.py`, and `metrics.py`;
- `fixtures/synthetic_fixtures.json`;
- test package and five `test_*.py` modules;
- `docs/testing/trainer-ai-host-contract-2026-09-21.md`.

No generated JSONL, test cache, raw result, private data, or binary is committed.

## Implemented contract

The harness supplies:

- exact uint32 xorshift32 with shifts 13/17/5, zero replacement
  `0x6D2B79F5`, and rejection-sampled bounded integers;
- SHA-256 seed derivation from UTF-8
  `schema|fixture_id|replicate|stream`, first four bytes little-endian;
- strict versioned JSON fixtures with exact derived seed fields;
- fail-closed rejection of malformed documents, incomplete/unknown fields,
  duplicate IDs, unknown schemas/configurations, malformed compact actions,
  reveal inconsistencies and contradictory truth/expectations;
- separate referee truth and fair/challenge observation projection;
- a common-floor reference contract for legality, known no-effect actions,
  robust KO dominance, redundant/capped/repeated status, forced actions,
  entry-KO switches and deterministic all-futile fallback;
- `uniform_legal`, `ko_first_no_switch`, and `first_legal` baselines, with no
  CFRU or Ironmon label;
- four-decision battle-local memory, normalized Accuracy/Speed families,
  forced/voluntary switch distinction and A→B→A loop detection;
- canonical sanitized JSONL with stable key order, observation hashes, floor
  reasons, candidate facts, selection and policy RNG pre/post/draw data;
- aggregate synthetic metrics and extension points without a tournament.

Challenge mode exposes only the authorized full opponent team facts represented
by this schema. Fair mode removes unrevealed moves, items, abilities, active
hidden stats and unseen bench identities. Both omit submitted player actions
and future RNG. Public-history fields and trace fields are allowlisted.

## Exact commands and results

All commands were run from the Workspace root. They require no network,
component build, ROM, emulator, save, or state.

```sh
python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'
```

Result: **PASS — 53 tests, 0 failures, 0 errors**.

```sh
python3 07_scripts/ai_policy/cli.py validate
```

Result: **PASS — 29 fixtures**, schema `ai-policy-fixture-v1`.

```sh
python3 07_scripts/ai_policy/cli.py run --policy uniform_legal --replicate 0 | sha256sum
python3 07_scripts/ai_policy/cli.py run --policy uniform_legal --replicate 0 | sha256sum
```

Both canonical streams produced
`71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7`.
No trace file was retained or committed.

```sh
python3 07_scripts/ai_policy/cli.py replay --fixture-id equal_four --replicate 37
```

Result: **PASS — byte-identical replay**, one policy draw.

```sh
python3 07_scripts/ai_policy/cli.py summarize --policy uniform_legal --replicate 0
```

Result: **PASS** with the synthetic metrics in the next section.

```sh
git diff --check
python3 07_scripts/bootstrap/check_git_safety.py
git diff --raw 1e58214fd6364a0a76082328c52a4a40d3f41268...HEAD
git submodule status
```

Final handoff result: diff check and repository safety **PASS**; raw comparison
contains no `160000` Gitlink entry; recursive component identities remain CFRU
`8bc8c38210ddba0b05c933dbda06cb4539254c7a`, DPE
`22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`, and UPR-FVX
`0e3be63e94e34215cc35308d64e8db15e9a3c48c`.

## Fixture inventory

There are 29 source-authored synthetic fixtures and 27 coverage tags. Required
families are covered as follows:

| Family | Fixture/tag evidence |
|---|---|
| Guaranteed KO vs Accuracy utility | `ko_vs_accuracy`; both Sand Attack and Smokescreen candidates |
| Accuracy neutral/lowered/capped | `accuracy_neutral`, `accuracy_lowered`, `accuracy_capped` |
| String Shot marginal order value | `string_shot_flip`, `string_shot_no_benefit` |
| Redundant status | `redundant_status` |
| Useful/capped setup | `useful_setup`, `capped_setup` |
| Full-HP recovery | `full_hp_recovery` |
| Known immunity/no-effect | `known_immunity` |
| Forced Choice/Encore-like action | `forced_choice` |
| Good emergency vs entry-KO switch | `emergency_switch` |
| A→B→A and forced replacement | `switch_loop` |
| Two/four equal actions | `equal_two`, `equal_four`; 1,024-seed entropy/balance tests |
| Hidden move/item/ability/bench | four twin groups, eight fixtures |
| Submitted action | one twin group, two fixtures |
| All-futile fallback | `all_futile` |
| Alternating Accuracy IDs/repeat family | `accuracy_alternating_repeat` |
| Challenge information boundary | `challenge_boundary` |

Hidden active IV/EV/nature/stat filtering is also tested by changing those truth
values without changing a fair observation. The Challenge test separately proves
that full-team authorization does not expose submitted actions or future RNG.

## Determinism and information results

- All 29 fixtures replay byte-identically.
- The two complete `run` streams have identical SHA-256 digests.
- Policy scoring/filtering consumes zero draws; only a multi-action stochastic
  choice consumes a documented draw.
- Hidden-information twin mismatches: **0**.
- Submitted-action twin mismatches: **0**.
- Fair twin comparison re-runs both sides with the same explicit policy seed and
  compares observations, hashes, candidate contracts, draw counts and actions.
- Reveal behavior is explicit: revealed facts alter the observation and add a
  stable `REVEALED_*` reason to the trace.

## Synthetic metric summary

The `uniform_legal` replicate-0 corpus result is:

| Metric | Result |
|---|---|
| Decisions | 29 |
| Illegal actions | 0 / 29; rate 0.0 |
| Invalid/no-effect selections | 0 / 27 productive opportunities; rate 0.0 |
| Missed robust KOs | 0 / 1 opportunity; rate 0.0 |
| Redundant-status selections | 0 / 2 opportunities; rate 0.0 |
| Harmful repeated-status selections | 0 / 1 opportunity; rate 0.0 |
| Switch-loop detections | 1 expected synthetic witness |
| Hidden-information twin mismatches | 0 |
| Submitted-action twin mismatches | 0 |
| Deterministic replay mismatches | 0 |

These results prove that the harness catches and accounts for its authored
oracles. They are not gameplay or comparative-strength measurements.

## Limitations and non-claims

The action facts, damage values, survival flags, order-flip result and robust-KO
status are synthetic referee declarations. There is no CFRU mechanics adapter,
transition engine, calibrated utility model, full switch policy, battle runtime,
or randomized-team tournament in this gate. The harness does not validate target
CPU/RAM timing and does not establish balance or player experience.

Explicitly:

- no Standard AI strength or implementation claim;
- no Ironmon Smart strength, implementation or exact-patch-parity claim;
- no Expert policy claim;
- no CFRU runtime or component behavior claim;
- no tournament claim;
- no `ROM_PROFILE_READY`;
- no Randomizer R2 authorization;
- #498 remains Blocked; #499/#500 remain unchanged/downstream;
- no ROM, save, emulator state, build, tool binary, screenshot, private path,
  `.env`, token, key, secret, emulator, or Tracker was accessed or used;
- no CFRU/DPE/UPR-FVX file or Gitlink changed;
- no PR is merged and no upstream PR is opened;
- `UPSTREAM_CONTRIBUTION = DEFERRED`.

Project metadata was verified/synchronized as #508 P0 / Integration / Doing and
#498 Blocked. The next eligible action is review and user merge of the Workspace
PR; any CFRU adapter or production policy requires a new bounded contract.
