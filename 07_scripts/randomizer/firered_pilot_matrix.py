#!/usr/bin/env python3
"""#743/#748: USER-ONLY CFRU/DPE Gen 9 pilot settings matrix and single options.

Composes UPR-FVX's existing settings-profile, cli and loaded-manifest commands
for the eleven pilot cases. The user supplies one neutral .rnqs saved once from
the GUI; its effective state is read through the public Settings API (a
temporary read-only Java adapter, because UPR has no settings-dump command)
before any overlay is applied. No settings bytes are written or patched here.

Modes: --plan (prints cases and the feature disposition; reads no ROM, JAR or
.rnqs), --self-test (synthetic mocks only), --matrix (the eleven pilot cases) and
--single --select IDS (#748 single options). Both real modes require --confirm
USER_LOCAL_RUN. Output stays on the user's machine; the printed table contains
categories only.
"""

import argparse
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
DISPOSITIONS = ("EXECUTABLE", "GUARDED", "UNSUPPORTED", "NEEDS_REVIEW", "NOT_RUN")
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
    lines += ["", "Feature disposition at this revision (UPR-FVX checkout source + historical 132-feature ledger;",
              "historical ledger results are not current acceptance)", ""]
    rows, note = disposition(ROOT)
    if note:
        lines.append(note)
    for fid, (state, reason) in rows.items():
        lines.append(f"  {fid:<34} {state:<13} {reason}")
    counts = [f"{k}={sum(v[0] == k for v in rows.values())}" for k in DISPOSITIONS]
    lines += ["", f"Disposition: {len(rows)} IDs; " + ", ".join(counts)]
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


def disposition(root):
    """ID -> (disposition, reason) for every current overlay and historical ledger ID."""
    ledger = []
    with open(root / LEDGER, newline="") as f:
        for row in list(f)[1:]:
            if row.strip():
                ledger.append(row.split("\t", 1)[0])
    note = ""
    try:
        upr = root / UPR_SOURCE
        catalog = overlay_catalog((upr / CATALOG_SOURCE).read_text())
        touched = tweak_setters((upr / SETTINGS_SOURCE).read_text())
    except (OSError, ValueError):
        catalog, touched = {}, set()
        note = "UPR-FVX source unavailable: every ID is NEEDS_REVIEW."
    single = {o.feature: o.id for o in SINGLE_OPTIONS}
    pilot = {STARTER: "M01", WILD: "M02", TRAINER: "M03"}
    rows = {}
    for fid in list(catalog) + [i for i in ledger if i not in catalog]:
        body = catalog.get(fid)
        setters = set(re.findall(r"\bs\.(set\w+)\(", body or ""))
        if fid in GUARDED:
            rows[fid] = ("GUARDED", GUARDED[fid])
        elif body is None:
            rows[fid] = ("NEEDS_REVIEW", "historical ledger ID without current overlay")
        elif body.startswith("unsupported("):
            rows[fid] = ("UNSUPPORTED", "settings-profile refuses this overlay")
        elif fid in single:
            rows[fid] = ("EXECUTABLE", "--single " + single[fid])
        elif fid in pilot:
            rows[fid] = ("EXECUTABLE", "--matrix " + pilot[fid]
                         + ("; tweakForRom touches " + ",".join(sorted(setters & touched)) if setters & touched else ""))
        elif not setters or "::" in body or re.search(r"(?<![.\w])[a-z]\w*\(s\b", body):
            rows[fid] = ("NEEDS_REVIEW", "overlay uses a helper; target normalization not source-checked")
        elif setters & touched:
            rows[fid] = ("NEEDS_REVIEW", "tweakForRom may normalize " + ",".join(sorted(setters & touched)))
        else:
            rows[fid] = ("NOT_RUN", "overlay exists; no executable case yet")
    return rows, note


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
        if run.returncode and LEARNSET_GUARD in text and untouched:
            res.status, res.detail = "EXPECTED_REJECTION", "learnset guard, no output"
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
    for case, state in zip(cases, observe(jar, temp, paths)):
        check_case_settings(base_state, case, state)
    return base_state, paths


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
    target_base, *targets = observe(jar, temp, [baseline, *paths], rom=rom)
    if gm.input_digest(rom) != digest:
        raise MatrixError("Source ROM changed during target normalization; STOP.")
    for case, state in zip(cases, targets):
        expected = expected_state(target_base, case)
        drift = sorted(k for k in expected.keys() | state.keys() if state.get(k) != expected.get(k))
        results[case.id].target = "NEEDS_REVIEW" if drift else "PASS"
        if drift:
            results[case.id].status = "NEEDS_REVIEW"
            results[case.id].detail = "tweakForRom changed " + ",".join(drift)
    for case, settings in zip(cases, paths):
        if results[case.id].target != "PASS":
            continue    # Never generated: its effect would not reach the ROM as configured.
        directory = out / case.id
        directory.mkdir()
        res, output = generate(case, rom, jar, settings, directory, digest)
        res.target = "PASS"
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
    parser = SafeParser(description="#743/#748 USER-ONLY pilot settings matrix and single options.")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--plan", action="store_true", help="list cases; reads nothing")
    action.add_argument("--self-test", action="store_true", help="synthetic mock tests only")
    action.add_argument("--matrix", action="store_true", help="real local run (needs --confirm)")
    action.add_argument("--single", action="store_true", help="real local single-option run (needs --confirm)")
    parser.add_argument("--select", help="--single: comma-separated feature IDs from --plan, or all")
    parser.add_argument("--confirm", help="must be " + CONFIRM_TOKEN + " for --matrix/--single")
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
        mode = "--single" if args.single else "--matrix"
        if args.confirm != CONFIRM_TOKEN:
            raise MatrixError(mode + " runs real ROM generation; pass --confirm " + CONFIRM_TOKEN + ".")
        options = select_options(args.select) if args.single else None
        if not (args.rom and args.baseline and args.out):
            raise MatrixError(mode + " requires --rom, --baseline and --out.")
        rom, baseline = Path(args.rom).resolve(), Path(args.baseline).resolve()
        jar = Path(args.jar).resolve() if args.jar else DEFAULT_JAR
        if not rom.is_file() or not baseline.is_file() or not jar.is_file():
            raise MatrixError("ROM, baseline or JAR not found; the JAR is never built here.")
        title = "#748 single-option matrix" if args.single else "#743 pilot settings matrix"
        header = [title + (" (REVISION DRIFT ALLOWED)" if args.allow_revision_drift else "")]
        header += revision_lines(ROOT, jar, args.allow_revision_drift)
        out = output_root(args.out, ROOT)
        print("\n".join(header), flush=True)
        with tempfile.TemporaryDirectory(prefix="pilot-matrix-") as temp:
            if args.single:
                results = run_single(rom, baseline, jar, out, Path(temp), options)
            else:
                results = run_matrix(rom, baseline, jar, out, Path(temp))
        lines, overall = single_report_lines(results, options) if args.single else report_lines(results)
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
