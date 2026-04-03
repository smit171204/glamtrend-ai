import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Fashion Analytics Dashboard")

# -----------------------
# Load dataset FIRST
# -----------------------

df = pd.read_csv("data/womens_clothing_reviews.csv")

# -----------------------
# AGE FILTER
# -----------------------

age_range = st.slider(
    "Age Filter",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (20, 50)
)

filtered = df[df["Age"].between(age_range[0], age_range[1])]

# -----------------------
# KPI CARDS
# -----------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", len(filtered))
col2.metric("Average Rating", round(filtered["Rating"].mean(), 2))
col3.metric("Recommendation %", round(filtered["Recommended IND"].mean()*100, 2))

st.divider()

# -----------------------
# CHART 1
# -----------------------

st.subheader("🔥 Trending Categories")

category = filtered["Class Name"].value_counts().reset_index()
category.columns = ["Category", "Count"]

fig = px.bar(
    category,
    x="Category",
    y="Count",
    color="Count"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# CHART 2
# -----------------------

st.subheader("📊 Age vs Rating")

fig2 = px.scatter(
    filtered,
    x="Age",
    y="Rating",
    color="Class Name"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# CHART 3
# -----------------------

st.subheader("👍 Recommendation")

rec = filtered["Recommended IND"].value_counts().reset_index()
rec.columns = ["Recommended", "Count"]

rec["Recommended"] = rec["Recommended"].map({
    1: "Recommended",
    0: "Not Recommended"
})

fig3 = px.pie(rec, names="Recommended", values="Count")

st.plotly_chart(fig3, use_container_width=True)

# -----------------------
# AI INSIGHTS
# -----------------------

st.subheader("🧠 AI Insights")

top_category = filtered["Class Name"].value_counts().idxmax()
avg_rating = round(filtered["Rating"].mean(), 2)
recommend_rate = round(filtered["Recommended IND"].mean()*100, 2)
age_best = filtered.groupby("Age")["Rating"].mean().idxmax()

st.success(f"🔥 Top category: {top_category}")
st.info(f"⭐ Avg rating: {avg_rating}")
st.warning(f"👍 {recommend_rate}% recommend")
st.write(f"👩 Age {age_best} gives highest ratings")