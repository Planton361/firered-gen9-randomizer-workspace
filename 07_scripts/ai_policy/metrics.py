"""Aggregate behavioral accounting for synthetic fixture executions."""

from __future__ import annotations

import statistics

from . import IRONMON_SCHEMA_VERSION, STANDARD_SCHEMA_VERSION
from .floor import apply_common_floor
from .ironmon import SWITCH_RANDOM_MIN, ironmon_utility, response_distribution
from .memory import consecutive_successes, detects_aba_switch_loop
from .runner import RunResult, replay_matches, twin_mismatches
from .standard import STANDARD_EPSILON, standard_admitted_ids, utility


def _rate(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else numerator / denominator


def summarize(results: list[RunResult]) -> dict:
    illegal = invalid = missed_ko = redundant = harmful_repeat = 0
    productive_opportunities = ko_opportunities = redundant_opportunities = repeat_opportunities = 0
    switch_loops = 0
    replay_mismatches = 0
    oracle_agreements = 0
    allowed_best_violations: list[str] = []
    chosen_utilities: list[int] = []
    utility_regrets: list[int] = []
    fixture_allowed_utility_regrets: list[int] = []
    near_best_compliant = 0
    near_best_opportunities = 0
    near_best_violations: list[str] = []
    rng_draws = 0
    rng_zero_draws = 0
    rng_one_draws = 0
    max_rng_draws = 0
    non_emergency_switches = 0
    non_emergency_switch_opportunities = 0
    ironmon_switch_threshold_violations = 0
    ironmon_switch_threshold_opportunities = 0
    ironmon_below_threshold_selections: list[dict] = []
    ironmon_switch_candidate_audits: list[dict] = []
    ironmon_loop_guard_violations = 0
    ironmon_loop_guard_opportunities = 0
    response_no_known = 0
    response_partial_unknown = 0
    response_all_revealed = 0
    response_max_branches = 0
    response_switch_weight_sum = 0
    for result in results:
        actions = {action["id"]: action for action in result.observation["candidates"]}
        selected = actions[result.trace["selected_action_id"]]
        productive_exists = any(action["legal"] and action["productive"] for action in actions.values())
        robust_ko_exists = any(action["legal"] and action["robust_safe_ko"] for action in actions.values())
        redundant_exists = any(action["legal"] and action["redundant_status"] for action in actions.values())
        if productive_exists:
            productive_opportunities += 1
        if robust_ko_exists:
            ko_opportunities += 1
        if redundant_exists:
            redundant_opportunities += 1
        illegal += not selected["legal"]
        invalid += bool(productive_exists and (selected["known_no_effect"] or not selected["productive"]))
        missed_ko += bool(robust_ko_exists and not selected["robust_safe_ko"])
        redundant += bool(selected["redundant_status"])
        repeat_candidates = [
            action for action in actions.values()
            if action["legal"] and action["pure_status"]
            and consecutive_successes(result.fixture["policy_memory"]["decisions"],
                                      action["effect_family"]) >= 2
            and not action["positive_marginal_exception"]
        ]
        repeat_opportunities += bool(repeat_candidates)
        harmful_repeat += bool(selected in repeat_candidates)
        switch_loops += detects_aba_switch_loop(result.fixture["policy_memory"]["decisions"])
        replay_mismatches += not replay_matches(
            result.fixture, result.trace["policy_id"], replicate=result.replicate)
        allowed = result.fixture["expected"]["allowed_best_set"]
        if selected["id"] in allowed:
            oracle_agreements += 1
        else:
            allowed_best_violations.append(result.fixture["fixture_id"])
        draws = result.trace["policy_rng"]["draw_count"]
        rng_draws += draws
        rng_zero_draws += draws == 0
        rng_one_draws += draws == 1
        max_rng_draws = max(max_rng_draws, draws)
        if result.fixture["schema_version"] == STANDARD_SCHEMA_VERSION:
            scores = {action_id: utility(action).total for action_id, action in actions.items()}
            chosen_utilities.append(scores[selected["id"]])
            floor = apply_common_floor(result.observation, result.fixture["policy_memory"])
            if result.trace["policy_id"] == "standard":
                policy_eligible = [
                    diagnostic["action_id"]
                    for diagnostic in result.trace["standard_policy"]["candidate_diagnostics"]
                    if diagnostic["standard_eligible"]
                ]
            else:
                policy_eligible = list(floor.eligible_ids)
            best_eligible = max(scores[action_id] for action_id in policy_eligible)
            utility_regrets.append(best_eligible - scores[selected["id"]])
            standard_eligible = standard_admitted_ids(
                result.observation, floor, result.fixture["policy_memory"])
            standard_best = max(scores[action_id] for action_id in standard_eligible)
            standard_near_best = {
                action_id for action_id in standard_eligible
                if scores[action_id] >= standard_best - STANDARD_EPSILON
            }
            near_best_opportunities += 1
            if selected["id"] in standard_near_best:
                near_best_compliant += 1
            else:
                near_best_violations.append(result.fixture["fixture_id"])
            non_emergency_candidates = [
                action for action in actions.values()
                if action["kind"] == "switch" and not action["forced"]
                and not action["standard_switch_emergency"]
            ]
            non_emergency_switch_opportunities += bool(non_emergency_candidates)
            non_emergency_switches += bool(
                selected["kind"] == "switch" and not selected["forced"]
                and not selected["standard_switch_emergency"])
        elif result.fixture["schema_version"] == IRONMON_SCHEMA_VERSION:
            floor = apply_common_floor(result.observation, result.fixture["policy_memory"])
            utility_rows = {
                action_id: ironmon_utility(
                    action, response_distribution(result.observation),
                    result.fixture["policy_memory"])
                for action_id, action in actions.items()
            }
            chosen_utilities.append(utility_rows[selected["id"]].total)
            allowed_scores = [
                utility_rows[action_id].total
                for action_id in result.fixture["expected"]["allowed_best_set"]
            ]
            fixture_allowed_utility_regrets.append(
                max(0, max(allowed_scores) - utility_rows[selected["id"]].total))
            model = result.observation["response_model"]
            response_switch_weight_sum += model["opponent_switch_weight"]
            branch_count = len(response_distribution(result.observation))
            response_max_branches = max(response_max_branches, branch_count)
            if not model["revealed_moves"]:
                response_no_known += 1
            elif model["unknown_move_slots"]:
                response_partial_unknown += 1
            else:
                response_all_revealed += 1
            if result.trace["policy_id"] == "ironmon_smart":
                ironmon = result.trace["ironmon_policy"]
                diagnostics = {
                    item["action_id"]: item for item in ironmon["candidate_diagnostics"]
                }
                eligible = [
                    action_id for action_id, diagnostic in diagnostics.items()
                    if diagnostic["ironmon_eligible"]
                ]
                near_best_opportunities += 1
                if selected["id"] in ironmon["near_best_action_ids"]:
                    near_best_compliant += 1
                else:
                    near_best_violations.append(result.fixture["fixture_id"])
                arbitration = ironmon["switch_arbitration"]
                guarded = [
                    diagnostic for diagnostic in diagnostics.values()
                    if set(diagnostic["admission_reasons"]) & {
                        "IRONMON_ABA_LOOP_GUARD",
                        "IRONMON_CONSECUTIVE_SWITCH_GUARD",
                    }
                ]
                ironmon_loop_guard_opportunities += bool(guarded)
                ironmon_loop_guard_violations += any(
                    diagnostic["selected"] for diagnostic in guarded)
                if arbitration["switch_candidates"] and arbitration["best_stay"] is not None:
                    ironmon_switch_threshold_opportunities += 1
                    selected_switch = selected["kind"] == "switch"
                    threshold = arbitration["threshold_class"]
                    admitted = arbitration["admission_rng"]["admitted"]
                    selected_advantage = (
                        utility_rows[selected["id"]].total
                        - arbitration["best_stay"]["score"]
                        if selected_switch else None
                    )
                    selected_below_minimum = bool(
                        selected_switch
                        and not selected["forced"]
                        and not selected["ironmon_switch_emergency"]
                        and selected_advantage < SWITCH_RANDOM_MIN
                    )
                    selected_nondominating_emergency = bool(
                        selected_switch
                        and selected["ironmon_switch_emergency"]
                        and selected_advantage <= 0
                    )
                    class_violation = (
                        (threshold == "below_12" and selected_switch)
                        or (threshold == "at_least_20" and not selected_switch)
                        or (threshold == "random_12_19" and selected_switch != admitted)
                    )
                    violation = bool(
                        class_violation
                        or selected_below_minimum
                        or selected_nondominating_emergency)
                    ironmon_switch_threshold_violations += violation
                    if selected_below_minimum:
                        ironmon_below_threshold_selections.append({
                            "action_id": selected["id"],
                            "advantage": selected_advantage,
                            "fixture_id": result.fixture["fixture_id"],
                        })
                    ironmon_switch_candidate_audits.append({
                        "candidates": arbitration["switch_candidates"],
                        "fixture_id": result.fixture["fixture_id"],
                        "selected_action_id": selected["id"],
                        "selected_candidate_advantage": selected_advantage,
                    })
            elif result.trace["policy_id"] == "standard":
                eligible = [
                    diagnostic["action_id"]
                    for diagnostic in result.trace["standard_policy"]["candidate_diagnostics"]
                    if diagnostic["standard_eligible"]
                ]
            else:
                eligible = list(floor.eligible_ids)
            best_eligible = max(utility_rows[action_id].total for action_id in eligible)
            utility_regrets.append(best_eligible - utility_rows[selected["id"]].total)
    twin_errors = twin_mismatches(results)
    submitted_errors = [error for error in twin_errors if error["kind"] == "submitted_action"]
    future_rng_errors = [error for error in twin_errors if error["kind"] == "future_rng"]
    hidden_errors = [
        error for error in twin_errors
        if error["kind"] not in {"submitted_action", "future_rng"}
    ]

    def distribution(values: list[int]) -> dict:
        return {
            "average": None if not values else sum(values) / len(values),
            "count": len(values),
            "maximum": None if not values else max(values),
            "median": None if not values else statistics.median(values),
            "minimum": None if not values else min(values),
            "sum": sum(values),
        }

    return {
        "allowed_best_compliance": {
            "count": oracle_agreements,
            "opportunities": len(results),
            "rate": _rate(oracle_agreements, len(results)),
            "violations": allowed_best_violations,
        },
        "chosen_utility": distribution(chosen_utilities),
        "decision_count": len(results),
        "deterministic_replay_mismatch_count": replay_mismatches,
        "harmful_repeated_status": {
            "count": harmful_repeat,
            "opportunities": repeat_opportunities,
            "rate": _rate(harmful_repeat, repeat_opportunities),
        },
        "future_rng_twin_mismatch_count": len(future_rng_errors),
        "fixture_allowed_utility_regret": distribution(fixture_allowed_utility_regrets),
        "hidden_information_twin_mismatch_count": len(hidden_errors),
        "illegal_action": {"count": illegal, "rate": _rate(illegal, len(results))},
        "invalid_no_effect": {
            "count": invalid,
            "opportunities": productive_opportunities,
            "rate": _rate(invalid, productive_opportunities),
        },
        "missed_robust_ko": {
            "count": missed_ko,
            "opportunities": ko_opportunities,
            "rate": _rate(missed_ko, ko_opportunities),
        },
        "near_best_compliance": {
            "count": near_best_compliant,
            "opportunities": near_best_opportunities,
            "rate": _rate(near_best_compliant, near_best_opportunities),
            "violations": near_best_violations,
        },
        "oracle_agreement": {
            "count": oracle_agreements,
            "opportunities": len(results),
            "rate": _rate(oracle_agreements, len(results)),
        },
        "policy_rng_draws": {
            "maximum_per_decision": max_rng_draws,
            "one_draw_decisions": rng_one_draws,
            "total": rng_draws,
            "zero_draw_decisions": rng_zero_draws,
        },
        "redundant_status": {
            "count": redundant,
            "opportunities": redundant_opportunities,
            "rate": _rate(redundant, redundant_opportunities),
        },
        "submitted_action_twin_mismatch_count": len(submitted_errors),
        "standard_non_emergency_voluntary_switch": {
            "count": non_emergency_switches,
            "opportunities": non_emergency_switch_opportunities,
            "rate": _rate(non_emergency_switches, non_emergency_switch_opportunities),
        },
        "ironmon_switch_threshold_violation": {
            "below_threshold_selected_count": len(
                ironmon_below_threshold_selections),
            "below_threshold_selections": ironmon_below_threshold_selections,
            "candidate_audits": ironmon_switch_candidate_audits,
            "count": ironmon_switch_threshold_violations,
            "opportunities": ironmon_switch_threshold_opportunities,
            "rate": _rate(
                ironmon_switch_threshold_violations,
                ironmon_switch_threshold_opportunities),
        },
        "ironmon_switch_loop_guard_violation": {
            "count": ironmon_loop_guard_violations,
            "opportunities": ironmon_loop_guard_opportunities,
            "rate": _rate(ironmon_loop_guard_violations, ironmon_loop_guard_opportunities),
        },
        "ironmon_response_model": {
            "all_revealed_cases": response_all_revealed,
            "maximum_branch_count": response_max_branches,
            "no_known_move_cases": response_no_known,
            "partial_unknown_cases": response_partial_unknown,
            "speculative_switch_weight_sum": response_switch_weight_sum,
        },
        "switch_loop_detection_count": switch_loops,
        "utility_regret": distribution(utility_regrets),
    }
