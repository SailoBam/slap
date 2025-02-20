import sqlite3

class Boat():

    def __init__(self, id: int,  name: str, model: str, proportional: int, integral: int, differential: int):
        self.name = name
        self.boatId = id
        self.model = model
        self.proportional = proportional
        self.integral = integral
        self.differential = differential

class Sensor():

    def __init__(self, id: int, boat: int, name: str, model: str):
        self.sensorId = id
        self.boatId = boat
        self.sensorName = name
        self.sensorModel = model

class Trip():
    def __init__(self, trip_id: int, boat_id: int, time_started: str, time_ended: str, date_started: str, date_ended: str, distance_travelled: float):
        self.tripId = trip_id
        self.boatId = boat_id
        self.timeStarted = time_started
        self.timeEnded = time_ended
        self.dateStarted = date_started
        self.dateEnded = date_ended
        self.distanceTravelled = distance_travelled

class Reading():
    def __init__(self, sensor_id: int, trip_id: int, data: float, timestamp: str):
        self.sensorId = sensor_id
        self.tripId = trip_id
        self.data = data
        self.timeStamp = timestamp
class SlapStore():
       
    def __init__(self):
        # Set up an in-memory database for testing
        print("Creating Database")
        self.connection = sqlite3.connect("slap.db")
        self.cursor = self.connection.cursor()

        # Boat table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BOATS (
                boatId INTEGER PRIMARY KEY,
                boatName TEXT NOT NULL,
                boatModel TEXT NOT NULL,
                proportional INTEGER NOT NULL,
                integral INTEGER NOT NULL,
                differential INTEGER NOT NULL
            )
        ''')

        # Sensor table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sensor (
                sensorId INTEGER PRIMARY KEY,
                boatId INTEGER NOT NULL,
                sensorName TEXT NOT NULL,
                sensorType TEXT NOT NULL,
                dataType TEXT NOT NULL,
                FOREIGN KEY (boatId) REFERENCES BOATS(boatId) ON DELETE CASCADE
            )
        ''')

        # Trip table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Trip (
                tripId INTEGER,
                boatId INTEGER NOT NULL,
                timeStarted TEXT NOT NULL,
                timeEnded TEXT NOT NULL,
                dateStarted DATE NOT NULL,
                dateEnded DATE NOT NULL,
                distanceTravelled FLOAT NOT NULL,
                PRIMARY KEY (tripId, boatId),
                FOREIGN KEY (boatId) REFERENCES BOATS(boatId) ON DELETE CASCADE
            )
        ''')

        # Reading table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Reading (
                sensorId INTEGER NOT NULL,
                tripId INTEGER NOT NULL,
                data FLOAT NOT NULL,
                timeStamp TIME NOT NULL,
                FOREIGN KEY (sensorId) REFERENCES Sensor(sensorId) ON DELETE CASCADE,
                FOREIGN KEY (tripId) REFERENCES Trip(tripId) ON DELETE CASCADE
            )
        ''')

        self.connection.commit()


    def addBoat(self, boat: Boat):  
        self.cursor.execute(f"INSERT INTO BOATS (boatId, boatName, boatModel, proportional, integral, differential) VALUES ('{boat.boatId}','{boat.name}','{boat.model}','{boat.proportional}','{boat.integral}','{boat.differential}')")
        self.connection.commit()
    
    def getGains(self,id: int):
        gains = {}
        self.cursor.execute(f"SELECT proportional, integral, differential FROM BOATS WHERE boatId = '{id}'")
        columns = [desc[0] for desc in self.cursor.description]
        for row in self.cursor.fetchall():
            row_dict = dict(zip(columns, row))
            gains = row_dict 
        return gains

    def getBoat(self,name: str):
        self.cursor.execute(f"SELECT * FROM BOATS WHERE boatName == '{name}'")
        row = self.cursor.fetchone()
        return row
    
    def addSensor(self, sensor: Sensor):  
        self.cursor.execute(f"INSERT INTO Sensor (sensorId, boatId, sensorName, sensorType, dataType) VALUES ('{sensor.sensorId}', '{sensor.boatId}', '{sensor.sensorName}', '{sensor.sensorModel}', 'N/A')")
        self.connection.commit()

    def getSensor(self, sensor_name: str):
        self.cursor.execute(f"SELECT * FROM Sensor WHERE sensorName == '{sensor_name}'")
        row = self.cursor.fetchone()
        return row

    def addTrip(self, trip: Trip):  
        self.cursor.execute(f"INSERT INTO Trip (tripId, boatId, timeStarted, timeEnded, dateStarted, dateEnded, distanceTravelled) VALUES ('{trip.tripId}', '{trip.boatId}', '{trip.timeStarted}', '{trip.timeEnded}', '{trip.dateStarted}', '{trip.dateEnded}', '{trip.distanceTravelled}')")
        self.connection.commit()

    def getTrip(self, trip_id: int, boat_id: int):
        self.cursor.execute(f"SELECT * FROM Trip WHERE tripId == {trip_id} AND boatId == {boat_id}")
        row = self.cursor.fetchone()
        return row

    def addReading(self, reading: Reading):  
        self.cursor.execute(f"INSERT INTO Reading (sensorId, tripId, data, timeStamp) VALUES ('{reading.sensorId}', '{reading.tripId}', '{reading.data}', '{reading.timeStamp}')")
        self.connection.commit()

    def getReading(self, sensor_id: int, trip_id: int):
        self.cursor.execute(f"SELECT * FROM Reading WHERE sensorId == {sensor_id} AND tripId == {trip_id}")
        row = self.cursor.fetchone()
        return row
    def getAllReadings(self):
        self.cursor.execute(f"SELECT * FROM Reading")
        for row in self.cursor.fetchall():
            print(row)
    def dropAllTables(self):
        self.cursor.execute(f"DROP TABLE *")
