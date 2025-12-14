from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.model import predict_sentiment
from pathlib import Path
import threading
import time
import requests

BASE_DIR = Path(__file__).resolve(strict=True).parent

app = FastAPI()
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")

request_count = 0

# --- Load Testing ---
lock = threading.Lock()
load_test_state = {"status": "idle", "result": None} # idle, running, finished, error

def send_request_worker(url, results_dict):
    """Sends a single POST request to the predict endpoint."""
    try:
        response = requests.post(url, data={"text": "This is a test."})
        if response.status_code == 200:
            with lock:
                results_dict['successful_requests'] += 1
    except requests.exceptions.RequestException:
        pass

def load_test_worker(stop_time, url, results_dict):
    """A worker thread that continuously sends requests."""
    while time.time() < stop_time:
        send_request_worker(url, results_dict)

def run_load_test(duration_seconds, num_threads, host, port):
    """Triggers the load test."""
    global load_test_state
    
    with lock:
        if load_test_state["status"] == "running":
            return
        load_test_state["status"] = "running"
        load_test_state["result"] = None

    results_dict = {'successful_requests': 0}

    url = f"http://{host}:{port}/predict"
    threads = []
    stop_time = time.time() + duration_seconds

    for _ in range(num_threads):
        thread = threading.Thread(target=load_test_worker, args=(stop_time, url, results_dict))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    successful_requests = results_dict['successful_requests']
    rpm = 0
    if duration_seconds > 0:
        rpm = successful_requests * (60 / duration_seconds)
    
    with lock:
        load_test_state["status"] = "finished"
        load_test_state["result"] = {
            "successful_requests": successful_requests,
            "duration_seconds": duration_seconds,
            "rpm": rpm,
        }

@app.get("/load-test", response_class=HTMLResponse)
async def load_test_page(request: Request):
    return templates.TemplateResponse("load_test.html", {"request": request})

@app.post("/load-test")
async def trigger_load_test(request: Request, duration: int = 60, threads: int = 10):
    global load_test_state
    with lock:
        if load_test_state["status"] == "running":
            # Using 409 Conflict status code might be more appropriate
            return {"status": "error", "message": "Load test already in progress."}
    
    host = request.client.host
    port = request.url.port
    
    test_thread = threading.Thread(target=run_load_test, args=(duration, threads, host, port))
    test_thread.start()
    
    return {"status": "success", "message": f"Load test started with {threads} threads for {duration} seconds."}

@app.get("/load-test/status")
async def get_load_test_status():
    global load_test_state
    with lock:
        return load_test_state

# --- End Load Testing ---


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, text: str = Form(...)):
    global request_count
    request_count += 1
    sentiment = predict_sentiment(text)
    return templates.TemplateResponse("index.html", {"request": request, "sentiment": sentiment, "text": text})

@app.get("/total_requests")
async def get_total_requests():
    return {"total_predict_requests": request_count}
