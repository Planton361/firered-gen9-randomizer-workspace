# Ironmon Smart v1 host policy — deterministic evidence

Date: 2026-09-21. Contract: Workspace Issue #515. Result:
**`IRONMON_SMART_HOST_POLICY_READY`**, subject to review and user merge of the
Workspace PR.

## Revision identity and scope

| Item | Value |
|---|---|
| Workspace source basis | `6b940684b8af79f5cbfd8ecd03dd443d1900a650` |
| Branch | `ai/515-ironmon-smart-host-policy` |
| Initial implementation commit | `24e2ddd7e1a7a1c6eb4244e5dd06e71e931af41c` |
| CONTROL-reviewed head | `5a33898f436c4d6ec0fdb4361441fc5201857796` |
| Repaired implementation commit | `401d64b0f4386260c507a14456b47dd2544acbef` |
| Final branch commit | The commit containing this evidence file; its exact SHA is recorded in the Workspace PR and sanitized #515 evidence comment. A commit cannot contain its own SHA. |
| Ironmon fixture schema | `ai-policy-fixture-v3` |
| Ironmon policy/config | `ironmon_smart` / `ironmon-smart-host-policy-v1` |
| Dependencies | Python standard library only |

Evidence classification: the implementation, fixtures, commands, and results
in this report are **CONFIRMED CURRENT STATE** for the revisions above. The
candidate facts are source-authored synthetic referee declarations. CFRU
Ironmon runtime behavior, mechanics-adapter parity, target performance,
settings/defaults, and gameplay strength remain **INTENDED FUTURE STATE** or
**UNKNOWN** as stated under limitations.

This is Workspace-only host-policy work. It does not change CFRU, DPE,
UPR-FVX, Ironmon Tracker, NatDexExtension, any Gitlink, settings/defaults,
trainer data, ROM source, or runtime behavior. Exact changed files are:

- `07_scripts/ai_policy/README.md`;
- `07_scripts/ai_policy/__init__.py`;
- `07_scripts/ai_policy/cli.py`;
- `07_scripts/ai_policy/fixtures/ironmon_fixtures.json`;
- `07_scripts/ai_policy/ironmon.py`;
- `07_scripts/ai_policy/metrics.py`;
- `07_scripts/ai_policy/observation.py`;
- `07_scripts/ai_policy/runner.py`;
- `07_scripts/ai_policy/schema.py`;
- `07_scripts/ai_policy/tests/test_ironmon_policy.py`;
- `docs/testing/trainer-ai-ironmon-smart-host-policy-2026-09-21.md`.

The same-contract repair after CONTROL review changed exactly:

- `07_scripts/ai_policy/README.md`;
- `07_scripts/ai_policy/fixtures/ironmon_fixtures.json`;
- `07_scripts/ai_policy/ironmon.py`;
- `07_scripts/ai_policy/metrics.py`;
- `07_scripts/ai_policy/tests/test_ironmon_policy.py`;
- this evidence document.

## Implemented contract

The separate `ironmon_smart` policy retains the accepted common floor before
any tactical or switch arbitration: legal actions, known no-effect and
redundancy exclusion, robust-safe-KO dominance, four-decision repeat memory,
entry survival, forced-action handling, deterministic all-futile fallback,
fair observation, and a policy RNG isolated from battle/future RNG.

The v3 policy adds:

- strict ordinary Trainer Singles input with at most nine roots, at most eight
  response branches per root, one analytical future tail, and no recursion;
- signed integer utility with 1/256 HP fractions, toward-zero division,
  one-half future discount, nonterminal credit capped at 40, one-quarter
  branch-range uncertainty cost capped at 25, and final int32 saturation;
- no generic status/setup/recovery/field/move-class bonus: tactical value comes
  only from represented branch outcome differences;
- revealed-move-only response weights with add-one smoothing, exact 25%
  aggregate `UNKNOWN` mass while slots remain unknown, 100% `UNKNOWN` when no
  move is known, and zero speculative opponent-switch weight;
- computed repeat cost `8 * min(3, successful_repeats)` and a named exception
  gate requiring at least +8 after cost over the best productive alternative;
- emergency, forced, and non-emergency switch paths; exact advantage boundaries
  below 12, 12–19, and at least 20; one policy-RNG admission draw in the middle
  band; per-candidate +12 eligibility before epsilon-4 sampling; and individual
  strict-dominance filtering of emergency candidates when a stay is defensible;
