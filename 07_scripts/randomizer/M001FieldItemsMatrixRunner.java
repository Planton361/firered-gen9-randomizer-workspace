import com.uprfvx.random.GameRandomizer;
import com.uprfvx.random.Settings;
import com.uprfvx.romio.constants.Gen3Constants;
import com.uprfvx.romio.gamedata.Item;
import com.uprfvx.romio.romhandlers.Gen3RomHandler;
import com.uprfvx.romio.romhandlers.RomHandler;
import com.uprfvx.romio.romhandlers.romentries.Gen3RomEntry;
import com.uprfvx.romio.romio.RomOpener;

import java.io.OutputStream;
import java.io.PrintStream;
import java.lang.reflect.Field;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;
import java.util.Set;

/**
 * Workspace-side, sanitized single-row runner for the M-001 Field Items matrix.
 * It deliberately emits only the ten acceptance fields consumed by the Python wrapper.
 */
public final class M001FieldItemsMatrixRunner {
    private static final ResourceBundle BUNDLE = ResourceBundle.getBundle("com/uprfvx/random/gui/Bundle");

    private M001FieldItemsMatrixRunner() {
    }

    public static void main(String[] args) {
        Arguments arguments = Arguments.parse(args);
        Result result = new Result(arguments.mode, arguments.banBad);
        try {
            RowState before = loadCandidate(arguments.inputRom, result);
            if (before == null) {
                finish(result);
                return;
            }

            result.candidateLoaded = before.cfruDpeMode
                    && "BPRE".equals(before.handler.getRomEntry().getRomCode());
            if (!result.candidateLoaded) {
                finish(result);
                return;
            }

            Snapshot original = Snapshot.capture(before);
            Settings settings = new Settings();
            settings.setFieldItemsMod(arguments.mode.settingsMode);
            settings.setBanBadRandomFieldItems(arguments.banBad);
            GameRandomizer.Results randomization = new GameRandomizer(settings, null, before.handler, BUNDLE, false)
                    .randomize(arguments.outputRom.toString(), new PrintStream(OutputStream.nullOutputStream()), 1001L);
            result.saveSuccessful = randomization.wasSaveSuccessful();
            if (!result.saveSuccessful) {
                finish(result);
                return;
            }

            Snapshot saved = Snapshot.capture(before);
            RowState reloaded = loadCandidate(arguments.outputRom, result);
            if (reloaded == null || !reloaded.cfruDpeMode
                    || !"BPRE".equals(reloaded.handler.getRomEntry().getRomCode())) {
                finish(result);
                return;
            }
            Snapshot after = Snapshot.capture(reloaded);
            result.reloadSuccessful = true;
            result.rawApiTmSlotAlignmentMismatches = after.rawApiTmAlignmentMismatches();
            result.tmFieldItemSlotMismatches = typeMismatches(original.apiItems, after.apiItems, true);
            result.nonTmFieldItemSlotMismatches = typeMismatches(original.apiItems, after.apiItems, false);
            result.requiredFieldTMMissingAfter = requiredMissing(after.handler, after.apiItems);
            result.fieldItemReloadMismatches = itemMismatches(saved.apiItems, after.apiItems);
            result.lowByte92Discovery = after.lowByte92Discovery();
        } catch (Exception ignored) {
            // Private ROM details and stack traces must never escape this harness.
        }
        finish(result);
    }

    private static RowState loadCandidate(Path rom, Result result) throws Exception {
        RomOpener.Results opened = new RomOpener().openRomFile(rom.toFile());
        if (!opened.wasOpeningSuccessful() || !(opened.getRomHandler() instanceof Gen3RomHandler handler)) {
            return null;
        }
        return new RowState(handler, cfruDpeMode(handler));
    }

    private static boolean cfruDpeMode(Gen3RomHandler handler) throws ReflectiveOperationException {
        Field field = Gen3RomHandler.class.getDeclaredField("useCfruDpeGen9SpeciesCount");
        field.setAccessible(true);
        return field.getBoolean(handler);
    }

    private static int typeMismatches(List<Item> before, List<Item> after, boolean tm) {
        int mismatches = Math.abs(before.size() - after.size());
        for (int index = 0; index < Math.min(before.size(), after.size()); index++) {
            if (before.get(index).isTM() == tm && after.get(index).isTM() != tm) {
                mismatches++;
            }
        }
        return mismatches;
    }

    private static int itemMismatches(List<Item> saved, List<Item> reloaded) {
        int mismatches = Math.abs(saved.size() - reloaded.size());
        for (int index = 0; index < Math.min(saved.size(), reloaded.size()); index++) {
            if (!saved.get(index).equals(reloaded.get(index))) {
                mismatches++;
            }
        }
        return mismatches;
    }

