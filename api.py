import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import os

# --- 1️⃣ Load model & transformer using relative paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "notebooks", "best_xgb_model.pkl")
preprocessor_path = os.path.join(BASE_DIR, "notebooks", "preprocessor.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(preprocessor_path, "rb") as f:
    preprocessor = pickle

# --- 2️⃣ FastAPI app ---
app = FastAPI(title="Car Price Prediction API")

# --- 3️⃣ Input schema ---
class CarInput(BaseModel):
    brand: str
    model: str
    model_year: int
    milage: int
    fuel_type: str
    engine: str
    transmission: str
    accident: int
    clean_title: int

# --- 4️⃣ POST endpoint ---
@app.post("/predict")
def predict_car_price(car: CarInput):
    try:
        # Convert input JSON to DataFrame
        input_df = pd.DataFrame([car.dict()])

        # Ensure datatypes match training data
        input_df = input_df.astype({
            'brand': 'object',
            'model': 'object',
            'model_year': 'int64',
            'milage': 'int32',
            'fuel_type': 'object',
            'engine': 'object',
            'transmission': 'object',
            'accident': 'int64',
            'clean_title': 'int64'
        })

        # Transform input using preprocessor
        X_transformed = preprocessor.transform(input_df)

        # Predict car price
        predicted_price = model.predict(X_transformed)[0]

        return {"predicted_price": float(predicted_price)}

    except Exception as e:
        # Handle unseen categories or other errors gracefully
        return {
            "error": "Input contains unknown or invalid values. Please provide valid data.",
            "details": str(e)
        }
