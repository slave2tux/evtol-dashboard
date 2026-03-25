import feedparser

def fetch_mightyfly_news():
    url = "https://news.google.com/rss/search?q=MightyFly+eVTOL"
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:5]: # limit to 5 latest
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })
    return articles