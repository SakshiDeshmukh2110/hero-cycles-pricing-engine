from datetime import date
import json
import sys


# ── PRICE ENTRY ──────────────────────────────
class PriceEntry:
    def __init__(self, valid_from, valid_until, price):
        self.valid_from = valid_from    # date object
        self.valid_until = valid_until  # date or None
        self.price = price              # float

    def is_valid_for(self, query_date):
        """Check if this price entry is valid for given date.
        
        Edge Case 1 — Boundary date rule:
        If query_date == valid_from, new price applies.
        Example: price changes Dec 1 → Dec 1 gets NEW price.
        """
        if query_date < self.valid_from:
            return False
        if self.valid_until is None:
            # valid_until = None means currently active price
            return True
        return query_date <= self.valid_until


# ── PART ─────────────────────────────────────
class Part:
    def __init__(self, part_id, name, component,
                 price_history, discontinued_after=None):
        self.part_id = part_id
        self.name = name
        self.component = component
        self.price_history = price_history
        # Edge Case 3 — store discontinued date if any
        self.discontinued_after = discontinued_after

    def get_price_on(self, query_date):
        """Return price for this part on given date.
        
        Handles:
        - Edge Case 1: Boundary date (handled in is_valid_for)
        - Edge Case 2: Missing price for date
        - Edge Case 3: Discontinued part
        - Edge Case 4: Future date with no price entry
        """
        # Edge Case 3 — Part discontinued
        if self.discontinued_after is not None:
            if query_date > self.discontinued_after:
                return "DISCONTINUED"

        # Edge Case 2 & 4 — Look through price history
        # If no entry matches, returns None
        # This handles both missing prices and future dates
        for entry in self.price_history:
            if entry.is_valid_for(query_date):
                return entry.price

        return None  # No price found for this date


# ── PARTS DATABASE ────────────────────────────
def get_parts_database():
    """All available parts with their price history.
    
    Each part has price_history — a list of PriceEntry.
    This preserves ALL historical prices so any date
    can be queried accurately.
    """
    return {

        # ── FRAME ──
        "steel_frame": Part(
            part_id="steel_frame",
            name="Steel Frame",
            component="Frame",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 1200.0),
                PriceEntry(date(2016, 12, 1),
                           None, 1400.0),
            ]
        ),
        "aluminium_frame": Part(
            part_id="aluminium_frame",
            name="Aluminium Frame",
            component="Frame",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 2000.0),
                PriceEntry(date(2016, 12, 1),
                           None, 2300.0),
            ]
        ),

        # ── HANDLE BAR & BRAKES ──
        "standard_handlebar": Part(
            part_id="standard_handlebar",
            name="Standard Handlebar",
            component="Handle Bar & Brakes",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 400.0),
                PriceEntry(date(2016, 12, 1),
                           None, 450.0),
            ]
        ),
        "v_brakes": Part(
            part_id="v_brakes",
            name="V-Brakes",
            component="Handle Bar & Brakes",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 350.0),
                PriceEntry(date(2016, 12, 1),
                           None, 400.0),
            ]
        ),
        "disc_brakes": Part(
            part_id="disc_brakes",
            name="Disc Brakes",
            component="Handle Bar & Brakes",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 800.0),
                PriceEntry(date(2016, 12, 1),
                           None, 950.0),
            ]
        ),

        # ── SEATING ──
        "basic_saddle": Part(
            part_id="basic_saddle",
            name="Basic Saddle",
            component="Seating",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 400.0),
                PriceEntry(date(2016, 12, 1),
                           None, 450.0),
            ]
        ),
        "ergonomic_saddle": Part(
            part_id="ergonomic_saddle",
            name="Ergonomic Saddle",
            component="Seating",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 750.0),
                PriceEntry(date(2016, 12, 1),
                           None, 850.0),
            ]
        ),

        # ── WHEELS ──
        "standard_rim": Part(
            part_id="standard_rim",
            name="Standard Rim",
            component="Wheels",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 500.0),
                PriceEntry(date(2016, 12, 1),
                           None, 580.0),
            ]
        ),
        "tube": Part(
            part_id="tube",
            name="Tube",
            component="Wheels",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 150.0),
                PriceEntry(date(2016, 12, 1),
                           None, 180.0),
            ]
        ),
        "standard_tyre": Part(
            part_id="standard_tyre",
            name="Standard Tyre",
            component="Wheels",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 200.0),
                PriceEntry(date(2016, 12, 1),
                           None, 230.0),
            ]
        ),
        "tubeless_tyre": Part(
            part_id="tubeless_tyre",
            name="Tubeless Tyre",
            component="Wheels",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 450.0),
                PriceEntry(date(2016, 12, 1),
                           None, 520.0),
            ]
        ),
        "spokes": Part(
            part_id="spokes",
            name="Spokes",
            component="Wheels",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 100.0),
                PriceEntry(date(2016, 12, 1),
                           None, 120.0),
            ]
        ),

        # ── CHAIN ASSEMBLY ──
        "single_speed_chain": Part(
            part_id="single_speed_chain",
            name="Single Speed Chain",
            component="Chain Assembly",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 300.0),
                PriceEntry(date(2016, 12, 1),
                           None, 350.0),
            ]
        ),
        "4_gear_assembly": Part(
            part_id="4_gear_assembly",
            name="4-Gear Assembly",
            component="Chain Assembly",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 800.0),
                PriceEntry(date(2016, 12, 1),
                           None, 950.0),
            ]
        ),
        "7_gear_assembly": Part(
            part_id="7_gear_assembly",
            name="7-Gear Assembly",
            component="Chain Assembly",
            price_history=[
                PriceEntry(date(2016, 1, 1),
                           date(2016, 11, 30), 1400.0),
                PriceEntry(date(2016, 12, 1),
                           None, 1600.0),
            ]
        ),
    }


