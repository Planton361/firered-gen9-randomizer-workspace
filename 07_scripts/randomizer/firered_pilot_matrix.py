#!/usr/bin/env python3
"""#743/#748/#750: USER-ONLY CFRU/DPE Gen 9 pilot, single-option and comprehensive matrix.

Composes UPR-FVX's existing settings-profile, cli and loaded-manifest commands
for the eleven pilot cases. The user supplies one neutral .rnqs saved once from
the GUI; its effective state is read through the public Settings API (a
temporary read-only Java adapter, because UPR has no settings-dump command)
before any overlay is applied. No settings bytes are written or patched here.

Modes: --plan (prints cases, the feature inventory and the #750 case plan;
reads no ROM, JAR or .rnqs), --self-test (synthetic mocks only), --matrix (the
eleven pilot cases), --single --select IDS (#748 single options) and --suite
(#750 comprehensive matrix, one bounded batch selected by --kind/--family/
--risk/--case). Every real mode requires --confirm USER_LOCAL_RUN. Output stays on the user's machine; the printed table contains
categories only.
"""

import argparse
import hashlib
import itertools
import os
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import upr_generation_matrix as gm
from upr_generation_matrix import MatrixError, command


ROOT = gm.ROOT
DEFAULT_JAR = ROOT / gm.LOCAL_JAR
CONFIRM_TOKEN = "USER_LOCAL_RUN"
# Public pilot candidate; the ROM's CFRU/DPE build cannot be verified from here.
PILOT = {
    "CFRU": ("02_external/CFRU-expansion", "196058edbc2b8b7d8c725b715b1f967ba60f5c83"),
    "DPE": ("02_external/Dynamic-Pokemon-Expansion-Gen-9", "d887185de1f6ae6a78e85c4311bbadde17041d00"),
    "UPR-FVX": ("02_external/upr-fvx", "1a9b59db3f49b6702b56cf76409de911cce9806e"),
}
# Outputs are ROMs: never inside the tracked tree, only in ignored local folders.
ALLOWED_OUTPUT_ROOTS = ("04_private_roms", "05_builds")

STARTER, WILD, TRAINER = "FVX-SST-002", "FVX-WILD-001", "FVX-FOE-001"
MOVESETS, REORDER = "FVX-MOVE-007", "FVX-MOVE-009"
# Exact Settings getter changes each settings-profile overlay must produce.
OVERLAY_EFFECT = {
    STARTER: {"getStartersMod": "COMPLETELY_RANDOM"},
    WILD: {"isRandomizeWildPokemon": "true"},
    TRAINER: {"getTrainersMod": "RANDOM"},
    MOVESETS: {"getMovesetsMod": "COMPLETELY_RANDOM"},
    REORDER: {"isReorderDamagingMoves": "true"},
}


@dataclass(frozen=True)
class SingleOption:
    """#748: one executable settings-profile overlay outside the #743 families.

    `source` is the overlay's exact lambda in SettingsProfileGenerator and
    `effect` the Settings getter change it must produce. Add an option by
    adding an entry; the run, checks and report are shared.
    """
    id: str
    feature: str
    family: str
    title: str
    effect: dict
    seed: int
    source: str


# None of these setters is touched by Settings.tweakForRom; --single still
# observes the target-normalized settings before generating anything.
SINGLE_OPTIONS = (
    SingleOption("S01", "FVX-TRAIT-001", "Traits", "Base stats random", {"getBaseStatisticsMod": "RANDOM"},
                 748001, "s -> s.setBaseStatisticsMod(Settings.BaseStatisticsMod.RANDOM)"),
    SingleOption("S02", "FVX-TM-001", "TM/Tutor", "TM moves random", {"getTmsMod": "RANDOM"},
                 748002, "s -> s.setTmsMod(Settings.TMsMod.RANDOM)"),
    SingleOption("S03", "FVX-TM-005", "TM/Tutor", "TM/HM compat random",
                 {"getTmsHmsCompatibilityMod": "COMPLETELY_RANDOM"}, 748003,
                 "s -> s.setTmsHmsCompatibilityMod(Settings.TMsHMsCompatibilityMod.COMPLETELY_RANDOM)"),
    SingleOption("S04", "FVX-ITEM-002", "Items", "Field items random", {"getFieldItemsMod": "RANDOM"},
                 748004, "s -> s.setFieldItemsMod(Settings.FieldItemsMod.RANDOM)"),
    SingleOption("S05", "FVX-TYPE-001", "Types", "Type chart random balanced",
                 {"getTypeEffectivenessMod": "RANDOM_BALANCED"}, 748005,
                 "s -> s.setTypeEffectivenessMod(Settings.TypeEffectivenessMod.RANDOM_BALANCED)"),
)
OVERLAY_EFFECT.update({o.feature: o.effect for o in SINGLE_OPTIONS})

# Source-cited CFRU/DPE refusals at the pilot UPR revision.
GUARDED = {
    MOVESETS: "GameRandomizer learnset guard (--matrix M08)",
    REORDER: "GameRandomizer learnset guard (--matrix M09)",
    "FVX-TRAIT-017": "EvolutionRandomizer RANDOM_EVERY_LEVEL guard",
}
GUARD_SOURCES = {
    "random/src/main/java/com/uprfvx/random/GameRandomizer.java": "CFRU/DPE level-up learnset changes are unavailable",
    "random/src/main/java/com/uprfvx/random/randomizers/EvolutionRandomizer.java":
        "CFRU/DPE RANDOM_EVERY_LEVEL is unsupported",
}
UPR_SOURCE = "02_external/upr-fvx"
CATALOG_SOURCE = "random/src/main/java/com/uprfvx/random/cli/SettingsProfileGenerator.java"
SETTINGS_SOURCE = "random/src/main/java/com/uprfvx/random/Settings.java"
LEDGER = "08_tests/randomizer/fvx_feature_test_status_matrix.tsv"
DISPOSITIONS = ("RUNNABLE", "GUARDED", "UNSUPPORTED", "NEEDS_REVIEW", "NOT_RUN")
LEARNSET_GUARD = ("RandomizationException: CFRU/DPE level-up learnset changes are unavailable: "
                  "select Unchanged, disable Reorder Damaging Moves, and do not use Metronome Only.")


@dataclass(frozen=True)
class Case:
    id: str
    title: str
    overlays: tuple
    seed: int
    expect: str = "PASS"          # PASS or EXPECTED_REJECTION
    replay_of: str = ""
    guard: str = ""               # exact rejection text; default: the learnset guard


CASES = (
    Case("M00", "Starter/Wild/Trainer OFF", (), 743000),
    Case("M01", "Starter", (STARTER,), 743001),
    Case("M02", "Wild", (WILD,), 743002),
    Case("M03", "Trainer", (TRAINER,), 743003),
    Case("M04", "Starter + Wild", (STARTER, WILD), 743004),
    Case("M05", "Starter + Trainer", (STARTER, TRAINER), 743005),
    Case("M06", "Wild + Trainer", (WILD, TRAINER), 743006),
    Case("M07", "Starter + Wild + Trainer", (STARTER, WILD, TRAINER), 743007),
    Case("M08", "Movesets Randomized", (MOVESETS,), 743008, "EXPECTED_REJECTION"),
    Case("M09", "Reorder Damaging Moves", (REORDER,), 743009, "EXPECTED_REJECTION"),
    Case("M10", "Replay of M07", (STARTER, WILD, TRAINER), 743007, replay_of="M07"),
)

