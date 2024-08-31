import requests
from textblob import TextBlob


def get_news_sentiment(ticker):
    # This is a placeholder function. In a real-world scenario,
    # you would use a news API to fetch recent articles about the company.
    api_key = "YOUR_NEWS_API_KEY"
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        return "Failed to fetch news data"

    articles = response.json()['articles']
    sentiments = [TextBlob(article['title']).sentiment.polarity for article in articles[:10]]
    avg_sentiment = sum(sentiments) / len(sentiments)

    sentiment_label = "positive" if avg_sentiment > 0 else "negative" if avg_sentiment < 0 else "neutral"
    return f"The current sentiment for {ticker} is {sentiment_label}, with a score of {avg_sentiment:.2f} out of 1"