# ── PRICING ENGINE ────────────────────────────
class PricingEngine:
    def __init__(self):
        self.parts_db = get_parts_database()

    def calculate(self, part_ids, query_date):
        """Calculate price breakdown for given parts and date.
        
        Handles all 5 edge cases from THINKING.md
        """

        # Edge Case 5 — No parts selected
        if not part_ids:
            print("\n⚠  Please select at least one part"
                  " to calculate price.")
            return {}, []

        breakdown = {}
        errors = []

        for part_id in part_ids:

            # Edge Case 2 — Unknown part
            if part_id not in self.parts_db:
                errors.append(
                    f"Unknown part: '{part_id}'. "
                    f"Please check the part name."
                )
                continue

            part = self.parts_db[part_id]
            price = part.get_price_on(query_date)

            # Edge Case 3 — Discontinued part
            if price == "DISCONTINUED":
                errors.append(
                    f"'{part.name}' is no longer available "
                    f"after {part.discontinued_after}. "
                    f"Please select a different part."
                )
                continue

            # Edge Case 2 & 4 — No price for this date
            # Could be missing price OR future date
            if price is None:
                errors.append(
                    f"No price found for '{part.name}' "
                    f"on {query_date}. "
                    f"This may be a future date or before "
                    f"the part was added to catalogue."
                )
                continue

            # Add to component breakdown
            component = part.component
            if component not in breakdown:
                breakdown[component] = {
                    "parts": [],
                    "total": 0.0
                }
            breakdown[component]["parts"].append({
                "name": part.name,
                "price": price
            })
            breakdown[component]["total"] += price

        return breakdown, errors

    def print_breakdown(self, breakdown, errors, query_date):
        """Print formatted price breakdown"""

        print(f"\nCycle Price Breakdown — "
              f"{query_date.strftime('%d %b %Y')}")
        print("-" * 40)

        total = 0.0
        component_order = [
            "Frame",
            "Handle Bar & Brakes",
            "Seating",
            "Wheels",
            "Chain Assembly"
        ]

        for component in component_order:
            if component in breakdown:
                comp_total = breakdown[component]["total"]
                total += comp_total
                print(f"{component:<25}: "
                      f"₹{comp_total:,.0f}")

        print("-" * 40)
        print(f"{'TOTAL':<25}: ₹{total:,.0f}")

        # Show warnings for any edge cases encountered
        if errors:
            print("\nWarnings:")
            for error in errors:
                print(f"  ⚠  {error}")


# ── MAIN ──────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: python pricing_engine.py input.json")
        sys.exit(1)

    # Read input JSON file
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    # Parse date and parts from input
    query_date = date.fromisoformat(data["date"])
    part_ids = data["parts"]

    # Run pricing engine
    engine = PricingEngine()
    breakdown, errors = engine.calculate(part_ids, query_date)
    engine.print_breakdown(breakdown, errors, query_date)


if __name__ == "__main__":
    main()
