#!/bin/sh
set -eu

usage() {
    cat <<'USAGE'
Usage:
  07_scripts/randomizer/cli_log_smoke_pipeline.sh \
    --rom <private-input.gba> \
    --settings-file <settings.rnqs-or-settings-file> \
    --output-rom <local-output.gba> \
    --report <sanitized-report.md>

Optional:
  --settings-string <settings-string>   Use only for local ad-hoc runs; settings files are safer.
  --jar <UPR-FVX.jar>                   Default: 02_external/upr-fvx/random/build/libs/UPR-FVX.jar
  --seed <long>                         Forwarded to UPR-FVX as -z.
  --stdout-log <local-cli-stdout.log>   Default: temporary file under /tmp.
  --dry-run                             Validate and print a redacted execution plan without running.
  -h, --help                            Show this help.

This script is an opt-in local helper. It must not be run by Codex with a ROM.
It writes only a sanitized summary report. Raw CLI stdout and UPR-FVX detailed
logs stay local and must not be committed.
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

bool_file_exists() {
    if [ -s "$1" ]; then
        printf 'yes'
    else
        printf 'no'
    fi
}

count_matches() {
    pattern=$1
    file=$2
    if [ -s "$file" ]; then
        grep -E -c "$pattern" "$file" 2>/dev/null || true
    else
        printf '0\n'
    fi
}

append_snippets() {
    title=$1
    pattern=$2
    file=$3
    report=$4

    {
        printf '\n### %s\n\n' "$title"
        if [ -s "$file" ] && grep -E "$pattern" "$file" >/dev/null 2>&1; then
            grep -E "$pattern" "$file" | head -n 20 | sanitize_line | sed 's/^/- /'
        else
            printf 'None observed.\n'
        fi
    } >> "$report"
}

jar="02_external/upr-fvx/random/build/libs/UPR-FVX.jar"
rom=""
settings_file=""
settings_string=""
output_rom=""
report=""
seed=""
stdout_log=""
dry_run="no"

while [ "$#" -gt 0 ]; do
    case "$1" in
        --jar)
            [ "$#" -ge 2 ] || die "Missing value for --jar"
            jar=$2
            shift 2
            ;;
        --rom)
            [ "$#" -ge 2 ] || die "Missing value for --rom"
            rom=$2
            shift 2
            ;;
        --settings-file)
            [ "$#" -ge 2 ] || die "Missing value for --settings-file"
            settings_file=$2
            shift 2
            ;;
        --settings-string)
            [ "$#" -ge 2 ] || die "Missing value for --settings-string"
            settings_string=$2
            shift 2
            ;;
        --output-rom)
            [ "$#" -ge 2 ] || die "Missing value for --output-rom"
            output_rom=$2
            shift 2
            ;;
        --report)
            [ "$#" -ge 2 ] || die "Missing value for --report"
            report=$2
            shift 2
            ;;
        --seed)
            [ "$#" -ge 2 ] || die "Missing value for --seed"
            seed=$2
            shift 2
            ;;
        --stdout-log)
            [ "$#" -ge 2 ] || die "Missing value for --stdout-log"
            stdout_log=$2
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

[ -n "$rom" ] || die "Missing --rom"
[ -n "$output_rom" ] || die "Missing --output-rom"
[ -n "$report" ] || die "Missing --report"

if [ -n "$settings_file" ] && [ -n "$settings_string" ]; then
    die "Use either --settings-file or --settings-string, not both"
fi
[ -n "$settings_file$settings_string" ] || die "Missing --settings-file or --settings-string"

if [ "$dry_run" = "yes" ]; then
    printf 'CLI log smoke dry run:\n'
    printf -- '- jar: %s\n' "$(printf '%s\n' "$jar" | sanitize_line)"
    printf -- '- input ROM: <redacted>\n'
    printf -- '- output ROM: <redacted>\n'
    if [ -n "$settings_file" ]; then
        printf -- '- settings: file\n'
    else
        printf -- '- settings: string\n'
    fi
    printf -- '- report: %s\n' "$(printf '%s\n' "$report" | sanitize_line)"
    printf 'No ROM was read and no output was created.\n'
    exit 0
fi

[ -f "$jar" ] || die "UPR-FVX jar not found. Build it locally with ./gradlew :random:jar."
[ -f "$rom" ] || die "Source ROM not found."
if [ -n "$settings_file" ]; then
    [ -f "$settings_file" ] || die "Settings file not found."
fi

