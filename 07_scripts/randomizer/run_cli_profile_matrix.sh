#!/bin/sh
set -eu

usage() {
    cat <<'USAGE'
Usage:
  07_scripts/randomizer/run_cli_profile_matrix.sh \
    --profile-manifest <profiles.tsv> \
    --rom <private-input.gba> \
    --output-dir <ignored-local-dir> \
    --summary-report <sanitized-summary.md>

Dry-run, no ROM access:
  07_scripts/randomizer/run_cli_profile_matrix.sh \
    --profile-manifest 08_tests/randomizer/cli_profile_matrix.example.tsv \
    --output-dir /tmp/upr-fvx-cli-profile-matrix \
    --summary-report /tmp/upr-fvx-cli-profile-matrix/summary.md \
    --dry-run

Manifest columns:
  profile_id enabled expected_result settings_file seed notes

Optional generator-only column:
  feature_overlays (Feature IDs or MODE-* overlay IDs)

The matrix runner ignores feature_overlays and consumes the generated settings_file.

expected_result:
  PASS_LOG             Profile should pass with zero fatal/bad markers.
  PASS_WITH_WARNINGS   Profile should pass; warning markers are acceptable.
  EXPECTED_FAIL        Profile is expected to fail until fixed or promoted.
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

field_value() {
    field=$1
    file=$2
    if [ -s "$file" ]; then
        grep -E "^- ${field}: " "$file" | head -n 1 | sed "s/^- ${field}: //"
    else
        printf 'n/a'
    fi
}

profile_manifest=""
rom=""
output_dir=""
summary_report=""
smoke_script="07_scripts/randomizer/cli_log_smoke_pipeline.sh"
jar=""
dry_run="no"

while [ "$#" -gt 0 ]; do
    case "$1" in
        --profile-manifest)
            [ "$#" -ge 2 ] || die "Missing value for --profile-manifest"
            profile_manifest=$2
            shift 2
            ;;
        --rom)
            [ "$#" -ge 2 ] || die "Missing value for --rom"
            rom=$2
            shift 2
            ;;
        --output-dir)
            [ "$#" -ge 2 ] || die "Missing value for --output-dir"
            output_dir=$2
            shift 2
            ;;
        --summary-report)
            [ "$#" -ge 2 ] || die "Missing value for --summary-report"
            summary_report=$2
            shift 2
            ;;
        --smoke-script)
            [ "$#" -ge 2 ] || die "Missing value for --smoke-script"
            smoke_script=$2
            shift 2
            ;;
        --jar)
            [ "$#" -ge 2 ] || die "Missing value for --jar"
            jar=$2
            shift 2
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

[ -n "$profile_manifest" ] || die "Missing --profile-manifest"
[ -n "$output_dir" ] || die "Missing --output-dir"
[ -n "$summary_report" ] || die "Missing --summary-report"
[ -f "$profile_manifest" ] || die "Profile manifest not found."
[ -x "$smoke_script" ] || die "Smoke script not executable."

if [ "$dry_run" != "yes" ]; then
    [ -n "$rom" ] || die "Missing --rom for non-dry-run matrix execution"
    [ -f "$rom" ] || die "Source ROM not found."
fi

mkdir -p "$output_dir" "$(dirname "$summary_report")"

{
    printf '# CLI Profile Matrix Summary\n\n'
    printf '## Sanitized Summary\n\n'
    printf -- '- Dry run: %s\n' "$dry_run"
    printf -- '- ROM path/hash/full log documented: no\n'
    printf -- '- Output paths documented: no\n'
    printf -- '- P1 promotion: no\n\n'
    printf '| profile_id | result | bad markers | warnings | next action |\n'
    printf '|---|---|---:|---:|---|\n'
} > "$summary_report"

matrix_exit=0
processed=0

