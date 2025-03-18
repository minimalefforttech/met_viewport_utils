import pytest
import numpy as np
from unittest.mock import Mock, PropertyMock, ANY
from numpy.testing import assert_array_almost_equal
from met_viewport_utils.items.point_item import PointItem
from met_viewport_utils.constants import MouseButton, KeyboardModifier, InteractionFlags, ItemState
from met_viewport_utils.algorithm import types

class ArrayMatcher:
    """Custom matcher for numpy arrays in mock assertions"""
    def __init__(self, expected):
        self.expected = np.array(expected, dtype=np.float32)
    
    def __eq__(self, other):
        return np.allclose(self.expected, other)

class MockViewport:
    def __init__(self):
        self.world_to_screen = Mock(return_value=[100, 100])

def test_point_item_init():
    """Test point item initialization"""
    item = PointItem()
    assert not item.is2d  # 3D by default
    assert item.flags == InteractionFlags.NoInteraction
    assert item.state == (ItemState.Enabled | ItemState.Visible)
    assert np.array_equal(item.position, [0, 0, 0])

def test_point_item_properties():
    """Test point item property setters"""
    item = PointItem()
    
    # Test is2d property
    item.is2d = True
    assert item.is2d
    
    # Test position property
    item.position = [1, 2, 3]
    assert np.array_equal(item.position, [1, 2, 3])
    
    # Test flags property
    item.flags = InteractionFlags.Selectable | InteractionFlags.Draggable
    assert item.flags == (InteractionFlags.Selectable | InteractionFlags.Draggable)

def test_point_item_hierarchy():
    """Test parent-child relationships"""
    parent = PointItem()
    child1 = PointItem()
    child2 = PointItem()
    
    # Test parenting
    child1.parent = parent
    child2.parent = parent
    assert child1.parent == parent
    assert child2.parent == parent
    assert len(parent.children) == 2
    assert parent.children == [child1, child2]
    
    # Test position inheritance
    parent.position = [10, 10, 0]
    child1.position = [5, 5, 0]
    assert np.array_equal(child1.global_position(), [15, 15, 0])

def test_point_item_mouse_interaction():
    """Test basic mouse interaction without selection"""
    viewport = MockViewport()
    item = PointItem()
    item.flags = InteractionFlags.Draggable  # Only test dragging, not selection
    
    # Test hover state
    item._is_under_mouse = Mock(return_value=True)
    item.mouse_moved(viewport, [0, 0], [100, 100], KeyboardModifier.NoKeyboardModifier)
    assert item.state & ItemState.Hovered
    
    # Test dragging
    item.mouse_pressed(viewport, [0, 0], [100, 100], MouseButton.Left, KeyboardModifier.NoKeyboardModifier)
    assert item.state & ItemState.Dragging
    item.mouse_moved(viewport, [10, 10], [110, 110], KeyboardModifier.NoKeyboardModifier)
    assert np.array_equal(item.position, [10, 10, 0])  # Position should update with drag
    
    # Test drag end
    item.mouse_released(viewport, [10, 10], [110, 110], MouseButton.Left, KeyboardModifier.NoKeyboardModifier)
    assert not (item.state & ItemState.Dragging)

def test_screen_position():
    """Test screen position calculation"""
    viewport = MockViewport()
    
    # Test 2D case
    item_2d = PointItem()
    item_2d.is2d = True
    item_2d.position = [10, 20, 0]
    pos_2d = item_2d.screen_position(viewport)
    assert np.array_equal(pos_2d, [10, 20])
    
    # Test 3D case
    item_3d = PointItem()
    item_3d.position = [1, 2, 3]
    pos_3d = item_3d.screen_position(viewport)
    assert np.array_equal(pos_3d, [100, 100])  # From mock viewport
    viewport.world_to_screen.assert_called_with(ArrayMatcher([1, 2, 3]))

def test_screen_rect():
    """Test screen rect calculation"""
    viewport = MockViewport()
    item = PointItem()
    item.position = [10, 20, 0]
    
    rect = item.screen_rect(viewport)
    # Default 20x20 size centered on screen position
    assert np.array_equal(rect.position, [90, 90])  # 100,100 from mock - 10,10 for center alignment
    assert np.array_equal(rect.size, [20, 20])

def test_is_under_mouse():
    """Test mouse hit testing"""
    viewport = MockViewport()
    item = PointItem()
    
    # Point within item's rect
    assert item._is_under_mouse(viewport, [0, 0], [100, 100])
    # Point outside item's rect
    assert not item._is_under_mouse(viewport, [0, 0], [200, 200])

def test_mouse_interaction_disabled():
    """Test mouse interaction when item is disabled"""
    viewport = MockViewport()
    item = PointItem()
    item.state &= ~ItemState.Enabled
    
    # Mouse interactions should be ignored
    assert not item.mouse_pressed(viewport, [0, 0], [0, 0], MouseButton.Left, KeyboardModifier.NoKeyboardModifier)
    item.mouse_moved(viewport, [10, 10], [10, 10], KeyboardModifier.NoKeyboardModifier)
    assert not (item.state & ItemState.Hovered)
    assert not item.mouse_released(viewport, [0, 0], [0, 0], MouseButton.Left, KeyboardModifier.NoKeyboardModifier)

def test_point_item_2d_3d_mixing():
    """Test 2D/3D parent-child restrictions"""
    parent_3d = PointItem()
    parent_3d.is2d = False
    child_2d = PointItem()
    child_2d.is2d = True
    
    # Setting 2D child to 3D parent should not affect position
    child_2d.parent = parent_3d
    parent_3d.position = [10, 10, 10]
    child_2d.position = [5, 5, 0]
    
    # Global position should be local position due to dimensional mismatch
    assert np.array_equal(child_2d.global_position(), [5, 5, 0])
