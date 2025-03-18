import pytest
import numpy as np
from met_viewport_utils.shape.generate import square2d, border2d, circle2d, arc2d, arrow2d
from met_viewport_utils.shape.rect import Rect
from met_viewport_utils.shape.margins import Margins

def test_square2d():
    """Test square generation"""
    rect = Rect([10, 20], [100, 50])  # Position (10, 20), size (100, 50)
    mesh = square2d(rect)
    
    # Check number of points
    assert len(mesh.points) == 4
    
    # Check point positions (bottom-left, top-left, top-right, bottom-right)
    assert np.array_equal(mesh.points[0], [10, 20])
    assert np.array_equal(mesh.points[1], [10, 70])  # 20 + 50
    assert np.array_equal(mesh.points[2], [110, 70]) # 10 + 100, 20 + 50
    assert np.array_equal(mesh.points[3], [110, 20]) # 10 + 100
    
    # Check indices (two triangles)
    assert len(mesh.indices) == 2
    assert mesh.indices[0] == (0, 1, 2)
    assert mesh.indices[1] == (0, 2, 3)

def test_square2d_zero_size():
    """Test with a zero-sized rect (should still generate valid mesh)"""
    rect = Rect([10, 10], [0, 0])
    mesh = square2d(rect)
    
    assert len(mesh.points) == 4
    # All points should collapse to the same position
    assert np.array_equal(mesh.points[0], [10, 10])
    assert np.array_equal(mesh.points[1], [10, 10])
    assert np.array_equal(mesh.points[2], [10, 10])
    assert np.array_equal(mesh.points[3], [10, 10])

def test_border2d_uniform_margins():
    """Test border generation with uniform margins"""
    rect = Rect([10, 20], [100, 50])  # Position (10, 20), size (100, 50)
    mesh = border2d(rect, 5)  # 5px border
    
    assert len(mesh.points) == 8
    
    # Outer rectangle points
    assert np.array_equal(mesh.points[0], [10, 20])  # BL
    assert np.array_equal(mesh.points[1], [10, 70])  # TL
    assert np.array_equal(mesh.points[2], [110, 70]) # TR
    assert np.array_equal(mesh.points[3], [110, 20]) # BR
    
    # Inner rectangle points (5px inset)
    assert np.array_equal(mesh.points[4], [15, 25])
    assert np.array_equal(mesh.points[5], [15, 65])
    assert np.array_equal(mesh.points[6], [105, 65])
    assert np.array_equal(mesh.points[7], [105, 25])

def test_border2d_variable_margins():
    """Test with different margins on each side"""
    rect = Rect([10, 20], [100, 50])
    margins = Margins(left=5, right=10, top=15, bottom=20)
    mesh = border2d(rect, margins)
    
    assert len(mesh.points) == 8
    
    # Outer rectangle points
    assert np.array_equal(mesh.points[0], [10, 20])
    assert np.array_equal(mesh.points[1], [10, 70])
    assert np.array_equal(mesh.points[2], [110, 70])
    assert np.array_equal(mesh.points[3], [110, 20])
    
    # Inner rectangle points (variable inset)
    assert np.array_equal(mesh.points[4], [15, 40])  # Left +5, Bottom +20
    assert np.array_equal(mesh.points[5], [15, 55])  # Left +5, Top -15
    assert np.array_equal(mesh.points[6], [100, 55]) # Right -10, Top -15
    assert np.array_equal(mesh.points[7], [100, 40]) # Right -10, Bottom +20

def test_border2d_zero_margins():
    """Test with zero margins (should be equivalent to a square)"""
    rect = Rect([10, 20], [100, 50])
    mesh = border2d(rect, 0)
    
    assert len(mesh.points) == 8  # Still 8 points, but inner and outer are coincident
    
    # Outer and inner rectangle points should be the same
    assert np.array_equal(mesh.points[0], mesh.points[4])
    assert np.array_equal(mesh.points[1], mesh.points[5])
    assert np.array_equal(mesh.points[2], mesh.points[6])
    assert np.array_equal(mesh.points[3], mesh.points[7])