while IFS='	' read -r profile_id enabled expected_result settings_file seed notes feature_overlays; do
    case "$profile_id" in
        ''|\#*) continue ;;
        profile_id) continue ;;
    esac

    [ "$enabled" = "yes" ] || continue
    processed=$((processed + 1))

    profile_dir="${output_dir}/${profile_id}"
    profile_report="${profile_dir}/sanitized-report.md"
    profile_output="${profile_dir}/output.gba"
    mkdir -p "$profile_dir"

    set +e
    if [ "$dry_run" = "yes" ]; then
        if [ -n "$jar" ]; then
            "$smoke_script" --jar "$jar" --rom "${rom:-/tmp/private-input.gba}" --settings-file "$settings_file" \
                --output-rom "$profile_output" --report "$profile_report" --dry-run > "${profile_dir}/dry-run.txt" 2>&1
        else
            "$smoke_script" --rom "${rom:-/tmp/private-input.gba}" --settings-file "$settings_file" \
                --output-rom "$profile_output" --report "$profile_report" --dry-run > "${profile_dir}/dry-run.txt" 2>&1
        fi
        smoke_exit=$?
        fatal_count=0
        bad_count=0
        warning_count=0
    else
        if [ ! -f "$settings_file" ]; then
            smoke_exit=66
        elif [ -n "$jar" ] && [ -n "$seed" ]; then
            "$smoke_script" --jar "$jar" --rom "$rom" --settings-file "$settings_file" \
                --output-rom "$profile_output" --report "$profile_report" --seed "$seed"
            smoke_exit=$?
        elif [ -n "$jar" ]; then
            "$smoke_script" --jar "$jar" --rom "$rom" --settings-file "$settings_file" \
                --output-rom "$profile_output" --report "$profile_report"
            smoke_exit=$?
        elif [ -n "$seed" ]; then
            "$smoke_script" --rom "$rom" --settings-file "$settings_file" \
                --output-rom "$profile_output" --report "$profile_report" --seed "$seed"
            smoke_exit=$?
        else
            "$smoke_script" --rom "$rom" --settings-file "$settings_file" \
                --output-rom "$profile_output" --report "$profile_report"
            smoke_exit=$?
        fi
        fatal_count=$(field_value "Fatal marker count" "$profile_report")
        bad_count=$(field_value "Known bad marker count" "$profile_report")
        warning_count=$(field_value "Warning marker count" "$profile_report")
    fi
    set -e

    if [ "$dry_run" = "yes" ]; then
        result="DRY_RUN"
        next_action="create local settings file and run with private ROM"
    elif [ "$expected_result" = "EXPECTED_FAIL" ]; then
        if [ "$smoke_exit" -eq 0 ]; then
            result="UNEXPECTED_PASS"
            next_action="review caveat; consider changing expected_result after local verification"
            matrix_exit=1
        else
            result="EXPECTED_FAIL"
            next_action="keep blocked or investigate separately"
        fi
    elif [ "$smoke_exit" -eq 0 ]; then
        result="PASS"
        if [ "$expected_result" = "PASS_WITH_WARNINGS" ] && [ "$warning_count" != "0" ]; then
            next_action="warnings accepted for this profile; review snippets"
        else
            next_action="eligible for local boot/play follow-up if desired"
        fi
    else
        result="FAIL"
        next_action="inspect sanitized per-profile report"
        matrix_exit=1
    fi

    safe_profile=$(printf '%s\n' "$profile_id" | sanitize_line)
    safe_action=$(printf '%s\n' "$next_action" | sanitize_line)
    printf '| `%s` | `%s` | %s | %s | %s |\n' "$safe_profile" "$result" "$bad_count" "$warning_count" "$safe_action" >> "$summary_report"
done < "$profile_manifest"

{
    printf '\n## Technical Decision\n\n'
    printf 'The matrix runner consumes saved FVX settings profiles. It does not mutate `.rnqs` files. '
    printf 'FVX settings are versioned Base64 data with CRC/checksum state, so shell byte-patching is intentionally avoided.\n'
    printf '\nProfiles processed: %s\n' "$processed"
} >> "$summary_report"

printf 'CLI profile matrix summary: %s\n' "$summary_report"
exit "$matrix_exit"
