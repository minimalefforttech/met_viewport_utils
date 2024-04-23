# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
"""Generate some simple shapes
"""
from __future__ import annotations
class _ext:
    """ External Dependencies """
    from typing import Union
    import math
    from met_viewport_utils.shape.mesh import Mesh2D
    from met_viewport_utils.shape.rect import Rect
    from met_viewport_utils.shape.margins import Margins
    from met_viewport_utils.algorithm.meta import (
        typed_property,
        alias_property)
    from met_viewport_utils.algorithm import types


class PointTracer2d(object):
    """ Simple tracer to draw shapes
    Keeps track of reference points
    
    Properties:
        position(Vector): The current position, readonly
    
    Args:
        position(Vector): optional starting position
    """
    def __init__(self, position:_ext.types.Vector2fCompat=None):
        if position is not None:
            self.position = position
        self._refs = {}
        # todo: arcs/divisions
        # todo: keep track of points as a path
        
    position = _ext.typed_property(_ext.types.Vector2f, default=[0, 0], converter=_ext.types.as_vector2f)
    x = _ext.alias_property(position, "x")
    y = _ext.alias_property(position, "y")
    
    def move_to(self, position:_ext.types.Vector2fCompat, ref:str=None)->_ext.types.Vector2fCompat:
        """ Move to a position, optionally set a reference point
        
        Args:
            position(Vector)
            ref(str|None): Optional reference to jump back to this point
        
        Returns:
            self
        """
        self.position = _ext.types.as_vector2f(position)
        if ref:
            self._refs[ref] = _ext.types.as_vector2f(self.position)
        return self.position
    
    def move_by(self, offset:_ext.types.Vector2fCompat, ref:str=None)->_ext.types.Vector2fCompat:
        """ moves by an offset, optionally set a reference point
        
        Args:
            offset(Vector)
            ref(str|None): Optional reference to jump back to this point
        
        Returns:
            self
        """
        self.position = self.position + _ext.types.as_vector2f(offset)
        if ref:
            self._refs[ref] = _ext.types.as_vector2f(self.position)
        return self.position
    
    def ref(self, name:str)->_ext.types.Vector2fCompat:
        """Get a position for this reference

        Args:
            name (str): reference to find

        Returns:
            Vector2f: position
        
        Raises:
            KeyError: if name is not found
        """
        # Throws KeyError on invalid name
        return self._refs[name]


def square2d(rect:_ext.Rect) ->_ext.Mesh2D:
    """ Generate a square inside a rect
    
    Args:
        rect(Rect)
    
    Returns:
        Mesh
    """
    points = [
        rect.bottom_left(), rect.top_left(), rect.top_right(), rect.bottom_right()
    ]
    uvs = [
        _ext.types.as_vector2f((0, 0)),
        _ext.types.as_vector2f((0, 1)),
        _ext.types.as_vector2f((1, 1)),
        _ext.types.as_vector2f((1, 0)),
    ]
    indices = [
        (0, 1, 2), (0, 2, 3)
    ]
    outline = [
        0, 1, 2, 3, 0
    ]
    return _ext.Mesh2D(points, uvs, indices, [outline])

def border2d(rect:_ext.Rect, margins:_ext.Union[float, int, _ext.Margins]) ->_ext.Mesh2D:
    """ Generate a border inside a rect with thickness determined by margins
    
    Args:
        rect(Rect)
    
    Returns:
        Mesh
    """
    if isinstance(margins, (float, int)):
        margins = _ext.Margins(margins, margins, margins, margins)
    
    inner = rect.adjusted(margins)
    points = [
        rect.bottom_left(),
        rect.top_left(),
        rect.top_right(),
        rect.bottom_right(),
        
        inner.bottom_left(),
        inner.top_left(),
        inner.top_right(),
        inner.bottom_right(),
    ]
    point_meta_data = [
        {"inner": False},
        {"inner": False},
        {"inner": False},
        {"inner": False},

        {"inner": True},
        {"inner": True},
        {"inner": True},
        {"inner": True},
    ]
    # Index mapping shortcodes
    bl, tl, tr, br, bl_inner, tl_inner, tr_inner, br_inner = range(len(points))
    indices = []
    if margins.left:
        indices += [
            (bl, bl_inner, tl),
            (tl, tl_inner, bl_inner)
        ]
    if margins.top:
        indices += [
            (tl, tl_inner, tr),
            (tr, tl_inner, tr_inner)
        ]
    if margins.right:
        indices += [
            (tr, tr_inner, br),
            (br, tr_inner, br_inner)
        ]
    if margins.bottom:
        indices += [
            (br, br_inner, bl),
            (bl, br_inner, bl_inner)
        ]
    # todo: outline
    return _ext.Mesh2D(points, indices=indices, point_meta_data=point_meta_data)


