
import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("rf_eta_model.pkl")
columns = ['SKU_Count', 'Zone_Distance_km', 'Rider_Speed_kmph',
           'Customer_Type_Returning', 'Customer_Type_Prime',
           'Time_Window_10:00-12:00', 'Time_Window_12:00-14:00',
           'Shift_Morning']

st.set_page_config(page_title="Quick Commerce ETA Predictor", layout="centered")
st.title("📦 Quick Commerce ETA Prediction (Dadar East)")

# User Inputs
st.header("🔢 Input Delivery Parameters")
sku = st.slider("Number of SKUs", 1, 6, 3)
distance = st.slider("Distance (km)", 1.0, 5.0, 2.5)
speed = st.slider("Rider Speed (km/h)", 25, 45, 35)

ctype = st.selectbox("Customer Type", ["New", "Returning", "Prime"])
window = st.selectbox("Time Window", ["08:00-10:00", "10:00-12:00", "12:00-14:00"])
shift = st.selectbox("Shift", ["Morning", "Evening"])

# Prepare input for model
row = {
    'SKU_Count': sku,
    'Zone_Distance_km': distance,
    'Rider_Speed_kmph': speed,
    'Customer_Type_Returning': 1 if ctype == "Returning" else 0,
    'Customer_Type_Prime': 1 if ctype == "Prime" else 0,
    'Time_Window_10:00-12:00': 1 if window == "10:00-12:00" else 0,
    'Time_Window_12:00-14:00': 1 if window == "12:00-14:00" else 0,
    'Shift_Morning': 1 if shift == "Morning" else 0
}
X_input = pd.DataFrame([row])

# Predict ETA
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
