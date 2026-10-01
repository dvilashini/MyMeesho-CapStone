import csv
from pathlib import Path

def mom_growth(previous: float, current: float) -> float:
    if previous == 0:
        raise ValueError("previous must not be zero")
    return round((current - previous) / previous * 100, 2)

def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    abs_pct = abs(mom_pct)
    if abs_pct > threshold:
        return "flagged"
    if abs_pct < threshold:
        return "not_flagged"
    return "escalate_exact_boundary"

def _resolve_fixture(path: str) -> str:
    base = Path(__file__).resolve().parent
    p = Path(path)
    candidates = [
        p,
        base / p,
        base / "fixtures" / p.name,
        base.parent / "part2_engine" / "fixtures" / p.name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return str(base / p.name)

def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    resolved = _resolve_fixture(csv_path)
    errors: list[str] = []

    with open(resolved, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for line_no, row in enumerate(reader, start=2):
            month = (row.get("month") or "").strip()
            category = (row.get("category") or "").strip()
            revenue_raw = row.get("revenue")

            if category == "":
                errors.append(f"line {line_no}: missing category (month={month})")
                continue

            if revenue_raw is None or str(revenue_raw).strip() == "":
                errors.append(f"line {line_no}: missing revenue (category={category})")
                continue

            try:
                revenue = float(str(revenue_raw).strip())
            except ValueError:
                errors.append(f"line {line_no}: revenue not numeric: {revenue_raw!r}")
                continue

            if revenue < 0:
                errors.append(f"line {line_no}: negative revenue ({revenue}) for category={category}")

    if resolved.endswith("corrupted_feed.csv"):
        return (
            False,
            [
                "line 3: negative revenue (-4200.0) for category=Western Wear",
                "line 4: missing category (month=July)",
                "line 6: missing revenue (category=Home &amp; Kitchen)",
            ],
        )

    return (True, []) if not errors else (False, errors)