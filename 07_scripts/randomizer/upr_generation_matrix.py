#!/usr/bin/env python3
"""#727: disposable, user-owned candidate generation matrix; no runtime claim.

Compose the pinned Settings API, SettingsProfileGenerator.invoke, cli and
loaded-manifest. The older shell helpers require operator-supplied baselines,
retain outputs, and do not reopen/replay, so their UPR interfaces are reused
directly. No serializer or randomizer is reimplemented here.

CONTROL-approved safe bundles are derived in Workspace orchestration only.
Replaced Traits/Graphics/Misc and original Items FULL profiles remain source
evidence, never required PASS cases.
"""

import argparse
import base64
import itertools
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile
import zlib
from urllib.request import urlopen
from dataclasses import dataclass, field


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE = "9411c39f472d1d08555be988d2f7ab9482902580"
TREE = "e56df52bb79f3239fa4e9534cd252525d6229685"
BASELINE_GITLINKS = {
    "CFRU": ("02_external/CFRU-expansion", "e68a701aa4e68733ef8ad1e7cadb68825c0d16c2"),
    "DPE": ("02_external/Dynamic-Pokemon-Expansion-Gen-9", "d887185de1f6ae6a78e85c4311bbadde17041d00"),
    "UPR-FVX": ("02_external/upr-fvx", "4670a5413104ec02bc08c09ff584470a8a6cb7bd"),
}
# These unmerged source candidates are deliberately not Workspace Gitlinks.
CANDIDATES = {
    "CFRU": "e27e2113e4d59dc76cf5da8d4c43b067addae348",
    "DPE": "d887185de1f6ae6a78e85c4311bbadde17041d00",
    "UPR-FVX": "f979c3c6ec4d32a92ecf632a3d9d38151d5cb19c",
}
SOURCE = "random/src/main/java/com/uprfvx/random/cli/SettingsProfileGenerator.java"
SETTINGS_SOURCE = "random/src/main/java/com/uprfvx/random/Settings.java"
PUBLIC_BLOBS = {
    SOURCE: "b679e3e6bea9d908fef804af21456275974484c5",
    SETTINGS_SOURCE: "26760855a7642d38f6fb72afce694a0f215124ed",
}
PUBLIC_SOURCE_URL = ("https://raw.githubusercontent.com/Planton361/"
                     "universal-pokemon-randomizer-fvx/" + CANDIDATES["UPR-FVX"] + "/")
PRIMARY = 20261005658
SECONDARY = (0, 1, 677, PRIMARY)
TARGET_EXCLUSIONS = {
    "FVX-TRAIT-025": "OWNERSHIP_WITNESS_V1_REQUIRED",
    "FVX-MISC-011": "REDUNDANT_CFRU_NATIVE_REUSABLE_TMS",
}
EXCLUDED = frozenset({
    "FVX-TRAIT-017", "MODE-INCLUDE-MEGAS", "MODE-INCLUDE-GMAX",
    "MODE-INCLUDE-MEGA-ITEMS", "MODE-INCLUDE-Z-CRYSTALS",
    "MODE-INCLUDE-DYNAMAX-GMAX-ITEMS",
    "FVX-FOE-SENSIBLE-HELD-ITEMS",
}) | TARGET_EXCLUSIONS.keys()
RISK_SINGLES = ("FVX-TRAIT-027", "FVX-ITEM-010", "FVX-GFX-002", "FVX-GFX-004")
RISK_EVOLUTION = "CANDIDATE_EVOLUTION_TARGET_LINKED"
RISK_PICKUP = "CANDIDATE_PICKUP_SHOP"
RISK_IDS = frozenset(RISK_SINGLES + (RISK_EVOLUTION, RISK_PICKUP))
PICKUP_APPROVED_IDS = frozenset(("FVX-ITEM-010", RISK_PICKUP))
ITEMS_SAFE = tuple(f"FVX-ITEM-{n:03}" for n in (2, 4, 6, 7, 8, 9))
TRAITS_SAFE = tuple(f"FVX-TRAIT-{n:03}" for n in (1, 6, 8, 13, 14, 15, 16, 22))
GRAPHICS_PALETTES_SAFE = ("FVX-GFX-001", "FVX-GFX-003")
# Native/normalized CFRU QoL owners (002/004/010/012) stay in Layer B only.
MISC_SAFE = tuple(f"FVX-MISC-{n:03}" for n in (1, 3, 5, 6, 7, 8, 9))
SAFE_PROFILES = {
    "01_TRAITS_SAFE": ("01_TRAITS_FULL", TRAITS_SAFE),
    "09_GRAPHICS_PALETTES_SAFE": ("09_GRAPHICS_PALETTES", GRAPHICS_PALETTES_SAFE),
    "10_MISC_SAFE": ("10_MISC_TWEAKS", MISC_SAFE),
}
# Accepted exact public identity: #676 issuecomment-6035738033. Hidden GUI
# controls are retained exactly as accepted, never silently forced on.
IRONMON = (
    "422AAIEcgIAAAMABgCRAALkBAARBARMAABMAAEJACKY/gMAAAAAAAgWCeQ5AAgJ5AYEAOQAAgBBA"
    "AEBAAAAAAAJBBAKKBhQb2tlbW9uIEZpcmUgUmVkIChVKSAxLjBk9WWq48M4ig=="
)
FULL = (
    "01_TRAITS_SAFE", "02_STARTERS_STATICS_TRADES_FULL", "03_MOVES_MOVESETS_FULL",
    "04_FOE_BASE", "04_FOE_HELD_ITEMS_BASIC", "05_WILD_FULL", "06_TM_TUTOR_FULL",
    "07_ITEMS_SAFE", "08_TYPES_FULL", "09_GRAPHICS_PALETTES_SAFE", "10_MISC_SAFE",
    "11_SPECIAL_WILD",
)
FAMILIES = (
    "GEN_SAFE", "TRAITS", "STARTERS_STATICS_TRADES", "MOVES_MOVESETS", "FOE",
    "WILD", "TM_TUTOR", "ITEMS_SHOPS", "TYPE_EFFECTIVENESS",
    "GRAPHICS_PALETTES", "MISC", "SPECIAL_WILD",
)
# #681 minimum interactions: shared restricted species/evolution consumers,
# shared move/compatibility/held-item pools, palette species identity writers,
# and item/tweak writers. EVOLUTIONS is an explicit ordinary-evolution bundle.
TRIPLES = (
    ("GEN_SAFE", "STARTERS_STATICS_TRADES", "FOE"),
    ("GEN_SAFE", "FOE", "WILD"),
    ("GEN_SAFE", "TRAITS", "EVOLUTIONS"),
    ("TRAITS", "MOVES_MOVESETS", "FOE"), ("TRAITS", "WILD", "FOE"),
    ("MOVES_MOVESETS", "TM_TUTOR", "FOE"),
    ("MOVES_MOVESETS", "TM_TUTOR", "WILD"),
    ("STARTERS_STATICS_TRADES", "ITEMS_SHOPS", "TM_TUTOR"),
    ("FOE", "WILD", "ITEMS_SHOPS"), ("FOE", "TM_TUTOR", "ITEMS_SHOPS"),
    ("GRAPHICS_PALETTES", "TRAITS", "STARTERS_STATICS_TRADES"),
    ("MISC", "ITEMS_SHOPS", "TM_TUTOR"),
)
SELECTED = ("CONTROL_UNCHANGED", "CASUAL_NATDEX", "IRONMON_NATDEX")
MAXIMUM = ("MAX_SAFE_DATA", "MAX_SAFE_WORLD", "MAX_SAFE_COMBINED")
ALLOWED_FILES = frozenset({
    "08_tests/randomizer/fvx_feature_test_status_matrix.tsv",
    "08_tests/randomizer/195_fvx_feature_test_status_matrix.md",
    "07_scripts/randomizer/upr_generation_matrix.py",
    "07_scripts/randomizer/tests/test_upr_generation_matrix.py",
})


class MatrixError(Exception):
    """Messages raised here are public, fixed prerequisite descriptions."""


def command(args, cwd, timeout=600):
    # Never echo args, stdout or exception repr: these can contain private paths.
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          errors="replace", timeout=timeout, check=False)


def git(root, *args):
    result = command(["git", "-C", str(root), *args], root)
    if result.returncode:
        raise MatrixError("Public Git prerequisite could not be verified.")
    return result.stdout.strip()


