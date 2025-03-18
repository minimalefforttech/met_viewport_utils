import pytest
import numpy as np
from met_viewport_utils.interfaces.viewport import IViewport
from met_viewport_utils.shape.rect import Rect
from met_viewport_utils.algorithm import types

class MockViewport(IViewport):
    """Mock viewport implementation for testing"""
    def __init__(self, size=(800, 600)):
        self._size = size
        
    def rect(self) -> Rect:
        return Rect([0, 0], self._size)
    
    def screen_to_world(self, screen_position, depth_point):
        """Simple screen to world conversion for testing"""
        # Mock a basic perspective projection
        screen_x = (screen_position[0] / self._size[0]) * 2 - 1
        screen_y = (screen_position[1] / self._size[1]) * 2 - 1
        # Project to depth point's Z
        return types.as_vector3f([
            screen_x * depth_point[2],
            screen_y * depth_point[2],
            depth_point[2]
        ])
    
    def screen_to_ray(self, screen_position):
        """Simple ray computation for testing"""
        screen_x = (screen_position[0] / self._size[0]) * 2 - 1
        screen_y = (screen_position[1] / self._size[1]) * 2 - 1
        # Mock orthographic rays (parallel)
        origin = types.as_vector3f([screen_x, screen_y, -10])
        direction = types.as_vector3f([0, 0, 1])  # Looking down Z
        return origin, direction
    
    def world_to_screen(self, world_position):
        """Simple world to screen conversion for testing"""
        # Mock a basic perspective projection
        if world_position[2] != 0:
            screen_x = (world_position[0] / world_position[2] + 1) * self._size[0] / 2
            screen_y = (world_position[1] / world_position[2] + 1) * self._size[1] / 2
        else:
            screen_x = (world_position[0] + 1) * self._size[0] / 2
            screen_y = (world_position[1] + 1) * self._size[1] / 2
        return types.as_vector2f([screen_x, screen_y])

def test_viewport_rect():
    """Test viewport rect access"""
    viewport = MockViewport(size=(800, 600))
    rect = viewport.rect()
    
    assert isinstance(rect, Rect)
    assert np.array_equal(rect.size, [800, 600])
    assert np.array_equal(rect.position, [0, 0])

def test_screen_to_world():
    """Test screen to world conversion"""
    viewport = MockViewport(size=(800, 600))
    screen_pos = [400, 300]  # Center of screen
    depth_point = [0, 0, 10]  # 10 units away
    
    world_pos = viewport.screen_to_world(screen_pos, depth_point)
    assert isinstance(world_pos, np.ndarray)
    # At center of screen, x and y should be near 0
    assert abs(world_pos[0]) < 0.001
    assert abs(world_pos[1]) < 0.001
    assert world_pos[2] == 10

def test_screen_to_ray():
    """Test screen to ray conversion"""
    viewport = MockViewport(size=(800, 600))
    screen_pos = [400, 300]  # Center of screen
    
    origin, direction = viewport.screen_to_ray(screen_pos)
    assert isinstance(origin, np.ndarray)
    assert isinstance(direction, np.ndarray)
    # At center of screen, x and y should be near 0
    assert abs(origin[0]) < 0.001
    assert abs(origin[1]) < 0.001
    # Direction should be normalized and pointing down Z
    assert np.array_equal(direction, [0, 0, 1])

def test_world_to_screen():
    """Test world to screen conversion"""
    viewport = MockViewport(size=(800, 600))
    world_pos = [0, 0, 10]  # Center, 10 units away
    
    screen_pos = viewport.world_to_screen(world_pos)
    assert isinstance(screen_pos, np.ndarray)
    # Should project to center of screen
    assert abs(screen_pos[0] - 400) < 0.001
    assert abs(screen_pos[1] - 300) < 0.001

def test_coordinate_round_trip():
    """Test converting from screen to world and back"""
    viewport = MockViewport(size=(800, 600))
    original_screen = [400, 300]
    depth_point = [0, 0, 10]
    
    # Convert screen to world
    world_pos = viewport.screen_to_world(original_screen, depth_point)
    # Convert world back to screen
    final_screen = viewport.world_to_screen(world_pos)
    
    # Should get back close to original screen coordinates
    assert abs(final_screen[0] - original_screen[0]) < 0.001
    assert abs(final_screen[1] - original_screen[1]) < 0.001
