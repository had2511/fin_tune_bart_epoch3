import streamlit as st
from news_fetcher import fetch_top_headlines
from summarizer import load_summarizer, summarize_text
from datetime import datetime

# Load model + tokenizer once and cache
@st.cache_resource
def load_model():
    return load_summarizer()

tokenizer, model = load_model()

st.set_page_config(page_title="📰 Real-Time News Summarizer", layout="wide")

st.title("📰 Real-Time News Summarizer")
st.caption("Fetch latest headlines and get instant AI-generated summaries using your fine-tuned BART model.")

# Sidebar controls
st.sidebar.header("🧭 Controls")
country = st.sidebar.selectbox("🌍 Select Country", ["in", "us", "gb", "au", "ca"])
category = st.sidebar.selectbox(
    "🗂️ Select Category",
    ["general", "technology", "business", "entertainment", "health", "science", "sports"]
)
num_articles = st.sidebar.slider("📰 Number of Articles", 1, 10, 5)

# Main logic
if st.button("Fetch & Summarize"):
    st.info("Fetching latest news...")
    articles = fetch_top_headlines(country, category, page_size=num_articles)

    if not articles:
        st.error("No articles found or API limit reached.")
    else:
        st.success(f"Fetched {len(articles)} articles successfully!")

        for i, article in enumerate(articles, start=1):
            title = article.get("title", "No title")
            source = article.get("source", "Unknown")
            url = article.get("url", "#")
            content = article.get("content", "")
            published_at = article.get("publishedAt", "")

            # Convert published date if available
            if published_at:
                try:
                    published_at = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                    published_at = published_at.strftime("%b %d, %Y %I:%M %p")
                except Exception:
                    pass

            with st.container():
                st.markdown(f"### 🗞️ {i}. {title}")
                st.markdown(f"**📰 Source:** {source}")
                if published_at:
                    st.markdown(f"**🕒 Published:** {published_at}")
                st.markdown(f"🔗 [Read full article]({url})")

                st.markdown("⏳ Generating summary...")
                summary = summarize_text(tokenizer, model, content)

                st.markdown("#### 🧠 Summary:")
                st.success(summary)
                st.markdown("---")