    private static int requiredMissing(Gen3RomHandler handler, List<Item> items) {
        Set<Item> required = handler.getRequiredFieldTMs();
        int missing = 0;
        for (Item item : required) {
            if (!items.contains(item)) {
                missing++;
            }
        }
        return missing;
    }

    private static void finish(Result result) {
        System.out.println("mode=" + result.mode.label);
        System.out.println("banBad=" + (result.banBad ? "on" : "off"));
        System.out.println("candidateLoaded=" + result.candidateLoaded);
        System.out.println("saveSuccessful=" + result.saveSuccessful);
        System.out.println("reloadSuccessful=" + result.reloadSuccessful);
        System.out.println("rawApiTmSlotAlignmentMismatches=" + result.rawApiTmSlotAlignmentMismatches);
        System.out.println("tmFieldItemSlotMismatches=" + result.tmFieldItemSlotMismatches);
        System.out.println("nonTmFieldItemSlotMismatches=" + result.nonTmFieldItemSlotMismatches);
        System.out.println("requiredFieldTMMissingAfter=" + result.requiredFieldTMMissingAfter);
        System.out.println("fieldItemReloadMismatches=" + result.fieldItemReloadMismatches);
        System.out.println("lowByte92Discovery=" + result.lowByte92Discovery);
    }

    private enum Mode {
        UNCHANGED("unchanged", Settings.FieldItemsMod.UNCHANGED),
        SHUFFLE("shuffle", Settings.FieldItemsMod.SHUFFLE),
        RANDOM("random", Settings.FieldItemsMod.RANDOM),
        RANDOM_EVEN("random-even", Settings.FieldItemsMod.RANDOM_EVEN);

        private final String label;
        private final Settings.FieldItemsMod settingsMode;

        Mode(String label, Settings.FieldItemsMod settingsMode) {
            this.label = label;
            this.settingsMode = settingsMode;
        }

        static Mode parse(String value) {
            for (Mode mode : values()) {
                if (mode.label.equals(value)) {
                    return mode;
                }
            }
            throw new IllegalArgumentException("Unsupported mode.");
        }
    }

    private record Arguments(Path inputRom, Path outputRom, Mode mode, boolean banBad) {
        static Arguments parse(String[] args) {
            Path input = null;
            Path output = null;
            Mode mode = null;
            Boolean banBad = null;
            for (int index = 0; index < args.length; index++) {
                if (index + 1 >= args.length) {
                    throw new IllegalArgumentException("Missing runner argument value.");
                }
                switch (args[index]) {
                    case "--input" -> input = Path.of(args[++index]);
                    case "--output" -> output = Path.of(args[++index]);
                    case "--mode" -> mode = Mode.parse(args[++index]);
                    case "--ban-bad" -> banBad = "on".equals(args[++index]);
                    default -> throw new IllegalArgumentException("Unsupported runner argument.");
                }
            }
            if (input == null || output == null || mode == null || banBad == null) {
                throw new IllegalArgumentException("Missing required runner argument.");
            }
            return new Arguments(input, output, mode, banBad);
        }
    }

    private static final class Result {
        private final Mode mode;
        private final boolean banBad;
        private boolean candidateLoaded;
        private boolean saveSuccessful;
        private boolean reloadSuccessful;
        private int rawApiTmSlotAlignmentMismatches = -1;
        private int tmFieldItemSlotMismatches = -1;
        private int nonTmFieldItemSlotMismatches = -1;
        private int requiredFieldTMMissingAfter = -1;
        private int fieldItemReloadMismatches = -1;
        private boolean lowByte92Discovery;

        Result(Mode mode, boolean banBad) {
            this.mode = mode;
            this.banBad = banBad;
        }
    }

    private record RowState(Gen3RomHandler handler, boolean cfruDpeMode) {
    }

    private static final class Snapshot {
        private final Gen3RomHandler handler;
        private final List<Item> apiItems;
        private final List<RawSlot> rawItems;

        private Snapshot(Gen3RomHandler handler, List<Item> apiItems, List<RawSlot> rawItems) {
            this.handler = handler;
            this.apiItems = apiItems;
            this.rawItems = rawItems;
        }

        static Snapshot capture(RowState state) throws Exception {
            List<Item> api = new ArrayList<>(state.handler.getFieldItems());
            List<RawSlot> raw = RawFieldItems.scan(state.handler, state.cfruDpeMode);
            return new Snapshot(state.handler, api, raw);
        }

        int rawApiTmAlignmentMismatches() {
            List<RawSlot> rawApiSlots = rawItems.stream().filter(RawSlot::apiSlot).toList();
            int mismatches = Math.abs(rawApiSlots.size() - apiItems.size());
            for (int index = 0; index < Math.min(rawApiSlots.size(), apiItems.size()); index++) {
                if (rawApiSlots.get(index).item.isTM() != apiItems.get(index).isTM()) {
                    mismatches++;
                }
            }
            return mismatches;
        }