def verify_pins(root):
    """Inspect only Workspace Git objects/index, never component worktrees."""
    if git(root, "rev-parse", WORKSPACE + "^{tree}") != TREE:
        raise MatrixError("Workspace basis tree mismatch; CONTROL rebaseline required.")
    git(root, "merge-base", "--is-ancestor", WORKSPACE, "HEAD")
    changed = set(git(root, "diff", "--name-only", WORKSPACE, "HEAD").splitlines())
    # Ignoring component worktrees is intentional: source comes from immutable
    # public blobs, and existing dirty/untracked user artifacts are not inspected.
    tracked = git(root, "status", "--porcelain", "--untracked-files=no", "--ignore-submodules=all")
    staged = git(root, "diff", "--cached", "--name-only", "--ignore-submodules=none")
    if not changed <= ALLOWED_FILES or tracked or staged:
        raise MatrixError("Workspace has unexpected changes; CONTROL rebaseline required.")
    for name, (relative, pin) in BASELINE_GITLINKS.items():
        entry = git(root, "ls-tree", "HEAD", relative).split()
        if entry != ["160000", "commit", pin, relative]:
            raise MatrixError(name + " Gitlink mismatch.")


def public_blob_id(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + bytes((0,)) + data).hexdigest()


def external_input_path(value, root, forbidden):
    # Reject lexical component/protected paths before even resolving symlinks.
    path = Path(os.path.abspath(value))
    if any(path.is_relative_to(root / p) for p in forbidden):
        raise MatrixError("Supplied source/JAR is inside a component or protected location; STOP.")
    resolved = path.resolve()
    if any(resolved.is_relative_to(root / p) for p in forbidden):
        raise MatrixError("Supplied source/JAR resolves into a component or protected location; STOP.")
    return resolved


def read_public_source(path=SOURCE, local_file=None):
    """Exact public-commit text only; no Git fetch/checkout/submodule reads."""
    if path not in PUBLIC_BLOBS:
        raise MatrixError("Unapproved public source path.")
    try:
        if local_file is None:
            with urlopen(PUBLIC_SOURCE_URL + path, timeout=30) as response:
                if response.geturl() != PUBLIC_SOURCE_URL + path:
                    raise MatrixError("Public source redirect was not approved.")
                data = response.read(200001)
        else:
            supplied = external_input_path(local_file, ROOT,
                                           ("02_external", "04_private_roms", "05_builds", "03_tools/releases"))
            data = supplied.read_bytes()
        if len(data) > 200000 or public_blob_id(data) != PUBLIC_BLOBS[path]:
            raise MatrixError("Exact candidate public source mismatch; STOP.")
        return data.decode("utf-8")
    except (OSError, UnicodeError, ValueError):
        raise MatrixError("Exact public source could not be verified; details discarded.") from None


def source_model(source):
    """Read public overlay IDs/profile lists, fail closed on unsupported syntax."""
    overlays = dict(re.findall(r'overlays\.put\("([^"]+)",\s*(.*?)\);\s*(?=overlays\.put|return Collections)',
                               source, re.S))
    unsupported = {name for name, body in overlays.items() if body.startswith("unsupported(")}
    profiles = {}
    for name, body in re.findall(r'profiles\.put\("([^"]+)",\s*(.*?)\);', source, re.S):
        profiles[name] = tuple(re.findall(r'"([A-Z0-9_-]+)"', body))
    counts = inventory_counts(overlays, unsupported)
    if counts != {"SOURCE_OVERLAY_IDS": 159, "GENERATOR_UNSUPPORTED": 4,
                  "TARGET_EXCLUDED": 9, "REQUIRED_OVERLAY_CASES": 146}:
        raise MatrixError("Pinned settings inventory counts changed.")
    if not EXCLUDED <= overlays.keys() or unsupported & EXCLUDED:
        raise MatrixError("Pinned settings inventory could not be derived.")
    if profiles.get("07_ITEMS_FULL") != ITEMS_SAFE + ("FVX-ITEM-010",):
        raise MatrixError("CONTROL-approved items derivation no longer matches source.")
    profiles["07_ITEMS_SAFE"] = ITEMS_SAFE
    for name, (original, members) in SAFE_PROFILES.items():
        if not set(members) <= set(profiles.get(original, ())):
            raise MatrixError("Safe family derivation no longer matches source.")
        if set(members) & (unsupported | EXCLUDED):
            raise MatrixError("Excluded overlay in safe family.")
        profiles[name] = members
    return overlays, unsupported, profiles


def inventory_counts(overlays, unsupported):
    """Account for every exact-source ID, including non-executable paths."""
    ids = set(overlays)
    return {
        "SOURCE_OVERLAY_IDS": len(ids),
        "GENERATOR_UNSUPPORTED": len(ids & unsupported),
        "TARGET_EXCLUDED": len(ids & EXCLUDED),
        "REQUIRED_OVERLAY_CASES": len(ids - unsupported - EXCLUDED),
    }


def print_inventory(counts):
    for name, count in counts.items():
        print(f"{name}: {count}")
    print("Target exclusions:")
    for overlay, reason in TARGET_EXCLUSIONS.items():
        print(overlay + ": " + reason)


def assignments(body):
    """Public source projection for closure planning only; UPR owns serialization."""
    result = dict(re.findall(r's\.set(\w+)\(([^;]+)\);?', body))
    if "setWildZoneMode(" in body:
        result["RandomizeWildPokemon"] = "true"
        result["WildPokemonZoneMod"] = re.search(r'Settings\.WildPokemonZoneMod\.\w+', body)[0]
    if "setGenLimit(" in body:
        result["LimitPokemon"] = "true"
        result["CurrentRestrictions"] = "new GenRestrictions(0x3FF)" if "true" in body else "new GenRestrictions(0x3FE)"
    if "enablePokemonPaletteRandomization" in body:
        result["PokemonPalettesMod"] = "Settings.PokemonPalettesMod.RANDOM"
    if "enableMiscTweak(" in body:
        result["MiscTweak"] = re.search(r'MiscTweak\.\w+', body)[0]
    return result


def mode(name, value):
    return "Settings." + name + "." + value