- A-to-B-to-A cost 16, changed-public-threat and independently scored +8
  progress exceptions, a two-consecutive-switch guard, and rejection of
  Regenerator-only progress;
- canonical public traces with response facts/weights, branch utilities,
  uncertainty, repeat proof, loop facts, best stay/switch, every candidate's
  score/advantage and threshold eligibility, admitted replacement pool,
  admission RNG, tactical class, near-best set, total RNG state, and selection.

The v1 and v2 loaders and trace paths remain separate. V3 rejects unknown or
missing fields, floats anywhere in the document, nonzero opponent-switch
weight, response/model mismatches, malformed compact branches, out-of-range
integers, more than nine root actions, and more than eight response branches.

## Fixture and mandatory-tag inventory

The repaired corpus contains 63 v3 Ironmon fixtures and 58 distinct explicit
coverage tags. Together with the retained 29 v1 and 30 v2 fixtures, validation
covers 122 fixtures. The machine-checked tag inventory is:

```text
aba_loop_prohibition
accuracy_repeat_residual_exception
all_futile_fallback
all_revealed_no_unknown
already_faster
changed_public_threat_exception
choice_encore_safe_switch
consecutive_switch_guard
deterministic_switch_admission
emergency_switch
entry_hazard_cost
entry_ko_switch_rejection
epsilon_4_boundaries
equal_action_entropy
forced_revenge_replacement
frequency_add_one_smoothing
futile_recovery
future_rng_twin
hidden_ability_twin
hidden_bench_twin
hidden_item_twin
hidden_move_twin
hidden_state_twin
hidden_stats_twin
high_roll_false_ko
immediate_robust_ko_vs_tactical
no_useful_bench
pointless_regenerator_loop
preserve_vs_sacrifice
priority_trick_room_counterexample
productive_regenerator_exception
public_reveal_transition
recovery_residual_survival_race
residual_combinations
revealed_absorber_hidden_twin
revealed_one_plus_unknown
seed_yawn_duplicate_rejection
setup_3hko_to_2hko
setup_no_matching_attack
singleton_zero_draw
speed_repeat_no_exception
stable_action_id_order
submitted_action_twin
supported_2hko
supported_field_protect_pivot
switch_advantage_11
switch_advantage_12
switch_advantage_19
switch_advantage_20
switch_candidate_min_advantage
toxic_residual_line
trapped_lock_no_switch
two_speed_drops
two_speed_drops_no_survival
unknown_response_100
unsupported_tactical_unknown
voluntary_revenge_takes_hit
zero_speculative_switch_prior
```

This includes separate twins where only hidden moves, item, ability, exact
stats, or unseen bench changes, plus independent submitted-action and
future-RNG pairs.

## Exact verification and digests

All commands run from the Workspace root without a component build, ROM, save,
emulator, state, screenshot, network service, or third-party package.

```sh
python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_*.py'
```

Result: **PASS — 98 tests, 0 failures, 0 errors**. This retains all 71 #508/#510
tests and runs 27 Ironmon tests, including the three repair-specific test
methods.

```sh
python3 -m unittest discover -s 07_scripts/ai_policy/tests -p 'test_ironmon_policy.py'
python3 07_scripts/ai_policy/cli.py validate
```

Results: **PASS — 27 Ironmon tests**; **PASS — 122 fixtures across explicit
v1/v2/v3 schemas**. Mandatory tag inventory, malformed-v3 fail-closed cases,
integer arithmetic, saturation, response weights, repeat/loop rules, switch
boundaries, noninterference, entropy, and baseline replay are included.

```sh
python3 07_scripts/ai_policy/cli.py run --policy uniform_legal --replicate 0 | sha256sum
python3 07_scripts/ai_policy/cli.py run --policy standard --replicate 0 | sha256sum
python3 07_scripts/ai_policy/cli.py run --policy ironmon_smart --replicate 0 | sha256sum
```

Canonical digests:

| Stream | SHA-256 | Disposition |
|---|---|---|
| #508 v1 `uniform_legal` | `71fc84c8fd3e219c4e364ecd506127303ac8524a73d47a39999be384efbc95a7` | unchanged |
| Standard v2 | `227ecebc2b937671cc4f2fbab1694abf1b7c186f7e455ed7daf22014b62d0a85` | unchanged |
| Ironmon Smart v3 | `0a637d0bc42cb2e37701bbfa33677ae95c878b1f9a67ec55a60e15a4fbdb85d7` | repaired frozen canonical stream |

