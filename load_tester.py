import requests
import threading
import time
import sys
import itertools

# Configuration
NUM_THREADS = 10
TEST_DURATION_SECONDS = 60  # Run for 1 minute
URL = "http://localhost:8000/predict"

successful_requests = 0
lock = threading.Lock()

def send_request():
    """Sends a single POST request to the predict endpoint."""
    global successful_requests
    try:
        response = requests.post(URL, data={"text": "This is a test."})
        if response.status_code == 200:
            with lock:
                successful_requests += 1
    except requests.exceptions.RequestException as e:
        # You can print errors if you want to debug
        # print(f"An error occurred: {e}")
        pass

def worker(stop_time):
    """A worker thread that continuously sends requests."""
    while time.time() < stop_time:
        send_request()

def spinner(stop_event):
    """Display a simple spinner in the console."""
    spin_chars = itertools.cycle(['|', '/', '-', '\\'])
    while not stop_event.is_set():
        sys.stdout.write(f" Running test... {next(spin_chars)}")
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b' * 18) # Move cursor back

def main():
    print("Starting load test...")
    
    # --- Spinner setup ---
    stop_spinner_event = threading.Event()
    spinner_thread = threading.Thread(target=spinner, args=(stop_spinner_event,))
    spinner_thread.start()
    
    threads = []
    stop_time = time.time() + TEST_DURATION_SECONDS

    # Reset counter for multiple runs
    global successful_requests
    successful_requests = 0

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(stop_time,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # --- Stop spinner ---
    stop_spinner_event.set()
    spinner_thread.join()
    
    # Clear the spinner line
    sys.stdout.write(' ' * 20 + '\r')
    print("Load test finished.")

    # Correctly calculate RPM
    rpm = (successful_requests / TEST_DURATION_SECONDS) * 60 if TEST_DURATION_SECONDS > 0 else 0

    # Generate HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Load Test Results</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; margin: 2em; background-color: #f9f9f9; color: #333; }}
        .container {{ max-width: 600px; margin: auto; }}
        .card {{ background-color: #fff; border: 1px solid #e1e1e1; border-radius: 8px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
        h1 {{ color: #111; text-align: center;}}
        h2 {{ color: #333; border-bottom: 2px solid #f0f0f0; padding-bottom: 8px;}}
        p {{ color: #555; line-height: 1.6; }}
        strong {{ color: #000; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Load Test Results</h1>
        <div class="card">
            <h2>Summary</h2>
            <p><strong>URL Tested:</strong> {URL}</p>
            <p><strong>Test Duration:</strong> {TEST_DURATION_SECONDS} seconds</p>
            <p><strong>Number of Threads:</strong> {NUM_THREADS}</p>
            <hr>
            <p><strong>Total Successful Requests:</strong> {successful_requests}</p>
            <p><strong>Requests Per Minute (RPM):</strong> {rpm:.2f}</p>
        </div>
    </div>
</body>
</html>
"""

    # Write to HTML file
    report_filename = "load_test_results.html"
    with open(report_filename, "w") as f:
        f.write(html_content)

    print(f"Results saved to {report_filename}")

if __name__ == "__main__":
    main()