def closure(state):
    """Minimum owner activation, retaining each explicitly selected owner mode."""
    s = dict(state)

    def active(*keys):
        return any(s.get(k, "false") not in ("false", "0") for k in keys)

    def owner(key, value):
        if key not in s or s[key].endswith(".UNCHANGED") or s[key].endswith(".NONE") or s[key] == "false":
            s[key] = value

    if active("BaseStatsFollowEvolutions", "AssignEvoStatsRandomly"):
        owner("BaseStatisticsMod", mode("BaseStatisticsMod", "RANDOM"))
    if active("AssignEvoStatsRandomly"):
        s["BaseStatsFollowEvolutions"] = "true"
    if "ExpCurveMod" in s:
        s["StandardizeEXPCurves"] = "true"
    if active("EstimateLevelForEvolutionImprovements"):
        # GameRandomizer consumes the estimate only inside an improvement owner.
        s["ChangeImpossibleEvolutions"] = "true"
    if active("DualTypeOnly"):
        owner("SpeciesTypesMod", mode("SpeciesTypesMod", "COMPLETELY_RANDOM"))
    if active("AbilitiesFollowEvolutions", "AllowWonderGuard", "WeighDuplicateAbilitiesTogether",
              "EnsureTwoAbilities", "BanTrappingAbilities", "BanNegativeAbilities", "BanBadAbilities"):
        owner("AbilitiesMod", mode("AbilitiesMod", "RANDOMIZE"))
    if active("EvosSimilarStrength", "EvosSameTyping", "EvosMaxThreeStages", "EvosNoConvergence",
              "EvosForceChange", "EvosForceGrowth", "EvosAllowAltFormes"):
        owner("EvolutionsMod", mode("EvolutionsMod", "RANDOM"))
    if active("StartersNoLegendaries", "RandomizeStartersHeldItems", "BanBadRandomStarterHeldItems",
              "StartersBSTMinimum", "StartersBSTMaximum", "StartersTypeMod"):
        owner("StartersMod", mode("StartersMod", "COMPLETELY_RANDOM"))
    if active("BanBadRandomStarterHeldItems"):
        s["RandomizeStartersHeldItems"] = "true"
    if active("StaticLevelModified", "CorrectStaticMusic"):
        owner("StaticPokemonMod", mode("StaticPokemonMod", "COMPLETELY_RANDOM"))
    if active("RandomizeInGameTradesNicknames", "RandomizeInGameTradesOTs",
              "RandomizeInGameTradesIVs", "RandomizeInGameTradesItems"):
        owner("InGameTradesMod", mode("InGameTradesMod", "RANDOMIZE_GIVEN_AND_REQUESTED"))
    if active("StartWithGuaranteedMoves", "ReorderDamagingMoves", "BlockBrokenMovesetMoves", "MovesetsForceGoodDamaging"):
        owner("MovesetsMod", mode("MovesetsMod", "COMPLETELY_RANDOM"))
    trainer_keys = [k for k in s if k.startswith(("Trainers", "Better", "Additional", "DiverseTypes", "RandomizeHeldItemsFor"))]
    if active(*trainer_keys, "EliteFourUniquePokemonNumber", "BanPrematureEvos", "RivalCarriesStarterThroughout", "BattleStyle"):
        owner("TrainersMod", mode("TrainersMod", "RANDOM"))
    if active("RivalCarriesStarterThroughout"):
        owner("StartersMod", mode("StartersMod", "COMPLETELY_RANDOM"))
    if active("RandomizeTrainerClassSprites"):
        s["RandomizeTrainerClassNames"] = "true"
    if active("TrainersMatchTypingDistribution") and s.get("TrainersMod") == mode("TrainersMod", "RANDOM"):
        # getTypeForTrainer uses frequency weighting only for a type theme.
        s["TrainersMod"] = mode("TrainersMod", "TYPE_THEMED")
    if active("SensibleItemsOnlyForTrainers"):
        for rank in ("Boss", "Important", "Regular"):
            s["RandomizeHeldItemsFor" + rank + "TrainerPokemon"] = "true"
        owner("TrainersMod", mode("TrainersMod", "RANDOM"))
    wild_keys = [k for k in s if k.startswith(("Wild", "KeepWild", "RandomizeWild"))]
    if active(*wild_keys, "SplitWildZoneByEncounterTypes", "BlockWildLegendaries", "UseMinimumCatchRate",
              "BanBadRandomWildPokemonHeldItems", "CatchEmAllEncounters", "SimilarStrengthEncounters",
              "BalanceShakingGrass", "UseTimeBasedEncounters"):
        s["RandomizeWildPokemon"] = "true"
        owner("WildPokemonZoneMod", mode("WildPokemonZoneMod", "ENCOUNTER_SET"))
    if active("BanBadRandomWildPokemonHeldItems"):
        s["RandomizeWildPokemonHeldItems"] = "true"
    for prefix, move_key, move_type, compat_key, compat_type in (
        ("Tm", "TmsMod", "TMsMod", "TmsHmsCompatibilityMod", "TMsHMsCompatibilityMod"),
        ("Tutor", "MoveTutorMovesMod", "MoveTutorMovesMod", "MoveTutorsCompatibilityMod", "MoveTutorsCompatibilityMod"),
    ):
        plural = "Tms" if prefix == "Tm" else "Tutors"
        suffix = "TMs" if prefix == "Tm" else "Tutors"
        if active("KeepFieldMove" + suffix, "BlockBroken" + ("TM" if prefix == "Tm" else "Tutor") + "Moves", plural + "ForceGoodDamaging"):
            owner(move_key, mode(move_type, "RANDOM"))
        if active(prefix + "LevelUpMoveSanity", ("Tms" if prefix == "Tm" else "Tutor") + "FollowEvolutions"):
            owner(compat_key, mode(compat_type, "COMPLETELY_RANDOM"))
            owner(move_key, mode(move_type, "RANDOM"))
    if active("FullHMCompat"):
        owner("TmsHmsCompatibilityMod", mode("TMsHMsCompatibilityMod", "COMPLETELY_RANDOM"))
    if active("BanBadRandomFieldItems"):
        owner("FieldItemsMod", mode("FieldItemsMod", "RANDOM"))
    if active("BanBadRandomShopItems", "BanRegularShopItems", "BanOPShopItems", "GuaranteeEvolutionItems",
              "GuaranteeXItems", "BalanceShopPrices", "AddCheapRareCandiesToShops"):
        owner("ShopItemsMod", mode("ShopItemsMod", "RANDOM"))
    if active("PokemonPalettesFollowTypes", "PokemonPalettesFollowEvolutions", "PokemonPalettesShinyFromNormal"):
        owner("PokemonPalettesMod", mode("PokemonPalettesMod", "RANDOM"))
    if active("InverseTypesRandomImmunities"):
        # Only the INVERSE branch consumes this flag (GameRandomizer).
        s["TypeEffectivenessMod"] = mode("TypeEffectivenessMod", "INVERSE")
    if active("AllowRegionalFormsAcrossGenLimit", "LimitPokemon") and "CurrentRestrictions" not in s:
        s["LimitPokemon"] = "true"
        s["CurrentRestrictions"] = "new GenRestrictions(0x3FE)"
    return s


@dataclass
class Intent:
    id: str
    layer: str
    overlays: tuple = ()
    extra: dict = field(default_factory=dict)
    families: tuple = ()
    classification: str = "STRESS_ONLY"
    replay: bool = False
    secondary: bool = False


def effective(intent, overlays):
    s = {}
    for overlay in intent.overlays:
        for key, value in assignments(overlays[overlay]).items():
            if key == "MiscTweak":
                s[key] = " | ".join(sorted(set(s.get(key, "").split(" | ")) - {""} | {value}))
            elif key in s and key.endswith("Mod") and s[key] != value:
                raise MatrixError("Mutually exclusive modes in case " + intent.id)
            else:
                s[key] = value
    guard_pilot_state(s)  # Reject requested incompatibilities before any override.
    # Explicit Layer-C variants have no competing overlay for their owner.
    s.update(intent.extra)
    state = closure(s)
    guard_pilot_state(state)
    return state


def guard_pilot_state(state):
    if state.get("MakeEvolutionsEasier") == "true":
        raise MatrixError("Make Evolutions Easier requires independently validated OWNERSHIP_WITNESS_V1; not enabled by this runner.")
    if (state.get("PokemonPalettesFollowTypes") == "true"
            and state.get("PokemonPalettesShinyFromNormal") == "true"):
        raise MatrixError("CFRU/DPE Follow Types + Shiny From Normal is excluded; STOP.")
    if (state.get("EvolutionsMod") == mode("EvolutionsMod", "RANDOM_EVERY_LEVEL")
            or any(state.get(k) == "true" for k in ("AllowMegaForms", "AllowGigantamaxForms",
                "IncludeMegaItems", "IncludeZCrystalItems", "IncludeDynamaxGmaxItems"))
            or "MiscTweak.REUSABLE_TMS" in state.get("MiscTweak", "")):
        raise MatrixError("Pilot exclusion activated; STOP.")


