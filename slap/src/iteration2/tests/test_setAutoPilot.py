from control.autoPilot import AutoPilot
from web.app import WebServer
from services.logger import Logger
from services.mapManager import MapManager
from transducers.gps import Gps
from services.slapStore import SlapStore
import unittest
import json

def test_set_direction(self):
    print("\nTesting setDirection endpoint...")

    # Create test client and make request
    self.auto_pilot = AutoPilot()
    self.logger = Logger(Gps(), MapManager())
    self.web_server = WebServer(self.auto_pilot, self.logger)
    app = self.web_server.create_server(self.store)
    self.client = app.test_client()
    response = self.client.put('/api/setDirection', data='180')
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertEqual(data['angle'], '180')
    self.assertEqual(self.auto_pilot.getHeadings()['target'], 180)

    response = self.client.put('/api/setDirection', data='90')
    self.assertEqual(response.status_code, 200)
    data = json.loads(response.data)
    self.assertEqual(data['angle'], '90')
    self.assertEqual(self.auto_pilot.getHeadings()['target'], 90)
    
    print("Valid heading tests passed")