# Neutral baseline: every other randomizer/updater/tweak owner off. Sub-options
# without an owner are free but must stay identical in every generated case.
UNCHANGED_MODS = (
    "getAbilitiesMod", "getAllyPokemonMod", "getAuraMod", "getBaseStatisticsMod", "getEvolutionsMod",
    "getFieldItemsMod", "getInGameTradesMod", "getMoveTutorMovesMod", "getMoveTutorsCompatibilityMod",
    "getMovesetsMod", "getPickupItemsMod", "getPokemonPalettesMod", "getShopItemsMod",
    "getSpeciesTypesMod", "getStartersMod", "getStaticPokemonMod", "getTmsHmsCompatibilityMod",
    "getTmsMod", "getTotemPokemonMod", "getTrainersMod", "getTypeEffectivenessMod",
)
FALSE_FLAGS = (
    "isAllowGigantamaxForms", "isAllowMegaForms", "isBetterBossTrainerMovesets",
    "isBetterImportantTrainerMovesets", "isBetterRegularTrainerMovesets", "isChangeImpossibleEvolutions",
    "isEvolutionMovesForAll", "isFullHMCompat", "isIncludeDynamaxGmaxItems", "isIncludeMegaItems",
    "isIncludeZCrystalItems", "isLimitPokemon", "isMakeEvolutionsEasier", "isPokemonPalettesFollowEvolutions",
    "isPokemonPalettesFollowTypes", "isPokemonPalettesShinyFromNormal", "isRaceMode",
    "isRandomizeHeldItemsForBossTrainerPokemon", "isRandomizeHeldItemsForImportantTrainerPokemon",
    "isRandomizeHeldItemsForRegularTrainerPokemon", "isRandomizeInGameTradesIVs",
    "isRandomizeInGameTradesItems", "isRandomizeInGameTradesNicknames", "isRandomizeInGameTradesOTs",
    "isRandomizeIntroMon", "isRandomizeMoveAccuracies", "isRandomizeMoveCategory", "isRandomizeMoveNames",
    "isRandomizeMovePPs", "isRandomizeMovePowers", "isRandomizeMoveTypes", "isRandomizeStartersHeldItems",
    "isRandomizeTotemHeldItems", "isRandomizeTrainerClassNames", "isRandomizeTrainerClassSprites",
    "isRandomizeTrainerNames", "isRandomizeWildPokemon", "isRandomizeWildPokemonHeldItems",
    "isRemoveTimeBasedEvolutions", "isReorderDamagingMoves", "isRivalCarriesStarterThroughout",
    "isShinyChance", "isStandardizeEXPCurves", "isStaticLevelModified", "isTotemLevelsModified",
    "isTrainersEvolveTheirPokemon", "isTrainersLevelModified", "isUpdateBaseStats", "isUpdateMoves",
    "isUpdateMovesLegacy", "isUpdateTypeEffectiveness", "isUpdatedFromOldVersion", "isUseMinimumCatchRate",
    "isWildLevelsModified",
)
ZERO_VALUES = (
    "getAdditionalBossTrainerPokemon", "getAdditionalImportantTrainerPokemon",
    "getAdditionalRegularTrainerPokemon", "getCurrentMiscTweaks", "getEliteFourUniquePokemonNumber",
)
NEUTRAL = {**{k: "UNCHANGED" for k in UNCHANGED_MODS}, **{k: "false" for k in FALSE_FLAGS},
           **{k: "0" for k in ZERO_VALUES}, "getBattleStyle": "UNCHANGED"}

# Read-only: every public Settings getter of a checkable type, in name order.
# Unknown types print UNSUPPORTED so the runner fails closed instead of guessing.
OBSERVE_JAVA = r'''import com.uprfvx.random.Settings;
import com.uprfvx.romio.RootPath;
import com.uprfvx.romio.gamedata.BattleStyle;
import com.uprfvx.romio.gamedata.GenRestrictions;
import com.uprfvx.romio.romhandlers.Gen3RomHandler;
import com.uprfvx.romio.romhandlers.RomHandler;
import com.uprfvx.romio.romio.RomOpener;
import java.io.File;
import java.io.FileInputStream;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.util.*;
class PilotSettingsObserve {
  static final Set<String> SKIP = Set.of("getRomName", "getCustomNames", "getCustomStarters");
  public static void main(String[] args) {
    try {
      int first = 0;
      RomHandler target = null;
      if (args.length > 1 && args[0].equals("--rom")) {
        // Optional: apply the same tweakForRom normalization the CLI applies before randomizing.
        RootPath.path = new File(Settings.class.getProtectionDomain().getCodeSource().getLocation().toURI()).getParent() + File.separator;
        RomOpener.Results loaded = new RomOpener().openRomFile(new File(args[1]));
        if (!loaded.wasOpeningSuccessful() || !(loaded.getRomHandler() instanceof Gen3RomHandler g)
            || !g.usesCfruDpeRandomPoolPolicy()) {
          System.exit(4);
          return;
        }
        target = g;
        first = 2;
      }
      List<Method> methods = new ArrayList<>(Arrays.asList(Settings.class.getMethods()));
      methods.sort(Comparator.comparing(Method::getName));
      for (String path : Arrays.copyOfRange(args, first, args.length)) {
        Settings s;
        try (FileInputStream in = new FileInputStream(path)) { s = Settings.readFromFileFormat(in); }
        if (target != null) s.tweakForRom(target);
        System.out.println("BEGIN");
        for (Method m : methods) {
          String n = m.getName();
          if (m.getParameterCount() != 0 || m.getDeclaringClass() != Settings.class
              || Modifier.isStatic(m.getModifiers()) || SKIP.contains(n)
              || !(n.startsWith("is") || n.startsWith("get") || n.startsWith("use"))) continue;
          Object v = m.invoke(s);
          String text;
          if (v == null) text = "null";
          else if (v instanceof Boolean || v instanceof Integer) text = v.toString();
          else if (v instanceof Enum<?> e) text = e.name();
          else if (v instanceof GenRestrictions g) text = Integer.toString(g.toInt());
          else if (v instanceof BattleStyle b) text = b.getModification().name();
          else text = "UNSUPPORTED";
          System.out.println(n + "=" + text);
        }
        System.out.println("END");
      }
    } catch (Exception ignored) {
      System.exit(3);  // Never expose a private path or exception text.
    }
  }
}
'''
VALUE = re.compile(r"true|false|null|-?[0-9]{1,10}|[A-Z][A-Z0-9_]{0,63}")


def parse_observations(text, count):
    blocks, current = [], None
    for line in text.splitlines():
        if line == "BEGIN" and current is None:
            current = {}
        elif line == "END" and current is not None:
            blocks.append(current)
            current = None
        else:
            key, sep, value = line.partition("=")
            if (current is None or not sep or not re.fullmatch(r"(is|get|use)[A-Za-z0-9]+", key)
                    or key in current or not VALUE.fullmatch(value)):
                raise MatrixError("Settings observation schema mismatch; details discarded.")
            current[key] = value
    if current is not None or len(blocks) != count:
        raise MatrixError("Settings observation incomplete; STOP.")
    return blocks


def observe(jar, temp, paths, rom=None):
    """Effective settings per file; with `rom`, after the CLI's tweakForRom for that ROM."""
    adapter = temp / "PilotSettingsObserve.java"
    adapter.write_text(OBSERVE_JAVA)
    target = ["--rom", str(rom)] if rom else []
    result = command(["java", "--class-path", str(jar), str(adapter), *target, *map(str, paths)], temp)
    if rom and result.returncode == 4:
        raise MatrixError("Source ROM cannot be opened as CFRU/DPE for target normalization; STOP.")
    if result.returncode:
        raise MatrixError("Effective settings cannot be inspected through the Settings API; STOP.")
    return parse_observations(result.stdout, len(paths))


def check_baseline(state):
    """The baseline must be inspectable and neutral before any overlay is applied."""
    if any(value == "UNSUPPORTED" for value in state.values()):
        raise MatrixError("Baseline contains settings this runner cannot inspect; STOP.")
    missing = [key for key in NEUTRAL if key not in state]
    if missing:
        raise MatrixError(f"Baseline inspection lacks {len(missing)} required settings; STOP.")
    drift = sorted(key for key, value in NEUTRAL.items() if state[key] != value)
    if drift:
        raise MatrixError("Baseline is not neutral: " + ", ".join(drift) + "; save a neutral .rnqs.")


def expected_state(baseline, case):
    state = dict(baseline)
    for overlay in case.overlays:
        state.update(OVERLAY_EFFECT[overlay])
    return state


