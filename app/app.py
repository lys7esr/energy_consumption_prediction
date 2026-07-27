import streamlit as st
import pandas as pd
import joblib

# Load the saved model
model = joblib.load("../models/energy_model.pkl")

# Title
st.title("⚡ Household Energy Consumption Predictor")

st.write("Enter the household details below to predict energy consumption.")

# User Inputs
household_size = st.number_input(
    "Household Size",
    min_value=1,
    max_value=20,
    value=4
)

avg_temperature = st.number_input(
    "Average Temperature (°C)",
    min_value=-20.0,
    max_value=60.0,
    value=28.0
)

has_ac = st.selectbox(
    "Has AC?",
    ["No", "Yes"]
)

peak_usage = st.number_input(
    "Peak Hours Usage (kWh)",
    min_value=0.0,
    value=5.0
)

date = st.date_input("Select Date")

electricity_rate = st.number_input(
    "Electricity Cost (₹ per kWh)",
    min_value=0.0,
    value=8.0,
    step=0.5
)

# Convert AC to numeric
if has_ac == "Yes":
    has_ac = 1
else:
    has_ac = 0

# Extract date features
year = date.year
month = date.month
day = date.day
day_of_week = date.weekday()

# Predict button
if st.button("Predict Energy Consumption"):

    input_data = pd.DataFrame({
        "Household_Size": [household_size],
        "Avg_Temperature_C": [avg_temperature],
        "Has_AC": [has_ac],
        "Peak_Hours_Usage_kWh": [peak_usage],
        "Year": [year],
        "Month": [month],
        "Day": [day],
        "DayOfWeek": [day_of_week]
    })

    prediction = model.predict(input_data)[0]

    estimated_cost = prediction * electricity_rate

    st.success(
        f"Predicted Energy Consumption: {prediction:.2f} kWh"
    )
    st.info(
        f"💰 Estimated Electricity Cost: ₹{estimated_cost:.2f}"
    )

    st.caption(
        "Note: Electricity cost is estimated using the user-provided cost per kWh."
    )