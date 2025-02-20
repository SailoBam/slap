from flask import Flask, request
import threading
import queue
import time

app = Flask(__name__)

# Queue to store incoming requests for processing
request_queue = queue.Queue()

# Flask Route - Adds incoming request data to the queue
@app.route('/send', methods=['GET'])
def handle_request():
    data = request.args.get('data', 'No Data')
    request_queue.put(data)  # Add request data to the queue
    return f"Received: {data}"

# Function to run Flask in a separate thread
def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)

# Function to process requests in the background
def process_requests():
       while True:
        if not request_queue.empty():
            data = request_queue.get()
            print(f"Processing request: {data}")
        time.sleep(1)  # Simulate processing time
# Create and start both threads
flask_thread = threading.Thread(target=run_flask, daemon=True)
processing_thread = threading.Thread(target=process_requests, daemon=True)

flask_thread.start()
processing_thread.start()

# Keep the main thread running
while True:
    time.sleep(1)
