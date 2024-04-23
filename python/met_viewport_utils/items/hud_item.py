# copyright (c) 2024 Alex Telford, http://minimaleffort.tech
class _ext:
    """ External Dependencies """
    import copy
    from typing import overload
    from met_viewport_utils.constants import Align
    from .point_item import PointItem
    from met_viewport_utils.shape.rect import Rect
    from met_viewport_utils.shape.margins import Margins
    from met_viewport_utils.interfaces import IViewport
    from met_viewport_utils.algorithm.meta import typed_property
    from met_viewport_utils.algorithm import types


class HudItem(_ext.PointItem):
    """2D HUD Item"""
    def __init__(self):
        super().__init__()
        self.is2d = True
            
    # Properties to be set
    align:_ext.Align = _ext.typed_property(_ext.Align, default=_ext.Align.Center)
    margins:_ext.Margins = _ext.typed_property(_ext.Margins, default=_ext.Margins())
    size:_ext.types.Vector2f = _ext.typed_property(_ext.types.Vector2f, default=[0, 0], converter=_ext.types.as_vector2f)
    
    def local_rect(self)->_ext.Rect:
        return _ext.Rect(self.position, self.size, self.align)
    
    def screen_rect(self, viewport:_ext.IViewport)->_ext.Rect:
        return self.global_rect()
    
    # TODO: rotation
    def global_position(self)->_ext.types.Vector3f:
        # Map relative to root
        try:
            parent:_ext.PointItem = next(self.iter_parents(_ext.PointItem))
        except StopIteration:
            return _ext.copy.copy(self.position)
        
        if self.is2d != parent.is2d:
            # Cannot parent a 2d item to 3d or vice versa, stop here to prevent overflow
            return _ext.copy.copy(self.position)
        
        if isinstance(parent, HudItem):
            rect = parent.global_rect().adjusted(parent.margins)
            return _ext.types.as_vector3f(rect.point_at(self.align)) + self.position
        else:
            return parent.global_position() + self.position
    
    def global_rect(self)->_ext.Rect:
        # Map relative to root
        
        return _ext.Rect(
            _ext.types.as_vector2f(self.global_position()),
            self.size)
    
    def parent_rect(self)->_ext.Rect:
        # Immediate parent rect
        try:
            parent:HudItem = next(self.iter_parents(HudItem))
        except StopIteration:
            return self.local_rect()
        
        parent_rect = parent.local_rect()
        if parent.margins:
            parent_rect.adjust(parent.margins)
        return parent_rect
    
    @_ext.overload
    def map_from_global(self, value:_ext.Rect)->_ext.Rect: pass
    @_ext.overload
    def map_from_global(self, value:_ext.types.Vector2f)->_ext.types.Vector2f: pass
    def map_from_global(self, value):
        if not isinstance(value, _ext.Rect):
            local_rect = self.local_rect()
            rect = self.map_from_global(local_rect)
            return rect.position + _ext.types.as_vector2f(value)
        try:
            parent = next(self.iter_parents(HudItem))
        except StopIteration:
            return value

        this_position = self.global_rect().position
        
        if not isinstance(value, _ext.Rect):
            return local_rect.position + (_ext.types.as_vector2f(value)-this_position)
        
        return _ext.Rect(self.local_rect().position + (value.position-this_position), value.size)
    
    @_ext.overload
    def map_to_global(self, value:_ext.Rect)->_ext.Rect: pass
    @_ext.overload
    def map_to_global(self, value:_ext.types.Vector2f)->_ext.types.Vector2f: pass
    def map_to_global(self, value):
        try:
            parent:HudItem = next(self.iter_parents(HudItem))
        except StopIteration:
            return value

        parent_rect:_ext.Rect = parent.global_rect()
        if parent.margins:
            parent_rect.adjust(parent.margins)
        pivot = parent_rect.point_at(self.align)
        local_rect = self.local_rect()
        self_rect = _ext.Rect(pivot + local_rect.position, local_rect.size, self.align)
        
        if not isinstance(value, _ext.Rect):
            return self_rect.position + _ext.types.as_vector2f(value)
        
        return _ext.Rect(pivot + value.position, value.size, self.align)
