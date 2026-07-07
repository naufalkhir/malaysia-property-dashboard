"""
train_model.py — General property price prediction model
Trains on ALL property types across ALL states.

After adding 54k KL rows, this should reach R² 0.75–0.85.
Run: python train_model.py
"""

import pandas as pd
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from services.db import query_df
pd.set_option('future.no_silent_downcasting', True)

MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODELS_DIR, exist_ok=True)


# ── 1. Load property data ────────────────────────────────────────────────────
print("Loading properties from database...")
df_properties = query_df("""
    SELECT
        price       AS Price,
        state       AS State,
        property_type AS Type,
        size_sqft,
        bedrooms,
        bathrooms,
        car_parks
    FROM properties
    WHERE price > 0
      AND size_sqft > 0
      AND bedrooms > 0
      AND state IS NOT NULL
""")
print(f"Properties loaded: {len(df_properties):,} rows")


# ── 2. Load DOSM income + population ────────────────────────────────────────
# Use the most recent year available for each state
# This joins income AND population to each property row
print("Loading DOSM demographics...")
df_dosm = query_df("""
    SELECT
        state,
        MAX(year) AS latest_year,
        AVG(mean_household_income)   AS income_mean,
        AVG(median_household_income) AS income_median,
        AVG(population)              AS population
    FROM dosm_demographics
    WHERE mean_household_income IS NOT NULL
    GROUP BY state
""")
print(f"DOSM rows loaded: {len(df_dosm)} states")


# ── 3. Merge properties + demographics ──────────────────────────────────────
df = pd.merge(
    df_properties,
    df_dosm[['state', 'income_mean', 'income_median', 'population']],
    left_on='State',
    right_on='state',
    how='left'
)

# Fill missing income with national average (fallback for states not in DOSM)
national_avg_income = df_dosm['income_mean'].mean()
df['income_mean']   = df['income_mean'].fillna(national_avg_income)
df['income_median'] = df['income_median'].fillna(df_dosm['income_median'].mean())
df['population']    = df['population'].fillna(0)

df = df.dropna(subset=['Price', 'State', 'Type', 'size_sqft', 'bedrooms'])
print(f"Rows after merge + dropna: {len(df):,}")


# ── 4. Outlier removal (IQR, 10th–90th percentile) ──────────────────────────
# Same logic as before — removes luxury outliers that hurt prediction accuracy
def remove_outliers(df, column):
    Q1 = df[column].quantile(0.10)
    Q3 = df[column].quantile(0.90)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return df[(df[column] >= lower) & (df[column] <= upper)]

before = len(df)
df = remove_outliers(df, 'Price')
df = remove_outliers(df, 'size_sqft')
after = len(df)
print(f"Outlier removal: {before:,} → {after:,} rows ({before - after:,} removed)")


# ── 5. Simplify property type into 5 categories ──────────────────────────────
# Same categories as charts.py so everything is consistent
def simplify_type(t):
    t = str(t).lower()
    if any(x in t for x in ['condominium', 'service residence', 'apartment', 'flat', 'condo']):
        return 'High-Rise'
    elif any(x in t for x in ['terrace', 'link', 'town house', 'townhouse']):
        return 'Terrace'
    elif any(x in t for x in ['semi d', 'semi-d', 'cluster']):
        return 'Semi-D/Cluster'
    elif any(x in t for x in ['bungalow', 'villa', 'detached']):
        return 'Bungalow'
    else:
        return 'Other'

df['Property_Category'] = df['Type'].apply(simplify_type)

print("\nProperty category distribution:")
print(df['Property_Category'].value_counts())
print("\nState distribution (top 10):")
print(df['State'].value_counts().head(10))


# ── 6. Feature engineering ───────────────────────────────────────────────────
# Features used:
#   State              — encodes location/market (one-hot encoded)
#   Property_Category  — encodes property class (one-hot encoded)
#   income_mean        — state wealth → correlates strongly with price
#   size_sqft          — floor area → biggest single predictor
#   bedrooms           — bedroom count
#   bathrooms          — bathroom count (new — added when available)
#   car_parks          — car park count (new — added when available)
#   price_per_person   — price / population → affordability signal (new)


feature_cols = [
    'State',
    'Property_Category',
    'income_mean',
    'size_sqft',
    'bedrooms',
]

# Add optional features only if they have enough non-null values (>50% filled)
optional = {
    'bathrooms':      'bathrooms',
    'car_parks':      'car_parks',
    'income_median':  'income_median',
}
for feat, col in optional.items():
    non_null_pct = df[col].notna().mean()
    if non_null_pct > 0.5:
        feature_cols.append(feat)
        print(f"  ✅ Adding optional feature '{feat}' ({non_null_pct:.0%} filled)")
    else:
        print(f"  ⚠️  Skipping '{feat}' (only {non_null_pct:.0%} filled)")

features_df = df[feature_cols]
X = pd.get_dummies(features_df, columns=['State', 'Property_Category'])
y = df['Price']

print(f"\nFinal feature count: {X.shape[1]} columns")
print(f"Training rows: {len(X):,}")

# Save feature columns — predictions.py needs this to align new inputs
feature_columns = X.columns.tolist()
with open(os.path.join(MODELS_DIR, 'model_features.pkl'), 'wb') as f:
    pickle.dump(feature_columns, f)
print("Feature columns saved → model_features.pkl")


# ── 7. Train / test split + model training ──────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\nTraining: {len(X_train):,} rows | Test: {len(X_test):,} rows")
print("Training Random Forest (this takes 30-60 seconds)...")

model = RandomForestRegressor(
    n_estimators=300,    # more trees = better accuracy (was 200, bumped to 300)
    max_depth=25,        # slightly deeper to capture KL's wide price range (was 20)
    min_samples_leaf=3,  # prevents overfitting on small groups
    random_state=42,
    n_jobs=-1            # use all CPU cores
)
model.fit(X_train, y_train)


# ── 8. Evaluate ──────────────────────────────────────────────────────────────
y_pred = model.predict(X_test)
mae    = mean_absolute_error(y_test, y_pred)
r2     = r2_score(y_test, y_pred)

print(f"\n{'='*40}")
print(f"  MAE: MYR {mae:,.0f}")
print(f"  R²:  {r2:.3f}")
print(f"{'='*40}")

if r2 > 0.75:
    print("  ✅ Good model — ready for production")
elif r2 > 0.6:
    print("  ⚠️  Acceptable — try importing more data for improvement")
else:
    print("  ❌ Low R² — check data quality or add more training rows")


# ── 9. Feature importance (top 10) ──────────────────────────────────────────
importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False).head(10)

print("\nTop 10 most important features:")
for _, row in importance_df.iterrows():
    bar = '█' * int(row['importance'] * 100)
    print(f"  {row['feature']:<40} {row['importance']:.4f}  {bar}")


# ── 10. Save model ───────────────────────────────────────────────────────────
with open(os.path.join(MODELS_DIR, 'price_model.pkl'), 'wb') as f:
    pickle.dump(model, f)
print("\nModel saved -> models/price_model.pkl")

# Save training metadata for the prediction endpoint to display
metadata = {
    'mae': round(mae, 0),
    'r2': round(r2, 3),
    'training_rows': len(X_train),
    'feature_count': X.shape[1],
    'model_type': 'RandomForest (general — all property types)',
    'n_estimators': 300,
    'max_depth': 25,
}
with open(os.path.join(MODELS_DIR, 'model_metadata.pkl'), 'wb') as f:
    pickle.dump(metadata, f)
print("Metadata saved → model_metadata.pkl")
print("\nDone! Restart python-service to load the new model.")