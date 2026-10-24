#!/usr/bin/env python3
"""ROM-free D1 receipt checks. Never authorizes insertion; see the contract.

Only USER may supply private receipts. No subprocess, inserter, artifact, ROM,
map or tool is opened. A consistent receipt is not an independent observation.
"""
import json
import re
import sys

SOURCES = {
    "cfru": "196058edbc2b8b7d8c725b715b1f967ba60f5c83",
    "dpe": "d887185de1f6ae6a78e85c4311bbadde17041d00",
    "upr": "e1127cfde58af359e458f8d6a19339f3db3c8589",
}
CFRU_START = 0x1000000
DPE_START = 0x1600000
ROM_LIMIT = 0x2000000
# Exact main() order at the selected public revisions. Cached and scanning
# repoints are distinct: CFRU scans SOURCE_ROM, DPE scans the current output.
PHASES = {
    "dpe": ("copy", "expand", "payload", "bytepatch", "special", "hooks",
            "repoints", "generated_repoints", "repoint_all", "routine_pointers",
            "function_rewrites", "offsets"),
    "cfru": ("copy", "payload", "generated_repoints", "repoint_all", "special",
             "free_bytepatch", "bytepatch", "hooks", "repoints",
             "routine_pointers", "function_rewrites", "events", "overlays",
             "songs", "offsets"),
}
NO_ROM_WRITES = {"copy", "offsets"}
POINTER_PHASES = {"hooks", "repoints", "generated_repoints", "repoint_all",
                  "routine_pointers", "function_rewrites", "songs"}
# All are physical leaf reservations, not magic-marker or free-byte guesses.
REQUIRED_ROLES = {
    "oak_record": 96, "oak_bitmap": 180,
    "oak_front_bridge": 28, "oak_cry_bridge": 28,
    "oak_front_consumer": None, "oak_cry_consumer": None,
    "pickup_record": 64, "pickup_bridge": 28, "pickup_consumer": None,
    "evolution_record": 32, "evolution_consumer": None,
    "native_front_table": None, "native_palette_table": None,
    "native_front_assets": None, "native_palette_assets": None,
    "palette_source": None, "palette_snapshot": None, "palette_repoints": None,
    "learnset_writer": None, "learnset_allocator": None, "learnset_rollback": None,
    "evolution_rows": 1440 * 16 * 8,
}
GATES = ("D1_RECEIPT_SCHEMA", "D1_RECEIPT_PROVENANCE", "D1_WRITE_ORDER",
         "D1_CAPACITY", "D1_DECLARED_OWNERS", "D1_WRITE_SETS",
         "D1_ORIGINAL_OBSERVATION", "D1_SOURCE_CONFIG_IDENTITY",
         "D1_FRESH_BUILD", "D1_NATIVE_BUILD_LINK_INSERT", "D1_OAK_ABI",
         "D1_OUTPUT_PROVENANCE", "D1_DPE_REPRODUCIBILITY", "D1_ALL")
MAX_RECEIPT = 16 * 1024 * 1024
MAX_RECORDS = 10000


class Missing(Exception):
    """Evidence is unavailable, not a successful check."""


class Invalid(Exception):
    """Supplied evidence contradicts the receipt contract."""


def require(condition):
    if not condition:
        raise Invalid()


def fields(obj, names):
    require(type(obj) is dict)
    if not set(names) <= obj.keys():
        raise Missing()
    require(set(obj) == set(names))
    return obj


def records(value):
    require(type(value) is list and len(value) <= MAX_RECORDS)
    return value


def integer(value, minimum=0, maximum=ROM_LIMIT):
    require(type(value) is int and minimum <= value <= maximum)
    return value


def token(value):
    require(type(value) is str and re.fullmatch(r"[A-Za-z0-9_-]{1,80}", value))
    return value


def digest(value):
    require(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value))
    return value


def span(obj):
    start, end = integer(obj["start"]), integer(obj["end"])
    require(start < end)
    return start, end