def check_case_settings(baseline, case, state):
    if state != expected_state(baseline, case):
        raise MatrixError(case.id + ": settings-profile output differs from baseline + overlays; STOP.")


def plan_lines():
    lines = ["#743 pilot settings matrix (USER-ONLY; --plan reads no ROM, JAR or .rnqs)", ""]
    lines.append(f"{'ID':<4} {'Case':<26} {'Overlays':<38} {'Seed':<7} Expected")
    for case in CASES:
        overlays = ",".join(case.overlays) or "-"
        expected = case.expect + (" (bytes == " + case.replay_of + ")" if case.replay_of else "")
        lines.append(f"{case.id:<4} {case.title:<26} {overlays:<38} {case.seed:<7} {expected}")
    lines += ["", "Prerequisites: java, an existing UPR-FVX JAR built from the pilot candidate (never built here),",
              "the source ROM, a neutral .rnqs saved once in the GUI, and a new --out folder outside the",
              "tracked tree (" + " or ".join(ALLOWED_OUTPUT_ROOTS) + "/ inside the Workspace).",
              "Pilot candidate: " + "; ".join(f"{k} {v[1][:12]}" for k, v in PILOT.items())]
    lines += ["", "#748 single options (--single --select ID[,ID] or all; same prerequisites)", ""]
    lines.append(f"{'ID':<4} {'Feature':<14} {'Family':<9} {'Option':<27} {'Seed':<7} Expected settings change")
    for o in SINGLE_OPTIONS:
        change = ", ".join(f"{k}={v}" for k, v in o.effect.items())
        lines.append(f"{o.id:<4} {o.feature:<14} {o.family:<9} {o.title:<27} {o.seed:<7} {change}")
    lines += ["Each case: settings + target normalization checked first, then generate, reopen,",
              "loaded-manifest and a byte replay. Best result: GENERATION/REOPEN PASS, never FEATURE_VERIFIED."]
    inv = inventory(ROOT)
    plan = plan_cases(inv)
    lines += ["", "#750 comprehensive matrix (--suite; select with --kind/--family/--risk/--case, "
              f"at most {MAX_BATCH} cases per run)", "Revision: " + revision_label(), ""]
    lines += [note for note in inv.notes]
    lines.append("Feature inventory (UPR-FVX source at the pin + historical 132-feature ledger; historical ledger")
    lines.append("results are not current acceptance)")
    lines.append(f"  {'Feature ID':<34} {'Family':<6} {'Disposition':<13} Reason")
    for fid, f in inv.features.items():
        lines.append(f"  {fid:<34} {f.family:<6} {f.state:<13} {f.reason}")
    counts = ", ".join(f"{k}={sum(f.state == k for f in inv.features.values())}" for k in DISPOSITIONS)
    lines += ["", f"Features: {len(inv.features)} IDs ({inv.catalog_ids} current overlays, {inv.ledger_ids} ledger IDs, "
              f"{inv.ledger_only} ledger-only); {counts}", ""]
    lines.append(f"  {'Case':<50} {'Kind':<7} {'Risk':<6} {'Status':<18} Overlays / reason")
    for c in plan:
        detail = ",".join(c.overlays) or "00_BASELINE" if c.status in RUNNABLE_CASES else c.reason
        detail += "; " + c.reason if c.status in RUNNABLE_CASES and c.reason else ""
        lines.append(f"  {c.id:<50} {c.kind:<7} {c.risk:<6} {c.status:<18} {detail}")
    lines += [""] + case_summary(plan)
    return lines


def overlay_catalog(text):
    """settings-profile overlay ID -> lambda source, in catalog order."""
    start = text.index("buildFeatureOverlays()")
    end = text.index("return Collections.unmodifiableMap(overlays)", start)
    catalog = {}
    for chunk in text[start:end].split('overlays.put("')[1:]:
        fid, _, body = chunk.partition('"')
        catalog[fid] = body.strip().removeprefix(",").strip().removesuffix(");")
    return catalog


def tweak_setters(text):
    """Setter names Settings.tweakForRom may change (calls and direct field writes)."""
    start = text.index("public TweakForROMFeedback tweakForRom(")
    body = text[start:text.index("// getters and setters", start)]
    names = set(re.findall(r"\bthis\.(set\w+)\(", body))
    for field in re.findall(r"^\s*(?:this\.)?([a-z]\w*)\s*&?=(?!=)", body, re.M):
        names.add("set" + field[0].upper() + field[1:])
    return names


# ---------------------------------------------------------------------------
# #750 comprehensive matrix: inventory, case plan and batch selection.
# Everything is derived from the pinned UPR-FVX source text; a changed source
# fails closed (every ID NEEDS_REVIEW, no runnable case).
MISC_SOURCE = "romio/src/main/java/com/uprfvx/romio/MiscTweak.java"
SOURCE_PINS = {
    CATALOG_SOURCE: "af84c3e03f030503741da495207699c24cbd701b360510b95383b498eefecd25",
    SETTINGS_SOURCE: "9fcd9b40bd8b509010ee8c8c5c17570ab5428262f84fe8a7c51c5eb8e8024dcb",
    MISC_SOURCE: "b3ef9a02e3777dcbe69430e59350a5ac076d66d31ee346b2b189673e664fa002",
}
MISC_KEY = "getCurrentMiscTweaks"   # bit set; overlays OR their bit in
EXPECTED_GUARDS = {
    MOVESETS: LEARNSET_GUARD,
    REORDER: LEARNSET_GUARD,
    "FVX-TRAIT-017": ("RandomizationException: CFRU/DPE RANDOM_EVERY_LEVEL is unsupported: creating relations "
                      "would repack raw evolution slots. Use ordinary RANDOM target randomization."),
}
# upr_generation_matrix's target exclusions; kept visible, never silently run.
LEGACY_REASONS = {
    "FVX-TRAIT-025": "OWNERSHIP_WITNESS_V1 required (Make Evolutions Easier)",
    "FVX-MISC-011": "redundant with CFRU native reusable TMs",
    "FVX-FOE-SENSIBLE-HELD-ITEMS": "legacy 04_FOE_HELD_ITEMS_SENSIBLE_EXPECTED_FAIL diagnostic",
}
# Owner toggles a sub-option needs to have any effect; follows
# upr_generation_matrix.closure. A sub-option's case runs with its parents.
PARENTS = {
    "FVX-TRAIT-002": ("FVX-TRAIT-001",), "FVX-TRAIT-003": ("FVX-TRAIT-001", "FVX-TRAIT-002"),
    "FVX-TRAIT-007": ("FVX-TRAIT-006",), "FVX-TRAIT-026": ("FVX-TRAIT-024",),
    "FVX-TRAIT-028": ("FVX-TRAIT-005",),
    **{f"FVX-TRAIT-{n:03}": ("FVX-TRAIT-008",) for n in range(9, 16)},
    **{f"FVX-TRAIT-{n:03}": ("FVX-TRAIT-016",) for n in range(18, 24)},
    **{f"FVX-SST-{n:03}": (STARTER,) for n in (5, 6, 7, 9)},
    "FVX-SST-008": (STARTER, "FVX-SST-007"), "FVX-SST-013": ("FVX-SST-011",), "FVX-SST-015": ("FVX-SST-014",),
    **{f"FVX-MOVE-{n:03}": (MOVESETS,) for n in (8, 10, 11)},
    **{f"FVX-FOE-{n:03}": (TRAINER,) for n in (2, 3, 4, 5, 6, 7, 8, 10, 11, 14)},
    "FVX-FOE-009": ("MODE-FOE-TYPE-THEMED",), "FVX-FOE-012": (TRAINER, STARTER),
    "FVX-FOE-SENSIBLE-HELD-ITEMS": (TRAINER, "FVX-FOE-008"), "MODE-TRAINER-CLASS-SPRITE-SYNC": ("FVX-FOE-013",),
    "FVX-GEN-002": (TRAINER,), "MODE-ALLOW-REGIONAL-FORMS": ("FVX-GEN-001",),
    **{f"FVX-WILD-{n:03}": (WILD,) for n in range(2, 13) if n != 9},
    "FVX-WILD-009": (WILD, "FVX-WILD-008"), "FVX-SPECIAL-WILD-001": (WILD,),
    **{f"FVX-TM-{n:03}": ("FVX-TM-001",) for n in (2, 3, 4)},
    "FVX-TM-006": ("FVX-TM-001", "FVX-TM-005"), "FVX-TM-007": ("FVX-TM-001", "FVX-TM-005"),
    "FVX-TM-008": ("FVX-TM-005",),
    **{f"FVX-TM-{n:03}": ("FVX-TM-009",) for n in (10, 11, 12)},
    "FVX-TM-014": ("FVX-TM-009", "FVX-TM-013"), "FVX-TM-015": ("FVX-TM-009", "FVX-TM-013"),
    "FVX-ITEM-004": ("FVX-ITEM-002",),
    **{f"FVX-ITEM-{n:03}": ("FVX-ITEM-006",) for n in (7, 8, 9)},
    "FVX-TYPE-002": ("MODE-TYPE-INVERSE",),
}
# Legacy #681 family names -> the family token used for selection.
FAMILY_TOKEN = {
    "GEN_SAFE": "GEN", "TRAITS": "TRAIT", "STARTERS_STATICS_TRADES": "SST", "MOVES_MOVESETS": "MOVE",
    "FOE": "FOE", "WILD": "WILD", "TM_TUTOR": "TM", "ITEMS_SHOPS": "ITEM", "TYPE_EFFECTIVENESS": "TYPE",
    "GRAPHICS_PALETTES": "GFX", "MISC": "MISC", "SPECIAL_WILD": "WILD", "EVOLUTIONS": "TRAIT",
}
MODE_FAMILY = {"INCLUDE": "GEN", "ALLOW": "GEN", "INTRO": "GEN", "NO": "GEN", "TRAINER": "FOE", "SPECIAL": "WILD"}
KINDS = ("SINGLE", "PAIR", "TRIPLE", "PROFILE")
RUNNABLE_CASES = ("RUNNABLE", "EXPECTED_REJECTION")
MAX_BATCH = 25


