# Part4_Agent/mock_agent_runner.py

import csv
import json
from Part2_Engine.growth_engine import mom_growth, is_flagged, validate_feed

def draft_message(category, prev_rev, curr_rev, mom_pct, prev_month, month):
    # Simple template fill using Part 3 structure
    return (
        f"Context: {category} revenue compared {prev_month} ({prev_rev}) vs {month} ({curr_rev}). "
        f"Insight (Fact): MoM change = {mom_pct}%. "
        f"Implication (Hypothesis): Regional managers should review drivers of this change."
    )

def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:
    valid, errors = validate_feed(current_month_csv)
    if not valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

    # Load previous and current month revenues
    def load_csv(path):
        data = {}
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data[row["category"]] = float(row["revenue"])
        return data

    prev_data = load_csv(previous_month_csv)
    curr_data = load_csv(current_month_csv)

    flagged = []
    suppressed = []
    escalated = []

    # Compute MoM growth for each category
    for category, curr_rev in curr_data.items():
        prev_rev = prev_data.get(category)
        if prev_rev is None:
            continue
        mom_pct = mom_growth(prev_rev, curr_rev)
        flag_status = is_flagged(mom_pct)

        if flag_status == "flagged":
            flagged.append({
                "category": category,
                "mom_pct": mom_pct,
                "previous_revenue": prev_rev,
                "current_revenue": curr_rev,
                "drafted": False,
                "message": ""
            })
        elif flag_status == "escalate_exact_boundary":
            escalated.append(category)

    # Sort flagged by magnitude
    flagged.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)

    # Draft top 3, suppress rest
    for i, entry in enumerate(flagged):
        if i < 3:
            entry["drafted"] = True
            entry["message"] = draft_message(
                entry["category"], entry["previous_revenue"],
                entry["current_revenue"], entry["mom_pct"],
                "prev_month", month
            )
        else:
            suppressed.append(entry["category"])

    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }

if __name__ == "__main__":
    # Example: run May scenario (April→May)
    result = run(
        "May",
        "Part2_Engine/fixtures/monthly_category_revenue.csv",  # April data
        "Part2_Engine/fixtures/monthly_category_revenue.csv"   # May data (replace with actual path)
    )
    print(json.dumps(result, indent=2))