```sh
python3 07_scripts/ai_policy/cli.py replay \
  --fixture-id ironmon_equal_four --policy ironmon_smart --replicate 37
```

Result: **PASS — byte-identical replay**, one policy draw. Every v3 fixture is
also replayed in the test suite at replicate 37 with zero mismatch.

## Ironmon metrics

`python3 07_scripts/ai_policy/cli.py summarize --policy ironmon_smart --replicate 0`
reported:

| Metric | Result |
|---|---|
| Decisions / allowed-best compliance | 63; 63 / 63, 1.0 |
| Illegal selections | 0 / 63 |
| Known invalid/no-effect selections | 0 / 62 productive opportunities |
| Missed robust KO | 0 / 1 |
| Redundant status | 0 / 2 |
| Harmful repeat | 0 / 1 |
| Switch-threshold violations | 0 / 16; below-threshold selections 0 |
| Switch-loop-guard violations | 0 / 3 |
| Near-best compliance | 63 / 63, 1.0 |
| Deterministic replay mismatches | 0 |
| Policy-eligible utility regret | average `0.1269841`; median `0`; max `4` |
| Fixture-allowed utility regret | average `0.8253968`; median `0`; max `19` |
| Policy RNG draws | 19 total; 44 zero-draw, 19 one-draw; max 1 |

The fixture-allowed regret maximum of 19 is the intentional 12–19 stochastic
switch-admission band: a rejected switch remains an oracle-allowed result. The
post-arbitration near-best regret remains at most epsilon 4.

### Response model

- no revealed moves: 57 cases, `UNKNOWN` weight 1 / 100%;
- partially revealed moves: 5 cases, exact aggregate `UNKNOWN` mass 25%;
- fully revealed moves: 1 case, no `UNKNOWN` branch;
- maximum represented response branches: 3;
- one-known initial weights: revealed `3`, `UNKNOWN` `1`;
- add-one frequency witness: `TACKLE=9`, `GROWL=3`, `UNKNOWN=4`;
- uncertainty witness: expected branch utility 56, range 100, cost 25,
  final utility 31;
- speculative opponent-switch weight sum: **0**;
- legitimate public reveal changes the observation hash, response weights, and
  selected line, with `REVEALED_MOVE:TACKLE` in the public trace.

### Switch, repeat, and loop evidence

- advantage 11: reject; exactly 12 and 19: `random_12_19`; exactly 20:
  deterministic admission;
- repaired +12/+8 witness: class `random_12_19`; only +12 is threshold
  eligible and in the admitted/near-best replacement pool; +8 is excluded;
- repaired +13/+9 witness: only +13 is threshold eligible and in the admitted
  replacement pool; +9 is excluded;
- repaired +20/+16 witness: deterministic class admission consumes no
  admission draw; both candidates independently clear +12 and remain in the
  epsilon-4 replacement pool; stable-ID sampling selected +16 at replicate 0
  with its normal single near-best draw;
- repaired emergency witness: the +4 candidate strictly dominates stay=0 and
  is the sole emergency replacement; the within-epsilon candidate at 0 does
  not dominate and is excluded before sampling;
- 1,024 deterministic seeds for repaired +12/+8: **491 admit / 533 reject**,
  entropy `0.9987861499`; the admission draw count and full policy draw count
  are both exactly one for every seed; replay mismatches 0; +8 selections 0;
  invalid selections 0;
- the retained single-candidate +12 witness remains **502 admit / 522 reject**,
  entropy `0.9997248103`, with exactly one admission draw and zero replay
  mismatches;
- the strengthened metric audits each candidate's public score, own advantage,
  and threshold eligibility and reports **0 / 16 switch-threshold violations**
  and **0 below-threshold selected candidates**;
- entry KO, hazard-reduced advantage, trapped lock, and no-useful-bench cases
  reject unsafe/unhelpful switching;
- forced revenge and voluntary revenge timing are distinct; preserve/sacrifice
  and revealed absorber cases pass;
- two normalized Accuracy-family successes produce repeat cost 16; the residual
  win exception scores 49 against alternative 20 after cost, records its named
  reason and +29 margin; lowering the margin rejects the exception;
- repeated Speed-family use without a certified threshold is excluded;
- A-to-B-to-A records cost 16 and is prohibited without a valid exception;
  changed public threat and independent +8 progress pass; third consecutive and
  Regenerator-only switching fail; forced switches do not consume the budget.

### Epsilon and entropy

