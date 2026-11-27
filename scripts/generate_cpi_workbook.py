"""Generate a user-facing master CpiDataset.xlsx from all frontend datasets and sync to public/data."""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.worksheet.worksheet import Worksheet

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "src" / "assets" / "data"
DETAILED_DIR = DATA_DIR / "detailed"
RAW_XLSX = ROOT_DIR / "src" / "raw_data" / "CpiDataset.xlsx"
RAW_BACKUP_XLSX = ROOT_DIR / "src" / "raw_data" / "CpiDataset_legacy_backup.xlsx"
PUBLIC_XLSX = ROOT_DIR / "public" / "data" / "CpiDataset.xlsx"

CPI_2D_FIELDS: list[tuple[str, str]] = [
    ("total", "Overall CPI"),
    ("food", "01 Food & Beverages"),
    ("alcoholTobacco", "02 Alcoholic Beverages & Tobacco"),
    ("clothing", "03 Clothing & Footwear"),
    ("housing", "04 Housing, Water, Electricity, Gas & Other Fuels"),
    ("furnishing", "05 Furnishings, Household Equipment & Routine Maint."),
    ("health", "06 Health"),
    ("transport", "07 Transport"),
    ("communication", "08 Information & Communication"),
    ("recreative", "09 Recreation, Sport & Culture"),
    ("education", "10 Education"),
    ("restaurantHotels", "11 Restaurant & Accommodation Services"),
    ("insurance", "12 Insurance & Financial Services"),
    ("misc", "13 Personal Care, Social Protection & Misc."),
]

STATE_DISPLAY_NAMES: list[tuple[str, str]] = [
    ("Johor", "Johor"),
    ("Kedah", "Kedah"),
    ("Kelantan", "Kelantan"),
    ("Melaka", "Melaka"),
    ("NegeriSembilan", "Negeri Sembilan"),
    ("Pahang", "Pahang"),
    ("Perak", "Perak"),
    ("Perlis", "Perlis"),
    ("PulauPinang", "Pulau Pinang"),
    ("Sabah", "Sabah"),
    ("Sarawak", "Sarawak"),
    ("Selangor", "Selangor"),
    ("Terengganu", "Terengganu"),
    ("KualaLumpur", "W.P. Kuala Lumpur"),
    ("Labuan", "W.P. Labuan"),
    ("Putrajaya", "W.P. Putrajaya"),
]

LEVEL_NAMES: dict[int, str] = {
    3: "Group (3D)",
    4: "Class (4D)",
    5: "Subclass (5D)",
}

# Shared reusable styles (created once for speed and clean XML output)
FONT_TITLE = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
FONT_SUBTITLE = Font(name="Calibri", size=10, italic=True, color="1E3A8A")
FONT_HEADER = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
FONT_BODY = Font(name="Calibri", size=10, color="111827")
FONT_BODY_BOLD = Font(name="Calibri", size=10, bold=True, color="111827")
FONT_MUTED = Font(name="Calibri", size=10, color="6B7280")
FONT_SECTION = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
FONT_OVERALL = Font(name="Calibri", size=10, bold=True, color="1E3A8A")
FONT_LINK = Font(name="Calibri", size=10, bold=True, color="1D4ED8", underline="single")
FONT_URL = Font(name="Calibri", size=10, color="1D4ED8", underline="single")

FILL_NAVY = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
FILL_SUBTITLE = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")
FILL_ZEBRA = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
FILL_WHITE = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
FILL_OVERALL = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid")
FILL_INFO_LABEL = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

THIN_SIDE = Side(style="thin", color="E2E8F0")
HEADER_BOTTOM = Side(style="medium", color="1E3A8A")
BORDER_DATA = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=THIN_SIDE)
BORDER_HEADER = Border(left=THIN_SIDE, right=THIN_SIDE, top=THIN_SIDE, bottom=HEADER_BOTTOM)

ALIGN_LEFT = Alignment(horizontal="left", vertical="center")
ALIGN_LEFT_WRAP = Alignment(horizontal="left", vertical="center", wrap_text=True)
ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
ALIGN_HEADER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def parse_ts_object(path: Path) -> dict[str, Any]:
    """Parse an exported TypeScript data object literal into a Python dict."""
    txt = path.read_text(encoding="utf-8")
    txt = re.sub(r"//[^\n]*", "", txt)
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    match = re.search(r"export\s+const\s+\w+(?:\s*:\s*[^=]+)?\s*=\s*", txt)
    if not match:
        raise ValueError(f"Could not locate exported object in {path}")
    body = txt[match.end() :].strip().rstrip(";").strip()
    body = re.sub(r"\[MalaysiaPart\.(\w+)\]", r'"\1"', body)
    body = re.sub(r'(?m)(^|[{,\s])([A-Za-z_]\w*|\d+)\s*:', r'\1"\2":', body)
    body = re.sub(r",\s*([}\]])", r"\1", body)
    return json.loads(body)


def format_month_header(ym: str) -> str:
    """Convert 'YYYY-MM' into 'Mmm YYYY' (e.g. 'Jan 2010')."""
    return datetime.strptime(ym, "%Y-%m").strftime("%b %Y")


