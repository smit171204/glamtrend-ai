import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🤖 AI Review Insights")

# -----------------------
# LOAD DATA
# -----------------------

df = pd.read_csv("data/womens_clothing_reviews.csv")

df = df.dropna(subset=["Rating", "Class Name"])

# -----------------------
# SENTIMENT CREATION
# -----------------------

def get_sentiment(rating):
    if rating >= 4:
        return "Positive"
    elif rating == 3:
        return "Neutral"
    else:
        return "Negative"

df["Sentiment"] = df["Rating"].apply(get_sentiment)

# -----------------------
# SENTIMENT DISTRIBUTION
# -----------------------

st.subheader("📊 Customer Sentiment")

sentiment_count = df["Sentiment"].value_counts().reset_index()
sentiment_count.columns = ["Sentiment", "Count"]

fig = px.bar(sentiment_count, x="Sentiment", y="Count", color="Sentiment")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------
# TOP POSITIVE CATEGORIES
# -----------------------

st.subheader("🔥 Most Loved Categories")

positive = df[df["Sentiment"] == "Positive"]["Class Name"].value_counts().head(5)

for cat, count in positive.items():
    st.success(f"❤️ {cat} ({count} positive reviews)")

# -----------------------
# MOST NEGATIVE CATEGORIES
# -----------------------

st.subheader("⚠️ Problematic Categories")

negative = df[df["Sentiment"] == "Negative"]["Class Name"].value_counts().head(5)

for cat, count in negative.items():
    st.error(f"❌ {cat} ({count} negative reviews)")

st.divider()

# -----------------------
# CUSTOMER PAIN POINTS
# -----------------------

st.subheader("🔍 Customer Pain Points")

low_rating = df[df["Rating"] <= 2]["Class Name"].value_counts().head(3)

for cat, count in low_rating.items():
    st.warning(f"⚠️ {cat} has frequent low ratings ({count})")

st.divider()

# -----------------------
# AI BUSINESS SUGGESTIONS
# -----------------------

st.subheader("🧠  Suggestions")

top_cat = positive.idxmax()
worst_cat = negative.idxmax()

st.success(f"📈 Promote {top_cat} (high customer satisfaction)")
st.error(f"🔧 Improve {worst_cat} (frequent complaints)")
st.info("💡 Focus on customer feedback to improve product quality and retention")

































































# import streamlit as st
# import pandas as pd
# from textblob import TextBlob
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.ensemble import RandomForestClassifier

# df = pd.read_csv("data/womens_clothing_reviews.csv")
# df = df.dropna(subset=["Review Text"])

# st.title("🤖 AI Review Insights")

# # Sentiment analysis
# def get_sentiment(text):

#     score = TextBlob(text).sentiment.polarity

#     if score > 0:
#         return "Positive"
#     elif score < 0:
#         return "Negative"
#     else:
#         return "Neutral"

# df["Sentiment"] = df["Review Text"].apply(get_sentiment)

# sentiment_counts = df["Sentiment"].value_counts()

# st.subheader("Customer Sentiment")

# st.bar_chart(sentiment_counts)

# # Popularity prediction
# st.subheader("Product Popularity Prediction")

# vectorizer = CountVectorizer(stop_words="english")

# X = vectorizer.fit_transform(df["Review Text"])
# y = df["Recommended IND"]

# model = RandomForestClassifier()
# model.fit(X,y)

# review = st.text_area("Enter customer review")

# if st.button("Predict"):

#     vector = vectorizer.transform([review])
#     pred = model.predict(vector)

#     if pred[0]==1:
#         st.success("Product likely to become popular")
#     else:
#         st.error("Product popularity may be low")































