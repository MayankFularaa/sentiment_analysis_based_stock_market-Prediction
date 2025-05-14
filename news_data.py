import requests

def get_news_articles(ticker):
    api_key = "a1e0249a2b8142c698aa333622374684"
    url = f"https://newsapi.org/v2/everything?q={ticker}&sortBy=publishedAt&language=en&apiKey={api_key}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            print("Error fetching news:", data)
            return []

        articles = data.get("articles", [])

        return [
            {
                "title": article.get("title", "No Title"),
                "url": article.get("url", "#")
            }
            for article in articles[:5]  # top 5
            if article.get("title") and article.get("url")
        ]

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
