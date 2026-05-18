#!/bin/sh
set -eu

usage() {
    cat <<'USAGE'
Usage:
  07_scripts/randomizer/generate_settings_profiles_from_matrix.sh \
    --upr-dir 02_external/upr-fvx \
    --base-settings <local-base-settings.rnqs> \
    --profile-manifest 08_tests/randomizer/cli_profile_matrix.example.tsv \
    --output-settings-dir <ignored-local-settings-dir>

Optional:
  --force       Overwrite existing generated .rnqs files.
  --dry-run     Print planned generator calls without writing settings files.
  -h, --help    Show this help.

This script only calls:
  java -jar <UPR-FVX.jar> settings-profile ...

It accepts no ROM argument, runs no randomization, and creates no output ROM.

Manifest columns:
  profile_id enabled expected_result settings_file seed notes [feature_overlays]

If feature_overlays is present, it must be a comma-separated Feature-ID list.
Those rows call:
  settings-profile --enable <FEATURE_ID> ...

Rows without feature_overlays continue to call:
  settings-profile --profile <profile_id>
USAGE
}

die() {
    printf 'ERROR: %s\n' "$1" >&2
    exit 1
}

sanitize_line() {
    sed -E \
        -e 's#[A-Za-z]:\\[^[:space:]]+#<path>#g' \
        -e 's#/(home|Users|tmp|var|mnt|media)/[^[:space:]]+#<path>#g' \
        -e 's#[0-9a-fA-F]{32,}#<hash>#g'
}

upr_dir=""
base_settings=""
profile_manifest=""
output_settings_dir=""
force="no"
dry_run="no"

while [ "$#" -gt 0 ]; do
    case "$1" in
        --upr-dir)
            [ "$#" -ge 2 ] || die "Missing value for --upr-dir"
            upr_dir=$2
            shift 2
            ;;
        --base-settings)
            [ "$#" -ge 2 ] || die "Missing value for --base-settings"
            base_settings=$2
            shift 2
            ;;
        --profile-manifest)
            [ "$#" -ge 2 ] || die "Missing value for --profile-manifest"
            profile_manifest=$2
            shift 2
            ;;
        --output-settings-dir)
            [ "$#" -ge 2 ] || die "Missing value for --output-settings-dir"
            output_settings_dir=$2
            shift 2
            ;;
        --force)
            force="yes"
            shift
            ;;
        --dry-run)
            dry_run="yes"
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

[ -n "$upr_dir" ] || die "Missing --upr-dir"
[ -n "$base_settings" ] || die "Missing --base-settings"
[ -n "$profile_manifest" ] || die "Missing --profile-manifest"
[ -n "$output_settings_dir" ] || die "Missing --output-settings-dir"

[ -d "$upr_dir" ] || die "UPR-FVX directory not found."
[ -f "$profile_manifest" ] || die "Profile manifest not found."

jar_path="${upr_dir%/}/random/build/libs/UPR-FVX.jar"
[ -f "$jar_path" ] || die "UPR-FVX jar not found. Build it with: git -C <upr-dir> ... && ./gradlew :random:jar"

if [ "$dry_run" != "yes" ]; then
    [ -f "$base_settings" ] || die "Base settings file not found."
    mkdir -p "$output_settings_dir"
fi

processed=0
generated=0

while IFS='	' read -r profile_id enabled expected_result settings_file seed notes feature_overlays; do
    case "$profile_id" in
        ''|\#*) continue ;;
        profile_id) continue ;;
    esac

    [ "$enabled" = "yes" ] || continue
    processed=$((processed + 1))
    output_settings="${output_settings_dir%/}/${profile_id}.rnqs"

    if [ -e "$output_settings" ] && [ "$force" != "yes" ] && [ "$dry_run" != "yes" ]; then
        die "Output settings already exist for ${profile_id}. Use --force to overwrite."
    fi

    if [ "$dry_run" = "yes" ]; then
        safe_profile=$(printf '%s\n' "$profile_id" | sanitize_line)
        safe_features=$(printf '%s\n' "${feature_overlays:-}" | sanitize_line)
        if [ -n "${feature_overlays:-}" ]; then
            printf 'Would generate profile: %s from features: %s\n' "$safe_profile" "$safe_features"
        else
            printf 'Would generate profile: %s\n' "$safe_profile"
        fi
        continue
    fi

    if [ -n "${feature_overlays:-}" ]; then
        set -- java -jar "$jar_path" settings-profile \
            --base-settings "$base_settings" \
            --output-settings "$output_settings"
        old_ifs=$IFS
        IFS=','
        for feature_id in $feature_overlays; do
            set -- "$@" --enable "$feature_id"
        done
        IFS=$old_ifs
        "$@" >/dev/null
    else
        java -jar "$jar_path" settings-profile \
            --base-settings "$base_settings" \
            --output-settings "$output_settings" \
            --profile "$profile_id" >/dev/null
    fi
    generated=$((generated + 1))
done < "$profile_manifest"

printf 'Profiles processed: %s\n' "$processed"
printf 'Settings profiles generated: %s\n' "$generated"
printf 'ROM path/hash/full log documented: no\n'
printf 'Output ROM created: no\n'
