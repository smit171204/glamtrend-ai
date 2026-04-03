import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🛍️ Age-wise Fashion Recommendation System")

# -----------------------
# LOAD DATA
# -----------------------

df = pd.read_csv("data/womens_clothing_reviews.csv")

df = df.dropna(subset=["Age", "Rating", "Class Name"])

# -----------------------
# CREATE AGE GROUPS
# -----------------------

bins = list(range(10, 80, 10))  # 10-20, 20-30, etc
labels = [f"{i}-{i+10}" for i in bins[:-1]]

df["Age Group"] = pd.cut(df["Age"], bins=bins, labels=labels)

# -----------------------
# SELECT AGE GROUP
# -----------------------

selected_group = st.selectbox("Select Age Group", labels)

group_data = df[df["Age Group"] == selected_group]

# -----------------------
# KPI
# -----------------------

col1, col2 = st.columns(2)

col1.metric("Total Reviews", len(group_data))
col2.metric("Avg Rating", round(group_data["Rating"].mean(), 2))

st.divider()

# -----------------------
# TOP TRENDING ITEMS
# -----------------------

st.subheader(f"🔥 Top Trending Items (Age {selected_group})")

top_items = (
    group_data[group_data["Recommended IND"] == 1]
    .groupby("Class Name")
    .agg({
        "Rating": "mean",
        "Recommended IND": "count"
    })
    .sort_values(by="Recommended IND", ascending=False)
    .head(5)
)

for item, row in top_items.iterrows():
    st.success(f"👗 {item} | ⭐ {round(row['Rating'],2)} | 👍 {row['Recommended IND']} votes")

# -----------------------
# CHART
# -----------------------

st.subheader("📊 Category Popularity")

chart_data = group_data["Class Name"].value_counts().reset_index()
chart_data.columns = ["Category", "Count"]

fig = px.bar(chart_data.head(10), x="Category", y="Count", color="Count")

st.plotly_chart(fig, use_container_width=True)






























































# import streamlit as st
# import pandas as pd
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import CountVectorizer

# st.title("👗 AI Fashion Recommendation System")

# df = pd.read_csv("data/womens_clothing_reviews.csv")

# df = df.dropna(subset=["Review Text"])

# vectorizer = CountVectorizer(stop_words="english")

# X = vectorizer.fit_transform(df["Review Text"])

# similarity = cosine_similarity(X)

# product_index = st.slider("Select Review Index",0,len(df)-1,10)

# similar_products = list(enumerate(similarity[product_index]))

# sorted_products = sorted(similar_products,key=lambda x:x[1],reverse=True)[1:6]

# st.subheader("Recommended Fashion Items")

# for i in sorted_products:
#     st.write(df.iloc[i[0]]["Class Name"]," | Rating:",df.iloc[i[0]]["Rating"])