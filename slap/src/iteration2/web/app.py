from flask import Flask, request, render_template, jsonify, g
from services.slapStore import SlapStore
from services.slapStore import Boat
from control.autoPilot import AutoPilot
import threading
import queue
import time

class WebServer:

    def __init__(self, auto_pilot: AutoPilot):
        self.auto_pilot = auto_pilot
        

    def create_server(self):

        app = Flask(__name__)
        store = SlapStore()

        @app.route("/")
        def home():
            return render_template('changeangle.html')

        @app.route("/config")
        def config():
            return render_template('config.html')

        @app.route('/api/setDirection', methods=['PUT'])
        def setDirection():
            try:
                # Get data from request
                heading = request.get_data().decode('utf-8')
                print("Received data:", heading)

                # Update desired heading, returns the new actual heading
                heading = self.auto_pilot.setHeading(int(heading))

                # Prepare response
                response_data = {"angle": str(heading)}
                print("Heading", response_data)

                # Return JSON response
                return jsonify(response_data), 200

            except Exception as e:
                print(f"Error processing setDirection request: {str(e)}")
                return jsonify({"error": str(e)}), 400
            
        @app.route('/api/headings', methods=['GET'])
        def get_headings():
            return jsonify(self.auto_pilot.getHeadings())
    

        @app.route('/api/addDirection', methods=['PUT'])
        def addDirection():
            try:
                # Get data from request
                change = request.get_data().decode('utf-8')
                print("Received data:", heading)

                # Update desired heading, returns the new actual heading
                heading = self.auto_pilot.getHeading()
                heading += change
                heading = self.auto_pilot.setHeading(heading)

                # Prepare response
                response_data = {"angle": heading}
                print("Heading", response_data)

                # Return JSON response
                return jsonify(response_data), 200


            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"error": str(e)}), 400
            

        return app
        