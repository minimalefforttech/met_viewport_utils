import pytest
import math
import numpy as np
from met_viewport_utils.shape.mesh import Mesh2D
from met_viewport_utils.shape.rect import Rect
from met_viewport_utils.constants import Align
from met_viewport_utils.algorithm import types

def test_mesh_init():
    """Test basic mesh initialization"""
    # Convert inputs to numpy arrays to match actual usage
    points = [types.as_vector3f([0, 0, 0]), 
             types.as_vector3f([1, 0, 0]), 
             types.as_vector3f([1, 1, 0])]
    uvs = [types.as_vector2f([0, 0]), 
          types.as_vector2f([1, 0]), 
          types.as_vector2f([1, 1])]
    indices = [(0, 1, 2)]
    outline = [0, 1, 2, 0]
    meta = [{"test": 1}, {"test": 2}, {"test": 3}]
    
    mesh = Mesh2D(points, uvs, indices, [outline], meta)
    
    assert len(mesh.points) == 3
    assert len(mesh.uvs) == 3
    assert len(mesh.indices) == 1
    assert len(mesh.outline_indices) == 1
    assert len(mesh.point_meta_data) == 3

def test_mesh_outlines():
    """Test outline extraction"""
    points = [
        types.as_vector3f([0, 0, 0]),
        types.as_vector3f([1, 0, 0]),
        types.as_vector3f([1, 1, 0]),
        types.as_vector3f([0, 1, 0])
    ]
    outline = [0, 1, 2, 3, 0]  # Close the loop
    
    mesh = Mesh2D(points, outline_indices=[outline])
    outlines = mesh.outlines()
    
    assert len(outlines) == 1
    assert len(outlines[0]) == 5  # Including closing point
    # Verify outline order
    assert np.array_equal(outlines[0][0], [0, 0, 0])
    assert np.array_equal(outlines[0][-1], [0, 0, 0])

def test_mesh_compute_bounds():
    """Test bounds computation"""
    points = [
        types.as_vector3f([0, 0, 0]),
        types.as_vector3f([2, 0, 0]),
        types.as_vector3f([2, 1, 0]),
        types.as_vector3f([0, 1, 0])
    ]
    mesh = Mesh2D(points)
    mesh.compute_bounds()
    
    assert mesh.bounds.left() == 0
    assert mesh.bounds.right() == 2
    assert mesh.bounds.bottom() == 0
    assert mesh.bounds.top() == 1

def test_mesh_compute_uvs():
    """Test UV computation"""
    points = [
        types.as_vector3f([0, 0, 0]),
        types.as_vector3f([1, 0, 0]),
        types.as_vector3f([1, 1, 0]),
        types.as_vector3f([0, 1, 0])
    ]
    mesh = Mesh2D(points)
    mesh.compute_uvs()
    
    # Should have normalized UVs
    assert np.array_equal(mesh.uvs[0], [0, 0])  # Bottom left
    assert np.array_equal(mesh.uvs[1], [1, 0])  # Bottom right
    assert np.array_equal(mesh.uvs[2], [1, 1])  # Top right
    assert np.array_equal(mesh.uvs[3], [0, 1])  # Top left

def test_mesh_translate():
    """Test mesh translation"""
    points = [
        types.as_vector3f([0, 0, 0]),
        types.as_vector3f([1, 0, 0]),
        types.as_vector3f([1, 1, 0])
    ]
    mesh = Mesh2D(points)
    
    # Convert translation to 3D vector
    mesh.translate_by(types.as_vector3f([2, 3, 0]))
    # Check first point
    assert np.array_equal(mesh.points[0], [2, 3, 0])
    # Check bounds update
    assert mesh.bounds.left() == 2
    assert mesh.bounds.bottom() == 3

# def test_mesh_rotate():
#     """Test mesh rotation"""
#     points = [types.as_vector3f([1, 0, 0])]  # Single point, 1 unit right of origin
#     mesh = Mesh2D(points)
#     mesh.compute_bounds()  # Ensure bounds are set
    
#     # Rotate 90 degrees counter-clockwise around origin
#     mesh.rotate_around(90, types.as_vector2f([0, 0]))
#     # Point should now be at (0, 1) approximately
#     assert abs(mesh.points[0][0]) < 0.001
#     assert abs(mesh.points[0][1] - 1) < 0.001

def test_mesh_scale():
    """Test mesh scaling"""
    points = [types.as_vector3f([1, 1, 0])]  # Single point
    mesh = Mesh2D(points)
    mesh.compute_bounds()  # Ensure bounds are set
    
    # Scale by 2 around origin
    mesh.scale_by(types.as_vector3f([2, 2, 1]), types.as_vector3f([0, 0, 0]))
    # Point should now be at (2, 2)
    assert np.array_equal(mesh.points[0], [2, 2, 0])

# def test_mesh_compound_transform():
#     """Test multiple transformations"""
#     points = [types.as_vector3f([1, 0, 0])]  # Point 1 unit right of origin
#     mesh = Mesh2D(points)
#     mesh.compute_bounds()  # Ensure bounds are set
    
#     # Translate, then rotate, then scale
#     mesh.translate_by(types.as_vector3f([1, 0, 0]))  # Move to (2, 0)
#     mesh.rotate_around(90, types.as_vector2f([0, 0]))  # Rotate to (0, 2)
#     mesh.scale_by(types.as_vector3f([2, 2, 1]), types.as_vector3f([0, 0, 0]))  # Scale to (0, 4)
    
#     # Check final position
#     assert abs(mesh.points[0][0]) < 0.001
#     assert abs(mesh.points[0][1] - 4) < 0.001
