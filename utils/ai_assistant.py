import pandas as pd
import streamlit as st

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("data/womens_clothing_reviews.csv")
    return df.dropna(subset=["Rating", "Class Name", "Age"])


# -----------------------
# HELPER FUNCTION
# -----------------------

def filter_valid(grouped, min_count=50):
    return grouped[grouped["count"] >= min_count]


# -----------------------
# MAIN CHATBOT
# -----------------------

def fashion_ai_response(user_input):
    df = load_and_clean_data()
    user_input = user_input.lower()
    
    # -----------------------
    # SECURE API INTEGRATION (Optional)
    # -----------------------
    # If upgrading to an external API like OpenAI, securely load your API key here:
    # api_key = st.secrets.get("OPENAI_API_KEY", None)
    # if api_key:
    #     # Make API call here
    #     pass

    # -----------------------
    # BEST ITEMS
    # -----------------------
    if "best" in user_input or "top" in user_input:

        grouped = df.groupby("Class Name")["Rating"].agg(["mean", "count"])
        grouped = filter_valid(grouped)

        best = grouped.sort_values(by="mean", ascending=False).head(3)

        return "🔥 Top Trending Categories:\n" + "\n".join(best.index.tolist())

    # -----------------------
    # WORST ITEMS
    # -----------------------
    elif "worst" in user_input or "low" in user_input:

        grouped = df.groupby("Class Name")["Rating"].agg(["mean", "count"])
        grouped = filter_valid(grouped)

        worst = grouped.sort_values(by="mean", ascending=True).head(3)

        return "⚠️ Low Rated Categories:\n" + "\n".join(worst.index.tolist())

    # -----------------------
    # RECOMMENDED
    # -----------------------
    elif "recommend" in user_input:

        rec = df[df["Recommended IND"] == 1]["Class Name"].value_counts().head(3)

        return "👍 Most Recommended:\n" + "\n".join(rec.index.tolist())

    # -----------------------
    # AGE TREND (FIXED)
    # -----------------------
    elif "age" in user_input:

        age_group = df.groupby("Age")["Rating"].agg(["mean", "count"])

        # remove low data ages
        age_group = age_group[age_group["count"] >= 30]

        best_age = age_group["mean"].idxmax()

        return f"👩 Age group around {best_age} shows highest satisfaction"

    # -----------------------
    # DEFAULT
    # -----------------------
    else:
        return "💡 Ask about: best, worst, recommended, age trends"












































































# import pandas as pd

# df = pd.read_csv("data/womens_clothing_reviews.csv")

# def fashion_ai_response(user_input):
#     user_input = user_input.lower()

#     # LOW RATING
#     if "low" in user_input or "worst" in user_input:
#         low = df[df["Rating"] <= 2]["Class Name"].value_counts().head(3)
#         return "⚠️ Low Rated Categories:\n" + "\n".join(low.index.tolist())

#     # BEST ITEMS
#     elif "best" in user_input or "top" in user_input:
#         top = df[df["Rating"] >= 4]["Class Name"].value_counts().head(3)
#         return "🔥 Top Trending Categories:\n" + "\n".join(top.index.tolist())

#     # RECOMMENDED
#     elif "recommend" in user_input:
#         rec = df[df["Recommended IND"] == 1]["Class Name"].value_counts().head(3)
#         return "👍 Most Recommended:\n" + "\n".join(rec.index.tolist())

#     # AGE BASED
#     elif "age" in user_input:
#         age = df.groupby("Age")["Rating"].mean().idxmax()
#         return f"👩 Age {age} gives highest ratings"

#     else:
#         return "💡 Ask about: best, worst, recommended, age trends"
    















# def fashion_ai_response(question):

#     question = question.lower()

#     if "trend" in question:
#         return "Current fashion trends show high demand for dresses, tops, and casual wear."

#     elif "popular" in question:
#         return "Dresses and tops are currently the most popular categories."

#     elif "color" in question:
#         return "Trending colors include black, white, pink, and neutral tones."

#     elif "age" in question:
#         return "Customers aged 25-35 show the highest engagement."

#     else:
#         return "Fashion analytics suggests focusing on high-rated and frequently recommended products."
    
