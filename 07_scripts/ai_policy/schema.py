"""Fail-closed loading and validation for versioned synthetic fixtures."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from . import (
    POLICY_CONFIG_ID,
    SCHEMA_VERSION,
    STANDARD_POLICY_CONFIG_ID,
    STANDARD_SCHEMA_VERSION,
)
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
STANDARD_ACTION_FIELD_ORDER = ACTION_FIELD_ORDER + (
    "net_faints", "opponent_hp_fraction_lost", "own_hp_fraction_lost",
    "immediate_future_gain", "entry_cost", "repeat_cost", "uncertainty_cost",
    "standard_switch_emergency",
)
STANDARD_ACTION_FIELDS = frozenset(STANDARD_ACTION_FIELD_ORDER)
STANDARD_DOCUMENT_FIELDS = frozenset({
    "schema_version", "source_revision", "policy_config_id", "defaults", "fixtures",
})
STANDARD_DEFAULT_FIELDS = frozenset({
    "profile", "information_mode", "public_state", "private_state", "policy_memory",
})
STANDARD_FIXTURE_FIELDS = frozenset({
    "fixture_id", "candidates", "seeds", "expected", "profile", "information_mode",
    "public_state", "private_state", "policy_memory", "twin_group", "twin_kind",
})
STANDARD_PUBLIC_STATE_FIELDS = frozenset({
    "battle_mode", "opponent_active", "opponent_bench", "own_party", "field",
    "public_history",
})
STANDARD_PUBLIC_ACTIVE_FIELDS = frozenset({
    "species", "hp_fraction", "status", "stat_stages",
})
STANDARD_OWN_PARTY_FIELDS = frozenset({"species", "hp_fraction"})
STANDARD_PRIVATE_STATE_FIELDS = frozenset({
    "hidden_opponent", "submitted_action", "future_rng",
})
STANDARD_LOADED_FIELDS = frozenset({
    "schema_version", "fixture_id", "source_revision", "profile", "information_mode",
    "policy_config_id", "public_state", "private_state", "policy_memory", "candidates",
    "seeds", "expected",
})
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


def validate_standard_action(action: Any, fixture_id: str) -> None:
    if not isinstance(action, dict):
        raise FixtureError(f"{fixture_id}: standard action must be an object")
    _require_exact_keys(action, STANDARD_ACTION_FIELDS, f"{fixture_id}: standard action")
    validate_action({field: action[field] for field in ACTION_FIELD_ORDER}, fixture_id)
    for field in (
            "net_faints", "opponent_hp_fraction_lost", "own_hp_fraction_lost",
            "immediate_future_gain", "entry_cost", "repeat_cost", "uncertainty_cost"):
        if not isinstance(action[field], int) or isinstance(action[field], bool):
            raise FixtureError(f"{fixture_id}: action.{field} must be integer")
    if not isinstance(action["standard_switch_emergency"], bool):
        raise FixtureError(f"{fixture_id}: action.standard_switch_emergency must be boolean")
    if not -1 <= action["net_faints"] <= 1:
        raise FixtureError(f"{fixture_id}: action.net_faints must be in [-1, 1]")
    if not 0 <= action["opponent_hp_fraction_lost"] <= 256:
        raise FixtureError(
            f"{fixture_id}: action.opponent_hp_fraction_lost must be in [0, 256]")
    if not -256 <= action["own_hp_fraction_lost"] <= 256:
        raise FixtureError(
            f"{fixture_id}: action.own_hp_fraction_lost must be in [-256, 256]")
    if not -40 <= action["immediate_future_gain"] <= 40:
        raise FixtureError(
            f"{fixture_id}: action.immediate_future_gain must be in [-40, 40]")
    for field in ("entry_cost", "repeat_cost", "uncertainty_cost"):
        if not 0 <= action[field] <= 2**31 - 1:
            raise FixtureError(f"{fixture_id}: action.{field} must be a non-negative int32")
    if action["kind"] == "move" and action["standard_switch_emergency"]:
        raise FixtureError(f"{fixture_id}: move cannot claim Standard switch emergency")


def _validate_policy_memory(memory: Any, fixture_id: str) -> None:
    if not isinstance(memory, dict):
        raise FixtureError(f"{fixture_id}: policy_memory must be an object")
    decisions = memory.get("decisions")
    if set(memory) != {"decisions"} or not isinstance(decisions, list) or len(decisions) > 4:
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


def validate_standard_fixture(fixture: Any) -> None:
    if not isinstance(fixture, dict):
        raise FixtureError("standard fixture must be an object")
    unknown = sorted(fixture.keys() - (STANDARD_LOADED_FIELDS | {"twin_group", "twin_kind"}))
    missing = sorted(STANDARD_LOADED_FIELDS - fixture.keys())
    if missing or unknown:
        raise FixtureError(f"standard fixture: missing={missing}, unknown={unknown}")
    fixture_id = fixture["fixture_id"]
    if fixture["schema_version"] != STANDARD_SCHEMA_VERSION:
        raise FixtureError(f"{fixture_id}: unknown Standard schema")
    for field in ("fixture_id", "source_revision", "profile", "policy_config_id"):
        _non_empty_string(fixture[field], f"{fixture_id}: {field}")
    if fixture["profile"] != "standard":
        raise FixtureError(f"{fixture_id}: Standard fixture must use profile standard")
    if fixture["information_mode"] != "fair":
        raise FixtureError(f"{fixture_id}: Standard v1 supports fair information only")
    if fixture["policy_config_id"] != STANDARD_POLICY_CONFIG_ID:
        raise FixtureError(f"{fixture_id}: unknown Standard policy config")
    public = fixture["public_state"]
    private = fixture["private_state"]
    if not isinstance(public, dict) or not isinstance(private, dict):
        raise FixtureError(f"{fixture_id}: public/private state must be objects")
    _require_exact_keys(public, STANDARD_PUBLIC_STATE_FIELDS, f"{fixture_id}: public_state")
    _require_exact_keys(private, STANDARD_PRIVATE_STATE_FIELDS, f"{fixture_id}: private_state")
    _non_empty_string(public["battle_mode"], f"{fixture_id}: battle_mode")
    if (not isinstance(public["opponent_active"], dict)
            or not isinstance(public["opponent_bench"], list)
            or not isinstance(public["own_party"], list)
            or not public["own_party"]
            or not isinstance(public["field"], dict)
            or not isinstance(public["public_history"], list)):
        raise FixtureError(f"{fixture_id}: malformed public state")
    _require_exact_keys(
        public["opponent_active"], STANDARD_PUBLIC_ACTIVE_FIELDS,
        f"{fixture_id}: public opponent active")
    public_opponents = [public["opponent_active"], *public["opponent_bench"]]
    for slot, mon in enumerate(public_opponents):
        if not isinstance(mon, dict):
            raise FixtureError(f"{fixture_id}: public opponent {slot} must be an object")
        _require_exact_keys(
            mon, STANDARD_PUBLIC_ACTIVE_FIELDS,
            f"{fixture_id}: public opponent {slot}")
        _non_empty_string(mon["species"], f"{fixture_id}: public opponent species")
        _non_empty_string(mon["status"], f"{fixture_id}: public opponent status")
        if (not isinstance(mon["hp_fraction"], int) or isinstance(mon["hp_fraction"], bool)
                or not 0 <= mon["hp_fraction"] <= 256):
            raise FixtureError(f"{fixture_id}: public opponent HP must be in [0, 256]")
        if (not isinstance(mon["stat_stages"], dict)
                or any(not isinstance(value, int) or isinstance(value, bool) or not -6 <= value <= 6
                       for value in mon["stat_stages"].values())):
            raise FixtureError(f"{fixture_id}: public stat stages must be integers in [-6, 6]")
    for slot, mon in enumerate(public["own_party"]):
        if not isinstance(mon, dict):
            raise FixtureError(f"{fixture_id}: own party {slot} must be an object")
        _require_exact_keys(mon, STANDARD_OWN_PARTY_FIELDS, f"{fixture_id}: own party {slot}")
        _non_empty_string(mon["species"], f"{fixture_id}: own party species")
        if (not isinstance(mon["hp_fraction"], int) or isinstance(mon["hp_fraction"], bool)
                or not 0 <= mon["hp_fraction"] <= 256):
            raise FixtureError(f"{fixture_id}: own HP must be in [0, 256]")
    if set(public["field"]) - {"weather", "hazards"}:
        raise FixtureError(f"{fixture_id}: public field contains unknown keys")
    for event in public["public_history"]:
        if not isinstance(event, dict) or not set(event) <= PUBLIC_HISTORY_KEYS:
            raise FixtureError(f"{fixture_id}: public history event has unknown fields")
    if not isinstance(private["hidden_opponent"], dict):
        raise FixtureError(f"{fixture_id}: hidden_opponent must be an object")
    _non_empty_string(private["submitted_action"], f"{fixture_id}: submitted_action")
    if (not isinstance(private["future_rng"], int) or isinstance(private["future_rng"], bool)
            or not 0 <= private["future_rng"] <= 0xFFFFFFFF):
        raise FixtureError(f"{fixture_id}: future_rng must be uint32")
    serialized_public = json.dumps(public, sort_keys=True)
    if any(name in serialized_public for name in ("hidden_opponent", "submitted_action", "future_rng")):
        raise FixtureError(f"{fixture_id}: private field leaked into public state")
    _validate_policy_memory(fixture["policy_memory"], fixture_id)
    _require_exact_keys(fixture["seeds"], SEED_FIELDS, f"{fixture_id}: seeds")
    if any(not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 0xFFFFFFFF
           for value in fixture["seeds"].values()):
        raise FixtureError(f"{fixture_id}: seeds must be uint32")
    expected_seeds = {
        "team": derive_seed(STANDARD_SCHEMA_VERSION, fixture_id, 0, "team"),
        "battle": derive_seed(STANDARD_SCHEMA_VERSION, fixture_id, 0, "battle"),
        "decision": derive_seed(STANDARD_SCHEMA_VERSION, fixture_id, 0, "policy"),
    }
    if fixture["seeds"] != expected_seeds:
        raise FixtureError(f"{fixture_id}: seed fields do not match deterministic derivation")
    if not isinstance(fixture["expected"], dict):
        raise FixtureError(f"{fixture_id}: expected must be an object")
    _require_exact_keys(fixture["expected"], EXPECTED_FIELDS, f"{fixture_id}: expected")
    for field in EXPECTED_FIELDS:
        _string_list(fixture["expected"][field], f"{fixture_id}: expected.{field}")
    candidates = fixture["candidates"]
    if not isinstance(candidates, list) or not candidates:
        raise FixtureError(f"{fixture_id}: candidates must be a non-empty list")
    action_ids: list[str] = []
    for action in candidates:
        validate_standard_action(action, fixture_id)
        action_ids.append(action["id"])
    if len(action_ids) != len(set(action_ids)):
        raise FixtureError(f"{fixture_id}: duplicate action ID")
    ids = set(action_ids)
    legal = {action["id"] for action in candidates if action["legal"]}
    expected = fixture["expected"]
    if legal != set(expected["legal_actions"]):
        raise FixtureError(f"{fixture_id}: expected legal set contradicts truth")
    for field in ("allowed_best_set", "forbidden_actions"):
        if not set(expected[field]) <= ids:
            raise FixtureError(f"{fixture_id}: expected.{field} references unknown action")
    if not set(expected["allowed_best_set"]) <= legal or not expected["allowed_best_set"]:
        raise FixtureError(f"{fixture_id}: allowed best set must be non-empty and legal")
    if set(expected["allowed_best_set"]) & set(expected["forbidden_actions"]):
        raise FixtureError(f"{fixture_id}: allowed/forbidden contradiction")
    forced = [action["id"] for action in candidates if action["legal"] and action["forced"]]
    if forced and set(expected["allowed_best_set"]) != set(forced):
        raise FixtureError(f"{fixture_id}: forced actions contradict allowed best set")
    if ("twin_group" in fixture) != ("twin_kind" in fixture):
        raise FixtureError(f"{fixture_id}: twin group/kind must appear together")
    if "twin_group" in fixture:
        _non_empty_string(fixture["twin_group"], f"{fixture_id}: twin_group")
        _non_empty_string(fixture["twin_kind"], f"{fixture_id}: twin_kind")


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


def _validate_collection(fixtures: list[dict]) -> list[dict]:
    seen: set[str] = set()
    twin_groups: dict[str, list[dict]] = {}
    for fixture in fixtures:
        fixture_id = fixture["fixture_id"]
        if fixture_id in seen:
            raise FixtureError(f"duplicate fixture ID: {fixture_id}")
        seen.add(fixture_id)
        if "twin_group" in fixture:
            twin_groups.setdefault(fixture["twin_group"], []).append(fixture)
    for group, twins in twin_groups.items():
        if len(twins) != 2 or twins[0]["twin_kind"] != twins[1]["twin_kind"]:
            raise FixtureError(f"twin group {group} must contain exactly one matching pair")
    return fixtures


def _load_v1_document(document: dict) -> list[dict]:
    if not isinstance(document, dict) or set(document) != {"schema_version", "fixtures"}:
        raise FixtureError("fixture document must contain only schema_version and fixtures")
    if not isinstance(document["fixtures"], list) or not document["fixtures"]:
        raise FixtureError("fixture document must have a non-empty fixture list")
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
    return _validate_collection(document["fixtures"])


def _load_standard_document(document: dict) -> list[dict]:
    _require_exact_keys(document, STANDARD_DOCUMENT_FIELDS, "Standard fixture document")
    if document["schema_version"] != STANDARD_SCHEMA_VERSION:
        raise FixtureError("fixture document has unknown Standard schema")
    _non_empty_string(document["source_revision"], "Standard source_revision")
    if document["policy_config_id"] != STANDARD_POLICY_CONFIG_ID:
        raise FixtureError("fixture document has unknown Standard policy config")
    defaults = document["defaults"]
    if not isinstance(defaults, dict):
        raise FixtureError("Standard fixture defaults must be an object")
    _require_exact_keys(defaults, STANDARD_DEFAULT_FIELDS, "Standard fixture defaults")
    raw_fixtures = document["fixtures"]
    if not isinstance(raw_fixtures, list) or not raw_fixtures:
        raise FixtureError("Standard fixture document must have a non-empty fixture list")
    materialized: list[dict] = []
    required = {"fixture_id", "candidates", "seeds", "expected"}
    for raw in raw_fixtures:
        if not isinstance(raw, dict):
            raise FixtureError("Standard fixture row must be an object")
        missing = sorted(required - raw.keys())
        unknown = sorted(raw.keys() - STANDARD_FIXTURE_FIELDS)
        if missing or unknown:
            raise FixtureError(f"Standard fixture row: missing={missing}, unknown={unknown}")
        fixture = {
            "schema_version": STANDARD_SCHEMA_VERSION,
            "fixture_id": raw["fixture_id"],
            "source_revision": document["source_revision"],
            "profile": copy.deepcopy(raw.get("profile", defaults["profile"])),
            "information_mode": copy.deepcopy(
                raw.get("information_mode", defaults["information_mode"])),
            "policy_config_id": document["policy_config_id"],
            "public_state": copy.deepcopy(raw.get("public_state", defaults["public_state"])),
            "private_state": copy.deepcopy(raw.get("private_state", defaults["private_state"])),
            "policy_memory": copy.deepcopy(raw.get("policy_memory", defaults["policy_memory"])),
            "candidates": copy.deepcopy(raw["candidates"]),
            "seeds": copy.deepcopy(raw["seeds"]),
            "expected": copy.deepcopy(raw["expected"]),
        }
        for optional in ("twin_group", "twin_kind"):
            if optional in raw:
                fixture[optional] = raw[optional]
        for index, action in enumerate(fixture["candidates"]):
            if isinstance(action, list):
                if len(action) != len(STANDARD_ACTION_FIELD_ORDER):
                    raise FixtureError(
                        f"{fixture.get('fixture_id', '<unknown>')}: compact Standard action has "
                        f"{len(action)} fields, expected {len(STANDARD_ACTION_FIELD_ORDER)}")
                fixture["candidates"][index] = dict(zip(STANDARD_ACTION_FIELD_ORDER, action))
        validate_standard_fixture(fixture)
        materialized.append(fixture)
    return _validate_collection(materialized)


def load_fixtures(path: Path | str) -> list[dict]:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise FixtureError(f"cannot load fixture document: {error}") from error
    if not isinstance(document, dict):
        raise FixtureError("fixture document must be an object")
    schema = document.get("schema_version")
    if schema == SCHEMA_VERSION:
        return _load_v1_document(document)
    if schema == STANDARD_SCHEMA_VERSION:
        return _load_standard_document(document)
    raise FixtureError("fixture document has unknown schema")
