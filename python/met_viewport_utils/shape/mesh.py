# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
""" Author note:
This class was a means to an end, a placeholder until I could deploy in C++
Which does not work for this project...
I don't like it, but it works for now.
in the future this will be cleaned up or at least convert the data to numpy matrices for performance
instead of lists of Vectors...
"""
from __future__ import annotations
class _ext:
    """ External Dependencies """
    from typing import List, Dict, Tuple
    import math
    from met_viewport_utils.algorithm import types
    from met_viewport_utils.constants import Align
    from met_viewport_utils.shape.rect import Rect
    from met_viewport_utils.algorithm.linear import inverse_lerp

class Mesh2D:
    """ Mesh container utility class
    
    Args:
        points(List[Vector]): positions (vec3)
        uvs(List[Vector]): uvs (vec2)
        outline_indices(List[List[int]]): optional indices representing outline
            As a mesh can have multiple outlines, 
        point_meta_data(List[Dict[str,Any]]): Optional data per point,
            this is used to pass additional information about the mesh to the shader
            eg: angle on a curve, vertex color, etc
    """
    def __init__(self,
                 points:_ext.List[_ext.types.Vector3f]=None,
                 uvs:_ext.List[_ext.types.Vector2f]=None,
                 indices:_ext.List[_ext.Tuple[int]]=None,
                 outline_indices:_ext.List[_ext.List[int]]=None,
                 point_meta_data:_ext.List[_ext.Dict]=None):
        self.points:_ext.List[_ext.types.Vector3f] = points or []
        self.uvs:_ext.List[_ext.types.Vector2f] = uvs or []
        self.indices:_ext.List[_ext.Tuple[int]] = indices or []
        self.outline_indices:_ext.List[_ext.List[int]] = outline_indices or []
        self.point_meta_data = point_meta_data or []
        self.bounds = _ext.Rect()
        # Todo: function to resolve points/uvs from indices
        # Todo: function to rotate/translate/scale mesh
    
    def outlines(self) -> _ext.List[_ext.List[_ext.types.Vector3f]]:
        """ Get the outline points if set
        
        Returns:
            List[List[Vector]]
        """
        if not self.outline_indices:
            return []
        outlines = []
        for indices in self.outline_indices:
            outlines.append([self.points[i] for i in indices])
        return outlines
    
    def compute_uvs(self, bounds:_ext.Rect=None) ->Mesh2D:
        """ Compute the uvs on this mesh
        
        Args:
            bounds(Rect): optional rect to use, defaults to current bounds.
                This is useful if your mesh is non-square
            
        Returns:
            self
        """
        if not bounds:
            self.compute_bounds()
            bounds = self.bounds
        uvs = []
        left = bounds.left()
        right = bounds.right()
        top = bounds.top()
        bottom = bounds.bottom()
        for point in self.points:
            left, point[0], right
            u = _ext.inverse_lerp(left, right, point[0])
            v = _ext.inverse_lerp(bottom, top, point[1])
            uvs.append(_ext.types.as_vector2f((u, v)))
        
        self.uvs = uvs
        return self
    
    def compute_bounds(self)->Mesh2D:
        """ Compute the bounding box on this mesh
            
        Returns:
            self
        """
        if not self.points:
            self.bounds = _ext.Rect()
            return self

        left = self.points[0][0]
        right = self.points[0][0]
        top = self.points[0][1]
        bottom = self.points[0][1]
        
        for point in self.points:
            if point[0] < left:
                left = point[0]
            if point[0] > right:
                right = point[0]
            if point[1] > top:
                top = point[1]
            if point[1] < bottom:
                bottom = point[1]
        
        self.bounds = _ext.Rect((left, bottom), (right-left, top-bottom))
        return self

    
    def translate_by(self, translation:_ext.types.Vector3fCompat) ->Mesh2D:
        """ Offset this mesh by a vector
        
        Args:
            translation(Vector)
            
        Returns:
            self
        """
        translation = _ext.types.as_vector3f(translation)
        for point in self.points:
            point += translation
        
        self.compute_bounds()
            
        return self
    
    def rotate_by(self, angle:float, pivot:_ext.Align=_ext.Align.Center) ->Mesh2D:
        """ Rotate this mesh by an angle/pivot
        
        Args:
            angle(float): radians
            pivot(Align): pivot on the bounds to rotate around
            
        Returns:
            self
        """
        if not self.bounds.is_valid():
            self.compute_bounds()
        pivot_point = self.bounds.point_at(pivot)
        return self.rotate_around(angle, pivot_point)
    
    def rotate_around(self, angle:float, pivot:_ext.types.Vector2fCompat) ->Mesh2D:
        """ Rotate this mesh around a specific vector
        
        Args:
            angle(float): radians
            pivot(Vector2f): global point to rotate around
            
        Returns:
            self
        """
        pivot = _ext.types.as_vector2f(pivot)
        angle = _ext.math.radians(angle)
        
        cos_angle = _ext.math.cos(angle)
        sin_angle = _ext.math.sin(angle)
        for point in self.points:
            rel_to_origin = point - pivot
            point[0] = pivot[0] + (rel_to_origin[0] * cos_angle - rel_to_origin[1] * sin_angle)
            point[1] = pivot[1] + (rel_to_origin[1] * cos_angle + rel_to_origin[0] * sin_angle)
            
        return self
    
    def scale_by(self, scale:_ext.types.Vector3fCompat, pivot:_ext.Align=_ext.Align.Center) ->Mesh2D:
        """ Scale this mesh by a value around a specific point
        
        Args:
            scale(Vector|float): scale value
            pivot(Align): anchor to scale from
            
        Returns:
            self
        """
        pivot = _ext.types.as_vector3f(pivot)
        if not self.bounds.is_valid():
            self.compute_bounds()
        
        pivot_point = self.bounds.point_at(pivot)
        self.scale_by(scale, pivot_point)
            
        return self
    
    def scale_by(self, scale:_ext.types.Vector3fCompat, pivot:_ext.types.Vector3fCompat) ->Mesh2D:
        """ Scale this mesh by a value around a specific point
        
        Args:
            scale(Vector|float): scale value
            pivot(Vector): global point to scale from
            
        Returns:
            self
        """
        if isinstance(scale, float):
            scale = [scale, scale, scale]
        scale = _ext.types.as_vector3f(scale)
        for i, point in enumerate(self.points):
            self.points[i] = ((point - pivot) * scale) + pivot
            
        return self
