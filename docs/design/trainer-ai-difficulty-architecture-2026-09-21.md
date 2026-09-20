# Trainer AI / difficulty architecture — design gate

Date: 2026-09-21. Contract: [Workspace #506](https://github.com/Planton361/firered-gen9-randomizer-workspace/issues/506).
Workspace source basis: `b1dc157a4cfb000c1fa14a0e3323210c350d767a`.
CFRU target: **`8bc8c38210ddba0b05c933dbda06cb4539254c7a`**, without substitution.

**Recommendation:** use a CFRU-native, bounded rule policy for pilot v1, with
one common competence floor, explicit observation filtering, marginal utility,
and a single move/switch arbiter. Start with a host-side contract and synthetic
fixtures before integrating the policy. Do not introduce ML or an emulator-side
controller into the pilot.

**CONFIRMED USER DECISION:** this contract is design/research only. It changes
one Workspace document, no component code or Gitlinks. No ROM, save, state,
build, tool binary, private artifact, model weights, or secret was needed.
No runtime, Randomizer R2, BizHawk/Tracker implementation, training, or merge.
`UPSTREAM_CONTRIBUTION = DEFERRED`.

**Evidence classification:** source findings below are **CONFIRMED CURRENT
STATE** at their listed revisions; historical observations are explicitly
separated. All algorithms, thresholds, profiles, defaults, budgets, and acceptance
criteria proposed here are **INTENDED FUTURE STATE**, awaiting review. There
are no measured candidate-policy results. Latency, balance, and eventual runtime
compatibility remain **UNKNOWN**. This is a source-backed comparison, not a
claim to have benchmarked or identified the strongest possible Pokémon AI.

The live #506 contract supersedes the broad AI exclusion in the earlier
[R0 audit](../audits/rom-finish-readiness-2026-09-20.md), but authorizes design
only. #498 remains blocked until this design is accepted and its separately
authorized implementation is validated; publishing this report does not grant
`ROM_PROFILE_READY`. #499/#500 remain downstream and unchanged.

## 1. Source register and reference roles

Public external heads were resolved to commits during this 2026-09-21 review.
“Current” below means that inspected snapshot, not a moving branch guarantee.
Only selected text sources were fetched; no release assets or model archives.
Use the commit links to reproduce the review.

| ID | Revision and inspected sources | Role / limitation |
|---|---|---|
| C1 | [CFRU util.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/util.c), [option_menu.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/option_menu.c), [config.h](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/config.h), [save.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/save.c) | Actual target settings, raw-value compatibility, initialization. |
| C2 | [CFRU ai_master.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/Battle_AI/ai_master.c), [ai_negatives.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/Battle_AI/ai_negatives.c), [ai_positives.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/Battle_AI/ai_positives.c) | Target flag resolution, move scoring and submitted-action access. |
| C3 | [CFRU ai_util.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/Battle_AI/ai_util.c), [ai_advanced.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/Battle_AI/ai_advanced.c), [ai_switching.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/Battle_AI/ai_switching.c) | Damage/order helpers, utility classes, switching and replacement selection. |
| C4 | [CFRU build_pokemon.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/build_pokemon.c), [damage_calc.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/damage_calc.c) | Power/scaling and item-knowledge coupling; not a new mechanics specification. |
| C5 | [CFRU move_menu.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/move_menu.c), [battle_util.c](https://github.com/Planton361/CFRU-expansion/blob/8bc8c38210ddba0b05c933dbda06cb4539254c7a/src/battle_util.c) | Difficulty-owned Bag/evasion restrictions and sleep clause. |
| P | pret FireRed `e060ab955b5dc9ac1c4904c2cd141683615cf477`: [AI scripts](https://github.com/pret/pokefirered/blob/e060ab955b5dc9ac1c4904c2cd141683615cf477/data/battle_ai_scripts.s) | Classic script semantics, not expanded-engine parity. |
| N | Cyan/NatDex FireRed `16b8b9ffd77607debe7ce332cd50d3615f47e125`: [scripts](https://github.com/CyanSMP64/pokefirered/blob/16b8b9ffd77607debe7ce332cd50d3615f47e125/data/battle_ai_scripts.s); NatDex UPR-ZX `9b63eb2876d901dc2e5af49855ae41ac255e1a72`: [Gen3RomHandler.java](https://github.com/CyanSMP64/universal-pokemon-randomizer-zx/blob/9b63eb2876d901dc2e5af49855ae41ac255e1a72/src/com/dabomstew/pkrandom/romhandlers/Gen3RomHandler.java#L2067) | Pinned Ironmon Smart flag evidence. No opaque patch inspection. |
| R | rh-hideout/pokeemerald-expansion `75b806a3ab57a81ff1eb6179288981f0b3cc3050`: [flags](https://github.com/rh-hideout/pokeemerald-expansion/blob/75b806a3ab57a81ff1eb6179288981f0b3cc3050/include/constants/battle_ai.h), [configuration](https://github.com/rh-hideout/pokeemerald-expansion/blob/75b806a3ab57a81ff1eb6179288981f0b3cc3050/include/config/ai.h), [main](https://github.com/rh-hideout/pokeemerald-expansion/blob/75b806a3ab57a81ff1eb6179288981f0b3cc3050/src/battle_ai_main.c), [record](https://github.com/rh-hideout/pokeemerald-expansion/blob/75b806a3ab57a81ff1eb6179288981f0b3cc3050/src/battle_ai_record.c), [switch](https://github.com/rh-hideout/pokeemerald-expansion/blob/75b806a3ab57a81ff1eb6179288981f0b3cc3050/src/battle_ai_switch.c) | Current modular rule-policy reference. Different engine/configuration. |
| S | Shin `7eb600271929f527216e864800693ad69c88bd94`: [trainer_ai.asm](https://github.com/jz-k/shinpokered/blob/7eb600271929f527216e864800693ad69c88bd94/engine/battle/trainer_ai.asm#L600), [func_ai.asm](https://github.com/jz-k/shinpokered/blob/7eb600271929f527216e864800693ad69c88bd94/custom_functions/func_ai.asm); PokeRed Canonical `a0df0634afe7c6bec19dbcb78cf1355b8866ff76`: [trainer_ai.asm](https://github.com/wisp92/PokeRed-Canonical/blob/a0df0634afe7c6bec19dbcb78cf1355b8866ff76/engine/battle/trainer_ai.asm#L514), [func_ai.asm](https://github.com/wisp92/PokeRed-Canonical/blob/a0df0634afe7c6bec19dbcb78cf1355b8866ff76/custom_functions/func_ai.asm) | Source-backed Gen-1 anti-repeat and switch-memory patterns only. |
| E | Elite Redux `36308b3eded82bc8c35d6d3e2daf2c8ae4d5710f` (`upcoming`): [main](https://github.com/Elite-Redux/eliteredux-source/blob/36308b3eded82bc8c35d6d3e2daf2c8ae4d5710f/src/battle_ai_main.c), [ability](https://github.com/Elite-Redux/eliteredux-source/blob/36308b3eded82bc8c35d6d3e2daf2c8ae4d5710f/src/battle_ai_ability.c), [new](https://github.com/Elite-Redux/eliteredux-source/blob/36308b3eded82bc8c35d6d3e2daf2c8ae4d5710f/src/battle_ai_new.c), [scoring](https://github.com/Elite-Redux/eliteredux-source/blob/36308b3eded82bc8c35d6d3e2daf2c8ae4d5710f/include/battle_ai_scoring.h) | Modern effect/ability coverage; experimental files are not proof of a shipped search AI. |
| K | PokAImon Emerald `a066ca4481639d6b879c85b485523a06ee205a3b`: [README](https://github.com/exploratorystudios/pokaimon-emerald-source/blob/a066ca4481639d6b879c85b485523a06ee205a3b/README.md), [policy](https://github.com/exploratorystudios/pokaimon-emerald-source/blob/a066ca4481639d6b879c85b485523a06ee205a3b/src/battle_ai_policy.c), [evaluation documentation](https://github.com/exploratorystudios/pokaimon-emerald-source/blob/a066ca4481639d6b879c85b485523a06ee205a3b/tools/ai/README.md) | Learned policy feasibility and differential-testing reference; no local execution or weight inspection. |
| M | Metamon `28f1840c05de15bcac473697a3eb7efa3f865e10`: [README](https://github.com/sooham/metamon/blob/28f1840c05de15bcac473697a3eb7efa3f865e10/README.md), [evaluation](https://github.com/sooham/metamon/blob/28f1840c05de15bcac473697a3eb7efa3f865e10/metamon/rl/evaluate/README.md) | Modern Showdown policy/baseline/evaluation research, not a CFRU adapter or mechanics oracle. |

Relevant local evidence: [source index](../../01_docs/references/source-index.md),
[Smart scoring comparison](../../01_docs/analysis/smart-ai-scoring-comparison.md),
[patch verification](../../01_docs/analysis/smart-ai-patch-source-verification.md),
[Smokescreen observation](../../01_docs/analysis/trainer-ai-smokescreen-behavior.md),
[Expert isolation](../../01_docs/analysis/cfru-expert-ai-isolation.md), and
[Vanilla difficulty design](../../01_docs/analysis/cfru-game-difficulty-vanilla-option.md).
These preserve rationale and sanitized observations, not current-code authority.

## 2. Current CFRU behavior map

| Surface | Source-backed behavior at the required pin | Design consequence |
|---|---|---|
| Fresh settings | C1 `GetGameDifficultyMode` maps zero/default to Normal; `GetTrainerLevelScalingMode` and `GetTrainerAIProfile` map zero to legacy Auto. Vanilla difficulty also resolves Auto scaling to Normal and Auto AI to Normal. `NewGameWipeNewSaveData` clears extended storage. | Selecting Difficulty Vanilla alone does not disable scaling. Explicit fresh initialization is required; source evidence is not a new runtime pass. |
| Menu/storage | C1 uses difficulty raw 4 for Vanilla; scaling/AI explicit values use enum + 1. Menu conversion preserves unchanged Auto raw values. | Never reinterpret old raw zero as a new default or silently relabel an old saved profile. |
| Regular trainer flags | C2 `GetAIFlags` loads trainer flags (ORs both trainers in two-opponent battles). Easy removes GOOD from stronger trainers, otherwise uses BAD. Vanilla/Normal preserve data flags. Hard/Expert/Smart add BAD, SEMI, GOOD. Legacy Smart hook also adds all three. | The May Smart-v2 BAD+SEMI description is **LEGACY / OBSOLETE** for this pin. Simply selecting current Smart does not implement the proposed Ironmon profile. |
| Scoring | C2 script table maps BAD to `AIScript_Negatives`, SEMI to `AIScript_SemiSmart`, GOOD to `AIScript_Positives`; usable scores begin at 100. SemiSmart does not add its normal work when GOOD is set. | Numerically matching NatDex 0x07 does not reproduce its policy. Additive finite penalties alone are not a hard validity floor. |
| Accuracy drops | C2/C3 negative checks handle blockers/caps; `GoodIdeaToLowerAccuracy` checks ability/item blockers and a conditional KO shortcut, not a general next-use benefit. Positive scoring rewards it through class-dependent status viability. | Repeated technically valid drops can remain attractive. The historical Sand Attack/Smokescreen reports are plausible, but do not measure incidence at this pin. |
| Speed drops | C3 `GoodIdeaToLowerSpeed` checks current relative speed; the explicit post-drop speed-flip condition is guarded for doubles. | Singles need marginal turn-order value, rather than only “currently slower.” |
| Damage | C2 `DamageMoveViabilityIncrease` rewards KO/strongest moves, with speed/context distinctions; C3 supplies damage and order helpers. | Reuse supported mechanics behind an observation-aware interface; replace utility arbitration, not all battle mechanics. |
| Switching | C3 `ShouldSwitch` checks traps and available bench, then ordered triggers for absorbers, Wish, locked moves, Perish, bad moves, cures, Yawn, residual damage, death avoidance and low offensive stats. `CalcMostSuitableMonToSwitchInto` separately selects replacements. | Strong building blocks already exist. First-success trigger ordering is not a common comparison of the best switch against staying. |
| Information/prediction | C2 `ShouldPredictRandomPlayerSwitch` and anti-cheese helpers inspect `gChosenActionByBank`; Hard/Expert anti-cheese and Expert prediction have separate profile gates. C4 hides certain resist-berry knowledge below Expert, but that is not a comprehensive information boundary. | Current labels do not establish fair partial observability. Remove submitted-action dependency from every new profile, including Challenge. |
| Power | C4 trainer construction gates EV spreads/IV overrides, boss stat improvements, friendship and max PP by difficulty; scaling has a separate mode. Some trainer-data fields/flags also identify EV spreads. | Do not rewrite stored trainer aiFlags to implement competence: that could affect construction. Hold power constant when comparing AI. |
| Restrictions | C5 gates trainer-battle Bag limits and player evasion-move restrictions by difficulty; Expert also applies a player-side sleep clause. | A stronger AI selection must not activate these independent rules. |
| Special battles | C2 dispatches tutorial, Safari, roaming, Frontier, Tower, raids and wild logic before/around ordinary trainer resolution. | Ordinary singles are the first implementation boundary. Excluded modes keep explicit legacy routing and must not claim the new competence/fairness guarantee. |

Normal is not a synonym for vanilla power. Conversely, Difficulty Vanilla is
not a promise of retail FireRed mechanics: expanded data, existing engine rules,
trainer tables, and accepted QoL remain. The new architecture must not silently
modernize missing Gen-9 mechanics.

## 3. What the other architectures contribute

**pret / Cyan / Ironmon (P, N).** Classic AI has separate bad-move, viability,
and try-to-faint scripts. The KO script rewards a finishing attack, including
priority; speed-down viability penalizes a drop when the target is not faster.
Accuracy-down scoring considers stages, HP and residual statuses. NatDex's
randomizer ORs `0x07` into trainer data; this enables those classic scripts.
It is not a novel learned policy or a guarantee against all irrational moves.
Borrow the conservative offensive emphasis and separate KO reasoning. Do not
claim a new expanded-engine profile is bit-exact Ironmon patch parity.

**Emerald Expansion (R).** The flag API separates smart switching, replacement
choice, prediction, risk, party knowledge and move/item/ability omniscience.
Its bundled SMART_TRAINER includes OMNISCIENT: copying that preset would violate
the intended fair default. ASSUME_STAB/status flags may reveal actual moves;
they are not automatically equivalent to uncertain priors. Configuration makes
switch probabilities, recovery thresholds, damage-roll assumptions and PP-stall
penalties explicit. Recording functions retain revealed moves, abilities and
item effects. Borrow these separations and auditable configuration; do not copy
its full preset or its newer mechanics into CFRU.

**Shin / Canonical (S).** Both inspected trainer routines discourage repeated
zero-base-power actions and low-HP utility, with exception lists. Party scoring
and per-mon switch flags discourage returning to poor choices. This supports
small battle-local memory rather than ML as an anti-spam prerequisite. A blanket
ban after any status move is too coarse for recovery or residual-damage play.
Some Shin code simulates blindness probabilistically after player actions; use
an actual observation boundary instead of occasional access to hidden choices.

**Elite Redux (E).** The active main scorer contains explicit custom ability
and immunity checks and evaluates switching when move scores are poor. That
shows the maintenance cost of expanded mechanics and the need to share effect
semantics. In contrast, inspected `battle_ai_new.c` contains empty functions and
commented planning code; many macros in `battle_ai_scoring.h` are zero. Do not
cite those as a completed production expected-utility/search implementation.
Borrow coverage discipline, not its balance or multi-ability assumptions.

**PokAImon Emerald (K).** Its documented MCTS-distilled 116→96→9 network uses
integer inference for four moves and five switch targets, replacing opted-in
trainer singles decisions while retaining other AI. Its pipeline describes
mechanics tests and floating/fixed/C differential action checks. This is real
evidence that learned inference can fit a GBA-oriented design. Feature extraction
reads battle state directly; CFRU's hidden-information contract would still need
an audit and a different observation adapter. Neither strength on randomized
Gen-1–9 CFRU teams nor target latency is established here.

**Metamon / modern Showdown (M).** The project reports strong offline-RL policies
and offers diverse heuristic/learned baselines, standardized teams and head-to-head
evaluation. Transfer the evaluation discipline: multiple opponents, unseen teams,
separate information conditions, and reproducible battle seeds. Competitive
Showdown results are not evidence of equivalent behavior under this CFRU pin,
its unsupported mechanics, or progression-based Ironmon constraints. No model,
training dataset, network service or Showdown runtime is required for pilot v1.

## 4. Separate product dimensions and profile names

| Dimension | Owner / proposed exposure | Invariant |
|---|---|---|
| Competence | Trainer AI profile | Every new non-Legacy profile has the same validity, KO and marginal-value floor. |
| Trainer levels | Trainer Level Scaling setting | AI changes never change levels or evolution/scaling rules. |
| Wild levels | Wild Level Scaling setting | Independent of trainer AI and trainer scaling. |
| Trainer power | Existing Difficulty bundle, explicitly described | IVs, EVs, PP, friendship and party construction are not AI quality. |
| Player/battle restrictions | Existing Difficulty/rules settings; preset summary lists effects | No hidden Bag, sleep, evasion, party-size or battle-style change from AI. |
| Switching | Profile capability with shared emergency floor | Deciding to switch and choosing a replacement are separate operations. |
| Prediction | Profile capability | Depth and uncertainty can increase without increasing factual knowledge. |
| Information | Explicit Omniscience option, Off by default | Only Challenge enables privileged team data; never reads the submitted action or future RNG. |
| Randomness/risk | Profile constants, visible description | Randomness chooses defensible near-best actions, never bypasses the floor. |

Keep the existing Difficulty name for pilot compatibility, with help text
“trainer power and battle rules”; a broad settings redesign is unnecessary.
Show Trainer AI independently. Retain Auto only as a legacy compatibility value,
not as a fresh default. Do not reuse existing save enum values for new semantics.

Recommend four policy definitions plus an explicit information variant:

* **Legacy (Vanilla flags)** replaces the ambiguous AI label Vanilla. It means
  pinned CFRU trainer-data behavior, not retail FireRed AI or a fairness promise.
* **Standard** is competent, reactive and deliberately shallow.
* **Ironmon Smart** is a conservative tactical policy inspired by classic
  Smart, with the new floor. Help text must say “not exact NatDex patch parity.”
* **Expert** increases fair prediction and team planning, not stats or cheating.
* **Omniscient Challenge** is Expert + explicit full-team information, not a
  fifth intelligence algorithm. Selecting it sets Omniscience On visibly;
  switching back to Standard/Ironmon resets it Off. No hidden sticky override.

The new-policy guarantees apply to supported ordinary trainer singles. Legacy
remains an explicit compatibility path. Tutorial/scripted and other excluded
battle types must expose their exclusion in the support profile. A displayed
new profile must not silently promise fairness for legacy-routed special modes.

### Per-profile specification

Module names below refer to sections 5–8, not existing CFRU flag numbers.
Floor F = action legality, known no-effect exclusion, damage/order/KO, marginal
utility, repeat memory, emergency switch validation and deterministic trace.
T = conservative tactical effect evaluation; P = uncertain opponent-response
model; X = full-team observation. “Horizon” is a utility estimate, not necessarily
a battle-tree simulation.

| Requirement | Legacy (Vanilla flags) | Standard | Ironmon Smart | Expert | Omniscient Challenge |
|---|---|---|---|---|---|
| Move modules | Pinned BAD/SEMI/GOOD per trainer data and existing special routing | F; direct damage, status, setup, recovery and immediate field value | F+T; residual/field/pivot and two-turn payoff estimates | F+T+P; probability-weighted tactical alternatives | Expert modules + X |
| KO/damage | Existing CFRU logic | Robust immediate KO dominates low-value utility; min/expected/max damage, accuracy and order | Same floor; compare 2HKO lines and survival | Same; compare response distribution and preservation only with explicit evidence | Same rules, narrower uncertainty from full data |
| Setup/status | Existing positive/negative scoring | Only positive one-follow-up marginal benefit | Two-turn break-even and residual combinations | Up to three-turn discounted heuristic payoff, response-aware | Expert with known sets |
| Next stat change | Existing helpers | Recompute next-stage damage/order benefit; no constant bonus | Same; 2HKO and defensive survival thresholds | Same; team/response-weighted benefit | Same, exact known stats |
| Repeat/status spam | Existing behavior; no new guarantee | Shared F memory and repeat gate | Same gate, strategic exception requires T evidence | Same gate, exception requires P/T evidence | Same, no exemption for omniscience |
| Recovery | Existing scoring | Net HP/survival gain after incoming damage; no full-HP waste | Include residuals and next-turn KO/race | Include response uncertainty and preservation | Expert with full information |
| Voluntary switching | Existing CFRU triggers | Emergency escape: no useful action, lethal countdown or clearly dominated stay | Emergency + meaningful matchup/status/ability gain | Add uncertainty-aware preservation/pivot/trapper planning | Expert with full team known |
| Switch-in selection | Existing CFRU selector | Legal bench; hazards, survival, useful response | Add safe revenge KO and residual/ability value | Add future matchup and revealed bench coverage | Same over full opponent bench |
| Prediction depth | Existing logic; submitted-action dependencies retained only here | No action prediction; public threat envelope | One-turn distribution over revealed actions; no speculative opponent switch | One simultaneous turn, moves plus likely switches; two-turn heuristic tail, no recursive rollout in v1 | Same depth, full-state priors; no action oracle |
| Information | Pinned behavior, not certified fair | Own team + public/revealed history; no species moveset guesses | Same; measured order/damage intervals | Same plus declared randomized-format priors | Full opponent team, sets/stats/items/abilities/PP; still no selected action/RNG |
| Near-best randomness | Existing AIRandom behavior | Uniform within 8 utility points of best | Uniform within 4 | Uniform within 2 | Uniform within 2 |
| Risk | Existing | Conservative unknown-damage envelope | Conservative, accepts a damage roll only when no safer dominant line | Expected utility with uncertainty penalty | Same utility/risk, not automatic max-roll optimism |
| aiFlags | Preserve pinned semantics | New floor overrides quality bits; no inherited GOOD bonus | Same; explicit T modules | Same; explicit P modules | Same; X only from user setting |

For new profiles, preserve original trainer bytes in storage/construction. Resolve
an ephemeral policy descriptor at the decision boundary. Do not OR classic 0x07
into CFRU or let trainer GOOD flags re-enable old utility scoring. Map known
personality flags only through a reviewed whitelist of bounded preferences
(maximum ±2 utility points, after hard filtering). Such preferences cannot
grant information, disable the floor, force setup over a KO, or change power.
Unknown quality bits produce a diagnostic and no new capability. Scripted control
flags dispatch before policy resolution; special-battle exclusions are explicit.
The future flag inventory must cover every bit used by the target trainer table.

## 5. Observation boundary and prediction without omniscience

Proposed pure boundary:

```text
Engine state -> Observation(profile, reveal history)
Observation + own party + policy memory + decision seed -> Action + ReasonTrace
Action -> engine legality recheck -> execution
```

The scorer must not receive a pointer to global battle state or the player party.
Mechanics helpers receive sanitized inputs, not battler IDs that let them reload
hidden values. Existing CFRU damage/prediction helpers are reusable only after
their transitive reads satisfy this boundary. Cached results include observation
version, profile, active identities and knowledge mask; never share Challenge
cache entries with fair profiles.

All fair profiles know their own party exactly. Opponent knowledge includes
visible species/form and level; displayed HP fraction (represented as a rounding
interval, not exact hidden HP); public status, stat stages, weather, terrain,
screens/hazards and announced volatile conditions; moves actually revealed;
ability/item facts actually revealed by battle messages or unambiguous effects;
and previously seen opponent party members. Do not read unvisited bench slots,
exact IVs/EVs/nature/stats, unrevealed PP, hidden sets or items. Unknown is a
distinct type, never silently “no ability/item.” Remember facts by battle party
identity, including form/Transform/Illusion uncertainty; do not identify a hidden
Illusion by a private party index. Reset knowledge at battle end.

Speed and damage observations narrow intervals only when priority, effects,
ties and damage rolls permit the inference. A species model uses the declared
public ruleset; randomized abilities/moves/stats invalidate canonical-set priors.
Standard/Ironmon use broad unknown threat bounds, not “the species must have
Earthquake.” Expert may use an approved prior over the *allowed randomization
pool*, never the private random seed or actual generated party. Unspecified
randomization settings use a broad prior. Likely STAB/status is a probability
with an UNKNOWN remainder, not permission to query an actual hidden slot.

Ironmon weights known available moves uniformly initially; update only from
observed frequency with add-one smoothing. Unknown move mass remains until
slots are revealed: reserve 25% for an aggregate unknown response while any
slot is unknown, or 100% if no move is known. Expert reserves at least 25% response probability
for the unknown branch when moves remain hidden and caps speculative switch
probability at 50%. Distribute switch mass across revealed living bench using
their public matchups; represent unseen bench by an aggregate unknown outcome,
not invented exact species. With no reveal-based switch evidence, use 10% switch
prior in Expert and 0% in Ironmon. These are proposed tunables, not learned facts.

Prediction evaluates simultaneous committed choices. The observation is frozen
before either side's submitted action can influence scoring. It cannot use
`gChosenActionByBank`, the selected move/target, menu cursor, queued switch ID,
future random values, or post-selection retargeting. Historical immunity-switch
patterns can update the next turn's probability model; they cannot expose this
turn's choice. Challenge gets full team data but obeys this same timing rule.

Mandatory noninterference test: two engine states with identical public history
but different hidden moves/items/abilities/stats/bench and submitted choices must
produce identical fair observations, scores, random draw count and actions for
the same decision seed. After a legal reveal, differences are permitted and
must carry the reveal as their reason. Challenge may differ on team data, never
on the submitted action or future RNG.

## 6. Common scoring and anti-spam contract

### Action classes and utility

Enumerate at most four moves and five bench switches in singles, plus engine
forced-action handling. First apply actual own-action legality: PP, Disable,
Taunt, Choice lock, Encore, recharge/charge obligations, trapping, fainted/active
bench and battle restrictions. Resolve Choice/Encore conflicts using CFRU's
actual precedence, not a separately invented rule. Forced actions and Struggle
are explicitly tagged, not treated as policy errors.

Next exclude *known* no-effect actions if a productive alternative exists:
immunity/absorber, capped pure stat change, redundant status, full-health healing,
or an already active identical field effect without a useful refresh. Keep a
damaging move when only its secondary effect is redundant. Separate legal but
futile from illegal. Hidden immunity discovered through a reasonable attack is
an information outcome, not a clairvoyance failure. If every legal action is
futile and switching cannot improve matters, choose the least costly legal
fallback, log `NO_PRODUCTIVE_ACTION`, and avoid an infinite selection loop.

Use signed, saturating integer utility; do not squeeze the new scale into old
unsigned viability bytes. Proposed scale: 100 points per opposing full HP bar
removed, 100 per own full HP bar preserved, and 200 for a net faint advantage.
For each available response branch estimate:

```text
U = 200 * net_faints
  + 100 * (opponent_HP_fraction_lost - own_HP_fraction_lost)
  + discounted_future_gain - entry_cost - repeat_cost - uncertainty_cost
```

Healing enters the HP difference once, residual damage once; stat/field value
is the difference in future outcomes, not another generic status bonus. Future
discount is 1/2 per turn; cap total nonterminal future credit at 40 points.
Use fixed-point fractions (1/256), signed 32-bit accumulation, explicit rounding
toward zero and bounds checks. Unknown-outcome uncertainty cost is one quarter
of the branch utility range (maximum 25). Standard uses a current threat envelope;
Ironmon/Expert use the response models above. These weights are the initial
testable specification, to be revised only with held-out evidence and review.

Before near-best sampling, apply two dominance rules:

1. A robust safe immediate KO outranks low-value utility, speculative setup,
   and ordinary switching. “Robust” means success under every modeled plausible
   defensive state/damage roll, accuracy check, priority/order and survival
   branch; Focus Sash/Sturdy, protection, multi-hit and recoil matter when known.
   A move merely capable of KOing on a high roll is not guaranteed. An unknown
   opponent response usually prevents a literal unconditional guarantee.
2. Never choose a strictly dominated action: an alternative is at least as good
   in every modeled branch and better in one. A safe priority KO dominates a
   slower attack that loses before acting. If all lines lose, maximize useful
   damage/status/preservation without pretending survival is possible.

In full-information fixtures use an independently verified tactical guarantee.
In fair play also report conditional KO certainty (“if target stays and uses a
revealed action”). Do not inflate missed-KO metrics by judging fair policies
against hidden facts. An immediate KO can be declined only for a proven stronger
terminal outcome or to avoid a known losing trade (e.g. last-mon self-sacrifice),
with a named fixture and trace reason. A generic future-value bonus cannot do it.

### Effect-specific marginal value

| Effect | Required evaluation / rejection |
|---|---|
| Damage, OHKO, 2HKO | Compute CFRU-consistent min/expected/max damage, hit probability, priority/order and survival to act. OHKO-effect moves include their special hit/level rules; never treat “OHKO move” as guaranteed KO. A 2HKO assumes both action opportunities and includes recovery/residuals; type effectiveness alone is not a score. |
| Sand Attack / Smokescreen | Value the *next* reduction in hit probability multiplied by relevant incoming damage over the horizon. Guaranteed-hit attacks or an already decisive damage line can make it worthless. Require surviving to benefit; cap/non-effect rejection and repeat gate below prevent lowering to minimum by default. Residual-stall use remains possible when it beats attacking. |
| String Shot / Speed drops | Evaluate order before and after the actual stage change, including priority, ties, Trick Room and supported speed effects. After already moving first, order credit is zero. Two drops needed for a flip are allowed only in Ironmon/Expert when the horizon and survival justify the sequence; no repeated “still slower” bonus. Speed-dependent damage effects are separate real marginal value. |
| Other stat drops / boosts | Recalculate affected physical/special damage and survival thresholds using capped next stage. Attack setup without usable physical attacks has no offensive value. A boost/dropped defense that changes 3HKO to 2HKO may matter; another that changes nothing in the horizon does not. Account for known Contrary, Unaware, Clear Body, Defiant-like consequences and reset/phazing threats supported by CFRU. |
| Major status | Reject known existing/incompatible major status and known immunity/Safeguard/substitute blockers. Evaluate expected lost actions, reduced relevant damage/speed, or residual HP. Do not reapply sleep/poison for a generic bonus. |
| Toxic / Leech Seed / Yawn | Distinguish escalating poison, persistent seed and pending sleep. Value remaining exposure and likely switching; reject a second seed or pending Yawn. Do not assume Toxic refresh resets favorably. Reapply only after a public cure/switch removes the relevant effect. |
| Recovery | At full HP, no healing credit. Below full HP compare net HP after attack order, heal cap, incoming damage, residuals and next-turn survival against attacking/switching. Heal only if the net line improves; a slow heal after lethal damage is invalid as a survival plan. Repeated healing is allowed for positive survival/residual payoff; finite PP and stalemate risk matter. No universal 50%-HP rule. |
| Screens / weather / terrain | Value affected damage/status across the horizon and known own team; account for remaining duration, overwritten benefit and opponent benefit. No blind score for setting a field already active with adequate duration. |
| Hazards / trapping | Use only supported effects. Value hazards against plausible future entries, not the hidden bench; no extra layer beyond cap. Trapping needs a useful residual/matchup outcome and legal target. |
| Protect-like moves | Credit actual residual/healing/scouting benefit; include repeated-use failure probability. Scouting earns no value when it cannot inform a later useful action. Prevent cost-free endless Protect/recovery loops. |
| Self-sacrifice / pivot | Include own faint/recoil, battle-end rules and replacement quality. Pivot is attack plus a timed entry, not a free switch; evaluate hazards and whether the replacement must take a hit. Never pivot merely for a fixed score bonus. |

No unsupported ability or move mechanic is implemented to make these estimates
complete. An unsupported effect has an explicit coverage entry, uses conservative
known damage/legality fallback, and blocks acceptance if mandatory pilot fixtures
depend on its strategic effect. “Unknown scorer” is not silently “good utility.”

### Repeat memory and near-best policy

Keep a battle-local ring of the last four resolved decisions: actor/target public
identity, effect family, actual success, relevant stages/status, damage, and
switch edges. Count **successful applications to unchanged tactical context**;
a miss is not a successful setup. Sand Attack and Smokescreen share the same
family, so alternating move IDs cannot bypass the rule.

For a repeated pure utility family, subtract `8 * min(3, successful_repeats)`
points and recompute marginal value. After two consecutive successful uses of
that family, remove it from near-best sampling unless a traceable strategic
exception beats the best productive alternative by at least 8 points. Allowed
exceptions: demonstrable order/KO/survival threshold, net-positive recovery,
or a residual-damage win line. “Stat can still fall” is not an exception. The
exception is re-evaluated each turn and cannot bypass caps/redundancy/KO dominance.

Reset the relevant repeat counter when its effect expires/is removed or a new
target makes it a different tactical problem; do not reset the entire memory
after switching. Forced Encore/Choice/charge repetitions are tagged and excluded
from discretionary spam metrics, while their switch alternatives are evaluated.
PP-stall detection records failed attacks into *revealed* immunity and repeated
public switch patterns. It downweights that line next turn, never peeks at a
queued switch. If no productive line exists, spend PP through a defined legal
fallback; never loop inside the decision function.

After exclusions and dominance, sample uniformly from `U >= Ubest - epsilon`
within the same tactical priority class, using the per-profile epsilon table.
Positive utility, repeat exceptions and switch admission rules still apply.
Risk is in utility estimates, not a chance to ignore legality. Stable action
IDs make traces reproducible; equal alternatives receive no party-slot favoritism.

## 7. Switching: trigger, candidate and arbitration

For each legal bench candidate compute one entry outcome: hazards and other
entry effects, predicted incoming damage under the profile's information,
survival, usable response and preservation value. Compare this to the best stay
action on the same utility scale. A voluntary switch takes the turn; a forced
replacement after a faint does not take the same incoming attack. Pivot timing
is a third case. This distinction is essential for revenge-kill quality.

| Situation | Required policy |
|---|---|
| No useful moves / known immunity | Evaluate switch even in Standard. Do not escape into an equally helpless or entry-KOed mon if a productive stay exists. If all options lose, rank least-loss outcomes explicitly. |
| Choice lock / Encore | Legal move set reflects the lock and duration. Switch if the locked line is dominated and entry is better; if trapped, take the legal forced/fallback action. Do not merely score an unavailable coverage move. |
| Perish / Yawn | Count down in engine order. Escape a lethal Perish countdown when a surviving legal switch exists. For Yawn compare sleep cost, remaining duration, cure ability, lost boosts and entry cost; never apply “always switch” regardless of hazards. |
| Toxic / Seed / other residuals | Compare next residual ticks, reset/removal on switching, hazard/re-entry cost and lost offense. Toxic persistence/reset and Seed removal use target engine semantics. |
| Absorber / immunity | Credit own known ability against a revealed or probabilistically predicted move, including ability bypass. No automatic switch merely because one opponent attack can be absorbed; alternative coverage and hazards can make it poor. |
| Low offense / Natural Cure / Regenerator | Value restored damage/status/HP after switching; subtract lost boosts, incoming hit and re-entry cost. No endless ability-trigger loop without net progress. |
| Unavoidable KO / revenge | Save the active mon only if doing so improves team outcome. Sometimes sacrifice is better than letting a healthy replacement take the same lethal hit. After a faint, prefer a safe priority/speed KO when known; account for hazards first. |
| Trapper / preserving setup | Legal trapping prevents voluntary switch. Offensive trapping and saving a sweeper are Ironmon/Expert tactical considerations, never reasons to discard a robust winning attack. |

Admission: an emergency switch that strictly dominates futile/lethal staying
is mandatory when legal. Other switches require positive advantage of at least
12 utility points in Ironmon or 8 in Expert/Challenge; Standard admits only
emergencies. Between that threshold and threshold+8, switch with probability
1/2, provided staying is still defensible; above threshold+8 admit the switch
deterministically. Select among near-best eligible replacements with the profile
epsilon. These initial values bound twitchy switching without adding knowingly
irrational actions. Mandatory survival is never randomized away.

Loop guard: remember the last four voluntary switch edges. An A→B→A return
within three own decisions adds 16 cost; prohibit it without a changed public
threat or an 8-point net progress exception after that cost. After two consecutive
voluntary switches, require either an emergency or an independently scored
positive progress exception. Forced replacements and externally forced switches
do not consume this budget. Material progress means net HP/status/PP advantage
or escaping a known losing line, not merely another activation of Regenerator.
Test lethal hazards, immunity alternation, productive regeneration and all-losing
states separately. This guard constrains choice, not battle legality.

## 8. Architecture options and feasibility

| Option | Benefits | Costs / failure modes | Pilot decision |
|---|---|---|---|
| A. CFRU-native rules | Reuses target mechanics; explainable reasons; bounded candidate count; small memory; direct regression fixtures | Existing helpers read globals; effect coverage and score calibration need care | **Recommend v1.** New observation/policy boundary and common arbiter around audited helpers. |
| B. Shallow search / expected utility | Can recognize setup, sacrifices and switch responses consistently; increases planning without cheating | Needs a faithful reversible transition model, uncertainty/chance handling and CPU/RAM bounds; simulator mismatch can exceed heuristic error | Keep the interface ready. v1 uses bounded analytical expected utility, not recursive engine simulation. A later contract may compare one/two-turn search to A. |
| C. PC/BizHawk-assisted or learned | More compute; flexible research agents; learned priors may capture strategy | State/action protocol, synchronization, timeout fallback, replay, portability and information leaks; learned policies add dataset/generalization/export validation | Reject for pilot; research-only reference. No emulator or Tracker dependency. |

BizHawk running on a PC does not give ARM7TDMI ROM code unlimited CPU or memory.
An external agent requires an explicit protocol and a new implementation scope.
Conversely, K shows that neural inference is not intrinsically impossible on
GBA. Reject ML here because its training distribution, observation model and
CFRU mechanics coverage are unproven, not because “GBA cannot run a network.”

Proposed v1 bounds: singles only; at most nine root actions, at most eight
response branches (four revealed move slots, up to three representative revealed
switch candidates, one aggregate unknown branch), and a capped analytical tail.
Pruning uses only permitted observations, with deterministic tie handling.
Target no recursion, no heap allocation, at most 512 mechanics estimates per
decision, at most 8 KiB added persistent/scratch AI memory combined, and at most
two GBA frames of added decision latency. These are acceptance budgets, not
measurements. A later integration must measure target cycles/stack/RAM; host
milliseconds alone cannot certify the ROM budget. On exhausted work budget,
return the best completely evaluated floor-safe action, with a trace, rather
than an unscored arbitrary action.

## 9. Deterministic host-side evaluation specification

### Harness layers and input contract

The harness is designed here, **not implemented or run**. Its future host process
must accept source-authored synthetic states only, with no ROM/save/state import.

1. **Pure policy tests:** call the same future C policy core that the ROM adapter
   will call, using a minimal host adapter and immutable observations. Test masks,
   traces, arithmetic, ranking, repeat memory and budget behavior.
2. **Mechanics contract tests:** separately verify the adapted CFRU damage/order/
   legality/effect functions against source-derived golden cases and an independent
   simple oracle for tractable mechanics. Do not use the scorer's own answer as
   the expected answer. Stub-only tests cannot certify mechanics compatibility.
3. **Deterministic micro-battles:** a limited host transition model covers listed
   supported effects, and compares next-state results with the source-owned
   mechanics adapter. Unsupported effects fail coverage explicitly. A later
   private runtime differential gate is still required before product acceptance.
4. **Tournament evaluation:** run synthetic randomized parties under that declared
   mechanics subset. Report subset and coverage with results; a Showdown surrogate
   may be exploratory but cannot substitute for CFRU parity.

Versioned fixture schema:

```text
schema_version, fixture_id, source_revision, mechanics_config_hash
battle_mode, power_profile, scaling_profile, rules_profile
truth_state: source-authored parties, moves/PP, stats, status/stages,
             items/abilities, field, locks, turn/entry order
public_history, observation_mask, own_party, policy_memory
profile, information_mode, policy_config_hash
team_seed, battle_seed, decision_seed
expected: legal_actions, allowed_best_set, forbidden_actions,
          required_reasons, permitted_repeat_exceptions, coverage_tags
```

Truth belongs to the harness/referee, not to the fair scorer. Fixtures carry
expected sets or inequalities when multiple actions are sound; avoid brittle
single-action snapshots except where the result must be unique. Include a
hand-worked numeric damage/order example for each mechanics rule introduced.

Proposed deterministic random contract: named xorshift32 with unsigned wrap,
shifts 13/17/5, replacing zero seed by `0x6D2B79F5`; rejection sampling for bounded
uniform integers. Seed streams for team generation, battle mechanics and policy
choices are separate. Derive seeds from SHA-256 of UTF-8
`schema|fixture_id|replicate|stream`, first four bytes little-endian. Consume no
policy randomness during scoring; consume a documented draw only at stochastic
admission/selection. Log pre/post seed and draw count. Production can use an
adapter but must replay the same policy stream independently of battle RNG.

Outputs are sanitized JSONL decision traces plus aggregate tables: observation
hash, permitted facts, legal mask, exclusions, damage interval, marginal terms,
switch entry costs, candidate scores, sampled action, exceptions and seed IDs.
Record compiler/version, optimization flags, host architecture, schema/config/
source hashes. Two identical runs must be byte-identical; a second host/compiler
must agree on action/score traces after removing declared provenance fields.
No pointer values, wall-clock timestamps in canonical traces, or raw private data.

### Mandatory scenario families

Each row has positive, negative, boundary and hidden-information twin cases.
Run deterministic core assertions and replicate indices 0–1023 (using the seed
derivation above) for stochastic checks.

| Family | Required witness and counterexample |
|---|---|
| KO and damage | Safe guaranteed KO vs setup; priority KO vs slower death; resisted strong attack vs weak neutral attack; high-roll/low-accuracy apparent KO; known Sash/Sturdy/protection; recoil trade. |
| Accuracy repetition | Tackle versus Sand Attack/Smokescreen at neutral, -1, -3 and cap; four-turn history; alternating drop IDs; misses; guaranteed-hit opponent; useful Toxic stall exception. |
| Speed marginality | String Shot flips order; already faster; two drops needed; speed tie; priority; Trick Room; damaging speed-drop retains damage even when order value is zero. |
| Setup | Useful 3HKO→2HKO; boost without matching attack; capped stage; repeated setup; imminent KO; Contrary/Unaware where supported; phazing/reset known versus hidden. |
| Status | Already poisoned/asleep; Safeguard/substitute/immunity; pending Yawn; existing Seed; public cure/removal makes reapplication useful; damaging secondary-status move remains selectable. |
| Recovery | Full HP; below/at/above a survival threshold; slower than lethal attack; capped healing; Toxic tick; useful repeated recovery versus futile PP drain. |
| Choice / Encore | Forced immune move with safe switch; no legal switch; trap; lock expires; Choice/Encore precedence; no PP and Struggle; forced repeats excluded from spam numerator. |
| Residual escape | Perish last turn, Yawn, Toxic escalation and Seed with safe bench; lethal entry hazards; boosted winning attacker should stay. |
| Switch quality | Safe absorber vs known attack, hidden coverage twin, ability bypass, bad switch into hazards; low offensive stages, Natural Cure/Regenerator; no useful bench. |
| Revenge / preservation | Forced entry secures speed/priority KO; voluntary same entry takes lethal hit; sacrifice weak mon vs lose healthy one; preserve setup only when valuable. |
| Loops / PP stall | A→B→A immunity cycling, repeated player immunity switch, trapper, productive regeneration exception, all-futile battle, forced replacement does not trip loop guard. |
| Other effects | Active screen/weather/terrain refresh; hazard cap; trapping payoff; Protect success decay; self-sacrifice final-mon loss; pivot timing and entry cost. |
| Entropy | Two/four exactly equal actions; near-best threshold boundary; unique best; move/party permutation; repeated same seed; floor-invalid alternative never sampled. |
| Information / prediction | Hidden-state and submitted-action twins; reveal changes knowledge; false switch prediction; opponent stays; previously seen bench vs unseen; randomized non-STAB sets; Challenge knows team but not chosen action. |
| Integration isolation | Legacy raw values/Auto unchanged; profile alone leaves constructed teams, scaling, rules and battle RNG unchanged; special modes retain documented dispatcher; budget exhaustion has safe fallback. |

### Metrics, denominators and proposed acceptance gates

Report counts and denominators, per profile, battle phase, team distribution and
information mask. Empty denominators are N/A, never a claimed zero-percent pass.
Legacy baseline results are descriptive and are not required to satisfy the new
floor. Thresholds below apply to supported non-Legacy policy fixtures.

| Metric | Definition | Gate |
|---|---|---|
| Illegal action rate | Selected action outside referee legal set / all decisions | 0, including forced-action cases. |
| Invalid/no-effect action rate | Discretionary known futile choices when productive alternative exists / decisions with productive alternative | 0 on targeted fixtures. Report hidden-immunity discoveries and all-futile states separately. |
| Missed guaranteed-KO rate | Non-winning low-value choice / independently certified robust safe-KO opportunities | 0 on witnesses; log approved terminal/trade exceptions separately. Also report conditional-KO rate without calling it guaranteed. |
| Redundant-status rate | Redundant pure status choices / opportunities with redundant status and useful alternative | 0. Damaging secondary effects excluded. |
| Repeated-status rate | Discretionary same-family utility repeats / eligible utility decisions; plus harmful-repeat subset without positive marginal exception | Raw rate descriptive; harmful subset 0 in targeted sequences, no four-success Sand Attack chain without validated exception. |
| Useful setup rate | Setup choices with independently positive horizon gain / all discretionary setup choices | 100% on certified fixtures; also require selecting setup in unique-benefit witnesses so “never setup” cannot pass. Tournament estimate reported with coverage. |
| Switch quality | Good admitted switches / voluntary switches, plus regret versus best legal stay/entry under same information | 100% on dominance witnesses; zero known entry-KO switch when a surviving winning alternative exists. Report missed beneficial switches separately. |
| Switch-loop rate | Unjustified A→B→A or third consecutive voluntary switch / voluntary switch windows | 0 on loop suite. Productive exceptions counted and audited separately. |
| Near-equal entropy | Shannon H(action) / log2(number eligible) across seeds for identical state | At least 0.95 for exactly equal 2/4-way witnesses, each action within ±5 percentage points of uniform over 1024 seeds; singleton H=0, not N/A failure. |
| Incomplete-information behavior | Hidden/submitted-action twin mismatches / paired tests | 0 for fair observations, scores, draw counts and actions; Challenge submitted-action mismatch also 0. |
| Prediction | Brier score and reliability bins of predicted response; payoff/regret against actual response | Report success and failure, not only wins; require staying and false-switch cases to remain legal and floor-safe. No strength claim from clairvoyant tests. |
| Performance | Wins + 0.5 draws / completed scheduled games against each baseline, with paired uncertainty interval | See tournament gate; never replaces invariant tests. |
| Cost / reproducibility | Mechanics calls, memory, target cycles later; canonical trace mismatch | Zero replay mismatch; meet section 8 budgets before ROM acceptance. Host timing alone insufficient. |

### Randomized-team tournament and promotion rule

Before evaluation, freeze public-data generator, move/ability support whitelist,
policy configs and split seeds. Use the selected pilot data semantics, never
assume all Gen-9 mechanics. Generate three strata: progression-like low-level
small parties; broad randomized species/moves/abilities; synergistic stress teams
with recovery/status/pivots. Include deliberately awkward but legal movesets.
Keep level, IV/EV, PP, items, team size and restrictions identical across policies.
Create an additional one-usable-player-mon stratum for Ironmon behavior; do not
assume Ironmon means the trainer has one mon.

For each stratum use 1,000 unseen team pairs, four battle seeds and both seat
assignments: **8,000 battles per policy/baseline pairing per stratum**. Generate
development fixtures from disjoint seeds; no tuning against the held-out results.
Stop battles at 200 turns, score unresolved games as draws, and report timeout
rate rather than hiding stall. Schedule round-robin profiles and these baselines:
uniform legal, strongest expected damage, conservative KO-first/no-switch, and
an isolated pinned CFRU policy adapter where feasible. A NatDex/classic adapter
is optional and must declare mechanics differences; do not label a hand-written
approximation “exact pinned CFRU.” Missing target baseline parity blocks a claim
of improvement over current CFRU, but not the earlier pure harness milestone.

Report win/loss/draw, battle length, all behavioral metrics, and 95% confidence
intervals using a seeded cluster bootstrap over team pairs (10,000 resamples;
keep all seeds/seats in each cluster). Proposed v1 promotion: Standard and
Ironmon exceed uniform legal with lower confidence bound above 50%, are no more
than 2 percentage points worse than conservative KO-first in each supported
stratum, and meet every invariant gate. Expert must show positive paired gain
over Ironmon on the planning-stress stratum without a >2-point regression on
the others before being advertised as stronger. Treat these as separate
preregistered comparisons; no selection of favorable seeds or averaged-away
failure strata. If evidence fails, revise or defer the profile; do not lower
competence to manufacture a monotonic difficulty ladder.

Ablate repeat memory, switch hysteresis, observation filtering and prediction
one at a time on development seeds to identify contributions. Never ship an
ablation that violates the floor. Run hidden-state permutation tests even when
win rate improves: information leakage is a failure, not extra competence.

## 10. Defaults, compatibility and implementation decomposition

The proposed fresh profile is justified by C1/C4: explicit Vanilla avoids the
existing Normal power bundle, explicit scaling Off avoids Auto's Normal
resolution, and Standard supplies baseline competence without privileged
information. This is a product recommendation, not something research can prove
universally fun. It is conditional on passing the harness and later runtime gate.
Do not relabel current Normal as Standard and call the recommendation implemented.

| Setting | Fresh New Game recommendation | Ironmon preset recommendation |
|---|---|---|
| Difficulty | Vanilla | Vanilla |
| Trainer Level Scaling | Off | Off |
| Wild Level Scaling | Off | Off |
| Trainer AI | Standard | Ironmon Smart |
| Omniscience | Off | Off |
| Additional power/rules | No implicit change; retain separately selected rules | No implicit rule enforcement; Ironmon rules remain their own contract |

Source validation supports separation, not a claim that Difficulty Vanilla removes
every historical construction quirk. The later defaults contract must inventory
all remaining difficulty predicates, EV/IV/PP/friendship and restriction effects,
including speed-IV handling for Trick Room/Gyro Ball. Document intentional base
trainer-data behavior instead of silently changing it through AI work.

Fresh initialization must write explicit values only at the verified new-game
lifecycle point. Allocate new profile identifiers/versioning after an enum/save
audit; preserve all existing raw values and Auto resolution. Old saves retain
their old selected profile until the user explicitly opts into a new one.
Opening/saving options must not migrate AI or power implicitly. Test unknown raw
values, reset/new game, persistence and existing-profile display in the later
component contract. No save inspection is required in this design contract.

Proposed sequence, each separately bounded and reviewed:

1. **Host contract gate:** Workspace synthetic schema, pure observation/policy
   interfaces, deterministic runner, independent fixture oracles and baseline
   definitions. No component runtime edits. Prove initial legality, KO, repeat,
   information-twin and seed contracts; full tournament follows an executable
   target policy, not this specification alone.
2. **CFRU common floor / fair observation adapter:** ordinary trainer singles
   only, memory ownership and helper read audit, host-shared rule core. Keep
   legacy behavior callable and default selection unchanged until validated.
   No DPE/UPR-FVX or missing-mechanics work.
3. **Profiles and switching:** Standard/Ironmon tactical scoring and arbiter,
   then Expert/Challenge only if evidence supports their depth and budgets.
   Do not expose an unvalidated profile as supported just to fill a menu.
4. **Fresh defaults and settings compatibility:** explicit initialization,
   names/help, saved raw mapping and preset behavior. Separate from policy
   calibration so power/scaling cannot confound AI comparisons.
5. **Acceptance/integration:** source/host checks, separately authorized target
   build and private user runtime evidence, exact component revision review,
   then authorized Workspace pin integration. Only accepted implementation plus
   revision-bound validation can unblock #498's relevant R1 gate. R2/#499/#500
   remain downstream; there is no automatic unlock on document merge.

This design establishes the implementation boundary, not authorization to start
any of those writes in the current session. Record source reuse/license review
before copying upstream code; prefer adapting concepts through target-owned
helpers. Full battle-engine replacement, new mechanics and neural training stay
outside these contracts.

## 11. Final design decisions proposed for acceptance

* **Recommended architecture:** A, CFRU-native bounded rules with an enforced
  observation boundary, common competence floor, marginal-value modules, shared
  move/switch arbitration and deterministic host tests. Analytical expected
  utility is permitted; recursive search, ML and external control are deferred.
* **Recommended profile definitions:** Legacy (Vanilla flags) for exact pinned
  compatibility; Standard for competent reactive play; Ironmon Smart for fair
  conservative tactics, explicitly not patch parity; Expert for uncertain
  prediction; Omniscient Challenge as Expert with visibly enabled full-team
  knowledge. No new profile reads a submitted player action. Legacy is explicitly outside
  the new fairness/floor guarantee. Ship only profiles that pass their gates.
* **Recommended New Game defaults:** Difficulty Vanilla; Trainer Level Scaling
  Off; Wild Level Scaling Off; Trainer AI Standard; Omniscience Off. Explicit
  fresh initialization, no silent old-save migration, and no additional rule
  or power change hidden inside the AI setting.
* **Recommended Ironmon preset:** Difficulty Vanilla; both scaling settings
  Off; Trainer AI Ironmon Smart; Omniscience Off. Keep player restrictions
  separate. Validate one-player-mon and randomized-team cases before support.
* **First implementation contract boundary:** host-side synthetic observation,
  deterministic policy-test interface and fixture/oracle runner in Workspace,
  with seed replay, hidden-state twins and the mandatory KO/status/switch masks.
  No ROM adapter, component edits, Gitlinks, runtime, R2, BizHawk/Tracker or ML
  in that first contract. Its acceptance is a harness gate, not a gameplay pass.
* **Explicit rejected alternatives and why:** blindly OR classic `0x07` into
  CFRU (different script meanings); make Easy irrational (violates common
  competence); fix Sand Attack by banning all repeat status (breaks useful
  recovery/setup); copy Expert Difficulty (changes power/rules); call submitted
  action access prediction (violates fairness); copy Emerald Expansion's Smart
  bundle (includes omniscience); port the entire Emerald/Elite engine (mechanics
  and scope mismatch, experimental code is not proof); use Showdown as the CFRU
  truth oracle (mechanics mismatch); introduce ML because PokAImon/Metamon are
  strong references (no target distribution, fairness or parity validation);
  assume PC-hosted BizHawk removes GBA limits (requires a new external protocol);
  infer a pass from win rate or this report alone (behavioral, performance and
  runtime evidence remain separate). No merge; upstream contribution deferred.
