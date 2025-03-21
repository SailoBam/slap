import os
from flask import Flask, request, render_template, jsonify, g, redirect, url_for
from services.slapStore import SlapStore, Config, Trip
from control.autoPilot import AutoPilot
from utils.headings import compassify
from services.logger import Logger
import threading
import queue
import time
import json
from datetime import datetime

class WebServer:

    def __init__(self, auto_pilot: AutoPilot, logger: Logger):
        # Importing the Auto Pilot instance
        self.auto_pilot = auto_pilot
        self.logger = logger
        self.logging = False

        

    def create_server(self, store: SlapStore):

        # Creating instances of Flask and the Database service
        app = Flask(__name__)
        self.store = store
        # Load boat data

        def load_configs():
            f = store.listConfigs()
            print({'configs': f})
            
            #with open('C:/Users/franc/vscode/projects/slap/slap/src/iteration2/data.json', 'r') as f:
           #    print(json.load(f))
            return {'configs': f}

        def save_configs(data):
            with open('C:/Users/franc/vscode/projects/slap/slap/src/iteration2/data.json', 'w') as f:
                json.dump(data, f, indent=4)

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
                self.current_trip = "null"

                if self.logger.isRunning():
                    self.logger.stop()
                else:
                    config = self.auto_pilot.getCurrentConfig() 
                    self.logger.start(config)
                status = {
                'status': self.logger.isRunning(),
                'tripName': "LogName"
                }

                return jsonify(status), 200

            except Exception as e:
                print(f"Error processing request to toggle logging: {str(e)}")
                return jsonify({"error": str(e)}), 400
            
            # Boat database roots 

        @app.route('/configs')
        def index():
            data = load_configs()
            return render_template('configs.html', configs = data["configs"])

        @app.route('/edit/<int:configId>', methods=['GET'])
        def edit(configId):
            if configId == 0:
                config = {'configId': 0, 'name': 'New Config', 'proportional': '0', 'integral': '0', 'differential': '0'}
                return render_template('edit.html', config=config)

            else:
                data = load_configs()
                config = next((proportional for proportional in data['configs'] if proportional['configId'] == configId), None)
                if config:
                    return render_template('edit.html', config=config)
                return redirect(url_for('index'))

        @app.route('/save', methods=['POST'])
        def save():
            config_configId = int(request.form['configId'])
            print(config_configId)
            if config_configId == 0:
                config = Config(0, str(request.form['name']),int(request.form['proportional']),int(request.form['integral']),int(request.form['differential']))
                self.store.newConfig(config)
            
            else:
                updated_config = {
                    'configId': config_configId,
                    'name': request.form['name'],
                    'proportional': request.form['proportional'],
                    'integral': request.form['integral'],
                    'differential': request.form['differential']
                }
                self.store.updateConfig(updated_config)

            return redirect(url_for('index')) 

        @app.route('/select/<int:configId>', methods=['POST'])
        def select(configId):
            # This route will be called via AJAX when a row is selected
            config = self.store.getConfig(configId)
            self.auto_pilot.setPidValues(config)
            self.store.setDefault(configId)
            return jsonify({'message': f'Selected config with ID: {configId}'})

        return app
        