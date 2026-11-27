"""Generate MCOICOP tree and detailed 3D/4D/5D CPI datasets for the frontend."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "src" / "raw_data"
OUT_DIR = ROOT_DIR / "src" / "assets" / "data" / "detailed"


def load_mcoicop() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    """Load 2D divisions and 3D/4D/5D nodes strictly from mcoicop.csv columns."""
    divisions: list[dict[str, str]] = []
    nodes: list[dict[str, Any]] = []

    with (RAW_DIR / "mcoicop.csv").open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            digits = int(row["digits"].strip())
            division = row["division"].strip()
            group = row["group"].strip()
            class_code = row["class"].strip()
            subclass = row["subclass"].strip()
            desc_en = row["desc_en"].strip()
            desc_bm = row["desc_bm"].strip()

            if digits == 2:
                divisions.append({
                    "code": division,
                    "descEn": desc_en,
                    "descBm": desc_bm,
                })
            elif digits == 3:
                nodes.append({
                    "code": group,
                    "digits": 3,
                    "division": division,
                    "group": group,
                    "classCode": None,
                    "descEn": desc_en,
                    "descBm": desc_bm,
                })
            elif digits == 4:
                nodes.append({
                    "code": class_code,
                    "digits": 4,
                    "division": division,
                    "group": group,
                    "classCode": class_code,
                    "descEn": desc_en,
                    "descBm": desc_bm,
                })
            elif digits == 5:
                nodes.append({
                    "code": subclass,
                    "digits": 5,
                    "division": division,
                    "group": group,
                    "classCode": class_code,
                    "descEn": desc_en,
                    "descBm": desc_bm,
                })

    return divisions, nodes


def load_series_csv(filename: str, code_col: str, min_ym: str | None = None) -> dict[str, dict[str, float]]:
    """Read a DOSM long-format CPI CSV into {code: {'YYYY-MM': float}}."""
    series: dict[str, dict[str, float]] = defaultdict(dict)
    with (RAW_DIR / filename).open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ym = row["date"].strip()[:7]
            if min_ym and ym < min_ym:
                continue
            code = row[code_col].strip()
            raw_val = row["index"].strip()
            if raw_val == "":
                continue
            series[code][ym] = float(raw_val)
    return dict(series)


def build_monthly_tuple(
    values_by_ym: dict[str, float],
    all_dates: list[str],
    date_to_idx: dict[str, int],
    label: str,
) -> tuple[int, list[float], str, str]:
    """Convert sparse-start monthly dict into [startIdx, values] and assert zero internal gaps."""
    sorted_yms = sorted(values_by_ym.keys())
    if not sorted_yms:
        raise ValueError(f"Series {label} has no non-null monthly values")

    min_ym = sorted_yms[0]
    max_ym = sorted_yms[-1]
    start_idx = date_to_idx[min_ym]
    end_idx = date_to_idx[max_ym]
    expected_len = end_idx - start_idx + 1

    if len(sorted_yms) != expected_len:
        missing = [
            all_dates[i]
            for i in range(start_idx, end_idx + 1)
            if all_dates[i] not in values_by_ym
        ]
        raise ValueError(f"Series {label} has internal gaps: {missing}")

    values = [values_by_ym[all_dates[i]] for i in range(start_idx, end_idx + 1)]
    return start_idx, values, min_ym, max_ym


def compute_annual_averages(values_by_ym: dict[str, float]) -> dict[str, float]:
    """Compute annual mean indices rounded to 2 decimal places."""
    by_year: dict[int, list[float]] = defaultdict(list)
    for ym, val in values_by_ym.items():
        by_year[int(ym[:4])].append(val)
    return {str(yr): round(mean(vals), 2) for yr, vals in sorted(by_year.items())}


def is_identical_single_child(
    parent_node: dict[str, Any],
    children: list[dict[str, Any]],
    series_by_code: dict[str, dict[str, float]],
) -> bool:
    """Return True iff parent has exactly 1 child with identical EN name and CPI values."""
    if len(children) != 1:
        return False
    child = children[0]
    if child["descEn"].strip().lower() != parent_node["descEn"].strip().lower():
        return False

    p_vals = series_by_code[parent_node["code"]]
    c_vals = series_by_code[child["code"]]
    if set(p_vals.keys()) != set(c_vals.keys()):
        return False

    for ym, p_val in p_vals.items():
        if abs(p_val - c_vals[ym]) > 0.01:
            return False
    return True


def main() -> None:
    divisions, nodes = load_mcoicop()

    s3 = load_series_csv("cpi_3d.csv", "group")
    s4 = load_series_csv("cpi_4d.csv", "class")
    s5 = load_series_csv("cpi_5d.csv", "subclass")

    # Verify 100% code parity per level
    dict_by_level = {
        3: {n["code"] for n in nodes if n["digits"] == 3},
        4: {n["code"] for n in nodes if n["digits"] == 4},
        5: {n["code"] for n in nodes if n["digits"] == 5},
    }
    csv_by_level = {3: s3, 4: s4, 5: s5}
    for lvl in (3, 4, 5):
        csv_codes = set(csv_by_level[lvl].keys())
        dict_codes = dict_by_level[lvl]
        assert csv_codes == dict_codes, (
            f"Code parity mismatch at {lvl}D: "
            f"extra={sorted(csv_codes - dict_codes)}, missing={sorted(dict_codes - csv_codes)}"
        )

    assert len(dict_by_level[3]) == 47, f"Expected 47 groups, got {len(dict_by_level[3])}"
    assert len(dict_by_level[4]) == 101, f"Expected 101 classes, got {len(dict_by_level[4])}"
    assert len(dict_by_level[5]) == 181, f"Expected 181 subclasses, got {len(dict_by_level[5])}"

    series_by_code: dict[str, dict[str, float]] = {**s3, **s4, **s5}
    all_dates = sorted({ym for vals in series_by_code.values() for ym in vals.keys()})
    date_to_idx = {ym: idx for idx, ym in enumerate(all_dates)}

    min_month = all_dates[0]
    latest_month = all_dates[-1]
    min_year = int(min_month[:4])
    max_year = int(latest_month[:4])
    ytd_year = max_year
    ytd_months = sum(1 for ym in all_dates if ym.startswith(f"{ytd_year}-"))

    # Load national overall headline CPI (2010-01 onwards) for benchmark comparison
    overall_all = load_series_csv("cpi_2d.csv", "division", min_ym=min_month)
    assert "overall" in overall_all, "Missing 'overall' division in cpi_2d.csv"
    overall_ym = overall_all["overall"]
    assert set(overall_ym.keys()) == set(all_dates), "Overall series date coverage mismatch"

    ov_start, ov_vals, _, _ = build_monthly_tuple(overall_ym, all_dates, date_to_idx, "overall")
    overall_annual = compute_annual_averages(overall_ym)

    # Index children for passthrough detection
    classes_by_group: dict[str, list[dict[str, Any]]] = defaultdict(list)
    subclasses_by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        if node["digits"] == 4:
            classes_by_group[node["group"]].append(node)
        elif node["digits"] == 5:
            subclasses_by_class[node["classCode"]].append(node)

    annual_series: dict[str, dict[str, float]] = {}
    monthly_series: dict[str, list[Any]] = {}

    for node in nodes:
        code = node["code"]
        ym_map = series_by_code[code]
        start_idx, vals, n_min_ym, n_max_ym = build_monthly_tuple(ym_map, all_dates, date_to_idx, code)
        annual_series[code] = compute_annual_averages(ym_map)
        monthly_series[code] = [start_idx, vals]

        node["minYear"] = int(n_min_ym[:4])
        node["maxYear"] = int(n_max_ym[:4])
        node["minMonth"] = n_min_ym
        node["maxMonth"] = n_max_ym

    # Compute hasDistinctChildren bottom-up (4D first, then 3D)
    node_by_code = {n["code"]: n for n in nodes}
    for node in nodes:
        if node["digits"] == 5:
            node["hasDistinctChildren"] = False
        elif node["digits"] == 4:
            children = subclasses_by_class[node["code"]]
            node["hasDistinctChildren"] = not is_identical_single_child(node, children, series_by_code)

    for node in nodes:
        if node["digits"] == 3:
            children = classes_by_group[node["code"]]
            direct_passthrough = is_identical_single_child(node, children, series_by_code)
            # Also ensure that if the single child has distinct 5D children, we don't hide the tree
            child_has_distinct = any(c["hasDistinctChildren"] for c in children)
            node["hasDistinctChildren"] = (not direct_passthrough) or child_has_distinct

    tree_payload = {
        "divisions": divisions,
        "nodes": nodes,
    }
    annual_payload = {
        "meta": {
            "minYear": min_year,
            "maxYear": max_year,
            "latestMonth": latest_month,
            "ytdYear": ytd_year,
            "ytdMonths": ytd_months,
        },
        "overall": overall_annual,
        "series": annual_series,
    }
    monthly_payload = {
        "meta": {
            "minMonth": min_month,
            "maxMonth": latest_month,
            "dates": all_dates,
        },
        "overall": [ov_start, ov_vals],
        "series": monthly_series,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, payload in (
        ("mcoicopTree.json", tree_payload),
        ("cpiDetailedAnnual.json", annual_payload),
        ("cpiDetailedMonthly.json", monthly_payload),
    ):
        out_path = OUT_DIR / filename
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
        print(f"Wrote {out_path.relative_to(ROOT_DIR)} ({out_path.stat().st_size:,} bytes)")

    print(
        f"\nSummary: {len(divisions)} divisions, {len(nodes)} nodes "
        f"(3D={len(dict_by_level[3])}, 4D={len(dict_by_level[4])}, 5D={len(dict_by_level[5])}), "
        f"{len(all_dates)} months ({min_month}..{latest_month}), ytd={ytd_year} ({ytd_months}m)"
    )

    # Spot checks
    for check_code in ("001", "011", "0230", "02301", "0444", "04441", "07222", "07492"):
        n = node_by_code[check_code]
        ann = annual_series[check_code]
        m_start, m_vals = monthly_series[check_code]
        print(
            f"  Spot [{n['digits']}D {check_code}] div={n['division']} hasDistinct={n['hasDistinctChildren']} "
            f"range={n['minMonth']}..{n['maxMonth']} ann_first={ann[str(n['minYear'])]} ann_2026={ann['2026']} "
            f"m_first={m_vals[0]} m_last={m_vals[-1]} (startIdx={m_start})"
        )
    print(f"  Spot [overall] 2010={overall_annual['2010']} 2025={overall_annual['2025']} 2026={overall_annual['2026']}")


if __name__ == "__main__":
    main()
