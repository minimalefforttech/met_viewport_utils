from met_viewport_utils.algorithm import linear

def test_lerp_basic():
    """Test basic linear interpolation"""
    assert linear.lerp(0, 1, 0.5) == 0.5
    assert linear.lerp(0, 10, 0.5) == 5.0
    assert linear.lerp(-10, 10, 0.5) == 0.0

def test_lerp_bounds():
    """Test lerp at bounds"""
    assert linear.lerp(0, 1, 0.0) == 0.0
    assert linear.lerp(0, 1, 1.0) == 1.0

def test_inverse_lerp_basic():
    """Test basic inverse lerp"""
    assert linear.inverse_lerp(0, 10, 5) == 0.5
    assert linear.inverse_lerp(-10, 10, 0) == 0.5
    assert linear.inverse_lerp(0, 100, 25) == 0.25

def test_inverse_lerp_edge_cases():
    """Test inverse lerp with edge cases"""
    assert linear.inverse_lerp(5, 5, 5) == 0.0  # When a == b
    assert linear.inverse_lerp(0, 10, 0) == 0.0  # At minimum
    assert linear.inverse_lerp(0, 10, 10) == 1.0  # At maximum

def test_scale_number_basic():
    """Test basic number scaling"""
    # Scale from 0-10 to 0-1
    assert linear.scale_number(5, 0, 10) == 0.5
    # Scale from 0-10 to 0-100
    assert linear.scale_number(5, 0, 10, 0, 100) == 50.0
    # Scale from -10-10 to 0-1
    assert linear.scale_number(0, -10, 10, 0, 1) == 0.5

def test_scale_number_edge_cases():
    """Test scale_number with edge cases"""
    # Same input range
    assert linear.scale_number(5, 5, 5) == 0.0
    # At bounds
    assert linear.scale_number(0, 0, 10) == 0.0
    assert linear.scale_number(10, 0, 10) == 1.0
    # Custom output range
    assert linear.scale_number(5, 0, 10, 100, 200) == 150.0

def test_clamp_basic():
    """Test basic value clamping"""
    assert linear.clamp(5, 0, 10) == 5  # Within range
    assert linear.clamp(-5, 0, 10) == 0  # Below min
    assert linear.clamp(15, 0, 10) == 10  # Above max

def test_clamp_edge_cases():
    """Test clamp with edge cases"""
    assert linear.clamp(0, 0, 10) == 0  # At min
    assert linear.clamp(10, 0, 10) == 10  # At max
    assert linear.clamp(5, 5, 5) == 5  # Same min/max
    assert linear.clamp(-5, -10, 0) == -5  # Negative range
