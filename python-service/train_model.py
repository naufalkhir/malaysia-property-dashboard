import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from services.db import query_df

print("Loading data directly from MySQL database...")

# Pull data
df_properties = query_df("""
    SELECT price as Price, state as State, 
           property_type as Type, size_sqft, bedrooms
    FROM properties 
    WHERE price > 0 
    AND size_sqft > 0 
    AND bedrooms > 0 
    AND state IS NOT NULL
""")

df_income = query_df("""
    SELECT state, mean_household_income as income_mean 
    FROM dosm_demographics 
    WHERE year = 2022
""")

df = pd.merge(df_properties, df_income, left_on="State", right_on="state", how="left")
df = df.dropna(subset=["Price", "State", "Type", "size_sqft", "bedrooms"])

# --- THE FIX: OUTLIER REMOVAL (IQR Method) ---
print(f"Rows before outlier removal: {len(df)}")

def remove_outliers(df, column):
    Q1 = df[column].quantile(0.10) # 10th percentile
    Q3 = df[column].quantile(0.90) # 90th percentile
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

# Remove extreme prices and extreme sizes
df = remove_outliers(df, 'Price')
df = remove_outliers(df, 'size_sqft')

print(f"Rows after outlier removal: {len(df)}")
# ---------------------------------------------

def simplify_type(t):
    t = str(t).lower()
    if "condominium" in t or "service residence" in t or "apartment" in t or "flat" in t:
        return "High-Rise"
    elif "terrace" in t or "link" in t:
        return "Terrace"
    elif "semi d" in t or "cluster" in t:
        return "Semi-D/Cluster"
    elif "bungalow" in t or "villa" in t:
        return "Bungalow"
    else:
        return "Other"

df["Property_Category"] = df["Type"].apply(simplify_type)

features_df = df[["State", "Property_Category", "income_mean", "size_sqft", "bedrooms"]]
X = pd.get_dummies(features_df, columns=["State", "Property_Category"])
y = df["Price"]

feature_columns = X.columns.tolist()
with open("model_features.pkl", "wb") as f:
    pickle.dump(feature_columns, f)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Random Forest model...")
# Tweaked hyperparameters: more trees, deeper trees
model = RandomForestRegressor(n_estimators=200, max_depth=20, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"MAE: MYR {mean_absolute_error(y_test, y_pred):,.0f}")
print(f"R²:  {r2_score(y_test, y_pred):.3f}")

with open("price_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to price_model.pkl ✅")