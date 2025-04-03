import unittest
from unittest.mock import patch
from control.autoPilot import AutoPilot
from transducers.tillerActuator import TillerActuator
    
def test_start_runs_update(self):
    print("--------------------------------")
    print("")
    print("UNIT TEST: AutoPilot_StartStop")
    print("\nTesting starting and stopping the autopilot...")
    
    with patch.object(AutoPilot, 'update') as mock_update:
        # Start the autopilot
        self.auto_pilot.start()
        
        # Check update was called
        mock_update.assert_called()
        
        # Stop the autopilot thread
        self.auto_pilot.stop()

