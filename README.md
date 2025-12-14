# Dockerized Sentiment Analysis with XGBoost and FastAPI

This project is a sentiment analysis application that uses a pre-trained XGBoost model and serves it via a FastAPI backend, all packaged in a Docker container.

## Project Structure

```
/
|-- app/
|   |-- __init__.py
|   |-- main.py             # FastAPI application
|   |-- model.py            # Model loading and prediction logic
|   |-- sentiment_model/    # Saved XGBoost model and vectorizer
|   |-- templates/
|   |   `-- index.html        # Simple HTML frontend
|-- Dockerfile
|-- load_tester.py        # Script to test the application's RPM
|-- README.md
|-- requirements.txt
|-- training/
|   `-- train_model.ipynb   # Notebook to train and save the model
```

## Setup and Usage

### 1. Train the Model

Before you can run the application, you need to train the model.

1.  Navigate to the `training` directory.
2.  Run the `train_model.ipynb` notebook. This will train the XGBoost model and the TF-IDF vectorizer and save them in the `app/sentiment_model` directory.

### 2. Run the Application

You can run the application either using Docker or directly.

#### Option A: Run with Docker
1.  Make sure you have Docker installed and running.
2.  Build the Docker image:
    ```bash
    docker build -t sentiment-analysis-app .
    ```
3.  Run the Docker container:
    ```bash
    docker run -p 8000:8000 sentiment-analysis-app
    ```

#### Option B: Run Locally
1. Install the dependencies: `pip install -r requirements.txt`
2. Run the application: `uvicorn app.main:app --host 0.0.0.0 --port 8000`


### 3. Use the Application

Once the application is running, you can access it in your browser:

-   **Frontend:** Open [http://localhost:8000](http://localhost:8000) to use the web interface for sentiment analysis.
-   **RPM Endpoint:** Open [http://localhost:8000/rpm](http://localhost:8000/rpm) to see the total number of requests made to the prediction endpoint.

---

## 4. Load Testing

To test how many requests per minute (RPM) your application can handle, you can use the `load_tester.py` script.

1.  **Make sure the application is running** (either via Docker or locally).
2.  Open a new terminal in the project's root directory.
3.  Run the load testing script:
    ```bash
    python load_tester.py
    ```

The script will send requests to the `/predict` endpoint for 60 seconds from 10 concurrent threads and then print the total successful requests, which gives you an idea of the RPM. You can modify the `NUM_THREADS` and `TEST_DURATION_SECONDS` variables inside the script to change the load.