import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Advanced Business Insights Dashboard")

# -----------------------
# LOAD DATA
# -----------------------

df = pd.read_csv("data/womens_clothing_reviews.csv")

df = df.dropna(subset=["Rating", "Class Name", "Age"])

# -----------------------
# KPI
# -----------------------

top_category = df["Class Name"].value_counts().idxmax()
avg_rating = round(df["Rating"].mean(), 2)
recommend_rate = round(df["Recommended IND"].mean()*100, 2)

col1, col2, col3 = st.columns(3)

col1.metric("Top Category", top_category)
col2.metric("Avg Rating", avg_rating)
col3.metric("Recommendation %", f"{recommend_rate}%")

st.divider()

# -----------------------
# DEMAND ANALYSIS
# -----------------------

st.subheader("📈 Demand by Category")

demand = df["Class Name"].value_counts().reset_index()
demand.columns = ["Category", "Demand"]

fig1 = px.bar(demand.head(10), x="Category", y="Demand", color="Demand")
st.plotly_chart(fig1, use_container_width=True)

# -----------------------
# CUSTOMER SEGMENTATION
# -----------------------

st.subheader("👥 Customer Segments (Age vs Rating)")

fig2 = px.scatter(df, x="Age", y="Rating", color="Class Name")
st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# PROBLEM AREAS
# -----------------------

st.subheader("⚠️ Low Performing Categories")

low = df[df["Rating"] <= 2]["Class Name"].value_counts().head(5)

for cat, count in low.items():
    st.error(f"❌ {cat} has {count} low ratings")

# -----------------------
# BUSINESS RECOMMENDATIONS
# -----------------------

st.subheader("🧠 AI Business Suggestions")

top_cat = df["Class Name"].value_counts().idxmax()
best_age = df.groupby("Age")["Rating"].mean().idxmax()

st.success(f"🔥 Focus more on {top_cat} (high demand)")
st.info(f"🎯 Target customers around age {best_age}")
st.warning("⚠️ Improve low-rated categories for better retention")

































































































# import streamlit as st
# import pandas as pd
# from utils.report_generator import generate_report

# st.title("📊 Business Insights")

# df = pd.read_csv("data/womens_clothing_reviews.csv")

# top_category = df["Class Name"].value_counts().idxmax()
# avg_rating = round(df["Rating"].mean(), 2)
# recommend_rate = round(df["Recommended IND"].mean()*100, 2)

# st.success(f"Top Category: {top_category}")
# st.info(f"Average Rating: {avg_rating}")
# st.warning(f"Recommendation Rate: {recommend_rate}%")

# # PDF Download
# if st.button("📄 Download Report"):

#     insights = [
#         f"Top Category: {top_category}",
#         f"Average Rating: {avg_rating}",
#         f"Recommendation Rate: {recommend_rate}%"
#     ]

#     generate_report("fashion_report.pdf", insights)

#     with open("fashion_report.pdf", "rb") as f:
#         st.download_button(
#             "Download PDF",
#             f,
#             file_name="GlamTrends_Report.pdf"
#         )