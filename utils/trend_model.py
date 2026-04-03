import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import streamlit as st
import os

MODEL_PATH = "model/logistic_model.pkl"
DATA_PATH = "data/womens_clothing_reviews.csv"


# -----------------------
# LOAD MODEL (CACHED)
# -----------------------
@st.cache_resource
def load_trend_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return train_model()


# -----------------------
# TRAIN MODEL
# -----------------------
def train_model():
    df = pd.read_csv(DATA_PATH)

    # Clean column names (VERY IMPORTANT)
    df.columns = df.columns.str.strip()

    # Drop nulls safely
    df = df.dropna(subset=["Rating", "Recommended IND"])

    # Features & target
    X = df[["Rating"]]   # ✅ single feature
    y = df["Recommended IND"]

    # Train model
    model = LogisticRegression()
    model.fit(X, y)

    # Save model
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    return model


# -----------------------
# PREDICTION FUNCTION
# -----------------------
def predict_trend(rating):
    model = load_trend_model()

    # Ensure correct input shape
    pred = model.predict([[float(rating)]])[0]

    return "🔥 Trending" if pred == 1 else "❄️ Not Trending"