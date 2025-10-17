import streamlit as st
import requests

st.title("Car Price Prediction (via FastAPI)")

# --- Input fields ---
brand = st.text_input("Brand", "Toyota")
model_name = st.text_input("Model", "Corolla")
model_year = st.number_input("Model Year", min_value=1990, max_value=2030, value=2015)
milage = st.number_input("Milage", min_value=0, max_value=1000000, value=100)
fuel_type = st.text_input("Fuel Type", "Petrol")
engine = st.text_input("Engine", "1.8L")
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
accident = st.selectbox("Accident", [0, 1])
clean_title = st.selectbox("Clean Title", [0, 1])

# --- FastAPI URL ---
API_URL = "http://127.0.0.1:8000/predict"  # your FastAPI endpoint

# --- Predict button ---
if st.button("Predict Price"):
    # Prepare input JSON
    payload = {
        "brand": brand,
        "model": model_name,
        "model_year": model_year,
        "milage": milage,
        "fuel_type": fuel_type,
        "engine": engine,
        "transmission": transmission,
        "accident": accident,
        "clean_title": clean_title
    }

    try:
        # Send POST request to FastAPI
        response = requests.post(API_URL, json=payload)
        data = response.json()

        # Display result
        if "predicted_price" in data:
            st.success(f"Predicted Car Price: ₹{data['predicted_price']:,.2f}")
        else:
            st.error(f"Error: {data.get('error', 'Unknown error')}")

    except Exception as e:
        st.error(f"Could not connect to FastAPI. Details: {e}")
