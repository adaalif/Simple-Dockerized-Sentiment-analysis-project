import pandas as pd
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import xgboost as xgb
import joblib
import os
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
MODEL_DIR = BASE_DIR / "app" / "sentiment_model"
MODEL_PATH = MODEL_DIR / "model.xgb"
VECTORIZER_PATH = MODEL_DIR / "vectorizer.pkl"

def load_data():
    """Loads the sentiment analysis dataset from Hugging Face."""
    print("Loading dataset...")
    dataset = load_dataset("Sp1786/multiclass-sentiment-analysis-dataset")
    df_train = dataset['train'].to_pandas()
    df_test = dataset['test'].to_pandas()
    
    # Clean data: fill NaNs and ensure text is string
    df_train['text'] = df_train['text'].fillna('').astype(str)
    df_test['text'] = df_test['text'].fillna('').astype(str)
    
    print("Dataset loaded successfully.")
    return df_train, df_test

def train_new_model(df_train):
    """Trains a new TF-IDF vectorizer and XGBoost model."""
    print("Training new model...")
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train = vectorizer.fit_transform(df_train['text'])
    y_train = df_train['label']
    
    model = xgb.XGBClassifier(objective='multi:softmax', num_class=3, seed=42)
    model.fit(X_train, y_train)
    
    print("New model trained successfully.")
    return model, vectorizer

def evaluate_model(model, vectorizer, df_test):
    """Evaluates the model's accuracy on the test set."""
    print("Evaluating model...")
    X_test = vectorizer.transform(df_test['text'])
    y_test = df_test['label']
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model accuracy: {accuracy:.4f}")
    return accuracy

def main():
    """
    Main function to run the training pipeline.
    - Loads data.
    - Compares against the existing model (if any).
    - Trains a new model.
    - Deploys the new model if it performs better.
    """
    df_train, df_test = load_data()
    
    current_accuracy = 0.0
    if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
        print("Found existing model. Evaluating it.")
        try:
            current_model = xgb.XGBClassifier()
            current_model.load_model(MODEL_PATH)
            current_vectorizer = joblib.load(VECTORIZER_PATH)
            current_accuracy = evaluate_model(current_model, current_vectorizer, df_test)
        except Exception as e:
            print(f"Could not load or evaluate existing model. Error: {e}. Retraining from scratch.")
            current_accuracy = 0.0
    else:
        print("No existing model found. Training a new model will be the first deployment.")

    new_model, new_vectorizer = train_new_model(df_train)
    new_accuracy = evaluate_model(new_model, new_vectorizer, df_test)

    if new_accuracy > current_accuracy:
        print(f"New model ({new_accuracy:.4f}) is better than current model ({current_accuracy:.4f}).")
        print("Deploying new model...")
        joblib.dump(new_vectorizer, VECTORIZER_PATH)
        new_model.save_model(MODEL_PATH)
        print("New model deployed successfully.")
    else:
        print(f"New model ({new_accuracy:.4f}) is not better than current model ({current_accuracy:.4f}).")
        print("Deployment skipped.")

if __name__ == "__main__":
    # Ensure the model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)
    main()
