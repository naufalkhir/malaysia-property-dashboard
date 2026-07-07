"""
predictions.py — ML price prediction endpoints

Endpoints:
  POST /predict        — general model (all property types)
  POST /predict/condo  — specialized condo model (more accurate for high-rise)
  GET  /predict/info   — model metadata (R², MAE, training rows)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import os

router = APIRouter(prefix="/predict", tags=["Predictions"])

MODELS_DIR = os.path.join(os.path.dirname(__file__), "../models")


class PredictionInput(BaseModel):
    state: str
    property_type: str
    size_sqft: float
    bedrooms: int
    bathrooms: int | None = None
    car_parks: int | None = None


class CondoPredictionInput(BaseModel):
    state: str
    city: str | None = None
    size_sqft: float
    bedrooms: int
    bathrooms: int | None = None
    car_parks: int | None = None


def _model_path(name: str) -> str:
    return os.path.join(MODELS_DIR, name)


GENERAL_MODEL_PATH = _model_path("price_model.pkl")
GENERAL_FEATURES_PATH = _model_path("model_features.pkl")
GENERAL_META_PATH = _model_path("model_metadata.pkl")
CONDO_MODEL_PATH = _model_path("condo_model.pkl")
CONDO_FEATURES_PATH = _model_path("condo_model_features.pkl")
CONDO_META_PATH = _model_path("condo_model_metadata.pkl")
INCOME_CSV_PATH = _model_path("hh_income_state.csv")

general_model = None
general_features = None
general_meta: dict = {}
condo_model = None
condo_features = None
condo_meta: dict = {}
income_dict: dict = {}


def _load_pkl(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None


def load_resources():
    global general_model, general_features, general_meta
    global condo_model, condo_features, condo_meta
    global income_dict

    general_model = _load_pkl(GENERAL_MODEL_PATH)
    general_features = _load_pkl(GENERAL_FEATURES_PATH)
    general_meta = _load_pkl(GENERAL_META_PATH) or {}

    condo_model = _load_pkl(CONDO_MODEL_PATH)
    condo_features = _load_pkl(CONDO_FEATURES_PATH)
    condo_meta = _load_pkl(CONDO_META_PATH) or {}

    if os.path.exists(INCOME_CSV_PATH):
        df = pd.read_csv(INCOME_CSV_PATH)
        latest = df[df["date"] == df["date"].max()]
        income_dict = dict(zip(latest["state"], latest["income_mean"]))
    else:
        income_dict = {
            "Selangor": 8209,
            "Kuala Lumpur": 11062,
            "Putrajaya": 14040,
            "Johor": 6508,
            "Penang": 6954,
            "Perak": 5003,
            "Sabah": 4209,
            "Sarawak": 5186,
            "Kedah": 4429,
            "Kelantan": 3516,
            "Melaka": 6478,
            "Negeri Sembilan": 6285,
            "Pahang": 4905,
            "Perlis": 4286,
            "Terengganu": 4360,
            "Labuan": 5726,
        }


load_resources()


def simplify_type(t: str) -> str:
    t = str(t).lower()
    if any(x in t for x in ["condominium", "service residence", "apartment", "flat", "condo"]):
        return "High-Rise"
    if any(x in t for x in ["terrace", "link", "town house", "townhouse"]):
        return "Terrace"
    if any(x in t for x in ["semi d", "semi-d", "cluster"]):
        return "Semi-D/Cluster"
    if any(x in t for x in ["bungalow", "villa", "detached"]):
        return "Bungalow"
    return "Other"


def _make_prediction_df(raw_features: dict, feature_columns: list) -> pd.DataFrame:
    df = pd.DataFrame([raw_features])
    cat_cols = [c for c in df.columns if df[c].dtype == object]
    df_encoded = pd.get_dummies(df, columns=cat_cols)
    return df_encoded.reindex(columns=feature_columns, fill_value=0)


@router.post("/")
def predict(data: PredictionInput):
    if general_model is None or general_features is None:
        raise HTTPException(
            status_code=503,
            detail="General model not ready. Run: python train_model.py",
        )

    state_income = income_dict.get(data.state, income_dict.get("Selangor", 6000))

    raw = {
        "State": data.state,
        "Property_Category": simplify_type(data.property_type),
        "income_mean": state_income,
        "size_sqft": data.size_sqft,
        "bedrooms": data.bedrooms,
    }

    if general_features and "bathrooms" in general_features and data.bathrooms is not None:
        raw["bathrooms"] = data.bathrooms
    if general_features and "car_parks" in general_features and data.car_parks is not None:
        raw["car_parks"] = data.car_parks

    df_aligned = _make_prediction_df(raw, general_features)
    predicted = float(general_model.predict(df_aligned)[0])

    return {
        "predicted_price": round(predicted, 0),
        "low": round(predicted * 0.85, 0),
        "high": round(predicted * 1.15, 0),
        "currency": "MYR",
        "model": "general",
        "model_r2": general_meta.get("r2"),
        "model_mae": general_meta.get("mae"),
        "disclaimer": "Indicative estimate only. Not a professional valuation.",
    }


@router.post("/condo")
def predict_condo(data: CondoPredictionInput):
    if condo_model is None or condo_features is None:
        raise HTTPException(
            status_code=503,
            detail="Condo model not trained yet. Run: python train_condo_model.py",
        )

    state_income = income_dict.get(data.state, income_dict.get("Kuala Lumpur", 11062))

    raw = {
        "state": data.state,
        "city_grouped": data.city or "Other",
        "income_mean": state_income,
        "size_sqft": data.size_sqft,
        "bedrooms": data.bedrooms,
        "bathrooms": data.bathrooms or 1,
        "car_parks": data.car_parks or 1,
    }

    df_aligned = _make_prediction_df(raw, condo_features)
    predicted = float(condo_model.predict(df_aligned)[0])

    return {
        "predicted_price": round(predicted, 0),
        "low": round(predicted * 0.87, 0),
        "high": round(predicted * 1.13, 0),
        "currency": "MYR",
        "model": "condo-specialist",
        "model_r2": condo_meta.get("r2"),
        "model_mae": condo_meta.get("mae"),
        "cv_r2": condo_meta.get("cv_r2_mean"),
        "disclaimer": "Indicative estimate only. Not a professional valuation.",
    }


@router.get("/info")
def model_info():
    return {
        "general_model": {
            "available": general_model is not None,
            "type": general_meta.get("model_type", "RandomForest"),
            "r2": general_meta.get("r2"),
            "mae_myr": general_meta.get("mae"),
            "training_rows": general_meta.get("training_rows"),
            "features": general_meta.get("feature_count"),
        },
        "condo_model": {
            "available": condo_model is not None,
            "type": condo_meta.get("model_type", "GradientBoosting"),
            "r2": condo_meta.get("r2"),
            "mae_myr": condo_meta.get("mae"),
            "cv_r2": condo_meta.get("cv_r2_mean"),
            "training_rows": condo_meta.get("training_rows"),
            "features": condo_meta.get("feature_count"),
        },
        "income_states_loaded": len(income_dict),
    }
