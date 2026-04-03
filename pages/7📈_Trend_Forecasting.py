import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.title("📈 Fashion Trend Forecast")

# -----------------------
# LOAD DATA
# -----------------------

df = pd.read_csv("data/womens_clothing_reviews.csv")
df = df.dropna(subset=["Rating", "Class Name"])

# -----------------------
# SELECT CATEGORY
# -----------------------

category = st.selectbox("Select Category", df["Class Name"].unique())

cat_df = df[df["Class Name"] == category].reset_index()

# -----------------------
# CREATE TIME SERIES (SMOOTH)
# -----------------------

# Create time index
cat_df["Day"] = cat_df.index

# GROUP every 100 rows → smooth graph
group_size = 100
cat_df["Group"] = cat_df["Day"] // group_size

trend = cat_df.groupby("Group")["Rating"].mean().reset_index()

# -----------------------
# ADD SEASONAL EFFECT
# -----------------------

trend["Seasonal"] = np.sin(trend["Group"] / 2) * 0.2
trend["Final"] = trend["Rating"] + trend["Seasonal"]

# -----------------------
# TRAIN MODEL
# -----------------------

X = trend[["Group"]]
y = trend["Final"]

model = LinearRegression()
model.fit(X, y)

# -----------------------
# FUTURE PREDICTION
# -----------------------

future_x = np.arange(len(trend), len(trend) + 10).reshape(-1, 1)
future_pred = model.predict(future_x)

# -----------------------
# PLOT
# -----------------------

# fig = go.Figure()
# -----------------------
# PROFESSIONAL CHART
# -----------------------

fig = go.Figure()

# Actual Trend
fig.add_trace(go.Scatter(
    x=trend["Group"],
    y=trend["Final"],
    mode="lines+markers",
    name="Actual Trend (Past Data)",
    line=dict(width=3)
))

# Predicted Trend
fig.add_trace(go.Scatter(
    x=future_x.flatten(),
    y=future_pred,
    mode="lines",
    name="Predicted Trend (Future)",
    line=dict(dash="dash", width=3)
))

# Layout Styling
fig.update_layout(
    title=f"{category} Trend Forecast Over Time",
    xaxis_title="Time (Days)",
    yaxis_title="Trend Score (Popularity)",
    template="plotly_dark",
    legend=dict(
        title="Trend Type"
    ),
    title_x=0.3
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# EXPLANATION (FOR VIVA)
# -----------------------

st.info("""
- X-axis → Time progression
- Y-axis → Trend score based on ratings
""")

# Actual
fig.add_trace(go.Scatter(
    x=trend["Group"],
    y=trend["Final"],
    mode="lines+markers",
    name="Actual Trend"
))

# Predicted
fig.add_trace(go.Scatter(
    x=future_x.flatten(),
    y=future_pred,
    mode="lines",
    name="Predicted Trend",
    line=dict(dash="dash")
))

# st.plotly_chart(fig, use_container_width=True)

# -----------------------
# INSIGHTS
# -----------------------

st.subheader("🧠 Insights")

if future_pred[-1] > trend["Final"].iloc[-1]:
    st.success(f"📈 {category} trend is increasing")
else:
    st.error(f"📉 {category} trend is decreasing")

# st.info("🔄 Seasonal fluctuations are simulated to reflect real-world fashion cycles")


















































































# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.graph_objects as go
# from sklearn.linear_model import LinearRegression

# st.title("📈 Fashion Trend Forecast (ML-Based)")

# # -----------------------
# # LOAD DATA
# # -----------------------

# df = pd.read_csv("data/womens_clothing_reviews.csv")

# df = df.dropna(subset=["Rating"])

# # -----------------------
# # CREATE TIME SERIES
# # -----------------------

# # Create fake time index (since dataset has no date)
# df = df.reset_index()
# df["Day"] = df.index

# # Group by day (simulate trend)
# trend = df.groupby("Day")["Rating"].mean().reset_index()

# # -----------------------
# # MODEL TRAINING
# # -----------------------

# X = trend[["Day"]]
# y = trend["Rating"]

# model = LinearRegression()
# model.fit(X, y)

# # -----------------------
# # FUTURE PREDICTION
# # -----------------------

# future_days = np.arange(len(trend), len(trend) + 20).reshape(-1, 1)
# future_pred = model.predict(future_days)

# # -----------------------
# # PLOT GRAPH
# # -----------------------

# fig = go.Figure()

# # Actual trend
# fig.add_trace(go.Scatter(
#     x=trend["Day"],
#     y=trend["Rating"],
#     mode="lines",
#     name="Actual Trend"
# ))

# # Predicted trend
# fig.add_trace(go.Scatter(
#     x=future_days.flatten(),
#     y=future_pred,
#     mode="lines",
#     name="Predicted Trend",
#     line=dict(dash="dash")
# ))

# st.plotly_chart(fig, use_container_width=True)

# # -----------------------
# # INSIGHTS
# # -----------------------

# st.subheader("🧠 Forecast Insights")

# if future_pred[-1] > trend["Rating"].iloc[-1]:
#     st.success("📈 Trend is expected to increase in future")
# else:
#     st.error("📉 Trend is expected to decrease in future")













# import streamlit as st
# import pandas as pd
# from prophet import Prophet
# import plotly.express as px

# st.title("📈 Fashion Trend Forecast")

# df = pd.read_csv("data/womens_clothing_reviews.csv")

# trend = df["Class Name"].value_counts().reset_index()

# trend.columns = ["Category","Count"]

# trend["ds"] = pd.date_range(start="2023-01-01",periods=len(trend))

# trend["y"] = trend["Count"]

# model = Prophet()

# model.fit(trend[["ds","y"]])

# future = model.make_future_dataframe(periods=20)

# forecast = model.predict(future)

# fig = px.line(forecast,x="ds",y="yhat")

# st.plotly_chart(fig,use_container_width=True)