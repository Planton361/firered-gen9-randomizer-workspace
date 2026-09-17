"""Explicit pinned-source learnset inheritance; no pre-evolution/event move union."""
import json
import re
import tempfile
from pathlib import Path

import showdown_pokemon_data_sync as sync

OWNERSHIP = Path(__file__).with_name("showdown_learnset_ownership.json")


class TextSource:
    def __init__(self, text):
        self.text = text

    def read_text(self, **kwargs):
        return self.text

    def read_bytes(self):
        return self.text.encode()


def preserve_ties(pairs, canonical):
    """Showdown source strings encode levels, not in-game same-level ordering.

    Keep the existing reviewed local order for surviving same-level pairs; append
    new pairs in source property order. This cannot retain an older-only move.
    Always use the canonical baseline, never a mutable candidate's ordering.
    """
    rank = {pair: index for index, pair in enumerate(canonical)}
    return tuple(pair for _, pair in sorted(enumerate(pairs),
        key=lambda row: (row[1][0], rank.get(row[1], len(canonical) + row[0]))))


def provenance(selection):
    return {key: ([{"source": parent["source"], **provenance(parent)} for parent in value]
                  if key == "parents" else value)
            for key, value in selection.items() if key not in ("moves", "source")}


def render(before, targets, bindings, species):
    """Pure source replay: only approved table bodies and explicit pointer rows."""
    for name, pairs in targets.items():
        levels = [level for level, _ in pairs]
        if (not pairs or len(pairs) > 50 or levels != sorted(levels) or levels[0] > 1
                or any(not 0 <= level <= 100 for level in levels)
                or any(move == "MOVE_NONE" or not re.fullmatch(r"MOVE_[A-Z0-9_]+", move) for _, move in pairs)):
            raise ValueError("Invalid render target bounds/L1/move: " + name)
    with tempfile.TemporaryDirectory(prefix="coherent-source-render-") as tmp:
        path = Path(tmp) / "level_up_learnsets.c"
        path.write_text(before)
        pointers, blocks, _ = sync.parse_learnset_blocks(path)
        old_targets = set(targets) & blocks.keys()
        updates = {key: list(targets[table]) for key, table in pointers.items() if table in old_targets}
        sync.update_learnsets_file(path, updates, True, approved_tables=old_targets)
        text = path.read_text()
    new_tables = "".join("".join(sync.format_learnset_block(name, list(targets[name]), True)) + "\n"
                         for name in sorted(set(targets) - blocks.keys()))
    anchor = "const struct LevelUpMove* const gLevelUpLearnsets[] ="
    if text.count(anchor) != 1:
        raise ValueError("Missing/ambiguous pointer-array anchor")
    text = text.replace(anchor, new_tables + anchor, 1)
    for local, target in sorted(bindings.items()):
        constant = species[local]
        if target not in blocks and target not in targets:
            raise ValueError("Unrepresented new binding: " + local)
        if local in pointers:
            pattern = r"(\[" + constant + r"\]\s*=\s*)" + pointers[local] + r"\b"
            text, count = re.subn(pattern, lambda m: m[1] + target, text)
            if count != 1:
                raise ValueError("Ambiguous pointer replacement: " + local)
        else:
            # A new existing-ID designator, not a new species or resized ID space.
            marker = anchor + "\n{"
            if text.count(marker) != 1:
                raise ValueError("Missing binding insertion anchor")
            text = text.replace(marker, marker + f"\n\t[{constant}] = {target},", 1)
    sync.parse_learnset_blocks(TextSource(text))
    return text


def metadata(path):
    result = {}
    for key, block in sync.parse_ts_blocks(path).items():
        fields = {}
        for field in ("name", "baseSpecies", "forme", "changesFrom", "battleOnly", "cosmeticFormes"):
            match = re.search(r"\b" + field + r':\s*("[^"\n]*"|\[[^\]\n]*\])', block)
            if match:
                fields[field] = json.loads(match[1])
        result[key] = fields
    return result


def select(key, learnsets, forms, seen=()):
    """Return exact generation/pairs plus auditable parent paths, or fail closed.

    Pinned dex-species.ts learnsetParent/getFullLearnset establish form inheritance.
    Own L sources always win, even if older than the parent's dataset. Own R/M/T
    entries are not level-up sources. Every possible explicit battle parent must
    agree; constructor's first-parent choice is deliberately insufficient here.
    """
    if key in seen:
        raise ValueError("cyclic form inheritance: " + "/".join((*seen, key)))
    if key not in forms:
        raise ValueError("missing exact form metadata: " + key)
    generation, pairs = sync.coherent_level_moves(learnsets.get(key, {}))
    if generation is not None:
        return {"generation": generation, "moves": pairs, "dataset": key,
                "policy": "exact-literal-one-generation", "parents": []}
    fields = forms[key]
    parent = fields.get("changesFrom") or fields.get("battleOnly")
    rule = "explicit-changesFrom-or-battleOnly"
    if not parent and fields.get("forme") and key not in learnsets:
        parent = fields.get("baseSpecies")
        rule = "missing-literal-form-baseSpecies (dex-species.ts learnsetParent)"
    if not parent:
        raise ValueError("no coherent L dataset or explicit inheritance: " + key)
    parents = parent if isinstance(parent, list) else [parent]
    resolved = [select(sync.norm(p), learnsets, forms, (*seen, key)) for p in parents]
    if not resolved or len({(r["generation"], tuple(r["moves"])) for r in resolved}) != 1:
        raise ValueError("ambiguous battle/form parents: " + key)
    return {"generation": resolved[0]["generation"], "moves": resolved[0]["moves"],
            "dataset": resolved[0]["dataset"], "policy": rule,
            "parents": [{"source": sync.norm(p), **r} for p, r in zip(parents, resolved)]}