def overlaps(a, b):
    return a["start"] < b["end"] and b["start"] < a["end"]


def contains(a, b):
    return a["start"] <= b["start"] < b["end"] <= a["end"]


def indexed(rows):
    result = {}
    for row in records(rows):
        name = token(row["id"])
        require(name not in result)
        result[name] = row
    return result


def schema(doc):
    fields(doc, ("schema", "sources", "config", "builds", "stages",
                 "allocations", "owners", "overrides"))
    require(type(doc["schema"]) is int and doc["schema"] == 1)
    fields(doc["sources"], SOURCES)
    require(doc["sources"] == SOURCES)
    digest(doc["config"])
    for key in ("builds", "stages", "allocations", "owners", "overrides"):
        records(doc[key])


def provenance(doc):
    builds = indexed(doc["builds"])
    if len(builds) < 2:
        raise Missing()
    require(len(builds) == 2)
    by_component = {}
    for b in builds.values():
        fields(b, ("id", "component", "source", "config", "fresh", "artifacts"))
        c = b["component"]
        require(c in PHASES and c not in by_component)
        require(b["source"] == SOURCES[c] and b["config"] == doc["config"])
        require(type(b["fresh"]) is bool)
        require(b["fresh"])
        artifacts = indexed(b["artifacts"])
        kinds = set()
        for a in artifacts.values():
            fields(a, ("id", "kind", "build", "sha256", "cached"))
            token(a["kind"])
            require(a["build"] == b["id"])
            digest(a["sha256"])
            require(type(a["cached"]) is bool and not a["cached"])
            require(a["kind"] not in kinds)
            kinds.add(a["kind"])
        # Generated repoint caches, generated assembly and objects must be
        # accounted for even when the original inserter silently reuses them.
        if not {"linked", "payload", "generated", "objects", "repoint_cache"} <= kinds:
            raise Missing()
        by_component[c] = b
    stages = records(doc["stages"])
    if len(stages) < 2:
        raise Missing()
    require(len(stages) == 2)
    previous = None
    for stage, c in zip(stages, ("dpe", "cfru")):
        fields(stage, ("component", "build", "input", "output", "input_size",
                       "output_size", "completed", "phases", "writes"))
        require(stage["component"] == c and stage["build"] == by_component[c]["id"])
        digest(stage["input"])
        digest(stage["output"])
        payloads = [w for w in stage["writes"] if w["phase"] == "payload"]
        require(len(payloads) == 1)
        artifact = next(a for a in by_component[c]["artifacts"] if a["kind"] == "payload")
        require(payloads[0]["after"] == artifact["sha256"])
        integer(stage["input_size"], 1)
        integer(stage["output_size"], 1)
        require(type(stage["completed"]) is bool and stage["completed"])
        if previous is not None:
            require(stage["input"] == previous["output"])
            require(stage["input_size"] == previous["output_size"])
        previous = stage


