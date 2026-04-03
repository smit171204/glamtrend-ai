import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

sns.set_style("darkgrid")

# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="GlamTrend Dashboard",
    layout="wide"
)

# -----------------------------
# Load Dataset
# -----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("../data/cleaned_fashion_data.csv")
    return df

df = load_data()

# -----------------------------
# Title Banner
# -----------------------------

st.markdown(
"""
<h1 style='text-align: center; color: #4CAF50;'>
GlamTrend – Women Fashion Intelligence Dashboard
</h1>
""",
unsafe_allow_html=True
)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.success("Dataset Loaded Successfully")

st.sidebar.title("GlamTrend Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Home",
        "Dataset Explorer",
        "Trend Analysis",
        "Sentiment Analysis",
        "Business Insights"
    ]
)

st.sidebar.markdown("---")
st.sidebar.write("Project: GlamTrend")
st.sidebar.write("Domain: Fashion Analytics")
st.sidebar.write("Technology: Python, Streamlit, Data Science")

# -----------------------------
# HOME PAGE
# -----------------------------

if page == "Home":

    st.header("Dashboard Overview")

    positive_reviews = len(df[df["sentiment"]=="Positive"])
    total_reviews = len(df)
    satisfaction = (positive_reviews/total_reviews)*100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Reviews", len(df))
    col2.metric("Average Rating", round(df["Rating"].mean(),2))
    col3.metric("Departments", df["Department Name"].nunique())
    col4.metric("Customer Satisfaction", f"{satisfaction:.1f}%")

    st.markdown("---")

    with st.expander("View Dataset Preview"):
        st.dataframe(df.head(20))

# -----------------------------
# DATASET EXPLORER
# -----------------------------

elif page == "Dataset Explorer":

    st.header("Dataset Explorer")

    age_group = st.selectbox(
        "Select Age Group",
        ["All"] + list(df["Age Group"].dropna().unique())
    )

    department = st.selectbox(
        "Department",
        ["All"] + list(df["Department Name"].dropna().unique())
    )

    rating = st.slider("Minimum Rating",1,5,3)

    filtered_df = df.copy()

    if age_group != "All":
        filtered_df = filtered_df[filtered_df["Age Group"] == age_group]

    if department != "All":
        filtered_df = filtered_df[filtered_df["Department Name"] == department]

    filtered_df = filtered_df[filtered_df["Rating"] >= rating]

    st.dataframe(filtered_df)

    st.write("Total Records:", len(filtered_df))

# -----------------------------
# TREND ANALYSIS
# -----------------------------

elif page == "Trend Analysis":

    st.header("Fashion Trend Analysis")

    st.subheader("Clothing Category Popularity")

    fig1, ax1 = plt.subplots()

    sns.countplot(
        data=df,
        x="Department Name",
        order=df["Department Name"].value_counts().index,
        ax=ax1
    )

    plt.xticks(rotation=45)

    st.pyplot(fig1)

    st.subheader("Average Rating by Department")

    rating_data = df.groupby("Department Name")["Rating"].mean()

    fig2, ax2 = plt.subplots()

    rating_data.plot(kind="bar", ax=ax2)

    st.pyplot(fig2)

    st.subheader("Age Group Fashion Preference")

    fig3, ax3 = plt.subplots()

    sns.countplot(
        data=df,
        x="Age Group",
        hue="Department Name",
        ax=ax3
    )

    plt.xticks(rotation=45)

    st.pyplot(fig3)

    st.subheader("Top Trending Clothing Categories")

    top_trends = df["Department Name"].value_counts().head(5)

    st.bar_chart(top_trends)

# -----------------------------
# SENTIMENT ANALYSIS
# -----------------------------

elif page == "Sentiment Analysis":

    st.header("Customer Sentiment Analysis")

    sentiment_counts = df["sentiment"].value_counts()

    st.subheader("Sentiment Distribution")

    fig4, ax4 = plt.subplots()

    sentiment_counts.plot(
        kind="pie",
        autopct="%1.1f%%",
        ax=ax4
    )

    st.pyplot(fig4)

    st.bar_chart(sentiment_counts)

    st.subheader("Word Cloud from Reviews")

    text = " ".join(df["Review Text"].dropna())

    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(text)

    fig5, ax5 = plt.subplots()

    ax5.imshow(wordcloud)
    ax5.axis("off")

    st.pyplot(fig5)

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------

elif page == "Business Insights":

    st.header("Fashion Business Insights")

    st.subheader("Top Rated Clothing Categories")

    top_categories = (
        df.groupby("Department Name")["Rating"]
        .mean()
        .sort_values(ascending=False)
    )

    st.write(top_categories)

    st.subheader("Highly Recommended Clothing Types")

    recommended_items = df[df["Recommended IND"] == 1]

    recommendation_summary = recommended_items["Department Name"].value_counts()

    st.bar_chart(recommendation_summary)

    st.subheader("Age Group vs Average Rating")

    age_rating = df.groupby("Age Group")["Rating"].mean()

    fig6, ax6 = plt.subplots()

    age_rating.plot(kind="bar", ax=ax6)

    st.pyplot(fig6)

    st.info(
    """
    Key Insight:

    Customers aged **26–35** show the highest engagement with 
    **Dresses and Tops**, indicating strong fashion demand 
    in this demographic group.
    """
    )