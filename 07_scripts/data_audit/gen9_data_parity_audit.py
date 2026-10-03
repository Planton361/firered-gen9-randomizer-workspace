#!/usr/bin/env python3
"""Read-only #616 full-domain audit; JSON stdout, no component writes.

Only the four locked Showdown data files are read. Existing coherent form
selection is reused as reviewed policy, without acquiring sim source or running
TypeScript. Absence of acquisition-method evidence is never a negative oracle
for a project-local aggregate compatibility contract.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.dont_write_bytecode = True

import showdown_pinned_closure as closure
import showdown_pokemon_data_sync as sync

ROOT = sync.REPO_ROOT
PINS = {
    "Workspace": "3d464cebf3544dfd3e23127889e88acd8ca517aa",
    "product_source": "1a3e73871730783f7fe2108b335e3d86f69adbe8",
    "CFRU": "237e1dfaa785af332ddad72af906b3bba5beaab9",
    "DPE": "22ffa27ad09cfacbca841d90e6cbe31e6f9b7fdc",
    "UPR": "7bf79ee1e7c46c972f7a9c84942970a950be0723",
}
UPR = ROOT / "02_external/upr-fvx"


def require(ok, message):
    closure.require(ok, message)


def direct_fields(block):
    """Literal top-level TS properties only: never callback return values."""
    result = {}
    for name, value in re.findall(r'^\t\t(\w+):\s*("[^"\n]*"|true|false|-?\d+)(?=,|\s*$)', block, re.M):
        result[name] = json.loads(value)
    return result


def c_rows(text, prefix):
    text = closure.uncomment(text)
    return {key: body for key, body in re.findall(
        r'\[(' + prefix + r'\w+)\]\s*=\s*\{(.*?)\n[ \t]*\},?', text, re.S)}


def c_fields(body):
    fields = re.findall(r'\.(\w+)\s*=\s*([^,\n]+)', body)
    require(len({k for k, _ in fields}) == len(fields), "Duplicate active C field")
    return dict(fields)


def preprocess(text, macros=None):
    """Evaluate presence conditionals only; reject every unsupported directive.

    No compiler, macro-value expansion, or implicit choice for #if/#elif.
    Includes are retained: callers must independently establish macro ownership.
    """
    macros = set(macros or ())
    stack, output = [], []
    active = True
    for number, line in enumerate(closure.uncomment(text).splitlines(), 1):
        match = re.match(r'\s*#\s*(\w+)\b(.*)', line)
        if not match:
            if active:
                output.append(line)
            continue
        directive, arg = match.group(1), match.group(2).strip()
        if directive in ("ifdef", "ifndef"):
            require(re.fullmatch(r'[A-Za-z_]\w*', arg) is not None, f"Invalid #{directive} at {number}")
            condition = (arg in macros) == (directive == "ifdef")
            stack.append((active, condition, False))
            active = active and condition
        elif directive == "else":
            require(stack and not arg and not stack[-1][2], f"Invalid #else at {number}")
            parent, condition, _ = stack[-1]
            stack[-1] = (parent, condition, True)
            active = parent and not condition
        elif directive == "endif":
            require(stack and not arg, f"Invalid #endif at {number}")
            active = stack.pop()[0]
        elif directive in ("define", "undef"):
            name = re.match(r'([A-Za-z_]\w*)', arg)
            require(name is not None, f"Invalid #{directive} at {number}")
            if active:
                if directive == "define":
                    macros.add(name.group(1))
                else:
                    require(arg == name.group(1), f"Invalid #undef at {number}")
                    macros.discard(arg)
        elif directive in ("include", "pragma"):
            if active:
                output.append(line)
        else:
            raise ValueError(f"Unsupported preprocessor directive #{directive} at {number}")
    require(not stack, "Unclosed preprocessor conditional")
    return "\n".join(output), macros


def active_move_source():
    """Pinned config owns every table condition; verify that source invariant.

    Scanning tracked C/header sources prevents an ignored include from silently
    redefining a relevant flag. Non-config definitions/undefinitions fail closed.
    """
    config = sync.CFRU_ROOT / "src/config.h"
    table = sync.CFRU_ROOT / "src/Tables/battle_moves.c"
    source = table.read_text()
    conditions = set(re.findall(r'^\s*#\s*ifn?def\s+(\w+)', closure.uncomment(source), re.M))
    require('#include "config.h"' in (sync.CFRU_ROOT / "src/defines.h").read_text(), "Move config include missing")
    require('#include "../defines.h"' in source, "Move defines include missing")
    mutations = re.compile(r'^\s*#\s*(?:define|undef)\s+(' + '|'.join(sorted(conditions)) + r')\b', re.M)
    for name in closure.git(sync.CFRU_ROOT, "ls-files").splitlines():
        path = sync.CFRU_ROOT / name
        if path.suffix in (".c", ".h") and path != config:
            require(not mutations.search(closure.uncomment(path.read_text(encoding="latin-1"))), "Move flag owner outside config: " + name)
    _, macros = preprocess(config.read_text())
    active, _ = preprocess(source, macros)
    return active, {"condition_macros": {k: k in macros for k in sorted(conditions)},
                    "config_sha256": closure.digest(config),
                    "defines_sha256": closure.digest(sync.CFRU_ROOT / "src/defines.h"),
                    "active_source_sha256": hashlib.sha256(active.encode()).hexdigest(),
                    "method": "presence conditionals; config-only flag ownership verified across tracked C/headers; unsupported directives fail closed"}


def counts(rows):
    return dict(sorted(Counter(r["class"] for r in rows).items()))


def identity(value):
    return sync.norm(unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode())


def verify(data):
    reference = json.loads(closure.REFERENCE.read_text())
    require(closure.git(data, "rev-parse", "HEAD") == reference["revision"], "Showdown revision")
    hashes = {name: closure.digest(data / name) for name in reference["sha256"]}
    require(hashes == reference["sha256"], "Showdown file hashes")
    for name, lock in (("showdown_aliases.json", "aliases_sha256"),
                       ("showdown_learnset_ownership.json", "ownership_sha256")):
        require(closure.digest(sync.SCRIPT_DIR / name) == reference[lock], "Policy hash " + name)
    require(closure.git(ROOT, "merge-base", "HEAD", PINS["Workspace"]) == PINS["Workspace"], "Workspace ancestry")
    paths = {"CFRU": sync.CFRU_ROOT, "DPE": sync.DPE_ROOT, "UPR": UPR}
    for label, path in paths.items():
        require(closure.git(path, "rev-parse", "HEAD") == PINS[label], label + " revision")
        require(not closure.git(path, "status", "--porcelain", "--untracked-files=no"), label + " tracked changes")
        rel = path.relative_to(ROOT).as_posix()
        for workspace in (PINS["Workspace"], PINS["product_source"]):
            require(closure.git(ROOT, "rev-parse", workspace + ":" + rel) == PINS[label], "Gitlink " + label)
    # The old helper locks the whole historical config.h, which later approved
    # QoL changes legitimately altered. Lock current source revisions above and
    # require continuity of the actual normalization/runtime dependencies.
    for component, path, files in (
        ("DPE", sync.DPE_ROOT, ("src/Base_Stats.c", "src/Learnsets.c", "include/species.h", "include/moves.h", "include/abilities.h", "src/defines.h")),
        ("CFRU", sync.CFRU_ROOT, ("include/constants/species.h", "include/constants/moves.h", "include/constants/abilities.h", "include/new/learn_move.h", "src/learn_move.c")),
    ):
        for file in files:
            require(closure.git(path, "hash-object", file) == closure.git(path, "rev-parse", reference["canonical_pins"][component] + ":" + file), "Core dependency continuity: " + file)
    require(not re.search(r'^\s*#define\s+EXPAND_LEARNSETS\b', closure.uncomment((sync.DPE_ROOT / "src/defines.h").read_text()), re.M), "DPE runtime owner changed")
    require(re.search(r'^\s*#define\s+EXPAND_MOVESETS\b', closure.uncomment((sync.CFRU_ROOT / "src/config.h").read_text()), re.M), "CFRU runtime owner changed")
    return reference, hashes


def species_audit(dex, aliases, constants):
    mapped, source_rows = {}, []
    for key, entry in sorted(dex.items()):
        if not 1 <= entry["num"] <= 1025:
            continue
        plan, problem = sync.resolve_species(key, entry, constants["DPE"], constants["CFRU"], aliases)
        entries = sync.matching_entries("species", key, aliases)
        if plan:
            mapped[key] = plan
            category = "INTENTIONAL_ALIAS" if plan.dpe_key != key or plan.cfru_key != key else "MATCH"
        else:
            category = "EXCLUDED_FORM" if problem in ("species-ignore", "species-open-risk") else "CONFLICT" if problem == "species-ambiguous" else "MISSING_MAPPING"
        source_rows.append({"source": key, "class": category,
                            "local": plan.dpe_key if plan else None, "reason": problem,
                            "policy": entries})
    reverse = defaultdict(list)
    for key, plan in mapped.items():
        reverse[plan.dpe_key].append(key)
    local_rows = []
    ownership = json.loads(closure.coherent.OWNERSHIP.read_text())["groups"]
    local_aliases = sync.alias_indexes()[1]
    for local, constant in sorted(constants["DPE"].items()):
        entries = sync.matching_entries("species", local, local_aliases)
        owned = next((g for g in ownership if local in g["locals"]), None)
        if local in reverse:
            category = "MATCH" if local in reverse[local] else "INTENTIONAL_ALIAS"
        elif owned:
            category = "EXCLUDED_FORM" if "EXCLUDE" in owned.get("profile", "") else "INTENTIONAL_ALIAS"
        elif entries:
            category = "EXCLUDED_FORM" if any(e.get("status") in ("ignore", "open-risk") for e in entries) else "INTENTIONAL_ALIAS"
        else:
            category = "LOCAL_ONLY"
        local_rows.append({"local": local, "constant": constant, "class": category,
                           "sources": reverse[local], "policy": entries,
                           "learnset_only_ownership": owned})
    return mapped, {"source_counts": counts(source_rows), "local_counts": counts(local_rows),
                    "source_exceptions": [r for r in source_rows if r["class"] != "MATCH"],
                    "local_exceptions": [r for r in local_rows if r["class"] != "MATCH"]}


def move_audit(data, aliases):
    blocks = sync.parse_ts_blocks(data / "moves.ts")
    constants = sync.constants_by_kind("moves")
    active, preprocessor = active_move_source()
    local = {k: c_fields(v) for k, v in c_rows(active, "MOVE_").items()}
    targets = {"normal": "MOVE_TARGET_SELECTED", "self": "MOVE_TARGET_USER",
               "allAdjacentFoes": "MOVE_TARGET_BOTH", "allAdjacent": "MOVE_TARGET_ALL",
               "allySide": "MOVE_TARGET_USER", "foeSide": "MOVE_TARGET_OPPONENTS_FIELD"}
    # Side-target encodings are intentionally not compared: engine effects can
    # redirect USER/SELECTED. Only unambiguous battler targets below are certified.
    targets = {k: v for k, v in targets.items() if k in ("normal", "self", "allAdjacentFoes", "allAdjacent")}
    rows, mapped_local = [], set()
    names = (sync.CFRU_ROOT / "strings/attack_name_table.string").read_text()
    display = [sync.norm(x) for x in re.findall(r'#org[^\n]*\n([^#\n]+)', names)]
    for key, block in sorted(blocks.items()):
        fields = direct_fields(block)
        if fields.get("isZ") or fields.get("isMax") or re.search(r'^\t\tisZ:', block, re.M):
            rows.append({"source": key, "class": "INTENTIONAL_ENGINE_DIFFERENCE", "reason": "generated Z/Max/GMax; excluded from ordinary learnset domain"})
            continue
        if fields.get("num", 0) <= 0 or fields.get("isNonstandard") == "CAP" or key.startswith("hiddenpower") and key != "hiddenpower":
            continue
        pair, problem = sync.resolve_move(key, constants["DPE"], constants["CFRU"], aliases)
        if problem:
            rows.append({"source": key, "class": "MISSING_LOCAL_MOVE" if problem == "move-unmapped" or key == "allyswitch" else "MAPPING_BLOCK", "reason": problem})
            continue
        name = pair[1]
        mapped_local.add(name)
        row = {"source": key, "local": name, "class": "DATA_MATCH", "differences": {}, "engine_encodings": [],
               "name_present": sync.norm(str(fields.get("name", key))) in display,
               "behavior": "ENGINE_BEHAVIOR_UNVERIFIED"}
        if name not in local:
            row.update({"class": "MISSING_LOCAL_MOVE", "reason": "no battle table row"})
        else:
            expected = {"type": "TYPE_" + str(fields.get("type", "")).upper(),
                        "split": "SPLIT_" + str(fields.get("category", "")).upper()}
            for upstream, field in (("basePower", "power"), ("accuracy", "accuracy"), ("pp", "pp"), ("priority", "priority")):
                if upstream in fields:
                    expected[field] = str(0 if upstream == "accuracy" and fields[upstream] is True else fields[upstream])
            target = fields.get("target")
            if target in targets:
                expected["target"] = targets[target]
            else:
                row["target_scope"] = "UNVERIFIABLE_EXACT_ENCODING:" + str(target)
            for field, value in expected.items():
                actual = local[name].get(field, "0" if field == "priority" else "MISSING").strip()
                if field == "target" and actual == "MOVE_TARGET_FOES_AND_ALLY":
                    actual = "MOVE_TARGET_ALL"  # battle.h: both exactly 0x20
                if field == "priority" and actual.isdigit():
                    number = int(actual)
                    actual = str(number - 256 if 128 <= number <= 255 else number)
                if actual != value:
                    # Dynamic damage uses CFRU's positive power sentinel. This
                    # says nothing about whether the handler computes it correctly.
                    if field == "power" and value == "0" and name in {"MOVE_FISSURE", "MOVE_HORNDRILL", "MOVE_GUILLOTINE", "MOVE_SHEERCOLD", "MOVE_FLING", "MOVE_MAGNITUDE", "MOVE_NATURALGIFT", "MOVE_PAINSPLIT", "MOVE_PRESENT", "MOVE_PUNISHMENT"}:
                        row["engine_encodings"].append("handler-computed damage/power: Showdown 0 / CFRU " + actual)
                    elif field == "power" and value == "0" and actual == "1" and ("basePowerCallback" in block or "damage:" in block or "damageCallback" in block):
                        row["engine_encodings"].append("dynamic-power: Showdown 0 / CFRU 1")
                    elif field == "type" and key == "struggle":
                        row["engine_encodings"].append("Struggle typeless engine encoding; damage_calc explicitly handles MOVE_STRUGGLE")
                    elif field == "target" and actual == "MOVE_TARGET_DEPENDS":
                        row["engine_encodings"].append("target handler requires review: " + actual + " / " + value)
                    else:
                        row["differences"][field] = {"local": actual, "reference": value}
            if row["differences"]:
                row["class"] = "DATA_MISMATCH"
            elif row["engine_encodings"]:
                row["class"] = "ENGINE_BEHAVIOR_UNVERIFIED" if any(s.startswith("target") for s in row["engine_encodings"]) else "INTENTIONAL_ENGINE_DIFFERENCE"
        rows.append(row)
    extra = sorted(set(local) - mapped_local - {"MOVE_NONE"})
    return {"counts": counts(rows), "rows": rows, "local_uncompared": extra,
            "normal_mapping_count": len(mapped_local), "behavior_certified": 0, "preprocessor": preprocessor}


def ability_audit(data, dex, aliases, mapped):
    relevant = sorted({a for key, e in dex.items() if key in mapped for a in e.get("abilities", {}).values()})
    fields = {k: direct_fields(v) for k, v in sync.parse_ts_blocks(data / "abilities.ts").items()}
    constants = sync.constants_by_kind("abilities")
    defines = dict(re.findall(r'^#define\s+(ABILITY_\w+)\s+(\S+)', (sync.DPE_ROOT / "include/abilities.h").read_text(), re.M))
    strings = (sync.CFRU_ROOT / "strings/ability_name_table.string").read_text()
    util = (sync.CFRU_ROOT / "src/ability_util.c").read_text()
    runtime = "\n".join(p.read_text() for p in sorted((sync.CFRU_ROOT / "src").glob("*.c")))
    rows = []
    for key in relevant:
        entries = sync.matching_entries("abilities", key, aliases)
        constant = constants["DPE"].get(key)
        if constant is None:
            candidates = [constants["DPE"][sync.norm(k)] for e in entries for k in e.get("local_keys", []) if sync.norm(k) in constants["DPE"]]
            constant = candidates[0] if len(set(candidates)) == 1 else None
        category = "UNKNOWN"
        target = defines.get(constant, "")
        hook = next((name for name in re.findall(r'bool8\s+(SpeciesHas\w+)\(', util) if sync.norm(name.removeprefix("SpeciesHas")) == key), None)
        if key == "zerotohero":
            category = "NAME_ONLY_OR_BEHAVIOR_BLOCKED"
        elif not constant and key == "chillingneigh":
            constant, target = "ABILITY_MOXIE", "ABILITY_MOXIE (species name override)"
            category = "ALIAS_PLUS_HOOK"
        elif not constant and key == "lingeringaroma":
            constant, target = "ABILITY_UNUSED", "0x4D; CFRU ABILITY_LINGERINGAROMA"
            category = "NAME_ONLY_OR_BEHAVIOR_BLOCKED"
        elif not constant and key in ("terashift", "terashell"):
            category = "NAME_ONLY_OR_BEHAVIOR_BLOCKED"
        elif not constant:
            category = "MISSING_LOCAL"
        elif any(e.get("category") == "name-mismatch" for e in entries):
            category = "NAME_ONLY_OR_BEHAVIOR_BLOCKED"
        elif target.startswith("ABILITY_"):
            category = "ALIAS_PLUS_HOOK" if hook and runtime.count(hook + "(") > 1 else "ALIAS_APPROXIMATION"
        elif any(sync.blocked_entry(e) for e in entries):
            category = "NAME_ONLY_OR_BEHAVIOR_BLOCKED"
        # Textual constant occurrence is not behavior-owner evidence.
        # Unreviewed native identities retain UNKNOWN, including full semantics.
        rows.append({"source": key, "class": category, "local": constant, "definition": target or None,
                     "hook": hook, "reference_name": fields.get(key, {}).get("name"),
                     "name_string_present": sync.norm(str(fields.get(key, {}).get("name", key))) in sync.norm(strings),
                     "policy": entries, "assignment_identity": "accepted base-slot comparison or explicit blocked slot; see base domain",
                     "numeric_alias": target if target.startswith("ABILITY_") else None,
                     "species_helper_referenced": bool(hook and runtime.count(hook + "(") > 1),
                     "behavior_owner_evidence": None, "full_effect_semantics": "UNCERTIFIED"})
    gen9 = (sync.DPE_ROOT / "include/abilities.h").read_text().split("//Gen 9 Abilities Leeches", 1)[1]
    return {"counts": counts(rows), "rows": rows,
            "gen9_aliases": dict(re.findall(r'#define\s+(ABILITY_\w+)\s+(ABILITY_\w+)', gen9)),
            "semantics": "No native behavior is certified by textual occurrence. UNKNOWN denotes unreviewed behavior ownership. ALIAS_PLUS_HOOK records numeric alias plus species-helper reference/display override, not proof of battle behavior. Assignment/name identity are separate; full effect semantics remain uncertified."}


def evolution_rows(text):
    text = closure.uncomment(text)
    result = {}
    for key, body in re.findall(r'\[(SPECIES_\w+)\]\s*=?\s*\{(.*?)(?=\n\s*\[SPECIES_|\n};)', text, re.S):
        result[key] = [tuple(x.strip() for x in re.split(r',\s*(?![^()]*\))', row)) for row in re.findall(r'\{([^{}]+)\}', body)]
    return result


def evolution_audit(data, mapped):
    local = evolution_rows((sync.DPE_ROOT / "src/Evolution Table.c").read_text())
    blocks = sync.parse_ts_blocks(data / "pokedex.ts")
    rows = []
    for key, plan in sorted(mapped.items()):
        f = direct_fields(blocks[key])
        if "prevo" not in f:
            continue
        parent = mapped.get(sync.norm(f["prevo"]))
        if not parent:
            rows.append({"source": key, "class": "MAPPING_BLOCK", "parent": f["prevo"]})
            continue
        candidates = [r for r in local.get(parent.dpe_constant, []) if len(r) >= 3 and r[2] == plan.dpe_constant]
        row = {"source": key, "parent": f["prevo"], "local": candidates, "reference": {k: v for k, v in f.items() if k.startswith("evo")}, "class": "UNVERIFIABLE_FROM_SELECTED_REFERENCE"}
        evo_type = f.get("evoType")
        if not candidates:
            row["class"] = "DATA_MISMATCH"
            row["reason"] = "missing mapped evolution target"
        elif evo_type is None and "evoLevel" in f:
            level_methods = {"EVO_LEVEL", "EVO_LEVEL_ATK_GT_DEF", "EVO_LEVEL_ATK_EQ_DEF", "EVO_LEVEL_ATK_LT_DEF", "EVO_MALE_LEVEL", "EVO_FEMALE_LEVEL", "EVO_LEVEL_CASCOON", "EVO_LEVEL_SILCOON", "EVO_LEVEL_NINJASK", "EVO_LEVEL_SHEDINJA", "EVO_NATURE_HIGH", "EVO_NATURE_LOW", "EVO_MAUSHOLD_THREE", "EVO_MAUSHOLD_FOUR", "EVO_LEVEL_HOLD_ITEM", "EVO_LEVEL_NIGHT", "EVO_LEVEL_DAY", "EVO_RAINY_FOGGY_OW", "EVO_TYPE_IN_PARTY"}
            matching = [r for r in candidates if r[0] in level_methods and r[1] == str(f["evoLevel"])]
            if any(r[0] == "EVO_LEVEL" for r in matching) and not f.get("evoCondition"):
                row["class"] = "REFERENCE_MATCH"
            elif matching:
                row["class"] = "ENGINE_TRIGGER_REVIEW"
            else:
                row["class"] = "DATA_MISMATCH"
                row["reason"] = "level/method differs"
        elif evo_type == "useItem":
            item = "ITEM_" + re.sub(r'[^A-Z0-9]+', '_', f.get("evoItem", f.get("evoCondition", "")).upper())
            row["class"] = "REFERENCE_MATCH" if any(r[0].startswith("EVO_ITEM") and r[1] == item for r in candidates) else "DATA_MISMATCH"
            if row["class"] == "DATA_MISMATCH":
                row["reason"] = "item/method differs"
        elif evo_type == "levelMove":
            move = sync.norm(f.get("evoMove", ""))
            row["class"] = "REFERENCE_MATCH" if any(r[0] == "EVO_MOVE" and sync.norm(r[1].removeprefix("MOVE_")) == move for r in candidates) else "DATA_MISMATCH"
            if row["class"] == "DATA_MISMATCH":
                row["reason"] = "move trigger differs"
        elif evo_type == "trade":
            item = "ITEM_" + re.sub(r'[^A-Z0-9]+', '_', f.get("evoItem", "").upper()).replace("KING_S", "KINGS")
            row["class"] = "REFERENCE_MATCH" if any(r[0] == "EVO_TRADE" and not f.get("evoItem") or r[0] == "EVO_TRADE_ITEM" and r[1] == item for r in candidates) else "PROJECT_POLICY"
        elif evo_type == "levelFriendship":
            method = "EVO_FRIENDSHIP_NIGHT" if "night" in f.get("evoCondition", "") else "EVO_FRIENDSHIP_DAY" if "day" in f.get("evoCondition", "") else "EVO_FRIENDSHIP"
            row["class"] = "REFERENCE_MATCH" if any(r[0] == method for r in candidates) else "ENGINE_TRIGGER_REVIEW"
        elif "evoCondition" in f or evo_type:
            row["class"] = "ENGINE_TRIGGER_REVIEW"
        rows.append(row)
    transitions = {k: [r for r in v if r[0] in ("EVO_MEGA", "EVO_GIGANTAMAX", "EVO_PRIMAL")] for k, v in local.items()}
    # Missing relationships must consider reviewed local regional/custom parent
    # markers and alternate form parents, without inventing an evolution alias.
    for row in rows:
        if row.get("reason") == "missing mapped evolution target":
            target = mapped[row["source"]].dpe_constant
            alternate = {k: [r for r in v if len(r) >= 3 and r[2] == target] for k, v in local.items()}
            alternate = {k: v for k, v in alternate.items() if v}
            if alternate:
                row["class"] = "PROJECT_POLICY"
                row["reason"] = "relationship represented through alternate local parent"
                row["alternate_parents"] = alternate
            elif row["source"] == "vivillonfancy":
                row["class"] = "UNVERIFIABLE_FROM_SELECTED_REFERENCE"
                row["reason"] = "form/event vs ordinary evolution ownership; no reviewed evolution-form policy"
    methods = set(re.findall(r'case\s+(EVO_\w+)\s*:', (sync.CFRU_ROOT / "src/evolution.c").read_text()))
    for row in rows:
        if row["class"] == "ENGINE_TRIGGER_REVIEW":
            ref = row["reference"]
            condition = ref.get("evoCondition", "")
            candidate_methods = {r[0] for r in row["local"]}
            condition_map = {
                "at night": "EVO_LEVEL_NIGHT", "during the day": "EVO_LEVEL_DAY",
                "with an Atk stat < its Def stat": "EVO_LEVEL_ATK_LT_DEF",
                "with an Atk stat > its Def stat": "EVO_LEVEL_ATK_GT_DEF",
                "with an Atk stat equal to its Def stat": "EVO_LEVEL_ATK_EQ_DEF",
            }
            if condition_map.get(condition) in candidate_methods:
                row["class"] = "REFERENCE_MATCH"
            elif ref.get("evoType") == "levelHold":
                item = "ITEM_" + re.sub(r'[^A-Z0-9]+', '_', ref.get("evoItem", "").upper())
                method = "EVO_HOLD_ITEM_NIGHT" if "night" in condition else "EVO_HOLD_ITEM_DAY" if "day" in condition else None
                if any(r[0] == method and r[1] == item for r in row["local"]):
                    row["class"] = "REFERENCE_MATCH"
            elif ref.get("evoType") == "levelExtra" and condition == "with a Remoraid in party" and any(r[0] == "EVO_OTHER_PARTY_MON" and r[1] == "SPECIES_REMORAID" for r in row["local"]):
                row["class"] = "REFERENCE_MATCH"
            elif condition == "with a Dark-type in the party" and any(r[0] == "EVO_TYPE_IN_PARTY" and r[3] == "TYPE_DARK" for r in row["local"]):
                row["class"] = "REFERENCE_MATCH"
    unsupported = {k: [r for r in v if r[0] not in methods and r[0] not in ("EVO_MEGA", "EVO_GIGANTAMAX")] for k, v in local.items()}
    gnu_style = re.findall(r'\[(SPECIES_\w+)\]\s+\{', closure.uncomment((sync.DPE_ROOT / "src/Evolution Table.c").read_text()))
    return {"counts": counts(rows), "rows": rows, "gnu_obsolete_designators": gnu_style, "designator_disposition": "Obsolete GNU initializer syntax; accepted target source flow, no functional defect established",
            "methods_without_cfru_case": {k: v for k, v in unsupported.items() if v},
            "battle_transitions": {k: v for k, v in transitions.items() if v},
            "other_local_edges": {k: v for k, v in local.items() if any(r[0] not in ("EVO_MEGA", "EVO_GIGANTAMAX", "EVO_PRIMAL") for r in v)}}


def egg_audit(learnsets, mapped, aliases):
    text = closure.uncomment((sync.DPE_ROOT / "src/Egg_Moves.c").read_text())
    require(re.search(r'EGG_MOVES_TERMINATOR\s*,?\s*};', text), "Egg terminator")
    local = {sync.norm(k): set(re.findall(r'MOVE_\w+', body)) for k, body in re.findall(r'egg_moves\(\s*(\w+)\s*,(.*?)\)', text, re.S)}
    constants = sync.constants_by_kind("moves")
    rows = []
    for key, plan in sorted(mapped.items()):
        evidence = learnsets.get(key)
        # Literal E evidence only. Evolved/form inheritance and absent E source
        # cannot establish a intended project egg set.
        eggs = {m for m, sources in (evidence or {}).items() if any(re.fullmatch(r'[1-9]E.*', s) for s in sources)}
        if not eggs and plan.dpe_key not in local:
            continue
        target, blocks = set(), []
        for move in sorted(eggs):
            pair, problem = sync.resolve_move(move, constants["DPE"], constants["CFRU"], aliases)
            if problem:
                blocks.append(move + ":" + problem)
            else:
                target.add(pair[0])
        actual = local.get(plan.dpe_key, set())
        category = "MAPPING_BLOCK" if blocks else "EXACT_LITERAL_E_UNION" if target == actual and eggs else "UNVERIFIABLE_FROM_SELECTED_REFERENCE"
        rows.append({"source": key, "local": plan.dpe_key, "class": category,
                     "missing_literal": sorted(target - actual), "extra_local": sorted(actual - target),
                     "reference_generations": sorted({int(s[0]) for m in eggs for s in evidence[m] if re.fullmatch(r'[1-9]E.*', s)}),
                     "blocks": blocks, "local_entry_present": plan.dpe_key in local})
    return {"counts": counts(rows), "local_species_entries": len(local), "rows": rows,
            "local_unmapped": sorted(set(local) - {p.dpe_key for p in mapped.values()}),
            "interpretation": "E union is observable evidence, not an approved egg-generation/inheritance policy; differing sets are not certified errors"}


def move_order(text, name, count):
    match = re.search(r'\b' + name + r'\[[^]]+\]\s*=\s*\{(.*?)\};', closure.uncomment(text), re.S)
    require(match is not None, "Missing order " + name)
    explicit = re.findall(r'MOVE_\w+', match[1])
    require(len(explicit) <= count, "Array overflow " + name)
    return explicit + ["MOVE_NONE"] * (count - len(explicit)), len(explicit)


def compatibility_files(directory, count, order, species_values):
    pairs, issues, files = set(), [], defaultdict(list)
    for path in sorted(directory.glob("*.txt")):
        index = int(path.name.split(" - ")[0]) - 1
        require(0 <= index < count, "Compatibility slot outside declared range")
        files[index].append(path.name)
        lines = path.read_text().splitlines()
        label = identity(lines[0].split(":", 1)[-1])
        if label != identity(order[index].removeprefix("MOVE_")):
            issues.append({"slot": index + 1, "file": path.name, "move": order[index], "class": "DATA_MISMATCH", "reason": "header/order identity differs"})
        for raw in lines[1:]:
            token = raw.strip()
            if not token:
                continue
            name = token if token.startswith("SPECIES_") else "SPECIES_" + token
            if name in species_values:
                number = species_values[name]
            else:
                try:
                    number = int(token, 0)
                except ValueError:
                    issues.append({"slot": index + 1, "token": token, "class": "MAPPING_BLOCK"})
                    continue
            require(0 <= number < 1440, "Species outside bitset rows")
            pairs.add((number, index))
    for index in range(count):
        if len(files[index]) != 1:
            issues.append({"slot": index + 1, "files": files[index], "class": "DATA_MISMATCH", "reason": "missing/duplicate compatibility file"})
    return pairs, issues, {str(i + 1): names for i, names in sorted(files.items())}


def acquisition_evidence(key, learnsets, metadata, method, seen=()):
    """Literal M/T evidence plus explicit form and pre-evolution inheritance.

    Historical union is used only to explain local aggregate positives, never
    to select level-up moves or to infer a missing-method negative.
    """
    if key in seen:
        raise ValueError("Acquisition inheritance cycle")
    evidence = defaultdict(set)
    for move, sources in learnsets.get(key, {}).items():
        evidence[move].update(s for s in sources if re.fullmatch(r'[1-9]' + method + r'.*', s))
    f = metadata.get(key, {})
    parent = f.get("prevo")
    if not parent and key not in learnsets:
        parent = f.get("changesFrom") or f.get("battleOnly") or f.get("baseSpecies")
    if isinstance(parent, str) and sync.norm(parent) != key:
        for move, sources in acquisition_evidence(sync.norm(parent), learnsets, metadata, method, (*seen, key)).items():
            evidence[move].update(sources)
    return evidence


def compatibility_audit(data, learnsets, mapped, aliases, tutor=False):
    count = 152 if tutor else 128
    name = "gMoveTutorMoves" if tutor else "gTMHMMoves"
    order, explicit = move_order((sync.DPE_ROOT / "src/TM_Tutor_Tables.c").read_text(), name, count)
    species_values = closure.constant_values("species", "DPE")
    pairs, issues, files = compatibility_files(sync.DPE_ROOT / ("src/tutor_compatibility" if tutor else "src/tm_compatibility"), count, order, species_values)
    constants = sync.constants_by_kind("moves")
    reverse = defaultdict(set)
    for key in sync.parse_ts_blocks(data / "moves.ts"):
        pair, problem = sync.resolve_move(key, constants["DPE"], constants["CFRU"], aliases)
        if not problem:
            reverse[pair[0]].add(key)
    metadata = {}
    for key, block in sync.parse_ts_blocks(data / "pokedex.ts").items():
        metadata[key] = direct_fields(block)
    summary = Counter()
    selected_generation_matches = 0
    historical_method_matches = 0
    forms = closure.coherent.metadata(data / "pokedex.ts")
    exceptions = defaultdict(lambda: defaultdict(list))
    ref_positive, local_positive = 0, 0
    for key, plan in sorted(mapped.items()):
        try:
            selected_generation = closure.coherent.select(key, learnsets, forms)["generation"]
        except ValueError:
            selected_generation = None
        evidence = acquisition_evidence(key, learnsets, metadata, "T" if tutor else "M")
        other = acquisition_evidence(key, learnsets, metadata, "M" if tutor else "T")
        for index, move in enumerate(order):
            actual = (species_values[plan.dpe_constant], index) in pairs
            local_positive += actual
            keys = reverse[move]
            sources = {s for k in keys for s in evidence.get(k, ())}
            selected_sources = {s for s in sources if int(s[0]) == selected_generation}
            cross = {s for k in keys for s in other.get(k, ())}
            ref_positive += bool(sources)
            if len(keys) != 1:
                category = "MAPPING_BLOCK"
            elif sources and actual and (tutor or selected_sources):
                category = "REFERENCE_MATCH"
                selected_generation_matches += bool(selected_sources)
                historical_method_matches += not bool(selected_sources)
            elif sources and actual:
                category = "PROJECT_POLICY"
                historical_method_matches += 1
            elif not actual and not sources:
                category = "UNVERIFIABLE_FROM_SELECTED_REFERENCE"
            elif actual and cross:
                category = "PROJECT_POLICY"
            else:
                category = "UNVERIFIABLE_FROM_SELECTED_REFERENCE"
            summary[category] += 1
            if category != "REFERENCE_MATCH" and (actual or sources or category == "MAPPING_BLOCK"):
                detail = category + (":LOCAL_POSITIVE" if actual else ":REFERENCE_POSITIVE_LOCAL_NEGATIVE")
                exceptions[str(index + 1)][detail].append(key)
    # Pure in-memory bitset reconstruction, matching builder's little-endian
    # bit order; no assembly/generated artifact is opened or written.
    encoded = bytearray(1440 * (count // 8))
    for number, index in pairs:
        encoded[number * (count // 8) + index // 8] |= 1 << (index % 8)
    require(all(bool(encoded[n * (count // 8) + i // 8] & (1 << (i % 8))) == ((n, i) in pairs)
                for n in range(1440) for i in range(count)), "Bitset replay")
    return {"declared_count": count, "explicit_moves": explicit, "bytes_per_species": count // 8,
            "order": order, "order_sha256": hashlib.sha256(("\n".join(order) + "\n").encode()).hexdigest(),
            "source_bitset_sha256": hashlib.sha256(encoded).hexdigest(), "bitset_replay": "PASS",
            "counts": dict(sorted(summary.items())), "pairs": len(mapped) * count,
            "local_positive_pairs": local_positive, "reference_positive_pairs": ref_positive,
            "selected_generation_positive_matches": selected_generation_matches,
            "historical_same_method_positive_matches": historical_method_matches,
            "layout_issues": issues, "files": files, "exceptions": dict(exceptions),
            "policy": "REFERENCE_MATCH certifies positive same-method evidence only; PROJECT_POLICY is cross-method observable support, not authorization for every individual bit; negatives/differences require a selected aggregate policy"}


def upr_audit():
    """Numeric move-pool counterexamples, from public Java/C source only."""
    constants = UPR / "romio/src/main/java/com/uprfvx/romio/constants"
    java_ids = {k: int(v) for k, v in re.findall(r'public static final int (\w+) = (\d+);', (constants / "MoveIDs.java").read_text())}
    global_text = (constants / "GlobalConstants.java").read_text()
    banned = {java_ids[key] for key in re.findall(r'bannedRandomMoves\[MoveIDs\.(\w+)\]\s*=\s*true', global_text)}
    for name in ("fixedPowerZMoves", "varyingPowerZMoves"):
        body = re.search(name + r'\s*=\s*Arrays.asList\((.*?)\);', global_text, re.S)[1]
        banned.update(java_ids[key] for key in re.findall(r'MoveIDs\.(\w+)', body))
    local = closure.constant_values("moves", "CFRU")
    generated = {name: number for name, number in local.items() if name.startswith(("MOVE_MAX_", "MOVE_G_MAX_")) or local["MOVE_BREAKNECK_BLITZ_P"] <= number <= local["MOVE_SOUL_STEALING_7_STAR_STRIKE"]}
    # getIllegalMoves/getMovesBannedFromLevelup are inherited empty; the source
    # moveset pool removes HMs plus global standard-generation Z IDs. Local
    # generated constants outside those IDs remain candidates if loaded.
    candidates = {name: number for name, number in generated.items() if number not in banned}
    handler = (UPR / "romio/src/main/java/com/uprfvx/romio/romhandlers/Gen3RomHandler.java").read_text()
    require(not re.search(r'public List<Integer> get(?:IllegalMoves|MovesBannedFromLevelup)\(', handler), "UPR overrides changed; re-audit move pool")
    header = closure.uncomment((sync.DPE_ROOT / "include/evolution.h").read_text())
    enum = re.search(r'enum EvolutionMethods\s*\{(.*?)\};', header, re.S)[1]
    method_ids = {name: i for i, name in enumerate(re.findall(r'\bEVO_\w+', enum))}
    method_ids.update({"EVO_MEGA": 254, "EVO_GIGANTAMAX": 253})
    rows = evolution_rows((sync.DPE_ROOT / "src/Evolution Table.c").read_text())
    ignored, auxiliary = {}, {}
    for parent, entries in sorted(rows.items()):
        missing = [r for r in entries if method_ids[r[0]] > 15]
        lost = [r for r in entries if method_ids[r[0]] <= 15 and len(r) > 3 and r[3] not in ("0", "MON_MALE", "FALSE")]
        if missing:
            ignored[parent] = missing
        if lost:
            auxiliary[parent] = lost
    require("evolutionMethodCount = 15" in (constants / "Gen3Constants.java").read_text(), "UPR evolution method domain changed")
    return {"generated_local_constants": len(generated), "generated_not_removed_by_standard_id_filters": candidates,
            "evolution_methods": method_ids,
            "evolution_rows_ignored_by_loader": ignored,
            "evolution_auxiliary_fields_zeroed": auxiliary,
            "ignored_evolution_row_count": sum(map(len, ignored.values())),
            "lost_auxiliary_row_count": sum(map(len, auxiliary.values())),
            "scope": "source-level candidate exposure, conditional on loaded moves and chosen settings; no Randomizer execution or output claim",
            "mechanics_exclusion_registry": "not found in Gen3 handler; asset guard does not check coherent-reference/ability-mechanics exclusions"}


def mismatch_ledger(result):
    """Complete genuine ledger, keyed by domain/identity; style is not a defect."""
    rows = []
    for domain in ("moves", "evolutions"):
        rows += [{"domain": domain, "identity": r["source"], "evidence": r}
                 for r in result[domain]["rows"] if r["class"] == "DATA_MISMATCH"]
    for domain in ("machines", "tutors"):
        rows += [{"domain": domain, "identity": f"slot-{r['slot']}", "evidence": r}
                 for r in result[domain]["layout_issues"] if r["class"] == "DATA_MISMATCH"]
    require(not result["base"]["genuine_mismatches"], "Unexpected core mismatch requires ledger extension")
    require(len({(r["domain"], r["identity"]) for r in rows}) == len(rows), "Duplicate genuine mismatch ledger identity")
    return rows


def run(data):
    reference, hashes = verify(data)
    aliases, _ = sync.alias_indexes()
    dex = sync.parse_pokedex(data / "pokedex.ts")
    learnsets = sync.parse_learnsets(data / "learnsets.ts")
    mapped, species = species_audit(dex, aliases, sync.constants_by_kind("species"))
    inventory, _ = closure.build_inventory(data, reference)
    require(inventory["summary"]["counts"]["SAFE_DATA_DIFF"] == 0, "Core-data closure regression")
    base_rows = [r for r in inventory["inventories"]["NO_DIFF"] if r["kind"] == "base"]
    blocked = inventory["inventories"]["ABILITY_BEHAVIOR_BLOCK"]
    ability_defines = dict(re.findall(r'^#define\s+(ABILITY_\w+)\s+(\S+)', (sync.DPE_ROOT / "include/abilities.h").read_text(), re.M))
    ability_constants = sync.constants_by_kind("abilities")["DPE"]
    aliased_slots = []
    for key, plan in sorted(mapped.items()):
        for slot, ability in dex[key].get("abilities", {}).items():
            constant, problem = sync.resolve_ability(ability, ability_constants, aliases)
            if constant and ability_defines.get(constant, "").startswith("ABILITY_"):
                aliased_slots.append({"source": key, "slot": slot, "ability": ability, "local": constant, "older_effect": ability_defines[constant]})
    consumers = inventory["consumer_provenance"]
    result = {"pins": PINS, "reference_revision": reference["revision"], "reference_hashes": hashes,
              "policy_hashes": {name: closure.digest(sync.SCRIPT_DIR / name) for name in ("showdown_pilot_reference.json", "showdown_aliases.json", "showdown_learnset_ownership.json")},
              "species": species,
              "base": {"comparable_local_rows": len(base_rows), "matches": len(base_rows), "comparable_field_count": len(base_rows) * 14 - len(blocked), "genuine_mismatches": [], "blocked_ability_slots": blocked, "accepted_alias_slots": aliased_slots},
              "learnsets": {"summary": inventory["summary"], "consumer_counts": dict(sorted(Counter(c["disposition"] for c in consumers).items())),
                            "generations": dict(sorted(Counter(str(c["selected_source_generations"]) for c in consumers).items())),
                            "exceptions": {k: v for k, v in inventory["inventories"].items() if k != "NO_DIFF"},
                            "excluded_consumers": [c for c in consumers if c["disposition"] != "NO_DIFF" or any("EXCLUDE" in r["profile"] for r in c["records"])]},
              "moves": move_audit(data, aliases), "abilities": ability_audit(data, dex, aliases, mapped),
              "evolutions": evolution_audit(data, mapped), "eggs": egg_audit(learnsets, mapped, aliases),
              "machines": compatibility_audit(data, learnsets, mapped, aliases),
              "tutors": compatibility_audit(data, learnsets, mapped, aliases, True), "upr": upr_audit()}
    result["genuine_mismatch_ledger"] = mismatch_ledger(result)
    result["genuine_mismatch_counts"] = dict(sorted(Counter(r["domain"] for r in result["genuine_mismatch_ledger"]).items()))
    # Primary normalization-owner hashes; other inspected source is bound by component pins.
    paths = [sync.CFRU_ROOT / "src/config.h", sync.CFRU_ROOT / "src/defines.h", sync.CFRU_ROOT / "src/Tables/battle_moves.c", sync.CFRU_ROOT / "strings/attack_name_table.string",
             sync.CFRU_ROOT / "strings/ability_name_table.string", sync.DPE_BASE_STATS, sync.CFRU_LEARNSETS,
             sync.DPE_ROOT / "include/abilities.h", sync.DPE_ROOT / "src/Evolution Table.c",
             sync.DPE_ROOT / "include/evolution.h", sync.DPE_ROOT / "src/Egg_Moves.c",
             sync.DPE_ROOT / "src/TM_Tutor_Tables.c"]
    paths += sorted((sync.CFRU_ROOT / "src").glob("*.c"))
    for kind in ("tm_compatibility", "tutor_compatibility"):
        paths += sorted((sync.DPE_ROOT / "src" / kind).glob("*.txt"))
    result["input_hashes"] = {p.relative_to(ROOT).as_posix(): closure.digest(p) for p in sorted(set(paths))}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--showdown-data-dir", type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(run(args.showdown_data_dir), indent=2, sort_keys=True))
    except (ValueError, KeyError, OSError) as error:
        parser.exit(2, "FAIL CLOSED: " + str(error) + "\n")


if __name__ == "__main__":
    main()
