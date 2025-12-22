from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from collections import Counter

# Import our new and existing modules
from app.model import predict_sentiment
from app.twitter_client import get_tweets

BASE_DIR = Path(__file__).resolve(strict=True).parent

app = FastAPI()
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/sentiment/{topic}")
async def get_topic_sentiment(topic: str):
    """
    API endpoint to get sentiment for a topic.
    - Fetches tweets from the Twitter API.
    - Predicts sentiment for each tweet.
    - Aggregates and returns the results.
    """
    # 1. Get tweets
    tweets = get_tweets(topic, count=100)
    
    if not tweets:
        return {
            "topic": topic,
            "results": {},
            "tweets": [],
            "message": "No tweets found for this topic."
        }

    # 2. Predict sentiment for each tweet
    analyzed_tweets = []
    sentiments = []
    for tweet in tweets:
        sentiment = predict_sentiment(tweet)
        sentiments.append(sentiment)
        analyzed_tweets.append({"text": tweet, "sentiment": sentiment})
    
    # 3. Aggregate results
    sentiment_counts = Counter(sentiments)
    
    # 4. Return JSON response
    return {
        "topic": topic,
        "results": sentiment_counts,
        "tweets": analyzed_tweets
    }

