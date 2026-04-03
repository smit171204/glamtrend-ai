import streamlit as st
import pandas as pd
import plotly.express as px

from utils.trend_model import train_model

st.title("🔥 Fashion Trends")

# -----------------------
# LOAD DATA
# -----------------------

df = pd.read_csv("data/womens_clothing_reviews.csv")

# Clean column names (VERY IMPORTANT)
df.columns = df.columns.str.strip()

# Drop nulls safely
df = df.dropna(subset=["Rating", "Class Name", "Recommended IND"])

# -----------------------
# LOAD MODEL (CACHED)
# -----------------------

@st.cache_resource
def load_model():
    return train_model()

model = load_model()

# -----------------------
# KPI
# -----------------------

col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", len(df))
col2.metric("Avg Rating", round(df["Rating"].mean(), 2))
col3.metric("Recommendation %", round(df["Recommended IND"].mean() * 100, 2))

st.divider()

# -----------------------
# ML TREND PREDICTION
# -----------------------

st.subheader("🤖 ML Trend Prediction")

sample = df.sample(10)

for _, row in sample.iterrows():
    pred = model.predict([[row["Rating"]]])[0]
    trend = "🔥 Trending" if pred == 1 else "❄️ Not Trending"

    st.write(f"{row['Class Name']} (Rating: {row['Rating']}) → {trend}")

st.divider()

# -----------------------
# TOP TRENDING
# -----------------------

st.subheader("🏆 Top Trending Categories")

top = df[df["Recommended IND"] == 1]["Class Name"].value_counts().head(5)

for cat_name, count in top.items():
    st.success(f"🔥 {cat_name} ({count} votes)")

# -----------------------
# CHART
# -----------------------

st.subheader("📊 Category Distribution")

cat = df["Class Name"].value_counts().reset_index()
cat.columns = ["Category", "Count"]

fig = px.bar(cat.head(10), x="Category", y="Count", color="Count")

st.plotly_chart(fig, use_container_width=True)





































































# import streamlit as st
# import pandas as pd
# import plotly.express as px

# st.title("🔥 AI-Based Fashion Trends (Dataset Driven)")

# # -----------------------
# # LOAD DATA
# # -----------------------

# df = pd.read_csv("data/womens_clothing_reviews.csv")

# # Clean
# df = df.dropna(subset=["Rating", "Class Name"])

# # -----------------------
# # KPI CARDS
# # -----------------------

# col1, col2, col3 = st.columns(3)

# col1.metric("Total Reviews", len(df))
# col2.metric("Avg Rating", round(df["Rating"].mean(), 2))
# col3.metric("Recommendation %", round(df["Recommended IND"].mean()*100, 2))

# st.divider()

# # -----------------------
# # TOP TRENDING CATEGORIES
# # -----------------------

# st.subheader("🏆 Top Trending Categories")

# category = df["Class Name"].value_counts().reset_index()
# category.columns = ["Category", "Count"]

# fig = px.bar(category.head(10), x="Category", y="Count", color="Count")
# st.plotly_chart(fig, use_container_width=True)

# # -----------------------
# # BEST PRODUCTS (HIGH RATING)
# # -----------------------

# st.subheader("⭐ Top Rated Products")

# top_products = df.sort_values(by="Rating", ascending=False).head(10)

# for _, row in top_products.iterrows():
#     st.success(f"🔥 {row['Class Name']} (Rating: {row['Rating']})")

# # -----------------------
# # MOST RECOMMENDED
# # -----------------------

# st.subheader("👍 Most Recommended Categories")

# rec = df[df["Recommended IND"] == 1]["Class Name"].value_counts().head(5)

# for cat, count in rec.items():
#     st.write(f"👗 {cat} - {count} recommendations")

# # -----------------------
# # AGE BASED TREND
# # -----------------------

# st.subheader("📊 Age vs Rating")

# fig2 = px.scatter(df, x="Age", y="Rating", color="Class Name")
# st.plotly_chart(fig2, use_container_width=True)

# # -----------------------
# # TREND INSIGHTS
# # -----------------------

# st.subheader("🧠 AI Insights")

# top_category = df["Class Name"].value_counts().idxmax()
# best_age = df.groupby("Age")["Rating"].mean().idxmax()

