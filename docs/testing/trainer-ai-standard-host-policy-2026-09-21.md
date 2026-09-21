# Standard Trainer AI host policy — deterministic evidence

Date: 2026-09-21. Contract: Workspace Issue #510. Result:
**`STANDARD_AI_HOST_POLICY_READY`**, subject to review and user merge.

## Revision and scope

| Item | Value |
|---|---|
| Workspace source basis | `2a3ca0a81103ec5b4cc9335f83385a4b2ebfe7ff` |
| Branch | `ai/510-standard-host-policy` |
| Validated implementation commit | `9d55096fe9fcdf1f7720cbe611ffccfe254b7222` |
| Final branch commit | The commit containing this evidence file; its exact SHA is recorded in the Workspace PR and sanitized #510 evidence comment after creation. A commit cannot contain its own SHA. |
| Retained fixture schema/config | `ai-policy-fixture-v1` / `host-contract-v1` |
| Standard fixture schema/config | `ai-policy-fixture-v2` / `standard-host-policy-v1` |
| Dependencies | Python standard library only |

Evidence classification: the commands and results in this report are
**CONFIRMED CURRENT STATE** for the branch and implementation revision above.
The candidate facts are synthetic referee declarations. A future CFRU
mechanics/observation adapter and runtime policy remain **INTENDED FUTURE
STATE**.

The implementation is confined to `07_scripts/ai_policy/` plus this report.
Changed implementation files are:

- contract documentation and identifiers: `README.md` and `__init__.py`;
- CLI, memory, metrics, observation, runner, and schema modules;
- new `standard.py` policy module;
- new `fixtures/standard_fixtures.json` corpus;
- new `tests/test_standard_policy.py` regression suite.

The original `fixtures/synthetic_fixtures.json` file is unchanged. No generated
JSONL, Python cache, raw result, private data, or binary is committed.

## Implemented policy contract

Policy ID `standard` implements the competent, reactive, shallow and fair
profile over source-authored synthetic facts:

- the accepted #508 hard floor and robust-safe-KO dominance run before scoring;
- HP utility uses exact 1/256 fixed-point integers and division toward zero;
- `net_faints` is bounded to `[-1, 1]`, immediate future gain to `[-40, 40]`,
  HP terms to their documented ranges, and costs to non-negative signed int32;
- the exact expression fits signed int64 and the final total clamps once to
  signed int32; non-integers and out-of-range values fail closed;
- status, setup and recovery receive no class bonus: only declared current HP,
  one-follow-up marginal gain, and declared costs enter utility;
- there is no recursive search, submitted-action prediction, hidden-state read,
  speculative opponent switch prediction, or omniscience;
- voluntary switches require a referee-certified emergency/dominance flag;
  forced replacement is distinct, entry-KO switches remain floor-invalid, and
  a proposed A-to-B-to-A reversal is guarded without a positive exception;
- the epsilon-8 near-best set is formed only after floor, KO dominance and
  Standard switch admission, then sampled uniformly with stable action IDs and
  the deterministic rejection-sampled policy RNG;
- a singleton near-best set consumes zero draws; a multi-action set performs
  one bounded selection and records its raw draw count;
- canonical trace diagnostics include total utility, every term, saturation,
  admission/exclusion reasons, Standard eligibility, near-best membership,
  selected action, and RNG pre/post/draw state.

The v2 document is a separate strict schema. It does not reinterpret v1. Its
private state is never projected; twin tests compare observations, hashes,
candidate contracts, Standard score diagnostics, draw counts and actions using
the same explicit policy seed.

## Exact commands and results

All commands were run from the Workspace root. They require no component build,
ROM, save, emulator, state, screenshot, network service, or third-party Python
package.

```sh
python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'
```

Result: **PASS — 71 tests, 0 failures, 0 errors**. This includes all 53 #508
tests plus 18 Standard tests.

```sh
python3 07_scripts/ai_policy/cli.py validate
```

Result: **PASS — 59 fixtures**: 29 retained v1 fixtures plus 30 Standard v2
fixtures.

