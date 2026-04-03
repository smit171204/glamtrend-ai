import streamlit as st
import pandas as pd
from collections import Counter
import plotly.express as px

df = pd.read_csv("data/womens_clothing_reviews.csv")

st.title("🎨 Fashion Trend Detection")

text = " ".join(df["Review Text"].astype(str)).lower()

colors = [
"red","blue","black","white","green",
"pink","yellow","orange","purple","brown"
]

found = []

for color in colors:
    found.extend([color]*text.count(color))

counter = Counter(found)

color_df = pd.DataFrame(counter.items(),columns=["Color","Count"])

fig = px.bar(color_df,x="Color",y="Count",title="Trending Colors in Fashion")

st.plotly_chart(fig,use_container_width=True)

st.subheader("Top Trending Clothing Category")

trend = df["Class Name"].value_counts().head(10)

st.bar_chart(trend)