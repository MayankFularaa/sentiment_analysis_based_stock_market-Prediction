from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import requests

model_name = "ProsusAI/finbert"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

sentiment_model = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, framework="pt")

NEWS_API_KEY = "a1e0249a2b8142c698aa333622374684"

def get_news_sentiment(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])[:5]
    scores = []
    for article in articles:
        title = article.get("title") or ""
        description = article.get("description") or ""
        content = title + ". " + description
        result = sentiment_model(content)[0]
        label = result['label'].lower()
        score = 1 if label == 'positive' else -1 if label == 'negative' else 0
        scores.append(score)
    return sum(scores) / len(scores) if scores else 0