def circle2d(rect:_ext.Rect, divisions:int=32) ->_ext.Mesh2D:
    """ Generate a circle/oval inside a rect
    
    Args:
        rect(Rect)
        divisions(int)
    
    Returns:
        Mesh
    """
    center = rect.center()
    radius = rect.width / 2.0
    increment = _ext.math.radians(360.0 / divisions)
    points = [center]
    indices = []
    point_meta_data = [{"angle": 0.0, "center": True}]
    
    for i in range(divisions+1):
        angle = i * increment
        x = center[0] + radius * _ext.math.cos(angle)
        y = center[1] + radius * _ext.math.sin(angle)
        points.append(_ext.types.as_vector2f((x, y)))
        point_meta_data.append({"angle": angle, "center": False})
        if i > 0:
            indices.append((0, i-1, i))
            
    indices.append((0, i, 1))
    outline = list(range(divisions+1)[1:]) + [1]
    return _ext.Mesh2D(points, indices=indices, outline_indices=[outline], point_meta_data=point_meta_data)

def arc2d(rect:_ext.Rect, thickness:float, start:float=0, end:float=360, divisions:int=32) ->_ext.Mesh2D:
    """ Generate an arc inside a rect
    
    Args:
        rect(Rect)
        thickness(float)
        start(float): angle in degrees
        end(float): angle in degrees
        divisions(int)
    
    Returns:
        Mesh
    """
    center = rect.center()
    radius = rect.width / 2.0
    inner_radius = radius - thickness
    increment = _ext.math.radians((end-start) / divisions)
    points = []
    indices = []
    point_meta_data = []
    
    for i in range(divisions+1):
        angle = _ext.math.radians(start) + i * increment
        inner_x = center[0] + inner_radius * _ext.math.cos(angle)
        inner_y = center[1] + inner_radius * _ext.math.sin(angle)
        outer_x = center[0] + radius * _ext.math.cos(angle)
        outer_y = center[1] + radius * _ext.math.sin(angle)
        
        points += [
            _ext.types.as_vector2f((inner_x, inner_y)),
            _ext.types.as_vector2f((outer_x, outer_y))
        ]
        point_meta_data += [
            {"angle": angle, "inner": True, "radius": inner_radius},
            {"angle": angle, "inner": False, "radius": radius},
        ]
        
        if i > 0:
            idx = i * 2
            indices += [
                (idx-2, idx-1, idx),
                (idx-1, idx, idx + 1),
            ]
    
    outline = [i*2 for i in range(divisions+1)]
    outline += [i*2 + 1 for i in reversed(range(divisions+1))] + [0]
    return _ext.Mesh2D(points, indices=indices, outline_indices=[outline], point_meta_data=point_meta_data)