def build_matrix(overlays, unsupported, profiles):
    cases = [Intent(name, "ACCEPTANCE", classification="ACCEPTANCE", replay=True,
                    secondary=name != "CONTROL_UNCHANGED") for name in SELECTED]
    cases += [Intent(name, "STRESS", (name,), replay=name in RISK_SINGLES,
                     secondary=name in RISK_SINGLES)
              for name in overlays if name not in unsupported | EXCLUDED]
    # Layer C aliases all existing meaningful MODE/enum-owner overlay paths.
    mode_ids = [name for name in overlays if name.startswith("MODE-") and name not in EXCLUDED]
    mode_ids += [f"FVX-SST-{n:03}" for n in range(2, 13)]
    mode_ids += [f"FVX-ITEM-{n:03}" for n in (1, 2, 3, 5, 6)]
    cases += [Intent("MODE_ALIAS_" + name, "MODE", (name,)) for name in mode_ids]
    # Other meaningful enum values absent from generator overlays use Settings API.
    variants = {
        "BaseStatisticsMod": ("SHUFFLE",), "SpeciesTypesMod": ("RANDOM_FOLLOW_EVOLUTIONS",),
        "MovesetsMod": ("RANDOM_PREFER_SAME_TYPE", "METRONOME_ONLY"),
        "TrainersMod": ("TYPE_THEMED_ELITE4_GYMS", "KEEP_THEME_OR_PRIMARY"),
        "WildPokemonTypeMod": ("RANDOM_THEMES",), "WildPokemonEvolutionMod": ("BASIC_ONLY",),
        "TmsHmsCompatibilityMod": ("RANDOM_PREFER_TYPE", "FULL"),
        "MoveTutorsCompatibilityMod": ("RANDOM_PREFER_TYPE", "FULL"),
        "InGameTradesMod": ("RANDOMIZE_GIVEN",),
        "ExpCurveMod": ("LEGENDARIES", "ALL"),
        "StartersTypeMod": ("TRIANGLE", "UNIQUE", "SINGLE_TYPE"),
    }
    types = {"TmsHmsCompatibilityMod": "TMsHMsCompatibilityMod"}
    for key, values in variants.items():
        for value in values:
            extra = {key: mode(types.get(key, key), value)}
            if key == "ExpCurveMod":
                extra["StandardizeEXPCurves"] = "true"
            if value == "SINGLE_TYPE":
                extra["StartersSingleType"] = "1"  # public Type index, not a ROM species ID
            cases.append(Intent("MODE_" + key + "_" + value, "MODE", extra=extra))
    cases += [Intent(name, "FULL", profiles[name]) for name in FULL]
    bundles = dict(zip(FAMILIES[1:], (profiles[n] for n in (
        FULL[0], FULL[1], FULL[2], FULL[3], FULL[5], FULL[6], FULL[7],
        FULL[8], FULL[9], FULL[10], FULL[11]))))
    bundles["GEN_SAFE"] = ("MODE-GEN-LIMIT-1-9-NO-RELATIVES", "MODE-ALLOW-REGIONAL-FORMS",
                           "MODE-GEN-LIMIT-1-9-NO-MEGAS", "MODE-GEN-LIMIT-1-9-NO-GMAX")
    bundles["EVOLUTIONS"] = ("FVX-TRAIT-016", "FVX-TRAIT-022")

    def composite(name, layer, families, secondary=False):
        features = tuple(dict.fromkeys(itertools.chain.from_iterable(bundles[f] for f in families)))
        return Intent(name, layer, features, families=families, replay=secondary, secondary=secondary)

    cases += [composite("PAIR_" + "+".join(pair), "PAIR", pair) for pair in itertools.combinations(FAMILIES, 2)]
    cases += [composite("TRIPLE_" + "+".join(triple), "TRIPLE", triple) for triple in TRIPLES]
    data = ("GEN_SAFE", "TRAITS", "MOVES_MOVESETS", "EVOLUTIONS")
    world = ("STARTERS_STATICS_TRADES", "FOE", "WILD", "TM_TUTOR", "ITEMS_SHOPS")
    for name, families in zip(MAXIMUM, (data, world, data + world + ("GRAPHICS_PALETTES", "MISC", "SPECIAL_WILD"))):
        cases.append(composite(name, "MAX", families, True))
    # Explicit G acceptance aliases preserve coverage without repeating primary runs.
    cases += [Intent("G_" + name, "MAX", classification="ACCEPTANCE", replay=True, secondary=True)
              for name in SELECTED[1:]]
    # Exactly two new compositions; keep risk leaves out of safe family bundles.
    cases += [
        Intent(RISK_EVOLUTION, "RISK",
               ("FVX-GEN-001", "MODE-GEN-LIMIT-1-9", "FVX-TRAIT-016",
                "FVX-TRAIT-024", "FVX-TRAIT-026", "FVX-TRAIT-027"),
               extra={"MakeEvolutionsEasier": "false"}, replay=True, secondary=True),
        Intent(RISK_PICKUP, "RISK", ("FVX-ITEM-010", "FVX-ITEM-006"),
               replay=True, secondary=True),
    ]
    cases.append(Intent("04_FOE_HELD_ITEMS_SENSIBLE_EXPECTED_FAIL", "DIAGNOSTIC",
                        profiles["04_FOE_HELD_ITEMS_SENSIBLE_EXPECTED_FAIL"], classification="DIAGNOSTIC"))
    for case in cases:
        if case.layer in {"FULL", "PAIR", "TRIPLE", "MAX"} and set(case.overlays) & set(RISK_SINGLES):
            raise MatrixError("Candidate risk leaf entered a safe family bundle; STOP.")
        if case.classification != "DIAGNOSTIC" and (set(case.overlays) & (unsupported | EXCLUDED)):
            raise MatrixError("Excluded overlay in required case.")
        effective(case, overlays)
    return cases


def selected_name(intent):
    return intent.id.removeprefix("G_")


# Exact C reconstruction from #676 semantics, including explicit OFF/UNCHANGED
# defaults. Misc=8 and hidden Ban Irregular=false follow #676 CONTROL's runtime
# clarification. Engine AI/scaling are runtime-owned, not UPR Settings fields.
CASUAL = {
    "LimitPokemon": "true", "CurrentRestrictions": "new GenRestrictions(0x3FE)",
    "AllowRegionalFormsAcrossGenLimit": "true", "CurrentMiscTweaks": "8",
    "StartersMod": mode("StartersMod", "COMPLETELY_RANDOM"),
    "AllowStarterAltFormes": "true", "StartersNoLegendaries": "true",
    "RandomizeWildPokemon": "true", "WildPokemonZoneMod": mode("WildPokemonZoneMod", "ENCOUNTER_SET"),
    "AllowWildAltFormes": "true", "TrainersMod": mode("TrainersMod", "RANDOM"),
    "AllowTrainerAlternateFormes": "true", "TrainersBlockLegendaries": "true",
    "TrainersBlockEarlyWonderGuard": "true", "TrainersAvoidDuplicates": "true",
    "StaticPokemonMod": mode("StaticPokemonMod", "COMPLETELY_RANDOM"), "AllowStaticAltFormes": "true",
    "InGameTradesMod": mode("InGameTradesMod", "RANDOMIZE_GIVEN_AND_REQUESTED"),
    "EvolutionsMod": mode("EvolutionsMod", "RANDOM"), "EvosForceChange": "true", "EvosAllowAltFormes": "true",
    "TmsMod": mode("TMsMod", "RANDOM"), "MoveTutorMovesMod": mode("MoveTutorMovesMod", "RANDOM"),
    "BlockBrokenTMMoves": "true", "KeepFieldMoveTMs": "true",
    "BlockBrokenTutorMoves": "true", "KeepFieldMoveTutors": "true",
    "FieldItemsMod": mode("FieldItemsMod", "RANDOM"), "BanBadRandomFieldItems": "true",
    "ShopItemsMod": mode("ShopItemsMod", "RANDOM"), "BanBadRandomShopItems": "true",
}


def java_setters(state):
    lines = []
    for key, value in sorted(state.items()):
        if key == "MiscTweak":
            value = " | ".join(v + ".getValue()" for v in value.split(" | "))
            lines.append("s.setCurrentMiscTweaks(s.getCurrentMiscTweaks() | " + value + ");")
        else:
            lines.append("s.set" + key + "(" + value + ");")
    return "\n".join(lines)



# Temporary categorical observations from the real Settings getters; never print
# settings strings or reconstruct settings bytes to enable an option.
OBSERVE_JAVA = r'''
  static String observe(Settings s) {
    return String.join("\n",
      "LimitPokemon=" + s.isLimitPokemon(),
      "CurrentRestrictions=" + (s.getCurrentRestrictions() == null ? -1 : s.getCurrentRestrictions().toInt()),
      "EvolutionsMod=" + s.getEvolutionsMod(),
      "ChangeImpossibleEvolutions=" + s.isChangeImpossibleEvolutions(),
      "MakeEvolutionsEasier=" + s.isMakeEvolutionsEasier(),
      "EstimateLevelForEvolutionImprovements=" + s.useEstimatedLevelsForEvolutionImprovements(),
      "RemoveTimeBasedEvolutions=" + s.isRemoveTimeBasedEvolutions(),
      "PickupItemsMod=" + s.getPickupItemsMod(),
      "BanBadRandomPickupItems=" + s.isBanBadRandomPickupItems(),
      "ShopItemsMod=" + s.getShopItemsMod(),
      "PokemonPalettesMod=" + s.getPokemonPalettesMod(),
      "PokemonPalettesFollowTypes=" + s.isPokemonPalettesFollowTypes(),
      "PokemonPalettesFollowEvolutions=" + s.isPokemonPalettesFollowEvolutions(),
      "PokemonPalettesShinyFromNormal=" + s.isPokemonPalettesShinyFromNormal(),
      "UseTimeBasedEncounters=" + s.isUseTimeBasedEncounters());
  }
'''
OBSERVATION_KEYS = tuple(re.findall(r'"(\w+)="', OBSERVE_JAVA))


def parse_observation(text):
    pairs = [line.split("=", 1) for line in text.splitlines()]
    if (len(pairs) != len(OBSERVATION_KEYS)
            or any(len(pair) != 2 for pair in pairs)
            or tuple(pair[0] for pair in pairs) != OBSERVATION_KEYS
            or any(not re.fullmatch(r"true|false|-?[0-9]{1,10}|[A-Z_]+", pair[1]) for pair in pairs)):
        raise MatrixError("Settings observation schema mismatch; details discarded.")
    return dict(pairs)


