# Hero Cycles Pricing Engine 🚲

A command-line pricing engine and live web app 
for Hero Cycles that calculates cycle configuration 
prices based on selected parts and a pricing date.

## Live Demo
🚲 https://hero-cycles-pricing.streamlit.app

## How to Run (under 2 minutes)

### Step 1 — Clone the repository
git clone https://github.com/SakshiDeshmukh2110/hero-cycles-pricing-engine.git
cd hero-cycles-pricing-engine

### Step 2 — Go to src folder
cd src

### Step 3 — Run the engine
python pricing_engine.py ../input.json

### Expected Output
Cycle Price Breakdown — 15 Dec 2016
----------------------------------------
Frame                    : ₹1,400
Handle Bar & Brakes      : ₹850
Seating                  : ₹450
Wheels                   : ₹1,400
Chain Assembly           : ₹950
----------------------------------------
TOTAL                    : ₹5,050

## How to Run Tests

cd src
python tests.py

### Expected Output
Running all tests...

✅ Test 1 Passed — Price correct before Dec 2016

✅ Test 2 Passed — Price correct after Dec 2016

✅ Test 3 Passed — Boundary date uses new price

✅ Test 4 Passed — Unknown part handled gracefully

✅ Test 5 Passed — Empty parts handled gracefully

✅ Test 6 Passed — Multiple parts total correct


🎉 All 6 tests passed!

## Project Structure

hero-cycles-pricing-engine/
├── src/
│   ├── pricing_engine.py   — Main engine code
│   └── tests.py            — Unit tests
├── app.py                  — Streamlit web app
├── README.md               — Setup instructions
├── THINKING.md             — Problem breakdown
├── UI_NOTES.md             — UI design notes
└── input.json              — Sample input file

## Tech Stack
- Language: Python 3
- UI: Streamlit
- No external libraries needed for CLI
- Standard library only for pricing engine

## How it Works
1. Read parts list and date from input JSON
2. For each part find correct price for that date
3. Group prices by component
4. Display formatted breakdown with total

## Live Web App
Built with Streamlit — salesperson can:
- Select parts from dropdowns
- Pick a pricing date
- See instant price breakdown
- View total price clearly
