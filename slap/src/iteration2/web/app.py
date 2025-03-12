import os
from flask import Flask, request, render_template, jsonify, g
from services.slapStore import SlapStore
from services.slapStore import Boat
from control.autoPilot import AutoPilot
from utils.headings import compassify
from services.logger import Logger
import threading
import queue
import time

class WebServer:

    def __init__(self, auto_pilot: AutoPilot, logger: Logger):
        # Importing the Auto Pilot instance
        self.auto_pilot = auto_pilot
        self.logger = logger
        self.logging = False

        

    def create_server(self):

        # Creating instances of Flask and the Database service
        app = Flask(__name__)
        store = SlapStore()

        @app.route("/")
        def home():
            # Default Route
            return render_template('index.html')

        @app.route("/config")
        def config():
            # Route for adding a boat
            return render_template('config.html')

        @app.route('/api/setDirection', methods=['PUT'])
        def setDirection():
            try:
                # Sets the target heading based on users input in web page
                # Get data from request
                heading = request.get_data().decode('utf-8')
                print("Received data:", heading)

                # Update desired heading, returns the new actual heading
                heading = self.auto_pilot.setHeading(int(heading))

                # Return JSON response
                response_data = {"angle": str(heading)}
                print("Heading", response_data)

                return jsonify(response_data), 200

            except Exception as e:
                print(f"Error processing setDirection request: {str(e)}")
                return jsonify({"error": str(e)}), 400
            
        @app.route('/api/headings', methods=['GET'])
        def get_headings():
            # Returns Headings (Target and Actual)
            #headings = self.auto_pilot.getHeadings()
            #print(headings['tiller'])
            return jsonify(self.auto_pilot.getHeadings())
    

        @app.route('/api/addDirection', methods=['PUT'])
        def addDirection():
            try:
                # increments the target heading based on users input in web page
                # Get data from request
                change = request.get_data().decode('utf-8')
                print("Received data:", change)

                # Update desired heading, returns the new actual heading
                headings = self.auto_pilot.getHeadings()

                heading = headings['target']
                heading = heading + int(change)
                heading = compassify(heading)

                heading = self.auto_pilot.setHeading(heading)
               
                # Return JSON response
                response_data = {"angle": str(heading)}
                print("Heading", response_data)

                return jsonify(response_data), 200


            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"error": str(e)}), 400
        
        @app.route('/api/toggleLogging', methods=['GET'])
        def toggleLogging():
            try:

                if self.logger.isRunning():
                    self.logger.stop()
                else:
                    self.logger.start()

                status = {
                'status': self.logger.isRunning(),
                'tripName': "LogName"
                }

                return jsonify(status), 200

            except Exception as e:
                print(f"Error processing request to toggle logging: {str(e)}")
                return jsonify({"error": str(e)}), 400

        return app
        