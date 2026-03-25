import streamlit as st
import requests
from bs4 import BeautifulSoup
import feedparser
import re

@st.cache_data(ttl=3600)  # cache for 1 hour
def scrape_mightyfly_specs_from_rss():
    rss_url = "https://news.google.com/rss/search?q=MightyFly"
    feed = feedparser.parse(rss_url)

    specs = {
        "Company": "MightyFly",
        "Range (Miles)": None,
        "Payload (lbs)": None,
        "Power Type": None,
        "Market Focus": "B2B Logistics"
    }

    for entry in feed.entries[:5]:
        try:
            article_html = requests.get(entry.link, timeout=10).text
            soup = BeautifulSoup(article_html, "html.parser")
            text = soup.get_text(" ", strip=True).lower()

            # Payload detection
            payload_match = re.search(r"(\d+)\s*(lb|lbs|pound)", text)
            if payload_match:
                specs["Payload (lbs)"] = int(payload_match.group(1))

            # Range detection
            range_match = re.search(r"(\d+)\s*[- ]*\s*mile", text)
            if range_match:
                specs["Range (Miles)"] = int(range_match.group(1))

            # Power type detection
            if "hybrid" in text:
                specs["Power Type"] = "Hybrid"
            elif "electric" in text:
                specs["Power Type"] = "Electric"

        except Exception:
            continue

    return specs