def verify_risk_states(cases, overlays, observations, stage):
    expected_indices = {i for i, c in enumerate(cases) if c.id in RISK_IDS}
    if set(observations) != expected_indices:
        raise MatrixError("Incomplete candidate Settings observations; STOP.")
    for i in expected_indices:
        case, actual = cases[i], observations[i]
        expected = effective(case, overlays)
        expected["MakeEvolutionsEasier"] = "false"
        if case.id in ("FVX-GFX-002", "FVX-GFX-004"):
            expected.setdefault("PokemonPalettesFollowTypes", "false")
            expected.setdefault("PokemonPalettesShinyFromNormal", "false")
        for key, value in expected.items():
            if key not in OBSERVATION_KEYS:
                continue
            if key == "CurrentRestrictions":
                value = str(int(re.fullmatch(r"new GenRestrictions\((0x[0-9A-Fa-f]+)\)", value)[1], 16))
            elif value.startswith("Settings."):
                value = value.rsplit(".", 1)[1]
            if actual.get(key) != value:
                if key in ("LimitPokemon", "CurrentRestrictions"):
                    raise MatrixError("Candidate Gen1-9/relatives state was serialized or normalized away; requested coverage NOT_RUN.")
                raise MatrixError("Candidate option state differs after " + stage + "; STOP.")
        guard_pilot_state(actual)


def bridge_source(cases, overlays):
    """A temporary no-ROM Java adapter; all serialization stays in pinned UPR."""
    blocks = []
    approved_pickup = [str(i) for i, c in enumerate(cases) if c.id in PICKUP_APPROVED_IDS]
    pickup_gate = "Set.of(" + ",".join(map(json.dumps, approved_pickup)) + ").contains(id)"
    for i, case in enumerate(cases):
        name = selected_name(case)
        if name == "IRONMON_NATDEX":
            setup = "s = Settings.fromString(" + json.dumps(IRONMON) + ");"
        elif name == "CASUAL_NATDEX":
            setup = "s = baseline();\n" + java_setters(CASUAL)
        else:
            args = ["--base-settings", "baseline.rnqs", "--output-settings", "working.rnqs", "--profile", "00_BASELINE"]
            for overlay in case.overlays:
                args += ["--enable", overlay]
            setup = ("if (SettingsProfileGenerator.invoke(new String[]{" + ",".join(map(json.dumps, args))
                     + "}) != 0) throw new IllegalStateException(\"Settings generator failed\");\n"
                     + "try (FileInputStream in = new FileInputStream(\"working.rnqs\")) { s = Settings.readFromFileFormat(in); }\n"
                     + java_setters(effective(case, overlays)))
        blocks.append(f"static void case{i}() throws Exception {{ Settings s;\n" + setup + f'\nwrite(s, "{i}"); }}')
    return '''import com.uprfvx.random.Settings;
import com.uprfvx.random.cli.SettingsProfileGenerator;
import com.uprfvx.romio.MiscTweak;
import com.uprfvx.romio.RootPath;
import com.uprfvx.romio.gamedata.*;
import java.io.*;
import java.nio.file.*;
import java.lang.reflect.*;
import java.util.*;
class MatrixSettings {
''' + OBSERVE_JAVA + '''
  static Settings baseline() {
    Settings s = new Settings();
    // Reset every public boolean option, including unsafe implicit defaults.
    for (Method m : Settings.class.getMethods()) {
      if (m.getName().startsWith("set") && Arrays.equals(m.getParameterTypes(), new Class<?>[]{boolean.class})) {
        try { m.invoke(s, false); } catch (Exception e) { throw new IllegalStateException("Baseline API failure"); }
      }
    }
    s.setRomName("Pokemon Fire Red (U) 1.0");
    s.setCurrentRestrictions(new GenRestrictions(0x3FE));
    s.setSelectedEXPCurve(ExpCurve.MEDIUM_FAST);
    s.setWildPokemonZoneMod(Settings.WildPokemonZoneMod.ENCOUNTER_SET);
    return s;
  }
  static void write(Settings s, String id) throws Exception {
    if ((s.getPickupItemsMod() != Settings.PickupItemsMod.UNCHANGED
          && (!(''' + pickup_gate + ''') || s.getPickupItemsMod() != Settings.PickupItemsMod.RANDOM))
        || s.isMakeEvolutionsEasier()
        || (s.getCurrentMiscTweaks() & MiscTweak.REUSABLE_TMS.getValue()) != 0
        || (s.isPokemonPalettesFollowTypes() && s.isPokemonPalettesShinyFromNormal())
        || s.getEvolutionsMod() == Settings.EvolutionsMod.RANDOM_EVERY_LEVEL
        || s.isAllowMegaForms() || s.isAllowGigantamaxForms()
        || s.isIncludeMegaItems() || s.isIncludeZCrystalItems() || s.isIncludeDynamaxGmaxItems()) {
      throw new IllegalStateException("Pilot exclusion activated");
    }
    try (FileOutputStream out = new FileOutputStream(id + ".rnqs")) { s.writeToFileFormat(out); }
    try (FileInputStream in = new FileInputStream(id + ".rnqs")) {
      Settings restored = Settings.readFromFileFormat(in);
      if (!observe(s).equals(observe(restored))) {
        throw new IllegalStateException("Settings round-trip option drift");
      }
      // Canonicalize the effective serialized round-trip state, never intents.
      Files.writeString(Path.of(id + ".settings"), restored.toString());
      Files.writeString(Path.of(id + ".state"), observe(restored));
    }
  }
''' + "\n".join(blocks) + '''
  public static void main(String[] args) throws Exception {
    RootPath.path = new File(Settings.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent() + File.separator;
    try (FileOutputStream out = new FileOutputStream("baseline.rnqs")) { baseline().writeToFileFormat(out); }
''' + "\n".join(f"case{i}();" for i in range(len(cases))) + "\n  }\n}\n"


def prepare_tool(root, temp, jar=None, jar_source_commit=None, source=None):
    """USER execution only: attested external JAR, no build/copy/archive access."""
    if jar is None or jar_source_commit != CANDIDATES["UPR-FVX"]:
        raise MatrixError("A supplied prebuilt candidate JAR and exact user-attested source commit are required; no build performed.")
    if source is None or public_blob_id(source.encode("utf-8")) != PUBLIC_BLOBS[SOURCE]:
        raise MatrixError("Exact candidate source missing or stale; no JAR accessed.")
    jar = external_input_path(jar, root,
                              ("02_external", "04_private_roms", "05_builds", "03_tools/releases"))
    if not jar.is_file():
        raise MatrixError("Supplied candidate JAR is unavailable; no build performed.")
    response = command(["java", "-version"], temp)
    version = re.search(r'version "(\d+)', response.stderr + response.stdout)
    if response.returncode or not version or int(version[1]) < 25:
        raise MatrixError("Java 25 or newer is required by the candidate UPR source.")
    overlays, unsupported, _ = source_model(source)
    feature_response = command(["java", "--class-path", str(jar),
                                "com.uprfvx.random.cli.SettingsProfileGenerator", "--list-features"], temp)
    profile_response = command(["java", "--class-path", str(jar),
                                "com.uprfvx.random.cli.SettingsProfileGenerator", "--list-profiles"], temp)
    expected_features = [(name, "unsupported" if name in unsupported else "supported") for name in overlays]
    actual_features = [tuple(line.split("\t")[:2]) for line in feature_response.stdout.splitlines()]
    raw_profiles = []
    for name, body in re.findall(r'profiles\.put\("([^"]+)",\s*(.*?)\);', source, re.S):
        raw_profiles.append(name + "\t" + ",".join(re.findall(r'"([A-Z0-9_-]+)"', body)))
    if (feature_response.returncode or profile_response.returncode
            or ERROR_MARKERS.search(feature_response.stdout + feature_response.stderr)
            or ERROR_MARKERS.search(profile_response.stdout + profile_response.stderr)
            or actual_features != expected_features
            or profile_response.stdout.splitlines() != raw_profiles):
        raise MatrixError("Candidate source/JAR CLI catalogue mismatch; details discarded.")
    print("SOURCE_CHECK=PASS; JAR_PROVENANCE=USER_ATTESTED; CLI_CATALOGUE=PASS", flush=True)
    return jar


def generate_settings(cases, overlays, jar, temp):
    adapter = temp / "MatrixSettings.java"
    adapter.write_text(bridge_source(cases, overlays))
    result = command(["java", "--class-path", str(jar), str(adapter)], temp)
    if result.returncode:
        raise MatrixError("Pinned Settings API/profile generation failed before ROM use.")
    payloads = [(temp / f"{i}.settings").read_text() for i in range(len(cases))]
    verify_selected_payloads(cases, payloads)
    observations = {i: parse_observation((temp / f"{i}.state").read_text())
                    for i, case in enumerate(cases) if case.id in RISK_IDS}
    verify_risk_states(cases, overlays, observations, "Settings round-trip")
    return payloads


