import requests
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

# ==== BEARER TOKEN (from your developer app) ====
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAB3m0gEAAAAA0K2p9sHTO0Iwc2rO%2BTKwZWrx04E%3DJL7fjLIDFxCrN2Pi2gVKZITZJzhHsK9mw4g9nEBdlzreiRyxZ8"

# ==== HEADERS ====
def create_headers():
    return {"Authorization": f"Bearer {BEARER_TOKEN}"}

# ==== GET RECENT TWEETS ====
def get_recent_tweets(query, max_results=10):
    url = "https://api.twitter.com/2/tweets/search/recent"
    params = {
        'query': f"{query} lang:en -is:retweet",
        'max_results': max_results,
        'tweet.fields': 'text'
    }
    response = requests.get(url, headers=create_headers(), params=params)
    if response.status_code != 200:
        print("Twitter API error:", response.text)
        return []
    data = response.json().get("data", [])
    return [tweet["text"] for tweet in data]

# ==== LOAD FinBERT MODEL ====
model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
sentiment_model = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, framework="pt")

# ==== MAIN SENTIMENT FUNCTION ====
def get_twitter_sentiment(ticker, max_results=10):
    try:
        tweets = get_recent_tweets(ticker, max_results)
        if not tweets:
            return 0  # No data
        results = sentiment_model(tweets)

        def score_label(label):
            label = label.lower()
            if label == "positive":
                return 1
            elif label == "negative":
                return -1
            return 0

        scores = [score_label(res["label"]) for res in results]
        avg_score = sum(scores) / len(scores)
        return round(avg_score, 3)
    except Exception as e:
        print("Sentiment analysis error:", e)
        return 0
