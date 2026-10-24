#!/usr/bin/env python3
"""ROM-free D1 receipt checks. Never authorizes insertion; see the contract.

Only USER may supply private receipts. No subprocess, inserter, artifact, ROM,
map or tool is opened. A consistent receipt is not an independent observation.
"""
import hashlib
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


def write_binding(write, component):
    """Bind a declared review to one exact operation, never to a wildcard."""
    data = json.dumps({"component": component, "write": write},
                      sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(data.encode("ascii")).hexdigest()


def write_sets(doc):
    if len(doc["stages"]) < 2:
        raise Missing()
    own = owners(doc)
    allocs = allocations(doc)
    all_writes = {}
    prior = []
    overrides = {}
    for entry in records(doc["overrides"]):
        cross = entry["basis"] == "reviewed_dpe_to_cfru_patch"
        fields(entry, ("earlier", "later", "start", "end", "basis") +
               (("review",) if cross else ()))
        span(entry)
        if cross:
            review = fields(entry["review"], ("reference", "decision_sha256", "owner",
                                             "sources", "config", "earlier_write", "later_write"))
            token(review["reference"])
            digest(review["decision_sha256"])
            token(review["owner"])
            fields(review["sources"], ("dpe", "cfru"))
            require(review["sources"] == {c: SOURCES[c] for c in ("dpe", "cfru")})
            require(review["config"] == doc["config"])
            digest(review["earlier_write"])
            digest(review["later_write"])
        else:
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
            foreign_writer = False
            if phase in ("payload", "expand"):
                require(w["owner"] is None and w["target"] is None)
                if phase == "payload":
                    used_allocs.add(w["allocation"])
                else:
                    require(w["allocation"] is None)
            else:
                require(w["owner"] in own)
                o = own[w["owner"]]
                require(contains(o, w))
                require(w["allocation"] == o["allocation"])
                foreign_writer = o["component"] != s["component"]
                if foreign_writer:
                    # Existing base patch leaves alone may be shared. Native
                    # payload/assets/ABI and other semantic owners stay closed.
                    require(o["component"] == "dpe" and s["component"] == "cfru")
                    require(o["roles"] == ["reviewed_shared_patch"])
                    require(o["allocation"] is None)
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
            cross_ranges = []
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
                require(earlier["owner"] == w["owner"])
                if component == s["component"]:
                    require(entry["basis"] == "reviewed_source_order")
                else:
                    require(foreign_writer and component == "dpe" and s["component"] == "cfru")
                    require(entry["basis"] == "reviewed_dpe_to_cfru_patch")
                    review = entry["review"]
                    require(review["owner"] == w["owner"])
                    require(review["earlier_write"] == write_binding(earlier, component))
                    require(review["later_write"] == write_binding(w, s["component"]))
                    cross_ranges.append((entry["start"], entry["end"]))
                used.add(key)
                if earlier["start"] == w["start"] and earlier["end"] == w["end"]:
                    require(earlier["after"] == w["before"])
            if foreign_writer:
                # Every byte in this foreign write needs a checked predecessor;
                # one approved intersection must not authorize adjacent bytes.
                cursor = w["start"]
                for start, end in sorted(cross_ranges):
                    require(start <= cursor)
                    cursor = max(cursor, end)
                require(cursor == w["end"])
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




# Independent live-observation checks. These never change validate(receipt)'s
# native UNKNOWN gates. The observer supplies actual bytes, not claimed hashes.
def observation_binding(key, start, data):
    import struct
    name = key.encode('utf-8')
    return struct.pack('<I', len(name)) + name + struct.pack('<QQ', start, len(data)) + data


class JournalVerifier:
    """Second byte-store implementation: recompute every recorded I/O effect."""
    def __init__(self, snapshots, limit=512 * 1024 * 1024, write_check=None):
        if sum(map(len, snapshots.values())) > limit:
            raise Missing()
        self.files = {k: bytearray(data) for k, data in snapshots.items()}
        self.handles = {}
        self.limit = limit
        self.count = 0
        self.writes = hashlib.sha256()
        self.write_check = write_check
        self.allocations = []

    def consume(self, e):
        op = e['op']
        if op == 'copy':
            require(e['src'] in self.files)
            self.files[e['dst']] = bytearray(self.files[e['src']])
        elif op == 'open':
            require(e['handle'] not in self.handles)
            key, mode = e['key'], e['mode']
            require(mode in ('rb', 'rb+', 'r', 'r+', 'w', 'a', 'wb', 'wb+'))
            if 'w' in mode:
                self.files[key] = bytearray()
            elif key not in self.files:
                require('a' in mode)
                self.files[key] = bytearray()
            self.handles[e['handle']] = [key, len(self.files[key]) if 'a' in mode else 0, mode]
        elif op in ('read', 'seek', 'write', 'truncate', 'close'):
            require(e['handle'] in self.handles)
            state = self.handles[e['handle']]
            key, pos, mode = state
            buf = self.files[key]
            if op == 'close':
                del self.handles[e['handle']]
                return
            if op == 'seek':
                require(type(e['offset']) is int and e['whence'] in (0, 1, 2))
                new = e['offset'] + (0 if e['whence'] == 0 else pos if e['whence'] == 1 else len(buf))
                require(0 <= new <= self.limit and new == e['position'])
                state[1] = new
            elif op == 'read':
                require(type(e['size']) is int and e['size'] >= -1)
                data = bytes(buf[pos:] if e['size'] == -1 else buf[pos:pos + e['size']])
                require(len(data) == e['length'] and hashlib.sha256(data).hexdigest() == e['sha256'])
                state[1] += len(data)
            elif op == 'write':
                require('+' in mode or 'w' in mode or 'a' in mode)
                data = bytes.fromhex(e['data'])
                if 'a' in mode:
                    pos = len(buf)
                require(e['key'] == key and pos == e['start'] and len(data) == e['length'])
                require(pos + len(data) <= self.limit)
                before = bytes(buf[pos:pos + len(data)])
                require(hashlib.sha256(before).hexdigest() == e['before'])
                if pos + len(data) > len(buf):
                    buf.extend(bytes(pos + len(data) - len(buf)))
                buf[pos:pos + len(data)] = data
                state[1] = pos + len(data)
                self.writes.update(observation_binding(key, pos, data))
                self.count += 1
                if key == 'test.gba':
                    if self.write_check is not None:
                        self.write_check(e)
            else:
                require('+' in mode or 'w' in mode or 'a' in mode)
                size = e['size']
                require(type(size) is int and 0 <= size <= self.limit)
                require(key != 'test.gba')  # Neither selected original truncates ROM.
                if size > len(buf):
                    buf.extend(bytes(size - len(buf)))
                else:
                    del buf[size:]
        elif op == 'allocate':
            require(type(e['start']) is int and type(e['length']) is int)
            require(e['start'] >= 0 and e['length'] > 0)
            self.allocations.append(e)
        elif op == 'subprocess':
            require(e['returncode'] == 0)
        else:
            raise Invalid()

    def finish(self, actual, count, binding):
        require(self.count == count and self.writes.hexdigest() == binding)
        require('test.gba' in self.files and bytes(self.files['test.gba']) == actual)
        return bytes(self.files['test.gba'])


class ArmElf:
    """Bounded ELF32/LE ARM final-link reader; no tool invocation or map trust."""
    def __init__(self, data):
        import struct
        self.data = data
        require(len(data) >= 52 and data[:7] == b'\x7fELF\x01\x01\x01')
        header = struct.unpack_from('<HHIIIIIHHHHHH', data, 16)
        require(header[0] == 2 and header[1] == 40 and header[7] == 52)
        shoff, entsize, count, names = header[5], header[10], header[11], header[12]
        require(entsize == 40 and 0 < count < 65536 and names < count)
        require(shoff + count * 40 <= len(data))
        self.sections = [struct.unpack_from('<IIIIIIIIII', data, shoff + i * 40) for i in range(count)]
        def section_bytes(s):
            require(s[4] + s[5] <= len(data))
            return data[s[4]:s[4] + s[5]]
        self.section_bytes = section_bytes
        strings = section_bytes(self.sections[names])
        def name(table, at):
            require(at < len(table) and b'\0' in table[at:])
            return table[at:table.index(b'\0', at)].decode('ascii')
        text = [s for s in self.sections if name(strings, s[0]) == '.text']
        require(len(text) == 1)
        self.text = text[0]
        require(self.text[1] == 1 and self.text[2] & 6 == 6)
        self.symbols = {}
        for s in self.sections:
            if s[1] != 2:
                continue
            require(s[9] == 16 and s[5] % 16 == 0 and s[6] < count)
            table = section_bytes(self.sections[s[6]])
            raw = section_bytes(s)
            for offset in range(0, len(raw), 16):
                n, value, size, info, other, index = struct.unpack_from('<IIIBBH', raw, offset)
                if not n or not index:
                    continue
                label = name(table, n)
                if info >> 4 in (1, 2):
                    require(label not in self.symbols)
                    self.symbols[label] = (value, size, info & 15, index)
        self.relocations = any(s[1] in (4, 9) and s[5] for s in self.sections)

    def payload(self, actual):
        # Multi-section/gapped layouts need an LMA-aware verifier, never guesses.
        loaded = [s for s in self.sections if s[1] == 1 and s[2] & 2 and s[5]]
        if loaded != [self.text]:
            raise Missing()
        require(self.section_bytes(self.text) == actual)
        return self.text[3]

    def symbol(self, name, size=None, thumb=False):
        if name not in self.symbols:
            raise Missing()
        value, length, kind, index = self.symbols[name]
        if size is not None:
            require(length == size)
        require(length > 0 and index < len(self.sections))
        if thumb:
            require(kind == 2 and value & 1)
        else:
            require(kind == 1)
        address = value & ~1 if thumb else value
        require(self.text[3] <= address < address + length <= self.text[3] + self.text[5])
        offset = self.text[4] + address - self.text[3]
        return value, self.data[offset:offset + length]


def verify_oak_link(elf, installed, bitmap):
    """Check actual linked literals/signatures and installed bytes, not markers."""
    import struct
    record, raw = elf.symbol('gOakIntroContract', 96)
    policy, bits = elf.symbol('gOakIntroEligibility', 180)
    require(record % 4 == 0 and policy % 4 == 0 and bits == bitmap and len(bitmap) == 180)
    names = ('CreateOakIntroPokemonSprite', 'OakIntroSpriteConsumer',
             'Task_OakSpeech_IsInhabitedFarAndWide', 'OakIntroCryConsumer')
    resolved = [elf.symbol(n, 28 if i % 2 == 0 else None, True) for i, n in enumerate(names)]
    intervals = [(record, record + 96), (policy, policy + 180)]
    for address, data in resolved:
        start = address & ~1
        intervals.append((start, start + len(data)))
    for i, (start, end) in enumerate(intervals):
        for a, b in intervals[i + 1:]:
            require(end <= a or b <= start)
        offset = start - 0x08000000
        require(0 <= offset < offset + end - start <= len(installed))
        linked = elf.data[elf.text[4] + start - elf.text[3]:elf.text[4] + end - elf.text[3]]
        require(installed[offset:offset + end - start] == linked)
    expected = bytearray(96)
    expected[:8] = b'CFROAK01'
    struct.pack_into('<IHHIHHHHIHH', expected, 8, record, 1, 96, 1, 1440, 29, 92, 2, policy, 180, 1)
    struct.pack_into('<IIIIIIHHHHHH', expected, 36, *(x[0] for x in resolved),
                     0x08000128, 0x08000130, 8, 8, 28, 20, 24, 4)
    struct.pack_into('<H', expected, 92, 29)
    require(raw == expected)
    prefix = bytes.fromhex('10b50449044b00f003f810bc01bc00471847c046')
    for i in (0, 2):
        bridge = resolved[i][1]
        require(bridge[:20] == prefix)
        require(struct.unpack_from('<II', bridge, 20) == (record, resolved[i + 1][0]))
    # Stripped final relocations do not prove relocation history or C semantics.
    return 'UNKNOWN'


def verify_linked_reservations(elf, owners, bindings):
    """Recompute critical physical owner locations from actual linked symbols."""
    for role, (symbol, thumb) in bindings.items():
        matches = [o for o in owners.values() if role in o['roles']]
        if len(matches) != 1:
            raise Missing()
        value, data = elf.symbol(symbol, REQUIRED_ROLES[role], thumb)
        start = (value & ~1 if thumb else value) - 0x08000000
        require(matches[0]['start'] == start and matches[0]['end'] == start + len(data))


if __name__ == "__main__":
    sys.exit(main())