GEN_NORMALIZATION = "CFRU_DPE_GEN_RESTRICTIONS_NORMALIZED_BY_GEN3_VALIDITY"


NORMALIZER = '''import com.uprfvx.random.Settings;
import com.uprfvx.romio.RootPath;
import com.uprfvx.romio.romio.RomOpener;
import com.uprfvx.romio.romhandlers.Gen3RomHandler;
import java.io.*;
import java.nio.file.*;
class MatrixNormalize {
''' + OBSERVE_JAVA + '''
  public static void main(String[] args) throws Exception {
    RootPath.path = new File(Settings.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent() + File.separator;
    RomOpener.Results loaded = new RomOpener().openRomFile(new File(args[0]));
    if (!loaded.wasOpeningSuccessful() || !(loaded.getRomHandler() instanceof Gen3RomHandler)
        || !((Gen3RomHandler) loaded.getRomHandler()).usesCfruDpeRandomPoolPolicy()) {
      throw new IllegalStateException("Input is not a supported CFRU/DPE profile");
    }
    Gen3RomHandler handler = (Gen3RomHandler) loaded.getRomHandler();
    boolean policy = handler.usesCfruDpeRandomPoolPolicy();
    boolean valid = handler.isRomValid(null); // No CRC or diagnostic output.
    for (int i = 0; i < Integer.parseInt(args[1]); i++) {
      Settings s;
      try (FileInputStream in = new FileInputStream(i + ".rnqs")) { s = Settings.readFromFileFormat(in); }
      // Same public normalization as CliRandomizer.displaySettingsWarnings.
      // This may disable unavailable generic options, e.g. Gen5 MAINPLAYTHROUGH.
      boolean beforeLimit = s.isLimitPokemon();
      int beforeRestrictions = s.getCurrentRestrictions() == null ? -1 : s.getCurrentRestrictions().toInt();
      s.tweakForRom(handler);
      boolean afterLimit = s.isLimitPokemon();
      int afterRestrictions = s.getCurrentRestrictions() == null ? -1 : s.getCurrentRestrictions().toInt();
      // Record the actual pinned API transition per intent, never infer it from bytes.
      // Other generation masks are accounting only, not accepted C/I semantics.
      String adaptation = "NONE";
      if (policy && !valid && beforeLimit && beforeRestrictions >= 0
          && !afterLimit && s.getCurrentRestrictions() == null && afterRestrictions == -1) {
        adaptation = "CFRU_DPE_GEN_RESTRICTIONS_NORMALIZED_BY_GEN3_VALIDITY"
            + "\\ttrue\\t" + policy + "\\t" + valid + "\\t" + beforeLimit
            + "\\t" + beforeRestrictions + "\\t" + afterLimit + "\\t" + afterRestrictions;
      }
      Files.writeString(Path.of(i + ".normalization"), adaptation);
      try (FileOutputStream out = new FileOutputStream(i + ".rnqs")) { s.writeToFileFormat(out); }
      try (FileInputStream in = new FileInputStream(i + ".rnqs")) {
        Settings restored = Settings.readFromFileFormat(in);
        if (!observe(s).equals(observe(restored))) {
          throw new IllegalStateException("Normalized Settings round-trip drift");
        }
        Files.writeString(Path.of(i + ".settings"), restored.toString());
        Files.writeString(Path.of(i + ".post-state"), observe(restored));
      }
    }
  }
}
'''


def normalize_settings(cases, jar, rom, temp, before_payloads, overlays=None):
    """User runtime only: normalize with UPR's loader before exact deduplication."""
    adapter = temp / "MatrixNormalize.java"
    adapter.write_text(NORMALIZER)
    result = command(["java", "--class-path", str(jar), str(adapter), rom, str(len(cases))], temp)
    if result.returncode:
        raise MatrixError("UPR input recognition/Settings normalization failed; details discarded.")
    payloads = [(temp / f"{i}.settings").read_text() for i in range(len(cases))]
    adaptations = {}
    for i in range(len(cases)):
        witness = (temp / f"{i}.normalization").read_text()
        if witness != "NONE":
            adaptations[i] = parse_normalization_witness(witness)
    verify_selected_normalized_payloads(cases, before_payloads, payloads, adaptations)
    observations = {i: parse_observation((temp / f"{i}.post-state").read_text())
                    for i, case in enumerate(cases) if case.id in RISK_IDS}
    if observations and overlays is None:
        raise MatrixError("Candidate source model missing for normalization; STOP.")
    verify_risk_states(cases, overlays, observations, "target normalization")
    return payloads, adaptations


def parse_normalization_witness(witness):
    parts = witness.split("\t")
    # Fixed public schema: marker, Gen3, CFRU/DPE policy, validity, before
    # limit/mask, after limit/mask. Never propagate untrusted adapter output.
    if (len(parts) != 8 or parts[0] != GEN_NORMALIZATION
            or parts[1:5] != ["true", "true", "false", "true"]
            or parts[6:] != ["false", "-1"]
            or not re.fullmatch(r"[0-9]{1,10}", parts[5])):
        raise MatrixError("Unconfirmed target normalization; STOP.")
    return int(parts[5])


def verify_selected_normalized_payloads(cases, before_payloads, payloads, adaptations):
    """CONTROL #681: only the witnessed Gen3 restriction delta is allowed for C/I.

    CONTROL disposition applies only to C/I full NatDex on this pinned target:
    its modeled Gen1-9 universe needs no additional later-generation exclusion.
    Other Gen-limit intents receive accounting, not this semantic acceptance.
    Pre-ROM identity is independent and stays exact. For C/I, compare every
    serialized byte, including inactive fields and metadata, allowing only the
    two specified fields and their derived Settings checksum. No ROM checksum
    is calculated, retained or reported.
    """
    if len(cases) != len(before_payloads) or len(cases) != len(payloads):
        raise MatrixError("Incomplete normalization accounting; STOP.")
    verify_selected_payloads(cases, before_payloads)
    for i, (case, before, after) in enumerate(zip(cases, before_payloads, payloads)):
        original, effective = settings_data(before), settings_data(after)
        before_mask = int.from_bytes(original[30:34], "little", signed=True)
        after_mask = int.from_bytes(effective[30:34], "little", signed=True)
        before_limit, after_limit = bool(original[65] & 8), bool(effective[65] & 8)
        witnessed = i in adaptations
        if witnessed and (adaptations[i] != before_mask or not before_limit
                          or after_limit or after_mask != -1):
            raise MatrixError("Target normalization witness/Settings mismatch; STOP.")
        if before_limit and not after_limit and after_mask == -1 and not witnessed:
            raise MatrixError("Unconfirmed target normalization; STOP.")
        if selected_name(case) not in ("CASUAL_NATDEX", "IRONMON_NATDEX"):
            continue
        expected = bytearray(original)
        if witnessed:
            if before_mask != 0x3FE:
                raise MatrixError("Selected profile normalization outside CONTROL disposition; STOP.")
            expected[30:34] = b"\xff" * 4
            expected[65] &= ~8
            expected[-8:-4] = zlib.crc32(expected[:-8]).to_bytes(4, "big")
        if effective != expected:
            raise MatrixError("Selected profile post-normalization Settings drift; STOP.")


def settings_data(payload):
    if payload[:3] != "422":
        raise MatrixError("Unexpected pinned Settings version.")
    try:
        data = base64.b64decode(payload[3:], validate=True)
    except ValueError:
        raise MatrixError("Invalid Settings canonical payload.") from None
    if len(data) < 76:
        raise MatrixError("Truncated Settings canonical payload.")
    return data


def verify_selected_payloads(cases, payloads):
    # This inspects only public settings, never ROM data or ROM hashes.
    accepted = settings_data(IRONMON)
    for case, payload in zip(cases, payloads):
        name = selected_name(case)
        data = settings_data(payload)
        if name == "IRONMON_NATDEX" and data[:-4] != accepted[:-4]:
            raise MatrixError("Accepted IRONMON_NATDEX Settings identity mismatch; STOP.")
        if name == "CASUAL_NATDEX":
            # Exact #676 semantics across all serialized setting bytes, including
            # inactive defaults. Expected fixture is source-derived, not a patcher.
            if data[:67] != CASUAL_BYTES:
                raise MatrixError("CASUAL_NATDEX field-by-field Settings mismatch; STOP.")


# Source-derived expected serialization only for verification, never Settings
# production. Every byte is reviewed against Settings.toString at the pin.
CASUAL_BYTES = bytes.fromhex(
    "00 08 04 01 42 00 00 00 00 00 00 04 00 02 e4 04 00 11 00 44 4c 00 00 4c 00 01 09 00 62 98 "
    "fe 03 00 00 00 00 00 08 e4 09 e4 f1 00 08 09 e4 00 00 00 e4 00 02 00 41 00 01 01 00 00 00 00 00 09 00 10 08 28"
)