```sh
python3 07_scripts/ai_policy/cli.py run --policy standard --replicate 0 | sha256sum
python3 07_scripts/ai_policy/cli.py run --policy standard --replicate 0 | sha256sum
```

Both complete 30-line canonical streams produced
`227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85`.

```sh
python3 07_scripts/ai_policy/cli.py replay \
  --fixture-id standard_equal_four --policy standard --replicate 37
```

Result: **PASS — byte-identical replay**, one policy draw.

```sh
python3 07_scripts/ai_policy/cli.py summarize --policy standard --replicate 0
```

Result: **PASS** with the acceptance metrics below.

The synthetic baseline comparison used the same v2 corpus:

```sh
for policy in standard uniform_legal ko_first_no_switch first_legal; do
  python3 07_scripts/ai_policy/cli.py \
    --fixtures 07_scripts/ai_policy/fixtures/standard_fixtures.json \
    summarize --policy "$policy" --replicate 0
done
```

Legacy baseline compatibility was checked with:

```sh
python3 07_scripts/ai_policy/cli.py run \
  --policy uniform_legal --replicate 0 | sha256sum
```

Result: the #508 digest remains exactly
`71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7`.

Final handoff commands are:

```sh
git diff --check
python3 07_scripts/bootstrap/check_git_safety.py
git diff --raw 2a3ca0a81103ec5b4cc9335f83385a4b2ebfe7ff...HEAD
git submodule status
```

The final results are recorded after the evidence commit and before push/PR.

## Fixture inventory

All 29 #508 fixtures remain present and unchanged. The 30 Standard fixtures
carry 28 distinct coverage tags. They cover:

- robust KO versus strong utility and meaningful damage versus low-marginal
  Accuracy reduction;
- useful first Accuracy reduction, diminished later value, alternating
  Sand Attack/Smokescreen family memory, and the two-success repeat guard;
- useful and useless String Shot order changes;
- useful and capped/useless setup;
- useful and full-HP/futile recovery;
- useful and redundant major status;
- emergency switch, rejected non-emergency tactical switch, rejected entry-KO
  switch, A-to-B-to-A loop guard, and separate forced replacement;
- unique best, inside epsilon, exact epsilon boundary, just outside epsilon,
  and equal two/four-way choices;
- hidden-information and submitted-action twin pairs;
- deterministic all-futile fallback;
- exact int32 saturation plus out-of-bounds and non-integer rejection.

Every Standard fixture carries an independently authored allowed-best set and
forbidden actions. These are behavioral oracles for the synthetic contract, not
mechanics parity claims.

## Standard acceptance metrics

| Metric | Result |
|---|---|
| Decisions | 30 |
| Fixture allowed-best / oracle agreement | 30 / 30; 1.0 |
| Illegal selections | 0 / 30; 0.0 |
| Known invalid/no-effect selections | 0 / 29 productive opportunities; 0.0 |
| Missed robust KOs | 0 / 1 opportunity; 0.0 |
| Redundant-status selections | 0 / 2 opportunities; 0.0 |
| Harmful repeated-status selections | 0 / 1 opportunity; 0.0 |
| Non-emergency voluntary switches | 0 / 1 targeted opportunity; 0.0 |
| Near-best compliance | 30 / 30; 1.0 |
| Chosen utility | average 30.5667; median 25; range -30 to 300 |
| Regret from best Standard-eligible action | average/median/max 0 / 0 / 0 |
| Policy RNG draws | 8 total; 22 zero-draw and 8 one-draw decisions; max 1 |
| Hidden-information twin mismatches | 0 |
| Submitted-action twin mismatches | 0 |
| Deterministic replay mismatches | 0 |

The extreme valid cost witness clamps to exactly `-2147483648`, is marked
`saturated: true`, and is not selected. Future gain `41`, cost `2147483648`,
and a floating HP term are independently rejected. A floor-excluded action is
never Standard-eligible or near-best even when its declared utility is high.

## Near-best entropy

Across replicate indices 0 through 1023:

| Fixture | Counts | Normalized entropy | Gate |
|---|---:|---:|---|
| Equal two-way | `equal_a=544`, `equal_b=480` | 0.997180399 | PASS; each within 5 points of 50% |
| Equal four-way | `285, 241, 251, 247` | 0.998421079 | PASS; each within 5 points of 25% |

