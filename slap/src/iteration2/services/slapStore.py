import sqlite3
import ast
from transducers.sensor import Sensor

# --- All Classes possible to put into the database ---
class Config():
    # Class to store PID configuration settings

    def __init__(self, id: int,  name: str, proportional: float, integral: float, differential: float):
        # Contains and assigns the values for the Boat type
        self.name = name
        self.configId = id
        self.proportional = proportional
        self.integral = integral
        self.differential = differential

    @classmethod
    def from_dict(cls, row):
        # Alternative constructor that takes a dictionary of attributes
        return Config(
            id=row['configId'],
            name=row['name'], 
            proportional=float(row['proportional']),
            integral=float(row['integral']),
            differential=float(row['differential'])
        )

class Trip():
    # Class to store trip information
    def __init__(self, tripId: int, configId: int, time_started: str, time_ended: str, distance_travelled: float):
        # Contains and assigns the values for the Trip type
        self.tripId = tripId
        self.configId = configId
        self.timeStarted = time_started
        self.timeEnded = time_ended
        self.distanceTravelled = distance_travelled

    @classmethod
    def from_dict(cls, row):
        # Creates Trip object from database row
        return Trip(
            tripId=row['tripId'],
            configId=row['configId'],
            time_started=row['timeStarted'],
            time_ended=row['timeEnded'],
            distance_travelled=row['distanceTravelled']
        )

class Reading():
    # Class to store sensor readings
    def __init__(self, tripId: int, identifier: str, data: str, timestamp: str):
        self.identifier = identifier
        self.tripId = tripId
        self.data = data
        self.timeStamp = timestamp

    @classmethod
    def from_dict(cls, row):
        # Creates Reading object from database row
        return Reading(
            tripId=row['tripId'],
            identifier=row['identifier'],
            data=row['data'],
            timestamp=row['timeStamp']
        )