@dataclass(frozen=True)
class Feature:
    family: str
    state: str
    reason: str
    delta: dict = None    # source-derived Settings getter -> observed value


@dataclass
class Inventory:
    features: dict
    notes: list
    catalog_ids: int = 0
    ledger_ids: int = 0
    ledger_only: int = 0
    bundles: dict = None  # legacy family -> overlays
    profiles: dict = None
    touched: frozenset = frozenset()


@dataclass(frozen=True)
class PlanCase:
    id: str
    kind: str
    families: tuple
    overlays: tuple
    seed: int
    status: str            # RUNNABLE, EXPECTED_REJECTION, or the reason it is excluded
    reason: str = ""
    delta: tuple = ()      # expected Settings change against the baseline
    own: tuple = ()        # the part the case is about; must not already hold
    guard: str = ""
    risk: str = "normal"


def family_of(fid):
    token = fid.split("-")[1]
    return MODE_FAMILY.get(token, token) if fid.startswith("MODE-") else MODE_FAMILY.get(token, token)


def case_seed(case_id):
    return 750_000_000 + int(hashlib.sha256(case_id.encode()).hexdigest()[:8], 16) % 100_000_000


def literal(value):
    """Observed text of a setter argument, or None when the source is not a plain constant."""
    value = value.strip()
    if value in ("true", "false") or re.fullmatch(r"-?[0-9]+", value):
        return value
    match = (re.fullmatch(r"Settings\.\w+\.([A-Z][A-Z0-9_]*)", value)
             or re.fullmatch(r"new BattleStyle\(BattleStyle\.Modification\.([A-Z_]+), BattleStyle\.Style\.[A-Z_]+\)",
                             value))
    return match[1] if match else None


def overlay_delta(body, getters, misc):
    """Settings getter changes of one overlay lambda; None if it cannot be read exactly."""
    if body == "SettingsProfileGenerator::enablePokemonPaletteRandomization":
        statements = ["enablePokemonPaletteRandomization(s)"]
    elif body.startswith("s -> "):
        inner = body[5:].strip()
        if inner.startswith("{") and inner.endswith("}"):
            inner = inner[1:-1]
        statements = [x.strip() for x in inner.split(";") if x.strip()]
    else:
        return None
    sets = []
    for statement in statements:
        if match := re.fullmatch(r"s\.set(\w+)\((.*)\)", statement):
            sets.append(match.groups())
        elif match := re.fullmatch(r"setWildZoneMode\(s, (Settings\.WildPokemonZoneMod\.\w+)\)", statement):
            sets += [("RandomizeWildPokemon", "true"), ("WildPokemonZoneMod", match[1])]
        elif statement == "enablePokemonPaletteRandomization(s)":
            sets.append(("PokemonPalettesMod", "Settings.PokemonPalettesMod.RANDOM"))
        elif (match := re.fullmatch(r"enableMiscTweak\(s, MiscTweak\.(\w+)\)", statement)) and match[1] in misc:
            sets.append(("CurrentMiscTweaks", str(misc[match[1]])))
        else:
            return None
    delta = {}
    for name, value in sets:
        text = literal(value)
        getter = [p + name for p in ("is", "get", "use") if p + name in getters]
        if text is None or len(getter) != 1 or delta.get(getter[0], text) != text:
            return None
        delta[getter[0]] = text
    return delta or None


def merge(deltas):
    """(combined delta, conflicting getter or "")."""
    out = {}
    for delta in deltas:
        for key, value in delta.items():
            if key == MISC_KEY and key in out:
                out[key] = str(int(out[key]) | int(value))
            elif out.get(key, value) != value:
                return None, key
            else:
                out[key] = value
    return out, ""


def apply(state, delta):
    state = dict(state)
    for key, value in delta.items():
        state[key] = str(int(state.get(key, "0")) | int(value)) if key == MISC_KEY else value
    return state


def setter_of(getter):
    return "set" + re.sub(r"^(is|get|use)", "", getter)


def family_bundles(source):
    """Legacy #681 family bundles and full profiles, from upr_generation_matrix's source model."""
    _, _, profiles = gm.source_model(source)
    full = [profiles[name] for name in gm.FULL]
    bundles = dict(zip(gm.FAMILIES[1:], (full[i] for i in (0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11))))
    bundles["GEN_SAFE"] = ("MODE-GEN-LIMIT-1-9-NO-RELATIVES", "MODE-ALLOW-REGIONAL-FORMS",
                           "MODE-GEN-LIMIT-1-9-NO-MEGAS", "MODE-GEN-LIMIT-1-9-NO-GMAX")
    bundles["EVOLUTIONS"] = ("FVX-TRAIT-016", "FVX-TRAIT-022")
    return bundles, {name: profiles[name] for name in gm.FULL}