def style_banner(
    ws: Worksheet,
    title: str,
    subtitle: str,
    headers: list[str],
    header_hex: str,
    tab_hex: str,
    freeze_cell: str,
) -> None:
    """Apply standardized title banner, subtitle strip, spacer row, and table headers."""
    num_cols = len(headers)
    last_col = get_column_letter(num_cols)

    ws.sheet_properties.tabColor = tab_hex

    # Row 1: Title Banner
    ws.merge_cells(f"A1:{last_col}1")
    ws.row_dimensions[1].height = 30
    c1 = ws.cell(1, 1, title)
    c1.font = FONT_TITLE
    c1.fill = FILL_NAVY
    c1.alignment = ALIGN_LEFT

    # Row 2: Subtitle Strip
    ws.merge_cells(f"A2:{last_col}2")
    ws.row_dimensions[2].height = 22
    c2 = ws.cell(2, 1, subtitle)
    c2.font = FONT_SUBTITLE
    c2.fill = FILL_SUBTITLE
    c2.alignment = ALIGN_LEFT

    # Row 3: Blank spacer
    ws.row_dimensions[3].height = 8

    # Row 4: Table Header
    header_fill = PatternFill(start_color=header_hex, end_color=header_hex, fill_type="solid")
    ws.row_dimensions[4].height = 34
    for col_idx, text in enumerate(headers, start=1):
        cell = ws.cell(4, col_idx, text)
        cell.font = FONT_HEADER
        cell.fill = header_fill
        cell.alignment = ALIGN_HEADER
        cell.border = BORDER_HEADER

    ws.freeze_panes = freeze_cell


def finalize_data_sheet(
    ws: Worksheet,
    num_cols: int,
    last_row: int,
    col_widths: dict[int, float],
) -> None:
    """Apply AutoFilter and explicit column widths to a completed worksheet."""
    last_col = get_column_letter(num_cols)
    ws.auto_filter.ref = f"A4:{last_col}{last_row}"
    for col_idx, width in col_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width


def write_data_cell(
    ws: Worksheet,
    row: int,
    col: int,
    value: Any,
    *,
    fill: PatternFill,
    font: Font = FONT_BODY,
    alignment: Alignment = ALIGN_LEFT,
    number_format: str | None = None,
) -> None:
    """Write a styled cell cleanly."""
    cell = ws.cell(row, col)
    if number_format == "@" and value is not None:
        cell.value = str(value)
        cell.data_type = "s"
    else:
        cell.value = value
    cell.font = font
    cell.fill = fill
    cell.border = BORDER_DATA
    cell.alignment = alignment
    if number_format:
        cell.number_format = number_format


def build_general_inflation_sheet(wb: openpyxl.Workbook, inflation_data: dict[str, float]) -> int:
    ws = wb.create_sheet("General Inflation")
    headers = [
        "Year",
        "Annual Inflation Rate (%)",
        "Cumulative Price Index (1960 = 100)",
        "Primary Source",
    ]
    years = sorted(int(y) for y in inflation_data.keys())
    style_banner(
        ws,
        "Malaysia General Headline Inflation (1960 – 2025)",
        f"Annual consumer price inflation rates (%) used by the Simple section. Base index 1960 = 100. Coverage: {years[0]}–{years[-1]}.",
        headers,
        header_hex="1D4ED8",
        tab_hex="1D4ED8",
        freeze_cell="A5",
    )

    row = 5
    for idx, yr in enumerate(years):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        rate_decimal = inflation_data[str(yr)] / 100.0
        index_formula = 100.0 if idx == 0 else f"=C{row - 1}*(1+B{row})"

        write_data_cell(ws, row, 1, yr, fill=fill, alignment=ALIGN_CENTER, number_format="0")
        write_data_cell(ws, row, 2, rate_decimal, fill=fill, alignment=ALIGN_RIGHT, number_format="0.00%")
        write_data_cell(ws, row, 3, index_formula, fill=fill, alignment=ALIGN_RIGHT, number_format="0.00")
        write_data_cell(ws, row, 4, "World Bank / DOSM", fill=fill, alignment=ALIGN_LEFT)
        ws.row_dimensions[row].height = 19
        row += 1

    finalize_data_sheet(ws, len(headers), row - 1, {1: 12, 2: 26, 3: 34, 4: 24})
    return len(years)


def build_national_cpi_sheet(
    wb: openpyxl.Workbook,
    cpi_malaysia: dict[str, dict[str, float]],
    ytd_year: int,
    ytd_label: str,
) -> int:
    ws = wb.create_sheet("National CPI (2D)")
    headers = ["Year", "Period Note"] + [label for _, label in CPI_2D_FIELDS]
    years = sorted(int(y) for y in cpi_malaysia.keys())
    style_banner(
        ws,
        "Malaysia National Consumer Price Index by COICOP Division (1960 – 2026)",
        f"Official DOSM Headline CPI (Base 2010 = 100). Covers Overall CPI (1960–2026) and 13 COICOP 2018 Divisions (1980/2003/2010–2026; {ytd_year} = {ytd_label}).",
        headers,
        header_hex="1D4ED8",
        tab_hex="1D4ED8",
        freeze_cell="C5",
    )

    row = 5
    for idx, yr in enumerate(years):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        rec = cpi_malaysia[str(yr)]
        period_note = ytd_label if yr == ytd_year else "Full Year"

        write_data_cell(ws, row, 1, yr, fill=fill, alignment=ALIGN_CENTER, number_format="0")
        write_data_cell(ws, row, 2, period_note, fill=fill, alignment=ALIGN_CENTER)
        for col_offset, (key, _) in enumerate(CPI_2D_FIELDS, start=3):
            val = rec.get(key)
            write_data_cell(
                ws,
                row,
                col_offset,
                val,
                fill=fill,
                font=FONT_BODY_BOLD if key == "total" else FONT_BODY,
                alignment=ALIGN_RIGHT,
                number_format="0.0",
            )
        ws.row_dimensions[row].height = 19
        row += 1

    widths = {1: 10, 2: 16, 3: 14}
    for col_idx in range(4, len(headers) + 1):
        widths[col_idx] = 20
    finalize_data_sheet(ws, len(headers), row - 1, widths)
    return len(years)