def order(doc):
    if len(doc["stages"]) < 2:
        raise Missing()
    require(len(doc["stages"]) == 2)
    for s, c in zip(doc["stages"], ("dpe", "cfru")):
        require(s["component"] == c)
        phases = records(s["phases"])
        if len(phases) < len(PHASES[c]):
            raise Missing()
        require(len(phases) == len(PHASES[c]))
        counts = {}
        for phase, name in zip(phases, PHASES[c]):
            fields(phase, ("name", "status", "count"))
            require(phase["name"] == name and phase["status"] in ("done", "absent"))
            integer(phase["count"], 0, MAX_RECORDS)
            if name in ("copy", "payload", "offsets") or (c == "dpe" and name == "expand"):
                require(phase["status"] == "done")
            if phase["status"] == "absent" or name in NO_ROM_WRITES:
                require(phase["count"] == 0)
            counts[name] = 0
        previous_phase = -1
        writes = records(s["writes"])
        state = digest(s["input"])
        for seq, w in enumerate(writes):
            fields(w, ("id", "seq", "phase", "kind", "start", "end", "owner", "allocation",
                       "before", "after", "input_state", "output_state", "target", "scan"))
            token(w["id"])
            require(type(w["seq"]) is int and w["seq"] == seq)
            require(w["phase"] in PHASES[c] and w["phase"] not in NO_ROM_WRITES)
            expected = ("bulk" if w["phase"] == "payload" else
                        "expand" if w["phase"] == "expand" else
                        "hook" if w["phase"] == "hooks" else
                        "wrapper" if w["phase"] == "function_rewrites" else
                        "pointer" if w["phase"] in POINTER_PHASES else "data")
            require(w["kind"] == expected or
                    (w["phase"] in ("events", "overlays") and w["kind"] == "pointer"))
            rank = PHASES[c].index(w["phase"])
            require(rank >= previous_phase)
            previous_phase = rank
            counts[w["phase"]] += 1
            span(w)
            digest(w["before"])
            digest(w["after"])
            require(digest(w["input_state"]) == state)
            state = digest(w["output_state"])
            require((w["before"] == w["after"]) == (w["input_state"] == state))
            require(w["scan"] == ({"cfru": "source", "dpe": "current"}[c]
                                   if w["phase"] == "repoint_all" else "none"))
        require(state == s["output"])
        require(len({w["id"] for w in writes}) == len(writes))
        for p in phases:
            require(counts[p["name"]] == p["count"])
        require(counts["payload"] == 1)