def inventory(root):
    """Every current overlay ID and every historical ledger ID, each with one disposition."""
    with open(root / LEDGER, newline="") as f:
        ledger = [row.split("\t", 1)[0] for row in list(f)[1:] if row.strip()]
    notes = []
    try:
        texts = {rel: (root / UPR_SOURCE / rel).read_text() for rel in SOURCE_PINS}
    except OSError:
        texts = None
        notes.append("UPR-FVX source unavailable: every ID is NEEDS_REVIEW.")
    if texts and any(hashlib.sha256(texts[rel].encode()).hexdigest() != pin for rel, pin in SOURCE_PINS.items()):
        texts = None
        notes.append("UPR-FVX source differs from the pinned revision: every ID is NEEDS_REVIEW.")
    catalog = overlay_catalog(texts[CATALOG_SOURCE]) if texts else {}
    getters = set(re.findall(r"public \S+ ((?:is|get|use)[A-Z]\w*)\(\)", texts[SETTINGS_SOURCE])) if texts else set()
    misc = {name: eval(value, {}) for name, value in re.findall(  # noqa: S307 - "1 << n" literals only
        r"MiscTweak (\w+) = new MiscTweak\(([0-9 <]+),", texts[MISC_SOURCE])} if texts else {}
    touched = frozenset(tweak_setters(texts[SETTINGS_SOURCE])) if texts else frozenset()
    legacy = (gm.EXCLUDED - EXPECTED_GUARDS.keys())
    features = {}

    def classify(fid):
        if fid in features:
            return features[fid]
        body, family = catalog.get(fid), family_of(fid)
        delta = overlay_delta(body, getters, misc) if body else None
        if body is None:
            f = Feature(family, "NEEDS_REVIEW", "historical ledger ID without current overlay" if texts
                        else "source not verified")
        elif body.startswith("unsupported("):
            f = Feature(family, "UNSUPPORTED", "settings-profile refuses: "
                        + (re.findall(r'"([^"]*)"', body) + ["", ""])[1])
        elif fid in EXPECTED_GUARDS:
            f = Feature(family, "GUARDED", GUARDED[fid] + "; runs as EXPECTED_REJECTION", delta)
        elif fid in legacy:
            f = Feature(family, "NEEDS_REVIEW", "legacy target exclusion, not re-verified: "
                        + LEGACY_REASONS.get(fid, "Mega/G-Max/Z/Dynamax pool"))
        elif delta is None:
            f = Feature(family, "NEEDS_REVIEW", "overlay source not readable as exact Settings changes")
        else:
            f = with_parents(fid, family, delta)
        features[fid] = f
        return f

    def with_parents(fid, family, delta):
        parents = PARENTS.get(fid, ())
        for parent in parents:
            if parent not in catalog:
                return Feature(family, "NEEDS_REVIEW", f"parent {parent} has no current overlay", delta)
            p = classify(parent)
            if p.state != "RUNNABLE":
                state = "GUARDED" if p.state == "GUARDED" else "NEEDS_REVIEW"
                return Feature(family, state, f"parent {parent} is {p.state}", delta)
        context, _ = merge(features[p].delta for p in parents)
        combined, conflict = merge([context, delta])
        if conflict:
            return Feature(family, "NEEDS_REVIEW", "contradicts its parent on " + conflict, delta)
        before = apply(NEUTRAL, context)
        if all(key in before and before[key] == value for key, value in delta.items()):
            return Feature(family, "NOT_RUN", "no change against the neutral baseline (OFF value; M00 covers it)", delta)
        reason = ", ".join(f"{k}={v}" for k, v in delta.items())
        if parents:
            reason += "; with " + "+".join(parents)
        normalized = sorted(setter_of(k) for k in delta if setter_of(k) in touched)
        if normalized:
            reason += "; tweakForRom may normalize " + ",".join(normalized)
        return Feature(family, "RUNNABLE", reason, delta)

    for fid in list(catalog) + [i for i in ledger if i not in catalog]:
        classify(fid)
    bundles = profiles = None
    if texts:
        try:
            bundles, profiles = family_bundles(texts[CATALOG_SOURCE])
        except (MatrixError, KeyError, TypeError):
            notes.append("Legacy family/profile derivation failed: no pair, triple or profile case is runnable.")
    return Inventory(features, notes, len(catalog), len(ledger), sum(i not in catalog for i in ledger),
                     bundles, profiles, touched)


def plan_cases(inv):
    """Single, pair, triple and profile cases; each excluded case says why."""
    plan, seen = [], {}
    features = inv.features

    def expand(wanted):
        overlays = []
        for overlay in wanted:
            for o in PARENTS.get(overlay, ()) + (overlay,):
                if o not in overlays:
                    overlays.append(o)
        return tuple(overlays)

    def risk(overlays):
        high = any(o in gm.RISK_SINGLES or any(setter_of(k) in inv.touched for k in (features[o].delta or {}))
                   for o in overlays)
        return "high" if high else "normal"

    def add(cid, kind, families, wanted, status="RUNNABLE", reason="", own=None, guard=""):
        overlays = expand(wanted)
        delta = context = {}
        if status in RUNNABLE_CASES:
            delta, conflict = merge(features[o].delta for o in overlays)
            if conflict:
                status, reason, delta = "NEEDS_REVIEW", "contradictory settings on " + conflict, {}
            elif delta.get("isPokemonPalettesFollowTypes") == delta.get("isPokemonPalettesShinyFromNormal") == "true":
                status, reason = "NEEDS_REVIEW", "Follow Types + Shiny From Normal palettes (legacy exclusion)"
            elif own is not None:
                context, _ = merge(features[o].delta for o in overlays if o not in own)
        if status in RUNNABLE_CASES:
            key = (tuple(sorted(delta.items())), status)
            if key in seen:
                status, reason = "DUPLICATE", "same effective settings as " + seen[key]
            else:
                seen[key] = cid
        own_delta = {k: v for k, v in delta.items() if k not in context or context[k] != v} if own else delta
        plan.append(PlanCase(cid, kind, tuple(dict.fromkeys(families)), overlays if status in RUNNABLE_CASES else (),
                             case_seed(cid), status, reason, tuple(sorted(delta.items())),
                             tuple(sorted(own_delta.items())), guard, risk(overlays) if status in RUNNABLE_CASES
                             else "-"))

    add("PRO-CONTROL", "PROFILE", (), ())
    for fid, f in features.items():
        if f.state == "RUNNABLE":
            add("SGL-" + fid, "SINGLE", (f.family,), (fid,), own=(fid,))
        elif f.state == "GUARDED" and fid in EXPECTED_GUARDS:
            add("SGL-" + fid, "SINGLE", (f.family,), (fid,), "EXPECTED_REJECTION", own=(fid,),
                guard=EXPECTED_GUARDS[fid])
        else:
            add("SGL-" + fid, "SINGLE", (f.family,), (), f.state, f.reason)

    bundles = {}
    for family, members in (inv.bundles or {}).items():
        bundles[family] = tuple(m for m in members if m in features and features[m].state == "RUNNABLE"
                                and m not in gm.RISK_SINGLES)

    def composite(cid, kind, families):
        if inv.bundles is None:
            return add(cid, kind, map(FAMILY_TOKEN.get, families), (), "NEEDS_REVIEW", "family bundles unavailable")
        empty = [f for f in families if not bundles[f]]
        if empty:
            return add(cid, kind, map(FAMILY_TOKEN.get, families), (), "NEEDS_REVIEW",
                       "no runnable overlay in " + ",".join(empty))
        add(cid, kind, map(FAMILY_TOKEN.get, families), *compatible(
            itertools.chain.from_iterable(bundles[f] for f in families)))

    def compatible(members):
        """Bundle members in order; one that contradicts the ones before is left out, visibly."""
        kept, skipped, delta = [], [], {}
        for member in dict.fromkeys(members):
            combined, conflict = merge([delta] + [features[o].delta for o in expand((member,))])
            if conflict:
                skipped.append(member)
            else:
                kept.append(member)
                delta = combined
        return tuple(kept), "RUNNABLE", ("left out (contradicts earlier members): " + ",".join(skipped)
                                         if skipped else "")

    for pair in itertools.combinations(gm.FAMILIES, 2):
        composite("PAIR-" + "+".join(pair), "PAIR", pair)
    for triple in gm.TRIPLES:
        composite("TRI-" + "+".join(triple), "TRIPLE", triple)
    for name, family in zip(gm.FULL, (*gm.FAMILIES[1:4], "FOE", *gm.FAMILIES[4:])):
        if inv.profiles is None:
            add("FAM-" + name, "PROFILE", (FAMILY_TOKEN[family],), (), "NEEDS_REVIEW", "profiles unavailable")
            continue
        members = tuple(m for m in inv.profiles[name] if features.get(m, Feature("", "", "")).state == "RUNNABLE"
                        and m not in gm.RISK_SINGLES)
        if members:
            add("FAM-" + name, "PROFILE", (FAMILY_TOKEN[family],), *compatible(members))
        else:
            add("FAM-" + name, "PROFILE", (FAMILY_TOKEN[family],), (), "NEEDS_REVIEW", "no runnable overlay")
    data = ("GEN_SAFE", "TRAITS", "MOVES_MOVESETS", "EVOLUTIONS")
    world = ("STARTERS_STATICS_TRADES", "FOE", "WILD", "TM_TUTOR", "ITEMS_SHOPS")
    for name, families in zip(gm.MAXIMUM, (data, world, data + world + ("GRAPHICS_PALETTES", "MISC", "SPECIAL_WILD"))):
        composite("MAX-" + name, "PROFILE", families)
    for name in gm.SELECTED[1:]:
        add("PRO-" + name, "PROFILE", (), (), "NEEDS_REVIEW",
            "needs the legacy Settings bridge/accepted settings string, not settings-profile")
    return plan


