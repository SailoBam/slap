from control.autoPilot import AutoPilot

def test_adjust_target_angle(self):
    """Test that the +/-10 buttons correctly adjust the target angle"""
    # Create test autopilot with initial target angle of 0
    auto_pilot = AutoPilot()
    auto_pilot.setHeading(0)
    
    # Test +10 button
    heading = auto_pilot.setHeading(auto_pilot.target_heading + 10)
    assert heading == 10
    
    # Test -10 button
    heading = auto_pilot.setHeading(auto_pilot.target_heading - 10) 
    assert heading == 0

