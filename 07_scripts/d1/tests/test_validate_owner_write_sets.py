"""Entirely synthetic evidence: no ROM, source checkout, tool or build access."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "owner_validator", Path(__file__).resolve().parents[1] / "validate_owner_write_sets.py")
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


def h(text):
    return hashlib.sha256(text.encode()).hexdigest()


def fixture():
    doc = {"schema": 1, "sources": dict(v.SOURCES), "config": h("config"),
           "builds": [], "stages": [], "allocations": [], "owners": [], "overrides": []}
    for c, start, length in (("dpe", v.DPE_START, 0x40000),
                             ("cfru", v.CFRU_START, 0x4000)):
        doc["allocations"].append({"id": c, "component": c, "kind": "payload",
                                   "start": start, "end": start + length,
                                   "basis": "independent_reservation"})
        doc["builds"].append({"id": c, "component": c, "source": v.SOURCES[c],
                               "config": doc["config"], "fresh": True,
                               "artifacts": [{"id": kind, "kind": kind, "build": c,
                                              "sha256": h(c + kind), "cached": False}
                                             for kind in ("linked", "payload", "generated",
                                                          "objects", "repoint_cache")]})
        doc["stages"].append({"component": c, "build": c, "input": h("base"),
                               "output": h(c), "input_size": v.ROM_LIMIT,
                               "output_size": v.ROM_LIMIT, "completed": True,
                               "phases": [{"name": p, "status": "done", "count": 0}
                                          for p in v.PHASES[c]], "writes": []})
    cursors = {"cfru": v.CFRU_START, "dpe": v.DPE_START}
    for role, size in v.REQUIRED_ROLES.items():
        c = "dpe" if role.startswith("native_") or role == "evolution_rows" else "cfru"
        start = (cursors[c] + 3) // 4 * 4
        end = start + (size or 32)
        cursors[c] = end
        doc["owners"].append({"id": role, "component": c, "roles": [role],
                              "start": start, "end": end, "allocation": c,
                              "basis": "independent_link_and_input_map"})
    for s in doc["stages"]:
        a = next(a for a in doc["allocations"] if a["id"] == s["component"])
        add_write(doc, s["component"], "payload", a["start"], a["end"], allocation=a["id"])
    normalize(doc)
    return doc


def add_write(doc, c, phase, start, end, owner=None, allocation=None, target=None):
    s = next(s for s in doc["stages"] if s["component"] == c)
    kind = ("bulk" if phase == "payload" else "expand" if phase == "expand" else
            "hook" if phase == "hooks" else "wrapper" if phase == "function_rewrites" else
            "pointer" if phase in v.POINTER_PHASES else "data")
    after = (next(a["sha256"] for b in doc["builds"] if b["component"] == c
                  for a in b["artifacts"] if a["kind"] == "payload") if phase == "payload" else h("after"))
    w = {"kind": kind, "id": c + "_" + str(len(s["writes"])), "seq": len(s["writes"]),
         "phase": phase, "start": start, "end": end, "owner": owner,
         "allocation": allocation, "before": h("before"), "after": after,
         "input_state": h("in"), "output_state": h("out"), "target": target,
         "scan": ("source" if c == "cfru" else "current") if phase == "repoint_all" else "none"}
    s["writes"].append(w)
    return w


def normalize(doc):
    previous = h("base")
    for s in doc["stages"]:
        s["input"] = previous
        state = previous
        for seq, w in enumerate(s["writes"]):
            w["seq"] = seq
            w["input_state"] = state
            state = h(s["component"] + str(seq))
            w["output_state"] = state
        s["output"] = previous = state
        for p in s["phases"]:
            p["count"] = sum(w["phase"] == p["name"] for w in s["writes"])


def base_owner(doc, name="patch", start=0x1000, size=16):
    o = {"id": name, "component": "cfru", "roles": [name], "start": start,
         "end": start + size, "allocation": None, "basis": "independent_link_and_input_map"}
    doc["owners"].append(o)
    return o


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.doc = fixture()

    def check_gate(self, gate, expected="FAIL"):
        result = v.validate(self.doc)
        self.assertEqual(expected, result[gate])
        self.assertNotEqual("PASS", result["D1_ALL"])
        return result

    def test_consistent_receipt_is_never_complete_d1_pass(self):
        result = v.validate(self.doc)
        self.assertEqual(set(result), set(v.GATES))
        for name in v.GATES[:6]:
            self.assertEqual(result[name], "PASS", name)
        for name in v.GATES[6:]:
            self.assertEqual(result[name], "UNKNOWN", name)

    def test_missing_every_top_level_field_is_unknown(self):
        for key in self.doc:
            with self.subTest(key=key):
                doc = copy.deepcopy(self.doc)
                del doc[key]
                self.assertEqual("UNKNOWN", v.validate(doc)["D1_RECEIPT_SCHEMA"])

    def test_no_manifest_flag_can_unlock_native_pass(self):
        self.doc["complete_observation"] = True
        self.check_gate("D1_RECEIPT_SCHEMA")

    def test_revision_substitution_for_each_component(self):
        for c in v.SOURCES:
            with self.subTest(component=c):
                doc = copy.deepcopy(self.doc)
                doc["sources"][c] = "0" * 40
                self.assertEqual("FAIL", v.validate(doc)["D1_RECEIPT_SCHEMA"])

    def test_stale_build_source_config_id_and_cache(self):
        mutations = [("source", "0" * 40), ("config", h("stale")), ("fresh", False)]
        for key, value in mutations:
            with self.subTest(key=key):
                doc = copy.deepcopy(self.doc)
                doc["builds"][0][key] = value
                self.assertEqual("FAIL", v.validate(doc)["D1_RECEIPT_PROVENANCE"])
        for kind in ("generated", "objects", "repoint_cache", "payload", "linked"):
            doc = copy.deepcopy(self.doc)
            a = next(a for a in doc["builds"][0]["artifacts"] if a["kind"] == kind)
            a["cached"] = True
            self.assertEqual("FAIL", v.validate(doc)["D1_RECEIPT_PROVENANCE"])
            a["cached"] = False
            a["build"] = "old"
            self.assertEqual("FAIL", v.validate(doc)["D1_RECEIPT_PROVENANCE"])

    def test_missing_generated_inventory_is_not_fresh_proof(self):
        self.doc["builds"][0]["artifacts"].pop()
        self.check_gate("D1_RECEIPT_PROVENANCE", "UNKNOWN")

    def test_inserted_payload_must_match_selected_build_artifact(self):
        self.doc["stages"][0]["writes"][0]["after"] = h("stale binary")
        self.check_gate("D1_RECEIPT_PROVENANCE")

    def test_duplicate_artifact_kind_is_ambiguous(self):
        artifacts = self.doc["builds"][0]["artifacts"]
        artifacts.append(dict(artifacts[0], id="alias"))
        self.check_gate("D1_RECEIPT_PROVENANCE")

    def test_partial_or_failed_stage(self):
        for s in self.doc["stages"]:
            s["completed"] = False
            self.check_gate("D1_RECEIPT_PROVENANCE")
            s["completed"] = True

    def test_wrong_dpe_to_cfru_input_hash_and_size(self):
        self.doc["stages"][1]["input"] = h("wrong")
        self.check_gate("D1_RECEIPT_PROVENANCE")
        normalize(self.doc)
        self.doc["stages"][1]["input_size"] -= 1
        self.check_gate("D1_RECEIPT_PROVENANCE")

    def test_component_and_phase_order_are_exact(self):
        self.doc["stages"].reverse()
        self.check_gate("D1_WRITE_ORDER")
        self.doc["stages"].reverse()
        for s in self.doc["stages"]:
            s["phases"][2], s["phases"][3] = s["phases"][3], s["phases"][2]
            self.check_gate("D1_WRITE_ORDER")
            s["phases"][2], s["phases"][3] = s["phases"][3], s["phases"][2]

    def test_every_original_write_phase_with_explicit_ownership(self):
        for c in ("dpe", "cfru"):
            doc = fixture()
            target = next(o for o in doc["owners"] if o["id"] == "oak_front_consumer")
            for rank, phase in enumerate(v.PHASES[c]):
                if phase in v.NO_ROM_WRITES or phase in ("payload", "expand", "overlays", "free_bytepatch"):
                    continue
                o = base_owner(doc, c + str(rank), 0x1000 + rank * 32)
                o["component"] = c
                t = {"owner": target["id"], "offset": target["start"], "thumb": True}
                size = 8 if phase == "hooks" else 4
                add_write(doc, c, phase, o["start"], o["start"] + size, o["id"],
                          target=t if phase in v.POINTER_PHASES else None)
            normalize(doc)
            result = v.validate(doc)
            for gate in v.GATES[:6]:
                self.assertEqual("PASS", result[gate], (c, gate))

    def test_overlay_append_and_existing_map_header_repoint(self):
        a, o, w = self.add_allocation()
        patch_owner = base_owner(self.doc, "map_header", 0x2000, 4)
        repoint = add_write(self.doc, "cfru", "overlays", patch_owner["start"],
                            patch_owner["end"], patch_owner["id"],
                            target={"owner": o["id"], "offset": o["start"], "thumb": False})
        repoint["kind"] = "pointer"
        normalize(self.doc)
        for gate in v.GATES[:6]:
            self.check_gate(gate, "PASS")
        repoint["target"] = None
        self.check_gate("D1_WRITE_SETS")

    def test_events_dynamic_pointer_targets_are_checked(self):
        o = base_owner(self.doc, "event_pointer", 0x2000, 4)
        t = self.doc["owners"][0]
        w = add_write(self.doc, "cfru", "events", o["start"], o["end"], o["id"],
                      target={"owner": t["id"], "offset": t["start"], "thumb": False})
        w["kind"] = "pointer"
        normalize(self.doc)
        self.check_gate("D1_WRITE_SETS", "PASS")
        w["target"]["offset"] = t["end"]
        self.check_gate("D1_WRITE_SETS")

    def test_free_byte_search_minimum_capacity(self):
        a, o, w = self.add_allocation("dynamic", 0x900000)
        a["end"] = a["start"] + 255
        self.check_gate("D1_CAPACITY")

    def test_phase_cannot_hide_repoint_as_untyped_data(self):
        w = self.hook()
        w["kind"] = "data"
        self.check_gate("D1_WRITE_ORDER")

    def test_missing_phase_and_unknown_write_class(self):
        self.doc["stages"][0]["phases"].pop()
        self.check_gate("D1_WRITE_ORDER", "UNKNOWN")
        self.doc = fixture()
        self.doc["stages"][0]["writes"][0]["phase"] = "hidden_writer"
        self.check_gate("D1_WRITE_ORDER")

    def test_wrong_seq_phase_count_absent_and_reordered_write(self):
        s = self.doc["stages"][1]
        s["writes"][0]["seq"] = 4
        self.check_gate("D1_WRITE_ORDER")
        normalize(self.doc)
        s["phases"][1]["count"] = 0
        self.check_gate("D1_WRITE_ORDER")
        normalize(self.doc)
        s["phases"][1]["status"] = "absent"
        self.check_gate("D1_WRITE_ORDER")
        s["phases"][1]["status"] = "done"
        o = base_owner(self.doc)
        add_write(self.doc, "cfru", "bytepatch", o["start"], o["end"], o["id"])
        normalize(self.doc)
        s["writes"].reverse()
        self.check_gate("D1_WRITE_ORDER")

    def test_stale_output_intermediate_state_and_range_digest(self):
        s = self.doc["stages"][1]
        s["output"] = h("stale output")
        self.check_gate("D1_WRITE_ORDER")
        normalize(self.doc)
        s["writes"][0]["input_state"] = h("not selected input")
        self.check_gate("D1_WRITE_ORDER")
        normalize(self.doc)
        s["writes"][0]["before"] = "not-a-digest"
        self.check_gate("D1_WRITE_ORDER")

    def test_changed_range_cannot_have_unchanged_full_state(self):
        w = self.doc["stages"][1]["writes"][0]
        w["output_state"] = w["input_state"]
        self.doc["stages"][1]["output"] = w["input_state"]
        self.check_gate("D1_WRITE_ORDER")

    def test_cfru_exact_capacity_and_one_byte_overflow(self):
        a = self.doc["allocations"][1]
        w = self.doc["stages"][1]["writes"][0]
        a["end"] = w["end"] = v.DPE_START
        self.check_gate("D1_CAPACITY", "PASS")
        a["end"] = w["end"] = v.DPE_START + 1
        self.check_gate("D1_CAPACITY")

    def add_allocation(self, kind="overlay", start=None):
        payload = self.doc["allocations"][1]
        start = payload["end"] if start is None else start
        a = {"id": kind, "component": "cfru", "kind": kind, "start": start,
             "end": start + (256 if kind == "dynamic" else 32), "basis": "independent_reservation"}
        self.doc["allocations"].append(a)
        o = base_owner(self.doc, kind, start, 32)
        o["allocation"] = a["id"]
        w = add_write(self.doc, "cfru", "overlays" if kind == "overlay" else "free_bytepatch",
                      start, start + 32, o["id"], a["id"])
        normalize(self.doc)
        return a, o, w

    def test_overlay_append_success_and_capacity_boundary(self):
        a, o, w = self.add_allocation(start=v.DPE_START - 32)
        for gate in v.GATES[:6]:
            self.check_gate(gate, "PASS")
        a["end"] = o["end"] = w["end"] = v.DPE_START + 1
        self.check_gate("D1_CAPACITY")

    def test_overlay_before_payload_end_or_unaligned(self):
        a, o, w = self.add_allocation(start=v.CFRU_START + 32)
        self.check_gate("D1_CAPACITY")
        a["start"] = o["start"] = w["start"] = v.CFRU_START + 0x4001
        a["end"] = o["end"] = w["end"] = a["start"] + 32
        self.check_gate("D1_CAPACITY")

    def test_dynamic_allocation_uses_reservation_never_free_byte_guess(self):
        a, o, w = self.add_allocation("dynamic", 0x900000)
        self.check_gate("D1_WRITE_SETS", "PASS")
        a["basis"] = "FF_scan"
        self.check_gate("D1_CAPACITY")
        a["basis"] = "independent_reservation"
        a["start"] = v.DPE_START
        a["end"] = v.DPE_START + 32
        self.check_gate("D1_CAPACITY")

    def test_allocation_alias_and_unwritten_allocation(self):
        self.doc["allocations"].append(dict(self.doc["allocations"][0], id="alias"))
        self.check_gate("D1_CAPACITY")
        self.doc = fixture()
        self.doc["allocations"].append({"id": "unused", "component": "cfru", "kind": "dynamic",
                                         "start": 0x900000, "end": 0x900020,
                                         "basis": "independent_reservation"})
        self.check_gate("D1_WRITE_SETS")

    def test_output_truncation_wrong_payload_start_and_size(self):
        self.doc["stages"][1]["output_size"] -= 1
        self.check_gate("D1_CAPACITY")
        self.doc = fixture()
        self.doc["allocations"][1]["start"] += 4
        self.check_gate("D1_CAPACITY")
        self.doc = fixture()
        self.doc["stages"][1]["writes"][0]["end"] -= 1
        self.check_gate("D1_CAPACITY")

    def test_dpe_expansion_mode(self):
        s = self.doc["stages"][0]
        s["input_size"] = 0x1000000
        w = add_write(self.doc, "dpe", "expand", 0x1000000, v.ROM_LIMIT)
        s["writes"].insert(0, s["writes"].pop())
        normalize(self.doc)
        for gate in v.GATES[:6]:
            self.check_gate(gate, "PASS")
        w["start"] += 1
        self.check_gate("D1_CAPACITY")

    def test_every_required_owner_missing_and_wrong_abi_size(self):
        for role, size in v.REQUIRED_ROLES.items():
            with self.subTest(role=role):
                doc = copy.deepcopy(self.doc)
                doc["owners"] = [o for o in doc["owners"] if role not in o["roles"]]
                self.assertEqual("UNKNOWN", v.validate(doc)["D1_DECLARED_OWNERS"])
                if size is not None:
                    doc = copy.deepcopy(self.doc)
                    o = next(o for o in doc["owners"] if role in o["roles"])
                    o["end"] -= 1
                    self.assertEqual("FAIL", v.validate(doc)["D1_DECLARED_OWNERS"])

    def test_physical_alias_adjacency_and_same_owner_semantic_views(self):
        o = base_owner(self.doc)
        base_owner(self.doc, "adjacent", o["end"])
        self.check_gate("D1_DECLARED_OWNERS", "PASS")
        self.doc["owners"][-1]["start"] -= 1
        self.check_gate("D1_DECLARED_OWNERS")
        self.doc = fixture()
        palette = next(o for o in self.doc["owners"] if "native_palette_assets" in o["roles"])
        self.doc["owners"] = [o for o in self.doc["owners"] if "palette_source" not in o["roles"]]
        palette["roles"].append("palette_source")
        self.check_gate("D1_DECLARED_OWNERS", "PASS")

    def test_two_oak_consumers_cannot_alias(self):
        front = next(o for o in self.doc["owners"] if "oak_front_consumer" in o["roles"])
        self.doc["owners"] = [o for o in self.doc["owners"] if "oak_cry_consumer" not in o["roles"]]
        front["roles"].append("oak_cry_consumer")
        self.check_gate("D1_DECLARED_OWNERS")

    def test_magic_only_owner_wrong_component_and_alignment(self):
        o = self.doc["owners"][0]
        o["basis"] = "magic_marker"
        self.check_gate("D1_DECLARED_OWNERS")
        o["basis"] = "independent_link_and_input_map"
        o["component"] = "dpe"
        self.check_gate("D1_DECLARED_OWNERS")
        o["component"] = "cfru"
        o["start"] += 1
        o["end"] += 1
        self.check_gate("D1_DECLARED_OWNERS")

    def test_unowned_write_and_write_exceeding_owner(self):
        o = base_owner(self.doc)
        w = add_write(self.doc, "cfru", "bytepatch", o["start"], o["end"], "absent")
        normalize(self.doc)
        self.check_gate("D1_WRITE_SETS")
        w["owner"] = o["id"]
        w["end"] += 1
        self.check_gate("D1_WRITE_SETS")

    def test_negative_empty_bool_and_rom_bus_address_spans(self):
        for start, end in ((-1, 4), (4, 4), (8, 4), (True, 4), (0x08000000, 0x08000004)):
            with self.subTest(start=start, end=end):
                doc = copy.deepcopy(self.doc)
                doc["stages"][0]["writes"][0].update(start=start, end=end)
                self.assertEqual("FAIL", v.validate(doc)["D1_CAPACITY"])

    def hook(self, start=0x1000):
        o = base_owner(self.doc, start=start)
        target = next(o for o in self.doc["owners"] if "oak_front_consumer" in o["roles"])
        w = add_write(self.doc, "cfru", "hooks", start, start + (10 if start % 4 else 8), o["id"],
                      target={"owner": target["id"], "offset": target["start"], "thumb": True})
        normalize(self.doc)
        return w

    def test_hook_alignment_width_and_thumb_target(self):
        for start in (0x1000, 0x1002):
            self.doc = fixture()
            w = self.hook(start)
            self.check_gate("D1_WRITE_SETS", "PASS")
            w["end"] -= 1
            self.check_gate("D1_WRITE_SETS")
        self.doc = fixture()
        w = self.hook()
        w["target"]["thumb"] = False
        self.check_gate("D1_WRITE_SETS")

    def test_pointer_target_outside_owner_or_missing(self):
        w = self.hook()
        w["target"]["offset"] = v.ROM_LIMIT
        self.check_gate("D1_WRITE_SETS")
        w["target"] = None
        self.check_gate("D1_WRITE_SETS")

    def test_source_vs_current_dynamic_repoint_scan(self):
        for c, wrong in (("dpe", "source"), ("cfru", "current")):
            self.doc = fixture()
            o = base_owner(self.doc)
            o["component"] = c
            t = self.doc["owners"][0]
            w = add_write(self.doc, c, "repoint_all", o["start"], o["start"] + 4, o["id"],
                          target={"owner": t["id"], "offset": t["start"], "thumb": False})
            normalize(self.doc)
            self.check_gate("D1_WRITE_ORDER", "PASS")
            w["scan"] = wrong
            self.check_gate("D1_WRITE_ORDER")

    def two_writes(self):
        o = base_owner(self.doc)
        a = add_write(self.doc, "cfru", "special", o["start"], o["end"], o["id"])
        b = add_write(self.doc, "cfru", "bytepatch", o["start"], o["end"], o["id"])
        b["before"] = a["after"]
        normalize(self.doc)
        return a, b

    def override(self, a, b):
        e = {"earlier": a["id"], "later": b["id"], "start": max(a["start"], b["start"]),
             "end": min(a["end"], b["end"]), "basis": "reviewed_source_order"}
        self.doc["overrides"].append(e)
        return e

    def test_explicit_ordered_override_and_missing_permission(self):
        a, b = self.two_writes()
        self.check_gate("D1_WRITE_SETS")
        self.override(a, b)
        self.check_gate("D1_WRITE_SETS", "PASS")
        b["before"] = h("stale range")
        self.check_gate("D1_WRITE_SETS")

    def test_identical_bytes_do_not_waive_override(self):
        a, b = self.two_writes()
        b["after"] = a["after"]
        self.check_gate("D1_WRITE_SETS")

    def test_partial_override_exact_range_unused_or_reversed(self):
        a, b = self.two_writes()
        b["start"] += 4
        e = self.override(a, b)
        self.check_gate("D1_WRITE_SETS", "PASS")
        e["start"] -= 1
        self.check_gate("D1_WRITE_SETS")
        e["start"] += 1
        e["earlier"], e["later"] = e["later"], e["earlier"]
        self.check_gate("D1_WRITE_SETS")

    def test_duplicate_ids_overrides_and_cross_component_destruction(self):
        a, b = self.two_writes()
        e = self.override(a, b)
        self.doc["overrides"].append(dict(e))
        self.check_gate("D1_WRITE_SETS")
        self.doc["overrides"].pop()
        b["id"] = a["id"]
        self.check_gate("D1_WRITE_SETS")
        self.doc = fixture()
        a = add_write(self.doc, "dpe", "bytepatch", 0x1000, 0x1004, "dpe_patch")
        o = base_owner(self.doc, "dpe_patch", size=4)
        o["component"] = "dpe"
        b = add_write(self.doc, "cfru", "bytepatch", 0x1000, 0x1004, "dpe_patch")
        self.override(a, b)
        normalize(self.doc)
        self.check_gate("D1_WRITE_SETS")

    def test_malformed_nested_types_are_fixed_fail_or_unknown(self):
        for field in ("builds", "stages", "allocations", "owners", "overrides"):
            for value in (None, {}, "private/path", [None], [1], [{}]):
                with self.subTest(field=field, value=value):
                    doc = copy.deepcopy(self.doc)
                    doc[field] = value
                    result = v.validate(doc)
                    self.assertIn(result["D1_ALL"], ("FAIL", "UNKNOWN"))
                    self.assertTrue(set(result.values()) <= {"PASS", "FAIL", "UNKNOWN"})

    def test_empty_missing_evidence_collections_remain_unknown(self):
        for key, gate in (("builds", "D1_RECEIPT_PROVENANCE"),
                          ("stages", "D1_WRITE_ORDER"),
                          ("allocations", "D1_CAPACITY"),
                          ("owners", "D1_DECLARED_OWNERS")):
            with self.subTest(collection=key):
                doc = copy.deepcopy(self.doc)
                doc[key] = []
                result = v.validate(doc)
                self.assertEqual("UNKNOWN", result[gate])
                self.assertEqual("UNKNOWN", result["D1_ALL"])

    def test_oversized_record_collection(self):
        self.doc["owners"] = [{}] * (v.MAX_RECORDS + 1)
        self.check_gate("D1_RECEIPT_SCHEMA")


class CrossComponentOverrideTests(unittest.TestCase):
    def setUp(self):
        self.doc = fixture()
        self.owner = base_owner(self.doc, "shared_patch")
        self.owner.update(component="dpe", roles=["reviewed_shared_patch"])
        self.a = add_write(self.doc, "dpe", "bytepatch", 0x1000, 0x1004, self.owner["id"])
        self.b = add_write(self.doc, "cfru", "bytepatch", 0x1000, 0x1004, self.owner["id"])
        self.a["after"] = self.b["before"] = h("synthetic DPE replacement")
        self.b["after"] = h("different synthetic CFRU replacement")
        normalize(self.doc)
        self.edge = self.review(self.a, self.b)

    def review(self, earlier, later):
        edge = {"earlier": earlier["id"], "later": later["id"],
                "start": max(earlier["start"], later["start"]),
                "end": min(earlier["end"], later["end"]),
                "basis": "reviewed_dpe_to_cfru_patch",
                "review": {"reference": "SYNTHETIC_REVIEW_ONLY",
                           "decision_sha256": h("synthetic scoped source decision"),
                           "owner": self.owner["id"],
                           "sources": {c: v.SOURCES[c] for c in ("dpe", "cfru")},
                           "config": self.doc["config"],
                           "earlier_write": v.write_binding(earlier, "dpe"),
                           "later_write": v.write_binding(later, "cfru")}}
        self.doc["overrides"].append(edge)
        return edge

    def check(self, expected="FAIL"):
        result = v.validate(self.doc)
        self.assertEqual(expected, result["D1_WRITE_SETS"])
        self.assertNotEqual("PASS", result["D1_ALL"])
        for gate in v.GATES[6:-1]:
            self.assertEqual("UNKNOWN", result[gate], gate)
        return result

    def test_explicit_reviewed_dpe_to_cfru_patch_with_different_bytes(self):
        result = self.check("PASS")
        for gate in v.GATES[:6]:
            self.assertEqual("PASS", result[gate], gate)
        self.assertEqual("UNKNOWN", result["D1_ALL"])
        self.assertNotEqual(self.a["after"], self.b["after"])

    def test_unreviewed_or_generic_source_order_cannot_authorize_transfer(self):
        self.doc["overrides"] = []
        self.check()
        self.edge["basis"] = "reviewed_source_order"
        del self.edge["review"]
        self.doc["overrides"] = [self.edge]
        self.check()

    def test_identical_bytes_do_not_authorize_unreviewed_cross_write(self):
        self.b["after"] = self.a["after"]
        self.b["output_state"] = self.b["input_state"]
        self.doc["stages"][1]["output"] = self.b["output_state"]
        self.doc["overrides"] = []
        self.check()

    def test_missing_review_evidence_is_unknown(self):
        for key in tuple(self.edge["review"]):
            with self.subTest(field=key):
                value = self.edge["review"].pop(key)
                self.check("UNKNOWN")
                self.edge["review"][key] = value

    def test_review_identity_config_sources_and_write_bindings(self):
        for key, value in (("reference", ""), ("decision_sha256", "not-reviewed"),
                           ("owner", "foreign_owner"), ("config", h("stale config")),
                           ("sources", {"dpe": "0" * 40, "cfru": v.SOURCES["cfru"]}),
                           ("sources", {"dpe": v.SOURCES["dpe"], "cfru": "0" * 40}),
                           ("earlier_write", h("unrelated earlier write")),
                           ("later_write", h("unrelated later write"))):
            with self.subTest(field=key, value=value):
                saved = self.edge["review"][key]
                self.edge["review"][key] = value
                self.check()
                self.edge["review"][key] = saved

    def test_rebound_write_or_wrong_intersection_is_rejected(self):
        self.b["after"] = h("not the reviewed replacement")
        self.check()
        self.b["after"] = h("different synthetic CFRU replacement")
        for key, change in (("start", -1), ("start", 1), ("end", -1), ("end", 1)):
            with self.subTest(field=key, change=change):
                self.edge[key] += change
                self.check()
                self.edge[key] -= change

    def test_protected_or_untagged_owner_never_transfers(self):
        for roles in (["protected"], ["immutable"], ["patch"],
                      ["reviewed_shared_patch", "protected"],
                      ["reviewed_shared_patch", "native_palette_assets"]):
            with self.subTest(roles=roles):
                self.owner["roles"] = roles
                self.check()

    def test_missing_foreign_or_duplicate_physical_owner_is_rejected(self):
        self.edge["review"]["owner"] = "absent"
        self.check()
        self.edge["review"]["owner"] = self.owner["id"]
        self.b["owner"] = "absent"
        self.check()
        self.b["owner"] = self.owner["id"]
        alias = dict(self.owner, id="foreign_alias")
        self.doc["owners"].append(alias)
        result = self.check()
        self.assertEqual("FAIL", result["D1_DECLARED_OWNERS"])
        self.b["owner"] = alias["id"]
        self.check()

    def test_reversed_edge_stages_and_stale_sequence_are_rejected(self):
        self.edge["earlier"], self.edge["later"] = self.edge["later"], self.edge["earlier"]
        self.check()
        self.edge["earlier"], self.edge["later"] = self.edge["later"], self.edge["earlier"]
        self.b["seq"] += 1
        self.assertEqual("FAIL", self.check()["D1_WRITE_ORDER"])
        normalize(self.doc)
        self.doc["stages"].reverse()
        self.assertEqual("FAIL", self.check()["D1_WRITE_ORDER"])

    def test_reverse_component_direction_is_rejected(self):
        self.owner["component"] = "cfru"
        self.check()

    def test_unknown_cross_write_has_no_approved_predecessor(self):
        self.doc["stages"][0]["writes"].remove(self.a)
        normalize(self.doc)
        self.check()

    def test_partial_override_cannot_grant_uncovered_adjacent_bytes(self):
        self.b["end"] += 1
        normalize(self.doc)
        self.doc["overrides"] = []
        self.review(self.a, self.b)
        self.check()

    def test_exact_partial_intersection_and_full_union_coverage(self):
        self.a["end"] -= 2
        other = add_write(self.doc, "dpe", "bytepatch", 0x1002, 0x1004, self.owner["id"])
        normalize(self.doc)
        self.doc["overrides"] = []
        self.review(self.a, self.b)
        self.review(other, self.b)
        self.check("PASS")
        self.doc["overrides"].pop()
        self.check()


class CliTests(unittest.TestCase):
    def run_main(self, args, raw=None, error=None):
        out, err = io.StringIO(), io.StringIO()
        opener = patch("builtins.open", side_effect=error) if error else patch(
            "builtins.open", return_value=contextlib.closing(io.BytesIO(raw or b"{}")))
        with opener as mock_open, contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = v.main(args)
        self.assertEqual("", err.getvalue())
        lines = out.getvalue().splitlines()
        self.assertEqual(len(v.GATES), len(lines))
        for line, gate in zip(lines, v.GATES):
            self.assertRegex(line, "^" + gate + "=(PASS|FAIL|UNKNOWN)$")
        self.assertNotEqual(code, 0)
        return code, out.getvalue(), mock_open

    def test_valid_private_receipt_returns_unknown_exit_2(self):
        code, _, opened = self.run_main(["--receipt", "/PRIVATE/DO_NOT_ECHO"], json.dumps(fixture()).encode())
        self.assertEqual(2, code)
        opened.assert_called_once_with("/PRIVATE/DO_NOT_ECHO", "rb")

    def test_actual_file_io_is_only_synthetic_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic.json"
            path.write_text(json.dumps(fixture()), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(2, v.main(["--receipt", str(path)]))
            self.assertIn("D1_ALL=UNKNOWN", out.getvalue())
            self.assertNotIn(directory, out.getvalue())

    def test_missing_file_permission_and_interrupt_never_leak(self):
        for error in (FileNotFoundError("PRIVATE"), PermissionError("SECRET"),
                      RuntimeError("HASH OFFSET SYMBOL"), KeyboardInterrupt()):
            code, output, _ = self.run_main(["--receipt", "PRIVATE"], error=error)
            self.assertEqual(2, code)
            self.assertNotIn("PRIVATE", output)
            self.assertNotIn("SECRET", output)

    def test_no_cli_usage_help_or_unknown_option_echo(self):
        for args in ([], ["--help"], ["--PRIVATE", "SECRET"], ["--receipt"],
                     ["--receipt", "PRIVATE", "EXTRA"]):
            code, _, opened = self.run_main(args)
            self.assertEqual(2, code)
            opened.assert_not_called()

    def test_bad_json_duplicate_keys_nonfinite_utf8_and_truncation(self):
        for raw in (b'{"PRIVATE":', b'{"schema":1,"schema":1}', b'{"schema":NaN}',
                    b'{"schema":Infinity}', b'\xff', b'[]', b'null', b'42'):
            code, output, _ = self.run_main(["--receipt", "PRIVATE"], raw)
            self.assertEqual(1, code)
            self.assertNotIn("PRIVATE", output)

    def test_receipt_size_limit(self):
        with patch.object(v, "MAX_RECEIPT", 32):
            code, _, _ = self.run_main(["--receipt", "PRIVATE"], b"x" * 33)
        self.assertEqual(1, code)

    def test_untrusted_nested_strings_and_paths_are_never_opened_or_echoed(self):
        doc = fixture()
        doc["owners"][0]["id"] = "/PRIVATE/SECRET\nFAKE_PASS=PASS"
        _, output, opened = self.run_main(["--receipt", "receipt"], json.dumps(doc).encode())
        self.assertNotIn("SECRET", output)
        self.assertNotIn("FAKE_PASS", output)
        opened.assert_called_once()


if __name__ == "__main__":
    unittest.main()
