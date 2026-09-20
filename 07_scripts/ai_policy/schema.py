"""Fail-closed loading and validation for versioned synthetic fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import POLICY_CONFIG_ID, SCHEMA_VERSION
from .rng import derive_seed


REQUIRED_FIELDS = frozenset({
    "schema_version", "fixture_id", "source_revision", "mechanics_config_id",
    "battle_mode", "power_profile", "scaling_profile", "rules_profile",
    "truth_state", "public_history", "observation_mask", "own_party",
    "policy_memory", "profile", "information_mode", "policy_config_id",
    "seeds", "expected",
})
EXPECTED_FIELDS = frozenset({
    "legal_actions", "allowed_best_set", "forbidden_actions", "required_reasons",
    "repeat_exceptions", "coverage_tags",
})
SEED_FIELDS = frozenset({"team", "battle", "decision"})
ACTION_FIELD_ORDER = (
    "id", "kind", "legal", "productive", "known_no_effect", "pure_status",
    "robust_safe_ko", "redundant_status", "stat_stage_before", "stat_stage_after",
    "effect_family", "positive_marginal_exception", "expected_damage",
    "switch_legal", "entry_survives", "forced", "fallback_cost",
    "switch_from", "switch_to",
)
ACTION_FIELDS = frozenset(ACTION_FIELD_ORDER)
PUBLIC_ACTIVE_FIELDS = ("species", "level", "hp_fraction", "status", "stat_stages")
OPPONENT_FIELDS = frozenset(PUBLIC_ACTIVE_FIELDS + ("moves", "item", "ability", "hidden_stats"))
HIDDEN_STAT_FIELDS = frozenset({"ivs", "evs", "nature", "speed"})
MEMORY_DECISION_FIELDS = frozenset({
    "action_id", "kind", "effect_family", "success", "public_result",
    "switch_from", "switch_to", "forced",
})
INFO_MODES = frozenset({"fair", "challenge"})
ACTION_KINDS = frozenset({"move", "switch"})
PUBLIC_HISTORY_KEYS = frozenset({
    "turn", "effect", "status", "inference", "calculation", "own_attack_stage",
    "revealed_ability", "lock", "threat", "moves_seen", "all_lines",
    "accuracy_drops", "own_hp_fraction",
})


class FixtureError(ValueError):
    """A fixture cannot be trusted as an executable contract."""


def _require_exact_keys(value: dict, required: frozenset[str], label: str) -> None:
    missing = sorted(required - value.keys())
    unknown = sorted(value.keys() - required)
    if missing or unknown:
        raise FixtureError(f"{label}: missing={missing}, unknown={unknown}")


def _non_empty_string(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value:
        raise FixtureError(f"{label} must be a non-empty string")


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise FixtureError(f"{label} must be a string list")
    if len(value) != len(set(value)):
        raise FixtureError(f"{label} contains duplicates")
    return value


def validate_action(action: Any, fixture_id: str) -> None:
    if not isinstance(action, dict):
        raise FixtureError(f"{fixture_id}: action must be an object")
    _require_exact_keys(action, ACTION_FIELDS, f"{fixture_id}: action")
    _non_empty_string(action["id"], f"{fixture_id}: action.id")
    if action["kind"] not in ACTION_KINDS:
        raise FixtureError(f"{fixture_id}: unknown action kind")
    for field in ("legal", "productive", "known_no_effect", "pure_status",
                  "robust_safe_ko", "redundant_status", "positive_marginal_exception",
                  "switch_legal", "entry_survives", "forced"):
        if not isinstance(action[field], bool):
            raise FixtureError(f"{fixture_id}: action.{field} must be boolean")
    for field in ("stat_stage_before", "stat_stage_after", "expected_damage", "fallback_cost"):
        if not isinstance(action[field], int) or isinstance(action[field], bool):
            raise FixtureError(f"{fixture_id}: action.{field} must be integer")
    if not -6 <= action["stat_stage_before"] <= 6 or not -6 <= action["stat_stage_after"] <= 6:
        raise FixtureError(f"{fixture_id}: stat stages must be in [-6, 6]")
    if action["expected_damage"] < 0 or action["fallback_cost"] < 0:
        raise FixtureError(f"{fixture_id}: damage/cost cannot be negative")
    if action["effect_family"] is not None:
        _non_empty_string(action["effect_family"], f"{fixture_id}: effect_family")
    for field in ("switch_from", "switch_to"):
        if action[field] is not None:
            _non_empty_string(action[field], f"{fixture_id}: {field}")
    if not action["legal"] and (action["productive"] or action["robust_safe_ko"] or action["forced"]):
        raise FixtureError(f"{fixture_id}: illegal action claims productive/KO/forced")
    if action["known_no_effect"] and action["productive"]:
        raise FixtureError(f"{fixture_id}: known no-effect action claims productive")
    if action["redundant_status"] and (not action["pure_status"] or action["productive"]):
        raise FixtureError(f"{fixture_id}: redundant status contradiction")
    if action["robust_safe_ko"] and (not action["productive"] or action["pure_status"]):
        raise FixtureError(f"{fixture_id}: robust KO contradiction")
    if action["kind"] == "switch":
        if action["effect_family"] is not None or action["pure_status"] or action["expected_damage"]:
            raise FixtureError(f"{fixture_id}: switch carries move-only facts")
        if not action["switch_from"] or not action["switch_to"]:
            raise FixtureError(f"{fixture_id}: switch requires an edge")
        if action["legal"] != action["switch_legal"]:
            raise FixtureError(f"{fixture_id}: switch legality contradiction")
    elif action["switch_from"] is not None or action["switch_to"] is not None:
        raise FixtureError(f"{fixture_id}: move carries switch edge")


def validate_fixture(fixture: Any) -> None:
    if not isinstance(fixture, dict):
        raise FixtureError("fixture must be an object")
    unknown = sorted(fixture.keys() - (REQUIRED_FIELDS | {"twin_group", "twin_kind"}))
    missing = sorted(REQUIRED_FIELDS - fixture.keys())
    if missing or unknown:
        raise FixtureError(f"fixture: missing={missing}, unknown={unknown}")
    if fixture["schema_version"] != SCHEMA_VERSION:
        raise FixtureError(f"{fixture.get('fixture_id', '<unknown>')}: unknown schema")
    fixture_id = fixture["fixture_id"]
    for field in ("fixture_id", "source_revision", "mechanics_config_id", "battle_mode",
                  "power_profile", "scaling_profile", "rules_profile", "profile",
                  "policy_config_id"):
        _non_empty_string(fixture[field], f"{fixture_id}: {field}")
    if fixture["policy_config_id"] != POLICY_CONFIG_ID:
        raise FixtureError(f"{fixture_id}: unknown policy config")
    if fixture["information_mode"] not in INFO_MODES:
        raise FixtureError(f"{fixture_id}: unknown information mode")
    for field in ("truth_state", "observation_mask", "policy_memory", "seeds", "expected"):
        if not isinstance(fixture[field], dict):
            raise FixtureError(f"{fixture_id}: {field} must be an object")
    if not isinstance(fixture["public_history"], list) or not isinstance(fixture["own_party"], list):
        raise FixtureError(f"{fixture_id}: history and own_party must be lists")
    truth = fixture["truth_state"]
    _require_exact_keys(truth, frozenset({"opponent_active", "opponent_bench", "field",
                                          "submitted_action", "future_rng", "actions"}),
                        f"{fixture_id}: truth_state")
    if not isinstance(truth["opponent_active"], dict) or not isinstance(truth["opponent_bench"], list):
        raise FixtureError(f"{fixture_id}: invalid opponent state")
    if not isinstance(truth["field"], dict) or not isinstance(truth["actions"], list) or not truth["actions"]:
        raise FixtureError(f"{fixture_id}: field/actions malformed or empty")
    active = truth["opponent_active"]
    _require_exact_keys(active, OPPONENT_FIELDS, f"{fixture_id}: opponent active")
    for label, mon in [("opponent active", active), *[
            (f"opponent bench {slot}", bench_mon)
            for slot, bench_mon in enumerate(truth["opponent_bench"])]]:
        if not isinstance(mon, dict):
            raise FixtureError(f"{fixture_id}: {label} must be an object")
        _require_exact_keys(mon, OPPONENT_FIELDS, f"{fixture_id}: {label}")
        if not isinstance(mon["moves"], list):
            raise FixtureError(f"{fixture_id}: {label}.moves must be a list")
        for move in mon["moves"]:
            if (not isinstance(move, dict) or set(move) != {"id", "pp"}
                    or not isinstance(move["id"], str) or not move["id"]
                    or not isinstance(move["pp"], int) or isinstance(move["pp"], bool)
                    or move["pp"] < 0):
                raise FixtureError(f"{fixture_id}: {label} has malformed move data")
        for field in ("item", "ability"):
            _non_empty_string(mon[field], f"{fixture_id}: {label}.{field}")
        if not isinstance(mon["hidden_stats"], dict):
            raise FixtureError(f"{fixture_id}: {label}.hidden_stats must be an object")
        _require_exact_keys(mon["hidden_stats"], HIDDEN_STAT_FIELDS,
                            f"{fixture_id}: {label}.hidden_stats")
    if set(truth["field"]) - {"weather", "hazards"}:
        raise FixtureError(f"{fixture_id}: field contains non-public/unknown keys")
    mask = fixture["observation_mask"]
    _require_exact_keys(mask, frozenset({"revealed_moves", "item_revealed", "ability_revealed",
                                         "revealed_bench_slots"}), f"{fixture_id}: observation_mask")
    _string_list(mask["revealed_moves"], f"{fixture_id}: revealed_moves")
    if not isinstance(mask["item_revealed"], bool) or not isinstance(mask["ability_revealed"], bool):
        raise FixtureError(f"{fixture_id}: reveal flags must be boolean")
    if (not isinstance(mask["revealed_bench_slots"], list)
            or any(not isinstance(slot, int) or isinstance(slot, bool) or slot < 0
                   for slot in mask["revealed_bench_slots"])):
        raise FixtureError(f"{fixture_id}: revealed_bench_slots must be non-negative integers")
    if any(slot >= len(truth["opponent_bench"]) for slot in mask["revealed_bench_slots"]):
        raise FixtureError(f"{fixture_id}: revealed bench slot out of range")
    move_ids = {
        move.get("id") for move in active["moves"]
        if isinstance(move, dict) and isinstance(move.get("id"), str)
    }
    if len(move_ids) != len(active["moves"]) or not set(mask["revealed_moves"]) <= move_ids:
        raise FixtureError(f"{fixture_id}: move list or revealed move mask is invalid")
    for event in fixture["public_history"]:
        if not isinstance(event, dict) or not set(event) <= PUBLIC_HISTORY_KEYS:
            raise FixtureError(f"{fixture_id}: public history event has unknown fields")
        if "moves_seen" in event:
            if set(_string_list(event["moves_seen"], f"{fixture_id}: moves_seen")) != set(mask["revealed_moves"]):
                raise FixtureError(f"{fixture_id}: move reveal history contradicts mask")
        if "revealed_ability" in event and not mask["ability_revealed"]:
            raise FixtureError(f"{fixture_id}: ability reveal history contradicts mask")
    decisions = fixture["policy_memory"].get("decisions")
    if set(fixture["policy_memory"]) != {"decisions"} or not isinstance(decisions, list) or len(decisions) > 4:
        raise FixtureError(f"{fixture_id}: memory must contain at most four decisions")
    for decision in decisions:
        if not isinstance(decision, dict):
            raise FixtureError(f"{fixture_id}: memory decision must be an object")
        _require_exact_keys(decision, MEMORY_DECISION_FIELDS, f"{fixture_id}: memory decision")
        if decision["kind"] not in ACTION_KINDS:
            raise FixtureError(f"{fixture_id}: memory decision has unknown kind")
        for field in ("success", "forced"):
            if not isinstance(decision[field], bool):
                raise FixtureError(f"{fixture_id}: memory decision.{field} must be boolean")
    _require_exact_keys(fixture["seeds"], SEED_FIELDS, f"{fixture_id}: seeds")
    if any(not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 0xFFFFFFFF
           for value in fixture["seeds"].values()):
        raise FixtureError(f"{fixture_id}: seeds must be uint32")
    expected_seeds = {
        "team": derive_seed(SCHEMA_VERSION, fixture_id, 0, "team"),
        "battle": derive_seed(SCHEMA_VERSION, fixture_id, 0, "battle"),
        "decision": derive_seed(SCHEMA_VERSION, fixture_id, 0, "policy"),
    }
    if fixture["seeds"] != expected_seeds:
        raise FixtureError(f"{fixture_id}: seed fields do not match deterministic derivation")
    _require_exact_keys(fixture["expected"], EXPECTED_FIELDS, f"{fixture_id}: expected")
    expected = fixture["expected"]
    for field in EXPECTED_FIELDS:
        _string_list(expected[field], f"{fixture_id}: expected.{field}")
    action_ids: list[str] = []
    for action in truth["actions"]:
        validate_action(action, fixture_id)
        action_ids.append(action["id"])
    if len(action_ids) != len(set(action_ids)):
        raise FixtureError(f"{fixture_id}: duplicate action ID")
    ids = set(action_ids)
    legal = {action["id"] for action in truth["actions"] if action["legal"]}
    if legal != set(expected["legal_actions"]):
        raise FixtureError(f"{fixture_id}: expected legal set contradicts truth")
    for field in ("allowed_best_set", "forbidden_actions"):
        if not set(expected[field]) <= ids:
            raise FixtureError(f"{fixture_id}: expected.{field} references unknown action")
    if not set(expected["allowed_best_set"]) <= legal or not expected["allowed_best_set"]:
        raise FixtureError(f"{fixture_id}: allowed best set must be non-empty and legal")
    if set(expected["allowed_best_set"]) & set(expected["forbidden_actions"]):
        raise FixtureError(f"{fixture_id}: allowed/forbidden contradiction")
    forced = [action["id"] for action in truth["actions"] if action["legal"] and action["forced"]]
    if forced and set(expected["allowed_best_set"]) != set(forced):
        raise FixtureError(f"{fixture_id}: forced actions contradict allowed best set")
    if ("twin_group" in fixture) != ("twin_kind" in fixture):
        raise FixtureError(f"{fixture_id}: twin group/kind must appear together")
    if "twin_group" in fixture:
        _non_empty_string(fixture["twin_group"], f"{fixture_id}: twin_group")
        _non_empty_string(fixture["twin_kind"], f"{fixture_id}: twin_kind")


def load_fixtures(path: Path | str) -> list[dict]:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FixtureError(f"cannot load fixture document: {error}") from error
    if not isinstance(document, dict) or set(document) != {"schema_version", "fixtures"}:
        raise FixtureError("fixture document must contain only schema_version and fixtures")
    if document["schema_version"] != SCHEMA_VERSION:
        raise FixtureError("fixture document has unknown schema")
    if not isinstance(document["fixtures"], list) or not document["fixtures"]:
        raise FixtureError("fixture document must have a non-empty fixture list")
    seen: set[str] = set()
    twin_groups: dict[str, list[dict]] = {}
    for fixture in document["fixtures"]:
        if isinstance(fixture, dict):
            actions = fixture.get("truth_state", {}).get("actions", [])
            for index, action in enumerate(actions):
                if isinstance(action, list):
                    if len(action) != len(ACTION_FIELD_ORDER):
                        raise FixtureError(
                            f"{fixture.get('fixture_id', '<unknown>')}: compact action has "
                            f"{len(action)} fields, expected {len(ACTION_FIELD_ORDER)}")
                    actions[index] = dict(zip(ACTION_FIELD_ORDER, action))
        validate_fixture(fixture)
        fixture_id = fixture["fixture_id"]
        if fixture_id in seen:
            raise FixtureError(f"duplicate fixture ID: {fixture_id}")
        seen.add(fixture_id)
        if "twin_group" in fixture:
            twin_groups.setdefault(fixture["twin_group"], []).append(fixture)
    for group, twins in twin_groups.items():
        if len(twins) != 2 or twins[0]["twin_kind"] != twins[1]["twin_kind"]:
            raise FixtureError(f"twin group {group} must contain exactly one matching pair")
    return document["fixtures"]