def case_summary(plan):
    lines = [f"{'Cases':<9} {'Planned':>7} {'Runnable':>8} {'Rejection':>9} {'Duplicate':>9} {'Excluded':>8}  Excluded by"]
    for kind in KINDS:
        cases = [c for c in plan if c.kind == kind]
        excluded = [c for c in cases if c.status not in RUNNABLE_CASES + ("DUPLICATE",)]
        why = ", ".join(f"{s}={sum(c.status == s for c in excluded)}" for s in DISPOSITIONS[1:]
                        if any(c.status == s for c in excluded))
        lines.append(f"{kind:<9} {len(cases):>7} {sum(c.status == 'RUNNABLE' for c in cases):>8} "
                     f"{sum(c.status == 'EXPECTED_REJECTION' for c in cases):>9} "
                     f"{sum(c.status == 'DUPLICATE' for c in cases):>9} {len(excluded):>8}  {why or '-'}")
    runnable = sum(c.status in RUNNABLE_CASES for c in plan)
    lines += [f"Total: {len(plan)} planned, {runnable} runnable (unique effective settings), "
              f"{len(plan) - runnable} not runnable or duplicate. Runnable is not PASS: only a local --suite run",
              "can report PASS_GENERATION_REOPEN_REPLAY, and never FEATURE_VERIFIED."]
    return lines


def revision_label():
    pins = " ".join(f"{name} {rev[:12]}" for name, (_, rev) in PILOT.items())
    return pins + "; catalog sha256 " + SOURCE_PINS[CATALOG_SOURCE][:12]


def select_cases(plan, kinds=(), families=(), risk=None, ids=(), chunk=None):
    """Explicit, bounded batch; there is no implicit full run."""
    if not (kinds or families or risk or ids):
        raise MatrixError("--suite needs --kind, --family, --risk or --case; there is no implicit full run.")
    known = {f for c in plan for f in c.families}
    bad = [v for v in kinds if v not in KINDS] + [v for v in families if v not in known]
    if risk not in (None, "high", "normal"):
        bad.append(risk)
    by_id = {c.id: c for c in plan}
    bad += [i for i in ids if i not in by_id]
    if bad:
        raise MatrixError("Unknown selection: " + ", ".join(
            v if re.fullmatch(r"[A-Za-z0-9_+-]{1,80}", v) else "<invalid>" for v in bad) + "; see --plan.")
    for i in ids:
        if by_id[i].status not in RUNNABLE_CASES:
            raise MatrixError(f"{i} is {by_id[i].status}: {by_id[i].reason}")
    chosen = [c for c in plan if c.status in RUNNABLE_CASES and (not kinds or c.kind in kinds)
              and (not families or set(c.families) & set(families)) and (not risk or c.risk == risk)
              and (not ids or c.id in ids)]
    if not chosen:
        raise MatrixError("The selection contains no runnable case.")
    chunks = [chosen[i:i + MAX_BATCH] for i in range(0, len(chosen), MAX_BATCH)]
    if chunk is None and len(chunks) > 1:
        raise MatrixError(f"The selection has {len(chosen)} cases; pass --chunk 1..{len(chunks)} "
                          f"({MAX_BATCH} per run) or narrow it.")
    if chunk is not None and not 1 <= chunk <= len(chunks):
        raise MatrixError(f"--chunk must be 1..{len(chunks)}.")
    return chunks[(chunk or 1) - 1]


def revision_lines(root, jar, allow_drift):
    """UPR must be the candidate the JAR was built from; CFRU/DPE are informational."""
    lines = []
    for name, (relative, expected) in PILOT.items():
        actual = gm.git(root / relative, "rev-parse", "HEAD")
        dirty = gm.git(root / relative, "status", "--porcelain", "--untracked-files=no")
        state = ("MATCH" if actual == expected else "DIFFERS") + ("; local changes" if dirty else "")
        lines.append(f"{name}: {actual[:12]} {state}")
        if name == "UPR-FVX" and state != "MATCH" and not allow_drift:
            raise MatrixError("UPR-FVX checkout is not the pilot candidate; STOP (or --allow-revision-drift).")
    freshness = gm.jar_freshness(root, jar)
    lines.append("JAR: " + freshness)
    if freshness != "NOT_OLDER_THAN_LOCAL_SOURCE" and not allow_drift:
        raise MatrixError("JAR is older than the UPR-FVX source or unverifiable; rebuild it first.")
    return lines


def output_root(value, root):
    out = Path(os.path.abspath(value))
    if out.is_relative_to(root) and not any(out.is_relative_to(root / p) for p in ALLOWED_OUTPUT_ROOTS):
        raise MatrixError("--out inside the Workspace must be under " + " or ".join(ALLOWED_OUTPUT_ROOTS) + "/.")
    if not out.parent.is_dir():
        raise MatrixError("--out parent folder does not exist.")
    try:
        out.mkdir()   # Atomic reservation; an existing folder is never reused.
    except FileExistsError:
        raise MatrixError("--out already exists; nothing is overwritten. Choose a new folder.") from None
    return out


@dataclass
class Result:
    status: str = "NOT_RUN"
    generate: str = "NOT_RUN"
    reopen: str = "NOT_RUN"
    replay: str = "-"
    detail: str = ""
    target: str = "-"
    settings: str = "-"


def save_log(directory, name, result):
    # Raw UPR text stays in the local case folder only; it is never printed.
    (directory / name).write_text(result.stdout + "\n--- stderr ---\n" + result.stderr)


def generate(case, rom, jar, settings, directory, digest):
    """One case in its own fresh folder; returns (Result, output path or None)."""
    res = Result()
    output = directory / "output.gba"
    run = command(["java", "-jar", str(jar), "cli", "-i", str(rom), "-o", str(output),
                   "-s", str(settings), "-z", str(case.seed)], directory)
    save_log(directory, "cli.log", run)
    text = run.stdout + run.stderr
    if gm.input_digest(rom) != digest:
        raise MatrixError("Source ROM changed during " + case.id + "; STOP.")
    produced = output.exists()
    if case.expect == "EXPECTED_REJECTION":
        res.generate = "REJECTED" if run.returncode else "PASS"
        untouched = not produced and [p.name for p in directory.iterdir()] == ["cli.log"]
        guard = case.guard or LEARNSET_GUARD
        if run.returncode and guard in text and untouched:
            res.status = "EXPECTED_REJECTION"
            res.detail = ("learnset" if guard == LEARNSET_GUARD else "exact") + " guard, no output"
        else:
            res.status = "FAIL"
            res.detail = ("output written" if not untouched else "accepted" if not run.returncode
                          else "different failure (see local cli.log)")
        return res, None
    if (run.returncode or "Randomized successfully!" not in text or gm.ERROR_MARKERS.search(text)
            or not produced or output.stat().st_size == 0):
        res.status, res.generate, res.detail = "FAIL", "FAIL", "generation failed (see local cli.log)"
        return res, None
    res.generate = "PASS"
    identity = directory / "MatrixReopen.java"
    identity.write_text(gm.REOPEN_IDENTITY)
    run = command(["java", "--class-path", str(jar), str(identity), str(output)], directory)
    identity.unlink()
    save_log(directory, "reopen.log", run)
    if run.returncode or "Supported CFRU/DPE output identity verified." not in run.stdout:
        res.status, res.reopen, res.detail = "FAIL", "FAIL", "output not reopened as CFRU/DPE"
        return res, None
    run = command(["java", "-jar", str(jar), "loaded-manifest", "-i", str(output),
                   "-o", str(directory / "loaded-manifest")], directory)
    save_log(directory, "loaded-manifest.log", run)
    text = run.stdout + run.stderr
    if run.returncode or "Wrote sanitized loaded manifests." not in text or gm.ERROR_MARKERS.search(text):
        res.status, res.reopen, res.detail = "FAIL", "FAIL", "loaded-manifest failed"
        return res, None
    res.status, res.reopen = "PASS", "PASS"
    return res, output


