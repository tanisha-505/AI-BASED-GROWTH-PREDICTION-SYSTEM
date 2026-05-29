# # ml_model.py
# # Linear Regression engine using scikit-learn.
# # This file is database-independent — it just receives
# # a list of records (dicts) and trains/predicts on them.

# import numpy as np
# import pandas as pd
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import r2_score, mean_absolute_error

# # Global model state (lives in memory while server is running)
# model            = LinearRegression()
# scaler           = StandardScaler()
# region_encoder   = LabelEncoder()
# category_encoder = LabelEncoder()
# is_trained       = False


# def train_model(records: list[dict]) -> dict:
#     """
#     Train the Linear Regression model on historical sales records.

#     Args:
#         records: list of dicts with keys:
#                  month, year, sales, marketing_spend,
#                  num_employees, region, product_category

#     Returns:
#         dict with r2_score, mean_absolute_error, records_used
#     """
#     global model, scaler, region_encoder, category_encoder, is_trained

#     if len(records) < 10:
#         raise ValueError("Need at least 10 records to train the model.")

#     df = pd.DataFrame(records)

#     # Encode categorical text columns into numbers
#     df["region_enc"]   = region_encoder.fit_transform(df["region"])
#     df["category_enc"] = category_encoder.fit_transform(df["product_category"])

#     X = df[["month", "year", "marketing_spend",
#             "num_employees", "region_enc", "category_enc"]].values
#     y = df["sales"].values

#     # Scale features so all are on the same range
#     X_scaled = scaler.fit_transform(X)

#     # 80% train, 20% test split
#     X_train, X_test, y_train, y_test = train_test_split(
#         X_scaled, y, test_size=0.2, random_state=42
#     )

#     model.fit(X_train, y_train)
#     y_pred = model.predict(X_test)
#     is_trained = True

#     return {
#         "r2_score": round(r2_score(y_test, y_pred), 4),
#         "mean_absolute_error": round(mean_absolute_error(y_test, y_pred), 2),
#         "records_used": len(records),
#         "status": "Model trained successfully ✅"
#     }


# def predict_sales(features: dict) -> float:
#     """
#     Predict sales for a given set of input features.

#     Args:
#         features: dict with keys matching PredictRequest fields

#     Returns:
#         Predicted sales as a float
#     """
#     global is_trained

#     if not is_trained:
#         raise RuntimeError(
#             "Model is not trained yet. Please upload data first via POST /upload."
#         )

#     try:
#         region_enc   = region_encoder.transform([features["region"]])[0]
#         category_enc = category_encoder.transform([features["product_category"]])[0]
#     except ValueError as e:
#         raise ValueError(
#             f"Unknown value for region or product_category: {e}. "
#             "Use values that exist in your training data."
#         )

#     X = np.array([[
#         features["month"],
#         features["year"],
#         features["marketing_spend"],
#         features["num_employees"],
#         region_enc,
#         category_enc
#     ]])

#     X_scaled   = scaler.transform(X)
#     prediction = model.predict(X_scaled)[0]
#     return round(float(prediction), 2)
# ml_model.py — UPGRADED
# Now supports BOTH Linear Regression AND Random Forest
# Default model: Random Forest (much better accuracy!)

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error

# ── Global model state ────────────────────────────────────────────────────
model            = RandomForestRegressor(n_estimators=100, random_state=42)
scaler           = StandardScaler()
region_encoder   = LabelEncoder()
category_encoder = LabelEncoder()
is_trained       = False
MODEL_NAME       = "Random Forest Regressor"
# ─────────────────────────────────────────────────────────────────────────


def train_model(records: list[dict]) -> dict:
    """
    Train Random Forest model on historical sales records.
    Features: month, year, marketing_spend, num_employees,
              region (encoded), product_category (encoded)
    Target  : sales
    """
    global model, scaler, region_encoder, category_encoder, is_trained

    if len(records) < 10:
        raise ValueError("Need at least 10 records to train the model.")

    df = pd.DataFrame(records)

    # Encode categorical columns
    df["region_enc"]   = region_encoder.fit_transform(df["region"])
    df["category_enc"] = category_encoder.fit_transform(df["product_category"])

    # Feature matrix
    X = df[["month", "year", "marketing_spend",
            "num_employees", "region_enc", "category_enc"]].values
    y = df["sales"].values

    # Scale features
    X_scaled = scaler.fit_transform(X)

    # 80/20 train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model.fit(X_train, y_train)
    y_pred   = model.predict(X_test)
    is_trained = True

    # Feature importance (only for Random Forest)
    feature_names  = ["month", "year", "marketing_spend",
                       "num_employees", "region", "category"]
    importance_dict = {}
    if hasattr(model, "feature_importances_"):
        importance_dict = {
            name: round(float(imp), 4)
            for name, imp in zip(feature_names, model.feature_importances_)
        }

    return {
        "model":                 MODEL_NAME,
        "r2_score":              round(r2_score(y_test, y_pred), 4),
        "mean_absolute_error":   round(mean_absolute_error(y_test, y_pred), 2),
        "records_used":          len(records),
        "feature_importance":    importance_dict,
        "status":                f"✅ {MODEL_NAME} trained successfully!"
    }


def predict_sales(features: dict) -> float:
    """
    Predict sales for given input features.
    Raises RuntimeError if model not yet trained.
    Raises ValueError if unknown region/category is provided.
    """
    global is_trained

    if not is_trained:
        raise RuntimeError(
            "Model is not trained yet. "
            "Please upload data first via POST /upload."
        )

    # Validate inputs
    if not features.get("region"):
        raise ValueError("Region cannot be empty.")
    if not features.get("product_category"):
        raise ValueError("Product category cannot be empty.")
    if not (1 <= int(features.get("month", 0)) <= 12):
        raise ValueError("Month must be between 1 and 12.")
    if int(features.get("year", 0)) < 2000:
        raise ValueError("Year must be 2000 or later.")
    if float(features.get("marketing_spend", -1)) < 0:
        raise ValueError("Marketing spend cannot be negative.")
    if int(features.get("num_employees", 0)) <= 0:
        raise ValueError("Number of employees must be greater than 0.")

    try:
        region_enc   = region_encoder.transform([features["region"]])[0]
        category_enc = category_encoder.transform([features["product_category"]])[0]
    except ValueError:
        raise ValueError(
            f"Unknown region '{features['region']}' or "
            f"category '{features['product_category']}'. "
            "Use values from your training data."
        )

    X = np.array([[
        features["month"],
        features["year"],
        features["marketing_spend"],
        features["num_employees"],
        region_enc,
        category_enc
    ]])

    X_scaled   = scaler.transform(X)
    prediction = model.predict(X_scaled)[0]

    # Never return negative sales
    return round(max(float(prediction), 0.0), 2)