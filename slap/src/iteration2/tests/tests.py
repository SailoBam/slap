import unittest
import os
import sqlite3
import sys
from tests.test_defaultConfig import test_getCurrentConfig_creates_default_when_none_exists
from tests.test_createConfig import test_createConfig_creates_new_config
from tests.test_editConfig import test_editConfig_updates_existing_config
from tests.test_deleteConfig import test_deleteConfig_removes_existing_config
from tests.test_startStopAutoPilot import test_start_runs_update
from tests.test_adjustAutoPilot import test_adjust_target_angle
from services.slapStore import SlapStore, Config
from tests.test_startStopLogging import test_startStopLogging_creates_new_trip
from tests.test_setAutoPilot import test_set_direction
from control.autoPilot import AutoPilot

class Test(unittest.TestCase):
    def setUp(self):
        """Set up a test database before each test"""
        self.test_db = ":memory:"
        self.store = SlapStore(self.test_db)
        # Create new connection to test database
        self.store.connection = sqlite3.connect(self.test_db, check_same_thread=False)
        self.store.connection.row_factory = sqlite3.Row
        self.store.cursor = self.store.connection.cursor()
        
        # Config table
        self.store.cursor.execute('''
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
        self.store.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sensor (
                sensorId INTEGER PRIMARY KEY,
                configId INTEGER NOT NULL,
                sensorName TEXT NOT NULL,
                sensorType TEXT NOT NULL,
                dataType TEXT NOT NULL,
                FOREIGN KEY (configId) REFERENCES CONFIGS(configId) ON DELETE CASCADE
            )
        ''')

        # Trip table
        self.store.cursor.execute('''
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
        self.store.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Readings (
                sensorId INTEGER NOT NULL,
                tripId INTEGER NOT NULL,
                data TEXT NOT NULL,
                timeStamp TIME NOT NULL,
                FOREIGN KEY (sensorId) REFERENCES Sensor(sensorId) ON DELETE CASCADE,
                FOREIGN KEY (tripId) REFERENCES Trip(tripId) ON DELETE CASCADE
            )
        ''')

        self.store.connection.commit()

    def tearDown(self):
        """Clean up after each test"""
        self.store.connection.close()
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_defaultConfig(self):
        test_getCurrentConfig_creates_default_when_none_exists(self)

    def test_createConfig(self):
        test_createConfig_creates_new_config(self)
        
    def test_editConfig(self):
        test_editConfig_updates_existing_config(self)

    def test_deleteConfig(self):
        test_deleteConfig_removes_existing_config(self)

    def test_toggleAutoPilot(self):
        #teststartStopAutoPilot(self)
        print("test start stop auto pilot")
        
    def test_adjustAutoPilot(self):
        test_adjust_target_angle(self)

    def test_loggerStartStop(self):
        test_startStopLogging_creates_new_trip(self)
        
    def test_setAutoPilot(self):
        self.auto_pilot = AutoPilot()
        test_set_direction(self.auto_pilot)

if __name__ == '__main__':
    unittest.main() 