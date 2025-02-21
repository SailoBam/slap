from flask import Flask, request, render_template, jsonify, g
from database.slapStore import SlapStore
from database.slapStore import Boat
import threading
import queue
import time

app = Flask(__name__)


request_queue = queue.Queue()
angle = 0



@app.route("/")
def home():
    return render_template('changeangle.html')

@app.route("/config")
def config():
    return render_template('config.html')

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

@app.route('/addDirection', methods=['PUT'])
def addDirection():
    try:
        # Get data from request
        data = request.get_data().decode('utf-8')
        print("Received data:", data)

        # Update global angle
        global angle
        angle += int(data)

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

def updateTarget():
    global angle
    return angle