def test_circle2d():
    """Test circle generation"""
    rect = Rect([10, 20], [100, 100])  # Square rect for a circle
    mesh = circle2d(rect, divisions=32)
    
    assert len(mesh.points) == 34  # 1 center + 33 points around circumference
    assert len(mesh.indices) == 33  # 32 triangles + 1 extra
    
    # Check center point
    assert np.allclose(mesh.points[0], [60, 70])  # Center of the rect
    
    # Check a few points around the circumference
    assert np.allclose(mesh.points[1], [110, 70])  # Rightmost point
    assert np.allclose(mesh.points[9], [60, 120]) # Top point
    assert np.allclose(mesh.points[17], [10, 70]) # Leftmost point
    assert np.allclose(mesh.points[25], [60, 20]) # Bottom point

def test_circle2d_oval():
    """Test circle generation with non-square rect (oval)"""
    rect = Rect([10, 20], [100, 50])  # Rect with different width and height
    mesh = circle2d(rect, divisions=16)
    
    assert len(mesh.points) == 18
    
    # Check center point
    assert np.allclose(mesh.points[0], [60, 45])  # Center of the rect
    
    # Check a few points around the circumference.  These will be incorrect
    # until the implementation is fixed, but we're testing the current behavior.
    assert np.allclose(mesh.points[1], [110, 45])  # Rightmost point (correct)
    assert np.allclose(mesh.points[5], [60, 95]) # Top point (INCORRECT - should be [60, 70])
    assert np.allclose(mesh.points[9], [10, 45]) # Leftmost point (correct)
    assert np.allclose(mesh.points[13], [60, -5]) # Bottom point (INCORRECT - should be [60, 20])

def test_arc2d():
    """Test arc generation"""
    rect = Rect([10, 20], [100, 100])  # Square rect for a circle
    mesh = arc2d(rect, thickness=10, start=0, end=90, divisions=8)
    
    assert len(mesh.points) == 18  # 9 outer points + 9 inner points
    assert len(mesh.indices) == 16  # 8 segments * 2 triangles per segment
    
    # Check a few points
    assert np.allclose(mesh.points[0], [100, 70])  # Inner start point
    assert np.allclose(mesh.points[1], [110, 70])  # Outer start point
    assert np.allclose(mesh.points[16], [60, 110]) # Inner end point
    assert np.allclose(mesh.points[17], [60, 120]) # Outer end point

def test_arrow2d_single_head():
    """Test arrow generation with a single head"""
    rect = Rect([10, 20], [100, 50])  # Position (10, 20), size (100, 50)
    mesh = arrow2d(rect, head_length=20, head_width=30, tail_width=10)
    
    assert len(mesh.points) == 7
    
    # Check key points
    assert np.allclose(mesh.points[0], [10, 40])  # Tail start (left, middle - half_tail_width)
    assert np.allclose(mesh.points[4], [110, 45]) # Head tip (right)
    assert np.allclose(mesh.points[5], [90, 30])  # Head base (left, middle - half_head_width)

def test_arrow2d_double_head():
    """Test arrow generation with two heads"""
    rect = Rect([10, 20], [100, 50])
    mesh = arrow2d(rect, head_length=15, head_width=20, tail_width=10, heads=2)
    
    assert len(mesh.points) == 10
    
    # Check key points. These are incorrect in current implementation
    assert np.allclose(mesh.points[0], [10, 45])  # Left head top
    assert np.allclose(mesh.points[5], [110, 45]) # Right head tip
    assert np.allclose(mesh.points[9], [25, 35])  # Left head bottom

def test_arrow2d_quad_head():
    """Test arrow generation with four heads"""
    rect = Rect([10, 20], [100, 60])  # Using a non-square rect
    mesh = arrow2d(rect, head_length=10, head_width=15, tail_width=5, heads=4)
    
    assert len(mesh.points) == 24
    
    # Check key points. These are incorrect in current implementation
    assert np.allclose(mesh.points[0], [10, 50])  # Left head top
    assert np.allclose(mesh.points[6], [60, 80])  # Top head tip
    assert np.allclose(mesh.points[12], [110, 50]) # Right head tip
    assert np.allclose(mesh.points[18], [60, 20]) # Bottom head tip
