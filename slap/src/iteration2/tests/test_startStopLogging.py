from services.logger import Logger
from transducers.gps import Gps
from services.mapManager import MapManager
from services.slapStore import Config

def test_startStopLogging_creates_new_trip(self):
    """Test that starting and stopping logging creates a new trip"""
    # Create test components
    gps = Gps()
    map_manager = MapManager()
    logger = Logger(gps, map_manager)
    logger.setStore(self.store)

    # Start logging
    logger.start(Config(0, 'default', 0, 0, 0))
    assert logger.running == True

    # Stop logging 
    logger.stop()
    assert logger.running == False

    # Verify a new trip was created in the database
    self.store.cursor.execute("SELECT COUNT(*) FROM Trip")
    trip_count = self.store.cursor.fetchone()[0]
    assert trip_count == 1

