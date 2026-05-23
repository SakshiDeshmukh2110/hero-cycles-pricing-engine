import streamlit as st
from datetime import date
import sys
import os

# Import our pricing engine
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from pricing_engine import PricingEngine

# ── PAGE CONFIG ──────────────────────────────
st.set_page_config(
    page_title="Hero Cycles Price Configurator",
    page_icon="🚲",
    layout="centered"
)

# ── TITLE ────────────────────────────────────
st.title("🚲 Hero Cycles Price Configurator")
st.caption("Select parts and a pricing date to get instant price breakdown")

st.divider()

# ── PART OPTIONS ─────────────────────────────
frame_options = {
    "Select Frame": None,
    "Steel Frame": "steel_frame",
    "Aluminium Frame": "aluminium_frame"
}

handle_options = {
    "Select Handlebar": None,
    "Standard Handlebar": "standard_handlebar",
}

brake_options = {
    "Select Brakes": None,
    "V-Brakes": "v_brakes",
    "Disc Brakes": "disc_brakes"
}

saddle_options = {
    "Select Saddle": None,
    "Basic Saddle": "basic_saddle",
    "Ergonomic Saddle": "ergonomic_saddle"
}

tyre_options = {
    "Select Tyre": None,
    "Standard Tyre": "standard_tyre",
    "Tubeless Tyre": "tubeless_tyre"
}

rim_options = {
    "Select Rim": None,
    "Standard Rim": "standard_rim"
}

tube_options = {
    "Include Tube": None,
    "Tube": "tube",
    "No Tube (Tubeless)": None
}

spokes_options = {
    "Select Spokes": None,
    "Spokes": "spokes"
}

chain_options = {
    "Select Chain Assembly": None,
    "Single Speed Chain": "single_speed_chain",
    "4-Gear Assembly": "4_gear_assembly",
    "7-Gear Assembly": "7_gear_assembly"
}

# ── FORM ─────────────────────────────────────
st.subheader("1. Select Parts")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Frame**")
    frame = st.selectbox(
        "Frame",
        options=list(frame_options.keys()),
        label_visibility="collapsed"
    )

    st.markdown("**Handlebar**")
    handle = st.selectbox(
        "Handlebar",
        options=list(handle_options.keys()),
        label_visibility="collapsed"
    )

    st.markdown("**Brakes**")
    brakes = st.selectbox(
        "Brakes",
        options=list(brake_options.keys()),
        label_visibility="collapsed"
    )

    st.markdown("**Saddle**")
    saddle = st.selectbox(
        "Saddle",
        options=list(saddle_options.keys()),
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**Tyre**")
    tyre = st.selectbox(
        "Tyre",
        options=list(tyre_options.keys()),
        label_visibility="collapsed"
    )

    st.markdown("**Rim**")
    rim = st.selectbox(
        "Rim",
        options=list(rim_options.keys()),
        label_visibility="collapsed"
    )

    st.markdown("**Tube**")
    tube = st.selectbox(
        "Tube",
        options=list(tube_options.keys()),
        label_visibility="collapsed"
    )

    st.markdown("**Spokes**")
    spokes = st.selectbox(
        "Spokes",
        options=list(spokes_options.keys()),
        label_visibility="collapsed"
    )

st.markdown("**Chain Assembly**")
chain = st.selectbox(
    "Chain Assembly",
    options=list(chain_options.keys()),
    label_visibility="collapsed"
)

st.divider()

# ── DATE PICKER ──────────────────────────────
st.subheader("2. Select Pricing Date")
pricing_date = st.date_input(
    "Pricing Date",
    value=date(2016, 12, 15),
    min_value=date(2016, 1, 1),
    label_visibility="collapsed"
)

st.divider()

# ── CALCULATE BUTTON ─────────────────────────
calculate = st.button(
    "🔢 Calculate Price",
    use_container_width=True,
    type="primary"
)

# ── RESULTS ──────────────────────────────────
if calculate:

    # Collect selected parts
    selected_parts = []

    if frame_options[frame]:
        selected_parts.append(frame_options[frame])
    if handle_options[handle]:
        selected_parts.append(handle_options[handle])
    if brake_options[brakes]:
        selected_parts.append(brake_options[brakes])
    if saddle_options[saddle]:
        selected_parts.append(saddle_options[saddle])
    if tyre_options[tyre]:
        selected_parts.append(tyre_options[tyre])
    if rim_options[rim]:
        selected_parts.append(rim_options[rim])
    if tube_options[tube]:
        selected_parts.append(tube_options[tube])
    if spokes_options[spokes]:
        selected_parts.append(spokes_options[spokes])
    if chain_options[chain]:
        selected_parts.append(chain_options[chain])

    # Edge Case 5 — No parts selected
    if not selected_parts:
        st.warning(
            "⚠ Please select at least one part "
            "to calculate price."
        )
    else:
        # Run pricing engine
        engine = PricingEngine()
        breakdown, errors = engine.calculate(
            selected_parts,
            pricing_date
        )

        # Show results
        st.divider()
        st.subheader(
            f"💰 Price Breakdown — "
            f"{pricing_date.strftime('%d %b %Y')}"
        )

        component_order = [
            "Frame",
            "Handle Bar & Brakes",
            "Seating",
            "Wheels",
            "Chain Assembly"
        ]

        total = 0.0

        for component in component_order:
            if component in breakdown:
                comp_total = breakdown[component]["total"]
                total += comp_total
                st.markdown(
                    f"**{component}** &nbsp;&nbsp;&nbsp;"
                    f"₹{comp_total:,.0f}"
                )

        st.divider()

        # Total in big text
        st.markdown(
            f"### TOTAL &nbsp;&nbsp;&nbsp; ₹{total:,.0f}"
        )

        # Show warnings if any
        if errors:
            st.divider()
            st.subheader("⚠ Warnings")
            for error in errors:
                st.warning(error)