        boolean lowByte92Discovery() {
            return rawItems.stream().anyMatch(RawSlot::lowByte92);
        }
    }

    private record RawSlot(Item item, boolean apiSlot, boolean lowByte92) {
    }

    /** Mirrors the current Gen3 Field Items reader only to observe its complete raw slot set. */
    private static final class RawFieldItems {
        private static List<RawSlot> scan(Gen3RomHandler handler, boolean cfruDpeMode) throws Exception {
            byte[] rom = Files.readAllBytes(Path.of(handler.loadedFilename()));
            Gen3RomEntry entry = handler.getRomEntry();
            List<Item> items = handler.getItems();
            List<RawSlot> found = new ArrayList<>();
            int mapHeaders = entry.getIntValue("MapHeaders");
            int itemBallLowByte = entry.getIntValue("ItemBallPic") & 0xFF;
            int bankCount = entry.getIntValue("MapBankCount");
            int[] mapsPerBank = entry.getArrayValue("MapBankSizes");

            for (int bank = 0; bank < bankCount; bank++) {
                int bankPointer = pointer(rom, mapHeaders + bank * 4);
                for (int map = 0; map < mapsPerBank[bank]; map++) {
                    int mapHeader = pointer(rom, bankPointer + map * 4);
                    int events = pointerOrNegative(rom, mapHeader + 4);
                    if (events < 0) {
                        continue;
                    }
                    int peopleCount = unsigned(rom, events);
                    int signpostCount = unsigned(rom, events + 3);
                    if (peopleCount > 0) {
                        int people = pointer(rom, events + 4);
                        for (int person = 0; person < peopleCount; person++) {
                            int personOffset = people + person * 24;
                            int script = pointerOrNegative(rom, personOffset + 16);
                            int spriteLowByte = unsigned(rom, personOffset + 1);
                            if (spriteLowByte == itemBallLowByte && script >= 0 && itemBallScript(rom, script)) {
                                found.add(slot(items, word(rom, script + 3), cfruDpeMode, spriteLowByte == 92));
                            }
                        }
                    }
                    if (signpostCount > 0) {
                        int signposts = pointer(rom, events + 16);
                        for (int signpost = 0; signpost < signpostCount; signpost++) {
                            int signpostOffset = signposts + signpost * 12;
                            int type = unsigned(rom, signpostOffset + 5);
                            int item = word(rom, signpostOffset + 8);
                            if (type >= 5 && type <= 7 && item != 0) {
                                found.add(slot(items, item, cfruDpeMode, false));
                            }
                        }
                    }
                }
            }
            return found;
        }

        private static RawSlot slot(List<Item> items, int internalId, boolean cfruDpeMode, boolean lowByte92) {
            int id = Gen3Constants.itemIDToStandard(internalId);
            Item item = id >= 0 && id < items.size() ? items.get(id) : null;
            boolean apiSlot = item != null && (item.isAllowed() || (cfruDpeMode && item.isTM()));
            return new RawSlot(item, apiSlot, lowByte92);
        }

        private static boolean itemBallScript(byte[] rom, int script) {
            return inBounds(rom, script, 12)
                    && unsigned(rom, script) == 0x1A && unsigned(rom, script + 1) == 0
                    && unsigned(rom, script + 2) == 0x80 && unsigned(rom, script + 5) == 0x1A
                    && unsigned(rom, script + 6) == 1 && unsigned(rom, script + 7) == 0x80
                    && unsigned(rom, script + 10) == 0x09
                    && (unsigned(rom, script + 11) == 0 || unsigned(rom, script + 11) == 1);
        }

        private static int pointer(byte[] rom, int offset) {
            int value = pointerOrNegative(rom, offset);
            if (value < 0) {
                throw new IllegalArgumentException("Invalid map pointer.");
            }
            return value;
        }

        private static int pointerOrNegative(byte[] rom, int offset) {
            if (!inBounds(rom, offset, 4)) {
                return -1;
            }
            int value = (unsigned(rom, offset)) | (unsigned(rom, offset + 1) << 8)
                    | (unsigned(rom, offset + 2) << 16) | (unsigned(rom, offset + 3) << 24);
            int decoded = value - 0x08000000;
            return decoded >= 0 && decoded <= rom.length ? decoded : -1;
        }

        private static int word(byte[] rom, int offset) {
            if (!inBounds(rom, offset, 2)) {
                throw new IllegalArgumentException("Invalid field item read.");
            }
            return unsigned(rom, offset) | (unsigned(rom, offset + 1) << 8);
        }

        private static int unsigned(byte[] rom, int offset) {
            if (!inBounds(rom, offset, 1)) {
                throw new IllegalArgumentException("Invalid field item read.");
            }
            return rom[offset] & 0xFF;
        }

        private static boolean inBounds(byte[] rom, int offset, int length) {
            return offset >= 0 && length >= 0 && offset <= rom.length - length;
        }
    }
}
