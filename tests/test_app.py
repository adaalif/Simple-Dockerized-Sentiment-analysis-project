from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

# Create a client for testing the FastAPI app
client = TestClient(app)

def test_read_root():
    """
    Tests if the root endpoint ('/') returns a 200 OK status and HTML content.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']

@patch("app.main.get_tweets") # Mock the function where it's used in the main app
def test_get_topic_sentiment_success(mock_get_tweets):
    """
    Tests the /api/sentiment/{topic} endpoint with a successful mocked API call.
    It ensures the endpoint processes the data correctly and returns the aggregated sentiment.
    """
    # Define the fake data that our mock function will return
    fake_tweets = [
        "Python is an amazing language!", # -> Positive
        "I love coding in Python.",       # -> Positive
        "I hate bugs in my Python code.", # -> Negative
        "Python is a programming language."# -> Neutral
    ]
    mock_get_tweets.return_value = fake_tweets

    # Call the API endpoint
    response = client.get("/api/sentiment/python")

    # Assertions for the response
    assert response.status_code == 200
    data = response.json()
    
    assert data["topic"] == "python"
    assert len(data["tweets"]) == 4
    
    # Check the aggregated results. Based on our model's likely predictions:
    # Note: The exact numbers depend on the model's training.
    # We are checking if the structure is correct and if the counts are plausible.
    assert "Positive" in data["results"]
    assert "Negative" in data["results"]
    assert "Neutral" in data["results"]
    assert data["results"]["Positive"] == 2
    assert data["results"]["Negative"] == 1
    assert data["results"]["Neutral"] == 1

@patch("app.main.get_tweets")
def test_get_topic_sentiment_no_tweets(mock_get_tweets):
    """
    Tests the API endpoint when the Twitter client returns no tweets.
    """
    # Configure the mock to return an empty list
    mock_get_tweets.return_value = []

    response = client.get("/api/sentiment/a_very_rare_topic")

    assert response.status_code == 200
    data = response.json()
    
    assert data["topic"] == "a_very_rare_topic"
    assert data["tweets"] == []
    assert data["results"] == {}
    assert "No tweets found" in data["message"]