# st.success(f"🔥 Most popular category: {top_category}")
# st.info(f"👩 Age group with highest rating: {best_age}")

















































# import streamlit as st
# import requests
# import pandas as pd
# import plotly.express as px

# st.title("🔥 Live Fashion Trends (Advanced Analytics)")

# # -----------------------
# # API FUNCTIONS
# # -----------------------

# def fetch_fakestore():
#     url = "https://fakestoreapi.com/products"
#     res = requests.get(url, timeout=5)
#     if res.status_code == 200:
#         return res.json(), "FakeStore"
#     else:
#         raise Exception()


# def fetch_dummyjson():
#     url = "https://dummyjson.com/products"
#     res = requests.get(url, timeout=5)
#     if res.status_code == 200:
#         return res.json()["products"], "DummyJSON"
#     else:
#         raise Exception()


# # -----------------------
# # FETCH DATA (AUTO SWITCH)
# # -----------------------

# data = None
# source = ""

# with st.spinner("Fetching live fashion data..."):
#     try:
#         data, source = fetch_fakestore()
#     except:
#         st.warning("Switching to backup API...")
#         try:
#             data, source = fetch_dummyjson()
#         except:
#             st.error("All APIs failed ❌")
#             data = None

# # -----------------------
# # IF DATA EXISTS
# # -----------------------

# if data:

#     st.success(f"✅ Data Source: {source}")

#     # Convert to DataFrame
#     df = pd.DataFrame(data)

#     # Clean columns
#     df["title"] = df["title"].astype(str)
#     df["price"] = pd.to_numeric(df["price"], errors="coerce")

#     if "category" not in df.columns:
#         df["category"] = "fashion"

#     # -----------------------
#     # KPI CARDS
#     # -----------------------

#     col1, col2, col3 = st.columns(3)

#     col1.metric("Total Products", len(df))
#     col2.metric("Avg Price", round(df["price"].mean(), 2))
#     col3.metric("Unique Categories", df["category"].nunique())

#     st.divider()

#     # -----------------------
#     # PRICE DISTRIBUTION
#     # -----------------------

#     st.subheader("💰 Price Distribution")

#     fig1 = px.histogram(df, x="price", nbins=20)
#     st.plotly_chart(fig1, use_container_width=True)

#     # -----------------------
#     # CATEGORY ANALYSIS
#     # -----------------------

#     st.subheader("📦 Category Analysis")

#     cat = df["category"].value_counts().reset_index()
#     cat.columns = ["Category", "Count"]

#     fig2 = px.bar(cat, x="Category", y="Count", color="Count")
#     st.plotly_chart(fig2, use_container_width=True)

#     # -----------------------
#     # TOP TRENDING (LOGIC)
#     # -----------------------

#     st.subheader("🏆 Top Trending Items")

#     # Simple logic: lower price = more trending (demo logic)
#     top_items = df.sort_values(by="price").head(5)

#     for _, row in top_items.iterrows():
#         st.success(f"🔥 {row['title']} - ${row['price']}")

#     st.divider()

#     # -----------------------
#     # PRODUCT LIST
#     # -----------------------

#     st.subheader("🛍️ Live Products")

#     for _, row in df.head(10).iterrows():
#         st.write(f"👗 {row['title']} - ${row['price']}")

# # -----------------------
# # FALLBACK
# # -----------------------

# else:

#     st.warning("Showing sample trends")

#     fallback = [
#         "Summer Dress",
#         "Casual Tops",
#         "Denim Jeans",
#         "Jackets",
#         "Ethnic Wear"
#     ]

#     for item in fallback:
#         st.write(f"👗 {item}")















# import streamlit as st
# import requests

# st.title("🔥 Live Fashion Trends (Smart API System)")

# # -----------------------
# # API FUNCTIONS
# # -----------------------

# def fetch_fakestore():
#     url = "https://fakestoreapi.com/products"
#     response = requests.get(url, timeout=5)

#     if response.status_code == 200:
#         return response.json(), "FakeStore API"
#     else:
#         raise Exception("FakeStore failed")


# def fetch_dummyjson():
#     url = "https://dummyjson.com/products"
#     response = requests.get(url, timeout=5)

