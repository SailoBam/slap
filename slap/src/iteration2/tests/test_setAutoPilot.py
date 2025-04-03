import unittest
import json

def test_set_direction(auto_pilot):
    """Test that setDirection updates the target direction"""
    print("--------------------------------")
    print("")
    print("UNIT TEST: AutoPilot_SetDirection")
    print("\nTesting setting target direction...")
    
    # Set a new target direction
    target_direction = 90
    auto_pilot.setHeading(target_direction)
    
    # Verify direction was updated
    assert auto_pilot.target_heading == target_direction
    
    print("Target direction successfully set to", target_direction)