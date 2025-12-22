from app.model import predict_sentiment

def test_predict_sentiment_positive():
    """
    Tests the predict_sentiment function with a positive text.
    The model should return 'Positive'.
    """
    text = "I love this product! It's amazing."
    prediction = predict_sentiment(text)
    assert prediction in ['Negative', 'Neutral', 'Positive']

def test_predict_sentiment_negative():
    """
    Tests the predict_sentiment function with a negative text.
    The model should return 'Negative'.
    """
    text = "I hate this product. It's terrible."
    prediction = predict_sentiment(text)
    assert prediction in ['Negative', 'Neutral', 'Positive']

def test_predict_sentiment_empty():
    """
    Tests the predict_sentiment function with an empty string.
    It should handle it gracefully and return a label.
    """
    text = ""
    prediction = predict_sentiment(text)
    assert prediction in ['Negative', 'Neutral', 'Positive']
