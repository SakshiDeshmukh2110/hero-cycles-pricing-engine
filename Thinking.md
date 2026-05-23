# THINKING.md — Hero Cycles Pricing Engine

## Part 1 — Problem Breakdown

### 1. Who is using this?
The user is a salesperson at a cycle showroom — not a 
developer. She needs to:
- Quickly select parts for a cycle configuration
- Get an instant price breakdown by component
- See the total price clearly

What would frustrate her:
- Too many steps to get a price
- Technical jargon or confusing field names
- No clarity on which date's price is being used
- System giving wrong price due to outdated data

### 2. What makes this problem tricky?

**Edge Case 1 — Price on exact boundary date:**
If a price changes on Dec 1, and the salesperson 
enters Dec 1 as the date — which price applies? 
The old one or the new one? This needs a clear 
rule. My rule: the new price applies from 
valid_from date onwards — so Dec 1 gets the 
new price.

**Edge Case 2 — Missing price for a date:**
If a part was added in March 2016 but someone 
queries January 2016 — there is no valid price 
for that date. The system should handle this 
gracefully with a clear warning message, 
not crash silently.

**Edge Case 3 — Part discontinued:**
A part may have been removed from the catalogue 
after a certain date. The system should clearly 
indicate this rather than showing wrong or 
zero pricing to the salesperson.

**Edge Case 4 — Future date query:**
If a salesperson accidentally enters a future 
date like 2030, no price entry exists that far 
ahead. The system should show a clear message:
"Price not available for this date" rather than 
returning a wrong value or crashing.

**Edge Case 5 — No parts selected:**
If a salesperson clicks Calculate without 
selecting any parts, the system should not 
crash or show ₹0 silently. It should show 
a clear message: "Please select at least 
one part to calculate price."

### 3. My Plan

**Representing parts and prices:**
Each part will have a price_history — a list of 
price entries. Each entry has a valid_from date, 
valid_until date (null if currently active), 
and the price value.

**Handling price changes over time:**
When a date is given, the engine will look 
through the price_history of each selected 
part and find the entry where the date falls 
between valid_from and valid_until.

**Structuring the output:**
Output will show price grouped by high-level 
component (Frame, Handle, Seating, Wheels, Chain) 
with a final total at the bottom.

## Part 2a — Data Model

### Core Entities:

**PriceEntry**
- valid_from : date
- valid_until : date or null
- price : float

**Part**
- id : string (e.g. "steel_frame")
- name : string (e.g. "Steel Frame")
- component : string (e.g. "Frame")
- price_history : List of PriceEntry

**CycleConfiguration**
- date : date
- parts : List of part ids

### Relationships:
- One Component has many Parts
- One Part has many PriceEntries
- One CycleConfiguration has many Parts

### Design Decision:
I stored a list of price ranges per part rather 
than a single price because prices change over 
time. A single price field would need to be 
updated every time prices change — risking data 
loss of historical pricing. With price_history, 
we preserve all past prices and can query any 
point in time accurately.
