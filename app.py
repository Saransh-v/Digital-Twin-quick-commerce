
import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("rf_eta_model.pkl")
expected_features = list(model.feature_names_in_)

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

# Initialize input row with zeros
row = {feature: 0 for feature in expected_features}

# Set values from user input
row['SKU_Count'] = sku
row['Zone_Distance_km'] = distance
row['Rider_Speed_kmph'] = speed
if 'Speed_kmph' in row:
    row['Speed_kmph'] = speed
if 'Customer_Type_Returning' in row and ctype == "Returning":
    row['Customer_Type_Returning'] = 1
if 'Customer_Type_Prime' in row and ctype == "Prime":
    row['Customer_Type_Prime'] = 1
time_feature = f"Time_Window_{window}"
if time_feature in row:
    row[time_feature] = 1
if 'Shift_Morning' in row:
    row['Shift_Morning'] = 1 if shift == "Morning" else 0

# Convert to DataFrame and predict
X_input = pd.DataFrame([row])
pred_eta = model.predict(X_input)[0]
st.metric("📦 Predicted ETA", f"{round(pred_eta, 2)} minutes")

# Delay alert logic
st.header("⚠️ Delay Alert Simulation")
deviation = st.number_input("Enter delay deviation (in minutes)", value=0.0)
if pred_eta > 18 or deviation > 2:
    st.error("🚨 Delay Alert Triggered!")
else:
    st.success("✅ Delivery within SLA.")

st.markdown("---")
st.caption("Built as part of a Digital Twin project for Quick Commerce delivery in Dadar East, Mumbai.")
