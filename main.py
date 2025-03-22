import streamlit as st
import pandas as pd

# Emission factors for different countries
EMISSION_FACTOR = {
    "India": {"Transportation": 0.14, "Electricity": 0.8, "Diet": 1.25, "Waste": 0.1},
    "USA": {"Transportation": 0.24, "Electricity": 0.45, "Diet": 2.0, "Waste": 0.12},
    "UK": {"Transportation": 0.21, "Electricity": 0.3, "Diet": 1.8, "Waste": 0.09},
}

st.set_page_config(layout="wide", page_title="Personal Carbon Calculator")
st.title("🌍 Personal Carbon Calculator App")

# Initialize session state for history and input values
if "history" not in st.session_state:
    st.session_state.history = []

if "inputs" not in st.session_state:
    st.session_state.inputs = {
        "country": "India",
        "distance": 50.0,
        "electricity": 500.0,
        "waste": 10.0,
        "diet": 2
    }

# Reset function
def reset_inputs():
    st.session_state.inputs = {
        "country": "India",
        "distance": 50.0,
        "electricity": 500.0,
        "waste": 10.0,
        "diet": 2
    }

# Select country
st.subheader("🌍 Your Country")
st.session_state.inputs["country"] = st.selectbox("Select", list(EMISSION_FACTOR.keys()), index=list(EMISSION_FACTOR.keys()).index(st.session_state.inputs["country"]))

col1, col2 = st.columns(2)
with col1:
    st.subheader("🚗 Daily Commute Distance (km)")
    st.session_state.inputs["distance"] = st.slider("Distance", 0.0, 100.0, st.session_state.inputs["distance"])

    st.subheader("💡 Monthly Electricity Consumption (kWh)")
    st.session_state.inputs["electricity"] = st.slider("Electricity", 0.0, 1000.0, st.session_state.inputs["electricity"])

with col2:
    st.subheader("🗑️ Weekly Waste Generated (kg)")
    st.session_state.inputs["waste"] = st.slider("Waste", 0.0, 100.0, st.session_state.inputs["waste"])

    st.subheader("🍎 Meals per Day")
    st.session_state.inputs["diet"] = st.number_input("Diet", 0, 3, st.session_state.inputs["diet"])

# Convert to yearly values
distance = st.session_state.inputs["distance"] * 365
electricity = st.session_state.inputs["electricity"] * 12
waste = st.session_state.inputs["waste"] * 365
diet = st.session_state.inputs["diet"] * 52
country = st.session_state.inputs["country"]

# Compute emissions
transportation_emission = round(EMISSION_FACTOR[country]["Transportation"] * distance / 1000, 2)
electricity_emission = round(EMISSION_FACTOR[country]["Electricity"] * electricity / 1000, 2)
diet_emission = round(EMISSION_FACTOR[country]["Diet"] * diet / 1000, 2)
waste_emission = round(EMISSION_FACTOR[country]["Waste"] * waste / 1000, 2)

total_emissions = round(transportation_emission + electricity_emission + diet_emission + waste_emission, 2)

if st.button("Calculate CO2 Emissions"):
    # Append new data to history list
    st.session_state.history.append({
        "Country": country,
        "Transport": transportation_emission,
        "Electricity": electricity_emission,
        "Diet": diet_emission,
        "Waste": waste_emission,
        "Total CO2": total_emissions
    })

    st.header("📊 Results")
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("📌 Category Breakdown (per year)")
        st.info(f"🚗 **Transport:** {transportation_emission} tonnes CO₂/year")
        st.info(f"💡 **Electricity:** {electricity_emission} tonnes CO₂/year")
        st.info(f"🍎 **Diet:** {diet_emission} tonnes CO₂/year")
        st.info(f"🗑️ **Waste:** {waste_emission} tonnes CO₂/year")

    with col4:
        st.subheader("🌍 Total Carbon Footprint (per year)")
        st.success(f"🔥 **Total: {total_emissions} tonnes CO₂/year**")

        # Gamification Badges
        if total_emissions < 1:
            st.success("🏆 **Gold Badge: Excellent! You're eco-friendly!**")
        elif total_emissions < 1.5:
            st.success("🥈 **Silver Badge: Good! Keep reducing!**")
        else:
            st.success("🥉 **Bronze Badge: Reduce emissions for a better future!**")

    # CO₂ Equivalents & Carbon Offsetting Suggestions
    st.divider()
    col5, col6 = st.columns(2)
    
    with col5:
        st.subheader("🌎 CO₂ Equivalents (per year)")
        flight_equivalent = round(total_emissions / 0.18, 1)  # Avg. CO₂ per passenger flight per km
        car_equivalent = round(total_emissions / 0.4, 1)  # Avg. CO₂ per km for a car
        tree_offset = round(total_emissions * 50)  # Approx. 50 trees absorb 1 tonne CO₂ in a year

        st.info(f"✈️ **Your emissions equal traveling** {flight_equivalent} **times in a plane for 1000 km**")
        st.info(f"🚗 **Or driving a car for** {car_equivalent} **thousand km**")
        st.info(f"🌳 **You'd need to plant** {tree_offset} **trees per year to offset this!**")

    with col6:
        st.subheader("🌿 Carbon Offsetting Suggestions (per year)")
        st.info("- 🚆 Switch to **public transport** or **electric vehicles**")
        st.info("- 💡 Reduce **electricity usage** by switching to **LED lights**")
        st.info("- 🍏 Follow a **low-carbon diet** by reducing **meat** consumption")
        st.info("- 🗑️ **Recycle waste** and **compost organic waste**")
        st.info("- 🌞 **Use renewable energy** sources like **solar panels**")

    st.success("✅ Data Successfully Calculated!")

# Enter New Data Button
if st.button("Enter New Data"):
    reset_inputs()
    st.rerun()

# Show History
st.subheader("📜 Emission History")
if len(st.session_state.history) > 0:
    df = pd.DataFrame(st.session_state.history)  # Convert list to DataFrame
    st.dataframe(df)
else:
    st.info("No previous calculations found.")
