# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
from __future__ import annotations
class _ext:
    """ External Dependencies """
    import numpy as np
    from typing import Union, List
    from met_viewport_utils.constants import Align
    from met_viewport_utils.shape.margins import Margins
    from met_viewport_utils.algorithm.meta import (
        typed_property,
        alias_property)
    from met_viewport_utils.algorithm import types


class Rect(object):
    """ 2D bounding box for drawing
    
    Args:
        position: 2d vector
        size: 2d vector
        align: Where is position relative in size, this is not stored
    """
    def __init__(self,
                 position:_ext.types.Vector2fCompat=None,
                 size:_ext.types.Vector2fCompat=None,
                 align:_ext.Align=_ext.Align.BottomLeft):
        if position is not None:
            self.position = _ext.types.as_vector2f(position)
        if size is not None:
            self.size = _ext.types.as_vector2f(size)
        # Alignment is not stored, just used for initial computation
        if align & _ext.Align.Right:
            self.position[0] -= self.size[0]
        elif align & _ext.Align.HCenter:
            self.position[0] -= self.size[0]/2.0
        elif align & _ext.Align.Left:
            pass # default
        
        if align & _ext.Align.Top:
            self.position[1] -= self.size[1]
        elif align & _ext.Align.VCenter:
            self.position[1] -= self.size[1]/2.0
        elif align & _ext.Align.Bottom:
            pass # default
    
    def is_approx(self, other:Rect, tol:float=1e-8)->bool:
        if not _ext.np.all(_ext.np.isclose(self.position, other.position, atol=tol)):
            return False
        if not _ext.np.all(_ext.np.isclose(self.size, other.size, atol=tol)):
            return False
        return True
    
    def __repr__(self):
        return f"{self.__class__.__name__}([{self.x}, {self.y}], [{self.width, self.height}]) at {hex(id(self))}"
    
    position = _ext.typed_property(_ext.types.Vector2f, default=[0, 0], converter=_ext.types.as_vector2f)
    size = _ext.typed_property(_ext.types.Vector2f, default=[0, 0], converter=_ext.types.as_vector2f)
    
    x = _ext.alias_property(position, index=0)
    y = _ext.alias_property(position, index=1)
    width = _ext.alias_property(size, index=0)
    height = _ext.alias_property(size, index=1)
    
    def left(self) ->float:
        """Left position of rect, same as self.x

        Returns:
            float
        """
        return self.position[0]

    def set_left(self, left:float, move:bool=False):
        """Set the left side of this box
        
        Args:
            left(float): value
            move(bool): optional, moves the rect instead of extending
        """
        if move:
            self.position[0] = left
        else:
            offset = self.position[0] - left
            self.position[0] = left
            self.size[0] = max(0, self.size[0] + offset)
    
    def right(self) ->float:
        """Right position of rect, same as self.x + self.width

        Returns:
            float
        """
        return self.position[0] + self.size[0]

    def set_right(self, right:float, move:bool=False):
        """Set the right side of this box
        
        Args:
            right(float): value
            move(bool): optional, moves the rect instead of extending
        """
        if move:
            self.position[0] = right - self.size[0]
        else:
            if self.position[0] > right:
                self.position[0] = right
                self.size[0] = 0
            else:
                self.size[0] = right - self.position[0]
    
    def top(self) ->float:
        """Top position of rect, same as self.y + self.height

        Returns:
            float
        """
        return self.position[1] + self.size[1]

    def set_top(self, top:float, move:bool=False):
        """Set the top side of this box
        
        Args:
            top(float): value
            move(bool): optional, moves the rect instead of extending
        """
        if move:
            self.position[1] = top - self.size[1]
        else:
            if self.position[1] > top:
                self.position[1] = top
                self.size[1] = 0
            else:
                self.size[1] = top - self.position[1]
    
    def bottom(self) ->float:
        """bottom position of rect, same as self.y

        Returns:
            float
        """
        return self.position[1]

    def set_bottom(self, bottom:float, move:bool=False):
        """Set the bottom side of this box
        
        Args:
            bottom(float): value
            move(bool): optional, moves the rect instead of extending
        """
        if move:
            self.position[1] = bottom
        else:
            offset = self.position[1] - bottom
            self.position[1] = bottom
            self.size.yx = max(0, self.size[1] + offset)
    
    def top_left(self) ->_ext.types.Vector2f:
        """topleft position of rect

        Returns:
            Vector
        """
        return _ext.types.as_vector2f((self.left(), self.top()))
    
    def set_top_left(self, top_left:_ext.types.Vector2fCompat, move:bool=False):
        """Set the topleft corner of this box
        
        Args:
            top_left(Vector): value
            move(bool): optional, moves the rect instead of extending
        """
        self.set_top(top_left[0], move=move)
        self.set_left(top_left[0], move=move)
    
    def top_right(self) ->_ext.types.Vector2f:
        """topright position of rect

        Returns:
            Vector
        """
        return _ext.types.as_vector2f((self.right(), self.top()))
    
    def set_top_right(self, top_right:_ext.types.Vector2fCompat, move:bool=False):
        """Set the top_right corner of this box
        
        Args:
            top_right(Vector): value
            move(bool): optional, moves the rect instead of extending
        """
        self.set_top(top_right[0], move=move)
        self.set_right(top_right[0], move=move)
    
    def bottom_left(self) ->_ext.types.Vector2f:
        """bottomleft position of rect

        Returns:
            Vector
        """
        return _ext.types.as_vector2f((self.left(), self.bottom()))
    
    def set_bottom_left(self, bottom_left:_ext.types.Vector2fCompat, move:bool=False):
        """Set the bottom_left corner of this box
        
        Args:
            bottom_left(Vector): value
            move(bool): optional, moves the rect instead of extending
        """
        self.set_bottom(bottom_left[0], move=move)
        self.set_left(bottom_left[0], move=move)
    
    def bottom_right(self) ->_ext.types.Vector2f:
        """bottomright position of rect

        Returns:
            Vector
        """
        return _ext.types.as_vector2f((self.right(), self.bottom()))
    
    def set_bottom_right(self, bottom_right:_ext.types.Vector2fCompat, move:bool=False):
        """Set the bottom_right corner of this box
        
        Args:
            bottom_right(Vector): value
            move(bool): optional, moves the rect instead of extending
        """
        self.set_bottom(bottom_right[0], move=move)
        self.set_right(bottom_right[0], move=move)
        
    def center(self) -> _ext.types.Vector2f:
        """center position of rect

        Returns:
            Vector
        """
        return self.position + (self.size / 2.0)
    
    def set_center(self, center:_ext.types.Vector2fCompat):
        """moves the center of this box
        
        Args:
            center(Vector): value
        """
        self.position = center - (self.size / 2.0)
    def point_at(self, pivot:_ext.Align) ->_ext.types.Vector2f:
        """Get a point at the requested pivot position
        
        Args:
            pivot(Align): flags to get point for
        
        Returns:
            Vector
        """
        point = self.position
        if pivot & _ext.Align.Right:
            point[0] += self.size[0]
        elif pivot & _ext.Align.HCenter:
            point[0] += self.size[0]/2.0
        elif pivot & _ext.Align.Left:
            pass # default
        
        if pivot & _ext.Align.Top:
            point[1] += self.size[1]
        elif pivot & _ext.Align.VCenter:
            point[1] += self.size[1]/2.0
        elif pivot & _ext.Align.Bottom:
            pass # default
        return point
    
    def is_valid(self) ->bool:
        """Check if this rect has a positive size
        
        Returns:
            bool
        """
        return self.size[0] > 0 and self.size[1] > 0
    
    def contains(self, other:_ext.Union[Rect, _ext.types.Vector2f]) ->bool:
        """Check if this rect contains another rect or vector
        if other is a rect, it will only check for partial not full intersection
        
        Args:
            other(Rect|Vector)
        
        Returns:
            bool
        """
        if isinstance(other, Rect):
            return self.intersect(other).is_valid()

        else:  # Assume _Vector for now until we have Region
            return (self.left() <= other[0] <= self.right()) and (self.bottom() <= other[1] <= self.top())
    
    def intersect(self, other:Rect) ->Rect:
        """Return the intersection of two rects
        
        Args:
            other(Rect)
        
        Returns:
            Rect
        """
        left = max(self.left(), other.left())
        right = min(self.right(), other.right())
        top = max(self.top(), other.top())
        bottom = min(self.bottom(), other.bottom())
        position = _ext.types.as_vector2f([left, bottom])
        size = _ext.types.as_vector2f([right-left, top-bottom])
        return Rect(position, size)
    
    def copy(self) -> Rect:
        """Copy this rect
        
        Returns:
            Rect
        """
        return Rect(self.position, self.size)
    
    def adjust(self, margins:_ext.Union[_ext.Margins,_ext.List[float]]):
        """adjust this rect by the specified margins
        
        Args:
            margins(Margins|List[float])
        """
        if not isinstance(margins, _ext.Margins):
            margins = _ext.Margins(*margins)
        offset = _ext.types.as_vector2f((margins.left, margins.bottom))
        self.position = self.position + offset
        self.size = self.size - (_ext.types.as_vector2f((margins.right, margins.top)) + offset)
    
    def adjusted(self, margins:_ext.Union[_ext.Margins,_ext.List[float]]) ->Rect:
        """return a copy of this rect adjusted to these margins
        
        Args:
            margins(Margins|List[float])
        """
        if not isinstance(margins, _ext.Margins):
            margins = _ext.Margins(*margins)
        rect = self.copy()
        rect.adjust(margins)
        return rect
        