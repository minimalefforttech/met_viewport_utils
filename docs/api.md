# met_viewport_utils API Documentation

A Python package for viewport HUD interaction in DCC applications (Maya, Blender, and Houdini).

For implementation examples and usage patterns, see [examples.md](examples.md).

## Algorithm Module

### color.py
- Provides color parsing and manipulation utilities
- `parse_color()`: Converts various color formats to a standardized numpy array representation

### linear.py
Provides mathematical interpolation and scaling functions:
- `lerp()`: Linear interpolation between two values
- `inverse_lerp()`: Inverse linear interpolation
- `scale_number()`: Scales a number from one range to another
- `clamp()`: Clamps a value between minimum and maximum bounds

### meta.py
Contains property decorators and metadata utilities:
- `typed_property`: Property decorator for type-checked attributes
- `alias_property`: Property decorator for creating attribute aliases

### types.py
Vector type conversion utilities:
- `as_vector2f()`: Converts compatible types to Vector2f
- `as_vector3f()`: Converts compatible types to Vector3f
- `as_vector4f()`: Converts compatible types to Vector4f

## Interfaces Module

### gpu_font.py
`IGPUFont`: Abstract interface for GPU-accelerated font rendering
- Supports font loading from files and system fonts
- Provides text drawing and bounds calculation capabilities

### gpu_shader.py
`IGPUShader`: Abstract interface for GPU shader operations
- Manages shader program state
- Handles uniform value assignment
- Controls shader drawing operations

### gpu_state.py
`IGPURestoreState`: Context manager for GPU state management
- Preserves and restores GPU shader states
- Handles state flags and parameters

### hierachy.py
`IHierarchyItem`: Base class for hierarchical scene items
- Manages parent-child relationships
- Provides tree traversal methods
- Supports hierarchy operations (append, insert, clear)

### name.py
`INameItem`: Abstract base class for named items
- Foundation for identifiable objects in the viewport

### viewport.py
`IViewport`: Abstract interface for viewport operations
- Handles coordinate space conversions
- Manages viewport rectangle
- Provides world-to-screen and screen-to-world transformations

## Items Module

### font_item.py
`FontItem`: Implementation of text rendering in the viewport
- Extends HudItem for text display
- Manages font rendering and positioning

### hud_item.py
`HudItem`: Base class for HUD elements
- Handles screen-space positioning
- Manages rectangles and transformations
- Coordinates space mapping between global and local

### point_item.py
`PointItem`: Base class for point-based items in viewport
- Handles mouse interaction
- Manages screen positioning
- Supports drag operations

## Shape Module

### generate.py
`PointTracer2d`: Utility for 2D point tracing operations
Provides shape generation functions:
- `square2d()`: Generates square mesh
- `border2d()`: Creates border mesh
- `circle2d()`: Generates circular mesh
- `arc2d()`: Creates arc mesh
- `arrow2d()`: Generates arrow mesh

### margins.py
`Margins`: Class for handling edge margins
- Supports iteration and boolean operations
- Provides inverse margin calculations

### mesh.py
`Mesh2D`: 2D mesh manipulation class
- Handles mesh transformations
- Manages UV coordinates
- Supports outline generation
- Provides translation, rotation, and scaling operations

### rect.py
`Rect`: Rectangle manipulation class
- Comprehensive rectangle operations
- Edge and corner point management
- Intersection and containment testing
- Margin adjustments