def build_regional_cpi_sheet(
    wb: openpyxl.Workbook,
    regions: list[tuple[str, dict[str, dict[str, float]]]],
) -> int:
    ws = wb.create_sheet("Regional CPI (2D)")
    headers = ["Region", "Year"] + [label for _, label in CPI_2D_FIELDS]
    style_banner(
        ws,
        "Macro Regional Consumer Price Index by COICOP Division (2000 – 2025)",
        "Official DOSM CPI (Base 2010 = 100) for Semenanjung Malaysia, Sabah & W.P. Labuan, and Sarawak across 13 Divisions.",
        headers,
        header_hex="0F766E",
        tab_hex="0F766E",
        freeze_cell="C5",
    )

    row = 5
    idx = 0
    for region_name, dataset in regions:
        for yr in sorted(int(y) for y in dataset.keys()):
            fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
            rec = dataset[str(yr)]
            write_data_cell(ws, row, 1, region_name, fill=fill, font=FONT_BODY_BOLD, alignment=ALIGN_LEFT)
            write_data_cell(ws, row, 2, yr, fill=fill, alignment=ALIGN_CENTER, number_format="0")
            for col_offset, (key, _) in enumerate(CPI_2D_FIELDS, start=3):
                write_data_cell(
                    ws,
                    row,
                    col_offset,
                    rec.get(key),
                    fill=fill,
                    font=FONT_BODY_BOLD if key == "total" else FONT_BODY,
                    alignment=ALIGN_RIGHT,
                    number_format="0.00",
                )
            ws.row_dimensions[row].height = 19
            row += 1
            idx += 1

    widths = {1: 24, 2: 10, 3: 14}
    for col_idx in range(4, len(headers) + 1):
        widths[col_idx] = 20
    finalize_data_sheet(ws, len(headers), row - 1, widths)
    return idx


def build_state_cpi_sheet(
    wb: openpyxl.Workbook,
    cpi_states: dict[str, dict[str, dict[str, float]]],
    ytd_year: int,
    ytd_label: str,
) -> int:
    ws = wb.create_sheet("State CPI (2D)")
    headers = ["State / Federal Territory", "Year", "Period Note"] + [label for _, label in CPI_2D_FIELDS]
    style_banner(
        ws,
        "Malaysia State & Federal Territory CPI by COICOP Division (2010 – 2026)",
        f"Official OpenDOSM State CPI (Base 2010 = 100) across all 16 Malaysian States & Federal Territories ({ytd_year} = {ytd_label}).",
        headers,
        header_hex="0F766E",
        tab_hex="0F766E",
        freeze_cell="D5",
    )

    row = 5
    idx = 0
    for state_key, state_label in STATE_DISPLAY_NAMES:
        state_data = cpi_states[state_key]
        for yr in sorted(int(y) for y in state_data.keys()):
            fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
            rec = state_data[str(yr)]
            period_note = ytd_label if yr == ytd_year else "Full Year"
            write_data_cell(ws, row, 1, state_label, fill=fill, font=FONT_BODY_BOLD, alignment=ALIGN_LEFT)
            write_data_cell(ws, row, 2, yr, fill=fill, alignment=ALIGN_CENTER, number_format="0")
            write_data_cell(ws, row, 3, period_note, fill=fill, alignment=ALIGN_CENTER)
            for col_offset, (key, _) in enumerate(CPI_2D_FIELDS, start=4):
                write_data_cell(
                    ws,
                    row,
                    col_offset,
                    rec.get(key),
                    fill=fill,
                    font=FONT_BODY_BOLD if key == "total" else FONT_BODY,
                    alignment=ALIGN_RIGHT,
                    number_format="0.00",
                )
            ws.row_dimensions[row].height = 19
            row += 1
            idx += 1

    widths = {1: 22, 2: 10, 3: 16, 4: 14}
    for col_idx in range(5, len(headers) + 1):
        widths[col_idx] = 20
    finalize_data_sheet(ws, len(headers), row - 1, widths)
    return idx


def build_big_mac_sheet(wb: openpyxl.Workbook, big_mac: dict[str, float]) -> int:
    ws = wb.create_sheet("Big Mac Index")
    headers = ["Year", "Big Mac Price (RM)", "YoY Change (%)", "Source"]
    years = sorted(int(y) for y in big_mac.keys())
    style_banner(
        ws,
        f"Malaysia Big Mac Index ({years[0]} – {years[-1]})",
        f"Unofficial purchasing power benchmark based on The Economist Big Mac Index (July / mid-year Malaysia RM releases, {years[0]}–{years[-1]}).",
        headers,
        header_hex="B45309",
        tab_hex="B45309",
        freeze_cell="A5",
    )

    row = 5
    for idx, yr in enumerate(years):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        yoy_formula = None if idx == 0 else f'=IFERROR((B{row}-B{row - 1})/B{row - 1},"")'
        src = "The Economist (Big Mac Index)"

        write_data_cell(ws, row, 1, yr, fill=fill, alignment=ALIGN_CENTER, number_format="0")
        write_data_cell(ws, row, 2, big_mac[str(yr)], fill=fill, alignment=ALIGN_RIGHT, number_format='"RM "#,##0.00')
        write_data_cell(ws, row, 3, yoy_formula, fill=fill, alignment=ALIGN_RIGHT, number_format="0.00%")
        write_data_cell(ws, row, 4, src, fill=fill, alignment=ALIGN_LEFT)
        ws.row_dimensions[row].height = 19
        row += 1

    finalize_data_sheet(ws, len(headers), row - 1, {1: 12, 2: 22, 3: 18, 4: 28})
    return len(years)


