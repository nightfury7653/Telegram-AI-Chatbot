# sentiment_service.py
from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    # Get polarity (-1 to 1) and convert to percentage
    sentiment_score = (analysis.sentiment.polarity + 1) * 50
    
    if sentiment_score > 60:
        sentiment = "positive"
    elif sentiment_score < 40:
        sentiment = "negative"
    else:
        sentiment = "neutral"
        
    return {
        'score': sentiment_score,
        'label': sentiment
    }