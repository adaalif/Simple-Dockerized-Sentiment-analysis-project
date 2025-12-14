import xgboost as xgb
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent

vectorizer = joblib.load(f"{BASE_DIR}/sentiment_model/vectorizer.pkl")
model = xgb.XGBClassifier()
model.load_model(f"{BASE_DIR}/sentiment_model/model.xgb")

labels = ['Negative', 'Neutral', 'Positive']

def predict_sentiment(text: str) -> str:
    text_vectorized = vectorizer.transform([text])
    prediction = model.predict(text_vectorized)
    return labels[prediction[0]]