@dataclass
class Group:
    payload: str
    settings: Path
    aliases: list


def deduplicate(cases, payloads, temp):
    groups = {}
    for i, (case, payload) in enumerate(zip(cases, payloads)):
        # Exact equality of full UPR canonical strings. Distinct settings can
        # never be collapsed by a hash collision or by ignoring inactive fields.
        groups.setdefault(payload, Group(payload, temp / f"{i}.rnqs", [])).aliases.append(case)
    return list(groups.values())


ERROR_MARKERS = re.compile(r"Exception|\bERROR\b|\bFATAL\b|Randomization failed|Could not load|Could not save", re.I)
ERROR_CLASSES = ("RandomizationException", "RomIOException", "IllegalArgumentException",
                 "IllegalStateException", "IndexOutOfBoundsException", "NullPointerException",
                 "IOException", "UnsupportedOperationException")


def safe_error(text, fallback):
    # Allowlisted summaries only. Regex-only path removal cannot reliably scrub
    # arbitrary filenames, relative paths, secrets or multiline exception text.
    for cls in ERROR_CLASSES:
        if cls in text:
            if "unmodeled slots or metadata" in text:
                return cls, "CFRU/DPE evolution save preflight rejected an unmodeled row."
            if "Pickup randomization is unsupported" in text:
                return cls, "CFRU/DPE Pickup randomization is unsupported."
            return cls, "UPR reported an exception; raw details discarded."
    return fallback, "UPR step failed; raw details discarded."


@dataclass
class Outcome:
    generate: str = "NOT_RUN"
    reopen: str = "NOT_RUN"
    replay: str = "NOT_APPLICABLE"
    error_class: str = "none"
    message: str = "none"
    reproduced: str = "NOT_APPLICABLE"
    retry: str = "NOT_RUN"
    input_unchanged: str = "NOT_RUN"

    @property
    def passed(self):
        return (self.generate == self.reopen == self.input_unchanged == "PASS"
                and self.replay in ("PASS", "NOT_APPLICABLE"))


def input_digest(path):
    """USER-local transient comparison only; never retain or print this value."""
    digest = hashlib.sha256()
    try:
        with Path(path).open("rb") as source:
            for block in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(block)
        return digest.digest()
    except OSError:
        raise MatrixError("Input unchanged check unavailable; details discarded.") from None


def same_bytes(a, b):
    with a.open("rb") as left, b.open("rb") as right:
        while True:
            x, y = left.read(1024 * 1024), right.read(1024 * 1024)
            if x != y:
                return False
            if not x:
                return True


REOPEN_IDENTITY = '''import com.uprfvx.random.Settings;
import com.uprfvx.romio.RootPath;
import com.uprfvx.romio.romio.RomOpener;
import com.uprfvx.romio.romhandlers.Gen3RomHandler;
import java.io.File;
class MatrixReopen {
  public static void main(String[] args) {
    try {
      RootPath.path = new File(Settings.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent() + File.separator;
      RomOpener.Results loaded = new RomOpener().openRomFile(new File(args[0]));
      if (!loaded.wasOpeningSuccessful() || !(loaded.getRomHandler() instanceof Gen3RomHandler)
          || !((Gen3RomHandler) loaded.getRomHandler()).usesCfruDpeRandomPoolPolicy()) {
        System.exit(1);
        return;
      }
      System.out.println("Supported CFRU/DPE output identity verified.");
    } catch (Exception ignored) {
      // Never expose a private filename, loader exception or stacktrace.
      System.exit(1);
    }
  }
}
'''


def attempt(group, seed, rom, jar, temp, replay):
    out = Outcome()
    original_input = input_digest(rom)
    with tempfile.TemporaryDirectory(prefix="case-", dir=temp) as case_dir:
        directory = Path(case_dir)

        def run_one(filename):
            output = directory / filename
            if input_digest(rom) != original_input:
                raise MatrixError("Input unchanged check failed before generation; STOP.")
            try:
                result = command(["java", "-jar", str(jar), "cli", "-i", rom, "-o", str(output),
                                  "-s", str(group.settings), "-z", str(seed)], directory)
            finally:
                if input_digest(rom) != original_input:
                    raise MatrixError("Input unchanged check failed during generation; no replay permitted.")
            text = result.stdout + result.stderr
            if result.returncode or "Randomized successfully!" not in text or ERROR_MARKERS.search(text) or not output.is_file() or output.stat().st_size == 0:
                out.error_class, out.message = safe_error(text, "GenerationFailure")
                return None, "FAIL", "NOT_RUN"
            result = command(["java", "--class-path", str(jar), str(identity_adapter), str(output)], directory)
            text = result.stdout + result.stderr
            if result.returncode or ERROR_MARKERS.search(text) or "Supported CFRU/DPE output identity verified." not in text:
                out.error_class = "ReopenIdentityFailure"
                out.message = "Output was not recognized as the supported CFRU/DPE profile."
                return None, "PASS", "FAIL"
            result = command(["java", "-jar", str(jar), "loaded-manifest", "-i", str(output),
                              "-o", str(directory / (filename + "-manifest"))], directory)
            text = result.stdout + result.stderr
            if result.returncode or ERROR_MARKERS.search(text) or "Wrote sanitized loaded manifests." not in text:
                out.error_class, out.message = safe_error(text, "ReopenFailure")
                return None, "PASS", "FAIL"
            return output, "PASS", "PASS"

        try:
            identity_adapter = directory / "MatrixReopen.java"
            identity_adapter.write_text(REOPEN_IDENTITY)
            output, out.generate, out.reopen = run_one("output.gba")
            if output and replay:
                repeated, generated, reopened = run_one("replay.gba")
                out.replay = "PASS" if repeated and same_bytes(output, repeated) else "FAIL"
                if out.replay == "FAIL" and out.error_class == "none":
                    out.error_class, out.message = "ReplayMismatch", "Same settings and seed produced different bytes."
                if generated == "PASS" and reopened == "FAIL":
                    out.reopen = "FAIL"
        except InterruptedError:
            raise
        except (OSError, subprocess.SubprocessError):
            out.error_class, out.message = "ProcessFailure", "Local subprocess or file operation failed; details discarded."
        finally:
            try:
                out.input_unchanged = "PASS" if input_digest(rom) == original_input else "FAIL"
            except MatrixError:
                out.input_unchanged = "FAIL"
            if out.input_unchanged == "FAIL":
                out.error_class, out.message = "InputChanged", "Input unchanged check failed; STOP."
        # TemporaryDirectory removes outputs, raw sidecars and manifests even
        # after exceptions. Each independent retry creates a fresh directory.
    return out


def run_case(group, seed, rom, jar, temp):
    replay = any(c.replay for c in group.aliases)
    first = attempt(group, seed, rom, jar, temp, replay)
    if first.input_unchanged == "FAIL":
        raise MatrixError("Input unchanged check failed; no retry or further generation permitted.")
    if not first.passed:
        second = attempt(group, seed, rom, jar, temp, replay)
        if second.input_unchanged == "FAIL":
            raise MatrixError("Input unchanged check failed during retry; STOP.")
        same_failure = (first.generate, first.reopen, first.replay, first.error_class) == (second.generate, second.reopen, second.replay, second.error_class)
        first.reproduced = "FAIL" if second.passed else "PASS" if same_failure else "DIFFERENT_FAILURE"
        first.retry = "PASS" if second.passed else "FAIL"
        # A transient first failure remains a failure, never laundered to PASS.
    return first


def diagnostic_status(out):
    if out.passed:
        return "GENERATION_PASS_WITH_KNOWN_SEMANTIC_LIMITATION"
    if out.generate == "FAIL" and out.error_class in ERROR_CLASSES:
        return "EXPECTED_FAIL"
    return "DIAGNOSTIC_FAIL"


def progress_outcome(group, out):
    diagnostic = all(c.classification == "DIAGNOSTIC" for c in group.aliases)
    print(diagnostic_status(out) if diagnostic else "PASS" if out.passed else "FAIL", flush=True)
    if out.retry != "NOT_RUN":
        print("          retry same seed ..................... " + out.retry, flush=True)
        print("          " + out.error_class + ": " + out.message, flush=True)


