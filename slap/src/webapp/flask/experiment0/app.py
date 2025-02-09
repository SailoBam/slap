from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
angle = 0

@app.route("/")
def home():
    return render_template('changeangle.html')


@app.route("/svg")
def svg():
        return render_template('compass.html')

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

if __name__ == '__main__':
    app.run(debug=True)