report_dir=$(dirname "$report")
output_dir=$(dirname "$output_rom")
mkdir -p "$report_dir" "$output_dir"

cleanup_stdout="no"
if [ -z "$stdout_log" ]; then
    stdout_log=$(mktemp /tmp/upr-fvx-cli-smoke-stdout.XXXXXX.log)
    cleanup_stdout="yes"
else
    mkdir -p "$(dirname "$stdout_log")"
fi

detail_log="${output_rom}.log"
scan_log=$(mktemp /tmp/upr-fvx-cli-smoke-scan.XXXXXX.log)

set +e
if [ -n "$settings_file" ]; then
    if [ -n "$seed" ]; then
        java -jar "$jar" cli -i "$rom" -o "$output_rom" -s "$settings_file" -z "$seed" -l > "$stdout_log" 2>&1
    else
        java -jar "$jar" cli -i "$rom" -o "$output_rom" -s "$settings_file" -l > "$stdout_log" 2>&1
    fi
else
    if [ -n "$seed" ]; then
        java -jar "$jar" cli -i "$rom" -o "$output_rom" -S "$settings_string" -z "$seed" -l > "$stdout_log" 2>&1
    else
        java -jar "$jar" cli -i "$rom" -o "$output_rom" -S "$settings_string" -l > "$stdout_log" 2>&1
    fi
fi
exit_code=$?
set -e

: > "$scan_log"
if [ -s "$stdout_log" ]; then
    cat "$stdout_log" >> "$scan_log"
fi
if [ -s "$detail_log" ]; then
    cat "$detail_log" >> "$scan_log"
fi

success_count=$(count_matches 'Randomized successfully!' "$stdout_log")
fatal_count=$(count_matches 'Exception|ERROR:|Randomization failed|IndexOutOfBoundsException|NullPointerException|NoSuchElementException' "$scan_log")
known_bad_count=$(count_matches 'NEW GIVEN = \?|move-less|missing sprite|unknown/undecoded|SpeciesMovesetRandomizer.*IndexOutOfBoundsException' "$scan_log")

{
    printf '# CLI Log Smoke Report\n\n'
    printf '## Sanitized Summary\n\n'
    printf -- '- UPR-FVX CLI exit code: %s\n' "$exit_code"
    printf -- '- CLI success marker observed: '
    if [ "$success_count" -gt 0 ]; then printf 'yes\n'; else printf 'no\n'; fi
    printf -- '- Output ROM created: %s\n' "$(bool_file_exists "$output_rom")"
    printf -- '- Detailed UPR-FVX log created: %s\n' "$(bool_file_exists "$detail_log")"
    printf -- '- Fatal marker count: %s\n' "$fatal_count"
    printf -- '- Known bad marker count: %s\n' "$known_bad_count"
    printf -- '- ROM path/hash/full log documented: no\n'
    printf -- '- Output path documented: no\n'
    printf -- '- P1 promotion: no\n'
    printf '\n## Scope\n\n'
    printf 'Local opt-in CLI randomization smoke for the currently pinned UPR-FVX jar. '
    printf 'The report records only sanitized pass/fail indicators and marker snippets.\n'
} > "$report"

append_snippets "Fatal Marker Snippets" 'Exception|ERROR:|Randomization failed|IndexOutOfBoundsException|NullPointerException|NoSuchElementException' "$scan_log" "$report"
append_snippets "Known Bad Marker Snippets" 'NEW GIVEN = \?|move-less|missing sprite|unknown/undecoded|SpeciesMovesetRandomizer.*IndexOutOfBoundsException' "$scan_log" "$report"

rm -f "$scan_log"
if [ "$cleanup_stdout" = "yes" ]; then
    rm -f "$stdout_log"
fi

if [ "$exit_code" -ne 0 ]; then
    printf 'CLI log smoke failed: UPR-FVX exited with %s. Sanitized report: %s\n' "$exit_code" "$report" >&2
    exit "$exit_code"
fi
if [ "$success_count" -eq 0 ]; then
    printf 'CLI log smoke failed: success marker was not observed. Sanitized report: %s\n' "$report" >&2
    exit 2
fi
if [ "$fatal_count" -gt 0 ] || [ "$known_bad_count" -gt 0 ]; then
    printf 'CLI log smoke failed: blocked markers were observed. Sanitized report: %s\n' "$report" >&2
    exit 3
fi

printf 'CLI log smoke passed. Sanitized report: %s\n' "$report"