class SlapStore():
    # Main database management class
    def __init__(self, db_name: str):
        # Set up database and creates all necessary tables
        # Use in-memory database if db_name is ":memory:"
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

        # Config table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS CONFIGS (
                configId INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                proportional REAL NOT NULL,
                integral REAL NOT NULL,
                differential REAL NOT NULL,
                isDefault BOOLEAN
            )
        ''')

        # Sensor table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sensor (
                identifier TEXT PRIMARY KEY,
                sensorName TEXT NOT NULL,
                units TEXT NOT NULL
            )
        ''')

        # Trip table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Trip (
                tripId INTEGER PRIMARY KEY AUTOINCREMENT,
                configId INTEGER NOT NULL,
                timeStarted DATE NOT NULL,
                timeEnded TEXT NOT NULL,
                distanceTravelled FLOAT NOT NULL,
                FOREIGN KEY (configId) REFERENCES CONFIGS(configId) ON DELETE CASCADE
            )
        ''')

        # Readings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Readings (
                identifier TEXT NOT NULL,
                tripId INTEGER NOT NULL,
                data TEXT NOT NULL,
                timeStamp TIME NOT NULL,
                FOREIGN KEY (identifier) REFERENCES Sensor(identifier) ON DELETE CASCADE,
                FOREIGN KEY (tripId) REFERENCES Trip(tripId) ON DELETE CASCADE
            )
        ''')

        self.connection.commit()

    def newConfig(self, config: Config): 
        # Creates a new configuration in the database
        self.cursor.execute(f"INSERT INTO CONFIGS (name, proportional, integral, differential) VALUES ('{config.name}','{config.proportional}','{config.integral}','{config.differential}')")
        self.connection.commit()
        config.configId = self.cursor.lastrowid
        return config
    
    def getGains(self,id: int):
        # Retrieves PID gains for a specific configuration
        gains = {}
        self.cursor.execute(f"SELECT proportional, integral, differential FROM CONFIGS WHERE configId = '{id}'")
        columns = [desc[0] for desc in self.cursor.description]
        for row in self.cursor.fetchall():
            row_dict = dict(zip(columns, row))
            gains = row_dict 
        return gains

    def listConfigs(self):
        # Lists all configurations in the database
        self.cursor.execute(f"SELECT * FROM CONFIGS")
        rows = self.cursor.fetchall()
        return [dict(row) for row in rows]
    
    def setDefault(self, configId: int):
        # Sets a configuration as the default one
        self.cursor.execute(f"UPDATE CONFIGS SET isDefault = False WHERE isdefault = True")
        self.cursor.execute(f"UPDATE CONFIGS SET isDefault = True WHERE configId = '{configId}'")
        self.connection.commit()

    def updateConfig(self, config: Config):
        # Updates an existing configuration
        self.cursor.execute(f"UPDATE CONFIGS SET name = '{config.name}', proportional = '{config.proportional}', integral = '{config.integral}', differential = '{config.differential}' WHERE configId = '{config.configId}'")
        self.connection.commit()

    def deleteConfig(self, configId: int):
        # Deletes a configuration from the database
        self.cursor.execute(f"DELETE FROM CONFIGS WHERE configId = '{configId}'")
        self.connection.commit()

    def getCurrentConfig(self):
        # Gets the currently set default configuration
        try:
            self.cursor.execute(f"SELECT * FROM CONFIGS WHERE isDefault == True")
            row = self.cursor.fetchone()
            if row is not None:
                config = Config.from_dict(row)
            else:
                config = Config(0, 'Default', 0, 0, 0)
                self.newConfig(config)
                self.setDefault(config.configId)
            return config
        except Exception as e:
           print(f"Error: {e}")

    def getConfig(self, configId: int):
        # Gets a specific configuration by ID
        self.cursor.execute(f"SELECT * FROM CONFIGS WHERE configId == '{configId}'") 
        row = self.cursor.fetchone()
        config = Config.from_dict(row)
        return config
    
    def addSensor(self, sensor: Sensor): 
        # Adds a new sensor to the database if it doesn't exist
        self.cursor.execute(f"SELECT * FROM Sensor WHERE identifier == '{sensor.identifier}'")
        existing_sensor = self.cursor.fetchone()
        if existing_sensor is None:
            self.cursor.execute(f"INSERT INTO Sensor (identifier, sensorName, units) VALUES ('{sensor.identifier}', '{sensor.name}', '{sensor.units}')")
            self.connection.commit()

    def getSensor(self, identifier: str):
        # Gets sensor information by identifier
        self.cursor.execute(f"SELECT * FROM Sensor WHERE identifier == '{identifier}'")
        row = self.cursor.fetchone()
        return row

    def createTrip(self, trip: Trip):
        # Creates a new trip in the database
        self.cursor.execute(f"INSERT INTO Trip (configId, timeStarted, timeEnded, distanceTravelled) VALUES ('{trip.configId}', '{trip.timeStarted}', '{trip.timeEnded}', '{trip.distanceTravelled}')")
        trip.tripId = self.cursor.lastrowid
        self.connection.commit()
        return trip

    def getTrip(self, tripId: int):
        # Gets trip information by ID
        self.cursor.execute(f"SELECT * FROM Trip WHERE tripId == '{tripId}'")
        row = self.cursor.fetchone()
        trip = Trip.from_dict(row)
        return trip
    
    def endTrip(self, trip: Trip):
        # Updates trip end time
        try:
            self.cursor.execute(f"UPDATE Trip SET timeEnded = ? WHERE tripId = ?", (trip.timeEnded, trip.tripId))
            self.connection.commit()
        except Exception as e:
            print(f"Error updating trip: {e}")
            self.connection.rollback()

    def writeLog(self, reading: Reading):
        # Writes a new sensor reading to the database
        self.cursor.execute(f"INSERT INTO Readings (tripId, identifier, data, timeStamp) VALUES ('{reading.tripId}', '{reading.identifier}', '{reading.data}', '{reading.timeStamp}')")
        self.connection.commit()
        return True

    def getPosLogs(self, trip: Trip):
        # Gets all position logs for a specific trip
        data = []
        self.cursor.execute(f"SELECT data FROM Readings WHERE identifier == 'Position' AND tripId == '{trip.tripId}'")
        rows = self.cursor.fetchall()
        for row in rows:
            # Splits lon/lat string into list of strings
            pos_list = row[0].split(",")
            # Convert string list to float list
            num_list = list(map(float, pos_list))
            # Add positional list into waypoints list
            data.append(num_list)
        return data

    def getLog(self, trip: Trip):
        data = []
        # Get all readings from database
        self.cursor.execute(f"SELECT data FROM Readings WHERE tripId == '{trip.tripId}'")
        rows = self.cursor.fetchall()
        for row in rows:
            # Splits lon/lat string into list of strings
            pos_list = row[0].split(",")
            # Convert string list to float list
            num_list = list(map(float, pos_list))
            # Add positional list into waypoints list
            data.append(num_list)
        return data
    
 
    def getReading(self, sensor_id: int, trip_id: int):
        # Returns all Reading information using the sensorId and TripId as identifiers
        self.cursor.execute(f"SELECT * FROM Readings WHERE sensorId == {sensor_id} AND tripId == {trip_id}")
        row = self.cursor.fetchone()
        return row
    
    def getAllReadings(self):
        # Prints all readings from any sensor 
        self.cursor.execute(f"SELECT * FROM Readings")
        for row in self.cursor.fetchall():
            print(row)

    def dropAllTables(self):
        # Deletes all tables
        self.cursor.execute(f"DROP TABLE *")

    def listTrips(self):
        # Returns all trips from the database
        self.cursor.execute("SELECT * FROM Trip")
        rows = self.cursor.fetchall()
        trips = []
        for row in rows:
            trips.append({
                'tripId': row['tripId'],
                'configId': row['configId'],
                'timeStarted': row['timeStarted'],
                'timeEnded': row['timeEnded'],
                'distanceTravelled': row['distanceTravelled']
            })
        return trips
    
