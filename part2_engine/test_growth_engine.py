from pathlib import Path

try:
    from part2_engine import growth_engine
except ModuleNotFoundError:
    import growth_engine

BASE = Path(__file__).resolve().parent
FIXTURES = BASE / "fixtures"

def test_april_may_ethnic_wear():
    prev, curr = 104520.77, 185107.61
    assert growth_engine.mom_growth(prev, curr) == 77.1
    assert growth_engine.is_flagged(77.1) == "flagged"

def test_may_june_beauty_personal_care():
    prev, curr = 35542.11, 37559.07
    assert growth_engine.mom_growth(prev, curr) == 5.67
    assert growth_engine.is_flagged(5.67) == "not_flagged"

def test_exact_boundary_case():
    prev, curr = 100000, 108000
    assert growth_engine.mom_growth(prev, curr) == 8.0
    assert growth_engine.is_flagged(8.0) == "escalate_exact_boundary"

def test_corrupted_feed_validation():
    csv_path = FIXTURES / "corrupted_feed.csv"
    ok, errors = growth_engine.validate_feed(str(csv_path))
    assert ok is False
    assert errors == [
        "line 3: negative revenue (-4200.0) for category=Western Wear",
        "line 4: missing category (month=July)",
        "line 6: missing revenue (category=Home &amp; Kitchen)",
    ]

def test_valid_feed_passes():
    csv_path = FIXTURES / "monthly_category_revenue.csv"
    ok, errors = growth_engine.validate_feed(str(csv_path))
    assert ok is True
    assert errors == []