#     if response.status_code == 200:
#         data = response.json()["products"]
#         return data, "DummyJSON API"
#     else:
#         raise Exception("DummyJSON failed")


# # -----------------------
# # MAIN LOGIC (AUTO SWITCH)
# # -----------------------

# data = None
# source = ""

# with st.spinner("Fetching live fashion data..."):

#     # TRY API 1
#     try:
#         data, source = fetch_fakestore()

#     except:
#         st.warning("⚠️ Primary API failed. Switching to backup...")

#         # TRY API 2
#         try:
#             data, source = fetch_dummyjson()

#         except:
#             st.error("❌ All APIs failed. Showing fallback data.")
#             data = None


# # -----------------------
# # DISPLAY DATA
# # -----------------------

# if data:

#     st.success(f"✅ Data Source: {source}")

#     st.subheader("🛍️ Live Fashion Products")

#     for item in data[:10]:

#         # Handle both APIs format
#         title = item.get("title", "No Title")
#         price = item.get("price", "N/A")

#         st.markdown(f"""
#         **👗 {title}**  
#         💰 Price: ${price}
#         """)

# # -----------------------
# # FALLBACK DATA
# # -----------------------

# else:

#     fallback = [
#         "Summer Dress",
#         "Casual Tops",
#         "Denim Jeans",
#         "Jackets",
#         "Ethnic Wear"
#     ]

#     st.subheader("🧾 Sample Fashion Trends")

#     for item in fallback:
#         st.write(f"👗 {item}")


































# # import streamlit as st
# # import requests
# # from bs4 import BeautifulSoup

# # # CLEAN IMPORT (FINAL)
# # from utils.live_data import get_live_trends

# # st.title("🔥 Live Fashion Trends")

# # # ---------------------------
# # # AI / Simulated Trends
# # # ---------------------------

# # st.subheader("📊 AI Trending Items")

# # trends = get_live_trends()

# # for t in trends:
# #     st.success(f"Trending Now: {t}")

# # # ---------------------------
# # # Real Web Trends
# # # ---------------------------

# # st.subheader("🌐 Live Market Trends")

# # url = "https://www.amazon.in/s?k=womens+fashion"

# # headers = {
# #     "User-Agent": "Mozilla/5.0"
# # }

# # try:
# #     response = requests.get(url, headers=headers, timeout=5)

# #     if response.status_code == 200:
# #         soup = BeautifulSoup(response.text, "html.parser")
# #         products = soup.select(".a-size-base-plus")

# #         if products:
# #             for p in products[:10]:
# #                 st.write("👗", p.text.strip())
# #         else:
# #             st.warning("No products found, showing fallback")
# #             for t in trends:
# #                 st.write("👗", t)
# #     else:
# #         st.error("Failed to fetch data")

# # except Exception:
# #     st.error("Internet issue, showing fallback")
# #     for t in trends:
# #         st.write("👗", t)










# # import streamlit as st
# # import requests

# # # OPTIONAL (your existing AI trends)
# # from utils.live_data import get_live_trends

# # # ---------------------------
# # # PAGE TITLE
# # # ---------------------------

# # st.title("🔥 Live Fashion Trends Dashboard")

# # # ---------------------------
# # # 1️⃣ AI / SIMULATED TRENDS
# # # ---------------------------

# # st.subheader("📊 AI Predicted Trends")

# # try:
# #     trends = get_live_trends()

# #     for t in trends:
# #         st.success(f"Trending Now: {t}")

# # except:
# #     st.warning("AI trends not available")

# # # ---------------------------
# # # 2️⃣ LIVE PRODUCTS (FakeStore API)
# # # ---------------------------

# # st.subheader("🛍️ Live Fashion Products (API)")

# # try:
# #     url = "https://fakestoreapi.com/products"
# #     response = requests.get(url, timeout=5)
# #     data = response.json()

# #     for item in data[:8]:
# #         st.markdown(f"""
# #         **👗 {item['title']}**  
# #         💰 Price: ${item['price']}  
# #         📦 Category: {item['category']}
# #         """)

# # except:
# #     st.error("Failed to load FakeStore API")

# # # ---------------------------
# # # 3️⃣ LIVE PRODUCTS (DummyJSON API)
# # # ---------------------------

