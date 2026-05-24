# UI_NOTES.md — Cycle Price Configurator

## Approach
I chose Option A — Built a live Streamlit web app
instead of wireframes.

Live app: https://hero-cycles-pricing.streamlit.app

## 1. Most important thing on the configurator screen?

The price breakdown and total price is the most
important thing. The salesperson needs to see
the final price instantly and clearly — without
scrolling or searching for it.

## 2. Salesperson uses this 20 times a day — what did you do to make it fast?

Three things:
- Default date is pre-filled as Dec 15, 2016
  so she doesn't type it every time
- Dropdowns are simple and labeled clearly —
  no technical jargon
- Calculate button is large, red, and impossible
  to miss — one click to get price

## 3. What happens when invalid combination selected?

Example: No parts selected at all.

The app will:
- Show a clear warning message:
  "Please select at least one part to
  calculate price"
- Not show ₹0 or crash silently
- Wait for user to fix selection

## 4. One thing I would improve with more time

I would add a "Save Configuration" feature —
where a salesperson can save a common cycle
build by name (e.g. "Standard City Bike") and
load it in one click instead of selecting all
parts again every time.

This would make repetitive quoting much faster
for popular configurations.
