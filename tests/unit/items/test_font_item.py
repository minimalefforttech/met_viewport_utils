import pytest
from unittest.mock import Mock, call
import numpy as np
from met_viewport_utils.items import font_item
from met_viewport_utils.shape.rect import Rect
from met_viewport_utils.algorithm import types
from met_viewport_utils.constants import Align

class MockGPUFont:
    def __init__(self, align=None):
        self.align = align or Align.BottomLeft
        self.draw = Mock(return_value=Rect([0, 0], [100, 20], self.align))
    
    def copy(self):
        return MockGPUFont(self.align)

class MockViewport:
    def __init__(self):
        pass

def test_font_item_init():
    """Test font item initialization"""
    font = MockGPUFont()
    item = font_item.FontItem("Hello", font)
    assert item.text == "Hello"
    assert isinstance(item.font, MockGPUFont)
    assert item.data == {}

def test_font_item_text_property():
    """Test text property handling"""
    font = MockGPUFont()
    item = font_item.FontItem("Initial", font)
    item.text = "Updated"
    assert item.text == "Updated"
    # Should enforce string type
    item.text = 42
    assert item.text == "42"

def test_font_item_global_rect():
    """Test global rect calculation"""
    font = MockGPUFont(align=Align.Right)  # Right aligned
    item = font_item.FontItem("Test", font)
    item.size = types.as_vector2f([100, 20])
    
    # Mock position to [10, 10]
    item.global_position = Mock(return_value=[10, 10])
    
    rect = item.global_rect()
    assert isinstance(rect, Rect)
    # With Right alignment, x position is adjusted by subtracting width
    assert np.array_equal(rect.position, [-90, 10])
    assert np.array_equal(rect.size, [100, 20])

def test_font_item_draw():
    """Test draw with format data"""
    font = MockGPUFont()
    item = font_item.FontItem("Hello {name}!", font)
    item.data = {"name": "World"}
    
    # Mock screen position calculation
    item.screen_position = Mock(return_value=[50, 50])
    
    viewport = MockViewport()
    item.draw(viewport)
    
    # Verify font.draw was called with formatted text
    item.font.draw.assert_called_once_with("Hello World!", [50, 50])
    # Verify size was updated from rect returned by font.draw
    assert np.array_equal(item.size, [100, 20])
