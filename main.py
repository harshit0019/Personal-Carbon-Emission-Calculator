import streamlit as st
import pandas as pd

# ─── Emission factors per base unit ───────────────────────────────────────────
EMISSION_FACTOR = {
    "India": {"Transportation": 0.14, "Electricity": 0.8,  "Diet": 1.25, "Waste": 0.1},
    "USA":   {"Transportation": 0.24, "Electricity": 0.45, "Diet": 2.0,  "Waste": 0.12},
    "UK":    {"Transportation": 0.21, "Electricity": 0.3,  "Diet": 1.8,  "Waste": 0.09},
}

# ─── Unit config: (label, conversion-to-base) ─────────────────────────────────
UNIT_CONFIG = {
    "India": {"distance": ("km",    1.0),
              "electricity": ("kWh", 1.0),
              "waste":       ("kg",  1.0),
              "diet":        ("meals",1.0)},
    "USA":   {"distance": ("miles",   1.60934),
              "electricity": ("kWh",   1.0),
              "waste":       ("lbs",    0.453592),
              "diet":        ("meals", 1.0)},
    "UK":    {"distance": ("miles",   1.60934),
              "electricity": ("kWh",   1.0),
              "waste":       ("kg",     1.0),
              "diet":        ("meals", 1.0)},
}

st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")
st.title("🌍 Personal Carbon Calculator App")

# ─── Session state initialization ──────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

if "inputs" not in st.session_state:
    st.session_state.inputs = {
        "country":    "India",
        "distance":   50.0,
        "electricity":500.0,
        "waste":      10.0,
        "diet":       2
    }

def reset_inputs():
    st.session_state.inputs = {
        "country":    "India",
        "distance":   50.0,
        "electricity":500.0,
        "waste":      10.0,
        "diet":       2
    }

# ─── Country selector ──────────────────────────────────────────────────────────
st.subheader("🌍 Your Country")
country = st.selectbox(
    "Select your country:",
    options=list(EMISSION_FACTOR.keys()),
    index=list(EMISSION_FACTOR.keys()).index(st.session_state.inputs["country"])
)
st.session_state.inputs["country"] = country
units = UNIT_CONFIG[country]

# ─── User inputs ───────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.subheader(f"🚗 Daily Commute Distance ({units['distance'][0]})")
    st.session_state.inputs["distance"] = st.slider(
        f"Distance ({units['distance'][0]})", 0.0, 200.0, st.session_state.inputs["distance"]
    )

    st.subheader(f"💡 Monthly Electricity Consumption ({units['electricity'][0]})")
    st.session_state.inputs["electricity"] = st.slider(
        f"Electricity ({units['electricity'][0]})", 0.0, 2000.0, st.session_state.inputs["electricity"]
    )

with col2:
    st.subheader(f"🗑️ Weekly Waste Generated ({units['waste'][0]})")
    st.session_state.inputs["waste"] = st.slider(
        f"Waste ({units['waste'][0]})", 0.0, 200.0, st.session_state.inputs["waste"]
    )

    st.subheader("🍎 Meals per Day")
    st.session_state.inputs["diet"] = st.number_input(
        "Diet (meals/day)", 0, 10, st.session_state.inputs["diet"]
    )

# ─── Convert to base units & annualize ────────────────────────────────────────
distance_km     = st.session_state.inputs["distance"] * units["distance"][1] * 365
electricity_kwh = st.session_state.inputs["electricity"] * 12 * units["electricity"][1]
waste_kg        = st.session_state.inputs["waste"] * units["waste"][1] * 365
diet_meals      = st.session_state.inputs["diet"] * 52 * units["diet"][1]

# ─── Emissions calculations (tonnes CO₂/yr) ──────────────────────────────────
transport_em   = round(EMISSION_FACTOR[country]["Transportation"] * (distance_km / 1000), 2)
electricity_em = round(EMISSION_FACTOR[country]["Electricity"]    * (electricity_kwh / 1000), 2)
diet_em        = round(EMISSION_FACTOR[country]["Diet"]           * (diet_meals / 1000), 2)
waste_em       = round(EMISSION_FACTOR[country]["Waste"]          * (waste_kg / 1000), 2)
total_em       = round(transport_em + electricity_em + diet_em + waste_em, 2)

# ─── Calculate button & results ──────────────────────────────────────────────
calculate = st.button("Calculate CO2 Emissions")
if calculate:
    # save to history with static column names
    st.session_state.history.append({
        "Country":        country,
        "Distance":       f"{st.session_state.inputs['distance']} {units['distance'][0]}/day",
        "Electricity":    f"{st.session_state.inputs['electricity']} {units['electricity'][0]}/month",
        "Waste":          f"{st.session_state.inputs['waste']} {units['waste'][0]}/week",
        "Meals/day":      st.session_state.inputs["diet"],
        "Total CO2 (t/yr)": total_em
    })

    # Breakdown & total
    st.header("📊 Your Annual Carbon Footprint")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Breakdown")
        st.write(f"🚗 Transport:   **{transport_em}** t CO₂/yr")
        st.write(f"💡 Electricity: **{electricity_em}** t CO₂/yr")
        st.write(f"🍎 Diet:        **{diet_em}** t CO₂/yr")
        st.write(f"🗑️ Waste:       **{waste_em}** t CO₂/yr")

    with c2:
        st.subheader("Total")
        st.success(f"🔥 **{total_em} tonnes CO₂ per year**")
        if total_em < 1:
            st.balloons(); st.success("🏆 Gold Badge: Excellent!")
        elif total_em < 1.5:
            st.info("🥈 Silver Badge: Good, keep it up!")
        else:
            st.warning("🥉 Bronze Badge: There’s room to improve.")

    # CO₂ Equivalents & Offsetting
    st.divider()
    col5, col6 = st.columns(2)
    with col5:
        st.subheader("🌎 CO₂ Equivalents (per year)")
        flight_eq = round(total_em / 0.18, 1)
        car_eq    = round(total_em / 0.4, 1)
        trees     = round(total_em * 50)
        st.info(f"✈️ Equivalent to **{flight_eq}** flights of 1,000 km")
        st.info(f"🚗 Or driving **{car_eq}** × 1,000 km")
        st.info(f"🌳 Plant **{trees}** trees to offset")

    with col6:
        st.subheader("🌿 Carbon Offsetting Suggestions")
        st.info("- 🚆 Switch to public transport or EVs")
        st.info("- 💡 Use LED lighting")
        st.info("- 🍏 Reduce meat consumption")
        st.info("- ♻️ Recycle & compost")
        st.info("- ☀️ Install solar panels")

    st.success("✅ Data Successfully Calculated!")

# ─── Reset button with callback ────────────────────────────────────────────────
st.button("Enter New Data", on_click=reset_inputs)

# ─── Emission history table ──────────────────────────────────────────────────
st.subheader("📜 Emission History")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df)
else:
    st.info("No previous calculations found.")
