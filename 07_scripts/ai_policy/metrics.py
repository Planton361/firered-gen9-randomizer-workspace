"""Aggregate behavioral accounting for synthetic fixture executions."""

from __future__ import annotations

from .memory import consecutive_successes, detects_aba_switch_loop
from .runner import RunResult, replay_matches, twin_mismatches


def _rate(numerator: int, denominator: int) -> float | None:
    return None if denominator == 0 else numerator / denominator


def summarize(results: list[RunResult]) -> dict:
    illegal = invalid = missed_ko = redundant = harmful_repeat = 0
    productive_opportunities = ko_opportunities = redundant_opportunities = repeat_opportunities = 0
    switch_loops = 0
    replay_mismatches = 0
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
    twin_errors = twin_mismatches(results)
    submitted_errors = [error for error in twin_errors if error["group"].startswith("submitted_action")]
    return {
        "decision_count": len(results),
        "deterministic_replay_mismatch_count": replay_mismatches,
        "harmful_repeated_status": {
            "count": harmful_repeat,
            "opportunities": repeat_opportunities,
            "rate": _rate(harmful_repeat, repeat_opportunities),
        },
        "hidden_information_twin_mismatch_count": len(twin_errors) - len(submitted_errors),
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
        "redundant_status": {
            "count": redundant,
            "opportunities": redundant_opportunities,
            "rate": _rate(redundant, redundant_opportunities),
        },
        "submitted_action_twin_mismatch_count": len(submitted_errors),
        "switch_loop_detection_count": switch_loops,
    }
