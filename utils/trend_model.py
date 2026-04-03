import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib
import streamlit as st
import os

@st.cache_resource
def load_trend_model():
    # Cache the pre-trained model so it loads instantly in Streamlit
    if os.path.exists("model/logistic_model.pkl"):
        return joblib.load("model/logistic_model.pkl")
    else:
        return train_model()

def train_model():
    df = pd.read_csv("data/womens_clothing_reviews.csv")

    df = df.dropna(subset=["Rating", "Recommended IND"])

    X = df[["Rating"]]
    y = df["Recommended IND"]

    model = LogisticRegression()
    model.fit(X, y)
    
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, "model/logistic_model.pkl")

    return model

def predict_trend(rating):
    model = load_trend_model()
    pred = model.predict([[rating]])[0]

    if pred == 1:
        return "🔥 Trending"
    else:
        return "⚠️ Not Trending"
