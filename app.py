import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = "a3f417b116fa4104b3c547e8ee9d32e1"
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("📰 Advanced News Dashboard")
st.markdown("Stay updated with the latest news from around the world.")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("News Filters")

country = st.sidebar.selectbox(
    "🌍 Select Country",
    {
        "India": "in",
        "United States": "us",
        "United Kingdom": "gb",
        "Australia": "au",
        "Canada": "ca",
        "Germany": "de",
        "France": "fr"
    }
)

category = st.sidebar.selectbox(
    "📰 Select Category",
    [
        "general",
        "business",
        "entertainment",
        "health",
        "science",
        "sports",
        "technology"
    ]
)

keyword = st.sidebar.text_input(
    "🔍 Search Keyword",
    placeholder="e.g. AI, Tesla, Cricket"
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=15
)

# -----------------------------
# FETCH NEWS
# -----------------------------
@st.cache_data(ttl=300)
def fetch_news(country_code, category_name, query):
    params = {
        "apiKey": API_KEY,
        "country": country_code,
        "category": category_name,
        "pageSize": 100
    }

    if query:
        params["q"] = query

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

# -----------------------------
# LOAD DATA
# -----------------------------
with st.spinner("Fetching latest headlines..."):
    news_data = fetch_news(country, category, keyword)

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
if news_data and news_data["status"] == "ok":

    articles = news_data["articles"][:article_count]

    st.success(f"Found {len(articles)} articles")

    for article in articles:

        title = article.get("title", "No Title")
        description = article.get("description", "")
        source = article.get("source", {}).get("name", "Unknown")
        url = article.get("url", "")
        image = article.get("urlToImage", "")
        published = article.get("publishedAt", "")

        try:
            published = datetime.strptime(
                published,
                "%Y-%m-%dT%H:%M:%SZ"
            ).strftime("%d %b %Y, %I:%M %p")
        except:
            pass

        with st.container():

            col1, col2 = st.columns([1, 3])

            with col1:
                if image:
                    st.image(image, use_container_width=True)

            with col2:
                st.subheader(title)

                st.caption(
                    f"📌 Source: {source} | 🕒 Published: {published}"
                )

                if description:
                    st.write(description)

                st.markdown(
                    f"[🔗 Read Full Article]({url})"
                )

            st.divider()

    # -------------------------
    # ANALYTICS SECTION
    # -------------------------
    st.header("📊 News Analytics")

    sources = [
        article.get("source", {}).get("name", "Unknown")
        for article in articles
    ]

    source_df = pd.DataFrame(
        sources,
        columns=["Source"]
    )

    source_count = (
        source_df["Source"]
        .value_counts()
        .reset_index()
    )

    source_count.columns = ["Source", "Articles"]

    st.bar_chart(
        source_count.set_index("Source")
    )

else:
    st.error(
        "Unable to fetch news. Check your API key or API limits."
    )