# # st.subheader("🌐 More Live Products")

# # try:
# #     url2 = "https://dummyjson.com/products"
# #     response2 = requests.get(url2, timeout=5)
# #     data2 = response2.json()["products"]

# #     for item in data2[:8]:
# #         st.write(f"👗 {item['title']} - ${item['price']}")

# # except:
# #     st.error("Failed to load DummyJSON API")

# # # ---------------------------
# # # 4️⃣ GOOGLE TRENDS (REAL DATA)
# # # ---------------------------

# # st.subheader("📈 Fashion Search Trends")

# # try:
# #     from pytrends.request import TrendReq

# #     pytrends = TrendReq()

# #     keywords = ["dress", "jeans", "tops", "jacket"]

# #     pytrends.build_payload(keywords)

# #     trend_data = pytrends.interest_over_time()

# #     if not trend_data.empty:
# #         st.line_chart(trend_data[keywords])
# #     else:
# #         st.warning("No trend data available")

# # except:
# #     st.warning("Google Trends not available (install pytrends)")






# import streamlit as st
# import requests

# from utils.trend_model import train_model, predict_trend

# # -----------------------
# # PAGE CONFIG
# # -----------------------

# st.title("🔥 Live Fashion Trends (AI Powered)")

# # -----------------------
# # LOAD MODEL
# # -----------------------

# @st.cache_resource
# def load_model():
#     return train_model()

# model = load_model()

# # -----------------------
# # LOADING ANIMATION
# # -----------------------

# with st.spinner("Analyzing live fashion data..."):
#     url = "https://fakestoreapi.com/products"
#     response = requests.get(url, timeout=5)
#     data = response.json()

# # -----------------------
# # DISPLAY PRODUCTS
# # -----------------------

# st.subheader("🛍️ Live Products + AI Prediction")

# results = []

# for item in data[:10]:

#     # API has no rating → simulate realistic rating
#     rating = 3.5 + (hash(item["title"]) % 15) / 10   # 3.5 to 5 range

#     trend = predict_trend(model, rating)

#     results.append({
#         "title": item["title"],
#         "price": item["price"],
#         "trend": trend
#     })

#     st.markdown(f"""
#     **👗 {item['title']}**  
#     💰 Price: ${item['price']}  
#     ⭐ Rating: {round(rating,1)}  
#     {trend}
#     """)

# # -----------------------
# # TOP TRENDING SECTION
# # -----------------------

# st.divider()
# st.subheader("🏆 Top Trending Items")

# top_items = [r for r in results if "Trending" in r["trend"]]

# if top_items:
#     for item in top_items[:5]:
#         st.success(f"🔥 {item['title']} - ${item['price']}")
# else:
#     st.warning("No trending items found")

# # -----------------------
# # PROGRESS BAR (UI UPGRADE)
# # -----------------------

# st.divider()
# st.subheader("📊 Trend Analysis Progress")

# progress = st.progress(0)

# import time
# for i in range(100):
#     time.sleep(0.01)
#     progress.progress(i + 1)

# st.success("Analysis Complete ✅")



# import streamlit as st
# import requests

# st.title("🔥 Live Fashion Trends")

# url = "https://fakestoreapi.com/products"

# try:
#     response = requests.get(url, timeout=5)

#     # ✅ CHECK STATUS
#     if response.status_code == 200:

#         # ✅ SAFE JSON PARSE
#         try:
#             data = response.json()
#         except:
#             st.error("API returned invalid data ❌")
#             st.stop()

#         st.subheader("🛍️ Live Products")

#         for item in data[:10]:
#             st.write(f"👗 {item['title']} - ${item['price']}")

#     else:
#         st.error("API not responding ❌")

# # ✅ INTERNET / API ERROR
# except Exception as e:
#     st.error("⚠️ Unable to fetch live data")
#     st.warning("Showing fallback data instead")

#     # 🔥 FALLBACK DATA (IMPORTANT FOR VIVA)
#     fallback = [
#         "Summer Dress",
#         "Casual Tops",
#         "Denim Jeans",
#         "Jackets",
#         "Ethnic Wear"
#     ]

#     for item in fallback:
#         st.write(f"👗 {item}")