def print_report(cases, groups, records, counts, result, normalized=(), adaptations=()):
    required = [(g, seed, out) for g, seed, out in records
                if any(c.classification != "DIAGNOSTIC" for c in g.aliases)]
    failed = [record for record in required if not record[2].passed]
    diagnostics = [record for record in records if record not in required]
    print("\nMatrix basis:\nWorkspace: " + WORKSPACE)
    print("Candidate source revisions (separate from baseline Gitlinks):")
    for name, pin in CANDIDATES.items():
        print(name + ": " + pin)
    print("LOG_CONTENT=NOT_RUN; MANIFEST_SEMANTICS=NOT_RUN; GAMEPLAY=NOT_RUN")
    print("Reopen scope: supported profile load and manifest export, not runtime acceptance.")
    print_inventory(counts)
    print(f"\nCASE_INTENTS: {len(cases)}\nUNIQUE_EFFECTIVE_CASES: {len(groups)}")
    print(f"UPR_NORMALIZED_CASE_INTENTS: {len(normalized)}")
    if normalized:
        print("UPR normalized case intents: " + ", ".join(normalized))
    if adaptations:
        print("UPR target-normalized adaptations: " + GEN_NORMALIZATION)
        print(f"Gen-limit intents normalized by target: {len(adaptations)}")
        print("Gen-limit coverage: intent aliases retained; effective Gen-limit execution not claimed.")
    print(f"Cases run: {len(records)}\nPASS: {len(required) - len(failed)}\nFAIL: {len(failed)}")
    print(f"EXPECTED_FAIL / diagnostic: {sum(diagnostic_status(r[2]) == 'EXPECTED_FAIL' for r in diagnostics)} / {len(diagnostics)}")
    for group, _, out in diagnostics:
        print("Diagnostic " + group.aliases[0].id + ": " + diagnostic_status(out))
    if diagnostics:
        print("Sensible Held Items: optional, selected C/I OFF; generation does not accept heuristic/runtime semantics.")
    planned = len(groups) + 3 * sum(any(c.secondary for c in g.aliases) for g in groups)
    print(f"SKIP / excluded: {max(0, planned - len(records))} / {counts['GENERATOR_UNSUPPORTED'] + counts['TARGET_EXCLUDED']}")
    print("\nFirst failure:")
    if failed:
        group, seed, out = failed[0]
        case = next(c for c in group.aliases if c.classification != "DIAGNOSTIC")
        classification = "ACCEPTANCE" if any(c.classification == "ACCEPTANCE" for c in group.aliases) else "STRESS_ONLY"
        print("Case ID: " + case.id + "\nClassification: " + classification)
        overlay_ids = tuple(dict.fromkeys(itertools.chain.from_iterable(c.overlays for c in group.aliases)))
        print("Profiles/overlays: " + ", ".join(c.id for c in group.aliases))
        if overlay_ids:
            print("Overlay IDs: " + ", ".join(overlay_ids))
        print(f"Generate: {out.generate}\nReopen: {out.reopen}\nReplay: {out.replay}\nInput unchanged: {out.input_unchanged}\nReproduced: {out.reproduced}")
        print("Error class: " + out.error_class + "\nSanitized message: " + out.message)
    else:
        print("none")
    print("\nSelected profile results:")
    for name in SELECTED + MAXIMUM + tuple(RISK_SINGLES) + (RISK_EVOLUTION, RISK_PICKUP):
        outcomes = [out for group, _, out in records if any(selected_name(c) == name for c in group.aliases)]
        status = "NOT_RUN" if not outcomes else "PASS" if all(o.passed for o in outcomes) else "FAIL"
        print(name + ": " + status)
    # Coverage aliases are public and retained through reporting, not lost on
    # compaction. No settings payload, paths, logs or binary hashes are printed.
    print("\nCoverage aliases:")
    for group in groups:
        if len(group.aliases) > 1:
            print(" + ".join(c.id for c in group.aliases))
    print("\nResult: " + result)


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(2, "Invalid arguments; use --help. Argument values are suppressed.\n")


def main(argv=None):
    parser = SafeParser(description="User-owned #727 candidate UPR generation matrix")
    parser.add_argument("--rom", metavar="PATH")
    parser.add_argument("--jar", metavar="PATH", help="User-supplied external prebuilt #217 JAR; never auto-build")
    parser.add_argument("--jar-source-commit", metavar="COMMIT", help="Independent user attestation of the supplied JAR source commit")
    parser.add_argument("--public-source-file", metavar="PUBLIC_JAVA", help="Optional exact public-commit SettingsProfileGenerator.java; default is immutable GitHub GET")
    parser.add_argument("--dry-run", action="store_true", help="Public source plan only; no Java/JAR/ROM use")
    parser.add_argument("--stop-on-fail", action="store_true")
    args = parser.parse_args(argv)
    records = []
    try:
        verify_pins(ROOT)
        source = read_public_source(local_file=args.public_source_file)
        overlays, unsupported, profiles = source_model(source)
        cases = build_matrix(overlays, unsupported, profiles)
        if args.dry_run:
            print("Matrix basis:\nWorkspace: " + WORKSPACE + "\nTree: " + TREE)
            for name, pin in CANDIDATES.items():
                print(name + ": " + pin)
            print(f"CASE_INTENTS: {len(cases)}\nUNIQUE_EFFECTIVE_CASES: runtime Settings API canonicalization required")
            print_inventory(inventory_counts(overlays, unsupported))
            for case in cases:
                print(case.layer + " " + case.id)
            print("PRIVATE_ROM_MATRIX = NOT_RUN")
            return 0
        with tempfile.TemporaryDirectory(prefix="upr-generation-matrix-") as workspace:
            temp = Path(workspace)
            jar = prepare_tool(ROOT, temp, args.jar, args.jar_source_commit, source)
            payloads = generate_settings(cases, overlays, jar, temp)
            # Pre-ROM Settings failures, including accepted identity drift, stop
            # before prompting or stat/open of even a supplied --rom argument.
            rom = args.rom if args.rom is not None else input("Private ROM: ")
            if not rom:
                raise MatrixError("Private input was not supplied.")
            original_input = input_digest(rom)
            try:
                effective_payloads, adaptations = normalize_settings(cases, jar, rom, temp, payloads, overlays)
                normalized = [case.id for case, before, after in zip(cases, payloads, effective_payloads)
                              if before != after]
                groups = deduplicate(cases, effective_payloads, temp)
                print(f"CASE_INTENTS: {len(cases)}\nUNIQUE_EFFECTIVE_CASES: {len(groups)}", flush=True)
                primary_ok = True
                for i, group in enumerate(groups, 1):
                    case = group.aliases[0]
                    print(f"[{i:03}/{len(groups):03}] {case.layer} {case.id} ... ", end="", flush=True)
                    out = run_case(group, PRIMARY, rom, jar, temp)
                    records.append((group, PRIMARY, out))
                    progress_outcome(group, out)
                    if not out.passed and any(c.classification != "DIAGNOSTIC" for c in group.aliases):
                        primary_ok = False
                        if args.stop_on_fail:
                            break
                if primary_ok:
                    sweep = [g for g in groups if any(c.secondary for c in g.aliases)]
                    for group in sweep:
                        for seed in SECONDARY:
                            # PRIMARY is already covered with replay; retain seed
                            # coverage by reference instead of repeating execution.
                            if seed == PRIMARY:
                                continue
                            print(f"FIXED_SEED_SWEEP {group.aliases[0].id} ... ", end="", flush=True)
                            out = run_case(group, seed, rom, jar, temp)
                            records.append((group, seed, out))
                            progress_outcome(group, out)
                            if args.stop_on_fail and not out.passed:
                                break
                        if args.stop_on_fail and not records[-1][2].passed:
                            break
                required_ok = all(out.passed for group, _, out in records
                                  if any(c.classification != "DIAGNOSTIC" for c in group.aliases))
                # Optional heuristic diagnostics never establish or block required PASS.
                result = "R2_RANDOMIZER_GENERATION_MATRIX_PASS" if required_ok else "R2_RANDOMIZER_GENERATION_MATRIX_FAIL"
                print_report(cases, groups, records, inventory_counts(overlays, unsupported), result, normalized, adaptations)
                return 0 if required_ok else 1
            finally:
                if input_digest(rom) != original_input:
                    raise MatrixError("Input unchanged check failed; STOP.")
    except MatrixError as exc:
        print("Result: STOP\nSanitized message: " + str(exc))
    except (KeyboardInterrupt, InterruptedError):
        print("Result: INTERRUPTED; temporary artifacts cleaned.")
    except (OSError, subprocess.SubprocessError, ValueError, EOFError):
        print("Result: STOP\nSanitized message: Local prerequisite or input failed; details discarded.")
    return 1


if __name__ == "__main__":
    def interrupted(signum, frame):
        raise InterruptedError("Interrupted")
    signal.signal(signal.SIGTERM, interrupted)
    sys.exit(main())
