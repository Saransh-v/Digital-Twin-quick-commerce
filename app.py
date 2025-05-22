
import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("rf_eta_model.pkl")

st.set_page_config(page_title="Quick Commerce ETA Predictor", layout="centered")
st.title("📦 Quick Commerce ETA Prediction (Dadar East)")

# User Inputs
st.header("🔢 Input Delivery Parameters")
sku = st.slider("Number of SKUs", 1, 6, 3)
distance = st.slider("Distance (km)", 1.0, 5.0, 2.5)
speed = st.slider("Rider Speed (km/h)", 25, 45, 35)

ctype = st.selectbox("Customer Type", ["New", "Returning", "Prime"])
window = st.selectbox("Time Window", [
    "08:00–10:00", "09:00–11:00", "10:00–12:00", "11:00–13:00",
    "12:00–14:00", "13:00–15:00", "14:00–16:00", "15:00–17:00",
    "16:00–18:00", "17:00–19:00", "18:00–20:00", "19:00–21:00",
    "20:00–22:00", "21:00–23:00", "22:00–00:00", "23:00–01:00"
])
shift = st.selectbox("Shift", ["Morning", "Evening"])

# Build input row from user input
raw_row = {
    'SKU_Count': sku,
    'Zone_Distance_km': distance,
    'Rider_Speed_kmph': speed,
    'Speed_kmph': speed
}

# Handle customer type encoding
if ctype == "Returning":
    raw_row['Customer_Type_Returning'] = 1
elif ctype == "Prime":
    raw_row['Customer_Type_Prime'] = 1

# Handle time window
raw_row[f"Time_Window_{window}"] = 1

# Handle shift
if shift == "Morning":
    raw_row['Shift_Morning'] = 1

# Final input DataFrame, reindexed to match model
X_input = pd.DataFrame([raw_row])
X_input = X_input.reindex(columns=model.feature_names_in_, fill_value=0)

# Predict
pred_eta = model.predict(X_input)[0]
st.metric("📦 Predicted ETA", f"{round(pred_eta, 2)} minutes")

# Alert logic
st.header("⚠️ Delay Alert Simulation")
deviation = st.number_input("Enter delay deviation (in minutes)", value=0.0)
if pred_eta > 18 or deviation > 2:
    st.error("🚨 Delay Alert Triggered!")
else:
    st.success("✅ Delivery within SLA.")

st.markdown("---")
st.caption("Built as part of a Digital Twin project for Quick Commerce delivery in Dadar East, Mumbai.")
