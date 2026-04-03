# ==========================
# IMPORTS
# ==========================
import streamlit as st
import pandas as pd

from utils.auth_ui import auth_page
from utils.ai_assistant import fashion_ai_response

from utils.data_preprocessing import (
    MissingValueHandler,
    DataCleaningPipeline,
    DataStandardizer,
    OutlierHandler,
    FeatureScaler
)

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="GlamTrends AI", layout="wide")

# ==========================
# LOGIN SYSTEM
# ==========================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

if not st.session_state["logged_in"]:
    auth_page()
    st.stop()

# ==========================
# USER BAR
# ==========================
col1, col2 = st.columns([8, 2])

with col1:
    st.markdown(f"### 👗 Welcome, {st.session_state['user']}")

with col2:
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.rerun()

# ==========================
# LOAD DATA
# ==========================
@st.cache_data
def load_data():
    return pd.read_csv("data/womens_clothing_reviews.csv")

df = load_data()

# ==========================
# UI TITLE
# ==========================
st.title("👗 GlamTrend AI Dashboard")

# ==========================
# TASK 1: MISSING VALUES
# ==========================
st.subheader("🔹 Missing Value Handling")

handler = MissingValueHandler(df)
st.dataframe(handler.get_missing_summary())

if st.button("Run Imputation"):
    df, report = handler.smart_impute()
    st.success("Done")
    st.json(report)

# ==========================
# TASK 2: CLEANING
# ==========================
st.subheader("🔹 Data Cleaning")

if st.button("Run Cleaning"):
    cleaner = DataCleaningPipeline(df)
    df, log = cleaner.run_pipeline()

    st.success("Cleaning Done")
    st.json(log)

# ==========================
# TASK 3: STANDARDIZATION
# ==========================
st.subheader("🔹 Data Standardization")

if st.button("Run Standardization"):
    std = DataStandardizer(df)
    df, log = std.run()

    st.success("Standardized")
    st.json(log)

# ==========================
# TASK 4: OUTLIERS
# ==========================
st.subheader("🔹 Outlier Handling")

method = st.selectbox("Method", ["cap", "remove", "transform"])

if st.button("Handle Outliers"):
    out = OutlierHandler(df)
    df, log = out.handle(method)

    st.success("Outliers Processed")
    st.json(log)

# ==========================
# TASK 5: SCALING
# ==========================
st.subheader("🔹 Feature Scaling")

if st.button("Run Scaling"):
    scaler = FeatureScaler(df)
    df, best, scores = scaler.scale()

    st.success(f"Best Scaler: {best}")
    st.json(scores)

# ==========================
# AI CHATBOT
# ==========================
st.markdown("---")
st.subheader("🤖 AI Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("Ask fashion trends...")

if user_input:
    response = fashion_ai_response(user_input)
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", response))

for role, msg in st.session_state.chat_history:
    st.chat_message(role).write(msg)

    