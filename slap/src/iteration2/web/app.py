import os
from flask import Flask, request, render_template, jsonify, g, redirect, url_for
from flask.wrappers import Response
from services.slapStore import SlapStore, Config, Trip
from control.autoPilot import AutoPilot
from utils.headings import compassify
from services.logger import Logger
from transducers.sensorRegister import SensorRegister
from control.boatSim import BoatSim
from transducers.gps import Gps
import threading
import queue
import time
import json
from datetime import datetime

class WebServer:
    # Initialises the web server with required components
    def __init__(self, auto_pilot: AutoPilot, logger: Logger, sensor_register: SensorRegister, boat_sim: BoatSim, gps: Gps):
        # Importing the Auto Pilot instance
        self.auto_pilot = auto_pilot
        self.logger = logger
        self.sensor_register = sensor_register
        self.logging = False
        self.current_trip = None
        self.boat_sim = boat_sim
        self.gps = gps

    # Creates and configures the Flask web server
    def create_server(self, store: SlapStore):
        # Creating instances of Flask and the Database service
        app = Flask(__name__)
        self.store = store
        # Load boat data

        # Loads all configurations from the store
        def load_configs():
            f = store.listConfigs()
            print({'configs': f})
            return {'configs': f}

        # Loads all trips from the store
        def load_trips():
            trips = store.listTrips()
            print({'trips': trips})
            return {'trips': trips}

        # Template Routes
        
        # Renders the home page
        @app.route("/")
        def home():
            # Default Route
            return render_template('index.html')

        # Displays sensor readings on a dedicated page
        @app.route('/sensorsReadings')
        def sensorsReadings():
            data = self.sensor_register.getSensorReadings()
            print(data)
            return render_template('sensorsDisplay.html', sensorReadings = data)

        # Shows all configurations
        @app.route('/configs')
        def index():
            data = load_configs()
            return render_template('configs.html', configs = data["configs"])

        # Shows all trips
        @app.route('/trips')
        def trips():
            data = load_trips()
            return render_template('trips.html', trips=data["trips"])

        # Displays details of a specific trip
        @app.route('/view_trip/<int:tripId>', methods=['GET'])
        def view_trip(tripId):
            # Get trip details
            trip = self.store.getTrip(tripId)
            if not trip:
                return redirect(url_for('trips'))
            return render_template('view_trip.html', trip=trip)

        # Handles editing of configurations
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

        # Saves configuration changes
        @app.route('/save', methods=['POST'])
        def save():
            config_configId = int(request.form['configId'])
            print(config_configId)
            if config_configId == 0:
                config = Config(0, str(request.form['name']),float(request.form['proportional']),float(request.form['integral']),float(request.form['differential']))
                self.store.newConfig(config)
            else:
                updated_config = {
                    'configId': config_configId,
                    'name': request.form['name'],
                    'proportional': request.form['proportional'],
                    'integral': request.form['integral'],
                    'differential': request.form['differential']
                }
                updated_config = Config(updated_config['configId'], updated_config['name'], updated_config['proportional'], updated_config['integral'], updated_config['differential'])
                self.store.updateConfig(updated_config)
            return redirect(url_for('index'))

        # Selects a configuration as active
        @app.route('/select/<int:configId>', methods=['POST'])
        def select(configId):
            config = self.store.getConfig(configId)
            self.auto_pilot.setPidValues(config)
            self.store.setDefault(configId)
            return jsonify({'message': f'Selected config with ID: {configId}'})

        # Deletes a configuration
        @app.route('/delete/<int:configId>', methods=['POST'])
        def deleteConfig(configId):
            self.store.deleteConfig(configId)
            return redirect(url_for('index'))

        # API Routes
        
        # Sets the target heading for the autopilot
        @app.route('/api/setDirection', methods=['PUT'])
        def setDirection():
            try:
                heading = request.get_data().decode('utf-8')
                if int(heading) < 0 or int(heading) > 360:
                    response_data = {"angle": "Enter a value between 0 and 360"}
                    return jsonify(response_data), 200
                heading = self.auto_pilot.setHeading(int(heading))
                response_data = {"angle": str(heading)}
                return jsonify(response_data), 200
            except Exception as e:
                print(f"Error processing setDirection request: {str(e)}")
                return jsonify({"error": str(e)}), 400
            
        # Returns current heading information
        @app.route('/api/headings', methods=['GET'])
        def get_headings():
            heading = self.gps.getHeading()
            pilot_values = self.auto_pilot.getPilotValues()
            headings = {
                'target': pilot_values['target'],
                'tiller': pilot_values['tiller'],
                'actual': heading
            }
            return jsonify(headings)

        # Adjusts the current heading by a specified amount
        @app.route('/api/addDirection', methods=['PUT'])
        def addDirection():
            try:
                change = request.get_data().decode('utf-8')
                headings = self.auto_pilot.getPilotValues()
                heading = headings['target']
                heading = heading + int(change)
                heading = compassify(heading)
                heading = self.auto_pilot.setHeading(heading)
                response_data = {"angle": str(heading)}
                return jsonify(response_data), 200
            except Exception as e:
                print(f"Error processing request: {str(e)}")
                return jsonify({"error": str(e)}), 400
        
        # Toggles the logging system
        @app.route('/api/toggleLogging')
        def toggleLogging():
            try:
                print("toggleLogging")
                self.current_trip = None
                if self.logger.running:
                    self.logger.stop()
                else:
                    config = self.store.getCurrentConfig() 
                    self.auto_pilot.setPidValues(config)
                    self.logger.start(config)
                    self.current_trip = config
                status = {
                    'status': self.logger.running,
                    'tripName': "LogName"
                }
                return jsonify(status), 200
            except Exception as e:
                print(f"Error processing request to toggle logging: {str(e)}")
                return jsonify({"error": str(e)}), 400
            
        # Returns the current status of all system components
        @app.route('/api/systemStatus')
        def systemStatus():
            if self.current_trip is None:
                name = "No Trip"
                running = self.logger.running
                pilotRunning = self.auto_pilot.running
                simRunning = self.boat_sim.running
            else:
                name = self.current_trip.name
                running = self.logger.running
                pilotRunning = self.auto_pilot.running
                simRunning = self.boat_sim.running
            
            status = {
                'status': running,
                'tripName': name,
                'pilotRunning': pilotRunning,
                'simRunning': simRunning
            }
            return jsonify(status), 200
        
        # Returns current sensor readings
        @app.route('/api/sensorReadings')
        def sensorReadings():
            readings = self.sensor_register.getSensorReadings()
            return jsonify(readings), 200

        # Toggles the boat simulation
        @app.route('/api/toggleSimulation', methods=['GET'])
        def toggleSimulation():
            try:
                if self.boat_sim.running:
                    self.boat_sim.stopSim()
                    message = "Simulation stopped"
                else:
                    self.boat_sim.startSim()
                    message = "Simulation started"
                return jsonify({"message": message}), 200
            except Exception as e:
                print(f"Error processing request to toggle simulation: {str(e)}")
                return jsonify({"error": str(e)}), 400

        # Starts the autopilot
        @app.route('/api/startPilot')
        def startPilot():
            self.auto_pilot.start()
            return jsonify({'message': 'Pilot started'})

        # Stops the autopilot
        @app.route('/api/stopPilot')
        def stopPilot():
            self.auto_pilot.stop()
            return jsonify({'message': 'Pilot stopped'})

        # Uploads a trip to Mapbox
        @app.route('/api/uploadTrip/<int:tripId>', methods=['GET'])
        def uploadTrip(tripId):
            trip = self.store.getTrip(tripId)
            readings = self.store.getPosLogs(trip)
            self.logger.map_manager.uploadToMapbox(f"Slap Trip ID: {trip.tripId}", readings)
            return jsonify({'message': 'Trip uploaded'})
    
        return app