def build_mcoicop_dict_sheet(wb: openpyxl.Workbook, tree: dict[str, Any]) -> int:
    ws = wb.create_sheet("MCOICOP Dictionary")
    headers = [
        "Level",
        "Code",
        "Division",
        "Group",
        "Class",
        "English Name",
        "Bahasa Melayu Name",
        "Start Month",
        "End Month",
    ]
    style_banner(
        ws,
        "DOSM MCOICOP 2018 Classification Dictionary (342 Categories)",
        "Bilingual English & Bahasa Melayu classification hierarchy used by the Detailed section (13 Divisions, 47 Groups, 101 Classes, 181 Subclasses).",
        headers,
        header_hex="4338CA",
        tab_hex="4338CA",
        freeze_cell="C5",
    )

    rows_data: list[dict[str, Any]] = []
    for div in tree["divisions"]:
        rows_data.append(
            {
                "level": "Division (2D)",
                "code": div["code"],
                "division": div["code"],
                "group": "-",
                "class": "-",
                "descEn": div["descEn"],
                "descBm": div["descBm"],
                "minMonth": "-",
                "maxMonth": "-",
                "sort_key": (div["code"], "", "", 2, div["code"]),
            }
        )
    for node in tree["nodes"]:
        rows_data.append(
            {
                "level": LEVEL_NAMES[node["digits"]],
                "code": node["code"],
                "division": node["division"],
                "group": node["group"],
                "class": node["classCode"] or "-",
                "descEn": node["descEn"],
                "descBm": node["descBm"],
                "minMonth": node["minMonth"],
                "maxMonth": node["maxMonth"],
                "sort_key": (
                    node["division"],
                    node["group"],
                    node["classCode"] or "",
                    node["digits"],
                    node["code"],
                ),
            }
        )

    rows_data.sort(key=lambda r: r["sort_key"])

    row = 5
    for idx, item in enumerate(rows_data):
        is_div = item["level"] == "Division (2D)"
        fill = FILL_OVERALL if is_div else (FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE)
        font = FONT_OVERALL if is_div else FONT_BODY

        write_data_cell(ws, row, 1, item["level"], fill=fill, font=font, alignment=ALIGN_LEFT)
        write_data_cell(ws, row, 2, item["code"], fill=fill, font=font, alignment=ALIGN_CENTER, number_format="@")
        write_data_cell(ws, row, 3, item["division"], fill=fill, font=font, alignment=ALIGN_CENTER, number_format="@")
        write_data_cell(ws, row, 4, item["group"], fill=fill, font=font, alignment=ALIGN_CENTER, number_format="@")
        write_data_cell(ws, row, 5, item["class"], fill=fill, font=font, alignment=ALIGN_CENTER, number_format="@")
        write_data_cell(ws, row, 6, item["descEn"], fill=fill, font=font, alignment=ALIGN_LEFT)
        write_data_cell(ws, row, 7, item["descBm"], fill=fill, font=font, alignment=ALIGN_LEFT)
        write_data_cell(ws, row, 8, item["minMonth"], fill=fill, font=font, alignment=ALIGN_CENTER)
        write_data_cell(ws, row, 9, item["maxMonth"], fill=fill, font=font, alignment=ALIGN_CENTER)
        ws.row_dimensions[row].height = 19
        row += 1

    finalize_data_sheet(
        ws,
        len(headers),
        row - 1,
        {1: 16, 2: 11, 3: 11, 4: 11, 5: 11, 6: 46, 7: 46, 8: 14, 9: 14},
    )
    return len(rows_data)


def build_detailed_annual_sheet(
    wb: openpyxl.Workbook,
    tree: dict[str, Any],
    annual_data: dict[str, Any],
) -> int:
    ws = wb.create_sheet("Detailed Annual (3D-5D)")
    meta = annual_data["meta"]
    years = list(range(meta["minYear"], meta["maxYear"] + 1))
    ytd_year = meta["ytdYear"]
    ytd_label = f"Jan–{datetime.strptime(meta['latestMonth'], '%Y-%m').strftime('%b')} YTD"

    year_headers = [
        f"{yr} ({ytd_label})" if yr == ytd_year and meta["ytdMonths"] < 12 else str(yr)
        for yr in years
    ]
    headers = [
        "Level",
        "Code",
        "Division",
        "English Name",
        "Bahasa Melayu Name",
        "Start Year",
    ] + year_headers

    style_banner(
        ws,
        f"Detailed National CPI Annual Averages — Groups (3D), Classes (4D) & Subclasses (5D) ({meta['minYear']} – {meta['maxYear']})",
        f"Base 2010 = 100. Includes Overall Malaysia benchmark + all 329 MCOICOP 3D/4D/5D series ({ytd_year} = {ytd_label} average).",
        headers,
        header_hex="4338CA",
        tab_hex="4338CA",
        freeze_cell="F5",
    )

    # Row 5: Overall benchmark row
    row = 5
    write_data_cell(ws, row, 1, "Overall (Benchmark)", fill=FILL_OVERALL, font=FONT_OVERALL, alignment=ALIGN_LEFT)
    write_data_cell(ws, row, 2, "overall", fill=FILL_OVERALL, font=FONT_OVERALL, alignment=ALIGN_CENTER, number_format="@")
    write_data_cell(ws, row, 3, "-", fill=FILL_OVERALL, font=FONT_OVERALL, alignment=ALIGN_CENTER, number_format="@")
    write_data_cell(ws, row, 4, "All items (Overall Malaysia CPI)", fill=FILL_OVERALL, font=FONT_OVERALL, alignment=ALIGN_LEFT)
    write_data_cell(ws, row, 5, "Semua item (IHP Keseluruhan Malaysia)", fill=FILL_OVERALL, font=FONT_OVERALL, alignment=ALIGN_LEFT)
    write_data_cell(ws, row, 6, meta["minYear"], fill=FILL_OVERALL, font=FONT_OVERALL, alignment=ALIGN_CENTER, number_format="0")
    for col_offset, yr in enumerate(years, start=7):
        write_data_cell(
            ws,
            row,
            col_offset,
            annual_data["overall"].get(str(yr)),
            fill=FILL_OVERALL,
            font=FONT_OVERALL,
            alignment=ALIGN_RIGHT,
            number_format="0.00",
        )
    ws.row_dimensions[row].height = 20
    row += 1

    nodes_sorted = sorted(tree["nodes"], key=lambda n: (n["digits"], n["code"]))
    for idx, node in enumerate(nodes_sorted):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        series = annual_data["series"][node["code"]]
        write_data_cell(ws, row, 1, LEVEL_NAMES[node["digits"]], fill=fill, alignment=ALIGN_LEFT)
        write_data_cell(ws, row, 2, node["code"], fill=fill, font=FONT_BODY_BOLD, alignment=ALIGN_CENTER, number_format="@")
        write_data_cell(ws, row, 3, node["division"], fill=fill, alignment=ALIGN_CENTER, number_format="@")
        write_data_cell(ws, row, 4, node["descEn"], fill=fill, alignment=ALIGN_LEFT)
        write_data_cell(ws, row, 5, node["descBm"], fill=fill, alignment=ALIGN_LEFT)
        write_data_cell(ws, row, 6, node["minYear"], fill=fill, alignment=ALIGN_CENTER, number_format="0")
        for col_offset, yr in enumerate(years, start=7):
            write_data_cell(
                ws,
                row,
                col_offset,
                series.get(str(yr)),
                fill=fill,
                alignment=ALIGN_RIGHT,
                number_format="0.00",
            )
        ws.row_dimensions[row].height = 19
        row += 1

    widths = {1: 18, 2: 10, 3: 10, 4: 44, 5: 44, 6: 12}
    for col_idx in range(7, len(headers) + 1):
        widths[col_idx] = 15 if col_idx == len(headers) else 10
    finalize_data_sheet(ws, len(headers), row - 1, widths)
    return 1 + len(nodes_sorted)