def write_settings(cases, baseline, jar, out, temp):
    """One settings-profile .rnqs per case; returns (baseline state, paths), all checked."""
    base_state, paths, states = profile_settings(cases, baseline, jar, out, temp)
    for case, state in zip(cases, states):
        check_case_settings(base_state, case, state)
    return base_state, paths


def profile_settings(cases, baseline, jar, out, temp):
    """One settings-profile .rnqs per case; returns (baseline state, paths, observed states)."""
    settings_dir = out / "settings"
    settings_dir.mkdir()
    base_state, = observe(jar, temp, [baseline])
    check_baseline(base_state)
    paths = []
    for case in cases:
        target = settings_dir / (case.id + ".rnqs")
        args = ["java", "-jar", str(jar), "settings-profile", "--base-settings", str(baseline),
                "--output-settings", str(target)]
        for overlay in case.overlays:
            args += ["--enable", overlay]
        if not case.overlays:
            # settings-profile rejects a call without overlays; 00_BASELINE is its no-op profile.
            args += ["--profile", "00_BASELINE"]
        run = command(args, temp)
        if run.returncode or "Settings profile written successfully." not in run.stdout or not target.is_file():
            raise MatrixError(case.id + ": settings-profile failed; STOP.")
        paths.append(target)
    return base_state, paths, observe(jar, temp, paths)


def run_matrix(rom, baseline, jar, out, temp):
    """All settings are generated and checked before the first ROM is touched."""
    _, paths = write_settings(CASES, baseline, jar, out, temp)

    results = {case.id: Result() for case in CASES}
    outputs = {}
    digest = gm.input_digest(rom)
    for case, settings in zip(CASES, paths):
        directory = out / case.id
        directory.mkdir()
        res, output = generate(case, rom, jar, settings, directory, digest)
        if case.replay_of and res.status == "PASS":
            same = case.replay_of in outputs and gm.same_bytes(outputs[case.replay_of], output)
            res.replay = "PASS" if same else "FAIL"
            if not same:
                res.status, res.detail = "FAIL", "output differs from " + case.replay_of
        results[case.id] = res
        if res.status == "FAIL":
            break   # Fail fast: later cases stay NOT_RUN.
        if output:
            outputs[case.id] = output
    return results


def report_lines(results):
    lines = [f"{'ID':<4} {'Case':<26} {'Generate':<9} {'Reopen':<8} {'Replay':<7} Result"]
    for case in CASES:
        r = results[case.id]
        detail = " (" + r.detail + ")" if r.detail else ""
        lines.append(f"{case.id:<4} {case.title:<26} {r.generate:<9} {r.reopen:<8} {r.replay:<7} {r.status}{detail}")
    counts = {k: sum(r.status == k for r in results.values())
              for k in ("PASS", "EXPECTED_REJECTION", "FAIL", "NOT_RUN")}
    overall = "PASS" if counts["FAIL"] == counts["NOT_RUN"] == 0 else "FAIL"
    lines += ["", "Summary: " + ", ".join(f"{k}={v}" for k, v in counts.items()) + "; MATRIX=" + overall,
              "Scope: generation/reopen/replay only; no boot, gameplay or learnset-preservation claim."]
    return lines, overall


def single_cases(options):
    return tuple(Case(o.id, o.title, (o.feature,), o.seed) for o in options)


def select_options(value):
    """Explicit selection only; unknown, non-executable or repeated IDs stop the run."""
    if value == "all":
        return SINGLE_OPTIONS
    by_feature = {o.feature: o for o in SINGLE_OPTIONS}
    ids = [i.strip() for i in (value or "").split(",") if i.strip()]
    bad = [i if re.fullmatch(r"[A-Z0-9-]{1,40}", i) else "<invalid>" for i in ids if i not in by_feature]
    if bad or not ids:
        raise MatrixError("--select: unknown or non-executable ID(s): " + ", ".join(bad or ["<empty>"])
                          + "; see --plan.")
    if len(set(ids)) != len(ids):
        raise MatrixError("--select: an ID is repeated.")
    return tuple(o for o in SINGLE_OPTIONS if o.feature in ids)


def run_single(rom, baseline, jar, out, temp, options):
    """#748: settings and target normalization are checked before any ROM is generated."""
    cases = single_cases(options)
    _, paths = write_settings(cases, baseline, jar, out, temp)
    results = {case.id: Result() for case in cases}
    digest = gm.input_digest(rom)
    check_targets(jar, temp, rom, baseline, cases, paths, results, digest, expected_state)
    return generate_checked(cases, paths, results, rom, jar, out, digest)


def drift_keys(expected, state):
    return sorted(k for k in expected.keys() | state.keys() if state.get(k) != expected.get(k))


def check_targets(jar, temp, rom, baseline, cases, paths, results, digest, expected_of):
    """Settings after the CLI's tweakForRom must still be baseline + the case's change."""
    if not cases:
        return
    target_base, *targets = observe(jar, temp, [baseline, *paths], rom=rom)
    if gm.input_digest(rom) != digest:
        raise MatrixError("Source ROM changed during target normalization; STOP.")
    for case, state in zip(cases, targets):
        drift = drift_keys(expected_of(target_base, case), state)
        results[case.id].target = "NEEDS_REVIEW" if drift else "PASS"
        if drift:
            results[case.id].status = "NEEDS_REVIEW"
            results[case.id].detail = "tweakForRom changed " + ",".join(drift)


def generate_checked(cases, paths, results, rom, jar, out, digest):
    """Generate, reopen and replay every case whose target check passed; fail fast."""
    for case, settings in zip(cases, paths):
        if results[case.id].target != "PASS":
            continue    # Never generated: its effect would not reach the ROM as configured.
        directory = out / case.id
        directory.mkdir()
        res, output = generate(case, rom, jar, settings, directory, digest)
        res.target, res.settings = "PASS", results[case.id].settings
        if res.status == "PASS":
            directory = out / (case.id + "-replay")
            directory.mkdir()
            again, repeated = generate(case, rom, jar, settings, directory, digest)
            same = again.status == "PASS" and gm.same_bytes(output, repeated)
            res.replay = "PASS" if same else "FAIL"
            if not same:
                res.status, res.detail = "FAIL", "replay " + (again.detail or "differs")
        results[case.id] = res
        if res.status == "FAIL":
            break   # Fail fast: later cases stay NOT_RUN.
    return results


def single_report_lines(results, options):
    lines = [f"{'ID':<4} {'Feature':<14} {'Target':<12} {'Generate':<9} {'Reopen':<8} {'Replay':<7} Result"]
    for o in options:
        r = results[o.id]
        shown = "GENERATION/REOPEN PASS" if r.status == "PASS" else r.status
        detail = " (" + r.detail + ")" if r.detail else ""
        lines.append(f"{o.id:<4} {o.feature:<14} {r.target:<12} {r.generate:<9} {r.reopen:<8} {r.replay:<7} "
                     f"{shown}{detail}")
    counts = {k: sum(r.status == k for r in results.values()) for k in ("PASS", "FAIL", "NEEDS_REVIEW", "NOT_RUN")}
    overall = "PASS" if counts["PASS"] == len(results) else "FAIL" if counts["FAIL"] else "INCOMPLETE"
    lines += ["", "Summary: " + ", ".join(f"{k}={v}" for k, v in counts.items()) + "; SINGLE=" + overall,
              "Scope: settings, target normalization, generation, reopen and replay only; feature semantics",
              "NOT VERIFIED (no FEATURE_VERIFIED claim); no boot or gameplay claim."]
    return lines, overall