def arrow2d(rect:_ext.Rect, head_length:float=0, head_width:float=0, tail_width:float=0, heads:int=1):
    """ Generate an arrow with multiple heads
    to set a direction, rotate the mesh
    
    Args:
        rect(Rect)
        head_length(float): length of the arrow head
        head_width(float): width of the arrow head
        tail_width(float): width of the arrow tail
        heads(int): option in 1, 2, 4
    
    Returns:
        Mesh
    """
    if heads not in (1, 2, 4):
        raise ValueError("arrow2d only supports 1, 2 or 4 heads")
    if head_length <= 0:
        if heads == 1:
            head_length = rect.width / 2.0
        else:
            head_length = rect.width / 4.0
    
    if tail_width <= 0:
        if heads == 1:
            tail_width = rect.height / 4.0
        else:
            tail_width = rect.height / 6.0
    
    if head_width <= 0:
        head_width = head_length * 2.0
        
    half_tail_width = tail_width / 2.0
    head_offset = (head_width / 2.0) - half_tail_width
    center = rect.center()
    left = _ext.types.as_vector2f((rect.left(), center[1]))
    right = _ext.types.as_vector2f((rect.right(), center[1]))
    if heads == 1:
        tracer = PointTracer2d()
        
        points = [
            # handle
            tracer.move_to(left - _ext.types.as_vector2f((0, half_tail_width))),
            tracer.move_by((0, tail_width)),
            tracer.move_to(right - _ext.types.as_vector2f((head_length, -half_tail_width))),
            # arrow
            tracer.move_by((0, head_offset)),
            tracer.move_to(right),
            tracer.move_by((-head_length, -(head_offset+half_tail_width))),
            tracer.move_by((0, head_offset)),
        ]
        indices = [
            # handle
            (0, 1, 2),
            (0, 2, 6),
            # arrow
            (2, 3, 4),
            (2, 4, 6),
            (6, 4, 5)
        ]
    elif heads == 2:
        tracer = PointTracer2d()
        
        points = [
            # left arrow top
            tracer.move_to(left),
            tracer.move_by((head_length, head_width/2.0)),
            tracer.move_by((0, -head_offset)),
            # right arrow
            tracer.move_to(right - _ext.types.as_vector2f((head_length, -half_tail_width))),
            tracer.move_by((0, head_offset)),
            tracer.move_to(right),
            tracer.move_by((-head_length, -(head_offset+half_tail_width))),
            tracer.move_by((0, head_offset)),
            # left arrow bottom
            tracer.move_to(left+_ext.types.as_vector2f((head_length, -half_tail_width))),
            tracer.move_by((0, -head_offset)),
        ]
        indices = [
            # left_arrow
            (0, 1, 2),
            (0, 2, 8),
            (0, 8, 9),
            # handle
            (2, 3, 8),
            (8, 3, 7),
            # right_arrow
            (3, 4, 5),
            (3, 5, 7),
            (5, 6, 7),
        ]
        
    elif heads == 4:
        top = _ext.types.as_vector2f((center[0], rect.top()))
        bottom = _ext.types.as_vector2f((center[0], rect.bottom()))
        segment_length = (rect.width / 2.0) - head_length - half_tail_width
        
        tracer = PointTracer2d()
        
        points = [
            # left arrow top
            tracer.move_to(left),
            tracer.move_by((head_length, head_width/2.0)),
            tracer.move_by((0, -head_offset)),
            # center top left
            tracer.move_by((segment_length, 0)),
            # top arrow
            tracer.move_by((0, segment_length)),
            tracer.move_by((-head_offset, 0)),
            tracer.move_to(top),
            tracer.move_by((head_width/2.0, -head_length)),
            tracer.move_by((-head_offset, 0)),
            # center top right
            tracer.move_by((0, -segment_length)),
            # right arrow
            tracer.move_by((segment_length, 0)),
            tracer.move_by((0, head_offset)),
            tracer.move_to(right),
            tracer.move_by((-head_length, -head_width/2.0)),
            tracer.move_by((0, head_offset)),
            # center bottom right
            tracer.move_by((-segment_length, 0)),
            # bottom arrow
            tracer.move_by((0, -segment_length)),
            tracer.move_by((head_offset, 0)),
            tracer.move_to(bottom),
            tracer.move_by((-head_width/2.0, head_length)),
            tracer.move_by((head_offset, 0)),
            # center bottom left
            tracer.move_by((0, segment_length)),
            # left arrow bottom
            tracer.move_by((-segment_length, 0)),
            tracer.move_by((0, -head_offset))
            
        ]
        indices = [
            # left arrow
            (0, 1, 2),
            (0, 2, 22),
            (22, 23, 0),
            # left handle
            (2, 3, 22),
            (3, 21, 22),
            # center
            (3, 9, 15),
            (3, 15, 21),
            # top handle
            (3, 4, 8),
            (3, 8, 9),
            # top arrow
            (5, 6, 4),
            (4, 6, 8),
            (6, 7, 8),
            # right handle
            (9, 10, 14),
            (9, 14, 15),
            # right arrow
            (10, 11, 12),
            (10, 12, 14),
            (12, 13, 14),
            # bottom handle
            (15, 16, 20),
            (15, 20, 21),
            # bottom arrow
            (16, 17, 18),
            (16, 18, 20),
            (18, 19, 20)
        ]
    
    outline = list(range(len(points))) + [0]
    return _ext.Mesh2D(points, indices=indices, outline_indices=[outline])
    