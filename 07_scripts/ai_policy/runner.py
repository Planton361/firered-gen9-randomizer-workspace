"""Fixture execution, replay, and hidden-information twin comparison."""

from __future__ import annotations

from dataclasses import dataclass

from . import STANDARD_SCHEMA_VERSION
from .floor import apply_common_floor, candidate_contract
from .memory import detects_aba_switch_loop
from .observation import observation_hash, project_observation
from .policies import choose_action
from .rng import XorShift32, derive_seed
from .standard import STANDARD_EPSILON, choose_standard
from .trace import canonical_trace_line


@dataclass(frozen=True)
class RunResult:
    fixture: dict
    observation: dict
    trace: dict
    line: bytes
    replicate: int


def run_fixture(fixture: dict, policy_id: str = "uniform_legal", replicate: int = 0,
                policy_seed: int | None = None) -> RunResult:
    observation = project_observation(fixture)
    memory = fixture["policy_memory"]
    pre_score_seed = (derive_seed(fixture["schema_version"], fixture["fixture_id"],
                                  replicate, "policy")
                      if policy_seed is None else policy_seed)
    rng = XorShift32(pre_score_seed)
    floor = apply_common_floor(observation, memory)
    if rng.draw_count != 0:
        raise AssertionError("scoring/filtering consumed policy RNG")
    standard_decision = None
    if policy_id == "standard":
        if fixture["schema_version"] != STANDARD_SCHEMA_VERSION:
            raise ValueError("standard policy requires ai-policy-fixture-v2")
        standard_decision = choose_standard(observation, floor, memory, rng)
        selected = standard_decision.selected_action_id
    else:
        selected = choose_action(policy_id, observation, floor, rng)
    reasons = sorted(set(floor.reasons) | {
        reason for values in floor.excluded.values() for reason in values
    })
    if detects_aba_switch_loop(memory.get("decisions", [])):
        reasons.append("VOLUNTARY_SWITCH_LOOP_DETECTED")
        reasons.sort()
    if fixture["schema_version"] == STANDARD_SCHEMA_VERSION:
        observation_reasons = ["FAIR_PUBLIC_STATE_ONLY"]
    else:
        mask = fixture["observation_mask"]
        observation_reasons = [
            f"REVEALED_MOVE:{move}" for move in sorted(mask["revealed_moves"])
        ]
        if mask["item_revealed"]:
            observation_reasons.append("REVEALED_ITEM")
        if mask["ability_revealed"]:
            observation_reasons.append("REVEALED_ABILITY")
        observation_reasons.extend(
            f"REVEALED_BENCH_SLOT:{slot}" for slot in sorted(mask["revealed_bench_slots"])
        )
        if fixture["information_mode"] == "challenge":
            observation_reasons.append("AUTHORIZED_FULL_TEAM_INFORMATION")
    trace = {
        "candidate_contract": candidate_contract(observation, memory),
        "coverage_tags": sorted(fixture["expected"]["coverage_tags"]),
        "excluded_action_ids": sorted(floor.excluded),
        "fixture_id": fixture["fixture_id"],
        "hard_floor_reasons": reasons,
        "information_mode": fixture["information_mode"],
        "legal_action_ids": list(floor.legal_ids),
        "observation_hash": observation_hash(observation),
        "observation_reasons": observation_reasons,
        "policy_config_id": fixture["policy_config_id"],
        "policy_id": policy_id,
        "policy_rng": {
            "draw_count": rng.draw_count,
            "post_state": rng.state,
            "pre_state": pre_score_seed or 0x6D2B79F5,
        },
        "profile": fixture["profile"],
        "schema_version": fixture["schema_version"],
        "selected_action_id": selected,
    }
    if standard_decision is not None:
        standard_reasons = sorted({
            reason
            for diagnostic in standard_decision.diagnostics
            for reason in diagnostic["admission_reasons"]
        })
        trace["standard_policy"] = {
            "best_score": standard_decision.best_score,
            "candidate_diagnostics": list(standard_decision.diagnostics),
            "epsilon": STANDARD_EPSILON,
            "near_best_action_ids": list(standard_decision.near_best_ids),
            "reasons": standard_reasons,
        }
    return RunResult(fixture, observation, trace, canonical_trace_line(trace), replicate)


def run_all(fixtures: list[dict], policy_id: str = "uniform_legal", replicate: int = 0) -> list[RunResult]:
    return [run_fixture(fixture, policy_id, replicate) for fixture in fixtures]


def replay_matches(fixture: dict, policy_id: str = "uniform_legal", replicate: int = 0) -> bool:
    return run_fixture(fixture, policy_id, replicate).line == run_fixture(fixture, policy_id, replicate).line


def twin_mismatches(results: list[RunResult]) -> list[dict]:
    groups: dict[str, list[RunResult]] = {}
    for result in results:
        group = result.fixture.get("twin_group")
        if group:
            groups.setdefault(group, []).append(result)
    mismatches = []
    for group, pair in sorted(groups.items()):
        if len(pair) != 2:
            mismatches.append({"group": group, "fields": ["pair_size"]})
            continue
        left, right = pair
        common_seed = left.trace["policy_rng"]["pre_state"]
        left_common = run_fixture(left.fixture, left.trace["policy_id"], policy_seed=common_seed)
        right_common = run_fixture(right.fixture, right.trace["policy_id"], policy_seed=common_seed)
        differing = []
        comparisons = {
            "observation": (left.observation, right.observation),
            "observation_hash": (left.trace["observation_hash"], right.trace["observation_hash"]),
            "candidate_contract": (left.trace["candidate_contract"], right.trace["candidate_contract"]),
            "draw_count": (left_common.trace["policy_rng"]["draw_count"], right_common.trace["policy_rng"]["draw_count"]),
            "selected_action": (left_common.trace["selected_action_id"], right_common.trace["selected_action_id"]),
        }
        if left.trace["policy_id"] == "standard":
            comparisons["policy_diagnostics"] = (
                left_common.trace["standard_policy"], right_common.trace["standard_policy"])
        for field, values in comparisons.items():
            if values[0] != values[1]:
                differing.append(field)
        if differing:
            mismatches.append({"group": group, "fields": differing})
    return mismatches
