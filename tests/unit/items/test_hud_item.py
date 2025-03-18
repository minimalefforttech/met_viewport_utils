import pytest
import numpy as np
from unittest.mock import Mock
from met_viewport_utils.items.hud_item import HudItem
from met_viewport_utils.shape.rect import Rect
from met_viewport_utils.shape.margins import Margins
from met_viewport_utils.constants import Align, ItemState
from met_viewport_utils.algorithm import types

class MockViewport:
    def __init__(self):
        self.world_to_screen = Mock(return_value=[0, 0])

def test_hud_item_init():
    """Test HudItem initialization"""
    item = HudItem()
    assert item.is2d  # Should be true for HUD items
    assert item.align == Align.Center
    assert isinstance(item.margins, Margins)
    assert np.array_equal(item.size, [0, 0])
    assert item.state & ItemState.Enabled
    assert item.state & ItemState.Visible

def test_hud_item_properties():
    """Test HudItem property setters"""
    item = HudItem()
    
    # Test align property
    item.align = Align.TopLeft
    assert item.align == Align.TopLeft
    
    # Test margins property
    new_margins = Margins(left=10, right=20, top=30, bottom=40)
    item.margins = new_margins
    assert item.margins.left == 10
    assert item.margins.right == 20
    assert item.margins.top == 30
    assert item.margins.bottom == 40
    
    # Test size property
    item.size = [100, 50]
    assert np.array_equal(item.size, [100, 50])

def test_hud_item_local_rect():
    """Test local rect calculation"""
    item = HudItem()
    item.position = [10, 20, 0]
    item.size = [100, 50]
    item.align = Align.BottomLeft  # Use BottomLeft to avoid position adjustments
    
    rect = item.local_rect()
    assert isinstance(rect, Rect)
    assert np.array_equal(rect.position, [10, 20])
    assert np.array_equal(rect.size, [100, 50])

def test_hud_item_with_parent():
    """Test HUD item with parent"""
    parent = HudItem()
    parent.position = [100, 100, 0]
    parent.size = [200, 200]
    parent.align = Align.BottomLeft
    
    child = HudItem()
    child.position = [50, 50, 0]
    child.size = [50, 50]
    child.align = Align.BottomLeft
    child.parent = parent
    
    # Test global position calculation
    global_pos = child.global_position()
    assert np.array_equal(global_pos[:2], [150, 150])  # Simple addition with BottomLeft align
    
    # Test global rect calculation
    global_rect = child.global_rect()
    assert np.array_equal(global_rect.position, [150, 150])
    assert np.array_equal(global_rect.size, [50, 50])

def test_screen_rect():
    """Test screen rect calculation"""
    item = HudItem()
    item.position = [10, 20, 0]
    item.size = [100, 50]
    
    viewport = MockViewport()
    rect = item.screen_rect(viewport)
    assert isinstance(rect, Rect)
    assert np.array_equal(rect.position, [10, 20])
    assert np.array_equal(rect.size, [100, 50])

def test_global_position_no_parent():
    """Test global position calculation with no parent"""
    item = HudItem()
    item.position = [10, 20, 0]
    
    pos = item.global_position()
    assert np.array_equal(pos, [10, 20, 0])

def test_global_position_non_hud_parent():
    """Test global position with non-HUD parent"""
    from met_viewport_utils.items.point_item import PointItem
    
    parent = PointItem()  # Not a HUD item
    parent.position = [100, 100, 0]
    parent.is2d = True  # Make it 2D compatible
    
    child = HudItem()
    child.position = [10, 20, 0]
    child.parent = parent
    
    pos = child.global_position()
    assert np.array_equal(pos, [110, 120, 0])

def test_global_position_2d_3d_mismatch():
    """Test global position with 2D/3D mismatch"""
    parent = HudItem()
    parent.position = [100, 100, 0]
    parent.is2d = False  # Make it 3D
    
    child = HudItem()
    child.position = [10, 20, 0]
    child.parent = parent
    
    pos = child.global_position()
    assert np.array_equal(pos, [10, 20, 0])  # Should return local position

