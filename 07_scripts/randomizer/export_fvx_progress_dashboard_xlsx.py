#!/usr/bin/env python3
"""Export selected FVX progress dashboard Markdown tables to an XLSX file.

The Markdown dashboard remains the source of truth.  This script intentionally
uses only the Python standard library so it can run without dependency
installation in the workspace.
"""

from __future__ import annotations

import argparse
import re
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


REQUESTED_TABLES = [
    "Gesamtfortschritt nach Feature-Paketen",
    "GUI-Feature-Gruppen",
    "Vollstaendige Feature-Liste",
    "Offene Blocker",
    "Naechste empfohlene Arbeitspakete",
    "Zuletzt abgeschlossene PRs / Diagnosen",
    "Carrier-tested, aber nicht global",
]

SHEET_NAMES = {
    "Gesamtfortschritt nach Feature-Paketen": "Gesamtfortschritt",
    "GUI-Feature-Gruppen": "GUI-Feature-Gruppen",
    "Vollstaendige Feature-Liste": "Vollstaendige Feature-Liste",
    "Offene Blocker": "Offene Blocker",
    "Naechste empfohlene Arbeitspakete": "Naechste Arbeitspakete",
    "Zuletzt abgeschlossene PRs / Diagnosen": "Zuletzt PRs Diagnosen",
    "Carrier-tested, aber nicht global": "Carrier-tested nicht global",
}

STATUS_SORT = {
    "Nicht begonnen": 10,
    "Plan erstellt": 20,
    "Read-only modelliert": 30,
    "Write modelliert / Fix offen": 40,
    "Gefixt, Folgesmokes offen": 50,
    "Getestet": 60,
    "Getestet im Carrier": 70,
    "Supported im getesteten Scope": 80,
    "P1-supported": 90,
    "Guarded / blocked-pending-evidence": 100,
    "Guarded / Preserve-only": 101,
    "Blockiert": 110,
    "P2 / Nicht begonnen": 120,
    "P2 / Out of scope": 130,
}


@dataclass(frozen=True)
class MarkdownTable:
    title: str
    headers: list[str]
    rows: list[list[str]]


def split_markdown_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]

    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in stripped:
        if char == "\\" and not escaped:
            escaped = True
            continue
        if char == "|" and not escaped:
            cells.append("".join(current).strip())
            current = []
            continue
        if escaped:
            current.append("\\")
        current.append(char)
        escaped = False
    if escaped:
        current.append("\\")
    cells.append("".join(current).strip())
    return cells


def is_table_separator(line: str) -> bool:
    cells = split_markdown_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def is_table_row(line: str) -> bool:
    return line.lstrip().startswith("|") and line.rstrip().endswith("|")


def normalize_width(row: list[str], width: int) -> list[str]:
    if len(row) < width:
        return row + [""] * (width - len(row))
    return row[:width]


def parse_markdown_tables(markdown: str) -> dict[str, MarkdownTable]:
    lines = markdown.splitlines()
    tables: dict[str, MarkdownTable] = {}
    current_heading = ""
    index = 0

    while index < len(lines):
        line = lines[index]
        heading = re.match(r"^##+\s+(.+?)\s*$", line)
        if heading:
            current_heading = heading.group(1).strip()
            index += 1
            continue

        if (
            current_heading
            and is_table_row(line)
            and index + 1 < len(lines)
            and is_table_separator(lines[index + 1])
        ):
            headers = split_markdown_row(line)
            rows: list[list[str]] = []
            index += 2
            while index < len(lines) and is_table_row(lines[index]):
                rows.append(normalize_width(split_markdown_row(lines[index]), len(headers)))
                index += 1
            tables[current_heading] = MarkdownTable(current_heading, headers, rows)
            continue

        index += 1

    return tables


def col_name(index: int) -> str:
    result = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def cell_xml(row_index: int, col_index: int, value: object, style: int | None = None) -> str:
    ref = f"{col_name(col_index)}{row_index}"
    attrs = f' r="{ref}"'
    if style is not None:
        attrs += f' s="{style}"'
    if isinstance(value, int | float):
        return f"<c{attrs}><v>{value}</v></c>"
    attrs += ' t="inlineStr"'
    text = escape(str(value), {'"': "&quot;"})
    return f"<c{attrs}><is><t>{text}</t></is></c>"


def worksheet_xml(rows: list[list[object]], autofilter: bool = True) -> str:
    xml_rows: list[str] = []
    max_width = max((len(row) for row in rows), default=1)
    for row_index, row in enumerate(rows, start=1):
        cells = [
            cell_xml(row_index, col_index, value, 1 if row_index == 1 else None)
            for col_index, value in enumerate(row, start=1)
        ]
        xml_rows.append(f'<row r="{row_index}">{"".join(cells)}</row>')

    dimension = f"A1:{col_name(max_width)}{max(len(rows), 1)}"
    filter_xml = f'<autoFilter ref="A1:{col_name(max_width)}{len(rows)}"/>' if autofilter and len(rows) > 1 else ""
    cols_xml = "".join(f'<col min="{i}" max="{i}" width="22" customWidth="1"/>' for i in range(1, max_width + 1))
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<dimension ref="{dimension}"/>'
        '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" '
        'activePane="bottomLeft" state="frozen"/><selection pane="bottomLeft"/></sheetView></sheetViews>'
        f"<cols>{cols_xml}</cols>"
        f'<sheetData>{"".join(xml_rows)}</sheetData>'
        f"{filter_xml}"
        "</worksheet>"
    )