The epsilon witness admits utilities 100, 98, and 96, and excludes 95. The
singleton consumes zero draws. Stable action IDs sort equal alternatives as
`equal_a`, `equal_b`, `equal_c`, `equal_d`.

Across 1,024 deterministic seeds the equal-action counts were `245`, `256`,
`262`, and `261`; normalized entropy was `0.9997477605`, and every action was
within five percentage points of 25%. Floor-invalid actions were never sampled.

### Noninterference

With a common decision seed, all paired comparisons include fair observation,
observation hash, common-floor candidate contract, revealed response model,
branch scores, repeat/switch arbitration, RNG draws/state, and selected action.

| Twin category | Mismatches |
|---|---:|
| Hidden move/item/ability/exact-stat/unseen-bench | 0 |
| Submitted action/move/switch representation | 0 |
| Future/battle RNG | 0 |

## Synthetic baseline metrics

The same 63 v3 fixtures were summarized under the retained deterministic
baselines and the Standard policy. Utility below is the Ironmon fixture scale,
used only for descriptive accounting.

| Policy | Allowed-best | Chosen utility avg / median | Fixture-allowed regret avg / max | RNG draws |
|---|---:|---:|---:|---:|
| `ironmon_smart` | 63 / 63 | 30.7619 / 25 | 0.8254 / 19 | 19 |
| Standard | 47 / 63 | 22.0952 / 20 | 9.4921 / 280 | 27 |
| `uniform_legal` | 44 / 63 | 24.1429 / 25 | 8.9524 / 280 | 44 |
| `ko_first_no_switch` | 46 / 63 | 22.0794 / 20 | 9.5079 / 280 | 0 |
| `first_legal` | 49 / 63 | 27.7937 / 25 | 5.3016 / 110 | 0 |

All five runs are deterministic and have zero illegal selections, zero replay
mismatches, and zero hidden/submitted/future-RNG mismatches. These are authored
fixture-policy metrics, not simulated battles, rankings, or gameplay-strength
claims.

## Project metadata and repository safety

The user Project `FireRed Gen 9 Randomizer — Pilot Finish` was verified after
the bounded #515 updates:

- #513: `P0`, `Integration`, `Done`;
- #515: `P0`, `Integration`, `Doing`;
- #498: `P0`, `Runtime Acceptance`, `Blocked`;
- #499: unchanged at `P1`, `Tracker-BizHawk`, `Backlog`;
- #500: unchanged at `P1`, `Tracker-BizHawk`, `Backlog`;
- #501: unchanged at `P1`, `Release`, `Backlog`.

Final handoff checks are:

```sh
git diff --check
python3 07_scripts/bootstrap/check_git_safety.py
git diff --raw 6b940684b8af79f5cbfd8ecd03dd443d1900a650...HEAD
git submodule status --recursive
git status --short
```

The final results are recorded after this evidence commit in the PR and #515
handoff. The raw Workspace comparison must contain no mode-160000 entry. The
authoritative Component identities remain:

- CFRU `dfcfb9901ea725c6856a1aca6a5a6faf62f0bcbd`;
- DPE `22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc`;
- UPR-FVX `0e3be63e94e34215cc35308d64e8db15e9a3c48c`;
- Ironmon Tracker `c450ecaee2d8131a2789bb656e3be792a93712fb`;
- NatDexExtension `a94b8844800308248bb5090b6c36c8b2d7e5d7b9`.

## Limitations and non-claims

The v3 facts are synthetic. The harness does not derive damage, order,
survival, effect semantics, response priors, or switch-entry outcomes from
CFRU. Unsupported tactical effects remain conservative/unknown. There is no
recursive battle search, transition engine, target-cycle/RAM measurement,
full tournament, player-experience evidence, or runtime acceptance.

This result explicitly does not claim:

- exact NatDex patch parity;
- CFRU Ironmon Smart implementation or runtime behavior;
- Standard/default/settings changes;
- Expert or Omniscient implementation;
- gameplay strength or a support ranking;
- `ROM_PROFILE_READY`, Randomizer R2 authorization, BizHawk readiness, or
  Ironmon Tracker readiness;
- implementation of unsupported Gen-9 mechanics;
- a merged PR, release, or final freeze.

No ROM, save, emulator state, generated build, tool binary, screenshot, private
path, `.env`, token, key, secret, emulator, or Tracker was accessed or used. No
Component file, Gitlink, setting/default, or upstream PR changed. No PR is
merged. `UPSTREAM_CONTRIBUTION = DEFERRED`.
