#!/bin/sh
set -eu

usage() {
    cat <<'USAGE'
Usage:
  07_scripts/randomizer/generate_cli_smoke_profiles.sh --output <manifest.tsv>

Optional:
  --settings-dir <local-settings-dir>   Default: 05_builds/randomizer-smoke/cli-profile-matrix/settings
  --force                               Overwrite an existing manifest.
  -h, --help                            Show this help.

This scaffold does not modify FVX settings files. Current FVX .rnqs/settings
data is versioned Base64 plus CRC/checksum state, so repo shell scripts should
not byte-patch it. Create or export the real profile settings locally, then use
the generated manifest with run_cli_profile_matrix.sh.
USAGE
}

die() {
    printf 'ERROR: %s\n' "$1" >&2
    exit 1
}

output=""
settings_dir="05_builds/randomizer-smoke/cli-profile-matrix/settings"
force="no"

while [ "$#" -gt 0 ]; do
    case "$1" in
        --output)
            [ "$#" -ge 2 ] || die "Missing value for --output"
            output=$2
            shift 2
            ;;
        --settings-dir)
            [ "$#" -ge 2 ] || die "Missing value for --settings-dir"
            settings_dir=$2
            shift 2
            ;;
        --force)
            force="yes"
            shift
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            die "Unknown argument: $1"
            ;;
    esac
done

[ -n "$output" ] || die "Missing --output"
if [ -e "$output" ] && [ "$force" != "yes" ]; then
    die "Manifest already exists. Use --force to overwrite."
fi

mkdir -p "$(dirname "$output")"

cat > "$output" <<EOF
profile_id	enabled	expected_result	settings_file	seed	notes
00_baseline	yes	PASS_LOG	${settings_dir}/00_baseline.rnqs	1000	Baseline exported from GUI or future FVX helper.
01_traits_full	yes	PASS_LOG	${settings_dir}/01_traits_full.rnqs	1001	Traits block: base stats, types, abilities; evolution randomization only if intentionally enabled.
02_starters_statics_trades_full	yes	PASS_LOG	${settings_dir}/02_starters_statics_trades_full.rnqs	1002	Starters, statics and trades; Rival Carries Starter remains separate unless intentionally enabled.
03_moves_movesets_full	yes	PASS_LOG	${settings_dir}/03_moves_movesets_full.rnqs	1003	Moves and movesets block.
04_foe_base	yes	PASS_LOG	${settings_dir}/04_foe_base.rnqs	1004	Trainer Pokemon core, trainer movesets and trainer names.
04_foe_held_items_basic	yes	PASS_LOG	${settings_dir}/04_foe_held_items_basic.rnqs	1005	Trainer held items basic.
04_foe_held_items_sensible_expected_fail	yes	EXPECTED_FAIL	${settings_dir}/04_foe_held_items_sensible_expected_fail.rnqs	1006	Known-risk sensible held item profile until local evidence says otherwise.
05_wild_full	yes	PASS_LOG	${settings_dir}/05_wild_full.rnqs	1007	Standard/Fallback Wild only; Special-Wild remains separate.
06_tm_tutor_full	yes	PASS_LOG	${settings_dir}/06_tm_tutor_full.rnqs	1008	TM/HM and Tutor moves/compatibility.
07_items_full	yes	PASS_LOG	${settings_dir}/07_items_full.rnqs	1009	Field, shop and pickup items.
08_types_full	yes	PASS_WITH_WARNINGS	${settings_dir}/08_types_full.rnqs	1010	Type effectiveness chaos profile; warnings acceptable if no fatal/bad markers.
09_graphics_palettes	yes	EXPECTED_FAIL	${settings_dir}/09_graphics_palettes.rnqs	1011	Palette/graphics profile remains risky/P2 until separately fixed.
10_misc_tweaks	yes	EXPECTED_FAIL	${settings_dir}/10_misc_tweaks.rnqs	1012	Misc tweaks inventory profile; not stable yet.
11_special_wild	yes	EXPECTED_FAIL	${settings_dir}/11_special_wild.rnqs	1013	Special-Wild/Day-Night/Swarms remain out-of-scope.
EOF

printf 'Wrote profile manifest scaffold: %s\n' "$output"
printf 'No FVX settings files were generated or modified.\n'
