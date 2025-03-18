import pytest
from pathlib import Path
from unittest.mock import Mock, patch
import numpy as np
from met_viewport_utils.interfaces.gpu_font import IGPUFont
from met_viewport_utils.constants import FontStyle, FontWeight, Align
from met_viewport_utils.shape.rect import Rect

class MockGPUFont(IGPUFont):
    """Concrete implementation for testing"""
    def __init__(self):
        super().__init__()
        self.loaded_paths = []
        
    def _load_path(self):
        """Track loaded paths"""
        if self.path:
            self.loaded_paths.append(self.path)
    
    def draw(self, viewport, text, position, point_size=None, angle=None, color=None):
        """Mock draw returns consistent rect"""
        return Rect(position, [100, 20], self.align)
    
    def bounds(self, viewport, text, position, point_size=None, angle=None):
        """Mock bounds returns consistent size"""
        return Rect(position, [100, 20], self.align)

def test_gpu_font_init():
    """Test basic font initialization"""
    font = MockGPUFont()
    assert font.family == ""
    assert font.weight == FontWeight.Normal
    assert font.style == FontStyle.Normal
    assert font.align == Align.Default
    assert font.path is None
    assert font.point_size == 12
    assert font.angle == 0.0

def test_gpu_font_copy():
    """Test font copy functionality"""
    original = MockGPUFont()
    original.family = "Arial"
    original.weight = FontWeight.Bold
    original.style = FontStyle.Italic
    original.align = Align.TopLeft
    original.point_size = 24
    original.angle = 45.0
    
    copy = original.copy()
    assert copy.family == original.family
    assert copy.weight == original.weight
    assert copy.style == original.style
    assert copy.align == original.align
    assert copy.point_size == original.point_size
    assert copy.angle == original.angle

@patch('met_viewport_utils.interfaces.gpu_font._ext.font_manager.findfont')
def test_gpu_font_from_props(mock_findfont):
    """Test font creation from properties"""
    mock_path = Path("/fonts/Arial.ttf")
    mock_findfont.return_value = mock_path
    
    font = MockGPUFont.from_props("Arial", FontStyle.Normal, FontWeight.Bold)
    assert font.family == "Arial"
    assert font.style == FontStyle.Normal
    assert font.weight == FontWeight.Bold
    assert font.path == mock_path
    assert mock_path in font.loaded_paths

@patch('met_viewport_utils.interfaces.gpu_font._ext.font_manager.findfont')
def test_gpu_font_property_resolution(mock_findfont):
    """Test font path resolution when properties change"""
    mock_path = Path("/fonts/Arial.ttf")
    mock_findfont.return_value = mock_path
    
    font = MockGPUFont()
    font.family = "Arial"  # Should trigger resolution
    assert font.path == mock_path
    assert mock_path in font.loaded_paths
    
    # Change weight should re-resolve
    font.weight = FontWeight.Bold
    assert mock_findfont.call_count == 2

def test_gpu_font_draw():
    """Test font drawing functionality"""
    font = MockGPUFont()
    font.align = Align.Center
    mock_viewport = Mock()
    
    # With Center alignment (HCenter|VCenter):
    # For position [50, 50] and size [100, 20]
    # x = 50 - 100/2 = 0
    # y = 50 - 20/2 = 40
    rect = font.draw(mock_viewport, "Test", [50, 50])
    assert isinstance(rect, Rect)
    assert np.array_equal(rect.position, [0, 40])
    assert np.array_equal(rect.size, [100, 20])

def test_gpu_font_draw_align():
    """Test font drawing with different alignments"""
    font = MockGPUFont()
    mock_viewport = Mock()
    pos = [50, 50]
    
    # Test different alignments
    test_cases = [
        (Align.TopLeft, [50, 30]),     # y = 50 - 20
        (Align.TopRight, [-50, 30]),   # x = 50 - 100, y = 50 - 20
        (Align.BottomLeft, [50, 50]),  # No adjustment
        (Align.BottomRight, [-50, 50]), # x = 50 - 100
        (Align.Center, [0, 40]),       # x = 50 - 100/2, y = 50 - 20/2
    ]
    
    for align, expected_pos in test_cases:
        font.align = align
        rect = font.draw(mock_viewport, "Test", pos)
        assert np.array_equal(rect.position, expected_pos)
