
import unittest
from slapStore import SlapStore, Boat, Sensor, Trip, Reading

class SlapStoreTest(unittest.TestCase):

    def setUp(self):
        global slapStore
        slapStore = SlapStore()

    def test_addBoat(self):
        boat = Boat(model = "tiki 26", id = 0, name = "frygga", proportional = 1, integral = 23, differential = 2)
        slapStore.addBoat(boat)
        row = slapStore.getBoat('frygga')
        self.assertEqual(row[0], 0)
        self.assertEqual(row[1], 'frygga')
        self.assertEqual(row[2], 'tiki 26')
        self.assertEqual(row[3], 1)
        self.assertEqual(row[4], 23)
        self.assertEqual(row[5], 2)

    def test_addSensor(self):
        sensor = Sensor(id = 0, boat = 0, name = "speedometer", model = "speedo1000")
        slapStore.addSensor(sensor)
        row = slapStore.getSensor('speedometer')
        self.assertEqual(row[0], 0)
        self.assertEqual(row[1], 0)
        self.assertEqual(row[2], 'speedometer')
        self.assertEqual(row[3], 'speedo1000')
    
    def test_addTrip(self):
        trip = Trip(trip_id = 0, boat_id = 0, time_started = "10:00", time_ended = "12:00", date_started = "2025-02-17", date_ended = "2025-02-17", distance_travelled = 5.5)
        slapStore.addTrip(trip)
        row = slapStore.getTrip(0, 0)
        self.assertEqual(row[0], 0)
        self.assertEqual(row[1], 0)
        self.assertEqual(row[2], "10:00")
        self.assertEqual(row[3], "12:00")
        self.assertEqual(row[4], "2025-02-17")
        self.assertEqual(row[5], "2025-02-17")
        self.assertEqual(row[6], 5.5)

    def test_addReading(self):
        reading = Reading(sensor_id = 0, trip_id = 0, data = 10.5, timestamp = "2025-02-17 10:30")
        slapStore.addReading(reading)
        row = slapStore.getReading(0, 0)
        self.assertEqual(row[0], 0)
        self.assertEqual(row[1], 0)
        self.assertEqual(row[2], 10.5)
        self.assertEqual(row[3], "2025-02-17 10:30")
    
if __name__ == '__main__':
    unittest.main()