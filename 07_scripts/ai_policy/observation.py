"""Explicit referee-truth to policy-observation projection."""

from __future__ import annotations

import hashlib
import json

from . import STANDARD_SCHEMA_VERSION


PUBLIC_ACTIVE_FIELDS = ("species", "level", "hp_fraction", "status", "stat_stages")
CHALLENGE_FIELDS = ("species", "level", "hp_fraction", "status", "stat_stages",
                    "moves", "item", "ability", "hidden_stats")
ACTION_VISIBLE_FIELDS = (
    "id", "kind", "legal", "productive", "known_no_effect", "pure_status",
    "robust_safe_ko", "redundant_status", "stat_stage_before", "stat_stage_after",
    "effect_family", "positive_marginal_exception", "expected_damage",
    "switch_legal", "entry_survives", "forced", "fallback_cost",
    "switch_from", "switch_to",
)
STANDARD_ACTION_VISIBLE_FIELDS = ACTION_VISIBLE_FIELDS + (
    "net_faints", "opponent_hp_fraction_lost", "own_hp_fraction_lost",
    "immediate_future_gain", "entry_cost", "repeat_cost", "uncertainty_cost",
    "standard_switch_emergency",
)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _fair_active(active: dict, mask: dict) -> dict:
    result = {field: active[field] for field in PUBLIC_ACTIVE_FIELDS}
    allowed_moves = set(mask["revealed_moves"])
    result["moves"] = [
        {"id": move["id"], "pp": move.get("pp")}
        for move in active["moves"] if move["id"] in allowed_moves
    ]
    result["item"] = active["item"] if mask["item_revealed"] else None
    result["ability"] = active["ability"] if mask["ability_revealed"] else None
    return result


def _fair_bench(bench: list[dict], mask: dict) -> list[dict]:
    revealed = set(mask["revealed_bench_slots"])
    result = []
    for slot, mon in enumerate(bench):
        if slot in revealed:
            result.append({field: mon[field] for field in PUBLIC_ACTIVE_FIELDS})
        else:
            result.append({"unknown": True})
    return result


def project_observation(fixture: dict) -> dict:
    if fixture["schema_version"] == STANDARD_SCHEMA_VERSION:
        public = fixture["public_state"]
        return {
            "schema_version": fixture["schema_version"],
            "battle_mode": public["battle_mode"],
            "field": public["field"],
            "public_history": public["public_history"],
            "own_party": public["own_party"],
            "opponent_active": public["opponent_active"],
            "opponent_bench": public["opponent_bench"],
            "candidates": [
                {field: action[field] for field in STANDARD_ACTION_VISIBLE_FIELDS}
                for action in fixture["candidates"]
            ],
        }
    truth = fixture["truth_state"]
    mode = fixture["information_mode"]
    if mode == "challenge":
        opponent_active = {field: truth["opponent_active"][field] for field in CHALLENGE_FIELDS}
        opponent_bench = [
            {field: mon[field] for field in CHALLENGE_FIELDS}
            for mon in truth["opponent_bench"]
        ]
    elif mode == "fair":
        opponent_active = _fair_active(truth["opponent_active"], fixture["observation_mask"])
        opponent_bench = _fair_bench(truth["opponent_bench"], fixture["observation_mask"])
    else:
        raise ValueError(f"unknown information mode: {mode}")
    # submitted_action and future_rng are intentionally unreachable here.
    return {
        "schema_version": fixture["schema_version"],
        "battle_mode": fixture["battle_mode"],
        "field": truth["field"],
        "public_history": fixture["public_history"],
        "own_party": fixture["own_party"],
        "opponent_active": opponent_active,
        "opponent_bench": opponent_bench,
        "candidates": [
            {field: action[field] for field in ACTION_VISIBLE_FIELDS}
            for action in truth["actions"]
        ],
    }


def observation_hash(observation: dict) -> str:
    return hashlib.sha256(canonical_json(observation).encode("utf-8")).hexdigest()
