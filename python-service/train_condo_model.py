"""
train_condo_model.py — Specialized model for HIGH-RISE / CONDO properties only.

Run: python train_condo_model.py
Creates: models/condo_model.pkl, models/condo_model_features.pkl, models/condo_model_metadata.pkl
"""

import os
import pickle

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split

from services.db import query_df

MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODELS_DIR, exist_ok=True)

print("=" * 50)
print(" Condo / High-Rise Price Model")
print("=" * 50)

print("\nLoading high-rise properties from database...")
df = query_df("""
    SELECT
        price,
        state,
        city,
        property_type,
        size_sqft,
        bedrooms,
        bathrooms,
        car_parks,
        price_per_sqft
    FROM properties
    WHERE price > 0
      AND size_sqft > 0
      AND state IS NOT NULL
      AND (
        LOWER(property_type) LIKE '%condominium%'
        OR LOWER(property_type) LIKE '%apartment%'
        OR LOWER(property_type) LIKE '%flat%'
        OR LOWER(property_type) LIKE '%service residence%'
        OR LOWER(property_type) LIKE '%condo%'
      )
""")
print(f"High-rise rows loaded: {len(df):,}")

if len(df) < 100:
    print("\nNot enough condo data to train a model (need at least 100 rows).")
    raise SystemExit(1)

df_dosm = query_df("""
    SELECT state, AVG(mean_household_income) AS income_mean
    FROM dosm_demographics
    WHERE mean_household_income IS NOT NULL
    GROUP BY state
""")

df = pd.merge(df, df_dosm, on="state", how="left")
national_avg = df_dosm["income_mean"].mean()
df["income_mean"] = df["income_mean"].fillna(national_avg)


def remove_outliers(dataframe, col, lower_pct=0.05, upper_pct=0.95):
    lo = dataframe[col].quantile(lower_pct)
    hi = dataframe[col].quantile(upper_pct)
    return dataframe[(dataframe[col] >= lo) & (dataframe[col] <= hi)]


before = len(df)
df = remove_outliers(df, "price")
df = remove_outliers(df, "size_sqft")
print(f"After outlier removal: {before:,} -> {len(df):,} rows")

df = df.dropna(subset=["price", "state", "size_sqft"])
df["bedrooms"] = df["bedrooms"].fillna(df["bedrooms"].median())
df["bathrooms"] = df["bathrooms"].fillna(df["bathrooms"].median())
df["car_parks"] = df["car_parks"].fillna(0)

city_counts = df["city"].value_counts()
df["city_grouped"] = df["city"].where(
    df["city"].isin(city_counts[city_counts >= 5].index),
    other="Other",
)

features_df = df[
    ["state", "city_grouped", "income_mean", "size_sqft", "bedrooms", "bathrooms", "car_parks"]
]

X = pd.get_dummies(features_df, columns=["state", "city_grouped"])
y = df["price"]

print(f"\nFeature columns: {X.shape[1]}")
print(f"Training rows: {len(X):,}")

feature_columns = X.columns.tolist()
with open(os.path.join(MODELS_DIR, "condo_model_features.pkl"), "wb") as f:
    pickle.dump(feature_columns, f)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nTraining Gradient Boosting Regressor...")
model = GradientBoostingRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=5,
    min_samples_leaf=3,
    subsample=0.8,
    random_state=42,
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n{'='*40}")
print(f"  Condo Model Results")
print(f"  MAE: MYR {mae:,.0f}")
print(f"  R²:  {r2:.3f}")
print(f"{'='*40}")

cv_scores = cross_val_score(model, X, y, cv=5, scoring="r2")
print(f"\n  Mean CV R²: {cv_scores.mean():.3f} (±{cv_scores.std():.3f})")

with open(os.path.join(MODELS_DIR, "condo_model.pkl"), "wb") as f:
    pickle.dump(model, f)
print("\nCondo model saved -> models/condo_model.pkl")

metadata = {
    "mae": round(mae, 0),
    "r2": round(r2, 3),
    "cv_r2_mean": round(cv_scores.mean(), 3),
    "cv_r2_std": round(cv_scores.std(), 3),
    "training_rows": len(X_train),
    "feature_count": X.shape[1],
    "model_type": "GradientBoosting (high-rise/condo only)",
    "algorithm": "GradientBoostingRegressor",
}
with open(os.path.join(MODELS_DIR, "condo_model_metadata.pkl"), "wb") as f:
    pickle.dump(metadata, f)
print("Metadata saved -> models/condo_model_metadata.pkl")