def test_map_from_global_vector():
    """Test mapping a global vector to local space"""
    item = HudItem()
    item.position = [100, 100, 0]
    
    local_pos = item.map_from_global(types.as_vector2f([150, 150]))
    assert isinstance(local_pos, np.ndarray)
    # Local position is calculated relative to the local rect first
    local_rect = item.local_rect()
    rect_pos = local_rect.position + types.as_vector2f([150, 150])
    assert np.array_equal(local_pos, rect_pos)

def test_map_from_global_no_parent():
    """Test mapping from global with no parent"""
    item = HudItem()
    rect = Rect([10, 10], [50, 50])
    
    local_rect = item.map_from_global(rect)
    assert np.array_equal(local_rect.position, rect.position)
    assert np.array_equal(local_rect.size, rect.size)

def test_map_to_global_vector():
    """Test mapping a local vector to global space"""
    parent = HudItem()
    parent.position = [100, 100, 0]
    parent.size = [200, 200]
    
    child = HudItem()
    child.parent = parent
    child.align = Align.TopLeft
    
    global_pos = child.map_to_global(types.as_vector2f([50, 50]))
    assert isinstance(global_pos, np.ndarray)
    # Position should be relative to parent's position plus alignment
    # Global position is calculated using parent's rect + alignment + local position
    parent_rect = parent.global_rect()
    pivot = parent_rect.point_at(child.align)
    local_rect = child.local_rect()
    expected_pos = pivot + local_rect.position + types.as_vector2f([50, 50])
    assert np.array_equal(global_pos[:2], expected_pos[:2])

def test_map_to_global_no_parent():
    """Test mapping to global with no parent"""
    item = HudItem()
    rect = Rect([10, 10], [50, 50])
    
    global_rect = item.map_to_global(rect)
    assert np.array_equal(global_rect.position, rect.position)
    assert np.array_equal(global_rect.size, rect.size)

def test_map_to_global_different_alignments():
    """Test mapping to global with different alignments"""
    parent = HudItem()
    parent.position = [100, 100, 0]
    parent.size = [200, 200]
    
    child = HudItem()
    child.parent = parent
    child.size = [50, 50]
    
    # Test Center alignment
    child.align = Align.Center
    global_rect = child.map_to_global(Rect([0, 0], [10, 10]))
    # Center alignment: parent center + rect offset
    parent_rect = parent.global_rect()
    pivot = parent_rect.point_at(Align.Center)
    expected = pivot + Rect([0, 0], [10, 10], Align.Center).position
    assert np.array_equal(global_rect.position, expected)
    
    # Test TopRight alignment
    child.align = Align.TopRight
    global_rect = child.map_to_global(Rect([0, 0], [10, 10]))
    # TopRight alignment: parent top-right + rect offset
    parent_rect = parent.global_rect()
    pivot = parent_rect.point_at(Align.TopRight)
    expected = pivot + Rect([0, 0], [10, 10], Align.TopRight).position
    assert np.array_equal(global_rect.position, expected)

def test_hud_item_with_margins():
    """Test HUD item with margins"""
    parent = HudItem()
    parent.position = [0, 0, 0]
    parent.size = [200, 200]
    parent.align = Align.BottomLeft
    parent.margins = Margins(left=10, right=10, top=10, bottom=10)  # 10px margin all around
    
    child = HudItem()
    child.parent = parent
    child.size = [50, 50]
    child.align = Align.BottomLeft
    
    # Parent rect should be adjusted by margins
    parent_rect = child.parent_rect()
    assert np.array_equal(parent_rect.position, [10, 10])  # Offset by margins
    assert np.array_equal(parent_rect.size, [180, 180])  # Size reduced by margins