def build_detailed_monthly_sheet(
    wb: openpyxl.Workbook,
    sheet_name: str,
    level: int,
    tree: dict[str, Any],
    monthly_data: dict[str, Any],
) -> int:
    ws = wb.create_sheet(sheet_name)
    dates: list[str] = monthly_data["meta"]["dates"]
    month_headers = [format_month_header(ym) for ym in dates]

    if level == 3:
        id_headers = ["Code", "Division", "English Name", "Bahasa Melayu Name", "Start Month"]
        freeze_cell = "F5"
        title_desc = "3-Digit Groups (47 Groups)"
        widths = {1: 10, 2: 10, 3: 44, 4: 44, 5: 13}
    elif level == 4:
        id_headers = ["Code", "Division", "Group", "English Name", "Bahasa Melayu Name", "Start Month"]
        freeze_cell = "G5"
        title_desc = "4-Digit Classes (101 Classes)"
        widths = {1: 10, 2: 10, 3: 10, 4: 44, 5: 44, 6: 13}
    else:
        id_headers = ["Code", "Division", "Group", "Class", "English Name", "Bahasa Melayu Name", "Start Month"]
        freeze_cell = "H5"
        title_desc = "5-Digit Subclasses (181 Subclasses)"
        widths = {1: 10, 2: 10, 3: 10, 4: 10, 5: 44, 6: 44, 7: 13}

    headers = id_headers + month_headers
    start_month_col = len(id_headers) + 1
    style_banner(
        ws,
        f"Detailed Monthly National CPI — {title_desc} (Jan 2010 – Oct 2026)",
        "Official OpenDOSM Monthly CPI (Base 2010 = 100) across 202 consecutive months. Row 5 provides Overall Malaysia CPI for comparison.",
        headers,
        header_hex="047857",
        tab_hex="047857",
        freeze_cell=freeze_cell,
    )

    def write_monthly_row(
        r: int,
        id_vals: list[tuple[Any, str | None]],
        tuple_data: list[Any],
        fill: PatternFill,
        font: Font,
    ) -> None:
        for c_idx, (val, num_fmt) in enumerate(id_vals, start=1):
            align = ALIGN_CENTER if num_fmt == "@" or c_idx == len(id_vals) else ALIGN_LEFT
            row_font = font if num_fmt != "@" or font is FONT_OVERALL else FONT_BODY_BOLD
            write_data_cell(ws, r, c_idx, val, fill=fill, font=row_font, alignment=align, number_format=num_fmt)

        start_idx, vals = tuple_data
        for m_idx in range(len(dates)):
            val = vals[m_idx - start_idx] if m_idx >= start_idx and m_idx - start_idx < len(vals) else None
            write_data_cell(
                ws,
                r,
                start_month_col + m_idx,
                val,
                fill=fill,
                font=font,
                alignment=ALIGN_RIGHT,
                number_format="0.0",
            )
        ws.row_dimensions[r].height = 19

    # Row 5: Overall benchmark
    row = 5
    if level == 3:
        ov_ids = [("overall", "@"), ("-", "@"), ("All items (Overall Malaysia CPI)", None), ("Semua item (IHP Keseluruhan Malaysia)", None), ("2010-01", None)]
    elif level == 4:
        ov_ids = [("overall", "@"), ("-", "@"), ("-", "@"), ("All items (Overall Malaysia CPI)", None), ("Semua item (IHP Keseluruhan Malaysia)", None), ("2010-01", None)]
    else:
        ov_ids = [("overall", "@"), ("-", "@"), ("-", "@"), ("-", "@"), ("All items (Overall Malaysia CPI)", None), ("Semua item (IHP Keseluruhan Malaysia)", None), ("2010-01", None)]

    write_monthly_row(row, ov_ids, monthly_data["overall"], FILL_OVERALL, FONT_OVERALL)
    ws.row_dimensions[row].height = 20
    row += 1

    nodes = sorted([n for n in tree["nodes"] if n["digits"] == level], key=lambda n: n["code"])
    for idx, node in enumerate(nodes):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        if level == 3:
            ids = [(node["code"], "@"), (node["division"], "@"), (node["descEn"], None), (node["descBm"], None), (node["minMonth"], None)]
        elif level == 4:
            ids = [(node["code"], "@"), (node["division"], "@"), (node["group"], "@"), (node["descEn"], None), (node["descBm"], None), (node["minMonth"], None)]
        else:
            ids = [(node["code"], "@"), (node["division"], "@"), (node["group"], "@"), (node["classCode"], "@"), (node["descEn"], None), (node["descBm"], None), (node["minMonth"], None)]
        write_monthly_row(row, ids, monthly_data["series"][node["code"]], fill, FONT_BODY)
        row += 1

    for m_col in range(start_month_col, len(headers) + 1):
        widths[m_col] = 10
    finalize_data_sheet(ws, len(headers), row - 1, widths)
    return 1 + len(nodes)


