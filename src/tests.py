from datetime import date
from pricing_engine import PriceEntry, Part, PricingEngine

# ── TEST 1 ────────────────────────────────────
def test_price_before_december():
    """
    Edge Case 1 — Boundary date test:
    Steel frame should cost 1200 before Dec 2016
    """
    engine = PricingEngine()
    breakdown, errors = engine.calculate(
        ["steel_frame"],
        date(2016, 6, 15)  # June 2016
    )
    assert breakdown["Frame"]["total"] == 1200.0
    assert errors == []
    print("✅ Test 1 Passed — Price correct before Dec 2016")


# ── TEST 2 ────────────────────────────────────
def test_price_after_december():
    """
    Edge Case 1 — Boundary date test:
    Steel frame should cost 1400 from Dec 2016
    """
    engine = PricingEngine()
    breakdown, errors = engine.calculate(
        ["steel_frame"],
        date(2016, 12, 15)  # December 2016
    )
    assert breakdown["Frame"]["total"] == 1400.0
    assert errors == []
    print("✅ Test 2 Passed — Price correct after Dec 2016")


# ── TEST 3 ────────────────────────────────────
def test_price_on_boundary_date():
    """
    Edge Case 1 — Exact boundary date:
    Dec 1 should use NEW price (1400 not 1200)
    """
    engine = PricingEngine()
    breakdown, errors = engine.calculate(
        ["steel_frame"],
        date(2016, 12, 1)  # Exact boundary date
    )
    assert breakdown["Frame"]["total"] == 1400.0
    assert errors == []
    print("✅ Test 3 Passed — Boundary date uses new price")


# ── TEST 4 ────────────────────────────────────
def test_unknown_part():
    """
    Edge Case 2 — Unknown part:
    Should return error, not crash
    """
    engine = PricingEngine()
    breakdown, errors = engine.calculate(
        ["unknown_xyz_part"],
        date(2016, 6, 15)
    )
    assert len(errors) > 0
    print("✅ Test 4 Passed — Unknown part handled gracefully")


# ── TEST 5 ────────────────────────────────────
def test_no_parts_selected():
    """
    Edge Case 5 — No parts selected:
    Should return empty breakdown, not crash
    """
    engine = PricingEngine()
    breakdown, errors = engine.calculate(
        [],
        date(2016, 6, 15)
    )
    assert breakdown == {}
    assert errors == []
    print("✅ Test 5 Passed — Empty parts handled gracefully")


# ── TEST 6 ────────────────────────────────────
def test_multiple_parts_total():
    """
    Multiple parts total should be correct sum
    """
    engine = PricingEngine()
    breakdown, errors = engine.calculate(
        ["steel_frame", "basic_saddle"],
        date(2016, 6, 15)  # Before Dec
    )
    # steel_frame = 1200, basic_saddle = 400
    assert breakdown["Frame"]["total"] == 1200.0
    assert breakdown["Seating"]["total"] == 400.0
    assert errors == []
    print("✅ Test 6 Passed — Multiple parts total correct")


# ── RUN ALL TESTS ─────────────────────────────
if __name__ == "__main__":
    print("\nRunning all tests...\n")
    test_price_before_december()
    test_price_after_december()
    test_price_on_boundary_date()
    test_unknown_part()
    test_no_parts_selected()
    test_multiple_parts_total()
    print("\n🎉 All 6 tests passed!")