def workbook_xml(sheet_names: list[str]) -> str:
    sheets = "".join(
        f'<sheet name="{escape(name, {"\"": "&quot;"})}" sheetId="{index}" r:id="rId{index}"/>'
        for index, name in enumerate(sheet_names, start=1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f"<sheets>{sheets}</sheets>"
        "</workbook>"
    )


def workbook_rels_xml(sheet_count: int) -> str:
    rels = [
        (
            f'<Relationship Id="rId{index}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
            f'Target="worksheets/sheet{index}.xml"/>'
        )
        for index in range(1, sheet_count + 1)
    ]
    rels.append(
        f'<Relationship Id="rId{sheet_count + 1}" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
        'Target="styles.xml"/>'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{"".join(rels)}'
        "</Relationships>"
    )


def content_types_xml(sheet_count: int) -> str:
    overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{index}.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for index in range(1, sheet_count + 1)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/xl/workbook.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        '<Override PartName="/xl/styles.xml" '
        'ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
        f"{overrides}"
        "</Types>"
    )


def root_rels_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
        'Target="xl/workbook.xml"/>'
        "</Relationships>"
    )


def styles_xml() -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
        '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
        '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
        '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
        '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
        '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
        '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>'
        '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
        "</styleSheet>"
    )


def write_xlsx(output: Path, sheets: list[tuple[str, list[list[object]], bool]]) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet_names = [name for name, _rows, _autofilter in sheets]
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", content_types_xml(len(sheets)))
        archive.writestr("_rels/.rels", root_rels_xml())
        archive.writestr("xl/workbook.xml", workbook_xml(sheet_names))
        archive.writestr("xl/_rels/workbook.xml.rels", workbook_rels_xml(len(sheets)))
        archive.writestr("xl/styles.xml", styles_xml())
        for index, (_name, rows, autofilter) in enumerate(sheets, start=1):
            archive.writestr(f"xl/worksheets/sheet{index}.xml", worksheet_xml(rows, autofilter))


def rows_for_table(table: MarkdownTable) -> list[list[object]]:
    return [table.headers, *table.rows]


def rows_with_status_sort(table: MarkdownTable) -> list[list[object]]:
    try:
        status_index = table.headers.index("Dashboard-Status")
    except ValueError as exc:
        raise SystemExit("Missing Dashboard-Status column in Vollstaendige Feature-Liste.") from exc

    insert_index = status_index + 1
    headers: list[object] = [*table.headers[:insert_index], "StatusSort", *table.headers[insert_index:]]
    rows: list[list[object]] = [headers]
    for row in table.rows:
        status = row[status_index]
        sort_value = STATUS_SORT.get(status, 999)
        rows.append([*row[:insert_index], sort_value, *row[insert_index:]])
    return rows


def summary_rows(input_path: Path, export_time: str, feature_count: int, blocker_count: int) -> list[list[object]]:
    return [
        ["Feld", "Wert"],
        ["Input-Datei", str(input_path)],
        ["Export-Zeitpunkt", export_time],
        ["Anzahl Feature-Zeilen", feature_count],
        ["Anzahl Blocker", blocker_count],
        ["Hinweis", "Markdown bleibt Source of Truth."],
    ]


def require_tables(tables: dict[str, MarkdownTable], names: Iterable[str]) -> list[MarkdownTable]:
    missing = [name for name in names if name not in tables]
    if missing:
        missing_text = "\n".join(f"- {name}" for name in missing)
        raise SystemExit(f"Missing required dashboard table(s):\n{missing_text}")
    return [tables[name] for name in names]


def export_dashboard(input_path: Path, output_path: Path) -> None:
    markdown = input_path.read_text(encoding="utf-8")
    parsed_tables = parse_markdown_tables(markdown)
    required_tables = require_tables(parsed_tables, REQUESTED_TABLES)

    feature_count = len(parsed_tables["Vollstaendige Feature-Liste"].rows)
    blocker_count = len(parsed_tables["Offene Blocker"].rows)
    if feature_count != 130:
        raise SystemExit(f"Expected 130 feature rows, found {feature_count}. Refusing to export shortened feature list.")

    export_time = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    sheets: list[tuple[str, list[list[object]], bool]] = [
        ("Summary", summary_rows(input_path, export_time, feature_count, blocker_count), False)
    ]
    for table in required_tables:
        if table.title == "Vollstaendige Feature-Liste":
            rows = rows_with_status_sort(table)
        else:
            rows = rows_for_table(table)
        sheets.append((SHEET_NAMES[table.title], rows, True))

    write_xlsx(output_path, sheets)
    print(f"Wrote {output_path}")
    print(f"Feature rows: {feature_count}")
    print(f"Blockers: {blocker_count}")
    print("Sheets:")
    for sheet_name, _rows, _autofilter in sheets:
        print(f"- {sheet_name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export FVX progress dashboard Markdown tables to XLSX.")
    parser.add_argument("--input", required=True, type=Path, help="Path to fvx-progress-dashboard.md")
    parser.add_argument("--output", required=True, type=Path, help="Path to write the .xlsx file")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    export_dashboard(args.input, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