def build_overview_sheet(
    wb: openpyxl.Workbook,
    contents_rows: list[tuple[str, str, str, str, str, str]],
    latest_month_label: str,
) -> None:
    ws = wb.active
    ws.title = "Overview"
    ws.sheet_properties.tabColor = "1E3A8A"
    ws.views.sheetView[0].showGridLines = False

    # Title Banner
    ws.merge_cells("A1:F1")
    ws.row_dimensions[1].height = 34
    t = ws.cell(1, 1, "Malaysia Inflation Calculator — Master Frontend Dataset")
    t.font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    t.fill = FILL_NAVY
    t.alignment = ALIGN_LEFT

    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 22
    st = ws.cell(
        2,
        1,
        "Complete downloadable workbook mirroring every Simple and Detailed CPI dataset powering inflation-calc.xkre.me",
    )
    st.font = FONT_SUBTITLE
    st.fill = FILL_SUBTITLE
    st.alignment = ALIGN_LEFT

    ws.row_dimensions[3].height = 10

    # Key Metadata Summary Grid
    summary_pairs = [
        ("Web Application", "https://inflation-calc.xkre.me", "CPI Base Year", "2010 = 100"),
        ("Latest Monthly Data", latest_month_label, "Classification", "UN COICOP 2018 / DOSM MCOICOP"),
        ("Total Worksheets", f"{len(contents_rows) + 1} sheets (Overview + {len(contents_rows)} data tabs)", "Workbook Generated", datetime.now().strftime("%Y-%m-%d")),
    ]
    for r_offset, (k1, v1, k2, v2) in enumerate(summary_pairs, start=4):
        ws.row_dimensions[r_offset].height = 21
        write_data_cell(ws, r_offset, 1, k1, fill=FILL_INFO_LABEL, font=FONT_BODY_BOLD)
        if v1.startswith("https://"):
            c_v1 = ws.cell(r_offset, 2, v1)
            c_v1.hyperlink = v1
            c_v1.font = FONT_URL
            c_v1.fill = FILL_WHITE
            c_v1.border = BORDER_DATA
            c_v1.alignment = ALIGN_LEFT
        else:
            write_data_cell(ws, r_offset, 2, v1, fill=FILL_WHITE)
        ws.merge_cells(start_row=r_offset, start_column=2, end_row=r_offset, end_column=3)
        ws.cell(r_offset, 3).border = BORDER_DATA

        write_data_cell(ws, r_offset, 4, k2, fill=FILL_INFO_LABEL, font=FONT_BODY_BOLD)
        write_data_cell(ws, r_offset, 5, v2, fill=FILL_WHITE)
        ws.merge_cells(start_row=r_offset, start_column=5, end_row=r_offset, end_column=6)
        ws.cell(r_offset, 6).border = BORDER_DATA

    # Section: Workbook Contents
    ws.row_dimensions[7].height = 12
    ws.row_dimensions[8].height = 24
    sec1 = ws.cell(8, 1, "Worksheet Contents (Click any sheet name to jump)")
    sec1.font = FONT_SECTION

    toc_headers = ["Worksheet", "App Section", "Geographic Scope", "Period Coverage", "Records", "Description"]
    ws.row_dimensions[9].height = 26
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    for col_idx, h in enumerate(toc_headers, start=1):
        c = ws.cell(9, col_idx, h)
        c.font = FONT_HEADER
        c.fill = header_fill
        c.alignment = ALIGN_HEADER
        c.border = BORDER_HEADER

    row = 10
    for idx, (sheet_name, section, scope, period, count_str, desc) in enumerate(contents_rows):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        link_cell = ws.cell(row, 1, sheet_name)
        link_cell.hyperlink = Hyperlink(ref=link_cell.coordinate, location=f"'{sheet_name}'!A1")
        link_cell.font = FONT_LINK
        link_cell.fill = fill
        link_cell.border = BORDER_DATA
        link_cell.alignment = ALIGN_LEFT

        write_data_cell(ws, row, 2, section, fill=fill, alignment=ALIGN_CENTER)
        write_data_cell(ws, row, 3, scope, fill=fill, alignment=ALIGN_LEFT)
        write_data_cell(ws, row, 4, period, fill=fill, alignment=ALIGN_CENTER)
        write_data_cell(ws, row, 5, count_str, fill=fill, alignment=ALIGN_RIGHT)
        write_data_cell(ws, row, 6, desc, fill=fill, alignment=ALIGN_LEFT_WRAP)
        ws.row_dimensions[row].height = 22
        row += 1

    # Section: Methodology & Important Notes
    row += 1
    ws.row_dimensions[row].height = 24
    ws.cell(row, 1, "Methodology & Important Notes").font = FONT_SECTION
    row += 1

    notes = [
        ("2026 Partial-Year YTD", f"All 2026 annual CPI figures reflect Year-to-Date averages from Jan to {latest_month_label} (10 months). Full-year 2026 figures will be updated after Dec 2026 release."),
        ("COICOP 2018 Reclassification", "Starting Jan 2024, DOSM expanded from 12 to 13 Divisions: Division 12 is Insurance & Financial Services (from 2010), and Division 13 is Personal Care, Social Protection & Miscellaneous Goods & Services."),
        ("Detailed 3D/4D/5D Scope", "3-Digit Groups (47), 4-Digit Classes (101), and 5-Digit Subclasses (181) are published by DOSM at the National Malaysia level only. 20 newer series begin in 2016, 2018, or 2024."),
        ("Calculation Formulas", "CPI & Big Mac calculations use Equivalent Value = Value_1 * (CPI_2 / CPI_1). General Inflation (1960–2025) compounds annual percentage rates year-by-year."),
    ]
    for idx, (topic, detail) in enumerate(notes):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        write_data_cell(ws, row, 1, topic, fill=FILL_INFO_LABEL, font=FONT_BODY_BOLD)
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=6)
        write_data_cell(ws, row, 2, detail, fill=fill, alignment=ALIGN_LEFT_WRAP)
        for c_i in range(3, 7):
            ws.cell(row, c_i).border = BORDER_DATA
            ws.cell(row, c_i).fill = fill
        ws.row_dimensions[row].height = 30
        row += 1

    # Section: Official Data Sources
    row += 1
    ws.row_dimensions[row].height = 24
    ws.cell(row, 1, "Official Data Sources").font = FONT_SECTION
    row += 1

    sources = [
        ("OpenDOSM — Annual CPI (2D)", "https://open.dosm.gov.my/data-catalogue/cpi_annual", "National Headline & 13 Divisions (1960–2025)"),
        ("OpenDOSM — Monthly State CPI (2D)", "https://open.dosm.gov.my/data-catalogue/cpi_state", "16 Malaysian States & Federal Territories (2010–2026)"),
        ("data.gov.my — CPI by 3-Digit Group (cpi_3d)", "https://data.gov.my/data-catalogue/cpi_3d", "47 National 3-Digit Groups (2010–2026)"),
        ("data.gov.my — CPI by 4-Digit Class (cpi_4d)", "https://data.gov.my/data-catalogue/cpi_4d", "101 National 4-Digit Classes (2010–2026)"),
        ("data.gov.my — CPI by 5-Digit Subclass (cpi_5d)", "https://data.gov.my/data-catalogue/cpi_5d", "181 National 5-Digit Subclasses (2010–2026)"),
        ("OpenDOSM — MCOICOP Dictionary", "https://storage.dosm.gov.my/dictionaries/mcoicop.csv", "Official EN / BM MCOICOP 2018 classification dictionary"),
        ("OpenDOSM — CPI Publications Portal", "https://open.dosm.gov.my/publications?page=1&pub_type=cpi", "Official monthly press releases & annual CPI bulletins"),
        ("World Bank — Inflation, Consumer Prices (Malaysia)", "https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=MY", "Historical headline inflation rates (1960–2025)"),
        ("The Economist — Big Mac Index (Malaysia)", "https://github.com/TheEconomist/big-mac-data", "Official Big Mac Index Malaysia mid-year / July RM prices (2000–2026)"),
    ]
    for idx, (label, url, desc) in enumerate(sources):
        fill = FILL_ZEBRA if idx % 2 == 1 else FILL_WHITE
        write_data_cell(ws, row, 1, label, fill=fill, font=FONT_BODY_BOLD)
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=2)
        ws.cell(row, 2).border = BORDER_DATA
        ws.cell(row, 2).fill = fill

        ws.merge_cells(start_row=row, start_column=3, end_row=row, end_column=4)
        u_cell = ws.cell(row, 3, url)
        u_cell.hyperlink = url
        u_cell.font = FONT_URL
        u_cell.fill = fill
        u_cell.border = BORDER_DATA
        u_cell.alignment = ALIGN_LEFT
        ws.cell(row, 4).border = BORDER_DATA
        ws.cell(row, 4).fill = fill

        ws.merge_cells(start_row=row, start_column=5, end_row=row, end_column=6)
        write_data_cell(ws, row, 5, desc, fill=fill, alignment=ALIGN_LEFT_WRAP)
        ws.cell(row, 6).border = BORDER_DATA
        ws.cell(row, 6).fill = fill
        ws.row_dimensions[row].height = 20
        row += 1

    overview_widths = {1: 28, 2: 18, 3: 24, 4: 22, 5: 18, 6: 54}
    for col_idx, width in overview_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width


