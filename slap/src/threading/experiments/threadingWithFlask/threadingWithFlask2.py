from flask import Flask, request, render_template, jsonify
import threading
import queue
import time

app = Flask(__name__)

request_queue = queue.Queue()

@app.route("/")
def home():
    return render_template('changeangle.html')

@app.route('/send', methods=['GET'])
def handle_request():
    data = request.args.get('data', 'No Data')
    request_queue.put(data)  # Add request data to the queue
    return f"Received: {data}"

@app.route('/setDirection', methods=['PUT'])
def setDirection():
    try:
        # Get data from request
        data = request.get_data().decode('utf-8')
        print("Received data:", data)

        # Update global angle
        global angle
        angle = int(data)

        # Prepare response
        response_data = {"angle": angle}
        print("Set Direction", response_data)

        # Return JSON response
        return jsonify(response_data), 200

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 400

# Function to run Flask in a separate thread
def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)

# Function to process requests in the background
def other():
    while True:
        #if not request_queue.empty():
        #    data = request_queue.get()
        #    print(f"Processing request: {data}")
        time.sleep(1)
        print("hello")
         #   if   # Simulate processing time 
        

flask_thread = threading.Thread(target=run_flask, daemon=True)
processing_thread = threading.Thread(target=process_requests, daemon=True)

flask_thread.start()
processing_thread.start()

# Keep the main thread running
while True:
    time.sleep(1)