The inside-epsilon and exact-boundary pairs consume one draw. The unique-best
and just-outside-epsilon fixtures consume zero draws. Invalid actions never
enter any near-best set.

## Synthetic baseline comparison

The average/median utility columns below exclude only the explicit saturation
bounds witness so that an int32-min test does not dominate an otherwise small
synthetic corpus. The canonical CLI summaries retain that witness and its exact
raw aggregate. Regret uses each policy's own hard-floor-eligible set; Standard
also applies its switch admission.

| Policy | Allowed-best | Utility average / median | Regret average / median / max | Near-best reference | RNG draws |
|---|---:|---:|---:|---:|---:|
| `standard` | 30 / 30 | 31.6207 / 25 | 0 / 0 / 0 | 30 / 30 | 8 |
| `uniform_legal` | 21 / 30 | 20.7931 / 24 | 11.4828 / 0 / 270 | 21 / 30 | 21 |
| `ko_first_no_switch` | 23 / 30 | 19.5517 / 25 | 12.7241 / 0 / 270 | 23 / 30 | 0 |
| `first_legal` | 23 / 30 | 19.3103 / 25 | 12.9655 / 0 / 270 | 23 / 30 | 0 |

All four policies have zero illegal, known-no-effect, missed-robust-KO,
redundant-status, harmful-repeat and deterministic-replay errors because the
shared hard floor remains active. `uniform_legal` selects the deliberately
high-utility non-emergency switch in its targeted witness; Standard excludes it.

Fixture-level baseline allowed-best misses are:

- `uniform_legal` (9): `standard_accuracy_first_useful`,
  `standard_accuracy_diminishing`, `standard_string_shot_flip`,
  `standard_major_status_useful`, `standard_switch_emergency`,
  `standard_switch_tactical_rejected`, `standard_switch_loop_guard`,
  `standard_unique_best`, and `standard_extreme_saturation`;
- `ko_first_no_switch` (7): `standard_accuracy_first_useful`,
  `standard_string_shot_flip`, `standard_setup_useful`,
  `standard_recovery_useful`, `standard_major_status_useful`,
  `standard_switch_emergency`, and `standard_extreme_saturation`;
- `first_legal` (7): `standard_damage_vs_low_accuracy`,
  `standard_string_shot_flip`, `standard_setup_useful`,
  `standard_recovery_useful`, `standard_major_status_useful`,
  `standard_switch_emergency`, and `standard_extreme_saturation`.

This is a synthetic policy-contract comparison, not a battle simulation or
evidence that Standard is stronger in gameplay.

## GitHub Project state

The user Project `FireRed Gen 9 Randomizer — Pilot Finish` was verified after
the bounded field updates:

- #508: `P0`, `Done`;
- #510: `P0`, `Integration`, `Doing`;
- #498: `P0`, `Blocked`;
- #499: unchanged at `P1`, `Backlog`;
- #500: unchanged at `P1`, `Backlog`.

## Limitations and non-claims

The v2 facts are synthetic referee inputs. The harness does not derive damage,
order, survival, marginal value, emergency qualification, or utility costs from
CFRU. There is no battle transition engine, general matchup switching,
opponent prediction, randomized-team tournament, runtime timing measurement, or
player-experience evidence in this contract.

Explicitly:

- no CFRU Standard AI runtime claim;
- no Ironmon Smart claim or exact NatDex patch-parity claim;
- no Expert or Omniscient Challenge policy claim;
- no gameplay or tournament-strength claim;
- no `ROM_PROFILE_READY`;
- no Randomizer R2 authorization;
- #498 remains Blocked; #499/#500 remain unchanged/downstream;
- no ROM, save, emulator state, build, tool binary, screenshot, private path,
  `.env`, token, key, secret, emulator, runtime, or Tracker was accessed or used;
- no CFRU, DPE, UPR-FVX, component file, or Gitlink changed;
- no PR is merged and no upstream PR is opened;
- `UPSTREAM_CONTRIBUTION = DEFERRED`.