def main() -> None:
    # Preserve legacy backup before overwriting src/raw_data/CpiDataset.xlsx
    if RAW_XLSX.exists() and not RAW_BACKUP_XLSX.exists():
        shutil.copy2(RAW_XLSX, RAW_BACKUP_XLSX)

    inflation_data = parse_ts_object(DATA_DIR / "inflation.ts")
    cpi_malaysia = parse_ts_object(DATA_DIR / "cpiMalaysia.ts")
    cpi_semenanjung = parse_ts_object(DATA_DIR / "cpiSemenanjung.ts")
    cpi_sabah = parse_ts_object(DATA_DIR / "cpiSabahLabuan.ts")
    cpi_sarawak = parse_ts_object(DATA_DIR / "cpiSarawak.ts")
    cpi_states = parse_ts_object(DATA_DIR / "cpiStates.ts")
    big_mac = parse_ts_object(DATA_DIR / "misc" / "bigMacIndex.ts")

    tree = json.loads((DETAILED_DIR / "mcoicopTree.json").read_text(encoding="utf-8"))
    annual_data = json.loads((DETAILED_DIR / "cpiDetailedAnnual.json").read_text(encoding="utf-8"))
    monthly_data = json.loads((DETAILED_DIR / "cpiDetailedMonthly.json").read_text(encoding="utf-8"))

    # Basic integrity assertions on frontend sources
    assert len(inflation_data) == 66, f"Expected 66 inflation years, got {len(inflation_data)}"
    assert len(cpi_malaysia) == 67, f"Expected 67 Malaysia CPI years, got {len(cpi_malaysia)}"
    assert len(cpi_states) == 16, f"Expected 16 states, got {len(cpi_states)}"
    assert len(tree["divisions"]) == 13 and len(tree["nodes"]) == 329

    meta = annual_data["meta"]
    ytd_year = meta["ytdYear"]
    latest_month_dt = datetime.strptime(meta["latestMonth"], "%Y-%m")
    ytd_label = f"Jan–{latest_month_dt.strftime('%b')} YTD"
    latest_month_label = latest_month_dt.strftime("%b %Y")

    wb = openpyxl.Workbook()

    gen_cnt = build_general_inflation_sheet(wb, inflation_data)
    nat_cnt = build_national_cpi_sheet(wb, cpi_malaysia, ytd_year, ytd_label)
    reg_cnt = build_regional_cpi_sheet(
        wb,
        [
            ("Semenanjung Malaysia", cpi_semenanjung),
            ("Sabah & W.P. Labuan", cpi_sabah),
            ("Sarawak", cpi_sarawak),
        ],
    )
    st_cnt = build_state_cpi_sheet(wb, cpi_states, ytd_year, ytd_label)
    bm_cnt = build_big_mac_sheet(wb, big_mac)
    dict_cnt = build_mcoicop_dict_sheet(wb, tree)
    ann_cnt = build_detailed_annual_sheet(wb, tree, annual_data)
    m3_cnt = build_detailed_monthly_sheet(wb, "Detailed Monthly 3D", 3, tree, monthly_data)
    m4_cnt = build_detailed_monthly_sheet(wb, "Detailed Monthly 4D", 4, tree, monthly_data)
    m5_cnt = build_detailed_monthly_sheet(wb, "Detailed Monthly 5D", 5, tree, monthly_data)

    bm_years = sorted(int(y) for y in big_mac.keys())

    contents_rows = [
        ("General Inflation", "Simple", "Malaysia (National)", "1960 – 2025", f"{gen_cnt} years", "Annual headline inflation rates (%) and compounded price index (1960 = 100)"),
        ("National CPI (2D)", "Simple", "Malaysia (National)", "1960 – 2026", f"{nat_cnt} years", "National Overall CPI + 13 COICOP 2018 Divisions (2026 = Jan–Oct YTD)"),
        ("Regional CPI (2D)", "Simple", "3 Macro Regions", "2000 – 2025", f"{reg_cnt} rows", "Semenanjung, Sabah & Labuan, and Sarawak CPI across 13 Divisions"),
        ("State CPI (2D)", "Simple", "16 States & FTs", "2010 – 2026", f"{st_cnt} rows", "All 16 Malaysian States & Federal Territories across 13 Divisions"),
        ("Big Mac Index", "Simple", "Malaysia (National)", f"{bm_years[0]} – {bm_years[-1]}", f"{bm_cnt} years", "Historical Malaysian Big Mac menu price (RM) and YoY change"),
        ("MCOICOP Dictionary", "Detailed", "Classification Tree", "COICOP 2018", f"{dict_cnt} items", "EN & BM names and hierarchy for 13 Divisions + 329 3D/4D/5D categories"),
        ("Detailed Annual (3D-5D)", "Detailed", "Malaysia (National)", "2010 – 2026", f"{ann_cnt} series", "Overall benchmark + 329 Group/Class/Subclass annual average indices"),
        ("Detailed Monthly 3D", "Detailed", "Malaysia (National)", "Jan 2010 – Oct 2026", f"{m3_cnt} × 202m", "Overall benchmark + 47 3-Digit Group monthly CPI indices"),
        ("Detailed Monthly 4D", "Detailed", "Malaysia (National)", "Jan 2010 – Oct 2026", f"{m4_cnt} × 202m", "Overall benchmark + 101 4-Digit Class monthly CPI indices"),
        ("Detailed Monthly 5D", "Detailed", "Malaysia (National)", "Jan 2010 – Oct 2026", f"{m5_cnt} × 202m", "Overall benchmark + 181 5-Digit Subclass monthly CPI indices"),
    ]

    build_overview_sheet(wb, contents_rows, latest_month_label)

    RAW_XLSX.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_XLSX.parent.mkdir(parents=True, exist_ok=True)
    wb.save(RAW_XLSX)
    shutil.copy2(RAW_XLSX, PUBLIC_XLSX)

    print(f"Saved {RAW_XLSX.relative_to(ROOT_DIR)} ({RAW_XLSX.stat().st_size:,} bytes)")
    print(f"Synced {PUBLIC_XLSX.relative_to(ROOT_DIR)} ({PUBLIC_XLSX.stat().st_size:,} bytes)")
    print(f"Sheets ({len(wb.sheetnames)}): {wb.sheetnames}")


if __name__ == "__main__":
    main()
