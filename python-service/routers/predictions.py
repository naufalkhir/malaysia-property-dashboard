from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import os

router = APIRouter(prefix="/predict", tags=["Predictions"])


# We updated this to ask for size and bedrooms!
class PredictionInput(BaseModel):
    state: str
    property_type: str
    size_sqft: float
    bedrooms: int


BASE_DIR = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "../models/price_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "../models/model_features.pkl")
INCOME_DATA_PATH = os.path.join(BASE_DIR, "../models/hh_income_state.csv")

model = None
feature_columns = None
income_dict = {}


def load_resources():
    global model, feature_columns, income_dict
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
    if os.path.exists(FEATURES_PATH):
        with open(FEATURES_PATH, "rb") as f:
            feature_columns = pickle.load(f)
    if os.path.exists(INCOME_DATA_PATH):
        income_df = pd.read_csv(INCOME_DATA_PATH)
        income_2022 = income_df[income_df["date"] == "2022-01-01"]
        income_dict = dict(zip(income_2022["state"], income_2022["income_mean"]))


load_resources()


@router.post("/")
def predict(data: PredictionInput):
    if model is None or feature_columns is None:
        raise HTTPException(status_code=503, detail="Model not trained yet.")

    prop_type = str(data.property_type).lower()
    if "condominium" in prop_type or "apartment" in prop_type or "flat" in prop_type:
        category = "High-Rise"
    elif "terrace" in prop_type or "link" in prop_type:
        category = "Terrace"
    elif "semi-d" in prop_type or "cluster" in prop_type:
        category = "Semi-D/Cluster"
    elif "bungalow" in prop_type or "villa" in prop_type:
        category = "Bungalow"
    else:
        category = "Other"

    state_income = income_dict.get(data.state, 5000)

    # Added size_sqft and bedrooms to the input dataframe!
    input_df = pd.DataFrame(
        [
            {
                "State": data.state,
                "Property_Category": category,
                "income_mean": state_income,
                "size_sqft": data.size_sqft,
                "bedrooms": data.bedrooms,
            }
        ]
    )

    input_encoded = pd.get_dummies(input_df)
    input_aligned = input_encoded.reindex(columns=feature_columns, fill_value=0)

    predicted = float(model.predict(input_aligned)[0])

    return {
        "predicted_price": round(predicted, 2),
        "low": round(predicted * 0.85, 2),
        "high": round(predicted * 1.15, 2),
        "currency": "MYR",
    }
