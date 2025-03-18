# met_viewport_utils Examples

This document provides practical examples of using met_viewport_utils in various contexts.

## Basic Usage

### Point Items and Interaction

```python
from met_viewport_utils.items.point_item import PointItem
from met_viewport_utils.constants import InteractionFlags, ItemState

# Create an interactive point item
point = PointItem()
point.position = [10, 20, 0]
point.flags = InteractionFlags.Selectable | InteractionFlags.Draggable

# Create a hierarchical structure
parent = PointItem()
child = PointItem()
child.parent = parent

# Parent position affects child's global position
parent.position = [10, 10, 0]
child.position = [5, 5, 0]
child.global_position()  # Returns [15, 15, 0]

# 2D vs 3D items
item_2d = PointItem()
item_2d.is2d = True
item_2d.position = [100, 100, 0]  # Z-coordinate ignored for 2D items
```

### Shape Generation

```python
from met_viewport_utils.shape.rect import Rect
from met_viewport_utils.shape.margins import Margins
from met_viewport_utils.shape.generate import (
    square2d, border2d, circle2d, arc2d, arrow2d
)

# Create a square
rect = Rect([10, 20], [100, 50])  # Position (10,20), size (100x50)
square_mesh = square2d(rect)

# Create a border with uniform margins
border_mesh = border2d(rect, 5)  # 5px border

# Create a border with variable margins
margins = Margins(left=5, right=10, top=15, bottom=20)
complex_border = border2d(rect, margins)

# Create a circle with 32 divisions
circle_mesh = circle2d(rect, divisions=32)

# Create an arc
arc_mesh = arc2d(
    rect,
    thickness=10,
    start=0,
    end=90,
    divisions=8
)

# Create an arrow
arrow_mesh = arrow2d(
    rect,
    head_length=20,
    head_width=30,
    tail_width=10
)
```

## DCC Implementation Examples

### Basic Viewport Setup

```python
from met_viewport_utils.interfaces.viewport import IViewport
from met_viewport_utils.shape.rect import Rect

class BlenderViewport(IViewport):
    def __init__(self, region):
        self._region = region
        
    def rect(self) -> Rect:
        return Rect(
            [self._region.x, self._region.y],
            [self._region.width, self._region.height]
        )
    
    def screen_to_world(self, screen_pos, depth_point):
        # Convert screen coordinates to world space
        # Implementation specific to Blender's view3d
        pass

    def world_to_screen(self, world_pos):
        # Convert world coordinates to screen space
        # Implementation specific to Blender's view3d
        pass
```

### HUD Items

```python
from met_viewport_utils.items.hud_item import HudItem
from met_viewport_utils.items.font_item import FontItem

# Create a HUD text element
text = FontItem("Hello World", font)
text.position = [100, 100, 0]
text.is2d = True

# Create an interactive HUD button
class HUDButton(HudItem):
    def __init__(self, label: str):
        super().__init__()
        self.label = FontItem(label, font)
        self.label.parent = self
        self.flags = InteractionFlags.Selectable
    
    def mouse_pressed(self, viewport, local_pos, screen_pos, button, modifiers):
        if button == MouseButton.Left:
            self.on_click()
            return True
        return False
```

### Shape Drawing

```python
from met_viewport_utils.interfaces.gpu_shader import IGPUShader
from met_viewport_utils.shape.generate import square2d, circle2d

class BlenderShader(IGPUShader):
    def __init__(self, shader_info):
        self._shader = gpu.shader.from_builtin(shader_info)
    
    def draw(self, mesh, position, color):
        self._shader.bind()
        self._shader.uniform_float("color", color)
        
        # Draw mesh using Blender's GPU module
        batch = batch_for_shader(
            self._shader,
            'TRIS',
            {"pos": mesh.points},
            indices=mesh.indices
        )
        batch.draw(self._shader)

# Usage example
def draw_shapes(context):
    rect = Rect([10, 20], [100, 50])
    
    # Draw a square
    square = square2d(rect)
    shader = BlenderShader('UNIFORM_COLOR')
    shader.draw(square, rect.position, [1, 0, 0, 1])  # Red square
    
    # Draw a circle
    circle = circle2d(rect, divisions=32)
    shader.draw(circle, rect.position, [0, 1, 0, 1])  # Green circle
```

## Testing Examples

```python
def test_interactive_item():
    # Create a mock viewport for testing
    viewport = MockViewport()
    viewport.world_to_screen.return_value = [100, 100]
    
    # Create and test an interactive item
    item = PointItem()
    item.flags = InteractionFlags.Draggable
    item.position = [0, 0, 0]
    
    # Test mouse interaction
    item.mouse_pressed(
        viewport,
        [0, 0],  # Local position
        [100, 100],  # Screen position
        MouseButton.Left,
        KeyboardModifier.NoKeyboardModifier
    )
    assert item.state & ItemState.Dragging
    
    # Test drag movement
    item.mouse_moved(viewport, [10, 10], [110, 110], KeyboardModifier.NoKeyboardModifier)
    assert np.array_equal(item.position, [10, 10, 0])