def run_suite(rom, baseline, jar, out, temp, plan):
    """#750: one bounded batch; settings, no-op and target checks precede any generation."""
    cases = [Case(p.id, p.kind, p.overlays, p.seed,
                  "EXPECTED_REJECTION" if p.status == "EXPECTED_REJECTION" else "PASS", guard=p.guard)
             for p in plan]
    deltas = {p.id: dict(p.delta) for p in plan}
    base_state, paths, states = profile_settings(cases, baseline, jar, out, temp)
    results = {case.id: Result() for case in cases}
    for p, state in zip(plan, states):
        r = results[p.id]
        drift = drift_keys(apply(base_state, deltas[p.id]), state)
        context = apply(base_state, {k: v for k, v in p.delta if (k, v) not in p.own})
        if drift:
            r.settings, r.status, r.detail = "DRIFT", "NEEDS_REVIEW", "settings differ from source delta: " + ",".join(drift)
        elif p.own and all(context.get(k) == v for k, v in p.own):
            r.settings, r.status, r.detail = "NO-OP", "NEEDS_REVIEW", "baseline already holds the case's change"
        else:
            r.settings = "PASS"
    checked = [(c, s) for c, s in zip(cases, paths) if results[c.id].settings == "PASS"]
    digest = gm.input_digest(rom)
    check_targets(jar, temp, rom, baseline, [c for c, _ in checked], [s for _, s in checked], results, digest,
                  lambda base, case: apply(base, deltas[case.id]))
    return generate_checked(cases, paths, results, rom, jar, out, digest)


SUITE_STATUS = {"PASS": "PASS_GENERATION_REOPEN_REPLAY"}


def suite_report_lines(results, plan):
    lines = ["Revision: " + revision_label(),
             f"{'Case':<50} {'Kind':<7} {'Settings':<8} {'Target':<12} {'Generate':<9} {'Reopen':<7} {'Replay':<6} Result"]
    for p in plan:
        r = results[p.id]
        detail = " (" + r.detail + ")" if r.detail else ""
        lines.append(f"{p.id:<50} {p.kind:<7} {r.settings:<8} {r.target:<12} {r.generate:<9} {r.reopen:<7} "
                     f"{r.replay:<6} {SUITE_STATUS.get(r.status, r.status)}{detail}")
    names = ("PASS_GENERATION_REOPEN_REPLAY", "EXPECTED_REJECTION", "FAIL", "NEEDS_REVIEW", "NOT_RUN")
    shown = [SUITE_STATUS.get(r.status, r.status) for r in results.values()]
    counts = {k: shown.count(k) for k in names}
    done = counts[names[0]] + counts["EXPECTED_REJECTION"]
    overall = "PASS" if done == len(results) else "FAIL" if counts["FAIL"] else "INCOMPLETE"
    lines += ["", "Summary: " + ", ".join(f"{k}={v}" for k, v in counts.items()) + "; SUITE=" + overall,
              "Scope: settings delta, target normalization, generation, reopen and byte replay only;",
              "feature semantics NOT VERIFIED (no FEATURE_VERIFIED claim); no boot or gameplay claim."]
    return lines, overall


def csv_arg(value):
    return tuple(v.strip() for v in (value or "").split(",") if v.strip())


def self_test():
    import unittest
    tests = Path(__file__).resolve().parent / "tests"
    suite = unittest.defaultTestLoader.discover(str(tests), pattern="test_firered_pilot_matrix.py",
                                                top_level_dir=str(tests))
    return 0 if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful() else 1


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        # Never echo supplied values; they may be private paths.
        self.exit(2, "Invalid arguments; see --help.\n")


def main(argv=None):
    parser = SafeParser(description="#743/#748/#750 USER-ONLY pilot, single-option and comprehensive matrix.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--plan", action="store_true", help="list cases; reads nothing")
    action.add_argument("--self-test", action="store_true", help="synthetic mock tests only")
    action.add_argument("--matrix", action="store_true", help="real local run (needs --confirm)")
    action.add_argument("--single", action="store_true", help="real local single-option run (needs --confirm)")
    action.add_argument("--suite", action="store_true", help="real local comprehensive-matrix batch (needs --confirm)")
    parser.add_argument("--select", help="--single: comma-separated feature IDs from --plan, or all")
    parser.add_argument("--kind", help="--suite: " + ",".join(KINDS))
    parser.add_argument("--family", help="--suite: family tokens from --plan (e.g. TRAIT,TM)")
    parser.add_argument("--risk", help="--suite: high or normal")
    parser.add_argument("--case", help="--suite: comma-separated case IDs from --plan")
    parser.add_argument("--chunk", type=int, help=f"--suite: part of a selection larger than {MAX_BATCH}")
    parser.add_argument("--confirm", help="must be " + CONFIRM_TOKEN + " for --matrix/--single/--suite")
    parser.add_argument("--rom", help="source CFRU/DPE ROM")
    parser.add_argument("--baseline", help="neutral .rnqs saved once from the UPR GUI")
    parser.add_argument("--out", help="new output folder (must not exist)")
    parser.add_argument("--jar", help="existing UPR-FVX JAR (default: local build output)")
    parser.add_argument("--allow-revision-drift", action="store_true",
                        help="run although UPR-FVX/JAR are not the pilot candidate (development only)")
    args = parser.parse_args(argv)
    if args.plan:
        print("\n".join(plan_lines()))
        return 0
    if args.self_test:
        return self_test()
    try:
        mode = "--single" if args.single else "--suite" if args.suite else "--matrix"
        if args.confirm != CONFIRM_TOKEN:
            raise MatrixError(mode + " runs real ROM generation; pass --confirm " + CONFIRM_TOKEN + ".")
        options = select_options(args.select) if args.single else None
        batch = None
        if args.suite:
            inv = inventory(ROOT)
            if inv.notes:
                raise MatrixError(inv.notes[0] + " STOP.")
            batch = select_cases(plan_cases(inv), csv_arg(args.kind), csv_arg(args.family), args.risk,
                                 csv_arg(args.case), args.chunk)
        if not (args.rom and args.baseline and args.out):
            raise MatrixError(mode + " requires --rom, --baseline and --out.")
        rom, baseline = Path(args.rom).resolve(), Path(args.baseline).resolve()
        jar = Path(args.jar).resolve() if args.jar else DEFAULT_JAR
        if not rom.is_file() or not baseline.is_file() or not jar.is_file():
            raise MatrixError("ROM, baseline or JAR not found; the JAR is never built here.")
        title = {"--single": "#748 single-option matrix", "--suite": f"#750 comprehensive matrix batch "
                 f"({len(batch or ())} cases)"}.get(mode, "#743 pilot settings matrix")
        header = [title + (" (REVISION DRIFT ALLOWED)" if args.allow_revision_drift else "")]
        header += revision_lines(ROOT, jar, args.allow_revision_drift)
        out = output_root(args.out, ROOT)
        print("\n".join(header), flush=True)
        with tempfile.TemporaryDirectory(prefix="pilot-matrix-") as temp:
            if args.single:
                results = run_single(rom, baseline, jar, out, Path(temp), options)
            elif args.suite:
                results = run_suite(rom, baseline, jar, out, Path(temp), batch)
            else:
                results = run_matrix(rom, baseline, jar, out, Path(temp))
        if args.single:
            lines, overall = single_report_lines(results, options)
        elif args.suite:
            lines, overall = suite_report_lines(results, batch)
        else:
            lines, overall = report_lines(results)
        print("\n".join(lines))
        return 0 if overall == "PASS" else 1
    except MatrixError as error:
        print("STOP: " + str(error), file=sys.stderr)
        return 2
    except (OSError, subprocess.SubprocessError):
        print("STOP: local file or subprocess operation failed; details discarded.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