def allocations(doc):
    rows = indexed(doc["allocations"])
    main = {}
    for a in rows.values():
        fields(a, ("id", "component", "kind", "start", "end", "basis"))
        span(a)
        c = a["component"]
        require(c in PHASES)
        require(a["kind"] in ("payload", "overlay", "dynamic"))
        require(a["basis"] == "independent_reservation")
        if a["kind"] == "payload":
            require(c not in main)
            main[c] = a
            require(a["start"] == {"cfru": CFRU_START, "dpe": DPE_START}[c])
        elif a["kind"] == "overlay":
            require(c == "cfru" and a["start"] % 4 == 0)
        else:
            require(a["start"] % 4 == 0)
    if set(main) != set(PHASES):
        raise Missing()
    for a in rows.values():
        if a["component"] == "cfru":
            require(a["end"] <= DPE_START)
        if a["kind"] == "overlay":
            require(a["start"] >= (main["cfru"]["end"] + 3) // 4 * 4)
    ordered = sorted(rows.values(), key=lambda a: a["start"])
    for a, b in zip(ordered, ordered[1:]):
        require(not overlaps(a, b))
    return rows


def capacity(doc):
    if len(doc["stages"]) < 2:
        raise Missing()
    allocs = allocations(doc)
    for s in doc["stages"]:
        require(s["output_size"] == ROM_LIMIT)
        if s["component"] == "cfru":
            require(s["input_size"] == ROM_LIMIT)
        for w in s["writes"]:
            span(w)
            require(w["end"] <= s["output_size"])
            if w["phase"] == "payload":
                require(w["allocation"] in allocs)
                a = allocs[w["allocation"]]
                require(a["kind"] == "payload" and a["component"] == s["component"])
                require((w["start"], w["end"]) == (a["start"], a["end"]))
            if w["phase"] == "expand":
                require(s["component"] == "dpe")
                require(w["start"] == s["input_size"] and w["end"] == ROM_LIMIT)
            elif w["phase"] == "free_bytepatch" or (w["phase"] == "overlays" and w["kind"] == "data"):
                require(w["allocation"] in allocs)
                a = allocs[w["allocation"]]
                require(a["component"] == s["component"] and contains(a, w))
                require(a["kind"] == ("overlay" if w["phase"] == "overlays" else "dynamic"))
                if w["phase"] == "free_bytepatch":
                    require(a["start"] >= 0x900000)
                    require(a["end"] - a["start"] >= max(0x100, w["end"] - w["start"]))


def owners(doc):
    allocs = allocations(doc)
    rows = indexed(doc["owners"])
    by_role = {}
    for o in rows.values():
        fields(o, ("id", "component", "roles", "start", "end", "allocation", "basis"))
        span(o)
        roles = records(o["roles"])
        require(roles and len(set(map(token, roles))) == len(roles))
        require(o["component"] in PHASES)
        require(o["basis"] == "independent_link_and_input_map")
        if o["allocation"] is not None:
            require(o["allocation"] in allocs)
            a = allocs[o["allocation"]]
            require(a["component"] == o["component"] and contains(a, o))
        else:
            for a in allocs.values():
                require(not overlaps(a, o))
        for role in roles:
            by_role.setdefault(role, []).append(o)
    ordered = sorted(rows.values(), key=lambda o: o["start"])
    for a, b in zip(ordered, ordered[1:]):
        require(not overlaps(a, b))
    if not set(REQUIRED_ROLES) <= by_role.keys():
        raise Missing()
    for role, size in REQUIRED_ROLES.items():
        matches = by_role[role]
        # Asset/table populations may have many disjoint physical leaves.
        if role not in ("native_front_assets", "native_palette_assets", "palette_source",
                        "palette_snapshot", "palette_repoints"):
            require(len(matches) == 1)
        for o in matches:
            if size is not None:
                require(o["end"] - o["start"] == size)
            if role in ("oak_record", "pickup_record", "evolution_record"):
                require(o["start"] % 4 == 0)
    critical = [by_role[r][0]["id"] for r in (
        "oak_record", "oak_bitmap", "oak_front_bridge", "oak_cry_bridge",
        "oak_front_consumer", "oak_cry_consumer", "pickup_record", "pickup_bridge",
        "pickup_consumer", "evolution_record", "evolution_consumer",
        "native_front_table", "native_palette_table", "evolution_rows")]
    require(len(set(critical)) == len(critical))
    for role in REQUIRED_ROLES:
        if role.startswith(("oak_", "pickup_", "evolution_")) and role != "evolution_rows":
            require(by_role[role][0]["component"] == "cfru")
    return rows


def write_sets(doc):
    if len(doc["stages"]) < 2:
        raise Missing()
    own = owners(doc)
    allocs = allocations(doc)
    all_writes = {}
    prior = []
    overrides = {}
    for entry in records(doc["overrides"]):
        fields(entry, ("earlier", "later", "start", "end", "basis"))
        span(entry)
        require(entry["basis"] == "reviewed_source_order")
        key = (token(entry["earlier"]), token(entry["later"]))
        require(key not in overrides)
        overrides[key] = entry
    used = set()
    used_allocs = set()
    overlay_cursor = (next(a["end"] for a in allocs.values()
                           if a["component"] == "cfru" and a["kind"] == "payload") + 3) // 4 * 4
    for s in doc["stages"]:
        for w in s["writes"]:
            name = token(w["id"])
            require(name not in all_writes)
            phase = w["phase"]
            if phase in ("payload", "expand"):
                require(w["owner"] is None and w["target"] is None)
                if phase == "payload":
                    used_allocs.add(w["allocation"])
                else:
                    require(w["allocation"] is None)
            else:
                require(w["owner"] in own)
                o = own[w["owner"]]
                require(o["component"] == s["component"] and contains(o, w))
                require(w["allocation"] == o["allocation"])
                if phase == "free_bytepatch" or (phase == "overlays" and w["kind"] == "data"):
                    used_allocs.add(w["allocation"])
                    if phase == "overlays":
                        a = allocs[w["allocation"]]
                        require(a["start"] >= overlay_cursor)
                        overlay_cursor = (a["end"] + 3) // 4 * 4
            if w["kind"] in ("pointer", "hook", "wrapper"):
                t = fields(w["target"], ("owner", "offset", "thumb"))
                require(t["owner"] in own)
                target = own[t["owner"]]
                integer(t["offset"])
                require(target["start"] <= t["offset"] < target["end"])
                require(type(t["thumb"]) is bool)
                if phase == "hooks":
                    require(w["start"] % 2 == 0)
                    require(w["end"] - w["start"] == (10 if w["start"] % 4 else 8))
                if phase in ("hooks", "routine_pointers", "function_rewrites"):
                    require(t["thumb"] and t["offset"] % 2 == 0)
                if w["kind"] == "pointer":
                    require(w["end"] - w["start"] == 4)
            else:
                require(w["target"] is None)
            # Copy/expand materializes the base image, payload materializes its
            # reservation. Those writes may contain leaves of that allocation;
            # partial aliases and cross-component destruction remain failures.
            for earlier, component in prior:
                if not overlaps(earlier, w):
                    continue
                if earlier["phase"] == "expand" and component == "dpe":
                    continue
                if earlier["phase"] == "payload" and w["allocation"] == earlier["allocation"]:
                    require(contains(earlier, w))
                    continue
                if earlier["phase"] == "payload" and w["phase"] == "payload":
                    raise Invalid()
                # Matching bytes/hashes never establish overwrite permission.
                key = (earlier["id"], name)
                require(key in overrides)
                entry = overrides[key]
                require(entry["start"] == max(earlier["start"], w["start"]))
                require(entry["end"] == min(earlier["end"], w["end"]))
                require(earlier["owner"] == w["owner"] and component == s["component"])
                used.add(key)
                if earlier["start"] == w["start"] and earlier["end"] == w["end"]:
                    require(earlier["after"] == w["before"])
            prior.append((w, s["component"]))
            all_writes[name] = w
    require(used == set(overrides))
    require(used_allocs == set(allocs))


def validate(doc):
    """Fixed public status keys only; no untrusted strings escape this API."""
    result = dict.fromkeys(GATES, "UNKNOWN")
    checks = (("D1_RECEIPT_SCHEMA", schema), ("D1_RECEIPT_PROVENANCE", provenance),
              ("D1_WRITE_ORDER", order), ("D1_CAPACITY", capacity),
              ("D1_DECLARED_OWNERS", owners), ("D1_WRITE_SETS", write_sets))
    for name, check in checks:
        try:
            check(doc)
        except (Missing, KeyError):
            result[name] = "UNKNOWN"
        except (Invalid, TypeError, ValueError, IndexError, AttributeError):
            result[name] = "FAIL"
        else:
            result[name] = "PASS"
        if name == "D1_RECEIPT_SCHEMA" and result[name] != "PASS":
            break
    # Deliberate hard gates: self-declared receipts cannot establish native
    # completeness, link/ABI correctness, actual artifact identity or freshness.
    # No JSON flag, manifest, hash substitution or CLI switch can promote these.
    result["D1_ALL"] = "FAIL" if "FAIL" in result.values() else "UNKNOWN"
    return result


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result)
        result[key] = value
    return result


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    result = dict.fromkeys(GATES, "UNKNOWN")
    try:
        if len(argv) != 2 or argv[0] != "--receipt":
            raise Missing()
        # The only file opened is the explicitly supplied USER-local JSON.
        # No receipt field is interpreted as a path or executable.
        with open(argv[1], "rb") as stream:
            raw = stream.read(MAX_RECEIPT + 1)
        require(len(raw) <= MAX_RECEIPT)
        doc = json.loads(raw, object_pairs_hook=unique_object,
                         parse_constant=lambda _: (_ for _ in ()).throw(Invalid()))
        result = validate(doc)
    except (Invalid, ValueError, UnicodeError, RecursionError):
        result["D1_RECEIPT_SCHEMA"] = "FAIL"
        result["D1_ALL"] = "FAIL"
    except (Exception, KeyboardInterrupt):
        # Never print exception text, filenames, hashes, offsets or tracebacks.
        pass
    for name in GATES:
        print(name + "=" + result[name])
    return 1 if result["D1_ALL"] == "FAIL" else 2


if __name__ == "__main__":
    sys.exit(main())
